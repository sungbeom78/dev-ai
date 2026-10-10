# DB security production apply failure

- Applied at: 2026-10-10 UTC
- Approval: `db-security-prod-apply-20261009 운영 적용을 승인한다.`
- Apply result: failed before container recreation
- Rollback result: `rollback_db_security.sh` exited 0
- Retry: not attempted

## Failure

The ownership loop attempted to change the owner of `ai_reference_briefings_id_seq` directly. PostgreSQL rejected it because the sequence is linked to its owning table and must follow the table owner. `ON_ERROR_STOP` terminated the apply script at that point.

The script had already created `bomts_app`, changed the database and schema owners, and started object ownership changes. It had not yet reached the PostgreSQL administrator password rotation or Docker Compose recreation.

## Rollback verification

- The previous PostgreSQL password succeeds over the Compose network.
- The prepared replacement PostgreSQL password fails, confirming that rotation did not occur.
- All eight public tables are again owned by `postgres`.
- `bomts_app` remains as an unused `NOSUPERUSER NOCREATEDB NOCREATEROLE` role; the rollback script does not remove it.
- PostgreSQL and Qdrant ports are back on their former `0.0.0.0` and `[::]` bindings.
- Qdrant without an API key returns HTTP 200, so Qdrant authentication was not applied.
- The API was restored separately and currently returns health 200 and real search 200.
- The prepared `docker-compose.yml` and `.env` working copies were restored from the pre-apply backup, but they have not been applied to DB or Qdrant.

## Required script correction before another attempt

1. Change table ownership before sequence ownership.
2. Exclude sequences linked to a table from explicit `ALTER SEQUENCE ... OWNER`; they follow their owning table.
3. Wrap the PostgreSQL role and ownership operations in a transaction so an ownership error does not leave partial DB changes.
4. Extend rollback to remove `bomts_app` when the failed apply created it and no pre-existing role was recorded.
5. Pin the API dependency versions or explicitly use the installed `psycopg2` dialect. The rollback rebuild installed a newer SQLAlchemy whose default driver required missing `psycopg`.

No second production apply should run until these corrections are reviewed and the pre-apply checks are repeated.
