#!/usr/bin/env python3
"""Parse the MD Logic B10 Export Documentation HTML page.
Extracts all prose content, JSON schemas, and produces a complete inventory."""

import json
import re

HTML_PATH = "../../../results/md-logic-inc--md-logic-ehr/downloads/b10-export-documentation.html"
PATIENT_SCHEMA_PATH = "../../../results/md-logic-inc--md-logic-ehr/downloads/patient-manifest-schema.json"
BULK_SCHEMA_PATH = "../../../results/md-logic-inc--md-logic-ehr/downloads/bulk-export-manifest-schema.json"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Extract the main content div
match = re.search(
    r'<div class="field-item even"[^>]*property="content:encoded">(.*?)(?:</div>\s*</div>\s*</div>\s*</article>)',
    html, re.DOTALL
)
content = match.group(1) if match else ""

# Extract paragraphs (they have inline style)
paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
prose_texts = []
for p in paragraphs:
    clean = re.sub(r'<[^>]+>', '', p).strip()
    clean = re.sub(r'\s+', ' ', clean)
    if clean:
        prose_texts.append(clean)

print("=== PROSE CONTENT ===")
for i, t in enumerate(prose_texts, 1):
    print(f"{i}. {t}")

word_count = sum(len(t.split()) for t in prose_texts)
print(f"\nTotal prose paragraphs: {len(prose_texts)}")
print(f"Total prose word count: {word_count}")

# Load and analyze schemas
with open(PATIENT_SCHEMA_PATH) as f:
    patient_schema = json.load(f)

with open(BULK_SCHEMA_PATH) as f:
    bulk_schema = json.load(f)

print("\n=== PATIENT MANIFEST SCHEMA ===")
patient_props = patient_schema["items"]["properties"]
patient_required = patient_schema["items"]["required"]
print(f"Fields: {len(patient_props)}")
print(f"Required: {len(patient_required)}")
for name, spec in patient_props.items():
    examples = spec.get("examples", [])
    print(f"  {name}: type={spec.get('type','?')}, examples={examples}")

print("\n=== BULK EXPORT MANIFEST SCHEMA ===")
bulk_props = bulk_schema["items"]["properties"]
bulk_required = bulk_schema["items"]["required"]
print(f"Fields defined in properties: {len(bulk_props)}")
print(f"Fields listed as required: {len(bulk_required)}")
for name, spec in bulk_props.items():
    examples = spec.get("examples", [])
    print(f"  {name}: type={spec.get('type','?')}, examples={examples}")

# Check for mismatches
required_not_defined = [r for r in bulk_required if r not in bulk_props]
defined_not_required = [d for d in bulk_props if d not in bulk_required]
print(f"\nSchema bugs:")
print(f"  Required but not defined: {required_not_defined}")
print(f"  Defined but not required: {defined_not_required}")

# Also check patient schema
patient_req_not_def = [r for r in patient_required if r not in patient_props]
print(f"  Patient schema: required but not defined: {patient_req_not_def}")

# Build full entity inventory
inventory = {
    "source": "MD Logic B10 Export Documentation",
    "source_url": "https://www.mdlogic.com/solutions/b10-export-documentation",
    "source_file": "downloads/b10-export-documentation.html",
    "export_type": "document_dump_with_json_manifest",
    "prose_summary": {
        "total_paragraphs": len(prose_texts),
        "total_word_count": word_count,
        "paragraphs": prose_texts
    },
    "schemas": [
        {
            "name": "Per-Patient Manifest (manifest.json)",
            "description": "Index of documents in a patient's export ZIP file",
            "schema_file": "downloads/patient-manifest-schema.json",
            "type": "array",
            "fields": []
        },
        {
            "name": "Bulk Export Manifest",
            "description": "Index of all patients in a bulk export, with demographics and ZIP file references",
            "schema_file": "downloads/bulk-export-manifest-schema.json",
            "type": "array",
            "fields": []
        }
    ],
    "schema_bugs": {
        "patient_manifest": {
            "typo_in_field_name": "'Descripton' missing letter 'i' (should be 'Description')",
        },
        "bulk_manifest": {
            "required_not_in_properties": required_not_defined,
            "defined_not_in_required": defined_not_required,
            "gender_missing": "Gender is listed as required but has no property definition",
            "address_mismatch": "'Address' in required array but property is 'Address1'"
        },
        "both": {
            "placeholder_id": "$id is 'http://example.com/example.json' (placeholder)",
        }
    },
    "total_entities": 2,
    "total_fields": len(patient_props) + len(bulk_props),
    "fields_with_descriptions": 0,
    "fields_with_types": len(patient_props) + len(bulk_props),
    "sample_data_provided": False,
    "data_dictionary_provided": False,
    "native_database_model": False
}

# Populate field details
for name, spec in patient_props.items():
    inventory["schemas"][0]["fields"].append({
        "name": name,
        "type": spec.get("type", "unknown"),
        "description": spec.get("title", ""),
        "examples": spec.get("examples", []),
        "required": name in patient_required,
        "has_description": False  # title like "The Descripton Schema" is auto-generated, not a real description
    })

for name, spec in bulk_props.items():
    inventory["schemas"][1]["fields"].append({
        "name": name,
        "type": spec.get("type", "unknown"),
        "description": spec.get("title", ""),
        "examples": spec.get("examples", []),
        "required": name in bulk_required,
        "has_description": False  # auto-generated titles, not real descriptions
    })

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(f"\n=== SUMMARY ===")
print(f"Total schemas/entities: {inventory['total_entities']}")
print(f"Total fields across all schemas: {inventory['total_fields']}")
print(f"Fields with real descriptions: {inventory['fields_with_descriptions']}")
print(f"Data dictionary: {inventory['data_dictionary_provided']}")
print(f"Sample data: {inventory['sample_data_provided']}")
print(f"Native database model: {inventory['native_database_model']}")

print("\nSaved full-entity-inventory.json")

