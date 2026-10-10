#!/usr/bin/env python3
"""Static invariants for the immutable Alembic production baseline."""

from __future__ import annotations

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION = ROOT / "migrations/versions/20261010_01_production_baseline.py"
CANONICAL = ROOT / "db/out/02_ddl_postgresql.sql"


def statements(sql: str) -> list[str]:
    kept = []
    for line in sql.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("--") or stripped in {"BEGIN;", "COMMIT;"}:
            continue
        kept.append(stripped)
    return [re.sub(r"\s+", " ", item.strip()) for item in " ".join(kept).split(";") if item.strip()]


tree = ast.parse(REVISION.read_text(encoding="utf-8"), filename=str(REVISION))
values: dict[str, object] = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
        try:
            values[node.targets[0].id] = ast.literal_eval(node.value)
        except (TypeError, ValueError):
            pass
if not isinstance(values.get("BASELINE_SQL"), str) or not isinstance(values.get("revision"), str):
    raise SystemExit("baseline revision constants are missing")

expected = statements(CANONICAL.read_text(encoding="utf-8"))
actual = statements(values["BASELINE_SQL"])
if expected != actual:
    for index, (left, right) in enumerate(zip(expected, actual), 1):
        if left != right:
            print(f"first_statement_difference={index}\ncanonical={left}\nmigration={right}")
            break
    if len(expected) != len(actual):
        print(f"statement_count canonical={len(expected)} migration={len(actual)}")
    raise SystemExit(1)

main_source = (ROOT / "app/main.py").read_text(encoding="utf-8")
if "Base.metadata.create_all" in main_source:
    raise SystemExit("app/main.py still calls Base.metadata.create_all")

print(f"PASS: alembic baseline revision={values['revision']} statements={len(actual)} create_all=absent")
