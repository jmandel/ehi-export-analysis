#!/usr/bin/env python3
"""
Merge SchemaSpy XML-parsed schema.json and HTML-extracted html-comments.json
to produce a complete full-entity-inventory.json with all 322 tables and 4941
columns, plus summary statistics.

Inputs:
  - results/openemr-foundation--openemr/downloads/enrichment/schema.json
  - results/openemr-foundation--openemr/downloads/enrichment/html-comments.json

Outputs:
  - full-entity-inventory.json  (complete entity/field inventory)
  - summary-stats.json          (aggregate statistics)
"""
import json, html as html_mod, re
from pathlib import Path
from collections import defaultdict

RESULTS = Path(__file__).resolve().parent.parent.parent.parent / "results" / "openemr-foundation--openemr" / "downloads" / "enrichment"
OUT = Path(__file__).resolve().parent

with open(RESULTS / "schema.json") as f:
    schema = json.load(f)

with open(RESULTS / "html-comments.json") as f:
    html_data = json.load(f)

# Build lookup from HTML comments by table name
html_by_table = {}
for entry in html_data:
    html_by_table[entry["name"]] = entry

# Domain categorization heuristics based on table name patterns
def categorize_table(name, remarks):
    name_lower = name.lower()
    remarks_lower = (remarks or "").lower()

    # Clinical forms
    if name_lower.startswith("form_") or name_lower == "forms":
        if "eye" in name_lower:
            return "Ophthalmology/Eye Care"
        return "Clinical Forms"

    # Billing / financial
    if any(x in name_lower for x in ["billing", "claims", "ar_activity", "ar_session",
            "fee_sheet", "payment", "x12_", "eligibility", "invoice"]):
        return "Billing & Financial"

    # Insurance
    if "insurance" in name_lower:
        return "Insurance"

    # Demographics / patient
    if any(x in name_lower for x in ["patient_data", "patient_access", "patient_history",
            "patient_portal", "history_data", "employer_data"]):
        return "Demographics & Patient"

    # Medications / prescriptions / drugs
    if any(x in name_lower for x in ["prescriptions", "drug", "immunization", "erx_"]):
        return "Medications & Prescriptions"

    # Labs / procedures
    if any(x in name_lower for x in ["procedure_", "lab_"]):
        return "Labs & Procedures"

    # Documents
    if any(x in name_lower for x in ["document", "onsite_document"]):
        return "Documents"

    # Scheduling / calendar
    if any(x in name_lower for x in ["calendar", "postcalendar", "openemr_postcalendar"]):
        return "Scheduling"

    # Messaging / notes
    if any(x in name_lower for x in ["pnotes", "notification", "secure_msg"]):
        return "Messaging & Notifications"

    # CCDA / interoperability
    if any(x in name_lower for x in ["ccda", "ccr_"]):
        return "Interoperability (CCDA)"

    # Users / access control / GACL
    if any(x in name_lower for x in ["users", "gacl_", "groups", "module_", "api_"]):
        return "Users & Access Control"

    # Lists / reference data
    if any(x in name_lower for x in ["list_options", "icd9", "icd10", "codes", "code_types",
            "lang_", "valueset", "fhir_value", "standardized_tables_track"]):
        return "Reference Data & Code Sets"

    # Amendments
    if "amendment" in name_lower:
        return "Amendments"

    # Care plans / care teams
    if any(x in name_lower for x in ["care_plan", "care_team"]):
        return "Care Plans & Teams"

    # Questionnaires
    if "questionnaire" in name_lower:
        return "Questionnaires"

    # Clinical / lists / issues
    if any(x in name_lower for x in ["lists", "issue_", "transactions"]):
        return "Clinical Lists & Issues"

    # Facility / pharmacy / providers
    if any(x in name_lower for x in ["facility", "pharmacies", "procedure_providers",
            "addresses", "address", "contact"]):
        return "Facility & Reference Entities"

    # Therapy groups
    if "therapy_group" in name_lower:
        return "Therapy Groups"

    # Misc clinical
    if any(x in name_lower for x in ["vitals", "allerg", "encounter"]):
        return "Clinical Forms"

    # Categories
    if name_lower.startswith("categories"):
        return "Documents"

    # Audit / logging (not EHI but included in export)
    if any(x in name_lower for x in ["audit_", "log", "api_log"]):
        return "Audit & Logging"

    # Background / system
    if any(x in name_lower for x in ["background_", "globals", "registry",
            "sequences", "session", "temp_", "keys",
            "esign_", "layout_", "extended_log", "product_registration",
            "miscellaneous", "misc_"]):
        return "System & Configuration"

    return "Other"


def decode_html(s):
    """Decode HTML entities and clean up."""
    if not s:
        return ""
    s = html_mod.unescape(s)
    s = s.strip()
    if s in ("NULL", "''", '""', ""):
        return ""
    return s


