from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List, Optional
import trafilatura
from trafilatura import sitemaps

from app.db.database import get_db
from app.db.models import CrawledPage, ContentSource, Document
from app.schemas.ask import AskRequest, AskResponse
from app.rag.answer_generator import AnswerGenerator
from app.services import log_service
from app.rag.chunker import CharacterChunker
from app.rag.vector_store import QdrantStore

router = APIRouter()
generator = AnswerGenerator()
chunker = CharacterChunker()
vector_store = QdrantStore()

class FetchUrlRequest(BaseModel):
    url: str
    topic: str = "general"
    translate: bool = True
    summarize: bool = True
    index: bool = True

class CrawlLatestRequest(BaseModel):
    limit: int = 10
    translate: bool = True
    summarize: bool = True
    index: bool = True

@router.get("/documents")
def get_trend_documents(limit: int = 100, db: Session = Depends(get_db)):
    pages = db.query(CrawledPage).order_by(desc(CrawledPage.id)).limit(limit).all()
    results = []
    for p in pages:
        source_name = "Manual"
        if p.source:
            source_name = p.source.name
            
        results.append({
            "document_id": p.document_id,
            "title": p.title,
            "source": p.url,
            "source_name": source_name,
            "topic": p.source.category if p.source else "general",
            "language": "ko" if p.summary or "한국어" in str(p.title) else "en",
            "translated": True if p.summary else False,
            "indexed": True if p.document_id else False,
            "created_at": p.crawled_at.isoformat() if p.crawled_at else None
        })
    return {"items": results, "total": len(results)}

@router.post("/ask", response_model=AskResponse)
def trend_ask(request: AskRequest, db: Session = Depends(get_db)):
    result = generator.generate(question=request.question, limit=request.limit, is_trend_search=True)
    
    ask_log_id = log_service.create_ask_log(
        db=db,
        question=result["question"],
        endpoint_type="trend_ask",
        intent="rag_query",
        answer=result["answer"],
        provider=result["provider"],
        model=result["model"],
        latency_ms=result["latency_ms"],
        retrieval_count=len(result["sources"]),
        sources=[s.model_dump() for s in result["sources"]]
    )
    result["ask_log_id"] = ask_log_id
    
    return AskResponse(**result)

def extract_and_process(url: str, topic: str, req_translate: bool, req_summarize: bool, req_index: bool, db: Session, source_name: str = "manual"):
    source = db.query(ContentSource).filter(ContentSource.name == source_name).first()
    if not source:
        source = ContentSource(name=source_name, base_url="manual", source_type="manual", category=topic)
        db.add(source)
        db.commit()
        db.refresh(source)
        
    page = db.query(CrawledPage).filter(CrawledPage.url == url).first()
    if page and page.document_id:
        return page

    # Extract
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise Exception("Failed to fetch URL")
    text = trafilatura.extract(downloaded)
    if not text:
        raise Exception("Failed to extract content")
        
    title = trafilatura.extract(downloaded, output_format="json")
    import json
    try:
        title_dict = json.loads(title)
        title_str = title_dict.get("title", "Untitled")
    except:
        title_str = "Untitled"

    # Save Document
    doc = Document(title=title_str, content=text, source=url, license="crawled")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    # Save CrawledPage
    if not page:
        page = CrawledPage(source_id=source.id, url=url, title=title_str, content=text, status="fetched", document_id=doc.id)
        db.add(page)
    else:
        page.title = title_str
        page.content = text
        page.status = "fetched"
        page.document_id = doc.id
    db.commit()
    db.refresh(page)
    
    # Chunk and index
    if req_index:
        chunks = chunker.chunk_text(doc.content)
        from app.db.models import DocumentChunk
        for c in chunks:
            chunk_rec = DocumentChunk(
                document_id=doc.id, 
                chunk_index=c["chunk_index"], 
                content=c["content"], 
                char_start=c["char_start"], 
                char_end=c["char_end"]
            )
            db.add(chunk_rec)
        db.commit()
        
        db.refresh(doc)
        vector_store.add_document_chunks(doc)
        
    return page

@router.post("/fetch-url")
def fetch_trend_url(req: FetchUrlRequest, db: Session = Depends(get_db)):
    try:
        page = extract_and_process(req.url, req.topic, req.translate, req.summarize, req.index, db)
        return {
            "document_id": page.document_id,
            "title": page.title,
            "translated": req.translate,
            "indexed": req.index,
            "source": req.url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/crawl-latest")
def crawl_trend_latest(req: CrawlLatestRequest, db: Session = Depends(get_db)):
    sources = db.query(ContentSource).filter(ContentSource.enabled == True).all()
    crawled_count = 0
    errors = []
    
    # We will just use trafilatura feed finding for a very basic automated fetch.
    for source in sources:
        if crawled_count >= req.limit:
            break
        try:
            feed_urls = sitemaps.sitemap_search(source.base_url)
            # If no sitemap, just use the base url as a single page or fallback
            if not feed_urls:
                feed_urls = [source.base_url]
            
            # just take a few from each source to not overload
            for url in feed_urls[:2]:
                if crawled_count >= req.limit:
                    break
                
                # Check if already fetched
                existing = db.query(CrawledPage).filter(CrawledPage.url == url).first()
                if existing and existing.document_id:
                    continue
                    
                extract_and_process(url, source.category, req.translate, req.summarize, req.index, db, source.name)
                crawled_count += 1
                
        except Exception as e:
            errors.append(f"Source {source.name}: {str(e)}")
            
    return {"crawled_count": crawled_count, "errors": errors, "message": "Crawling finished."}
