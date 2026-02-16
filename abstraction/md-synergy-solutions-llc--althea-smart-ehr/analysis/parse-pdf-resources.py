#!/usr/bin/env python3
"""
Parse the Althea EHI Documentation PDF to extract all FHIR resource sections,
their JSON examples, and field inventories. Produces entity-inventory-full.json
and entity-inventory-summary.json.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "downloads" / "AltheaEHIDocumentation.pdf"
ENRICHMENT_PATH = Path(__file__).parent.parent / "downloads" / "enrichment" / "fhir-examples.json"
OUT_DIR = Path(__file__).parent

def extract_pdf_text():
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF_PATH), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_sections(text):
    """Parse the PDF text into sections based on headings from the TOC."""
    # Known section headings from the TOC
    section_headings = [
        "Patient", "Allergies and Intolerances", "Care Plan", "Care Team",
        "Condition", "Health Concern", "Implantable Device", "Diagnostic Report",
        "Document Reference", "Goal", "Immunization", "Medication Request",
        "Smoking Status Observation", "Pediatric Weight for Height Observation Tests",
        "Laboratory Result Observation", "Pediatric BMI for Age Observation",
        "Pulse Oximetry Tests",
        "Pediatric Head Occipital-frontal Circumference Percentile",
        "Observation Body Height", "Observation Body Temperature",
        "Observation Blood Pressure", "Observation Body Weight",
        "Observation Heart Rate", "Observation Respiratory Rate",
        "Procedure", "Claims", "Coverage", "Explanation of Benefits",
        "Export Current CCD"
    ]
    
    sections = []
    lines = text.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        stripped = line.strip()
        # Check if this line is a section heading
        matched = False
        for heading in section_headings:
            if stripped == heading:
                if current_section:
                    sections.append({
                        "name": current_section,
                        "content": '\n'.join(current_content)
                    })
                current_section = heading
                current_content = []
                matched = True
                break
        if not matched and current_section:
            current_content.append(line)
    
    if current_section:
        sections.append({
            "name": current_section,
            "content": '\n'.join(current_content)
        })
    
    return sections

def extract_json_blocks(text):
    """Extract JSON blocks from text using brace matching."""
    blocks = []
    i = 0
    while i < len(text):
        if text[i] == '{':
            depth = 0
            start = i
            while i < len(text):
                if text[i] == '{':
                    depth += 1
                elif text[i] == '}':
                    depth -= 1
                    if depth == 0:
                        block_text = text[start:i+1]
                        try:
                            parsed = json.loads(block_text)
                            blocks.append(parsed)
                        except json.JSONDecodeError:
                            # Try cleaning common PDF artifacts
                            cleaned = re.sub(r'\s+', ' ', block_text)
                            try:
                                parsed = json.loads(cleaned)
                                blocks.append(parsed)
                            except json.JSONDecodeError:
                                pass
                        break
                i += 1
        i += 1
    return blocks

def map_section_to_resource_type(section_name):
    """Map section names to FHIR resource types."""
    mapping = {
        "Patient": "Patient",
        "Allergies and Intolerances": "AllergyIntolerance",
        "Care Plan": "CarePlan",
        "Care Team": "CareTeam",
        "Condition": "Condition",
        "Health Concern": "Condition",
        "Implantable Device": "Device",
        "Diagnostic Report": "DiagnosticReport",
        "Document Reference": "DocumentReference",
        "Goal": "Goal",
        "Immunization": "Immunization",
        "Medication Request": "MedicationRequest",
        "Smoking Status Observation": "Observation",
        "Pediatric Weight for Height Observation Tests": "Observation",
        "Laboratory Result Observation": "Observation",
        "Pediatric BMI for Age Observation": "Observation",
        "Pulse Oximetry Tests": "Observation",
        "Pediatric Head Occipital-frontal Circumference Percentile": "Observation",
        "Observation Body Height": "Observation",
        "Observation Body Temperature": "Observation",
        "Observation Blood Pressure": "Observation",
        "Observation Body Weight": "Observation",
        "Observation Heart Rate": "Observation",
        "Observation Respiratory Rate": "Observation",
        "Procedure": "Procedure",
        "Claims": "Claim",
        "Coverage": "Coverage",
        "Explanation of Benefits": "ExplanationOfBenefit",
        "Export Current CCD": None,
    }
    return mapping.get(section_name, None)

def extract_fields_from_example(example, prefix=""):
    """Recursively extract all field paths from a FHIR example."""
    fields = []
    if isinstance(example, dict):
        for key, value in example.items():
            full_path = f"{prefix}.{key}" if prefix else key
            field_type = type(value).__name__
            if isinstance(value, dict):
                fields.append({"path": full_path, "type": "object", "example_value": None})
                fields.extend(extract_fields_from_example(value, full_path))
            elif isinstance(value, list):
                fields.append({"path": full_path, "type": "array", "example_value": None})
                if value:
                    fields.extend(extract_fields_from_example(value[0], f"{full_path}[]"))
            else:
                fields.append({
                    "path": full_path,
                    "type": field_type,
                    "example_value": str(value) if value is not None else None
                })
    return fields

def main():
    # Load pre-extracted examples from enrichment
    with open(ENRICHMENT_PATH) as f:
        enrichment_examples = json.load(f)
    
    # Also parse PDF text to get section structure
    pdf_text = extract_pdf_text()
    sections = parse_sections(pdf_text)
    
    # Build entity inventory from enrichment examples (more reliable parsing)
    entities = {}
    
    for example in enrichment_examples:
        rt = example.get("resourceType", "unknown")
        section = example.get("section", rt)
        
        if rt not in entities:
            entities[rt] = {
                "resource_type": rt,
                "section_names": [],
                "example_count": 0,
                "fields": {},
                "has_us_core_link": True,  # All sections reference US Core
                "has_data_dictionary": False,
                "has_field_descriptions": False,
            }
        
        if section not in entities[rt]["section_names"]:
            entities[rt]["section_names"].append(section)
        entities[rt]["example_count"] += 1
        
        # Extract fields from this example
        fields = extract_fields_from_example(example.get("json", example))
        for field in fields:
            path = field["path"]
            if path not in entities[rt]["fields"]:
                entities[rt]["fields"][path] = {
                    "path": path,
                    "type": field["type"],
                    "description": None,  # No descriptions in the PDF
                    "example_value": field.get("example_value"),
                }
            elif field.get("example_value") and not entities[rt]["fields"][path].get("example_value"):
                entities[rt]["fields"][path]["example_value"] = field["example_value"]
    
    # Map to USCDI categories
    uscdi_mapping = {
        "Patient": "Demographics",
        "AllergyIntolerance": "Allergies & Intolerances",
        "CarePlan": "Assessment & Plan of Treatment",
        "CareTeam": "Care Team Members",
        "Condition": "Problems / Conditions",
        "Device": "Medical Devices",
        "DiagnosticReport": "Diagnostic Imaging / Clinical Tests",
        "DocumentReference": "Clinical Notes",
        "Goal": "Goals & Preferences",
        "Immunization": "Immunizations",
        "MedicationRequest": "Medications",
        "Observation": "Vitals / Labs / Clinical Tests",
        "Procedure": "Procedures",
        "Claim": "Claims / Billing",
        "Coverage": "Insurance / Coverage",
        "ExplanationOfBenefit": "Claims / Billing",
    }
    
    # Build full inventory
    inventory = []
    for rt, data in sorted(entities.items()):
        field_list = list(data["fields"].values())
        entity = {
            "entity_name": rt,
            "resource_type": rt,
            "section_names": data["section_names"],
            "example_count": data["example_count"],
            "field_count": len(field_list),
            "fields_with_descriptions": 0,  # None have descriptions
            "fields_with_types": len([f for f in field_list if f["type"]]),
            "fields_with_examples": len([f for f in field_list if f.get("example_value")]),
            "uscdi_category": uscdi_mapping.get(rt, "Other"),
            "documentation_quality": "example-only",
            "fields": field_list,
        }
        inventory.append(entity)
    
    # Write full inventory
    with open(OUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Build summary
    total_entities = len(inventory)
    total_fields = sum(e["field_count"] for e in inventory)
    total_with_descriptions = 0  # None
    total_with_examples = sum(e["fields_with_examples"] for e in inventory)
    total_examples = sum(e["example_count"] for e in inventory)
    
    # Category breakdown
    categories = {}
    for e in inventory:
        cat = e["uscdi_category"]
        if cat not in categories:
            categories[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += e["field_count"]
        categories[cat]["entities"].append(e["entity_name"])
    
    summary = {
        "product": "Althea Smart EHR",
        "source_artifact": "AltheaEHIDocumentation.pdf",
        "source_pages": 108,
        "total_resource_types": total_entities,
        "total_fields_observed": total_fields,
        "fields_with_descriptions": total_with_descriptions,
        "fields_with_descriptions_pct": 0.0,
        "fields_with_example_values": total_with_examples,
        "total_fhir_examples": total_examples,
        "documentation_type": "FHIR JSON examples only — no data dictionary, no field descriptions, no schema",
        "export_format": "FHIR R4 JSON (bulk zip)",
        "also_supports": "C-CDA (CCD export)",
        "category_breakdown": categories,
        "resource_type_summary": [
            {
                "resource_type": e["entity_name"],
                "sections": e["section_names"],
                "example_count": e["example_count"],
                "field_count": e["field_count"],
                "uscdi_category": e["uscdi_category"],
            }
            for e in inventory
        ],
        "notes": [
            "No data dictionary or field-level documentation exists — only FHIR JSON examples",
            "All sections link to US Core profiles with no product-specific documentation",
            "Export includes 3 financial resource types (Claim, Coverage, ExplanationOfBenefit) beyond standard USCDI",
            "No Encounter resource despite being a core USCDI requirement",
            "DocumentReference examples contain base64-encoded CDA documents",
        ]
    }
    
    with open(OUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary for console
    print(f"Total resource types: {total_entities}")
    print(f"Total fields observed across examples: {total_fields}")
    print(f"Fields with descriptions: {total_with_descriptions} (0%)")
    print(f"Fields with example values: {total_with_examples}")
    print(f"Total FHIR examples: {total_examples}")
    print(f"\nCategory breakdown:")
    for cat, data in sorted(categories.items()):
        print(f"  {cat}: {data['entity_count']} entities, {data['field_count']} fields — {', '.join(data['entities'])}")

if __name__ == "__main__":
    main()