# Build merged inventory
inventory = []
for table in schema["tables"]:
    tname = table["name"]
    html_entry = html_by_table.get(tname, {})
    html_cols_by_name = {}
    for hc in html_entry.get("columns", []):
        html_cols_by_name[hc["name"]] = hc

    category = categorize_table(tname, table.get("remarks"))

    # Merge column data
    merged_columns = []
    for col in table["columns"]:
        cname = col["name"]
        html_col = html_cols_by_name.get(cname, {})
        html_comment = decode_html(html_col.get("comments", ""))
        xml_remark = col.get("remarks", "")

        # Pick the best description: prefer XML remark if non-empty, else HTML comment
        description = xml_remark if xml_remark else html_comment

        foreign_keys = []
        for parent in col.get("parents", []):
            foreign_keys.append({
                "references_table": parent.get("table", ""),
                "references_column": parent.get("column", ""),
                "foreign_key_name": parent.get("foreignKey", "")
            })
        for child in col.get("children", []):
            pass  # children are reverse references, not FKs from this column

        merged_columns.append({
            "name": cname,
            "type": col.get("type", ""),
            "size": col.get("size"),
            "nullable": col.get("nullable", True),
            "default_value": col.get("defaultValue", ""),
            "auto_updated": col.get("autoUpdated", False),
            "description": description,
            "xml_remark": xml_remark,
            "html_comment": html_comment,
            "foreign_keys": foreign_keys
        })

    inventory.append({
        "table_name": tname,
        "type": table.get("type", "TABLE"),
        "num_rows": table.get("numRows", 0),
        "table_remarks": table.get("remarks", ""),
        "category": category,
        "num_columns": len(merged_columns),
        "primary_key": table.get("primaryKey", []),
        "indexes": table.get("indexes", []),
        "columns": merged_columns
    })

# Save full inventory
with open(OUT / "full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Compute summary statistics
total_tables = len(inventory)
total_columns = sum(e["num_columns"] for e in inventory)
columns_with_any_desc = sum(
    1 for e in inventory for c in e["columns"] if c["description"]
)
columns_with_xml_remark = sum(
    1 for e in inventory for c in e["columns"] if c["xml_remark"]
)
columns_with_html_comment = sum(
    1 for e in inventory for c in e["columns"] if c["html_comment"]
)
tables_with_remarks = sum(1 for e in inventory if e["table_remarks"])
total_fks = sum(
    1 for e in inventory for c in e["columns"] for fk in c["foreign_keys"]
)

# Category breakdown
cat_stats = defaultdict(lambda: {"tables": 0, "columns": 0, "described_columns": 0})
for e in inventory:
    cat = e["category"]
    cat_stats[cat]["tables"] += 1
    cat_stats[cat]["columns"] += e["num_columns"]
    cat_stats[cat]["described_columns"] += sum(1 for c in e["columns"] if c["description"])

category_breakdown = []
for cat, stats in sorted(cat_stats.items(), key=lambda x: -x[1]["columns"]):
    category_breakdown.append({
        "category": cat,
        "tables": stats["tables"],
        "columns": stats["columns"],
        "described_columns": stats["described_columns"],
        "description_pct": round(100 * stats["described_columns"] / stats["columns"], 1) if stats["columns"] > 0 else 0
    })

# Top 20 largest tables by column count
top_tables = sorted(inventory, key=lambda x: -x["num_columns"])[:20]
top_table_summary = [{
    "table_name": t["table_name"],
    "category": t["category"],
    "num_columns": t["num_columns"],
    "table_remarks": t["table_remarks"],
    "described_columns": sum(1 for c in t["columns"] if c["description"]),
    "num_rows": t["num_rows"]
} for t in top_tables]

# Tables with 0 descriptions
thin_tables = [
    {"table_name": t["table_name"], "category": t["category"], "num_columns": t["num_columns"]}
    for t in inventory
    if t["num_columns"] > 0 and not any(c["description"] for c in t["columns"])
]

summary = {
    "total_tables": total_tables,
    "total_columns": total_columns,
    "tables_with_table_remarks": tables_with_remarks,
    "columns_with_any_description": columns_with_any_desc,
    "columns_with_xml_remark": columns_with_xml_remark,
    "columns_with_html_comment": columns_with_html_comment,
    "description_coverage_pct": round(100 * columns_with_any_desc / total_columns, 1),
    "total_foreign_keys": total_fks,
    "category_breakdown": category_breakdown,
    "top_20_tables_by_columns": top_table_summary,
    "tables_with_zero_described_columns": thin_tables,
    "tables_with_zero_columns": sum(1 for e in inventory if e["num_columns"] == 0)
}

with open(OUT / "summary-stats.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total tables: {total_tables}")
print(f"Total columns: {total_columns}")
print(f"Columns with any description: {columns_with_any_desc} ({summary['description_coverage_pct']}%)")
print(f"Tables with table remarks: {tables_with_remarks}")
print(f"Foreign keys: {total_fks}")
print(f"\nCategory breakdown:")
for cb in category_breakdown:
    print(f"  {cb['category']}: {cb['tables']} tables, {cb['columns']} cols, {cb['described_columns']} described ({cb['description_pct']}%)")
print(f"\nTables with zero described columns: {len(thin_tables)}")
print(f"Tables with zero columns: {summary['tables_with_zero_columns']}")
