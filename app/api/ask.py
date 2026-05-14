from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ask import AskRequest, AskResponse
from app.rag.answer_generator import AnswerGenerator
from app.db.database import get_db
from app.services import log_service

router = APIRouter()
generator = AnswerGenerator()

@router.post("", response_model=AskResponse)
def ask_question(request: AskRequest, db: Session = Depends(get_db)):
    result = generator.generate(question=request.question, limit=request.limit)
    
    ask_log_id = log_service.create_ask_log(
        db=db,
        question=result["question"],
        endpoint_type="ask",
        intent="rag_query",
        answer=result["answer"],
        provider=result["provider"],
        model=result["model"],
        latency_ms=result["latency_ms"],
        retrieval_count=len(result["sources"]),
        sources=[s.model_dump() for s in result["sources"]]
    )
    result["ask_log_id"] = ask_log_id
    
    return AskResponse(**result)
