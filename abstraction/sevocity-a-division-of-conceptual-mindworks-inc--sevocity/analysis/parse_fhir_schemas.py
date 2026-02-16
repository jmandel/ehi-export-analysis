#!/usr/bin/env python3
"""
Parse all Sevocity FHIR OpenAPI schema YAML files and examples to produce
a full entity inventory for the EHI export analysis.
"""

import yaml
import json
import os
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/sevocity-a-division-of-conceptual-mindworks-inc--sevocity/downloads")
SCHEMA_DIR = RESULTS_DIR / "fhir-api-docs" / "components" / "schemas"
EXAMPLE_DIR = RESULTS_DIR / "fhir-api-docs" / "examples"
PATHS_DIR = RESULTS_DIR / "fhir-api-docs" / "paths"
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/sevocity-a-division-of-conceptual-mindworks-inc--sevocity/analysis")

def count_fields(schema, prefix=""):
    """Recursively count leaf fields in an OpenAPI schema object."""
    fields = []
    if not isinstance(schema, dict):
        return fields
    
    props = schema.get("properties", {})
    for name, prop in props.items():
        full_name = f"{prefix}.{name}" if prefix else name
        field_type = prop.get("type", "unknown")
        
        if field_type == "object":
            # Has nested properties
            children = count_fields(prop, full_name)
            if children:
                fields.extend(children)
            else:
                fields.append({"name": full_name, "type": field_type, "leaf": True})
        elif field_type == "array":
            items = prop.get("items", {})
            if items.get("type") == "object":
                children = count_fields(items, full_name + "[]")
                if children:
                    fields.extend(children)
                else:
                    fields.append({"name": full_name, "type": "array", "leaf": True})
            else:
                fields.append({"name": full_name, "type": f"array<{items.get('type', 'unknown')}>", "leaf": True})
        else:
            fields.append({"name": full_name, "type": field_type, "leaf": True})
    
    return fields

def parse_schema_file(filepath):
    """Parse a single YAML schema file."""
    with open(filepath) as f:
        schema = yaml.safe_load(f)
    if not schema:
        return None
    return schema

def get_resource_type_from_filename(filename):
    """Extract resource type from schema filename."""
    name = filename.replace(".yml", "").replace(".YML", "")
    # Remove READ/SEARCH prefixes
    for prefix in ["READ", "SEARCH"]:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name

def classify_resource(resource_type):
    """Classify a FHIR resource into an EHI domain category."""
    categories = {
        "PATIENT": "Demographics",
        "RELATEDPERSON": "Demographics",
        "ENCOUNTER": "Encounters / Visits",
        "CONDITION": "Problems / Conditions",
        "ALLERGYINTOLERANCE": "Allergies",
        "MEDICATION": "Medications",
        "MEDICATIONREQUEST": "Medications",
        "MEDICATIONSTATEMENT": "Medications",
        "MEDICATIONDISPENSE": "Medications",
        "IMMUNIZATION": "Immunizations",
        "OBSERVATION": "Vitals / Lab Results / Social History",
        "DIAGNOSTICREPORT": "Lab Results / Diagnostic Reports",
        "PROCEDURE": "Procedures",
        "CAREPLAN": "Care Plans / Goals",
        "GOAL": "Care Plans / Goals",
        "CARETEAM": "Care Plans / Goals",
        "DOCUMENTREFERENCE": "Clinical Notes / Documents",
        "COVERAGE": "Insurance / Coverage",
        "SERVICEREQUEST": "Orders / Referrals",
        "APPOINTMENT": "Encounters / Visits",
        "QUESTIONNAIRE": "Clinical Assessments",
        "QUESTIONNAIRERESPONSE": "Clinical Assessments",
        "PROVENANCE": "Provenance / Metadata",
        "ORGANIZATION": "Administrative",
        "PRACTITIONER": "Administrative",
        "LOCATION": "Administrative",
        "ENDPOINT": "Administrative",
        "DEVICE": "Devices",
    }
    return categories.get(resource_type.upper(), "Other")

