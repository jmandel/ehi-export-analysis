"""
Parse the IHS BREH EHI export schema (2025 version) and produce:
1. full-entity-inventory.json - complete machine-readable extraction
2. summary-stats.json - aggregate statistics
3. category-breakdown.json - per-category counts
"""
import json
import sys
import os
from collections import Counter, defaultdict

SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..",
    "results/indian-health-service--resource-and-patient-management-system-electronic-health-rec",
    "downloads/BREH_OIT_20250714.txt"
)
OUTPUT_DIR = os.path.dirname(__file__)

def parse_field(field_key, field_data, parent_file_name):
    """Parse a single field definition, recursively handling subfields."""
    # Extract field name and number from key like "FIELD_NAME_.01"
    parts = field_key.replace("FIELD_", "", 1)
    # Split on last underscore-dot pattern to get name and number
    name = parts
    field_number = ""
    # Try to find the field number (after last _)
    last_underscore = parts.rfind("_")
    if last_underscore > 0:
        possible_num = parts[last_underscore+1:]
        if possible_num and (possible_num[0].isdigit() or possible_num[0] == '.'):
            name = parts[:last_underscore]
            field_number = possible_num

    result = {
        "name": name,
        "field_number": field_number,
        "field_type": field_data.get("FIELD_TYPE", ""),
        "field_sequence": field_data.get("FIELD_SEQUENCE", ""),
    }

    # DD_INFO
    dd = field_data.get("DD_INFO", {})
    if dd:
        result["dd_info"] = {
            "file_subfile": dd.get("FILE-SUBFILE", ""),
            "global": dd.get("GLOBAL", ""),
            "node": dd.get("NODE", ""),
            "piece": dd.get("PIECE", ""),
            "check": dd.get("CHECK", ""),
        }

    # Pointer reference
    if "POINTER_FILE" in field_data:
        result["pointer_file"] = field_data["POINTER_FILE"]
    if "POINTER_FILE_NAME" in field_data:
        result["pointer_file_name"] = field_data["POINTER_FILE_NAME"]

    # Value set for SET OF CODES
    if "VALUE_LIST" in field_data:
        result["value_list"] = field_data["VALUE_LIST"]

    # Numeric constraints
    for k in ["MAXIMUM_LENGTH", "MINIMUM_LENGTH", "MAXIMUM_VALUE", "MINIMUM_VALUE",
              "DECIMAL_PLACES", "UPPER_BOUND", "LOWER_BOUND"]:
        if k in field_data and field_data[k] != "":
            result[k.lower()] = field_data[k]

    # Word processing sub-field
    if "WORD SUB-FIELD NAME" in field_data:
        result["word_subfield_name"] = field_data["WORD SUB-FIELD NAME"]

    # Variable pointer
    if "VARIABLE_POINTER" in field_data:
        result["variable_pointer"] = field_data["VARIABLE_POINTER"]

    # Internal values
    if "INTERNAL_DATE" in field_data:
        result["internal_date"] = field_data["INTERNAL_DATE"]

    # Check for nested subfields (multiples/subfiles)
    if isinstance(field_data, dict) and "0" in field_data:
        subentry = field_data["0"]
        if isinstance(subentry, dict):
            subfields = []
            for sk, sv in subentry.items():
                if sk.startswith("FIELD_") and isinstance(sv, dict):
                    subfields.append(parse_field(sk, sv, parent_file_name))
            if subfields:
                result["subfields"] = subfields

    return result


def count_fields_recursive(fields_list):
    """Count total fields including subfields."""
    total = 0
    for f in fields_list:
        total += 1
        if "subfields" in f:
            total += count_fields_recursive(f["subfields"])
    return total


def flatten_fields(fields_list, prefix=""):
    """Flatten nested fields for counting."""
    result = []
    for f in fields_list:
        full_name = f"{prefix}{f['name']}" if not prefix else f"{prefix}.{f['name']}"
        result.append({**f, "full_name": full_name})
        if "subfields" in f:
            result.extend(flatten_fields(f["subfields"], full_name))
    return result


