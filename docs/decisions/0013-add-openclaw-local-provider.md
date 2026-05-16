# 0013. Add OpenClaw Local Provider

## Context
비용 효율적인 RAG 실험과 데이터 프라이버시, 보안 등급이 높은 환경 구축을 위해 로컬 LLM의 필요성이 대두되었습니다. 
사용자 로컬 데스크탑 환경에 OpenClaw 브리지 서버를 통해 구동되는 Qwen, Gemma 등의 모델을 Dev AI 프로젝트의 LLM Provider로 연동하고자 합니다.

## Decision
기존의 추상화된 `BaseLLMProvider` 구조를 상속받아 `OpenClawLLMProvider`를 추가로 구현합니다.
- `.env`에 `LLM_PROVIDER=openclaw`를 설정하고, `OPENCLAW_BASE_URL`, `OPENCLAW_DEFAULT_MODEL`을 환경 변수로 주입합니다.
- 내부 IP 및 API Key와 같은 민감 정보는 소스코드에 하드코딩하지 않고 `.env`에서만 관리합니다.
- `app/api/system/status` 등의 상태 API에서 OpenClaw의 구성 여부를 확인할 수 있게 하여, 사용자가 언제든 상태를 파악할 수 있게 합니다.

## Consequences
- 외부 API 의존 없이도 무료로 지속적인 AI 실험 및 RAG 구축이 가능해집니다.
- 데스크탑이 꺼져 있거나 연결할 수 없는 경우의 예외 처리를 명시하고 사용자에게 알림으로써, 운영상의 오류를 방지할 수 있습니다.
- 보안이 높은 인프라 환경에서 LLM 연동 아키텍처를 증명할 수 있는 좋은 포트폴리오 사례가 됩니다.
