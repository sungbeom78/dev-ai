# DB security production retry result

- Approval: `db-security-prod-retry-20261010`
- Apply result: the ownership transaction committed and all four containers were recreated.
- Observed before rollback: ports 5432, 6333, and 6334 listened only on `127.0.0.1`; `bomts_app` had no superuser, database-create, or role-create privilege; all eight public tables were owned by `bomts_app`.
- Validation failure: the old-password check looked for `POSTGRES_PASSWORD` in the rollback environment. The rollback environment stores the legacy password only inside `DATABASE_URL`, so the check could not obtain its input.
- Safety action: the rollback script ran immediately and exited successfully.
- Rollback recovery: database and Qdrant returned to the legacy runtime settings. The API needed the already-prepared Qdrant key injected into its runtime environment because the current application code requires it; health and one real search then returned HTTP 200.
- Prepared files: `docker-compose.yml` and `.env` were restored from the checksum-verified pre-apply backup. Restoring these files did not recreate services.
- Next validation: parse the legacy password from the URL with `urllib.parse.urlsplit`, keep all credential values hidden, and require the old credential to fail after the next approved apply.
