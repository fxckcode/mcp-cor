"""
Project COR MCP tools — Resource Allocations.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_get_allocations_by_project(project_id: int | str) -> str:
    """Get resource allocations for a project.

    Args:
        project_id: The project ID
    """
    client = get_client()
    data = await client.get(
        "/resource-allocations",
        params={"project_id": project_id},
    )
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_save_allocation(data: dict[str, Any]) -> str:
    """Create or update a resource allocation.

    Args:
        data: Allocation data (projectId, userId, allocationPercentage, startDate, endDate, etc.)
    """
    client = get_client()
    result = await client.post("/resource-allocations", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_delete_allocation(allocation_id: int | str) -> str:
    """Delete a resource allocation.

    Args:
        allocation_id: The allocation ID
    """
    client = get_client()
    await client.delete(f"/resource-allocations/{allocation_id}")
    return json.dumps(
        {"success": True, "message": f"Allocation {allocation_id} deleted."},
        indent=2,
    )
