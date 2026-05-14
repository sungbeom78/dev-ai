#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "== BomTS Dev AI Phase 3 Check =="
echo "BASE_URL=${BASE_URL}"

echo
echo "1) Docker compose status"
docker compose ps

echo
echo "2) Health check"
HEALTH_RESPONSE="$(curl -s "${BASE_URL}/health")"
echo "${HEALTH_RESPONSE}"

echo "${HEALTH_RESPONSE}" | grep -q '"status":"ok"' || {
  echo "ERROR: health check failed"
  exit 1
}

echo
echo "3) Create test document"
DOC_RESPONSE="$(curl -s -X POST "${BASE_URL}/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Phase 3 Vector Search Test",
    "content": "BomTS Dev AI is a domain-neutral AI backend portfolio. It demonstrates document ingestion, chunking, embedding, Qdrant vector indexing, and semantic search.",
    "source": "phase3-check-script",
    "license": "private"
  }')"

echo "${DOC_RESPONSE}"

DOCUMENT_ID="$(echo "${DOC_RESPONSE}" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')"

if [ -z "${DOCUMENT_ID}" ]; then
  echo "ERROR: failed to parse document id"
  exit 1
fi

echo "DOCUMENT_ID=${DOCUMENT_ID}"

echo
echo "4) Create chunks"
CHUNK_RESPONSE="$(curl -s -X POST "${BASE_URL}/documents/${DOCUMENT_ID}/chunks")"
echo "${CHUNK_RESPONSE}"

echo "${CHUNK_RESPONSE}" | grep -q "chunk_index" || {
  echo "ERROR: chunk creation failed"
  exit 1
}

echo
echo "5) Index document chunks into Qdrant"
INDEX_RESPONSE="$(curl -s -X POST "${BASE_URL}/documents/${DOCUMENT_ID}/index")"
echo "${INDEX_RESPONSE}"

echo "${INDEX_RESPONSE}" | grep -Eq "indexed|count|success|document_id" || {
  echo "ERROR: indexing response does not look successful"
  exit 1
}

echo
echo "6) Search indexed chunks"
SEARCH_RESPONSE="$(curl -s -X POST "${BASE_URL}/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this project demonstrate?",
    "limit": 5
  }')"

echo "${SEARCH_RESPONSE}" | python3 -m json.tool || echo "${SEARCH_RESPONSE}"

echo "${SEARCH_RESPONSE}" | grep -q "results" || {
  echo "ERROR: search response does not contain results"
  exit 1
}

echo "${SEARCH_RESPONSE}" | grep -q "score" || {
  echo "ERROR: search response does not contain score"
  exit 1
}

echo
echo "✅ Phase 3 OK: document ingestion, chunking, vector indexing, and search are working."
