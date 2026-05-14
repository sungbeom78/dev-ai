from sqlalchemy.orm import Session
from app.db import models
from typing import List, Dict, Any, Optional

def create_ask_log(
    db: Session,
    question: str,
    endpoint_type: str,
    intent: Optional[str],
    answer: str,
    provider: str,
    model: str,
    latency_ms: int,
    retrieval_count: int,
    sources: List[Dict[str, Any]]
) -> int:
    ask_log = models.AskLog(
        question=question,
        endpoint_type=endpoint_type,
        intent=intent,
        answer=answer,
        provider=provider,
        model=model,
        latency_ms=latency_ms,
        retrieval_count=retrieval_count
    )
    db.add(ask_log)
    db.commit()
    db.refresh(ask_log)
    
    # Create sources
    if sources:
        for s in sources:
            source_log = models.AskSourceLog(
                ask_log_id=ask_log.id,
                document_id=s.get("document_id"),
                chunk_id=s.get("chunk_id"),
                title=s.get("title"),
                content=s.get("content"),
                score=s.get("score"),
                source=s.get("source")
            )
            db.add(source_log)
        db.commit()
        
    return ask_log.id

def create_feedback(
    db: Session,
    ask_log_id: int,
    rating: str,
    comment: Optional[str]
) -> models.FeedbackLog:
    feedback = models.FeedbackLog(
        ask_log_id=ask_log_id,
        rating=rating,
        comment=comment
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

def list_recent_ask_logs(db: Session, limit: int = 20):
    return db.query(models.AskLog).order_by(models.AskLog.created_at.desc()).limit(limit).all()

def get_ask_log_detail(db: Session, ask_log_id: int):
    return db.query(models.AskLog).filter(models.AskLog.id == ask_log_id).first()
