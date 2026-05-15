from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import trafilatura
from bs4 import BeautifulSoup
import requests

from app.db.database import get_db
from app.db.models import ContentSource, CrawledPage, Document

router = APIRouter()

class SourceCreate(BaseModel):
    name: str
    base_url: str
    source_type: str = "blog"
    category: str = "ai_engineering"
    enabled: bool = True
    crawl_interval_hours: int = 24

class SourceResponse(BaseModel):
    id: int
    name: str
    base_url: str
    source_type: str
    category: str
    enabled: bool
    crawl_interval_hours: int
    last_crawled_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class FetchUrlRequest(BaseModel):
    url: str
    source_name: str = "manual-url"
    category: str = "ai_engineering"

@router.get("", response_model=List[SourceResponse])
def get_sources(db: Session = Depends(get_db)):
    return db.query(ContentSource).all()

@router.post("", response_model=SourceResponse)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    db_source = ContentSource(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@router.patch("/{source_id}")
def update_source(source_id: int, enabled: bool, db: Session = Depends(get_db)):
    db_source = db.query(ContentSource).filter(ContentSource.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    db_source.enabled = enabled
    db.commit()
    return {"status": "ok"}

def extract_content(url: str):
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            # Fallback to requests + bs4 if trafilatura fails to fetch
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            downloaded = resp.text
            
        text = trafilatura.extract(downloaded)
        
        # Try to get title via BeautifulSoup if trafilatura extraction lacks it
        title = None
        soup = BeautifulSoup(downloaded, "html.parser")
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
            
        if not text:
            # simple fallback
            text = soup.get_text(separator="\n", strip=True)
            
        return {"title": title or "Untitled", "content": text}
    except Exception as e:
        return {"error": str(e)}

@router.post("/fetch-url")
def fetch_url(req: FetchUrlRequest, db: Session = Depends(get_db)):
    # Find or create source
    source = db.query(ContentSource).filter(ContentSource.name == req.source_name).first()
    if not source:
        source = ContentSource(
            name=req.source_name,
            base_url="manual",
            source_type="manual",
            category=req.category
        )
        db.add(source)
        db.commit()
        db.refresh(source)

    # Check if crawled page exists
    page = db.query(CrawledPage).filter(CrawledPage.url == req.url).first()
    if page and page.document_id:
        return {
            "document_id": page.document_id,
            "title": page.title,
            "url": page.url,
            "content_length": len(page.content) if page.content else 0,
            "status": "already_fetched"
        }

    # Extract
    extracted = extract_content(req.url)
    if "error" in extracted:
        if not page:
            page = CrawledPage(source_id=source.id, url=req.url, status="failed", error_message=extracted["error"])
            db.add(page)
            db.commit()
        raise HTTPException(status_code=400, detail=f"Failed to extract: {extracted['error']}")
    
    title = extracted.get("title", "Untitled")
    content = extracted.get("content", "")

    # Save to documents
    doc = Document(
        title=title,
        content=content,
        source=req.url,
        license="source-linked"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    if not page:
        page = CrawledPage(
            source_id=source.id,
            url=req.url,
            title=title,
            content=content,
            status="fetched",
            document_id=doc.id
        )
        db.add(page)
    else:
        page.title = title
        page.content = content
        page.status = "fetched"
        page.document_id = doc.id

    db.commit()

    return {
        "document_id": doc.id,
        "title": title,
        "url": req.url,
        "content_length": len(content),
        "status": "fetched"
    }

@router.post("/{source_id}/crawl")
def crawl_source(source_id: int, db: Session = Depends(get_db)):
    source = db.query(ContentSource).filter(ContentSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    # For MVP, we won't fully automate crawling within the API here,
    # The API can just be a trigger, but complex logic is in the script.
    # We will just return a message saying it should be run via CLI or implemented via background tasks.
    return {"status": "ok", "message": "Triggered crawl (use CLI script for actual logic in MVP)"}
