#!/usr/bin/env python3
"""Parse the Export_data.pdf documentation and the enrichment JSON to produce
entity-inventory-full.json and entity-inventory-summary.json."""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
ENRICHMENT = os.path.join(BASE_DIR, "downloads", "enrichment", "export-schema.json")

with open(ENRICHMENT) as f:
    schema = json.load(f)

# Build entity inventory from xml_entities
entities = []
total_fields = 0
fields_with_desc = 0

for entity in schema["xml_entities"]:
    fields = []
    for field in entity["fields"]:
        has_desc = bool(field.get("description") and field["description"].strip())
        fields.append({
            "name": field["name"],
            "type": field["type"],
            "description": field.get("description", ""),
            "optional": field.get("optional"),
            "has_description": has_desc
        })
        total_fields += 1
        if has_desc:
            fields_with_desc += 1

    entities.append({
        "entity_name": entity["entity_name"],
        "context": entity.get("context", ""),
        "field_count": len(fields),
        "fields": fields,
        "has_examples": len(entity.get("examples", [])) > 0
    })

# Also add loinc_code as a sub-entity if present
# (Already included in xml_entities in the enrichment)

# Add enumerators as separate reference entities
enumerators = []
for enum in schema.get("enumerators", []):
    enumerators.append({
        "name": enum["name"],
        "value_count": len(enum["values"]),
        "values": enum["values"]
    })

# Build exported file types
exported_files = schema.get("exported_files", [])

# Full inventory
inventory = {
    "vendor": schema["vendor"],
    "product": schema["product"],
    "document_date": schema["document_date"],
    "export_format": schema["export_format"],
    "export_standard": schema["export_standard"],
    "source_file": "Export_data.pdf",
    "total_entities": len(entities),
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
    "entities": entities,
    "enumerators": enumerators,
    "exported_file_types": exported_files,
    "fax_export": schema.get("fax_export", {}),
    "directory_structure": schema.get("directory_structure", {})
}

with open(os.path.join(SCRIPT_DIR, "entity-inventory-full.json"), "w") as f:
    json.dump(inventory, f, indent=2)

# Summary
summary = {
    "vendor": inventory["vendor"],
    "product": inventory["product"],
    "document_date": inventory["document_date"],
    "export_format": inventory["export_format"],
    "total_entities": inventory["total_entities"],
    "total_fields": inventory["total_fields"],
    "fields_with_descriptions": inventory["fields_with_descriptions"],
    "description_coverage_pct": inventory["description_coverage_pct"],
    "entity_summary": [
        {
            "entity_name": e["entity_name"],
            "context": e["context"],
            "field_count": e["field_count"],
            "has_examples": e["has_examples"]
        }
        for e in entities
    ],
    "enumerator_summary": [
        {"name": en["name"], "value_count": en["value_count"]}
        for en in enumerators
    ],
    "exported_file_type_count": len(exported_files),
    "notes": [
        "C-CDA component (account_ccda.xml) defers to HL7 C-CDA 2.1 standard - no product-specific field documentation",
        "Proprietary XML sidecars document 7 entities with 71 fields total",
        "All 71 fields have descriptions (100% coverage)",
        "2 enumerators with 32 total values documented",
        "Fax inbox/outbox metadata included with 20 fields across 2 entities"
    ]
}

with open(os.path.join(SCRIPT_DIR, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

# Print summary stats
print(f"Entities: {inventory['total_entities']}")
print(f"Total fields: {inventory['total_fields']}")
print(f"Fields with descriptions: {inventory['fields_with_descriptions']} ({inventory['description_coverage_pct']}%)")
print(f"Enumerators: {len(enumerators)} with {sum(e['value_count'] for e in enumerators)} values")
print(f"Exported file types: {len(exported_files)}")
print()
for e in entities:
    print(f"  {e['entity_name']}: {e['field_count']} fields (context: {e['context']})")
