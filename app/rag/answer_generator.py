import time
from typing import Dict, Any
from app.rag.embeddings import Embedder
from app.rag.vector_store import QdrantStore
from app.rag.prompt_builder import PromptBuilder
from app.rag.llm_provider import get_llm_provider
from app.schemas.ask import AskSource

class AnswerGenerator:
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = QdrantStore()
        self.prompt_builder = PromptBuilder()
        self.llm_provider = get_llm_provider()

    def generate(self, question: str, limit: int = 5, is_trend_search: bool = False) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Embed question
        query_vector = self.embedder.get_embedding(question)
        
        # 2. Search vector store
        hits = self.vector_store.search(query_vector=query_vector, limit=limit * 2) # Fetch more to filter
        
        # Prepare context chunks
        chunks = []
        sources = []
        for hit in hits:
            title = hit.payload.get("title", "")
            source = hit.payload.get("source", "")
            score = hit.score
            
            if is_trend_search:
                if score < 0.3 or score <= 0:
                    continue
                if any(x in title for x in ["Sample", "Test", "Phase"]):
                    continue
                if any(x in source for x in ["phase", "test", "check-script", "reference-sample", "manual"]):
                    continue
                if title in ["MCP Concept Sample", "Phase 3 Vector Search Test", "undefined", "Untitled", "null"]:
                    continue
                if source in ["undefined", "null"]:
                    continue
            
            chunk_data = {
                "title": title,
                "content": hit.payload.get("content", ""),
                "source": source,
                "document_id": hit.payload.get("document_id", 0),
                "chunk_id": hit.id,
                "score": score
            }
            chunks.append(chunk_data)
            
            sources.append(AskSource(
                document_id=chunk_data["document_id"],
                chunk_id=chunk_data["chunk_id"],
                title=chunk_data["title"],
                content=chunk_data["content"],
                score=chunk_data["score"],
                source=chunk_data["source"]
            ))
            
            if len(chunks) >= limit:
                break
            
        if not chunks and is_trend_search:
            answer = "현재 인덱싱된 AI 기술 레퍼런스 중에서 질문과 충분히 관련 있는 문서를 찾지 못했습니다.\n먼저 관련 문서를 수집하거나, 질문을 더 구체적으로 입력해 주세요."
            model_name = "system"
        else:
            # 3. Build prompt
            prompt = self.prompt_builder.build(question, chunks)
            
            # 4. Generate answer
            answer, model_name = self.llm_provider.generate_answer(prompt)
        
        # 5. Return result
        latency_ms = int((time.time() - start_time) * 1000)
        provider_name = self.llm_provider.__class__.__name__.replace("LLMProvider", "").lower()
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "provider": provider_name,
            "model": model_name,
            "latency_ms": latency_ms
        }
