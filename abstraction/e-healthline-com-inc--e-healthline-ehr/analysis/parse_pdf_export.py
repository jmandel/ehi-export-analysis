#!/usr/bin/env python3
"""
Parse the E*HealthLine EHI Export PDF and extract structured information
about the export format, file components, and documentation quality.

Input: Electronic_Health_Information_Export.pdf (via pdftotext)
Output: full-entity-inventory.json, pdf-analysis-summary.json
"""

import json
import subprocess
import re
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent.parent.parent / \
    "results/e-healthline-com-inc--care-integrated-hospital-information-management-system"
PDF_PATH = RESULTS_DIR / "downloads/Electronic_Health_Information_Export.pdf"
OUTPUT_DIR = Path(__file__).resolve().parent

def extract_pdf_text():
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF_PATH), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def get_pdf_info():
    result = subprocess.run(
        ["pdfinfo", str(PDF_PATH)],
        capture_output=True, text=True
    )
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            info[key.strip()] = val.strip()
    return info

def parse_export_components(text):
    """Extract the 7 file components described in the export format section."""
    components = []

    # Documents
    components.append({
        "name": "Documents",
        "format": "CDA XML",
        "type": "folder",
        "description": "CDA XML DOC Export file containing the 'Documents' folder containing patient's supporting documents or attachments when available.",
        "fields_documented": False,
        "field_names": [],
        "field_count": 0,
        "category": "Clinical Documents"
    })

    # Notes
    components.append({
        "name": "Notes",
        "format": "CDA XML",
        "type": "folder",
        "description": "CDA XML DOC Export file folder containing all the notes recorded during the patient's previous medical visits/encounters.",
        "fields_documented": False,
        "field_names": [],
        "field_count": 0,
        "category": "Clinical Notes"
    })

    # BillingReport
    components.append({
        "name": "BillingReport",
        "format": "CSV",
        "type": "file",
        "description": "CSV file containing the patient's financial transactions with their provider. The information includes the patient information, transaction dates, charges, claims and the description of transactions made with status.",
        "fields_documented": False,
        "field_names": [
            "patient information", "transaction dates", "charges",
            "claims", "description of transactions", "status"
        ],
        "field_count": 0,  # exact columns not documented
        "category": "Billing"
    })

    # CCDA
    components.append({
        "name": "CCDA",
        "format": "XML (HL7 C-CDA)",
        "type": "file",
        "description": "XML file export of a patient's clinical data. The system allows exports of HL7 CCDA which complies with United States Core Data for Interoperability (USCDI), Version 1 requirements. The specifications for the CCDA can be obtained from the HL7 website.",
        "fields_documented": False,
        "field_names": [],
        "field_count": 0,
        "category": "Clinical Data (USCDI v1)",
        "standard_reference": "HL7 C-CDA / USCDI v1"
    })

    # demographics
    components.append({
        "name": "demographics",
        "format": "CSV",
        "type": "file",
        "description": "CSV file that contains the patient's key information, identification details, contact information, insurance information etc.",
        "fields_documented": False,
        "field_names": [
            "key information", "identification details",
            "contact information", "insurance information"
        ],
        "field_count": 0,
        "category": "Demographics"
    })

    # PatientDocumentFiles
    components.append({
        "name": "PatientDocumentFiles",
        "format": "CSV",
        "type": "file",
        "description": "CSV mapping file that contains the list of patient's documents. This file outlines the contents of the patient's supporting attachments contained in the 'Documents' folder.",
        "fields_documented": False,
        "field_names": [],
        "field_count": 0,
        "category": "Document Mapping"
    })

    # Schedule
    components.append({
        "name": "Schedule",
        "format": "CSV",
        "type": "file",
        "description": "CSV file that contains a record of the patient's encounters with specific information including appointment date, provider, location, appointment type, workflow, notes and date on which notes are recorded.",
        "fields_documented": False,
        "field_names": [
            "appointment date", "provider", "location",
            "appointment type", "workflow", "notes",
            "date on which notes are recorded"
        ],
        "field_count": 0,
        "category": "Encounters/Scheduling"
    })

    # Optional components
    components.append({
        "name": "Chart Documents",
        "format": "Mixed (TIF, etc.)",
        "type": "folder (optional)",
        "description": "Optionally included via [Include Chart Documents] checkbox. Contains chart documents with optional sticky notes on TIF documents.",
        "fields_documented": False,
        "field_names": [],
        "field_count": 0,
        "category": "Clinical Documents (Optional)"
    })

    components.append({
        "name": "Custom Patient Data Tables",
        "format": "CDA XML (embedded)",
        "type": "embedded in CCDA",
        "description": "Custom (user-created) Patient Data Tables are included as part of the CDA whenever the export is done using the Batch CDA option, unless the custom Patient Data Table is set to be excluded as FHR.",
        "fields_documented": False,
        "field_names": [],
        "field_count": 0,
        "category": "Custom/Extensible Data"
    })

    return components

