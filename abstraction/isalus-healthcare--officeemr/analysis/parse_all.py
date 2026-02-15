"""
Parse all EHI export artifacts for iSALUS/OfficeEMR:
1. JSON Schema files → entity/field inventory
2. XLSX data dictionary → field descriptions
3. Sample export JSON files → record counts and field coverage
Outputs analysis results as JSON files.
"""
import json, os, glob as globmod
from pathlib import Path
import openpyxl

BASE = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare--officeemr/downloads")
OUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare--officeemr/analysis")

# ── 1. Parse JSON Schema files ──
schema_dir = BASE / "schema" / "OfficeEMR_B10_Schema_v1-OCT2023"
schema_inventory = []
for f in sorted(schema_dir.glob("*.schema.json")):
    with open(f) as fh:
        schema = json.load(fh)
    entity_name = f.stem.replace(".schema", "")
    # Schemas wrap records as array of objects: items.properties
    items = schema.get("items", schema)
    props = items.get("properties", schema.get("properties", {}))
    fields = []
    for fname, fdef in props.items():
        desc = fdef.get("description", "")
        ftype = fdef.get("type", "unknown")
        fields.append({
            "name": fname,
            "type": ftype,
            "has_description": bool(desc and desc.strip())
        })
    schema_inventory.append({
        "entity": entity_name,
        "field_count": len(fields),
        "fields_with_descriptions": sum(1 for f in fields if f["has_description"]),
        "fields": fields
    })

with open(OUT / "schema-inventory.json", "w") as fh:
    json.dump(schema_inventory, fh, indent=2)

total_schema_fields = sum(e["field_count"] for e in schema_inventory)
total_schema_described = sum(e["fields_with_descriptions"] for e in schema_inventory)
print(f"JSON Schemas: {len(schema_inventory)} entities, {total_schema_fields} total fields, {total_schema_described} with descriptions")

# ── 2. Parse XLSX data dictionary ──
xlsx_path = BASE / "data-elements" / "iSalus_EHI_ExportDataElements_published_version1_Oct2023_pristine.xlsx"
wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
xlsx_data = {}
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        xlsx_data[sheet_name] = {"headers": [], "row_count": 0, "fields": []}
        continue
    headers = [str(h).strip() if h else "" for h in rows[0]]
    data_rows = rows[1:]
    xlsx_data[sheet_name] = {
        "headers": headers,
        "row_count": len(data_rows),
        "sample_rows": [list(r) for r in data_rows[:3]]
    }

# Parse field-level detail from XLSX
xlsx_fields = []
xlsx_entities = {}
for sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    if len(rows) < 2:
        continue
    headers = [str(h).strip().lower() if h else "" for h in rows[0]]
    
    # Find relevant columns
    export_col = None
    field_col = None
    desc_col = None
    for i, h in enumerate(headers):
        if "export" in h and "name" in h:
            export_col = i
        elif h == "field":
            field_col = i
        elif "description" in h:
            desc_col = i
    
    if field_col is None:
        continue
    
    for row in rows[1:]:
        export_name = str(row[export_col]).strip() if export_col is not None and row[export_col] else ""
        field_name = str(row[field_col]).strip() if row[field_col] else ""
        description = str(row[desc_col]).strip() if desc_col is not None and row[desc_col] else ""
        
        if not field_name or field_name == "None":
            continue
        
        # Clean export name
        export_name = export_name.replace(".json", "").strip()
        
        has_desc = bool(description and description != "None" and len(description) > 0)
        
        xlsx_fields.append({
            "sheet": sheet_name,
            "entity": export_name,
            "field": field_name,
            "description": description if has_desc else "",
            "has_description": has_desc
        })
        
        if export_name not in xlsx_entities:
            xlsx_entities[export_name] = {"fields": 0, "with_desc": 0, "sheet": sheet_name}
        xlsx_entities[export_name]["fields"] += 1
        if has_desc:
            xlsx_entities[export_name]["with_desc"] += 1

wb.close()

with open(OUT / "xlsx-summary.json", "w") as fh:
    json.dump({
        "sheets": xlsx_data,
        "entity_summary": xlsx_entities,
        "total_fields": len(xlsx_fields),
        "total_with_descriptions": sum(1 for f in xlsx_fields if f["has_description"])
    }, fh, indent=2, default=str)

print(f"\nXLSX Data Dictionary:")
print(f"  Sheets: {list(xlsx_data.keys())}")
print(f"  Total field entries: {len(xlsx_fields)}")
print(f"  Fields with descriptions: {sum(1 for f in xlsx_fields if f['has_description'])}")
print(f"  Distinct entities: {len(xlsx_entities)}")

