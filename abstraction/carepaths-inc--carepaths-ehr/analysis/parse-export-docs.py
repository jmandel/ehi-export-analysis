#!/usr/bin/env python3
"""Parse CarePaths B.10 EHI Export documentation page and extract export file categories."""

import json
from html.parser import HTMLParser

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth == 0:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)

with open('../downloads/b10-export-format.html') as f:
    html_content = f.read()

extractor = ContentExtractor()
extractor.feed(html_content)
page_text = '\n'.join(extractor.text_parts)

# The export documentation lists 7 file categories
export_files = [
    {
        "id": 1,
        "name": "CCD (Continuity of Care Document)",
        "format": "XML",
        "naming_scheme": "cda_PATIENT_NAME.xml",
        "description": "CCD (Continuity of Care Document) in xml format",
        "count_per_patient": "1",
        "data_type": "clinical_summary"
    },
    {
        "id": 2,
        "name": "Accounting Statement",
        "format": "PDF",
        "naming_scheme": "PATIENT_ID_Statements_asOfDate.pdf",
        "description": "Accounting Statement listing Patient's accounting transactions",
        "count_per_patient": "1",
        "data_type": "billing"
    },
    {
        "id": 3,
        "name": "Messaging History",
        "format": "TXT",
        "naming_scheme": "PATIENT_ID_Message_History_asOfDate.txt",
        "description": "Messaging History file of messages sent/received by Patient",
        "count_per_patient": "1",
        "data_type": "communications"
    },
    {
        "id": 4,
        "name": "Patient Charts",
        "format": "PDF",
        "naming_scheme": "PATIENT_ID_Chart_Year.pdf",
        "description": "Patient Charts documenting completed service documents grouped by year",
        "count_per_patient": "multiple (one per year)",
        "data_type": "clinical_documents"
    },
    {
        "id": 5,
        "name": "Audit Logs",
        "format": "unspecified",
        "naming_scheme": "unspecified",
        "description": "Audit Logs related to changes made to patient chart/account",
        "count_per_patient": "unspecified",
        "data_type": "audit"
    },
    {
        "id": 6,
        "name": "Appointment History",
        "format": "unspecified",
        "naming_scheme": "unspecified",
        "description": "Appointment History and Statuses for the patient",
        "count_per_patient": "unspecified",
        "data_type": "scheduling"
    },
    {
        "id": 7,
        "name": "Uploaded Documents/Images",
        "format": "original format",
        "naming_scheme": "original filename",
        "description": "Any other files included are document/image uploads from the patient's uploads on their EHR facesheet, in the same format as when uploaded",
        "count_per_patient": "variable",
        "data_type": "attachments"
    }
]

# Build entity inventory (best approximation - no data dictionary exists)
# Since there is no data dictionary, we document the file categories as "entities"
entity_inventory = {
    "source": "downloads/b10-export-format.html",
    "source_url": "https://carepaths.com/features/onc-certification/b10-export-format/",
    "parse_method": "HTML text extraction of B.10 EHI Export documentation page",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "export_file_categories": export_files,
    "total_file_categories": len(export_files),
    "total_fields_documented": 0,
    "field_descriptions": 0,
    "notes": [
        "No data dictionary, schema, or field-level documentation exists.",
        "Documentation consists solely of a single web page listing 7 file categories.",
        "No field names, types, relationships, or value sets are documented.",
        "3 of 7 categories specify format and naming scheme; 2 specify neither.",
        "The CCD is a standard C-CDA clinical summary, not a custom export.",
        "Accounting, charts, and messaging are rendered as PDF/TXT — not structured data.",
        "No sample data files are provided."
    ]
}

with open('entity-inventory-full.json', 'w') as f:
    json.dump(entity_inventory, f, indent=2)

# Summary
summary = {
    "product": "CarePaths EHR",
    "total_entities": len(export_files),
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_machine_readable_schema": False,
    "export_formats": ["XML (CCD/C-CDA)", "PDF", "TXT", "original upload format"],
    "structured_data_formats": ["XML (CCD only)"],
    "unstructured_data_formats": ["PDF (accounting, charts)", "TXT (messaging)"],
    "categories": {
        "clinical_summary": {"count": 1, "files": ["CCD XML"]},
        "billing": {"count": 1, "files": ["Accounting Statement PDF"]},
        "communications": {"count": 1, "files": ["Messaging History TXT"]},
        "clinical_documents": {"count": 1, "files": ["Patient Charts PDF"]},
        "audit": {"count": 1, "files": ["Audit Logs"]},
        "scheduling": {"count": 1, "files": ["Appointment History"]},
        "attachments": {"count": 1, "files": ["Uploaded Documents/Images"]}
    },
    "documentation_assessment": {
        "total_documentation_pages": 1,
        "total_words_in_documentation": len(page_text.split()),
        "detail_level": "minimal",
        "provides_field_names": False,
        "provides_field_types": False,
        "provides_field_descriptions": False,
        "provides_relationships": False,
        "provides_value_sets": False,
        "developer_usability": "A developer could not build an import from this documentation alone. No field-level detail, no schemas, no sample data."
    }
}

with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== CarePaths EHI Export Documentation Analysis ===")
print(f"Total file categories in export: {len(export_files)}")
print(f"Total fields documented: 0 (no data dictionary)")
print(f"Documentation word count: ~{len(page_text.split())}")
print(f"Formats: XML (CCD), PDF, TXT, original uploads")
print(f"Data dictionary: None")
print(f"Sample data: None")
print(f"Machine-readable schema: None")
print()
for f in export_files:
    print(f"  {f['id']}. {f['name']} ({f['format']}) — {f['description']}")
