# 최종 보고서 — 20261010-model-baseline

- 생성 시각: 2026-10-10T12:46:23.624340+00:00
- **최종 판정**: `completed`

## 1. 업무 의미
운영 PostgreSQL 을 현재 그대로 정본으로

## 완료 기준
- [x] #1 정본 DDL 과 운영 스키마 차이 0 -- met (sealed ddl_postgres run 4455a3ec4c55: temporary PostgreSQL 15 created 8 tables/80 columns/6 FKs; production vs generated normalized schema-only pg_dump diff lines=0)
- [x] #2 문제 목록 분리 기록 -- met (db/01_modeling_notes.md separates current-as-is baseline from six explicit problem items; no problem fix was added to baseline DDL)
- [x] #3 논리 모델 사용자 승인 -- met (사용자 원문 '현재 논리 모델을 승인한다.'를 model-approve logical에 기록; pgModeler 실제 열기 화면에서 8개 테이블과 관계선 확인)
- [x] #4 용어 사전 등록 -- met (model_glossary run fd20577dbab1 verified; user-approved 22 terms committed as glossary d16f5e7 and origin/main contains that commit)

## 2. 실제 변경
운영 PostgreSQL 8개 테이블을 정본화하고 DDL·pgModeler·정의서를 생성했으며 임시 PostgreSQL에서 운영 스키마와 차이 0을 검증

## 3. 검증 근거
data_stance=allow[verified]; ddl_postgres=allow[verified]; encoding=allow[verified]; logical_review_dbm=allow[verified]; model_dictionary=allow[verified]; model_export=allow[verified]; model_export_recovery=allow[verified]; model_glossary=allow[verified]; prior_art=allow[reported_only]

## 4. 변경·복구 이력
model-dictionary-script-moved(owner=20261010-model-baseline): 원인=own_change, 계획 1, 라운드 1, 재시도 0, status=resolved; model-export-missing-meta-schema(owner=20261010-model-baseline): 원인=unknown, 계획 1, 라운드 2, 재시도 0, status=resolved; pgdump-nondeterministic-noise(owner=20261010-model-baseline): 원인=environment, 계획 1, 라운드 3, 재시도 1, status=resolved; xlsx-core-properties-none(owner=20261010-model-baseline): 원인=unknown, 계획 1, 라운드 1, 재시도 0, status=resolved

## 5. 운영 상태
work=done, commit=629a81ffe7e54aee94c409652d959285e6e8bdc8, push=pushed, deploy=not_in_scope

## 사용설명서
해당 없음 -- 기타: 운영 스키마 역설계 정본화, 운영 DB 변경 없음

## 6. 남은 문제
없음

## 7. Incident 상세
### model-dictionary-script-moved (resolved, 원인 own_change, 계획 1, 라운드 1, 재시도 0)
- Round 1 ✅ [confirmed] 프로젝트 검증기의 프레임워크 스크립트 경로만 새 data-modeling-expert 위치로 바꾸면 표준 사전 검사와 로컬 baseline 검사가 모두 실행된다 -> 새 data-modeling-expert check_dictionary 실행; 표준 검사 errors=0, baseline_contract errors=0
### model-export-missing-meta-schema (resolved, 원인 unknown, 계획 1, 라운드 2, 재시도 0)
- Round 1 ❌ [failed] 기존 역설계 model.json이 exporter 필수 메타데이터 meta_schema와 generated_at을 포함하지 않아 검토용 산출물 생성이 시작되지 못했다 -> meta_schema와 generated_at 보완 후 export가 column.domain KeyError로 다시 중단됨; 기존 모델은 column.data_type 직접형이며 framework exporter 입력 계약과 다름
- Round 2 ✅ [confirmed] 기존 역설계 모델은 framework prospective-design contract와 달라 공식 export 전 논리 검토에는 현재 type·relationship·unique 구조를 직접 읽는 review-only DBM adapter가 필요하다 -> sealed logical_review_dbm check: XML well-formed, tables=8, columns=80, relationships=6, 한글 aliases 포함
### pgdump-nondeterministic-noise (resolved, 원인 environment, 계획 1, 라운드 3, 재시도 1)
- Round 1 ❌ [failed] pg_dump emits random restrict tokens and environment-dependent comments that are not schema statements -> dump normalization was applied, but retry stopped before comparison because temporary server accepted connections while database bomts did not exist
- Round 2 ❌ [failed] pg_isready only confirms server acceptance and does not guarantee POSTGRES_DB creation completed -> explicit createdb still raced with asynchronous initdb/entrypoint initialization immediately after pg_isready
- Round 3 ❌ [failed] SQL readiness must be established with psql, and database creation must tolerate the entrypoint having already created bomts -> psql readiness reached the entrypoint temporary server; it shut down before createdb, so validation could not continue
### xlsx-core-properties-none (resolved, 원인 unknown, 계획 1, 라운드 1, 재시도 0)
- Round 1 ✅ [confirmed] openpyxl requires datetime values for W3CDTF core properties -> deterministic datetime properties allow all three exports; consistency check confirmed 8 tables, 80 columns, 6 relationships
