"""
Parse the FHIR IG package and CSV schemas to produce a complete entity inventory.
Reads from:
  - downloads/enrichment/structure-definitions.json (pre-extracted FHIR StructureDefinitions)
  - downloads/enrichment/csv-schemas.json (pre-extracted CSV assessment schemas)
  - downloads/package/package/*.json (raw FHIR IG package files)
Outputs:
  - analysis/full-entity-inventory.json (complete machine-readable inventory)
  - analysis/summary-stats.json (aggregate statistics)
  - stdout: summary report
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/pointclickcare-technologies-inc--pointclickcare")
ANALYSIS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/pointclickcare-technologies-inc--pointclickcare/analysis")

def load_json(path):
    with open(path) as f:
        return json.load(f)

def classify_profile(profile):
    """Classify a FHIR profile into a data domain category."""
    pid = profile["id"].lower()
    name = profile.get("name", "").lower()
    desc = (profile.get("description") or "").lower()
    ptype = (profile.get("type") or "").lower()
    is_custom = profile.get("isCustomResource", False)

    # Extensions get their own category
    if profile.get("kind") == "complex-type" and "extension" in (profile.get("baseDefinition") or "").lower():
        return "Extension"

    # Custom resources
    if is_custom:
        if pid in ("billingstatement", "invoicetransaction", "claim", "payment", "authorization"):
            return "Billing & Financial"
        if pid == "census":
            return "Census / Admissions"
        if pid == "order":
            return "Orders"
        if pid == "careprofile":
            return "Care Profile"
        if pid in ("medicaldevice", "singledevice"):
            return "Medical Devices"
        return "Custom Resource"

    # Standard FHIR resource profiles
    if pid in ("patient",):
        return "Demographics"
    if pid in ("coverage",):
        return "Insurance / Coverage"
    if pid in ("encounter",):
        return "Encounters"
    if pid in ("condition",):
        return "Problems / Conditions"
    if pid in ("allergy-intolerance",):
        return "Allergies"
    if pid in ("medication", "medicationrequest", "medicationdispense"):
        return "Medications"
    if pid in ("immunization",):
        return "Immunizations"
    if "observation" in pid or pid in ("occupation",):
        return "Observations / Vitals"
    if pid in ("diagnostic-eport",):  # note: typo in PCC's naming
        return "Lab / Diagnostics"
    if pid in ("servicerequest",):
        return "Lab / Diagnostics"
    if pid in ("specimen",):
        return "Lab / Diagnostics"
    if pid in ("procedure",):
        return "Procedures"
    if pid in ("documentreference",):
        return "Clinical Notes / Documents"
    if pid in ("care-plan",):
        return "Care Plans / Goals"
    if pid in ("goal",):
        return "Care Plans / Goals"
    if pid in ("care-team",):
        return "Care Team"
    if pid in ("familymemberhistory",):
        return "Family History"
    if pid in ("implantable-device",):
        return "Medical Devices"
    if pid in ("relatedperson",):
        return "Demographics"
    if pid in ("practitioner", "practitionerrole"):
        return "Providers"
    if pid in ("organization",):
        return "Organizations"
    if pid in ("location",):
        return "Locations"
    if pid in ("provenance",):
        return "Provenance"

    return "Other"

def count_elements_with_descriptions(elements):
    """Count elements that have non-empty descriptions."""
    total = 0
    described = 0
    typed = 0
    for el in elements:
        total += 1
        d = el.get("definition") or el.get("short") or el.get("description") or ""
        if d.strip():
            described += 1
        if el.get("type"):
            typed += 1
    return total, described, typed

def process_profiles(sd_data):
    """Process FHIR StructureDefinition profiles into inventory entries."""
    entities = []
    for profile in sd_data["profiles"]:
        kind = profile.get("kind", "")
        base = profile.get("baseDefinition", "")

        # Skip extensions - we'll count them separately
        if kind == "complex-type" and "Extension" in base:
            continue

        elements = profile.get("elements", [])
        total_fields, described_fields, typed_fields = count_elements_with_descriptions(elements)

        category = classify_profile(profile)

        fields_detail = []
        for el in elements:
            field_info = {
                "path": el.get("path", ""),
                "type": el.get("type", ""),
                "short": el.get("short", ""),
                "definition": el.get("definition", ""),
                "min": el.get("min"),
                "max": el.get("max"),
            }
            # Include binding if present
            if el.get("binding"):
                field_info["binding"] = el["binding"]
            fields_detail.append(field_info)

        entity = {
            "id": profile["id"],
            "name": profile.get("name", profile["id"]),
            "source_type": "FHIR StructureDefinition",
            "resource_type": profile.get("type", ""),
            "is_custom_resource": profile.get("isCustomResource", False),
            "category": category,
            "description": profile.get("description", ""),
            "url": profile.get("url", ""),
            "base_definition": base,
            "status": profile.get("status", ""),
            "total_fields": total_fields,
            "fields_with_descriptions": described_fields,
            "fields_with_types": typed_fields,
            "fields": fields_detail,
        }
        entities.append(entity)

    return entities

def process_extensions(sd_data):
    """Process extension definitions separately."""
    extensions = []
    for profile in sd_data["profiles"]:
        kind = profile.get("kind", "")
        base = profile.get("baseDefinition", "")
        if kind == "complex-type" and "Extension" in base:
            elements = profile.get("elements", [])
            total_fields, described_fields, typed_fields = count_elements_with_descriptions(elements)
            ext = {
                "id": profile["id"],
                "name": profile.get("name", profile["id"]),
                "description": profile.get("description", ""),
                "url": profile.get("url", ""),
                "total_fields": total_fields,
                "fields_with_descriptions": described_fields,
                "value_type": "",
            }
            # Find the value[x] type
            for el in elements:
                if "value" in el.get("path", "").lower() and el.get("type"):
                    ext["value_type"] = el["type"]
                    break
            extensions.append(ext)
    return extensions

def process_csv_schemas(csv_data):
    """Process CSV assessment schemas into inventory entries."""
    entities = []
    for schema in csv_data["schemas"]:
        columns = schema.get("columns", [])
        total = len(columns)
        described = sum(1 for c in columns if (c.get("description") or "").strip())
        typed = sum(1 for c in columns if (c.get("type") or "").strip())

        source_page = schema.get("sourcePage", "")
        if "MDS" in source_page and "NonMDS" not in source_page:
            category = "MDS Assessments"
        else:
            category = "Non-MDS Assessments"

        fields_detail = []
        for col in columns:
            field_info = {
                "path": col.get("name", ""),
                "type": col.get("type", ""),
                "description": col.get("description", ""),
                "nullable": col.get("nullable"),
            }
            fields_detail.append(field_info)

        entity = {
            "id": f"csv-{schema['fileName'].replace('.csv', '')}",
            "name": schema["fileName"],
            "source_type": "CSV Schema",
            "resource_type": "CSV",
            "is_custom_resource": True,
            "category": category,
            "description": f"CSV file from {source_page} export",
            "url": "",
            "base_definition": "",
            "status": "active",
            "total_fields": total,
            "fields_with_descriptions": described,
            "fields_with_types": typed,
            "fields": fields_detail,
        }
        entities.append(entity)
    return entities

def process_value_sets(sd_data):
    """Extract value sets and code systems."""
    vs_info = []
    for vs in sd_data.get("valueSets", []):
        vs_info.append({
            "id": vs["id"],
            "name": vs["name"],
            "url": vs["url"],
            "concept_count": len(vs.get("concepts", [])),
            "concepts": vs.get("concepts", []),
        })
    cs_info = []
    for cs in sd_data.get("codeSystems", []):
        cs_info.append({
            "id": cs["id"],
            "name": cs["name"],
            "url": cs["url"],
            "concept_count": len(cs.get("concepts", [])),
            "concepts": cs.get("concepts", []),
        })
    return vs_info, cs_info


def main():
    sd_data = load_json(RESULTS_DIR / "downloads/enrichment/structure-definitions.json")
    csv_data = load_json(RESULTS_DIR / "downloads/enrichment/csv-schemas.json")

    # Process all entities
    fhir_entities = process_profiles(sd_data)
    csv_entities = process_csv_schemas(csv_data)
    extensions = process_extensions(sd_data)
    value_sets, code_systems = process_value_sets(sd_data)

    all_entities = fhir_entities + csv_entities

    # Compute summary statistics
    total_entities = len(all_entities)
    total_fields = sum(e["total_fields"] for e in all_entities)
    total_described = sum(e["fields_with_descriptions"] for e in all_entities)
    total_typed = sum(e["fields_with_types"] for e in all_entities)

    # Category breakdown
    categories = defaultdict(lambda: {"entity_count": 0, "field_count": 0, "described_count": 0})
    for e in all_entities:
        cat = e["category"]
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += e["total_fields"]
        categories[cat]["described_count"] += e["fields_with_descriptions"]

    # Separate standard vs custom FHIR resources
    standard_fhir = [e for e in fhir_entities if not e["is_custom_resource"]]
    custom_fhir = [e for e in fhir_entities if e["is_custom_resource"]]

    # Sort entities by field count (descending) for the "largest" view
    sorted_entities = sorted(all_entities, key=lambda x: x["total_fields"], reverse=True)

    summary = {
        "total_entities": total_entities,
        "standard_fhir_profiles": len(standard_fhir),
        "custom_fhir_resources": len(custom_fhir),
        "csv_schemas": len(csv_entities),
        "extensions": len(extensions),
        "value_sets": len(value_sets),
        "code_systems": len(code_systems),
        "total_fields": total_fields,
        "fields_with_descriptions": total_described,
        "description_percentage": round(total_described / total_fields * 100, 1) if total_fields > 0 else 0,
        "fields_with_types": total_typed,
        "type_percentage": round(total_typed / total_fields * 100, 1) if total_fields > 0 else 0,
        "category_breakdown": dict(categories),
        "top_20_by_field_count": [
            {"id": e["id"], "name": e["name"], "category": e["category"],
             "total_fields": e["total_fields"], "described": e["fields_with_descriptions"],
             "source_type": e["source_type"]}
            for e in sorted_entities[:20]
        ],
    }

    # Full inventory
    inventory = {
        "extraction_date": sd_data.get("extractionDate", ""),
        "ig_package": sd_data.get("igPackage", ""),
        "ig_version": sd_data.get("igVersion", ""),
        "fhir_version": sd_data.get("fhirVersion", ""),
        "summary": summary,
        "entities": all_entities,
        "extensions": extensions,
        "value_sets": value_sets,
        "code_systems": code_systems,
    }

    # Save outputs
    with open(ANALYSIS_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)

    with open(ANALYSIS_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("=" * 70)
    print("PointClickCare EHI Export — Entity Inventory Summary")
    print("=" * 70)
    print()
    print(f"FHIR IG Package: {sd_data.get('igPackage', 'N/A')}")
    print(f"IG Version: {sd_data.get('igVersion', 'N/A')}")
    print(f"FHIR Version: {sd_data.get('fhirVersion', 'N/A')}")
    print()
    print(f"Total entities (profiles + CSV schemas): {total_entities}")
    print(f"  Standard FHIR profiles: {len(standard_fhir)}")
    print(f"  Custom FHIR resources: {len(custom_fhir)}")
    print(f"  CSV schemas: {len(csv_entities)}")
    print(f"  Extensions: {len(extensions)}")
    print(f"  Value Sets: {len(value_sets)}")
    print(f"  Code Systems: {len(code_systems)}")
    print()
    print(f"Total fields across all entities: {total_fields}")
    print(f"  Fields with descriptions: {total_described} ({summary['description_percentage']}%)")
    print(f"  Fields with types: {total_typed} ({summary['type_percentage']}%)")
    print()
    print("CATEGORY BREAKDOWN:")
    print("-" * 70)
    print(f"{'Category':<30} {'Entities':>8} {'Fields':>8} {'Described':>10}")
    print("-" * 70)
    for cat in sorted(categories.keys()):
        c = categories[cat]
        print(f"{cat:<30} {c['entity_count']:>8} {c['field_count']:>8} {c['described_count']:>10}")
    print("-" * 70)
    print(f"{'TOTAL':<30} {total_entities:>8} {total_fields:>8} {total_described:>10}")
    print()
    print("TOP 20 ENTITIES BY FIELD COUNT:")
    print("-" * 70)
    print(f"{'Entity':<35} {'Cat':<20} {'Fields':>6} {'Desc':>6} {'Type'}")
    print("-" * 70)
    for e in sorted_entities[:20]:
        print(f"{e['id'][:35]:<35} {e['category'][:20]:<20} {e['total_fields']:>6} {e['fields_with_descriptions']:>6} {e['source_type']}")
    print()
    print("EXTENSIONS:")
    print("-" * 70)
    for ext in extensions:
        vt = ext.get("value_type", "")
        desc = (ext.get("description") or "")[:50]
        print(f"  {ext['id']:<35} type={vt:<15} {desc}")

    print()
    print("VALUE SETS:")
    for vs in value_sets:
        print(f"  {vs['name']}: {vs['concept_count']} concepts")
    print()
    print("CODE SYSTEMS:")
    for cs in code_systems:
        print(f"  {cs['name']}: {cs['concept_count']} concepts")

    print()
    print(f"Output saved to:")
    print(f"  {ANALYSIS_DIR / 'full-entity-inventory.json'}")
    print(f"  {ANALYSIS_DIR / 'summary-stats.json'}")

if __name__ == "__main__":
    main()
