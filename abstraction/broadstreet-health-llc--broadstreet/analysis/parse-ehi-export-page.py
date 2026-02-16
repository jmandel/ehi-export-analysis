#!/usr/bin/env python3
"""
Parse the BroadStreet EHI Export HTML page to extract structured information.
Produces entity-inventory-full.json and entity-inventory-summary.json.
"""

import json
import re
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent / "downloads"
ANALYSIS = Path(__file__).parent

html_content = (DOWNLOADS / "ehi-export-page-rendered.html").read_text()

# --- Parse FHIR resources listed on the EHI export page ---
# Resources are listed between "such as:" and "Usage in BroadStreet"
fhir_list_start = html_content.find('such as:')
fhir_list_end = html_content.find('Usage in BroadStreet Health', fhir_list_start)
fhir_section = html_content[fhir_list_start:fhir_list_end]

fhir_resources = []
for match in re.finditer(r'<li><strong>([\w]+):</strong>\s*(.*?)</li>', fhir_section):
    name = match.group(1).strip()
    desc = re.sub(r'<[^>]+>', '', match.group(2)).strip().rstrip('.')
    fhir_resources.append({"name": name, "description": desc})

# --- Parse BroadStreet Notes (HTML) field structure ---
notes_start = html_content.find('id="broadstreet-notes-html"')
notes_section = html_content[notes_start:]
notes_fields = []
current_section = None

for match in re.finditer(r'<h3[^>]*>.*?</a>(.*?)</h3>|<li><strong>(.*?)</strong>:\s*(.*?)</li>', notes_section, re.DOTALL):
    if match.group(1):
        current_section = re.sub(r'<[^>]+>', '', match.group(1)).strip()
    elif match.group(2):
        field_name = match.group(2).strip()
        field_desc = re.sub(r'<[^>]+>', '', match.group(3)).strip().rstrip('.')
        notes_fields.append({
            "name": field_name,
            "section": current_section,
            "description": field_desc,
            "type": "string"
        })

# Capture text-only sections
for section_name in ["Treatment Review", "Additional Notes"]:
    pattern = rf'{section_name}</h3>\s*<ul><li>((?:(?!<strong>).)*?)</li>'
    m = re.search(pattern, notes_section, re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if text and '<strong>' not in m.group(1):
            notes_fields.append({
                "name": f"{section_name} Content",
                "section": section_name,
                "description": text,
                "type": "string"
            })

# --- Build full inventory ---
entities = []

entities.append({
    "entity_name": "CDA 2.1 Document",
    "format": "CDA 2.1",
    "category": "Clinical Document",
    "description": "Patient data as CDA 2.1 documents. No BroadStreet-specific sections or fields documented.",
    "fields": [
        {"name": "Header", "description": "Metadata: patient, author, document type", "type": "CDA Header"},
        {"name": "Body", "description": "Clinical sections with entries for diagnoses, observations, medications", "type": "CDA Body"}
    ],
    "field_count": 2,
    "fields_with_descriptions": 2,
    "note": "Only generic CDA structure described. No product-specific fields."
})

for res in fhir_resources:
    entities.append({
        "entity_name": f"FHIR {res['name']}",
        "format": "FHIR R4",
        "category": "FHIR Resource",
        "description": res["description"],
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "note": "No field-level detail. Refers to standard FHIR R4 / US Core profiles."
    })

notes_entity = {
    "entity_name": "BroadStreet Notes (HTML)",
    "format": "HTML",
    "category": "Clinical Notes",
    "description": "Clinical notes exported as HTML with sections for physician info, visit details, vitals, assessment, and signatures.",
    "fields": notes_fields,
    "field_count": len(notes_fields),
    "fields_with_descriptions": sum(1 for f in notes_fields if f.get("description")),
    "note": "Only product-specific field documentation. No data types, constraints, or value sets."
}
entities.append(notes_entity)

inventory = {
    "product": "BroadStreet",
    "version": "1",
    "source_file": "downloads/ehi-export-page-rendered.html",
    "extraction_notes": "CDA and FHIR sections describe standards generically. Only the Notes (HTML) section provides product-specific field structure.",
    "entities": entities
}

(ANALYSIS / "entity-inventory-full.json").write_text(json.dumps(inventory, indent=2))

# --- Summary ---
total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)
total_described = sum(e["fields_with_descriptions"] for e in entities)
fhir_count = sum(1 for e in entities if e["format"] == "FHIR R4")

summary = {
    "product": "BroadStreet",
    "total_entities": total_entities,
    "total_fields_documented": total_fields,
    "fields_with_descriptions": total_described,
    "description_pct": round(total_described / total_fields * 100, 1) if total_fields > 0 else 0,
    "breakdown_by_format": {
        "CDA 2.1": {"entities": 1, "fields": 2, "note": "Generic CDA structure only"},
        "FHIR R4": {"entities": fhir_count, "fields": 0, "note": "Resource names only, no field-level docs"},
        "HTML Notes": {"entities": 1, "fields": len(notes_fields), "note": "Only product-specific field docs"}
    },
    "fhir_resources_listed": [r["name"] for r in fhir_resources],
    "notes_sections": sorted(set(f["section"] for f in notes_fields if f.get("section"))),
    "notes_fields": [f["name"] for f in notes_fields]
}

(ANALYSIS / "entity-inventory-summary.json").write_text(json.dumps(summary, indent=2))

print(f"Entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {total_described}")
print(f"FHIR resources: {fhir_count} — {', '.join(r['name'] for r in fhir_resources)}")
print(f"Notes fields: {len(notes_fields)} — {', '.join(f['name'] for f in notes_fields)}")
