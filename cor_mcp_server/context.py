"""
Shared context for the COR MCP Server.

Provides a way for tool modules to access the shared CORClient instance
without circular imports.
"""

from __future__ import annotations

from .client import CORClient

_client: CORClient | None = None


def set_client(client: CORClient) -> None:
    """Set the global CORClient instance."""
    global _client  # noqa: PLW0603
    _client = client


def get_client() -> CORClient:
    """Get the global CORClient instance."""
    if _client is None:
        msg = "CORClient not initialized. Call set_client() first."
        raise RuntimeError(msg)
    return _client


def get_or_create_client(auth=None, base_url: str | None = None) -> CORClient:
    """Get existing client or create a new one."""
    global _client  # noqa: PLW0603
    if _client is None:
        if auth is None:
            from .auth import AuthManager
            auth = AuthManager()
        _client = CORClient(auth, base_url=base_url)
    return _client
