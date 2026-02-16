#!/usr/bin/env python3
"""
Parse the G10 API documentation PDF to extract all FHIR resource types,
their parameters, and sample output structures. Produces a JSON inventory
of the FHIR-based export content.
"""
import json
import re
import subprocess
import sys

PDF_PATH = "../../../results/radysans-inc--radysans-ehr/downloads/G10ApplicationAccessTermsandCondition.pdf"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Parse section headers like "1.1 AllergyIntolerance"
sections = []
pattern = re.compile(r'^1\.(\d+)\s+(.+?)(?:\s*:)?\s*$', re.MULTILINE)
for m in pattern.finditer(text):
    sections.append({
        "number": f"1.{m.group(1)}",
        "name": m.group(2).strip(),
        "start": m.start()
    })

# Extract parameters for each section
resources = []
for i, sec in enumerate(sections):
    end = sections[i+1]["start"] if i+1 < len(sections) else len(text)
    block = text[sec["start"]:end]
    
    # Extract URL
    url_match = re.search(r'URL:\s*(https?://\S+)', block)
    url = url_match.group(1) if url_match else None
    
    # Extract parameters
    param_match = re.search(r'Parameter Input:\s*\n(.*?)(?:Exception|Sample)', block, re.DOTALL)
    params = []
    if param_match:
        for line in param_match.group(1).strip().split('\n'):
            p = line.strip()
            if p and not p.startswith('170.315'):
                params.append(p)
    
    # Check if sample output exists
    has_sample = "Sample Output:" in block
    
    resources.append({
        "section": sec["number"],
        "resource_type": sec["name"],
        "url": url,
        "parameters": params,
        "has_sample_output": has_sample
    })

# Also parse the function table
func_table_match = re.search(r'Function Names.*?(?=1\.1 )', text, re.DOTALL)
table_resources = []
if func_table_match:
    table_text = func_table_match.group(0)
    # Extract resource names from table
    for line in table_text.split('\n'):
        url_match = re.search(r'cutecharts\.com/radywebapi/(\w+)', line)
        if url_match:
            rtype = url_match.group(1)
            if rtype not in table_resources:
                table_resources.append(rtype)

output = {
    "source_file": "G10ApplicationAccessTermsandCondition.pdf",
    "pdf_pages": 41,
    "total_fhir_resources": len(resources),
    "resource_types_from_table": table_resources,
    "resources": resources,
    "notes": [
        "All resources follow US Core STU 3.1.1 profiles",
        "Each resource section includes URL, parameters, exception handling note, and sample JSON output",
        "No custom extensions or vendor-specific resources beyond US Core",
        "No billing, scheduling, or administrative resources present"
    ]
}

with open("fhir_resource_inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
