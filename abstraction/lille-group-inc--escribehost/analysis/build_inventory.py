#!/usr/bin/env python3
"""
Build full-entity-inventory.json and summary-stats.json from the enrichment JSON.
Uses the already-parsed ehi-tables.json as the source of truth, after independent
verification that it correctly contains 80 tables and 1,246 columns matching the HTML.
"""

import json
import re
from pathlib import Path

ENRICHMENT_PATH = Path(__file__).parent / "../../../results/lille-group-inc--escribehost/downloads/enrichment/ehi-tables.json"
OUT_DIR = Path(__file__).parent


def categorize_table(name):
    """Assign a domain category based on table name."""
    n = name.upper()
    
    if n in ("PATIENTS", "PATIENT_ADDRESSES", "PATIENT_PREVIOUS_NAMES", 
             "PATIENT_RACE", "PATIENT_ETHNICITY", "ETHNICITIES", "PC_PATIENT_CONTACTS"):
        return "Demographics"
    if any(k in n for k in ["MED_RXS", "MED_THERAPIES", "MED_CONCERNS", "MEDS"]):
        return "Medications & Allergies"
    if any(k in n for k in ["RXHUB", "DRUG_HISTORY"]):
        return "Drug History (PDMP)"
    if "RECONCILIATION" in n:
        return "Medications & Allergies"
    if any(k in n for k in ["LAB_", "LABORATORY"]):
        return "Lab Results"
    if "VITAL" in n:
        return "Vitals"
    if n == "PE_PATIENT_ENCOUNTER":
        return "Encounters"
    if "ORDER" in n:
        return "Orders"
    if "INSURANCE" in n or "ELIGIBILITY" in n:
        return "Insurance & Eligibility"
    if "SURVEY" in n:
        return "Surveys & Assessments"
    if "PHR_" in n:
        return "Patient Portal"
    if any(k in n for k in ["DOCUMENT_SNAPSHOT", "CCDS_IMPORTED", "SCANNED_CARD"]):
        return "Documents"
    if "INTERVENTION" in n:
        return "Interventions"
    if "PROBLEM" in n:
        return "Problems / Diagnoses"
    if "RS_" in n:
        return "Research Studies"
    if "MISC_DEVICE" in n:
        return "Devices"
    if "EDUCATION" in n:
        return "Patient Education"
    if "RELATIVE" in n:
        return "Family History"
    if "TOC_" in n or "TRANSITION" in n:
        return "Transitions of Care"
    if "IMMUNIZATION" in n:
        return "Immunizations"
    if "PROCEDURE" in n:
        return "Procedures"
    if "SOCIAL_HISTORY" in n:
        return "Social History"
    if "HEALTH_CARE_TEAM" in n:
        return "Care Team"
    if "PROGRAM" in n:
        return "Programs"
    if "AMENDMENT" in n:
        return "Amendments"
    if "DIAGNOSTIC_IMAGING" in n:
        return "Imaging"
    if "TRANSFER" in n:
        return "Transfers"
    if n == "PATIENT_PHARMACIES":
        return "Reference / Lookup"
    if any(k in n for k in ["PROVIDER", "USER", "LOCATION", "OTHER_CONTACT"]):
        return "Reference / Lookup"
    return "Other"


def extract_value_set(constraints_list):
    """Extract CHECK constraint value sets."""
    for c in constraints_list:
        match = re.search(r"IN\s*\(([^)]+)\)", c)
        if match:
            values = [v.strip().strip("'\"") for v in match.group(1).split(",")]
            return values
    return None


