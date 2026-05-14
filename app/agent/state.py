from typing import TypedDict, Optional, List, Dict, Any

class AgentState(TypedDict):
    question: str
    limit: int
    intent: Optional[str]
    answer: Optional[str]
    sources: List[Dict[str, Any]]
    provider: Optional[str]
    model: Optional[str]
    workflow_steps: List[Dict[str, str]]
    latency_ms: Optional[int]
    error: Optional[str]
