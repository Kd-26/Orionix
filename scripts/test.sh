#!/usr/bin/env bash
set -euo pipefail

uv run pytest -m "not gpu and not performance and not slow"
