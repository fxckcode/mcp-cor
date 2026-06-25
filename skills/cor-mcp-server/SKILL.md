---
name: cor-mcp-server
description: "Main skill for the COR MCP Server — a comprehensive MCP server that exposes 61 Project COR API tools via FastMCP with dual auth (email/password or client credentials), stdio/SSE transport, and auto-refreshing OAuth 2.0."
version: 1.0.0
plugin: false
---

# COR MCP Server

## What Is COR?

[Project COR](https://www.projectcor.com) is a project management platform for creative and professional teams. It provides tools for:

- **Project management** — Create and manage projects, track budgets, costs, and profitability
- **Task management** — Assign tasks, set deadlines, track progress
- **Client management** — Manage clients, contracts, and billing
- **Time tracking** — Log hours, approve/reject entries, manage timesheets
- **Team management** — Organize users into teams, allocate resources
- **Ratecards & Products** — Define pricing and billing structures
- **Resource allocation** — Allocate team members to projects with percentages and dates

The COR MCP Server wraps the COR REST API (`api.projectcor.com/v1`) as **61 Model Context Protocol (MCP) tools**, making them accessible from any MCP-compatible AI agent.

## Architecture Overview

```
┌──────────────────────┐     ┌──────────────────────────────┐     ┌──────────────────────┐
│  MCP Client          │     │  COR MCP Server              │     │  COR REST API        │
│  (Hermes / Claude /  │◄───►│  (FastMCP + httpx)           │────►│  api.projectcor.com  │
│   Cursor / etc.)     │     │                              │     │  /v1                 │
└──────────────────────┘     ├──────────────────────────────┤     └──────────────────────┘
                             │  Auth auto-detection          │
                             │  • Email/Password (priority)  │
                             │  • API Key + Client Secret    │
                             └──────────────────────────────┘
```

**Technology stack:**
- **FastMCP** (`mcp[cli]>=1.0.0`) — MCP server framework
- **httpx** (`>=0.27.0`) — Async HTTP client
- **python-dotenv** (`>=1.0.0`) — Environment variable management
- **Python 3.11+** — Async/await throughout
- **Dual transport** — stdio (for local agents) and SSE/HTTP (for remote access)

**Project structure:**
```
cor-mcp-server/
├── pyproject.toml              # Dependencies and metadata
├── README.md                   # Full documentation
├── .env.example                # Env var template
├── Dockerfile                  # Container deployment
├── skills/                     # Hermes Agent skills
├── cor_mcp_server/
│   ├── __init__.py
│   ├── __main__.py             # CLI entry point
│   ├── server.py               # FastMCP + 61 tool registrations
│   ├── auth.py                 # Dual-mode OAuth 2.0
│   ├── client.py               # Async HTTP client
│   ├── context.py              # Shared client context
│   ├── models.py               # Pydantic models
│   └── tools/                  # 11 tool modules
│       ├── projects.py         # 14 tools
│       ├── tasks.py            # 10 tools
│       ├── time_tracking.py    # 5 tools
│       ├── clients.py          # 6 tools
│       ├── contracts.py        # 5 tools
│       ├── messaging.py        # 4 tools
│       ├── team.py             # 8 tools
│       ├── labels.py           # 1 tool
│       ├── ratecards.py        # 3 tools
│       ├── allocations.py      # 3 tools
│       └── products.py         # 2 tools
└── tests/
    └── test_tools.py           # 24 passing tests (mocked)
```

## How to Install & Run

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- COR account with credentials

### Install

```bash
cd /path/to/cor-mcp-server
uv sync
```

### Configure

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then set one of the two auth modes (see below).

### Run

```bash
# stdio transport (default — for MCP agents like Hermes)
uv run cor-mcp-server

# SSE/HTTP transport (for remote access)
uv run cor-mcp-server --transport sse --host 0.0.0.0 --port 8000

# Verbose logging
uv run cor-mcp-server --verbose
```

### Docker

```bash
docker build -t cor-mcp-server .
docker run -i --rm \
  -e COR_EMAIL=your@email.com \
  -e COR_PASSWORD=your_pass \
  -e COR_API_URL=https://api.projectcor.com/v1 \
  cor-mcp-server
```

## Authentication — Both Modes

The server auto-detects which auth mode to use. **Email/password takes priority when both are set.**

### Mode A: Email + Password (personal use)

```ini
COR_EMAIL=your.email@company.com
COR_PASSWORD=your_password
COR_API_URL=https://api.projectcor.com/v1
```

Auth flow: `POST /v1/auth/login` with form data → JWT tokens.

### Mode B: API Key + Client Secret (server-to-server)

```ini
COR_API_KEY=your_api_key
COR_CLIENT_SECRET=your_client_secret
COR_API_URL=https://api.projectcor.com/v1
```

Auth flow: `POST /v1/oauth/token?grant_type=client_credentials` with Basic auth → access token (1-hour TTL).

Both modes include automatic token refresh with a 60-second safety margin before expiry.

## All 61 Tools (Grouped by Module)

### Projects (14 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_list_projects` | List projects with filters | `page`, `per_page`, `filters` |
| `cor_get_project` | Get project by ID | `project_id` |
| `cor_create_project` | Create a new project | `data` (name, clientId, dates, status, etc.) |
| `cor_update_project` | Partial update a project | `project_id`, `data` |
| `cor_delete_project` | Delete a project | `project_id` |
| `cor_get_project_collaborators` | List collaborators | `project_id` |
| `cor_add_project_collaborator` | Add a collaborator | `project_id`, `user_id` |
| `cor_remove_project_collaborator` | Remove a collaborator | `project_id`, `user_id` |
| `cor_get_project_costs` | Get costs/estimates | `project_id` |
| `cor_add_project_cost` | Add cost entry | `project_id`, `data` |
| `cor_get_project_labels` | Get project labels | `project_id` |
| `cor_get_project_ratecard` | Get assigned ratecard | `project_id` |
| `cor_get_project_templates` | Get project templates | `page`, `per_page` |
| `cor_get_project_profitability` | Get profitability data | `project_id` |

### Tasks (10 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_search_tasks` | Search tasks with filters | `filters` (projectId, status, text, labels, etc.) |
| `cor_get_my_pending_tasks` | My pending tasks | None |
| `cor_get_task` | Get task by ID | `task_id` |
| `cor_create_task` | Create a new task | `data` (title, projectId, deadline, priority, etc.) |
| `cor_update_task` | Partial update a task | `task_id`, `data` |
| `cor_delete_task` | Delete a task | `task_id` |
| `cor_get_task_collaborators` | List task collaborators | `task_id` |
| `cor_sync_task_collaborators` | Replace task collaborators | `task_id`, `user_ids` |
| `cor_add_task_label` | Add label to task | `task_id`, `label_id` |
| `cor_remove_task_label` | Remove label from task | `task_id`, `label_id` |

### Clients (6 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_list_clients` | List clients | `page`, `per_page` |
| `cor_get_client` | Get client by ID | `client_id` |
| `cor_create_client` | Create a new client | `data` (name, email, phone, notes) |
| `cor_update_client` | Update a client | `client_id`, `data` |
| `cor_delete_client` | Delete a client | `client_id` |
| `cor_get_client_fees` | Get client fees | `client_id` |

### Contracts (5 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_list_contracts` | List contracts | `page`, `per_page` |
| `cor_get_contract` | Get contract by ID | `contract_id` |
| `cor_create_contract` | Create a contract | `data` (name, clientId, dates, value) |
| `cor_get_contract_positions` | List contract positions | `contract_id` |
| `cor_create_contract_position` | Create a position | `contract_id`, `data` |

### Time Tracking (5 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_log_hours` | Log hours against a task | `task_id`, `data` (hours, date, notes) |
| `cor_search_time_entries` | Search time entries | `filters` (userId, projectId, dates, status) |
| `cor_get_hours_by_date` | Get entries for a date | `datetime_unix` (Unix timestamp) |
| `cor_change_hours_status` | Change entry status | `hours_id`, `status` (approved/rejected/pending) |
| `cor_accept_suggested_hours` | Accept suggested hours | `datetime_unix` |

### Team & Users (8 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_get_my_profile` | Get current user profile | None |
| `cor_list_users` | List users | `page`, `per_page`, `filters` |
| `cor_get_user` | Get user by ID | `user_id` |
| `cor_list_teams` | List teams | `page`, `per_page` |
| `cor_create_team` | Create a team | `data` (name, description) |
| `cor_add_team_users` | Add users to team | `team_id`, `user_ids` |
| `cor_remove_team_users` | Remove users from team | `team_id`, `user_ids` |
| `cor_get_working_time` | Get working time | None |

### Messaging (4 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_get_task_messages` | Get task messages | `task_id` |
| `cor_post_task_message` | Post task message | `task_id`, `content` |
| `cor_get_project_messages` | Get project messages | `project_id` |
| `cor_post_project_message` | Post project message | `project_id`, `content` |

### Ratecards (3 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_list_ratecards` | List ratecards | `page`, `per_page` |
| `cor_get_ratecard` | Get ratecard by ID | `ratecard_id` |
| `cor_create_ratecard` | Create a ratecard | `data` (name, description, rates) |

### Allocations (3 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_get_allocations_by_project` | Get project allocations | `project_id` |
| `cor_save_allocation` | Create/update allocation | `data` (projectId, userId, percentage, dates) |
| `cor_delete_allocation` | Delete allocation | `allocation_id` |

### Products (2 tools)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_list_products` | List products | `page`, `per_page` |
| `cor_create_product` | Create a product | `data` (name, description, rate) |

### Labels (1 tool)

| Tool | Description | Parameters |
|------|-------------|------------|
| `cor_get_labels` | Get labels | `entity_type` (project/task/user, or empty for all) |

## Configuration for Hermes Agent

Add to `~/.hermes/config.yaml` under `mcp_servers`:

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

Then run `/reload-mcp` in your Hermes session.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` | Invalid credentials | Check email/password or API key in `.env` |
| `AuthError: No access_token...` | Wrong auth mode | Set EITHER email+password OR api_key+client_secret, not both |
| `Auth not configured` / `No COR credentials` | Missing env vars | Set `COR_EMAIL`+`COR_PASSWORD` or `COR_API_KEY`+`COR_CLIENT_SECRET` |
| `Connection refused` | uv not in PATH or wrong directory | Run from the project root, ensure `uv` is installed |
| MCP tools not appearing | Config not reloaded | Run `/reload-mcp` in Hermes or restart the MCP client |
| `Rate limited. Retry after Xs.` | API rate limit hit | Wait for the retry-after period |
| `Command not found: uv` | uv not installed | Install: `curl -LsSf https://astral.sh/uv/install.sh | sh` |
| Tests fail | Dependency issue | Run `uv sync --dev` then retry |

## Verification

```bash
# Test from terminal
uv run cor-mcp-server --help

# Run tests (no live credentials needed)
uv run pytest tests/ -v  # Expect 24 passing tests
```