# ── 3. Parse sample export ──
sample_dir = BASE / "sample-export"
sample_inventory = []
for f in sorted(sample_dir.glob("*.json")):
    with open(f, encoding='utf-8-sig') as fh:
        try:
            data = json.load(fh)
        except json.JSONDecodeError:
            sample_inventory.append({
                "file": f.name,
                "error": "invalid JSON",
                "record_count": 0,
                "field_count": 0,
                "populated_fields": 0,
                "fields": []
            })
            continue
    
    entity_name = f.stem
    if isinstance(data, list):
        record_count = len(data)
        # Get field names from first record
        if record_count > 0 and isinstance(data[0], dict):
            all_fields = set()
            populated_fields = set()
            for rec in data:
                for k, v in rec.items():
                    all_fields.add(k)
                    if v is not None and v != "" and v != 0:
                        populated_fields.add(k)
            fields_info = sorted(all_fields)
        else:
            fields_info = []
            populated_fields = set()
    elif isinstance(data, dict):
        record_count = 1
        fields_info = sorted(data.keys())
        populated_fields = {k for k, v in data.items() if v is not None and v != ""}
    else:
        record_count = 0
        fields_info = []
        populated_fields = set()
    
    sample_inventory.append({
        "file": f.name,
        "record_count": record_count,
        "field_count": len(fields_info),
        "populated_fields": len(populated_fields),
        "fields": fields_info
    })

with open(OUT / "sample-export-inventory.json", "w") as fh:
    json.dump(sample_inventory, fh, indent=2)

total_sample_records = sum(s["record_count"] for s in sample_inventory)
print(f"\nSample Export:")
print(f"  Files: {len(sample_inventory)}")
print(f"  Total records: {total_sample_records}")
for s in sorted(sample_inventory, key=lambda x: -x["record_count"])[:15]:
    print(f"    {s['file']}: {s['record_count']} records, {s['field_count']} fields ({s['populated_fields']} populated)")

# ── 4. Cross-reference: schemas vs sample export vs XLSX ──
schema_entities = set(e["entity"] for e in schema_inventory)
sample_entities = set(s["file"].replace(".json", "") for s in sample_inventory)
xlsx_entity_set = set(xlsx_entities.keys())

print(f"\n=== Cross-Reference ===")
print(f"Schema entities: {len(schema_entities)}")
print(f"Sample export files: {len(sample_entities)}")
print(f"XLSX entities: {len(xlsx_entity_set)}")

in_schema_not_sample = schema_entities - sample_entities
in_sample_not_schema = sample_entities - schema_entities

print(f"\nIn schema but not sample ({len(in_schema_not_sample)}):")
for e in sorted(in_schema_not_sample):
    print(f"  - {e}")

print(f"\nIn sample but not schema ({len(in_sample_not_schema)}):")
for e in sorted(in_sample_not_schema):
    print(f"  - {e}")

# ── 5. Build complete entity inventory ──
all_entities = sorted(schema_entities | sample_entities | xlsx_entity_set)
entity_inventory = []
for e in all_entities:
    schema_match = next((s for s in schema_inventory if s["entity"] == e), None)
    sample_match = next((s for s in sample_inventory if s["file"].replace(".json", "") == e), None)
    xlsx_match = xlsx_entities.get(e)
    
    entity_inventory.append({
        "entity": e,
        "in_schema": e in schema_entities,
        "in_sample": e in sample_entities,
        "in_xlsx": e in xlsx_entity_set,
        "schema_fields": schema_match["field_count"] if schema_match else 0,
        "xlsx_fields": xlsx_match["fields"] if xlsx_match else 0,
        "xlsx_described": xlsx_match["with_desc"] if xlsx_match else 0,
        "xlsx_category": xlsx_match["sheet"] if xlsx_match else "",
        "sample_records": sample_match["record_count"] if sample_match else 0,
        "sample_fields": sample_match["field_count"] if sample_match else 0
    })

with open(OUT / "full-entity-inventory.json", "w") as fh:
    json.dump(entity_inventory, fh, indent=2)

# Category summary
categories = {}
for e in entity_inventory:
    cat = e["xlsx_category"] or "Uncategorized"
    if cat not in categories:
        categories[cat] = {"entities": 0, "schema_fields": 0, "xlsx_fields": 0, "xlsx_described": 0}
    categories[cat]["entities"] += 1
    categories[cat]["schema_fields"] += e["schema_fields"]
    categories[cat]["xlsx_fields"] += e["xlsx_fields"]
    categories[cat]["xlsx_described"] += e["xlsx_described"]

print(f"\n=== Categories (from XLSX) ===")
for cat, stats in sorted(categories.items()):
    desc_pct = f"{stats['xlsx_described']/stats['xlsx_fields']*100:.0f}%" if stats['xlsx_fields'] > 0 else "N/A"
    print(f"  {cat}: {stats['entities']} entities, {stats['schema_fields']} schema fields, {stats['xlsx_fields']} xlsx fields ({desc_pct} described)")

with open(OUT / "category-summary.json", "w") as fh:
    json.dump(categories, fh, indent=2)

print("\n=== Done ===")
