"""
Project COR MCP tools — Projects.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_list_projects(
    page: int = 1,
    per_page: int = 20,
    filters: dict[str, Any] | None = None,
) -> str:
    """List projects with optional filters (clientId, status, health, dates).

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
        filters: Optional dict with filter fields
    """
    client = get_client()
    params = filters or {}
    data = await client.get("/projects", params=params, page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_project(project_id: int | str) -> str:
    """Get a single project by ID.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(f"/projects/{project_id}")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_project(data: dict[str, Any]) -> str:
    """Create a new project.

    Args:
        data: Project data (name, clientId, description, startDate, endDate, status, etc.)
    """
    client = get_client()
    result = await client.post("/projects", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_update_project(project_id: int | str, data: dict[str, Any]) -> str:
    """Update an existing project (partial update).

    Args:
        project_id: The project ID
        data: Fields to update
    """
    client = get_client()
    result = await client.put(f"/projects/{project_id}", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_delete_project(project_id: int | str) -> str:
    """Delete a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    await client.delete(f"/projects/{project_id}")
    return json.dumps({"success": True, "message": f"Project {project_id} deleted."}, indent=2)


async def cor_get_project_collaborators(project_id: int | str) -> str:
    """Get collaborators for a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(f"/projects/{project_id}/collaborators")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_add_project_collaborator(project_id: int | str, user_id: int | str) -> str:
    """Add a collaborator to a project.

    Args:
        project_id: The project ID
        user_id: The user ID to add
    """
    client = get_client()
    result = await client.post(
        f"/projects/{project_id}/collaborators", data={"userId": user_id}
    )
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_remove_project_collaborator(project_id: int | str, user_id: int | str) -> str:
    """Remove a collaborator from a project.

    Args:
        project_id: The project ID
        user_id: The user ID to remove
    """
    client = get_client()
    await client.delete(f"/projects/{project_id}/collaborators/{user_id}")
    return json.dumps(
        {"success": True, "message": f"Collaborator {user_id} removed from project {project_id}."},
        indent=2,
    )


async def cor_get_project_costs(project_id: int | str) -> str:
    """Get costs/estimates for a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(f"/projects/{project_id}/costs")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_add_project_cost(project_id: int | str, data: dict[str, Any]) -> str:
    """Add a cost entry to a project.

    Args:
        project_id: The project ID
        data: Cost data (description, amount, date, etc.)
    """
    client = get_client()
    result = await client.post(f"/projects/{project_id}/costs", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_get_project_labels(project_id: int | str) -> str:
    """Get labels assigned to a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(f"/projects/{project_id}/labels")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_project_ratecard(project_id: int | str) -> str:
    """Get the ratecard assigned to a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(f"/projects/{project_id}/ratecard")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_project_templates(page: int = 1, per_page: int = 20) -> str:
    """Get available project templates.

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    client = get_client()
    data = await client.get("/projects/templates", page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_project_profitability(project_id: int | str) -> str:
    """Get profitability data for a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(f"/projects/{project_id}/profitability")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)
