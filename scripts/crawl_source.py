import sys
import os
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Add parent directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import ContentSource
from app.api.sources import extract_content
from app.db.models import Document, CrawledPage

def crawl_url(db, url, source_id, source_name, category):
    print(f"Crawling URL: {url}")
    # Check if crawled page exists
    page = db.query(CrawledPage).filter(CrawledPage.url == url).first()
    if page and page.document_id:
        print(f"  -> Already crawled as doc_id {page.document_id}")
        return

    extracted = extract_content(url)
    if "error" in extracted:
        print(f"  -> Failed to extract: {extracted['error']}")
        if not page:
            page = CrawledPage(source_id=source_id, url=url, status="failed", error_message=extracted["error"])
            db.add(page)
            db.commit()
        return

    title = extracted.get("title", "Untitled")
    content = extracted.get("content", "")

    doc = Document(
        title=title,
        content=content,
        source=url,
        license="source-linked"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    if not page:
        page = CrawledPage(
            source_id=source_id,
            url=url,
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
    print(f"  -> Success! Created doc_id {doc.id}")

def crawl_source(db, source_name, limit):
    source = db.query(ContentSource).filter(ContentSource.name == source_name).first()
    if not source:
        print(f"Source not found: {source_name}")
        return

    print(f"Fetching links from {source.base_url}...")
    try:
        resp = requests.get(source.base_url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/'):
                href = urljoin(source.base_url, href)
            # basic filter to avoid obvious non-articles
            if href.startswith('http') and source.base_url in href and href != source.base_url:
                if href not in links:
                    links.append(href)
                    
        print(f"Found {len(links)} links. Limiting to {limit}.")
        links = links[:limit]
        
        for link in links:
            crawl_url(db, link, source.id, source.name, source.category)
            
    except Exception as e:
        print(f"Failed to fetch source page: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl AI Trend Sources")
    parser.add_argument("--source", type=str, help="Source name to crawl (e.g., 'Hugging Face Blog')")
    parser.add_argument("--url", type=str, help="Specific URL to crawl")
    parser.add_argument("--limit", type=int, default=5, help="Number of pages to crawl")
    
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        if args.url:
            # For manual URL, use a manual source
            source = db.query(ContentSource).filter(ContentSource.name == "manual-url").first()
            if not source:
                source = ContentSource(name="manual-url", base_url="manual", source_type="manual", category="ai_engineering")
                db.add(source)
                db.commit()
                db.refresh(source)
            crawl_url(db, args.url, source.id, "manual-url", "ai_engineering")
        elif args.source:
            crawl_source(db, args.source, args.limit)
        else:
            print("Please provide --source or --url")
    finally:
        db.close()
