#!/usr/bin/env python3
"""
Parse the IHS RPMS BREH EHI export schema (JSON format) directly from the raw .txt file.
Produces entity-inventory-full.json and entity-inventory-summary.json.

Schema structure:
  Top-level: {COMPILE TIME, DATA LOCATION, EXPORT TYPE, LOCATION, PATIENT: [{DFN, FILE: {FILE_<name>_<num>: ...}}], POINTER FILE: [...], ...}
  Each FILE entry: {"0": {ENTRY_IEN, FIELD_<name>_<num>: {...}, ...}, "FILE ORIGIN", "FILE VERSION", ...}
  Each FIELD: {FIELD_TYPE, DD_INFO: {FILE-SUBFILE, GLOBAL, NODE, PIECE}, VALUE_LIST?, POINTER_FILE?, POINTER_DATA?, ...}
"""

import json
import sys
import os
from collections import Counter, defaultdict

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "..", "downloads", "BREH_OIT_20250714.txt")


def parse_schema(path):
    """Parse the raw BREH schema JSON file."""
    with open(path, "r") as f:
        raw = json.load(f)

    metadata = {
        "schema_name": raw.get("SCHEMA NAME", {}).get("VALUE", ""),
        "version_status": raw.get("VERSION STATUS", {}).get("VALUE", ""),
        "public_url": raw.get("PUBLIC URL", {}).get("VALUE", ""),
        "compile_time": raw.get("COMPILE TIME", {}),
        "export_type": raw.get("EXPORT TYPE", {}),
    }

    # Patient files are under PATIENT[0].FILE
    patient_data = raw["PATIENT"][0]
    patient_files = patient_data.get("FILE", {})

    # Pointer/reference files
    pointer_files = raw.get("POINTER FILE", [])

    return metadata, patient_files, pointer_files


