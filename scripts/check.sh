#!/usr/bin/env bash
set -euo pipefail

export PYTHONPYCACHEPREFIX=/tmp/dev-ai-pycache
python3 -m compileall -q app scripts
docker compose config -q
