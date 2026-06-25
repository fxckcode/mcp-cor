---
name: cor-api-tools
description: "Deep reference for all 61 COR MCP API tools — complete argument listings, JSON request/response examples, and common usage patterns for every module."
version: 1.0.0
plugin: false
---

# COR API Tools — Complete Reference

All tool names are prefixed with `cor_`. Every tool returns a JSON string. All async functions use `httpx` under the hood with automatic Bearer token injection via `get_client()`.

## Projects Module (14 tools)

### `cor_list_projects`

List projects with optional filters.

**Arguments:**
| Arg | Type | Default | Description |
|-----|------|---------|-------------|
| `page` | int | 1 | Page number |
| `per_page` | int | 20 | Results per page |
| `filters` | dict or None | None | Filter fields: `clientId`, `status`, `health`, `startDate`, `endDate` |

**Example call:**
```python
await cor_list_projects(
    page=1,
    per_page=10,
    filters={"status": "active", "clientId": 42}
)
```

**Response shape:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Website Redesign",
      "clientId": 42,
      "status": "active",
      "health": "on_track",
      "startDate": "2025-01-01",
      "endDate": "2025-06-30",
      "description": "Complete website overhaul"
    }
  ],
  "totalPages": 1,
  "page": 1,
  "perPage": 10
}
```

### `cor_get_project`

Get a single project by ID.

**Arguments:** `project_id` (int | str) — The project ID.

**Example call:**
```python
await cor_get_project(project_id=42)
```

### `cor_create_project`

Create a new project.

**Arguments:** `data` (dict) — Fields: `name` (required), `clientId`, `description`, `startDate`, `endDate`, `status`.

**Example call:**
```python
await cor_create_project(data={
    "name": "New Campaign",
    "clientId": 42,
    "description": "Q3 marketing campaign",
    "startDate": "2025-07-01",
    "endDate": "2025-09-30",
    "status": "active"
})
```

### `cor_update_project`

Partial update an existing project.

**Arguments:** `project_id` (int | str), `data` (dict) — Fields to update.

### `cor_delete_project`

Delete a project.

**Arguments:** `project_id` (int | str).

### `cor_get_project_collaborators`

Get collaborators for a project.

**Arguments:** `project_id` (int | str).

**Response:**
```json
[
  {"id": 1, "name": "Alice", "email": "alice@agency.com", "role": "manager"},
  {"id": 2, "name": "Bob", "email": "bob@agency.com", "role": "contributor"}
]
```

### `cor_add_project_collaborator`

Add a collaborator to a project.

**Arguments:** `project_id` (int | str), `user_id` (int | str).

### `cor_remove_project_collaborator`

Remove a collaborator from a project.

**Arguments:** `project_id` (int | str), `user_id` (int | str).

### `cor_get_project_costs`

Get costs/estimates for a project.

**Arguments:** `project_id` (int | str).

### `cor_add_project_cost`

Add a cost entry to a project.

**Arguments:** `project_id` (int | str), `data` (dict) — Fields: `description`, `amount`, `date`, etc.

**Example:**
```python
await cor_add_project_cost(project_id=42, data={
    "description": "Photography",
    "amount": 2500.00,
    "date": "2025-03-15"
})
```

### `cor_get_project_labels`

Get labels assigned to a project.

**Arguments:** `project_id` (int | str).

### `cor_get_project_ratecard`

Get the ratecard assigned to a project.

**Arguments:** `project_id` (int | str).

### `cor_get_project_templates`

Get available project templates.

**Arguments:** `page` (int, default=1), `per_page` (int, default=20).

### `cor_get_project_profitability`

Get profitability data for a project.

**Arguments:** `project_id` (int | str).

---

## Tasks Module (10 tools)

### `cor_search_tasks`

Search tasks with filters.

**Arguments:** `filters` (dict or None) — Fields: `projectId`, `clientId`, `status`, `text` (search in title/description), `labels`, `dates`.

**Example:**
```python
await cor_search_tasks(filters={
    "projectId": 42,
    "status": "open",
    "text": "design"
})
```

### `cor_get_my_pending_tasks`

Get current user's pending tasks.

**Arguments:** None.

### `cor_get_task`

Get a single task by ID.

**Arguments:** `task_id` (int | str).

### `cor_create_task`

Create a new task.

**Arguments:** `data` (dict) — Fields: `title` (required), `projectId`, `description`, `deadline`, `priority`, `assigneeId`.

**Example:**
```python
await cor_create_task(data={
    "title": "Design homepage mockup",
    "projectId": 42,
    "description": "Create Figma mockups for the new homepage",
    "deadline": "2025-04-01",
    "priority": "high"
})
```

### `cor_update_task`

Partial update a task.

**Arguments:** `task_id` (int | str), `data` (dict) — Fields to update.

### `cor_delete_task`

Delete a task.

**Arguments:** `task_id` (int | str).

### `cor_get_task_collaborators`

Get collaborators for a task.

**Arguments:** `task_id` (int | str).

### `cor_sync_task_collaborators`

Replace all collaborators on a task.

**Arguments:** `task_id` (int | str), `user_ids` (list[int | str]).

**Example:**
```python
await cor_sync_task_collaborators(task_id=123, user_ids=[5, 8, 12])
```

### `cor_add_task_label`

Add a label to a task.

**Arguments:** `task_id` (int | str), `label_id` (int | str).

### `cor_remove_task_label`

Remove a label from a task.

**Arguments:** `task_id` (int | str), `label_id` (int | str).

---

## Clients Module (6 tools)

### `cor_list_clients`

List clients.

**Arguments:** `page` (int, default=1), `per_page` (int, default=20).

### `cor_get_client`

Get a single client by ID.

**Arguments:** `client_id` (int | str).

### `cor_create_client`

Create a new client.

**Arguments:** `data` (dict) — Fields: `name` (required), `email`, `phone`, `notes`.

**Example:**
```python
await cor_create_client(data={
    "name": "Acme Corp",
    "email": "contact@acme.com",
    "phone": "+1-555-0123",
    "notes": "Enterprise client, monthly billing"
})
```

### `cor_update_client`

Update an existing client.

**Arguments:** `client_id` (int | str), `data` (dict).

### `cor_delete_client`

Delete a client.

**Arguments:** `client_id` (int | str).

### `cor_get_client_fees`

Get fees for a client.

**Arguments:** `client_id` (int | str).

---

## Contracts Module (5 tools)

### `cor_list_contracts`

List contracts.

**Arguments:** `page` (int, default=1), `per_page` (int, default=20).

### `cor_get_contract`

Get a single contract by ID.

**Arguments:** `contract_id` (int | str).

### `cor_create_contract`

Create a new contract.

**Arguments:** `data` (dict) — Fields: `name` (required), `clientId`, `startDate`, `endDate`, `value`, `status`.

**Example:**
```python
await cor_create_contract(data={
    "name": "Q3 Retainer",
    "clientId": 42,
    "startDate": "2025-07-01",
    "endDate": "2025-09-30",
    "value": 50000.00,
    "status": "active"
})
```

### `cor_get_contract_positions`

Get positions for a contract.

**Arguments:** `contract_id` (int | str).

### `cor_create_contract_position`

Create a position in a contract.

**Arguments:** `contract_id` (int | str), `data` (dict) — Fields: `title`, `rate`, `hours`.

**Example:**
```python
await cor_create_contract_position(contract_id=10, data={
    "title": "Senior Designer",
    "rate": 150.00,
    "hours": 160
})
```

---

## Time Tracking Module (5 tools)

### `cor_log_hours`

Log hours against a task.

**Arguments:** `task_id` (int | str), `data` (dict) — Fields: `hours` (float), `date` (YYYY-MM-DD), `notes`.

**Example:**
```python
await cor_log_hours(task_id=123, data={
    "hours": 6.5,
    "date": "2025-03-10",
    "notes": "Worked on homepage layout"
})
```

### `cor_search_time_entries`

Search time entries with filters.

**Arguments:** `filters` (dict or None) — Fields: `userId`, `projectId`, `startDate`, `endDate`, `status`.

### `cor_get_hours_by_date`

Get time entries for a specific date.

**Arguments:** `datetime_unix` (int) — Unix timestamp.

**Example:**
```python
import time
await cor_get_hours_by_date(datetime_unix=int(time.time()))
```

### `cor_change_hours_status`

Change the status of a time entry.

**Arguments:** `hours_id` (int | str), `status` (str) — One of: `"approved"`, `"rejected"`, `"pending"`.

### `cor_accept_suggested_hours`

Accept suggested hours for a given date.

**Arguments:** `datetime_unix` (int) — Unix timestamp.

---

## Team & Users Module (8 tools)

### `cor_get_my_profile`

Get the current user's profile.

**Arguments:** None.

**Response:**
```json
{
  "id": 1,
  "name": "Alejandro Duran",
  "email": "alejandro@agency.com",
  "role": "admin",
  "teams": [{"id": 1, "name": "Creative"}]
}
```

### `cor_list_users`

List users with optional filters.

**Arguments:** `page` (int, default=1), `per_page` (int, default=20), `filters` (dict or None).

### `cor_get_user`

Get a single user by ID.

**Arguments:** `user_id` (int | str).

### `cor_list_teams`

List teams.

**Arguments:** `page` (int, default=1), `per_page` (int, default=20).

### `cor_create_team`

Create a new team.

**Arguments:** `data` (dict) — Fields: `name` (required), `description`.

### `cor_add_team_users`

Add users to a team.

**Arguments:** `team_id` (int | str), `user_ids` (list[int | str]).

### `cor_remove_team_users`

Remove users from a team.

**Arguments:** `team_id` (int | str), `user_ids` (list[int | str]).

### `cor_get_working_time`

Get working time for users.

**Arguments:** None.

---

## Messaging Module (4 tools)

### `cor_get_task_messages`

Get messages on a task.

**Arguments:** `task_id` (int | str).

### `cor_post_task_message`

Post a message on a task.

**Arguments:** `task_id` (int | str), `content` (str) — Message text, supports @mentions.

**Example:**
```python
await cor_post_task_message(task_id=123, content="@Alice can you review this? Thanks!")
```

### `cor_get_project_messages`

Get messages on a project.

**Arguments:** `project_id` (int | str).

### `cor_post_project_message`

Post a message on a project.

**Arguments:** `project_id` (int | str), `content` (str) — Supports @mentions.

---

## Ratecards Module (3 tools)

### `cor_list_ratecards`

List ratecards.

**Arguments:** `page` (int, default=1), `per_page` (int, default=20).

### `cor_get_ratecard`

Get a single ratecard by ID.

**Arguments:** `ratecard_id` (int | str).

### `cor_create_ratecard`

Create a new ratecard.

**Arguments:** `data` (dict) — Fields: `name` (required), `description`, `rates` (list of rate entries).

**Example:**
```python
await cor_create_ratecard(data={
    "name": "Standard 2025",
    "description": "Standard billing rates for 2025",
    "rates": [
        {"role": "Senior Dev", "rate": 200},
        {"role": "Junior Dev", "rate": 120},
        {"role": "Designer", "rate": 150}
    ]
})
```

---

## Allocations Module (3 tools)

### `cor_get_allocations_by_project`

Get resource allocations for a project.

**Arguments:** `project_id` (int | str).

### `cor_save_allocation`

Create or update a resource allocation.

**Arguments:** `data` (dict) — Fields: `projectId`, `userId`, `allocationPercentage`, `startDate`, `endDate`.

**Example:**
```python
await cor_save_allocation(data={
    "projectId": 42,
    "userId": 5,
    "allocationPercentage": 50,
    "startDate": "2025-01-01",
    "endDate": "2025-06-30"
})
```

### `cor_delete_allocation`

Delete a resource allocation.

**Arguments:** `allocation_id` (int | str).

---

## Products Module (2 tools)

### `cor_list_products`

List products.

**Arguments:** `page` (int, default=1), `per_page` (int, default=20).

### `cor_create_product`

Create a new product.

**Arguments:** `data` (dict) — Fields: `name` (required), `description`, `rate`.

**Example:**
```python
await cor_create_product(data={
    "name": "Website Design",
    "description": "Full website design service",
    "rate": 5000.00
})
```

---

## Labels Module (1 tool)

### `cor_get_labels`

Get labels, optionally filtered by entity type.

**Arguments:** `entity_type` (str, default="") — One of `"project"`, `"task"`, `"user"`, or empty for all.

**Example:**
```python
await cor_get_labels(entity_type="task")
```

**Response:**
```json
[
  {"id": 1, "name": "urgent", "color": "#FF0000", "entityType": "task"},
  {"id": 2, "name": "design", "color": "#0000FF", "entityType": "task"}
]
```

---

## Common Patterns

### Pagination

Most list tools support `page` and `per_page` parameters:

```python
# Get page 2 with 50 results
result = await cor_list_projects(page=2, per_page=50)
```

### Filtering

Projects, tasks, time entries, and users accept a `filters` dict:

```python
await cor_search_tasks(filters={
    "projectId": 42,
    "status": "open",
    "text": "urgent"
})
```

### IDs

All entity IDs accept either `int` or `str`:

```python
await cor_get_task(task_id="123")   # string
await cor_get_task(task_id=123)     # int — both work
```

### Error Handling

Tools raise `CORClientError` on failures. The JSON response body indicates success/failure:

```python
try:
    result = await cor_get_project(project_id=99999)
except CORClientError as e:
    print(f"Error {e.status_code}: {e.body}")
```

### Chaining: Create then Assign

```python
# 1. Create a task
task = await cor_create_task(data={
    "title": "Design homepage",
    "projectId": 42
})
task_data = json.loads(task)
task_id = task_data.get("id")

# 2. Assign collaborator
await cor_sync_task_collaborators(
    task_id=task_id,
    user_ids=[5, 8]
)

# 3. Add a label
await cor_add_task_label(task_id=task_id, label_id=3)
```

### Chaining: Find Project by Name, then Get Profitability

```python
projects = await cor_list_projects(filters={"status": "active"})
data = json.loads(projects)
proj = next(p for p in data["data"] if "Campaign" in p["name"])
profit = await cor_get_project_profitability(project_id=proj["id"])
```
