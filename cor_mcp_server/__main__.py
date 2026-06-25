"""
Entry point for the COR MCP Server.

Supports running as:
    python -m cor_mcp_server
    cor-mcp-server
"""

from __future__ import annotations

import argparse
import logging
import sys

from .server import create_server, run_server


def main() -> None:
    """Main entry point for the COR MCP Server."""
    parser = argparse.ArgumentParser(
        description="Comprehensive MCP server for Project COR",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default=None,
        help="Transport type (default: stdio, or MCP_TRANSPORT env var)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for SSE transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE transport (default: 8000)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )

    server = create_server()

    # Set host/port for SSE transport if provided
    if args.transport == "sse":
        import os as _os
        _os.environ.setdefault("MCP_HOST", args.host)
        _os.environ.setdefault("MCP_PORT", str(args.port))

    run_server(server, transport=args.transport)


if __name__ == "__main__":
    main()
