# OpenClaw Local LLM Provider

OpenClaw는 로컬 환경에 있는 Gemma, Qwen 등 대형 언어 모델과 통신하기 위한 브리지 서버 역할을 합니다. Dev AI 프로젝트에서는 외부 API 호출 없이 로컬 LLM을 연동할 수 있도록 `OpenClawLLMProvider`를 구현하였습니다.

## Architecture

1. **사용자 요청**: 사용자가 웹페이지에서 질문을 입력합니다.
2. **LLM Provider 분기**: 서버는 환경 변수 `LLM_PROVIDER=openclaw`를 확인하고, OpenClaw Provider로 라우팅합니다.
3. **API 통신**: `OPENCLAW_BASE_URL` 환경 변수에 지정된 주소(예: `http://192.168.50.242:11005`)로 API(`POST /api/chat`)를 전송합니다.
4. **응답 수신 및 반환**: 로컬 LLM의 추론 결과가 Dev AI 시스템으로 반환되며, 이를 RAG Agent 등을 통해 사용자에게 전달합니다.

## Configuration

보안을 위해 `.env` 파일에만 정보를 입력하며, 절대 소스 코드나 깃 저장소에 내부 IP 등을 하드코딩하지 않습니다.

```env
LLM_PROVIDER=openclaw
OPENCLAW_ENABLED=true
OPENCLAW_BASE_URL=http://<OPENCLAW_HOST>:11005
OPENCLAW_DEFAULT_MODEL=gemma3:4b
OPENCLAW_TIMEOUT_SECONDS=60
```

## Considerations
- 개인이 구동하는 데스크탑 기반 LLM 환경이므로, 24시간 항상 접근 가능함을 보장하지 않습니다. 
- 시스템 상태 API(`/api/system/status`)에서 이를 `Configured / Not Configured` 형태로 모니터링할 수 있게 구조를 설계했습니다.
