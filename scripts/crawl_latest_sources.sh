#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-http://localhost:8771/api}"
LIMIT="${LIMIT:-10}"

echo "Crawling latest sources (limit: ${LIMIT})..."
curl -s -X POST "${API_BASE_URL}/sources/crawl-latest" \
  -H "Content-Type: application/json" \
  -d "{\"limit\": ${LIMIT}, \"translate\": true, \"index\": true}"

echo "Done."
