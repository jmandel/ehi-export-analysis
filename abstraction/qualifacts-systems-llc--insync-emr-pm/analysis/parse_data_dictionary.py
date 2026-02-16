#!/usr/bin/env python3
"""
Parse InSync EHI Export Data Dictionary XLS → entity-inventory-full.json + summary.
Reads the raw XLS directly (not enrichment output).
"""

import json
import sys
import os

# Activate venv if present
venv_path = os.path.join(os.path.dirname(__file__), '.venv')
if os.path.exists(venv_path):
    activate = os.path.join(venv_path, 'bin', 'activate_this.py')

import xlrd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
XLS_PATH = os.path.join(SCRIPT_DIR, '..', 'downloads', 'InSync_EHI_Export_Data_Dictionary.xls')

SKIP_SHEETS = {"Confidential Notice", "INDEX", "Changelogs"}

def parse_index(wb):
    """Parse INDEX sheet for category/module metadata."""
    ws = wb.sheet_by_name("INDEX")
    entries = []
    for i in range(3, ws.nrows):
        row = [ws.cell_value(i, c) for c in range(ws.ncols)]
        section_name = str(row[1]).strip() if len(row) > 1 else ""
        if not section_name:
            continue
        entries.append({
            "section_name": section_name,
            "category": str(row[2]).strip() if len(row) > 2 else "",
            "module": str(row[3]).strip() if len(row) > 3 else "",
            "details": str(row[4]).strip() if len(row) > 4 else "",
        })
    return entries

def find_index_entry(sheet_name, index_entries):
    """Match sheet name to INDEX entry (exact or prefix match)."""
    sn_lower = sheet_name.lower()
    for e in index_entries:
        if e["section_name"].lower() == sn_lower:
            return e
    for e in index_entries:
        if e["section_name"].lower().startswith(sn_lower):
            return e
    for e in index_entries:
        if sn_lower.startswith(e["section_name"].lower()[:30]):
            return e
    return None

def parse_sheet(ws, sheet_name, index_entries):
    """Parse a data section sheet into entity with fields."""
    # Get description from row 1, col 2
    description = ""
    if ws.nrows > 1 and ws.ncols > 2:
        description = str(ws.cell_value(1, 2)).strip()

    # Find header row
    header_row_idx = -1
    for i in range(min(10, ws.nrows)):
        for c in range(ws.ncols):
            val = str(ws.cell_value(i, c)).strip().lower()
            if "name of the column" in val:
                header_row_idx = i
                break
        if header_row_idx >= 0:
            break

    if header_row_idx < 0:
        return None, f"No header row found in sheet '{sheet_name}'"

    fields = []
    for i in range(header_row_idx + 1, ws.nrows):
        row = [ws.cell_value(i, c) if c < ws.ncols else "" for c in range(6)]
        col_name = str(row[1]).strip()
        if not col_name:
            continue
        
        desc = str(row[4]).strip() if len(row) > 4 else ""
        remarks = str(row[5]).strip() if len(row) > 5 else ""
        
        fields.append({
            "column_name": col_name,
            "data_type": str(row[2]).strip(),
            "nullable": str(row[3]).strip().lower() == "yes",
            "description": desc,
            "remarks": remarks if remarks else None,
        })

    idx = find_index_entry(sheet_name, index_entries)
    
    return {
        "entity_name": idx["section_name"] if idx else sheet_name,
        "sheet_name": sheet_name,
        "description": description,
        "category": idx["category"] if idx else "",
        "module": idx["module"] if idx else "",
        "field_count": len(fields),
        "fields": fields,
    }, None

def main():
    wb = xlrd.open_workbook(XLS_PATH)
    index_entries = parse_index(wb)
    
    entities = []
    failures = []
    
    for sheet_name in wb.sheet_names():
        if sheet_name in SKIP_SHEETS:
            continue
        ws = wb.sheet_by_name(sheet_name)
        entity, error = parse_sheet(ws, sheet_name, index_entries)
        if error:
            failures.append({"sheet": sheet_name, "error": error})
        elif entity:
            entities.append(entity)

    # Compute stats
    total_fields = sum(e["field_count"] for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e["fields"]
        if f["description"] and f["description"] != f["column_name"]
    )
    fields_with_type = sum(
        1 for e in entities for f in e["fields"]
        if f["data_type"]
    )

    # Category breakdown
    categories = {}
    for e in entities:
        cat = e["category"] or "(uncategorized)"
        if cat not in categories:
            categories[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += sum(1 for _ in e["fields"])
        categories[cat]["entities"].append(e["entity_name"])

    # Full inventory
    full_inventory = {
        "source_file": "InSync_EHI_Export_Data_Dictionary.xls",
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "parse_failures": failures,
        "entities": entities,
    }

    # Summary
    summary = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "pct_with_descriptions": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
        "pct_with_types": round(100 * fields_with_type / total_fields, 1) if total_fields else 0,
        "parse_failures": len(failures),
        "categories": {k: {"entity_count": v["entity_count"], "field_count": v["field_count"], "entities": v["entities"]} for k, v in sorted(categories.items())},
        "entities_by_size": sorted(
            [{"entity": e["entity_name"], "category": e["category"], "module": e["module"], "fields": e["field_count"]} for e in entities],
            key=lambda x: -x["fields"]
        ),
    }

    with open(os.path.join(SCRIPT_DIR, "entity-inventory-full.json"), "w") as f:
        json.dump(full_inventory, f, indent=2)
    
    with open(os.path.join(SCRIPT_DIR, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['pct_with_descriptions']}%)")
    print(f"Fields with types: {fields_with_type} ({summary['pct_with_types']}%)")
    print(f"Parse failures: {len(failures)}")
    
    print("\nCategory breakdown:")
    for cat, info in sorted(categories.items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    
    print("\nTop 15 entities by field count:")
    for item in summary["entities_by_size"][:15]:
        print(f"  {item['entity']}: {item['fields']} fields ({item['category']} / {item['module']})")

if __name__ == "__main__":
    main()
