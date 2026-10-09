# 에이전트 시작 지시문 (init_project 생성 -- 복사해서 첫 메시지로 쓴다)

```text
이 프로젝트는 dev-process-framework 개발 표준을 따른다. 먼저 AGENTS.md 를 읽어라.
스킬 명령: python .claude/skills/sk-mgm-task-state/scripts/run.py <명령>   (Codex 는 .agents/skills/...)

0) 절대 규칙: dev-process-framework/·설치본·glossary/ 의 시스템 파일은 읽기만 한다 (사전 데이터는 사전 명령으로만).
   이 프로젝트 고유 지침은 dev-process/local/ 에 있다 -- 먼저 읽는다.
1) `next` 로 다음 행동을 확인하고 그대로 따른다.
2) 새 작업이면 아래 목표로 `task-new --goal "..." --title <짧은영문> --change-kind <종류>` 를 만든다.
   만들기 전에 완료 기준(무엇이 되면 끝인지)을 3~5개 제안해 나에게 확인받고 `--accept` 로 기록한다.
   종류: new_project(신규 개발)·new_feature(새 기능)·usage_change(설계·사용법 변경)이면 사용설명서를 만들거나 고친다
   (`sk-dev-user-manual`: HTML 슬라이드, 페이지마다 도식 + 대본, 한 단계 = 한 페이지, 전공자 인수인계 수준.
   먼저 `references/quality_bar.md` 와 기준 예시 `dev-process-framework/docs/manual/` 를 본다. 템플릿 쪽수로 끝내지 않는다).
   fix·refactor·other 는 `--change-reason` 으로 사용법이 그대로인 이유를 적는다.
3) 구현은 작은 단위로 하고, 단위마다 `verify` 로 검증한다. 실패하면 원인을 고쳐 다시 verify 한다.
   같은 실패가 반복되면 `sk-mgm-failure-recovery` 절차를 따른다 (같은 사건 최대 3회).
4) 새 이름(변수·함수·클래스)은 공통 사전 단어로 짓는다. 사전에 없는 단어가 꼭 필요하면
   `glossary-sync` 표를 나에게 보여주고 승인받은 것만 등록한다.
5) 완료 기준을 하나씩 실제로 확인해 `accept --index N --status met --note "확인 방법"` 으로 기록하고,
   `finish --message "..." --all-changed --changelog "..."` 로 커밋·보고서를 만든다.
   판정이 completed 가 아니면 "완료"라고 말하지 말고 남은 이유를 보고한다.
6) 사용설명서를 만들거나 고쳤으면 `manual-review` 미리보기 PNG 를 직접 열어 확인하고(겹침·넘침·빈 페이지),
   `manual-show --task-id <id> --changed` 출력을 요약하지 말고 미리보기와 함께 채팅에 보여 준다.
   내가 "사용설명서 보여 줘"라고 하면 `manual-show` (목차) → 고른 장 `manual-show --section <이름>`.

작업 목표: <여기에 이번 작업 목표를 적는다>
```
