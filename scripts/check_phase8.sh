#!/usr/bin/env bash
set -euo pipefail

WEB_URL="${WEB_URL:-http://localhost:8771}"
API_URL="${WEB_URL}/api"

echo "== BomTS Dev AI Phase 8 Check (AI Trend Pipeline) =="
echo "API_URL=${API_URL}"

echo
echo "1) Checking /health..."
curl -s "${API_URL}/health" | grep -q '"status":"ok"' || {
  echo "ERROR: /health check failed"
  exit 1
}
echo "✅ /health OK"

echo
echo "2) Checking /sources GET..."
SOURCES=$(curl -s "${API_URL}/sources")
if [[ "$SOURCES" == *"[]"* ]] || [[ "$SOURCES" == *'"id"'* ]]; then
  echo "✅ /sources GET OK"
else
  echo "ERROR: /sources failed to return list"
  exit 1
fi

echo
echo "3) Testing /sources/fetch-url (Manual URL)..."
TEST_URL="https://example.com"
FETCH_RES=$(curl -s -X POST "${API_URL}/sources/fetch-url" \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"${TEST_URL}\",\"source_name\":\"check-script-test\",\"category\":\"ai_engineering\"}")

if echo "$FETCH_RES" | grep -q '"document_id"'; then
  DOC_ID=$(echo "$FETCH_RES" | grep -o '"document_id":[0-9]*' | cut -d: -f2)
  echo "✅ /sources/fetch-url OK (doc_id: $DOC_ID)"
else
  echo "ERROR: /sources/fetch-url failed -> $FETCH_RES"
  exit 1
fi

echo
echo "4) Checking if document is in /documents..."
DOCS=$(curl -s "${API_URL}/documents")
if echo "$DOCS" | grep -q "${TEST_URL}"; then
  echo "✅ Document saved successfully"
else
  echo "ERROR: Document not found in /documents"
  exit 1
fi

echo
echo "5) Testing Chunk & Index for the new document..."
curl -s -X POST "${API_URL}/documents/${DOC_ID}/chunks" > /dev/null
echo "✅ Chunks created"

curl -s -X POST "${API_URL}/documents/${DOC_ID}/index" > /dev/null
echo "✅ Indexed successfully"

echo
echo "6) Testing /agent/ask with new content..."
ASK_RES=$(curl -s -X POST "${API_URL}/agent/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What domain does example.com belong to?","limit":3}')

if echo "$ASK_RES" | grep -q '"intent"'; then
  echo "✅ /agent/ask OK"
else
  echo "ERROR: /agent/ask failed"
  exit 1
fi

echo
echo "✅ Phase 8 OK: AI Trend Pipeline is working!"
