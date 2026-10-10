#!/usr/bin/env bash
set -euo pipefail

if [[ "${ROLLBACK_DB_SECURITY:-}" != "YES" ]]; then
  echo "Set ROLLBACK_DB_SECURITY=YES only after rollback approval." >&2
  exit 2
fi

backup_dir=${1:-/project/backup/bomts-ai/2026-10-09/pre-db-security/rollback}
previous_compose="$backup_dir/docker-compose.yml.before"
previous_env="$backup_dir/.env.before"
[[ -f "$previous_compose" && -f "$previous_env" ]] || {
  echo "Rollback files are missing under $backup_dir" >&2
  exit 2
}

previous_admin_password=$(python3 - "$previous_env" <<'PY'
from pathlib import Path
from urllib.parse import urlparse
import sys
url=''
for line in Path(sys.argv[1]).read_text().splitlines():
    if line.startswith('DATABASE_URL='):
        url=line.split('=',1)[1]
        break
password=urlparse(url).password
if not password:
    raise SystemExit('DATABASE_URL password not found in rollback environment')
print(password)
PY
)

docker exec -i bomts_db psql \
  -v ON_ERROR_STOP=1 \
  -v previous_admin_password="$previous_admin_password" \
  -U postgres -d bomts <<'SQL'
BEGIN;

ALTER DATABASE bomts OWNER TO postgres;
ALTER SCHEMA public OWNER TO postgres;
SELECT format(
  'ALTER %s %I.%I OWNER TO postgres',
  CASE c.relkind
    WHEN 'v' THEN 'VIEW'
    WHEN 'm' THEN 'MATERIALIZED VIEW'
    ELSE 'TABLE'
  END,
  n.nspname, c.relname
)
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public'
  AND c.relkind IN ('r', 'p', 'v', 'm', 'f')
ORDER BY c.relkind, c.relname
\gexec
SELECT format('ALTER SEQUENCE %I.%I OWNER TO postgres', n.nspname, c.relname)
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
SELECT format('ALTER FUNCTION %s OWNER TO postgres', p.oid::regprocedure)
FROM pg_proc p
JOIN pg_namespace n ON n.oid = p.pronamespace
WHERE n.nspname = 'public'
ORDER BY p.oid::regprocedure::text
\gexec
SELECT 'REASSIGN OWNED BY bomts_app TO postgres'
WHERE EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bomts_app')
\gexec
SELECT 'DROP OWNED BY bomts_app'
WHERE EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bomts_app')
\gexec
SELECT 'DROP ROLE bomts_app'
WHERE EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'bomts_app')
\gexec
ALTER ROLE postgres WITH PASSWORD :'previous_admin_password';

COMMIT;
SQL

install -m 644 "$previous_compose" docker-compose.yml
install -m 600 "$previous_env" .env
docker compose up -d --build --force-recreate
