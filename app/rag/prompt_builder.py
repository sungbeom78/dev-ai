from typing import List, Dict, Any

class PromptBuilder:
    def build(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        context_texts = []
        for i, chunk in enumerate(chunks, 1):
            title = chunk.get("title", "Unknown")
            content = chunk.get("content", "")
            context_texts.append(f"[Source {i}] Title: {title}\nContent: {content}\n")
            
        context_str = "\n".join(context_texts)
        
        prompt = f"""You are an AI assistant that answers questions based on the provided context.
Follow these rules strictly:
1. Use the given context to answer the question.
2. If the context does not contain enough information, simply say "I don't know based on the provided context." Do not make up facts.
3. Base your answer on the sources provided.
4. Avoid overly definitive statements if the context is ambiguous.

Context:
{context_str}

Question: {question}
Answer:"""
        return prompt
