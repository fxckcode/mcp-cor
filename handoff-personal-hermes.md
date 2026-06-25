# INSTRUCTIONS FOR HERMES (PERSONAL INSTANCE)

**Subject:** Clone, set up, and publish the COR MCP Server

**From:** Alejandro's development agent (opencode-go session)
**Date:** 2026-06-25

---

## Overview

This document is a self-contained handoff for you, Hermes (Alejandro's personal instance running at a trycloudflare URL), to take the COR MCP Server codebase and:

1. Clone the original Bitbucket repo
2. Set it up locally with both authentication modes
3. Publish it to Alejandro's personal GitHub
4. Understand the full architecture (all 61 tools)
5. Configure yourself to use it

The code currently lives at `/Users/alejandro.duran/FLARE/BACKEND/TOOLS/cor-mcp-server/` on the development machine, but you should clone fresh from Bitbucket.

---

## Step 1 — Clone the Original Repository

The upstream repo is on Bitbucket (Omnicom Media Group's workspace):

```bash
# Clone the original
git clone git@bitbucket.org:qdata/mcp-cor.git cor-mcp-server
cd cor-mcp-server

# This is the current remote (already set in the local copy)
git remote -v
# origin  git@bitbucket.org:qdata/mcp-cor.git (fetch)
# origin  git@bitbucket.org:qdata/mcp-cor.git (push)
```

**SSH Key Note:** You'll need Bitbucket SSH access. If Alejandro's personal Hermes doesn't have the Bitbucket SSH key, ask him to add one or use HTTPS with an app password:

```bash
git clone https://x-token-auth:{APP_PASSWORD}@bitbucket.org/qdata/mcp-cor.git
```

---

## Step 2 — Set Up the Environment

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Install Dependencies

```bash
cd cor-mcp-server
uv sync
```

This installs everything from `pyproject.toml`:

| Dependency | Version | Purpose |
|-----------|---------|---------|
| `mcp[cli]` | >=1.0.0 | MCP server framework (FastMCP) |
| `httpx` | >=0.27.0 | Async HTTP client for COR REST API |
| `python-dotenv` | >=1.0.0 | Load `.env` files |

### Configure Authentication (Two Modes)

Copy the template:

```bash
cp .env.example .env
```

**Mode A — User Credentials (recommended for personal use):**

```ini
COR_EMAIL=alejandro.duran@omnicommedia.com
COR_PASSWORD=<ask_alejandro_for_his_cor_password>
COR_API_URL=https://api.projectcor.com/v1
```

**Mode B — Client Credentials (server-to-server, alternative):**

```ini
COR_API_KEY=<ask_alejandro_for_cor_api_key>
COR_CLIENT_SECRET=<ask_alejandro_for_cor_client_secret>
COR_API_URL=https://api.projectcor.com/v1
```

**The server auto-detects which mode you configured.** Email/password takes priority when both are set. To use Client Credentials, leave email/password unset.

> ⚠️ **Important:** Never commit `.env` with real credentials. It's already in `.gitignore`.

### Verify It Works

```bash
# Run the tests (24 tests, all mocked — no live API needed)
uv run pytest tests/ -v

# Check the CLI works
uv run cor-mcp-server --help
```

---

## Step 3 — Run the Server

### stdio Transport (for MCP agents like yourself)

```bash
uv run cor-mcp-server
```

### SSE/HTTP Transport (for remote access via trycloudflare)

```bash
uv run cor-mcp-server --transport sse --host 0.0.0.0 --port 8000
```

### Verbose Logging

```bash
uv run cor-mcp-server --verbose
```

### Docker

```bash
docker build -t cor-mcp-server .
docker run -i --rm \
  -e COR_EMAIL=alejandro.duran@omnicommedia.com \
  -e COR_PASSWORD=<password> \
  -e COR_API_URL=https://api.projectcor.com/v1 \
  cor-mcp-server
```

---

## Step 4 — Publish to Alejandro's Personal GitHub

The user wants this on his personal GitHub. He said the repo name is `cor-mcp-server`.

### Create GitHub Repo

You can create it using the GitHub CLI if available:

```bash
gh repo create alejandro-duran/cor-mcp-server --public --description "MCP server for Project COR — 61 tools exposing the full COR REST API" --remote github
```

Or manually at https://github.com/new — name: `cor-mcp-server`, public, no README/no .gitignore/no license (we'll push existing).

### Push to GitHub

```bash
# Add GitHub as a second remote
git remote add github git@github.com:alejandro-duran/cor-mcp-server.git

# Push main branch
git push github main

# Push with all history (the Bitbucket repo already has a single commit on main)
# If you want to preserve the Bitbucket origin as well:
git remote set-url origin git@bitbucket.org:qdata/mcp-cor.git  # keep original
git remote add github git@github.com:alejandro-duran/cor-mcp-server.git
```

### Commit Any Local Changes

If you make any configuration or documentation changes:

```bash
git add -A
git commit -m "chore: initial setup for personal deployment"
git push github main
```

### Set Default Remote

After pushing, you can set GitHub as the default push target:

```bash
git remote set-url --add --push origin git@github.com:alejandro-duran/cor-mcp-server.git
git remote set-url --add --push origin git@bitbucket.org:qdata/mcp-cor.git
```

---

## Step 5 — Complete Architecture Reference

### How It Works

```
┌──────────────────────┐     ┌──────────────────────────────┐     ┌──────────────────────┐
│  MCP Client          │     │  COR MCP Server              │     │  COR REST API        │
│  (You, Hermes)       │◄───►│  (FastMCP + httpx)           │────►│  api.projectcor.com  │
│                      │     │                              │     │  /v1                 │
└──────────────────────┘     ├──────────────────────────────┤     └──────────────────────┘
                             │  Auth auto-detection          │
                             │  • Email/Password (priority)  │
                             │  • API Key + Client Secret    │
                             └──────────────────────────────┘
```

### Project Structure

```
cor-mcp-server/
├── pyproject.toml              # Dependencies and metadata
├── README.md                   # Full documentation
├── .env.example                # Env var template (both auth modes)
├── Dockerfile                  # Container deployment
├── skills/                     # Hermes Agent skill files
│   ├── cor-auth/SKILL.md       # Auth cheat sheet
│   ├── cor-api-tools/SKILL.md  # Complete 61-tool reference
│   └── cor-mcp-server/SKILL.md # Main skill with full docs
├── cor_mcp_server/
│   ├── __init__.py
│   ├── __main__.py             # CLI entry point (argparse: --transport, --host, --port)
│   ├── server.py               # FastMCP server + 61 tool registrations
│   ├── auth.py                 # Dual-mode OAuth 2.0 (user creds + client creds)
│   ├── client.py               # Async HTTP client (httpx)
│   ├── context.py              # Shared client context / DI
│   ├── models.py               # 14 Pydantic entity models
│   └── tools/
│       ├── __init__.py
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
├── tests/
│   └── test_tools.py           # 24 passing tests (fully mocked)
```

### Key Architectural Decisions

1. **Dual Transport:** Supports both `stdio` (for local MCP agents) and `sse` (for remote/HTTP access)
2. **Dual Auth:** Auto-detects which auth mode to use. User Credentials take priority
3. **Token Caching:** `TokenStore` is thread-safe, stores tokens in-memory, auto-refreshes with 60-second safety margin before expiry
4. **Async Everywhere:** All HTTP calls use `httpx` async client, all tool functions are async
5. **Shared Context:** `context.py` provides `get_client()` / `set_client()` for dependency injection across tool modules
6. **All tools return JSON strings** for consistent serialization

### Auth Mechanism Details

**File:** `cor_mcp_server/auth.py`

- `AuthManager` reads env vars at init, calls `_detect_mode()` to pick between `"user_credentials"` and `"client_credentials"`
- `TokenStore` wraps a `threading.Lock` for thread-safe token access
- **User Credentials flow:** POST to `/v1/auth/login` with form data → JWT tokens. The `_login()` method normalises 3 different response shapes
- **Client Credentials flow:** POST to `/v1/oauth/token?grant_type=client_credentials` with Basic auth header → access token (1-hour TTL)
- On each API call, `get_access_token()` checks `is_expired()` and refreshes proactively if within 60s of expiry

---

## Step 6 — All 61 Tools Reference

All tool names are prefixed with `cor_`. Every tool returns a JSON string.

### Projects (14 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_list_projects` | List projects with filters | `page`, `per_page`, `filters` (clientId, status, health, dates) |
| `cor_get_project` | Get project by ID | `project_id` |
| `cor_create_project` | Create a new project | `data` (name, clientId, description, startDate, endDate, status) |
| `cor_update_project` | Partial update a project | `project_id`, `data` |
| `cor_delete_project` | Delete a project | `project_id` |
| `cor_get_project_collaborators` | List collaborators | `project_id` |
| `cor_add_project_collaborator` | Add a collaborator | `project_id`, `user_id` |
| `cor_remove_project_collaborator` | Remove a collaborator | `project_id`, `user_id` |
| `cor_get_project_costs` | Get costs/estimates | `project_id` |
| `cor_add_project_cost` | Add cost entry | `project_id`, `data` (description, amount, date) |
| `cor_get_project_labels` | Get project labels | `project_id` |
| `cor_get_project_ratecard` | Get assigned ratecard | `project_id` |
| `cor_get_project_templates` | Get project templates | `page`, `per_page` |
| `cor_get_project_profitability` | Get profitability data | `project_id` |

### Tasks (10 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_search_tasks` | Search tasks with filters | `filters` (projectId, clientId, status, text, labels, dates) |
| `cor_get_my_pending_tasks` | My pending tasks | None |
| `cor_get_task` | Get task by ID | `task_id` |
| `cor_create_task` | Create a new task | `data` (title, projectId, description, deadline, priority) |
| `cor_update_task` | Partial update a task | `task_id`, `data` |
| `cor_delete_task` | Delete a task | `task_id` |
| `cor_get_task_collaborators` | List task collaborators | `task_id` |
| `cor_sync_task_collaborators` | Replace all collaborators | `task_id`, `user_ids` (list) |
| `cor_add_task_label` | Add label to task | `task_id`, `label_id` |
| `cor_remove_task_label` | Remove label from task | `task_id`, `label_id` |

### Clients (6 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_list_clients` | List clients | `page`, `per_page` |
| `cor_get_client` | Get client by ID | `client_id` |
| `cor_create_client` | Create a new client | `data` (name, email, phone, notes) |
| `cor_update_client` | Update a client | `client_id`, `data` |
| `cor_delete_client` | Delete a client | `client_id` |
| `cor_get_client_fees` | Get client fees | `client_id` |

### Contracts (5 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_list_contracts` | List contracts | `page`, `per_page` |
| `cor_get_contract` | Get contract by ID | `contract_id` |
| `cor_create_contract` | Create a contract | `data` (name, clientId, startDate, endDate, value, status) |
| `cor_get_contract_positions` | List contract positions | `contract_id` |
| `cor_create_contract_position` | Create a position | `contract_id`, `data` (title, rate, hours) |

### Time Tracking (5 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_log_hours` | Log hours against a task | `task_id`, `data` (hours, date, notes) |
| `cor_search_time_entries` | Search time entries | `filters` (userId, projectId, dates, status) |
| `cor_get_hours_by_date` | Get entries for a date | `datetime_unix` (Unix timestamp) |
| `cor_change_hours_status` | Change entry status | `hours_id`, `status` ("approved"/"rejected"/"pending") |
| `cor_accept_suggested_hours` | Accept suggested hours | `datetime_unix` |

### Team & Users (8 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_get_my_profile` | Get current user profile | None |
| `cor_list_users` | List users with filters | `page`, `per_page`, `filters` |
| `cor_get_user` | Get user by ID | `user_id` |
| `cor_list_teams` | List teams | `page`, `per_page` |
| `cor_create_team` | Create a team | `data` (name, description) |
| `cor_add_team_users` | Add users to team | `team_id`, `user_ids` (list) |
| `cor_remove_team_users` | Remove users from team | `team_id`, `user_ids` (list) |
| `cor_get_working_time` | Get working time for users | None |

### Messaging (4 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_get_task_messages` | Get task messages | `task_id` |
| `cor_post_task_message` | Post task message | `task_id`, `content` (supports @mentions) |
| `cor_get_project_messages` | Get project messages | `project_id` |
| `cor_post_project_message` | Post project message | `project_id`, `content` (supports @mentions) |

### Ratecards (3 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_list_ratecards` | List ratecards | `page`, `per_page` |
| `cor_get_ratecard` | Get ratecard by ID | `ratecard_id` |
| `cor_create_ratecard` | Create a ratecard | `data` (name, description, rates) |

### Allocations (3 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_get_allocations_by_project` | Get project allocations | `project_id` |
| `cor_save_allocation` | Create/update allocation | `data` (projectId, userId, allocationPercentage, startDate, endDate) |
| `cor_delete_allocation` | Delete allocation | `allocation_id` |

### Products (2 tools)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_list_products` | List products | `page`, `per_page` |
| `cor_create_product` | Create a product | `data` (name, description, rate) |

### Labels (1 tool)

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `cor_get_labels` | Get labels by entity type | `entity_type` ("project", "task", "user", or empty for all) |

---

## Step 7 — Configure Hermes to Use the COR MCP Server

### Option A — Local stdio (recommended for direct use)

Edit your `~/.hermes/config.yaml` and add under `mcp_servers`:

```yaml
mcp_servers:
  cor:
    command: "uv"
    args: ["run", "--directory", "/ABSOLUTE/PATH/TO/cor-mcp-server", "python", "-m", "cor_mcp_server"]
    env:
      COR_EMAIL: "alejandro.duran@omnicommedia.com"
      COR_PASSWORD: "<ask_alejandro>"
      COR_API_URL: "https://api.projectcor.com/v1"
    timeout: 180
    connect_timeout: 60
```

### Option B — Remote SSE via trycloudflare

If you want to run the COR MCP Server as a remote service that you connect to via SSE:

1. Start the server on your machine with SSE transport:
   ```bash
   cd /path/to/cor-mcp-server
   uv run cor-mcp-server --transport sse --host 0.0.0.0 --port 8000
   ```

2. Expose it via trycloudflare:
   ```bash
   cloudflared tunnel --url http://localhost:8000
   # → https://XXXX.trycloudflare.com
   ```

3. In your Hermes config.yaml, use the `url` field instead of `command`:
   ```yaml
   mcp_servers:
     cor:
       url: "https://XXXX.trycloudflare.com/sse"
       env:
         COR_EMAIL: "alejandro.duran@omnicommedia.com"
         COR_PASSWORD: "<ask_alejandro>"
         COR_API_URL: "https://api.projectcor.com/v1"
   ```

### Reload MCP

After adding the config, run in your Hermes session:

```
/reload-mcp
```

Then verify with:

```
what's my COR profile
```

If it returns user data, auth is working.

---

## Step 8 — Verify Everything

### Verification Checklist

- [ ] **Clone:** Repository cloned from `git@bitbucket.org:qdata/mcp-cor.git`
- [ ] **Setup:** `uv sync` completes without errors
- [ ] **Auth:** `.env` configured with either email/password or API key/secret
- [ ] **Tests:** `uv run pytest tests/ -v` → 24 passed
- [ ] **CLI:** `uv run cor-mcp-server --help` shows help text
- [ ] **GitHub:** Repository pushed to `github.com:alejandro-duran/cor-mcp-server`
- [ ] **Hermes config:** `~/.hermes/config.yaml` has `cor` under `mcp_servers`
- [ ] **Live test:** `/reload-mcp` then ask "what's my COR profile"
- [ ] **Tool test:** "list my projects" or "show my tasks"

### Quick Smoke Test (terminal, no Hermes needed)

```bash
cd /path/to/cor-mcp-server
uv run python -c "
import asyncio
from cor_mcp_server.auth import AuthManager
from cor_mcp_server.client import CORClient

async def test():
    auth = AuthManager()
    client = CORClient(auth)
    try:
        profile = await client.get('/users/me')
        print('Auth OK! Profile:', profile)
    except Exception as e:
        print(f'Auth failed: {e}')

asyncio.run(test())
"
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `401 Unauthorized` | Invalid credentials | Check email/password or API key in `.env` |
| `Auth not configured` | Missing env vars | Set EITHER `COR_EMAIL`+`COR_PASSWORD` OR `COR_API_KEY`+`COR_CLIENT_SECRET` |
| `Command not found: uv` | uv not installed | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| MCP tools not appearing | Config not reloaded | Run `/reload-mcp` in Hermes |
| `Rate limited. Retry after Xs.` | API rate limit hit | Wait for retry-after period |
| Tests fail | Dependency issue | Run `uv sync --dev` then retry |

---

## Summary for Alejandro

When you hand this off to your personal Hermes, it needs:

1. **Credentials** (one of these pairs):
   - COR email + password
   - OR COR API key + client secret

2. **SSH key** or **Bitbucket app password** for cloning

3. **GitHub personal access token** (classic or fine-grained) with `repo` scope for pushing

The handoff document at `cor-mcp-server/handoff-personal-hermes.md` has everything else — just point Hermes at it.
