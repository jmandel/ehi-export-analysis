#!/usr/bin/env python3
"""
Parse the OneTouch EMR FHIR API Documentation PDF text to extract:
- All 18 FHIR resource types documented
- Supported attributes (field names + descriptions) for each resource
- Search parameters for each resource
- Output: full-entity-inventory.json + summary statistics

The PDF text has a specific structure for each resource:
  - Resource name as header
  - Description paragraph
  - "The following attributes are supported:" header
  - Two-column table: Name | Comments (space-separated, with continuation lines)
  - "FHIR Operations" section
  - "Search Parameters" section with Name | Type | Description table
"""

import re
import json

PDF_TEXT_PATH = "pdf-text.txt"
OUTPUT_INVENTORY = "full-entity-inventory.json"
OUTPUT_SUMMARY = "summary-stats.txt"

RESOURCE_NAMES = [
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
    "Device", "DiagnosticReport", "DocumentReference", "Encounter",
    "Goal", "Immunization", "Location", "MedicationRequest",
    "Observation", "Organization", "Patient", "Practitioner",
    "Procedure", "Provenance"
]

def read_lines():
    with open(PDF_TEXT_PATH, 'r', encoding='utf-8') as f:
        return f.readlines()

def find_resource_sections(lines):
    """Find line ranges for each resource section."""
    sections = {}
    # Find where each resource section starts
    starts = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        for rn in RESOURCE_NAMES:
            # Match exact resource name (possibly with trailing whitespace)
            if stripped == rn or re.match(rf'^{rn}\s*$', stripped):
                # Avoid matching lines within JSON examples or URLs
                if '{' not in line and '/' not in line and '"' not in line and 'http' not in line.lower():
                    starts.append((rn, i))
    
    # Find section boundaries
    # Each resource ends when the next resource starts or at FHIR BULK DATA
    major_boundaries = []
    for i, line in enumerate(lines):
        # Skip TOC entries (those are in the first ~100 lines)
        if i > 100 and line.strip().startswith("FHIR BULK DATA ACCESS API"):
            major_boundaries.append(i)
            break
    
    for idx, (name, start) in enumerate(starts):
        if idx + 1 < len(starts):
            end = starts[idx + 1][1]
        elif major_boundaries:
            end = major_boundaries[0]
        else:
            end = len(lines)
        sections[name] = (start, end)
    
    return sections

def parse_attributes_table(lines, start, end):
    """Parse the supported attributes table from a resource section."""
    attributes = []
    
    # Find "The following attributes are supported:" or "Supported Attributes"
    attr_start = None
    for i in range(start, end):
        if "following attributes are supported" in lines[i].lower() or \
           "supported attributes" in lines[i].lower():
            attr_start = i + 1
            break
    
    if attr_start is None:
        return attributes
    
    # Find the Name/Comments header
    header_line = None
    for i in range(attr_start, min(attr_start + 10, end)):
        if 'Name' in lines[i] and 'Comments' in lines[i]:
            header_line = i
            break
    
    if header_line is None:
        return attributes
    
    # Find where attributes end (at "FHIR Operations" or "Search Parameters")
    attr_end = end
    for i in range(header_line + 1, end):
        stripped = lines[i].strip()
        if stripped.startswith("FHIR Operations") or \
           stripped.startswith("Search Parameters"):
            attr_end = i
            break
    
    # Parse attribute lines
    # Attributes start at a consistent column position
    # Name is in the left column, Comments in the right
    # Continuation lines are indented to the Comments column
    
    current_attr = None
    
    for i in range(header_line + 1, attr_end):
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:
            continue
        
        # Check if this line starts a new attribute (has text in the Name column)
        # The Name column starts around position 1-2, Comments around position 25-30
        # A new attribute has text starting near the left margin
        
        # Find where the text starts
        leading_spaces = len(line) - len(line.lstrip())
        
        # Detect if this is a new attribute or a continuation
        # New attributes typically have the name starting at column 1-5
        # Continuations are indented further (matching the Comments column)
        
        if leading_spaces < 15 and not stripped.startswith('('):
            # This looks like a new attribute line
            # Split by multiple spaces to separate name from comment
            parts = re.split(r'\s{3,}', stripped, maxsplit=1)
            if parts:
                if current_attr:
                    attributes.append(current_attr)
                current_attr = {
                    "name": parts[0].strip(),
                    "description": parts[1].strip() if len(parts) > 1 else ""
                }
        else:
            # Continuation line - append to current attribute's description
            if current_attr:
                current_attr["description"] += " " + stripped
    
    if current_attr:
        attributes.append(current_attr)
    
    # Clean up descriptions
    for attr in attributes:
        attr["description"] = attr["description"].strip()
        attr["has_description"] = bool(attr["description"])
    
    return attributes

