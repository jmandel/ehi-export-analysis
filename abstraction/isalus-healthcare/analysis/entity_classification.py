#!/usr/bin/env python3
"""Generate the comprehensive entity-field table for the analysis, including XLSX descriptions,
data type classification, and sample data coverage. Run with venv python."""

import json
from pathlib import Path
import openpyxl

XLSX_PATH = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare/downloads/data-elements/iSalus_EHI_ExportDataElements_published_version1_Oct2023_pristine.xlsx")
SCHEMA_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare/downloads/schema/OfficeEMR_B10_Schema_v1-OCT2023")
SAMPLE_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/isalus-healthcare/downloads/sample-export")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare/analysis")

# Parse XLSX
wb = openpyxl.load_workbook(XLSX_PATH, read_only=True)
ws = wb['Export Field Listing']
rows = list(ws.iter_rows(values_only=True))
header = rows[0]

xlsx_entities = {}
for row in rows[1:]:
    export_name = str(row[0]).strip() if row[0] else ""
    field = str(row[3]).strip() if row[3] else ""
    desc = str(row[4]).strip() if row[4] else ""
    example = str(row[5]).strip() if row[5] else ""
    dtype = str(row[6]).strip() if row[6] else ""
    
    if not export_name:
        continue
    # Normalize entity name (remove .json)
    entity = export_name.replace(".json", "")
    if entity not in xlsx_entities:
        xlsx_entities[entity] = {"fields": [], "data_type": dtype}
    xlsx_entities[entity]["fields"].append({
        "field": field,
        "description": desc,
        "example": example,
        "data_type": dtype
    })

# Count by data_type
clinical_entities = []
pm_entities = []
for entity, info in sorted(xlsx_entities.items()):
    dtype = info["data_type"]
    if dtype == "Clinical":
        clinical_entities.append(entity)
    elif dtype == "PM":
        pm_entities.append(entity)
    else:
        clinical_entities.append(entity)  # default

# Parse schemas for field counts
schema_field_counts = {}
for f in sorted(SCHEMA_DIR.glob("*.json")):
    try:
        with open(f) as fh:
            schema = json.load(fh)
        items = schema.get("items", {})
        props = items.get("properties", schema.get("properties", {}))
        entity = f.stem.replace(".schema", "")
        schema_field_counts[entity] = len(props)
    except:
        pass

# Parse sample export for record counts
sample_record_counts = {}
for f in sorted(SAMPLE_DIR.glob("*.json")):
    entity = f.stem
    try:
        with open(f, encoding='utf-8-sig') as fh:
            data = json.load(fh)
        if isinstance(data, list):
            sample_record_counts[entity] = len(data)
        else:
            sample_record_counts[entity] = 1
    except:
        sample_record_counts[entity] = -1

# Build unified summary table
print("=== Clinical Data Entities ===")
print(f"{'Entity':<45} {'XLSX Fields':>11} {'Schema Fields':>13} {'Sample Recs':>11}")
print("-" * 85)
clinical_total_fields = 0
for e in sorted(clinical_entities):
    xlsx_fields = len(xlsx_entities.get(e, {}).get("fields", []))
    schema_fields = schema_field_counts.get(e, 0)
    sample_recs = sample_record_counts.get(e, 0)
    clinical_total_fields += xlsx_fields
    print(f"{e:<45} {xlsx_fields:>11} {schema_fields:>13} {sample_recs:>11}")

print(f"\nClinical entities: {len(clinical_entities)}, total fields: {clinical_total_fields}")

print("\n=== Practice Management Entities ===")
print(f"{'Entity':<45} {'XLSX Fields':>11} {'Schema Fields':>13} {'Sample Recs':>11}")
print("-" * 85)
pm_total_fields = 0
for e in sorted(pm_entities):
    xlsx_fields = len(xlsx_entities.get(e, {}).get("fields", []))
    schema_fields = schema_field_counts.get(e, 0)
    sample_recs = sample_record_counts.get(e, 0)
    pm_total_fields += xlsx_fields
    print(f"{e:<45} {xlsx_fields:>11} {schema_fields:>13} {sample_recs:>11}")

print(f"\nPM entities: {len(pm_entities)}, total fields: {pm_total_fields}")
print(f"\nGrand total: {len(clinical_entities) + len(pm_entities)} entities, {clinical_total_fields + pm_total_fields} fields")

# Save
output = {
    "clinical": {"count": len(clinical_entities), "total_fields": clinical_total_fields, "entities": clinical_entities},
    "practice_management": {"count": len(pm_entities), "total_fields": pm_total_fields, "entities": pm_entities},
    "grand_total_entities": len(clinical_entities) + len(pm_entities),
    "grand_total_fields": clinical_total_fields + pm_total_fields,
}
with open(OUTPUT_DIR / "entity_classification.json", "w") as fh:
    json.dump(output, fh, indent=2)
print(f"\nSaved to {OUTPUT_DIR / 'entity_classification.json'}")
