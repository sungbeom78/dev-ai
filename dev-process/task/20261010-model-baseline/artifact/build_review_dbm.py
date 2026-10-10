#!/usr/bin/env python3
"""Build a review-only pgModeler file from the read-only reverse-engineered model.

This adapter exists because the framework exporter expects the prospective-design
model contract, while the initial baseline stores observed PostgreSQL types,
relationships, constraints, and indexes directly. It never connects to a database.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parents[4]
MODEL = ROOT / "db/model.json"
OUTPUT = Path(__file__).resolve().parent / "logical-review/03_model.dbm"


def xml_type(pg_type: str) -> str:
    match = re.fullmatch(r"character varying\((\d+)\)", pg_type)
    if match:
        return f'<type name="varchar" length="{match.group(1)}"/>'
    return f'<type name={quoteattr(pg_type)} length="0"/>'


model = json.loads(MODEL.read_text(encoding="utf-8"))
tables = {table["name"]: table for table in model["tables"]}
lines: list[str] = []
write = lines.append

write('<?xml version="1.0" encoding="UTF-8"?>')
write('<!-- Review artifact generated from db/model.json; do not edit by hand. -->')
write(
    '<dbmodel pgmodeler-ver="1.1.0" use-changelog="false" '
    f'max-obj-count="{len(tables) + 8}" last-position="0,0" last-zoom="1" '
    'scene-rect="0,0,2600,1600" default-schema="public" default-owner="bomts_app" '
    'layers="Default layer" active-layers="0" layer-name-colors="#000000" '
    'layer-rect-colors="#b4b4b4" show-layer-names="false" show-layer-rects="false">'
)
write('<database name="bomts" is-template="false" allow-conns="true"></database>')
write('<role name="bomts_app"></role>')
write(
    '<schema name="public" layers="0" rect-visible="true" fill-color="#e1e1e1" '
    'name-color="#000000"><role name="bomts_app"/></schema>'
)

for index, table in enumerate(model["tables"]):
    x = 80 + (index % 4) * 600
    y = 80 + (index // 4) * 700
    table_name = table["name"]
    write(
        f'<table name={quoteattr(table_name)} alias={quoteattr(table["kor"])} layers="0" '
        f'collapse-mode="2" max-obj-count="{len(table["columns"]) + 4}" z-value="0">'
    )
    write('\t<schema name="public"/><role name="bomts_app"/>')
    write(f'\t<comment> <![CDATA[{table["kor"]} — {table["description"]}]]> </comment>')
    write(f'\t<position x="{x}" y="{y}"/>')
    for column in table["columns"]:
        attrs = [f'name={quoteattr(column["name"])}', f'alias={quoteattr(column["kor"])}']
        if not column["nullable"]:
            attrs.append('not-null="true"')
        if column.get("default") is not None:
            attrs.append(f'default-value={quoteattr(str(column["default"]))}')
        write(f'\t<column {" ".join(attrs)}>')
        write(f'\t\t{xml_type(column["type"])}')
        write(f'\t\t<comment> <![CDATA[{column["kor"]}]]> </comment>')
        write('\t</column>')
    primary_columns = [column["name"] for column in table["columns"] if column.get("pk")]
    write(f'\t<constraint name={quoteattr(table_name + "_pkey")} type="pk-constr" table={quoteattr("public." + table_name)}>')
    write(f'\t\t<columns names={quoteattr(",".join(primary_columns))} ref-type="src-columns"/>')
    write('\t</constraint>')
    for unique in table.get("uniques", []):
        write(f'\t<constraint name={quoteattr(unique["name"])} type="uq-constr" table={quoteattr("public." + table_name)}>')
        write(f'\t\t<columns names={quoteattr(",".join(unique["columns"]))} ref-type="src-columns"/>')
        write('\t</constraint>')
    write('</table>')

for relationship in model["relationships"]:
    write(
        f'<constraint name={quoteattr(relationship["name"])} type="fk-constr" comparison-type="MATCH SIMPLE" '
        f'upd-action={quoteattr(relationship["on_update"])} del-action={quoteattr(relationship["on_delete"])} '
        f'ref-table={quoteattr("public." + relationship["to"])} table={quoteattr("public." + relationship["from"])}>'
    )
    write(f'\t<columns names={quoteattr(",".join(relationship["from_columns"]))} ref-type="src-columns"/>')
    write(f'\t<columns names={quoteattr(",".join(relationship["to_columns"]))} ref-type="dst-columns"/>')
    write('</constraint>')

for relationship in model["relationships"]:
    source = tables[relationship["from"]]
    target = tables[relationship["to"]]
    alias = f'{source["kor"]}→{target["kor"]}'
    write(
        f'<relationship name={quoteattr("rel_" + relationship["name"])} alias={quoteattr(alias)} '
        f'type="relfk" layers="0" src-table={quoteattr("public." + relationship["from"])} '
        f'dst-table={quoteattr("public." + relationship["to"])} src-required="false" dst-required="false"/>'
    )

write('</dbmodel>')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

root = ET.parse(OUTPUT).getroot()
assert sum(1 for _ in root.iter("table")) == 8
assert sum(1 for _ in root.iter("column")) == 80
assert sum(1 for _ in root.iter("relationship")) == 6
print(f"generated={OUTPUT}")
print("tables=8 columns=80 relationships=6 xml=well_formed")