# Domain categorization rules
def categorize_file(file_name):
    name_upper = file_name.upper()
    if name_upper.startswith("V ") or name_upper == "VISIT":
        return "Clinical - PCC V-files"
    if any(x in name_upper for x in ["PRESCRIPTION", "PHARMACY", "APSP", "PSO", "RX ",
                                      "DRUG ACCOUNTABILITY", "IB BILL/CLAIMS PRESCRIPTION",
                                      "PATIENT NOTIFICATION (RX"]):
        return "Clinical - Pharmacy"
    if any(x in name_upper for x in ["LAB DATA", "LAB ORDER", "BLRA ", "BLRAU", "BLS LOINC",
                                      "BLOOD INVENTORY", "PT LAB"]):
        return "Clinical - Laboratory"
    if any(x in name_upper for x in ["MHSS", "BH CD", "SUICIDE"]):
        return "Clinical - Behavioral Health"
    if "DENTAL" in name_upper:
        return "Clinical - Dental"
    if any(x in name_upper for x in ["BI PATIENT", "BI V IMMUN", "IZ EXPORT"]):
        return "Clinical - Immunizations"
    if any(x in name_upper for x in ["IMAGE", "IMAGING", "PACS", "TELEREADER", "MULTI IMAGE"]):
        return "Imaging"
    if any(x in name_upper for x in ["3P ", "A/R ", "ABSP", "AGEV", "BILL", "CLAIM",
                                      "MEDICAID", "MEDICARE", "PRIVATE INSURANCE",
                                      "RAILROAD", "INSURANCE REVIEW", "INTEGRATED BILLING",
                                      "SPECIAL INPATIENT BILLING", "CATEGORY C BILLING",
                                      "CDMIS BILL", "BENEFICIARY TRAVEL CLAIM"]):
        return "Administrative - Billing"
    if any(x in name_upper for x in ["SCHEDUL", "WAIT LIST", "WAITING LIST", "BSDX APPOINT",
                                      "APPOINTMENT PFSS", "SD WAIT"]):
        return "Administrative - Scheduling"
    return "Clinical - Other / Administrative"


