#!/usr/bin/env python3
"""Parse the Tebra General Clinical API documentation to extract all resources and fields."""

import json
import re

with open("general_api_docs_text.txt") as f:
    text = f.read()

# Find the Resources section
resources_start = text.find("Resources\n\nPatient")
if resources_start == -1:
    resources_start = text.find("Resources\n")
    
content = text[resources_start:]

# Parse the response fields tables
# The format is: Parent Field | Field | Type | Description

resources = []
current_resource = None
current_fields = []

lines = content.split('\n')
i = 0
in_response = False
header_seen = False

while i < len(lines):
    line = lines[i].strip()
    
    # Detect resource headers - endpoints like "Patient", "Encounter", etc.
    # They appear as single words on a line followed by request info
    if line and re.match(r'^(Patient|Encounter|AllergyIntolerance|CarePlan|Condition|Device|Procedure|Goal|Observation|SmokingStatus|DiagnosticReport|Immunization|MedicationStatement|Summary)\s', line):
        # Check if this is a resource header
        if 'Retrieves' in line or 'Retrieves' in lines[i+1] if i+1 < len(lines) else False:
            if current_resource and current_fields:
                resources.append({
                    "name": current_resource,
                    "endpoint": current_endpoint,
                    "fields": current_fields
                })
            current_resource = line.split()[0]
            current_endpoint = ""
            current_fields = []
            in_response = False
            header_seen = False
    
    # Detect endpoint URL
    if 'Request' in line and 'https://api.tebra.com' in line:
        current_endpoint = re.search(r'https://\S+', line).group()
    
    # Detect response fields header
    if 'Parent Field' in line and 'Field' in line and 'Type' in line:
        header_seen = True
        in_response = True
        i += 1
        continue
    
    # Parse response field rows
    if in_response and line:
        # Try to parse field rows - they have format: parent_field  field_name  type  description
        # Fields end when we hit another header or resource
        parts = re.split(r'\s{2,}', line)
        if len(parts) >= 3:
            parent = parts[0].strip()
            field_name = parts[1].strip()
            field_type = parts[2].strip()
            description = parts[3].strip() if len(parts) > 3 else ""
            
            # Skip if this looks like a header row or noise
            if field_name and field_type and field_name not in ('Field', 'N/A '):
                current_fields.append({
                    "parent": parent if parent != "N/A" else None,
                    "name": field_name,
                    "type": field_type,
                    "description": description
                })
    
    # End of response when we see copyright line or new resource
    if '© 2023 Tebra' in line or '© 2025 Tebra' in line:
        in_response = False
    
    i += 1

# Don't forget the last resource
if current_resource and current_fields:
    resources.append({
        "name": current_resource,
        "endpoint": current_endpoint,
        "fields": current_fields
    })

# Now let's do a more targeted parsing approach
# Parse each resource section more carefully
resources2 = []

# Split by the pattern of "Request    https://api.tebra.com/..."
sections = re.split(r'(?=\s+Request\s+https://api\.tebra\.com)', content)

for section in sections:
    url_match = re.search(r'https://api\.tebra\.com/clinical/v1/api/(\S+)', section)
    if not url_match:
        continue
    
    endpoint = url_match.group()
    resource_name = url_match.group(1)
    
    # Find response fields
    fields = []
    field_section = section.find('Response Fields')
    if field_section == -1:
        field_section = section.find('Parent Field')
    
    if field_section >= 0:
        field_content = section[field_section:]
        # Parse field rows
        field_lines = field_content.split('\n')
        for fl in field_lines:
            fl = fl.strip()
            if not fl or 'Parent Field' in fl or '© 20' in fl:
                continue
            parts = re.split(r'\s{2,}', fl)
            if len(parts) >= 3:
                parent = parts[0].strip()
                name = parts[1].strip()
                ftype = parts[2].strip()
                desc = ' '.join(parts[3:]).strip() if len(parts) > 3 else ""
                if name and ftype and name not in ('Field',):
                    fields.append({
                        "parent": parent if parent not in ("N/A", "") else None,
                        "name": name,
                        "type": ftype,
                        "description": desc
                    })
    
    resources2.append({
        "name": resource_name,
        "endpoint": endpoint,
        "field_count": len(fields),
        "fields": fields
    })

# Output
output = {
    "api_type": "Tebra General Clinical API (REST/JSON)",
    "base_url": "https://api.tebra.com/clinical/v1/api",
    "total_resources": len(resources2),
    "total_fields": sum(r["field_count"] for r in resources2),
    "resources": resources2
}

print(json.dumps(output, indent=2))

# Save
with open("general_api_inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\n\nSummary:")
print(f"Total resources: {output['total_resources']}")
print(f"Total fields: {output['total_fields']}")
for r in resources2:
    print(f"  {r['name']}: {r['field_count']} fields")
