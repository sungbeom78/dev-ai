from typing import List, Dict, Any

class PromptBuilder:
    def build(self, question: str, chunks: List[Dict[str, Any]]) -> str:
        context_texts = []
        for i, chunk in enumerate(chunks, 1):
            title = chunk.get("title", "Unknown")
            content = chunk.get("content", "")
            context_texts.append(f"[Source {i}] Title: {title}\nContent: {content}\n")
            
        context_str = "\n".join(context_texts)
        
        prompt = f"""당신은 AI 기술 동향 분석 도우미입니다.
사용자의 질문에는 반드시 자연스러운 한국어로 답변합니다.
답변은 제공된 브리핑 내용(요약, 중요성, 적용 메모 등)을 기반으로 작성합니다.

답변 형식:
- 요약: [질문에 대한 핵심 답변 요약]
- 최근 흐름: [최근 문서나 브리핑에서 확인된 변화]
- 관련 브리핑: [참고한 브리핑 제목 목록]
- dev-ai 적용 관점: [내 프로젝트에 어떻게 연결할 수 있는지]
- 다음에 해볼 작업: [실제 개발 태스크]
- 주의할 점: [불확실성, 보안, 비용, 적용 난이도]

"Based on the retrieved context" 같은 영어 템플릿 문구를 절대 사용하지 않습니다.

Context:
{context_str}

Question: {question}
Answer:"""
        return prompt
