#!/usr/bin/env python3
"""
Parse the IHS RPMS BREH EHI export schema (2025 version) into a complete
full-entity-inventory.json and compute summary statistics.

Input: ../../../results/indian-health-service--resource-and-patient-management-system-electronic-health-record/downloads/BREH_OIT_20250714.txt
Output:
  - full-entity-inventory.json  (complete parse of all 301 entities + all fields)
  - summary-stats.json          (aggregate statistics derived from the inventory)
"""

import json
import os
import sys
from collections import Counter, defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__),
    "../../../results/indian-health-service--resource-and-patient-management-system-electronic-health-record/downloads")
SCHEMA_FILE = os.path.join(RESULTS_DIR, "BREH_OIT_20250714.txt")
ENRICHMENT_DIR = os.path.join(RESULTS_DIR, "enrichment")

OUTPUT_DIR = os.path.dirname(__file__)

def parse_field(field_key, field_data):
    """Parse a single field from the raw schema into a normalized structure."""
    # Extract field name and number from key like "FIELD_DATE ESTABLISHED_.08"
    parts = field_key[len("FIELD_"):]
    # The last segment after _ is the field number
    last_underscore = parts.rfind("_")
    if last_underscore >= 0:
        field_name = parts[:last_underscore]
        field_number = parts[last_underscore + 1:]
    else:
        field_name = parts
        field_number = ""

    result = {
        "fieldKey": field_key,
        "fieldName": field_name,
        "fieldNumber": field_number,
        "fieldType": field_data.get("FIELD_TYPE", ""),
    }

    # DD_INFO
    dd = field_data.get("DD_INFO", {})
    if dd:
        result["fileSubfile"] = dd.get("FILE-SUBFILE")
        result["global"] = dd.get("GLOBAL", "")
        result["node"] = dd.get("NODE")
        result["piece"] = dd.get("PIECE")
        if dd.get("CHECK"):
            result["check"] = dd["CHECK"]

    result["fieldSequence"] = field_data.get("FIELD_SEQUENCE", "")

    # Handle WORD PROCESSING subfile fields (no FIELD_TYPE, have '0' subkey)
    if not result["fieldType"] and "0" in field_data:
        result["fieldType"] = "WORD PROCESSING"
        # Extract subfield info
        sub = field_data["0"]
        if isinstance(sub, dict):
            for sk, sv in sub.items():
                if sk.startswith("FIELD_") and isinstance(sv, dict):
                    sdd = sv.get("DD_INFO", {})
                    if sdd:
                        result["fileSubfile"] = sdd.get("FILE-SUBFILE")
                        result["global"] = sdd.get("GLOBAL", "")
                    result["wordSubFieldName"] = sv.get("WORD SUB-FIELD NAME", "")
                    break

    # Type-specific attributes
    ft = result["fieldType"]

    if ft == "SET OF CODES":
        value_list = field_data.get("VALUE_LIST", [])
        if value_list:
            result["valueList"] = [{"code": v.get("INTERNAL_CODE", ""), "value": v.get("VALUE", "")} for v in value_list]
        elif "INTERNAL_CODE" in field_data and "VALUE" in field_data:
            # Single value entry
            result["valueList"] = [{"code": field_data["INTERNAL_CODE"], "value": field_data["VALUE"]}]

    if ft in ("FREE TEXT",):
        if "MINIMUM_LENGTH" in field_data and field_data["MINIMUM_LENGTH"] != "":
            result["minLength"] = field_data["MINIMUM_LENGTH"]
        if "MAXIMUM_LENGTH" in field_data and field_data["MAXIMUM_LENGTH"] != "":
            result["maxLength"] = field_data["MAXIMUM_LENGTH"]

    if ft == "NUMERIC":
        if "LOWER_BOUND" in field_data and field_data["LOWER_BOUND"] != "":
            result["lowerBound"] = field_data["LOWER_BOUND"]
        if "UPPER_BOUND" in field_data and field_data["UPPER_BOUND"] != "":
            result["upperBound"] = field_data["UPPER_BOUND"]
        if "DECIMAL_PLACES" in field_data and field_data["DECIMAL_PLACES"] != "":
            result["decimalPlaces"] = field_data["DECIMAL_PLACES"]

    if ft == "POINTER TO A FILE":
        # Direct pointer reference at field level
        if "POINTER_FILE" in field_data:
            result["pointsToFileNumber"] = field_data["POINTER_FILE"]
            result["pointsToFileName"] = field_data.get("POINTER_FILE_NAME", "")
        # Embedded pointer data
        ptr = field_data.get("POINTER_DATA", {})
        if ptr:
            for pk, pv in ptr.items():
                if pk.startswith("FIELD_"):
                    pdd = pv.get("DD_INFO", {})
                    if pdd and "FILE-SUBFILE" in pdd:
                        if "pointsToFileNumber" not in result:
                            result["pointsToFileNumber"] = pdd["FILE-SUBFILE"]
                        result["pointsToGlobal"] = pdd.get("GLOBAL", "")
                    break

    if ft == "DATE/TIME":
        result["hasUtcOffset"] = "UTC_OFFSET" in field_data

    if ft in ("WORD PROCESSING", "WORD-PROCESSING"):
        result["wordSubFieldName"] = field_data.get("WORD SUB-FIELD NAME", "")

    if ft == "VARIABLE-POINTER":
        vp_list = field_data.get("VARIABLE_POINTER_DATA", [])
        if vp_list:
            result["variablePointers"] = vp_list

    return result


