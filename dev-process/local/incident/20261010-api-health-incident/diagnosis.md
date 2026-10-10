# API health incident diagnosis

- Task: `20261010-api-health-incident`
- Diagnosed at: 2026-10-10 UTC
- Scope: read-only diagnosis; no container or operational configuration changes made

## Observed impact

- `http://127.0.0.1:8000/health` and `/healthz` accepted TCP but returned no HTTP bytes and timed out after 10 seconds.
- `http://127.0.0.1:8771/` returned HTTP 200 in 0.001 seconds during this diagnosis. The earlier web timeout was transient and is not currently reproducible.
- The API and web containers report `running`, have no Docker healthcheck, and have restart count 0.

## Root cause and evidence

The API's Uvicorn reload parent is alive, but its application worker is dead:

- Uvicorn parent and resource tracker remain running.
- The only application child is a zombie process that died at `2026-10-09 14:21:14 UTC`.
- `app/api/health.py`, `app/db/database.py`, and `app/rag/vector_store.py` have the same modification timestamp.
- The container bind-mounts the host `app/` directory and runs `uvicorn ... --reload`, so the uncommitted `db-security` preparation code was loaded immediately without an intentional deployment.
- The modified Qdrant client code now requires `QDRANT_API_KEY`, while the running API container does not have that environment variable.
- The prepared environment uses DB role `bomts_app`, but the live database currently has only the `postgres` role for this application and all eight public tables are still owned by `postgres`. Recreating from the prepared compose configuration without the full approved security rollout would therefore introduce a second startup failure.

This explains the symptom: the reload parent still owns the listening socket, so TCP connects, but no application worker exists to return HTTP. Docker considers the container running because no healthcheck is defined.

## Ruled out

- Host pressure: about 12 GiB memory available; Docker filesystem 29% used.
- PostgreSQL outage: `pg_isready` succeeded in 0.056 seconds.
- Qdrant outage: `/healthz` returned 200 in 0.001 seconds.
- CPU saturation: API used about 4% CPU during sampling.
- Six-hour pipeline or external LLM/search wait: no API worker exists, no scheduled pipeline process is running, and no established outbound API connection was found. The background loop cannot currently run.
- Web service outage: Nginx returned 200 and logged the diagnostic request.

## Proposed recovery requiring approval

Recreate only `bomts_api`, using the existing live PostgreSQL connection settings and the already prepared Qdrant API key, without editing any `db-security` files and without recreating DB, Qdrant, or web containers. This lets the current mounted code start while preserving the pending DB-security rollout boundary.

- Expected API interruption: 10–30 seconds. The API is already unavailable; web, DB, and Qdrant should remain online.
- Validation: wait for API startup, require `/health` HTTP 200, run one real search request and require HTTP 200, then inspect API/web logs for five minutes.
- Rollback: recreate only the API again from the same image with the captured legacy PostgreSQL environment. No persistent data or database schema change is part of this action.

Longer-term prevention is proposal-only for this incident: remove `--reload` from production, add an API healthcheck and restart policy, and move the six-hour collector into a separately supervised worker with explicit external-call timeouts.
