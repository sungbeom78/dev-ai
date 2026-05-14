import os
from abc import ABC, abstractmethod
from typing import Tuple

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LOCAL_LLM_BASE_URL = os.getenv("LOCAL_LLM_BASE_URL", "")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "")

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_answer(self, prompt: str) -> Tuple[str, str]:
        """Returns a tuple of (answer_text, model_name)"""
        pass

class MockLLMProvider(BaseLLMProvider):
    def generate_answer(self, prompt: str) -> Tuple[str, str]:
        answer = "Based on the retrieved context, this project is about demonstrating RAG capabilities using a domain-neutral AI backend portfolio."
        return answer, "mock-llm"

class OpenAILLMProvider(BaseLLMProvider):
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set when LLM_PROVIDER is 'openai'")
        from openai import OpenAI
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def generate_answer(self, prompt: str) -> Tuple[str, str]:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content, self.model

class LocalLLMProvider(BaseLLMProvider):
    def __init__(self):
        # TODO: Implement local LLM connection (e.g. Ollama, vLLM)
        self.base_url = LOCAL_LLM_BASE_URL
        self.model = LOCAL_LLM_MODEL
        
    def generate_answer(self, prompt: str) -> Tuple[str, str]:
        return "Local LLM is not implemented yet. Please use mock or openai.", self.model or "local-llm"

def get_llm_provider() -> BaseLLMProvider:
    if LLM_PROVIDER == "openai":
        if OPENAI_API_KEY:
            return OpenAILLMProvider()
        else:
            return MockLLMProvider() # fallback
    elif LLM_PROVIDER == "local":
        return LocalLLMProvider()
    else:
        return MockLLMProvider()
