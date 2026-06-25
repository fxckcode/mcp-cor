"""
Project COR MCP tools — Ratecards.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_list_ratecards(page: int = 1, per_page: int = 20) -> str:
    """List ratecards.

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    client = get_client()
    data = await client.get("/ratecards", page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_ratecard(ratecard_id: int | str) -> str:
    """Get a single ratecard by ID.

    Args:
        ratecard_id: The ratecard ID
    """
    client = get_client()
    data = await client.get(f"/ratecards/{ratecard_id}")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_ratecard(data: dict[str, Any]) -> str:
    """Create a new ratecard.

    Args:
        data: Ratecard data (name, description, rates, etc.)
    """
    client = get_client()
    result = await client.post("/ratecards", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)
