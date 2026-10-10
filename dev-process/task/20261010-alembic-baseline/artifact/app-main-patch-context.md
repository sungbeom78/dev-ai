# app/main.py patch context failure

- First error: `apply_patch verification failed: Failed to find expected lines`.
- Cause evidence: the prepared patch expected the database imports before the API import and expected `create_all` at module scope. The actual source has the API import first and calls `create_all` inside `lifespan()`.
- Safety result: apply_patch is atomic for this hunk; `app/main.py` was not modified. Its SHA-256 still equals the pre-apply backup.
