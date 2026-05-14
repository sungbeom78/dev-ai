#!/usr/bin/env bash
set -euo pipefail

WEB_URL="${WEB_URL:-http://localhost:8771}"
API_URL="${API_URL:-http://localhost:8000}"

echo "== BomTS Dev AI Phase 5 Check =="

echo "1) Checking Docker compose status..."
docker compose ps

echo
echo "2) Checking API health..."
curl -s "${API_URL}/health" | grep -q '"status":"ok"' || {
  echo "ERROR: API health check failed"
  exit 1
}
echo "API OK"

echo
echo "3) Checking Web UI availability..."
WEB_RESPONSE="$(curl -s "${WEB_URL}")"
echo "${WEB_RESPONSE}" | grep -q "BomTS Dev AI" || {
  echo "ERROR: Web UI does not contain expected title"
  exit 1
}
echo "Web UI OK"

echo
echo "4) Running Phase 3 and Phase 4 checks..."
bash scripts/check_phase3.sh
bash scripts/check_phase4.sh

echo
echo "✅ Phase 5 OK: Web UI and all RAG backend flows are working."
