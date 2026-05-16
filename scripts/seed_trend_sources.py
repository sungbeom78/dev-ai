import requests

sources = [
    {"name": "Hugging Face Blog", "base_url": "https://huggingface.co/blog", "category": "open_model"},
    {"name": "LangChain Blog", "base_url": "https://blog.langchain.dev", "category": "agent"},
    {"name": "Qwen Blog", "base_url": "https://qwenlm.github.io/blog", "category": "open_model"},
    {"name": "Google AI Blog / Gemma", "base_url": "https://blog.research.google", "category": "open_model"},
    {"name": "Model Context Protocol Docs", "base_url": "https://modelcontextprotocol.io", "category": "mcp"},
    {"name": "Ollama Blog", "base_url": "https://ollama.com/blog", "category": "local_llm"},
    {"name": "LlamaIndex Blog", "base_url": "https://www.llamaindex.ai/blog", "category": "rag"}
]

for s in sources:
    res = requests.post("http://localhost:8771/api/sources", json=s)
    if res.ok:
        print(f"Created: {s['name']}")
    else:
        print(f"Failed to create: {s['name']} - {res.text}")
