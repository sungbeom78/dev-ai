#!/usr/bin/env python3
"""Export the current-database baseline from db/model.json.

This project adapter preserves the observed PostgreSQL schema.  In particular it
does not add the framework's prospective-design meta tables, FK indexes, audit
columns, comments, or renamed constraints.  Those changes belong in later
migrations, after the baseline has been accepted.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


def load_model(path: Path) -> dict:
    model = json.loads(path.read_text(encoding="utf-8"))
    if model.get("baseline_mode") != "existing_database":
        raise ValueError("baseline_mode must be existing_database")
    return model


def sequence_name(default: object) -> str | None:
    if not isinstance(default, str):
        return None
    match = re.fullmatch(r"nextval\('(?:public\.)?([^']+)'::regclass\)", default)
    return match.group(1) if match else None


def export_ddl(model: dict, path: Path) -> None:
    schema = model["schema"]
    lines = [
        f"-- {model['project']} existing PostgreSQL baseline",
        "-- Generated from db/model.json. Apply only to an empty temporary database.",
        "BEGIN;",
        "",
    ]
    sequences: list[tuple[str, str, str, str]] = []
    for table in model["tables"]:
        columns = []
        for column in table["columns"]:
            value = f"    {column['name']} {column['type']}"
            seq = sequence_name(column.get("default"))
            if not column["nullable"]:
                value += " NOT NULL"
            if column.get("default") is not None and not seq:
                value += f" DEFAULT {column['default']}"
            columns.append(value)
            if seq:
                sequences.append((seq, table["name"], column["name"], column["type"]))
        lines += [
            f"CREATE TABLE {schema}.{table['name']} (",
            ",\n".join(columns),
            ");",
            "",
        ]

    for seq, table_name, column_name, data_type in sequences:
        seq_type = "integer" if data_type == "integer" else "bigint"
        lines += [
            f"CREATE SEQUENCE {schema}.{seq}",
            f"    AS {seq_type}",
            "    START WITH 1",
            "    INCREMENT BY 1",
            "    NO MINVALUE",
            "    NO MAXVALUE",
            "    CACHE 1;",
            "",
            f"ALTER SEQUENCE {schema}.{seq} OWNED BY {schema}.{table_name}.{column_name};",
            "",
        ]
    for seq, table_name, column_name, _ in sequences:
        lines += [
            f"ALTER TABLE ONLY {schema}.{table_name} ALTER COLUMN {column_name} "
            f"SET DEFAULT nextval('{schema}.{seq}'::regclass);",
            "",
        ]

    constraint_names: set[str] = set()
    for table in model["tables"]:
        primary = [c["name"] for c in table["columns"] if c.get("pk")]
        pk_name = table.get("primary_key_constraint", f"{table['name']}_pkey")
        constraint_names.add(pk_name)
        lines += [
            f"ALTER TABLE ONLY {schema}.{table['name']}",
            f"    ADD CONSTRAINT {pk_name} PRIMARY KEY ({', '.join(primary)});",
            "",
        ]
        observed = table.get("observed_unique_constraints", [])
        for unique in observed:
            constraint_names.add(unique["name"])
            lines += [
                f"ALTER TABLE ONLY {schema}.{table['name']}",
                f"    ADD CONSTRAINT {unique['name']} UNIQUE ({', '.join(unique['columns'])});",
                "",
            ]
        for columns in table.get("uniques", []):
            name = f"{table['name']}_{'_'.join(columns)}_key"
            if name not in constraint_names:
                constraint_names.add(name)
                lines += [
                    f"ALTER TABLE ONLY {schema}.{table['name']}",
                    f"    ADD CONSTRAINT {name} UNIQUE ({', '.join(columns)});",
                    "",
                ]

    for table in model["tables"]:
        for index in table.get("indexes", []):
            if index["name"] not in constraint_names:
                lines += [index["definition"].rstrip(";") + ";", ""]

    for rel in model["relationships"]:
        lines += [
            f"ALTER TABLE ONLY {schema}.{rel['from']}",
            f"    ADD CONSTRAINT {rel['name']} FOREIGN KEY ({rel['from_col']}) "
            f"REFERENCES {schema}.{rel['to']}({rel['to_col']}) ON DELETE {rel['on_delete']};",
            "",
        ]
    lines += ["COMMIT;", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def xml_type(pg_type: str) -> str:
    match = re.fullmatch(r"character varying\((\d+)\)", pg_type)
    if match:
        return f'<type name="varchar" length="{match.group(1)}"/>'
    return f'<type name={quoteattr(pg_type)} length="0"/>'


def export_dbm(model: dict, path: Path, pgmodeler_ver: str) -> None:
    schema = model["schema"]
    owner = model["assumptions"][1].split("`")[1] if len(model.get("assumptions", [])) > 1 and "`" in model["assumptions"][1] else "bomts_app"
    tables = {table["name"]: table for table in model["tables"]}
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<!-- Generated from db/model.json; do not edit by hand. -->')
    lines.append(
        f'<dbmodel pgmodeler-ver="{pgmodeler_ver}" use-changelog="false" max-obj-count="{len(tables)+8}" '
        f'last-position="0,0" last-zoom="1" scene-rect="0,0,2600,1600" default-schema="{schema}" '
        f'default-owner="{owner}" layers="Default layer" active-layers="0" layer-name-colors="#000000" '
        'layer-rect-colors="#b4b4b4" show-layer-names="false" show-layer-rects="false">'
    )
    lines += [f'<database name="bomts" is-template="false" allow-conns="true"></database>', f'<role name="{owner}"></role>']
    lines.append(f'<schema name="{schema}" layers="0" rect-visible="true" fill-color="#e1e1e1" name-color="#000000"><role name="{owner}"/></schema>')
    for index, table in enumerate(model["tables"]):
        x, y = 80 + (index % 4) * 600, 80 + (index // 4) * 700
        lines.append(f'<table name={quoteattr(table["name"])} alias={quoteattr(table["kor"])} layers="0" collapse-mode="2" max-obj-count="{len(table["columns"])+4}" z-value="0">')
        lines += [f'\t<schema name="{schema}"/><role name="{owner}"/>', f'\t<comment> <![CDATA[{table["kor"]} — {table["description"]}]]> </comment>', f'\t<position x="{x}" y="{y}"/>']
        for column in table["columns"]:
            attrs = [f'name={quoteattr(column["name"])}', f'alias={quoteattr(column["kor"])}']
            if not column["nullable"]:
                attrs.append('not-null="true"')
            if column.get("default") is not None:
                attrs.append(f'default-value={quoteattr(str(column["default"]))}')
            lines += [f'\t<column {" ".join(attrs)}>', f'\t\t{xml_type(column["type"])}', f'\t\t<comment> <![CDATA[{column["kor"]}]]> </comment>', '\t</column>']
        primary = [c["name"] for c in table["columns"] if c.get("pk")]
        lines += [f'\t<constraint name={quoteattr(table["primary_key_constraint"])} type="pk-constr" table={quoteattr(schema+"."+table["name"])}>', f'\t\t<columns names={quoteattr(",".join(primary))} ref-type="src-columns"/>', '\t</constraint>']
        for unique in table.get("observed_unique_constraints", []):
            lines += [f'\t<constraint name={quoteattr(unique["name"])} type="uq-constr" table={quoteattr(schema+"."+table["name"])}>', f'\t\t<columns names={quoteattr(",".join(unique["columns"]))} ref-type="src-columns"/>', '\t</constraint>']
        lines.append('</table>')
    for rel in model["relationships"]:
        lines.append(f'<constraint name={quoteattr(rel["name"])} type="fk-constr" comparison-type="MATCH SIMPLE" upd-action={quoteattr(rel["on_update"])} del-action={quoteattr(rel["on_delete"])} ref-table={quoteattr(schema+"."+rel["to"])} table={quoteattr(schema+"."+rel["from"])}>')
        lines += [f'\t<columns names={quoteattr(rel["from_col"])} ref-type="src-columns"/>', f'\t<columns names={quoteattr(rel["to_col"])} ref-type="dst-columns"/>', '</constraint>']
    for rel in model["relationships"]:
        alias = f'{tables[rel["from"]]["kor"]}→{tables[rel["to"]]["kor"]}'
        lines.append(f'<relationship name={quoteattr("rel_"+rel["name"])} alias={quoteattr(alias)} type="relfk" layers="0" src-table={quoteattr(schema+"."+rel["from"])} dst-table={quoteattr(schema+"."+rel["to"])} src-required="false" dst-required="false"/>')
    lines.append('</dbmodel>')
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ET.parse(path)


def style_sheet(ws, widths: list[int]) -> None:
    fill = PatternFill("solid", fgColor="D9EAF7")
    border = Border(bottom=Side(style="thin", color="808080"))
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.fill = fill
        cell.border = border
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    for index, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(index)].width = width


def export_xlsx(model: dict, path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "개요"
    ws.append(["항목", "내용"])
    ws.append(["프로젝트", model["project"]])
    ws.append(["DB", f"{model['db']} {model['db_version']}"])
    ws.append(["스키마", model["schema"]])
    ws.append(["기준", "운영 PostgreSQL 읽기 전용 역설계 기준선"])
    ws.append(["테이블 수", len(model["tables"])])
    ws.append(["컬럼 수", sum(len(t["columns"]) for t in model["tables"])])
    ws.append(["관계 수", len(model["relationships"])])
    ws.append(["가정", "\n".join(model.get("assumptions", []))])
    ws.append(["열린 질문", "\n".join(model.get("open_questions", []))])
    style_sheet(ws, [20, 100])

    ws = wb.create_sheet("테이블목록")
    ws.append(["스키마", "테이블명", "논리명", "구분", "설명", "PI여부", "컬럼수"])
    for table in model["tables"]:
        ws.append([model["schema"], table["name"], table["kor"], table["kind"], table["description"], "Y" if table["is_pi"] else "N", len(table["columns"])])
    style_sheet(ws, [12, 28, 20, 10, 55, 10, 10])

    ws = wb.create_sheet("컬럼명세")
    ws.append(["테이블명", "테이블논리명", "순번", "컬럼명", "논리명", "도메인", "자료형", "NULL", "PK", "FK(참조)", "UNIQUE", "기본값", "CHECK", "PI", "설명"])
    for table in model["tables"]:
        for ordinal, column in enumerate(table["columns"], 1):
            fk = column.get("fk")
            ws.append([table["name"], table["kor"], ordinal, column["name"], column["kor"], column["domain"], column["type"], "Y" if column["nullable"] else "N", "Y" if column.get("pk") else "N", f"{fk['table']}.{fk['column']}" if fk else "", "Y" if column.get("unique") else "N", column.get("default") or "", "", "Y" if column.get("pi") else "N", column.get("description") or ""])
    style_sheet(ws, [28, 20, 8, 28, 24, 24, 24, 8, 8, 34, 10, 38, 14, 8, 40])

    ws = wb.create_sheet("관계(FK)")
    ws.append(["제약명", "자식테이블", "자식컬럼", "부모테이블", "부모컬럼", "관계", "필수", "삭제규칙", "갱신규칙", "업무의미"])
    for rel in model["relationships"]:
        ws.append([rel["name"], rel["from"], rel["from_col"], rel["to"], rel["to_col"], rel["type"], "N" if rel["optional"] else "Y", rel["on_delete"], rel["on_update"], rel["meaning"]])
    style_sheet(ws, [44, 28, 20, 28, 20, 10, 10, 14, 14, 55])

    ws = wb.create_sheet("용어사전")
    ws.append(["구분", "한글", "약어/물리명", "영문/단어경로", "도메인", "설명"])
    for word in model["words"]:
        ws.append(["단어", word["kor"], word["abbr"], word["full"], "", word["desc"]])
    for term in model["terms"]:
        ws.append(["용어", term["kor"], term["phys"], term["word_path"], term["domain"] or "", term.get("desc") or ""])
    for domain in model["domains"]:
        ws.append(["도메인", domain["name"], "", domain["type"], "", domain["desc"]])
    style_sheet(ws, [12, 24, 30, 40, 28, 55])

    ws = wb.create_sheet("개인정보")
    ws.append(["테이블", "컬럼", "논리명", "현재 판정", "제안"])
    ws.append(["ask_logs", "question, answer", "질문·답변", "자유 텍스트에 개인정보 포함 가능", "보존 기간과 파기 정책 결정"])
    ws.append(["feedback_logs", "comment", "피드백 내용", "자유 텍스트에 개인정보 포함 가능", "보존 기간과 파기 정책 결정"])
    style_sheet(ws, [28, 28, 22, 55, 55])

    ws = wb.create_sheet("코드정의")
    ws.append(["대상", "현재 상태", "검토 사항"])
    ws.append(["status/category/rating", "자유 텍스트", "후속 개선 작업에서 코드/체크 제약 검토"])
    style_sheet(ws, [34, 28, 70])

    ws = wb.create_sheet("검토메모")
    ws.append(["구분", "내용"])
    for note in model.get("dq_notes", []):
        ws.append(["DQ", note])
    for question in model.get("open_questions", []):
        ws.append(["열린 질문", question])
    style_sheet(ws, [18, 110])
    wb.properties.creator = "BOMTS dev-process"
    fixed_time = datetime(2026, 10, 10, tzinfo=timezone.utc)
    wb.properties.created = fixed_time
    wb.properties.modified = fixed_time
    wb.save(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("model", nargs="?", default="db/model.json")
    parser.add_argument("outdir", nargs="?", default="db/out")
    parser.add_argument("--pgmodeler-ver", default="1.1.0")
    args = parser.parse_args()
    model = load_model(Path(args.model))
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    export_ddl(model, out / "02_ddl_postgresql.sql")
    export_dbm(model, out / "03_model.dbm", args.pgmodeler_ver)
    export_xlsx(model, out / "04_table_spec.xlsx")
    print(f"exported={out} tables={len(model['tables'])} columns={sum(len(t['columns']) for t in model['tables'])} relationships={len(model['relationships'])}")


if __name__ == "__main__":
    main()
