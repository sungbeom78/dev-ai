# 최종 보고서 — 20261009-db-security

- 생성 시각: 2026-10-10T09:18:39.295233+00:00
- **최종 판정**: `completed`

## 1. 업무 의미
DB 노출·권한·비밀값 정리

## 완료 기준
- [x] #1 5432·6333·6334 포트가 127.0.0.1에만 열려 있다 -- met (sealed db_security_runtime d2d3bd45410e: 5432·6333·6334 각각 127.0.0.1 listener 1개, 0.0.0.0·[::] 없음)
- [x] #2 애플리케이션이 NOSUPERUSER NOCREATEDB NOCREATEROLE 전용 계정 bomts_app을 사용하고 public 스키마 객체를 소유한다 -- met (bomts_app=f/f/f, public 테이블 8개 모두 bomts_app 소유, pg_stat_activity에서 앱 접속 사용자 bomts_app 확인)
- [x] #3 비밀값은 저장소 밖 .env에 있고 .gitignore로 차단되며 .env.example에는 키 이름만 있다 -- met (.env gitignore 확인, .env.example 민감 키 값 비어 있음; 이전 비밀번호는 이력 7커밋에 있으나 교체되어 api→db 인증 거부, 이력 재작성 안 함)
- [x] #4 Qdrant API 키가 설정되고 애플리케이션 vector_store가 api_key를 사용한다 -- met (Qdrant 무키 401·키 포함 200, vector_store api_key 설정과 config invariant 검사 통과)
- [x] #5 PostgreSQL 전체 백업과 Qdrant 스냅샷이 저장소 밖에 있고 PostgreSQL 복구 시험에서 테이블 8개와 행 수가 일치한다 -- met (저장소 밖 pg_dump·Qdrant snapshot checksum OK; 임시 PostgreSQL 복구에서 8테이블·행 수 일치, 임시 컨테이너 제거 확인)
- [x] #6 승인 후 앱 health와 실제 질의 1건이 성공하고 Qdrant 무키 호출은 401이며 LAN DB 접속은 차단된다 -- met (최종 운영 검증: health 200, 실제 검색 200, Qdrant 무키 401·키 포함 200, 10분 로그 22줄·auth/connection 오류 0. 사용자 제공 독립 LAN PC 192.168.50.64의 Test-NetConnection 결과에서 192.168.50.221:5432 및 :6333 모두 TcpTestSucceeded=False; screenshot/text evidence 저장)

## 2. 실제 변경
PostgreSQL과 Qdrant를 loopback으로 제한하고 앱 전용 DB role, 외부 비밀값, Qdrant API 키, 백업·복구 및 운영 증거를 적용

## 3. 검증 근거
db_security_runtime=allow[verified]; db_security_sequence_recovery=allow[verified]; encoding=allow[verified]; identifier_audit=allow[verified]; lint=allow[verified]; prior_art=allow[reported_only]; qa_quick=allow[verified]; unit_or_regression=allow[verified]

## 4. 변경·복구 이력
db-security-linked-sequence-owner(owner=20261009-db-security): 2/3 rounds, status=resolved; db-security-old-password-check-source(owner=20261009-db-security): 1/3 rounds, status=resolved

## 5. 운영 상태
work=done, commit=87dc823b4d3ad94714ad329cf4a4dc86c97c3dc0, push=pushed, deploy=not_in_scope

## 사용설명서
해당 없음 -- 버그 수정(사용법 같음): 운영 보안, 사용법 같음

## 6. 남은 문제
없음

## 7. Incident 상세
### db-security-linked-sequence-owner (resolved, 2/3 rounds)
- Round 1 ❌ [partially_confirmed] 소유권 SQL이 relkind 순서로 sequence를 소유 테이블보다 먼저 처리해 PostgreSQL이 linked sequence 단독 ALTER를 거부했다 -> apply 실패 직후 rollback 스크립트 exit 0; 테이블 소유권·포트·Qdrant는 이전 상태로 복구됐으나 미사용 bomts_app 역할이 남고 새 비밀번호는 적용되지 않음
- Round 2 ✅ [confirmed] 연결된 PostgreSQL 시퀀스를 ALTER SEQUENCE OWNER로 직접 변경한 것이 첫 적용 실패 원인이다 -> 보완 SQL이 COMMIT되고 8개 테이블의 bomts_app 소유권을 확인해 연결 시퀀스 오류가 재발하지 않았다
### db-security-old-password-check-source (resolved, 1/3 rounds)
- Round 1 ✅ [confirmed] 이전 비밀번호를 DATABASE_URL에서 추출하고 Docker 네트워크 경로로 인증하면 교체 여부를 정확히 판정할 수 있다 -> DATABASE_URL에서 이전 비밀번호를 추출하고 api→db TCP 인증으로 이전 값 거부, 새 관리자·앱 값 성공을 확인했다
