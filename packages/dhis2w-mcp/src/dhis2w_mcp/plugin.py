"""The plugin object dhis2w-core loads from the `dhis2w.plugins.v1` entry-point group."""

from __future__ import annotations

from dhis2w_core.plugin import Contribution, extension

#: The tool trees this pack ships, one per supported DHIS2 major.
SUPPORTED_VERSION_KEYS: frozenset[str] = frozenset({"v41", "v42", "v43", "v44"})
#: The tree an unrecognised version key binds to; v43 is the canonical baseline.
DEFAULT_VERSION_KEY = "v43"


class McpToolsPlugin:
    """Plugin descriptor for the MCP tools of every built-in dhis2w-core plugin."""

    @extension
    def contribute(self, version_key: str) -> Contribution:
        """Contribute the built-in plugins' MCP tools for `version_key`; no CLI module."""
        tree = version_key if version_key in SUPPORTED_VERSION_KEYS else DEFAULT_VERSION_KEY
        return Contribution(
            name="mcp",
            description="The MCP tools of every built-in dhis2w-core plugin, registered on the dhis2w-mcp server.",
            cli_module=None,
            mcp_module=f"dhis2w_mcp.tools.{tree}",
        )


plugin = McpToolsPlugin()
