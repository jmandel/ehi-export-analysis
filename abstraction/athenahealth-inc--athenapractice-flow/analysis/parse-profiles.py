#!/usr/bin/env python3
"""Parse all athena FHIR StructureDefinition profiles to build entity-inventory-full.json.
Reads from ../downloads/definitions/ and produces entity-level + field-level inventory."""

import json
import glob
import os
import re
from pathlib import Path

DEFS_DIR = Path(__file__).parent.parent / "downloads" / "definitions"
EHI_RESOURCES_PRACTICE = [
    "Account", "Adjustment", "AllergyIntolerance", "Appointment", "BillingStatement",
    "Binary", "CarePlan", "CareTeam", "Charge", "Claim", "ClinicalImpression",
    "Collection", "Condition", "Consent", "Coverage", "Deductible", "Device",
    "DiagnosticReport", "DocumentReference", "Eligibility", "Encounter",
    "FamilyMemberHistory", "Goal", "Immunization", "Location", "Medication",
    "MedicationAdministration", "MedicationRequest", "MedicationStatement",
    "Observation", "Organization", "Patient", "PatientInsurance", "Payment",
    "Practitioner", "PractitionerRole", "Procedure", "Provenance", "RelatedPerson",
    "Schedule", "ServiceRequest", "Slot"
]
EHI_RESOURCES_FLOW = [
    "AllergyIntolerance", "Appointment", "Binary", "CarePlan", "CareTeam",
    "ClinicalImpression", "Condition", "Consent", "Coverage", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "FamilyMemberHistory",
    "Goal", "Immunization", "Location", "Medication", "MedicationAdministration",
    "MedicationRequest", "MedicationStatement", "Observation", "Organization",
    "Patient", "Practitioner", "PractitionerRole", "Procedure", "Provenance",
    "RelatedPerson", "ServiceRequest"
]

# Categorization from the EHI export page
CATEGORIES = {
    "System": ["Location", "Medication", "Organization", "Practitioner", "PractitionerRole", "OperationOutcome"],
    "Clinical": [
        "AllergyIntolerance", "Binary", "CarePlan", "CareTeam", "ClinicalImpression",
        "Condition", "Consent", "Device", "DiagnosticReport", "DocumentReference",
        "Encounter", "FamilyMemberHistory", "Goal", "Immunization",
        "MedicationAdministration", "MedicationRequest", "MedicationStatement",
        "Observation", "Procedure", "Provenance", "ServiceRequest"
    ],
    "Practice Management": ["Account", "Appointment", "Coverage", "Patient", "RelatedPerson", "Schedule", "Slot"],
    "Custom (Financial/PM)": [
        "Adjustment", "BillingStatement", "Charge", "Claim", "Collection",
        "Deductible", "Eligibility", "PatientInsurance", "Payment"
    ]
}

# Also include non-EHI profiles for completeness
NON_EHI_PROFILES = [
    "AuditEvent", "ConceptMap", "Endpoint", "List", "Media", "MedicationDispense",
    "NamingSystem", "Specimen", "Subscription", "ValueSet"
]

def get_category(resource_type, name=""):
    for cat, types in CATEGORIES.items():
        if resource_type in types:
            return cat
    # For custom resources, try matching by name
    for cat, types in CATEGORIES.items():
        if name in types:
            return cat
    return "Other"

