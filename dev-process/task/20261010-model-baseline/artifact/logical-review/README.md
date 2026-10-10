# Logical-review artifacts

`03_model.dbm` is a review-only pgModeler 1.1 model generated from the current `db/model.json`.

- It contains the observed 8 tables, 80 columns, 6 declared relationships, Korean aliases, defaults, primary keys, and unique constraints.
- It does not connect to or modify PostgreSQL.
- XML structure and object counts are checked automatically.
- Actual opening and rendering must be checked in pgModeler because pgModeler is not installed on this host.
- After logical approval and glossary review, the final artifacts are regenerated under `db/out/`.
