#!/usr/bin/env python3
"""
Parse all Epic EHI Tables HTML files from the extracted ZIP.
Produces entity-inventory-full.json and entity-inventory-summary.json.

Reads raw .htm files from downloads/ehi-tables-extracted/DocGen_*/ directory.
Uses html.parser (stdlib) to avoid external dependency for parsing.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter, defaultdict

SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
EXTRACTED_DIR = None

# Find the extracted directory
for d in (BASE_DIR / "downloads" / "ehi-tables-extracted").iterdir():
    if d.is_dir() and d.name.startswith("DocGen"):
        EXTRACTED_DIR = d
        break

if not EXTRACTED_DIR:
    print("ERROR: Could not find extracted EHI tables directory")
    sys.exit(1)

OUTPUT_FULL = SCRIPT_DIR / "entity-inventory-full.json"
OUTPUT_SUMMARY = SCRIPT_DIR / "entity-inventory-summary.json"


class EHITableParser(HTMLParser):
    """Parse a single Epic EHI Table HTML file."""

    def __init__(self):
        super().__init__()
        self._stack = []  # tag stack
        self._text_buf = []
        self._in_cell = False
        self._current_tag = None

        # Collected data
        self.table_name = ""
        self.description = ""
        self.primary_key = []
        self.columns = []

        # State machine
        self._phase = "init"  # init -> header -> desc -> pk -> columns
        self._row_cells = []
        self._in_table = 0
        self._table_classes = []
        self._current_classes = []
        self._pk_section = False
        self._col_section = False
        self._in_header2 = False
        self._in_t1value = False
        self._current_col = None
        self._in_desc_row = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "").split()

        if tag == "table":
            self._in_table += 1
            self._table_classes.append(classes)

        if tag == "tr":
            self._row_cells = []

        if tag == "td" or tag == "th":
            self._in_cell = True
            self._text_buf = []
            self._current_classes = classes

        self._stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "td" or tag == "th":
            text = " ".join("".join(self._text_buf).split())
            self._row_cells.append((text, self._current_classes))
            self._in_cell = False

        if tag == "tr":
            self._process_row()

        if tag == "table" and self._in_table > 0:
            self._in_table -= 1
            if self._table_classes:
                self._table_classes.pop()

        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._in_cell:
            self._text_buf.append(data)

    def _get_current_table_classes(self):
        if self._table_classes:
            return self._table_classes[-1]
        return []

    def _process_row(self):
        cells = self._row_cells
        if not cells:
            return

        texts = [c[0] for c in cells]
        cell_classes = [c[1] for c in cells]

        # Detect table name from Header2 table
        tbl_classes = self._get_current_table_classes()

        if "Header2" in tbl_classes and texts:
            name = texts[0].strip()
            if name:
                self.table_name = name
            return

        # Detect description from KeyValue table
        if "KeyValue" in tbl_classes:
            for i, (text, cls) in enumerate(cells):
                if "T1Value" in cls and text.strip():
                    self.description = text.strip()
            return

        # Detect section headers
        if "SubHeader3" in tbl_classes:
            for text, _ in cells:
                t = text.strip()
                if t == "Primary Key":
                    self._pk_section = True
                    self._col_section = False
                elif t == "Columns":
                    self._col_section = True
                    self._pk_section = False
            return

        # Primary key rows (in List table, not SubList)
        if self._pk_section and "List" in tbl_classes and "SubList" not in tbl_classes:
            if len(texts) >= 2:
                name = texts[0].strip()
                try:
                    pos = int(texts[1].strip())
                    if name:
                        self.primary_key.append({"name": name, "ordinal_position": pos})
                except (ValueError, IndexError):
                    pass
            return

        # Column rows (in SubList List table)
        if "SubList" in tbl_classes and "List" in tbl_classes:
            self._col_section = True
            # Header row
            if any("T1Head" in cls for _, cls in cells):
                # Save previous column
                if self._current_col and self._current_col.get("name"):
                    self.columns.append(self._current_col)

                head_cells = [(t, c) for t, c in cells if "T1Head" in c]
                other_cells = [(t, c) for t, c in cells if "T1Head" not in c]

                ordinal = 0
                name = ""
                col_type = ""
                discontinued = False

                if len(head_cells) >= 1:
                    try:
                        ordinal = int(head_cells[0][0].strip())
                    except ValueError:
                        pass
                if len(head_cells) >= 2:
                    name = head_cells[1][0].strip()
                if len(head_cells) >= 3:
                    col_type = head_cells[2][0].strip()

                for t, c in other_cells:
                    t = t.strip()
                    if t == "Yes":
                        discontinued = True
                    elif t == "No":
                        discontinued = False

                self._current_col = {
                    "ordinal": ordinal,
                    "name": name,
                    "type": col_type,
                    "discontinued": discontinued,
                    "description": "",
                }
            else:
                # Description row
                if self._current_col:
                    desc_text = " ".join(t.strip() for t, _ in cells if t.strip())
                    if desc_text:
                        if self._current_col["description"]:
                            self._current_col["description"] += " " + desc_text
                        else:
                            self._current_col["description"] = desc_text

    def finalize(self):
        if self._current_col and self._current_col.get("name"):
            self.columns.append(self._current_col)


def parse_htm_file(filepath):
    """Parse a single .htm file and return structured data."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    parser = EHITableParser()
    parser.feed(html)
    parser.finalize()

    if not parser.table_name:
        parser.table_name = filepath.stem

    return {
        "table_name": parser.table_name,
        "source_file": filepath.name,
        "description": parser.description,
        "primary_key": parser.primary_key,
        "columns": parser.columns,
    }


