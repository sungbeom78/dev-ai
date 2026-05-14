from pydantic import BaseModel
from typing import List

class AskRequest(BaseModel):
    question: str
    limit: int = 5

class AskSource(BaseModel):
    document_id: int
    chunk_id: int
    title: str
    content: str
    score: float
    source: str

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[AskSource]
    provider: str
    model: str
    latency_ms: int
