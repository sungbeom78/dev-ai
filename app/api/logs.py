from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.db.database import get_db
from app.services import log_service

router = APIRouter()

class FeedbackRequest(BaseModel):
    rating: str
    comment: Optional[str] = None

@router.get("/asks")
def get_ask_logs(limit: int = 20, db: Session = Depends(get_db)):
    logs = log_service.list_recent_ask_logs(db=db, limit=limit)
    return logs

@router.get("/asks/{ask_log_id}")
def get_ask_log_detail(ask_log_id: int, db: Session = Depends(get_db)):
    log = log_service.get_ask_log_detail(db=db, ask_log_id=ask_log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Ask log not found")
        
    return {
        "id": log.id,
        "question": log.question,
        "endpoint_type": log.endpoint_type,
        "intent": log.intent,
        "answer": log.answer,
        "provider": log.provider,
        "model": log.model,
        "latency_ms": log.latency_ms,
        "retrieval_count": log.retrieval_count,
        "created_at": log.created_at,
        "sources": [
            {
                "id": s.id,
                "document_id": s.document_id,
                "chunk_id": s.chunk_id,
                "title": s.title,
                "content": s.content,
                "score": s.score,
                "source": s.source
            } for s in log.sources
        ],
        "feedback": [
            {
                "id": f.id,
                "rating": f.rating,
                "comment": f.comment,
                "created_at": f.created_at
            } for f in log.feedback
        ]
    }

@router.post("/asks/{ask_log_id}/feedback")
def submit_feedback(ask_log_id: int, request: FeedbackRequest, db: Session = Depends(get_db)):
    log = log_service.get_ask_log_detail(db=db, ask_log_id=ask_log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Ask log not found")
        
    feedback = log_service.create_feedback(
        db=db,
        ask_log_id=ask_log_id,
        rating=request.rating,
        comment=request.comment
    )
    return {"status": "success", "feedback_id": feedback.id}
