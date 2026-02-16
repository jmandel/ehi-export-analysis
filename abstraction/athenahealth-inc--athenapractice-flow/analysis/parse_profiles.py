#!/usr/bin/env python3
"""Parse all FHIR StructureDefinition profiles from the athenahealth IG
and produce a complete entity inventory (full-entity-inventory.json)."""

import json
import os
import glob
import sys

DEFINITIONS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/athenahealth-inc--athenapractice-flow/downloads/definitions"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/athenahealth-inc--athenapractice-flow/analysis"
ENRICHMENT_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/athenahealth-inc--athenapractice-flow/downloads/enrichment"

def parse_profile(filepath):
    """Parse a single StructureDefinition profile JSON file."""
    with open(filepath) as f:
        sd = json.load(f)
    
    if sd.get("resourceType") != "StructureDefinition":
        return None
    
    # Only process profiles (not extensions)
    if sd.get("type") == "Extension" or "-extension-" in os.path.basename(filepath):
        return None
    
    profile_id = sd.get("id", "")
    name = sd.get("name", "")
    title = sd.get("title", "")
    base_type = sd.get("type", "")
    kind = sd.get("kind", "")
    description = sd.get("description", "")
    
    # Get snapshot elements
    snapshot_elements = sd.get("snapshot", {}).get("element", [])
    # Get differential elements (what athena customized)
    differential_elements = sd.get("differential", {}).get("element", [])
    
    fields = []
    for elem in snapshot_elements:
        path = elem.get("path", "")
        # Skip the root element
        if path == base_type or path == name or "." not in path:
            continue
        
        field_name = path.split(".")[-1] if "." in path else path
        
        # Get type info
        types = []
        for t in elem.get("type", []):
            type_code = t.get("code", "")
            target_profiles = t.get("targetProfile", [])
            types.append({
                "code": type_code,
                "targetProfile": target_profiles if target_profiles else None
            })
        
        # Get binding info
        binding = elem.get("binding")
        binding_info = None
        if binding:
            binding_info = {
                "strength": binding.get("strength", ""),
                "valueSet": binding.get("valueSet", ""),
                "description": binding.get("description", "")
            }
        
        field = {
            "path": path,
            "name": field_name,
            "short": elem.get("short", ""),
            "definition": elem.get("definition", ""),
            "min": elem.get("min"),
            "max": elem.get("max", ""),
            "types": types if types else None,
            "binding": binding_info,
            "isModifier": elem.get("isModifier", False),
            "isSummary": elem.get("isSummary", False),
            "mustSupport": elem.get("mustSupport", False),
        }
        
        # Clean up None values for compact output
        field = {k: v for k, v in field.items() if v is not None and v != "" and v != False and v != []}
        
        fields.append(field)
    
    return {
        "id": profile_id,
        "name": name,
        "title": title,
        "baseType": base_type,
        "kind": kind,
        "description": description,
        "totalSnapshotElements": len(snapshot_elements),
        "totalDifferentialElements": len(differential_elements),
        "fieldCount": len(fields),
        "fields": fields
    }


def categorize_profile(profile_id, name, coverage_data):
    """Use the coverage accounting data to categorize profiles."""
    categories = coverage_data.get("summary", {}).get("byCategory", {})
    for cat, profiles in categories.items():
        if name in profiles:
            return cat
    return "uncategorized"


def count_described_fields(fields):
    """Count fields that have a description beyond just a name."""
    count = 0
    for f in fields:
        short = f.get("short", "")
        definition = f.get("definition", "")
        if short or definition:
            count += 1
    return count


def count_typed_fields(fields):
    """Count fields that have type information."""
    return sum(1 for f in fields if f.get("types"))


def count_bound_fields(fields):
    """Count fields that have value set bindings."""
    return sum(1 for f in fields if f.get("binding"))


