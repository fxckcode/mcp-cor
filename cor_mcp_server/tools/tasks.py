"""
Project COR MCP tools — Tasks.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_search_tasks(filters: dict[str, Any] | None = None) -> str:
    """Search tasks with filters (projectId, clientId, status, text, dates, labels).

    Args:
        filters: Dict with filter fields like projectId, status, text, etc.
    """
    client = get_client()
    params = filters or {}
    data = await client.get("/tasks", params=params)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_my_pending_tasks() -> str:
    """Get my pending tasks."""
    client = get_client()
    data = await client.get("/tasks", params={"mine": True})
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_task(task_id: int | str) -> str:
    """Get a single task by ID.

    Args:
        task_id: The task ID
    """
    client = get_client()
    data = await client.get(f"/tasks/{task_id}")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_task(data: dict[str, Any]) -> str:
    """Create a new task.

    Args:
        data: Task data (title, projectId, description, deadline, priority, etc.)
    """
    client = get_client()
    result = await client.post("/tasks", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_update_task(task_id: int | str, data: dict[str, Any]) -> str:
    """Update an existing task (partial update).

    Args:
        task_id: The task ID
        data: Fields to update
    """
    client = get_client()
    result = await client.put(f"/tasks/{task_id}", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_delete_task(task_id: int | str) -> str:
    """Delete a task.

    Args:
        task_id: The task ID
    """
    client = get_client()
    await client.delete(f"/tasks/{task_id}")
    return json.dumps({"success": True, "message": f"Task {task_id} deleted."}, indent=2)


async def cor_get_task_collaborators(task_id: int | str) -> str:
    """Get collaborators for a task.

    Args:
        task_id: The task ID
    """
    client = get_client()
    data = await client.get(f"/tasks/{task_id}/collaborators")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_sync_task_collaborators(task_id: int | str, user_ids: list[int | str]) -> str:
    """Sync (replace) collaborators for a task.

    Args:
        task_id: The task ID
        user_ids: List of user IDs to set as collaborators
    """
    client = get_client()
    result = await client.put(f"/tasks/{task_id}/collaborators", data={"userIds": user_ids})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_add_task_label(task_id: int | str, label_id: int | str) -> str:
    """Add a label to a task.

    Args:
        task_id: The task ID
        label_id: The label ID to add
    """
    client = get_client()
    result = await client.post(f"/tasks/{task_id}/labels", data={"labelId": label_id})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_remove_task_label(task_id: int | str, label_id: int | str) -> str:
    """Remove a label from a task.

    Args:
        task_id: The task ID
        label_id: The label ID to remove
    """
    client = get_client()
    await client.delete(f"/tasks/{task_id}/labels/{label_id}")
    return json.dumps(
        {"success": True, "message": f"Label {label_id} removed from task {task_id}."},
        indent=2,
    )