def parse_file_entry(file_key, file_entry):
    """Parse a single file/table from the raw schema."""
    # Extract name and number from key like "FILE_*MHSS PATIENT TP GOALS 2_9002011.63"
    parts = file_key[len("FILE_"):]
    last_underscore = parts.rfind("_")
    if last_underscore >= 0:
        file_name = parts[:last_underscore]
        file_number = parts[last_underscore + 1:]
    else:
        file_name = parts
        file_number = ""

    result = {
        "fileKey": file_key,
        "fileName": file_name,
        "fileNumber": file_number,
        "global": file_entry.get("FILE_DEFINITION_GLOBAL", ""),
        "ehiEnabled": file_entry.get("FILE_DEFINITION_EHI_ENABLED", "") == "ENABLED",
        "customFile": file_entry.get("FILE_DEFINITION_CUSTOM_FILE", "") not in ("", "0"),
        "fileVersion": file_entry.get("FILE VERSION", ""),
        "fileOrigin": file_entry.get("FILE ORIGIN", ""),
        "fileSequence": file_entry.get("FILE_SEQUENCE", ""),
        "lookupType": file_entry.get("FILE_DEFINITION_LOOKUP_TYPE", ""),
        "storedName": file_entry.get("FILE_DEFINITION_STORED_NAME", ""),
    }

    # Parse fields from the "0" key
    fields = []
    zero = file_entry.get("0", {})
    if isinstance(zero, dict):
        for k, v in sorted(zero.items()):
            if k.startswith("FIELD_") and isinstance(v, dict):
                field = parse_field(k, v)
                fields.append(field)

    result["fields"] = fields
    result["fieldCount"] = len(fields)

    return result


