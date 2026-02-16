#!/usr/bin/env python3
"""
Parse myhELO FHIR StructureDefinitions from structure-definitions.json
and produce entity-inventory-full.json and entity-inventory-summary.json.

Reads: ../downloads/structure-definitions.json (17 US Core StructureDefinitions)
       ../downloads/dataset-summaries.json (overview metadata)
       ../downloads/fhir-well-known.json (example FHIR responses)
       ../downloads/fhir-metadata.json (CapabilityStatement)
Outputs: entity-inventory-full.json, entity-inventory-summary.json
"""

import json
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(BASE, "..", "downloads")


def load_json(path):
    with open(os.path.join(DOWNLOADS, path)) as f:
        return json.load(f)


def parse_element(el):
    """Parse a single FHIR StructureDefinition snapshot element."""
    result = {
        "path": el.get("id", el.get("path", "")),
        "short": el.get("short", ""),
        "definition": el.get("definition", ""),
        "min": el.get("min"),
        "max": el.get("max", ""),
        "types": [],
        "is_modifier": el.get("isModifier", False),
        "is_summary": el.get("isSummary", False),
        "must_support": el.get("mustSupport", False),
        "binding": None,
        "fixed_value": None,
        "pattern_value": None,
    }

    # Types
    if "type" in el:
        for t in el["type"]:
            type_entry = {"code": t.get("code", "")}
            if "targetProfile" in t:
                type_entry["targetProfile"] = t["targetProfile"]
            if "profile" in t:
                type_entry["profile"] = t["profile"]
            result["types"].append(type_entry)

    # Binding
    if "binding" in el:
        b = el["binding"]
        result["binding"] = {
            "strength": b.get("strength", ""),
            "description": b.get("description", ""),
            "valueSet": b.get("valueSet", ""),
        }

    # Fixed values
    for key in el:
        if key.startswith("fixed"):
            result["fixed_value"] = {key: el[key]}
        if key.startswith("pattern"):
            result["pattern_value"] = {key: el[key]}

    return result


