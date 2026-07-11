# Contributing to COR MCP Server

Thanks for your interest! This guide covers how to contribute effectively.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/fxckcode/mcp-cor.git
cd mcp-cor

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies
uv sync --dev

# Copy env config
cp .env.example .env
# Edit .env with your COR credentials
```

## Code Style

- **Python 3.11+** — type annotations on all public functions
- **Ruff** — linting and formatting (`uv run ruff check .`)
- **Imports** — standard library → third-party → local (separated by blank lines)
- **Async** — all I/O functions use `async def` with `httpx`

## Adding a New Tool

1. Create or edit a module in `cor_mcp_server/tools/`
2. Write an async function with the `cor_` prefix
3. Use `get_client()` for the authenticated HTTP client
4. Return a JSON string (`json.dumps(...)`)
5. Register the tool in `cor_mcp_server/server.py`
6. Add tests in `tests/test_tools.py`
7. Update the tool count in tests if needed

## Testing

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=cor_mcp_server -v

# Run specific test
uv run pytest tests/test_tools.py::TestToolFunctions -v
```

All tests use mocking — no live COR credentials required.

## Pull Request Process

1. Branch from `main`
2. Write tests for your changes
3. Ensure all tests pass (`uv run pytest`)
4. Ensure lint passes (`uv run ruff check .`)
5. Open a PR with a clear description
6. Keep PRs focused — one feature/fix per PR

## Commit Messages

Use [conventional commits](https://www.conventionalcommits.org/):

```
feat: add cor_list_reports tool
fix: handle empty project collaborator response
refactor: extract auth refresh logic
chore: bump httpx to 0.28
docs: update README with SSE example
test: add coverage for pagination edge cases
```

## Questions?

Open a [Discussion](https://github.com/fxckcode/mcp-cor/discussions) or an Issue.
