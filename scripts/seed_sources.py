import sys
import os

# Add parent directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import ContentSource

SOURCES = [
    {
        "name": "LangGraph Docs",
        "base_url": "https://langchain-ai.github.io/langgraph/",
        "source_type": "docs",
        "category": "agent",
        "enabled": True
    },
    {
        "name": "Model Context Protocol Docs",
        "base_url": "https://modelcontextprotocol.io/",
        "source_type": "docs",
        "category": "ai_engineering",
        "enabled": True
    },
    {
        "name": "Qdrant Docs",
        "base_url": "https://qdrant.tech/documentation/",
        "source_type": "docs",
        "category": "rag",
        "enabled": True
    },
    {
        "name": "OpenAI Skills Docs",
        "base_url": "https://platform.openai.com/docs/guides/function-calling",
        "source_type": "docs",
        "category": "ai_engineering",
        "enabled": False
    },
    {
        "name": "Hugging Face Blog",
        "base_url": "https://huggingface.co/blog",
        "source_type": "blog",
        "category": "open_model",
        "enabled": False
    },
    {
        "name": "Qwen Blog",
        "base_url": "https://qwenlm.github.io/blog/",
        "source_type": "model_blog",
        "category": "open_model",
        "enabled": False
    },
    {
        "name": "Google Gemma Blog",
        "base_url": "https://ai.google.dev/gemma",
        "source_type": "model_blog",
        "category": "open_model",
        "enabled": False
    },
    {
        "name": "Ollama Blog",
        "base_url": "https://ollama.com/blog",
        "source_type": "blog",
        "category": "open_model",
        "enabled": False
    }
]

def seed():
    db = SessionLocal()
    try:
        for s_data in SOURCES:
            existing = db.query(ContentSource).filter(ContentSource.name == s_data["name"]).first()
            if not existing:
                source = ContentSource(**s_data)
                db.add(source)
                print(f"Added source: {s_data['name']}")
            else:
                print(f"Source already exists: {s_data['name']}")
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
