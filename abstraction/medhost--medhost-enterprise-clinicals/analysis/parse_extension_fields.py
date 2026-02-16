#!/usr/bin/env python3
"""
Parses MEDHOST-FHIR-Extension-Fields.xlsx from raw source into complete JSON inventory.
Reads all sheets, extracts every field with all available metadata.
Outputs: entity-inventory-full.json, entity-inventory-summary.json
"""

import json
import openpyxl
from pathlib import Path
from collections import defaultdict

XLSX_PATH = Path(__file__).parent.parent / "downloads" / "MEDHOST-FHIR-Extension-Fields.xlsx"
OUT_FULL = Path(__file__).parent / "entity-inventory-full.json"
OUT_SUMMARY = Path(__file__).parent / "entity-inventory-summary.json"

# Map sheet names to FHIR resource types and categories
SHEET_META = {
    "Directions": {"resource": "Directions", "category": "Reference", "skip": True},
    "Main": {"resource": "Main", "category": "Reference", "skip": True},
    "Allergy": {"resource": "AllergyIntolerance", "category": "Clinical"},
    "Ancillary Order": {"resource": "ServiceRequest", "category": "Orders"},
    "Appointment": {"resource": "Appointment", "category": "Administrative"},
    "Charge Item": {"resource": "ChargeItem", "category": "Billing"},
    "Condition": {"resource": "Condition", "category": "Clinical"},
    "Condition-Past Medical History": {"resource": "Condition", "category": "Clinical"},
    "Consent": {"resource": "Consent", "category": "Administrative"},
    "Coverage": {"resource": "Coverage", "category": "Insurance"},
    "Detected Issue": {"resource": "DetectedIssue", "category": "Clinical Decision Support"},
    "Diagnostic Report": {"resource": "DiagnosticReport", "category": "Diagnostics"},
    "Discharge Plan (CarePlan)": {"resource": "CarePlan", "category": "Clinical"},
    "Encounter": {"resource": "Encounter", "category": "Clinical"},
    "Family Member History": {"resource": "FamilyMemberHistory", "category": "Clinical"},
    "Goal": {"resource": "Goal", "category": "Clinical"},
    "Immunization": {"resource": "Immunization", "category": "Clinical"},
    "Implantable Device": {"resource": "Device", "category": "Clinical"},
    "Location": {"resource": "Location", "category": "Administrative"},
    "MDRO": {"resource": "Observation", "category": "Clinical"},
    "Medication Administration": {"resource": "MedicationAdministration", "category": "Medications"},
    "MedicationRequest-Discharge Med": {"resource": "MedicationRequest", "category": "Medications"},
    "MedicationRequest-InpatientMed": {"resource": "MedicationRequest", "category": "Medications"},
    "MedicationRequest-Prescriptions": {"resource": "MedicationRequest", "category": "Medications"},
    "MedicationStatement-HomeMed": {"resource": "MedicationStatement", "category": "Medications"},
    "Observation Alcohol Use": {"resource": "Observation", "category": "Social History"},
    "Observation Drug Use": {"resource": "Observation", "category": "Social History"},
    "Observation Education": {"resource": "Observation", "category": "Social History"},
    "Observation General Comment": {"resource": "Observation", "category": "Clinical"},
    "Observation Labs": {"resource": "Observation", "category": "Diagnostics"},
    "Observation Marital Status": {"resource": "Observation", "category": "Social History"},
    "Observation Occupation": {"resource": "Observation", "category": "Social History"},
    "Observation Sexual Behavior": {"resource": "Observation", "category": "Social History"},
    "Observation Travel": {"resource": "Observation", "category": "Social History"},
    "Past Procedure": {"resource": "Procedure", "category": "Clinical"},
    "Patient": {"resource": "Patient", "category": "Demographics"},
    "PC Orders (Service Request)": {"resource": "ServiceRequest", "category": "Orders"},
    "Practitioner": {"resource": "Practitioner", "category": "Administrative"},
    "Problem": {"resource": "Problem", "category": "Clinical"},
    "Procedure": {"resource": "Procedure", "category": "Clinical"},
    "Question Answer": {"resource": "QuestionnaireResponse", "category": "Clinical"},
    "Related Person": {"resource": "RelatedPerson", "category": "Demographics"},
    "Smoking Status": {"resource": "Observation", "category": "Social History"},
}

SKIP_SHEETS = {"MEDHOST", "_reference"}

# Standard header names we look for
STD_HEADERS = {
    "field_name": ["Field Name"],
    "version": ["Version"],
    "fhir_type": ["FHIR Field Type"],
    "max_length": ["Max Field Length"],
    "description": ["Field Description", "Field Description/Definition"],
    "enterprise_db": ["Enterprise Database table/col (internal use only)"],
    "edis_db": ["EDIS database table/col (internal use only)"],
    "yourcare_db": ["Y database table/col (internal use only)"],
    "comment": ["Comment"],
}


