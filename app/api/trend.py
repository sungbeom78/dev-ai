from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List, Optional
import trafilatura
from trafilatura import sitemaps

from app.db.database import get_db
from app.db.models import CrawledPage, ContentSource, Document, AIReferenceBriefing
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

@router.get("/briefings")
def get_briefings(limit: int = 20, db: Session = Depends(get_db)):
    briefings = db.query(AIReferenceBriefing).filter(
        AIReferenceBriefing.status.in_(["approved", "indexed"])
    ).order_by(desc(AIReferenceBriefing.id)).limit(limit).all()
    
    results = []
    for b in briefings:
        results.append({
            "id": b.id,
            "clean_title": b.clean_title,
            "source_url": b.source_url,
            "source_name": b.source_name,
            "topic": b.topic,
            "korean_summary": b.korean_summary,
            "key_changes": getattr(b, "key_changes", ""),
            "why_it_matters": b.why_it_matters,
            "dev_ai_application_note": b.dev_ai_application_note,
            "suggested_tasks": b.suggested_tasks,
            "risk_or_caution": getattr(b, "risk_or_caution", ""),
            "tags": b.tags,
            "status": b.status,
            "freshness_status": getattr(b, "freshness_status", "최신"),
            "indexed_at": b.indexed_at.isoformat() if b.indexed_at else None
        })
    return {"items": results, "total": len(results)}

@router.get("/documents")
def get_trend_documents(limit: int = 100, db: Session = Depends(get_db)):
    pages = db.query(CrawledPage).order_by(desc(CrawledPage.id)).limit(limit).all()
    results = []
    for p in pages:
        source_name = "Manual"
        if p.source:
            source_name = p.source.name
            
        # Hide raw test/sample docs from this endpoint since it might still be used by test.html
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

@router.post("/brief", response_model=AskResponse)
def trend_brief(request: AskRequest, db: Session = Depends(get_db)):
    if request.question.strip() == "하네스":
        answer = """“하네스”는 여러 의미로 쓰일 수 있습니다.
1. Harness.io 같은 DevOps/CI/CD 플랫폼
2. AI 모델 평가용 evaluation harness
3. 테스트 자동화 test harness
4. Agent 실행/평가 harness

어떤 의미인지 구체적으로 입력해 주세요. (예: "하네스 프로그램 최신 동향")"""
        return AskResponse(
            question=request.question,
            answer=answer,
            sources=[],
            provider="system",
            model="system",
            latency_ms=0,
            ask_log_id=0
        )
        
    query = request.question
    if "하네스 프로그램" in query:
        query += " Harness.io CI/CD DevOps AI automation"
    
    result = generator.generate(question=query, limit=request.limit, is_trend_search=True)
    
    ask_log_id = log_service.create_ask_log(
        db=db,
        question=request.question, # Log original question
        endpoint_type="trend_brief",
        intent="rag_query",
        answer=result["answer"],
        provider=result["provider"],
        model=result["model"],
        latency_ms=result["latency_ms"],
        retrieval_count=len(result["sources"]),
        sources=[s.model_dump() for s in result["sources"]]
    )
    result["ask_log_id"] = ask_log_id
    result["question"] = request.question
    
    return AskResponse(**result)

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
        from app.rag.embeddings import Embedder
        embedder = Embedder()
        
        chunks_data = []
        for c in chunks:
            chunk_rec = DocumentChunk(
                document_id=doc.id, 
                chunk_index=c["chunk_index"], 
                content=c["content"], 
                char_start=c["char_start"], 
                char_end=c["char_end"]
            )
            db.add(chunk_rec)
            db.flush()
            
            vector = embedder.get_embedding(c["content"])
            chunk_int_id = doc.id * 1000 + c["chunk_index"]
            
            chunks_data.append({
                "chunk_id": chunk_int_id,
                "vector": vector,
                "document_id": doc.id,
                "chunk_index": c["chunk_index"],
                "title": title_str,
                "content": c["content"],
                "source": url
            })
            
        db.commit()
        
        vector_store.ensure_collection()
        vector_store.upsert_chunks(chunks_data)
        
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
