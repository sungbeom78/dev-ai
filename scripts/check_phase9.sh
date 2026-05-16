#!/usr/bin/env bash
set -euo pipefail

echo "===================================="
echo "Phase 9 Validation: Web Page Split & Newsletter UI"
echo "===================================="

# Check local files first
echo "Checking local files..."
if [ ! -f "web/index.html" ]; then
    echo "❌ Error: web/index.html is missing"
    exit 1
fi
if [ ! -f "web/docs.html" ]; then
    echo "❌ Error: web/docs.html is missing"
    exit 1
fi
if [ ! -f "web/test.html" ]; then
    echo "❌ Error: web/test.html is missing"
    exit 1
fi

echo "Checking keywords in HTML files..."
grep -q "AI 뉴스레터" web/index.html || { echo "❌ Error: 'AI 뉴스레터' not found in index.html"; exit 1; }
grep -q "프로젝트 문서" web/docs.html || { echo "❌ Error: '프로젝트 문서' not found in docs.html"; exit 1; }
grep -q "테스트 콘솔" web/test.html || { echo "❌ Error: '테스트 콘솔' not found in test.html"; exit 1; }
grep -q "API: Checking" web/index.html || { echo "❌ Error: API status panel not found in index.html"; exit 1; }

echo "Checking API Endpoints..."
curl -s http://localhost:8771/api/health | grep -q "status" || { echo "❌ Error: API health check failed"; exit 1; }
curl -s http://localhost:8771/api/system/status | grep -q "online" || { echo "❌ Error: API system status check failed"; exit 1; }

echo "Phase 9 validation complete! ✨"
exit 0
