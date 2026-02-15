#!/usr/bin/env python3
"""Parse all EHI export artifacts for Radysans EHR and produce structured summary."""

import json
import subprocess
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/radysans-inc--radysans-ehr/downloads"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/radysans-inc--radysans-ehr/analysis"

def extract_pdf_text(path):
    result = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    return result.stdout

def get_pdf_info(path):
    result = subprocess.run(["pdfinfo", path], capture_output=True, text=True)
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

# Analyze B-10 document
b10_text = extract_pdf_text(os.path.join(DOWNLOADS, "B-10-Documentation.pdf"))
b10_info = get_pdf_info(os.path.join(DOWNLOADS, "B-10-Documentation.pdf"))

# Extract C-CDA sections from B-10
ccda_sections = []
in_sections = False
for line in b10_text.split("\n"):
    stripped = line.strip()
    if stripped == "Sections of EHI exported in CCDA :":
        in_sections = True
        continue
    if in_sections and stripped:
        if stripped.startswith("The specifications"):
            break
        if stripped.startswith("2. FHIR"):
            break
        ccda_sections.append(stripped)

# Analyze G10 document
g10_text = extract_pdf_text(os.path.join(DOWNLOADS, "G10ApplicationAccessTermsandCondition.pdf"))
g10_info = get_pdf_info(os.path.join(DOWNLOADS, "G10ApplicationAccessTermsandCondition.pdf"))

# Extract FHIR resource types
fhir_resources = []
for line in g10_text.split("\n"):
    stripped = line.strip()
    if stripped.startswith("1.") and " " in stripped:
        parts = stripped.split(" ", 1)
        if len(parts) == 2 and parts[0].startswith("1."):
            # Check it's a section header (number format 1.N)
            num = parts[0].rstrip(":")
            try:
                section_num = int(num.split(".")[1])
                resource_name = parts[1].strip().rstrip(":")
                fhir_resources.append(resource_name)
            except (ValueError, IndexError):
                pass

# Analyze Costs document
costs_text = extract_pdf_text(os.path.join(DOWNLOADS, "RadysansEHRCostsandLimitations.pdf"))
costs_info = get_pdf_info(os.path.join(DOWNLOADS, "RadysansEHRCostsandLimitations.pdf"))

# Analyze FHIR endpoint bundle
with open(os.path.join(DOWNLOADS, "fhir-endpoint-bundle.json")) as f:
    fhir_bundle = json.load(f)

# Build summary
summary = {
    "b10_document": {
        "filename": "B-10-Documentation.pdf",
        "pages": int(b10_info.get("Pages", 0)),
        "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "B-10-Documentation.pdf")),
        "creation_date": b10_info.get("CreationDate", ""),
        "title": b10_info.get("Title", ""),
        "ccda_sections": ccda_sections,
        "ccda_section_count": len(ccda_sections),
        "mentions_fhir_bulk_data": "FHIR Bulk Data" in b10_text or "Bulk Data" in b10_text,
        "mentions_data_dictionary": "data dictionary" in b10_text.lower(),
        "mentions_schema": "schema" in b10_text.lower(),
        "has_field_level_detail": False,
        "has_sample_data": False,
    },
    "g10_document": {
        "filename": "G10ApplicationAccessTermsandCondition.pdf",
        "pages": int(g10_info.get("Pages", 0)),
        "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "G10ApplicationAccessTermsandCondition.pdf")),
        "creation_date": g10_info.get("CreationDate", ""),
        "fhir_resources": fhir_resources,
        "fhir_resource_count": len(fhir_resources),
        "has_sample_outputs": "Sample Output" in g10_text,
        "has_oauth_docs": "OAuth" in g10_text or "authorize" in g10_text,
        "has_api_terms": "API Terms of Use" in g10_text,
    },
    "costs_document": {
        "filename": "RadysansEHRCostsandLimitations.pdf",
        "pages": int(costs_info.get("Pages", 0)),
        "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "RadysansEHRCostsandLimitations.pdf")),
        "data_portability_fee": "One-time fee per provider upon request of data extraction",
    },
    "fhir_endpoint": {
        "filename": "fhir-endpoint-bundle.json",
        "api_base_url": "https://ehrwebapi.cutecharts.com/radywebapi",
        "organization": "Radysans Inc.",
        "endpoint_status": "active",
    },
    "analysis_summary": {
        "total_artifacts": 5,
        "export_formats": ["C-CDA (XML)", "FHIR R4 (JSON)"],
        "ccda_section_count": len(ccda_sections),
        "fhir_resource_count": len(fhir_resources),
        "has_native_data_model": False,
        "has_data_dictionary": False,
        "has_billing_coverage": False,
        "has_sample_data_files": False,
        "classification": "Standard-based projection",
    }
}

# Write output
output_path = os.path.join(OUTPUT, "artifact_analysis.json")
with open(output_path, "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
