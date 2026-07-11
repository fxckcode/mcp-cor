"""Tests for the COR MCP server tools and client."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cor_mcp_server.auth import AuthManager, TokenStore
from cor_mcp_server.client import CORClient


class TestTokenStore:
    """Tests for the thread-safe token store."""

    def test_set_and_get(self):
        store = TokenStore()
        store.set_token("test-token", 3600)
        assert store.get_token() == "test-token"

    def test_expired(self):
        store = TokenStore()
        store.set_token("test-token", 0)  # expires immediately
        assert store.is_expired() is True

    def test_not_expired(self):
        store = TokenStore()
        store.set_token("test-token", 3600)
        assert store.is_expired() is False

    def test_clear(self):
        store = TokenStore()
        store.set_token("test-token", 3600)
        store.clear()
        assert store.get_token() is None
        assert store.is_expired() is True


class TestCORClient:
    """Tests for the COR API client."""

    @pytest.fixture
    def auth(self):
        mock = MagicMock(spec=AuthManager)
        mock.get_access_token = AsyncMock(return_value="test-bearer-token")
        return mock

    @pytest.fixture
    def client(self, auth):
        return CORClient(auth, base_url="https://api.projectcor.com/v1")

    @pytest.mark.asyncio
    async def test_get_success(self, client):
        """Test successful GET request."""
        with patch.object(client, "_request", new=AsyncMock()) as mock_request:
            mock_request.return_value = {"data": [{"id": 1, "name": "Test"}]}
            result = await client.get("/projects")
            assert result["data"][0]["id"] == 1
            mock_request.assert_called_once_with("GET", "/projects", params={})

    @pytest.mark.asyncio
    async def test_get_with_pagination(self, client):
        """Test GET request with pagination params."""
        with patch.object(client, "_request", new=AsyncMock()) as mock_request:
            mock_request.return_value = {"data": []}
            await client.get("/projects", page=2, per_page=50)
            mock_request.assert_called_once_with(
                "GET", "/projects", params={"page": 2, "perPage": 50}
            )

    @pytest.mark.asyncio
    async def test_post(self, client):
        """Test POST request with data."""
        with patch.object(client, "_request", new=AsyncMock()) as mock_request:
            mock_request.return_value = {"id": 1, "name": "New Project"}
            result = await client.post("/projects", data={"name": "New Project"})
            assert result["id"] == 1
            mock_request.assert_called_once_with(
                "POST", "/projects", json_body={"name": "New Project"}
            )

    @pytest.mark.asyncio
    async def test_put(self, client):
        """Test PUT request."""
        with patch.object(client, "_request", new=AsyncMock()) as mock_request:
            mock_request.return_value = {"id": 1, "name": "Updated"}
            result = await client.put("/projects/1", data={"name": "Updated"})
            assert result["name"] == "Updated"

    @pytest.mark.asyncio
    async def test_delete(self, client):
        """Test DELETE request."""
        with patch.object(client, "_request", new=AsyncMock()) as mock_request:
            mock_request.return_value = None
            result = await client.delete("/projects/1")
            assert result is None

    @pytest.mark.asyncio
    async def test_paginated_get(self, client):
        """Test paginated get helper."""
        with patch.object(client, "get", new=AsyncMock()) as mock_get:
            mock_get.side_effect = [
                {"data": [{"id": 1}], "totalPages": 2},
                {"data": [{"id": 2}], "totalPages": 2},
            ]
            result = await client.paginated_get("/projects", per_page=1)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 2

    @pytest.mark.asyncio
    async def test_auto_auth_header(self, client):
        """Test that Authorization header is set."""
        with patch.object(client, "_get_http_client", new=AsyncMock()) as mock_get_client:
            mock_httpx = AsyncMock()
            mock_httpx.request = AsyncMock()
            mock_httpx.request.return_value = MagicMock(
                status_code=200,
                json=lambda: {"data": []},
            )
            mock_get_client.return_value = mock_httpx

            await client.get("/projects")

            # Verify the request was made with proper auth
            call_kwargs = mock_httpx.request.call_args[1]
            assert "Authorization" in call_kwargs["headers"]
            assert call_kwargs["headers"]["Authorization"] == "Bearer test-bearer-token"


class TestToolFunctions:
    """Tests for tool function imports and signatures."""

    def test_import_projects(self):
        from cor_mcp_server.tools import projects
        assert hasattr(projects, "cor_list_projects")
        assert hasattr(projects, "cor_get_project")
        assert hasattr(projects, "cor_create_project")
        assert hasattr(projects, "cor_update_project")
        assert hasattr(projects, "cor_delete_project")
        assert hasattr(projects, "cor_get_project_collaborators")
        assert hasattr(projects, "cor_add_project_collaborator")
        assert hasattr(projects, "cor_remove_project_collaborator")
        assert hasattr(projects, "cor_get_project_costs")
        assert hasattr(projects, "cor_add_project_cost")
        assert hasattr(projects, "cor_get_project_labels")
        assert hasattr(projects, "cor_get_project_ratecard")
        assert hasattr(projects, "cor_get_project_templates")
        assert hasattr(projects, "cor_get_project_profitability")

    def test_import_tasks(self):
        from cor_mcp_server.tools import tasks
        assert hasattr(tasks, "cor_search_tasks")
        assert hasattr(tasks, "cor_get_my_pending_tasks")
        assert hasattr(tasks, "cor_get_task")
        assert hasattr(tasks, "cor_create_task")
        assert hasattr(tasks, "cor_update_task")
        assert hasattr(tasks, "cor_delete_task")
        assert hasattr(tasks, "cor_get_task_collaborators")
        assert hasattr(tasks, "cor_sync_task_collaborators")
        assert hasattr(tasks, "cor_add_task_label")
        assert hasattr(tasks, "cor_remove_task_label")

    def test_import_time_tracking(self):
        from cor_mcp_server.tools import time_tracking
        assert hasattr(time_tracking, "cor_log_hours")
        assert hasattr(time_tracking, "cor_search_time_entries")
        assert hasattr(time_tracking, "cor_get_hours_by_date")
        assert hasattr(time_tracking, "cor_change_hours_status")
        assert hasattr(time_tracking, "cor_accept_suggested_hours")

    def test_import_clients(self):
        from cor_mcp_server.tools import clients
        assert hasattr(clients, "cor_list_clients")
        assert hasattr(clients, "cor_get_client")
        assert hasattr(clients, "cor_create_client")
        assert hasattr(clients, "cor_update_client")
        assert hasattr(clients, "cor_delete_client")
        assert hasattr(clients, "cor_get_client_fees")

    def test_import_contracts(self):
        from cor_mcp_server.tools import contracts
        assert hasattr(contracts, "cor_list_contracts")
        assert hasattr(contracts, "cor_get_contract")
        assert hasattr(contracts, "cor_create_contract")
        assert hasattr(contracts, "cor_get_contract_positions")
        assert hasattr(contracts, "cor_create_contract_position")

    def test_import_messaging(self):
        from cor_mcp_server.tools import messaging
        assert hasattr(messaging, "cor_get_task_messages")
        assert hasattr(messaging, "cor_post_task_message")
        assert hasattr(messaging, "cor_get_project_messages")
        assert hasattr(messaging, "cor_post_project_message")

    def test_import_team(self):
        from cor_mcp_server.tools import team
        assert hasattr(team, "cor_get_my_profile")
        assert hasattr(team, "cor_list_users")
        assert hasattr(team, "cor_get_user")
        assert hasattr(team, "cor_list_teams")
        assert hasattr(team, "cor_create_team")
        assert hasattr(team, "cor_add_team_users")
        assert hasattr(team, "cor_remove_team_users")
        assert hasattr(team, "cor_get_working_time")

    def test_import_labels(self):
        from cor_mcp_server.tools import labels
        assert hasattr(labels, "cor_get_labels")

    def test_import_ratecards(self):
        from cor_mcp_server.tools import ratecards
        assert hasattr(ratecards, "cor_list_ratecards")
        assert hasattr(ratecards, "cor_get_ratecard")
        assert hasattr(ratecards, "cor_create_ratecard")

    def test_import_allocations(self):
        from cor_mcp_server.tools import allocations
        assert hasattr(allocations, "cor_get_allocations_by_project")
        assert hasattr(allocations, "cor_save_allocation")
        assert hasattr(allocations, "cor_delete_allocation")

    def test_import_products(self):
        from cor_mcp_server.tools import products
        assert hasattr(products, "cor_list_products")
        assert hasattr(products, "cor_create_product")

    def test_tool_count(self):
        """Count all tool functions."""
        from cor_mcp_server.tools import (
            projects, tasks, time_tracking, clients, contracts,
            messaging, team, labels, ratecards, allocations, products,
        )

        count = 0
        for module in [
            projects, tasks, time_tracking, clients, contracts,
            messaging, team, labels, ratecards, allocations, products,
        ]:
            for attr_name in dir(module):
                if attr_name.startswith("cor_") and callable(getattr(module, attr_name)):
                    count += 1

        # We expect 14 projects + 10 tasks + 5 time_tracking + 6 clients
        # + 5 contracts + 4 messaging + 8 team + 1 labels
        # + 3 ratecards + 3 allocations + 2 products = 61 tools
        assert count >= 60, f"Expected ~60+ tools, got {count}"


class TestServerCreation:
    """Tests for the server factory."""

    def test_create_server(self):
        """Test that server can be created."""
        from cor_mcp_server.server import create_server
        mcp = create_server()
        assert mcp is not None
        assert mcp.name == "COR MCP Server"
