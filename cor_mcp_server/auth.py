"""
OAuth 2.0 Client Credentials + User Credentials (email/password) authentication
for Project COR.

Manages token acquisition, caching, and auto-refresh with thread safety.

Supports two authentication modes:
    1. Client Credentials: COR_API_KEY + COR_CLIENT_SECRET (server-to-server)
    2. User Credentials: COR_EMAIL + COR_PASSWORD (testing / personal use)
"""

from __future__ import annotations

import base64
import logging
import os
import time
from threading import Lock
from typing import Any

import httpx

logger = logging.getLogger(__name__)

DEFAULT_API_URL = "https://api.projectcor.com/v1"
DEFAULT_TOKEN_URL = f"{DEFAULT_API_URL}/oauth/token?grant_type=client_credentials"
LOGIN_URL = f"{DEFAULT_API_URL}/auth/login"
TOKEN_REFRESH_MARGIN = 60  # seconds before expiry to trigger refresh


class AuthError(Exception):
    """Raised when authentication fails."""


class TokenStore:
    """Thread-safe token store with auto-refresh awareness."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._access_token: str | None = None
        self._expires_at: float = 0.0

    def set_token(self, access_token: str, expires_in: int) -> None:
        with self._lock:
            self._access_token = access_token
            self._expires_at = time.time() + expires_in

    def get_token(self) -> str | None:
        with self._lock:
            return self._access_token

    def is_expired(self) -> bool:
        with self._lock:
            return time.time() >= (self._expires_at - TOKEN_REFRESH_MARGIN)

    def clear(self) -> None:
        with self._lock:
            self._access_token = None
            self._expires_at = 0.0


class AuthManager:
    """Manages authentication for Project COR.

    Supports two modes:
      - Client Credentials (server-to-server):
          COR_API_KEY + COR_CLIENT_SECRET
      - User Credentials (email/password):
          COR_EMAIL + COR_PASSWORD

    Config via environment variables:
        COR_API_KEY: The API key (Client Credentials mode)
        COR_CLIENT_SECRET: The client secret (Client Credentials mode)
        COR_EMAIL: User email (User Credentials mode)
        COR_PASSWORD: User password (User Credentials mode)
        COR_API_URL: Base URL for the COR API (optional)
    """

    def __init__(
        self,
        api_key: str | None = None,
        client_secret: str | None = None,
        email: str | None = None,
        password: str | None = None,
        api_url: str | None = None,
    ) -> None:
        self._api_key = api_key or os.environ.get("COR_API_KEY", "")
        self._client_secret = client_secret or os.environ.get("COR_CLIENT_SECRET", "")
        self._email = email or os.environ.get("COR_EMAIL", "")
        self._password = password or os.environ.get("COR_PASSWORD", "")
        base_url = api_url or os.environ.get("COR_API_URL", DEFAULT_API_URL)
        self._base_url = base_url.rstrip("/")
        self._token_url = f"{self._base_url}/oauth/token?grant_type=client_credentials"
        self._login_url = f"{self._base_url}/auth/login"
        self._token_store = TokenStore()
        self._client: httpx.AsyncClient | None = None
        self._mode: str = self._detect_mode()

    def _detect_mode(self) -> str:
        """Auto-detect which auth mode to use based on available credentials."""
        if self._email and self._password:
            logger.info("Auth mode: User Credentials (email/password)")
            return "user_credentials"
        if self._api_key and self._client_secret:
            logger.info("Auth mode: Client Credentials (API key/secret)")
            return "client_credentials"
        logger.warning(
            "No COR credentials found. Set COR_EMAIL+COR_PASSWORD "
            "or COR_API_KEY+COR_CLIENT_SECRET."
        )
        return "none"

    def _get_basic_auth_header(self) -> str:
        """Create Basic auth header from API key and client secret."""
        credentials = f"{self._api_key}:{self._client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    async def _fetch_token(self) -> dict[str, Any]:
        """Acquire a new access token.

        Uses the detected auth mode:
          - client_credentials: OAuth Client Credentials grant
          - user_credentials: Login with email + password
        """
        if self._mode == "user_credentials":
            return await self._login()
        return await self._client_credentials_grant()

    async def _client_credentials_grant(self) -> dict[str, Any]:
        """OAuth 2.0 Client Credentials grant (API Key + Client Secret)."""
        headers = {
            "Authorization": self._get_basic_auth_header(),
            "Accept": "application/json",
        }
        async with httpx.AsyncClient() as client:
            logger.debug("Fetching token via client credentials from %s", self._token_url)
            response = await client.post(self._token_url, headers=headers)
            if response.status_code != 200:
                raise AuthError(
                    f"Token acquisition failed: HTTP {response.status_code} - {response.text}"
                )
            return response.json()

    async def _login(self) -> dict[str, Any]:
        """User Credentials login (email + password).

        POST to /v1/auth/login with form data.
        Returns a dict with access_token and expires_in.
        """
        if not self._email or not self._password:
            raise AuthError("COR_EMAIL and COR_PASSWORD must be set for user credentials auth")

        async with httpx.AsyncClient() as client:
            logger.debug("Authenticating user %s at %s", self._email, self._login_url)
            response = await client.post(
                self._login_url,
                data={"email": self._email, "password": self._password},
                headers={"Accept": "application/json"},
            )
            if response.status_code not in (200, 201):
                raise AuthError(
                    f"Login failed: HTTP {response.status_code} - {response.text}"
                )
            data = response.json()
            # Normalise the response shape to match what the rest of the code expects
            if "access_token" not in data:
                # Response shapes from COR /v1/auth/login:
                #   {"token": {"access_token": "jwt...", "type": "bearer",
                #              "refreshToken": "...", "expirationTime": "1234567890"}}
                #   or "token" could be the string directly
                token = data.get("token")
                if isinstance(token, dict):
                    data["access_token"] = token.get("access_token", "")
                    # expirationTime is a unix timestamp in ms
                    exp_ms = token.get("expirationTime")
                    if exp_ms:
                        exp_secs = int(exp_ms) // 1000
                        remaining = max(1, exp_secs - int(time.time()))
                        data["expires_in"] = remaining
                elif token:
                    data["access_token"] = token
                else:
                    tok = (data.get("data") or {}).get("token")
                    if tok:
                        data["access_token"] = tok
            return data

    async def get_access_token(self) -> str:
        """Return a valid access token, refreshing if necessary."""
        if not self._token_store.is_expired():
            token = self._token_store.get_token()
            if token:
                return token

        data = await self._fetch_token()
        access_token = data.get("access_token")
        expires_in = data.get("expires_in", 3600)

        if not access_token:
            raise AuthError("No access_token in token response")

        self._token_store.set_token(access_token, expires_in)
        logger.debug("Access token acquired/refreshed, expires in %ds", expires_in)
        return access_token

    async def close(self) -> None:
        """Clean up resources."""
        if self._client:
            await self._client.aclose()
            self._client = None