def main():
    # Load structure definitions (dict keyed by resource type)
    struct_defs_dict = load_json("structure-definitions.json")
    summaries = load_json("dataset-summaries.json")
    capability = load_json("fhir-metadata.json")
    well_known = load_json("fhir-well-known.json")

    resources = []

    for _key, sd in struct_defs_dict.items():
        resource_type = sd.get("type", sd.get("name", "Unknown"))
        profile_id = sd.get("id", "")
        profile_url = sd.get("url", "")

        # Get summary info
        summary_info = summaries.get(resource_type, {})

        # Parse all snapshot elements
        elements = []
        snapshot = sd.get("snapshot", {})
        for el in snapshot.get("element", []):
            elements.append(parse_element(el))

        # Check for example data in well-known
        display_name_map = {
            "AllergyIntolerance": "Allergy Intolerance",
            "CarePlan": "Care Plan",
            "CareTeam": "Care Team",
            "DiagnosticReport": "Diagnostic Report",
            "DocumentReference": "Document Reference",
            "MedicationRequest": "Medication Request",
        }
        display_name = display_name_map.get(resource_type, resource_type)
        has_example = display_name in well_known and (
            "read" in well_known[display_name] or "search" in well_known[display_name]
        )

        # Count stats
        uscdi_count = sum(1 for e in elements if e["must_support"])
        required_count = sum(1 for e in elements if e["min"] and e["min"] > 0)
        with_binding = sum(1 for e in elements if e["binding"])
        with_description = sum(1 for e in elements if e["definition"])
        with_short = sum(1 for e in elements if e["short"])

        resource_entry = {
            "resourceType": resource_type,
            "profileId": profile_id,
            "profileUrl": profile_url,
            "title": summary_info.get("title", resource_type),
            "brief": summary_info.get("brief", ""),
            "supportedProfiles": [
                p["name"] for p in summary_info.get("supported_profiles", [])
            ],
            "hasExampleData": has_example,
            "elementCount": len(elements),
            "uscdiElementCount": uscdi_count,
            "requiredElementCount": required_count,
            "elementsWithBinding": with_binding,
            "elementsWithDescription": with_description,
            "elementsWithShort": with_short,
            "elements": elements,
        }
        resources.append(resource_entry)

    # Sort by resource type
    resources.sort(key=lambda r: r["resourceType"])

    # Build full inventory
    full_inventory = {
        "vendor": "myhELO, Inc.",
        "product": "myhELO",
        "exportFormat": "FHIR R4 JSON",
        "fhirVersion": "4.0.1",
        "baseUrl": "https://provider.myhelo.com/fhir",
        "analysisDate": "2026-02-16",
        "sourceFiles": [
            "downloads/structure-definitions.json",
            "downloads/dataset-summaries.json",
            "downloads/fhir-metadata.json",
            "downloads/fhir-well-known.json",
        ],
        "totalResources": len(resources),
        "totalElements": sum(r["elementCount"] for r in resources),
        "totalUscdiElements": sum(r["uscdiElementCount"] for r in resources),
        "totalRequiredElements": sum(r["requiredElementCount"] for r in resources),
        "totalElementsWithDescription": sum(
            r["elementsWithDescription"] for r in resources
        ),
        "totalElementsWithBinding": sum(r["elementsWithBinding"] for r in resources),
        "resources": resources,
    }

    # Write full inventory
    out_path = os.path.join(BASE, "entity-inventory-full.json")
    with open(out_path, "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"Wrote {out_path} ({os.path.getsize(out_path)} bytes)")

    # Build summary
    summary = {
        "vendor": full_inventory["vendor"],
        "product": full_inventory["product"],
        "exportFormat": full_inventory["exportFormat"],
        "fhirVersion": full_inventory["fhirVersion"],
        "analysisDate": full_inventory["analysisDate"],
        "totals": {
            "resources": full_inventory["totalResources"],
            "elements": full_inventory["totalElements"],
            "uscdiElements": full_inventory["totalUscdiElements"],
            "requiredElements": full_inventory["totalRequiredElements"],
            "elementsWithDescription": full_inventory["totalElementsWithDescription"],
            "elementsWithBinding": full_inventory["totalElementsWithBinding"],
            "descriptionCoverage": f"{full_inventory['totalElementsWithDescription']/full_inventory['totalElements']*100:.1f}%",
        },
        "resourceSummary": [],
    }

    for r in resources:
        summary["resourceSummary"].append(
            {
                "resourceType": r["resourceType"],
                "elementCount": r["elementCount"],
                "uscdiElements": r["uscdiElementCount"],
                "requiredElements": r["requiredElementCount"],
                "elementsWithBinding": r["elementsWithBinding"],
                "hasExampleData": r["hasExampleData"],
                "supportedProfiles": r["supportedProfiles"],
            }
        )

    # USCDI coverage analysis
    uscdi_resource_types = {
        "AllergyIntolerance",
        "CarePlan",
        "CareTeam",
        "Condition",
        "Device",
        "DiagnosticReport",
        "DocumentReference",
        "Encounter",
        "Goal",
        "Immunization",
        "MedicationRequest",
        "Observation",
        "Organization",
        "Patient",
        "Practitioner",
        "Procedure",
        "Provenance",
    }
    non_uscdi_resources = [
        r["resourceType"]
        for r in resources
        if r["resourceType"] not in uscdi_resource_types
    ]
    summary["uscdiAnalysis"] = {
        "allResourcesAreUSCDI": len(non_uscdi_resources) == 0,
        "nonUscdiResources": non_uscdi_resources,
        "missingNonUscdiDomains": [
            "Billing/Claims (Claim, ExplanationOfBenefit, Account)",
            "Coverage/Insurance (Coverage)",
            "Appointments/Scheduling (Appointment, Schedule, Slot)",
            "ServiceRequest/Referrals",
            "Communication/Messages",
            "Consent",
            "QuestionnaireResponse (intake forms, PROs)",
            "FamilyMemberHistory",
            "Specimen",
            "RelatedPerson",
            "MedicationDispense",
        ],
    }

    # CapabilityStatement analysis
    cap_resources = [
        r["type"] for r in capability["rest"][0]["resource"]
    ]
    ehi_resources = [r["resourceType"] for r in resources]
    summary["capabilityComparison"] = {
        "capabilityStatementResources": cap_resources,
        "ehiExportResources": ehi_resources,
        "inCapabilityButNotEHI": [
            r for r in cap_resources if r not in ehi_resources
        ],
        "inEHIButNotCapability": [
            r for r in ehi_resources if r not in cap_resources
        ],
        "identical": set(cap_resources) == set(ehi_resources),
        "note": "The CapabilityStatement includes Group (for bulk export) and Location which are not in the EHI data dictionary. Otherwise the resource sets are identical, confirming this is the same API surface.",
    }

    sum_path = os.path.join(BASE, "entity-inventory-summary.json")
    with open(sum_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {sum_path} ({os.path.getsize(sum_path)} bytes)")

    # Print summary stats
    print(f"\n=== Summary ===")
    print(f"Resources: {full_inventory['totalResources']}")
    print(f"Total elements: {full_inventory['totalElements']}")
    print(f"USCDI elements (mustSupport): {full_inventory['totalUscdiElements']}")
    print(f"Required elements: {full_inventory['totalRequiredElements']}")
    print(f"Elements with description: {full_inventory['totalElementsWithDescription']}")
    print(f"Elements with binding: {full_inventory['totalElementsWithBinding']}")
    print(
        f"Description coverage: {full_inventory['totalElementsWithDescription']/full_inventory['totalElements']*100:.1f}%"
    )
    print(f"\nPer resource:")
    for r in resources:
        print(
            f"  {r['resourceType']}: {r['elementCount']} elements, {r['uscdiElementCount']} USCDI, {r['requiredElementCount']} required, example={r['hasExampleData']}"
        )


if __name__ == "__main__":
    main()
