import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.agent.schemas import AgentAskRequest, AgentAskResponse
from app.agent.workflow import agent_app
from app.agent.state import AgentState
from app.db.database import get_db
from app.services import log_service

router = APIRouter()

@router.post("/ask", response_model=AgentAskResponse)
def agent_ask(request: AgentAskRequest, db: Session = Depends(get_db)):
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
    
    sources = final_state.get("sources", [])
    
    ask_log_id = log_service.create_ask_log(
        db=db,
        question=final_state.get("question"),
        endpoint_type="agent_ask",
        intent=final_state.get("intent"),
        answer=final_state.get("answer"),
        provider=final_state.get("provider"),
        model=final_state.get("model"),
        latency_ms=final_state.get("latency_ms"),
        retrieval_count=len(sources),
        sources=sources
    )
    
    return AgentAskResponse(
        ask_log_id=ask_log_id,
        question=final_state.get("question"),
        intent=final_state.get("intent"),
        answer=final_state.get("answer"),
        sources=sources,
        provider=final_state.get("provider"),
        model=final_state.get("model"),
        workflow=final_state.get("workflow_steps", []),
        latency_ms=final_state.get("latency_ms"),
        error=final_state.get("error")
    )
