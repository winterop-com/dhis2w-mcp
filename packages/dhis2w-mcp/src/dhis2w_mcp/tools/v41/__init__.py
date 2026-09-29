"""The MCP tools of every built-in dhis2w-core plugin for DHIS2 v41."""

from __future__ import annotations

from typing import Any

from dhis2w_mcp.tools.v41 import (
    analytics,
    apps,
    customize,
    data,
    datastore,
    doctor,
    files,
    maintenance,
    messaging,
    metadata,
    profile,
    route,
    system,
    user,
    user_group,
    user_role,
)

#: Every built-in plugin's tool module for this tree, registered in this order. `data` registers
#: the aggregate and tracker modules itself, as the `data` plugin mounts both.
TOOL_MODULES = (
    analytics,
    apps,
    customize,
    data,
    datastore,
    doctor,
    files,
    maintenance,
    messaging,
    metadata,
    profile,
    route,
    system,
    user,
    user_group,
    user_role,
)


def register(mcp: Any) -> None:
    """Register every built-in plugin's tools on the FastMCP server."""
    for module in TOOL_MODULES:
        module.register(mcp)
