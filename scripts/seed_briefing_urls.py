seed_data = [
    {
        "topic": "coding_agent, agent_workflow",
        "title_hint": "GitHub Agent HQ: Claude와 Codex coding agents 통합",
        "url": "https://www.theverge.com/news/873665/github-claude-codex-ai-agents",
        "source_name": "The Verge",
        "why_collect": "GitHub가 Claude, Codex, Copilot 등을 한 곳에서 선택해 이슈/PR 작업에 투입하는 Agent HQ를 공개했다. AI 코딩 도구가 '에디터 보조'에서 '개발 워크플로우에 들어오는 agent'로 이동하는 흐름을 설명할 수 있다.",
        "expected_dev_ai_usage": "dev-ai도 단순 RAG 페이지가 아니라 Codex/Claude/Antigravity가 참고할 수 있는 Reference KB 또는 MCP/Skill 기반 지식 소스로 발전시킬 수 있다.",
        "freshness_status": "최신"
    },
    {
        "topic": "skills, governance, security",
        "title_hint": "Agent Skills enterprise governance (AI 에이전트 스킬의 기업 보안 리스크)",
        "url": "https://www.techradar.com/pro/ai-agent-skills-are-becoming-the-next-enterprise-supply-chain-risk-heres-how-to-govern-them",
        "source_name": "TechRadar",
        "why_collect": "agent skill이 prompts/scripts/orchestration 묶음으로 확산되면서 출처, 버전, 권한, 감사 문제가 생긴다는 관점.",
        "expected_dev_ai_usage": "향후 dev-ai에 Codex/Claude Skill을 만들더라도 버전 관리, 권한, 읽기 전용 원칙, 검증 절차를 두어야 한다.",
        "freshness_status": "최근"
    },
    {
        "topic": "qwen, coding_agent, open_model",
        "title_hint": "Qwen3-Coder-Next Technical Report",
        "url": "https://arxiv.org/abs/2603.00729",
        "source_name": "arXiv",
        "why_collect": "Qwen3-Coder-Next는 coding agent 특화 open-weight 모델로, executable environment feedback, agentic training, SWE-Bench/Terminal-Bench 같은 agent-centric benchmark를 다룬다.",
        "expected_dev_ai_usage": "OpenClaw에서 Qwen 계열 모델을 사용할 때 '단순 채팅 모델'이 아니라 coding agent workflow에 적합한 모델 후보로 평가할 수 있다.",
        "freshness_status": "최신"
    },
    {
        "topic": "skills, agent_workflow, graph_orchestration",
        "title_hint": "GraSP: Graph-Structured Skill Compositions for LLM Agents",
        "url": "https://arxiv.org/abs/2604.17870",
        "source_name": "arXiv",
        "why_collect": "skill을 많이 주는 것보다, skill을 구조화하고 그래프로 조합하는 것이 중요하다는 연구.",
        "expected_dev_ai_usage": "LangGraph workflow와 Skills를 연결할 때 단순 skill 목록보다 '어떤 순서/조건으로 skill을 실행할지'가 중요하다는 방향을 반영한다.",
        "freshness_status": "최신"
    },
    {
        "topic": "mcp, tool_integration",
        "title_hint": "Model Context Protocol 공식 Introduction",
        "url": "https://modelcontextprotocol.io/docs/getting-started/intro",
        "source_name": "Model Context Protocol",
        "why_collect": "MCP가 무엇이고 왜 필요한지 설명하는 기초 레퍼런스.",
        "expected_dev_ai_usage": "dev-ai의 reference search를 MCP read-only tool로 노출하는 설계의 기초 자료로 사용한다.",
        "freshness_status": "기초 자료"
    }
]

if __name__ == "__main__":
    print(f"Seed briefing URLs: {len(seed_data)}")
