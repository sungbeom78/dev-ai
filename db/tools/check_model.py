#!/usr/bin/env python3
"""Validate the framework model contract plus existing-database observations."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "db/model.json"
FRAMEWORK_CHECK = ROOT / "dev-process-framework/data-modeling-expert/skill/scripts/check_dictionary.py"

model = json.loads(MODEL.read_text(encoding="utf-8"))
errors: list[str] = []
if model.get("baseline_mode") != "existing_database":
    errors.append("baseline_mode must be existing_database")
if model.get("schema") != "public":
    errors.append("observed schema must be public")
tables = model.get("tables", [])
relationships = model.get("relationships", [])
columns = [column for table in tables for column in table.get("columns", [])]
if (len(tables), len(columns), len(relationships)) != (8, 80, 6):
    errors.append(f"expected 8 tables/80 columns/6 relationships, got {len(tables)}/{len(columns)}/{len(relationships)}")
for table in tables:
    if table.get("owner") != "bomts_app":
        errors.append(f"{table['name']}: observed owner must be bomts_app")
    if not table.get("indexes"):
        errors.append(f"{table['name']}: observed indexes missing")
    for column in table.get("columns", []):
        if column.get("domain") != column.get("type"):
            errors.append(f"{table['name']}.{column['name']}: domain/type mismatch")
for relationship in relationships:
    if relationship.get("from_col") != relationship.get("from_columns", [None])[0]:
        errors.append(f"{relationship['name']}: from column representation mismatch")
    if relationship.get("to_col") != relationship.get("to_columns", [None])[0]:
        errors.append(f"{relationship['name']}: to column representation mismatch")

result = subprocess.run([sys.executable, str(FRAMEWORK_CHECK), str(MODEL)], text=True)
for error in errors:
    print("ERROR", error)
print(f"baseline_contract errors={len(errors)}")
raise SystemExit(1 if result.returncode or errors else 0)
