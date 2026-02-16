#!/usr/bin/env python3
"""
Parse Canvas Medical EHI export artifacts and produce:
1. full-entity-inventory.json - complete machine-readable extraction of FHIR resources + SDK models
2. summary-stats.json - aggregate statistics
3. coverage-mapping.json - mapping between SDK internal models and FHIR export resources
"""

import json
import os
import sys

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/canvas-medical-inc--canvas-medical/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/canvas-medical-inc--canvas-medical/analysis"

def parse_fhir_resources():
    """Parse the pre-extracted FHIR API resources JSON."""
    with open(os.path.join(RESULTS_DIR, "enrichment/fhir-api-resources.json")) as f:
        data = json.load(f)
    
    resources = []
    for r in data["resources"]:
        # Collect all unique attributes across operations (dedup by name within a resource)
        # The GET operation typically has the response fields which matter for export
        all_attrs = {}
        for op in r["operations"]:
            for attr in op.get("attributes", []):
                name = attr["name"]
                if name not in all_attrs or (attr.get("description") and not all_attrs[name].get("description")):
                    all_attrs[name] = attr
        
        # Build flat field list
        fields = []
        for name, attr in all_attrs.items():
            field = {
                "name": name,
                "type": attr.get("type", ""),
                "required": attr.get("required", False),
                "description": attr.get("description", ""),
            }
            if attr.get("values"):
                field["values"] = attr["values"]
            if attr.get("children"):
                field["children"] = attr["children"]
            fields.append(field)
        
        resource = {
            "resource_name": r["name"],
            "source_file": r["sourceFile"],
            "source_url": r["sourceUrl"],
            "last_updated": r.get("lastUpdated", ""),
            "description": r.get("description", ""),
            "endpoints": r.get("endpoints", []),
            "total_fields_all_ops": r["totalFields"],
            "unique_fields": len(fields),
            "fields": fields,
        }
        resources.append(resource)
    
    return resources


def count_described_fields(fields):
    """Count fields with non-empty descriptions."""
    return sum(1 for f in fields if f.get("description", "").strip())


def count_typed_fields(fields):
    """Count fields with non-empty types."""
    return sum(1 for f in fields if f.get("type", "").strip())


def parse_sdk_models():
    """Parse the pre-extracted SDK data models JSON."""
    with open(os.path.join(RESULTS_DIR, "enrichment/sdk-data-models.json")) as f:
        data = json.load(f)
    
    pages = []
    for p in data["dataPages"]:
        models = []
        for m in p.get("models", []):
            fields = []
            for field in m.get("fields", []):
                f = {
                    "name": field.get("name", ""),
                    "type": field.get("type", ""),
                }
                if field.get("description"):
                    f["description"] = field["description"]
                if field.get("properties"):
                    f["properties"] = field["properties"]
                fields.append(f)
            models.append({
                "name": m.get("name", ""),
                "field_count": len(fields),
                "fields": fields,
            })
        
        enums = []
        for e in p.get("enums", []):
            enums.append({
                "name": e.get("name", ""),
                "values": e.get("values", []),
            })
        
        pages.append({
            "page_name": p["pageName"],
            "source_file": p.get("sourceFile", ""),
            "source_url": p.get("sourceUrl", ""),
            "last_updated": p.get("lastUpdated", ""),
            "introduction": p.get("introduction", ""),
            "model_count": len(models),
            "total_fields": sum(m["field_count"] for m in models),
            "enum_count": len(enums),
            "models": models,
            "enums": enums,
        })
    
    return pages


def classify_sdk_page(page_name):
    """Classify SDK pages into categories and whether they're EHI-relevant."""
    # Patient-facing clinical data
    clinical = {
        "AllergyIntolerance", "Assessment", "Condition", "DetectedIssue",
        "Device", "Encounter", "Imaging", "Immunization", "Labs", "Medication",
        "Medication History", "Medication Statement", "Note", "Observation",
        "Patient", "PatientConsent", "Questionnaire", "ReasonForVisit",
        "Referral", "Stop Medication Event", "Uncategorized Clinical Document",
        "CareTeam", "CompoundMedication", "Letter", "Message",
    }
    # Billing/financial
    billing = {
        "BillingLineItem", "ChargeDescriptionMaster", "Claim", "Coverage",
        "PayorSpecificCharge", "Posting",
    }
    # Administrative/system (not EHI)
    system = {
        "Application", "BusinessLine", "Calendar", "CanvasUser", "Command",
        "Common Enumeration Type", "ExternalEvent", "Facility", "LabPartner & LabPartnerTest",
        "Organization", "Practice Location", "Protocol Current", "ProtocolOverride",
        "ServiceProvider", "Staff", "Team", "ValueSets", "BannerAlert",
    }
    # Scheduling
    scheduling = {"Appointment"}
    # Tasks
    tasks = {"Task"}
    
    if page_name in clinical:
        return "Clinical", True
    elif page_name in billing:
        return "Billing/Financial", True
    elif page_name in scheduling:
        return "Scheduling", True
    elif page_name in tasks:
        return "Tasks/Workflow", True
    elif page_name in system:
        return "System/Admin", False
    else:
        return "Other", False


