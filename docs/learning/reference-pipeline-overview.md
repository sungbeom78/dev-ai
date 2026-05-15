# Reference Pipeline 개요

## 1. 수동 문서 등록의 한계
초기 RAG(Phase 1~7)는 사용자가 수동으로 텍스트를 입력해야만 작동했습니다. 
하지만 AI 기술(프레임워크, LLM 모델 가이드, MCP 등)은 매일같이 새롭게 갱신되며, 이를 일일이 복사/붙여넣기 하는 것은 실질적인 AI Engineering Knowledge Lab 역할을 수행하기 어렵습니다. 

## 2. Reference Pipeline이 필요한 이유
최신 AI 개발 트렌드와 기술 공식 문서를 수집하여, 프로젝트에 곧바로 적용할 수 있는 지식(Actionable Knowledge)으로 전환하기 위해 도입했습니다.
이 파이프라인을 통해 "새로운 프레임워크가 출시되었다"라는 뉴스를 넘어, "이 프레임워크를 어떻게 우리 코드에 적용할 수 있는가?"를 묻고 답할 수 있는 기반이 마련됩니다.

## 3. Reference Data 구조의 이해
파이프라인은 단순히 텍스트만 긁어오는 것이 아니라 지식을 단계별로 정제할 수 있는 잠재력을 가집니다.
- **Raw Reference**: 크롤러가 수집한 블로그나 공식 문서의 원본 텍스트입니다. (현재 구현된 단계)
- **Summary**: 긴 원문을 AI가 요약한 핵심 정보입니다. (향후 단계)
- **Application Note**: "이 기술을 BomTS Dev AI 프로젝트에 어떻게 적용할까?"에 대한 통찰이 담긴 메모입니다. (향후 단계)

## 4. 기술 트렌드에서 프로젝트 지식으로의 전환
1. **Fetch & Extract**: `trafilatura`를 통해 노이즈(광고, 헤더, 푸터)를 제거한 본문을 추출합니다.
2. **Ingest**: 문서 객체(`Document`)로 저장되며 `Reference` 태그가 붙습니다.
3. **Chunk & Index**: 기존의 텍스트 분할 알고리즘을 거쳐 Qdrant에 임베딩됩니다.
4. **Agent Retrieval**: 사용자가 "이 새로운 기능 어떻게 써?" 라고 물어보면 LangGraph 에이전트가 Reference 문서를 찾아내 응답합니다.

## 5. 향후 연동 방향 (Future Scope)
현재는 기본적인 수집(Single URL, 정적 블로그 위주)만 지원합니다. 
앞으로는 **Model Context Protocol (MCP)** 등을 활용하여 외부 IDE(Codex/Claude/Antigravity)가 이 지식 베이스에 직접 접근하거나, **Reference Discovery Agent**가 자율적으로 최신 문서를 수집하고 요약본(Application Note)을 자동 작성하는 방향으로 발전해 나갈 수 있습니다.
