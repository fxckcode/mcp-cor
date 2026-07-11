"""
Project COR MCP tools — Messaging.
"""

from __future__ import annotations

import json

from ..context import get_client


async def cor_get_task_messages(task_id: int | str) -> str:
    """Get messages for a task.

    Args:
        task_id: The task ID
    """
    client = get_client()
    data = await client.get(f"/tasks/{task_id}/messages")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_post_task_message(task_id: int | str, content: str) -> str:
    """Post a message on a task (with optional @mentions in content).

    Args:
        task_id: The task ID
        content: Message content text
    """
    client = get_client()
    result = await client.post(f"/tasks/{task_id}/messages", data={"content": content})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_get_project_messages(project_id: int | str) -> str:
    """Get messages for a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(f"/projects/{project_id}/messages")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_post_project_message(project_id: int | str, content: str) -> str:
    """Post a message on a project (with optional @mentions in content).

    Args:
        project_id: The project ID
        content: Message content text
    """
    client = get_client()
    result = await client.post(f"/projects/{project_id}/messages", data={"content": content})
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)