def parse_profile(filepath):
    """Parse a StructureDefinition profile JSON and extract entity + field info."""
    with open(filepath) as f:
        sd = json.load(f)
    
    profile_id = sd.get("id", "")
    name = sd.get("name", "")
    title = sd.get("title", "")
    resource_type = sd.get("type", "")
    base_def = sd.get("baseDefinition", "")
    is_custom = "http://hl7.org/fhir" not in base_def if base_def else True
    description = sd.get("description", "")
    
    # Use differential elements - these are the vendor-customized fields
    diff_elements = sd.get("differential", {}).get("element", [])
    # Use snapshot for full picture
    snap_elements = sd.get("snapshot", {}).get("element", [])
    
    # Build set of paths that are in differential (vendor-defined/constrained)
    diff_paths = {e["id"] for e in diff_elements}
    
    # Parse extensions defined on this profile
    extensions = []
    
    fields = []
    for elem in snap_elements:
        path = elem.get("path", "")
        elem_id = elem.get("id", "")
        
        # Skip the root element
        if path == resource_type:
            continue
        
        # Skip deeply nested sub-elements (meta.*, extension sub-elements, etc.)
        # We want top-level fields and their immediate children
        parts = path.split(".")
        if len(parts) < 2:
            continue
        
        # Get type info
        types = []
        for t in elem.get("type", []):
            code = t.get("code", "")
            if code and "System.String" not in code:
                types.append(code)
        
        # Check if this is an extension
        is_extension = any(t.get("code") == "Extension" for t in elem.get("type", []))
        
        # Get binding info
        binding = elem.get("binding", {})
        value_set = binding.get("valueSet", "")
        binding_strength = binding.get("strength", "")
        
        field_info = {
            "path": path,
            "id": elem_id,
            "short": elem.get("short", ""),
            "definition": elem.get("definition", ""),
            "types": types,
            "min": elem.get("min", 0),
            "max": elem.get("max", "*"),
            "is_in_differential": elem_id in diff_paths,
            "is_extension": is_extension,
        }
        
        if value_set:
            field_info["valueSet"] = value_set
            field_info["bindingStrength"] = binding_strength
        
        # Check for fixed values
        for key in elem:
            if key.startswith("fixed") or key.startswith("pattern"):
                field_info["fixedValue"] = str(elem[key])
                break
        
        fields.append(field_info)
    
    # For custom resources, use the name as display resource type
    display_type = name if is_custom else resource_type
    
    # Determine which products include this in EHI export
    in_practice_ehi = resource_type in EHI_RESOURCES_PRACTICE or name in EHI_RESOURCES_PRACTICE
    in_flow_ehi = resource_type in EHI_RESOURCES_FLOW or name in EHI_RESOURCES_FLOW
    
    return {
        "profileId": profile_id,
        "name": name,
        "title": title,
        "resourceType": resource_type,
        "displayType": display_type,
        "baseDefinition": base_def,
        "isCustomResource": is_custom,
        "description": description,
        "category": get_category(resource_type, name),
        "inPracticeEHI": in_practice_ehi,
        "inFlowEHI": in_flow_ehi,
        "totalSnapshotElements": len(snap_elements),
        "totalDifferentialElements": len(diff_elements),
        "totalFields": len(fields),
        "fields": fields
    }

def count_described_fields(fields):
    """Count fields that have a non-generic description."""
    count = 0
    for f in fields:
        desc = f.get("definition", "")
        short = f.get("short", "")
        # Generic FHIR boilerplate descriptions
        if desc and len(desc) > 20:
            count += 1
    return count

