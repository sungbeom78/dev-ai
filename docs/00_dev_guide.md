# 개발 가이드

## 로컬 개발 환경 설정
1. 이 저장소를 클론합니다.
2. `.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 값을 입력합니다.
   ```bash
   cp .env.example .env
   ```
3. Docker Compose를 사용하여 컨테이너를 실행합니다.
   ```bash
   docker compose up -d
   ```

## 디렉터리 구조
- `app/`: FastAPI 애플리케이션 코드가 위치합니다.
  - `api/`: API 라우터 정의
  - `core/`: 설정, 보안, 공통 의존성 등
  - `db/`: 데이터베이스 연결 및 모델
  - `rag/`: RAG 핵심 모듈 (chunking, embedding 등)
  - `schemas/`: Pydantic 스키마
  - `services/`: 비즈니스 로직
- `docs/`: 프로젝트 관련 문서
  - `decisions/`: 기술적 의사결정 기록 (ADR)
  - `learning/`: 학습 로깅 및 트러블슈팅 기록
- `docker/`: Docker 관련 설정 파일 및 스크립트

## 코딩 컨벤션
- PEP 8 스타일 가이드를 따릅니다.
- Black, isort를 사용하여 코드를 포매팅합니다.
- 함수와 클래스에는 명확한 Type Hinting과 Docstring을 작성합니다.
