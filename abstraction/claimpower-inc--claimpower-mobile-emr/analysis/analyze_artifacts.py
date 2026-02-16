#!/usr/bin/env python3
"""
Analyze all EHI export artifacts for Claimpower Mobile EMR.
Extracts structured information from PDFs and produces a full inventory JSON.
"""

import json
import subprocess
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/claimpower-inc--claimpower-mobile-emr/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/claimpower-inc--claimpower-mobile-emr/analysis"

def get_pdf_info(filepath):
    """Extract metadata from a PDF file."""
    result = subprocess.run(["pdfinfo", filepath], capture_output=True, text=True)
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

def get_pdf_text(filepath):
    """Extract text from a PDF file."""
    result = subprocess.run(["pdftotext", "-layout", filepath, "-"], capture_output=True, text=True)
    return result.stdout

def analyze_artifacts():
    artifacts = []
    
    pdf_files = [
        ("CCDA_Export.PDF", "Main EHI export documentation - index page plus all three sub-documents inline"),
        ("CCDA_Export_Single_Patient.PDF", "Single patient C-CDA export walkthrough"),
        ("CCDA_Multiple_Patients.PDF", "Multiple patient C-CDA export walkthrough"),
        ("CCDA_Patient_Portal.PDF", "Patient portal C-CDA export walkthrough"),
    ]
    
    for filename, description in pdf_files:
        filepath = os.path.join(DOWNLOADS, filename)
        info = get_pdf_info(filepath)
        text = get_pdf_text(filepath)
        
        artifact = {
            "filename": filename,
            "description": description,
            "file_size_bytes": os.path.getsize(filepath),
            "pages": int(info.get("Pages", 0)),
            "author": info.get("Author", ""),
            "creator": info.get("Creator", ""),
            "creation_date": info.get("CreationDate", ""),
            "modification_date": info.get("ModDate", ""),
            "text_content": text.strip(),
            "text_length_chars": len(text.strip()),
            "has_data_dictionary": False,
            "has_field_definitions": False,
            "has_schema": False,
            "has_sample_data": False,
            "content_type": "screenshot_walkthrough",
        }
        artifacts.append(artifact)
    
    return artifacts

def extract_ccda_sections_from_screenshots():
    """
    Based on visual inspection of the PDF screenshots, extract the C-CDA
    sections visible in the patient portal 'View Health Information' page.
    """
    return [
        "Patient Demographics",
        "Provider Details",
        "Patient Medical Documents",
        "Allergies",
        "Medications",
        "Problems",
        "Procedures",
        "Vital Signs",
        "Encounters",
        "Social History",
        "Family History",
        "Results (Discrete)",
    ]

def extract_ccda_header_fields():
    """
    Based on visual inspection of the Summary Of Care document screenshots
    (pages 4 and 9), extract the C-CDA header fields visible.
    """
    return [
        {"field": "Patient", "example": "MICHAEL AGRATI"},
        {"field": "date of birth", "example": "January 7, 1951"},
        {"field": "Race", "example": "White"},
        {"field": "Ethnicity", "example": "Not Hispanic or Latino"},
        {"field": "Preferred Language", "example": "en-US"},
        {"field": "Contact info", "example": "Primary Home address, phone, patient IDs"},
        {"field": "Patient IDs", "example": "MRN, insurance IDs"},
        {"field": "Document Id", "example": "OID-based document identifier"},
        {"field": "Document Created", "example": "August 25, 2023"},
        {"field": "Performer", "example": "Provider name"},
        {"field": "Author", "example": "Provider name"},
        {"field": "Contact info (author)", "example": "Address and phone"},
        {"field": "Encounter Id", "example": "UUID"},
        {"field": "Encounter Date", "example": "Date range"},
        {"field": "Encounter Location", "example": "Practice name"},
        {"field": "Responsible party", "example": "Provider name"},
        {"field": "Contact info (responsible party)", "example": "Address and phone"},
        {"field": "Personal relationship", "example": "Contact person"},
        {"field": "Contact info (personal relationship)", "example": "Address and phone"},
        {"field": "Covered by", "example": "Insurance/payer"},
        {"field": "Contact info (covered by)", "example": "Address and phone"},
        {"field": "Information recipient", "example": "Provider name"},
        {"field": "Legal authenticator", "example": "Signed by provider with timestamp"},
    ]

def extract_reports_menu():
    """
    Reports menu items visible in the EMR Reports screenshot (page 5).
    """
    return [
        "Ad Effectiveness Report",
        "Patients Processing Status",
        "Billing Sent Report",
        "Billing Stats Report",
        "Charts Created",
        "Checked In Patient Status",
        "Patient List",
        "Audit Report",
        "Public Health Surveillance Report",
        "Clinical Quality Measures Report",
        "Automated Measure Calculation Report",
        "Labs Filed Report",
        "Search Charts",
        "Export Patient Health Records",  # This is the EHI export function
        "Insurance Liability Status",
        "Daily Office Collection Report",
        "TCM Report",
        "RPM Report",
        "Re-Signed Chart Status Report",
    ]

