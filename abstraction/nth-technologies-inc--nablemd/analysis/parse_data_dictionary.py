"""
Parse all CSV data dictionary sheets from nAbleMD's Google Sheets export.
Each CSV file represents one entity/table, with columns: FieldName, Description.
Some CSVs have a "Table Description" header row before the field rows.
Outputs entity-inventory-full.json and entity-inventory-summary.json.
"""

import csv
import json
import os
import sys
from pathlib import Path
from collections import defaultdict

CSV_DIR = Path("../downloads/csv-sheets")
SKIP_FILES = {"read_me.csv", "table_of_contents.csv", "revision_history.csv"}

def parse_csv_sheet(filepath):
    """Parse a single CSV data dictionary sheet."""
    entity_name = filepath.stem  # filename without .csv
    table_description = ""
    fields = []
    
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if not rows:
        return {"entity": entity_name, "table_description": "", "fields": [], "parse_error": "empty file"}
    
    # Find the field header row (FieldName, Description)
    field_start = None
    for i, row in enumerate(rows):
        if len(row) >= 2:
            # Check for "Table Description" row
            if row[0].strip().lower() == "table description":
                # Next non-empty row might be the description
                if i + 1 < len(rows) and rows[i+1]:
                    table_description = rows[i][1].strip() if len(row) > 1 else ""
                    # Sometimes description is in the next row
                    if not table_description and i + 1 < len(rows):
                        table_description = rows[i+1][0].strip() if rows[i+1] else ""
            
            # Standard header or entity-named header (e.g., "EmrDonor", "Description")
            if (row[0].strip().lower() == "fieldname" or 
                (row[1].strip().lower() == "description" and row[0].strip().lower() != "table description")):
                field_start = i + 1
                break
    
    if field_start is None:
        # Try to find fields anyway - maybe no header
        return {"entity": entity_name, "table_description": table_description, "fields": [], 
                "parse_error": "no FieldName header found", "raw_rows": len(rows)}
    
    # Also look for table description before the FieldName row
    for i in range(field_start - 1):
        row = rows[i]
        if len(row) >= 1 and row[0].strip().lower() == "table description" and len(row) >= 2:
            table_description = row[1].strip()
        # Sometimes the description is in a standalone row after "Table Description"
        if len(row) >= 1 and row[0].strip() and row[0].strip().lower() not in ("table description", "fieldname", ""):
            if not any(r[0].strip().lower() == "table description" for r in rows[:i]):
                continue
            if not table_description:
                table_description = row[0].strip()
    
    # Parse fields
    for i in range(field_start, len(rows)):
        row = rows[i]
        if not row or not row[0].strip():
            continue
        field_name = row[0].strip()
        description = row[1].strip() if len(row) > 1 else ""
        fields.append({
            "name": field_name,
            "description": description,
            "has_description": bool(description)
        })
    
    return {
        "entity": entity_name,
        "table_description": table_description,
        "fields": fields,
        "field_count": len(fields)
    }


