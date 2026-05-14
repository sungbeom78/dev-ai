from pydantic import BaseModel
from typing import List, Optional, Any

class AgentAskRequest(BaseModel):
    question: str
    limit: int = 5

class WorkflowStep(BaseModel):
    step: str
    result: str

class AgentAskResponse(BaseModel):
    ask_log_id: int
    question: str
    intent: Optional[str] = None
    answer: Optional[str] = None
    sources: List[Any] = []
    provider: Optional[str] = None
    model: Optional[str] = None
    workflow: List[WorkflowStep] = []
    latency_ms: Optional[int] = None
    error: Optional[str] = None
