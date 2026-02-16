#!/usr/bin/env python3
"""
Parse openapiServices.json (OpenAPI 3.0.1 spec) for RevolutionEHR's EHI export.
Produces full-entity-inventory.json with every schema and field, plus summary stats.
"""

import json
import sys
from pathlib import Path

OPENAPI_PATH = Path("/home/jmandel/hobby/ehi-export-analysis/results/health-innovation-technologies-inc--revolutionehr/downloads/openapiServices.json")
OUTPUT_DIR = Path(__file__).parent

def parse_openapi(spec):
    schemas = spec.get("components", {}).get("schemas", {})
    
    inventory = {
        "source_file": "openapiServices.json",
        "openapi_version": spec.get("openapi"),
        "title": spec["info"]["title"],
        "version": spec["info"]["version"],
        "export_endpoint": list(spec.get("paths", {}).keys())[0] if spec.get("paths") else None,
        "export_method": "POST",
        "schemas": [],
        "summary": {}
    }
    
    total_fields = 0
    fields_with_descriptions = 0
    fields_with_types = 0
    fields_required = 0
    fields_with_format = 0
    fields_with_refs = 0
    
    for schema_name, schema_def in sorted(schemas.items()):
        props = schema_def.get("properties", {})
        required_fields = schema_def.get("required", [])
        
        schema_entry = {
            "name": schema_name,
            "description": schema_def.get("description", ""),
            "field_count": len(props),
            "required_count": len(required_fields),
            "fields": []
        }
        
        for field_name, field_def in props.items():
            is_ref = "$ref" in field_def
            ref_schema = None
            if is_ref:
                ref_schema = field_def["$ref"].split("/")[-1]
            
            is_array = field_def.get("type") == "array"
            item_ref = None
            item_type = None
            if is_array and "items" in field_def:
                items = field_def["items"]
                if "$ref" in items:
                    item_ref = items["$ref"].split("/")[-1]
                    item_type = item_ref
                else:
                    item_type = items.get("type", "unknown")
            
            desc = field_def.get("description", "")
            field_type = field_def.get("type", ref_schema or "object")
            fmt = field_def.get("format")
            is_required = field_name in required_fields
            
            field_entry = {
                "name": field_name,
                "type": field_type,
                "description": desc,
                "required": is_required,
            }
            if fmt:
                field_entry["format"] = fmt
            if is_ref:
                field_entry["ref_schema"] = ref_schema
            if is_array:
                field_entry["is_array"] = True
                if item_ref:
                    field_entry["item_ref"] = item_ref
                if item_type:
                    field_entry["item_type"] = item_type
            
            # Assess description quality
            desc_lower = desc.lower().strip()
            name_lower = field_name.lower().strip()
            # Description is "non-trivial" if it's not just the field name with minor formatting
            trivial = (desc_lower == name_lower or 
                       desc_lower == name_lower.replace("_", " ") or
                       desc_lower == "" or
                       desc_lower == schema_name.lower() + " " + name_lower)
            field_entry["description_is_trivial"] = trivial
            
            schema_entry["fields"].append(field_entry)
            
            total_fields += 1
            if desc:
                fields_with_descriptions += 1
            if field_type:
                fields_with_types += 1
            if is_required:
                fields_required += 1
            if fmt:
                fields_with_format += 1
            if is_ref or item_ref:
                fields_with_refs += 1
        
        inventory["schemas"].append(schema_entry)
    
    # Count descriptions that go beyond restating the field name
    nontrivial_descriptions = sum(
        1 for s in inventory["schemas"] 
        for f in s["fields"] 
        if not f.get("description_is_trivial", True)
    )
    
    inventory["summary"] = {
        "total_schemas": len(inventory["schemas"]),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "fields_with_nontrivial_descriptions": nontrivial_descriptions,
        "fields_with_types": fields_with_types,
        "fields_required": fields_required,
        "fields_with_format": fields_with_format,
        "fields_with_references": fields_with_refs,
        "description_coverage_pct": round(fields_with_descriptions / total_fields * 100, 1) if total_fields else 0,
        "nontrivial_description_pct": round(nontrivial_descriptions / total_fields * 100, 1) if total_fields else 0,
        "type_coverage_pct": round(fields_with_types / total_fields * 100, 1) if total_fields else 0,
    }
    
    # Categorize schemas by domain
    domain_mapping = {
        "Demographics": "Demographics",
        "Address": "Demographics",
        "Employment": "Demographics",
        "Contact": "Demographics",
        "FamilyMember": "Demographics",
        "Encounter": "Clinical - Encounters",
        "EncounterDiagnosis": "Clinical - Encounters",
        "ReasonForVisit": "Clinical - Encounters",
        "Service": "Clinical - Encounters",
        "OrientationMood": "Clinical - Encounters",
        "Diagnosis": "Clinical - Diagnoses",
        "DiagnosisCarePlanItem": "Clinical - Diagnoses",
        "CarePlanItem": "Clinical - Care Plans",
        "HealthGoal": "Clinical - Care Plans",
        "HealthConcern": "Clinical - Care Plans",
        "Allergy": "Clinical - Allergies",
        "Immunization": "Clinical - Immunizations",
        "ImplantableDevice": "Clinical - Devices",
        "VitalSigns": "Clinical - Vitals",
        "Refraction": "Specialty - Optometry",
        "Test": "Specialty - Optometry",
        "TestValue": "Specialty - Optometry",
        "ClinicalDecisionSupport": "Clinical - CDS",
        "MedicalOrder": "Clinical - Orders/Labs",
        "SocialHistory": "Clinical - Social History",
        "FamilyHistory": "Clinical - Family History",
        "FamilyHealthHistory": "Clinical - Family History",
        "Insurance": "Financial - Insurance",
        "Invoice": "Financial - Billing",
        "InvoiceItem": "Financial - Billing",
        "Payment": "Financial - Billing",
        "Claim": "Financial - Billing",
        "Statement": "Financial - Billing",
        "Referral": "Clinical - Referrals",
        "Patient": "Root",
    }
    
    domain_summary = {}
    for schema in inventory["schemas"]:
        domain = domain_mapping.get(schema["name"], "Other")
        if domain not in domain_summary:
            domain_summary[domain] = {"schemas": 0, "fields": 0}
        domain_summary[domain]["schemas"] += 1
        domain_summary[domain]["fields"] += schema["field_count"]
    
    inventory["domain_breakdown"] = domain_summary
    
    return inventory

if __name__ == "__main__":
    with open(OPENAPI_PATH) as f:
        spec = json.load(f)
    
    inventory = parse_openapi(spec)
    
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Print summary
    s = inventory["summary"]
    print(f"Schemas: {s['total_schemas']}")
    print(f"Total fields: {s['total_fields']}")
    print(f"Fields with descriptions: {s['fields_with_descriptions']} ({s['description_coverage_pct']}%)")
    print(f"Fields with NON-TRIVIAL descriptions: {s['fields_with_nontrivial_descriptions']} ({s['nontrivial_description_pct']}%)")
    print(f"Fields with types: {s['fields_with_types']} ({s['type_coverage_pct']}%)")
    print(f"Fields required: {s['fields_required']}")
    print(f"Fields with format: {s['fields_with_format']}")
    print(f"Fields with references: {s['fields_with_references']}")
    print()
    print("Domain breakdown:")
    for domain, counts in sorted(inventory["domain_breakdown"].items()):
        print(f"  {domain}: {counts['schemas']} schemas, {counts['fields']} fields")
