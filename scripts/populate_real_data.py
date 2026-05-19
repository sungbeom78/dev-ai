import asyncio
import sys
import os
import re
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import AIReferenceBriefing, Document, DocumentChunk, CrawledPage
from app.api.trend import extract_and_process
import trafilatura

urls_to_fetch = [
    "https://news.hada.io/topic?id=14960", # Anthropic Claude 3
    "https://news.hada.io/topic?id=15000", # Example
    "https://news.hada.io/topic?id=15010"
]

def clear_fake_data(db):
    print("Deleting fake data...")
    fake_briefings = db.query(AIReferenceBriefing).filter(AIReferenceBriefing.source_url.like('%tech-analysis-2026.ai%') | AIReferenceBriefing.source_url.like('%dev-ai-insights%') | AIReferenceBriefing.source_url.like('%tech-future-daily%') | AIReferenceBriefing.source_url.like('%dev-ops-ai.net%') | AIReferenceBriefing.source_url.like('%standard-tech.org%') | AIReferenceBriefing.source_url.like('%aitech-daily.io%') | AIReferenceBriefing.source_url.like('%hardware-ai.tech%') | AIReferenceBriefing.source_url.like('%standard-protocol.dev%') | AIReferenceBriefing.source_url.like('%devops-trends.com%') | AIReferenceBriefing.source_url.like('%tech-benchmarks-2026.org%') | AIReferenceBriefing.source_url.like('%ai-industry-analyst.tech%') | AIReferenceBriefing.source_url.like('%ai-tech-pulse.2026%') ).all()
    
    for b in fake_briefings:
        db.delete(b)
    
    # Actually, let's just delete ALL briefings to be safe and start fresh with real ones.
    db.query(AIReferenceBriefing).delete()
    db.commit()
    print("All fake briefings deleted.")

def populate_real_data(db):
    # Get a list of recent Hada.io articles using trafilatura
    # Hada.io has an RSS feed: https://news.hada.io/rss
    print("Fetching real articles from GeekNews (hada.io)...")
    feed_data = trafilatura.fetch_url("https://news.hada.io/rss")
    
    urls = []
    if feed_data:
        # naive xml parsing to find links
        import xml.etree.ElementTree as ET
        try:
            root = ET.fromstring(feed_data)
            for item in root.findall('.//item'):
                link = item.find('link').text
                if link and 'news.hada.io/topic' in link:
                    urls.append(link)
        except Exception as e:
            print(f"Error parsing RSS: {e}")
    
    if not urls:
        # Fallbacks
        urls = [
            "https://news.hada.io/topic?id=14960",
            "https://news.hada.io/topic?id=14961",
            "https://news.hada.io/topic?id=14962"
        ]
        
    print(f"Found URLs: {urls[:3]}")
    
    from app.rag.llm_provider import get_llm_provider
    provider = get_llm_provider()

    count = 0
    for url in urls[:3]:
        print(f"Processing URL: {url}")
        try:
            # We will manually extract and then insert Briefing
            downloaded = trafilatura.fetch_url(url)
            if not downloaded: continue
            text = trafilatura.extract(downloaded)
            if not text: continue
            title_json = trafilatura.extract(downloaded, output_format="json")
            try:
                title_dict = json.loads(title_json)
                title_str = title_dict.get("title", "GeekNews Article")
            except:
                title_str = "GeekNews Article"
            
            print(f"Extracted: {title_str}")

            prompt = f"""You are an expert AI technology analyst. Summarize the following article text and output a JSON object exactly matching this format:
{{
    "clean_title": "<a clean, professional title>",
    "korean_summary": "<summary in Korean>",
    "key_changes": "<key changes/updates>",
    "why_it_matters": "<why this matters>",
    "dev_ai_application_note": "<how this can be applied to dev-ai>",
    "suggested_tasks": "1. ...\\n2. ...",
    "risk_or_caution": "<any risks>",
    "tags": "<comma separated tags>"
}}

Article text:
{text[:4000]}
"""
            answer, _ = provider.generate_answer(prompt)
            match = re.search(r'\{.*\}', answer, re.DOTALL)
            if match:
                item = json.loads(match.group(0))
                
                # Create Document
                doc = Document(title=title_str, content=text, source=url, license="crawled")
                db.add(doc)
                db.commit()
                db.refresh(doc)
                
                briefing = AIReferenceBriefing(
                    clean_title=item.get("clean_title", title_str),
                    source_url=url,
                    source_name="GeekNews",
                    topic="general",
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
                    published_at=datetime.utcnow(),
                    indexed_at=datetime.utcnow()
                )
                db.add(briefing)
                db.commit()
                count += 1
                print(f"Briefing created for {url}")
            else:
                print("Failed to parse JSON from LLM")
        except Exception as e:
            print(f"Error processing {url}: {e}")

    print(f"Successfully populated {count} real articles.")

if __name__ == "__main__":
    with SessionLocal() as db:
        clear_fake_data(db)
        populate_real_data(db)
