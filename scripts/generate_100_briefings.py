import os
import sys
import json
import time
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.database import SessionLocal
from app.db.models import AIReferenceBriefing, Document, DocumentChunk
from app.rag.llm_provider import get_llm_provider
from app.rag.chunker import CharacterChunker
from app.rag.vector_store import QdrantStore
from app.rag.embeddings import Embedder

def generate_batch(provider, batch_index):
    prompt = f"""You are an expert AI technology analyst in 2026. Generate exactly 5 distinct, high-quality AI technology trend briefings that are highly relevant to 2026. Include cutting-edge topics like Harness, Skills, OpenClaw, Hermes Agent, Model Context Protocol, LangGraph, Qwen3, Gemma 4, Agentic workflows, local LLMs, etc. All briefings must have published dates within the last 5 days.

Batch {batch_index}: Make sure these 5 are unique and different from other typical news.
Return ONLY a valid JSON array of objects. Do not wrap in markdown blocks.
Format for each object:
{{
    "clean_title": "...",
    "source_url": "https://example.com/ai-news/2026-...",
    "source_name": "...",
    "topic": "...",
    "korean_summary": "...",
    "key_changes": "...",
    "why_it_matters": "...",
    "dev_ai_application_note": "...",
    "suggested_tasks": "1. ...\\n2. ...",
    "risk_or_caution": "...",
    "tags": "...",
    "freshness_status": "최신"
}}
"""
    answer, _ = provider.generate_answer(prompt)
    try:
        import re
        match = re.search(r'\[.*\]', answer, re.DOTALL)
        if match:
            json_str = match.group(0)
            data = json.loads(json_str)
            return data
        else:
            print("No JSON array found.")
            return []
    except Exception as e:
        print(f"Error parsing JSON for batch {batch_index}: {e}")
        return []

def run():
    db = SessionLocal()
    provider = get_llm_provider()
    chunker = CharacterChunker()
    vector_store = QdrantStore()
    embedder = Embedder()
    
    total_generated = 0
    
    for batch_id in range(20):
        print(f"Generating batch {batch_id+1}/5...")
        items = generate_batch(provider, batch_id)
        print(f"Found {len(items)} items in batch.")
        
        for item in items:
            # check if exists
            url = item.get("source_url", f"https://example.com/ai-news/{time.time()}")
            if db.query(AIReferenceBriefing).filter(AIReferenceBriefing.source_url == url).first():
                continue
                
            text = item.get("korean_summary", "") + "\n\n" + item.get("key_changes", "")
            
            doc = Document(title=item["clean_title"], content=text, source=url, license="generated")
            db.add(doc)
            db.commit()
            db.refresh(doc)
            
            briefing = AIReferenceBriefing(
                clean_title=item["clean_title"],
                source_url=url,
                source_name=item.get("source_name", "AI Tech News"),
                topic=item.get("topic", "ai_trend"),
                korean_summary=item.get("korean_summary", ""),
                key_changes=item.get("key_changes", ""),
                why_it_matters=item.get("why_it_matters", ""),
                dev_ai_application_note=item.get("dev_ai_application_note", ""),
                suggested_tasks=item.get("suggested_tasks", ""),
                risk_or_caution=item.get("risk_or_caution", ""),
                tags=item.get("tags", ""),
                quality_score=0.9,
                provider_used=getattr(provider, "mode", "unknown"),
                status="indexed",
                freshness_status="최신",
                document_id=doc.id,
                published_at=datetime.utcnow() - timedelta(days=batch_id)
            )
            briefing.indexed_at = datetime.utcnow()
            db.add(briefing)
            db.commit()
            db.refresh(briefing)
            
            combined_content = f"Title: {briefing.clean_title}\n\nSummary: {briefing.korean_summary}\n\nWhy it matters: {briefing.why_it_matters}\n\nApplication Note: {briefing.dev_ai_application_note}\n\nTasks: {briefing.suggested_tasks}\n\nTags: {briefing.tags}\n\n---\nRaw Content:\n{text}"
            
            chunks = chunker.chunk_text(combined_content)
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
                    "title": briefing.clean_title,
                    "content": c["content"],
                    "source": url
                })
                
            db.commit()
            vector_store.ensure_collection()
            if chunks_data:
                vector_store.upsert_chunks(chunks_data)
                
            total_generated += 1
            
        time.sleep(2) # avoid rate limits
        
    print(f"Total {total_generated} briefings generated.")
    db.close()

if __name__ == "__main__":
    run()
