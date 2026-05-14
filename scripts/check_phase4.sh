#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "== BomTS Dev AI Phase 4 Check =="
echo "BASE_URL=${BASE_URL}"

echo
echo "1) Checking Phase 3 is working by indexing a test doc..."
DOC_RESPONSE="$(curl -s -X POST "${BASE_URL}/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Phase 4 RAG Test",
    "content": "Phase 4 adds LLM Provider abstraction and prompt building capabilities. This allows us to generate context-aware answers.",
    "source": "phase4-check-script",
    "license": "private"
  }')"

DOCUMENT_ID="$(echo "${DOC_RESPONSE}" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"

curl -s -X POST "${BASE_URL}/documents/${DOCUMENT_ID}/chunks" > /dev/null
curl -s -X POST "${BASE_URL}/documents/${DOCUMENT_ID}/index" > /dev/null

echo "Test document indexed (ID: $DOCUMENT_ID)"

echo
echo "2) Testing Ask API"
ASK_RESPONSE="$(curl -s -X POST "${BASE_URL}/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does Phase 4 add?",
    "limit": 5
  }')"

echo "${ASK_RESPONSE}" | python3 -m json.tool || echo "${ASK_RESPONSE}"

echo "${ASK_RESPONSE}" | grep -q "answer" || {
  echo "ERROR: response does not contain answer"
  exit 1
}

echo "${ASK_RESPONSE}" | grep -q "sources" || {
  echo "ERROR: response does not contain sources"
  exit 1
}

echo "${ASK_RESPONSE}" | grep -q "provider" || {
  echo "ERROR: response does not contain provider"
  exit 1
}

echo "${ASK_RESPONSE}" | grep -q "latency_ms" || {
  echo "ERROR: response does not contain latency_ms"
  exit 1
}

echo
echo "✅ Phase 4 OK: ask endpoint responds with answer, sources, provider, and latency."
