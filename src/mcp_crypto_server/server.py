from __future__ import annotations

from typing import Any

from .mcp_tools import mcp


def main() -> None:
    """Run the MCP server if available; otherwise, print a friendly message.

    In production, `mcp` should be the real FastMCP instance from the
    `mcp` package. When running locally without that package, the shim in
    `mcp_tools` is used which may not implement `run()`; we handle that.
    """
    runner = getattr(mcp, "run", None)
    if callable(runner):
        runner()
    else:
        print("mcp.run() not available in this environment. MCP shim loaded.")


if __name__ == "__main__":
    main()
