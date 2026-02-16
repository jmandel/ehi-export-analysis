#!/usr/bin/env python3
"""Parse all EHI export artifacts for MedOne OneConnect and produce inventory files.

Since OneConnect has no data dictionary or schema, this script:
1. Extracts the full text of the EHI Export PDF
2. Extracts FHIR resource types from the FHIR API Specifications PDF
3. Parses the FHIR Valid URLs JSON
4. Produces entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import subprocess
import re
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')
ANALYSIS = os.path.dirname(__file__)

# 1. Extract EHI Export PDF text
ehi_text = subprocess.run(
    ['pdftotext', '-layout', os.path.join(DOWNLOADS, 'EHI-Export.pdf'), '-'],
    capture_output=True, text=True
).stdout.strip()

# 2. Extract FHIR API resource types from the specifications PDF
fhir_text = subprocess.run(
    ['pdftotext', '-layout', os.path.join(DOWNLOADS, 'FHIR-API-Specifications.pdf'), '-'],
    capture_output=True, text=True
).stdout

# Parse FHIR resource types from TOC
fhir_resources = []
for line in fhir_text.split('\n'):
    m = re.match(r'^Request\s*:\s*(.+?)\.{2,}', line)
    if m:
        name = m.group(1).strip()
        fhir_resources.append(name)

# 3. Parse FHIR Valid URLs JSON
with open(os.path.join(DOWNLOADS, 'FHIR_Valid_URLs.json')) as f:
    fhir_urls = json.load(f)

# Build entity inventory
# Since there's NO data dictionary, we document what we know:
# The export is C-CDA per encounter. C-CDA has standard sections.
# We can list the standard C-CDA sections as "probable entities" but
# there's no vendor-specific documentation to confirm which are populated.

ccda_standard_sections = [
    {"name": "Allergies and Intolerances", "loinc": "48765-2"},
    {"name": "Medications", "loinc": "10160-0"},
    {"name": "Problem List", "loinc": "11450-4"},
    {"name": "Procedures", "loinc": "47519-4"},
    {"name": "Results", "loinc": "30954-2"},
    {"name": "Vital Signs", "loinc": "8716-3"},
    {"name": "Immunizations", "loinc": "11369-6"},
    {"name": "Plan of Treatment", "loinc": "18776-5"},
    {"name": "Goals", "loinc": "61146-7"},
    {"name": "Social History", "loinc": "29762-2"},
    {"name": "Encounters", "loinc": "46240-8"},
    {"name": "Reason for Referral", "loinc": "42349-1"},
    {"name": "Functional Status", "loinc": "47420-5"},
    {"name": "Mental Status", "loinc": "10190-7"},
    {"name": "Assessment", "loinc": "51848-0"},
    {"name": "Medical Equipment", "loinc": "46264-8"},
]

inventory = {
    "product": "OneConnect",
    "vendor": "MedOne Healthcare Partners",
    "export_format": "C-CDA (ZIP archive, one C-CDA per encounter)",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "documentation_source": "EHI-Export.pdf (1 page, 6 sentences)",
    "ehi_export_pdf_text": ehi_text,
    "ehi_export_pdf_word_count": len(ehi_text.split()),
    "fhir_api_resource_types": fhir_resources,
    "fhir_api_resource_count": len(fhir_resources),
    "entities": [],
    "notes": [
        "No data dictionary exists. The export documentation is a single-page PDF with 6 sentences.",
        "Export format is C-CDA per encounter in a ZIP archive.",
        "Documentation explicitly states 'other files attached to the patient's chart will be added later (e.g. PDF and images)' — implying current export is incomplete.",
        "No field-level documentation, no schema, no sample data provided.",
        "C-CDA sections listed below are INFERRED from C-CDA standard — vendor does not specify which sections are populated."
    ],
    "inferred_ccda_sections": ccda_standard_sections
}

# Write full inventory
with open(os.path.join(ANALYSIS, 'entity-inventory-full.json'), 'w') as f:
    json.dump(inventory, f, indent=2)

# Build summary
summary = {
    "product": "OneConnect",
    "vendor": "MedOne Healthcare Partners",
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "pct_fields_described": "N/A",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "export_format": "C-CDA (ZIP archive)",
    "documentation_pages": 1,
    "documentation_word_count": len(ehi_text.split()),
    "fhir_api_resources_documented": len(fhir_resources),
    "fhir_api_resources_list": fhir_resources,
    "inferred_ccda_section_count": len(ccda_standard_sections),
    "artifacts_reviewed": [
        {
            "file": "EHI-Export.pdf",
            "size_bytes": 282272,
            "pages": 1,
            "description": "Entire (b)(10) EHI export documentation. 6 sentences. No data dictionary.",
            "informativeness": "low"
        },
        {
            "file": "FHIR-API-Specifications.pdf",
            "size_bytes": 1296059,
            "pages": 58,
            "description": "(g)(10) FHIR API documentation. Smart on FHIR OAuth2 + US Core resource access. Not (b)(10).",
            "informativeness": "contextual"
        },
        {
            "file": "FHIR_Valid_URLs.json",
            "size_bytes": 2235,
            "description": "FHIR Bundle with Endpoint and Organization resources. Infrastructure metadata.",
            "informativeness": "minimal"
        },
        {
            "file": "certifications-page-screenshot.png",
            "size_bytes": 366699,
            "description": "Screenshot of MedOne certifications page showing document links.",
            "informativeness": "contextual"
        }
    ]
}

with open(os.path.join(ANALYSIS, 'entity-inventory-summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

print(f"EHI Export PDF: {len(ehi_text.split())} words")
print(f"FHIR API Resources: {len(fhir_resources)}")
print(f"  {', '.join(fhir_resources)}")
print(f"Inferred C-CDA sections: {len(ccda_standard_sections)}")
print("Wrote entity-inventory-full.json and entity-inventory-summary.json")
