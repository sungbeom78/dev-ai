#!/usr/bin/env bash
set -euo pipefail

echo "===================================="
echo "R1 Validation: Reference Page"
echo "===================================="

# Check local files first
echo "Checking mock strings in HTML/JS files..."
if grep -q "(Mock)" web/index.html; then
    echo "❌ Error: '(Mock)' still found in web/index.html"
    exit 1
fi
if grep -q "AI 뉴스레터" web/index.html; then
    echo "❌ Error: 'AI 뉴스레터' still found in web/index.html"
    exit 1
fi
if ! grep -q "AI 기술 레퍼런스 검색" web/index.html; then
    echo "❌ Error: 'AI 기술 레퍼런스 검색' not found in web/index.html"
    exit 1
fi

echo "Checking API Endpoints..."
STATUS_API=$(curl -s http://localhost:8771/api/system/status)
if ! echo "$STATUS_API" | grep -q "api"; then
    echo "❌ Error: API system status check failed"
    exit 1
fi

DOCS_API=$(curl -s http://localhost:8771/api/trend/documents)
if ! echo "$DOCS_API" | grep -q "items"; then
    echo "❌ Error: API trend documents check failed"
    exit 1
fi

# We can't fully mock /ask in bash without LLM provider running, 
# but we check if the response format is okay if it returns 200
ASK_RES=$(curl -s -X POST http://localhost:8771/api/trend/ask -H "Content-Type: application/json" -d '{"question":"테스트 질문", "limit": 5}')
if echo "$ASK_RES" | grep -q "Based on the retrieved context"; then
    echo "❌ Error: English template string found in answer"
    exit 1
fi

if echo "$ASK_RES" | grep -iq "undefined"; then
    echo "❌ Error: 'undefined' found in ask response"
    exit 1
fi

echo "R1 validation complete! ✨"
exit 0
