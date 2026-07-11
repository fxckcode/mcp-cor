"""
FastMCP server for Project COR MCP.

Registers all tools from the tools package and manages the COR API client lifecycle.
Supports both stdio and SSE/HTTP transports.
"""

from __future__ import annotations

import logging
import os

from mcp.server.fastmcp import FastMCP

from .auth import AuthManager
from .client import CORClient
from .context import set_client

from .tools import projects as _projects
from .tools import tasks as _tasks
from .tools import time_tracking as _time_tracking
from .tools import clients as _clients
from .tools import contracts as _contracts
from .tools import messaging as _messaging
from .tools import team as _team
from .tools import labels as _labels
from .tools import ratecards as _ratecards
from .tools import allocations as _allocations
from .tools import products as _products

logger = logging.getLogger(__name__)


def create_server(
    api_key: str | None = None,
    client_secret: str | None = None,
    email: str | None = None,
    password: str | None = None,
    api_url: str | None = None,
) -> FastMCP:
    """Create and configure the COR MCP server.

    Args:
        api_key: COR API key (Client Credentials mode)
        client_secret: COR client secret (Client Credentials mode)
        email: COR user email (User Credentials mode)
        password: COR user password (User Credentials mode)
        api_url: COR API base URL (default: COR_API_URL env var)

    Returns:
        Configured FastMCP server instance
    """
    # Initialize auth and client
    auth = AuthManager(
        api_key=api_key,
        client_secret=client_secret,
        email=email,
        password=password,
        api_url=api_url,
    )
    base_url = api_url or os.environ.get("COR_API_URL", "https://api.projectcor.com/v1")
    client = CORClient(auth, base_url=base_url)
    set_client(client)

    # Create MCP server
    mcp = FastMCP(
        "COR MCP Server",
    )

    # ----- Projects -----
    mcp.tool(
        name="cor_list_projects",
        description=_projects.cor_list_projects.__doc__,
    )(_projects.cor_list_projects)

    mcp.tool(
        name="cor_get_project",
        description=_projects.cor_get_project.__doc__,
    )(_projects.cor_get_project)

    mcp.tool(
        name="cor_create_project",
        description=_projects.cor_create_project.__doc__,
    )(_projects.cor_create_project)

    mcp.tool(
        name="cor_update_project",
        description=_projects.cor_update_project.__doc__,
    )(_projects.cor_update_project)

    mcp.tool(
        name="cor_delete_project",
        description=_projects.cor_delete_project.__doc__,
    )(_projects.cor_delete_project)

    mcp.tool(
        name="cor_get_project_collaborators",
        description=_projects.cor_get_project_collaborators.__doc__,
    )(_projects.cor_get_project_collaborators)

    mcp.tool(
        name="cor_add_project_collaborator",
        description=_projects.cor_add_project_collaborator.__doc__,
    )(_projects.cor_add_project_collaborator)

    mcp.tool(
        name="cor_remove_project_collaborator",
        description=_projects.cor_remove_project_collaborator.__doc__,
    )(_projects.cor_remove_project_collaborator)

    mcp.tool(
        name="cor_get_project_costs",
        description=_projects.cor_get_project_costs.__doc__,
    )(_projects.cor_get_project_costs)

    mcp.tool(
        name="cor_add_project_cost",
        description=_projects.cor_add_project_cost.__doc__,
    )(_projects.cor_add_project_cost)

    mcp.tool(
        name="cor_get_project_labels",
        description=_projects.cor_get_project_labels.__doc__,
    )(_projects.cor_get_project_labels)

    mcp.tool(
        name="cor_get_project_ratecard",
        description=_projects.cor_get_project_ratecard.__doc__,
    )(_projects.cor_get_project_ratecard)

    mcp.tool(
        name="cor_get_project_templates",
        description=_projects.cor_get_project_templates.__doc__,
    )(_projects.cor_get_project_templates)

    mcp.tool(
        name="cor_get_project_profitability",
        description=_projects.cor_get_project_profitability.__doc__,
    )(_projects.cor_get_project_profitability)

    # ----- Tasks -----
    mcp.tool(
        name="cor_search_tasks",
        description=_tasks.cor_search_tasks.__doc__,
    )(_tasks.cor_search_tasks)

    mcp.tool(
        name="cor_get_my_pending_tasks",
        description=_tasks.cor_get_my_pending_tasks.__doc__,
    )(_tasks.cor_get_my_pending_tasks)

    mcp.tool(
        name="cor_get_task",
        description=_tasks.cor_get_task.__doc__,
    )(_tasks.cor_get_task)

    mcp.tool(
        name="cor_create_task",
        description=_tasks.cor_create_task.__doc__,
    )(_tasks.cor_create_task)

    mcp.tool(
        name="cor_update_task",
        description=_tasks.cor_update_task.__doc__,
    )(_tasks.cor_update_task)

    mcp.tool(
        name="cor_delete_task",
        description=_tasks.cor_delete_task.__doc__,
    )(_tasks.cor_delete_task)

    mcp.tool(
        name="cor_get_task_collaborators",
        description=_tasks.cor_get_task_collaborators.__doc__,
    )(_tasks.cor_get_task_collaborators)

    mcp.tool(
        name="cor_sync_task_collaborators",
        description=_tasks.cor_sync_task_collaborators.__doc__,
    )(_tasks.cor_sync_task_collaborators)

    mcp.tool(
        name="cor_add_task_label",
        description=_tasks.cor_add_task_label.__doc__,
    )(_tasks.cor_add_task_label)

    mcp.tool(
        name="cor_remove_task_label",
        description=_tasks.cor_remove_task_label.__doc__,
    )(_tasks.cor_remove_task_label)

    # ----- Time Tracking -----
    mcp.tool(
        name="cor_log_hours",
        description=_time_tracking.cor_log_hours.__doc__,
    )(_time_tracking.cor_log_hours)

    mcp.tool(
        name="cor_search_time_entries",
        description=_time_tracking.cor_search_time_entries.__doc__,
    )(_time_tracking.cor_search_time_entries)

    mcp.tool(
        name="cor_get_hours_by_date",
        description=_time_tracking.cor_get_hours_by_date.__doc__,
    )(_time_tracking.cor_get_hours_by_date)

    mcp.tool(
        name="cor_change_hours_status",
        description=_time_tracking.cor_change_hours_status.__doc__,
    )(_time_tracking.cor_change_hours_status)

    mcp.tool(
        name="cor_accept_suggested_hours",
        description=_time_tracking.cor_accept_suggested_hours.__doc__,
    )(_time_tracking.cor_accept_suggested_hours)

    # ----- Clients -----
    mcp.tool(
        name="cor_list_clients",
        description=_clients.cor_list_clients.__doc__,
    )(_clients.cor_list_clients)

    mcp.tool(
        name="cor_get_client",
        description=_clients.cor_get_client.__doc__,
    )(_clients.cor_get_client)

    mcp.tool(
        name="cor_create_client",
        description=_clients.cor_create_client.__doc__,
    )(_clients.cor_create_client)

    mcp.tool(
        name="cor_update_client",
        description=_clients.cor_update_client.__doc__,
    )(_clients.cor_update_client)

    mcp.tool(
        name="cor_delete_client",
        description=_clients.cor_delete_client.__doc__,
    )(_clients.cor_delete_client)

    mcp.tool(
        name="cor_get_client_fees",
        description=_clients.cor_get_client_fees.__doc__,
    )(_clients.cor_get_client_fees)

    # ----- Contracts -----
    mcp.tool(
        name="cor_list_contracts",
        description=_contracts.cor_list_contracts.__doc__,
    )(_contracts.cor_list_contracts)

    mcp.tool(
        name="cor_get_contract",
        description=_contracts.cor_get_contract.__doc__,
    )(_contracts.cor_get_contract)

    mcp.tool(
        name="cor_create_contract",
        description=_contracts.cor_create_contract.__doc__,
    )(_contracts.cor_create_contract)

    mcp.tool(
        name="cor_get_contract_positions",
        description=_contracts.cor_get_contract_positions.__doc__,
    )(_contracts.cor_get_contract_positions)

    mcp.tool(
        name="cor_create_contract_position",
        description=_contracts.cor_create_contract_position.__doc__,
    )(_contracts.cor_create_contract_position)

    # ----- Messaging -----
    mcp.tool(
        name="cor_get_task_messages",
        description=_messaging.cor_get_task_messages.__doc__,
    )(_messaging.cor_get_task_messages)

    mcp.tool(
        name="cor_post_task_message",
        description=_messaging.cor_post_task_message.__doc__,
    )(_messaging.cor_post_task_message)

    mcp.tool(
        name="cor_get_project_messages",
        description=_messaging.cor_get_project_messages.__doc__,
    )(_messaging.cor_get_project_messages)

    mcp.tool(
        name="cor_post_project_message",
        description=_messaging.cor_post_project_message.__doc__,
    )(_messaging.cor_post_project_message)

    # ----- Team & Users -----
    mcp.tool(
        name="cor_get_my_profile",
        description=_team.cor_get_my_profile.__doc__,
    )(_team.cor_get_my_profile)

    mcp.tool(
        name="cor_list_users",
        description=_team.cor_list_users.__doc__,
    )(_team.cor_list_users)

    mcp.tool(
        name="cor_get_user",
        description=_team.cor_get_user.__doc__,
    )(_team.cor_get_user)

    mcp.tool(
        name="cor_list_teams",
        description=_team.cor_list_teams.__doc__,
    )(_team.cor_list_teams)

    mcp.tool(
        name="cor_create_team",
        description=_team.cor_create_team.__doc__,
    )(_team.cor_create_team)

    mcp.tool(
        name="cor_add_team_users",
        description=_team.cor_add_team_users.__doc__,
    )(_team.cor_add_team_users)

    mcp.tool(
        name="cor_remove_team_users",
        description=_team.cor_remove_team_users.__doc__,
    )(_team.cor_remove_team_users)

    mcp.tool(
        name="cor_get_working_time",
        description=_team.cor_get_working_time.__doc__,
    )(_team.cor_get_working_time)

    # ----- Labels -----
    mcp.tool(
        name="cor_get_labels",
        description=_labels.cor_get_labels.__doc__,
    )(_labels.cor_get_labels)

    # ----- Ratecards -----
    mcp.tool(
        name="cor_list_ratecards",
        description=_ratecards.cor_list_ratecards.__doc__,
    )(_ratecards.cor_list_ratecards)

    mcp.tool(
        name="cor_get_ratecard",
        description=_ratecards.cor_get_ratecard.__doc__,
    )(_ratecards.cor_get_ratecard)

    mcp.tool(
        name="cor_create_ratecard",
        description=_ratecards.cor_create_ratecard.__doc__,
    )(_ratecards.cor_create_ratecard)

    # ----- Allocations -----
    mcp.tool(
        name="cor_get_allocations_by_project",
        description=_allocations.cor_get_allocations_by_project.__doc__,
    )(_allocations.cor_get_allocations_by_project)

    mcp.tool(
        name="cor_save_allocation",
        description=_allocations.cor_save_allocation.__doc__,
    )(_allocations.cor_save_allocation)

    mcp.tool(
        name="cor_delete_allocation",
        description=_allocations.cor_delete_allocation.__doc__,
    )(_allocations.cor_delete_allocation)

    # ----- Products -----
    mcp.tool(
        name="cor_list_products",
        description=_products.cor_list_products.__doc__,
    )(_products.cor_list_products)

    mcp.tool(
        name="cor_create_product",
        description=_products.cor_create_product.__doc__,
    )(_products.cor_create_product)

    logger.info(
        "COR MCP Server initialized with %d tools",
        len(mcp._tool_manager._tools) if hasattr(mcp, "_tool_manager") else "N/A",
    )
    return mcp


def run_server(mcp: FastMCP | None = None, transport: str | None = None) -> None:
    """Run the COR MCP server.

    Args:
        mcp: Pre-configured FastMCP server, or None to create one
        transport: Transport type: "stdio", "sse", or None for auto-detect
    """
    server = mcp or create_server()

    # Determine transport
    detected_transport = transport or os.environ.get("MCP_TRANSPORT", "stdio")
    if detected_transport not in ("stdio", "sse"):
        detected_transport = "stdio"

    logger.info(
        "Starting COR MCP Server (transport=%s)",
        detected_transport,
    )
    server.run(transport=detected_transport)
