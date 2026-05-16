from typing import List, Dict, Any

class PromptBuilder:
    def build(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        context_texts = []
        for i, chunk in enumerate(chunks, 1):
            title = chunk.get("title", "Unknown")
            content = chunk.get("content", "")
            context_texts.append(f"[Source {i}] Title: {title}\nContent: {content}\n")
            
        context_str = "\n".join(context_texts)
        
        prompt = f"""당신은 AI 기술 레퍼런스 분석 도우미입니다.
사용자의 질문에는 반드시 자연스러운 한국어로 답변합니다.
검색된 문서가 영어여도 한국어로 해석해서 답변합니다.
참고 출처가 부족하면 추측하지 말고 부족하다고 말합니다.
"Based on the retrieved context" 같은 영어 템플릿 문구를 절대 사용하지 않습니다.

Context:
{context_str}

Question: {question}
Answer:"""
        return prompt
