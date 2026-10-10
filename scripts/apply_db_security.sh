#!/usr/bin/env bash
set -euo pipefail

if [[ "${APPLY_DB_SECURITY:-}" != "YES" ]]; then
  echo "Set APPLY_DB_SECURITY=YES only after the operational approval." >&2
  exit 2
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

: "${POSTGRES_DB:?}"
: "${POSTGRES_ADMIN_USER:?}"
: "${POSTGRES_ADMIN_PASSWORD:?}"
: "${POSTGRES_APP_USER:?}"
: "${POSTGRES_APP_PASSWORD:?}"
: "${QDRANT_API_KEY:?}"

if [[ "$POSTGRES_APP_USER" != "bomts_app" ]]; then
  echo "POSTGRES_APP_USER must be bomts_app" >&2
  exit 2
fi

# The local container connection uses PostgreSQL's trusted Unix socket. Passwords
# are passed as psql variables and are never written to SQL files or command output.
docker exec -i bomts_db psql \
  -v ON_ERROR_STOP=1 \
  -v app_user="$POSTGRES_APP_USER" \
  -v app_password="$POSTGRES_APP_PASSWORD" \
  -v admin_user="$POSTGRES_ADMIN_USER" \
  -v admin_password="$POSTGRES_ADMIN_PASSWORD" \
  -v database_name="$POSTGRES_DB" \
  -U postgres -d "$POSTGRES_DB" <<'SQL'
BEGIN;

SELECT format(
  'CREATE ROLE %I LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD %L',
  :'app_user', :'app_password'
)
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :'app_user')
\gexec

SELECT format(
  'ALTER ROLE %I WITH LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD %L',
  :'app_user', :'app_password'
)
\gexec

SELECT format('ALTER DATABASE %I OWNER TO %I', :'database_name', :'app_user')
\gexec
SELECT format('ALTER SCHEMA public OWNER TO %I', :'app_user')
\gexec

SELECT format(
  'ALTER %s %I.%I OWNER TO %I',
  CASE c.relkind
    WHEN 'v' THEN 'VIEW'
    WHEN 'm' THEN 'MATERIALIZED VIEW'
    ELSE 'TABLE'
  END,
  n.nspname, c.relname, :'app_user'
)
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relkind IN ('r', 'p', 'v', 'm', 'f')
ORDER BY c.relkind, c.relname
\gexec

-- A sequence linked to a serial/identity column follows its owning table and
-- PostgreSQL rejects changing that sequence owner directly. Only standalone
-- sequences need an explicit owner change.
SELECT format('ALTER SEQUENCE %I.%I OWNER TO %I', n.nspname, c.relname, :'app_user')
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relkind = 'S'
  AND NOT EXISTS (
    SELECT 1
    FROM pg_depend d
    WHERE d.classid = 'pg_class'::regclass
      AND d.objid = c.oid
      AND d.deptype IN ('a', 'i')
  )
ORDER BY c.relname
\gexec

SELECT format('ALTER FUNCTION %s OWNER TO %I', p.oid::regprocedure, :'app_user')
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
ORDER BY p.oid::regprocedure::text
\gexec

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
SELECT format('GRANT USAGE, CREATE ON SCHEMA public TO %I', :'app_user')
\gexec
SELECT format('ALTER ROLE %I WITH PASSWORD %L', :'admin_user', :'admin_password')
\gexec

COMMIT;
SQL

docker compose up -d --build --force-recreate
