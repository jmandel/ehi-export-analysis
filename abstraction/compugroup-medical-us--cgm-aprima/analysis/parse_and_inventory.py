#!/usr/bin/env python3
"""
Parse the enrichment JSON data dictionary and the raw PDF text to produce:
1. full-entity-inventory.json — complete field-level inventory
2. summary-stats.json — aggregate statistics
3. category-breakdown.json — fields grouped by domain category
"""

import json
import re
import sys
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/compugroup-medical-us--cgm-aprima")
ENRICHMENT_JSON = RESULTS_DIR / "downloads/enrichment/ehi-data-dictionary.json"
OUTPUT_DIR = Path(__file__).parent

# Load the enrichment JSON (prior agent's extraction)
with open(ENRICHMENT_JSON) as f:
    data = json.load(f)

# Assign domain categories based on CSV file content
DOMAIN_MAP = {
    "Audit Trail": "Administrative",
    "Contacts": "Demographics",
    "Active Medication": "Clinical",
    "Allergies": "Clinical",
    "Appointment Information": "Administrative",
    "Family History": "Clinical",
    "Immunization": "Clinical",
    "Medical History": "Clinical",
    "Patient Demographics": "Demographics",
    "Patient Insurance": "Insurance / Coverage",
    "Problem List": "Clinical",
    "Responsible Party": "Demographics",
    "Results": "Clinical",
    "Social History": "Clinical",
    "Visit Comments": "Clinical",
    "Vitals": "Clinical",
    "Eligibility": "Insurance / Coverage",
    "Employment": "Demographics",
    "Patient Ledger": "Billing / Financial",
    "Patient Referrals": "Clinical",
    "Providers": "Clinical",
    "Response Report": "Clinical Decision Support",
}

# Build full entity inventory
entities = []
total_fields = 0
fields_with_descriptions = 0
fields_with_types = 0

for csv_file in data["csv_files"]:
    name = csv_file["name"]
    category = DOMAIN_MAP.get(name, "Unknown")
    fields = []
    for field in csv_file.get("fields", []):
        col_name = field.get("column_heading", field.get("name", ""))
        data_type = field.get("data_type", field.get("type", ""))
        description = field.get("description", "")
        
        has_desc = bool(description and description.strip())
        has_type = bool(data_type and data_type.strip())
        
        total_fields += 1
        if has_desc:
            fields_with_descriptions += 1
        if has_type:
            fields_with_types += 1
        
        fields.append({
            "name": col_name,
            "type": data_type,
            "description": description,
            "has_description": has_desc,
            "has_type": has_type,
        })
    
    entities.append({
        "entity_name": name,
        "file_name": csv_file.get("file_name", ""),
        "entity_description": csv_file.get("description", ""),
        "category": category,
        "field_count": len(fields),
        "fields": fields,
    })

# Full inventory
inventory = {
    "source": "cgm-aprima-electronic-health-information-export-user-guide.pdf",
    "extraction_method": "enrichment JSON derived from PDF via pdftotext + TypeScript parser",
    "product": "CGM APRIMA",
    "export_format": "CSV files in ZIP archive (plus USCDI XML, Complete Patient Chart PDF, images)",
    "total_entities": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "fields_with_types": fields_with_types,
    "description_coverage_pct": round(fields_with_descriptions / total_fields * 100, 1) if total_fields else 0,
    "type_coverage_pct": round(fields_with_types / total_fields * 100, 1) if total_fields else 0,
    "entities": entities,
}

with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Summary stats
summary = {
    "total_csv_files": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_descriptions,
    "fields_with_types": fields_with_types,
    "description_coverage_pct": inventory["description_coverage_pct"],
    "type_coverage_pct": inventory["type_coverage_pct"],
    "largest_entities": sorted(
        [{"name": e["entity_name"], "fields": e["field_count"], "category": e["category"]} for e in entities],
        key=lambda x: x["fields"],
        reverse=True,
    ),
}

with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
    json.dump(summary, f, indent=2)

# Category breakdown
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
    categories[cat]["entity_count"] += 1
    categories[cat]["field_count"] += e["field_count"]
    categories[cat]["entities"].append(e["entity_name"])

with open(OUTPUT_DIR / "category-breakdown.json", "w") as f:
    json.dump(categories, f, indent=2)

# Print summary
print(f"Total CSV files: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_descriptions} ({inventory['description_coverage_pct']}%)")
print(f"Fields with types: {fields_with_types} ({inventory['type_coverage_pct']}%)")
print()
print("Category breakdown:")
for cat, info in sorted(categories.items()):
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    for e in info["entities"]:
        print(f"    - {e}")
print()
print("Entities by size (descending):")
for item in summary["largest_entities"]:
    print(f"  {item['name']}: {item['fields']} fields ({item['category']})")

# Check for fields missing descriptions
print()
print("Fields missing descriptions:")
missing_count = 0
for e in entities:
    for f in e["fields"]:
        if not f["has_description"]:
            print(f"  {e['entity_name']}.{f['name']}")
            missing_count += 1
if missing_count == 0:
    print("  None — all fields have descriptions")
else:
    print(f"  Total: {missing_count} fields missing descriptions")
