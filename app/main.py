from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import health, documents, ask
from app.db.database import engine
from app.db.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown

app = FastAPI(
    title="BomTS Dev AI",
    description="AI Backend Portfolio MVP",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(health.router, prefix="", tags=["health"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(ask.router, prefix="/ask", tags=["ask"])
