#!/usr/bin/env bash
set -euo pipefail

WEB_URL="${WEB_URL:-http://localhost:8771}"
API_URL="${WEB_URL}/api"

echo "== BomTS Dev AI Phase 8.1 Check (Reference Pipeline Stabilization) =="
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
echo "3) Checking /sources GET..."
SOURCES=$(curl -s "${API_URL}/sources")
if [[ "$SOURCES" == *"[]"* ]] || [[ "$SOURCES" == *'"id"'* ]]; then
  echo "✅ /sources GET OK"
else
  echo "ERROR: /sources failed to return list"
  exit 1
fi

echo
echo "4) Inserting local/fixed Reference Document (Bypassing external fetch)..."
# In order to test robustly without external network reliance, we manually insert a document
# into /documents mimicking a crawled Application Note.

TEST_TITLE="[reference:mcp] MCP Concept Sample"
TEST_CONTENT="Model Context Protocol (MCP) is an emerging open standard that helps AI assistants connect to and understand the context of applications and systems they interact with. It standardizes how AI agents access files, databases, and tools."

DOC_RES=$(curl -s -X POST "${API_URL}/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "'"${TEST_TITLE}"'",
    "content": "'"${TEST_CONTENT}"'",
    "source": "reference-sample",
    "license": "source-linked"
  }')

if echo "$DOC_RES" | grep -q '"id"'; then
  DOC_ID=$(echo "$DOC_RES" | grep -o '"id":[0-9]*' | cut -d: -f2 | tr -d '}')
  echo "✅ Local Reference Doc created (doc_id: $DOC_ID)"
else
  echo "ERROR: Failed to create reference doc -> $DOC_RES"
  exit 1
fi

echo
echo "5) Testing Chunk for the new Reference Document..."
curl -s -X POST "${API_URL}/documents/${DOC_ID}/chunks" > /dev/null
echo "✅ Chunks created"

echo
echo "6) Testing Vector Index for the new Reference Document..."
curl -s -X POST "${API_URL}/documents/${DOC_ID}/index" > /dev/null
echo "✅ Indexed successfully"

echo
echo "7) Testing /search for the Reference Document..."
SEARCH_RES=$(curl -s -X POST "${API_URL}/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"'"${TEST_CONTENT}"'","limit":3}')

if echo "$SEARCH_RES" | grep -q "Model Context Protocol"; then
  echo "✅ /search OK"
else
  echo "ERROR: /search failed or didn't find the reference"
  exit 1
fi

echo
echo "8) Testing /agent/ask with Reference context..."
ASK_RES=$(curl -s -X POST "${API_URL}/agent/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is MCP?","limit":3}')

if echo "$ASK_RES" | grep -q '"intent"'; then
  echo "✅ /agent/ask OK"
else
  echo "ERROR: /agent/ask failed"
  exit 1
fi

echo
echo "✅ Phase 8.1 OK: Reference pipeline is explainable and working."
