# DB security task — dev-process-framework compliance audit

Task: `20261009-db-security`  
Audit date: 2026-10-10 UTC  
Framework revision: `c93b8e7`

## Executive finding

The final production application followed the framework gates: the exact user approval and scope fingerprint were recorded, protected zones stayed unchanged, failures used bounded recovery incidents, runtime checks were executed and sealed, and no verification hook was bypassed. The required independent LAN test was reported from `192.168.50.64`; both PostgreSQL 5432 and Qdrant 6333 returned `TcpTestSucceeded=False`.

One earlier artifact does not fully comply with the data-model policy: `db/model.json` and the first modeling notes were prepared inside the security task instead of a dedicated `work_type: data_model` task with logical-model and glossary gates. The approved remediation is the next `model-baseline` task after T1 and T2 finish.

## Rule-by-rule audit

| Framework requirement | Evidence | Finding |
|---|---|---|
| Start with task state and explicit acceptance criteria | `dev-process/task/20261009-db-security/task_state.json` | Followed |
| Run prior-art checks before implementation | Task artifact and task-state history | Followed |
| Do not modify framework or glossary protected zones | `protect-check`; both submodule statuses empty | Followed |
| Record non-delegated operations as approvals | Approval requests `db-security-prod-apply-20261009`, `db-security-prod-retry-20261010`, and `db-security-prod-final-retry-20261010` include exact user quotes and scope fingerprints | Followed |
| Use bounded recovery rounds after failure | `db-security-linked-sequence-owner` and `db-security-old-password-check-source` incidents | Followed |
| Do not repeat the same failed hypothesis without evidence | Linked-sequence handling changed after PostgreSQL error evidence; credential validation changed after environment-key evidence | Followed |
| Roll back a failed production application | Both unsuccessful applications invoked `rollback_db_security.sh`; runtime recovery was checked | Followed, with project-level rollback weakness noted below |
| Execute and seal required checks | `verify` receipts plus `db_security_sequence_recovery` and `db_security_runtime` receipts | Followed |
| Do not bypass hooks | No `--no-verify` use | Followed |
| Finish only after acceptance criteria are met | Independent-LAN evidence was received before acceptance criterion 6 was marked met and before `finish` | Followed |
| Use a formal `data_model` task for reverse engineering and model governance | Initial `db/model.json` was produced in this security task | Not fully followed; remediation scheduled as `model-baseline` |
| Update a user manual only for new project, new feature, or usage change | Change kind is `fix`; DBeaver SSH-tunnel operations documentation was still added because the secure connection procedure matters | Followed |

## Recovery history and lessons

1. The first apply failed because PostgreSQL does not allow a linked sequence owner to be changed independently of its table. The operation rolled back. The SQL was made transactional and linked sequences were excluded from the generic sequence loop.
2. The second apply completed, but the old-password verifier searched for a `POSTGRES_PASSWORD` key that the rollback environment did not have. It rolled back safely. The verifier now extracts the legacy password from `DATABASE_URL`.
3. A password test from inside the database container was invalid because local PostgreSQL authentication can bypass password verification. The final verifier tests the real `api → db` TCP path.
4. The project rollback restored the legacy Compose environment but the current application code required `QDRANT_API_KEY`, so the API worker needed a separate recovery injection. This is a project rollback-script defect; the framework correctly required recovery evidence but does not currently validate rollback completeness automatically.
5. The final approved apply passed immediate checks and a 600-second observation: 21 health responses were 200, final search was 200, API logs were nonempty, and authentication/connection errors were zero.

## Completion boundary

- Local listener and same-host LAN-address probes prove that ports 5432 and 6333 are not bound to the LAN address.
- The independent Windows/LAN probe from `192.168.50.64` reached the host by ping while both TCP probes returned `False`. The screenshot and transcription are stored with the final retry evidence.
- No model DDL was executed against the production database.

## Framework improvement candidates

The concrete upstream requests are recorded in `dev-process/local/upstream-requests.md`. They cover approval status reconciliation, recovery next-action guidance, record-commit behavior with ignored reports, rollback-completeness checks, and an explicit reverse-engineering workflow that prevents a model artifact from being created under a non-`data_model` task.
