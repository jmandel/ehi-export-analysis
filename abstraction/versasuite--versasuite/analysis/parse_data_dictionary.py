#!/usr/bin/env python3
"""
Parse all VersaSuite EHI export data dictionary HTML files independently.
Produces full-entity-inventory.json and summary statistics.
"""

import json
import os
import re
from html.parser import HTMLParser
from pathlib import Path

DATA_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/versasuite--versasuite/downloads/data-dictionary")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/versasuite--versasuite/analysis")

class TableParser(HTMLParser):
    """Extract table rows from HTML data dictionary pages."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = []
        self.current_row = []
        self.current_cell = ""
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.in_h1 = False
        self.in_h2 = False
        self.h1_texts = []
        self.h2_texts = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
            self.current_table = []
        elif tag == "tr" and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th") and self.in_row:
            self.in_cell = True
            self.current_cell = ""
        elif tag == "h1":
            self.in_h1 = True
            self.current_cell = ""
        elif tag == "h2":
            self.in_h2 = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
            self.current_table = []
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
            self.current_row = []
        elif tag in ("td", "th") and self.in_cell:
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
            self.current_cell = ""
        elif tag == "h1" and self.in_h1:
            self.in_h1 = False
            self.h1_texts.append(self.current_cell.strip())
            self.current_cell = ""
        elif tag == "h2" and self.in_h2:
            self.in_h2 = False
            self.h2_texts.append(self.current_cell.strip())
            self.current_cell = ""

    def handle_data(self, data):
        if self.in_cell or self.in_h1 or self.in_h2:
            self.current_cell += data


PLACEHOLDER_PATTERNS = [
    "Provides information related to",
    "Contains detailed information or identifiers for the corresponding",
    "Specifies the date associated with the",
    "Specifies the .* event or record",
]

def is_placeholder(desc):
    """Check if a description is a generic placeholder."""
    if not desc:
        return True
    for pat in PLACEHOLDER_PATTERNS:
        if re.search(pat, desc, re.IGNORECASE):
            # Check if the description is essentially just the pattern with the field name
            cleaned = re.sub(pat, '', desc, flags=re.IGNORECASE).strip().rstrip('.')
            # If what remains is very short (just a field name restatement), it's placeholder
            if len(cleaned) < 30:
                return True
    return False


def classify_domain(table_name, prefix):
    """Classify table into domain based on prefix and name."""
    if prefix == "AP_":
        return "Administrative/Patient"
    elif prefix == "AX_":
        return "Accounting/Financial"
    elif prefix == "HC_":
        # Sub-classify HC tables
        name_lower = table_name.lower()
        if any(x in name_lower for x in ['blng', 'billing', 'bal', 'earning']):
            return "Billing/Financial"
        elif any(x in name_lower for x in ['lab']):
            return "Laboratory"
        elif any(x in name_lower for x in ['drug', 'med', 'rx', 'allergy']):
            return "Medications/Pharmacy"
        elif any(x in name_lower for x in ['appt']):
            return "Appointments"
        elif any(x in name_lower for x in ['bb', 'bt', 'blood']):
            return "Blood Bank"
        elif any(x in name_lower for x in ['bhcp', 'behavioral']):
            return "Behavioral Health"
        elif any(x in name_lower for x in ['problem']):
            return "Problems/Diagnoses"
        elif any(x in name_lower for x in ['pt.html', 'ptprv']):
            return "Patient Demographics"
        elif any(x in name_lower for x in ['contofcare', 'continuity']):
            return "Continuity of Care"
        elif any(x in name_lower for x in ['phi']):
            return "PHI Requests"
        elif any(x in name_lower for x in ['override']):
            return "Clinical Overrides"
        elif any(x in name_lower for x in ['osinst']):
            return "Order Sets/Instructions"
        else:
            return "Healthcare/Clinical"
    elif prefix == "EM_":
        return "Encounter Management"
    elif prefix == "VE_":
        return "EHR Exam/Template Data"
    elif prefix == "FQ_":
        return "Financial/Quality"
    else:
        # No prefix - classify by name
        name_lower = table_name.lower()
        if 'clinical' in name_lower or 'note' in name_lower:
            return "Clinical Notes"
        elif 'encounter' in name_lower or 'pthis' in name_lower or 'pttransfer' in name_lower or 'pttype' in name_lower:
            return "Encounter Management"
        elif 'billing' in name_lower or 'earning' in name_lower:
            return "Billing/Financial"
        elif 'address' in name_lower or 'patient address' in name_lower:
            return "Administrative/Patient"
        elif 'attachment' in name_lower:
            return "Documents/Attachments"
        elif 'allergy' in name_lower:
            return "Medications/Pharmacy"
        elif 'blood' in name_lower or 'behavioral' in name_lower:
            return "Healthcare/Clinical"
        elif 'direct deposit' in name_lower:
            return "Payroll/HR"
        else:
            return "Other"


def extract_table_name(filename, h1_texts, h2_texts):
    """Extract the canonical table name from filename and headings."""
    # Try to get CSV filename from h1
    for h in h1_texts:
        m = re.search(r'Documentation for (\S+\.csv)', h)
        if m:
            return m.group(1).replace('.csv', '')
    
    # Use filename without extension as base
    name = filename.replace('.html', '')
    # Clean up common suffixes but preserve uniqueness
    name = re.sub(r'\s*Data Dictionary\s*$', '', name)
    name = re.sub(r'\s*_Documentation_Updated\s*$', '', name)
    name = re.sub(r'\s*_Documentation\s*(\(\d+\))?\s*$', '', name)
    name = re.sub(r'\s*_documentation\s*$', '', name)
    name = re.sub(r'\s*_dataset_documentation\s*$', '', name)
    return name


def get_prefix(table_name):
    """Extract prefix like AP_, HC_, etc."""
    m = re.match(r'^([A-Z]{2}_)', table_name)
    return m.group(1) if m else None


def parse_file(filepath):
    """Parse a single HTML data dictionary file."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    parser = TableParser()
    parser.feed(content)
    
    # Handle unclosed tables - if current_table has data, add it
    if parser.current_table and not parser.tables:
        parser.tables.append(parser.current_table)
    elif parser.current_table:
        parser.tables.append(parser.current_table)
    
    if not parser.tables:
        return None
    
    # Use the first (usually only) table
    table = parser.tables[0]
    
    # First row should be headers
    if not table:
        return None
    
    headers = table[0] if table else []
    rows = table[1:] if len(table) > 1 else []
    
    filename = os.path.basename(filepath)
    table_name = extract_table_name(filename, parser.h1_texts, parser.h2_texts)
    prefix = get_prefix(table_name)
    
    columns = []
    has_ptid = False
    has_ptencid = False
    
    for row in rows:
        if len(row) >= 3:
            col = {
                "original_name": row[0],
                "expanded_name": row[1],
                "description": row[2],
                "is_placeholder": is_placeholder(row[2]),
            }
            columns.append(col)
            if row[0] == "PtID":
                has_ptid = True
            if row[0] == "PtEncID":
                has_ptencid = True
        elif len(row) == 2:
            col = {
                "original_name": row[0],
                "expanded_name": row[1],
                "description": "",
                "is_placeholder": True,
            }
            columns.append(col)
    
    domain = classify_domain(table_name, prefix)
    
    meaningful_descs = sum(1 for c in columns if not c["is_placeholder"])
    
    return {
        "file_name": filename,
        "table_name": table_name,
        "title": " | ".join(parser.h1_texts + parser.h2_texts),
        "prefix": prefix,
        "domain": domain,
        "column_count": len(columns),
        "meaningful_descriptions": meaningful_descs,
        "placeholder_descriptions": len(columns) - meaningful_descs,
        "has_patient_id": has_ptid,
        "has_encounter_id": has_ptencid,
        "columns": columns,
    }


