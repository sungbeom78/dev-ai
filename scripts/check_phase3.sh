#!/bin/bash

# Exit on any error
set -e

echo "1. Checking Docker containers..."
docker compose ps

echo "2. Checking /health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health | grep '"status":"ok"')
if [ -z "$HEALTH" ]; then
  echo "Error: /health endpoint failed"
  exit 1
fi
echo "Health OK"

echo "3. Creating a test document..."
DOC_RESP=$(curl -s -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Phase 3 Test",
    "content": "This is a test document to verify Phase 3 vector indexing and search functionality.",
    "source": "test",
    "license": "private"
  }')
DOC_ID=$(echo $DOC_RESP | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
if [ -z "$DOC_ID" ]; then
  echo "Error: Document creation failed"
  exit 1
fi
echo "Document created with ID: $DOC_ID"

echo "4. Creating chunks..."
CHUNK_RESP=$(curl -s -X POST http://localhost:8000/documents/$DOC_ID/chunks)
if [[ $CHUNK_RESP != *"chunk_index"* ]]; then
  echo "Error: Chunk creation failed"
  exit 1
fi
echo "Chunks created."

echo "5. Indexing document..."
INDEX_RESP=$(curl -s -X POST http://localhost:8000/documents/$DOC_ID/index)
if [[ $INDEX_RESP != *"chunks_indexed"* ]]; then
  echo "Error: Document indexing failed"
  exit 1
fi
echo "Document indexed."

echo "6. Performing vector search..."
SEARCH_RESP=$(curl -s -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test document", "limit": 1}')

if [[ $SEARCH_RESP == *"results"* ]]; then
  echo "Phase 3 OK"
  exit 0
else
  echo "Error: Search failed or no results found in response"
  echo "Response: $SEARCH_RESP"
  exit 1
fi
