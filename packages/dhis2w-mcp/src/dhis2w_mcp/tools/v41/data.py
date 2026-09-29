"""FastMCP tool registration for `data` — delegates to aggregate + tracker MCP modules."""

from __future__ import annotations

from typing import Any

from dhis2w_mcp.tools.v41 import aggregate as aggregate_mcp
from dhis2w_mcp.tools.v41 import tracker as tracker_mcp


def register(mcp: Any) -> None:
    """Register all data-layer tools (`data_aggregate_*`, `data_tracker_*`)."""
    aggregate_mcp.register(mcp)
    tracker_mcp.register(mcp)