def categorize_table(table_name, description):
    """Categorize a table into a domain based on name and description."""
    tn = table_name.upper()
    desc = (description or "").lower()

    # Order matters - more specific first
    categories = [
        # Billing / Revenue Cycle
        (r"^(ACCT_|ACCOUNT|ARPB_|AP_CLAIM|BILLING|BEN_|BUCKET_|CHG_|CLAIM|CLM_|COLLECTION|COVERAGE|CVG_|"
         r"EAF_|EAR_|EOB_|FIN_|GUAR_|HSP_ACCT|INS_|INVOICE|PAYOR|PMT_|RCTRL_|REFUND_|REV_|RX_CLAIM|"
         r"STMT_|TAX_|TX_|HAR_)", "Billing & Revenue Cycle"),

        # Scheduling / ADT
        (r"^(APPT_|BED_|PAT_ENC_APPT|SCHED_|DEPT_)", "Scheduling & ADT"),

        # Demographics / Patient
        (r"^(PATIENT|PAT_|IDENTITY_|EMERGENCY_)", "Patient Demographics"),

        # Encounters
        (r"^(PAT_ENC|ENC_|ENCOUNTER|HSP_|ADMIT_|DISCH_|TRANSFER_|VISIT_)", "Encounters"),

        # Problems / Diagnoses
        (r"^(PROBLEM_|DX_|DIAG_|CLARITY_EDG)", "Problems & Diagnoses"),

        # Medications
        (r"^(MAR_|MED_|RX_|RXNORM|DRUG_|PHARM_|DISPENSING|ORDER_MED|IP_MED|OP_MED)", "Medications"),

        # Allergies
        (r"^(ALLERGY|ALRGY_)", "Allergies"),

        # Immunizations
        (r"^(IMMUNE_|IMM_|IMMUNIZATION)", "Immunizations"),

        # Lab
        (r"^(LAB_|SPECIMEN|RESULT_|ORDER_RESULTS|ORD_RESULT|PATH_|MICRO_)", "Laboratory"),

        # Radiology / Imaging
        (r"^(RAD_|IMAGING|HNO_XRAY|IMG_)", "Radiology & Imaging"),

        # Vitals / Flowsheets
        (r"^(VITAL_|IP_FLWSHT|FLO_|FLWSHT_)", "Vitals & Flowsheets"),

        # Procedures / Surgery
        (r"^(OR_|SURGERY|SURG_|PROC_|ANES_|PERIOP_|OP_PROCEDURE|SURGICAL)", "Procedures & Surgery"),

        # Clinical Notes / Documents
        (r"^(HNO_|NOTE_|DOC_|SCAN_|CLINICAL_DOC)", "Clinical Notes & Documents"),

        # Orders
        (r"^(ORDER_|ORD_|REFERRAL)", "Orders & Referrals"),

        # Care Plans / Goals
        (r"^(CARE_PLAN|GOAL_|PLAN_)", "Care Plans & Goals"),

        # Oncology
        (r"^(ONCO_|CHEMO_|CANCER_|TUMOR_|BCN_|REGIMEN_|RADIATION)", "Oncology"),

        # Cardiology
        (r"^(CARDIAC|CATH_|ECG_|EKG_|ECHO_|EP_)", "Cardiology"),

        # OB / Perinatal
        (r"^(OB_|PREG_|LABOR_|DELIVERY|BABY_|BIRTH_|FETUS_|LDA_|LDR_)", "Obstetrics & Perinatal"),

        # Transplant
        (r"^(TRANSPLANT|XPLANT_|ORGAN_)", "Transplant"),

        # Social / Behavioral
        (r"^(SOCIAL_|BH_|SUBST_|BEHAV_|SUD_)", "Social & Behavioral Health"),

        # Consent / Advance Directives
        (r"^(ABN_|CONSENT_|ADV_DIR|DIRECTIVE)", "Consents & Directives"),

        # Communications / MyChart
        (r"^(MYC_|MYCHART|MSG_|MESSAGE|SECURE_MSG|PORTAL)", "Communications & Portal"),

        # Insurance / Coverage
        (r"^(CVG_|COVERAGE|AUTH_|PRIOR_AUTH|ELIG_|BENEFIT)", "Insurance & Coverage"),

        # Family History
        (r"^(FAM_|FAMILY_HX|FAMILY_HIST)", "Family History"),

        # Health Maintenance / Preventive
        (r"^(HM_|HEALTH_MAINT|PREV_CARE)", "Health Maintenance"),

        # Infection Control
        (r"^(INFECTION|HAI_|SURVEIL)", "Infection Control"),

        # Research / Trials
        (r"^(STUDY_|RESEARCH_|TRIAL_|IRB_)", "Research"),

        # General Clinical (catch-all for clinical)
        (r"^(CLARITY_|CL_|IP_|OP_)", "General Clinical"),
    ]

    for pattern, category in categories:
        if re.match(pattern, tn):
            return category

    # Description-based fallback
    desc_categories = [
        ("billing|charge|claim|payment|invoice|revenue|financial", "Billing & Revenue Cycle"),
        ("appointment|schedule|booking", "Scheduling & ADT"),
        ("medication|drug|pharmacy|prescription|dispens", "Medications"),
        ("allerg", "Allergies"),
        ("immuniz|vaccin", "Immunizations"),
        ("lab|specimen|culture|pathology", "Laboratory"),
        ("radiol|imaging|x-ray|ct scan|mri", "Radiology & Imaging"),
        ("surgery|surgical|anesthesia|periop|operative", "Procedures & Surgery"),
        ("note|document|report|narrative", "Clinical Notes & Documents"),
        ("order|referral", "Orders & Referrals"),
        ("oncol|chemo|cancer|tumor|radiation therapy", "Oncology"),
        ("cardiac|cardiol|catheter|echocard", "Cardiology"),
        ("obstetric|prenatal|labor|delivery|pregnan|perinatal|fetus|newborn", "Obstetrics & Perinatal"),
        ("transplant", "Transplant"),
        ("consent|advance directive|abn", "Consents & Directives"),
        ("mychart|patient portal|secure message", "Communications & Portal"),
        ("insurance|coverage|eligib|authorization|benefit|payer", "Insurance & Coverage"),
        ("family history", "Family History"),
        ("infection|surveillance|hai", "Infection Control"),
        ("encounter|visit|admission|discharge|transfer", "Encounters"),
        ("patient|demographic|address|phone|email|identity|race|ethnic", "Patient Demographics"),
        ("problem|diagnosis|condition", "Problems & Diagnoses"),
        ("vital|blood pressure|heart rate|temperature|weight|height|bmi", "Vitals & Flowsheets"),
        ("care plan|goal", "Care Plans & Goals"),
        ("flowsheet", "Vitals & Flowsheets"),
        ("health maintenance|preventive|screening", "Health Maintenance"),
        ("research|study|trial|clinical trial", "Research"),
        ("social|behavioral|substance", "Social & Behavioral Health"),
    ]

    for pattern, category in desc_categories:
        if re.search(pattern, desc):
            return category

    return "Other / Uncategorized"