def parse_field_name_number(field_key):
    """Extract field name and number from key like 'FIELD_ACCIDENT TYPE_.83'"""
    # Remove FIELD_ prefix
    rest = field_key[6:]  # skip "FIELD_"
    # The field number is after the last underscore, but field names can contain underscores
    # Convention: FIELD_<NAME>_<NUMBER> where NUMBER is like .01, 1201, .83, etc.
    parts = rest.rsplit("_", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return rest, ""


def extract_fields(entry_data, file_name, file_key):
    """Extract all field definitions from a file's '0' entry."""
    fields = []
    for key, value in entry_data.items():
        if not key.startswith("FIELD_"):
            continue
        if not isinstance(value, dict):
            continue

        field_name, field_number = parse_field_name_number(key)
        field_type = value.get("FIELD_TYPE", "")
        if not field_type:
            # Fields without explicit FIELD_TYPE but with "0" subentry are
            # WORD PROCESSING or MULTIPLE-type fields in FileMan
            if "0" in value and isinstance(value["0"], dict):
                field_type = "WORD PROCESSING"
            else:
                field_type = "UNKNOWN"

        field = {
            "field_key": key,
            "field_name": field_name,
            "field_number": field_number,
            "field_type": field_type,
            "parent_file": file_name,
            "parent_file_key": file_key,
        }

        # DD_INFO metadata
        dd = value.get("DD_INFO", {})
        if dd:
            field["file_subfile"] = dd.get("FILE-SUBFILE", "")
            field["global"] = dd.get("GLOBAL", "")
            field["node"] = dd.get("NODE", "")
            field["piece"] = dd.get("PIECE", "")

        # Length constraints
        if value.get("MAXIMUM_LENGTH", "") != "":
            field["max_length"] = value["MAXIMUM_LENGTH"]
        if value.get("MINIMUM_LENGTH", "") != "":
            field["min_length"] = value["MINIMUM_LENGTH"]

        # Field sequence
        if "FIELD_SEQUENCE" in value:
            field["field_sequence"] = value["FIELD_SEQUENCE"]

        # Set of codes (value list)
        if "VALUE_LIST" in value:
            field["value_list"] = value["VALUE_LIST"]

        # Pointer info
        if "POINTER_FILE" in value:
            field["pointer_file"] = value["POINTER_FILE"]
        if "POINTER_FILE_NAME" in value:
            field["pointer_file_name"] = value["POINTER_FILE_NAME"]

        # Check for nested subfields (multiples / word-processing)
        subfield_keys = [k for k in value.keys() if k.startswith("FIELD_") and isinstance(value[k], dict)]
        if subfield_keys:
            subfields = []
            for sk in subfield_keys:
                sv = value[sk]
                sf_name, sf_number = parse_field_name_number(sk)
                sub = {
                    "field_key": sk,
                    "field_name": sf_name,
                    "field_number": sf_number,
                    "field_type": sv.get("FIELD_TYPE", "UNKNOWN"),
                    "is_subfield": True,
                }
                if "VALUE_LIST" in sv:
                    sub["value_list"] = sv["VALUE_LIST"]
                if "POINTER_FILE" in sv:
                    sub["pointer_file"] = sv["POINTER_FILE"]
                subfields.append(sub)
            field["subfields"] = subfields

        # Also check for nested entries via numbered keys (like "0" containing sub-entries)
        nested_entry_keys = [k for k in value.keys() if k == "0" and isinstance(value[k], dict)]
        if nested_entry_keys:
            nested_fields = extract_fields(value["0"], file_name, file_key)
            if nested_fields:
                field["subfields"] = field.get("subfields", []) + [
                    {k: v for k, v in nf.items() if k not in ("parent_file", "parent_file_key")}
                    for nf in nested_fields
                ]

        fields.append(field)
    return fields


def categorize_file(file_name):
    """Assign domain category based on file name patterns."""
    name = file_name.upper()

    if name.startswith("V ") or name == "VISIT":
        return "Clinical - PCC V-files"
    if any(x in name for x in ["PRESCRIPTION", "PHARMACY", "APSP", "DRUG", "RX ",
                                 "BCMA MEDICATION", "NON FORMULARY", "BPHR MED"]):
        return "Clinical - Pharmacy"
    if any(x in name for x in ["LAB ", "BLOOD ", "BLS ", "BLRA", "BLRAU", "PT LAB"]):
        return "Clinical - Laboratory"
    if any(x in name for x in ["MHSS", "BH CD", "MST HISTORY"]):
        return "Clinical - Behavioral Health"
    if "DENTAL" in name:
        return "Clinical - Dental"
    if any(x in name for x in ["BI PATIENT", "BI V IMMUNIZATION", "IZ EXPORT",
                                 "IMMUNIZATION"]):
        return "Clinical - Immunizations"
    if any(x in name for x in ["IMAGE", "IMAGING", "PACS", "TELEREADER",
                                 "MULTI IMAGE"]):
        return "Imaging"
    if any(x in name for x in ["3P BILL", "3P CLAIM", "3P CANCEL", "A/R ",
                                 "BILL/CLAIM", "BILLING", "CLAIMS TRACKING",
                                 "MEDICAID", "MEDICARE", "PRIVATE INSURANCE",
                                 "RAILROAD", "INSURANCE CLAIM", "INSURANCE REVIEW",
                                 "IB AUTO", "IB BILL", "INTEGRATED BILLING",
                                 "ABSP", "AGEV", "BENEFICIARY TRAVEL CLAIM",
                                 "CDMIS BILL", "CATEGORY C BILLING",
                                 "SPECIAL INPATIENT", "A/R FLAT", "A/R PREP",
                                 "A/R EDI", "A/R TRANS", "A/R ACCOUNT"]):
        return "Administrative - Billing"
    if any(x in name for x in ["PATIENT", "ENROLLMENT", "INPATIENT", "OUTPATIENT",
                                 "VA PATIENT", "REFERRAL PATIENT", "RAD/NUC MED PATIENT",
                                 "MSP PATIENT", "IB CONTINUOUS", "ICARE PATIENT",
                                 "BCDM PATIENT", "BW PATIENT", "GMRY PATIENT"]) and \
       "BILLING PATIENT" not in name:
        # Registration/patient management files
        if "BILLING" in name:
            return "Administrative - Billing"
        return "Administrative - Registration"
    if any(x in name for x in ["APPOINTMENT", "BSDX", "SCHEDULED", "SCHEDULING",
                                 "WAIT LIST", "WAITING LIST", "SD WAIT"]):
        return "Administrative - Scheduling"
    if any(x in name for x in ["RAD/NUC", "RADIATION"]) and "PATIENT" not in name:
        return "Clinical - Radiology"
    if any(x in name for x in ["ER ADMISSION", "ER VISIT", "EMERGENCY"]):
        return "Clinical - Emergency"
    if any(x in name for x in ["PROBLEM", "ADVERSE REACTION", "ALLERGY"]):
        return "Clinical - Problems/Allergies"
    if any(x in name for x in ["TIU ", "GMR TEXT", "NARRATIVE"]):
        return "Clinical - Documents/Notes"
    if any(x in name for x in ["ORDER", "REQUEST/CONSULTATION", "CONSULT"]):
        return "Clinical - Orders/Consults"
    if any(x in name for x in ["PRENATAL", "BJPN", "REPRODUCTIVE", "BIRTH",
                                 "V DELIVERY", "BW "]):
        return "Clinical - Women's Health/OB"
    if any(x in name for x in ["CARE PLAN", "TREATMENT PLAN", "PATIENT GOALS"]):
        return "Clinical - Care Plans"
    if any(x in name for x in ["CHR ", "CHS ", "CDMIS", "COMMUNITY"]):
        return "Administrative - Community Health"
    if any(x in name for x in ["ELDER CARE"]):
        return "Clinical - Elder Care"
    if any(x in name for x in ["ADVANCE DIRECTIVE", "LEGAL DOCS", "NOTICE OF PRIVACY",
                                 "RESTRICTED HEALTH", "ROI LISTING", "ACCESS RESTRICT"]):
        return "Administrative - Legal/Privacy"
    if any(x in name for x in ["INSURANCE", "POLICY", "GUARANTOR", "SPENDDOWN",
                                 "WORKMAN", "AUTO/LIABILITY", "THIRD PARTY",
                                 "PERSONAL POLICY", "BENEFIT"]):
        return "Administrative - Insurance/Coverage"

    return "Clinical - Other"


def parse_file_name_number(file_key):
    """Extract file name and number from key like 'FILE_3P BILL_9002274.4'"""
    rest = file_key[5:]  # skip "FILE_"
    parts = rest.rsplit("_", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return rest, ""


def main():
    metadata, patient_files, pointer_files = parse_schema(SCHEMA_FILE)

    entities = []
    total_fields = 0
    total_subfields = 0
    fields_with_description = 0
    fields_with_valueset = 0
    fields_with_pointer = 0

    for file_key, file_data in patient_files.items():
        file_name, file_number = parse_file_name_number(file_key)

        # Get the "0" entry which contains field definitions
        entry_data = file_data.get("0", {})
        fields = extract_fields(entry_data, file_name, file_key)
        field_count = len(fields)
        total_fields += field_count

        # Count subfields
        for f in fields:
            if "subfields" in f:
                total_subfields += len(f["subfields"])

        desc_count = sum(1 for f in fields if f.get("description"))
        vs_count = sum(1 for f in fields if f.get("value_list"))
        ptr_count = sum(1 for f in fields if f.get("pointer_file"))

        fields_with_description += desc_count
        fields_with_valueset += vs_count
        fields_with_pointer += ptr_count

        category = categorize_file(file_name)

        entity = {
            "file_key": file_key,
            "file_name": file_name,
            "file_number": file_number,
            "global": file_data.get("0", {}).get("ENTRY_IEN", {}).get("VALUE", ""),
            "file_origin": file_data.get("FILE ORIGIN", ""),
            "file_version": file_data.get("FILE VERSION", ""),
            "ehi_enabled": file_data.get("FILE_DEFINITION_4DW_ENABLED", False),
            "custom_file": file_data.get("FILE_DEFINITION_ALTERNATE_FILE_LOOKUP", False),
            "category": category,
            "field_count": field_count,
            "fields_with_description": desc_count,
            "fields_with_valueset": vs_count,
            "fields_with_pointer": ptr_count,
            "fields": fields,
        }
        entities.append(entity)

    # Sort by category then name
    entities.sort(key=lambda e: (e["category"], e["file_name"]))

    # Full inventory
    full_inventory = {
        "schema_version": "BREH_OIT_20250714",
        "metadata": metadata,
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_subfields": total_subfields,
        "fields_with_description": fields_with_description,
        "fields_with_valueset": fields_with_valueset,
        "fields_with_pointer": fields_with_pointer,
        "pointer_file_count": len(pointer_files),
        "entities": entities,
    }

    # Summary
    category_stats = defaultdict(lambda: {"count": 0, "fields": 0, "files": []})
    for e in entities:
        cat = e["category"]
        category_stats[cat]["count"] += 1
        category_stats[cat]["fields"] += e["field_count"]
        category_stats[cat]["files"].append(e["file_name"])

    type_counts = Counter()
    for e in entities:
        for f in e["fields"]:
            type_counts[f["field_type"]] += 1

    # Top entities by field count
    top_entities = sorted(entities, key=lambda e: e["field_count"], reverse=True)[:20]

    summary = {
        "schema_version": "BREH_OIT_20250714",
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_subfields": total_subfields,
        "fields_with_description": fields_with_description,
        "pct_fields_with_description": round(100 * fields_with_description / total_fields, 1) if total_fields else 0,
        "fields_with_valueset": fields_with_valueset,
        "fields_with_pointer": fields_with_pointer,
        "pointer_file_count": len(pointer_files),
        "field_type_distribution": dict(type_counts.most_common()),
        "category_breakdown": {
            cat: {"entity_count": v["count"], "field_count": v["fields"], "files": v["files"]}
            for cat, v in sorted(category_stats.items())
        },
        "top_20_entities_by_field_count": [
            {"file_name": e["file_name"], "category": e["category"], "field_count": e["field_count"]}
            for e in top_entities
        ],
    }

    out_dir = os.path.dirname(__file__)
    with open(os.path.join(out_dir, "entity-inventory-full.json"), "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"Wrote entity-inventory-full.json: {len(entities)} entities, {total_fields} fields")

    with open(os.path.join(out_dir, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")

    # Print summary to stdout
    print(f"\n=== SCHEMA SUMMARY ===")
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with description: {fields_with_description} ({summary['pct_fields_with_description']}%)")
    print(f"Fields with value sets: {fields_with_valueset}")
    print(f"Fields with pointers: {fields_with_pointer}")
    print(f"Pointer/reference files: {len(pointer_files)}")
    print(f"\n=== CATEGORIES ===")
    for cat in sorted(category_stats.keys()):
        v = category_stats[cat]
        print(f"  {cat}: {v['count']} entities, {v['fields']} fields")
    print(f"\n=== TOP 20 ENTITIES BY FIELD COUNT ===")
    for e in top_entities:
        print(f"  {e['file_name']}: {e['field_count']} fields ({e['category']})")

    print(f"\n=== FIELD TYPES ===")
    for t, c in type_counts.most_common():
        print(f"  {t}: {c}")


if __name__ == "__main__":
    main()
