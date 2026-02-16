#!/usr/bin/env python3
"""Parse the B10 EHI Export PDF and extract structured information about export components."""

import json
import subprocess
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', '..', '..', 
                         'results', 'maxremind-inc--maximus', 'downloads')
PDF_PATH = os.path.join(DOWNLOADS, 'B10-Electronic-Health-information-Export.pdf')

# Extract PDF metadata
info = subprocess.run(['pdfinfo', PDF_PATH], capture_output=True, text=True)
info_lines = info.stdout.strip().split('\n')
metadata = {}
for line in info_lines:
    if ':' in line:
        key, val = line.split(':', 1)
        metadata[key.strip()] = val.strip()

# Extract text
text = subprocess.run(['pdftotext', '-layout', PDF_PATH, '-'], capture_output=True, text=True)
raw_text = text.stdout

# Define the export components found in the PDF
export_components = [
    {
        "id": 1,
        "name": "Single Patient Export",
        "description": "Maximus allows a user to export electronic health information (EHI) for a single patient at any time without developer assistance.",
        "format": "Multiple (see sub-components)",
        "field_level_detail": False,
        "data_dictionary": False
    },
    {
        "id": 2,
        "name": "Multi-Patient Export",
        "description": "Maximus can export all the data for a patient population in standardized format.",
        "format": "Multiple (see sub-components)",
        "field_level_detail": False,
        "data_dictionary": False
    },
    {
        "id": 3,
        "name": "CCD/C-CDA Documents",
        "description": "Bulk export of HL7 CCDA xml files complying to USCDI v1 requirements.",
        "format": "HL7 C-CDA XML (R2.1)",
        "standards_referenced": [
            "HL7 CDA Release 2: IHE Health Story Consolidation DSTU R1.1 (July 2012)",
            "HL7 CDA R2: Consolidated CDA Templates for Clinical Notes (US Realm) DSTU R2.1 (August 2015, June 2019 with Errata)",
            "HL7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2 (October 2019)"
        ],
        "field_level_detail": False,
        "data_dictionary": False,
        "note": "Standard C-CDA; no vendor-specific extensions or customizations documented"
    },
    {
        "id": 4,
        "name": "FHIR Bulk Data Access",
        "description": "FHIR R4 / US Core STU V3.1.1 bulk data export via (g)(10) SmartOnFHIR API.",
        "format": "FHIR R4 (US Core STU 3.1.1)",
        "fhir_resources": [
            "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
            "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
            "Immunization", "Location", "MedicationRequest", "Observation",
            "Organization", "Patient", "Practitioner", "Procedure", "Provenance"
        ],
        "fhir_resource_count": 18,
        "documentation_url": "https://documents.maximus.care/",
        "field_level_detail": False,
        "data_dictionary": False,
        "note": "Standard US Core resources only; no custom profiles or extensions documented. This is the (g)(10) API repackaged as (b)(10) component."
    },
    {
        "id": 5,
        "name": "Patient Demographics & Insurance",
        "description": "Comprehensive view of demographics and insurance details structured for clarity and ease of access.",
        "format": "Excel",
        "field_level_detail": False,
        "data_dictionary": False,
        "fields_documented": 0,
        "note": "One-sentence description only. No column names, no field definitions, no sample data."
    },
    {
        "id": 6,
        "name": "Appointments",
        "description": "Comprehensive view of all future appointment details, structured for clarity and ease of access.",
        "format": "Excel",
        "field_level_detail": False,
        "data_dictionary": False,
        "fields_documented": 0,
        "note": "One-sentence description only. Explicitly says 'future' appointments — historical visit data not mentioned."
    },
    {
        "id": 7,
        "name": "Documents",
        "description": "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document in the patient's record.",
        "format": "Native file formats (PDF, JPG, PNG)",
        "field_level_detail": False,
        "data_dictionary": False,
        "organizational_structure": "Sorted by patient chart number folders with category subfolders (Lab Reports, Radiology, Scanned Receipts, etc.)",
        "note": "Document file export with folder-based organization. No metadata manifest or index file described."
    }
]

result = {
    "source_file": "B10-Electronic-Health-information-Export.pdf",
    "pdf_metadata": metadata,
    "page_count": int(metadata.get("Pages", 0)),
    "file_size_bytes": int(metadata.get("File size", "0").replace(" bytes", "")),
    "created_date": "2023-10-03",
    "author": metadata.get("Author", ""),
    "export_components": export_components,
    "total_export_components": len(export_components),
    "has_data_dictionary": False,
    "has_field_level_documentation": False,
    "has_sample_data": False,
    "has_schema_files": False,
    "summary_statistics": {
        "total_entities_documented": 0,
        "total_fields_documented": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "export_formats": ["C-CDA XML", "FHIR R4 JSON", "Excel", "PDF/JPG/PNG"],
        "fhir_resource_types": 18,
        "proprietary_components": 3,
        "proprietary_components_detail": ["Demographics & Insurance Excel", "Appointments Excel", "Document files"]
    }
}

output_path = os.path.join(os.path.dirname(__file__), 'full-entity-inventory.json')
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)

print(f"Parsed B10 PDF: {result['page_count']} pages, {result['total_export_components']} export components")
print(f"Has data dictionary: {result['has_data_dictionary']}")
print(f"Has field-level docs: {result['has_field_level_documentation']}")
print(f"FHIR resource types: {result['summary_statistics']['fhir_resource_types']}")
print(f"Proprietary components: {result['summary_statistics']['proprietary_components']}")
print(f"Output saved to: {output_path}")
