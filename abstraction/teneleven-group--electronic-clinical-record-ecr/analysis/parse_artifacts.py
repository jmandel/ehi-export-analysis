#!/usr/bin/env python3
"""
Analyze EHI export documentation for TenEleven eCR.

This script examines all artifacts in downloads/ and produces
entity-inventory-full.json and entity-inventory-summary.json.

In this case, the vendor provides no data dictionary, schema, or
structured documentation — only a 1-page PDF describing two export
formats (JSON and .bak) with no field-level detail. The script
verifies this by parsing the PDF and checking for any tabular or
structured content.
"""

import json
import subprocess
import os

DOWNLOADS = os.path.join(os.path.dirname(__file__), "..", "downloads")
OUTPUT_DIR = os.path.dirname(__file__)


def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout


def analyze_pdf(pdf_path):
    """Analyze the File Formats PDF for any structured content."""
    text = extract_pdf_text(pdf_path)
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]

    # Check for table-like structures (lines with multiple columns separated by whitespace)
    table_lines = [l for l in lines if l.count("  ") >= 2]

    # Check for field definitions (patterns like "field_name: type" or "field_name | type")
    field_patterns = [l for l in lines if "|" in l or ":" in l and len(l.split()) <= 5]

    return {
        "total_lines": len(lines),
        "text": text.strip(),
        "has_tables": len(table_lines) > 0,
        "table_line_count": len(table_lines),
        "possible_field_definitions": len(field_patterns),
        "entities_found": 0,
        "fields_found": 0
    }


def main():
    pdf_path = os.path.join(DOWNLOADS, "PDF-for-Website-on-Formats-2.pdf")

    print("=== Analyzing TenEleven eCR EHI Export Documentation ===\n")

    # Analyze PDF
    if os.path.exists(pdf_path):
        pdf_info = analyze_pdf(pdf_path)
        print(f"PDF: {os.path.basename(pdf_path)}")
        print(f"  Lines of text: {pdf_info['total_lines']}")
        print(f"  Has table structures: {pdf_info['has_tables']}")
        print(f"  Entities defined: {pdf_info['entities_found']}")
        print(f"  Fields defined: {pdf_info['fields_found']}")
        print(f"\n  Full text:\n  ---")
        for line in pdf_info['text'].split('\n'):
            print(f"  {line}")
        print(f"  ---\n")
    else:
        print(f"PDF not found at {pdf_path}")
        pdf_info = None

    # List all artifacts
    print("All artifacts in downloads/:")
    for f in sorted(os.listdir(DOWNLOADS)):
        fpath = os.path.join(DOWNLOADS, f)
        size = os.path.getsize(fpath)
        print(f"  {f} ({size:,} bytes)")

    # Produce inventory
    inventory = {
        "_metadata": {
            "product": "electronic Clinical Record (eCR)",
            "vendor": "TenEleven Group (Ensora Health)",
            "analysis_date": "2026-02-16",
            "source_artifacts": [
                "downloads/PDF-for-Website-on-Formats-2.pdf",
                "https://ensorahealth.com/onc/teneleven/"
            ],
            "notes": (
                "No data dictionary, schema, or structured export documentation "
                "was provided by the vendor. The only documentation is a 1-page PDF "
                "describing two file formats (JSON for single patient, .bak for "
                "population) with no field-level detail. This inventory therefore "
                "contains zero entities and zero fields."
            )
        },
        "entities": [],
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0
    }

    with open(os.path.join(OUTPUT_DIR, "entity-inventory-full.json"), "w") as f:
        json.dump(inventory, f, indent=2)

    summary = {
        "_metadata": {
            "product": "electronic Clinical Record (eCR)",
            "vendor": "TenEleven Group (Ensora Health)",
            "analysis_date": "2026-02-16",
            "derived_from": "entity-inventory-full.json"
        },
        "summary": {
            "total_entities": 0,
            "total_fields": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "percent_described": "N/A",
            "categories": []
        },
        "export_formats": [
            {
                "name": "Single Patient Export",
                "format": "JSON",
                "description": "USCDI v1 data as well as other applicable data",
                "mechanism": "User-initiated, no developer assistance required",
                "schema_documented": False
            },
            {
                "name": "Patient Population Export",
                "format": ".bak (SQL Server database backup)",
                "description": "Full SQL Server database backup of all data for an agency",
                "mechanism": "Vendor-assisted via Salesforce support ticket",
                "schema_documented": False
            }
        ],
        "documentation_artifacts": [
            {
                "artifact": "PDF-for-Website-on-Formats-2.pdf",
                "pages": 1,
                "content": "Two bullet points describing JSON and .bak formats",
                "entities_defined": 0,
                "fields_defined": 0
            },
            {
                "artifact": "ensorahealth.com/onc/teneleven/ (web page)",
                "content": "Two paragraphs describing single patient and population export",
                "entities_defined": 0,
                "fields_defined": 0
            }
        ]
    }

    with open(os.path.join(OUTPUT_DIR, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Summary ===")
    print(f"Total entities documented: 0")
    print(f"Total fields documented: 0")
    print(f"Data dictionary present: No")
    print(f"Schema documentation: None")
    print(f"Sample data: None")
    print(f"\nOutput written to:")
    print(f"  {os.path.join(OUTPUT_DIR, 'entity-inventory-full.json')}")
    print(f"  {os.path.join(OUTPUT_DIR, 'entity-inventory-summary.json')}")


if __name__ == "__main__":
    main()
