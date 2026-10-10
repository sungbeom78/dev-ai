#!/usr/bin/env python3
"""Validate Alembic baseline on disposable PostgreSQL and compare production read-only."""

from __future__ import annotations

import difflib
import os
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROD = os.environ.get("BOMTS_PROD_DB_CONTAINER", "bomts_db")
name = f"bomts-alembic-check-{uuid.uuid4().hex[:12]}"


def run(args: list[str], *, env: dict[str, str] | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, env=env, text=True, capture_output=True, check=check)


def normalized_dump(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line or line.startswith("--") or line.startswith("\\restrict ") or line.startswith("\\unrestrict "):
            continue
        lines.append(line)
    return "\n".join(lines).strip() + "\n"


try:
    run([
        "docker", "run", "-d", "--rm", "--name", name,
        "--tmpfs", "/var/lib/postgresql/data:rw,nosuid,size=512m",
        "-p", "127.0.0.1::5432",
        "-e", "POSTGRES_HOST_AUTH_METHOD=trust", "-e", "POSTGRES_DB=bomts",
        "postgres:15-alpine",
    ])
    for _ in range(120):
        logs = run(["docker", "logs", name], check=False)
        ready = run(["docker", "exec", name, "pg_isready", "-U", "postgres", "-d", "bomts"], check=False)
        if "PostgreSQL init process complete; ready for start up." in (logs.stdout + logs.stderr) and ready.returncode == 0:
            break
        time.sleep(0.5)
    else:
        raise RuntimeError("final temporary PostgreSQL did not become ready")

    mapping = run(["docker", "port", name, "5432/tcp"]).stdout.strip()
    port = mapping.rsplit(":", 1)[1]
    env = os.environ.copy()
    env["DATABASE_URL"] = f"postgresql+psycopg2://postgres@127.0.0.1:{port}/bomts"
    upgrade = run([str(ROOT / ".venv/bin/alembic"), "-c", "alembic.ini", "upgrade", "head"], env=env, check=False)
    if upgrade.returncode:
        print(upgrade.stdout)
        print(upgrade.stderr, file=sys.stderr)
        raise SystemExit(upgrade.returncode)
    current = run([str(ROOT / ".venv/bin/alembic"), "-c", "alembic.ini", "current"], env=env)
    if "20261010_01" not in (current.stdout + current.stderr):
        print(current.stdout + current.stderr)
        raise SystemExit("temporary database is not at baseline head")

    dump_args = [
        "pg_dump", "-U", "postgres", "-d", "bomts", "--schema-only",
        "--no-owner", "--no-privileges", "--exclude-table=public.alembic_version",
    ]
    production = run(["docker", "exec", PROD, *dump_args]).stdout
    temporary = run(["docker", "exec", name, *dump_args]).stdout
    diff = list(difflib.unified_diff(
        normalized_dump(production).splitlines(),
        normalized_dump(temporary).splitlines(),
        fromfile="production", tofile="alembic-baseline", lineterm="",
    ))
    count_sql = "select count(*) from information_schema.tables where table_schema='public' and table_type='BASE TABLE' and table_name <> 'alembic_version'"
    table_count = run(["docker", "exec", name, "psql", "-U", "postgres", "-d", "bomts", "-Atc", count_sql]).stdout.strip()
    column_count = run(["docker", "exec", name, "psql", "-U", "postgres", "-d", "bomts", "-Atc", "select count(*) from information_schema.columns where table_schema='public' and table_name <> 'alembic_version'"]).stdout.strip()
    fk_count = run(["docker", "exec", name, "psql", "-U", "postgres", "-d", "bomts", "-Atc", "select count(*) from pg_constraint c join pg_namespace n on n.oid=c.connamespace where n.nspname='public' and c.contype='f'"]).stdout.strip()
    print(f"alembic_upgrade_head=20261010_01 tables={table_count} columns={column_count} foreign_keys={fk_count}")
    print(f"production_pg_dump_vs_alembic_pg_dump_diff_lines={len(diff)}")
    if diff:
        print("\n".join(diff[:120]))
        raise SystemExit(1)
    if (table_count, column_count, fk_count) != ("8", "80", "6"):
        raise SystemExit(1)

    downgrade = run([str(ROOT / ".venv/bin/alembic"), "-c", "alembic.ini", "downgrade", "base"], env=env, check=False)
    if downgrade.returncode:
        print(downgrade.stdout)
        print(downgrade.stderr, file=sys.stderr)
        raise SystemExit(downgrade.returncode)
    after = run(["docker", "exec", name, "psql", "-U", "postgres", "-d", "bomts", "-Atc", count_sql]).stdout.strip()
    print(f"alembic_downgrade_base_application_tables={after}")
    if after != "0":
        raise SystemExit(1)
finally:
    run(["docker", "rm", "-f", name], check=False)
