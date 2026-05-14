from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api import health, documents, ask, search
from app.db.database import engine
from app.db.models import Base
from app.rag.vector_store import QdrantStore

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    vector_store = QdrantStore()
    vector_store.ensure_collection()
    yield
    # Shutdown

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="BomTS Dev AI",
    description="AI Backend Portfolio MVP",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="", tags=["health"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(ask.router, prefix="/ask", tags=["ask"])
