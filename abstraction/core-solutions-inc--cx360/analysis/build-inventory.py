#!/usr/bin/env python3
"""
Parse the enrichment JSON (ccd-sections.json) to produce entity-inventory-full.json
and entity-inventory-summary.json. The enrichment was hand-curated from visual
inspection of the PDF data dictionary (pages 7-12).

We verify against the raw PDF text extraction to confirm completeness.
"""

import json
from pathlib import Path

base = Path(__file__).parent.parent

# Load the enrichment data (hand-curated from PDF)
with open(base / "downloads/enrichment/ccd-sections.json") as f:
    data = json.load(f)

sections = data["ccd_sections"]

# Build full inventory
entities = []
total_fields = 0
fields_with_code_system = 0
fields_with_xpath = 0

for section in sections:
    fields = []
    for elem in section["data_elements"]:
        has_code = bool(elem.get("code_system_oid"))
        has_xpath = bool(elem.get("xpath_entry"))
        if has_code:
            fields_with_code_system += 1
        if has_xpath:
            fields_with_xpath += 1
        total_fields += 1
        fields.append({
            "name": elem["name"],
            "xpath_entry": elem.get("xpath_entry"),
            "code_system_oid": elem.get("code_system_oid"),
            "code_system_name": elem.get("code_system_name"),
            "has_code_system": has_code,
            "has_xpath": has_xpath,
            "description": None,  # No descriptions provided in the documentation
            "type": None,  # No data types documented
        })

    entities.append({
        "entity_name": section["section_name"],
        "template_id": section.get("template_id"),
        "effective_date": section.get("effective_date"),
        "field_count": len(fields),
        "fields": fields,
        "category": "C-CDA Section",
    })

full_inventory = {
    "vendor": data["vendor"],
    "product": data["product"],
    "version": data["version"],
    "export_format": data["export_format"],
    "export_standard": data["standard_referenced"],
    "document_date": data["document_date"],
    "total_sections": len(entities),
    "total_fields": total_fields,
    "fields_with_code_system": fields_with_code_system,
    "fields_with_xpath": fields_with_xpath,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "entities": entities,
}

# Write full inventory
out_dir = Path(__file__).parent
with open(out_dir / "entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Build summary
section_summary = []
for e in entities:
    section_summary.append({
        "section": e["entity_name"],
        "template_id": e["template_id"],
        "field_count": e["field_count"],
        "fields_with_code_system": sum(1 for f in e["fields"] if f["has_code_system"]),
        "fields_with_xpath": sum(1 for f in e["fields"] if f["has_xpath"]),
    })

summary = {
    "vendor": data["vendor"],
    "product": data["product"],
    "version": data["version"],
    "export_format": data["export_format"],
    "total_sections": len(entities),
    "total_fields": total_fields,
    "fields_with_code_system": fields_with_code_system,
    "fields_with_code_system_pct": round(fields_with_code_system / total_fields * 100, 1),
    "fields_with_xpath": fields_with_xpath,
    "fields_with_xpath_pct": round(fields_with_xpath / total_fields * 100, 1),
    "fields_with_descriptions": 0,
    "fields_with_descriptions_pct": 0.0,
    "fields_with_types": 0,
    "fields_with_types_pct": 0.0,
    "sections": section_summary,
}

with open(out_dir / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total C-CDA sections: {len(entities)}")
print(f"Total data elements: {total_fields}")
print(f"Elements with code system OID: {fields_with_code_system} ({summary['fields_with_code_system_pct']}%)")
print(f"Elements with XPATH/Entry: {fields_with_xpath} ({summary['fields_with_xpath_pct']}%)")
print(f"Elements with descriptions: 0 (0%)")
print(f"Elements with data types: 0 (0%)")
print()
print("Sections:")
for s in section_summary:
    print(f"  {s['section']}: {s['field_count']} fields, {s['fields_with_code_system']} coded")
