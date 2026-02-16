#!/usr/bin/env python3
"""Generate entity-inventory-full.json and entity-inventory-summary.json.

Since StrateqEHR provides NO data dictionary — just a statement that the
export is C-CDA per encounter plus attachments — we document exactly that:
there are zero enumerable entities/fields from the vendor's documentation.
"""

import json

# The vendor provides no data dictionary. The only information is that
# the export contains C-CDA documents and attached files.
inventory_full = {
    "product": "StrateqEHR",
    "version": "5",
    "source": "downloads/Strateq-Export.pdf",
    "extraction_notes": (
        "The vendor's EHI export documentation is a single-page PDF with 6 sentences. "
        "It contains no data dictionary, no entity/table definitions, no field definitions, "
        "no schemas, and no sample data. The export is described as a ZIP of per-encounter "
        "C-CDA documents and attached files (PDFs, images). No specific C-CDA sections, "
        "templates, or data elements are enumerated."
    ),
    "entities": [],
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "inferred_export_components": [
        {
            "name": "C-CDA Documents",
            "description": "Per-encounter C-CDA clinical documents in ZIP archives",
            "format": "C-CDA XML (zipped)",
            "fields_documented": 0,
            "notes": "No specific C-CDA document types, sections, or templates are identified",
        },
        {
            "name": "Attached Files",
            "description": "Files attached to the patient's chart",
            "format": "PDF, images (unspecified types)",
            "fields_documented": 0,
            "notes": "No details on what types of attachments are included",
        },
    ],
}

summary = {
    "product": "StrateqEHR",
    "version": "5",
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "pct_fields_with_descriptions": "N/A",
    "fields_with_types": 0,
    "pct_fields_with_types": "N/A",
    "categories": [],
    "category_breakdown": "No categories — no data dictionary provided",
    "documentation_quality": "None — 6 sentences, 3 of which define common file formats",
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory_full, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Generated entity-inventory-full.json and entity-inventory-summary.json")
print(f"Total entities: {inventory_full['total_entities']}")
print(f"Total fields: {inventory_full['total_fields']}")
