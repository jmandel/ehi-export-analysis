#!/usr/bin/env python3
"""Parse all SmartEMR HTML artifacts and produce entity-inventory-full.json and summary."""

import json
import os
from pathlib import Path

DOWNLOADS = Path("../downloads")
ENRICHMENT = DOWNLOADS / "enrichment"

# Load the enrichment data models (these were parsed from the HTML import spec pages)
with open(ENRICHMENT / "smartemr-data-models.json") as f:
    data_models = json.load(f)

# Load the EHI export structure  
with open(ENRICHMENT / "smartemr-ehi-export.json") as f:
    ehi_export = json.load(f)

# Build entity-inventory-full.json
# The only structured data specs available are the import specifications
# The EHI export itself (CDA + document repository) has NO data dictionary
entities = []

for model in data_models:
    entity = {
        "entity_name": model["page"],
        "title": model["title"],
        "source": f"{model['sourceFile']}",
        "category": model["category"],
        "description": model.get("description", ""),
        "is_export_spec": False,  # These are import specs, not export specs
        "is_import_spec": True,
        "field_count": len(model.get("fields", [])),
        "fields": []
    }
    for field in model.get("fields", []):
        entity["fields"].append({
            "number": field.get("number"),
            "name": field.get("name", ""),
            "description": field.get("description", ""),
            "data_type": field.get("dataType", ""),
            "max_length": field.get("maxLength", ""),
            "required": field.get("required", False),
            "validation_rule": field.get("validationRule", ""),
            "has_description": bool(field.get("description", "").strip() and field.get("description", "").strip() != "—")
        })
    entities.append(entity)

# Add the EHI export entity (CDA + document repository) - no field-level detail
entities.append({
    "entity_name": "ehi-export-cda",
    "title": "EHI Export - CDA Clinical Data",
    "source": "electronic-health-information-export-b10.html",
    "category": "ehi-export",
    "description": ehi_export.get("description", ""),
    "is_export_spec": True,
    "is_import_spec": False,
    "field_count": 0,
    "fields": [],
    "export_format": "CDA (Clinical Document Architecture)",
    "notes": "No data dictionary or field-level specification provided. Export format is CDA but no sections, templates, or data elements are documented."
})

entities.append({
    "entity_name": "ehi-export-document-repository",
    "title": "EHI Export - Document Repository",
    "source": "electronic-health-information-export-b10.html",
    "category": "ehi-export",
    "description": ehi_export.get("documentRepository", {}).get("description", ""),
    "is_export_spec": True,
    "is_import_spec": False,
    "field_count": 0,
    "fields": [],
    "export_format": "PDF, JPG, PNG files in patient-organized folders",
    "notes": "Document repository export with folder-based organization by patient chart ID. No field-level metadata documented."
})

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

# Compute summary
total_fields = sum(e["field_count"] for e in entities)
fields_with_desc = sum(
    1 for e in entities for field in e["fields"] if field.get("has_description")
)
import_spec_entities = [e for e in entities if e["is_import_spec"]]
export_spec_entities = [e for e in entities if e["is_export_spec"]]

summary = {
    "total_entities": len(entities),
    "import_spec_entities": len(import_spec_entities),
    "export_spec_entities": len(export_spec_entities),
    "total_fields_documented": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_without_descriptions": total_fields - fields_with_desc,
    "description_percentage": round(fields_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
    "export_data_dictionary_exists": False,
    "export_formats": ["CDA (Clinical Document Architecture)", "PDF/JPG/PNG (Document Repository)"],
    "export_mechanisms": {
        "single_patient": True,
        "bulk_all_patients": True,
        "api_access": False,
        "scheduled_export": True
    },
    "entities_by_category": {},
    "entity_summary": []
}

for e in entities:
    cat = e["category"]
    if cat not in summary["entities_by_category"]:
        summary["entities_by_category"][cat] = {"count": 0, "total_fields": 0}
    summary["entities_by_category"][cat]["count"] += 1
    summary["entities_by_category"][cat]["total_fields"] += e["field_count"]

for e in entities:
    summary["entity_summary"].append({
        "entity_name": e["entity_name"],
        "title": e["title"],
        "category": e["category"],
        "field_count": e["field_count"],
        "is_export_spec": e["is_export_spec"],
        "fields_with_descriptions": sum(1 for f in e["fields"] if f.get("has_description"))
    })

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== SmartEMR Artifact Analysis ===")
print(f"Total entities: {summary['total_entities']}")
print(f"  Import specs: {summary['import_spec_entities']}")
print(f"  Export specs: {summary['export_spec_entities']} (no field-level detail)")
print(f"Total fields documented (import specs only): {summary['total_fields_documented']}")
print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['description_percentage']}%)")
print(f"Export data dictionary exists: {summary['export_data_dictionary_exists']}")
print()
print("Entity breakdown:")
for e in summary["entity_summary"]:
    print(f"  {e['title']}: {e['field_count']} fields ({e['fields_with_descriptions']} described)")
