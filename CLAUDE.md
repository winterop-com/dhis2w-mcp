# CLAUDE.md

Guidance for Claude Code working in the `dhis2w-mcp` plugin pack.

## NO EMOJIS EVER

Not in commit messages, PR titles, PR descriptions, code comments, docstrings,
documentation, or any output. Use plain text (`[x]`, `[ ]`, `CRITICAL`, `Note:`,
`WARNING:`).

## This repository follows the host's rules

`dhis2w-mcp` is a plugin pack for
[dhis2w](https://github.com/winterop-com/dhis2w). The host's
[CLAUDE.md](https://github.com/winterop-com/dhis2w/blob/main/CLAUDE.md) is the
authority on conventions, and everything in it applies here: `uv` for every Python
operation (`uv add`, never a hand-edited dependency), the `src/` layout with the
`uv_build` backend, Pydantic for all structured data (no `dict`s, no `@dataclass`es),
Typer for the CLI, FastMCP for the MCP surface, pytest for every test, strict ruff +
mypy + pyright, full descriptive names, one-line Google-style docstrings on every
module, class, and function, conventional commits, no AI attribution, and the
greenfield voice: describe what the code does now, never how it got there.

## What lives here

Three packages in one uv workspace: `dhis2w-mcp` (the full FastMCP server), `dhis2w-mcp-bridge`
(the single-tool bridge over the `d2w` CLI) and `dhis2w-mcp-router` (search and dispatch over
upstream MCP servers; domain-neutral, no dhis2w imports). Every member uses the `src/` layout and
releases the same version.

## The tools and the version trees

The MCP tools of every built-in dhis2w-core plugin live in `dhis2w_mcp.tools.v41`, `.v42`, `.v43`
and `.v44`, one module per plugin, each exposing `register(mcp)`. A tool is a thin wrapper over the
same `dhis2w_core.v{N}.plugins.<plugin>.service` function the `d2w` CLI calls - the domain logic
stays in dhis2w-core, and a tool never reimplements it. v43 is the canonical baseline: a new tool is
written there first and copied to the siblings. Every behaviour-changing edit lands in every
tree. Each tree's `__init__.py` lists the modules it registers; `data` registers the
aggregate and tracker modules itself.

## The pluginkit contract

`dhis2w_mcp.plugin` advertises one plain-class plugin object under the `dhis2w.plugins.v1`
entry-point group. Its `@extension def contribute(self, version_key)` returns a `Contribution` named
`mcp` whose `mcp_module` is the tree's tool package and whose `cli_module` is `None`. The server
builds its tool surface from the plugin host, so these tools and every other pack's arrive the same
way. The object is a plain class, not a `BaseModel` - pluginkit scans its attributes and a model
subclass raises during that scan.

## Tests

The suite opts into the host's test environment: `dhis2w-core[testing]` as a dev dependency and
`pytest_plugins = ["dhis2w_core.testing"]` in the root `conftest.py`. `make test` leaves out the
live tests, marked `slow`; `make test-slow` runs them against the DHIS2 that `DHIS2_URL` and
`DHIS2_PAT` name. `make check-examples` checks every example's `call_tool(...)` against the
registered tools.

Run every invocation with `BROWSER=true`.

## Docs

The documentation site is `docs/` built by mkdocs-material (`make docs`, which first regenerates
`docs/tool-reference.md` from the in-process server; published to GitHub Pages by
`.github/workflows/docs.yml`). Examples live in `examples/`.

## Before a PR

`make lint && make test` must pass.

## Releases

This repository releases the same version as the dhis2w host, the way every repository of the
ecosystem does (host `docs/decisions.md`, 2026-09-29). The host is released first. Then every
package here moves to that version and pins the host packages it depends on - `dhis2w-core` and
`dhis2w-client` for the server, `dhis2w-cli` for the bridge, and `dhis2w-core[testing]` in the dev
group - to exactly that version; the workspace is relocked (`uv lock --upgrade`, with `--refresh`
when the PyPI index lags behind the host's publish), passes `make lint`, `make test` and `make docs`,
and is tagged `vX.Y.Z` - the tag is what publishes the three packages to PyPI. A pack released
before the host cannot resolve it.