def main():
    with open(ENRICHMENT_PATH) as f:
        tables = json.load(f)
    
    inventory = []
    total_fields = 0
    fields_with_desc = 0
    fields_without_desc = 0
    fields_with_value_sets = 0
    
    for table in tables:
        category = categorize_table(table["name"])
        enriched_cols = []
        table_desc_count = 0
        table_no_desc_count = 0
        table_vs_count = 0
        
        for col in table["columns"]:
            has_desc = bool(col.get("description", "").strip())
            value_set = extract_value_set(col.get("constraints", []))
            
            if has_desc:
                fields_with_desc += 1
                table_desc_count += 1
            else:
                fields_without_desc += 1
                table_no_desc_count += 1
            
            if value_set:
                fields_with_value_sets += 1
                table_vs_count += 1
            
            total_fields += 1
            
            enriched_cols.append({
                "ordinal": col["ordinal"],
                "name": col["name"],
                "dataType": col["dataType"],
                "isPrimaryKey": col["isPrimaryKey"],
                "nullable": col["nullable"],
                "description": col.get("description", ""),
                "constraints": col.get("constraints", []),
                "hasDescription": has_desc,
                "valueSet": value_set
            })
        
        pks = [c["name"] for c in enriched_cols if c["isPrimaryKey"]]
        fk_hints = [c["name"] for c in enriched_cols 
                     if c["name"].endswith("_ID") and not c["isPrimaryKey"]]
        
        inventory.append({
            "name": table["name"],
            "description": table.get("description", ""),
            "category": category,
            "columnCount": len(enriched_cols),
            "columnsWithDescription": table_desc_count,
            "columnsWithoutDescription": table_no_desc_count,
            "columnsWithValueSets": table_vs_count,
            "primaryKeys": pks,
            "foreignKeyHints": fk_hints,
            "columns": enriched_cols
        })
    
    # Save full inventory
    with open(OUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved full-entity-inventory.json ({len(inventory)} tables, {total_fields} fields)")
    
    # Category breakdown
    categories = {}
    for entity in inventory:
        cat = entity["category"]
        if cat not in categories:
            categories[cat] = {"tables": 0, "fields": 0, "fieldsWithDesc": 0, 
                              "fieldsWithValueSets": 0, "tableNames": []}
        categories[cat]["tables"] += 1
        categories[cat]["fields"] += entity["columnCount"]
        categories[cat]["fieldsWithDesc"] += entity["columnsWithDescription"]
        categories[cat]["fieldsWithValueSets"] += entity["columnsWithValueSets"]
        categories[cat]["tableNames"].append(entity["name"])
    
    sorted_cats = sorted(categories.items(), key=lambda x: x[1]["fields"], reverse=True)
    
    # Tables with missing descriptions
    tables_missing_desc = [
        {"name": e["name"], "missing": e["columnsWithoutDescription"], 
         "total": e["columnCount"], "category": e["category"]}
        for e in inventory if e["columnsWithoutDescription"] > 0
    ]
    tables_missing_desc.sort(key=lambda x: x["missing"], reverse=True)
    
    # Tables with value sets
    tables_with_vs = [
        {"name": e["name"], "valueSets": e["columnsWithValueSets"], "category": e["category"]}
        for e in inventory if e["columnsWithValueSets"] > 0
    ]
    
    summary = {
        "totalTables": len(inventory),
        "totalFields": total_fields,
        "fieldsWithDescription": fields_with_desc,
        "fieldsWithoutDescription": fields_without_desc,
        "descriptionCoveragePercent": round(fields_with_desc / total_fields * 100, 1),
        "fieldsWithValueSets": fields_with_value_sets,
        "categoryBreakdown": [
            {"category": cat, **{k: v for k, v in stats.items()}} 
            for cat, stats in sorted_cats
        ],
        "largestTables": sorted(
            [{"name": e["name"], "columns": e["columnCount"], "category": e["category"],
              "withDesc": e["columnsWithDescription"]} for e in inventory],
            key=lambda x: x["columns"], reverse=True
        )[:20],
        "tablesWithMissingDescriptions": tables_missing_desc,
        "tablesWithValueSets": tables_with_vs
    }
    
    with open(OUT_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print report
    print(f"\n=== SUMMARY ===")
    print(f"Total tables: {summary['totalTables']}")
    print(f"Total fields: {summary['totalFields']}")
    print(f"Fields with description: {summary['fieldsWithDescription']} ({summary['descriptionCoveragePercent']}%)")
    print(f"Fields without description: {summary['fieldsWithoutDescription']}")
    print(f"Fields with CHECK value sets: {summary['fieldsWithValueSets']}")
    print(f"\n=== CATEGORY BREAKDOWN ===")
    for item in summary["categoryBreakdown"]:
        print(f"  {item['category']}: {item['tables']} tables, {item['fields']} fields, "
              f"{item['fieldsWithDesc']} described")
    print(f"\n=== LARGEST TABLES ===")
    for t in summary["largestTables"]:
        print(f"  {t['name']}: {t['columns']} cols ({t['withDesc']} described) [{t['category']}]")
    print(f"\n=== TABLES WITH MISSING DESCRIPTIONS ===")
    for t in tables_missing_desc:
        print(f"  {t['name']}: {t['missing']}/{t['total']} missing [{t['category']}]")
    print(f"\n=== TABLES WITH VALUE SETS ===")
    for t in tables_with_vs:
        print(f"  {t['name']}: {t['valueSets']} constrained fields [{t['category']}]")

if __name__ == "__main__":
    main()
