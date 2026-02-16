#!/usr/bin/env python3
"""Parse eClinicalWorks EHI Export HTML data dictionary into structured JSON.

Reads all HTML table pages from downloads/tables/ and the index from
downloads/tableindex.html, producing:
  - entity-inventory-full.json: complete field-level inventory
  - entity-inventory-summary.json: aggregate statistics
"""

import json, os, re, sys
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).resolve().parent.parent / "downloads"
TABLES_DIR = DOWNLOADS / "tables"
INDEX_FILE = DOWNLOADS / "tableindex.html"
OUT_DIR = Path(__file__).resolve().parent


class TablePageParser(HTMLParser):
    """Parse a single table detail HTML page."""

    def __init__(self):
        super().__init__()
        self.table_name = ""
        self.table_description = ""
        self.columns = []
        # State tracking
        self._in_td = False
        self._td_class = ""
        self._td_text = ""
        self._current_row = []
        self._in_header_table = True  # first table is header, second is columns
        self._header_rows = []
        self._column_rows = []
        self._table_count = 0
        self._in_strong = False
        self._strong_text = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "table":
            self._table_count += 1
        elif tag == "tr":
            self._current_row = []
        elif tag == "td":
            self._in_td = True
            self._td_class = attrs_dict.get("class", "")
            self._td_text = ""
        elif tag == "strong":
            self._in_strong = True
            self._strong_text = ""

    def handle_endtag(self, tag):
        if tag == "td":
            self._in_td = False
            self._current_row.append(self._td_text.strip())
        elif tag == "tr":
            if self._table_count <= 1:
                self._header_rows.append(self._current_row)
            else:
                self._column_rows.append(self._current_row)
            self._current_row = []
        elif tag == "strong":
            self._in_strong = False

    def handle_data(self, data):
        if self._in_td:
            self._td_text += data

    def get_result(self):
        # Extract table name and description from header rows
        for row in self._header_rows:
            if len(row) >= 2:
                label = row[0].strip().lower()
                if label in ("table", "table name"):
                    self.table_name = row[1].strip()
                elif label == "description":
                    self.table_description = row[1].strip()

        # Extract columns from column rows (skip header row)
        for row in self._column_rows:
            if len(row) >= 3:
                col_name = row[0].strip()
                col_type = row[1].strip()
                col_desc = row[2].strip()
                # Skip header row
                if col_name.lower() in ("column", "column name") and col_type.lower() in ("datatype", "data type"):
                    continue
                # Clean up column name - remove "(Primary Key)" annotations
                is_pk = False
                if "(Primary Key)" in col_name:
                    is_pk = True
                    col_name = col_name.replace("(Primary Key)", "").strip()

                # Detect foreign key references in description
                fk_ref = None
                # Pattern: "refers to the X column in the Y table"
                fk_match = re.search(
                    r'refers?\s+to\s+the\s+(\w+)\s+column\s+in\s+the\s+(\w+)\s+table',
                    col_desc, re.IGNORECASE
                )
                if fk_match:
                    fk_ref = {"table": fk_match.group(2), "column": fk_match.group(1)}
                if not fk_ref:
                    # Pattern: "FK reference with the X table, Y column"
                    fk_match = re.search(
                        r'FK\s+reference\s+with\s+(?:the\s*)?(\w+)\s+table,?\s+(\w+)\s+column',
                        col_desc, re.IGNORECASE
                    )
                    if fk_match:
                        fk_ref = {"table": fk_match.group(1), "column": fk_match.group(2)}
                if not fk_ref:
                    # Pattern: "FK reference with theX table, Y column" (some pages have no space)
                    fk_match = re.search(
                        r'FK\s+reference\s+with\s+the(\w+)table,?\s+(\w+)\s+column',
                        col_desc, re.IGNORECASE
                    )
                    if fk_match:
                        fk_ref = {"table": fk_match.group(1), "column": fk_match.group(2)}

                col_obj = {
                    "name": col_name,
                    "type": col_type,
                    "description": col_desc,
                }
                if is_pk:
                    col_obj["primary_key"] = True
                if fk_ref:
                    col_obj["foreign_key"] = fk_ref

                self.columns.append(col_obj)

        return {
            "table_name": self.table_name,
            "table_description": self.table_description,
            "columns": self.columns,
            "column_count": len(self.columns),
        }


