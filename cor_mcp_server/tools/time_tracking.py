"""
Project COR MCP tools — Time Tracking.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_log_hours(task_id: int | str, data: dict[str, Any]) -> str:
    """Log hours against a task.

    Args:
        task_id: The task ID to log hours against
        data: Time entry data (hours, date, notes, etc.)
    """
    client = get_client()
    result = await client.post("/hours", data={"taskId": task_id, **data})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_search_time_entries(filters: dict[str, Any] | None = None) -> str:
    """Search time entries with filters (userId, projectId, dates, status).

    Args:
        filters: Dict with filter fields
    """
    client = get_client()
    params = filters or {}
    data = await client.get("/hours", params=params)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_hours_by_date(datetime_unix: int) -> str:
    """Get time entries for a specific date.

    Args:
        datetime_unix: Unix timestamp for the date
    """
    client = get_client()
    data = await client.get(f"/hours/date/{datetime_unix}")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_change_hours_status(hours_id: int | str, status: str) -> str:
    """Change the status of a time entry.

    Args:
        hours_id: The time entry ID
        status: New status (e.g. "approved", "rejected", "pending")
    """
    client = get_client()
    result = await client.put(f"/hours/{hours_id}/status", data={"status": status})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_accept_suggested_hours(datetime_unix: int) -> str:
    """Accept suggested hours for a given date.

    Args:
        datetime_unix: Unix timestamp for the date
    """
    client = get_client()
    result = await client.post("/hours/accept-suggested", data={"date": datetime_unix})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)
