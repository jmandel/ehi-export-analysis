#!/usr/bin/env python3
"""Parse all EHI export artifacts for Office Ally EHR 24/7 and produce structured inventory."""

import json
import subprocess
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/office-ally-llc--ehr-24-7"
ANALYSIS_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/office-ally-llc--ehr-24-7/analysis"

def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def get_pdf_info(pdf_path):
    """Get PDF metadata using pdfinfo."""
    result = subprocess.run(
        ["pdfinfo", pdf_path],
        capture_output=True, text=True
    )
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

def parse_ehi_pdf():
    """Parse the EHI Export Documentation PDF into structured data."""
    pdf_path = os.path.join(RESULTS_DIR, "downloads", "EHI_Export_Documentation.pdf")
    text = extract_pdf_text(pdf_path)
    info = get_pdf_info(pdf_path)

    # The PDF describes 4 export components
    export_components = [
        {
            "name": "CCDA",
            "format": "HL7 C-CDA XML",
            "standard": "USCDI Version 1",
            "description": "Bulk export of HL7 CCDA xml files which comply to United States Core Data for Interoperability (USCDI), Version 1 requirements.",
            "field_definitions_provided": False,
            "sample_data_provided": False,
            "schema_provided": False,
            "notes": "References external HL7 C-CDA specification; no vendor-specific profile or template constraints documented."
        },
        {
            "name": "Appointments",
            "format": "CSV",
            "standard": None,
            "description": "This file offers a comprehensive view of appointment details, the data will be exported in CSV format.",
            "field_definitions_provided": False,
            "sample_data_provided": False,
            "schema_provided": False,
            "notes": "No column headers, field names, data types, or value sets documented."
        },
        {
            "name": "Claims",
            "format": "CSV",
            "standard": None,
            "description": "This file offers a comprehensive view of claim details, the data will be exported in CSV format.",
            "field_definitions_provided": False,
            "sample_data_provided": False,
            "schema_provided": False,
            "notes": "No column headers, field names, data types, or value sets documented."
        },
        {
            "name": "Attachments",
            "format": "Original upload format",
            "standard": None,
            "description": "Contains any scanned or uploaded documents in the patient's record, the files will be exported in the format in which they were uploaded.",
            "field_definitions_provided": False,
            "sample_data_provided": False,
            "schema_provided": False,
            "notes": "Documents exported as-is in their original format (e.g., PDF, JPEG, PNG)."
        }
    ]

    return {
        "source_file": "downloads/EHI_Export_Documentation.pdf",
        "pdf_metadata": {
            "author": info.get("Author", ""),
            "creator": info.get("Creator", ""),
            "creation_date": info.get("CreationDate", ""),
            "pages": int(info.get("Pages", 0)),
            "file_size_bytes": int(info.get("File size", "0").split()[0]),
        },
        "document_version": "1.0.1",
        "document_date": "2024-02-08",
        "product_version_in_doc": "5.6.81",
        "current_certified_version": "5.9.255",
        "version_mismatch": True,
        "supports_single_patient": True,
        "supports_population_export": True,
        "export_components": export_components,
        "total_components": len(export_components),
        "components_with_field_definitions": 0,
        "components_with_sample_data": 0,
        "components_with_schema": 0,
        "data_dictionary_present": False,
        "version_history": [
            {"version": "1.0.0", "date": "2023-11-30", "comments": "Original Draft"},
            {"version": "1.0.1", "date": "2024-01-18", "comments": "Included Attachments and updated Product Version"}
        ],
        "raw_text": text.strip()
    }

