"""
Project COR MCP tools — Labels.
"""

from __future__ import annotations

import json

from ..context import get_client


async def cor_get_labels(entity_type: str = "") -> str:
    """Get labels, optionally filtered by entity type.

    Args:
        entity_type: Entity type filter - "project", "task", "user", or empty for all
    """
    client = get_client()
    params = {}
    if entity_type:
        params["entity"] = entity_type
    data = await client.get("/labels", params=params)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)
