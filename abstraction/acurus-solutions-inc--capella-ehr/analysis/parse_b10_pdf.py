#!/usr/bin/env python3
"""Parse the (b)(10) EHI export PDF to extract all CCD sections and data elements."""

import subprocess
import json
import re

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/170.315(b)(10)-EHI-export-v3.pdf", "-"],
    capture_output=True, text=True
)
text = result.stdout

# Parse sections and data elements
sections = []
current_section = None
current_elements = []

lines = text.split('\n')
for line in lines:
    line = line.strip()
    if not line:
        continue
    
    # Detect CCD section headers (they have OIDs in brackets)
    section_match = re.match(r'^(.+?)\s*\[([0-9.]+(?:\s*:\s*[\d-]+)?)\]', line)
    if section_match:
        if current_section:
            sections.append({
                "section": current_section["name"],
                "oid": current_section["oid"],
                "data_elements": current_elements
            })
        current_section = {
            "name": section_match.group(1).strip(),
            "oid": section_match.group(2).strip()
        }
        current_elements = []
        continue
    
    # Detect standalone section headers (no OID)
    standalone_sections = [
        "Patient Demographics/Information",
        "Provider's name and office contact information",
        "Laboratory Tests",
        "Laboratory Information",
    ]
    if line in standalone_sections:
        if current_section:
            sections.append({
                "section": current_section["name"],
                "oid": current_section.get("oid"),
                "data_elements": current_elements
            })
        current_section = {"name": line, "oid": None}
        current_elements = []
        continue

    # Skip non-data lines
    skip_patterns = [
        r'^Version:', r'^§170', r'^This document', r'^Contents',
        r'^Overview', r'^Capella EHR', r'^by implementing',
        r'^generate the', r'^To achieve', r'^•', r'^a\.\s',
        r'^b\.\s', r'^For assistance', r'^Data Elements',
        r'^Standard Referenced', r'^Sections in the CCD',
        r'^CCD Output Format', r'^\(Diagnostic tests',
        r'^Recommended patient', r'^Page \d',
        r'^Single Patient Export', r'^Bulk Export',
        r'^The user can', r'^Generate CCD',
        r'^human readable',
    ]
    if any(re.match(p, line) for p in skip_patterns):
        continue
    
    # Skip if the line looks like an XPATH or code system (starts with numbers/dots)
    if re.match(r'^2\.16\.', line):
        continue
    
    # Capture data element names (left-column entries)
    # These are typically short phrases without OIDs
    if current_section and len(line) < 80 and not line.startswith('§'):
        # Clean up: skip pure code system references
        if re.match(r'^[\d.]+$', line):
            continue
        # Skip lines that are just "SNOMED", "LOINC", etc.
        if line in ['SNOMED', 'LOINC', 'CPT', 'RxNorm', 'NDC', 'CVX', 'HCPCS',
                     'CPT-4', 'RxNorm and NDC', 'SNOMED and ICD10']:
            continue
        current_elements.append(line)

if current_section:
    sections.append({
        "section": current_section["name"],
        "oid": current_section.get("oid"),
        "data_elements": current_elements
    })

# Clean up: remove duplicate/noise elements and merge related items
cleaned_sections = []
for s in sections:
    # Remove known noise
    clean_elems = []
    for e in s["data_elements"]:
        # Skip if it's a continuation of XPATH or template ID
        if re.match(r'^0\.22\.', e):
            continue
        if e in ['(translation code)', '-']:
            continue
        # Remove code system annotations embedded in element names
        e = re.sub(r'\s*2\.16\.\d+[\d.]*', '', e).strip()
        if e and e not in clean_elems:
            clean_elems.append(e)
    if clean_elems or s["oid"]:
        cleaned_sections.append({
            "section": s["section"],
            "oid": s["oid"],
            "data_elements": clean_elems,
            "element_count": len(clean_elems)
        })

# Output results
output = {
    "source": "170.315(b)(10)-EHI-export-v3.pdf",
    "format": "C-CDA (CCD)",
    "standard": "HL7 CDA R2 Consolidated CDA Templates for Clinical Notes (US Realm) DSTU R2.1, August 2015",
    "total_sections": len(cleaned_sections),
    "total_data_elements": sum(s["element_count"] for s in cleaned_sections),
    "sections": cleaned_sections
}

with open("b10_sections_parsed.json", "w") as f:
    json.dump(output, f, indent=2)

# Print summary
print(f"Total sections: {output['total_sections']}")
print(f"Total data elements: {output['total_data_elements']}")
print()
for s in cleaned_sections:
    print(f"  {s['section']}: {s['element_count']} elements")
    for e in s['data_elements']:
        print(f"    - {e}")
