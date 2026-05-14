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

## 데이터베이스 초기화
현재 MVP 단계(Phase 2)에서는 Alembic과 같은 복잡한 마이그레이션 도구를 배제하고, FastAPI 앱 구동 시(`lifespan` 이벤트) `Base.metadata.create_all()`을 호출하여 PostgreSQL에 `documents`, `document_chunks` 테이블을 자동 생성합니다.

## API 테스트 (Phase 2)

### 1. 문서 등록
```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "BomTS Dev AI Intent",
    "content": "This project is a portfolio for AI backend development using FastAPI, PostgreSQL, Qdrant, and RAG.",
    "source": "manual",
    "license": "private"
  }'
```

### 2. 문서 목록 조회
```bash
curl http://localhost:8000/documents
```

### 3. 문서 청킹 (Chunking) 실행
```bash
curl -X POST http://localhost:8000/documents/1/chunks
```

### 4. 청크 목록 조회
```bash
curl http://localhost:8000/documents/1/chunks
```
