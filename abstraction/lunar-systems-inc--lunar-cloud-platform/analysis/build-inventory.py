#!/usr/bin/env python3
"""
Parse the enrichment JSON files from the Lunar EHI Export PDF extraction
and produce a unified full-entity-inventory.json.

Input: enrichment/ehi-export-sections.json, enrichment/ehi-export-supplemental.json
Output: full-entity-inventory.json, summary-stats.json
"""

import json
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/lunar-systems-inc--lunar-cloud-platform/downloads/enrichment"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/lunar-systems-inc--lunar-cloud-platform/analysis"

# Load enrichment data
with open(os.path.join(RESULTS_DIR, "ehi-export-sections.json")) as f:
    sections_data = json.load(f)

with open(os.path.join(RESULTS_DIR, "ehi-export-supplemental.json")) as f:
    supplemental_data = json.load(f)

# Build inventory
inventory = {
    "document": sections_data["document"],
    "export_components": [],
    "summary": {}
}

# Component 1: C-CDA Sections
ccda_component = {
    "type": "C-CDA XML",
    "description": "Primary clinical data in Consolidated Clinical Document Architecture format",
    "cda_version": sections_data["document"]["ccdaVersion"],
    "sections": [],
    "total_sections": 0,
    "total_key_elements": 0,
    "elements_with_descriptions": 0
}

for section in sections_data["ccdaSections"]:
    sec_entry = {
        "name": section["name"],
        "description": section["description"],
        "templateId": section.get("templateId"),
        "loincCode": section.get("loincCode"),
        "loincDisplay": section.get("loincDisplay"),
        "hasExampleXml": section.get("hasExampleXml", False),
        "pageRange": section.get("pageRange"),
        "key_elements": []
    }
    for elem in section.get("keyElements", []):
        sec_entry["key_elements"].append({
            "element": elem["element"],
            "description": elem["description"],
            "has_description": bool(elem.get("description", "").strip())
        })
    
    ccda_component["sections"].append(sec_entry)
    ccda_component["total_key_elements"] += len(sec_entry["key_elements"])
    ccda_component["elements_with_descriptions"] += sum(
        1 for e in sec_entry["key_elements"] if e["has_description"]
    )

ccda_component["total_sections"] = len(ccda_component["sections"])
inventory["export_components"].append(ccda_component)

# Component 2: Supplemental CSV
csv_component = {
    "type": "Supplemental CSV",
    "description": supplemental_data["description"],
    "categories": [],
    "total_categories": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0
}

for cat in supplemental_data["categories"]:
    cat_entry = {
        "category": cat["category"],
        "fields": [],
        "field_count": len(cat["fields"])
    }
    for field in cat["fields"]:
        f_entry = {
            "field": field["field"],
            "description": field.get("description", ""),
            "dataType": field.get("dataType", ""),
            "has_description": bool(field.get("description", "").strip()),
            "has_type": bool(field.get("dataType", "").strip()),
            "is_opaque": field.get("dataType", "") in ("dict", "array")
        }
        cat_entry["fields"].append(f_entry)
    
    csv_component["categories"].append(cat_entry)
    csv_component["total_fields"] += cat_entry["field_count"]
    csv_component["fields_with_descriptions"] += sum(
        1 for f in cat_entry["fields"] if f["has_description"]
    )
    csv_component["fields_with_types"] += sum(
        1 for f in cat_entry["fields"] if f["has_type"]
    )

csv_component["total_categories"] = len(csv_component["categories"])
inventory["export_components"].append(csv_component)

# Summary statistics
total_documented_elements = (
    ccda_component["total_key_elements"] + csv_component["total_fields"]
)
total_with_descriptions = (
    ccda_component["elements_with_descriptions"] + csv_component["fields_with_descriptions"]
)
opaque_fields = sum(
    1 for cat in csv_component["categories"]
    for f in cat["fields"] if f["is_opaque"]
)

summary = {
    "ccda_sections": ccda_component["total_sections"],
    "ccda_key_elements": ccda_component["total_key_elements"],
    "ccda_elements_with_descriptions": ccda_component["elements_with_descriptions"],
    "supplemental_categories": csv_component["total_categories"],
    "supplemental_fields": csv_component["total_fields"],
    "supplemental_fields_with_descriptions": csv_component["fields_with_descriptions"],
    "supplemental_fields_with_types": csv_component["fields_with_types"],
    "supplemental_opaque_fields": opaque_fields,
    "total_documented_elements": total_documented_elements,
    "total_with_descriptions": total_with_descriptions,
    "description_coverage_pct": round(
        total_with_descriptions / total_documented_elements * 100, 1
    ) if total_documented_elements > 0 else 0,
    "export_format": "C-CDA XML + supplemental CSV",
    "model_type": "Standard-based projection (C-CDA) with supplemental native CSV",
    "sample_data_available": False,
    "bulk_export": True,
    "single_patient_export": True
}

inventory["summary"] = summary

# Write outputs
with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
    json.dump(inventory, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "summary-stats.json"), "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== Lunar EHI Export Inventory ===")
print(f"C-CDA Sections: {summary['ccda_sections']}")
print(f"C-CDA Key Elements: {summary['ccda_key_elements']}")
print(f"  with descriptions: {summary['ccda_elements_with_descriptions']}")
print(f"Supplemental CSV Categories: {summary['supplemental_categories']}")
print(f"Supplemental Fields: {summary['supplemental_fields']}")
print(f"  with descriptions: {summary['supplemental_fields_with_descriptions']}")
print(f"  with types: {summary['supplemental_fields_with_types']}")
print(f"  opaque (dict/array): {summary['supplemental_opaque_fields']}")
print(f"Total documented elements: {summary['total_documented_elements']}")
print(f"Description coverage: {summary['description_coverage_pct']}%")
print()

# Per-section breakdown
print("=== C-CDA Section Details ===")
for sec in ccda_component["sections"]:
    print(f"  {sec['name']}: {len(sec['key_elements'])} elements (pages {sec['pageRange']})")

print()
print("=== Supplemental CSV Details ===")
for cat in csv_component["categories"]:
    opaque = sum(1 for f in cat["fields"] if f["is_opaque"])
    print(f"  {cat['category']}: {cat['field_count']} fields ({opaque} opaque dict/array)")
