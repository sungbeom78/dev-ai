from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import ContentSource, CrawledPage
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse

router = APIRouter()

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "BomTS Dev AI is running."}

@router.get("/system/status")
async def system_status(db: Session = Depends(get_db)):
    # Get db counts
    source_count = db.query(ContentSource).count()
    crawled_page_count = db.query(CrawledPage).count()
    
    # Get qdrant count
    vector_count = 0
    qdrant_status = "offline"
    
    # Check if QDRANT_URL contains 'qdrant' hostname, we might be running on PM2 host
    qdrant_urls_to_try = [QDRANT_URL]
    if "qdrant" in QDRANT_URL:
        qdrant_urls_to_try.append(QDRANT_URL.replace("qdrant", "localhost"))

    for url in qdrant_urls_to_try:
        try:
            client = QdrantClient(url=url)
            # 1. Check if Qdrant itself is online
            collections_response = client.get_collections()
            qdrant_status = "online"
            
            # 2. Check if the 'documents' collection exists and get count
            if any(c.name == "documents" for c in collections_response.collections):
                collection_info = client.get_collection(collection_name="documents")
                vector_count = getattr(collection_info, "points_count", 0)
                if hasattr(collection_info, "vectors_count") and collection_info.vectors_count:
                    vector_count = collection_info.vectors_count
                
            break  # Success
        except Exception:
            pass

    return {
        "api": {
            "status": "online",
            "version": "phase-9"
        },
        "database": {
            "type": "postgresql",
            "status": "online"
        },
        "vector_db": {
            "type": "qdrant",
            "status": qdrant_status,
            "collection": "documents",
            "vector_count": vector_count
        },
        "llm": {
            "provider": os.getenv("LLM_PROVIDER", "mock"),
            "model": os.getenv("OPENCLAW_DEFAULT_MODEL", "mock-llm"),
            "openclaw_enabled": os.getenv("OPENCLAW_ENABLED", "false").lower() == "true",
            "google_enabled": os.getenv("GOOGLE_PROVIDER_ENABLED", "false").lower() == "true"
        },
        "embedding": {
            "provider": os.getenv("EMBEDDING_MODE", "mock"),
            "dimension": 1536
        },
        "reference_pipeline": {
            "source_count": source_count,
            "crawled_page_count": crawled_page_count,
            "last_crawled_at": None
        },
        "scheduler": {
            "enabled": False,
            "interval_hours": 6,
            "last_run_at": None
        }
    }