def categorize_file(file_name):
    """Categorize a file into a domain based on its name."""
    name = file_name.upper()

    if name.startswith("V ") or name == "VISIT":
        return "Clinical - PCC V-files"
    if any(x in name for x in ["PRESCRIPTION", "PHARMACY", "APSP", "DRUG ACCOUNT",
                                  "RX SUSPENSE", "RX VERIFY", "BCMA MEDICATION",
                                  "PATIENT NOTIFICATION (RX", "IB BILL/CLAIMS PRESCRIPTION"]):
        return "Clinical - Pharmacy"
    if any(x in name for x in ["LAB DATA", "LAB ORDER", "BLRA", "BLRAU", "BLS LOINC",
                                  "BLOOD INVENTORY", "PT LAB"]):
        return "Clinical - Laboratory"
    if any(x in name for x in ["MHSS", "BH CD", "MST HISTORY"]):
        return "Clinical - Behavioral Health"
    if "DENTAL" in name:
        return "Clinical - Dental"
    if name.startswith("BI ") or name == "IZ EXPORTS":
        return "Clinical - Immunizations"
    if any(x in name for x in ["IMAGE", "IMAGING", "PACS", "TELEREADER", "MULTI IMAGE"]):
        return "Imaging"
    if any(x in name for x in ["3P BILL", "3P CLAIM", "3P CANCEL", "A/R ", "ABSP",
                                  "AGEV INSURANCE", "BILLING", "CLAIMS TRACKING",
                                  "INTEGRATED BILLING", "INSURANCE CLAIM",
                                  "INSURANCE REVIEW", "MEDICAID", "MEDICARE",
                                  "PRIVATE INSURANCE", "RAILROAD", "SPECIAL INPATIENT",
                                  "BENEFICIARY TRAVEL CLAIM", "CATEGORY C BILLING",
                                  "CDMIS BILL", "IB AUTOMATED", "BILL/CLAIMS"]):
        return "Administrative - Billing"
    if any(x in name for x in ["PATIENT_9000001", "VA PATIENT", "ENROLLMENT",
                                  "INPATIENT ", "OUTPATIENT", "PATIENT MOVEMENT",
                                  "PATIENT NAME", "PATIENT ALLERG", "PATIENT APPLICATION",
                                  "PATIENT ENROLLMENT", "PATIENT GOAL", "PATIENT IMPLANT",
                                  "PATIENT REFUSAL", "PATIENT'S LEGAL", "PRE-REGISTRATION",
                                  "ORDER CHECK PATIENT", "IB CONTINUOUS", "MSP PATIENT",
                                  "GMRY PATIENT", "OE/RR PATIENT", "PENDING OUTPATIENT",
                                  "RAD/NUC MED PATIENT", "REFERRAL PATIENT",
                                  "TRANSMITTED OUTPATIENT", "DELETED OUTPATIENT",
                                  "SDSC SERVICE", "AG ", "AGVQ", "ICARE PATIENT",
                                  "BW PATIENT", "BCDM PATIENT", "OUTPATIENT CLASSIFICATION"]):
        return "Administrative - Registration"
    if file_name == "PATIENT":
        return "Administrative - Registration"
    if any(x in name for x in ["APPOINTMENT", "BSDX", "SCHEDULED", "SCHEDULING",
                                  "WAIT LIST", "WAITING LIST", "SD WAIT", "SDWL"]):
        return "Administrative - Scheduling"

    return "Clinical - Other"