def map_sdk_to_fhir(sdk_page_name):
    """Map SDK internal model names to FHIR export resource types."""
    mapping = {
        "AllergyIntolerance": ["AllergyIntolerance"],
        "Appointment": ["Appointment"],
        "Assessment": [],  # May be in Encounter/Condition
        "BannerAlert": [],
        "BillingLineItem": [],  # Partially in Claim
        "BusinessLine": [],
        "Calendar": [],
        "CanvasUser": [],
        "CareTeam": ["CareTeam"],
        "ChargeDescriptionMaster": [],
        "Claim": ["Claim"],
        "Command": [],
        "CompoundMedication": [],  # May be in MedicationRequest
        "Condition": ["Condition"],
        "Coverage": ["Coverage", "CoverageEligibilityResponse"],
        "DetectedIssue": [],  # NOT in export despite having API
        "Device": ["Device"],
        "Encounter": ["Encounter"],
        "Common Enumeration Type": [],
        "ExternalEvent": [],
        "Facility": [],
        "Imaging": ["DiagnosticReport", "Media"],
        "Immunization": ["Immunization"],
        "LabPartner & LabPartnerTest": [],
        "Labs": ["DiagnosticReport", "Observation", "Specimen"],
        "Letter": [],  # May be in Communication or DocumentReference
        "Medication": ["MedicationRequest", "MedicationDispense"],
        "Medication History": ["MedicationRequest"],
        "Medication Statement": ["MedicationStatement"],
        "Message": ["Communication"],
        "Note": ["Encounter", "DocumentReference"],
        "Observation": ["Observation"],
        "Organization": [],
        "Patient": ["Patient", "RelatedPerson"],
        "PatientConsent": ["Consent"],
        "PayorSpecificCharge": [],
        "Posting": [],  # No FHIR mapping
        "Practice Location": [],
        "Protocol Current": [],
        "ProtocolOverride": [],
        "Questionnaire": ["QuestionnaireResponse"],
        "ReasonForVisit": [],  # May be in Encounter.reason
        "Referral": ["ServiceRequest"],
        "ServiceProvider": [],
        "Staff": [],
        "Stop Medication Event": [],  # May be in MedicationRequest/Statement
        "Task": ["Task"],
        "Team": [],
        "Uncategorized Clinical Document": ["DocumentReference"],
        "ValueSets": [],
        "Application": [],
    }
    return mapping.get(sdk_page_name, [])


