# 최종 보고서 — 20261010-alembic-baseline

- 생성 시각: 2026-10-10T13:16:18.220938+00:00
- **최종 판정**: `completed`

## 1. 업무 의미
Alembic baseline을 도입하고 애플리케이션 기동 시 create_all 의존을 제거

## 완료 기준
- [x] #1 Alembic baseline revision이 T4 정본의 8개 테이블·80개 컬럼·6개 관계를 재현 -- met (alembic_schema run 0bf0162a9725: head 20261010_01, tables=8, columns=80, foreign_keys=6, production diff lines=0)
- [x] #2 애플리케이션 기동 경로에서 Base.metadata.create_all 호출 제거 -- met (scripts/check.sh와 live_apply_smoke run 06aea2021f9a에서 app/main.py create_all 및 engine/Base 불필요 import 부재 확인)
- [x] #3 빈 임시 PostgreSQL에 alembic upgrade head 후 정본 DDL과 스키마 차이 0 -- met (빈 UUID 임시 PostgreSQL에서 alembic upgrade head 후 운영 schema-only 정규화 diff 0, downgrade 후 앱 테이블 0 (run 0bf0162a9725))
- [x] #4 운영 DB에는 migration을 실행하지 않고 기존 DB stamp·upgrade 절차와 rollback을 기록 -- met (production_db_untouched run e5fba9d5bcf8: alembic_version absent, public tables 8, DDL/stamp 미실행. db/MIGRATIONS.md에 stamp·upgrade·rollback 절차 기록)
- [x] #5 기존 검사와 애플리케이션 테스트 통과 -- met (전체 verify verified: lint 68581436330e, regression 820d3ebf4e18, encoding 93ae00dc510a, identifier 041779c45aec, qa d732dea3f2eb; live health/search 200)

## 2. 실제 변경
Alembic baseline 도입, startup create_all 제거, 빈 임시 PostgreSQL 스키마 diff 0, 운영 DB 미변경, live health·검색 200 및 전체 필수 검사 통과

## 3. 검증 근거
alembic_schema=allow[verified]; encoding=allow[verified]; identifier_audit=allow[verified]; lint=allow[verified]; live_apply_smoke=allow[verified]; preview_image_import=allow[verified]; prior_art=allow[reported_only]; production_db_untouched=allow[verified]; python_compile=allow[verified]; qa_quick=allow[verified]; unit_or_regression=allow[verified]; work_state_ready=allow[verified]

## 4. 변경·복구 이력
alembic-psycopg2-missing(owner=20261010-alembic-baseline): 원인=environment, 계획 1, 라운드 0, 재시도 1, status=resolved; app-main-patch-context(owner=20261010-alembic-baseline): 원인=own_change, 계획 1, 라운드 1, 재시도 0, status=resolved; host-pycache-permission(owner=20261010-alembic-baseline): 원인=environment, 계획 1, 라운드 0, 재시도 1, status=resolved; mark-work-done-missing-summary(owner=20261010-alembic-baseline): 원인=own_change, 계획 1, 라운드 1, 재시도 0, status=resolved; preview-import-qdrant-endpoint(owner=20261010-alembic-baseline): 원인=own_change, 계획 1, 라운드 1, 재시도 0, status=resolved; identifier-audit-missing-httpx(owner=20261010-api-health-incident, linked): 원인=environment, 계획 1, 라운드 2, 재시도 1, status=resolved

## 5. 운영 상태
work=done, commit=be369b6a00e0969cc3f929b0e96208e0329eb22e, push=pushed, deploy=not_in_scope

## 사용설명서
해당 없음 -- 내부 정리: 운영 DB 구조와 사용자 사용법은 그대로이며 스키마 변경 관리 방식만 버전형 migration으로 전환

## 6. 남은 문제
없음

## 7. Incident 상세
### alembic-psycopg2-missing (resolved, 원인 environment, 계획 1, 라운드 0, 재시도 1)
### app-main-patch-context (resolved, 원인 own_change, 계획 1, 라운드 1, 재시도 0)
- Round 1 ✅ [confirmed] 첫 패치는 실제 app/main.py의 import 순서와 lifespan 내부 호출 위치를 반영하지 않은 문맥을 사용했다 -> 실제 파일 문맥으로 승인 범위 3줄만 제거. live_apply_smoke에서 health 200, 실제 검색 200/결과 1건, 최근 로그 20줄, auth/connection 오류 0건.
### host-pycache-permission (resolved, 원인 environment, 계획 1, 라운드 0, 재시도 1)
### mark-work-done-missing-summary (resolved, 원인 own_change, 계획 1, 라운드 1, 재시도 0)
- Round 1 ✅ [confirmed] 필수 --summary 인자 누락이 유일한 실패 원인이다 -> 필수 summary를 포함해 work=done 전환. work_state_ready에서 completion done 및 acceptance 5건 met 확인.
### preview-import-qdrant-endpoint (resolved, 원인 own_change, 계획 1, 라운드 1, 재시도 0)
- Round 1 ✅ [confirmed] 격리 컨테이너가 bridge namespace의 loopback을 호스트 Qdrant로 오인했다 -> host network로 preview image import 성공. image sha256:a34c452b..., create_all 부재 단언 성공, Qdrant 인증 연결 성공. credential 값 출력 없음.
### identifier-audit-missing-httpx (resolved, 원인 environment, 계획 1, 라운드 2, 재시도 1)
- Round 1 ❌ [partially_confirmed] 검증을 프로젝트 가상환경이 아닌 시스템 Python으로 실행해 프레임워크 의존성 httpx를 찾지 못했다 -> 가상환경 사용으로 httpx import 오류는 해소됐으나, 별도 db-security 준비 변경의 DATABASE_URL 식별자 사전 위반이 드러나 전체 검증은 아직 실패
- Round 2 ✅ [confirmed] httpx 환경 문제 해소 후 남은 실패는 db-security 준비 코드가 DATABASE_URL을 변경된 모듈 선언으로 만든 데서 발생했다 -> DATABASE_URL 중간 모듈 변수를 제거한 뒤 identifier_audit와 전체 필수 검사가 verified