def build_full_inventory():
    """Build the full entity inventory - in this case, minimal since no data dictionary exists."""
    # Since there is no data dictionary, we document what we know from the PDF
    entities = []

    # C-CDA sections (USCDI v1 standard set)
    uscdi_v1_sections = [
        "Patient Demographics", "Allergies and Intolerances", "Assessment and Plan of Treatment",
        "Care Team Members", "Clinical Notes", "Goals", "Health Concerns",
        "Immunizations", "Laboratory Results", "Medications", "Problems",
        "Procedures", "Provenance", "Smoking Status", "Unique Device Identifiers",
        "Vital Signs"
    ]

    for section in uscdi_v1_sections:
        entities.append({
            "entity_name": f"C-CDA: {section}",
            "source_component": "CCDA",
            "format": "HL7 C-CDA XML",
            "standard": "USCDI v1",
            "fields": "N/A - defined by HL7 C-CDA standard, no vendor-specific documentation",
            "field_count": None,
            "fields_with_descriptions": None,
            "fields_with_types": None,
            "vendor_documented": False,
            "notes": "Content inferred from USCDI v1 standard reference; vendor does not document which C-CDA sections or templates are populated."
        })

    # CSV components - completely undocumented
    entities.append({
        "entity_name": "Appointments",
        "source_component": "Appointments",
        "format": "CSV",
        "standard": None,
        "fields": "Unknown - no column headers or field definitions provided",
        "field_count": None,
        "fields_with_descriptions": None,
        "fields_with_types": None,
        "vendor_documented": False,
        "notes": "Described only as 'a comprehensive view of appointment details' with no further specification."
    })

    entities.append({
        "entity_name": "Claims",
        "source_component": "Claims",
        "format": "CSV",
        "standard": None,
        "fields": "Unknown - no column headers or field definitions provided",
        "field_count": None,
        "fields_with_descriptions": None,
        "fields_with_types": None,
        "vendor_documented": False,
        "notes": "Described only as 'a comprehensive view of claim details' with no further specification."
    })

    entities.append({
        "entity_name": "Attachments",
        "source_component": "Attachments",
        "format": "Original upload format",
        "standard": None,
        "fields": "N/A - binary files exported as-is",
        "field_count": None,
        "fields_with_descriptions": None,
        "fields_with_types": None,
        "vendor_documented": False,
        "notes": "Scanned/uploaded documents in original format. No metadata schema documented."
    })

    return {
        "vendor": "Office Ally, LLC",
        "product": "EHR 24/7",
        "extraction_date": "2026-02-15",
        "source_artifact": "downloads/EHI_Export_Documentation.pdf",
        "data_dictionary_available": False,
        "total_entities": len(entities),
        "entities_from_standard": len(uscdi_v1_sections),
        "entities_vendor_specific": 3,
        "entities_with_field_definitions": 0,
        "total_documented_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "entities": entities
    }

def main():
    # Parse the PDF
    pdf_data = parse_ehi_pdf()
    with open(os.path.join(ANALYSIS_DIR, "parsed-ehi-documentation.json"), "w") as f:
        json.dump(pdf_data, f, indent=2)
    print(f"Parsed EHI documentation: {pdf_data['total_components']} export components")
    print(f"  Components with field definitions: {pdf_data['components_with_field_definitions']}")
    print(f"  Components with sample data: {pdf_data['components_with_sample_data']}")
    print(f"  Data dictionary present: {pdf_data['data_dictionary_present']}")

    # Build full entity inventory
    inventory = build_full_inventory()
    with open(os.path.join(ANALYSIS_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nFull entity inventory: {inventory['total_entities']} entities")
    print(f"  From standard (USCDI v1 C-CDA sections): {inventory['entities_from_standard']}")
    print(f"  Vendor-specific: {inventory['entities_vendor_specific']}")
    print(f"  Entities with field definitions: {inventory['entities_with_field_definitions']}")
    print(f"  Total documented fields: {inventory['total_documented_fields']}")

    # Summary statistics
    summary = {
        "artifact_count": 2,
        "artifacts": [
            {
                "file": "EHI_Export_Documentation.pdf",
                "type": "PDF",
                "pages": 1,
                "size_bytes": 97036,
                "informativeness": "low",
                "content": "Single page describing 4 export components with no field-level detail"
            },
            {
                "file": "certification-page-full.png",
                "type": "Screenshot",
                "size_bytes": 753134,
                "informativeness": "minimal",
                "content": "Screenshot of certification page confirming PDF is the only EHI export artifact"
            }
        ],
        "export_components": 4,
        "export_formats": ["HL7 C-CDA XML", "CSV", "Original upload format"],
        "data_dictionary": False,
        "field_definitions": 0,
        "sample_data": False,
        "machine_readable_schema": False,
        "export_mechanism": "Not documented (UI assumed)",
        "single_patient": True,
        "bulk_export": True,
    }
    with open(os.path.join(ANALYSIS_DIR, "summary-statistics.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary statistics saved.")

if __name__ == "__main__":
    main()
