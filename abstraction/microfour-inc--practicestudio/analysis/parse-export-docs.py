#!/usr/bin/env python3
"""
Parse all PracticeStudio EHI export documentation artifacts.

Extracts:
- Export process page content (the (b)(10) documentation)
- CCD sections from interoperability page
- FHIR API resources and their parameters/example data
- Produces entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT_DIR = Path(".")

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.text.append(t)

def extract_text(filepath):
    with open(filepath, 'r', errors='replace') as f:
        p = TextExtractor()
        p.feed(f.read())
        return p.text

def parse_export_process():
    """Parse the (b)(10) export process page."""
    lines = extract_text(DOWNLOADS / "ExportProcess.html")
    # Find the actual export content
    content = None
    for i, line in enumerate(lines):
        if line == "Export Process":
            if i + 1 < len(lines):
                content = lines[i + 1]
                break
    return {
        "page_title": "Export Process",
        "content": content or "Not found",
        "source_file": "ExportProcess.html"
    }

def parse_interoperability():
    """Parse the interoperability page for CCD sections."""
    lines = extract_text(DOWNLOADS / "Interoperability.html")
    
    ccd_sections = []
    in_ccd = False
    ccd_intro = None
    
    for i, line in enumerate(lines):
        if "CCD contains the following sections" in line or "A CCD contains the following" in line:
            in_ccd = True
            ccd_intro = line
            continue
        if in_ccd:
            # CCD sections are listed after the intro line
            # They end when we hit something that's not a section name
            if line in ["Advance Directives", "Alerts", "Encounters", "Family History",
                       "Functional Status", "Immunizations", "Medical Equipment", 
                       "Medications", "Payers", "Plan of Care", "Problems", 
                       "Procedures", "Purpose", "Results", "Social History", "Vital Signs"]:
                ccd_sections.append(line)
            elif len(ccd_sections) > 0:
                break
    
    return {
        "ccd_section_count": len(ccd_sections),
        "ccd_sections": ccd_sections,
        "ccd_description": ccd_intro,
        "source_file": "Interoperability.html"
    }

def parse_fhir_resource(filepath):
    """Parse a FHIR API documentation page to extract resource details."""
    lines = extract_text(filepath)
    
    resource_name = filepath.stem.replace("Documentation", "")
    
    # Look for parameter tables and example data
    parameters = []
    has_example = False
    example_data = None
    
    # Read the raw HTML to find tables and JSON examples
    with open(filepath, 'r', errors='replace') as f:
        html_content = f.read()
    
    # Check for example JSON responses
    if '"resourceType"' in html_content:
        has_example = True
        # Extract example JSON
        json_matches = re.findall(r'\{[^{}]*"resourceType"[^{}]*\}', html_content[:5000])
        if json_matches:
            example_data = json_matches[0][:200] + "..."
    
    # Count table rows for parameters
    param_count = html_content.count('<tr')
    
    # Extract field names from example JSON responses
    fields = set()
    json_blocks = re.findall(r'"(\w+)":', html_content)
    for field in json_blocks:
        if field not in ('resourceType', 'meta', 'link', 'relation', 'self', 'type',
                        'system', 'code', 'display', 'userSelected', 'coding',
                        'entry', 'total', 'lastUpdated', 'profile', 'searchset',
                        'Bundle', 'reference', 'text', 'value', 'url', 'extension'):
            fields.add(field)
    
    return {
        "resource_type": resource_name,
        "source_file": filepath.name,
        "file_size_bytes": filepath.stat().st_size,
        "has_example_response": has_example,
        "fields_in_examples": sorted(list(fields)),
        "field_count": len(fields),
    }

def build_entity_inventory():
    """Build the complete entity inventory from all sources."""
    
    export_process = parse_export_process()
    interop = parse_interoperability()
    
    # Parse FHIR API docs
    fhir_dir = DOWNLOADS / "fhir-api-docs"
    fhir_resources = []
    if fhir_dir.exists():
        for f in sorted(fhir_dir.glob("Documentation*.html")):
            if "Authorization" in f.name:
                continue  # Skip auth docs, not a resource
            resource = parse_fhir_resource(f)
            fhir_resources.append(resource)
    
    # Build entities from CCD sections (the actual b10 export format)
    ccd_entities = []
    for section in interop["ccd_sections"]:
        ccd_entities.append({
            "entity_name": section,
            "entity_type": "CCD Section",
            "source": "CCD Export (b)(10)",
            "fields": [],
            "field_count": 0,
            "description": f"Standard CCD section: {section}",
            "has_field_descriptions": False,
            "has_field_types": False,
        })
    
    # Build entities from FHIR resources (the g10 API, NOT the b10 export)
    fhir_entities = []
    for r in fhir_resources:
        fhir_entities.append({
            "entity_name": r["resource_type"],
            "entity_type": "FHIR Resource",
            "source": "FHIR API (g)(10)",
            "fields": [{"name": f, "type": None, "description": None} for f in r["fields_in_examples"]],
            "field_count": r["field_count"],
            "description": f"FHIR R4 {r['resource_type']} resource via (g)(10) API",
            "has_example_response": r["has_example_response"],
            "has_field_descriptions": False,
            "has_field_types": False,
        })
    
    inventory = {
        "product": "PracticeStudio",
        "vendor": "MicroFour, Inc.",
        "export_type": "CCD (Continuity of Care Document)",
        "export_description": export_process["content"],
        "export_mechanism": "Contact MicroFour technical support for mass CCD export",
        "b10_export": {
            "format": "CCD (C-CDA)",
            "entity_count": len(ccd_entities),
            "entities": ccd_entities,
            "documentation_detail": "No data dictionary. Single paragraph description. Lists 16 standard CCD sections from interoperability page.",
        },
        "g10_fhir_api": {
            "format": "FHIR R4",
            "resource_count": len(fhir_entities),
            "resources": fhir_entities,
            "note": "This is the (g)(10) FHIR API, NOT the (b)(10) EHI export. Included for context.",
        },
        "total_documented_entities": len(ccd_entities),
        "total_documented_fields": 0,  # No field-level documentation for CCD export
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_machine_readable_schema": False,
    }
    
    return inventory

def build_summary(inventory):
    """Build summary statistics from the full inventory."""
    return {
        "product": inventory["product"],
        "vendor": inventory["vendor"],
        "export_format": inventory["export_type"],
        "export_mechanism": inventory["export_mechanism"],
        "b10_entity_count": inventory["b10_export"]["entity_count"],
        "b10_entities": [e["entity_name"] for e in inventory["b10_export"]["entities"]],
        "b10_total_fields_documented": 0,
        "b10_fields_with_descriptions": 0,
        "b10_fields_with_types": 0,
        "g10_fhir_resource_count": inventory["g10_fhir_api"]["resource_count"],
        "g10_fhir_resources": [r["entity_name"] for r in inventory["g10_fhir_api"]["resources"]],
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_machine_readable_schema": False,
        "documentation_quality": "Minimal - single paragraph with no data dictionary",
        "ccd_sections": inventory["b10_export"]["entities"],
        "ccd_section_count": len(inventory["b10_export"]["entities"]),
    }

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    
    inventory = build_entity_inventory()
    summary = build_summary(inventory)
    
    with open(OUTPUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(OUTPUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("=== PracticeStudio EHI Export Analysis ===")
    print(f"Export format: {inventory['export_type']}")
    print(f"Export mechanism: {inventory['export_mechanism']}")
    print(f"(b)(10) entities (CCD sections): {inventory['b10_export']['entity_count']}")
    print(f"Total documented fields: {inventory['total_documented_fields']}")
    print(f"Has data dictionary: {inventory['has_data_dictionary']}")
    print(f"Has sample data: {inventory['has_sample_data']}")
    print()
    print("CCD Sections in (b)(10) export:")
    for e in inventory["b10_export"]["entities"]:
        print(f"  - {e['entity_name']}")
    print()
    print(f"(g)(10) FHIR resources (for context): {inventory['g10_fhir_api']['resource_count']}")
    for r in inventory["g10_fhir_api"]["resources"]:
        print(f"  - {r['entity_name']} ({r['field_count']} fields in examples)")
    print()
    print(f"Saved: entity-inventory-full.json, entity-inventory-summary.json")
