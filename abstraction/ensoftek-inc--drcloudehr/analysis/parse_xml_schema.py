#!/usr/bin/env python3
"""
Parse the SchemaSpy XML directly (drcloudehr.FHIR.xml) and produce a complete
entity inventory with all available metadata.

Outputs:
- full-entity-inventory.json — every table, every column, with all attributes
- summary-stats.json — aggregate statistics and category breakdowns
"""

import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

XML_PATH = Path(__file__).parent.parent.parent.parent / "results/ensoftek-inc--drcloudehr/downloads/drcloudehr.FHIR.xml"
OUTPUT_DIR = Path(__file__).parent


def infer_category(table_name: str, remarks: str) -> str:
    """Infer a data domain category from table name and remarks."""
    name = table_name.lower()
    rem = (remarks or "").lower()

    if name.startswith("form_eye_"):
        return "Eye Care / Ophthalmology"
    if name.startswith("form_"):
        if any(x in name for x in ["phq9", "gad7", "sdoh"]):
            return "Behavioral Health Assessments"
        if any(x in name for x in ["care_plan", "treatment_plan"]):
            return "Care Plans / Treatment Plans"
        if name == "form_ros":
            return "Clinical Forms — Review of Systems"
        if name == "form_dictation":
            return "Clinical Forms — Dictation"
        if any(x in name for x in ["soap", "vitals", "vital_details"]):
            return "Clinical Forms — Vitals/SOAP"
        if "billing" in name:
            return "Billing / Revenue Cycle"
        if "transfer" in name:
            return "Referrals / Transfers"
        if name == "form_encounter":
            return "Encounters"
        if name == "form_questionnaire_assessments":
            return "Patient-Reported Outcomes"
        return "Clinical Forms"
    if any(x in name for x in ["billing", "claims", "ar_activity", "ar_session", "voids"]):
        return "Billing / Revenue Cycle"
    if any(x in name for x in ["insurance", "eligibility", "benefit"]):
        return "Insurance / Coverage"
    if any(x in name for x in ["prescriptions", "drugs", "drug_sales", "lists_medication", "medex"]):
        return "Medications / Prescriptions"
    if name.startswith("procedure_"):
        return "Lab / Procedure Orders & Results"
    if "document" in name:
        return "Documents / Attachments"
    if name.startswith("onsite_") or name.startswith("patient_access"):
        return "Patient Portal / Messaging"
    if "immuniz" in name:
        return "Immunizations"
    if "therapy_group" in name:
        return "Therapy Groups"
    if any(x in name for x in ["patient_data", "patient_history", "history_data"]):
        return "Demographics / Patient Data"
    if "amendment" in name:
        return "Amendments"
    if name in ("openemr_postcalendar_events", "openemr_postcalendar_categories",
                "patient_tracker", "patient_tracker_element"):
        return "Scheduling / Appointments"
    if "esign" in name:
        return "E-Signatures"
    if "clinical_plan" in name:
        return "Care Plans / Treatment Plans"
    if name == "forms":
        return "Encounters"
    if any(x in name for x in ["questionnaire", "pro_assess"]):
        return "Patient-Reported Outcomes"
    if name in ("lists", "issue_types", "issue_encounter"):
        return "Problems / Allergies / Conditions"
    if any(x in name for x in ["list_options", "layout_", "shared_attributes", "lbf_data", "lbt_data"]):
        return "Reference / Configuration Data"
    if name == "users":
        return "Users / Providers"
    if name.startswith("external_"):
        return "External / Imported Data"
    if name == "facility":
        return "Facility"
    if name == "transactions":
        return "Referrals / Transfers"
    if name == "pnotes":
        return "Clinical Notes"
    if name == "notes":
        return "Clinical Notes"
    if name == "groups":
        return "Therapy Groups"
    if name == "pharmacies":
        return "Medications / Prescriptions"
    if name.startswith("rule_"):
        return "Clinical Decision Support"
    if name == "patient_reminders":
        return "Patient Communications"
    if "log" in name:
        return "Logging / Audit"
    return "Other"


def parse_xml():
    tree = ET.parse(str(XML_PATH))
    root = tree.getroot()

    db_info = {
        "database_name": root.get("name"),
        "schema_name": root.get("schema"),
        "database_type": root.get("type"),
    }

    inventory = []

    tables_container = root.find("tables")
    if tables_container is None:
        tables_container = root
    for table_elem in tables_container.findall("table"):
        t_name = table_elem.get("name")
        t_remarks = table_elem.get("remarks", "")
        t_numrows = table_elem.get("numRows")
        category = infer_category(t_name, t_remarks)

        # Parse columns (direct children only)
        columns = []
        for col_elem in table_elem:
            if col_elem.tag != "column":
                continue

            parents = []
            children_refs = []
            for sub in col_elem:
                if sub.tag == "parent":
                    parents.append({
                        "table": sub.get("table"),
                        "column": sub.get("column"),
                        "foreign_key": sub.get("foreignKey"),
                        "implied": sub.get("implied") == "true",
                    })
                elif sub.tag == "child":
                    children_refs.append({
                        "table": sub.get("table"),
                        "column": sub.get("column"),
                        "foreign_key": sub.get("foreignKey"),
                        "implied": sub.get("implied") == "true",
                    })

            col_remarks = col_elem.get("remarks", "")
            columns.append({
                "name": col_elem.get("name"),
                "type": col_elem.get("type"),
                "size": col_elem.get("size"),
                "nullable": col_elem.get("nullable") == "true",
                "auto_updated": col_elem.get("autoUpdated") == "true",
                "default_value": col_elem.get("defaultValue"),
                "description": col_remarks,
                "has_description": bool(col_remarks),
                "parent_references": parents,
                "child_references": children_refs,
            })

        # Parse primary keys
        primary_keys = []
        for pk in table_elem.findall("primaryKey"):
            primary_keys.append(pk.get("column"))

        # Parse indexes
        indexes = []
        for idx_elem in table_elem.findall("index"):
            idx_cols = [ic.get("name") for ic in idx_elem.findall("column")]
            indexes.append({
                "name": idx_elem.get("name"),
                "unique": idx_elem.get("unique") == "true",
                "columns": idx_cols,
            })

        inventory.append({
            "table_name": t_name,
            "description": t_remarks,
            "category": category,
            "num_rows_sample": int(t_numrows) if t_numrows else None,
            "column_count": len(columns),
            "columns_with_descriptions": sum(1 for c in columns if c["has_description"]),
            "primary_keys": primary_keys,
            "indexes": indexes,
            "columns": columns,
        })

    return db_info, inventory


