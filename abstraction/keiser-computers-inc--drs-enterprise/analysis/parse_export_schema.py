#!/usr/bin/env python3
"""Parse the enrichment export-schema.json and produce full-entity-inventory.json
with verified counts and summary statistics."""

import json
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent.parent.parent / "results/keiser-computers-inc--drs-enterprise/downloads/enrichment/export-schema.json"
OUTPUT_DIR = Path(__file__).parent

with open(SCHEMA_PATH) as f:
    schema = json.load(f)

# Build full entity inventory
entities = []
total_fields = 0
fields_with_descriptions = 0
fields_with_types = 0

for entity in schema["xml_entities"]:
    fields = []
    for field in entity["fields"]:
        has_desc = bool(field.get("description", "").strip())
        has_type = bool(field.get("type", "").strip())
        fields_with_descriptions += int(has_desc)
        fields_with_types += int(has_type)
        total_fields += 1
        fields.append({
            "name": field["name"],
            "type": field.get("type", ""),
            "description": field.get("description", ""),
            "optional": field.get("optional", None),
            "has_description": has_desc,
            "has_type": has_type,
        })

    entities.append({
        "entity_name": entity["entity_name"],
        "context": entity.get("context", ""),
        "field_count": len(fields),
        "fields": fields,
        "has_examples": len(entity.get("examples", [])) > 0,
        "example_count": len(entity.get("examples", [])),
    })

# Enumerator summary
enumerators = []
total_enum_values = 0
for enum in schema.get("enumerators", []):
    values = [{"value": v["type"], "description": v.get("description", "")} for v in enum["values"]]
    total_enum_values += len(values)
    enumerators.append({
        "name": enum["name"],
        "value_count": len(values),
        "values": values,
    })

# Exported file types
exported_files = schema.get("exported_files", [])

inventory = {
    "vendor": schema["vendor"],
    "product": schema["product"],
    "document_date": schema["document_date"],
    "export_format": schema["export_format"],
    "summary": {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "fields_with_types": fields_with_types,
        "description_coverage_pct": round(100 * fields_with_descriptions / total_fields, 1) if total_fields > 0 else 0,
        "type_coverage_pct": round(100 * fields_with_types / total_fields, 1) if total_fields > 0 else 0,
        "total_enumerators": len(enumerators),
        "total_enum_values": total_enum_values,
        "exported_file_types": len(exported_files),
    },
    "entities": entities,
    "enumerators": enumerators,
    "exported_files": exported_files,
    "directory_structure": schema.get("directory_structure", {}),
    "fax_export": schema.get("fax_export", {}),
}

# Write full inventory
out_path = OUTPUT_DIR / "full-entity-inventory.json"
with open(out_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== Export Schema Summary ===")
print(f"Entities: {inventory['summary']['total_entities']}")
print(f"Total fields: {inventory['summary']['total_fields']}")
print(f"Fields with descriptions: {inventory['summary']['fields_with_descriptions']} ({inventory['summary']['description_coverage_pct']}%)")
print(f"Fields with types: {inventory['summary']['fields_with_types']} ({inventory['summary']['type_coverage_pct']}%)")
print(f"Enumerators: {inventory['summary']['total_enumerators']} ({inventory['summary']['total_enum_values']} values)")
print(f"Exported file types: {inventory['summary']['exported_file_types']}")
print()
print("=== Entity Breakdown ===")
for e in entities:
    optional_count = sum(1 for f in e["fields"] if f["optional"])
    required_count = sum(1 for f in e["fields"] if not f["optional"])
    print(f"  {e['entity_name']}: {e['field_count']} fields ({required_count} required, {optional_count} optional), examples: {e['has_examples']}")
print()
print("=== Enumerators ===")
for en in enumerators:
    print(f"  {en['name']}: {en['value_count']} values")

print(f"\nFull inventory written to: {out_path}")
