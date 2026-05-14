# Local LLM의 선택적(Optional) Provider 채택 방향

## 1. 개요
RAG 파이프라인에서 응답(Answer) 생성을 담당하는 LLM(Large Language Model)의 구동 방식에 대한 의사결정입니다. 현재 Gemma, Qwen 등 경량화된 모델들이 오픈소스로 널리 활용되고 있으나, 이를 시스템의 필수 구성요소로 편입할지에 대한 방향성을 정의합니다.

## 2. 로컬 LLM의 운영 한계점
- 로컬 데스크탑 환경이나 자원이 제한된 단일 서버 환경에서 구동될 경우 메모리(VRAM) 부족 및 추론 속도 지연이 발생할 가능성이 매우 높습니다.
- 컨테이너 형태로 Local LLM(Ollama, vLLM 등)을 함께 묶어 배포하면 전체 프로젝트의 무게가 과도하게 무거워지며 이식성이 떨어집니다.

## 3. Provider 설계 전략 (Phase 4 이후)
이러한 한계점을 고려하여 본 시스템은 다음과 같은 전략을 취합니다.
1. **Mock 및 OpenAI 우선 지원**: Phase 4에서는 OpenAI API와 자체 Mock Provider를 중심으로 답변 생성기(Answer Generator)를 개발합니다. 이는 외부 의존성 문제 없이 누구든 즉시 시스템을 실행할 수 있게 하기 위함입니다.
2. **Local LLM은 '선택 기능'으로 분리**: Local LLM은 항상 구동되어야 하는 필수 요소가 아닙니다. Phase 8 혹은 후속 개선 작업으로 미뤄 확장성 모듈로 구현합니다.
3. **인터페이스 호환성 기반 연결**: Local LLM을 사용하게 될 경우 시스템 자체에 무거운 모델 런타임을 포함시키기보다는, 이미 OpenAI 호환 규격을 제공하는 Ollama 또는 vLLM과 같은 별도 Endpoint를 활용하여 Provider 모듈만 갈아끼울 수 있도록(Pluggable) 설계합니다.
