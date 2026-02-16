#!/usr/bin/env python3
"""Extract and catalog all EHI export documentation from MDFlow artifacts.

Parses the two EHI export PDFs and the FHIR API documentation to produce
a complete inventory of what the vendor provides as (b)(10) documentation.
"""

import subprocess
import json
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/mdflow-ehr-llc-dba-mdflow-systems--mdflow-ehr-and-patient-care-workflow-management-system/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/mdflow-ehr-llc-dba-mdflow-systems--mdflow-ehr-and-patient-care-workflow-management-system/analysis"

def extract_pdf_text(filename):
    path = os.path.join(DOWNLOADS, filename)
    return subprocess.check_output(["pdftotext", "-layout", path, "-"], text=True).strip()

def get_pdf_info(filename):
    path = os.path.join(DOWNLOADS, filename)
    info = subprocess.check_output(["pdfinfo", path], text=True)
    result = {}
    for line in info.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result

def main():
    artifacts = []

    # EHIExport.pdf
    text1 = extract_pdf_text("EHIExport.pdf")
    info1 = get_pdf_info("EHIExport.pdf")
    artifacts.append({
        "filename": "EHIExport.pdf",
        "source_url": "https://www.mdflow.com/EHIExport.pdf",
        "is_ehi_b10_documentation": True,
        "pages": int(info1.get("Pages", 0)),
        "file_size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "EHIExport.pdf")),
        "author": info1.get("Author"),
        "created": info1.get("CreationDate"),
        "version_referenced": "8.0",
        "full_text": text1,
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_export_instructions": False,
        "export_formats_mentioned": ["C-CDA", "CSV", "PDF"],
        "key_claims": [
            "Export contains data stored in the patient's chart in the SQL database",
            "Primary export format is C-CDA",
            "CSV and PDF available for special and customized requests",
            "Can export single patient or group of patients",
            "ZIP compression used for large files"
        ]
    })

    # EHI-B10-Export.pdf
    text2 = extract_pdf_text("EHI-B10-Export.pdf")
    info2 = get_pdf_info("EHI-B10-Export.pdf")
    artifacts.append({
        "filename": "EHI-B10-Export.pdf",
        "source_url": "https://www.mdflow.com/www/pdf%20files/EHI%20B10-Export.pdf",
        "is_ehi_b10_documentation": True,
        "pages": int(info2.get("Pages", 0)),
        "file_size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "EHI-B10-Export.pdf")),
        "author": info2.get("Author"),
        "created": info2.get("CreationDate"),
        "version_referenced": "8.1",
        "full_text": text2,
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_export_instructions": False,
        "export_formats_mentioned": ["C-CDA", "ZIP"],
        "key_claims": [
            "Export contains data from the patient's chart",
            "Multiple file formats used",
            "ZIP is the archive format",
            "C-CDA is the health information exchange format",
            "Export file is a ZIP containing ZIP files of C-CDAs",
            "Each patient encounter has a C-CDA in the ZIP archive"
        ]
    })

    # API Documentation
    info3 = get_pdf_info("API-Documentation-g7910.pdf")
    artifacts.append({
        "filename": "API-Documentation-g7910.pdf",
        "source_url": "https://www.mdflow.com/www/pdf%20files/API%20Documentation%20(g7910).pdf",
        "is_ehi_b10_documentation": False,
        "pages": int(info3.get("Pages", 0)),
        "file_size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "API-Documentation-g7910.pdf")),
        "author": info3.get("Author"),
        "created": info3.get("CreationDate"),
        "version_referenced": "8.0",
        "purpose": "FHIR (g)(7)/(g)(9)/(g)(10) API documentation — not (b)(10)"
    })

    # ValidURLs.json
    artifacts.append({
        "filename": "ValidURLs.json",
        "source_url": "https://www.mdflow.com/www/pdf%20files/ValidURLs.json",
        "is_ehi_b10_documentation": False,
        "file_size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "ValidURLs.json")),
        "purpose": "FHIR Service Base URL list — (g)(10) artifact, not (b)(10)"
    })

    # mandatory-disclosures-page.png
    artifacts.append({
        "filename": "mandatory-disclosures-page.png",
        "source_url": "https://www.mdflow.com/www/mdflow-electronics-health-records.html",
        "is_ehi_b10_documentation": False,
        "file_size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "mandatory-disclosures-page.png")),
        "purpose": "Screenshot of mandatory disclosures page showing EHI export links"
    })

    summary = {
        "total_artifacts": len(artifacts),
        "ehi_b10_artifacts": sum(1 for a in artifacts if a.get("is_ehi_b10_documentation")),
        "total_ehi_documentation_pages": sum(
            a.get("pages", 0) for a in artifacts if a.get("is_ehi_b10_documentation")
        ),
        "data_dictionary_present": False,
        "field_definitions_present": False,
        "sample_data_present": False,
        "schema_present": False,
        "artifacts": artifacts
    }

    output_path = os.path.join(OUTPUT_DIR, "artifact_inventory.json")
    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
