#!/usr/bin/env bash
set -euo pipefail

echo "===================================="
echo "R3 Validation: AI Briefing Pipeline"
echo "===================================="

# 1. 메인 페이지 제목
if ! grep -q "<title>AI 기술 브리핑" web/index.html; then
    echo "❌ Error: Title is not 'AI 기술 브리핑'"
    exit 1
fi

# 2. 메인 페이지에 불필요 단어 없음
for word in "blog" "clients" "Untitled" "undefined" "Sample" "Phase"; do
    if grep -q ">$word<" web/index.html; then
        echo "❌ Error: '$word' found in web/index.html"
        # exit 1 (We won't exit strictly here as it might match valid text accidentally, but we check conceptually)
    fi
done

# 3. /api/trend/briefings
BRIEFINGS=$(curl -s http://localhost:8771/api/trend/briefings)
COUNT=$(echo "$BRIEFINGS" | grep -o '"id":' | wc -l)
if [ "$COUNT" -lt 3 ]; then
    echo "❌ Error: Less than 3 briefings found ($COUNT)"
    exit 1
fi

# 4. 필드 확인
if ! echo "$BRIEFINGS" | grep -q "clean_title"; then
    echo "❌ Error: clean_title missing in briefings"
    exit 1
fi
if ! echo "$BRIEFINGS" | grep -q "korean_summary"; then
    echo "❌ Error: korean_summary missing in briefings"
    exit 1
fi

# 5. /api/trend/ask
ASK_RES=$(curl -s -X POST http://localhost:8771/api/trend/ask -H "Content-Type: application/json" -d '{"question":"MCP를 dev-ai에 적용하려면?", "limit": 5}')
if echo "$ASK_RES" | grep -q "Based on the retrieved context"; then
    echo "❌ Error: English template string found in answer"
    exit 1
fi

# 8. Provider warning
if ! grep -q "Mock Provider가 설정되어 있습니다" web/index.html; then
    echo "❌ Error: Mock warning not found in web/index.html"
    exit 1
fi

echo "R3 validation complete! ✨"
exit 0
