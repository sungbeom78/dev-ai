# LangGraph 기초 및 구현

## 1. LangGraph란?
LangGraph는 복잡한 AI 에이전트(Agent) 워크플로우를 상태 머신(State Machine) 형태로 정의하고 실행할 수 있게 해주는 프레임워크입니다. 순환(Cyclic) 구조의 워크플로우 작성이 용이하여 Multi-Agent 시스템이나 복잡한 RAG 파이프라인 제어에 적합합니다.

## 2. 핵심 개념
- **StateGraph**: 전체 워크플로우의 상태(State)와 흐름을 관리하는 메인 객체입니다.
- **Node**: 특정 작업을 수행하는 함수 또는 객체입니다. 입력을 받아 상태(State)를 업데이트합니다.
- **Edge**: Node 간의 연결선으로, 데이터가 어떻게 흘러갈지 정의합니다.
- **Conditional Edge**: 상태(State) 값에 따라 다음 Node를 동적으로 결정하는 분기 처리 라인입니다.

## 3. 본 프로젝트의 구조
- `state.py`: 에이전트가 공유할 `AgentState` 정의 (질문, 의도, 답변, 소스, 실행 기록 등 보관)
- `classifier.py`: 사용자의 질문 의도를 분류하는 모듈 (현재는 Rule-based)
- `nodes.py`: 실제 답변을 생성하는 노드들 (`rag_answer_node`, `system_status_answer_node` 등)
- `workflow.py`: `StateGraph`에 노드와 조건부 엣지를 등록하고 엮어서 최종 컴파일된 Agent App 생성

## 4. 향후 확장
현재 `classifier`는 빠르고 명확한 설명을 위해 Rule-based(키워드 기반)로 작성되었으나, 향후 LLM을 사용한 의도 분류(Intent Classification) 모듈로 교체하거나 다수의 Agent가 협업하는 구조로 손쉽게 확장할 수 있습니다.
