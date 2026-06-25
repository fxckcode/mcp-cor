"""
Project COR MCP tools — Products.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_list_products(page: int = 1, per_page: int = 20) -> str:
    """List products.

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    client = get_client()
    data = await client.get("/products", page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_product(data: dict[str, Any]) -> str:
    """Create a new product.

    Args:
        data: Product data (name, description, rate, etc.)
    """
    client = get_client()
    result = await client.post("/products", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)
