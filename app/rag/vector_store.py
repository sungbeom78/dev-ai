import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")

class QdrantStore:
    def __init__(self, collection_name: str = "documents"):
        url_to_try = QDRANT_URL
        try:
            # First try the configured URL
            self.client = QdrantClient(url=url_to_try)
            self.client.get_collections() # test connection
        except Exception:
            if "qdrant" in url_to_try:
                # Fallback to localhost for PM2 host execution
                url_to_try = url_to_try.replace("qdrant", "localhost")
                self.client = QdrantClient(url=url_to_try)
            else:
                raise
                
        self.collection_name = collection_name
        self.dimension = 1536 # Should match embedder
        
    def ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.dimension,
                    distance=models.Distance.COSINE
                )
            )
            
    def upsert_chunks(self, chunks_data: List[Dict[str, Any]]):
        points = []
        for chunk in chunks_data:
            points.append(
                models.PointStruct(
                    id=chunk['chunk_id'], # integer
                    vector=chunk['vector'],
                    payload={
                        "document_id": chunk['document_id'],
                        "chunk_index": chunk['chunk_index'],
                        "title": chunk.get('title', ''),
                        "content": chunk['content'],
                        "source": chunk.get('source', '')
                    }
                )
            )
            
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

    def search(self, query_vector: List[float], limit: int = 5):
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )
        return search_result.points
