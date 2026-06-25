# COR MCP Server

Comprehensive MCP server for [Project COR](https://www.projectcor.com) — a project management platform for creative and professional teams.

Exposes **61 tools** covering the complete COR REST API surface as MCP tools, usable from any MCP-compatible client (Claude Desktop, Cursor, Hermes Agent, Claude Code, Cline, Windsurf, etc.).

## Features

- **61 MCP tools** — full CRUD for all COR entities
- **Dual authentication** — pick what suits you:
  - **User Credentials** (email + password) — quick personal use
  - **Client Credentials** (API key + client secret) — server-to-server
- **Async everywhere** — `httpx` + `asyncio`, non-blocking I/O
- **Dual transport** — stdio (default for agents) and SSE/HTTP (for remote access)
- **OAuth token auto-refresh** — never worry about expiry mid-session
- **Docker support** — one-command deployment
- **Hermes Agent skills** included — `/skills/cor-mcp-setup` for easy integration

### Entity Coverage

| Module | Tools | Covers |
|--------|-------|--------|
| Projects | 14 | CRUD, collaborators, costs, labels, ratecards, templates, profitability |
| Tasks | 10 | Search, CRUD, collaborators, labels, messages |
| Clients | 6 | CRUD, fees |
| Contracts | 5 | CRUD, positions |
| Time Tracking | 5 | Log, search, status, accept suggested |
| Team & Users | 8 | Profile, users, teams, working time |
| Messaging | 4 | Project + task messages |
| Allocations | 3 | CRUD |
| Ratecards | 3 | CRUD |
| Products | 2 | CRUD |
| Labels | 1 | By entity type |

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- COR account with credentials

### Install & Run

```bash
# Clone the repo
git clone https://github.com/YOUR_USER/cor-mcp-server.git
cd cor-mcp-server

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

### Configure

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then choose **one** auth mode in `.env`:

**Mode A — Email + Password (recommended for personal use):**
```ini
COR_EMAIL=your.email@company.com
COR_PASSWORD=your_password
COR_API_URL=https://api.projectcor.com/v1
```

**Mode B — API Key + Client Secret (for server-to-server):**
```ini
COR_API_KEY=your_api_key
COR_CLIENT_SECRET=your_client_secret
COR_API_URL=https://api.projectcor.com/v1
```

The server auto-detects which mode you configured. Email/password takes priority when both are set.

### Run

```bash
# stdio transport (default — for MCP agents)
uv run cor-mcp-server

# SSE/HTTP transport (for remote access)
uv run cor-mcp-server --transport sse --host 0.0.0.0 --port 8000

# Verbose logging
uv run cor-mcp-server --verbose
```

## Connecting from MCP Clients

### Hermes Agent (recommended)

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  cor:
    command: "uv"
    args: ["run", "--directory", "/path/to/cor-mcp-server", "python", "-m", "cor_mcp_server"]
    env:
      COR_EMAIL: "your.email@company.com"
      COR_PASSWORD: "your_password"
      COR_API_URL: "https://api.projectcor.com/v1"
    timeout: 180
    connect_timeout: 60
```

Then restart or run `/reload-mcp`.

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "cor": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/cor-mcp-server", "python", "-m", "cor_mcp_server"],
      "env": {
        "COR_EMAIL": "your.email@company.com",
        "COR_PASSWORD": "your_password",
        "COR_API_URL": "https://api.projectcor.com/v1"
      }
    }
  }
}
```

### Cursor / Windsurf / Cline

In MCP Servers settings, add:

- **Name**: COR
- **Type**: command
- **Command**: `uv run --directory /path/to/cor-mcp-server python -m cor_mcp_server`
- **Environment variables**: `COR_EMAIL`, `COR_PASSWORD`, `COR_API_URL`

### Claude Code

```bash
env COR_EMAIL=your@email.com COR_PASSWORD=your_pass COR_API_URL=https://api.projectcor.com/v1 \
  npx @anthropic/claude-code --mcp "uv run --directory /path/to/cor-mcp-server python -m cor_mcp_server"
```

### Docker

Build with the included `Dockerfile`, pass env vars at runtime (supports either auth mode as environment variables).

```bash
docker build -t cor-mcp-server .
docker run -i --rm \
  -e COR_EMAIL=your@email.com \
  -e COR_PASSWORD=your_password \
  -e COR_API_URL=https://api.projectcor.com/v1 \
  cor-mcp-server
