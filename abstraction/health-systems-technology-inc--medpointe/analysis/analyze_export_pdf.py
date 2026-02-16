#!/usr/bin/env python3
"""
Analyze MedPointe EHI export documentation.

Parses the sole artifact (a 2-page PDF) and the help-documents page screenshot
to extract all available information about the export.

Since there is no data dictionary, schema, or structured artifact to parse,
this script extracts text from the PDF and documents what was found.
"""

import json
import subprocess
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), "..", "downloads")
PDF_PATH = os.path.join(DOWNLOADS, "Providers - Exporting Computer Readable Documents.pdf")

def extract_pdf_info():
    """Extract metadata and text from the PDF."""
    info = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
    text = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
    return {
        "metadata": info.stdout.strip(),
        "text": text.stdout.strip(),
        "page_count": 2,
        "file_size_bytes": os.path.getsize(PDF_PATH),
    }

def analyze():
    pdf = extract_pdf_info()

    # Document types from Export Chart dialog (verified from PDF page 2 screenshot)
    document_types = [
        "Cover Sheet",
        "Notes",
        "Text Documents",
        "Scanned/Faxed Documents",
        "Include Restricted Documents",
    ]

    # Other export functions visible in right-click menu (PDF page 1 screenshot)
    other_exports = [
        "Export Continuity of Care",
        "Export Continuity of Care - Referral",
        "Export Continuity of Care - Batch",
        "Export Immunization Data",
        "Export Syndromic Data",
        "Export Medical Records",
    ]

    # Output options from Export Chart dialog
    output_options = ["Print", "Export to Folder", "Export to C62 file"]

    # Batch export patient filters mentioned in text
    patient_filters = [
        "last name range",
        "date of birth",
        "patient classification",
        "provider",
    ]

    result = {
        "artifact_analyzed": "Providers - Exporting Computer Readable Documents.pdf",
        "pdf_pages": pdf["page_count"],
        "pdf_size_bytes": pdf["file_size_bytes"],
        "export_format": "C62 (proprietary, undocumented)",
        "document_types_in_export_dialog": document_types,
        "other_export_functions_in_menu": other_exports,
        "output_options": output_options,
        "batch_patient_filters": patient_filters,
        "data_dictionary_present": False,
        "schema_present": False,
        "sample_data_present": False,
        "field_definitions": 0,
        "total_fields_documented": 0,
        "assessment": (
            "The entire EHI export documentation is a 2-page PDF describing "
            "how to click export buttons in the MedPointe UI. It uses a proprietary "
            "'C62' format with zero documentation of its structure, fields, or content. "
            "No data dictionary, no schema, no sample data. The export appears to cover "
            "only clinical documents (notes, scanned docs) — not structured clinical data "
            "(medications, labs, vitals, allergies), billing, insurance, or administrative data."
        ),
    }

    output_path = os.path.join(os.path.dirname(__file__), "pdf-analysis-output.json")
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    analyze()
