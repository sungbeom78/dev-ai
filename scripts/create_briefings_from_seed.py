import os
import sys
import time
import trafilatura

# Add the project root to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import AIReferenceBriefing, Document, DocumentChunk
from app.rag.llm_provider import get_llm_provider
from app.rag.chunker import CharacterChunker
from app.rag.vector_store import QdrantStore
from scripts.seed_briefing_urls import seed_data

def generate_briefing(text, seed, provider):
    is_mock = provider.__class__.__name__ == "MockLLMProvider"
    provider_used = "mock" if is_mock else getattr(provider, "mode", "unknown")
    
    if is_mock:
        return {
            "clean_title": seed["title_hint"],
            "korean_summary": "[자동 초안 / Provider 미설정]\n" + text[:200] + "...",
            "key_changes": "Provider 미설정으로 핵심 변화를 분석할 수 없습니다.",
            "why_it_matters": seed["why_collect"] + "\n\n실제 분석 품질 검증은 Google 또는 OpenClaw 설정 후 가능합니다.",
            "dev_ai_application_note": seed["expected_dev_ai_usage"] + "\n\n실제 분석 품질 검증은 Google 또는 OpenClaw 설정 후 가능합니다.",
            "suggested_tasks": "1. Provider 설정\n2. 브리핑 재생성",
            "risk_or_caution": "Mock 응답이므로 신뢰할 수 없습니다.",
            "tags": seed["topic"],
            "quality_score": 0.5,
            "provider_used": provider_used
        }
        
    prompt = f"""다음은 AI 기술 관련 웹 문서의 내용입니다. 이 문서를 읽고 아래의 JSON 형식에 맞게 요약과 적용 메모를 작성해주세요.

문서 내용 (일부):
{text[:3000]}

작성 지침:
1. clean_title: 문서의 제목을 명확하고 한국어로 이해하기 쉽게 적어주세요.
2. korean_summary: 문서의 핵심 내용을 2~3문장으로 한국어로 요약해주세요.
3. key_changes: 무엇이 새롭거나 중요한 변화인지 요약해주세요.
4. why_it_matters: 이 기술/문서가 현재 AI 생태계에서 왜 중요한지 작성해주세요. (참고: {seed['why_collect']})
5. dev_ai_application_note: 내 프로젝트(dev-ai)에 어떻게 적용할 수 있을지 아이디어를 구체적으로 적어주세요. (참고: {seed['expected_dev_ai_usage']})
6. suggested_tasks: 적용을 위한 할 일 목록을 번호 매겨 작성해주세요. (1. ~, 2. ~)
7. risk_or_caution: 적용 시 고려해야 할 위험성, 한계, 불확실성을 적어주세요.
8. tags: 쉼표로 구분된 관련 태그 3~4개 (영문 소문자)

출력 형식은 반드시 아래의 필드를 포함하는 유효한 JSON 이어야 합니다.
{{
    "clean_title": "...",
    "korean_summary": "...",
    "key_changes": "...",
    "why_it_matters": "...",
    "dev_ai_application_note": "...",
    "suggested_tasks": "...",
    "risk_or_caution": "...",
    "tags": "..."
}}
"""
    answer, _ = provider.generate_answer(prompt)
    
    # Extract json
    import json
    try:
        start = answer.find('{')
        end = answer.rfind('}') + 1
        json_str = answer[start:end]
        data = json.loads(json_str)
        data["quality_score"] = 0.9
        data["provider_used"] = provider_used
        return data
    except Exception as e:
        print(f"JSON Parsing Error: {e}\nRaw output: {answer}")
        return {
            "clean_title": seed["title_hint"],
            "korean_summary": "[파싱 오류] " + answer[:200],
            "key_changes": "[파싱 오류]",
            "why_it_matters": seed["why_collect"],
            "dev_ai_application_note": seed["expected_dev_ai_usage"],
            "suggested_tasks": "1. 파싱 수정",
            "risk_or_caution": "[파싱 오류]",
            "tags": seed["topic"],
            "quality_score": 0.5,
            "provider_used": provider_used
        }

def run():
    db = SessionLocal()
    provider = get_llm_provider()
    chunker = CharacterChunker()
    vector_store = QdrantStore()
    
    for seed in seed_data:
        url = seed["url"]
        
        # Check if already exists
        existing = db.query(AIReferenceBriefing).filter(AIReferenceBriefing.source_url == url).first()
        if existing:
            print(f"Skipping {url}, already exists.")
            continue
            
        print(f"Fetching {url}...")
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            import requests
            try:
                downloaded = requests.get(url, timeout=10).text
            except Exception as e:
                print(f"Failed to fetch {url} using requests: {e}")
                continue
                
        text = trafilatura.extract(downloaded)
        if not text:
            from bs4 import BeautifulSoup
            text = BeautifulSoup(downloaded, "html.parser").get_text()[:3000]
            if not text:
                print(f"Failed to extract text from {url}")
                continue
            
        print("Generating briefing...")
        data = generate_briefing(text, seed, provider)
        
        print("Saving to DB and Vector Store...")
        
        # Save Document for raw content
        doc = Document(title=data["clean_title"], content=text, source=url, license="crawled")
        db.add(doc)
        db.commit()
        db.refresh(doc)
        
        # Save Briefing
        briefing = AIReferenceBriefing(
            clean_title=data["clean_title"],
            source_url=url,
            source_name=seed["source_name"],
            topic=seed["topic"],
            korean_summary=data["korean_summary"],
            key_changes=data.get("key_changes", ""),
            why_it_matters=data["why_it_matters"],
            dev_ai_application_note=data["dev_ai_application_note"],
            suggested_tasks=data["suggested_tasks"],
            risk_or_caution=data.get("risk_or_caution", ""),
            tags=data["tags"],
            quality_score=data["quality_score"],
            provider_used=data.get("provider_used", "unknown"),
            status="approved",
            freshness_status=seed.get("freshness_status", "최신"),
            document_id=doc.id
        )
        db.add(briefing)
        db.commit()
        db.refresh(briefing)
        
        # Create a combined content for chunking
        combined_content = f"Title: {briefing.clean_title}\n\nSummary: {briefing.korean_summary}\n\nWhy it matters: {briefing.why_it_matters}\n\nApplication Note: {briefing.dev_ai_application_note}\n\nTasks: {briefing.suggested_tasks}\n\nTags: {briefing.tags}\n\n---\nRaw Content:\n{text}"
        
        from app.rag.embeddings import Embedder
        embedder = Embedder()
        
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
            db.flush() # To get chunk_rec.id if needed, but we use manual id below or Qdrant uuid
            
            vector = embedder.get_embedding(c["content"])
            # Generate a consistent integer ID for Qdrant based on document_id and chunk_index
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
        vector_store.upsert_chunks(chunks_data)
        
        from sqlalchemy.sql import func
        briefing.status = "indexed"
        briefing.indexed_at = func.now()
        db.commit()
        
        print(f"Successfully processed {url}")
        time.sleep(5)

    db.close()

if __name__ == "__main__":
    run()
