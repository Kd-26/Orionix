#!/usr/bin/env bash
set -euo pipefail

command -v uv >/dev/null
command -v python3 >/dev/null
uv --version
python3 --version
echo "CPU development prerequisites are available; GPU/provider checks are intentionally omitted."
