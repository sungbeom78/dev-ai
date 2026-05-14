# LLM Provider 추상화 설계

## 1. 개요
LLM(Large Language Model) 환경은 매우 빠르게 변하고 있습니다. OpenAI의 GPT 시리즈뿐만 아니라 Claude, Gemini 등의 상용 모델과, Ollama, vLLM을 통해 구동하는 Local 모델(Llama, Qwen, Gemma 등)까지 선택지가 다양합니다. 

## 2. 추상화(Abstraction) 전략
이러한 다양성에 유연하게 대응하기 위해 `BaseLLMProvider`라는 추상 클래스를 정의했습니다.
- **MockLLMProvider**: 외부 API 연동 없이 시스템이 동작하는지 빠르게 검증하기 위한 데모용 모듈입니다.
- **OpenAILLMProvider**: 현재 표준처럼 쓰이는 OpenAI API 스펙에 맞춰 구현되었습니다.
- **LocalLLMProvider**: 로컬 구동 모델을 위한 스켈레톤(TODO) 코드를 두어, 향후 어떠한 로컬 솔루션을 도입하든 기존 RAG 파이프라인(검색 및 프롬프트 생성 등) 코드를 전혀 수정하지 않고 주입(Inject)만으로 확장할 수 있도록 설계했습니다.

## 3. 결론
이와 같은 추상화 구조는 도메인 중립성 뿐만 아니라 "인프라 중립성"까지 확보하여 유연한 백엔드 아키텍처를 구성할 수 있게 합니다.
