# Embedding, Qdrant Retrieval, and LLM Generation

## 1. Overview

BomTS Dev AI separates the RAG pipeline into two major layers.

1. Embedding / Retrieval Layer
2. LLM Generation Layer

The embedding layer converts documents and user questions into vectors.
Qdrant uses these vectors to find relevant chunks.
The LLM generation layer receives the retrieved chunks as text context and generates the final answer.

In other words, vectors are used for retrieval, not directly passed to the final LLM.

```text
User Question
  ↓
Embedding Provider
  ↓
Query Vector
  ↓
Qdrant Semantic Search
  ↓
Relevant Chunks
  ↓
Prompt Builder
  ↓
LLM Provider
  ↓
Answer
```

## 2. Embedding Provider

The embedding provider converts text into embedding vectors.

Current supported modes:

```text
EMBEDDING_MODE=mock
EMBEDDING_MODE=openai
```

### Mock Embedding

Mock embedding is used for local development and pipeline testing.

It is deterministic and does not require an external API key.
However, it does not represent true semantic similarity.

Mock embedding is useful for validating:

* document ingestion
* chunking
* Qdrant upsert
* search API flow
* ask API flow
* logging and feedback flow

It should not be used to evaluate real RAG retrieval quality.

### OpenAI Embedding

OpenAI embedding uses `text-embedding-3-small` and produces 1536-dimensional vectors.

This mode should be used when testing real semantic retrieval quality.

When OpenAI embedding is enabled:

* document chunks are converted into real semantic vectors
* user questions are converted into real query vectors
* Qdrant can retrieve semantically relevant chunks
* RAG answer quality can improve because the LLM receives better context

## 3. Qdrant

Qdrant is used as the semantic retrieval index.

It stores:

* chunk id
* embedding vector
* payload metadata

Example payload:

```json
{
  "document_id": 1,
  "chunk_index": 3,
  "title": "RAG Pipeline",
  "content": "Chunking is the transform step of RAG...",
  "source": "manual"
}
```

Qdrant is not the source of truth.
PostgreSQL remains the source of truth for documents, chunks, logs, feedback, and source registry data.

Qdrant is used to retrieve the most relevant chunks for a user question.

## 4. LLM Provider

The LLM Provider generates the final answer.

Current generation providers include:

* OpenClaw

  * Gemma 3
  * Qwen 2.5
* Google Gemini API
* OpenAI Chat models
* Mock fallback

These providers receive prompt text, not vectors.

The prompt contains:

* the user question
* retrieved chunks from Qdrant
* instructions for answer generation

```text
Retrieved Chunks
  + User Question
  + Prompt Template
  = Final Prompt to LLM
```

## 5. Why Retrieval and Generation Are Separated

This separation is intentional.

Embedding and retrieval answer the question:

> Which chunks are relevant to this question?

LLM generation answers the question:

> How should the final answer be written using those chunks?

This allows BomTS Dev AI to combine different components:

```text
OpenAI Embedding + Qdrant + Gemma 3
OpenAI Embedding + Qdrant + Qwen 2.5
OpenAI Embedding + Qdrant + Google Gemini
Local Embedding + Qdrant + Local LLM
```

This structure is practical for real-world AI systems where multiple LLMs may be tested or switched without rebuilding the retrieval layer.

## 6. Important Limitation

If `EMBEDDING_MODE=mock`, the system can validate the RAG pipeline, but it cannot validate real semantic search quality.

Mock embedding means:

```text
The system works structurally,
but retrieval quality is not reliable.
```

For real RAG evaluation, use:

```text
EMBEDDING_MODE=openai
```

or implement a local embedding provider.

## 7. Future Improvements

Recommended future improvements:

1. Add `EmbeddingProvider` abstraction similar to `LLMProvider`.
2. Add Local Embedding Provider.
3. Show active embedding provider and model in the UI.
4. Show active LLM provider and model in the UI.
5. Add warning when mock embedding is enabled.
6. Store embedding model and dimension metadata.
7. Consider separate Qdrant collections per embedding model.

Example future provider structure:

```text
EmbeddingProvider
  ├─ MockEmbeddingProvider
  ├─ OpenAIEmbeddingProvider
  ├─ LocalOpenAICompatibleEmbeddingProvider
  ├─ OllamaEmbeddingProvider
  └─ GoogleEmbeddingProvider
```

## 8. Summary

BomTS Dev AI uses embeddings for retrieval and LLMs for generation.

Vectors are used to find relevant chunks in Qdrant.
The final LLM receives text context, not vectors.

This is a normal and practical RAG architecture.

The current system is structurally correct.
However, real RAG quality requires real embeddings.
Mock embedding is only for development and pipeline validation.
