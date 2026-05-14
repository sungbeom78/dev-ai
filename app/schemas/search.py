from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class SearchResultItem(BaseModel):
    score: float
    document_id: int
    chunk_id: int
    chunk_text: str
    title: str

class SearchResult(BaseModel):
    results: List[SearchResultItem]

class IndexResponse(BaseModel):
    document_id: int
    chunks_indexed: int