def main():
    print(f"Loading schema from {SCHEMA_PATH}")
    with open(SCHEMA_PATH) as f:
        schema = json.load(f)

    patient = schema["PATIENT"][0]
    files_dict = patient["FILE"]
    pointer_files = schema.get("POINTER FILE", {})

    entities = []
    total_top_level_fields = 0
    total_all_fields = 0
    type_counter = Counter()
    category_counts = defaultdict(lambda: {"files": 0, "top_level_fields": 0, "all_fields": 0, "file_list": []})

    for file_key, file_data in sorted(files_dict.items()):
        # Parse file key: FILE_{NAME}_{NUMBER}
        parts = file_key.split("_", 1)
        if len(parts) < 2:
            continue
        rest = parts[1]  # e.g., "*MHSS PATIENT TP GOALS 2_9002011.63"
        # Find file number (last _ segment that starts with digit)
        last_us = rest.rfind("_")
        if last_us > 0:
            file_name = rest[:last_us]
            file_number = rest[last_us+1:]
        else:
            file_name = rest
            file_number = ""

        # File metadata
        entity = {
            "file_key": file_key,
            "file_name": file_name,
            "file_number": file_number,
            "global": file_data.get("FILE_DEFINITION_GLOBAL", ""),
            "stored_name": file_data.get("FILE_DEFINITION_STORED_NAME", ""),
            "ehi_enabled": file_data.get("FILE_DEFINITION_EHI_ENABLED", ""),
            "internal_ehi_enabled": file_data.get("FILE_DEFINITION_INTERNAL_EHI_ENABLED", ""),
            "custom_file": file_data.get("FILE_DEFINITION_CUSTOM_FILE", ""),
            "file_version": file_data.get("FILE VERSION", ""),
            "lookup_type": file_data.get("FILE_DEFINITION_LOOKUP_TYPE", ""),
        }

        # Parse fields from the "0" entry
        fields = []
        entry_zero = file_data.get("0", {})
        if isinstance(entry_zero, dict):
            for fk, fv in sorted(entry_zero.items()):
                if fk.startswith("FIELD_") and isinstance(fv, dict):
                    fields.append(parse_field(fk, fv, file_name))

        entity["fields"] = fields
        entity["top_level_field_count"] = len(fields)

        # Flatten to count all fields including subfields
        flat = flatten_fields(fields)
        entity["total_field_count"] = len(flat)

        total_top_level_fields += len(fields)
        total_all_fields += len(flat)

        for f in flat:
            ft = f.get("field_type", "UNKNOWN")
            type_counter[ft] += 1

        category = categorize_file(file_name)
        entity["category"] = category
        category_counts[category]["files"] += 1
        category_counts[category]["top_level_fields"] += len(fields)
        category_counts[category]["all_fields"] += len(flat)
        category_counts[category]["file_list"].append(file_name)

        entities.append(entity)

    # Count fields with descriptions (field names serve as descriptions in FileMan)
    # Count fields with value sets
    fields_with_value_sets = sum(1 for e in entities for f in flatten_fields(e["fields"]) if f.get("value_list"))
    fields_with_pointer = sum(1 for e in entities for f in flatten_fields(e["fields"])
                              if f.get("pointer_file") or f.get("pointer_file_name"))
    fields_with_dd_info = sum(1 for e in entities for f in flatten_fields(e["fields"]) if f.get("dd_info"))

    # Pointer files count
    if isinstance(pointer_files, dict):
        pointer_count = len(pointer_files)
    elif isinstance(pointer_files, list):
        pointer_count = len(pointer_files)
    else:
        pointer_count = 0

    # Summary stats
    summary = {
        "schema_version": "BREH_OIT_20250714",
        "total_patient_files": len(entities),
        "total_top_level_fields": total_top_level_fields,
        "total_fields_including_subfields": total_all_fields,
        "pointer_reference_files": pointer_count,
        "field_type_distribution": dict(type_counter.most_common()),
        "fields_with_value_sets": fields_with_value_sets,
        "fields_with_pointer_references": fields_with_pointer,
        "fields_with_dd_info": fields_with_dd_info,
        "categories": {cat: {"files": v["files"], "top_level_fields": v["top_level_fields"],
                             "all_fields": v["all_fields"]}
                       for cat, v in sorted(category_counts.items())},
        "largest_files_by_field_count": sorted(
            [{"name": e["file_name"], "number": e["file_number"],
              "top_level_fields": e["top_level_field_count"],
              "total_fields": e["total_field_count"],
              "category": e["category"]}
             for e in entities],
            key=lambda x: x["total_fields"], reverse=True
        )[:20],
        "ehi_enabled_files": sum(1 for e in entities
                                 if e.get("internal_ehi_enabled") in ["Y", "YES", True, "1"]),
    }

    # Save outputs
    inventory_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(inventory_path, "w") as f:
        json.dump(entities, f, indent=2, default=str)
    print(f"Wrote {inventory_path} ({len(entities)} entities)")

    summary_path = os.path.join(OUTPUT_DIR, "summary-stats.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"Wrote {summary_path}")

    cat_path = os.path.join(OUTPUT_DIR, "category-breakdown.json")
    cat_data = {cat: {"files": v["files"], "top_level_fields": v["top_level_fields"],
                      "all_fields": v["all_fields"], "file_list": sorted(v["file_list"])}
                for cat, v in sorted(category_counts.items())}
    with open(cat_path, "w") as f:
        json.dump(cat_data, f, indent=2)
    print(f"Wrote {cat_path}")

    # Print summary
    print(f"\n=== Summary ===")
    print(f"Patient files: {len(entities)}")
    print(f"Top-level fields: {total_top_level_fields}")
    print(f"Total fields (incl subfields): {total_all_fields}")
    print(f"Pointer reference files: {pointer_count}")
    print(f"Fields with value sets: {fields_with_value_sets}")
    print(f"Fields with pointer refs: {fields_with_pointer}")
    print(f"\nField type distribution:")
    for ft, count in type_counter.most_common():
        print(f"  {ft}: {count}")
    print(f"\nCategory breakdown:")
    for cat, v in sorted(category_counts.items()):
        print(f"  {cat}: {v['files']} files, {v['top_level_fields']} top-level fields, {v['all_fields']} total fields")
    print(f"\nTop 10 largest files:")
    for item in summary["largest_files_by_field_count"][:10]:
        print(f"  {item['name']} ({item['number']}): {item['total_fields']} fields [{item['category']}]")

if __name__ == "__main__":
    main()