```

## Available Tools

All tool names are prefixed with `cor_` for clean discoverability.

### Projects (14)

| Tool | Description |
|------|-------------|
| `cor_list_projects` | List projects with filters (clientId, status, health, dates) |
| `cor_get_project` | Get project details |
| `cor_create_project` | Create a new project |
| `cor_update_project` | Update a project (partial) |
| `cor_delete_project` | Delete a project |
| `cor_get_project_collaborators` | Get project collaborators |
| `cor_add_project_collaborator` | Add collaborator to project |
| `cor_remove_project_collaborator` | Remove collaborator from project |
| `cor_get_project_costs` | Get project costs/estimates |
| `cor_add_project_cost` | Add cost to project |
| `cor_get_project_labels` | Get project labels |
| `cor_get_project_ratecard` | Get project ratecard |
| `cor_get_project_templates` | Get available project templates |
| `cor_get_project_profitability` | Get project profitability |

### Tasks (10)

| Tool | Description |
|------|-------------|
| `cor_search_tasks` | Search tasks with filters (projectId, clientId, status, text, dates, labels) |
| `cor_get_my_pending_tasks` | Get my pending tasks |
| `cor_get_task` | Get task details |
| `cor_create_task` | Create a new task |
| `cor_update_task` | Update a task |
| `cor_delete_task` | Delete a task |
| `cor_get_task_collaborators` | Get task collaborators |
| `cor_sync_task_collaborators` | Sync (replace) task collaborators |
| `cor_add_task_label` | Add label to task |
| `cor_remove_task_label` | Remove label from task |

### Clients (6)

| Tool | Description |
|------|-------------|
| `cor_list_clients` | List clients |
| `cor_get_client` | Get client details |
| `cor_create_client` | Create a new client |
| `cor_update_client` | Update a client |
| `cor_delete_client` | Delete a client |
| `cor_get_client_fees` | Get client fees |

### Contracts (5)

| Tool | Description |
|------|-------------|
| `cor_list_contracts` | List contracts |
| `cor_get_contract` | Get contract details |
| `cor_create_contract` | Create a new contract |
| `cor_get_contract_positions` | Get contract positions |
| `cor_create_contract_position` | Create position in contract |

### Time Tracking (5)

| Tool | Description |
|------|-------------|
| `cor_log_hours` | Log hours against a task |
| `cor_search_time_entries` | Search time entries with filters |
| `cor_get_hours_by_date` | Get time entries by date |
| `cor_change_hours_status` | Change time entry status |
| `cor_accept_suggested_hours` | Accept suggested hours |

### Team & Users (8)

| Tool | Description |
|------|-------------|
| `cor_get_my_profile` | Get current user profile |
| `cor_list_users` | List users with filters |
| `cor_get_user` | Get user details |
| `cor_list_teams` | List teams |
| `cor_create_team` | Create a new team |
| `cor_add_team_users` | Add users to a team |
| `cor_remove_team_users` | Remove users from a team |
| `cor_get_working_time` | Get working time for users |

### Messaging (4)

| Tool | Description |
|------|-------------|
| `cor_get_task_messages` | Get messages on a task |
| `cor_post_task_message` | Post a message on a task |
| `cor_get_project_messages` | Get messages on a project |
| `cor_post_project_message` | Post a message on a project |

### Ratecards (3)

| Tool | Description |
|------|-------------|
| `cor_list_ratecards` | List ratecards |
| `cor_get_ratecard` | Get ratecard details |
| `cor_create_ratecard` | Create a new ratecard |

### Allocations (3)

| Tool | Description |
|------|-------------|
| `cor_get_allocations_by_project` | Get allocations for a project |
| `cor_save_allocation` | Create/update a resource allocation |
| `cor_delete_allocation` | Delete a resource allocation |

### Products (2)

| Tool | Description |
|------|-------------|
| `cor_list_products` | List products |
| `cor_create_product` | Create a new product |

### Labels (1)

| Tool | Description |
|------|-------------|
| `cor_get_labels` | Get labels (filter by entity type) |

## Authentication

Two modes supported. The server auto-detects which to use.

### User Credentials (Mode A)

```
POST https://api.projectcor.com/v1/auth/login
Content-Type: application/x-www-form-urlencoded

email=user@corp.com&password=*****
```

Returns JWT `access_token` + `refresh_token`. Auto-refresh built in.

### Client Credentials (Mode B)

```
POST https://api.projectcor.com/v1/oauth/token?grant_type=client_credentials
Authorization: Basic base64(COR_API_KEY:COR_CLIENT_SECRET)
```

Returns `access_token` (1-hour TTL) + `refresh_token`. Cached and auto-refreshed.

## Architecture

```
┌──────────────────────┐     ┌───────────────────────────┐     ┌──────────────────────┐
│  MCP Client          │     │  COR MCP Server           │     │  COR REST API        │
│  (Hermes / Claude /  │◄───►│  (FastMCP + httpx)        │────►│  api.projectcor.com  │
│   Cursor / etc.)     │     │                            │     │  /v1                 │
└──────────────────────┘     ├───────────────────────────┤     └──────────────────────┘
                             │  Auth auto-detection       │
                             │  • Email/Password (prio)   │
                             │  • API Key + Secret        │
                             └───────────────────────────┘
```

## Development

```bash
# Install dev deps
uv sync --dev

# Run tests (no live API needed — uses mocking)
uv run pytest tests/ -v

# Test server startup
uv run cor-mcp-server --help

# Lint
uv run ruff check .
```

## Project Structure

```
cor-mcp-server/
├── pyproject.toml            # Dependencies and metadata
├── README.md                 # This file
├── .env.example              # Env var template (both auth modes)
├── Dockerfile                # Container deployment
├── skills/                   # Hermes Agent skills
│   └── cor-mcp-setup/
│       └── SKILL.md          # Skill: setup + usage guide
├── cor_mcp_server/
│   ├── __init__.py           # Package init
│   ├── __main__.py           # CLI entry point
│   ├── server.py             # FastMCP server + tool registration
│   ├── auth.py               # OAuth 2.0 (dual mode: user creds + client creds)
│   ├── client.py             # COR API HTTP client (httpx)
│   ├── context.py            # Shared client context / lifespan
│   ├── models.py             # Pydantic models
│   └── tools/
│       ├── __init__.py
│       ├── projects.py       # 14 tools
│       ├── tasks.py          # 10 tools
│       ├── time_tracking.py  # 5 tools
│       ├── clients.py        # 6 tools
│       ├── contracts.py      # 5 tools
│       ├── messaging.py      # 4 tools
│       ├── team.py           # 8 tools
│       ├── labels.py         # 1 tool
│       ├── ratecards.py      # 3 tools
│       ├── allocations.py    # 3 tools
│       └── products.py       # 2 tools
├── tests/
│   ├── __init__.py
│   └── test_tools.py         # Tests for auth, client, and tools
└── handoff-personal-hermes.md # Self-contained instructions for personal Hermes
```

## License

MIT

## Author

Alejandro Duran — Omnicom Media Group
