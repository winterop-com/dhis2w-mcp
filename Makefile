.DEFAULT_GOAL := help

.PHONY: help install lint test test-slow check-examples coverage docs-reference docs docs-serve build clean

# The DHIS2 major the tool reference is generated against; v43 is the canonical baseline.
DOCS_DHIS2_VERSION ?= v43

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

install:  ## Sync the workspace (the three packages and the dev tools)
	uv sync --all-packages --all-groups

lint:  ## Run ruff, mypy and pyright
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy packages scripts
	uv run pyright

test:  ## Run the test suite, without the tests that need a running DHIS2
	BROWSER=true uv run pytest -q -n auto -m "not slow"

test-slow:  ## Run the live tests against a running DHIS2 (DHIS2_URL + DHIS2_PAT)
	BROWSER=true uv run pytest -q -m slow

check-examples:  ## Check every example's MCP tool calls against the registered tools
	uv run python scripts/check_tool_refs.py

coverage:  ## Run the test suite with coverage
	BROWSER=true uv run pytest -q -n auto -m "not slow" --cov --cov-report=term-missing

docs-reference:  ## Regenerate docs/tool-reference.md from the in-process server
	DHIS2_VERSION=$(DOCS_DHIS2_VERSION) uv run python -u scripts/gen_tool_reference.py

docs: docs-reference  ## Build the documentation site into site/, strictly
	uv run mkdocs build --strict

docs-serve: docs-reference  ## Serve the documentation site with live reload
	uv run mkdocs serve

build:  ## Build every package's wheel and source distribution
	uv build --all-packages

clean:  ## Remove build output and tool caches
	rm -rf dist build site .pytest_cache .ruff_cache .mypy_cache .coverage htmlcov
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
