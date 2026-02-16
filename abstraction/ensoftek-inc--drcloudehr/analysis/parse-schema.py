"""
Parse the DrCloudEHR SchemaSpy XML export and produce:
  - entity-inventory-full.json: complete table/column inventory
  - entity-inventory-summary.json: aggregate stats
  - table-list.txt: quick reference
"""

import xml.etree.ElementTree as ET
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(SCRIPT_DIR, "..", "downloads", "drcloudehr.FHIR.xml")
FULL_OUT = os.path.join(SCRIPT_DIR, "entity-inventory-full.json")
SUMMARY_OUT = os.path.join(SCRIPT_DIR, "entity-inventory-summary.json")

tree = ET.parse(INPUT)
root = tree.getroot()

db_name = root.attrib.get("name", "")
db_type = root.attrib.get("type", "")
db_schema = root.attrib.get("schema", "")

tables_out = []

for table_el in root.findall(".//table"):
    t_name = table_el.attrib.get("name", "")
    t_remarks = table_el.attrib.get("remarks", "")
    t_rows = int(table_el.attrib.get("numRows", "0"))

    # Primary keys
    pk_cols = [pk.attrib["column"] for pk in table_el.findall("primaryKey")]

    # Columns (direct children only, not inside index)
    columns = []
    for col_el in table_el.findall("column"):
        parents = []
        for p in col_el.findall("parent"):
            parents.append({"table": p.attrib.get("table",""), "column": p.attrib.get("column","")})
        children = []
        for c in col_el.findall("child"):
            children.append({"table": c.attrib.get("table",""), "column": c.attrib.get("column","")})

        col = {
            "name": col_el.attrib.get("name", ""),
            "type": col_el.attrib.get("type", "Unknown"),
            "size": col_el.attrib.get("size", ""),
            "nullable": col_el.attrib.get("nullable") == "true",
            "auto_updated": col_el.attrib.get("autoUpdated") == "true",
            "default_value": None if col_el.attrib.get("defaultValue") == "null" else col_el.attrib.get("defaultValue"),
            "remarks": col_el.attrib.get("remarks", ""),
            "is_primary_key": col_el.attrib.get("name", "") in pk_cols,
            "foreign_keys": parents if parents else None,
            "children": children if children else None,
        }
        columns.append(col)

    # Indexes
    indexes = []
    for idx_el in table_el.findall("index"):
        idx_cols = [ic.attrib.get("name","") for ic in idx_el.findall("column")]
        indexes.append({
            "name": idx_el.attrib.get("name",""),
            "unique": idx_el.attrib.get("unique") == "true",
            "columns": idx_cols,
        })

    tables_out.append({
        "name": t_name,
        "remarks": t_remarks,
        "num_rows": t_rows,
        "column_count": len(columns),
        "columns": columns,
        "primary_key": pk_cols,
        "indexes": indexes,
    })

# Write full inventory
full_inventory = {
    "database_name": db_name,
    "database_type": db_type,
    "schema_name": db_schema,
    "total_tables": len(tables_out),
    "total_columns": sum(t["column_count"] for t in tables_out),
    "tables": tables_out,
}
with open(FULL_OUT, "w") as f:
    json.dump(full_inventory, f, indent=2)

# Compute summary stats
total_cols = full_inventory["total_columns"]
cols_with_remarks = sum(1 for t in tables_out for c in t["columns"] if c["remarks"])
tables_with_remarks = sum(1 for t in tables_out if t["remarks"])
cols_with_fk = sum(1 for t in tables_out for c in t["columns"] if c["foreign_keys"])
cols_with_type = sum(1 for t in tables_out for c in t["columns"] if c["type"] != "Unknown")

# Categorize tables by name patterns
categories = {}
for t in tables_out:
    name = t["name"]
    if name.startswith("form_"):
        cat = "Clinical Forms"
    elif name in ("patient_data",) or name.startswith("patient_"):
        cat = "Patient Data"
    elif name in ("billing", "claims", "ar_activity", "ar_session", "drug_sales", "eligibility_verification", "benefit_eligibility", "insurance_data", "insurance_numbers"):
        cat = "Billing & Insurance"
    elif name in ("prescriptions", "drugs", "immunizations"):
        cat = "Medications & Immunizations"
    elif name in ("lists", "lists_touch", "issue_encounter", "issue_types"):
        cat = "Problems/Issues"
    elif name in ("procedure_order", "procedure_result", "procedure_report", "procedure_type", "procedure_providers", "procedure_answers", "procedure_order_code"):
        cat = "Orders & Results"
    elif name in ("documents", "document_templates", "notes"):
        cat = "Documents & Notes"
    elif name in ("amendments", "amendments_history"):
        cat = "Amendments"
    elif name in ("facility", "facility_user_ids", "users", "users_facility", "user_settings", "globals"):
        cat = "Facility & Users"
    elif name in ("form_encounter", "external_encounters"):
        cat = "Encounters"
    elif name in ("openemr_postcalendar_events",):
        cat = "Scheduling"
    elif name in ("list_options", "layout_options", "layout_group_properties"):
        cat = "Configuration/Lists"
    elif name in ("ccda_components", "ccda_sections", "ccda_field_mapping", "ccda_table_mapping"):
        cat = "CCDA"
    elif name in ("transactions",):
        cat = "Transactions/Referrals"
    elif name in ("therapy_groups", "therapy_groups_counselors", "therapy_groups_participant_attendance", "therapy_groups_participants"):
        cat = "Therapy Groups"
    elif name in ("onsite_documents", "onsite_messages", "onsite_mail", "onsite_portal_activity", "onsite_signatures"):
        cat = "Patient Portal"
    elif name in ("extended_log",):
        cat = "Audit/Logging"
    else:
        cat = "Other"

    if cat not in categories:
        categories[cat] = {"table_count": 0, "column_count": 0, "tables": []}
    categories[cat]["table_count"] += 1
    categories[cat]["column_count"] += t["column_count"]
    categories[cat]["tables"].append(t["name"])

# Sort tables by column count desc for "largest tables"
largest = sorted(tables_out, key=lambda t: t["column_count"], reverse=True)[:20]

summary = {
    "total_tables": len(tables_out),
    "total_columns": total_cols,
    "tables_with_remarks": tables_with_remarks,
    "tables_without_remarks": len(tables_out) - tables_with_remarks,
    "columns_with_remarks": cols_with_remarks,
    "columns_without_remarks": total_cols - cols_with_remarks,
    "remark_coverage_pct": round(cols_with_remarks / total_cols * 100, 1) if total_cols else 0,
    "columns_with_type_info": cols_with_type,
    "columns_with_foreign_keys": cols_with_fk,
    "categories": categories,
    "largest_tables": [{"name": t["name"], "columns": t["column_count"], "remarks": t["remarks"][:100]} for t in largest],
    "all_table_names": sorted([t["name"] for t in tables_out]),
}

with open(SUMMARY_OUT, "w") as f:
    json.dump(summary, f, indent=2)

print(f"Tables: {len(tables_out)}")
print(f"Columns: {total_cols}")
print(f"Columns with remarks: {cols_with_remarks} ({summary['remark_coverage_pct']}%)")
print(f"Tables with remarks: {tables_with_remarks}")
print(f"Columns with FK: {cols_with_fk}")
print(f"Categories: {len(categories)}")
for cat, info in sorted(categories.items(), key=lambda x: -x[1]['column_count']):
    print(f"  {cat}: {info['table_count']} tables, {info['column_count']} columns")
