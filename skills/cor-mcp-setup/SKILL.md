---
name: cor-mcp-setup
description: "Set up and use the COR MCP Server — 61 tools for Project COR (projects, tasks, clients, time tracking, teams). Covers both auth modes: email/password and API key + client secret."
version: 1.0.0
author: Alejandro Duran
platforms: [macos, linux, windows]
---

# COR MCP Server

An MCP server that exposes the full [Project COR](https://www.projectcor.com) REST API (61 tools) for use from any MCP-compatible agent (Hermes Agent, Claude Desktop, Cursor, Claude Code, etc.).

## Prerequisites

- Python 3.11+
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- COR credentials (email + password **or** API key + client secret)

## Quick Install

```bash
cd /path/to/cor-mcp-server
uv sync
```

## Configuration

Copy `.env.example` to `.env` and set ONE authentication mode:

### Mode A: Email + Password (personal use)

```ini
COR_EMAIL=your.email@company.com
COR_PASSWORD=your_password
COR_API_URL=https://api.projectcor.com/v1
```

### Mode B: API Key + Client Secret (server-to-server)

```ini
COR_API_KEY=your_api_key
COR_CLIENT_SECRET=your_client_secret
COR_API_URL=https://api.projectcor.com/v1
```

The server auto-detects which mode you configured. Email/password takes priority when both are set.

## Running

```bash
# stdio (default — for MCP agents)
uv run cor-mcp-server

# SSE/HTTP (for remote access)
uv run cor-mcp-server --transport sse --host 0.0.0.0 --port 8000
```

## Hermes Agent Integration

Add this to your `~/.hermes/config.yaml` under `mcp_servers`:

```yaml
mcp_servers:
  cor:
    command: "uv"
    args: ["run", "--directory", "/absolute/path/to/cor-mcp-server", "python", "-m", "cor_mcp_server"]
    env:
      COR_EMAIL: "your.email@company.com"
      COR_PASSWORD: "your_password"
      COR_API_URL: "https://api.projectcor.com/v1"
    timeout: 180
    connect_timeout: 60
```

Then do `/reload-mcp` in the Hermes session.

## Available Tools (all prefixed with `cor_`)

| Entity | Count | Key Tools |
|--------|-------|-----------|
| Projects | 14 | list, create, update, delete, collaborators, costs, profitability |
| Tasks | 10 | search, create, update, labels, collaborators, my pending |
| Clients | 6 | list, create, update, delete, fees |
| Contracts | 5 | list, create, positions |
| Time Tracking | 5 | log hours, search, change status, accept suggested |
| Team & Users | 8 | profile, users, teams, working time |
| Messaging | 4 | project/task messages |
| Ratecards | 3 | list, get, create |
| Allocations | 3 | by project, save, delete |
| Products | 2 | list, create |
| Labels | 1 | by entity type |

## Installation Verification

```bash
uv run cor-mcp-server --help
# Should show: "COR MCP Server — Expose COR API as MCP tools"
```

If connected via Hermes Agent:

```
/reload-mcp
```
Then ask: "what's my COR profile" to verify it works.

## Test Command

```bash
uv run pytest tests/ -v
# 24 tests should pass (uses mocking — no live credentials needed)
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `401 Unauthorized` | Check email/password or API key in .env |
| `Auth not configured` | Set EITHER COR_EMAIL+COR_PASSWORD or COR_API_KEY+COR_CLIENT_SECRET |
| `Connection refused` | Ensure `uv run` works from the project directory |
| MCP tools not appearing | Do `/reload-mcp` in Hermes, or restart the MCP client |
