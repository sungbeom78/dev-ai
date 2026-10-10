# 공유 컴포넌트 수정 요청

이 프로젝트에서 dev-process-framework 나 공통 용어사전 시스템을 **직접 고치지 않는다.** 필요한 점을 여기 적으면
소유자가 원본 저장소(sungbeom78/dev-process-framework, sungbeom78/bomiyang-glossary)에서 처리한다.

<!-- - YYYY-MM-DD [framework|glossary] 무엇이 문제인가 / 원하는 변경 / 관련 작업 id -->

- 2026-10-10 [framework] `record-user-approval`이 일치하는 deferred 요청을 승인해도 task `status`가 `waiting`에 남을 수 있고 `open_waits`는 비어 있는 불일치가 발생한다. 승인 기록 시 `in_progress`로 복귀시키거나 `verdict`가 승인된 wait를 무시하도록 정합성을 보장해 달라. 관련 작업: `20261009-db-security`, `20261010-data-stance`.
- 2026-10-10 [framework] 최신 recovery round가 `unconfirmed`일 때 `next`가 `recover-result` 대신 새 `recover-round`를 안내했다. 실행 중인 round의 결과 기록을 먼저 안내해 recovery budget을 잘못 소비하지 않게 해 달라. 관련 작업: `20261009-db-security`.
- 2026-10-10 [framework] `finish`가 `.gitignore` 대상인 `dev-process/report/`를 기록 커밋에 포함하려다 기록 커밋만 실패하고 전체 결과를 `completed`로 반환했다. 추적 가능한 task 기록은 별도로 커밋하고, 보고서가 의도적으로 ignored이면 건너뛰며, 실제 기록 실패는 별도 machine-readable 상태로 노출해 달라. 관련 작업: BOMTS public `20261010-data-stance`.
- 2026-10-10 [framework] 운영 적용 후 rollback 명령이 종료 코드 0이어도 현재 애플리케이션 코드와 이전 환경의 조합 때문에 서비스가 기동하지 않을 수 있다. rollback gate에 health/search 같은 사용자 정의 복구 완료 검사를 필수로 연결할 수 있게 해 달라. 관련 작업: `20261009-db-security`.
- 2026-10-10 [framework] 기존 DB 역설계 산출물 생성 시 일반 작업에서 `db/model.json`이 만들어지면 `work_type: data_model` task와 logical/glossary gate가 없음을 `verify` 또는 `data-stance`가 탐지하도록 해 달라. 관련 작업: `20261009-db-security`, 후속 `model-baseline`.
- 2026-10-10 [framework] `data-stance`는 `owned`와 `db/model.json` 존재만으로 통과했지만, 기존 DB 역설계 모델은 표준 exporter 입력 계약과 호환되지 않았다. 역설계 모델의 `column.type`·최상위 `relationships`·이름 있는 `uniques`·관측 `indexes`를 표준 `column.domain`·인라인 FK 계약으로 정규화하거나, 불일치를 `data-stance`/`model_dictionary`에서 즉시 보고해 달라. 관련 작업: `20261010-model-baseline`.
- 2026-10-10 [framework] `export_all.py`가 `meta_schema`·`generated_at`을 선택 키처럼 문서화하지 않고 필수 조회하며, `schema=public`이면 pgModeler XML에 `public` 스키마를 중복 생성한다. 기존 운영 DB 기준선에서는 meta 5개 테이블과 FK 인덱스를 무조건 추가해 schema diff 0을 만들 수 없다. `baseline/existing_db` 모드에서 관측 스키마만 내보내고 meta·권장 인덱스를 별도 제안으로 분리해 달라. 관련 작업: `20261010-model-baseline`.
- 2026-10-10 [framework] 임시 PostgreSQL 검증이 로컬 `pg_ctl` 설치만 지원해 Docker 환경에서는 프로젝트별 검증기를 다시 만들어야 한다. 공식 이미지 초기화 중 임시 서버도 `pg_isready`와 `psql`에 응답한 뒤 종료되므로, 컨테이너 health 상태와 entrypoint의 `PostgreSQL init process complete` 이후 최종 서버를 판별하는 공용 Docker 검증 경로를 제공해 달라. 관련 작업: `20261010-model-baseline`.
- 2026-10-10 [framework] **해결됨 — 프레임워크 `43b34f2`에서 원인별 처리로 해결됨.** 기존 요청: recovery incident의 최초 오류와 복구 도중 드러난 독립 환경 오류를 원인별 재시도·Plan B로 처리할 경로가 필요했다. 관련 작업: `20261010-model-baseline`.
