#!/usr/bin/env python3
"""Parse CliniComp USCDI API PDF to extract all data objects and their field definitions."""

import subprocess
import re
import json

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/clinicomp-intl--clinicomp-ehr/downloads/250-70079_CliniComp_EHR_ONC-API_USCDI.pdf"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# The 20 USCDI objects listed in Section 3.1
objects = [
    "Patient_Name", "Sex", "Date_of_Birth", "Race", "Ethnicity",
    "Preferred_Language", "Smoking_Status", "Problems", "Medications",
    "Medication_Allergies", "Laboratory_Tests", "Laboratory_Values",
    "Vital_Signs", "Implantable_Device", "Procedures", "Care_Team_Members",
    "Immunizations", "Health_Concerns", "Assessment_Treatment", "Goals"
]

# Parse each object's field definitions from sections 5.6.1 through 5.6.20
# Each section has a table with columns: NAME, TYPE, NULLABLE, DESCRIPTION, EHR MAJOR IT
# Parse section-by-section from the extracted text

sections = {}
lines = text.split('\n')

# Find each section header and extract field rows
current_section = None
current_fields = []

in_definitions = False
for i, line in enumerate(lines):
    # Match section headers like "5.6.1 USCDI Patient Name" (at start of line, no leading dots)
    m = re.match(r'^5\.6\.(\d+)\s+USCDI\s+(.*)', line)
    if m:
        if current_section and current_fields:
            sections[current_section] = current_fields
        current_section = m.group(2).strip()
        current_fields = []
        in_definitions = True
        continue
    
    # Also match section 5.7 to stop parsing
    if re.match(r'^5\.7\s+', line):
        if current_section and current_fields:
            sections[current_section] = current_fields
        current_section = None
        in_definitions = False
        break
    
    if not in_definitions or not current_section:
        continue
    
    stripped = line.strip()
    if not stripped:
        continue
    
    # Skip header rows, page footers
    if any(skip in line for skip in ['NAME', 'NULLABLE', 'Table ', 'P/N:', 'CliniComp, Intl.', 'Library of USCDI', 'Page ']):
        continue
    
    # Try to parse field rows
    # Format: " FieldName    String    YES/NO    Description    EHR Major IT"
    field_match = re.match(r'\s+(.+?)\s{2,}(String|Number|Array)\s{2,}(YES|NO)\s{2,}(.*)', line)
    if field_match:
        name = field_match.group(1).strip()
        ftype = field_match.group(2).strip()
        nullable = field_match.group(3).strip()
        rest = field_match.group(4).strip()
        current_fields.append({
            "name": name,
            "type": ftype,
            "nullable": nullable,
            "description_and_ehr_it": rest
        })

# Output results
output = {
    "total_objects": len(objects),
    "objects_parsed": len(sections),
    "total_fields": sum(len(f) for f in sections.values()),
    "objects": {}
}

for name, fields in sections.items():
    output["objects"][name] = {
        "field_count": len(fields),
        "fields": [f["name"] for f in fields],
        "field_details": fields
    }

# Print summary
print(f"USCDI API Objects: {len(objects)} defined, {len(sections)} parsed with field details")
print(f"Total fields across all objects: {sum(len(f) for f in sections.values())}")
print()
for name, fields in sections.items():
    print(f"  {name}: {len(fields)} fields")
    for f in fields:
        print(f"    - {f['name']} ({f['type']}, nullable={f['nullable']})")

# Save full output
with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/clinicomp-intl--clinicomp-ehr/analysis/uscdi_objects_parsed.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nFull output saved to uscdi_objects_parsed.json")
