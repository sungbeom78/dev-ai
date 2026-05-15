from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(255))
    license = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    char_start = Column(Integer, nullable=False)
    char_end = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="chunks")

class AskLog(Base):
    __tablename__ = "ask_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    endpoint_type = Column(String(50), nullable=False) # "ask" or "agent_ask"
    intent = Column(String(50))
    answer = Column(Text)
    provider = Column(String(50))
    model = Column(String(100))
    latency_ms = Column(Integer)
    retrieval_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sources = relationship("AskSourceLog", back_populates="ask_log", cascade="all, delete-orphan")
    feedback = relationship("FeedbackLog", back_populates="ask_log", cascade="all, delete-orphan")

class AskSourceLog(Base):
    __tablename__ = "ask_source_logs"

    id = Column(Integer, primary_key=True, index=True)
    ask_log_id = Column(Integer, ForeignKey("ask_logs.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(Integer)
    chunk_id = Column(Integer)
    title = Column(String(255))
    content = Column(Text)
    score = Column(Float)
    source = Column(String(255))

    ask_log = relationship("AskLog", back_populates="sources")

class FeedbackLog(Base):
    __tablename__ = "feedback_logs"

    id = Column(Integer, primary_key=True, index=True)
    ask_log_id = Column(Integer, ForeignKey("ask_logs.id", ondelete="CASCADE"), nullable=False)
    rating = Column(String(50), nullable=False) # "up", "down", "neutral"
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ask_log = relationship("AskLog", back_populates="feedback")

class ContentSource(Base):
    __tablename__ = "content_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    base_url = Column(String(255), nullable=False)
    source_type = Column(String(50)) # blog, docs, newsletter, model_blog, manual
    category = Column(String(50)) # open_model, rag, agent, vibe_coding, model_serving, ai_engineering
    enabled = Column(Boolean, default=True)
    crawl_interval_hours = Column(Integer, default=24)
    last_crawled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    crawled_pages = relationship("CrawledPage", back_populates="source", cascade="all, delete-orphan")

class CrawledPage(Base):
    __tablename__ = "crawled_pages"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("content_sources.id", ondelete="CASCADE"), nullable=False)
    url = Column(String(512), nullable=False, unique=True)
    title = Column(String(512))
    content = Column(Text)
    summary = Column(Text)
    author = Column(String(255))
    published_at = Column(DateTime(timezone=True))
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="fetched") # fetched, failed, skipped
    error_message = Column(Text)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="SET NULL"))

    source = relationship("ContentSource", back_populates="crawled_pages")
    document = relationship("Document")
