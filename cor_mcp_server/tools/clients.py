"""
Project COR MCP tools — Clients.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_list_clients(page: int = 1, per_page: int = 20) -> str:
    """List clients.

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    client = get_client()
    data = await client.get("/clients", page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_client(client_id: int | str) -> str:
    """Get a single client by ID.

    Args:
        client_id: The client ID
    """
    client = get_client()
    data = await client.get(f"/clients/{client_id}")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_client(data: dict[str, Any]) -> str:
    """Create a new client.

    Args:
        data: Client data (name, email, phone, notes, etc.)
    """
    client = get_client()
    result = await client.post("/clients", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_update_client(client_id: int | str, data: dict[str, Any]) -> str:
    """Update an existing client.

    Args:
        client_id: The client ID
        data: Fields to update
    """
    client = get_client()
    result = await client.put(f"/clients/{client_id}", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_delete_client(client_id: int | str) -> str:
    """Delete a client.

    Args:
        client_id: The client ID
    """
    client = get_client()
    await client.delete(f"/clients/{client_id}")
    return json.dumps({"success": True, "message": f"Client {client_id} deleted."}, indent=2)


async def cor_get_client_fees(client_id: int | str) -> str:
    """Get fees for a client.

    Args:
        client_id: The client ID
    """
    client = get_client()
    data = await client.get(f"/clients/{client_id}/fees")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)
