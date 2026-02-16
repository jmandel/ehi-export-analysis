#!/usr/bin/env python3
"""
Parses the Paragon EHI Export CapabilityStatement.json and Extension-Details.xlsx
to produce entity-inventory-full.json and entity-inventory-summary.json.

Reads from ../downloads/paragon-25-1/
"""

import json
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(BASE, "..", "downloads", "paragon-25-1")
CS_PATH = os.path.join(DOWNLOADS, "CapabilityStatement.json")

# We'll parse extensions from the enrichment JSON since openpyxl may not be available
# but let's try openpyxl first, falling back to the enrichment extraction
EXT_XLSX = os.path.join(DOWNLOADS, "Extension-Details.xlsx")
EXT_ENRICHMENT = os.path.join(BASE, "..", "downloads", "enrichment", "extension-details-extracted.json")


def load_extensions():
    """Load extension details - try openpyxl first, fall back to enrichment JSON."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(EXT_XLSX, read_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(min_row=2, values_only=True))
        extensions = {}
        for row in rows:
            if len(row) >= 4:
                resource = str(row[0] or "").strip()
                key = str(row[1] or "").strip()
                name = str(row[2] or "").strip()
                definition = str(row[3] or "").strip()
                if resource:
                    if resource not in extensions:
                        extensions[resource] = []
                    extensions[resource].append({
                        "key": key,
                        "name": name,
                        "definition": definition
                    })
        wb.close()
        return extensions, "xlsx"
    except ImportError:
        # Fall back to enrichment JSON
        with open(EXT_ENRICHMENT) as f:
            data = json.load(f)
        extensions = {}
        for resource, exts in data["extensionsByResource"].items():
            extensions[resource] = [{
                "key": e["key"],
                "name": e["extensionName"],
                "definition": e["definition"]
            } for e in exts]
        return extensions, "enrichment-json"


def parse_capability_statement():
    with open(CS_PATH) as f:
        cs = json.load(f)

    extensions_by_resource, ext_source = load_extensions()

    metadata = {
        "resourceType": cs.get("resourceType"),
        "name": cs.get("name"),
        "title": cs.get("title"),
        "status": cs.get("status"),
        "date": cs.get("date"),
        "publisher": cs.get("publisher"),
        "fhirVersion": cs.get("fhirVersion"),
        "format": cs.get("format"),
        "description": cs.get("description", ""),
    }

    entities = []
    rest = cs.get("rest", [])
    if not rest:
        print("ERROR: No 'rest' section in CapabilityStatement", file=sys.stderr)
        return

    for resource in rest[0].get("resource", []):
        rtype = resource["type"]
        fields = []

        # Standard FHIR elements
        for ext in resource.get("extension", []):
            url = ext.get("url", "")
            name = ext.get("valueString", "")
            is_custom = "alterahealth.com" in url or "paragon" in url

            if not is_custom:
                # Standard element
                fields.append({
                    "name": name,
                    "source": "fhir-standard",
                    "type": None,  # Not specified in CapabilityStatement
                    "description": None,  # Not in CapabilityStatement for standard elements
                    "extension_url": url,
                    "is_custom": False,
                })
            else:
                # Custom Paragon extension - find definition from XLSX
                ext_name = name
                ext_def = None
                ext_key = url

                resource_exts = extensions_by_resource.get(rtype, [])
                for re_ext in resource_exts:
                    if re_ext["name"].lower().strip() == ext_name.lower().strip():
                        ext_def = re_ext["definition"]
                        ext_key = re_ext["key"]
                        break
                    # Try matching by key URL
                    if re_ext["key"] and re_ext["key"] in url:
                        ext_def = re_ext["definition"]
                        ext_key = re_ext["key"]
                        break

                fields.append({
                    "name": ext_name,
                    "source": "paragon-extension",
                    "type": None,
                    "description": ext_def,
                    "extension_url": url,
                    "extension_key": ext_key,
                    "is_custom": True,
                })

        # Check for extensions in XLSX not matched in CapabilityStatement
        cs_custom_names = {f["name"].lower().strip() for f in fields if f["is_custom"]}
        resource_exts = extensions_by_resource.get(rtype, [])
        xlsx_only = []
        for re_ext in resource_exts:
            if re_ext["name"].lower().strip() not in cs_custom_names:
                xlsx_only.append(re_ext)

        # Search params
        search_params = []
        for sp in resource.get("searchParam", []):
            search_params.append({
                "name": sp.get("name"),
                "type": sp.get("type"),
            })

        entity = {
            "entity": rtype,
            "category": categorize_resource(rtype),
            "field_count": len(fields),
            "standard_field_count": sum(1 for f in fields if not f["is_custom"]),
            "custom_extension_count": sum(1 for f in fields if f["is_custom"]),
            "fields_with_description": sum(1 for f in fields if f.get("description")),
            "fields": fields,
            "search_params": search_params,
            "xlsx_only_extensions": xlsx_only,
            "xlsx_only_count": len(xlsx_only),
        }
        entities.append(entity)

    # Summary stats
    total_fields = sum(e["field_count"] for e in entities)
    total_standard = sum(e["standard_field_count"] for e in entities)
    total_custom = sum(e["custom_extension_count"] for e in entities)
    total_with_desc = sum(e["fields_with_description"] for e in entities)
    total_xlsx_only = sum(e["xlsx_only_count"] for e in entities)

    full_inventory = {
        "metadata": metadata,
        "extension_source": ext_source,
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_standard_fields": total_standard,
        "total_custom_extensions": total_custom,
        "total_fields_with_description": total_with_desc,
        "total_xlsx_only_extensions": total_xlsx_only,
        "entities": entities,
    }

    # Write full inventory
    out_full = os.path.join(BASE, "entity-inventory-full.json")
    with open(out_full, "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"Wrote {out_full}")

    # Summary
    categories = {}
    for e in entities:
        cat = e["category"]
        if cat not in categories:
            categories[cat] = {"entity_count": 0, "field_count": 0, "custom_count": 0, "entities": []}
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += e["field_count"]
        categories[cat]["custom_count"] += e["custom_extension_count"]
        categories[cat]["entities"].append(e["entity"])

    summary = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_standard_fields": total_standard,
        "total_custom_extensions": total_custom,
        "total_fields_with_description": total_with_desc,
        "description_percentage": round(total_with_desc / total_fields * 100, 1) if total_fields else 0,
        "total_xlsx_only_extensions": total_xlsx_only,
        "categories": categories,
        "top_entities_by_fields": sorted(
            [{"entity": e["entity"], "total_fields": e["field_count"],
              "standard": e["standard_field_count"], "custom": e["custom_extension_count"]}
             for e in entities],
            key=lambda x: -x["total_fields"]
        )[:20],
        "entities_with_zero_fields": [e["entity"] for e in entities if e["field_count"] == 0],
    }

    out_summary = os.path.join(BASE, "entity-inventory-summary.json")
    with open(out_summary, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {out_summary}")

    # Print summary to stdout
    print(f"\n=== SUMMARY ===")
    print(f"Entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"  Standard FHIR: {total_standard}")
    print(f"  Custom Paragon: {total_custom}")
    print(f"  With descriptions: {total_with_desc} ({summary['description_percentage']}%)")
    print(f"  XLSX-only (not in CS): {total_xlsx_only}")
    print(f"\nBy category:")
    for cat, info in sorted(categories.items()):
        print(f"  {cat:20s}: {info['entity_count']:2d} entities, {info['field_count']:4d} fields ({info['custom_count']} custom)")
    print(f"\nEntities with zero fields: {summary['entities_with_zero_fields']}")


def categorize_resource(rtype):
    cats = {
        "demographics": ["Patient", "RelatedPerson", "Person"],
        "encounters": ["Encounter", "Appointment", "AppointmentResponse"],
        "clinical": ["AllergyIntolerance", "Condition", "Procedure", "CarePlan",
                      "CareTeam", "Goal", "FamilyMemberHistory", "Consent",
                      "DetectedIssue", "GuidanceResponse", "BodyStructure"],
        "medications": ["Medication", "MedicationRequest", "MedicationAdministration",
                        "MedicationDispense", "MedicationStatement", "NutritionOrder"],
        "diagnostics": ["Observation", "DiagnosticReport", "Specimen", "ImagingStudy"],
        "documents": ["DocumentReference", "Media"],
        "orders": ["ServiceRequest", "Communication", "CommunicationRequest"],
        "billing": ["Account", "Claim", "ChargeItem", "ChargeItemDefinition",
                     "Coverage", "CoverageEligibilityRequest", "CoverageEligibilityResponse",
                     "PaymentNotice", "PaymentReconciliation"],
        "immunizations": ["Immunization"],
        "infrastructure": ["Device", "Endpoint", "Location", "Organization",
                           "Practitioner", "PractitionerRole"],
    }
    for cat, types in cats.items():
        if rtype in types:
            return cat
    return "other"


if __name__ == "__main__":
    parse_capability_statement()
