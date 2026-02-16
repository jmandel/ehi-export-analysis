#!/usr/bin/env python3
"""
Parse all EHI export artifacts for Axxess Palliative and produce
a structured JSON inventory of what was found.

Since there is no data dictionary, this script documents what the
two PDFs contain and produces artifact-level metadata.
"""

import json
import subprocess
import os
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/axxess--axxess-palliative/downloads")
OUTPUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/axxess--axxess-palliative/analysis")

def get_pdf_info(pdf_path):
    """Extract metadata from a PDF using pdfinfo."""
    result = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True)
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            info[key.strip()] = value.strip()
    return info

def get_pdf_text(pdf_path):
    """Extract text from a PDF using pdftotext."""
    result = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, text=True)
    return result.stdout

def analyze_b10_pdf():
    """Analyze the primary b10 EHI export PDF."""
    path = DOWNLOADS / "b10-electronic-health-information-export.pdf"
    info = get_pdf_info(path)
    text = get_pdf_text(path)
    
    return {
        "file": "b10-electronic-health-information-export.pdf",
        "type": "EHI Export Documentation",
        "pages": int(info.get("Pages", 0)),
        "size_bytes": os.path.getsize(path),
        "author": info.get("Author", ""),
        "creation_date": info.get("CreationDate", ""),
        "pdf_version": info.get("PDF version", ""),
        "content_summary": {
            "export_format": ["C-CDA 2.1 XML", "PDF"],
            "delivery_format": "ZIP file",
            "scope": "Single patient or population (multiple patients)",
            "mechanism": "Patients > Download Patient Chart > Request Documents > Export",
            "data_dictionary_present": False,
            "schema_present": False,
            "sample_data_present": False,
            "field_definitions": 0,
            "entity_definitions": 0,
            "contains_internal_note": True,
            "internal_note_text": "This should comply with what we need and buy us time to finish the feature in the overall direction we are thinking."
        },
        "full_text": text.strip()
    }

def analyze_disclosures_pdf():
    """Analyze the CEHRT Disclosures PDF."""
    path = DOWNLOADS / "Axxess-CEHRT-Disclosures-V3.0.2022.pdf"
    info = get_pdf_info(path)
    text = get_pdf_text(path)
    
    # Extract the (b)(10) specific entry
    b10_text = ""
    lines = text.split("\n")
    capturing = False
    for line in lines:
        if "170.315(b)(10)" in line or "b)(10)" in line:
            capturing = True
        if capturing:
            b10_text += line + "\n"
            if "stored" in line.lower() or "export" in line.lower():
                # Continue capturing until we hit next section
                pass
            if "170.315" in line and "b)(10)" not in line and capturing and len(b10_text) > 50:
                break
    
    # Count certified criteria mentioned
    criteria = []
    for line in lines:
        if "§ 170.315" in line or "§170.315" in line:
            # Extract the criterion code
            import re
            match = re.search(r'170\.315\s*\(([a-z])\)\((\d+)\)', line)
            if match:
                criteria.append(f"170.315 ({match.group(1)})({match.group(2)})")
    
    return {
        "file": "Axxess-CEHRT-Disclosures-V3.0.2022.pdf",
        "type": "CEHRT Transparency Disclosures",
        "pages": int(info.get("Pages", 0)),
        "size_bytes": os.path.getsize(path),
        "author": info.get("Author", ""),
        "creation_date": info.get("CreationDate", ""),
        "pdf_version": info.get("PDF version", ""),
        "certified_criteria_count": len(set(criteria)),
        "certified_criteria": sorted(set(criteria)),
        "b10_entry": {
            "description": "Axxess Palliative enables a user to timely create an export file(s) with all of a single patient's or population of patient's electronic health information that can be stored.",
            "costs": "All costs are included within software licenses fees according to contract terms and conditions"
        }
    }

def main():
    artifacts = {
        "product": "Axxess Palliative",
        "analysis_date": "2026-02-16",
        "total_artifacts": 3,
        "artifacts": [
            analyze_b10_pdf(),
            analyze_disclosures_pdf(),
            {
                "file": "cehrt-page-screenshot.png",
                "type": "Screenshot",
                "size_bytes": os.path.getsize(DOWNLOADS / "cehrt-page-screenshot.png"),
                "description": "Full-page screenshot of the CEHRT compliance hub page"
            }
        ],
        "data_dictionary": {
            "present": False,
            "entities": 0,
            "fields": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "machine_readable_schema": False,
            "sample_data": False
        },
        "export_details": {
            "format": "C-CDA 2.1 XML + PDF in ZIP",
            "model_type": "standard_projection",
            "is_native_database_export": False,
            "is_ccda_or_fhir_repackaging": True,
            "mechanism": "UI: Patients > Download Patient Chart",
            "single_patient": True,
            "bulk_export": True,
            "access_constraints": "Appropriate user permissions required",
            "fees": "Included in software license"
        }
    }
    
    output_path = OUTPUT / "artifact-analysis.json"
    with open(output_path, "w") as f:
        json.dump(artifacts, f, indent=2)
    
    print(f"Artifact analysis written to {output_path}")
    print(f"\nSummary:")
    print(f"  Total artifacts: {artifacts['total_artifacts']}")
    print(f"  Data dictionary present: {artifacts['data_dictionary']['present']}")
    print(f"  Export format: {artifacts['export_details']['format']}")
    print(f"  Model type: {artifacts['export_details']['model_type']}")
    print(f"  Entities documented: {artifacts['data_dictionary']['entities']}")
    print(f"  Fields documented: {artifacts['data_dictionary']['fields']}")

if __name__ == "__main__":
    main()