def categorize_entity(entity_name):
    """Categorize entities based on naming patterns."""
    name_lower = entity_name.lower()
    
    # IVF/Fertility
    ivf_keywords = ['cycle', 'oocyte', 'ivf', 'semen', 'embryo', 'cryo', 'donor', 
                     'culture', 'transfer', 'infertility', 'follicular', 'witnessing']
    if any(k in name_lower for k in ivf_keywords):
        return "IVF/Fertility"
    
    # OB/GYN
    ob_keywords = ['pregnancy', 'obgyn', 'obhistory', 'obstetric', 'contraception',
                    'multibirth', 'estimatedduedate', 'pregoutcome']
    if any(k in name_lower for k in ob_keywords):
        return "OB/GYN"
    
    # Billing/Financial
    billing_keywords = ['payment', 'billing', 'ledger', 'charge', 'prepayment', 
                        'quote', 'insurance', 'priorauth', 'visitpayment']
    if any(k in name_lower for k in billing_keywords):
        return "Billing/Financial"
    
    # Clinical/EMR
    if name_lower.startswith('emr') and name_lower not in [e.lower() for e in []]:
        return "Clinical/EMR"
    
    # Medications
    if 'newcrop' in name_lower or 'drug' in name_lower:
        return "Medications"
    
    # Immunizations
    if 'immunization' in name_lower:
        return "Immunizations"
    
    # Documents
    if 'document' in name_lower or 'chartnote' in name_lower or 'cosign' in name_lower:
        return "Documents/Notes"
    
    # Patient
    if name_lower.startswith('patient') or name_lower == 'patients' or name_lower == 'relative':
        return "Patient Demographics/Admin"
    
    # Communication
    if 'patmail' in name_lower or 'smsnavi' in name_lower:
        return "Communications"
    
    # Scheduling
    if 'appointment' in name_lower or 'dailyworklist' in name_lower:
        return "Scheduling"
    
    # Tasks
    if name_lower in ('task', 'taskassigned', 'action'):
        return "Tasks/Workflow"
    
    # Visits/Encounters
    if name_lower in ('visit', 'procedure', 'procedurecharge'):
        return "Encounters/Visits"
    
    # Consent/Forms
    if 'consent' in name_lower or 'kiosk' in name_lower or 'survey' in name_lower:
        return "Consent/Forms"
    
    return "Other"


def main():
    entities = []
    csv_files = sorted(CSV_DIR.glob("*.csv"))
    
    for csv_file in csv_files:
        if csv_file.name in SKIP_FILES:
            continue
        result = parse_csv_sheet(csv_file)
        result["category"] = categorize_entity(result["entity"])
        entities.append(result)
    
    # Write full inventory
    with open("entity-inventory-full.json", 'w') as f:
        json.dump(entities, f, indent=2)
    
    # Compute summary
    total_entities = len(entities)
    total_fields = sum(e["field_count"] for e in entities if "field_count" in e)
    fields_with_desc = sum(
        sum(1 for fd in e["fields"] if fd["has_description"]) 
        for e in entities
    )
    fields_without_desc = total_fields - fields_with_desc
    
    # Category breakdown
    categories = defaultdict(lambda: {"entity_count": 0, "field_count": 0, "entities": []})
    for e in entities:
        cat = e["category"]
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += e.get("field_count", 0)
        categories[cat]["entities"].append(e["entity"])
    
    # Top entities by field count
    sorted_entities = sorted(entities, key=lambda e: e.get("field_count", 0), reverse=True)
    top_entities = [
        {"entity": e["entity"], "field_count": e["field_count"], "category": e["category"],
         "described": sum(1 for f in e["fields"] if f["has_description"])}
        for e in sorted_entities[:20]
    ]
    
    # Entities with parse errors
    error_entities = [e for e in entities if "parse_error" in e]
    
    summary = {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_without_descriptions": fields_without_desc,
        "description_percentage": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "categories": dict(categories),
        "top_20_entities_by_field_count": top_entities,
        "entities_with_parse_errors": [{"entity": e["entity"], "error": e.get("parse_error", "")} for e in error_entities],
        "entities_with_table_descriptions": sum(1 for e in entities if e.get("table_description"))
    }
    
    with open("entity-inventory-summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Total entities: {total_entities}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['description_percentage']}%)")
    print(f"Entities with table descriptions: {summary['entities_with_table_descriptions']}")
    print(f"\nCategories:")
    for cat, info in sorted(categories.items(), key=lambda x: x[1]["field_count"], reverse=True):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print(f"\nTop 10 entities by field count:")
    for e in top_entities[:10]:
        print(f"  {e['entity']}: {e['field_count']} fields ({e['described']} described) [{e['category']}]")
    if error_entities:
        print(f"\nEntities with parse errors: {len(error_entities)}")
        for e in error_entities:
            print(f"  {e['entity']}: {e.get('parse_error', '')}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