def normalize_header(h):
    """Map actual header text to a standard key."""
    if not h:
        return None
    h = str(h).strip()
    for key, variants in STD_HEADERS.items():
        if h in variants:
            return key
    return None


def parse_workbook():
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True, data_only=True)
    entities = []
    parse_errors = []

    for sheet_name in wb.sheetnames:
        if sheet_name in SKIP_SHEETS:
            continue

        meta = SHEET_META.get(sheet_name, {"resource": sheet_name, "category": "Unknown"})
        if meta.get("skip"):
            continue

        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue

        # Find header row (first row with "Field Name" in it)
        header_row_idx = None
        raw_headers = []
        for i, row in enumerate(rows):
            for cell in row:
                if cell and "Field Name" in str(cell):
                    header_row_idx = i
                    raw_headers = [str(c).strip() if c else None for c in row]
                    break
            if header_row_idx is not None:
                break

        if header_row_idx is None:
            parse_errors.append({"sheet": sheet_name, "error": "No header row found"})
            continue

        # Map headers
        header_map = {}
        for col_idx, h in enumerate(raw_headers):
            key = normalize_header(h)
            if key and key not in header_map:
                header_map[key] = col_idx

        # Parse data rows
        fields = []
        for row in rows[header_row_idx + 1:]:
            # Skip empty rows
            if not any(cell for cell in row):
                continue

            field = {}
            for key, col_idx in header_map.items():
                if col_idx < len(row):
                    val = row[col_idx]
                    if val is not None:
                        val = str(val).strip() if not isinstance(val, (int, float)) else val
                    field[key] = val

            # Skip rows without a field name
            if not field.get("field_name"):
                continue

            # Skip noise rows (notes, section headers, etc.)
            name = str(field["field_name"]).strip()
            if (name.startswith("Note:") or
                name.startswith("CodeableConcept combines") or
                not field.get("fhir_type")):
                continue

            fields.append(field)

        # Check description quality
        described_count = sum(
            1 for f in fields
            if f.get("description") and str(f["description"]).strip()
            and str(f["description"]).strip().lower() not in ("n/a", "null", "none", "")
        )

        entity = {
            "sheet_name": sheet_name,
            "fhir_resource": meta["resource"],
            "category": meta["category"],
            "field_count": len(fields),
            "fields_with_descriptions": described_count,
            "fields": fields,
        }
        entities.append(entity)

    wb.close()
    return entities, parse_errors


def build_summary(entities):
    total_fields = sum(e["field_count"] for e in entities)
    total_described = sum(e["fields_with_descriptions"] for e in entities)

    # By category
    cat_stats = defaultdict(lambda: {"entities": 0, "fields": 0, "described": 0})
    for e in entities:
        cat = e["category"]
        cat_stats[cat]["entities"] += 1
        cat_stats[cat]["fields"] += e["field_count"]
        cat_stats[cat]["described"] += e["fields_with_descriptions"]

    # By FHIR resource
    res_stats = defaultdict(lambda: {"sheets": [], "fields": 0})
    for e in entities:
        res = e["fhir_resource"]
        res_stats[res]["sheets"].append(e["sheet_name"])
        res_stats[res]["fields"] += e["field_count"]

    # Unique FHIR resources
    unique_resources = sorted(set(e["fhir_resource"] for e in entities))

    # Entity summary table
    entity_table = [
        {
            "sheet_name": e["sheet_name"],
            "fhir_resource": e["fhir_resource"],
            "category": e["category"],
            "field_count": e["field_count"],
            "fields_with_descriptions": e["fields_with_descriptions"],
            "pct_described": round(100 * e["fields_with_descriptions"] / e["field_count"], 1) if e["field_count"] > 0 else 0,
        }
        for e in entities
    ]

    return {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_fields_with_descriptions": total_described,
        "pct_described": round(100 * total_described / total_fields, 1) if total_fields > 0 else 0,
        "unique_fhir_resources": unique_resources,
        "unique_fhir_resource_count": len(unique_resources),
        "by_category": {k: dict(v) for k, v in sorted(cat_stats.items())},
        "by_fhir_resource": {k: dict(v) for k, v in sorted(res_stats.items())},
        "entity_table": entity_table,
    }


if __name__ == "__main__":
    entities, errors = parse_workbook()
    summary = build_summary(entities)

    if errors:
        summary["parse_errors"] = errors

    with open(OUT_FULL, "w") as f:
        json.dump(entities, f, indent=2)

    with open(OUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Entities: {summary['total_entities']}")
    print(f"Fields: {summary['total_fields']}")
    print(f"Described: {summary['total_fields_with_descriptions']} ({summary['pct_described']}%)")
    print(f"FHIR resources: {summary['unique_fhir_resource_count']}")
    if errors:
        print(f"Parse errors: {len(errors)}")
        for e in errors:
            print(f"  {e['sheet']}: {e['error']}")
    print(f"\nBy category:")
    for cat, stats in sorted(summary["by_category"].items()):
        print(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields")
