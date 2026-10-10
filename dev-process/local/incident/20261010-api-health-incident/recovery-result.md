# API health incident recovery result

- Approved action: recreate `bomts_api` only
- Approval quote: `api-container-recreate-20261010 운영 적용을 승인한다.`
- Applied at: 2026-10-10 UTC
- Container recreation: 3 seconds
- Other containers: web, PostgreSQL, and Qdrant container identities and start times were unchanged

## Validation

- Immediate `/health`: HTTP 200 in 0.001 seconds
- Immediate real `/search`: HTTP 200 in 0.137 seconds, one result returned
- Five-minute observation: 11 of 11 health samples returned HTTP 200
- Final real `/search`: HTTP 200
- Observation log: 12 lines, so the result was not accepted from an empty log
- Authentication or connection error matches: 0
- API process tree: Uvicorn reload parent, resource tracker, and live application worker present

The incident was recovered without changing the pending `db-security` files and without recreating the web, PostgreSQL, or Qdrant containers.

## Prevention proposals

These proposals were not applied in this incident:

1. Remove Uvicorn `--reload` from production.
2. Add an API healthcheck and restart policy.
3. Run the six-hour collection pipeline as a separately supervised worker.
4. Add explicit timeouts around external LLM and search calls.
