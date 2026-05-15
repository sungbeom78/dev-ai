#!/usr/bin/env bash
set -euo pipefail

WEB_URL="${WEB_URL:-http://localhost:8771}"
API_URL="${WEB_URL}/api"

echo "== BomTS Dev AI Phase 8.2 Check (Portfolio Page Enhancements) =="
echo "WEB_URL=${WEB_URL}"
echo "API_URL=${API_URL}"

echo
echo "1) Checking Docker Compose Processes..."
docker compose ps || true

echo
echo "2) Checking /health..."
curl -s "${API_URL}/health" | grep -q '"status":"ok"' || {
  echo "ERROR: /health check failed"
  exit 1
}
echo "✅ /health OK"

echo
echo "3) Fetching HTML content from ${WEB_URL}..."
HTML_FILE=$(mktemp)
curl -s "${WEB_URL}" > "$HTML_FILE"

if [ ! -s "$HTML_FILE" ]; then
    echo "ERROR: Failed to fetch HTML content."
    rm -f "$HTML_FILE"
    exit 1
fi

echo "4) Checking required texts in HTML..."

REQUIRED_TEXTS=(
    "BomTS Dev AI"
    "개인 AI Engineering Knowledge Lab"
    "왜 이 프로젝트를 만들었는가"
    "전체 시스템 구조"
    "RAG 파이프라인 흐름"
    "PostgreSQL"
    "Qdrant"
    "Docker Compose"
    "LangGraph"
    "AI Engineering Reference Pipeline"
)

for text in "${REQUIRED_TEXTS[@]}"; do
    if grep -F -q "$text" "$HTML_FILE"; then
        echo "  ✅ Found: '$text'"
    else
        echo "  ❌ ERROR: Missing '$text'"
        rm -f "$HTML_FILE"
        exit 1
    fi
done

rm -f "$HTML_FILE"

echo "✅ All required texts found in Web UI."

echo
echo "5) Running check_phase8_1.sh to ensure functionality is intact..."
if [ -f "scripts/check_phase8_1.sh" ]; then
    chmod +x scripts/check_phase8_1.sh
    ./scripts/check_phase8_1.sh
else
    echo "⚠️ scripts/check_phase8_1.sh not found, skipping."
fi

echo
echo "✅ Phase 8.2 OK: Portfolio Explanation Page is working."
