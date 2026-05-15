# 의사결정: Reference Pipeline 안정화 및 문서화 (Phase 8.1)

## 상황 (Context)
Phase 8에서 `trafilatura`와 `BeautifulSoup4`를 도입하여 외부 URL을 수집하고 RAG 파이프라인에 연결하는 AI Trend Source Pipeline을 구현했습니다.
하지만 기능이 막 추가된 상태여서, 사용자가 Web UI에서 어떤 목적으로 이 기능을 사용해야 하는지 한눈에 파악하기 어렵고, 실제 어떻게 기술 레퍼런스로 활용되는지 설명이 부족했습니다.

## 결정 (Decision)
**새로운 기능을 추가하는 대신 Phase 8의 산출물을 정리하고 설명 가능한 상태로 안정화(Stabilization)하기로 결정했습니다.**
1. Web UI의 각 섹션에 기능의 목적과 한계를 명시하는 설명을 추가했습니다.
2. `seed_sources.py`를 AI Engineering(LangGraph, MCP, Qdrant 등)에 특화된 Reference Source 중심으로 개편했습니다.
3. 외부 네트워크나 차단에 의존하지 않고도 전체 파이프라인을 검증할 수 있는 `check_phase8_1.sh`를 추가했습니다.

## 이유 (Rationale)
1. **포트폴리오의 완성도는 '설명 가능성'에서 옵니다.** 코드가 돌아간다는 것만으로는 부족하며, 면접관이나 리뷰어가 페이지에 들어왔을 때 "무엇을 누르면 어떤 결과가 나오는지" 즉시 이해해야 합니다.
2. 파이프라인의 목적을 "단순한 뉴스 크롤링"이 아니라 **"AI 개발을 위한 기술 참고자료(Reference) 관리 시스템"**으로 명확히 규정하기 위함입니다.
3. 이 안정화를 거쳐야만 다음 단계(Phase 9)인 자율형 Agent 연동이나 MCP(Model Context Protocol) 도입을 탄탄한 기초 위에서 진행할 수 있습니다.

## 결과 (Consequences)
- README.md에 `Current Capabilities`가 명확히 정리되었습니다.
- 현재의 한계(동적 렌더링 한계, 자동 요약 미지원 등)가 명시되어, 시스템이 해결하지 못한 부분을 솔직하고 명확히 파악할 수 있습니다.
- 로컬 환경에서도 외부 서버 상태와 무관하게(Bypassing External Fetch) 파이프라인 전체 워크플로우를 신뢰성 있게 자동 테스트(check_phase8_1.sh)할 수 있게 되었습니다.
