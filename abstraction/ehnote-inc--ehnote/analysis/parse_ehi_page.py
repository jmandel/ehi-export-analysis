"""Parse the EHNOTE EHI export HTML page and extract all structured information.
Produces entity-inventory-full.json and entity-inventory-summary.json."""

import json
import re
from html.parser import HTMLParser


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, skipping scripts and styles."""
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            stripped = data.strip()
            if stripped:
                self.text.append(stripped)


with open('../downloads/ehi-export-page.html') as f:
    html_content = f.read()

parser = TextExtractor()
parser.feed(html_content)
full_text = '\n'.join(parser.text)

# The EHI export documentation describes two file types with loosely-described content.
# There is NO data dictionary, no field-level documentation, no schema.
# We extract what we can: the described export file categories and the vague field descriptions.

export_file_types = [
    {
        "file_type": "PDF Case Sheets",
        "format": "PDF",
        "naming_convention": "CaseSheet_{BranchId}P{PatientId}_A{AppointmentDate}.pdf",
        "example": "CaseSheet_731P518612_A2023-12-08.pdf",
        "described_content": [
            "Name of the clinic",
            "Patient demographics",
            "Chief complaints",
            "Review of systems",
            "Assessments",
            "Medications",
            "Other clinical data part of the appointment"
        ],
        "notes": "One PDF per appointment per patient. Contains rendered clinical history."
    },
    {
        "file_type": "Image Files",
        "format": "PNG/JPEG",
        "naming_convention": "{PatientName}_P{PatientId}_{Date}.{ext}",
        "example": "Alice_P2546_2023-01-08.PNG",
        "categories": [
            "Investigations",
            "Surgery consents",
            "Referrals",
            "Billings and Authorization files"
        ],
        "notes": "Native image files. Categories identified by special identification in the file."
    }
]

# Since there's no data dictionary, we construct an inventory of what
# the documentation claims is in the export, at the highest level.
# These are NOT database entities—they are described output categories.

entities = [
    {
        "entity_name": "CaseSheet (PDF)",
        "category": "Clinical",
        "format": "PDF",
        "fields": [
            {"name": "Clinic name", "type": "text", "description": "Name of the clinic"},
            {"name": "Patient demographics", "type": "text", "description": "Patient demographic information (unspecified fields)"},
            {"name": "Chief complaints", "type": "text", "description": "Patient's chief complaints for the visit"},
            {"name": "Review of systems", "type": "text", "description": "Review of systems findings"},
            {"name": "Assessments", "type": "text", "description": "Clinical assessments/diagnoses"},
            {"name": "Medications", "type": "text", "description": "Medication information"},
            {"name": "Other clinical data", "type": "text", "description": "Other clinical data part of the appointment (unspecified)"}
        ],
        "notes": "Fields are described only at category level, not at individual field level. All rendered as unstructured PDF text."
    },
    {
        "entity_name": "Investigations (Image)",
        "category": "Clinical",
        "format": "PNG/JPEG",
        "fields": [
            {"name": "Image content", "type": "image", "description": "Investigation-related image file"}
        ],
        "notes": "Image files with no structured metadata beyond filename identifiers."
    },
    {
        "entity_name": "Surgery Consents (Image)",
        "category": "Clinical",
        "format": "PNG/JPEG",
        "fields": [
            {"name": "Image content", "type": "image", "description": "Surgery consent document as image"}
        ],
        "notes": "Image files with no structured metadata beyond filename identifiers."
    },
    {
        "entity_name": "Referrals (Image)",
        "category": "Clinical",
        "format": "PNG/JPEG",
        "fields": [
            {"name": "Image content", "type": "image", "description": "Referral document as image"}
        ],
        "notes": "Image files with no structured metadata beyond filename identifiers."
    },
    {
        "entity_name": "Billings and Authorization (Image)",
        "category": "Billing",
        "format": "PNG/JPEG",
        "fields": [
            {"name": "Image content", "type": "image", "description": "Billing or authorization document as image"}
        ],
        "notes": "Image files with no structured metadata. Unclear what billing data this actually contains."
    }
]

# Build full inventory
inventory_full = {
    "product": "EHNOTE",
    "vendor": "EHNOTE, INC",
    "source": "downloads/ehi-export-page.html",
    "source_url": "https://ehnote.com/certification/ehi-export",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "export_format": "PDF and image files (PNG/JPEG)",
    "export_file_types": export_file_types,
    "entities": entities,
    "total_entities": len(entities),
    "total_fields": sum(len(e["fields"]) for e in entities),
    "fields_with_descriptions": sum(
        1 for e in entities for f in e["fields"] if f.get("description")
    ),
    "fields_with_types": sum(
        1 for e in entities for f in e["fields"] if f.get("type")
    ),
    "notes": (
        "EHNOTE provides NO data dictionary, NO schema, and NO structured export format. "
        "The 'entities' listed here are reconstructed from the documentation's description of "
        "exported file categories. The 7 'fields' for CaseSheet PDFs are broad content categories "
        "(e.g., 'Patient demographics', 'Medications'), NOT individual database fields. "
        "The documentation explicitly states: 'There is no one size fits all set of fields in "
        "the software because of the extensive customization that is possible.'"
    )
}

# Summary
summary = {
    "product": "EHNOTE",
    "vendor": "EHNOTE, INC",
    "total_entities": len(entities),
    "total_fields": sum(len(e["fields"]) for e in entities),
    "fields_with_descriptions": sum(
        1 for e in entities for f in e["fields"] if f.get("description")
    ),
    "pct_fields_with_descriptions": "100% (but descriptions are vague category-level labels, not field-level definitions)",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "export_format": "PDF and image files (PNG/JPEG)",
    "categories": {
        "Clinical": {
            "entity_count": 4,
            "field_count": 10,
            "entities": ["CaseSheet (PDF)", "Investigations (Image)", "Surgery Consents (Image)", "Referrals (Image)"]
        },
        "Billing": {
            "entity_count": 1,
            "field_count": 1,
            "entities": ["Billings and Authorization (Image)"]
        }
    },
    "documentation_word_count": len(full_text.split()),
    "key_limitations": [
        "No structured data format — all exports are rendered PDFs or raw images",
        "No data dictionary or field-level documentation",
        "No machine-readable schema",
        "No sample export files provided",
        "Documentation explicitly acknowledges lack of standardized field definitions",
        "Export is per-appointment, not comprehensive patient record dump"
    ]
}

with open('entity-inventory-full.json', 'w') as f:
    json.dump(inventory_full, f, indent=2)

with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("Generated entity-inventory-full.json and entity-inventory-summary.json")
print(f"Entities: {summary['total_entities']}")
print(f"Fields: {summary['total_fields']}")
print(f"Documentation word count: {summary['documentation_word_count']}")
