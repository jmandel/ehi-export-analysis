#!/usr/bin/env python3
"""
Parse all Tbl_*.htm files from the Sunrise EHI WebERDiagram PR38 extract.
Produces entity-inventory-full.json and entity-inventory-summary.json.

Usage:
  cd analysis/
  unzip -q ../downloads/ehi-weberdiagram-22-1-pr38.zip -d pr38-extracted
  python3 parse-weber.py
  rm -rf pr38-extracted  # cleanup
"""

import os
import re
import json
import glob as globmod
from html import unescape
from collections import Counter, defaultdict

BASE_DIR = os.path.join(os.path.dirname(__file__), "pr38-extracted", "EHI WebERDiagram 22.1 PR38")
SCHEMAS = ["FS", "IMG", "MNC", "SCM"]

def clean_text(s):
    """Strip HTML tags and entities, normalize whitespace."""
    s = re.sub(r'<[^>]+>', '', s)
    s = unescape(s)
    s = s.replace('\xa0', ' ').replace('&nbsp;', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_table_file(filepath, schema):
    """Parse a single Tbl_*.htm file into a structured dict."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        html = f.read()

    result = {"schema": schema, "sourceFile": os.path.relpath(filepath, os.path.dirname(__file__))}

    # Table name from TITLE
    m = re.search(r'<TITLE>([^<]+)</TITLE>', html, re.I)
    if not m:
        return None
    result["tableName"] = m.group(1).strip()

    # Qualified name
    m = re.search(r'dbo\.(\w+)', html)
    result["qualifiedName"] = f"dbo.{m.group(1)}" if m else f"dbo.{result['tableName']}"

    # Definition
    m = re.search(r'Definition[^<]*</FONT></B></TD>\s*<TD><FONT[^>]*>(.*?)</FONT></TD>', html, re.I | re.S)
    result["definition"] = clean_text(m.group(1)) if m else ""

    # Find PK columns (marked with pk.gif)
    pk_cols = set()
    for pm in re.finditer(r'<A[^>]*>([^<]+)</A>\s*<img[^>]*pk\.gif', html, re.I):
        pk_cols.add(clean_text(pm.group(1)))

    # Find FK columns (marked with fk.gif)
    fk_cols = set()
    for fm in re.finditer(r'<A[^>]*>([^<]+)</A>\s*<img[^>]*fk\.gif', html, re.I):
        fk_cols.add(clean_text(fm.group(1)))

    # Parse columns section
    columns = []
    col_section = re.search(r'ColumnName[\s\S]*?Definition[\s\S]*?</TR>([\s\S]*?)(?:</TABLE>)', html, re.I)
    if col_section:
        row_pattern = re.compile(
            r'<TR>\s*<TD[^>]*>\s*<FONT[^>]*>(?:<A[^>]*>)?([^<]+)(?:</A>)?(?:<img[^>]*>)?[^<]*</FONT></TD>'
            r'\s*<TD[^>]*>\s*<FONT[^>]*>(.*?)</FONT></TD>'
            r'\s*<TD[^>]*>\s*<FONT[^>]*>(.*?)</FONT></TD>'
            r'\s*<TD[^>]*>\s*<FONT[^>]*>(.*?)</FONT></TD>'
            r'\s*<TD[^>]*>\s*<FONT[^>]*>([\s\S]*?)</FONT></TD>',
            re.I
        )
        for rm in row_pattern.finditer(col_section.group(1)):
            col_name = clean_text(rm.group(1))
            col = {
                "name": col_name,
                "domain": clean_text(rm.group(2)),
                "datatype": clean_text(rm.group(3)),
                "nullable": clean_text(rm.group(4)).upper() == "YES",
                "isPrimaryKey": col_name in pk_cols,
                "isForeignKey": col_name in fk_cols,
                "definition": clean_text(rm.group(5)),
            }
            columns.append(col)

    result["columns"] = columns
    result["columnCount"] = len(columns)

    # Parse keys section
    keys = []
    key_section = re.search(r'Key Name.*?Keys.*?</TR>([\s\S]*?)(?:</TABLE>)', html, re.I)
    if key_section:
        key_row = re.compile(
            r'<TR>\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)</FONT></TD>'
            r'\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)</FONT></TD>'
            r'\s*<TD[^>]*>\s*<FONT[^>]*>([^<]*)</FONT></TD>',
            re.I
        )
        for km in key_row.finditer(key_section.group(1)):
            keys.append({
                "name": clean_text(km.group(1)),
                "type": clean_text(km.group(2)),
                "columns": clean_text(km.group(3)),
            })
    result["keys"] = keys

    return result

def infer_domain(table_name):
    """Infer functional domain from table name prefix."""
    prefixes = [
        ("SXARCM", "Revenue Cycle / Billing"),
        ("CV3Allergy", "Allergies"),
        ("CV3BasicObs", "Observations / Vitals"),
        ("CV3Clinical", "Clinical Documentation"),
        ("CV3Chart", "Chart / Documentation"),
        ("CV3Diag", "Diagnoses / Problems"),
        ("CV3Drug", "Medications / Pharmacy"),
        ("CV3Enc", "Encounters"),
        ("CV3Imm", "Immunizations"),
        ("CV3Lab", "Lab / Results"),
        ("CV3MedAdmin", "Medication Administration"),
        ("CV3Med", "Medications / Pharmacy"),
        ("CV3Note", "Clinical Notes"),
        ("CV3Order", "Orders"),
        ("CV3Obs", "Observations / Vitals"),
        ("CV3Pat", "Patient / Demographics"),
        ("CV3Person", "Patient / Demographics"),
        ("CV3Prob", "Problems / Conditions"),
        ("CV3Rad", "Radiology / Imaging"),
        ("CV3Reg", "Registration / ADT"),
        ("CV3Res", "Results"),
        ("CV3Spec", "Specimens"),
        ("CV3Surg", "Surgery / Perioperative"),
        ("CV3Task", "Tasks / Workflow"),
        ("CV3Visit", "Encounters / Visits"),
        ("CV3", "Core Clinical (CV3)"),
        ("SXAAMB", "Ambulatory Care"),
        ("SXAAM", "Ambulatory Care"),
        ("SXAADM", "Administration"),
        ("SXAADR", "ADR / Adverse Reactions"),
        ("SXAALRG", "Allergies"),
        ("SXAADT", "ADT / Registration"),
        ("SXABCMA", "Barcode Medication Admin"),
        ("SXACDE", "Clinical Doc / eICR"),
        ("SXACD", "Clinical Documentation"),
        ("SXACLIN", "Clinical"),
        ("SXACPOE", "CPOE / Orders"),
        ("SXACRT", "Clinical Record Tracking"),
        ("SXAEHR", "EHR Core"),
        ("SXAESM", "Enterprise Service Mgmt"),
        ("SXAFDB", "Drug Database (FDB)"),
        ("SXAHM", "Health Management"),
        ("SXAIMM", "Immunization Management"),
        ("SXAIMG", "Imaging / Documents"),
        ("SXAINT", "Interface / Integration"),
        ("SXAMNC", "Medical Necessity"),
        ("SXAMM", "Medication Management"),
        ("SXANOT", "Notifications"),
        ("SXAORD", "Orders"),
        ("SXAPHM", "Pharmacy Management"),
        ("SXAREG", "Registration"),
        ("SXARPT", "Reporting"),
        ("SXASCH", "Scheduling"),
        ("SXASRG", "Surgery / Perioperative"),
        ("SXATRS", "Transitions of Care"),
        ("SXAXRD", "Cross-Reference Data"),
        ("SXA", "Sunrise Application"),
        ("SXEHI", "EHI Export"),
    ]
    for prefix, domain in prefixes:
        if table_name.startswith(prefix):
            return domain
    return "Other / Uncategorized"

def main():
    all_tables = []
    errors = []

    for schema in SCHEMAS:
        content_dir = os.path.join(BASE_DIR, f"{schema} WebERDiagram 22.1 PR38", "Content")
        if not os.path.isdir(content_dir):
            print(f"Skipping {schema}: {content_dir} not found")
            continue

        table_files = sorted(globmod.glob(os.path.join(content_dir, "Tbl_*.htm")))
        # Exclude _Attr files
        table_files = [f for f in table_files if "_Attr" not in os.path.basename(f)]
        print(f"{schema}: found {len(table_files)} table files")

        for fp in table_files:
            try:
                tbl = parse_table_file(fp, schema)
                if tbl:
                    tbl["inferredDomain"] = infer_domain(tbl["tableName"])
                    all_tables.append(tbl)
                else:
                    errors.append({"file": fp, "error": "No TITLE tag"})
            except Exception as e:
                errors.append({"file": fp, "error": str(e)})

    # Stats
    total_columns = sum(t["columnCount"] for t in all_tables)
    cols_with_def = sum(
        1 for t in all_tables for c in t["columns"] if c["definition"]
    )
    cols_with_type = sum(
        1 for t in all_tables for c in t["columns"] if c["datatype"]
    )
    tables_with_def = sum(1 for t in all_tables if t["definition"])
    fk_count = sum(1 for t in all_tables for c in t["columns"] if c["isForeignKey"])

    # Domain breakdown
    domain_stats = defaultdict(lambda: {"tables": 0, "columns": 0, "described_columns": 0})
    for t in all_tables:
        d = t["inferredDomain"]
        domain_stats[d]["tables"] += 1
        domain_stats[d]["columns"] += t["columnCount"]
        domain_stats[d]["described_columns"] += sum(1 for c in t["columns"] if c["definition"])

    schema_stats = Counter(t["schema"] for t in all_tables)

    # Full inventory
    full_output = {
        "extractionDate": "2026-02-16",
        "sourceVersion": "EHI WebERDiagram 22.1 PR38",
        "product": "Altera Sunrise (Acute Care / Ambulatory Care)",
        "summary": {
            "totalTables": len(all_tables),
            "totalColumns": total_columns,
            "columnsWithDescription": cols_with_def,
            "columnsWithDatatype": cols_with_type,
            "tablesWithDefinition": tables_with_def,
            "foreignKeyColumns": fk_count,
            "parseErrors": len(errors),
            "tablesBySchema": dict(schema_stats),
        },
        "tables": all_tables,
        "parseErrors": errors,
    }

    out_dir = os.path.dirname(__file__)
    with open(os.path.join(out_dir, "entity-inventory-full.json"), "w") as f:
        json.dump(full_output, f, indent=2)
    print(f"\nWrote entity-inventory-full.json ({len(all_tables)} tables, {total_columns} columns)")

    # Summary inventory
    summary_output = {
        "extractionDate": "2026-02-16",
        "sourceVersion": "EHI WebERDiagram 22.1 PR38",
        "product": "Altera Sunrise (Acute Care / Ambulatory Care)",
        "summary": full_output["summary"],
        "domainBreakdown": {
            k: v for k, v in sorted(domain_stats.items(), key=lambda x: -x[1]["tables"])
        },
        "schemaBreakdown": dict(schema_stats),
        "top20LargestTables": sorted(
            [{"schema": t["schema"], "tableName": t["tableName"], "columnCount": t["columnCount"],
              "definition": t["definition"][:200], "domain": t["inferredDomain"]}
             for t in all_tables],
            key=lambda x: -x["columnCount"]
        )[:20],
        "tablesWithNoColumns": [
            {"schema": t["schema"], "tableName": t["tableName"], "definition": t["definition"]}
            for t in all_tables if t["columnCount"] == 0
        ],
        "tablesWithNoDefinition": sum(1 for t in all_tables if not t["definition"]),
        "descriptionCoverage": {
            "totalFields": total_columns,
            "fieldsWithDescription": cols_with_def,
            "percentDescribed": round(cols_with_def / total_columns * 100, 1) if total_columns else 0,
        },
    }

    with open(os.path.join(out_dir, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary_output, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")

    # Print key stats
    print(f"\n=== Summary ===")
    print(f"Tables: {len(all_tables)}")
    print(f"Columns: {total_columns}")
    print(f"Columns with description: {cols_with_def} ({cols_with_def/total_columns*100:.1f}%)")
    print(f"Tables with definition: {tables_with_def} ({tables_with_def/len(all_tables)*100:.1f}%)")
    print(f"FK columns: {fk_count}")
    print(f"Parse errors: {len(errors)}")
    print(f"\nSchema breakdown: {dict(schema_stats)}")
    print(f"\nDomain breakdown (top 15):")
    for domain, stats in sorted(domain_stats.items(), key=lambda x: -x[1]["tables"])[:15]:
        print(f"  {domain}: {stats['tables']} tables, {stats['columns']} cols, {stats['described_columns']} described")

if __name__ == "__main__":
    main()
