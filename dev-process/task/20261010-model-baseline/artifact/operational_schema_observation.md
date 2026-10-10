# Operational schema observation

Captured read-only on 2026-10-10 UTC.

| Observation | Result |
|---|---|
| PostgreSQL version | 15.17 |
| Public base tables | 8 |
| Public columns | 80 |
| Declared foreign keys | 6 |
| Public table owner | `bomts_app` for all 8 tables |
| FK child-column independent indexes | 0 of 6 |
| `ask_source_logs.document_id` | nullable integer, no FK |
| `ask_source_logs.chunk_id` | nullable integer, no FK |
| Qdrant point ID mapping | application passes `document_chunks.id` as point ID |

Commands used were read-only catalog queries against `information_schema` and `pg_catalog`, plus source search for the Qdrant mapping. No schema or data mutation was performed.
