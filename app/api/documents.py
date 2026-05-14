from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import Document, DocumentChunk
from app.schemas.document import DocumentCreate, DocumentResponse, ChunkResponse
from app.rag.chunker import CharacterChunker

router = APIRouter()

@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(**doc.model_dump())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.get("", response_model=List[DocumentResponse])
def get_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/{document_id}/chunks", response_model=List[ChunkResponse], status_code=status.HTTP_201_CREATED)
def create_document_chunks(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete existing chunks if any to allow re-chunking
    db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
    
    chunker = CharacterChunker(chunk_size=800, chunk_overlap=100)
    chunk_data = chunker.chunk_text(doc.content)
    
    db_chunks = []
    for data in chunk_data:
        chunk = DocumentChunk(document_id=document_id, **data)
        db.add(chunk)
        db_chunks.append(chunk)
        
    db.commit()
    
    for chunk in db_chunks:
        db.refresh(chunk)
        
    return db_chunks

@router.get("/{document_id}/chunks", response_model=List[ChunkResponse])
def get_document_chunks(document_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).order_by(DocumentChunk.chunk_index).all()
    return chunks
