#!/usr/bin/env bash
set -euo pipefail

export PYTHONPYCACHEPREFIX=/tmp/dev-ai-pycache
python3 -m compileall -q app scripts
python3 scripts/check_db_security_config.py
python3 scripts/check_alembic_baseline.py
docker compose config -q