def is_certified_g10(resource_type):
    """Check if a resource type is certified under (g)(10)."""
    certified = {
        "ALLERGYINTOLERANCE", "CAREPLAN", "CARETEAM", "CONDITION", "COVERAGE",
        "DEVICE", "DIAGNOSTICREPORT", "DOCUMENTREFERENCE", "ENCOUNTER",
        "ENDPOINT", "GOAL", "IMMUNIZATION", "LOCATION", "MEDICATION",
        "MEDICATIONDISPENSE", "MEDICATIONREQUEST", "OBSERVATION",
        "ORGANIZATION", "PATIENT", "PRACTITIONER", "PROCEDURE", "PROVENANCE"
    }
    return resource_type.upper() in certified

def main():
    inventory = {
        "extraction_date": "2026-02-16",
        "source": "Sevocity FHIR OpenAPI 3.0.1 Specification",
        "spec_version": "1.0.0",
        "fhir_version": "R4",
        "us_core_version": "STU6.1.0",
        "resources": [],
        "summary": {}
    }

    # Parse main spec for tags
    main_spec_path = RESULTS_DIR / "openAPIDocs.yml"
    with open(main_spec_path) as f:
        main_spec = yaml.safe_load(f)
    
    tags = {t["name"]: t.get("description", "") for t in main_spec.get("tags", [])}

    # Parse all schema files
    schema_files = sorted(SCHEMA_DIR.glob("*.yml")) + sorted(SCHEMA_DIR.glob("*.YML"))
    
    # Group schemas by resource type (READ vs SEARCH variants)
    resource_schemas = {}
    for sf in schema_files:
        fname = sf.name.upper().replace(".YML", "")
        schema = parse_schema_file(sf)
        if not schema:
            continue
        
        if fname.startswith("READ"):
            rtype = fname[4:]
            if rtype not in resource_schemas:
                resource_schemas[rtype] = {}
            resource_schemas[rtype]["read_schema"] = schema
            resource_schemas[rtype]["read_file"] = sf.name
        elif fname.startswith("SEARCH"):
            rtype = fname[6:]
            # Normalize some names
            rtype = rtype.rstrip("S")  # SEARCHGOALS -> GOAL, SEARCHDEVICES -> DEVICE
            if rtype == "ALLENDPOINT":
                rtype = "ENDPOINT"
            if rtype not in resource_schemas:
                resource_schemas[rtype] = {}
            resource_schemas[rtype]["search_schema"] = schema
            resource_schemas[rtype]["search_file"] = sf.name
        elif fname == "METADATA":
            resource_schemas["METADATA"] = {"read_schema": schema, "read_file": sf.name}
        elif fname == "FHIR-JSON-RESOURCE":
            continue  # Generic passthrough
        elif fname == "PROVENANCE":
            resource_schemas["PROVENANCE"] = {"read_schema": schema, "read_file": sf.name}
        elif fname == "APPOINTMENT":
            resource_schemas["APPOINTMENT"] = {"read_schema": schema, "read_file": sf.name}
        else:
            # Other schema files
            if fname not in resource_schemas:
                resource_schemas[fname] = {}
            resource_schemas[fname]["read_schema"] = schema
            resource_schemas[fname]["read_file"] = sf.name

    # Parse examples
    examples = {}
    for ef in sorted(EXAMPLE_DIR.glob("*.yml")):
        with open(ef) as f:
            example = yaml.safe_load(f)
        examples[ef.stem] = example

    # Also check search schemas for appointment, coverage, questionnaire variants
    search_files = sorted(SCHEMA_DIR.glob("SEARCH*.yml")) + sorted(SCHEMA_DIR.glob("SEARCH*.YML"))
    for sf in search_files:
        fname = sf.name.upper().replace(".YML", "")
        rtype = fname[6:]
        rtype = rtype.rstrip("S")
        if rtype == "ALLENDPOINT":
            rtype = "ENDPOINT"
        schema = parse_schema_file(sf)
        if rtype not in resource_schemas:
            resource_schemas[rtype] = {}
        if "search_schema" not in resource_schemas[rtype]:
            resource_schemas[rtype]["search_schema"] = schema
            resource_schemas[rtype]["search_file"] = sf.name

    # Build resource inventory
    total_fields = 0
    total_resources = 0
    
    # Skip METADATA as it's a server capability, not a patient resource
    skip_types = {"METADATA"}
    
    for rtype in sorted(resource_schemas.keys()):
        if rtype in skip_types:
            continue
            
        info = resource_schemas[rtype]
        read_schema = info.get("read_schema")
        
        if not read_schema:
            continue
        
        fields = count_fields(read_schema)
        field_count = len(fields)
        total_fields += field_count
        total_resources += 1
        
        # Check for example
        example_key = rtype.lower()
        # Map some names
        example_mappings = {
            "allergyintolerance": "allergyIntolerance",
            "diagnosticreport": "diagnosticReport",
            "documentreference": "documentReference",
            "medicationrequest": "medicationRequest",
            "medicationstatement": "medicationStatement",
            "medicationdispense": "medicationDispense",
            "questionnaireresponse": "questionnaireResponse",
            "relatedperson": "relatedPerson",
            "servicerequest": "serviceRequest",
            "careplan": "careplan",
            "careteam": "careteam",
            "goal": "goals",
        }
        example_key = example_mappings.get(example_key, example_key)
        has_example = example_key in examples
        
        resource_entry = {
            "resourceType": rtype,
            "category": classify_resource(rtype),
            "certified_g10": is_certified_g10(rtype),
            "schema_file": info.get("read_file", ""),
            "search_schema_file": info.get("search_file", ""),
            "field_count": field_count,
            "has_example": has_example,
            "fields": fields
        }
        
        inventory["resources"].append(resource_entry)
    
    # Summary statistics
    categories = {}
    for r in inventory["resources"]:
        cat = r["category"]
        if cat not in categories:
            categories[cat] = {"resource_count": 0, "field_count": 0}
        categories[cat]["resource_count"] += 1
        categories[cat]["field_count"] += r["field_count"]
    
    certified_count = sum(1 for r in inventory["resources"] if r["certified_g10"])
    non_certified_count = total_resources - certified_count
    
    inventory["summary"] = {
        "total_resources": total_resources,
        "total_fields": total_fields,
        "certified_g10_resources": certified_count,
        "non_certified_resources": non_certified_count,
        "resources_with_examples": sum(1 for r in inventory["resources"] if r["has_example"]),
        "categories": categories,
        "fields_with_descriptions": 0,  # FHIR schemas don't have descriptions in these files
        "description_percentage": "0%"
    }
    
    # Write full inventory
    output_path = OUTPUT_DIR / "full-entity-inventory.json"
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    print(f"Total FHIR resource types: {total_resources}")
    print(f"Total fields (leaf): {total_fields}")
    print(f"Certified (g)(10): {certified_count}")
    print(f"Non-certified: {non_certified_count}")
    print(f"With examples: {inventory['summary']['resources_with_examples']}")
    print()
    print("By category:")
    for cat, info in sorted(categories.items()):
        print(f"  {cat}: {info['resource_count']} resources, {info['field_count']} fields")
    print()
    print("Resource details:")
    for r in sorted(inventory["resources"], key=lambda x: x["field_count"], reverse=True):
        cert = "*" if r["certified_g10"] else " "
        ex = "✓" if r["has_example"] else " "
        print(f"  {cert} {r['resourceType']:<30} {r['field_count']:>3} fields  example:{ex}  [{r['category']}]")

if __name__ == "__main__":
    main()
