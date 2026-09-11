#!/usr/bin/env bash
set -euo pipefail

uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest -m "not gpu and not performance and not slow"
