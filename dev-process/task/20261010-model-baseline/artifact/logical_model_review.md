# Logical model review — BOMTS AI production baseline

Observed read-only from the running `bomts` PostgreSQL 15.17 database on 2026-10-10 UTC. No DDL was executed.

## Scope

- 8 tables
- 80 columns
- 6 declared foreign-key relationships
- PostgreSQL is the relational source of truth.
- Qdrant `documents` is a derived vector-search collection whose point ID is `document_chunks.id`.

## Entities

| Entity | Responsibility |
|---|---|
| `documents` | Retrieval source documents |
| `document_chunks` | Searchable subdivisions of documents |
| `content_sources` | Crawl-source configuration |
| `crawled_pages` | Pages collected from a content source |
| `ask_logs` | Questions, answers, model metadata, and latency |
| `ask_source_logs` | Retrieved sources used for an ask log |
| `feedback_logs` | Rating and feedback attached to an ask log |
| `ai_reference_briefings` | Generated AI reference briefings and indexing state |

## Declared relationships

1. `documents 1 — N document_chunks` (`ON DELETE CASCADE`)
2. `ask_logs 1 — N ask_source_logs` (`ON DELETE CASCADE`)
3. `ask_logs 1 — N feedback_logs` (`ON DELETE CASCADE`)
4. `content_sources 1 — N crawled_pages` (`ON DELETE CASCADE`)
5. `documents 1 — N crawled_pages` (optional, `ON DELETE SET NULL`)
6. `documents 1 — N ai_reference_briefings` (optional, `ON DELETE SET NULL`)

## Baseline assumptions

- The baseline reproduces the current production schema without structural redesign.
- All eight public application tables are owned by `bomts_app`.
- Existing nullable columns, constraints, indexes, and delete rules remain exactly as observed.
- Identified weaknesses are recorded separately and are not silently repaired in the baseline.

## Separate problem list

- `ask_source_logs.document_id` and `chunk_id` have no declared FK.
- None of the six declared FK child-column sets has an independent supporting index.
- Free-text in `ask_logs`, `feedback_logs`, and crawled content may contain personal data; retention rules are undecided.
- Qdrant point identity depends on `document_chunks.id` and needs a defined reindex/recovery invariant.
- SQLAlchemy `create_all` remains in use; Alembic baseline is a later task.

## Logical approval boundary

Approval means that these entities, six existing relationships, and baseline assumptions correctly describe the current system. It does not approve any production DDL or the separate problem-list improvements.
