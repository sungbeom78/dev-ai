import sys
import os

# Add parent directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import Document, DocumentChunk
from app.api.documents import index_document
from app.rag.vector_store import QdrantStore

def main():
    db = SessionLocal()
    try:
        # Ensure collection exists first
        vector_store = QdrantStore()
        vector_store.ensure_collection()
        
        docs = db.query(Document).all()
        indexed_count = 0
        for doc in docs:
            # check if doc is already indexed in qdrant? 
            # Or just check if it has chunks
            chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).all()
            if not chunks:
                print(f"Indexing Document {doc.id}: {doc.title}...")
                index_document(doc.id, db)
                indexed_count += 1
            else:
                print(f"Document {doc.id} already has chunks.")
                
        print(f"Successfully indexed {indexed_count} new documents.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
