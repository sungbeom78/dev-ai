seed_data = [
    {
        "topic": "mcp",
        "title_hint": "MCP가 AI 개발 도구 연결 표준으로 중요한 이유",
        "url": "https://www.anthropic.com/news/model-context-protocol",
        "source_name": "Anthropic Blog",
        "why_collect": "Claude, Antigravity 등의 도구가 외부 데이터를 읽는 표준 스펙이 됨",
        "expected_dev_ai_usage": "dev-ai의 Reference Search를 MCP tool로 감싸 노출할 수 있다."
    },
    {
        "topic": "langgraph",
        "title_hint": "LangGraph를 이용한 상태 기반 AI 에이전트 구축",
        "url": "https://blog.langchain.dev/langgraph/",
        "source_name": "LangChain Blog",
        "why_collect": "단순 체인을 넘어 상태 머신 기반 에이전트 구축에 필수적임",
        "expected_dev_ai_usage": "dev-ai Agent 모듈을 LangGraph 기반으로 재작성하여 복잡한 태스크를 안정적으로 처리한다."
    },
    {
        "topic": "local_llm",
        "title_hint": "Local LLM 생태계와 개발 환경 적용 장단점",
        "url": "https://ollama.com/blog",
        "source_name": "Ollama Blog",
        "why_collect": "비용 절감 및 보안 강화를 위해 사내 개발망에 로컬 모델을 배포하는 사례 증가",
        "expected_dev_ai_usage": "dev-ai의 OpenClaw 설정을 최적화하여 Gemma/Qwen 로컬 모델과 유연하게 통신한다."
    }
]

if __name__ == "__main__":
    print(f"Seed briefing URLs: {len(seed_data)}")
