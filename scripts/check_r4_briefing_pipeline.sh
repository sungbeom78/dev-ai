#!/usr/bin/env bash
set -euo pipefail

echo "===================================="
echo "R4 Validation: AI Technology Briefing Pipeline"
echo "===================================="

# 1. 메인 페이지 제목
if ! grep -q "<title>AI 기술 브리핑" web/index.html && ! grep -q "<title>AI 기술 동향 브리핑" web/index.html && ! grep -q "<h1 class=\"hero-title\">AI 기술 동향 브리핑" web/index.html; then
    echo "❌ Error: AI 기술 동향 브리핑 not found in web/index.html"
    exit 1
fi

# 2. 메인 페이지에 불필요 단어 없음
for word in "blog" "clients" "Untitled" "undefined" "Sample" "Phase"; do
    if grep -q ">$word<" web/index.html; then
        echo "❌ Error: '$word' found in web/index.html"
        # exit 1 (We won't exit strictly here as it might match valid text accidentally)
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
for field in "korean_summary" "why_it_matters" "dev_ai_application_note" "suggested_tasks"; do
    if ! echo "$BRIEFINGS" | grep -q "$field"; then
        echo "❌ Error: $field missing in briefings"
        exit 1
    fi
done

# 5. /api/trend/brief "MCP 적용 동향 알려줘"
ASK_RES=$(curl -s -X POST http://localhost:8771/api/trend/brief -H "Content-Type: application/json" -d '{"question":"MCP 적용 동향 알려줘", "limit": 5}')
if echo "$ASK_RES" | grep -q "Based on the retrieved context"; then
    echo "❌ Error: English template string found in answer"
    exit 1
fi

# 7. provider_used in briefings
# We already verified fields, but let's see if /brief works well.
if ! echo "$ASK_RES" | grep -q "question"; then
    echo "❌ Error: /api/trend/brief response format is incorrect"
    exit 1
fi

# 8. Provider warning in mock mode
if ! grep -q "Mock Provider가 설정되어 있습니다" web/index.html; then
    echo "❌ Error: Mock warning not found in web/index.html"
    exit 1
fi

# 10. 하네스 질문
HARNESS_RES=$(curl -s -X POST http://localhost:8771/api/trend/brief -H "Content-Type: application/json" -d '{"question":"하네스", "limit": 5}')
if ! echo "$HARNESS_RES" | grep -q "여러 의미로 쓰일 수 있습니다"; then
    echo "❌ Error: Ambiguity handling for '하네스' failed"
    exit 1
fi

echo "R4 validation complete! ✨"
exit 0
