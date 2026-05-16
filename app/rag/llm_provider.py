import os
import requests
from abc import ABC, abstractmethod
from typing import Tuple

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# OpenClaw Settings
OPENCLAW_BASE_URL = os.getenv("OPENCLAW_BASE_URL", "")
OPENCLAW_DEFAULT_MODEL = os.getenv("OPENCLAW_DEFAULT_MODEL", "gemma3:4b")
OPENCLAW_TIMEOUT = int(os.getenv("OPENCLAW_TIMEOUT_SECONDS", "60"))

# Google Provider Settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_DEFAULT_MODEL = os.getenv("GOOGLE_DEFAULT_MODEL", "gemini-1.5-flash")

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

class OpenClawLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.base_url = OPENCLAW_BASE_URL
        self.model = OPENCLAW_DEFAULT_MODEL
        self.timeout = OPENCLAW_TIMEOUT
        
    def generate_answer(self, prompt: str) -> Tuple[str, str]:
        if not self.base_url:
            return "OpenClaw base URL is not configured.", "openclaw-error"
            
        url = f"{self.base_url}/api/chat"
        payload = {
            "message": prompt,
            "model": self.model,
            "mode": "auto",
            "workspaceRoot": "/project"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer") or data.get("message") or str(data)
            return answer, self.model
        except Exception as e:
            return f"Error calling OpenClaw API: {e}", self.model

class GoogleLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        self.model = GOOGLE_DEFAULT_MODEL
        
    def generate_answer(self, prompt: str) -> Tuple[str, str]:
        if not self.api_key:
            return "Google API key is not configured.", "google-error"
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            return answer, self.model
        except Exception as e:
            return f"Error calling Google API: {e}", self.model

def get_llm_provider() -> BaseLLMProvider:
    if LLM_PROVIDER == "openai":
        if OPENAI_API_KEY:
            return OpenAILLMProvider()
        else:
            return MockLLMProvider() # fallback
    elif LLM_PROVIDER == "openclaw":
        return OpenClawLLMProvider()
    elif LLM_PROVIDER == "google":
        return GoogleLLMProvider()
    else:
        return MockLLMProvider()