def parse_table_file(filepath):
    """Parse a single table HTML file."""
    try:
        html = filepath.read_text(encoding="utf-8", errors="replace")
        parser = TablePageParser()
        parser.feed(html)
        result = parser.get_result()
        result["source_file"] = filepath.name
        # If table_name is empty, derive from filename
        if not result["table_name"]:
            result["table_name"] = filepath.stem
        return result
    except Exception as e:
        return {
            "table_name": filepath.stem,
            "table_description": "",
            "columns": [],
            "column_count": 0,
            "source_file": filepath.name,
            "parse_error": str(e),
        }


def parse_index(filepath):
    """Parse the index page to get list of table names and links."""
    html = filepath.read_text(encoding="utf-8", errors="replace")
    # Extract table links from the index
    links = re.findall(r'href="tables/([^"]+)"', html, re.IGNORECASE)
    return [l.replace(".html", "") for l in links]


def categorize_table(name, desc):
    """Heuristic categorization based on table name and description."""
    name_lower = name.lower()
    desc_lower = desc.lower() if desc else ""
    combined = name_lower + " " + desc_lower

    # Order matters - more specific first
    if any(k in name_lower for k in ["dental", "perio", "tooth"]):
        return "Dental"
    if any(k in name_lower for k in ["ip_rh_", "inpatient", "discharge_summary", "ip_homemedic"]):
        return "Inpatient / Hospital"
    if any(k in name_lower for k in ["vision_", "eyechart", "ophth", "slitlamp", "tonometry", "refraction", "visual_acuity", "iop_"]):
        return "Vision / Ophthalmology"
    if any(k in name_lower for k in ["bh_", "behavioral"]):
        return "Behavioral Health"
    if any(k in name_lower for k in ["ob_", "obgyn", "prenatal", "pregnancy", "labor_delivery", "newborn", "obf_"]):
        return "OB/GYN"
    if any(k in name_lower for k in ["cardio", "ecg", "ekg", "holter"]):
        return "Cardiology"
    if any(k in name_lower for k in ["derm"]):
        return "Dermatology"
    if any(k in name_lower for k in ["vascular"]):
        return "Vascular"
    if any(k in name_lower for k in ["occhealth"]):
        return "Occupational Health"
    if any(k in name_lower for k in ["athletics"]):
        return "Sports Medicine"
    if any(k in name_lower for k in ["correctional"]):
        return "Correctional Health"
    if any(k in name_lower for k in ["asc_"]):
        return "Ambulatory Surgery Center"
    if any(k in name_lower for k in ["billing", "claim", "payment", "charge", "invoice", "era_", "remittance",
                                       "superbill", "copay", "deductible", "adjustmentposting",
                                       "patientbalance", "patientstatement", "collectionagency",
                                       "hcfa", "ub92", "mcaid_", "massform", "nycomp", "edi_"]):
        return "Billing / Revenue Cycle"
    if any(k in name_lower for k in ["insurance", "eligib", "x12", "x271", "x270", "payer", "coverage"]):
        return "Insurance / Coverage"
    if any(k in name_lower for k in ["rx_", "prescription", "erx_", "eprescri", "medication", "medic",
                                       "druginteraction", "formulary", "dispens", "surescript"]):
        return "Medications / Prescriptions"
    if any(k in name_lower for k in ["allergy", "allergies", "allergen"]):
        return "Allergies"
    if any(k in name_lower for k in ["immuniz", "vaccine", "vfc_", "cvx_", "antigen"]):
        return "Immunizations"
    if any(k in name_lower for k in ["vital", "bmi_", "bloodpressure", "pulse", "temperature_"]):
        return "Vitals"
    if any(k in name_lower for k in ["lab_", "laborder", "labresult", "labpanel", "specimen", "loinc"]):
        return "Lab Results"
    if any(k in name_lower for k in ["imaging", "radiology", "dicom", "pacs"]):
        return "Imaging / Radiology"
    if any(k in name_lower for k in ["procedure", "cpt_", "surgic"]):
        return "Procedures"
    if any(k in name_lower for k in ["enc_", "encounter", "visit_"]):
        return "Encounters"
    if name_lower.startswith("enc") and not any(k in name_lower for k in ["encrypt", "encod"]):
        return "Encounters"
    if any(k in name_lower for k in ["diagnosis", "problem", "icd", "dx_"]):
        return "Problems / Diagnoses"
    if any(k in name_lower for k in ["referral", "consult_ref"]):
        return "Referrals / Orders"
    if any(k in name_lower for k in ["order_", "orderentry", "cpoe", "ptorder"]):
        return "Referrals / Orders"
    if any(k in name_lower for k in ["note", "progress", "document", "letter_", "addendum", "eicr"]):
        return "Clinical Notes / Documents"
    if any(k in name_lower for k in ["template", "formpanel", "questionnaire", "customform"]):
        return "Templates / Forms"
    if any(k in name_lower for k in ["careplan", "care_plan", "goal_"]):
        return "Care Plans / Goals"
    if any(k in name_lower for k in ["message", "inbox", "messenger", "telephone", "communication"]):
        return "Messages / Communication"
    if any(k in name_lower for k in ["patient", "demographics", "user_", "guardian", "birth"]):
        return "Patient Demographics"
    if any(k in name_lower for k in ["appointment", "schedule", "appt", "waitlist"]):
        return "Scheduling"
    if any(k in name_lower for k in ["flowsheet", "flowchart"]):
        return "Flowsheets"
    if any(k in name_lower for k in ["consent", "directive", "advance_"]):
        return "Consents / Directives"
    if any(k in name_lower for k in ["aco", "hedis", "quality", "measure_", "phm_"]):
        return "Quality / Value-Based Care"
    if any(k in name_lower for k in ["ccm_", "ccmr", "chronic_care"]):
        return "Chronic Care Management"
    if any(k in name_lower for k in ["telehealth", "televisit"]):
        return "Telehealth"
    if any(k in name_lower for k in ["portal", "healow"]):
        return "Patient Portal"
    if any(k in name_lower for k in ["fax", "scan", "attachment", "upload"]):
        return "Documents / Attachments"
    if any(k in name_lower for k in ["prisma"]):
        return "Interoperability (PRISMA)"
    if any(k in name_lower for k in ["fhir", "bulk_"]):
        return "FHIR / Interoperability"
    if any(k in name_lower for k in ["rpm_"]):
        return "Remote Patient Monitoring"
    if any(k in name_lower for k in ["inventory_"]):
        return "Inventory Management"
    if any(k in name_lower for k in ["todo_", "todolist"]):
        return "Tasks / To-Do"
    if any(k in name_lower for k in ["employment"]):
        return "Occupational Health"
    if any(k in name_lower for k in ["case_", "casemanag"]):
        return "Case Management"
    if any(k in name_lower for k in ["lsm_"]):
        return "Lifestyle Medicine"
    if any(k in name_lower for k in ["emcoder"]):
        return "Billing / Revenue Cycle"
    if any(k in name_lower for k in ["growth", "growthchart"]):
        return "Growth Charts"
    if any(k in name_lower for k in ["warfarin", "anticoag"]):
        return "Anticoagulation Management"

    # Description-based fallback
    if "billing" in desc_lower or "claim" in desc_lower or "charge" in desc_lower:
        return "Billing / Revenue Cycle"
    if "insurance" in desc_lower or "eligib" in desc_lower:
        return "Insurance / Coverage"
    if "prescription" in desc_lower or "medication" in desc_lower:
        return "Medications / Prescriptions"
    if "allergy" in desc_lower or "allergen" in desc_lower:
        return "Allergies"
    if "encounter" in desc_lower or "visit" in desc_lower:
        return "Encounters"
    if "patient" in desc_lower and ("demograph" in desc_lower or "registr" in desc_lower):
        return "Patient Demographics"
    if "lab" in desc_lower and ("result" in desc_lower or "order" in desc_lower):
        return "Lab Results"
    if "immuniz" in desc_lower or "vaccine" in desc_lower:
        return "Immunizations"
    if "vital" in desc_lower:
        return "Vitals"
    if "note" in desc_lower or "progress" in desc_lower:
        return "Clinical Notes / Documents"
    if "referral" in desc_lower:
        return "Referrals / Orders"
    if "care plan" in desc_lower or "goal" in desc_lower:
        return "Care Plans / Goals"
    if "message" in desc_lower:
        return "Messages / Communication"

    return "Other"


