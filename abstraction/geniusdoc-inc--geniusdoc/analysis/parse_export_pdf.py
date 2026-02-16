#!/usr/bin/env python3
"""
Parse the GeniusDoc EHI Export PDF and extract all structured information.

The PDF (GeniusDoc_Data_Export.pdf) contains only 6 high-level export categories
with one-sentence descriptions each. There is no data dictionary, no field-level
documentation, and no schema. This script extracts the category-level information
and produces the entity-inventory JSON files.
"""

import json
import subprocess
import re
import sys
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent / "downloads"
OUTPUT_DIR = Path(__file__).parent

def extract_pdf_text(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_categories(text):
    """Parse the 6 numbered categories from the PDF text."""
    categories = []
    # Pattern: number followed by category name and description
    pattern = r'(\d+)\.\s+(.+?):\s*\n\s*(.*?)(?=\n\s*\d+\.|It is crucial|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    
    for num, name, desc in matches:
        # Clean up description
        desc = ' '.join(desc.split())
        categories.append({
            "number": int(num),
            "name": name.strip(),
            "description": desc.strip()
        })
    return categories

def main():
    pdf_path = DOWNLOADS / "GeniusDoc_Data_Export.pdf"
    if not pdf_path.exists():
        print(f"ERROR: PDF not found at {pdf_path}", file=sys.stderr)
        sys.exit(1)
    
    text = extract_pdf_text(pdf_path)
    categories = parse_categories(text)
    
    print(f"Extracted {len(categories)} categories from PDF:")
    for cat in categories:
        print(f"  {cat['number']}. {cat['name']}: {cat['description'][:80]}...")
    
    # Verify we got all 6
    if len(categories) != 6:
        print(f"WARNING: Expected 6 categories, got {len(categories)}")
    
    # PDF metadata
    info_result = subprocess.run(
        ["pdfinfo", str(pdf_path)], capture_output=True, text=True
    )
    print(f"\nPDF Info:\n{info_result.stdout}")
    
    print(f"\nKey findings:")
    print(f"  - Total export categories: {len(categories)}")
    print(f"  - Total documented fields: 0 (no field-level documentation)")
    print(f"  - Data dictionary: None")
    print(f"  - Schema: None")
    print(f"  - Sample data: None")
    print(f"  - Export formats: Excel, PDF, CDA (HL7)")
    
    # Note about Problems category
    for cat in categories:
        if cat['name'] == 'Problems':
            if 'active' in cat['description'].lower():
                print(f"\n  RED FLAG: Problems category says '{cat['description']}'")
                print(f"  This excludes resolved/historical diagnoses.")

if __name__ == "__main__":
    main()
