#!/usr/bin/env python3
"""
Parse all available EHI export artifacts for emr4MD.

Since MedNet provides NO data dictionary, schema, or format documentation
for their (b)(10) EHI export, this script extracts what little structured
information exists from the available artifacts:
1. The Price Transparency PDF (b)(10) description
2. The InteropEngine 2026 API docs (g)(10) FHIR resources — NOT b(10) but the
   only technical documentation available)
3. The certified criteria from the Cures Update page
"""

import json
import subprocess
import re
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT = Path(".")

def extract_pdf_b10():
    """Extract the (b)(10) description from the Price Transparency PDF."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(DOWNLOADS / "Price_Transparency_emr4MD_v9.10.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Find b(10) section
    b10_info = {}
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "b)(10)" in line or "Electronic Health Information (EHI)" in line.replace("\n", ""):
            # Capture surrounding context
            context = "\n".join(lines[max(0, i-2):min(len(lines), i+6)])
            b10_info["raw_context"] = context.strip()
            break
    
    b10_info["description"] = "This functionality allows a practice to create individual and group exports of PHI without programming intervention."
    b10_info["cost"] = "Included in base service agreement, subscription fee plus Subscription fee from 3rd party - EMR Direct, one time implementation fee and annual subscription charged."
    b10_info["source"] = "Price_Transparency_emr4MD_v9.10.pdf"
    
    return b10_info

def extract_api_resources():
    """Extract FHIR resources from the enrichment JSON."""
    enrichment = json.load(open(DOWNLOADS / "enrichment" / "api-documentation-extracted.json"))
    
    api_2026 = enrichment["apiVersions"][1]
    resources = sorted(set(r["resourceType"] for r in api_2026["resources"]))
    
    return {
        "api_version": api_2026["version"],
        "fhir_version": "R4",
        "us_core_version": "6.1.0",
        "resource_count": len(resources),
        "resources": resources,
        "note": "These are g(10) Standardized API resources, NOT b(10) EHI export entities. No b(10)-specific documentation exists."
    }

def extract_certified_criteria():
    """Extract criteria from the Cures Update page."""
    html = open(DOWNLOADS / "mednet-2015-cures-update.html").read()
    criteria = re.findall(r'\(([a-h])\)\((\d+)\)', html)
    unique = sorted(set(f"({c[0]})({c[1]})" for c in criteria))
    return unique

def main():
    results = {
        "vendor": "MedNet Medical Solutions",
        "product": "emr4MD",
        "version": "Version 9.10",
        "chpl_id": "15.04.04.2796.emr4.09.00.1.191218",
        "b10_export": extract_pdf_b10(),
        "g10_api_resources": extract_api_resources(),
        "certified_criteria_count": len(extract_certified_criteria()),
        "ehi_documentation_status": {
            "data_dictionary": False,
            "schema_files": False,
            "sample_data": False,
            "field_definitions": False,
            "format_specified": False,
            "export_instructions": False,
            "value_sets": False,
            "relationships": False,
        },
        "summary": "No EHI export (b)(10) documentation exists. The registered URL points to g(7)/g(9) FHIR API docs. The only b(10) reference is a single sentence in the Price Transparency PDF."
    }
    
    with open(OUTPUT / "artifact-analysis.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Wrote artifact-analysis.json")
    
    # Since there is no data dictionary, entity-inventory-full.json is empty
    inventory = {
        "extraction_date": "2026-02-16",
        "source": "No data dictionary or schema exists for (b)(10) EHI export",
        "entities": [],
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "note": "MedNet provides zero documentation for the (b)(10) EHI export format, content, or structure. The g(10) API covers 29 FHIR resource types but is a separate system (EMR Direct Interoperability Engine) for clinical exchange only."
    }
    
    with open(OUTPUT / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print("Wrote entity-inventory-full.json")
    
    summary = {
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "pct_fields_with_descriptions": "N/A",
        "categories": {},
        "g10_api_resource_count": results["g10_api_resources"]["resource_count"],
        "documentation_exists": False,
        "export_format": "Unknown",
        "note": "No (b)(10) EHI export documentation exists. All numbers are zero because no data dictionary was provided."
    }
    
    with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("Wrote entity-inventory-summary.json")

if __name__ == "__main__":
    main()
