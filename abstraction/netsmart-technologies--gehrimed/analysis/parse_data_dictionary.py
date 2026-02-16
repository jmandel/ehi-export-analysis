#!/usr/bin/env python3
"""Parse the GEHRIMED EHI Export data dictionary from pdftotext output.

Reads the plain-text extraction of the PDF and produces:
  - entity-inventory-full.json: every table and every column with all metadata
  - entity-inventory-summary.json: aggregate statistics
"""

import json
import re
import sys
from pathlib import Path

TEXT_FILE = Path(__file__).parent.parent / "downloads" / "ehi_export_all_tables_gehrimed_2023.txt"

def parse(text: str):
    # Split into table sections using "Table Name:" headers (skip TOC lines with dots)
    # The actual table sections start with "Table Name: Xxx" followed by a description or columns
    lines = text.split("\n")

    tables = []
    current_table = None
    current_column = None
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip TOC entries (contain dots/page numbers)
        if re.match(r"^Table Name:.*\.{3,}", line):
            i += 1
            continue

        # Detect table header
        m = re.match(r"^Table Name:\s*(.+)$", line)
        if m:
            if current_table and current_column:
                current_table["columns"].append(current_column)
                current_column = None
            if current_table:
                tables.append(current_table)
            table_name = m.group(1).strip()
            current_table = {
                "table_name": table_name,
                "description": "",
                "columns": []
            }
            # Next line(s) may be table description (before first Column Name:)
            desc_lines = []
            i += 1
            while i < len(lines):
                peek = lines[i].strip()
                if peek.startswith("Column Name:"):
                    break
                if peek and not peek.startswith("Confidential.") and not peek.startswith("Table Name:") and not re.match(r"^\d+$", peek):
                    desc_lines.append(peek)
                i += 1
            current_table["description"] = " ".join(desc_lines).strip()
            continue

        # Detect column
        cm = re.match(r"^Column Name:\s*(.+)$", line)
        if cm and current_table is not None:
            if current_column:
                current_table["columns"].append(current_column)
            current_column = {
                "column_name": cm.group(1).strip(),
                "column_type": None,
                "max_length": None,
                "description": ""
            }
            i += 1
            continue

        # Detect column type
        tm = re.match(r"^ColumnType:\s*(.+)$", line)
        if tm and current_column is not None:
            current_column["column_type"] = tm.group(1).strip()
            i += 1
            continue

        # Detect max length
        lm = re.match(r"^Max Length:\s*(.+)$", line)
        if lm and current_column is not None:
            val = lm.group(1).strip()
            current_column["max_length"] = val if val != "NULL" else None
            i += 1
            continue

        # Accumulate description lines for current column
        if current_column is not None and line and not line.startswith("Confidential.") and not re.match(r"^\d+$", line):
            if current_column["description"]:
                current_column["description"] += " " + line
            else:
                current_column["description"] = line

        i += 1

    # Flush last
    if current_table and current_column:
        current_table["columns"].append(current_column)
    if current_table:
        tables.append(current_table)

    return tables


def categorize(table_name: str) -> str:
    """Assign a domain category based on table name."""
    name = table_name.lower()
    if name.startswith("patient_medication") or name.startswith("patient_med"):
        return "Medications"
    if name.startswith("patient_immuniz"):
        return "Immunizations"
    if name.startswith("patient_lab") or name.startswith("lab"):
        return "Laboratory"
    if name.startswith("patient_problem"):
        return "Problems / Diagnoses"
    if name.startswith("patient_vital"):
        return "Vitals"
    if name.startswith("patient_procedure"):
        return "Procedures"
    if name.startswith("patient_assess"):
        return "Assessments"
    if name.startswith("patient_history"):
        return "Family History"
    if name.startswith("patient_imaging"):
        return "Imaging"
    if name.startswith("patient_relationship"):
        return "Demographics / Relationships"
    if name.startswith("patient_schedule"):
        return "Scheduling"
    if name.startswith("patientinfo") or name == "hl7_patient":
        return "Demographics"
    if name.startswith("patientimplant"):
        return "Implantable Devices"
    if name.startswith("smoking") or name == "patientinfo_smoking":
        return "Smoking / Social History"
    if name.startswith("dictation") or name == "document":
        return "Clinical Notes / Encounters"
    if name.startswith("hl7_patientinsurance"):
        return "Insurance"
    if name.startswith("attachment"):
        return "Attachments / Documents"
    if name.startswith("aspnet") or name == "groups":
        return "User / System"
    if name.startswith("companyinfo"):
        return "Organization"
    if name.startswith("enum"):
        return "Reference / Lookup"
    if name.startswith("interface"):
        return "Interfaces / Integration"
    return "Other"


def main():
    text = TEXT_FILE.read_text()
    tables = parse(text)

    # Build full inventory
    full_inventory = []
    for t in tables:
        cols = []
        for c in t["columns"]:
            cols.append({
                "column_name": c["column_name"],
                "column_type": c["column_type"],
                "max_length": c["max_length"],
                "description": c["description"] if c["description"] else None,
            })
        full_inventory.append({
            "table_name": t["table_name"],
            "table_description": t["description"] if t["description"] else None,
            "category": categorize(t["table_name"]),
            "column_count": len(cols),
            "columns": cols
        })

    out_dir = Path(__file__).parent
    with open(out_dir / "entity-inventory-full.json", "w") as f:
        json.dump(full_inventory, f, indent=2)

    # Build summary
    total_tables = len(full_inventory)
    total_fields = sum(t["column_count"] for t in full_inventory)
    fields_with_desc = sum(
        1 for t in full_inventory for c in t["columns"]
        if c["description"]
    )
    fields_with_type = sum(
        1 for t in full_inventory for c in t["columns"]
        if c["column_type"]
    )

    # Category breakdown
    cat_stats = {}
    for t in full_inventory:
        cat = t["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"tables": 0, "fields": 0, "fields_with_description": 0}
        cat_stats[cat]["tables"] += 1
        cat_stats[cat]["fields"] += t["column_count"]
        cat_stats[cat]["fields_with_description"] += sum(
            1 for c in t["columns"] if c["description"]
        )

    summary = {
        "total_tables": total_tables,
        "total_fields": total_fields,
        "fields_with_description": fields_with_desc,
        "fields_with_type": fields_with_type,
        "pct_described": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
        "pct_typed": round(100 * fields_with_type / total_fields, 1) if total_fields else 0,
        "categories": cat_stats,
        "tables": [
            {
                "table_name": t["table_name"],
                "category": t["category"],
                "column_count": t["column_count"],
                "described_columns": sum(1 for c in t["columns"] if c["description"]),
                "table_description": t["table_description"]
            }
            for t in full_inventory
        ]
    }

    with open(out_dir / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary to stdout
    print(f"Tables: {total_tables}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with description: {fields_with_desc} ({summary['pct_described']}%)")
    print(f"Fields with type: {fields_with_type} ({summary['pct_typed']}%)")
    print()
    print("Category breakdown:")
    for cat, stats in sorted(cat_stats.items()):
        print(f"  {cat}: {stats['tables']} tables, {stats['fields']} fields, {stats['fields_with_description']} described")
    print()
    print("Tables:")
    for t in summary["tables"]:
        print(f"  {t['table_name']}: {t['column_count']} cols, {t['described_columns']} described — [{t['category']}]")


if __name__ == "__main__":
    main()
