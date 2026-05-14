#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://localhost:8000}"

echo "== BomTS Dev AI Phase 6 Check =="

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
echo "3) Running previous phase checks..."
bash scripts/check_phase3.sh > /dev/null
bash scripts/check_phase4.sh > /dev/null
echo "Previous phases OK"

echo
echo "4) Testing Agent Ask API with different intents"

# Helper function to test intent
test_intent() {
    local question="$1"
    local expected_intent="$2"
    
    echo "  -> Question: '$question'"
    local response=$(curl -s -X POST "${API_URL}/agent/ask" \
      -H "Content-Type: application/json" \
      -d "{\"question\": \"${question}\", \"limit\": 3}")
      
    local intent=$(echo "$response" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("intent", ""))')
    
    if [ "$intent" != "$expected_intent" ]; then
        echo "     ❌ ERROR: Expected intent '$expected_intent', got '$intent'"
        echo "$response"
        exit 1
    fi
    echo "     ✅ Intent matched: $intent"
}

test_intent "What is BomTS Dev AI?" "rag_query"
test_intent "What can this system do?" "system_status"
test_intent "How do I register a document?" "how_to_use"
test_intent "Should I buy this stock?" "out_of_scope"
test_intent "Help" "needs_clarification"

echo
echo "✅ Phase 6 OK: LangGraph Agent Workflow is fully operational."
