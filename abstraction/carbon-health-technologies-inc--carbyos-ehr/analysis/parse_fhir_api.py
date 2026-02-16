#!/usr/bin/env python3
"""Parse the FHIR API PDF text to extract resources and their data elements.
This parses the (g)(10) FHIR API doc to understand what clinical data CarbyOS
exposes via FHIR — which is relevant for assessing whether (b)(10) goes beyond it.
"""

import json
import re

with open("analysis/fhir-api-text.txt", "r") as f:
    text = f.read()

# Find resource sections by looking for "Data Elements" headers
# The structure is: Resource Name header, then Data Elements table, then Endpoints table

lines = text.split('\n')

resources = []
current_resource = None
in_data_elements = False
in_endpoints = False

# Parse the USCDIv3 mapping table too
uscdi_mappings = []

i = 0
while i < len(lines):
    line = lines[i].strip()
    
    # Detect resource headers - they appear as standalone names before "Data Elements"
    # Look for patterns like "Patient", "Allergy Intolerance", etc.
    
    # Detect "Data Elements" section start
    if line == "Data Elements":
        in_data_elements = True
        in_endpoints = False
        i += 1
        continue
    
    # Detect "Endpoints" section start
    if line == "Endpoints":
        in_data_elements = False
        in_endpoints = True
        i += 1
        continue
    
    # Resource headers appear as top-level headings
    resource_names = [
        "Patient", "Allergy Intolerance", "Care Plan", "Care Teams", 
        "Conditions", "Coverages", "Implantable Devices", "Diagnostic Reports",
        "Document Reference", "Encounter", "Goal", "Immunization", "Location",
        "Medical Dispense", "Medication Request", "Observation", "Procedure",
        "Service Request", "Organization", "Practitioner", "Provenance",
        "Related Person", "Specimen"
    ]
    
    if line in resource_names:
        if current_resource:
            resources.append(current_resource)
        current_resource = {
            "name": line,
            "data_elements": [],
            "endpoints": []
        }
        in_data_elements = False
        in_endpoints = False
        i += 1
        continue
    
    # Parse data element rows - they have format: element_name  type  description
    if in_data_elements and current_resource and line:
        # Skip header rows
        if line.startswith("Element") or line.startswith("Type") or line.startswith("---"):
            i += 1
            continue
        # Skip page numbers
        if re.match(r'^\d+$', line):
            i += 1
            continue
        
        # Try to parse as a data element row
        # Format varies but generally: element_name   Type   Description
        parts = re.split(r'\s{2,}', line)
        if len(parts) >= 2:
            element = {
                "name": parts[0].strip(),
                "type": parts[1].strip() if len(parts) > 1 else "",
                "description": parts[2].strip() if len(parts) > 2 else ""
            }
            # Skip if it looks like a continuation or noise
            if element["name"] and not element["name"].startswith("GET") and not element["name"].startswith("POST"):
                current_resource["data_elements"].append(element)
    
    i += 1

if current_resource:
    resources.append(current_resource)

# Output summary
print(f"Total FHIR resources found: {len(resources)}")
print(f"Total data elements across all resources: {sum(len(r['data_elements']) for r in resources)}")
print()

for r in resources:
    print(f"  {r['name']}: {len(r['data_elements'])} elements")

# Save full parse
with open("analysis/fhir-api-resources.json", "w") as f:
    json.dump(resources, f, indent=2)

print(f"\nSaved to analysis/fhir-api-resources.json")