def main():
    print("Parsing FHIR API resources...")
    fhir_resources = parse_fhir_resources()
    
    print("Parsing SDK data models...")
    sdk_pages = parse_sdk_models()
    
    # Build full entity inventory
    inventory = {
        "export_format": "FHIR R4 NDJSON (Bulk Data Access)",
        "fhir_resources": [],
        "sdk_internal_models": [],
    }
    
    # FHIR resources (what's in the export)
    total_fhir_fields = 0
    total_fhir_described = 0
    total_fhir_typed = 0
    
    for r in fhir_resources:
        described = count_described_fields(r["fields"])
        typed = count_typed_fields(r["fields"])
        total_fhir_fields += r["unique_fields"]
        total_fhir_described += described
        total_fhir_typed += typed
        
        inventory["fhir_resources"].append({
            "resource_name": r["resource_name"],
            "source_url": r["source_url"],
            "last_updated": r["last_updated"],
            "description": r["description"],
            "endpoints": r["endpoints"],
            "unique_field_count": r["unique_fields"],
            "fields_with_descriptions": described,
            "fields_with_types": typed,
            "fields": r["fields"],
        })
    
    # SDK models (internal data model for gap analysis)
    total_sdk_models = 0
    total_sdk_fields = 0
    ehi_sdk_models = 0
    ehi_sdk_fields = 0
    
    for p in sdk_pages:
        category, is_ehi = classify_sdk_page(p["page_name"])
        fhir_mapping = map_sdk_to_fhir(p["page_name"])
        
        total_sdk_models += p["model_count"]
        total_sdk_fields += p["total_fields"]
        if is_ehi:
            ehi_sdk_models += p["model_count"]
            ehi_sdk_fields += p["total_fields"]
        
        inventory["sdk_internal_models"].append({
            "page_name": p["page_name"],
            "category": category,
            "is_ehi_relevant": is_ehi,
            "fhir_export_mapping": fhir_mapping,
            "has_fhir_mapping": len(fhir_mapping) > 0,
            "model_count": p["model_count"],
            "total_fields": p["total_fields"],
            "models": p["models"],
            "enums": p["enums"],
        })
    
    # Save full inventory
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved full-entity-inventory.json")
    
    # Build summary stats
    # Count SDK EHI-relevant pages without FHIR mapping
    unmapped_ehi = []
    for item in inventory["sdk_internal_models"]:
        if item["is_ehi_relevant"] and not item["has_fhir_mapping"]:
            unmapped_ehi.append({
                "page_name": item["page_name"],
                "category": item["category"],
                "model_count": item["model_count"],
                "total_fields": item["total_fields"],
            })
    
    summary = {
        "fhir_export": {
            "resource_count": len(fhir_resources),
            "total_unique_fields": total_fhir_fields,
            "fields_with_descriptions": total_fhir_described,
            "fields_with_types": total_fhir_typed,
            "description_percentage": round(100 * total_fhir_described / total_fhir_fields, 1) if total_fhir_fields else 0,
            "resources": [{
                "name": r["resource_name"],
                "unique_fields": r["unique_field_count"],
                "described": count_described_fields(r["fields"]),
            } for r in inventory["fhir_resources"]],
        },
        "sdk_internal": {
            "total_pages": len(sdk_pages),
            "total_models": total_sdk_models,
            "total_fields": total_sdk_fields,
            "ehi_relevant_models": ehi_sdk_models,
            "ehi_relevant_fields": ehi_sdk_fields,
        },
        "coverage_gaps": {
            "unmapped_ehi_relevant_pages": unmapped_ehi,
            "total_unmapped_ehi_models": sum(u["model_count"] for u in unmapped_ehi),
            "total_unmapped_ehi_fields": sum(u["total_fields"] for u in unmapped_ehi),
        },
        "category_breakdown": {},
    }
    
    # Category breakdown for SDK models
    categories = {}
    for item in inventory["sdk_internal_models"]:
        cat = item["category"]
        if cat not in categories:
            categories[cat] = {"pages": 0, "models": 0, "fields": 0, "mapped": 0, "unmapped": 0}
        categories[cat]["pages"] += 1
        categories[cat]["models"] += item["model_count"]
        categories[cat]["fields"] += item["total_fields"]
        if item["has_fhir_mapping"]:
            categories[cat]["mapped"] += 1
        else:
            categories[cat]["unmapped"] += 1
    summary["category_breakdown"] = categories
    
    with open(os.path.join(OUTPUT_DIR, "summary-stats.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary-stats.json")
    
    # Print key stats
    print("\n=== KEY STATISTICS ===")
    print(f"FHIR Export Resources: {len(fhir_resources)}")
    print(f"Total unique FHIR fields: {total_fhir_fields}")
    print(f"Fields with descriptions: {total_fhir_described} ({summary['fhir_export']['description_percentage']}%)")
    print(f"Fields with types: {total_fhir_typed}")
    print(f"\nSDK Internal Model Pages: {len(sdk_pages)}")
    print(f"Total SDK models: {total_sdk_models}")
    print(f"Total SDK fields: {total_sdk_fields}")
    print(f"EHI-relevant SDK models: {ehi_sdk_models} ({ehi_sdk_fields} fields)")
    print(f"\nUnmapped EHI-relevant pages: {len(unmapped_ehi)}")
    for u in unmapped_ehi:
        print(f"  {u['page_name']}: {u['model_count']} models, {u['total_fields']} fields ({u['category']})")
    
    print(f"\nCategory breakdown:")
    for cat, counts in sorted(categories.items()):
        print(f"  {cat}: {counts['pages']} pages, {counts['models']} models, {counts['fields']} fields (mapped: {counts['mapped']}, unmapped: {counts['unmapped']})")
    
    # Per-resource field list
    print(f"\nFHIR Resource field counts:")
    for r in sorted(inventory["fhir_resources"], key=lambda x: x["unique_field_count"], reverse=True):
        print(f"  {r['resource_name']}: {r['unique_field_count']} fields ({count_described_fields(r['fields'])} described)")


if __name__ == "__main__":
    main()