def main():
    all_tables = []
    parse_errors = []
    
    # Get all HTML files except index
    html_files = sorted([
        f for f in DATA_DIR.glob("*.html") 
        if f.name != "index.html"
    ])
    
    for filepath in html_files:
        try:
            result = parse_file(filepath)
            if result:
                all_tables.append(result)
            else:
                parse_errors.append({
                    "file": filepath.name,
                    "error": "No table found",
                    "parse_error": True
                })
        except Exception as e:
            parse_errors.append({
                "file": filepath.name,
                "error": str(e),
                "parse_error": True
            })
    
    # Sort by table name
    all_tables.sort(key=lambda t: t["table_name"])
    
    # Write full inventory
    inventory_path = OUTPUT_DIR / "full-entity-inventory.json"
    with open(inventory_path, 'w') as f:
        json.dump(all_tables, f, indent=2)
    
    # Compute summary statistics
    total_cols = sum(t["column_count"] for t in all_tables)
    total_meaningful = sum(t["meaningful_descriptions"] for t in all_tables)
    total_placeholder = sum(t["placeholder_descriptions"] for t in all_tables)
    tables_with_ptid = sum(1 for t in all_tables if t["has_patient_id"])
    tables_with_encid = sum(1 for t in all_tables if t["has_encounter_id"])
    
    # Domain breakdown
    domain_stats = {}
    for t in all_tables:
        d = t["domain"]
        if d not in domain_stats:
            domain_stats[d] = {"tables": 0, "columns": 0, "meaningful_descs": 0, "placeholder_descs": 0}
        domain_stats[d]["tables"] += 1
        domain_stats[d]["columns"] += t["column_count"]
        domain_stats[d]["meaningful_descs"] += t["meaningful_descriptions"]
        domain_stats[d]["placeholder_descs"] += t["placeholder_descriptions"]
    
    # Prefix breakdown
    prefix_stats = {}
    for t in all_tables:
        p = t["prefix"] or "(none)"
        if p not in prefix_stats:
            prefix_stats[p] = {"tables": 0, "columns": 0}
        prefix_stats[p]["tables"] += 1
        prefix_stats[p]["columns"] += t["column_count"]
    
    # Top 20 largest tables
    largest = sorted(all_tables, key=lambda t: t["column_count"], reverse=True)[:20]
    
    # Tables with worst documentation (highest placeholder ratio)
    worst_docs = sorted(
        [t for t in all_tables if t["column_count"] > 5],
        key=lambda t: t["placeholder_descriptions"] / max(t["column_count"], 1),
        reverse=True
    )[:10]
    
    summary = {
        "total_tables": len(all_tables),
        "total_columns": total_cols,
        "meaningful_descriptions": total_meaningful,
        "placeholder_descriptions": total_placeholder,
        "description_rate": round(total_meaningful / total_cols * 100, 1) if total_cols else 0,
        "tables_with_patient_id": tables_with_ptid,
        "tables_with_encounter_id": tables_with_encid,
        "parse_errors": parse_errors,
        "domain_breakdown": domain_stats,
        "prefix_breakdown": prefix_stats,
        "largest_tables": [
            {"name": t["table_name"], "columns": t["column_count"], 
             "meaningful": t["meaningful_descriptions"], "domain": t["domain"]}
            for t in largest
        ],
        "worst_documented_tables": [
            {"name": t["table_name"], "columns": t["column_count"],
             "placeholders": t["placeholder_descriptions"], 
             "ratio": round(t["placeholder_descriptions"] / t["column_count"] * 100, 1)}
            for t in worst_docs
        ],
    }
    
    summary_path = OUTPUT_DIR / "summary-statistics.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary to stdout
    print(f"=== VersaSuite Data Dictionary Parse Results ===")
    print(f"Tables parsed: {len(all_tables)}")
    print(f"Parse errors: {len(parse_errors)}")
    print(f"Total columns: {total_cols}")
    print(f"Meaningful descriptions: {total_meaningful} ({round(total_meaningful/total_cols*100, 1)}%)")
    print(f"Placeholder descriptions: {total_placeholder} ({round(total_placeholder/total_cols*100, 1)}%)")
    print(f"Tables with PtID: {tables_with_ptid}")
    print(f"Tables with PtEncID: {tables_with_encid}")
    print()
    print("=== Domain Breakdown ===")
    for domain, stats in sorted(domain_stats.items(), key=lambda x: x[1]["columns"], reverse=True):
        print(f"  {domain}: {stats['tables']} tables, {stats['columns']} columns, {stats['meaningful_descs']} meaningful descs")
    print()
    print("=== Top 10 Largest Tables ===")
    for t in largest[:10]:
        print(f"  {t['table_name']}: {t['column_count']} cols ({t['meaningful_descriptions']} meaningful)")
    print()
    if parse_errors:
        print("=== Parse Errors ===")
        for e in parse_errors:
            print(f"  {e['file']}: {e['error']}")


if __name__ == "__main__":
    main()
