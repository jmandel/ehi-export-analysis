#!/usr/bin/env python3
"""
Extract and document all observable details from the Axiom EHI Export Instructions PDF.
Since there is no data dictionary or schema, this script documents what IS visible
in the screenshots and text of the 4-page PDF.
"""

import json
import subprocess
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/health-information-management-systems-llc--axiom"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/health-information-management-systems-llc--axiom/analysis"

pdf_path = os.path.join(RESULTS_DIR, "downloads", "Axiom-EHI-Export-Instructions.pdf")

# Extract PDF metadata
info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True)
text = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)

# Parse pdfinfo output
metadata = {}
for line in info.stdout.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Form types visible in the PDF screenshots (from page 2 dropdown and page 3 record list)
# These were read directly from the rendered PDF page images.
form_types_in_dropdown = [
    "Dynamic Form: AccountLogin",
    "Dynamic Form: Active Meds Test",
    "Dynamic Form: ADAD Test Form",
    "Dynamic Form: Adult ADHD Self-Report Scale (ASRS-v1...)",
    "Dynamic Form: Adult Brief Pscyhosocial Assessment - Dra...",
    "Dynamic Form: Adult Brief Pscyhosocial Assessment - Dra...",
    "Dynamic Form: Advance Directive Form",
    "Dynamic Form: Agency - Encounter Form Signature",
    "Dynamic Form: AKDA",
    "Dynamic Form: All Tools Form",
    "Dynamic Form: allow fax 1",
]

form_types_in_export_list = [
    "Dynamic Form: 13-17 EPSDT",
    "Dynamic Form: NPP Weekly Progress Report",
    "Dynamic Form: NPP Weekly Progress Report",
    "Encounter: CPT Note",
]

export_history_entry = {
    "rec": "461053",
    "patient_name": "KING, TERRY",
    "patient_number": "TK10140210",
    "patient_id": "81662",
    "form_type": "Encounter - CM 3.0",
    "form_date": "11/26/2023",
    "file_name": "1BA97653-8CC0-4C82-A96F-FF42748F15AA.zip",
    "status": "Completed",
}

output = {
    "artifact": "Axiom-EHI-Export-Instructions.pdf",
    "source_url": "https://axiomehr.com/wp-content/uploads/2024/05/Axiom-EHI-Export-Instructions.pdf",
    "pdf_metadata": metadata,
    "pages": 4,
    "page_contents": {
        "page_1": "Cover page: HiMS logo, title '170.315 (b)(10) Electronic Health Information Export', Company: Health Information Management Systems, Product Name: Axiom, Version Number: 7",
        "page_2": "Instructions for single-patient EHI export: Login, go to Report page, enter patient name/parameters, click BUILD REPORT. Screenshot shows report parameters form (Start Date, End Date, Patient, Form Types dropdown). Text about selecting records and using EHI Export action.",
        "page_3": "Screenshots showing: (1) Export record list with patient KING, TERRY (Patient # TK10140210, Patient ID 81662), 16 forms, columns: Form Type, Doc Type, File Date. (2) EHI Export action dropdown. (3) Success confirmation message.",
        "page_4": "EHI Export History table showing completed export. Note about password-encrypted compressed ZIP file sent to employee and patient email. Brief 'Patient Population Data Bulk Export' section: 2 sentences stating bulk export includes 'all population data' with compression.",
    },
    "form_types_visible_in_dropdown": form_types_in_dropdown,
    "form_types_visible_in_export_list": form_types_in_export_list,
    "export_history_example": export_history_entry,
    "export_format_info": {
        "output_format": "Password-encrypted compressed ZIP file",
        "file_naming": "GUID-based (e.g., 1BA97653-8CC0-4C82-A96F-FF42748F15AA.zip)",
        "delivery": "Password emailed to employee and patient",
        "contents_of_zip": "UNKNOWN - not documented",
        "structured_data_format": "UNKNOWN - not documented",
    },
    "data_dictionary": None,
    "schema": None,
    "sample_data": None,
    "field_definitions": None,
    "total_entities_documented": 0,
    "total_fields_documented": 0,
    "typos_found": ["informaiton (should be: information)", "cllick (should be: click)"],
    "assessment": {
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "has_field_definitions": False,
        "has_format_specification": False,
        "has_value_sets": False,
        "has_relationships": False,
        "documents_export_contents": False,
        "documents_export_format": False,
        "supports_single_patient": True,
        "supports_bulk_export": True,
        "bulk_export_details": "Two sentences only: 'The request for patient population export will include all population data. The export file(s) will be compressed to reduce file size.'",
    },
}

# Also extract raw text for reference
output["raw_text"] = text.stdout.strip()

output_path = os.path.join(OUTPUT_DIR, "pdf-extraction.json")
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"PDF extraction saved to {output_path}")
print(f"\nPDF Details:")
print(f"  Pages: {metadata.get('Pages', 'N/A')}")
print(f"  Author: {metadata.get('Author', 'N/A')}")
print(f"  Creator: {metadata.get('Creator', 'N/A')}")
print(f"  Created: {metadata.get('CreationDate', 'N/A')}")
print(f"  File size: {metadata.get('File size', 'N/A')}")
print(f"\nForm types visible in dropdown: {len(form_types_in_dropdown)}")
print(f"Form types visible in export list: {len(set(form_types_in_export_list))}")
print(f"Data dictionary present: No")
print(f"Schema present: No")
print(f"Sample data present: No")
print(f"Field-level documentation: None")
print(f"Export format documented: No (ZIP contents unknown)")
