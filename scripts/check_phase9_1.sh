#!/usr/bin/env bash
set -euo pipefail

echo "===================================="
echo "Phase 9.1 Validation"
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
if ! grep -q "AI 기술 트렌드 검색 시스템" web/index.html; then
    echo "❌ Error: 'AI 기술 트렌드 검색 시스템' not found in web/index.html"
    exit 1
fi

echo "Checking API Endpoints..."
curl -s http://localhost:8771/api/trend/documents | grep -q "items" || { echo "❌ Error: API trend documents check failed"; exit 1; }

echo "Phase 9.1 validation complete! ✨"
exit 0
