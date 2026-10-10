#!/usr/bin/env bash
set -euo pipefail

revision_table=$(docker exec bomts_db psql -U postgres -d bomts -tAc \
  "select coalesce(to_regclass('public.alembic_version')::text, 'absent')")
table_count=$(docker exec bomts_db psql -U postgres -d bomts -tAc \
  "select count(*) from pg_tables where schemaname='public'")

[[ "$revision_table" == "absent" ]]
[[ "$table_count" == "8" ]]
printf 'production_alembic_version=%s public_tables=%s ddl_or_stamp_executed=no\n' \
  "$revision_table" "$table_count"
