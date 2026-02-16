#!/usr/bin/env python3
"""
Parse all artifacts from Systemedx Clinical Navigator EHI export documentation.
Extracts structured content from the HTML export page and PDF disclosures.
"""

import json
import re
import os
from html.parser import HTMLParser

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')
OUTPUT_DIR = os.path.dirname(__file__)

# --- Parse dataExport.html ---

with open(os.path.join(DOWNLOADS, 'dataExport.html'), 'r') as f:
    html_content = f.read()

# Extract the substantive content from the HTML
# The documentation is in the <div class="services"> section
class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_services = False
        self.depth = 0
        self.text_parts = []
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'div' and 'services' in attrs_dict.get('class', ''):
            self.in_services = True
            self.depth = 0
        if self.in_services and tag == 'div':
            self.depth += 1
        self.current_tag = tag
            
    def handle_endtag(self, tag):
        if self.in_services and tag == 'div':
            self.depth -= 1
            if self.depth <= 0:
                self.in_services = False
                
    def handle_data(self, data):
        if self.in_services:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)

extractor = ContentExtractor()
extractor.feed(html_content)
doc_text = '\n'.join(extractor.text_parts)

# Count words in the actual documentation content
# Remove navigation/header/footer text
substantive_lines = [l for l in extractor.text_parts if l not in ['DataExport', '']]
word_count = sum(len(line.split()) for line in substantive_lines)

# Extract bullet points (the export format description)
bullet_items = []
for line in substantive_lines:
    if line.startswith('•') or line.startswith('-'):
        bullet_items.append(line.strip('•- ').strip())

# Build the artifact inventory
artifacts = {
    "collection_date": "2026-02-15",
    "product": "Systemedx Clinical Navigator",
    "version": "2024.12",
    "artifacts": [
        {
            "file": "dataExport.html",
            "type": "HTML page",
            "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, 'dataExport.html')),
            "description": "EHI export documentation page - the sole (b)(10) documentation artifact",
            "content_word_count": word_count,
            "substantive_content": doc_text,
            "bullet_items": bullet_items,
            "last_modified": "2022-05-05 (per HTTP Last-Modified header from prior agent)",
            "contains_data_dictionary": False,
            "contains_schema": False,
            "contains_sample_data": False,
            "contains_field_definitions": False,
            "downloadable_attachments": 0
        },
        {
            "file": "dataExport-screenshot.png",
            "type": "Screenshot",
            "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, 'dataExport-screenshot.png')),
            "description": "Full-page screenshot of the export documentation page"
        },
        {
            "file": "Mandatory-Disclosures-2022.pdf",
            "type": "PDF",
            "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, 'Mandatory-Disclosures-2022.pdf')),
            "pages": 2,
            "description": "ONC mandatory cost transparency disclosures listing fees for certified capabilities",
            "mentions_b10_export": False,
            "mentions_export_costs": False
        }
    ],
    "export_description": {
        "module_name": "CDAEXPORT (Data Export)",
        "export_modes": [
            "All Patients - full export with date range filter",
            "Select Patients - subset by manual selection or appointment date range",
            "Single Patient - single patient export"
        ],
        "export_formats": [
            "CDA XML files (demographics + 'distinct chart data')",
            "HTML files (human-readable CDA copies, named 'CDA.html')",
            "PDF documents (chart documents, organized by document type)"
        ],
        "folder_structure": "LastName_FirstName_DOB_PatientID",
        "data_elements_mentioned": ["patient demographics", "medications", "problems"],
        "data_elements_explicitly_missing": [
            "billing/claims data",
            "surgical pathway data",
            "lab results (not mentioned)",
            "allergies (not mentioned)",
            "vital signs (not mentioned)",
            "immunizations (not mentioned)",
            "orders (not mentioned)",
            "insurance data (not mentioned)",
            "patient portal messages (not mentioned)"
        ],
        "cda_template_specified": False,
        "sections_enumerated": False,
        "field_level_documentation": False
    }
}

with open(os.path.join(OUTPUT_DIR, 'artifact-analysis.json'), 'w') as f:
    json.dump(artifacts, f, indent=2)

print(f"Documentation word count: {word_count}")
print(f"Bullet items: {len(bullet_items)}")
print(f"Data elements explicitly mentioned: {len(artifacts['export_description']['data_elements_mentioned'])}")
print(f"Artifacts analyzed: {len(artifacts['artifacts'])}")
print(f"Saved to artifact-analysis.json")

# --- Generate entity inventory ---
# Since there is NO data dictionary, schema, or field-level documentation,
# we can only document what the vendor mentions at the highest level.

entity_inventory = {
    "source": "dataExport.html (https://www.systemedx.com/dataExport.html)",
    "extraction_method": "Manual extraction from ~150-word prose description; no structured data dictionary exists",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "note": "The vendor provides NO entity-level or field-level documentation. The export is described only in prose as producing 'CDA XML files' containing 'patient demographics and distinct chart data (medications, problems, etc.)' plus PDF chart documents. No tables, fields, types, value sets, or relationships are documented.",
    "mentioned_data_concepts": [
        {
            "concept": "Patient demographics",
            "format": "CDA XML",
            "fields_documented": 0,
            "evidence": "Mentioned in export page: 'Patient demographics and distinct chart data... are exported as CDA XML files'"
        },
        {
            "concept": "Medications",
            "format": "CDA XML",
            "fields_documented": 0,
            "evidence": "Mentioned parenthetically: '(medications, problems, etc.)'"
        },
        {
            "concept": "Problems",
            "format": "CDA XML",
            "fields_documented": 0,
            "evidence": "Mentioned parenthetically: '(medications, problems, etc.)'"
        },
        {
            "concept": "Chart documents",
            "format": "PDF",
            "fields_documented": 0,
            "evidence": "Mentioned: 'Patient chart documents are exported as PDF documents and stored in a main Documents folder'"
        }
    ]
}

with open(os.path.join(OUTPUT_DIR, 'entity-inventory-full.json'), 'w') as f:
    json.dump(entity_inventory, f, indent=2)

summary = {
    "product": "Systemedx Clinical Navigator",
    "version": "2024.12",
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "pct_fields_with_descriptions": "N/A",
    "categories": [],
    "data_dictionary_exists": False,
    "schema_exists": False,
    "sample_data_exists": False,
    "documentation_word_count": word_count,
    "mentioned_data_concepts_count": len(entity_inventory["mentioned_data_concepts"]),
    "export_format": "CDA XML + HTML + PDF",
    "notes": "No structured data dictionary or schema provided. Documentation consists of ~{} words of prose describing the export mechanism and listing 3 data concepts (demographics, medications, problems) plus PDF chart documents.".format(word_count)
}

with open(os.path.join(OUTPUT_DIR, 'entity-inventory-summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\nEntity inventory: {entity_inventory['total_entities']} entities, {entity_inventory['total_fields']} fields")
print(f"Mentioned data concepts: {len(entity_inventory['mentioned_data_concepts'])}")
print(f"Saved entity-inventory-full.json and entity-inventory-summary.json")