def main():
    htm_files = sorted([
        f for f in EXTRACTED_DIR.iterdir()
        if f.suffix == ".htm" and not f.name.startswith("_")
    ])

    print(f"Found {len(htm_files)} .htm files to parse")

    tables = []
    failures = []

    for i, filepath in enumerate(htm_files):
        try:
            table = parse_htm_file(filepath)
            table["category"] = categorize_table(table["table_name"], table["description"])
            tables.append(table)
        except Exception as e:
            failures.append({"file": filepath.name, "error": str(e)})

        if (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1}/{len(htm_files)}...")

    tables.sort(key=lambda t: t["table_name"])

    # Write full inventory
    with open(OUTPUT_FULL, "w") as f:
        json.dump(tables, f, indent=2)
    print(f"Wrote {OUTPUT_FULL} ({len(tables)} tables)")

    # Compute summary
    total_columns = sum(len(t["columns"]) for t in tables)
    cols_with_desc = sum(1 for t in tables for c in t["columns"] if c["description"])
    cols_with_type = sum(1 for t in tables for c in t["columns"] if c["type"])
    tables_with_desc = sum(1 for t in tables if t["description"])
    discontinued_cols = sum(1 for t in tables for c in t["columns"] if c.get("discontinued"))

    # Category breakdown
    cat_stats = defaultdict(lambda: {"tables": 0, "columns": 0, "table_names": []})
    for t in tables:
        cat = t["category"]
        cat_stats[cat]["tables"] += 1
        cat_stats[cat]["columns"] += len(t["columns"])
        cat_stats[cat]["table_names"].append(t["table_name"])

    # Column type distribution
    type_counts = Counter(c["type"] for t in tables for c in t["columns"])

    # Largest tables
    largest = sorted(tables, key=lambda t: len(t["columns"]), reverse=True)[:25]

    summary = {
        "parse_info": {
            "total_htm_files": len(htm_files),
            "tables_parsed": len(tables),
            "parse_failures": len(failures),
            "failure_details": failures[:20],
        },
        "totals": {
            "tables": len(tables),
            "columns": total_columns,
            "columns_with_descriptions": cols_with_desc,
            "columns_with_types": cols_with_type,
            "tables_with_descriptions": tables_with_desc,
            "discontinued_columns": discontinued_cols,
            "description_coverage_pct": round(cols_with_desc / total_columns * 100, 1) if total_columns else 0,
        },
        "column_types": dict(type_counts.most_common()),
        "categories": {
            cat: {
                "tables": stats["tables"],
                "columns": stats["columns"],
                "sample_tables": stats["table_names"][:10],
            }
            for cat, stats in sorted(cat_stats.items(), key=lambda x: -x[1]["tables"])
        },
        "largest_tables": [
            {
                "table_name": t["table_name"],
                "columns": len(t["columns"]),
                "category": t["category"],
                "description": t["description"][:200],
            }
            for t in largest
        ],
    }

    with open(OUTPUT_SUMMARY, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {OUTPUT_SUMMARY}")

    # Print highlights
    print(f"\n=== SUMMARY ===")
    print(f"Tables: {len(tables)}")
    print(f"Columns: {total_columns}")
    print(f"Columns with descriptions: {cols_with_desc} ({summary['totals']['description_coverage_pct']}%)")
    print(f"Tables with descriptions: {tables_with_desc}")
    print(f"Discontinued columns: {discontinued_cols}")
    print(f"Parse failures: {len(failures)}")
    print(f"\nCategories:")
    for cat, stats in sorted(cat_stats.items(), key=lambda x: -x[1]["tables"]):
        print(f"  {cat}: {stats['tables']} tables, {stats['columns']} columns")

    if failures:
        print(f"\nFirst failures: {failures[:5]}")


if __name__ == "__main__":
    main()