def parse_search_params(lines, start, end):
    """Parse search parameters table from a resource section."""
    params = []
    
    # Find "Search Parameters" header (not inside FHIR Operations)
    sp_start = None
    for i in range(start, end):
        stripped = lines[i].strip()
        if stripped == "Search Parameters" or stripped.startswith("Search Parameters"):
            sp_start = i + 1
            break
    
    if sp_start is None:
        return params
    
    # Find the Name/Type/Description header
    header_line = None
    for i in range(sp_start, min(sp_start + 10, end)):
        if ('Name' in lines[i] or 'Key' in lines[i]) and \
           ('Type' in lines[i] or 'Description' in lines[i]):
            header_line = i
            break
    
    if header_line is None:
        return params
    
    # Find where search params end (at Example or next major section)
    sp_end = end
    for i in range(header_line + 1, end):
        stripped = lines[i].strip()
        if stripped.startswith("Example") or stripped.startswith("Read ") or \
           stripped.startswith("GET ") or stripped.startswith("POST "):
            sp_end = i
            break
    
    for i in range(header_line + 1, sp_end):
        stripped = lines[i].strip()
        if not stripped:
            continue
        
        parts = re.split(r'\s{3,}', stripped)
        if len(parts) >= 2:
            params.append({
                "name": parts[0].strip(),
                "type": parts[1].strip() if len(parts) > 1 else "",
                "description": parts[2].strip() if len(parts) > 2 else ""
            })
    
    return params

def extract_profiles(lines, start, end):
    """Extract US Core profile URLs from a resource section."""
    profiles = []
    text = ''.join(lines[start:end])
    for match in re.finditer(r'(http://[^\s]+StructureDefinition[^\s,)]+)', text):
        url = match.group(1).rstrip('.')
        if url not in profiles:
            profiles.append(url)
    return profiles

def main():
    lines = read_lines()
    sections = find_resource_sections(lines)
    
    resources = []
    for rn in RESOURCE_NAMES:
        if rn not in sections:
            print(f"WARNING: Could not find section for {rn}")
            continue
        
        start, end = sections[rn]
        attrs = parse_attributes_table(lines, start, end)
        search_params = parse_search_params(lines, start, end)
        profiles = extract_profiles(lines, start, end)
        
        resources.append({
            "name": rn,
            "attributes": attrs,
            "attribute_count": len(attrs),
            "search_parameters": search_params,
            "search_parameter_count": len(search_params),
            "us_core_profiles": profiles
        })
    
    # Summary
    total_attrs = sum(r["attribute_count"] for r in resources)
    total_with_desc = sum(
        sum(1 for a in r["attributes"] if a.get("has_description", False))
        for r in resources
    )
    total_search = sum(r["search_parameter_count"] for r in resources)
    
    inventory = {
        "product": "OneTouch EMR",
        "version": "3",
        "export_format": "FHIR R4 NDJSON (ZIP)",
        "export_mechanism": "UI-based single patient export; vendor-assisted all-patient export",
        "source_document": "OneTouchEMR_FHIR_Restful_API_Documentation_v3.pdf",
        "source_pages": 159,
        "resource_count": len(resources),
        "total_attributes": total_attrs,
        "attributes_with_descriptions": total_with_desc,
        "attributes_without_descriptions": total_attrs - total_with_desc,
        "description_coverage_pct": round(total_with_desc / total_attrs * 100, 1) if total_attrs > 0 else 0,
        "total_search_parameters": total_search,
        "resources": resources
    }
    
    with open(OUTPUT_INVENTORY, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Summary text
    summary_lines = [
        f"Total FHIR resources: {len(resources)}",
        f"Total attributes: {total_attrs}",
        f"Attributes with descriptions: {total_with_desc}",
        f"Attributes without descriptions: {total_attrs - total_with_desc}",
        f"Description coverage: {inventory['description_coverage_pct']}%",
        f"Total search parameters: {total_search}",
        "",
        "Per-resource breakdown:",
        f"{'Resource':<25} {'Attrs':>6} {'Described':>10} {'Search':>7} {'Profiles':>9}",
        "-" * 62,
    ]
    
    for r in resources:
        desc_count = sum(1 for a in r["attributes"] if a.get("has_description", False))
        summary_lines.append(
            f"{r['name']:<25} {r['attribute_count']:>6} {desc_count:>10} "
            f"{r['search_parameter_count']:>7} {len(r['us_core_profiles']):>9}"
        )
    
    summary = '\n'.join(summary_lines)
    with open(OUTPUT_SUMMARY, 'w') as f:
        f.write(summary)
    
    print(summary)

if __name__ == "__main__":
    main()
