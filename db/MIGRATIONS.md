# PostgreSQL migration operations

`db/model.json` is the design source of truth. Alembic records the ordered,
immutable changes derived from that model. Revision `20261010_01` reproduces
the approved T4 production baseline: 8 application tables, 80 columns, and 6
foreign keys.

## New empty database

Set `DATABASE_URL` for the target database, then run:

```bash
alembic upgrade head
alembic current
```

This creates the application schema plus Alembic's `alembic_version` tracking
table. The repository check excludes only that tracking table when comparing
the result with `db/out/02_ddl_postgresql.sql`.

## Existing production database

Do not run baseline `upgrade` against an existing BOMTS schema. It would try to
create tables that already exist. Production adoption is a separate operating
action and requires explicit approval after all of these checks:

1. Take and verify a current PostgreSQL backup.
2. Run the read-only production-versus-baseline comparison; it must report zero.
3. Confirm `alembic_version` does not already exist and no migration is active.
4. Stamp the existing schema without executing DDL:

   ```bash
   alembic stamp 20261010_01
   alembic current
   ```

5. Deploy the application build that no longer calls `create_all`.

The current task prepares and tests these files only. It does not stamp,
upgrade, downgrade, or otherwise alter the running production database.

## Rollback

Before production adoption, rollback is simply deploying the previous
application image; the database has not changed. After stamping, remove a
mistaken stamp with `alembic stamp base` only when no later revision was
applied. Never run `alembic downgrade base` against production: the baseline
downgrade intentionally removes all eight application tables and exists only
for disposable database verification. If a later migration changes production
data or schema, use its reviewed downgrade when safe or restore the verified
backup.

## Creating later revisions

Change `db/model.json` and receive the required logical-model approval first.
Regenerate model outputs, then create and review an Alembic revision. Validate
`upgrade` and `downgrade` on a disposable PostgreSQL instance before requesting
production approval.
