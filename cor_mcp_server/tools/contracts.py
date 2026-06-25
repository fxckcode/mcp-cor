"""
Project COR MCP tools — Contracts.
"""

from __future__ import annotations

import json
from typing import Any

from ..context import get_client


async def cor_list_contracts(page: int = 1, per_page: int = 20) -> str:
    """List contracts.

    Args:
        page: Page number (default: 1)
        per_page: Results per page (default: 20)
    """
    client = get_client()
    data = await client.get("/contracts", page=page, per_page=per_page)
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_get_contract(contract_id: int | str) -> str:
    """Get a single contract by ID.

    Args:
        contract_id: The contract ID
    """
    client = get_client()
    data = await client.get(f"/contracts/{contract_id}")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_contract(data: dict[str, Any]) -> str:
    """Create a new contract.

    Args:
        data: Contract data (name, clientId, startDate, endDate, value, status, etc.)
    """
    client = get_client()
    result = await client.post("/contracts", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)


async def cor_get_contract_positions(contract_id: int | str) -> str:
    """Get positions for a contract.

    Args:
        contract_id: The contract ID
    """
    client = get_client()
    data = await client.get(f"/contracts/{contract_id}/positions")
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


async def cor_create_contract_position(contract_id: int | str, data: dict[str, Any]) -> str:
    """Create a position in a contract.

    Args:
        contract_id: The contract ID
        data: Position data (title, rate, hours, etc.)
    """
    client = get_client()
    result = await client.post(f"/contracts/{contract_id}/positions", data=data)
    return json.dumps(result, indent=2, ensure_ascii=False, default=str)
