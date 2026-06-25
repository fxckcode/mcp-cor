"""
Project COR MCP tools — Team & Users.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_get_my_profile() -> str:
    """Get the current user's profile."""
    client = get_client()
    data = await client.get("/me")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_list_users(
    page: int = 1,
    per_page: int = 20,
    filters: dict[str, Any] | None = None,
) -> str:
    """List users with optional filters.

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
        filters: Optional dict with filter fields
    """
    client = get_client()
    params = filters or {}
    data = await client.get("/users", params=params, page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_user(user_id: int | str) -> str:
    """Get a single user by ID.

    Args:
        user_id: The user ID
    """
    client = get_client()
    data = await client.get(f"/users/{user_id}")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_list_teams(page: int = 1, per_page: int = 20) -> str:
    """List teams.

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    client = get_client()
    data = await client.get("/teams", page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_team(data: dict[str, Any]) -> str:
    """Create a new team.

    Args:
        data: Team data (name, description, etc.)
    """
    client = get_client()
    result = await client.post("/teams", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_add_team_users(team_id: int | str, user_ids: list[int | str]) -> str:
    """Add users to a team.

    Args:
        team_id: The team ID
        user_ids: List of user IDs to add
    """
    client = get_client()
    result = await client.post(f"/teams/{team_id}/users", data={"userIds": user_ids})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_remove_team_users(team_id: int | str, user_ids: list[int | str]) -> str:
    """Remove users from a team.

    Args:
        team_id: The team ID
        user_ids: List of user IDs to remove
    """
    client = get_client()
    result = await client.delete(f"/teams/{team_id}/users", data={"userIds": user_ids})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_get_working_time() -> str:
    """Get working time for users."""
    client = get_client()
    data = await client.get("/working-time/users")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)
