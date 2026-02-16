#!/usr/bin/env python3
"""Parse MD Logic EHI export documentation artifacts and produce inventory JSON files.

Reads:
  - downloads/patient-manifest-schema.json (per-patient manifest schema)
  - downloads/bulk-export-manifest-schema.json (bulk export manifest schema)
  - downloads/b10-export-documentation.html (full HTML page)

Produces:
  - analysis/entity-inventory-full.json
  - analysis/entity-inventory-summary.json
"""

import json
import os
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE, "downloads")
ANALYSIS = os.path.join(BASE, "analysis")


def load_json(path):
    with open(os.path.join(DOWNLOADS, path)) as f:
        return json.load(f)


def extract_fields_from_schema(schema, entity_name):
    """Extract field-level info from a JSON Schema items.properties block."""
    props = schema.get("items", {}).get("properties", {})
    required = set(schema.get("items", {}).get("required", []))
    fields = []
    for name, defn in props.items():
        fields.append({
            "name": name,
            "type": defn.get("type", "unknown"),
            "description": defn.get("title", ""),
            "required": name in required,
            "examples": defn.get("examples", []),
        })
    return fields


def extract_page_prose(html_path):
    """Extract the prose text from the B10 HTML page."""
    class ProseExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text_parts = []
            self.skip = False
            self.in_body = False

        def handle_starttag(self, tag, attrs):
            if tag == "body":
                self.in_body = True
            if tag in ("script", "style", "noscript"):
                self.skip = True

        def handle_endtag(self, tag):
            if tag in ("script", "style", "noscript"):
                self.skip = False

        def handle_data(self, data):
            if self.in_body and not self.skip:
                t = data.strip()
                if t:
                    self.text_parts.append(t)

    with open(html_path) as f:
        html = f.read()

    p = ProseExtractor()
    p.feed(html)
    return p.text_parts


# --- Parse schemas ---
patient_schema = load_json("patient-manifest-schema.json")
bulk_schema = load_json("bulk-export-manifest-schema.json")

patient_fields = extract_fields_from_schema(patient_schema, "per_patient_manifest")
bulk_fields = extract_fields_from_schema(bulk_schema, "bulk_export_manifest")

# --- Build entity inventory ---
entities = [
    {
        "entity_name": "per_patient_manifest",
        "vendor_category": "Export Manifest",
        "description": "JSON manifest inside each patient's ZIP file listing all exported documents with metadata",
        "source_file": "patient-manifest-schema.json",
        "field_count": len(patient_fields),
        "fields": patient_fields,
    },
    {
        "entity_name": "bulk_export_manifest",
        "vendor_category": "Export Manifest",
        "description": "Top-level JSON manifest for bulk (all-patient) export, mapping patient demographics to ZIP files",
        "source_file": "bulk-export-manifest-schema.json",
        "field_count": len(bulk_fields),
        "fields": bulk_fields,
    },
]

# Count stats
total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)
fields_with_desc = sum(
    1
    for e in entities
    for f in e["fields"]
    if f["description"] and f["description"] != ""
)
fields_with_examples = sum(
    1
    for e in entities
    for f in e["fields"]
    if f["examples"]
)

# Note schema bugs
schema_bugs = [
    "per_patient_manifest: 'Descripton' field has typo (missing 'i')",
    "bulk_export_manifest: 'required' array lists 'Address' but property is named 'Address1' (mismatch)",
    "bulk_export_manifest: 'Gender' is listed as required but has no property definition in 'properties'",
    "Both schemas use placeholder $id values (http://example.com/example.json)",
]

# --- Extract page content stats ---
html_path = os.path.join(DOWNLOADS, "b10-export-documentation.html")
with open(html_path) as f:
    html_size = len(f.read())

prose_parts = extract_page_prose(html_path)
# Filter out nav/footer/schema text to count just prose paragraphs
# The meaningful prose is about 3 paragraphs for individual + 2 for bulk
# We'll count words in the full body text
all_text = " ".join(prose_parts)
word_count = len(all_text.split())

# --- Write full inventory ---
full_inventory = {
    "product": "MD Logic EHR",
    "export_type": "document-centric ZIP export with JSON manifests",
    "export_format": "ZIP files containing documents (PDF, Word, CCDA, JPEG) + JSON manifest",
    "documentation_source": "https://www.mdlogic.com/solutions/b10-export-documentation",
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_examples": fields_with_examples,
    "schema_bugs": schema_bugs,
    "html_page_size_bytes": html_size,
    "entities": entities,
}

with open(os.path.join(ANALYSIS, "entity-inventory-full.json"), "w") as f:
    json.dump(full_inventory, f, indent=2)

# --- Write summary ---
summary = {
    "product": "MD Logic EHR",
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_examples": fields_with_examples,
    "pct_fields_with_descriptions": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "schema_bugs_count": len(schema_bugs),
    "html_page_size_bytes": html_size,
    "export_format": "ZIP (documents) + JSON manifest",
    "structured_clinical_data_exported": False,
    "data_dictionary_provided": False,
    "sample_data_provided": False,
    "categories": {
        "Export Manifest": {
            "entity_count": 2,
            "field_count": total_fields,
        }
    },
    "notes": [
        "No data dictionary exists — only two JSON schemas for manifest files",
        "Export is document-centric: ZIP of files (PDF/Word/JPEG/CCDA) per patient",
        "No structured clinical data export (medications, labs, vitals, allergies, etc.)",
        "No billing/financial data in export",
        "Bulk export requires contacting vendor support",
        f"Entire documentation is a single HTML page ({html_size} bytes) with ~{word_count} words of body text",
    ],
}

with open(os.path.join(ANALYSIS, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print(f"Entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc}")
print(f"Fields with examples: {fields_with_examples}")
print(f"Schema bugs: {len(schema_bugs)}")
print(f"HTML page size: {html_size} bytes")
print(f"Body text word count (approx): {word_count}")
print(f"\nOutput written to:")
print(f"  {os.path.join(ANALYSIS, 'entity-inventory-full.json')}")
print(f"  {os.path.join(ANALYSIS, 'entity-inventory-summary.json')}")
