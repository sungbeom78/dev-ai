from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "BomTS Dev AI is running."}

@router.get("/system/status")
async def system_status():
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
            "status": "online",
            "collection": "documents",
            "vector_count": 0 # This could be real if queried
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
            "source_count": 0,
            "crawled_page_count": 0,
            "last_crawled_at": None
        },
        "scheduler": {
            "enabled": False,
            "interval_hours": 6,
            "last_run_at": None
        }
    }
