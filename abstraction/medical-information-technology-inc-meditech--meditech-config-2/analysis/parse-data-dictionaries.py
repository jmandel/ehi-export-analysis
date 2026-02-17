#!/usr/bin/env python3
"""
Parses MEDITECH EHI Export CSV data dictionary PDFs (via pdftotext -layout output).

Reads three pre-extracted text files:
  - cs-text.txt (Client/Server Acute & Ambulatory)
  - mg-text.txt (MAGIC Acute & Ambulatory)
  - 608-text.txt (MPM 6.08 Ambulatory)

Produces:
  - entity-inventory-full.json (complete field-level extraction)
  - entity-inventory-summary.json (aggregate statistics)
"""

import json
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_pdf_text(filepath: str) -> dict:
    """Parse a pdftotext -layout extracted text file from a MEDITECH CSV data dictionary PDF."""
    with open(filepath, "r") as f:
        text = f.read()

    lines = text.split("\n")

    # Extract metadata
    platform = ""
    last_updated = ""
    for line in lines[:15]:
        t = line.strip()
        if t.startswith("Platform:"):
            platform = t.replace("Platform:", "").strip()
        if "Last Updated:" in t:
            m = re.search(r"Last Updated:\s*(.*)", t)
            if m:
                last_updated = m.group(1).strip()

    # Find the header row "Field ... Table ... Column"
    data_start = -1
    for i, line in enumerate(lines):
        t = line.strip()
        if re.match(r"^Field\s+Table\s+Column\s*$", t):
            data_start = i + 1
            break

    if data_start == -1:
        return {
            "platform": platform,
            "last_updated": last_updated,
            "tables": [],
            "total_fields": 0,
            "total_tables": 0,
            "parse_errors": ["Could not find 'Field Table Column' header row"],
        }

    # Parse data rows
    # The PDF has three columns: Field (human label), Table (table name), Column (column name)
    # Table headers appear as standalone lines (single word, PascalCase)
    # Page numbers, "MEDITECH", header repeats, and metadata repeats are noise

    tables = {}  # table_name -> list of field dicts
    current_table = None
    parse_errors = []
    total_raw_lines = 0

    noise_patterns = [
        r"^\d+$",  # page numbers
        r"^MEDITECH$",
        r"EHI Export Data in CSV File",
        r"Last Updated:",
        r"^Field\s+Table\s+Column\s*$",  # repeated header
        r"^Platform:",
        r"^The tables/columns below",
        r"^EHI Export Patient Data",
    ]

    for i in range(data_start, len(lines)):
        line = lines[i]
        trimmed = line.strip()

        if not trimmed:
            continue

        # Skip noise lines
        is_noise = False
        for pat in noise_patterns:
            if re.search(pat, trimmed, re.IGNORECASE):
                is_noise = True
                break
        if is_noise:
            continue

        total_raw_lines += 1

        # Split on 2+ whitespace to identify columns
        # But we need to be careful: some field names have spaces within them
        # The layout uses fixed-width columns, so we can use column positions

        # Strategy: split on runs of 2+ spaces
        segments = re.split(r"\s{2,}", trimmed)

        if len(segments) == 1:
            # Single segment = table header (e.g., "AdmEmployers")
            # But also check it looks like an identifier (PascalCase or similar)
            name = segments[0]
            # Some table names might have spaces if they're multi-word,
            # but in practice MEDITECH uses PascalCase
            current_table = name
            if current_table not in tables:
                tables[current_table] = []
        elif len(segments) == 2:
            # Two segments: field + column (table implied from context)
            # Or could be table_header + something
            # In context, this is usually: Field, Column (table is current_table)
            if current_table:
                tables[current_table].append({
                    "field": segments[0],
                    "table": current_table,
                    "column": segments[1],
                })
            else:
                parse_errors.append(f"Line {i+1}: Two-segment line without active table: '{trimmed}'")
        elif len(segments) >= 3:
            # Three+ segments: Field, Table, Column
            field_name = segments[0]
            table_name = segments[1]
            column_name = " ".join(segments[2:])

            # If the table changed, update current
            if table_name != current_table:
                current_table = table_name
                if current_table not in tables:
                    tables[current_table] = []

            tables.setdefault(table_name, []).append({
                "field": field_name,
                "table": table_name,
                "column": column_name,
            })

    # Build structured output
    table_list = []
    total_fields = 0
    for table_name, fields in tables.items():
        table_list.append({
            "table_name": table_name,
            "field_count": len(fields),
            "fields": fields,
        })
        total_fields += len(fields)

    return {
        "platform": platform,
        "last_updated": last_updated,
        "tables": table_list,
        "total_fields": total_fields,
        "total_tables": len(table_list),
        "parse_errors": parse_errors,
        "raw_data_lines_processed": total_raw_lines,
    }


def categorize_table(table_name: str) -> str:
    """Categorize a table by its prefix into a domain."""
    prefix_map = {
        "Adm": "Admissions / Demographics",
        "Apr": "Ambulatory / Practice Management",
        "Arm": "Authorization / Referral Management",
        "Bbk": "Blood Bank",
        "Edm": "Emergency Department",
        "Eps": "E-Prescribing",
        "Hub": "Interoperability Hub",
        "Its": "Interface Transaction Services",
        "Lab": "Laboratory",
        "Mic": "Microbiology",
        "Mri": "Medical Records / Imaging",
        "Nur": "Nursing",
        "Oe": "Order Entry",
        "Pbr": "Patient Billing / Records",
        "Pha": "Pharmacy",
        "Pth": "Pathology",
        "Rad": "Radiology",
        "Rxm": "Prescriptions / Medications",
        "Sch": "Scheduling / Care",
    }

    for prefix, category in sorted(prefix_map.items(), key=lambda x: -len(x[0])):
        if table_name.startswith(prefix):
            return category

    return "Other"


