#!/usr/bin/env python3
"""Regenerate all model outputs and prove checked-in artifacts are current."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
MODEL = ROOT / "db/model.json"
OUT = ROOT / "db/out"
EXPORTER = ROOT / "db/tools/export_all.py"
model = json.loads(MODEL.read_text(encoding="utf-8"))

with tempfile.TemporaryDirectory(prefix="bomts-model-export-") as tmp:
    subprocess.run([sys.executable, str(EXPORTER), str(MODEL), tmp], check=True)
    generated = Path(tmp)
    errors = []
    for name in ("02_ddl_postgresql.sql", "03_model.dbm"):
        target = OUT / name
        if not target.exists() or target.read_bytes() != (generated / name).read_bytes():
            errors.append(f"stale or missing: db/out/{name}")
    root = ET.parse(generated / "03_model.dbm").getroot()
    dbm_counts = (sum(1 for _ in root.iter("table")), sum(1 for _ in root.iter("column")), sum(1 for _ in root.iter("relationship")))
    workbook = load_workbook(generated / "04_table_spec.xlsx", read_only=True)
    required_sheets = {"개요", "테이블목록", "컬럼명세", "관계(FK)", "용어사전", "개인정보", "코드정의", "검토메모"}
    if not required_sheets.issubset(workbook.sheetnames):
        errors.append("xlsx required sheets missing")
    xlsx_counts = (workbook["테이블목록"].max_row - 1, workbook["컬럼명세"].max_row - 1, workbook["관계(FK)"].max_row - 1)
    expected = (len(model["tables"]), sum(len(t["columns"]) for t in model["tables"]), len(model["relationships"]))
    if dbm_counts != expected:
        errors.append(f"dbm counts {dbm_counts} != {expected}")
    if xlsx_counts != expected:
        errors.append(f"xlsx counts {xlsx_counts} != {expected}")
    committed_xlsx = OUT / "04_table_spec.xlsx"
    if not committed_xlsx.exists():
        errors.append("missing: db/out/04_table_spec.xlsx")
    else:
        checked = load_workbook(committed_xlsx, read_only=True)
        checked_counts = (checked["테이블목록"].max_row - 1, checked["컬럼명세"].max_row - 1, checked["관계(FK)"].max_row - 1)
        if checked_counts != expected:
            errors.append(f"checked-in xlsx counts {checked_counts} != {expected}")
    for error in errors:
        print("ERROR", error)
    print(f"model_export expected={expected} dbm={dbm_counts} xlsx={xlsx_counts} errors={len(errors)}")
    raise SystemExit(1 if errors else 0)
