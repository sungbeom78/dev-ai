#!/usr/bin/env bash
set -euo pipefail

curl -fsS --max-time 5 \
  http://127.0.0.1:8000/health \
  >/dev/null

curl -fsS --max-time 30 \
  -H 'Content-Type: application/json' \
  --data '{"query":"RAG pipeline","limit":1}' \
  http://127.0.0.1:8000/search \
  >/dev/null
