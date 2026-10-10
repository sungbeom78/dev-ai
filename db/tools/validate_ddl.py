#!/usr/bin/env python3
"""Apply generated DDL to temporary PostgreSQL and compare with production.

Production is read-only: the only production operation is pg_dump --schema-only.
"""

from __future__ import annotations

import difflib
import os
import re
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORTER = ROOT / "db/tools/export_all.py"
MODEL = ROOT / "db/model.json"
PROD = os.environ.get("BOMTS_PROD_DB_CONTAINER", "bomts_db")
name = f"bomts-model-check-{uuid.uuid4().hex[:12]}"


def run(args: list[str], *, input_text: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, input=input_text, text=True, capture_output=True, check=check)


def normalized_dump(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = raw.rstrip()
        # pg_dump 17 emits a random psql safety token on every run. Comments
        # also vary with the initdb ownership of the built-in public schema.
        # Neither is executable schema SQL, so compare statements only.
        if not line or line.startswith("--") or line.startswith("\\restrict ") or line.startswith("\\unrestrict "):
            continue
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


with tempfile.TemporaryDirectory(prefix="bomts-ddl-check-") as tmp:
    out = Path(tmp)
    run([sys.executable, str(EXPORTER), str(MODEL), str(out)])
    ddl = out / "02_ddl_postgresql.sql"
    try:
        run([
            "docker", "run", "-d", "--rm", "--name", name,
            "--tmpfs", "/var/lib/postgresql/data:rw,nosuid,size=512m",
            "-e", "POSTGRES_HOST_AUTH_METHOD=trust", "-e", "POSTGRES_DB=bomts",
            "postgres:15-alpine",
        ])
        # The official entrypoint exposes a temporary initialization server
        # before stopping it and exec'ing the final server.  Require both the
        # entrypoint completion marker and readiness of the requested DB.
        for _ in range(120):
            logs = run(["docker", "logs", name], check=False)
            ready = run(["docker", "exec", name, "pg_isready", "-U", "postgres", "-d", "bomts"], check=False)
            if "PostgreSQL init process complete; ready for start up." in (logs.stdout + logs.stderr) and ready.returncode == 0:
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("final temporary PostgreSQL did not become ready")
        run(["docker", "cp", str(ddl), f"{name}:/tmp/model.sql"])
        applied = run(["docker", "exec", name, "psql", "-v", "ON_ERROR_STOP=1", "-U", "postgres", "-d", "bomts", "-f", "/tmp/model.sql"], check=False)
        if applied.returncode:
            print(applied.stdout)
            print(applied.stderr, file=sys.stderr)
            raise SystemExit(applied.returncode)

        smoke = """
BEGIN;
INSERT INTO public.documents (title, content) VALUES ('baseline-smoke', 'baseline-smoke');
INSERT INTO public.document_chunks (document_id, chunk_index, content, char_start, char_end)
  SELECT id, 0, 'baseline-smoke', 0, 14 FROM public.documents WHERE title='baseline-smoke';
DO $$
BEGIN
  BEGIN
    INSERT INTO public.document_chunks (document_id, chunk_index, content, char_start, char_end)
    VALUES (-1, 0, 'must-fail', 0, 9);
    RAISE EXCEPTION 'FK did not reject invalid parent';
  EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'OK: invalid document_id rejected';
  END;
END $$;
DELETE FROM public.documents WHERE title='baseline-smoke';
DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM public.document_chunks WHERE content='baseline-smoke') THEN
    RAISE EXCEPTION 'CASCADE did not remove child';
  END IF;
  RAISE NOTICE 'OK: document delete cascaded';
END $$;
ROLLBACK;
"""
        smoke_result = run(["docker", "exec", "-i", name, "psql", "-v", "ON_ERROR_STOP=1", "-U", "postgres", "-d", "bomts"], input_text=smoke, check=False)
        if smoke_result.returncode:
            print(smoke_result.stdout)
            print(smoke_result.stderr, file=sys.stderr)
            raise SystemExit(smoke_result.returncode)

        dump_args = ["pg_dump", "-U", "postgres", "-d", "bomts", "--schema-only", "--no-owner", "--no-privileges"]
        production = run(["docker", "exec", PROD, *dump_args]).stdout
        temporary = run(["docker", "exec", name, *dump_args]).stdout
        prod_norm, temp_norm = normalized_dump(production), normalized_dump(temporary)
        diff = list(difflib.unified_diff(prod_norm.splitlines(), temp_norm.splitlines(), fromfile="production", tofile="generated", lineterm=""))
        table_count = run(["docker", "exec", name, "psql", "-U", "postgres", "-d", "bomts", "-Atc", "select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE'"]).stdout.strip()
        column_count = run(["docker", "exec", name, "psql", "-U", "postgres", "-d", "bomts", "-Atc", "select count(*) from information_schema.columns where table_schema='public'"]).stdout.strip()
        fk_count = run(["docker", "exec", name, "psql", "-U", "postgres", "-d", "bomts", "-Atc", "select count(*) from pg_constraint c join pg_namespace n on n.oid=c.connamespace where n.nspname='public' and c.contype='f'"]).stdout.strip()
        print(f"temporary_postgres=15 tables={table_count} columns={column_count} foreign_keys={fk_count}")
        print("smoke=invalid_fk_rejected,cascade_verified")
        print(f"production_pg_dump_vs_generated_pg_dump_diff_lines={len(diff)}")
        if diff:
            print("\n".join(diff[:120]))
            raise SystemExit(1)
        if (table_count, column_count, fk_count) != ("8", "80", "6"):
            raise SystemExit(1)
    finally:
        run(["docker", "rm", "-f", name], check=False)
