"""
Async HTTP client for the Project COR API.

Handles authentication, request signing, pagination, and error wrapping.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from .auth import AuthManager, AuthError

logger = logging.getLogger(__name__)


class CORClientError(Exception):
    """Base exception for COR API client errors."""

    def __init__(self, message: str, status_code: int | None = None, body: Any = None) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(message)


class CORClient:
    """Async HTTP client for Project COR API.

    Automatically handles Bearer token auth via AuthManager.
    Supports pagination, error wrapping, and rate-limit awareness.
    """

    def __init__(self, auth: AuthManager, base_url: str | None = None) -> None:
        self._auth = auth
        self._base_url = (base_url or "").rstrip("/")
        self._client: httpx.AsyncClient | None = None
        self._lock_init = __import__("threading").Lock()
        self._http_client: httpx.AsyncClient | None = None

    async def _get_http_client(self) -> httpx.AsyncClient:
        """Get or create the shared httpx client."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=httpx.Timeout(30.0, connect=10.0),
                follow_redirects=True,
            )
        return self._http_client

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_body: Any = None,
    ) -> Any:
        """Make an authenticated request to the COR API."""
        token = await self._auth.get_access_token()
        client = await self._get_http_client()

        headers: dict[str, str] = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        if json_body is not None:
            headers["Content-Type"] = "application/json"

        url = path if path.startswith("http") else path

        try:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json_body,
                headers=headers,
            )
        except httpx.TimeoutException as e:
            raise CORClientError(f"Request timed out: {e}") from e
        except httpx.HTTPError as e:
            raise CORClientError(f"HTTP error: {e}") from e

        # Handle rate limiting
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "5")
            logger.warning("Rate limited. Retry after %s seconds.", retry_after)
            raise CORClientError(
                f"Rate limited. Retry after {retry_after}s.",
                status_code=429,
            )

        # Handle errors
        if response.status_code >= 400:
            try:
                body = response.json()
            except Exception:
                body = response.text
            raise CORClientError(
                f"API error: HTTP {response.status_code} - {response.text[:500]}",
                status_code=response.status_code,
                body=body,
            )

        # Return JSON for success responses
        if response.status_code == 204:
            return None

        try:
            return response.json()
        except Exception:
            return response.text

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Any:
        """GET request with optional pagination params."""
        if params is None:
            params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["perPage"] = per_page
        return await self._request("GET", path, params=params)

    async def post(self, path: str, data: dict[str, Any] | None = None) -> Any:
        """POST request with JSON body."""
        return await self._request("POST", path, json_body=data)

    async def put(self, path: str, data: dict[str, Any] | None = None) -> Any:
        """PUT request with JSON body."""
        return await self._request("PUT", path, json_body=data)

    async def delete(self, path: str) -> Any:
        """DELETE request."""
        return await self._request("DELETE", path)

    async def paginated_get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        page: int = 1,
        per_page: int = 20,
        max_pages: int = 100,
    ) -> list[Any]:
        """Fetch paginated results. Returns combined list from all pages up to max_pages."""
        all_items: list[Any] = []
        current_page = page

        while True:
            result = await self.get(
                path,
                params=params,
                page=current_page,
                per_page=per_page,
            )

            if isinstance(result, dict):
                items = result.get("data", result.get("items", result.get("results", [])))
                all_items.extend(items)

                # Check if there are more pages
                total_pages = result.get("totalPages", result.get("pages", current_page))
                if current_page >= total_pages or current_page >= max_pages:
                    break
            elif isinstance(result, list):
                all_items.extend(result)
                break
            else:
                all_items.append(result)
                break

            current_page += 1

        return all_items

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
