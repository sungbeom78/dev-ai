# BomTS Dev AI

AI 백엔드 개발자 지원용 포트폴리오 프로젝트입니다. FastAPI, PostgreSQL, Qdrant를 활용한 최소 RAG(Retrieval-Augmented Generation) 백엔드 MVP입니다.

## 주요 문서
- [프로젝트 의도 및 채용 포트폴리오 목적](docs/01_intent.md)
- [초기 아키텍처](docs/02_architecture.md)
- [개발 가이드](docs/00_dev_guide.md)

## 실행 방법

### 요구 사항
- Docker 및 Docker Compose

### 실행
1. 환경 변수 파일 생성
   ```bash
   cp .env.example .env
   ```
2. Docker Compose 실행
   ```bash
   docker compose up -d
   ```
3. 상태 확인
   ```bash
   curl http://localhost:8000/health
   ```

## 구조 및 설계
- 이 프로젝트는 완성형 서비스보다는 RAG의 내부 파이프라인을 직접 구현하여 설명 가능한 구조를 지향합니다.
- 기술적 의사결정과 학습 내용은 `docs/learning/` 및 `docs/decisions/`에 기록합니다.
  - [Document Ingestion과 Chunking 학습 기록](docs/learning/document-ingestion.md)
  - [Qdrant 도입 의사결정](docs/decisions/0001-choose-qdrant.md)
  - [컨테이너 네트워크 및 포트 정책](docs/decisions/0002-container-network-and-port-policy.md)
  - [도메인 중립적 AI 포트폴리오 원칙](docs/decisions/0003-domain-neutral-ai-portfolio.md)
  - [Local LLM의 선택적(Optional) Provider 채택 방향](docs/decisions/0004-local-llm-optional-provider.md)
  - [LLM Provider 추상화 설계](docs/decisions/0005-llm-provider-abstraction.md)
  - [Web UI 배포 및 포트 정책 (8771)](docs/decisions/0006-web-ui-port-8771.md)
  - [LangGraph를 활용한 Agent Workflow 도입](docs/decisions/0007-use-langgraph-for-agent-workflow.md)
  - [평가 로깅 및 피드백 기능 도입](docs/decisions/0008-add-evaluation-logging.md)
  - [Vector DB 기초](docs/learning/vector-db-basics.md)
  - [임베딩(Embedding) 기초](docs/learning/embedding-basics.md)
  - [RAG 파이프라인 기초](docs/learning/rag-pipeline.md)
  - [Prompt Building 전략](docs/learning/prompt-building.md)
  - [Web UI를 통한 RAG 시각화](docs/learning/web-ui.md)
  - [LangGraph 기초 및 구현](docs/learning/langgraph-basics.md)
  - [Agent Workflow 도입 이유](docs/learning/agent-workflow.md)
  - [AI 서비스의 평가와 피드백](docs/learning/evaluation-and-feedback.md)
  - [AI 관찰 가능성 (Observability) 기초](docs/learning/ai-observability.md)
  - [AI 트렌드 자동 수집 파이프라인 (Phase 8)](docs/learning/ai-trend-pipeline.md)
  - [안전한 웹 크롤링 정책](docs/learning/web-crawling-policy.md)
  - [AI Trend Source Pipeline 도입 의사결정](docs/decisions/0009-add-ai-trend-source-pipeline.md)
  - [Reference Pipeline 안정화 및 문서화](docs/decisions/0010-reference-pipeline-stabilization.md)
  - [Reference Pipeline 개요](docs/learning/reference-pipeline-overview.md)

## Current Capabilities (현재 제공 기능)

- **Manual Document Ingestion**: 직접 문서나 메모를 등록 (`POST /documents`, UI 섹션 1)
- **Chunking**: 문서를 적절한 크기로 분할 (`POST /documents/{id}/chunks`, UI 섹션 2)
- **Vector Indexing**: 청크를 임베딩하여 Vector DB에 저장 (`POST /documents/{id}/index`, UI 섹션 2)
- **Semantic Search**: 의미 기반 검색 (`POST /search`, UI 섹션 3)
- **RAG Ask**: 검색 기반 LLM 답변 생성 (`POST /ask`, UI 섹션 4)
- **LangGraph Agent Ask**: 의도 분석 및 라우팅 에이전트 (`POST /agent/ask`, UI 섹션 5)
- **Evaluation Logs / Feedback**: 답변 평가 및 피드백 기록 (`GET /logs/asks`, `POST /logs/asks/{id}/feedback`, UI 섹션 6)
- **AI Engineering Reference Source 등록**: 크롤링 대상 소스 관리 (`GET /sources`, `POST /sources`, UI 섹션 7)
- **URL 기반 Reference 수집**: 특정 URL 문서 수집 및 정규화 (`POST /sources/fetch-url`, UI 섹션 7)
- **Reference 질의응답**: 수집된 AI 개발 문서를 기반으로 답변 (`POST /agent/ask`, UI 섹션 8)

