import os
import sys
import json
import time
from datetime import datetime
import urllib.request
import xml.etree.ElementTree as ET

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.database import SessionLocal
from app.db.models import AIReferenceBriefing, Document, DocumentChunk
from app.rag.llm_provider import get_llm_provider
from app.rag.chunker import CharacterChunker
from app.rag.vector_store import QdrantStore
from app.rag.embeddings import Embedder
import trafilatura

def fetch_hada_rss():
    url = "https://news.hada.io/rss/news"
    try:
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        xml_data = response.content
        root = ET.fromstring(xml_data)
        
        items = []
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ''
            link_el = entry.find('atom:link', ns)
            link = link_el.attrib['href'] if link_el is not None and 'href' in link_el.attrib else ''
            content = entry.find('atom:content', ns).text if entry.find('atom:content', ns) is not None else ''
            
            items.append({
                "title": title,
                "link": link,
                "description": content
            })
            if len(items) >= 5:
                break
        return items
    except Exception as e:
        print(f"Failed to fetch RSS: {e}")
        return []

def generate_briefing(text, original_title, url, provider):
    prompt = f"""You are an expert AI technology analyst in 2026. Review the following news/document content and generate a high-quality trend briefing.
Title: {original_title}
URL: {url}

Content:
{text[:3000]}

Return ONLY a valid JSON object. Do not wrap in markdown blocks.
Format:
{{
    "clean_title": "...",
    "source_url": "{url}",
    "source_name": "GeekNews",
    "topic": "ai_trend",
    "korean_summary": "...",
    "key_changes": "...",
    "why_it_matters": "...",
    "dev_ai_application_note": "...",
    "suggested_tasks": "1. ...\\n2. ...",
    "risk_or_caution": "...",
    "tags": "geeknews, ai",
    "freshness_status": "최신"
}}
"""
    answer, _ = provider.generate_answer(prompt)
    try:
        import re
        match = re.search(r'\{.*\}', answer, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return None
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def run():
    db = SessionLocal()
    provider = get_llm_provider()
    chunker = CharacterChunker()
    vector_store = QdrantStore()
    embedder = Embedder()
    
    print("Fetching hada.io RSS...")
    items = fetch_hada_rss()
    print(f"Found {len(items)} items.")
    
    for item in items:
        url = item['link']
        if db.query(AIReferenceBriefing).filter(AIReferenceBriefing.source_url == url).first():
            print(f"Skipping {url}, already exists.")
            continue
            
        print(f"Processing {url} ...")
        # For geeknews, the description usually contains the summary, but let's try to fetch the actual URL content
        # or use the description if fetch fails.
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded) or item['description']
        else:
            text = item['description']
            
        data = generate_briefing(text, item['title'], url, provider)
        if not data:
            print("Failed to generate briefing.")
            continue
            
        doc = Document(title=data["clean_title"], content=text, source=url, license="crawled")
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        briefing = AIReferenceBriefing(
            clean_title=data["clean_title"],
            source_url=url,
            source_name=data.get("source_name", "GeekNews"),
            topic=data.get("topic", "ai_trend"),
            korean_summary=data.get("korean_summary", ""),
            key_changes=data.get("key_changes", ""),
            why_it_matters=data.get("why_it_matters", ""),
            dev_ai_application_note=data.get("dev_ai_application_note", ""),
            suggested_tasks=data.get("suggested_tasks", ""),
            risk_or_caution=data.get("risk_or_caution", ""),
            tags=data.get("tags", ""),
            quality_score=0.9,
            provider_used=getattr(provider, "mode", "unknown"),
            status="indexed",
            freshness_status="최신",
            document_id=doc.id,
            published_at=datetime.utcnow()
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
            
        print(f"Successfully saved {url}")
        time.sleep(2)
        
    db.close()

if __name__ == "__main__":
    run()
