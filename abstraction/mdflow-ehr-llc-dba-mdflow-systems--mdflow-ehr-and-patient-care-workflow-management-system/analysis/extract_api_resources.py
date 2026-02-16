#!/usr/bin/env python3
"""Extract FHIR resource types from the MDFlow API documentation PDF.

Parses pdftotext output to identify all FHIR resource endpoints documented
in the (g)(7)/(g)(9)/(g)(10) API documentation, and extracts key fields
shown in JSON response examples for each resource type.
"""

import subprocess
import re
import json

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/mdflow-ehr-llc-dba-mdflow-systems--mdflow-ehr-and-patient-care-workflow-management-system/downloads"

def extract_api_resources():
    text = subprocess.check_output(
        ["pdftotext", "-layout", f"{DOWNLOADS}/API-Documentation-g7910.pdf", "-"],
        text=True
    )

    # Find all "Request :" or "Request:" lines that name a FHIR resource
    resource_pattern = re.compile(r'Request\s*:\s*(.+?)(?:\s*\.{2,}|\s*$)', re.MULTILINE)
    resources = []
    seen = set()
    for m in resource_pattern.finditer(text):
        name = m.group(1).strip().rstrip('.')
        if name and name not in seen and not name.startswith('Page'):
            seen.add(name)
            resources.append(name)

    # Also extract the FHIR resource types from GET URL patterns
    url_pattern = re.compile(r'GET\s+\d+\s+https?://[^/]+/[^/]+/fhir/(\w+)')
    fhir_types = set()
    for m in url_pattern.finditer(text):
        fhir_types.add(m.group(1))

    result = {
        "source": "API-Documentation-g7910.pdf",
        "page_count": 58,
        "purpose": "(g)(7)/(g)(9)/(g)(10) FHIR API documentation — NOT (b)(10) EHI export",
        "documented_resource_sections": resources,
        "fhir_resource_types_in_urls": sorted(fhir_types),
        "note": "This documents the FHIR API, not the EHI export. Included for context on what clinical data MDFlow exposes via FHIR."
    }

    return result

if __name__ == "__main__":
    result = extract_api_resources()
    output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/mdflow-ehr-llc-dba-mdflow-systems--mdflow-ehr-and-patient-care-workflow-management-system/analysis/api_resources.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
