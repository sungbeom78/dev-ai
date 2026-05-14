# BomTS AI Path — 개발 지침서

> 이 문서는 BomTS AI Path 프로젝트에 참여하는 모든 개발자(사람 또는 AI 코딩 에이전트)가
> 가장 먼저 읽고, 작업 중에도 수시로 참조해야 하는 **단일 기준 문서(Single Source of Truth)** 다.
> 구현 디테일보다 **"왜 이렇게 만드는가"** 를 먼저 합의하기 위한 문서다.

---

## 0. 이 문서를 읽는 사람에게

이 프로젝트는 단순한 토이 프로젝트가 아니다.
**16년차 데이터 엔지니어가 AI 백엔드 개발자로 직무 전환을 검증하기 위한 포트폴리오이자 실험장**이다.

따라서 다음을 항상 의식하고 작업한다.

1. **모든 코드와 문서는 외부 공개를 전제로 한다.** 면접관, 채용 검토자, 다른 개발자가 본다.
2. **"동작하는 것"보다 "설명 가능한 것"이 더 중요하다.** 면접에서 설명할 수 없는 코드는 의미가 없다.
3. **모르는 것을 모른다고 적는 것이 약점이 아니라 강점이다.** 학습 로그(`docs/learning/`)는 이 프로젝트의 핵심 산출물 중 하나다.
4. **빠른 동작 > 완벽한 설계.** 단, 학습 과정과 의사결정 근거는 반드시 문서로 남긴다.

---

## 1. 프로젝트 정체성

### 1.1. 프로젝트명
**BomTS AI Path**

### 1.2. 도메인
`https://ai.bomts.net`

### 1.3. 한 줄 정의
> LLM, RAG, Agent, Vector DB, Docker를 직접 학습하고 실제 서비스 형태로 구현하는,
> AI 백엔드 개발자 전환을 위한 포트폴리오형 실험 프로젝트.

