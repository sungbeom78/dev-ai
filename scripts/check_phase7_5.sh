#!/usr/bin/env bash
set -euo pipefail

WEB_URL="${WEB_URL:-http://localhost:8771}"

echo "== BomTS Dev AI Phase 7.5 Check =="
echo "WEB_URL=${WEB_URL}"

echo
echo "1) Checking Web UI root..."
curl -s "${WEB_URL}/" | grep -q 'BomTS Dev AI' || {
  echo "ERROR: Web UI index.html failed to load from ${WEB_URL}"
  exit 1
}
echo "✅ Web UI OK"

echo
echo "2) Checking API Proxy (/api/health)..."
curl -s "${WEB_URL}/api/health" | grep -q '"status":"ok"' || {
  echo "ERROR: API proxy health check failed from ${WEB_URL}/api/health"
  exit 1
}
echo "✅ API Proxy OK"

echo
echo "✅ Phase 7.5 OK: Nginx proxy is correctly routing / and /api/"
