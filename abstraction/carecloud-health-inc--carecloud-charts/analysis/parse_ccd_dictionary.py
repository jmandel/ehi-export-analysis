#!/usr/bin/env python3
"""Parse the CCD data dictionary from the EHI export documentation PDF.
Extracts sections, data elements, XPATHs, and code systems from the PDF text."""

import subprocess
import re
import json

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/carecloud-health-inc--carecloud-charts/downloads/ehi-export-documentation.pdf"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Parse CCD sections and their data elements
# Sections are identified by their templateId pattern: [2.16.840.1.113883...]
# or by headers like "Patient Demographics/Information"

sections = []
current_section = None
current_elements = []

lines = text.split('\n')

# Track which page we're on
in_ccd_section = False

for line in lines:
    stripped = line.strip()
    if not stripped:
        continue
    
    # Skip page headers/footers
    if '§170.315(b)(10)' in stripped and 'Documentation' in stripped:
        continue
    if re.match(r'^Page \d+ of \d+$', stripped):
        continue
    
    # Detect section headers - they're lines with templateId brackets or standalone headers
    # Pattern: "Section Name [templateId]" or just "Section Name" followed by data elements
    section_match = re.match(r'^([A-Z][A-Za-z /\(\)&\']+(?:\s*\[[\d\.:]+\s*(?::\s*[\d-]+)?\])?)$', stripped)
    
    # Check for known section headers
    known_sections = [
        "Patient Demographics/Information",
        "Provider's name and office contact information",
        "Chief Complaint and Reason for visit",
        "Encounters",
        "Immunizations",
        "Instructions",
        "Treatment Plan",
        "Social History",
        "Problems",
        "Medications",
        "Medication Allergies",
        "Laboratory Tests",
        "Laboratory Information",
        "Laboratory value(s)/result(s)",
        "Vitals",
        "Goal",
        "Procedures",
        "Care team member(s)",
        "Reason for Referral",
        "Medical Equipment",
        "Mental Status",
        "Functional Status",
        "Health Concern",
        "Date and Location of visit",
    ]
    
    is_section = False
    for sec_name in known_sections:
        if stripped.startswith(sec_name):
            is_section = True
            if current_section:
                sections.append({
                    "section": current_section,
                    "elements": current_elements
                })
            # Extract templateId if present
            tid_match = re.search(r'\[([\d\.:]+(?:\s*:\s*[\d-]+)?)\]', stripped)
            template_id = tid_match.group(1).strip() if tid_match else None
            current_section = sec_name
            current_elements = []
            break
    
    if is_section:
        continue
    
    # Skip table headers
    if stripped.startswith("Data Elements") or stripped.startswith("XPATH"):
        in_ccd_section = True
        continue
    if stripped.startswith("Code System") and "Name" in stripped:
        continue
    
    # Detect data elements (lines that start with a field name, possibly with XPATH)
    # Data elements are typically indented field names
    if current_section and in_ccd_section:
        # Skip lines that are just OIDs or code system references
        if re.match(r'^[\d\.]+$', stripped):
            continue
        # Skip lines that are just parenthetical notes
        if stripped.startswith('(') and stripped.endswith(')'):
            # This might be a note for the section, not a data element
            continue
        # Skip the "and" connector lines
        if stripped in ['and', 'or']:
            continue
        
        # Check if this looks like a data element name
        # Data elements typically start with a capitalized word
        if re.match(r'^[A-Z][a-zA-Z]', stripped) and not stripped.startswith('Standard Referenced'):
            # Extract possible code systems from the line
            code_systems = re.findall(r'2\.16\.840\.1\.\d+(?:\.\d+)*', stripped)
            # Clean element name (remove XPATH and code system info)
            elem_name = re.split(r'\s{2,}', stripped)[0].strip()
            if elem_name and len(elem_name) > 1 and elem_name not in ['SNOMED', 'LOINC', 'RxNorm', 'NDC', 'CVX', 'HCPCS', 'CPT']:
                current_elements.append(elem_name)

# Don't forget the last section
if current_section:
    sections.append({
        "section": current_section,
        "elements": current_elements
    })

# Output results
total_elements = 0
print("=" * 70)
print("CCD DATA DICTIONARY - PARSED SECTIONS AND DATA ELEMENTS")
print("=" * 70)

for sec in sections:
    n = len(sec["elements"])
    total_elements += n
    print(f"\n{sec['section']} ({n} elements)")
    for elem in sec["elements"]:
        print(f"  - {elem}")

print(f"\n{'=' * 70}")
print(f"TOTAL SECTIONS: {len(sections)}")
print(f"TOTAL DATA ELEMENTS: {total_elements}")
print(f"{'=' * 70}")

# Save as JSON
with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/carecloud-health-inc--carecloud-charts/analysis/ccd_dictionary.json", "w") as f:
    json.dump({
        "total_sections": len(sections),
        "total_elements": total_elements,
        "sections": sections
    }, f, indent=2)

print("\nSaved to ccd_dictionary.json")

# Also produce a summary of code systems used
print("\n\nCODE SYSTEMS REFERENCED IN THE CCD:")
text_after_ccd = text[text.find("CCD Output Format"):]
code_systems_found = set()
for match in re.finditer(r'(2\.16\.840\.1\.\d+(?:\.\d+)*)\s+(\S+(?:\s+\S+)*?)(?=\n|$)', text_after_ccd):
    oid = match.group(1)
    name = match.group(2).strip()
    if name and not name.startswith('2.16'):
        code_systems_found.add((oid, name))

for oid, name in sorted(code_systems_found):
    print(f"  {oid}: {name}")
