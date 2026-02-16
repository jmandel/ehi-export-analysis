#!/usr/bin/env python3
"""
Parses the Simplify EMR EHI export documentation (a plain text file)
and produces the entity inventory JSON files.

The documentation is extremely minimal — 831 bytes describing only
folder structure and file naming conventions, with no data dictionary
or field definitions. This script extracts what little structure exists.
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(SCRIPT_DIR, "..", "downloads")

def main():
    # Read the source document
    txt_path = os.path.join(DOWNLOADS_DIR, "ehi-export-doc.txt")
    with open(txt_path, "r") as f:
        content = f.read()

    print(f"Source file: {txt_path}")
    print(f"Source size: {len(content)} bytes")
    print(f"Source lines: {len(content.splitlines())}")
    print()

    # The document describes 3 export components
    entities = []

    # 1. C-CDA XML file
    entities.append({
        "name": "C-CDA XML File",
        "vendor_description": "CCDA File Conformant to USCDI v1",
        "format": "XML (C-CDA)",
        "naming_convention": "Lastname_FirstName_ccda.xml",
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "No field-level documentation. References USCDI v1 errata for specs."
    })

    # 2. Encounter notes
    entities.append({
        "name": "Encounter Notes",
        "vendor_description": "All Visit Notes in PDF or HTML Format (0 to many)",
        "format": "PDF or HTML",
        "naming_convention": "{encounterId}_{date}.pdf or .html",
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "Unstructured documents. No content documentation."
    })

    # 3. Patient documents
    entities.append({
        "name": "Patient Documents",
        "vendor_description": "Other Documents in PDF Format or HTML Format (0 to many)",
        "format": "PDF or HTML",
        "naming_convention": "{documentId}_{date}.pdf or .html",
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "Unstructured documents. No content documentation."
    })

    # Summary stats
    total_entities = len(entities)
    total_fields = sum(e["field_count"] for e in entities)
    total_described = sum(e["fields_with_descriptions"] for e in entities)

    print(f"Total export components: {total_entities}")
    print(f"Total documented fields: {total_fields}")
    print(f"Fields with descriptions: {total_described}")
    print()
    print("Components:")
    for e in entities:
        print(f"  - {e['name']}: {e['format']} ({e['vendor_description']})")

    print()
    print("Assessment: No data dictionary exists. Documentation describes only")
    print("folder structure and file naming conventions (831 bytes of text).")
    print("The C-CDA content is entirely unspecified beyond claiming USCDI v1 conformance.")

if __name__ == "__main__":
    main()
