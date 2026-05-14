from fastapi import APIRouter
from app.schemas.search import SearchRequest, SearchResult, SearchResultItem
from app.rag.embeddings import Embedder
from app.rag.vector_store import QdrantStore

router = APIRouter()
embedder = Embedder()
vector_store = QdrantStore()

@router.post("", response_model=SearchResult)
def search_documents(request: SearchRequest):
    query_vector = embedder.get_embedding(request.query)
    
    hits = vector_store.search(query_vector=query_vector, limit=request.limit)
    
    results = []
    for hit in hits:
        results.append(
            SearchResultItem(
                score=hit.score,
                document_id=hit.payload.get("document_id", 0),
                chunk_id=hit.id,
                chunk_text=hit.payload.get("content", ""),
                title=hit.payload.get("title", "")
            )
        )
        
    return SearchResult(results=results)
