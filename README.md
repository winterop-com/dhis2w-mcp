# dhis2w-mcp

The [dhis2w](https://github.com/winterop-com/dhis2w) MCP servers, as one plugin pack:

| Package | What it is |
| --- | --- |
| [`dhis2w-mcp`](packages/dhis2w-mcp) | The full FastMCP server: every built-in dhis2w plugin's tools, typed, plus whatever other packs (`dhis2w-security`) register. |
| [`dhis2w-mcp-bridge`](packages/dhis2w-mcp-bridge) | One tool, `dhis2_cli`, over the `d2w` CLI, for small local models; read-only by default. |
| [`dhis2w-mcp-router`](packages/dhis2w-mcp-router) | Search and dispatch over upstream MCP servers, so the tool surface never inflates a model's context. |

The MCP tools of the built-in dhis2w plugins live here, as `dhis2w_mcp.tools.v41|v42|v43`, and reach
the server through the `dhis2w.plugins.v1` entry point, the same way every pack registers. They
call the same `service.py` functions of `dhis2w-core` that the `d2w` CLI does.

Documentation: <https://winterop-com.github.io/dhis2w-mcp/>

## Install

```bash
claude mcp add dhis2 -- uvx dhis2w-mcp          # the full server
uv tool install dhis2w-mcp-bridge                # the single-tool bridge
uv tool install dhis2w-mcp-router                # the router
```

## Development

```bash
make install         # uv sync --all-packages --all-groups
make lint            # ruff, mypy, pyright
make test            # the suite, without the tests that need a running DHIS2
make test-slow       # the live tests: DHIS2_URL and DHIS2_PAT pointing at a running DHIS2
make check-examples  # every example's call_tool(...) names a registered tool
make docs            # regenerate the tool reference and build the site, strictly
```

This repository releases the same version as the dhis2w host; see `CLAUDE.md`.
