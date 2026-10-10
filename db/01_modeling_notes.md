# BOMTS AI 운영 PostgreSQL 기준선 모델링 노트

## 범위와 방법

이 문서는 2026-10-10 현재 운영 중인 PostgreSQL 15 `bomts.public` 스키마를 읽기 전용으로 역설계한 기록이다. 운영 스키마의 테이블 8개, 컬럼 80개, 관계 6개와 현재 제약·인덱스를 `db/model.json`에 그대로 정본화한다. 이번 작업은 현 상태를 재현하는 기준선이며 운영 DB에 DDL을 실행하거나 문제를 함께 고치지 않는다.

## 현재 그대로 정본화하는 대상

| 엔터티 | 역할 | 현재 관계 |
|---|---|---|
| `documents` | 검색·답변의 원문 문서 | `document_chunks`의 부모, `crawled_pages`·`ai_reference_briefings`에서 선택 참조 |
| `document_chunks` | 문서를 검색 단위로 나눈 청크 | `documents`에 N:1, 삭제 시 CASCADE |
| `content_sources` | 크롤링 대상 출처 설정 | `crawled_pages`의 부모 |
| `crawled_pages` | 출처에서 수집한 페이지 | `content_sources`에 N:1 CASCADE, `documents`에 선택 N:1 SET NULL |
| `ask_logs` | 질문·답변·모델·지연시간 기록 | `ask_source_logs`·`feedback_logs`의 부모 |
| `ask_source_logs` | 질문에 사용한 검색 출처 기록 | `ask_logs`에 선택 N:1 CASCADE |
| `feedback_logs` | 질문 답변의 평점·의견 | `ask_logs`에 선택 N:1 CASCADE |
| `ai_reference_briefings` | AI 참고 브리핑과 색인 상태 | `documents`에 선택 N:1 SET NULL |

PostgreSQL이 관계형 데이터의 정본이다. Qdrant `documents` 컬렉션은 문서 청크의 파생 벡터 검색 저장소이며 별도 스냅샷으로 백업한다. 현재 애플리케이션은 Qdrant point ID에 `document_chunks.id`를 사용한다.

## 현재 업무 규칙과 가정

- 문서 하나는 여러 청크를 소유하고 문서를 삭제하면 청크도 삭제된다.
- 질문 로그 하나는 여러 출처 로그와 피드백을 소유하고 질문 로그를 삭제하면 종속 로그도 삭제된다.
- 콘텐츠 출처 하나는 여러 수집 페이지를 소유하고 출처를 삭제하면 수집 페이지도 삭제된다.
- 수집 페이지는 문서를 선택적으로 참조하며 문서 삭제 시 연결만 해제된다.
- 수집 페이지의 원본 URL은 중복될 수 없다.
- 이번 기준선은 구조 개선 없이 운영 스키마를 그대로 재현한다.
- 운영 테이블 8개의 소유자는 `bomts_app`이며 이 role은 `NOSUPERUSER NOCREATEDB NOCREATEROLE`이다.

## 현재 모델과 분리해 기록하는 문제

이 항목은 후속 마이그레이션 후보이며 이번 기준선 DDL에는 반영하지 않는다.

1. `ask_source_logs.document_id`와 `ask_source_logs.chunk_id`에는 FK가 없다. 로그 생성 시 참조 대상이 없어져도 고아 식별자가 남을 수 있다.
2. 현재 선언된 FK 6개의 자식 컬럼 모두에 독립 인덱스가 없다. PostgreSQL은 FK 인덱스를 자동 생성하지 않으므로 조인·부모 삭제 검사 성능을 별도 측정해야 한다.
3. `ask_logs`의 질문·답변과 `feedback_logs`의 의견은 개인정보를 포함할 수 있다. 보존 기간, 삭제 기준, 마스킹·분리 정책이 정해지지 않았다. `crawled_pages` 내용·작성자·URL도 같은 검토가 필요하다.
4. Qdrant point ID가 `document_chunks.id`에 의존한다. 청크 재생성·복원·ID 재할당 시 PostgreSQL과 Qdrant 정합성을 확인할 규칙과 재색인 절차가 필요하다.
5. 애플리케이션 기동 시 SQLAlchemy `create_all`에 의존한다. 기준선 확정 후 Alembic baseline과 버전형 마이그레이션으로 전환하는 별도 작업이 필요하다.
6. 여러 상태·분류 컬럼이 자유 텍스트이고 CHECK 또는 코드 테이블로 제한되지 않는다. 실제 값 분포를 확인한 뒤 업무 규칙으로 확정해야 한다.

## 개인정보 처리 현황

전용 사용자 엔터티는 없지만 질문, 답변, 피드백, 수집 본문, 작성자, URL에는 개인정보가 섞일 수 있다. 이번 기준선은 기존 컬럼을 이동하거나 `pi_` 테이블을 추가하지 않는다. 보존·삭제 정책이 승인되면 정본부터 바꾸고 마이그레이션으로 적용한다.

## 변화 시나리오

- Alembic 도입 시 이 기준선과 운영 스키마의 차이가 0인 revision에서 시작한다.
- Qdrant 컬렉션이 늘어나면 각 컬렉션의 관계형 정본, point ID 규칙, 스냅샷·복구 시험을 명시한다.
- 사용자 계정이나 비공개 업로드 문서를 추가하기 전에 PI 분리와 접근 제어를 별도 데이터 모델 작업으로 승인받는다.

## 열린 질문

- 질문·답변·피드백·수집 콘텐츠의 보존 기간과 삭제 책임자는 누구인가?
- `ask_source_logs.document_id`·`chunk_id`를 강한 FK로 둘지, 삭제 후에도 당시 참조값을 보존하는 감사 로그로 둘지?
- Qdrant 재색인의 정합성 기준과 실패 시 복구 순서를 어디까지 자동화할지?