### 현재 한계 (Limitations)
- 현재 크롤러는 공개 페이지와 단일 URL 수집을 중심으로 작동합니다.
- JavaScript 렌더링이 필수적인 동적 페이지는 아직 추출이 제한적입니다.
- robots.txt와 rate limit 정책을 준수하므로 대규모 연속 수집보다는 필요한 문서 중심의 수집을 지향합니다.
- Reference Pipeline은 자동 뉴스 수집기가 아니라 AI 개발 참고자료 관리 시스템입니다. 요약 및 적용 메모(Application Note)는 아직 기초적인 수준입니다.
- Local LLM은 선택 기능이며 항상 연결되는 운영 의존성이 아닙니다.

## 단일 진입점 (Single Entrypoint) 정책
이 프로젝트는 `http://localhost:8771` 포트 단일 진입점을 제공합니다. Nginx 리버스 프록시가 적용되어 다음과 같이 요청을 분기합니다.
- `http://localhost:8771/`: Web UI(정적 파일) 제공
- `http://localhost:8771/api/`: FastAPI 백엔드로 리버스 프록시 (내부 8000 포트)
기존 개발용 8000 포트는 유지되나, 실제 서비스 접근 및 포트폴리오 시연 시에는 8771 포트를 사용합니다.

## 데이터베이스 초기화
현재 MVP 단계(Phase 2)에서는 Alembic과 같은 복잡한 마이그레이션 도구를 배제하고, FastAPI 앱 구동 시(`lifespan` 이벤트) `Base.metadata.create_all()`을 호출하여 PostgreSQL에 `documents`, `document_chunks` 테이블을 자동 생성합니다.

## Web UI 사용 방법 (Phase 5)
브라우저에서 전체 RAG 워크플로우를 시각적으로 테스트할 수 있습니다.
- **Web UI URL**: `http://localhost:8771`
- **API URL**: `http://localhost:8000` (Phase 5 기준)
  
Web UI에서 지원하는 기능:
1. 문서 텍스트 직접 입력 및 등록
2. 문서 목록 조회 및 선택
3. 문서 청킹(Chunking) 생성
4. Qdrant 벡터 인덱싱(Indexing)
5. 의미론적 유사도 검색(Semantic Search)
6. LLM 기반 답변 생성(RAG Ask) 및 참고 소스, Latency 확인

## 외부 노출 포트 정책
- 서버 호스트의 불필요한 포트 노출을 방지하기 위해 데이터베이스(PostgreSQL)와 Vector DB(Qdrant)는 Docker 내부 네트워크에서만 통신합니다.
- Phase 5까지는 개발 편의를 위해 API 컨테이너를 `8000` 포트로 노출하고 있습니다.
- 향후에는 Nginx의 Reverse Proxy를 통해 외부 노출 포트를 `8771` 하나로 줄이고, API 요청(`/api/*`)을 내부 네트워크로 라우팅하는 구조로 변경할 예정입니다.

## 검증 스크립트
각 단계별 검증 스크립트를 통해 전체 파이프라인이 올바르게 동작하는지 테스트할 수 있습니다.
```bash
# Phase 3 검증 (문서 등록 -> 임베딩 -> 검색)
chmod +x scripts/check_phase3.sh
./scripts/check_phase3.sh

# Phase 4 검증 (LLM 답변 생성)
chmod +x scripts/check_phase4.sh
./scripts/check_phase4.sh

# Phase 5 검증 (Web UI 및 전체 통합 테스트)
chmod +x scripts/check_phase5.sh
./scripts/check_phase5.sh

# Phase 6 검증 (LangGraph Agent Workflow 테스트)
chmod +x scripts/check_phase6.sh
./scripts/check_phase6.sh

# Phase 7 검증 (평가 로깅 및 피드백 기능)
chmod +x scripts/check_phase7.sh
./scripts/check_phase7.sh

# Phase 7.5 검증 (Nginx API Proxy 및 단일 진입점)
chmod +x scripts/check_phase7_5.sh
./scripts/check_phase7_5.sh

# Phase 8 검증 (AI Trend Source Pipeline)
chmod +x scripts/check_phase8.sh
./scripts/check_phase8.sh

# Phase 8.1 검증 (Reference Pipeline Stabilization)
chmod +x scripts/check_phase8_1.sh
./scripts/check_phase8_1.sh
```

## 외부 데이터 수집(Crawling) 사용법
Phase 8에 추가된 외부 AI 블로그 자동 수집 기능입니다.
```bash
# 기본 소스 목록 등록
docker compose exec api python scripts/seed_sources.py

# CLI 스크립트를 통한 특정 URL 수집
docker compose exec api python scripts/crawl_source.py --url https://example.com/article

# 특정 소스의 여러 문서 수집
docker compose exec api python scripts/crawl_source.py --source "Hugging Face Blog" --limit 3
```
