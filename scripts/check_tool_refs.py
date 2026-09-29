"""Guard: every MCP tool an example calls must be a registered tool.

Examples only execute live against a DHIS2 instance, so a renamed or removed tool hides until
then. This validates statically, with no DHIS2 running: each `call_tool("name", ...)` in an
example (`examples/*.py`) must name a tool the dhis2 FastMCP server registers.

Run via `make check-examples`.
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path

from dhis2w_mcp.server import build_server

ROOT = Path(__file__).resolve().parents[1] / "examples"


def _strip_comments(text: str) -> str:
    """Drop the `#` comment portion of each line so prose is not parsed as calls."""
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


async def _live_tools() -> set[str]:
    """Every registered MCP tool name."""
    return {tool.name for tool in await build_server().list_tools()}


def main() -> int:
    """Validate every example's MCP tool calls; exit 1 on any unknown tool."""
    tools = asyncio.run(_live_tools())
    problems: list[str] = []
    for path in sorted(p for p in ROOT.rglob("*.py") if ".venv" not in p.parts):
        for name in sorted(set(re.findall(r'call_tool\(\s*"([a-z0-9_]+)"', _strip_comments(path.read_text())))):
            if name not in tools:
                problems.append(f"{path.relative_to(ROOT.parent)}: unknown MCP tool `{name}`")
    if problems:
        print("Example tool calls that don't resolve:")
        for line in problems:
            print(f"  - {line}")
        return 1
    print("all example MCP tool calls resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