def analyze_documentation_quality(text):
    """Analyze the quality indicators in the PDF."""
    issues = []

    # Check for wrong criterion in footer
    g10_count = text.count("170.315(g)(10)")
    b10_count = text.count("170.315(b)(10)")
    if g10_count > b10_count:
        issues.append({
            "type": "copy_paste_error",
            "detail": f"Footer references '170.315(g)(10)' ({g10_count} times) instead of (b)(10). Document was likely created from a (g)(10) template.",
            "severity": "medium"
        })

    # Check for truncated sentences
    truncated = text.count("For additional details on the export format and default paths,")
    if truncated > 0:
        issues.append({
            "type": "truncated_content",
            "detail": f"Found {truncated} truncated sentence(s) ending with 'For additional details on the export format and default paths,' — references a document not provided.",
            "severity": "high"
        })

    # Check for duplicate revision entries
    if "Original Document" in text:
        orig_count = text.count("Original Document")
        if orig_count > 1:
            issues.append({
                "type": "confusing_versioning",
                "detail": f"Both v1.0 and v2.0 are described as 'Original Document' ({orig_count} entries).",
                "severity": "low"
            })

    # Missing documentation elements
    missing = []
    if "column" not in text.lower() and "field name" not in text.lower():
        missing.append("field/column names for CSV files")
    if "data type" not in text.lower():
        missing.append("data types")
    if "value set" not in text.lower() and "code set" not in text.lower():
        missing.append("value sets or code sets")
    if "foreign key" not in text.lower() and "relationship" not in text.lower():
        missing.append("relationships between files")
    if "sample" not in text.lower() or "sample data" not in text.lower():
        missing.append("sample data files")
    if "schema" not in text.lower() and "xsd" not in text.lower():
        missing.append("machine-readable schemas")
    if "screenshot" not in text.lower():
        missing.append("screenshots of the export UI")

    issues.append({
        "type": "missing_documentation",
        "detail": f"Documentation lacks: {', '.join(missing)}",
        "severity": "critical",
        "missing_elements": missing
    })

    return issues

def main():
    text = extract_pdf_text()
    pdf_info = get_pdf_info()
    components = parse_export_components(text)
    quality_issues = analyze_documentation_quality(text)

    # Build full entity inventory
    inventory = {
        "source_file": "Electronic_Health_Information_Export.pdf",
        "source_url": "http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf",
        "pdf_metadata": {
            "pages": int(pdf_info.get("Pages", 0)),
            "title": pdf_info.get("Title", ""),
            "author": pdf_info.get("Author", ""),
            "creation_date": pdf_info.get("CreationDate", ""),
            "mod_date": pdf_info.get("ModDate", ""),
            "encrypted": pdf_info.get("Encrypted", ""),
            "file_size_bytes": int(pdf_info.get("File size", "0").split()[0]) if "File size" in pdf_info else 0
        },
        "export_mechanism": {
            "function_name": "Export Batch CCDA",
            "menu_location": "Data Maintenance Menu",
            "output_path": "\\\\SERVERNAME\\BarcodeScans\\HL7ExportFiles\\CDAexports",
            "output_format": "ZIP file (CDAXMLExport_8.Zip)",
            "single_patient": True,
            "population_export": True,
            "api_based": False,
            "requires_privileges": True,
            "privilege_requirements": [
                "Edit General Database Setup",
                "Print Documents OR Chart Reviewer"
            ]
        },
        "export_components": components,
        "documentation_quality": {
            "has_data_dictionary": False,
            "has_field_definitions": False,
            "has_data_types": False,
            "has_value_sets": False,
            "has_relationships": False,
            "has_sample_data": False,
            "has_schemas": False,
            "has_screenshots": False,
            "total_pages": int(pdf_info.get("Pages", 0)),
            "content_pages": int(pdf_info.get("Pages", 0)) - 3,  # minus cover, ToC, revision history
            "issues": quality_issues
        },
        "summary_statistics": {
            "total_export_components": len(components),
            "csv_files": sum(1 for c in components if c["format"] == "CSV"),
            "xml_components": sum(1 for c in components if "XML" in c["format"] or "CDA" in c["format"]),
            "optional_components": sum(1 for c in components if "optional" in c.get("type", "").lower() or "Optional" in c.get("category", "")),
            "fields_with_names_documented": 0,
            "fields_with_types_documented": 0,
            "fields_with_descriptions": 0,
            "total_field_names_mentioned": sum(len(c["field_names"]) for c in components),
            "note": "No field-level documentation exists. The PDF describes file components at a high level (file name, format, 1-2 sentence description) but does not document individual columns/fields within CSV files or CDA sections."
        }
    }

    # Save full entity inventory
    inventory_path = OUTPUT_DIR / "full-entity-inventory.json"
    with open(inventory_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved: {inventory_path}")

    # Save summary
    summary = {
        "vendor": "E*HealthLine.com, Inc.",
        "product": "CARE© Integrated Hospital Information Management System",
        "document_version": "2.0",
        "document_date": "October 24, 2023",
        "pdf_last_modified": "July 18, 2024",
        "pages": int(pdf_info.get("Pages", 0)),
        "export_format": "ZIP containing C-CDA XML + CSV files + CDA XML folders",
        "export_components_count": len(components),
        "csv_files": [c["name"] for c in components if c["format"] == "CSV"],
        "xml_folders": [c["name"] for c in components if "XML" in c["format"] or "CDA" in c["format"]],
        "data_dictionary_present": False,
        "field_level_documentation": False,
        "sample_data_provided": False,
        "schema_provided": False,
        "documentation_issues_count": len(quality_issues),
        "key_issues": [q["detail"] for q in quality_issues],
        "classification": "Standard-based projection with CSV supplements",
        "model_type": "C-CDA standard + vendor CSV supplements"
    }

    summary_path = OUTPUT_DIR / "pdf-analysis-summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {summary_path}")

    # Print key stats
    print(f"\n=== PDF Analysis Summary ===")
    print(f"Pages: {summary['pages']}")
    print(f"Export components: {summary['export_components_count']}")
    print(f"CSV files: {', '.join(summary['csv_files'])}")
    print(f"Data dictionary: {'Yes' if summary['data_dictionary_present'] else 'No'}")
    print(f"Field-level docs: {'Yes' if summary['field_level_documentation'] else 'No'}")
    print(f"Documentation issues: {summary['documentation_issues_count']}")
    for issue in quality_issues:
        print(f"  [{issue['severity'].upper()}] {issue['detail']}")

if __name__ == "__main__":
    main()
