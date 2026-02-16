#!/usr/bin/env python3
"""Parse the Aarista EHI Export PDF data dictionary into structured JSON.

Reads the pdftotext output and extracts all 7 tables with their fields,
data types, and metadata. Produces full-entity-inventory.json and summary stats.
"""

import json
import re
import subprocess
import sys

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/aarista-technology-llc--aarista/downloads/Aarista_EHI_Export.pdf"
OUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/aarista-technology-llc--aarista/analysis"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_tables(text):
    # Split into sections by table headers
    table_patterns = [
        ("patient_demographics", "Single Patient - Patient Demographics"),
        ("patient_addresses", "Single Patient - Patient Addresses"),
        ("patient_contacts", "Single Patient - Patient Contacts"),
        ("patient_insurances", "Single Patient - Patient Insurances"),
        ("patient_encounters_clinical_billing", "Single Patient - Patient Encounters – Clinical and Billing"),
        ("practice_billing_encounters", "Practice Patients - Patient Demographics and Billing Encounters"),
        ("practice_clinical_encounters", "Practice Patients - Patient Demographics and Clinical Encounters"),
    ]

    tables = []
    lines = text.split('\n')

    def normalize(s):
        return s.replace('\u2013', '-').replace('\u2014', '-').replace('–', '-').replace('—', '-').lower()

    for idx, (table_id, table_title) in enumerate(table_patterns):
        start_line = None
        for i, line in enumerate(lines):
            if normalize(table_title) in normalize(line):
                start_line = i
                break

        if start_line is None:
            print(f"WARNING: Could not find table '{table_title}'", file=sys.stderr)
            continue

        end_line = len(lines)
        if idx + 1 < len(table_patterns):
            next_title = table_patterns[idx + 1][1]
            for i in range(start_line + 1, len(lines)):
                if normalize(next_title) in normalize(lines[i]):
                    end_line = i
                    break

        section_lines = lines[start_line:end_line]
        fields = []

        # More permissive pattern: field name (with special chars) separated by 2+ spaces from type
        field_pattern = re.compile(r'^\s*(.+?)\s{2,}(\S.+?)\s*$')

        for line in section_lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            if 'Data Field' in line_stripped and 'Data Type' in line_stripped:
                continue
            if line_stripped == 'Data Field' or line_stripped == 'Data Type':
                continue
            if normalize(table_title) in normalize(line_stripped):
                continue
            # Skip bullet points and prose
            if line_stripped.startswith('•') or line_stripped.startswith('The '):
                continue

            match = field_pattern.match(line)
            if match:
                field_name = match.group(1).strip()
                data_type = match.group(2).strip()

                # Skip header-like lines
                if field_name in ('Data Field', 'Data Type', ''):
                    continue
                # Skip if data_type doesn't look like a SQL type or known annotation
                if not re.search(r'(nvarchar|int|date|float|bit|varchar|nchar|derived|n/a|digits|constant)', data_type, re.I):
                    continue

                required = '*' in field_name or '*' in data_type
                field_name = field_name.replace('*', '').strip()

                multiple = 'multiple records' in data_type.lower()
                notes = None
                if ' - ' in data_type:
                    parts = data_type.split(' - ', 1)
                    data_type_clean = parts[0].strip()
                    notes = parts[1].strip()
                else:
                    data_type_clean = data_type

                extra_notes = []
                if 'hardcoded' in data_type.lower():
                    extra_notes.append('hardcoded')
                if 'derived' in data_type.lower():
                    extra_notes.append('derived field')
                if data_type_clean.strip().lower() == 'n/a':
                    extra_notes.append('not applicable / unused')

                field_obj = {
                    "name": field_name,
                    "data_type": data_type_clean,
                    "required": required,
                    "description": "",
                }
                if multiple:
                    field_obj["multiple_records"] = True
                if notes:
                    field_obj["notes"] = notes
                if extra_notes:
                    field_obj["annotations"] = extra_notes

                fields.append(field_obj)

        # Determine scope and category
        scope = "practice-wide (all patients)" if table_id.startswith("practice_") else "single patient"
        
        if table_id == "patient_encounters_clinical_billing":
            category = "Clinical and Billing"
        elif 'billing' in table_id:
            category = "Billing"
        elif 'clinical' in table_id:
            category = "Clinical"
        elif 'insurance' in table_id:
            category = "Insurance"
        elif any(x in table_id for x in ('demographic', 'address', 'contact')):
            category = "Demographics"
        else:
            category = "Other"

        tables.append({
            "id": table_id,
            "title": table_title,
            "scope": scope,
            "category": category,
            "field_count": len(fields),
            "fields": fields,
        })

    return tables


def compute_summary(tables):
    total_fields = sum(t["field_count"] for t in tables)
    fields_with_descriptions = sum(
        1 for t in tables for f in t["fields"] if f.get("description", "").strip()
    )
    required_fields = sum(
        1 for t in tables for f in t["fields"] if f.get("required")
    )
    multi_record_fields = sum(
        1 for t in tables for f in t["fields"] if f.get("multiple_records")
    )

    typos = [
        {"field": "Mother Mainder Name", "correct": "Mother Maiden Name", "table": "patient_demographics"},
        {"field": "Ethnithity", "correct": "Ethnicity", "table": "patient_demographics"},
        {"field": "Chief Comlaint", "correct": "Chief Complaint", "table": "patient_encounters_clinical_billing"},
        {"field": "Historhy of Present Illness", "correct": "History of Present Illness", "table": "patient_encounters_clinical_billing"},
        {"field": "L:abs", "correct": "Labs", "table": "patient_encounters_clinical_billing"},
    ]

    return {
        "total_tables": len(tables),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "pct_fields_with_descriptions": 0,
        "required_fields": required_fields,
        "multi_record_fields": multi_record_fields,
        "fields_per_table": {t["id"]: t["field_count"] for t in tables},
        "typos_found": typos,
        "value_sets_documented": 0,
        "relationships_documented": 0,
        "sample_data_provided": False,
    }


def main():
    text = extract_text()
    tables = parse_tables(text)
    summary = compute_summary(tables)

    inventory = {
        "source": "Aarista_EHI_Export.pdf",
        "source_type": "PDF data dictionary",
        "created_date": "2023-11-28",
        "author": "Michael Mai",
        "summary": summary,
        "entities": tables,
    }

    out_path = f"{OUT_DIR}/full-entity-inventory.json"
    with open(out_path, 'w') as f:
        json.dump(inventory, f, indent=2)

    # Print summary
    print(f"Tables parsed: {summary['total_tables']}")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Fields with descriptions: {summary['fields_with_descriptions']}")
    print(f"Required fields: {summary['required_fields']}")
    print(f"Multi-record fields: {summary['multi_record_fields']}")
    print()
    for t in tables:
        print(f"  {t['id']}: {t['field_count']} fields ({t['scope']})")

    print(f"\nOutput: {out_path}")


if __name__ == "__main__":
    main()
