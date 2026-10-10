# Preview image import failure

- Command context: isolated image `bomts-api:t5-alembic-preview`, default bridge network, `QDRANT_URL=http://127.0.0.1:6333`.
- First error: `httpcore.ConnectError: [Errno 111] Connection refused` at `app/rag/vector_store.py:14` while `QdrantStore.__init__()` called `get_collections()`.
- Product data change: none. The connection failed before collection or database mutation, and the `--rm` container exited.
- Procedure defect: the original multi-command shell did not use `set -e`; later successful commands masked the failed import with overall exit code 0. This attempt is not accepted as a passed check.
- Classification basis: the preview command supplied a container-local loopback address even though Qdrant is published only on the host loopback. The import-time Qdrant connection behavior predates T5.
