import time
from fastapi import APIRouter
from app.agent.schemas import AgentAskRequest, AgentAskResponse
from app.agent.workflow import agent_app
from app.agent.state import AgentState

router = APIRouter()

@router.post("/ask", response_model=AgentAskResponse)
def agent_ask(request: AgentAskRequest):
    start_time = time.time()
    
    initial_state: AgentState = {
        "question": request.question,
        "limit": request.limit,
        "intent": None,
        "answer": None,
        "sources": [],
        "provider": None,
        "model": None,
        "workflow_steps": [],
        "latency_ms": None,
        "error": None
    }
    
    final_state = agent_app.invoke(initial_state)
    
    latency_ms = int((time.time() - start_time) * 1000)
    final_state["latency_ms"] = latency_ms
    
    return AgentAskResponse(
        question=final_state.get("question"),
        intent=final_state.get("intent"),
        answer=final_state.get("answer"),
        sources=final_state.get("sources", []),
        provider=final_state.get("provider"),
        model=final_state.get("model"),
        workflow=final_state.get("workflow_steps", []),
        latency_ms=final_state.get("latency_ms"),
        error=final_state.get("error")
    )
