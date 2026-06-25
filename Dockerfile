FROM python:3.11-slim

WORKDIR /app

# Install uv for fast dependency management
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml README.md ./
COPY cor_mcp_server/ ./cor_mcp_server/

# Install dependencies
RUN uv pip install --system -e .

# Expose SSE port
EXPOSE 8000

# Default: run with stdio transport (for MCP clients)
# Override with --transport sse for HTTP/SSE mode
ENTRYPOINT ["python", "-m", "cor_mcp_server"]
CMD []
