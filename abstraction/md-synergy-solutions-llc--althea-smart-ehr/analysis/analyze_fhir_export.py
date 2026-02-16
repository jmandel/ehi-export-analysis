#!/usr/bin/env python3
"""
Analyze the Althea Smart EHR FHIR export documentation.
Parses extracted FHIR examples and PDF text to produce a full entity inventory.
"""

import json
import subprocess
import re
from pathlib import Path
from collections import defaultdict

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/md-synergy-solutions-llc--althea-smart-ehr")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/md-synergy-solutions-llc--althea-smart-ehr/analysis")

def extract_pdf_text():
    """Extract full text from the PDF."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(RESULTS_DIR / "downloads/AltheaEHIDocumentation.pdf"), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def load_fhir_examples():
    """Load the pre-extracted FHIR examples."""
    with open(RESULTS_DIR / "downloads/enrichment/fhir-examples.json") as f:
        return json.load(f)

def load_extraction_summary():
    """Load the extraction summary."""
    with open(RESULTS_DIR / "downloads/enrichment/extraction-summary.json") as f:
        return json.load(f)

def count_fields_recursive(obj, prefix=""):
    """Recursively count all unique field paths in a FHIR resource."""
    fields = set()
    if isinstance(obj, dict):
        for key, val in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            fields.add(path)
            if isinstance(val, dict):
                fields.update(count_fields_recursive(val, path))
            elif isinstance(val, list) and val:
                # Explore first element for structure
                if isinstance(val[0], dict):
                    fields.update(count_fields_recursive(val[0], path))
    return fields

def analyze_resource_fields(examples):
    """For each resource type, collect all unique fields seen across examples."""
    resource_fields = defaultdict(set)
    resource_examples = defaultdict(list)
    
    for ex in examples:
        rt = ex["resourceType"]
        resource_examples[rt].append(ex["json"])
        fields = count_fields_recursive(ex["json"])
        resource_fields[rt].update(fields)
    
    return resource_fields, resource_examples

def get_section_info(pdf_text):
    """Parse the table of contents to get all sections and their page numbers."""
    toc_sections = []
    lines = pdf_text.split("\n")
    in_toc = False
    for line in lines:
        # TOC entries have section name followed by page number
        m = re.match(r'\s{2,}(.+?)\s{2,}(\d+)\s*$', line)
        if m:
            name = m.group(1).strip()
            page = int(m.group(2))
            if name and page > 0:
                toc_sections.append({"name": name, "page": page})
                in_toc = True
        elif in_toc and line.strip() == "":
            continue
        elif in_toc and not line.strip().startswith("Althea") and line.strip():
            # End of TOC
            pass
    return toc_sections

def build_full_inventory(examples, summary):
    """Build the full entity inventory JSON."""
    resource_fields, resource_examples = analyze_resource_fields(examples)
    
    inventory = {
        "export_format": "FHIR R4 JSON",
        "export_mechanism": "Bulk export via download link (ZIP file)",
        "secondary_format": "C-CDA (CCD)",
        "documentation_type": "Examples only - no data dictionary or schema",
        "total_resource_types": len(resource_fields),
        "total_examples": len(examples),
        "total_unique_field_paths": sum(len(f) for f in resource_fields.values()),
        "parse_failures": summary.get("parse_failures", []),
        "resource_types": []
    }
    
    # Map sections to categories
    section_categories = {
        "Patient": "Demographics",
        "AllergyIntolerance": "Clinical - Allergies",
        "CarePlan": "Clinical - Care Planning",
        "CareTeam": "Clinical - Care Planning",
        "Condition": "Clinical - Problems/Diagnoses",
        "Goal": "Clinical - Care Planning",
        "Immunization": "Clinical - Immunizations",
        "MedicationRequest": "Clinical - Medications",
        "Observation": "Clinical - Observations/Vitals/Labs",
        "Procedure": "Clinical - Procedures",
        "Claim": "Financial - Claims",
        "Coverage": "Financial - Insurance",
        "ExplanationOfBenefit": "Financial - Payment/Adjudication",
    }
    
    # Observation subtypes from sections
    observation_subtypes = {}
    for ex in examples:
        if ex["resourceType"] == "Observation":
            section = ex["section"]
            obs_id = ex["id"]
            code = ex["json"].get("code", {})
            coding = code.get("coding", [{}])[0] if code.get("coding") else {}
            observation_subtypes[obs_id] = {
                "section": section,
                "loinc_code": coding.get("code", ""),
                "display": coding.get("display", "")
            }
    
    for rt, fields in sorted(resource_fields.items()):
        rt_examples = resource_examples[rt]
        
        # Collect all field paths with their types from examples
        field_details = []
        for fp in sorted(fields):
            # Determine type from first example that has this field
            field_type = "unknown"
            sample_value = None
            for ex in rt_examples:
                val = get_nested_value(ex, fp)
                if val is not None:
                    field_type = type(val).__name__
                    if isinstance(val, str) and len(val) > 100:
                        sample_value = val[:100] + "..."
                    else:
                        sample_value = val
                    break
            
            field_details.append({
                "path": fp,
                "type": field_type,
                "sample_value": str(sample_value) if sample_value is not None else None,
                "description": None  # No descriptions in examples-only documentation
            })
        
        resource_entry = {
            "resource_type": rt,
            "category": section_categories.get(rt, "Other"),
            "example_count": summary["resource_type_counts"].get(rt, 0),
            "unique_field_paths": len(fields),
            "fields_with_descriptions": 0,  # None have descriptions
            "fields_with_types": len(fields),  # Types can be inferred from examples
            "fields": field_details
        }
        
        # Add observation subtypes if applicable
        if rt == "Observation":
            sections_for_obs = set(ex["section"] for ex in examples if ex["resourceType"] == "Observation")
            resource_entry["observation_subtypes"] = sorted(sections_for_obs)
        
        inventory["resource_types"].append(resource_entry)
    
    # Add entries for parse failures (sections with no extracted examples)
    for failure in summary.get("parse_failures", []):
        section_name = failure["section"]
        # Map section names to FHIR resource types
        section_to_rt = {
            "Implantable Device": "Device",
            "Diagnostic Report": "DiagnosticReport",
            "Document Reference": "DocumentReference",
            "Observation Body Temperature": "Observation (Body Temperature)",
            "Observation Body Weight": "Observation (Body Weight)",
        }
        rt = section_to_rt.get(section_name, section_name)
        category_map = {
            "Device": "Clinical - Devices",
            "DiagnosticReport": "Clinical - Diagnostic Reports",
            "DocumentReference": "Clinical - Documents",
            "Observation (Body Temperature)": "Clinical - Observations/Vitals/Labs",
            "Observation (Body Weight)": "Clinical - Observations/Vitals/Labs",
        }
        
        inventory["resource_types"].append({
            "resource_type": rt,
            "category": category_map.get(rt, "Other"),
            "example_count": 0,
            "unique_field_paths": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "fields": [],
            "parse_failure": True,
            "parse_error": failure["error"],
            "note": f"Section '{section_name}' exists in PDF but JSON examples could not be extracted"
        })
    
    return inventory

def get_nested_value(obj, path):
    """Get a value from a nested dict using dot-separated path."""
    parts = path.split(".")
    current = obj
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and current:
            if isinstance(current[0], dict) and part in current[0]:
                current = current[0][part]
            else:
                return None
        else:
            return None
    return current

def generate_summary_stats(inventory):
    """Generate summary statistics."""
    stats = {
        "total_resource_types_documented": inventory["total_resource_types"],
        "total_resource_types_with_parse_failures": len([r for r in inventory["resource_types"] if r.get("parse_failure")]),
        "total_resource_types_including_failed": len(inventory["resource_types"]),
        "total_examples": inventory["total_examples"],
        "total_unique_field_paths": inventory["total_unique_field_paths"],
        "fields_with_descriptions": 0,
        "pct_fields_with_descriptions": 0.0,
        "by_category": {},
    }
    
    for rt in inventory["resource_types"]:
        cat = rt["category"]
        if cat not in stats["by_category"]:
            stats["by_category"][cat] = {
                "resource_count": 0,
                "total_fields": 0,
                "examples": 0,
            }
        stats["by_category"][cat]["resource_count"] += 1
        stats["by_category"][cat]["total_fields"] += rt["unique_field_paths"]
        stats["by_category"][cat]["examples"] += rt["example_count"]
    
    return stats

def main():
    print("Loading FHIR examples...")
    examples = load_fhir_examples()
    summary = load_extraction_summary()
    
    print(f"Loaded {len(examples)} examples across {len(summary['resource_type_counts'])} resource types")
    print(f"Parse failures: {len(summary['parse_failures'])} sections")
    
    print("\nExtracting PDF text for section analysis...")
    pdf_text = extract_pdf_text()
    toc_sections = get_section_info(pdf_text)
    print(f"Found {len(toc_sections)} TOC sections")
    
    print("\nBuilding full entity inventory...")
    inventory = build_full_inventory(examples, summary)
    
    # Save full inventory
    inv_path = OUTPUT_DIR / "full-entity-inventory.json"
    with open(inv_path, "w") as f:
        json.dump(inventory, f, indent=2, default=str)
    print(f"Saved inventory to {inv_path}")
    
    # Generate and save summary stats
    stats = generate_summary_stats(inventory)
    stats_path = OUTPUT_DIR / "summary-stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved stats to {stats_path}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Resource types with examples: {inventory['total_resource_types']}")
    print(f"Resource types with parse failures: {len(inventory['resource_types']) - inventory['total_resource_types']}")
    print(f"Total examples extracted: {inventory['total_examples']}")
    print(f"Total unique field paths: {inventory['total_unique_field_paths']}")
    print(f"Fields with descriptions: 0 (examples-only documentation)")
    print()
    
    print("By category:")
    for cat, data in sorted(stats["by_category"].items()):
        print(f"  {cat}: {data['resource_count']} types, {data['total_fields']} fields, {data['examples']} examples")
    
    print("\nParse failures (sections in PDF but examples not extractable):")
    for f in summary["parse_failures"]:
        print(f"  - {f['section']}: {f['error']}")
    
    # Save TOC sections
    toc_path = OUTPUT_DIR / "pdf-toc-sections.json"
    with open(toc_path, "w") as f:
        json.dump(toc_sections, f, indent=2)
    print(f"\nSaved TOC sections to {toc_path}")

if __name__ == "__main__":
    main()
