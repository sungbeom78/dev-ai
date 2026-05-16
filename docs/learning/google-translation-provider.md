# Google Translation & LLM Provider

Phase 9 개발에서는 수집된 외국어(영어 등) 문서를 효과적으로 활용하기 위해 구글 번역/LLM API 연동 구조를 추가했습니다.

## Objectives
- 해외 유수 블로그와 공식 문서의 원문을 정확한 한국어로 변환합니다.
- 단순 번역을 넘어 문서의 핵심을 한국어로 요약하고, RAG 임베딩 대상 텍스트의 질을 높입니다.

## Implementation Details

`GoogleLLMProvider` 클래스를 추가하여 향후 번역뿐 아니라 LLM 생성 기능까지 포괄할 수 있도록 하였습니다. 
주요 환경 변수 구조는 다음과 같습니다:

```env
# Google Provider Configuration
GOOGLE_API_KEY=your-api-key
GOOGLE_PROVIDER_ENABLED=true
GOOGLE_TRANSLATION_ENABLED=true
GOOGLE_DEFAULT_MODEL=gemini-1.5-flash
```

## Security Note
Google API Key는 반드시 서버의 실제 `.env` 환경 변수에서만 관리합니다. `.env.example`에는 구조만 노출하며, 프론트엔드나 `system/status` API에서는 키 값을 노출하지 않고 `google_enabled` 여부만 반환하도록 구현했습니다.
