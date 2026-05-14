from fastapi import FastAPI
from app.api import health, documents, ask

app = FastAPI(
    title="BomTS Dev AI",
    description="AI Backend Portfolio MVP",
    version="0.1.0"
)

app.include_router(health.router, prefix="", tags=["health"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(ask.router, prefix="/api/ask", tags=["ask"])
