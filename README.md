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

## 구조
이 프로젝트는 완성형 서비스보다는 RAG의 내부 파이프라인을 직접 구현하여 설명 가능한 구조를 지향합니다. 학습 과정 및 의사결정 기록은 `docs/learning/` 및 `docs/decisions/` 에서 확인할 수 있습니다.