def compute_summary(db_info, inventory):
    total_tables = len(inventory)
    total_columns = sum(t["column_count"] for t in inventory)
    cols_with_desc = sum(t["columns_with_descriptions"] for t in inventory)
    tables_with_desc = sum(1 for t in inventory if t["description"])

    total_parent_refs = sum(
        len(c["parent_references"])
        for t in inventory for c in t["columns"]
    )
    total_child_refs = sum(
        len(c["child_references"])
        for t in inventory for c in t["columns"]
    )

    # Category breakdown
    categories = defaultdict(lambda: {
        "tables": [], "table_count": 0,
        "column_count": 0, "columns_with_descriptions": 0
    })
    for t in inventory:
        cat = t["category"]
        categories[cat]["tables"].append(t["table_name"])
        categories[cat]["table_count"] += 1
        categories[cat]["column_count"] += t["column_count"]
        categories[cat]["columns_with_descriptions"] += t["columns_with_descriptions"]

    sorted_cats = dict(sorted(categories.items(), key=lambda x: -x[1]["table_count"]))

    summary = {
        "database_info": db_info,
        "total_tables": total_tables,
        "total_columns": total_columns,
        "columns_with_descriptions": cols_with_desc,
        "columns_without_descriptions": total_columns - cols_with_desc,
        "description_coverage_pct": round(cols_with_desc / total_columns * 100, 1),
        "tables_with_descriptions": tables_with_desc,
        "tables_without_descriptions": total_tables - tables_with_desc,
        "total_parent_references": total_parent_refs,
        "total_child_references": total_child_refs,
        "total_relationships": total_parent_refs + total_child_refs,
        "category_count": len(sorted_cats),
        "categories": {k: {
            "table_count": v["table_count"],
            "column_count": v["column_count"],
            "columns_with_descriptions": v["columns_with_descriptions"],
            "description_pct": round(v["columns_with_descriptions"] / v["column_count"] * 100, 1) if v["column_count"] > 0 else 0,
            "tables": v["tables"]
        } for k, v in sorted_cats.items()},
        "largest_tables": sorted(
            [{
                "table": t["table_name"],
                "columns": t["column_count"],
                "described": t["columns_with_descriptions"],
                "category": t["category"],
                "description": t["description"][:120] if t["description"] else "",
            } for t in inventory],
            key=lambda x: -x["columns"]
        )[:25],
        "tables_with_no_column_descriptions": sorted([
            {"table": t["table_name"], "columns": t["column_count"], "category": t["category"]}
            for t in inventory
            if t["columns_with_descriptions"] == 0
        ], key=lambda x: -x["columns"]),
        "tables_with_full_descriptions": sorted([
            {"table": t["table_name"], "columns": t["column_count"], "category": t["category"]}
            for t in inventory
            if t["columns_with_descriptions"] == t["column_count"] and t["column_count"] > 0
        ], key=lambda x: -x["columns"]),
    }

    return summary


def main():
    db_info, inventory = parse_xml()

    # Save full inventory
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved full-entity-inventory.json ({len(inventory)} tables)")

    # Compute and save summary
    summary = compute_summary(db_info, inventory)
    with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary-stats.json")

    # Print key stats
    print(f"\n=== Summary ===")
    print(f"Database: {db_info['database_type']}")
    print(f"Tables: {summary['total_tables']}")
    print(f"Columns: {summary['total_columns']}")
    print(f"Columns with descriptions: {summary['columns_with_descriptions']} ({summary['description_coverage_pct']}%)")
    print(f"Tables with descriptions: {summary['tables_with_descriptions']}/{summary['total_tables']}")
    print(f"Relationships: {summary['total_relationships']} ({summary['total_parent_references']} parent, {summary['total_child_references']} child)")
    print(f"\nCategories ({summary['category_count']}):")
    for cat, info in summary["categories"].items():
        print(f"  {cat}: {info['table_count']} tables, {info['column_count']} cols, {info['columns_with_descriptions']} described ({info['description_pct']}%)")

    print(f"\nTables with ALL columns described ({len(summary['tables_with_full_descriptions'])}):")
    for t in summary["tables_with_full_descriptions"]:
        print(f"  {t['table']}: {t['columns']} cols [{t['category']}]")

    print(f"\nTables with NO column descriptions ({len(summary['tables_with_no_column_descriptions'])}):")
    for t in summary["tables_with_no_column_descriptions"]:
        print(f"  {t['table']}: {t['columns']} cols [{t['category']}]")


if __name__ == "__main__":
    main()