def extract_dashboard_icons():
    """
    Dashboard icons visible in the EMR screenshots (pages 2 and 5).
    """
    return [
        "Patient Queue",
        "Messages",
        "Rules",
        "Confirm/Prescribe/Manage Refills/Available Letter",
        "Results",
        "Lookup Medical Records",
        "Charts",
        "Billing",
        "Immunization",
        "Patient Registration",
        "Scheduling",
        "Census",
        "Speed Billing",
        "EMR Reports",
        "Attach Documents",
        "Settings",
        "Monitoring Module",
        "MIPS",
        "CCM List",
        "TCM List",
    ]

def main():
    artifacts = analyze_artifacts()
    ccda_sections = extract_ccda_sections_from_screenshots()
    ccda_header = extract_ccda_header_fields()
    reports_menu = extract_reports_menu()
    dashboard_icons = extract_dashboard_icons()
    
    inventory = {
        "vendor": "Claimpower, Inc.",
        "product": "Claimpower Mobile EMR",
        "version": "6.1",
        "export_type": "C-CDA Summary of Care",
        "export_format": "C-CDA XML in ZIP archive",
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_schema": False,
        "has_sample_data": False,
        "artifacts": artifacts,
        "artifact_summary": {
            "total_files": len(artifacts),
            "total_pages": sum(a["pages"] for a in artifacts),
            "all_authored_by": "Rohan Thadani",
            "all_created_on": "2023-08-28",
            "content_type": "screenshot_walkthrough_only",
            "data_dictionary_present": False,
            "field_definitions_present": False,
        },
        "export_paths": [
            {
                "name": "Single Patient Export",
                "mechanism": "UI - Lookup Medical Records → Clinical Document → Summary of Care Records → Generate CCDA → Download ZIP",
                "capability": "single_patient",
                "format": "C-CDA ZIP",
            },
            {
                "name": "Multiple Patient Export",
                "mechanism": "UI - EMR Reports → Export Patient Health Records → Select patients → Generate ZIP",
                "capability": "bulk",
                "format": "C-CDA ZIP",
                "note": "Screenshot shows 12,217 total patients with 'All Patients' checkbox",
            },
            {
                "name": "Patient Portal Export",
                "mechanism": "Patient Portal login → View Health Information → Summary of Care Records → Download ZIP",
                "capability": "single_patient_self_service",
                "format": "C-CDA ZIP",
            },
        ],
        "ccda_sections_visible": ccda_sections,
        "ccda_header_fields_visible": ccda_header,
        "emr_reports_menu": reports_menu,
        "emr_dashboard_icons": dashboard_icons,
        "clinical_tabs_visible": [
            "SUMMARY",
            "E.PROGRESS NOTE",
            "COMM LOG",
            "CONSULTS",
            "FLAG",
            "LAB REQUISITION",
            "SCREENING",
        ],
        "patient_portal_sections": [
            "View Summary of Care",
            "Secure Messaging",
            "View My Actions",
            "View Health Information",
        ],
    }
    
    # Summary stats
    stats = {
        "total_artifacts": len(artifacts),
        "total_pdf_pages": sum(a["pages"] for a in artifacts),
        "entities_documented": 0,
        "fields_documented": 0,
        "fields_with_descriptions": 0,
        "ccda_sections_visible_in_portal": len(ccda_sections),
        "ccda_header_fields_visible": len(ccda_header),
        "export_format": "C-CDA (Consolidated Clinical Document Architecture)",
        "model_type": "Standard projection (C-CDA)",
        "classification": "Standard-based projection",
        "documentation_quality": "Minimal - screenshot walkthroughs only, no technical documentation",
    }
    
    # Write outputs
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(os.path.join(OUTPUT_DIR, "summary-stats.json"), "w") as f:
        json.dump(stats, f, indent=2)
    
    # Print summary
    print("=== Claimpower Mobile EMR - EHI Export Artifact Analysis ===")
    print(f"\nTotal artifacts: {len(artifacts)}")
    print(f"Total PDF pages: {sum(a['pages'] for a in artifacts)}")
    for a in artifacts:
        print(f"  {a['filename']}: {a['pages']} pages, {a['file_size_bytes']} bytes, {a['text_length_chars']} chars of text")
    print(f"\nExport type: C-CDA Summary of Care")
    print(f"Export format: C-CDA XML in ZIP archive")
    print(f"Export paths: {len(inventory['export_paths'])}")
    for p in inventory["export_paths"]:
        print(f"  - {p['name']} ({p['capability']})")
    print(f"\nC-CDA sections visible in patient portal: {len(ccda_sections)}")
    for s in ccda_sections:
        print(f"  - {s}")
    print(f"\nC-CDA header fields visible: {len(ccda_header)}")
    print(f"\nData dictionary: NO")
    print(f"Field definitions: NO")
    print(f"Schema documentation: NO")
    print(f"Sample data files: NO")
    print(f"\nClassification: Standard-based projection")
    print(f"\nOutputs written to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
