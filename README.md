# BomTS Dev AI

개인 AI Engineering Knowledge Lab 및 AI 백엔드 포트폴리오 프로젝트입니다. 
문서 등록부터 RAG(Retrieval-Augmented Generation), Agent Workflow, Reference 크롤링까지의 과정을 직접 구현하고 학습할 수 있도록 설계되었습니다.

## 프로젝트 개요 (Project Overview)
이 프로젝트는 단순히 LLM API를 호출하는 데서 끝나지 않고, 실제 AI 서비스가 문서를 어떻게 수집하고 검색 가능한 지식으로 바꾸며, LLM에게 근거로 제공하고 결과를 평가/개선하는지 보여주는 것을 목표로 합니다.

## 왜 만들었는가 (Why I Built This)
AI 개발은 ChatGPT API를 호출하는 것으로 끝나지 않습니다. 실제 서비스에서는 문서, 개발 기록, 기술 레퍼런스 등을 수집해 검색 가능한 단위로 가공하고 Vector DB에 인덱싱하며, 사용자 질문에 맞는 context를 찾아 LLM에 전달하는 전체 파이프라인이 필요합니다.
이 과정을 직접 구현하여 RAG, Agent Workflow, Local LLM, MCP 등 최신 AI 기술을 학습하고 실제 개발 지원 체계로 연결하기 위해 만들었습니다.

## 전체 시스템 구조 (Architecture Overview)
```text
사용자 브라우저 -> Nginx Web Gateway (8771) -> FastAPI Application
                                                |
                              ----------------------------------
                              |                                |
                        PostgreSQL (원문/로그)      Qdrant (임베딩 벡터)
                              |                                |
                              ----------------------------------
                                                |
                             RAG / LangGraph Agent / LLM Provider
```

## RAG 파이프라인 흐름 (RAG Pipeline Overview)
1. 문서 등록 -> 2. Chunk 생성 -> 3. Embedding 생성 -> 4. Qdrant Vector Index 저장 -> 5. 사용자 질문 Embedding -> 6. Semantic Search -> 7. 검색 결과를 Context로 구성 -> 8. LLM 답변 생성 -> 9. Sources와 함께 응답 반환 -> 10. Logs/Feedback 저장

## 사용 기술 (Technology Stack)
- **Docker Compose**: 전체 서비스 로컬 통합 환경 구성
- **FastAPI**: RAG 백엔드 API 제공
- **PostgreSQL**: 문서 원본, 질문/답변 이력 및 피드백 영속 저장
- **Qdrant**: 의미 기반 유사도 검색을 위한 Vector DB
- **LangGraph**: 의도 분석 및 Agent 라우팅 (RAG, System Status, How-to 등)
- **Nginx**: Web UI 및 API Reverse Proxy

## 이 페이지를 어떻게 보는가 (How to Read the Web Page)
웹 페이지(`http://localhost:8771`)는 단순 테스트 콘솔이 아니라 파이프라인 단계별 학습용 설명서입니다. 
1. Ingest (문서 등록)
2. Chunk & Index (청킹 및 임베딩)
3. Search (의미 검색)
4. Ask (RAG 기반 응답)
5. Agent (LangGraph 의도 분류)
6. Evaluate (로그 및 피드백)
7. Reference (AI 문서 수집)

## 면접/포트폴리오 설명 포인트 (Portfolio Talking Points)
- **AI 백엔드 구조 이해**: LLM뿐만 아니라 문서 수집, Vector DB 검색, 평가까지의 RAG 전체 파이프라인 구축.
- **데이터 엔지니어링 및 RAG 연결**: ETL 구조와 유사한 문서 처리 과정 경험.
- **운영 가능한 구조 설계**: Docker Compose와 Nginx를 사용한 서비스 지향 아키텍처 구현.
- **Agent Workflow**: LangGraph를 통한 조건부 라우팅으로 단순 RAG의 한계 극복 실험.

---

## 주요 문서
- [프로젝트 의도 및 채용 포트폴리오 목적](docs/01_intent.md)
- [초기 아키텍처](docs/02_architecture.md)
- [개발 가이드](docs/00_dev_guide.md)
- [AI 트렌드 자동 수집 파이프라인 (Phase 8)](docs/learning/ai-trend-pipeline.md)
- [Reference Pipeline 안정화 및 문서화](docs/decisions/0010-reference-pipeline-stabilization.md)
- [Web UI 포트폴리오 설명 페이지 개편](docs/learning/web-portfolio-page.md)

## 실행 방법
```bash
cp .env.example .env
docker compose up -d
```

## 단일 진입점 (Single Entrypoint) 정책
- `http://localhost:8771/`: Web UI(정적 파일) 제공
- `http://localhost:8771/api/`: FastAPI 백엔드 리버스 프록시

## 검증 스크립트
각 단계별 파이프라인의 정상 동작 여부를 확인합니다.
```bash
./scripts/check_phase3.sh
./scripts/check_phase4.sh
./scripts/check_phase5.sh
./scripts/check_phase6.sh
./scripts/check_phase7.sh
./scripts/check_phase8.sh
./scripts/check_phase8_1.sh
./scripts/check_phase8_2.sh
```

## 외부 데이터 수집(Crawling) 사용법
```bash
docker compose exec api python scripts/seed_sources.py
docker compose exec api python scripts/crawl_source.py --url https://example.com/article
```
