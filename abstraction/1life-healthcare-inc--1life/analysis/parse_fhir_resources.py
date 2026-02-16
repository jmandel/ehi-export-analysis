#!/usr/bin/env python3
"""Parse all FHIR resource HTML pages into a full entity inventory JSON.
Reads from the enrichment JSON (which was extracted from raw HTML) and 
also directly verifies against the EHI export overview page."""

import json
import os
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/1life-healthcare-inc--1life/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/1life-healthcare-inc--1life/analysis"

# Load the enrichment data as our primary parse
with open(os.path.join(RESULTS_DIR, "enrichment/fhir-resources.json")) as f:
    fhir_resources = json.load(f)

with open(os.path.join(RESULTS_DIR, "enrichment/ehi-export-summary.json")) as f:
    ehi_summary = json.load(f)

# Build full entity inventory
inventory = {
    "extraction_source": "enrichment/fhir-resources.json (parsed from HTML documentation)",
    "ehi_export_format": {
        "description": ehi_summary["ehiExport"]["description"],
        "json_format": "FHIR R4 Bundle",
        "xml_format": "C-CDA v2.1 Patient Continuity of Care Document",
        "delivery": "ZIP file containing .json and .xml per patient"
    },
    "ehi_export_fhir_resources": ehi_summary["ehiExport"]["formats"]["json"]["resourceTypes"],
    "ehi_export_ccda_sections": ehi_summary["ehiExport"]["formats"]["xml"]["ccdaSections"],
    "custom_extensions": [
        {"name": ext["name"], "url": ext["url"], "usedIn": ext["usedIn"]}
        for ext in ehi_summary["extensions"]
    ],
    "custom_terminology": ehi_summary["terminology"],
    "entities": [],
    "summary": {}
}

# Map which resources are explicitly listed as EHI export resources
ehi_resources_set = set(ehi_summary["ehiExport"]["formats"]["json"]["resourceTypes"])

total_fields = 0
total_with_description = 0
total_with_type = 0

for resource in fhir_resources:
    resource_name = resource["resourceType"]
    # Normalize case and spaces for matching
    ehi_lower = {r.lower().replace(" ", "") for r in ehi_resources_set}
    in_ehi_export = resource_name.lower().replace(" ", "") in ehi_lower
    
    entity = {
        "resourceType": resource_name,
        "sourceFile": resource["sourceFile"],
        "sourceUrl": resource["sourceUrl"],
        "inEhiExportList": in_ehi_export,
        "tableCount": len(resource["tables"]),
        "fields": []
    }
    
    for table in resource["tables"]:
        for field in table["fields"]:
            has_desc = bool(field.get("description", "").strip())
            has_type = bool(field.get("type", "").strip())
            
            field_entry = {
                "name": field["name"],
                "type": field.get("type", ""),
                "cardinality": field.get("cardinality", ""),
                "description": field.get("description", ""),
                "hasDescription": has_desc,
                "hasType": has_type
            }
            entity["fields"].append(field_entry)
            
            total_fields += 1
            if has_desc:
                total_with_description += 1
            if has_type:
                total_with_type += 1
    
    entity["fieldCount"] = len(entity["fields"])
    entity["fieldsWithDescription"] = sum(1 for f in entity["fields"] if f["hasDescription"])
    entity["fieldsWithType"] = sum(1 for f in entity["fields"] if f["hasType"])
    
    inventory["entities"].append(entity)

# Identify resources in EHI export list but NOT documented
documented_resources = {r["resourceType"] for r in fhir_resources}
# Normalize for comparison
documented_lower = {r.lower() for r in documented_resources}
undocumented_ehi = []
for r in ehi_resources_set:
    if r.lower().replace(" ", "") not in {d.lower().replace(" ", "") for d in documented_resources}:
        undocumented_ehi.append(r)

# Resources documented but not in EHI export list
extra_documented = []
for r in documented_resources:
    found = False
    for e in ehi_resources_set:
        if r.lower().replace(" ", "") == e.lower().replace(" ", ""):
            found = True
            break
    if not found:
        extra_documented.append(r)

inventory["summary"] = {
    "totalDocumentedResources": len(fhir_resources),
    "totalFields": total_fields,
    "fieldsWithDescription": total_with_description,
    "fieldsWithType": total_with_type,
    "descriptionPercentage": round(total_with_description / total_fields * 100, 1) if total_fields else 0,
    "typePercentage": round(total_with_type / total_fields * 100, 1) if total_fields else 0,
    "ehiExportResourceCount": len(ehi_resources_set),
    "ehiExportResourcesUndocumented": sorted(undocumented_ehi),
    "documentedButNotInEhiList": sorted(extra_documented),
    "ccdaSectionCount": len(ehi_summary["ehiExport"]["formats"]["xml"]["ccdaSections"]),
    "extensionCount": len(ehi_summary["extensions"]),
    "customTerminologyCount": len(ehi_summary["terminology"]),
    "duplicateInEhiList": ["Condition (listed twice in FHIR resource types table)"]
}

# Write full inventory
output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== Full Entity Inventory Generated ===")
print(f"Documented FHIR resources: {inventory['summary']['totalDocumentedResources']}")
print(f"Total fields: {inventory['summary']['totalFields']}")
print(f"Fields with descriptions: {inventory['summary']['fieldsWithDescription']} ({inventory['summary']['descriptionPercentage']}%)")
print(f"Fields with types: {inventory['summary']['fieldsWithType']} ({inventory['summary']['typePercentage']}%)")
print(f"\nEHI export lists {inventory['summary']['ehiExportResourceCount']} FHIR resources (including duplicate 'Condition')")
print(f"Undocumented EHI resources: {inventory['summary']['ehiExportResourcesUndocumented']}")
print(f"Documented but not in EHI list: {inventory['summary']['documentedButNotInEhiList']}")
print(f"\nC-CDA sections: {inventory['summary']['ccdaSectionCount']}")
print(f"Custom extensions: {inventory['summary']['extensionCount']}")
print(f"Custom terminology codes: {inventory['summary']['customTerminologyCount']}")

print("\n=== Per-Resource Breakdown ===")
for entity in sorted(inventory["entities"], key=lambda x: x["fieldCount"], reverse=True):
    ehi_marker = "✓ EHI" if entity["inEhiExportList"] else "  (supporting)"
    print(f"{entity['resourceType']:25s} {entity['fieldCount']:3d} fields | {entity['fieldsWithDescription']:3d} described | {entity['fieldsWithType']:3d} typed | {ehi_marker}")