def build_summary(platforms: dict) -> dict:
    """Build summary statistics from parsed platform data."""
    summary = {
        "platforms": {},
        "cross_platform": {
            "total_tables_all": 0,
            "total_fields_all": 0,
            "unique_table_names": set(),
            "shared_tables": [],
            "platform_only_tables": {},
        },
    }

    all_table_names = {}  # table_name -> set of platforms

    for plat_key, data in platforms.items():
        # Per-platform stats
        categories = {}
        for tbl in data["tables"]:
            cat = categorize_table(tbl["table_name"])
            if cat not in categories:
                categories[cat] = {"table_count": 0, "field_count": 0, "tables": []}
            categories[cat]["table_count"] += 1
            categories[cat]["field_count"] += tbl["field_count"]
            categories[cat]["tables"].append(tbl["table_name"])

            # Track cross-platform
            if tbl["table_name"] not in all_table_names:
                all_table_names[tbl["table_name"]] = set()
            all_table_names[tbl["table_name"]].add(plat_key)

        summary["platforms"][plat_key] = {
            "platform": data["platform"],
            "last_updated": data["last_updated"],
            "total_tables": data["total_tables"],
            "total_fields": data["total_fields"],
            "parse_errors": len(data["parse_errors"]),
            "categories": {
                k: {"table_count": v["table_count"], "field_count": v["field_count"], "tables": sorted(v["tables"])}
                for k, v in sorted(categories.items())
            },
        }
        summary["cross_platform"]["total_tables_all"] += data["total_tables"]
        summary["cross_platform"]["total_fields_all"] += data["total_fields"]

    # Cross-platform analysis
    summary["cross_platform"]["unique_table_names"] = sorted(all_table_names.keys())
    summary["cross_platform"]["unique_table_count"] = len(all_table_names)

    all_platform_keys = set(platforms.keys())
    shared = [name for name, plats in all_table_names.items() if plats == all_platform_keys]
    summary["cross_platform"]["shared_tables"] = sorted(shared)
    summary["cross_platform"]["shared_table_count"] = len(shared)

    for plat_key in platforms:
        only = [name for name, plats in all_table_names.items() if plats == {plat_key}]
        summary["cross_platform"]["platform_only_tables"] = summary["cross_platform"].get("platform_only_tables", {})
        summary["cross_platform"]["platform_only_tables"][plat_key] = sorted(only)

    # Category breakdown across all platforms (unique tables)
    all_categories = {}
    for name in all_table_names:
        cat = categorize_table(name)
        if cat not in all_categories:
            all_categories[cat] = set()
        all_categories[cat].add(name)

    summary["cross_platform"]["categories_unique"] = {
        k: {"unique_tables": len(v), "table_names": sorted(v)}
        for k, v in sorted(all_categories.items())
    }

    return summary


def main():
    files = {
        "client_server": os.path.join(SCRIPT_DIR, "cs-text.txt"),
        "magic": os.path.join(SCRIPT_DIR, "mg-text.txt"),
        "mpm_608": os.path.join(SCRIPT_DIR, "608-text.txt"),
    }

    platforms = {}
    for key, filepath in files.items():
        print(f"Parsing {filepath}...")
        result = parse_pdf_text(filepath)
        platforms[key] = result
        print(f"  Platform: {result['platform']}")
        print(f"  Tables: {result['total_tables']}, Fields: {result['total_fields']}")
        if result["parse_errors"]:
            print(f"  Parse errors: {len(result['parse_errors'])}")
            for err in result["parse_errors"][:5]:
                print(f"    - {err}")

    # Build full inventory
    full_inventory = {
        "extraction_date": "2026-02-16",
        "source": "MEDITECH EHI Export CSV Data Dictionary PDFs (Config 2)",
        "description": "Complete field-level extraction of all three platform-specific CSV data dictionaries for MEDITECH Configuration 2 EHI Export.",
        "platforms": {}
    }
    for key, data in platforms.items():
        full_inventory["platforms"][key] = {
            "platform": data["platform"],
            "last_updated": data["last_updated"],
            "total_tables": data["total_tables"],
            "total_fields": data["total_fields"],
            "parse_errors": data["parse_errors"],
            "tables": data["tables"],
        }

    full_path = os.path.join(SCRIPT_DIR, "entity-inventory-full.json")
    with open(full_path, "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"\nFull inventory written to {full_path}")

    # Build summary
    summary = build_summary(platforms)
    summary["extraction_date"] = "2026-02-16"
    summary["source"] = "MEDITECH EHI Export CSV Data Dictionary PDFs (Config 2)"

    summary_path = os.path.join(SCRIPT_DIR, "entity-inventory-summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=lambda x: sorted(x) if isinstance(x, set) else x)
    print(f"Summary written to {summary_path}")

    # Print summary for console
    print("\n=== SUMMARY ===")
    for key, pdata in summary["platforms"].items():
        print(f"\n{pdata['platform']}:")
        print(f"  Tables: {pdata['total_tables']}, Fields: {pdata['total_fields']}")
        print(f"  Categories:")
        for cat, cdata in sorted(pdata["categories"].items()):
            print(f"    {cat}: {cdata['table_count']} tables, {cdata['field_count']} fields")

    print(f"\nCross-platform:")
    print(f"  Total tables (all): {summary['cross_platform']['total_tables_all']}")
    print(f"  Total fields (all): {summary['cross_platform']['total_fields_all']}")
    print(f"  Unique table names: {summary['cross_platform']['unique_table_count']}")
    print(f"  Shared across all 3: {summary['cross_platform']['shared_table_count']}")


if __name__ == "__main__":
    main()
