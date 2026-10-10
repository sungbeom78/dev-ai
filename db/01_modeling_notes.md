# BOMTS AI existing data model notes

## Scope and method

This is a read-only reverse engineering record of the production PostgreSQL 15 `public` schema on 2026-10-09. It captures the existing eight SQLAlchemy-managed tables, columns, constraints, indexes, and relationships. No DDL was executed against production while preparing this model.

## Managed entities

- `documents`: source documents used by retrieval.
- `document_chunks`: searchable subdivisions of a document.
- `content_sources`: configured crawl sources.
- `crawled_pages`: pages collected from a source and optionally linked to a document.
- `ask_logs`: questions, generated answers, model metadata, and latency.
- `ask_source_logs`: retrieved sources associated with an ask log.
- `feedback_logs`: ratings and optional feedback associated with an ask log.
- `ai_reference_briefings`: generated AI reference briefings and indexing state.

Qdrant holds the vector representation for document chunks in the `documents` collection. PostgreSQL remains the relational source of truth; Qdrant is a derived search store and is backed up separately.

## Existing business rules

- A document can own many chunks; deleting the document cascades to those chunks.
- An ask log can own many source logs and feedback rows; deleting the ask log cascades to both.
- A content source can own many crawled pages; deleting the source cascades to its pages.
- A crawled page can optionally point to a document; deleting that document sets the link to null.
- Source URLs on crawled pages are unique.

## Security target prepared by this task

- `bomts_app` owns the database, `public` schema, application tables, sequences, views, and public functions.
- `bomts_app` has `LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE`.
- PostgreSQL and Qdrant bind to loopback only.
- PostgreSQL passwords and the Qdrant API key live in the ignored `.env` file.
- These ownership and service changes remain unapplied until the service owner approves the restart.

## Data-quality and privacy observations

The schema has primary and foreign keys for the main relationships, but several status/category fields remain unconstrained text. Questions, answers, feedback comments, crawled content, author names, and URLs can contain personal information even though there is no dedicated person entity. Retention, deletion, and PI separation require a separate product-policy decision and are not changed by this security task.

## Change scenarios

- Moving from `create_all` to versioned migrations should preserve `db/model.json` as the design source of truth.
- Adding another vector collection should add an `external_stores` entry and a backup/restore test.
- Adding user accounts or uploaded private documents requires a dedicated PI model and access-control design before implementation.
