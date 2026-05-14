import os
import hashlib
from typing import List
from openai import OpenAI

EMBEDDING_MODE = os.getenv("EMBEDDING_MODE", "mock")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

class Embedder:
    def __init__(self, mode: str = EMBEDDING_MODE, api_key: str = OPENAI_API_KEY):
        self.mode = mode
        self.api_key = api_key
        self.dimension = 1536  # Default text-embedding-3-small or text-embedding-ada-002 dimension
        
        if self.mode == "openai":
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY must be set when EMBEDDING_MODE is 'openai'")
            self.client = OpenAI(api_key=self.api_key)
            
    def get_embedding(self, text: str) -> List[float]:
        if self.mode == "mock":
            return self._mock_embedding(text)
        elif self.mode == "openai":
            response = self.client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            return response.data[0].embedding
        else:
            raise ValueError(f"Unsupported embedding mode: {self.mode}")

    def _mock_embedding(self, text: str) -> List[float]:
        # Create a deterministic mock embedding based on hash
        hash_val = int(hashlib.md5(text.encode('utf-8')).hexdigest()[:8], 16)
        # Normalize to something between -1 and 1
        base_val = (hash_val / (16**8)) * 2 - 1
        vector = [base_val] * self.dimension
        # Add some variation based on text characters
        for i in range(min(len(text), self.dimension)):
            vector[i] = (ord(text[i]) / 255.0) * 2 - 1
        return vector