def main():
    print(f"Loading schema from {SCHEMA_FILE}...")
    with open(SCHEMA_FILE) as f:
        schema = json.load(f)

    # Parse all patient files
    raw_files = schema["PATIENT"][0]["FILE"]
    print(f"Found {len(raw_files)} files in schema")

    entities = []
    for file_key in sorted(raw_files.keys()):
        file_entry = raw_files[file_key]
        parsed = parse_file_entry(file_key, file_entry)
        parsed["category"] = categorize_file(parsed["fileName"])
        entities.append(parsed)

    # Parse pointer files (list of dicts with FILE_NAME, FILE_NUMBER, GLOBAL, FIELDS)
    raw_pointers = schema.get("POINTER FILE", [])
    pointer_files = []
    if isinstance(raw_pointers, list):
        for pv in raw_pointers:
            pf = {
                "fileName": pv.get("FILE_NAME", ""),
                "fileNumber": pv.get("FILE_NUMBER", ""),
                "global": pv.get("GLOBAL", ""),
                "fileSequence": pv.get("FILE_SEQUENCE", ""),
            }
            # Each has a FIELDS list with one entry containing FIELD REFERENCE
            fields = pv.get("FIELDS", [])
            if fields and isinstance(fields, list):
                fr = fields[0].get("FIELD REFERENCE", "")
                pf["fieldReference"] = fr
            pointer_files.append(pf)

    # Build full inventory
    inventory = {
        "schemaVersion": "BREH_OIT_20250714",
        "schemaDate": "2025-07-14",
        "exportType": "EHI",
        "totalEntities": len(entities),
        "totalFields": sum(e["fieldCount"] for e in entities),
        "totalPointerFiles": len(pointer_files),
        "entities": entities,
        "pointerFiles": pointer_files,
    }

    # Write full inventory
    inv_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(inv_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote full-entity-inventory.json ({os.path.getsize(inv_path):,} bytes)")

    # Compute summary statistics
    total_fields = inventory["totalFields"]
    type_counts = Counter()
    fields_with_valuelist = 0
    fields_with_constraints = 0
    fields_with_pointer = 0
    fields_with_check = 0

    for entity in entities:
        for field in entity["fields"]:
            ft = field.get("fieldType", "")
            type_counts[ft] += 1
            if "valueList" in field:
                fields_with_valuelist += 1
            if any(k in field for k in ("minLength", "maxLength", "lowerBound", "upperBound")):
                fields_with_constraints += 1
            if "pointsToFile" in field or field.get("fieldType") == "POINTER TO A FILE":
                fields_with_pointer += 1
            if "check" in field:
                fields_with_check += 1

    # Category breakdown
    category_stats = defaultdict(lambda: {"entityCount": 0, "fieldCount": 0, "entities": []})
    for entity in entities:
        cat = entity["category"]
        category_stats[cat]["entityCount"] += 1
        category_stats[cat]["fieldCount"] += entity["fieldCount"]
        category_stats[cat]["entities"].append({
            "fileName": entity["fileName"],
            "fieldCount": entity["fieldCount"],
            "ehiEnabled": entity["ehiEnabled"],
        })

    # Top entities by field count
    top_entities = sorted(entities, key=lambda e: e["fieldCount"], reverse=True)[:20]

    summary = {
        "totalEntities": len(entities),
        "totalFields": total_fields,
        "totalPointerFiles": len(pointer_files),
        "fieldsWithValueSets": fields_with_valuelist,
        "fieldsWithConstraints": fields_with_constraints,
        "fieldsPointerType": fields_with_pointer,
        "fieldsWithValidationCheck": fields_with_check,
        "fieldsWithDescriptions": 0,  # Schema doesn't include narrative descriptions
        "fieldTypeDistribution": dict(type_counts.most_common()),
        "categoryBreakdown": {k: {"entityCount": v["entityCount"], "fieldCount": v["fieldCount"]}
                              for k, v in sorted(category_stats.items())},
        "categoryDetail": {k: v for k, v in sorted(category_stats.items())},
        "top20EntitiesByFieldCount": [
            {"fileName": e["fileName"], "fileNumber": e["fileNumber"],
             "fieldCount": e["fieldCount"], "category": e["category"]}
            for e in top_entities
        ],
        "ehiEnabledCount": sum(1 for e in entities if e["ehiEnabled"]),
        "customFileCount": sum(1 for e in entities if e["customFile"]),
    }

    stats_path = os.path.join(OUTPUT_DIR, "summary-stats.json")
    with open(stats_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote summary-stats.json ({os.path.getsize(stats_path):,} bytes)")

    # Print key stats
    print(f"\n=== Summary Statistics ===")
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Total pointer/reference files: {len(pointer_files)}")
    print(f"Fields with value sets: {fields_with_valuelist}")
    print(f"Fields with constraints: {fields_with_constraints}")
    print(f"Fields of pointer type: {fields_with_pointer}")
    print(f"Fields with validation checks: {fields_with_check}")
    print(f"EHI-enabled files: {summary['ehiEnabledCount']}")
    print(f"Custom files: {summary['customFileCount']}")
    print()
    print("Field type distribution:")
    for ft, count in type_counts.most_common():
        print(f"  {ft}: {count}")
    print()
    print("Category breakdown:")
    for cat in sorted(category_stats.keys()):
        cs = category_stats[cat]
        print(f"  {cat}: {cs['entityCount']} entities, {cs['fieldCount']} fields")
    print()
    print("Top 20 entities by field count:")
    for e in top_entities:
        print(f"  {e['fileName']} ({e['fileNumber']}): {e['fieldCount']} fields [{e['category']}]")


if __name__ == "__main__":
    main()
