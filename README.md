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
```