def main():
    # Parse all table files
    table_files = sorted(TABLES_DIR.glob("*.html"))
    print(f"Found {len(table_files)} table HTML files")

    entities = []
    parse_errors = 0

    for f in table_files:
        result = parse_table_file(f)
        if "parse_error" in result:
            parse_errors += 1
        # Categorize
        result["category"] = categorize_table(result["table_name"], result["table_description"])
        # Track description quality
        described_cols = sum(
            1 for c in result["columns"]
            if c["description"]
            and c["description"].lower() not in ("", "n/a", "this column is not being used.")
        )
        result["columns_with_descriptions"] = described_cols
        result["columns_with_fk"] = sum(1 for c in result["columns"] if "foreign_key" in c)
        entities.append(result)

    # Write full inventory
    full_path = OUT_DIR / "entity-inventory-full.json"
    with open(full_path, "w") as f:
        json.dump(entities, f, indent=2)
    print(f"Wrote {full_path} ({len(entities)} entities)")

    # Compute summary statistics
    total_fields = sum(e["column_count"] for e in entities)
    total_described = sum(e["columns_with_descriptions"] for e in entities)
    total_fk = sum(e["columns_with_fk"] for e in entities)
    tables_with_desc = sum(1 for e in entities if e["table_description"])
    entities_with_errors = sum(1 for e in entities if "parse_error" in e)
    empty_tables = sum(1 for e in entities if e["column_count"] == 0)

    # Category breakdown
    categories = {}
    for e in entities:
        cat = e["category"]
        if cat not in categories:
            categories[cat] = {"table_count": 0, "field_count": 0, "described_fields": 0, "tables": []}
        categories[cat]["table_count"] += 1
        categories[cat]["field_count"] += e["column_count"]
        categories[cat]["described_fields"] += e["columns_with_descriptions"]
        categories[cat]["tables"].append(e["table_name"])

    # Sort categories by table count
    sorted_cats = dict(sorted(categories.items(), key=lambda x: x[1]["table_count"], reverse=True))

    # Top 20 largest tables
    top_tables = sorted(entities, key=lambda e: e["column_count"], reverse=True)[:20]

    summary = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_fields_with_descriptions": total_described,
        "description_percentage": round(total_described / total_fields * 100, 1) if total_fields else 0,
        "total_foreign_keys": total_fk,
        "tables_with_table_description": tables_with_desc,
        "tables_with_parse_errors": entities_with_errors,
        "tables_with_zero_columns": empty_tables,
        "category_breakdown": {
            cat: {
                "table_count": info["table_count"],
                "field_count": info["field_count"],
                "described_fields": info["described_fields"],
            }
            for cat, info in sorted_cats.items()
        },
        "top_20_largest_tables": [
            {
                "table_name": t["table_name"],
                "column_count": t["column_count"],
                "category": t["category"],
                "description": t["table_description"][:120] if t["table_description"] else "",
            }
            for t in top_tables
        ],
    }

    summary_path = OUT_DIR / "entity-inventory-summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {summary_path}")

    # Print key stats
    print(f"\n=== SUMMARY ===")
    print(f"Total tables: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({summary['description_percentage']}%)")
    print(f"Foreign key references: {total_fk}")
    print(f"Tables with table-level descriptions: {tables_with_desc}")
    print(f"Parse errors: {entities_with_errors}")
    print(f"Tables with 0 columns: {empty_tables}")
    print(f"\n=== CATEGORIES ===")
    for cat, info in sorted_cats.items():
        print(f"  {cat}: {info['table_count']} tables, {info['field_count']} fields")
    print(f"\n=== TOP 20 LARGEST TABLES ===")
    for t in top_tables:
        print(f"  {t['table_name']}: {t['column_count']} columns ({t['category']})")


if __name__ == "__main__":
    main()
