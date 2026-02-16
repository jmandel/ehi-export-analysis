#!/usr/bin/env python3
"""Parse the TheraOffice EHI Export PDF data dictionary from pdftotext output.

Reads the raw PDF text (extracted with pdftotext -layout) and produces:
- entity-inventory-full.json: complete table/column inventory
- entity-inventory-summary.json: aggregate statistics
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PDF_TEXT = SCRIPT_DIR / "pdf-text.txt"

def parse_tables(text: str) -> list[dict]:
    """Parse table definitions from the PDF text."""
    tables = []
    lines = text.split('\n')
    
    current_table = None
    in_columns = False
    header_seen = False
    
    for line in lines:
        stripped = line.strip()
        
        # Detect table header (table name on its own line, all caps with underscores)
        # Table names appear as standalone lines like "PAT_PROFILE" or "PTCASE"
        table_match = re.match(r'^(PAT_PROFILE\w*|PTCASE)\s*$', stripped)
        if table_match:
            if current_table:
                tables.append(current_table)
            current_table = {
                "table_name": table_match.group(1),
                "columns": []
            }
            in_columns = False
            header_seen = False
            continue
        
        if current_table is None:
            continue
        
        # Detect column header line
        if re.match(r'^Name\s+Data type\s+Max length', stripped):
            in_columns = True
            header_seen = True
            continue
        
        # Detect total line
        total_match = re.match(r'^Total:\s+(\d+)\s+column', stripped)
        if total_match:
            current_table["documented_column_count"] = int(total_match.group(1))
            in_columns = False
            continue
        
        # Skip empty lines, footer lines, page numbers
        if not stripped:
            continue
        if 'Confidential' in stripped or 'Copyright' in stripped or 'Netsmart' in stripped:
            continue
        if re.match(r'^\d+$', stripped):
            continue
        if stripped == 'Columns':
            continue
        
        # Parse column definition lines
        if in_columns and header_seen:
            # Column lines: NAME  datatype  maxlength
            col_match = re.match(r'^(\S+)\s+(varchar|int|smallint|tinyint|bit|smalldatetime|datetime|uniqueidentifier|decimal|bigint|float|nvarchar|text|ntext|image|varbinary|money|numeric|real|char|nchar)\s+(\S+)\s*$', stripped)
            if col_match:
                current_table["columns"].append({
                    "name": col_match.group(1),
                    "data_type": col_match.group(2),
                    "max_length": col_match.group(3),
                    "description": None
                })
            else:
                # Try more lenient match for multi-word types or edge cases
                col_match2 = re.match(r'^(\S+)\s+(.+?)\s+(\d+)\s*$', stripped)
                if col_match2:
                    current_table["columns"].append({
                        "name": col_match2.group(1),
                        "data_type": col_match2.group(2).strip(),
                        "max_length": col_match2.group(3),
                        "description": None
                    })
    
    if current_table:
        tables.append(current_table)
    
    return tables


def add_glossary_descriptions(tables: list[dict]) -> None:
    """Add descriptions from the glossary to matching columns."""
    glossary = {
        "Id": "The database row id of the selected record. When present, this field will often be considered a unique row identifier.",
        "PAT_ID": "Unique patient identifier within the TheraOffice environment.",
        "MODIFIED_USER": "The user who last updated the row.",
        "MODIFIED_DATE": "The date the row was last updated.",
        "CREATED_USER": "The user who created the record.",
        "CREATED_DATE": "The date the row was created."
    }
    for table in tables:
        for col in table["columns"]:
            name_upper = col["name"].upper()
            if col["name"] in glossary:
                col["description"] = glossary[col["name"]]
            elif name_upper == "PAT_ID":
                col["description"] = glossary["PAT_ID"]
            elif name_upper == "MODIFIED_USER":
                col["description"] = glossary["MODIFIED_USER"]
            elif name_upper == "MODIFIED_DATE":
                col["description"] = glossary["MODIFIED_DATE"]
            elif name_upper == "CREATED_USER":
                col["description"] = glossary["CREATED_USER"]
            elif name_upper == "CREATED_DATE":
                col["description"] = glossary["CREATED_DATE"]


def categorize_table(table_name: str) -> str:
    """Assign a domain category based on table name."""
    categories = {
        "PAT_PROFILE": "Demographics",
        "PAT_PROFILE_CORE": "Demographics",
        "PAT_PROFILE_CORE_ETHNICITY": "Demographics",
        "PAT_PROFILE_CORE_GENDER": "Demographics",
        "PAT_PROFILE_CORE_RACE": "Demographics",
        "PAT_PROFILE_USCDI_ALLERGIES": "Allergies",
        "PAT_PROFILE_USCDI_FAMILY_HISTORY": "Family Health History",
        "PAT_PROFILE_USCDI_FAMILY_MEMBER": "Family Health History",
        "PAT_PROFILE_USCDI_GOALS": "Goals",
        "PAT_PROFILE_USCDI_IMMUNIZATIONS": "Immunizations",
        "PAT_PROFILE_USCDI_IMMUNIZATIONS_ACKNOWLEDGEMENT": "Immunizations",
        "PAT_PROFILE_USCDI_IMPLANTDEVS": "Implantable Devices",
        "PAT_PROFILE_USCDI_LABS": "Laboratory Results",
        "PAT_PROFILE_USCDI_MEDICATIONS": "Medications",
        "PAT_PROFILE_USCDI_PROBLEMS": "Problems / Conditions",
        "PAT_PROFILE_USCDI_PROCEDURES": "Procedures",
        "PAT_PROFILE_USCDI_PROGRAM_ADMISSION": "Encounters / Admissions",
        "PAT_PROFILE_USCDI_VITALSIGNS": "Vital Signs",
        "PTCASE": "Case / Billing"
    }
    return categories.get(table_name, "Unknown")


def generate_summary(tables: list[dict]) -> dict:
    """Generate summary statistics from the parsed tables."""
    total_columns = sum(len(t["columns"]) for t in tables)
    columns_with_desc = sum(
        1 for t in tables for c in t["columns"] if c.get("description")
    )
    
    # Category breakdown
    categories = {}
    for t in tables:
        cat = categorize_table(t["table_name"])
        if cat not in categories:
            categories[cat] = {"table_count": 0, "field_count": 0}
        categories[cat]["table_count"] += 1
        categories[cat]["field_count"] += len(t["columns"])
    
    # Data type distribution
    type_dist = {}
    for t in tables:
        for c in t["columns"]:
            dt = c["data_type"]
            type_dist[dt] = type_dist.get(dt, 0) + 1
    
    # Tables with USCDI prefix
    uscdi_tables = [t for t in tables if "USCDI" in t["table_name"]]
    non_uscdi_tables = [t for t in tables if "USCDI" not in t["table_name"]]
    
    # Parse validation
    parse_mismatches = []
    for t in tables:
        doc_count = t.get("documented_column_count")
        actual_count = len(t["columns"])
        if doc_count and doc_count != actual_count:
            parse_mismatches.append({
                "table": t["table_name"],
                "documented": doc_count,
                "parsed": actual_count
            })
    
    return {
        "total_tables": len(tables),
        "total_columns": total_columns,
        "columns_with_descriptions": columns_with_desc,
        "description_percentage": round(columns_with_desc / total_columns * 100, 1) if total_columns else 0,
        "uscdi_prefixed_tables": len(uscdi_tables),
        "uscdi_prefixed_columns": sum(len(t["columns"]) for t in uscdi_tables),
        "non_uscdi_tables": len(non_uscdi_tables),
        "non_uscdi_columns": sum(len(t["columns"]) for t in non_uscdi_tables),
        "category_breakdown": categories,
        "data_type_distribution": dict(sorted(type_dist.items(), key=lambda x: -x[1])),
        "parse_mismatches": parse_mismatches,
        "coded_fields_without_valuesets": sum(
            1 for t in tables for c in t["columns"]
            if c["data_type"] in ("tinyint", "smallint") and not c.get("description")
        )
    }


def main():
    text = PDF_TEXT.read_text()
    tables = parse_tables(text)
    add_glossary_descriptions(tables)
    
    # Add category to each table
    for t in tables:
        t["category"] = categorize_table(t["table_name"])
        t["parsed_column_count"] = len(t["columns"])
    
    # Write full inventory
    full_output = {
        "source": "EHI Export All Tables - May 2024 (TheraOffice).pdf",
        "extraction_method": "pdftotext -layout → regex parsing",
        "tables": tables
    }
    
    full_path = SCRIPT_DIR / "entity-inventory-full.json"
    with open(full_path, 'w') as f:
        json.dump(full_output, f, indent=2)
    print(f"Wrote {full_path} ({len(tables)} tables)")
    
    # Write summary
    summary = generate_summary(tables)
    summary_path = SCRIPT_DIR / "entity-inventory-summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {summary_path}")
    
    # Print summary to console
    print(f"\n=== Summary ===")
    print(f"Tables: {summary['total_tables']}")
    print(f"Total columns: {summary['total_columns']}")
    print(f"Columns with descriptions: {summary['columns_with_descriptions']} ({summary['description_percentage']}%)")
    print(f"USCDI-prefixed tables: {summary['uscdi_prefixed_tables']} ({summary['uscdi_prefixed_columns']} cols)")
    print(f"Non-USCDI tables: {summary['non_uscdi_tables']} ({summary['non_uscdi_columns']} cols)")
    print(f"Coded fields without value sets: {summary['coded_fields_without_valuesets']}")
    
    if summary['parse_mismatches']:
        print(f"\n⚠ Parse mismatches:")
        for m in summary['parse_mismatches']:
            print(f"  {m['table']}: documented={m['documented']}, parsed={m['parsed']}")
    else:
        print(f"\n✓ All table column counts match documented counts")
    
    print(f"\nCategory breakdown:")
    for cat, info in sorted(summary['category_breakdown'].items()):
        print(f"  {cat}: {info['table_count']} tables, {info['field_count']} fields")
    
    print(f"\nData type distribution:")
    for dt, count in summary['data_type_distribution'].items():
        print(f"  {dt}: {count}")


if __name__ == "__main__":
    main()
