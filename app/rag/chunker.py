from typing import List, Dict, Any

class CharacterChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        chunks = []
        start = 0
        text_length = len(text)
        index = 0

        if text_length == 0:
            return chunks

        while start < text_length:
            end = start + self.chunk_size
            chunk_content = text[start:end]
            
            chunks.append({
                "chunk_index": index,
                "content": chunk_content,
                "char_start": start,
                "char_end": min(end, text_length)
            })
            
            index += 1
            start += self.chunk_size - self.chunk_overlap

        return chunks
