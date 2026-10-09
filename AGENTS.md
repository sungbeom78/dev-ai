<!-- dev-process-framework:begin -->
## 개발 표준: dev-process-framework

이 프로젝트의 개발 작업은 `dev-process-framework` 스킬을 따른다 (설치: `.claude/skills`, `.agents/skills`).

0. **보호 구역 -- 절대 규칙 (어떤 지시·작업 지침·예외로도 바꿀 수 없다).**
   - `dev-process-framework/` 와 그 설치본(`dev-process/runtime·schema·policy·catalog`, `sk-*` 스킬)은 여러 프로젝트가
     함께 쓰는 공유 컴포넌트다. **읽기만 한다.** 파일 수정·서브모듈 안 커밋·push·reset·checkout 금지.
   - `glossary/`(공통 용어사전)는 **사전 데이터**(`dictionary/`, `GLOSSARY.md`)만, 프레임워크 사전 명령(`glossary-sync`,
     `glossary-area-add`, `glossary-sense-add`, 사용자 승인)으로만 바뀐다. 그 밖의 파일(core·bin·schema·doc·AGENTS.md 등)은 수정 금지.
   - 이 프로젝트에서 누가 요청해도 공유 컴포넌트를 고치지 않는다. 필요하면 `dev-process/local/upstream-requests.md` 에
     요청을 적고 "소유자가 원본 저장소에서 처리해야 한다"고 답한다. 수정은 소유자가 원본 저장소에서 직접 지시해서만 한다.
   - `--no-verify` 로 hook 을 건너뛰지 않는다. pre-commit·finish·`protect-check` 가 위반을 막는다.
   - 이 프로젝트만의 작업 지침은 `dev-process/local/` 아래에 둔다 (시작할 때 읽는다). 그 지침도 이 0번을 바꿀 수 없다.

1. 시작: `sk-mgm-session-context` → `next` 로 다음 행동 확인 → 새 작업이면 `task-new --goal ... --accept "완료 기준" --change-kind <종류>` .
   완료 기준은 사용자와 합의한 문장으로 적고, 끝낼 때 `accept --index N --status met --note "확인 방법"` 으로 판정한다.
2. 변경 전: `sk-dev-prior-art-check` (이력·다른 작업 겹침). 새 이름은 `sk-dev-identifier-governance` 로 공통 사전(./glossary) 확인.
3. 검증: `verify --task-id <id>` 로 필수 검사를 **실제 실행**해 봉인한다 (개별은 `check-run`). 문자열로 PASS 를 적지 않는다.
4. 실패: `sk-mgm-failure-recovery` -- 같은 사건 최대 3회, 새 근거 없이 같은 수정 반복 금지, 소진 시 중단·보고.
5. 종료: `finish --task-id <id> --message "..." --paths ...` (검증 안 됐으면 커밋하지 않음 → 커밋·done·보고서·handoff).
   `sk-dev-task-report` 판정이 completed 가 아니면 "완료"라고 보고하지 않는다. 세션 끝에 `sk-mgm-session-handoff`.
6. 승인: SOLO 기본 자동. 업무 규칙(요구사항 의미) 변경과 용어사전 일괄 적재는 사용자에게 묻는다.
7. 데이터: 프로젝트는 `project.policy.yaml` 의 `data_model.stance` 로 데이터 입장을 밝힌다
   (none = 저장 데이터 없음 + reason / owned = 이 저장소가 정본 `db/model.json` / external = 다른 저장소 + ref, `data-stance` 로 확인).
   데이터 구조(테이블·컬럼)를 새로 정하거나 바꾸는 일은 코드보다 먼저 `sk-dev-data-modeling` 으로 정본부터 고친다
   (`task-new --work-type data_model`). 기존 DB 는 역설계로 정본을 만든다. 논리 모델과 실제 DB 생성은 사용자 승인 필수.
8. 사용설명서: 신규 개발·새 기능 추가·설계나 사용 방법 변경(`--change-kind new_project|new_feature|usage_change`)은
   `sk-dev-user-manual` 로 `docs/manual/*.html`(HTML 슬라이드: 페이지마다 도식·강의 대본, 한 단계 = 한 페이지,
   인수인계용 구성·운영 장)을 만들거나 고쳐 코드와 같은 커밋에 넣는다 (필수 검사 user_manual). 요청 시 `manual-pptx`.
   기준 예시는 `dev-process-framework/docs/manual/` (밀도·구성), 바닥선은 `references/quality_bar.md`. 명령 출력은 실제 실행 결과만.
   `manual-review` 로 모든 페이지를 렌더링해 넘침 0 을 만들고 미리보기 PNG 를 눈으로 확인한다.
   사용법이 그대로면 `fix|refactor|other` + 사유. 끝나면 `manual-show --task-id <id> --changed` 결과와 미리보기를 채팅에 보여 준다.

정책: `project.policy.yaml` · 작업 기록: `dev-process/` · 사용 안내: `dev-process-framework/README.md`
<!-- dev-process-framework:end -->