### 1.4. 비교 참조
같은 운영자(`bomts`)의 기존 프로젝트인 [AA Web Path](https://aa.bomts.net)와 동일한 철학을 따른다.
- 개념(Concept) → 실험(Lab) → 데모(Demo) → 운영(Deployment) → 회고(Retrospective)
- 단순 결과물이 아닌 **사고 과정이 보이는 사이트**
- 학습 로그를 결과물의 일부로 취급

### 1.5. 이 프로젝트가 겨냥하는 직무
다우기술 디지털혁신그룹 AX개발팀(또는 유사 포지션)의 AI 백엔드 개발자.
공고의 핵심 요구사항:
- Python/FastAPI 기반 백엔드 개발
- RAG 파이프라인 설계 (Vector DB, Hybrid Search)
- LangChain/LangGraph 기반 Agent/Workflow
- 데이터 처리 파이프라인 구축
- Docker 기반 배포

---

## 2. 핵심 의도 (Intent)

### 2.1. 무엇을 보여주는 프로젝트인가

이 프로젝트는 면접관에게 다음 메시지를 전달해야 한다.

> **"이 사람은 AI 기능을 실제 서비스 백엔드로 설계하고 운영할 수 있다."**
> **"이 사람은 모르는 기술도 구조화해서 빠르게 학습하고, 실제 동작하는 서비스로 연결한다."**
> **"이 사람은 16년의 데이터 엔지니어링 경험을 AI 파이프라인 설계에 자연스럽게 적용한다."**

### 2.2. 무엇을 보여주는 프로젝트가 아닌가

- 최신 LLM 연구를 따라잡는 프로젝트가 아니다.
- 모델을 직접 학습/파인튜닝하는 프로젝트가 아니다.
- 화려한 프론트엔드를 만드는 프로젝트가 아니다.
- 완벽한 SaaS를 만드는 프로젝트가 아니다.

### 2.3. 운영자(개발자)의 배경 가정

- **강점:** 16년 데이터 엔지니어링, ETL 설계/운영, 데이터 모델링(SQLP/DAP 보유), 대용량 게임 데이터 파이프라인, 모니터링/Alert 시스템 자동화 경험
- **약점(학습 중):** Docker, Vector DB, LLM/RAG 실무, FastAPI 기반 모던 백엔드 운영

이 약점은 **숨기지 않고 학습 로그로 명시화한다.**
면접에서 "Docker 잘 압니까?"가 아니라 "Docker를 어떤 식으로 학습하고 적용했습니까?"로 대화가 흐르도록 만든다.

---

## 3. 방향 원칙 (Direction Principles)

작업 중 결정이 필요할 때마다 다음 원칙으로 판단한다.

### 원칙 1. AI 연구가 아닌 AI 서비스 개발
모델 성능 0.5% 개선보다 **구조 분리, 명확한 API, 운영 가능성**을 우선한다.

### 원칙 2. 학습 과정을 산출물로 취급
Docker, Vector DB, RAG 모두 학습 단계다. 학습한 내용은 `docs/learning/` 아래에 반드시 기록한다.
"잘 아는 척"하지 않는다. "모르는 것을 어떻게 학습했는가"가 강점이다.

### 원칙 3. 데이터 엔지니어 경력의 연속선임을 드러낸다
RAG의 인덱싱 파이프라인을 설계할 때는, ETL 설계와의 유사점/차이점을 의도적으로 문서화한다.
- chunking ↔ 데이터 분할 전략
- embedding 저장 ↔ DW 적재
- 검색 품질 평가 ↔ 데이터 품질 모니터링
- LLM 응답 검증 ↔ QA 시나리오 검증

이 연결고리가 이 프로젝트의 차별점이다.

### 원칙 4. 설명 가능한 RAG
LangChain의 high-level abstraction을 무비판적으로 쓰지 않는다.
**RAG의 각 단계(질문 임베딩 → 검색 → 컨텍스트 구성 → 프롬프트 → 응답)를 코드 레벨에서 설명할 수 있어야 한다.**
LangChain을 쓰더라도 핵심 흐름은 별도 모듈로 분리해 직접 작성한다.

### 원칙 5. 작은 것을 먼저 띄운다
완성된 LangGraph Multi-Agent를 6개월 만에 띄우는 것보다,
**4주 안에 Docker로 뜨는 단순 RAG API**가 100배 가치 있다.

### 원칙 6. 모든 결정은 문서로 남는다
기술 선택, 라이브러리 비교, 실험 결과는 `docs/decisions/` 에 ADR(Architecture Decision Record) 형태로 기록한다.
면접에서 "왜 Qdrant 골랐어요?"에 답할 수 있어야 한다.

---

## 4. 범위 (Scope)

### 4.1. MVP (Phase 1~4) — 4주 목표

다음 기능까지만 MVP로 정의한다.

- [ ] Docker Compose 기반 실행 환경 (FastAPI + PostgreSQL + Qdrant)
- [ ] Health check 엔드포인트
- [ ] 문서 등록 API (마크다운/텍스트)
- [ ] Chunking 로직 (최소 1가지 전략)
- [ ] Embedding 생성 (OpenAI API 우선)
- [ ] Qdrant 저장 및 검색
- [ ] RAG 기반 `/ask` API (질문 → 검색 → LLM 응답 → 출처 반환)
- [ ] 최소한의 데모 화면 (질문 입력, 응답·출처 표시)
- [ ] README, 아키텍처 문서, 학습 로그 3편 이상

### 4.2. Phase 5~7 — 확장 목표

MVP가 안정화된 후 진행.

- [ ] Hybrid Search 실험 (Qdrant sparse + dense, BM25 가중치 비교)
- [ ] LangGraph 기반 단순 Agent Workflow (질문 분류 → 검색 분기 → 응답)
- [ ] 검색 품질 평가 로그 (질문, 검색 결과 score, 사용자 피드백 저장)
- [ ] 실패 케이스 분석 페이지
- [ ] Architecture / Monitoring / Retrospective 페이지

### 4.3. Non-Goal (명시적으로 안 한다)

- ❌ 자체 LLM 학습/파인튜닝
- ❌ 투자 추천/매수·매도 판단 (도메인 안전성)
- ❌ 자체 GPU 모델 서빙 (vLLM은 초기 범위 밖, 학습 로그로만 다룸)
- ❌ Graph DB (학습 로그로만 다루고 실제 구현은 보류)
- ❌ MCP / A2A / Multi-Agent 전체 구현 (개념 문서 + 단순 실험까지만)
- ❌ 사용자 인증/권한 시스템 (포트폴리오 데모에 불필요)
- ❌ 화려한 UI/UX

---

## 5. 인프라 환경 (Infrastructure)

### 5.1. 실행 환경
- **호스트:** 개인 NUC (Linux)
- **컨테이너:** Docker / Docker Compose
- **도메인:** `ai.bomts.net` (단일 도메인에 모든 컴포넌트 매핑)
- **리버스 프록시:** Nginx (또는 Caddy — 인증서 자동화 고려 시)
- **모든 서비스는 하나의 Docker Compose 스택 안에서 동작한다.**

### 5.2. 컴포넌트
1. `ai-api` — FastAPI 백엔드
2. `ai-web` — 정적 프론트엔드 (또는 Vite 빌드 결과물을 Nginx에 마운트)
3. `postgres` — 문서 metadata, 질문 로그, 평가 로그
4. `qdrant` — Vector DB
5. `nginx` — 리버스 프록시, TLS 종단
6. (향후) `worker` — 비동기 인덱싱, `redis` — 큐, `monitoring` — Prometheus/Grafana

### 5.3. 환경변수 관리
- `.env.example` 만 git에 포함
- 실제 `.env`, OpenAI API key, DB 비밀번호는 절대 git에 포함 금지
- `pre-commit` 훅으로 secret 누출 방지 (예: `detect-secrets`)

---

## 6. 기술 스택

### 6.1. 확정
- **언어:** Python 3.11+
- **웹 프레임워크:** FastAPI + Uvicorn
- **데이터 검증:** Pydantic v2
- **RDB:** PostgreSQL 16
- **Vector DB:** Qdrant
- **컨테이너:** Docker, Docker Compose
- **LLM:** OpenAI API (gpt-4o-mini 우선, 비용 관리 위해)
- **Embedding:** OpenAI `text-embedding-3-small` 우선
- **테스트:** pytest

### 6.2. 선택적 도입
- **LangChain:** 사용하되, 핵심 RAG 흐름은 직접 구현. LangChain은 보조 도구로만.
- **LangGraph:** Phase 6에서 도입.
- **프론트엔드:** Vite + React (또는 단순 HTML+Alpine.js). AA Path와 톤 일치 우선.

### 6.3. 의도적으로 보류
- vLLM, Triton (학습 문서로만)
- Neo4j 등 Graph DB (학습 문서로만)
- Kafka, Airflow 같은 본격 파이프라인 도구 (오버킬)

---

## 7. 아키텍처 (초기)

```
                       [User Browser]
                             |
                             v
                       [Nginx (TLS)]
                       /            \
                      v              v
              [ai-web (static)]  [ai-api (FastAPI)]
                                       |
                  +-------------------- + --------------------+
                  |                     |                     |
                  v                     v                     v
           [Document Ingestion]   [Question Answering]   [Logging/Eval]
                  |                     |                     |
                  | chunking            | query embedding     | save query log
                  | embedding           | vector search       | save score
                  | metadata save       | context build       | save feedback
                  |                     | LLM generation      |
                  v                     v                     v
            [PostgreSQL]            [Qdrant]            [PostgreSQL]
```

**원칙:**
- API 레이어, RAG 코어 로직, 외부 서비스(LLM/Vector DB) 호출이 명확히 분리되어야 한다.
- RAG 핵심 모듈(`chunker`, `embeddings`, `vector_store`, `retriever`, `prompt_builder`, `answer_generator`)은 각각 독립적으로 단위 테스트 가능해야 한다.
- 외부 의존성(OpenAI, Qdrant)은 인터페이스로 추상화하여 교체 가능하게 둔다.

---

## 8. 디렉터리 구조

```
bomts-ai-path/
├─ app/
│  ├─ main.py                  # FastAPI entrypoint
│  ├─ api/
│  │  ├─ health.py
│  │  ├─ documents.py
│  │  └─ ask.py
│  ├─ core/
│  │  ├─ config.py             # 환경변수 로딩 (pydantic-settings)
│  │  ├─ logging.py
│  │  └─ exceptions.py
│  ├─ db/
│  │  ├─ session.py            # SQLAlchemy session
│  │  ├─ models.py             # ORM 모델
│  │  └─ migrations/           # Alembic
│  ├─ rag/
│  │  ├─ chunker.py
│  │  ├─ embeddings.py         # Embedding 모델 추상화
│  │  ├─ vector_store.py       # Qdrant 클라이언트 래퍼
│  │  ├─ retriever.py          # Hybrid search 포함
│  │  ├─ prompt_builder.py
│  │  └─ answer_generator.py   # LLM 호출
│  ├─ schemas/
│  │  ├─ document.py
│  │  └─ ask.py
│  └─ services/                # API와 RAG 사이의 use-case 계층
│     ├─ ingest_service.py
│     └─ ask_service.py
├─ web/                        # 프론트엔드 (Vite or static)
├─ docs/
│  ├─ 01_intent.md             # 이 프로젝트의 의도
│  ├─ 02_architecture.md
│  ├─ 03_mvp_scope.md
│  ├─ 04_tech_stack.md
│  ├─ decisions/               # ADR
│  │  ├─ 0001-choose-qdrant-over-chroma.md
│  │  ├─ 0002-use-postgres-for-metadata.md
│  │  └─ ...
│  └─ learning/                # 학습 로그
│     ├─ docker-basics.md
│     ├─ vector-db-comparison.md
│     ├─ rag-pipeline.md
│     ├─ embedding-models.md
│     ├─ chunking-strategies.md
│     └─ langgraph-first-look.md
├─ docker/
│  ├─ Dockerfile.api
│  ├─ nginx/
│  │  └─ default.conf
│  └─ init/                    # DB 초기화 스크립트
├─ tests/
│  ├─ unit/
│  └─ integration/
├─ scripts/
│  ├─ ingest_sample_docs.py
│  └─ eval_retrieval.py
├─ .env.example
├─ .gitignore
├─ .pre-commit-config.yaml
├─ docker-compose.yml
├─ pyproject.toml              # uv or poetry
├─ Makefile                    # make up / make test / make ingest
└─ README.md
```

---

## 9. 데이터 정책

### 9.1. 초기 데이터 소스
다음 문서를 코퍼스로 사용한다.

- BomTS 개인 프로젝트 설계 문서
- AA Path 기획/설계 문서 (공개 가능 범위)
- 이 프로젝트의 자체 문서(`docs/` 전체)
- AI 개념 정리 문서 (학습 로그)
- 공개된 기술 문서 (MIT/Apache 라이선스 등 명확한 것만)

### 9.2. 금지 데이터
- ❌ 전 직장(NCSOFT)의 모든 내부 자료
- ❌ 개인정보가 포함된 모든 데이터
- ❌ 투자/금융 추천 데이터
- ❌ 라이선스 불명 외부 콘텐츠

### 9.3. 데이터 거버넌스
- 모든 문서에는 `source`, `license`, `ingested_at` 메타데이터를 부여
- 추후 삭제 요청 시 vector + metadata 동시 삭제 가능한 구조로 설계

---

## 10. API 설계 (MVP 기준)

### 10.1. 엔드포인트

| Method | Path | 역할 |
|---|---|---|
| GET | `/health` | 헬스 체크 |
| POST | `/documents` | 문서 등록 (raw text/markdown) |
| GET | `/documents` | 문서 목록 |
| GET | `/documents/{id}` | 문서 단건 조회 |
| POST | `/documents/{id}/index` | 단건 인덱싱 (chunk + embed + store) |
| POST | `/reindex` | 전체 재인덱싱 |
| POST | `/ask` | 질의응답 |
| POST | `/ask/{ask_id}/feedback` | 응답 평가 저장 |

### 10.2. `/ask` 응답 표준

```json
{
  "ask_id": "uuid",
  "question": "원본 질문",
  "answer": "LLM 응답",
  "sources": [
    {
      "document_id": 1,
      "title": "architecture.md",
      "chunk_text": "...",
      "score": 0.82,
      "chunk_index": 3
    }
  ],
  "confidence": "high | medium | low",
  "retrieval_strategy": "dense | hybrid",
  "model": "gpt-4o-mini",
  "latency_ms": 1342
}
```

**`confidence` 산정 규칙은 별도 ADR로 문서화한다.**

---

## 11. 코드 품질 기준

- **포매터:** `ruff format`
- **린터:** `ruff check`
- **타입:** `mypy` (strict 모드는 점진적으로)
- **테스트 커버리지:** MVP 단계에서 RAG 핵심 모듈은 70%+ 목표
- **커밋 메시지:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`)
- **브랜치 전략:** main + feature branch + PR. PR 본인 셀프 리뷰 후 머지.
- **PR 설명에는 항상 다음을 포함:**
  1. 무엇을 변경했는가
  2. 왜 변경했는가
  3. 어떻게 검증했는가
  4. 학습 로그가 갱신되었는가

---

## 12. 검증 체크리스트 (각 단계 종료 시)

새 기능을 머지하기 전 다음을 점검한다.

1. [ ] 이 변경이 RAG 흐름의 어느 단계에 해당하는가, README에 반영되었는가?
2. [ ] Docker Compose를 처음 받는 개발자가 README만 보고 실행 가능한가?
3. [ ] Qdrant와 PostgreSQL의 역할 분리가 코드에서 명확한가?
4. [ ] `/ask` 응답에서 출처와 검색 점수가 확인되는가?
5. [ ] 환경변수/시크릿이 git에 포함되지 않았는가?
6. [ ] 면접에서 이 코드의 모든 의사결정을 설명할 수 있는가?
7. [ ] 학습한 새 개념이 있다면 `docs/learning/` 에 기록되었는가?
8. [ ] 외부에 공개되어도 문제없는 내용만 포함되었는가?

---

## 13. 개발 우선순위 (Phase별)

### Phase 0 — 기획/문서 (이 문서 + 추가 문서)
- `README.md` 초안
- `docs/01_intent.md`
- `docs/02_architecture.md`
- `docs/03_mvp_scope.md`
- `docs/04_tech_stack.md`
- 첫 ADR 2~3개

### Phase 1 — Docker 기본 환경
- `docker-compose.yml` (api + postgres + qdrant + nginx)
- `Dockerfile.api`
- `/health` 동작
- `docs/learning/docker-basics.md`

### Phase 2 — 문서 등록 파이프라인
- `POST /documents`, `GET /documents`, `GET /documents/{id}`
- PostgreSQL 스키마 + Alembic 마이그레이션

### Phase 3 — Embedding + Vector 저장
- chunking 전략 1종 구현 + 1종 비교 실험
- OpenAI embedding 호출
- Qdrant 컬렉션 설계 (payload 스키마 포함)
- `POST /documents/{id}/index`
- `docs/learning/vector-db-comparison.md`
- `docs/learning/chunking-strategies.md`

### Phase 4 — RAG 질문 API
- `POST /ask`
- 검색 → context → prompt → answer → source
- `confidence` 산정 로직
- `docs/learning/rag-pipeline.md`

### Phase 5 — 데모 UI
- 문서 목록 / 등록 / 질문 화면
- AA Path 스타일과 톤 일치

### Phase 6 — Agent Workflow (LangGraph)
- 질문 분류 → 검색 필요 여부 판단 → 검색/직답 분기 → 응답
- `docs/learning/langgraph-first-look.md`

### Phase 7 — 평가/모니터링
- 질문 로그 / 검색 score / 사용자 피드백 저장
- 실패 케이스 분석 페이지
- 회고 문서

---

## 14. AI 코딩 에이전트(Claude Code 등)에게 주는 행동 지침

이 프로젝트에서 코드를 생성·수정할 때는 다음을 지킨다.

1. **모르는 것을 추측하지 않는다.** 운영자(범)의 환경(NUC, 도메인 구성, 기존 BomTS 인프라)에 대한 가정이 필요하면 먼저 묻는다.
2. **LangChain의 마법 같은 한 줄 코드를 우선하지 않는다.** RAG 각 단계를 명시적으로 분리해서 작성한다.
3. **새 라이브러리를 도입할 때는 반드시 ADR을 함께 생성한다.**
4. **테스트 없는 핵심 RAG 모듈은 머지하지 않는다.**
5. **학습성 작업(Docker, Vector DB, LangGraph 등)을 진행할 때는 동시에 `docs/learning/` 문서를 작성한다.**
6. **운영자의 데이터 엔지니어링 배경을 의식한다.** chunking, embedding, retrieval 같은 개념을 설명할 때 ETL/DW 관점의 비유를 적극 사용한다.
7. **포트폴리오 목적임을 잊지 않는다.** 모든 결정의 끝에 "이걸 면접에서 설명할 수 있는가?"를 묻는다.

---

## 15. 면접에서 설명할 핵심 메시지 (역으로 설계 기준이 됨)

이 프로젝트가 완성되었을 때, 다음 질문에 답할 수 있어야 한다.

1. 왜 RAG를 직접 만들었나? — 데이터 엔지니어링 경험이 RAG 파이프라인으로 어떻게 연결되는지 설명할 수 있다.
2. 왜 Qdrant를 골랐나? — Chroma와의 비교, Docker 친화성, payload 모델, Hybrid Search 지원 측면에서 설명한다.
3. Chunking 전략은 어떻게 선택했나? — 최소 2가지 전략을 비교 실험한 결과를 제시한다.
4. 검색 품질을 어떻게 평가했나? — 평가 로그와 실패 케이스 분석을 제시한다.
5. Docker로 어떻게 배포했나? — Docker Compose 구조와 NUC 운영 경험을 설명한다.
6. Agent를 어디까지 도입했나? — LangGraph로 만든 단순 분기 Agent를 시연한다.
7. 운영하면서 어려웠던 점은? — 학습 로그와 회고 문서로 답한다.

**이 7개 질문에 막힘없이 답할 수 있는 상태가 이 프로젝트의 완성 조건이다.**

---

## 16. 변경 이력

| 일자 | 작성자 | 변경 내용 |
|---|---|---|
| 2026-05-14 | 초안 | 최초 작성 |

