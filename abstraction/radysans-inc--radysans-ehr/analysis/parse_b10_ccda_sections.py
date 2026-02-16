#!/usr/bin/env python3
"""
Parse the B-10 documentation PDF to extract all C-CDA sections listed
and produce a structured inventory.
"""
import json
import subprocess

PDF_PATH = "../../../results/radysans-inc--radysans-ehr/downloads/B-10-Documentation.pdf"

result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Extract C-CDA section names (lines in all caps between the header and FHIR section)
lines = text.split('\n')
sections = []
in_sections = False
for line in lines:
    stripped = line.strip()
    if stripped == "Sections of EHI exported in CCDA :":
        in_sections = True
        continue
    if in_sections:
        if stripped.startswith("The specifications"):
            break
        if stripped and not stripped.startswith("170.315"):
            sections.append(stripped)

output = {
    "source_file": "B-10-Documentation.pdf",
    "pdf_pages": 1,
    "document_title": "Documentation for Export of Electronic Health Information — 170.315(b)(10)",
    "product": "Radysans EHR v 5.0",
    "creation_date": "2023-11-27",
    "export_formats": [
        {
            "format": "C-CDA",
            "description": "Bulk export of HL7 CCDA xml files compliant with USCDI v1",
            "sections": sections,
            "section_count": len(sections)
        },
        {
            "format": "FHIR R4",
            "description": "HL7 FHIR R4 with US Core STU 3.1.1 via Bulk Data export",
            "reference": "See 170.315(g)(10) documentation"
        }
    ],
    "capabilities": {
        "single_patient": True,
        "bulk_population": True
    },
    "data_dictionary": False,
    "field_level_documentation": False,
    "sample_data": False,
    "schema_files": False,
    "notes": [
        "Single-page document with no field-level detail",
        "References HL7 C-CDA spec for format details",
        "References G10 document for FHIR details",
        "No data dictionary or mapping to internal data model",
        "No documentation of what data is NOT included"
    ]
}

with open("b10_ccda_inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