def main():
    # Load coverage accounting for categorization
    coverage_path = os.path.join(ENRICHMENT_DIR, "coverage-accounting.json")
    with open(coverage_path) as f:
        coverage_data = json.load(f)
    
    # Find all profile JSON files
    profile_files = sorted(glob.glob(os.path.join(DEFINITIONS_DIR, "StructureDefinition-athena-*-profile.json")))
    
    entities = []
    total_fields = 0
    total_described = 0
    total_typed = 0
    total_bound = 0
    parse_errors = []
    
    for filepath in profile_files:
        try:
            profile = parse_profile(filepath)
            if profile is None:
                continue
            
            category = categorize_profile(profile["id"], profile["name"], coverage_data)
            described = count_described_fields(profile["fields"])
            typed = count_typed_fields(profile["fields"])
            bound = count_bound_fields(profile["fields"])
            
            entity = {
                "id": profile["id"],
                "name": profile["name"],
                "title": profile["title"],
                "baseType": profile["baseType"],
                "kind": profile["kind"],
                "category": category,
                "description": profile["description"],
                "totalSnapshotElements": profile["totalSnapshotElements"],
                "fieldCount": profile["fieldCount"],
                "fieldsWithDescription": described,
                "fieldsWithTypes": typed,
                "fieldsWithBindings": bound,
                "fields": profile["fields"]
            }
            entities.append(entity)
            
            total_fields += profile["fieldCount"]
            total_described += described
            total_typed += typed
            total_bound += bound
            
        except Exception as e:
            parse_errors.append({
                "file": os.path.basename(filepath),
                "error": str(e),
                "parse_error": True
            })
    
    # Also look for non-standard profile files (custom resources)
    all_sd_files = sorted(glob.glob(os.path.join(DEFINITIONS_DIR, "StructureDefinition-*.json")))
    profile_basenames = {os.path.basename(f) for f in profile_files}
    
    for filepath in all_sd_files:
        basename = os.path.basename(filepath)
        if basename in profile_basenames:
            continue
        if "-extension-" in basename:
            continue
        # Check if it's a profile we missed
        try:
            with open(filepath) as f:
                sd = json.load(f)
            if sd.get("resourceType") != "StructureDefinition":
                continue
            if sd.get("type") == "Extension":
                continue
            if sd.get("kind") not in ("resource", "logical"):
                continue
            # This is a profile we missed
            profile = parse_profile(filepath)
            if profile:
                category = categorize_profile(profile["id"], profile["name"], coverage_data)
                described = count_described_fields(profile["fields"])
                typed = count_typed_fields(profile["fields"])
                bound = count_bound_fields(profile["fields"])
                entity = {
                    "id": profile["id"],
                    "name": profile["name"],
                    "title": profile["title"],
                    "baseType": profile["baseType"],
                    "kind": profile["kind"],
                    "category": category,
                    "description": profile["description"],
                    "totalSnapshotElements": profile["totalSnapshotElements"],
                    "fieldCount": profile["fieldCount"],
                    "fieldsWithDescription": described,
                    "fieldsWithTypes": typed,
                    "fieldsWithBindings": bound,
                    "fields": profile["fields"]
                }
                entities.append(entity)
                total_fields += profile["fieldCount"]
                total_described += described
                total_typed += typed
                total_bound += bound
        except Exception as e:
            pass
    
    # Count extensions
    extension_files = sorted(glob.glob(os.path.join(DEFINITIONS_DIR, "StructureDefinition-athena-*-extension-*.json")))
    
    # Build summary
    summary = {
        "totalEntities": len(entities),
        "totalFields": total_fields,
        "totalFieldsWithDescription": total_described,
        "totalFieldsWithTypes": total_typed,
        "totalFieldsWithBindings": total_bound,
        "descriptionCoverage": f"{total_described/total_fields*100:.1f}%" if total_fields > 0 else "N/A",
        "totalExtensionDefinitions": len(extension_files),
        "parseErrors": parse_errors,
        "byCategory": {}
    }
    
    # Group by category
    for entity in entities:
        cat = entity["category"]
        if cat not in summary["byCategory"]:
            summary["byCategory"][cat] = {"count": 0, "totalFields": 0, "entities": []}
        summary["byCategory"][cat]["count"] += 1
        summary["byCategory"][cat]["totalFields"] += entity["fieldCount"]
        summary["byCategory"][cat]["entities"].append(entity["title"])
    
    inventory = {
        "metadata": {
            "vendor": "athenahealth, Inc.",
            "products": ["athenaPractice", "athenaFlow"],
            "igVersion": "v25.0.0",
            "generatedDate": "2025-04-10",
            "sourceFormat": "FHIR R4 StructureDefinition profiles",
            "sourceDirectory": "definitions/"
        },
        "summary": summary,
        "entities": entities
    }
    
    # Write full inventory
    output_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary to stdout
    print(f"Total entities (profiles): {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({total_described/total_fields*100:.1f}%)")
    print(f"Fields with types: {total_typed} ({total_typed/total_fields*100:.1f}%)")
    print(f"Fields with value set bindings: {total_bound} ({total_bound/total_fields*100:.1f}%)")
    print(f"Extension definitions: {len(extension_files)}")
    print(f"Parse errors: {len(parse_errors)}")
    print()
    print("By category:")
    for cat, info in summary["byCategory"].items():
        print(f"  {cat}: {info['count']} entities, {info['totalFields']} fields")
        for e in info["entities"]:
            print(f"    - {e}")
    print()
    print(f"Output written to: {output_path}")


if __name__ == "__main__":
    main()
