from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
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
