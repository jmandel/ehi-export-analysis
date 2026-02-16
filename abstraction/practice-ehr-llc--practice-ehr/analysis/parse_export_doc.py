#!/usr/bin/env python3
"""
Parse the Practice EHR B10 EHI Export PDF and produce a structured JSON
representation of its contents. Since this PDF contains no data dictionary
or schema, the output documents the export structure as described.
"""

import json
import subprocess
import os
import sys

RESULTS_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "results", "practice-ehr-llc--practice-ehr"
)
PDF_PATH = os.path.join(RESULTS_DIR, "downloads",
                        "Practice-EHR-B10-Electronic-Health-Information-Export.pdf")
OUTPUT_DIR = os.path.dirname(__file__)

# Extract PDF metadata
pdfinfo = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
pdftext = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)

# Parse pdfinfo output
metadata = {}
for line in pdfinfo.stdout.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Build structured representation of the export documentation
export_doc = {
    "source_file": "Practice-EHR-B10-Electronic-Health-Information-Export.pdf",
    "source_url": "https://www.practiceehr.com/hubfs/PracticeEHR-2023/Practice%20EHR%20B10-Electronic%20Health%20Information%20Export.pdf",
    "pdf_metadata": {
        "pages": int(metadata.get("Pages", 0)),
        "creator": metadata.get("Creator", ""),
        "creation_date": metadata.get("CreationDate", ""),
        "file_size_bytes": os.path.getsize(PDF_PATH),
        "pdf_version": metadata.get("PDF version", ""),
    },
    "document_version": "1.0",
    "document_date": "2023-11-22",
    "export_modes": [
        {
            "name": "Single Patient Export",
            "description": "Practice EHR allows users to export electronic health information (EHI) for a single patient at any time without developer assistance."
        },
        {
            "name": "Multi-Patient Export",
            "description": "Practice EHR allows users to export electronic health information (EHI) for multiple patients at any time without developer assistance."
        }
    ],
    "export_structure": {
        "format": "ZIP file (one per patient)",
        "contents": [
            {
                "name": "Clinical folder",
                "description": "Contains one XML-based C-CDA file per patient",
                "format": "C-CDA XML",
                "standard": "C-CDA R2.1 compliant with USCDI v1",
                "specifications_referenced": [
                    "HL7 CDA R2 IHE Health Story Consolidation, DSTU R1.1 (July 2012)",
                    "HL7 CDA R2 Consolidated CDA Templates, DSTU R2.1 (August 2015, June 2019 Errata)",
                    "HL7 CDA R2 C-CDA Templates R2.1 Companion Guide, Release 2 (October 2019)"
                ],
                "field_level_documentation": False,
                "sections_documented": False,
                "template_ids_documented": False
            },
            {
                "name": "Documents folder",
                "description": "Patient documents in original upload/scan formats",
                "format": "Mixed (.jpg, .gif, .bmp, .png, .pdf, .txt)",
                "document_types": [
                    "Signed progress notes",
                    "Available lab results",
                    "Radiology reports",
                    "Scanned documents",
                    "Imported documents",
                    "Uploaded documents (typo: 'Iploaded' in original)"
                ]
            },
            {
                "name": "Patient Documents Detail.xls",
                "description": "Excel spreadsheet (structure and contents NOT documented)",
                "format": "XLS",
                "field_level_documentation": False
            }
        ]
    },
    "documentation_quality": {
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_data_types": False,
        "has_value_sets": False,
        "has_relationships": False,
        "has_sample_data": False,
        "has_machine_readable_schema": False,
        "has_screenshots": False,
        "has_step_by_step_instructions": False,
        "total_content_pages": 3,
        "typos_found": ["USCD (should be USCDI)", "Iploaded (should be Uploaded)"]
    },
    "data_domains_documented": {
        "clinical_via_ccda": True,
        "clinical_detail_level": "Implicit via C-CDA standard reference only; no vendor-specific mapping",
        "billing": False,
        "scheduling": False,
        "insurance": False,
        "patient_portal": False,
        "e_prescribing_detail": False,
        "telehealth": False,
        "practice_management": False,
        "documents_attachments": True
    }
}

# Write output
output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
with open(output_path, "w") as f:
    json.dump(export_doc, f, indent=2)

print(f"Wrote structured export documentation to {output_path}")

# Print summary statistics
print(f"\n=== Summary Statistics ===")
print(f"PDF pages: {export_doc['pdf_metadata']['pages']}")
print(f"Content pages: {export_doc['documentation_quality']['total_content_pages']}")
print(f"Export components: {len(export_doc['export_structure']['contents'])}")
print(f"Export modes: {len(export_doc['export_modes'])}")
print(f"Data dictionary present: {export_doc['documentation_quality']['has_data_dictionary']}")
print(f"Field definitions present: {export_doc['documentation_quality']['has_field_definitions']}")
print(f"Sample data present: {export_doc['documentation_quality']['has_sample_data']}")
print(f"Machine-readable schema: {export_doc['documentation_quality']['has_machine_readable_schema']}")
print(f"Document types in Documents folder: {len(export_doc['export_structure']['contents'][1]['document_types'])}")
print(f"Typos found: {len(export_doc['documentation_quality']['typos_found'])}")

# Domains covered vs not covered
covered = sum(1 for v in export_doc['data_domains_documented'].values()
              if v is True)
not_covered = sum(1 for v in export_doc['data_domains_documented'].values()
                  if v is False)
print(f"Data domains with any coverage: {covered}")
print(f"Data domains with no coverage: {not_covered}")