def main():
    profile_files = sorted(glob.glob(str(DEFS_DIR / "StructureDefinition-athena-*-profile.json")))
    print(f"Found {len(profile_files)} profile files")
    
    entities = []
    for fp in profile_files:
        entity = parse_profile(fp)
        entities.append(entity)
    
    # Sort by category, then name
    cat_order = {"System": 0, "Clinical": 1, "Practice Management": 2, "Custom (Financial/PM)": 3, "Other": 4}
    entities.sort(key=lambda e: (cat_order.get(e["category"], 5), e["name"]))
    
    # Write full inventory
    out_path = Path(__file__).parent / "entity-inventory-full.json"
    with open(out_path, "w") as f:
        json.dump(entities, f, indent=2)
    print(f"Wrote {out_path}")
    
    # Build summary
    total_fields = 0
    total_described = 0
    total_differential = 0
    ehi_entities = []
    non_ehi_entities = []
    
    category_stats = {}
    
    for e in entities:
        n_fields = e["totalFields"]
        n_described = count_described_fields(e["fields"])
        n_diff = e["totalDifferentialElements"]
        total_fields += n_fields
        total_described += n_described
        total_differential += n_diff
        
        cat = e["category"]
        if cat not in category_stats:
            category_stats[cat] = {"entities": 0, "fields": 0, "described": 0, "differential": 0, "names": []}
        category_stats[cat]["entities"] += 1
        category_stats[cat]["fields"] += n_fields
        category_stats[cat]["described"] += n_described
        category_stats[cat]["differential"] += n_diff
        category_stats[cat]["names"].append(e["title"] or e["name"])
        
        if e["inPracticeEHI"] or e["inFlowEHI"]:
            ehi_entities.append(e)
        else:
            non_ehi_entities.append(e)
    
    # Count extensions
    extension_files = sorted(glob.glob(str(DEFS_DIR / "StructureDefinition-athena-*-extension-*.json")))
    extensions_info = []
    for fp in extension_files:
        with open(fp) as f:
            ext = json.load(f)
        extensions_info.append({
            "id": ext.get("id", ""),
            "name": ext.get("name", ""),
            "title": ext.get("title", ""),
            "description": ext.get("description", ""),
            "context": [c.get("expression", "") for c in ext.get("context", [])],
            "type": [t.get("code", "") for t in ext.get("differential", {}).get("element", [{}])[-1].get("type", [])]
        })
    
    summary = {
        "totalProfiles": len(entities),
        "totalEHIProfiles_practice": sum(1 for e in entities if e["inPracticeEHI"]),
        "totalEHIProfiles_flow": sum(1 for e in entities if e["inFlowEHI"]),
        "totalFields": total_fields,
        "totalFieldsDescribed": total_described,
        "descriptionRate": f"{total_described/total_fields*100:.1f}%" if total_fields else "N/A",
        "totalDifferentialElements": total_differential,
        "totalExtensions": len(extensions_info),
        "categoryBreakdown": {},
        "ehi_practice_resources": sorted([e["resourceType"] for e in entities if e["inPracticeEHI"]]),
        "ehi_flow_resources": sorted([e["resourceType"] for e in entities if e["inFlowEHI"]]),
        "non_ehi_resources": sorted([e["resourceType"] for e in entities if not e["inPracticeEHI"] and not e["inFlowEHI"]]),
        "extensions": extensions_info,
        "entitySummary": []
    }
    
    for cat in ["System", "Clinical", "Practice Management", "Custom (Financial/PM)", "Other"]:
        if cat in category_stats:
            cs = category_stats[cat]
            summary["categoryBreakdown"][cat] = {
                "entityCount": cs["entities"],
                "totalFields": cs["fields"],
                "describedFields": cs["described"],
                "differentialElements": cs["differential"],
                "entityNames": cs["names"]
            }
    
    for e in entities:
        n_ext = sum(1 for f in e["fields"] if f.get("is_extension"))
        n_bindings = sum(1 for f in e["fields"] if f.get("valueSet"))
        summary["entitySummary"].append({
            "name": e["title"] or e["name"],
            "resourceType": e["resourceType"],
            "category": e["category"],
            "isCustom": e["isCustomResource"],
            "totalFields": e["totalFields"],
            "describedFields": count_described_fields(e["fields"]),
            "differentialElements": e["totalDifferentialElements"],
            "extensions": n_ext,
            "bindings": n_bindings,
            "inPracticeEHI": e["inPracticeEHI"],
            "inFlowEHI": e["inFlowEHI"]
        })
    
    summary_path = Path(__file__).parent / "entity-inventory-summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {summary_path}")
    
    # Print summary to stdout
    print(f"\n=== SUMMARY ===")
    print(f"Total profiles: {len(entities)}")
    print(f"Total EHI profiles (athenaPractice): {summary['totalEHIProfiles_practice']}")
    print(f"Total EHI profiles (athenaFlow): {summary['totalEHIProfiles_flow']}")
    print(f"Total fields across all profiles: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({total_described/total_fields*100:.1f}%)")
    print(f"Total differential elements: {total_differential}")
    print(f"Total custom extensions: {len(extensions_info)}")
    print()
    
    for cat in ["System", "Clinical", "Practice Management", "Custom (Financial/PM)", "Other"]:
        if cat in category_stats:
            cs = category_stats[cat]
            print(f"  {cat}: {cs['entities']} entities, {cs['fields']} fields ({cs['described']} described)")
    
    print(f"\n=== ENTITY TABLE ===")
    print(f"{'Entity':<30} {'Type':<25} {'Cat':<20} {'Fields':>6} {'Desc':>6} {'Diff':>6} {'Custom':>6} {'PrEHI':>6} {'FlEHI':>6}")
    print("-" * 140)
    for e in entities:
        nd = count_described_fields(e["fields"])
        print(f"{(e['title'] or e['name']):<30} {e['resourceType']:<25} {e['category']:<20} {e['totalFields']:>6} {nd:>6} {e['totalDifferentialElements']:>6} {'Yes' if e['isCustomResource'] else 'No':>6} {'Yes' if e['inPracticeEHI'] else 'No':>6} {'Yes' if e['inFlowEHI'] else 'No':>6}")

if __name__ == "__main__":
    main()
