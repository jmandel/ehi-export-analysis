#!/usr/bin/env python3
"""
Parse the MedConnectHealth EHI Export Documentation PDF and HTML page.
Extracts all structured information available (which is minimal).
Outputs full-entity-inventory.json and artifact-summary.json.
"""

import json
import subprocess
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/medconnect-inc--medconnecthealth"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/medconnect-inc--medconnecthealth/analysis"

def get_pdf_info(pdf_path):
    """Extract PDF metadata using pdfinfo."""
    result = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True)
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            info[key.strip()] = value.strip()
    return info

def get_pdf_text(pdf_path):
    """Extract PDF text using pdftotext."""
    result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
    return result.stdout

def analyze_html_page(html_path):
    """Analyze the EHI export HTML page for substantive content."""
    with open(html_path, "r") as f:
        content = f.read()
    
    # Count PDF links
    import re
    pdf_links = re.findall(r'href="([^"]*\.pdf[^"]*)"', content, re.IGNORECASE)
    
    return {
        "file": os.path.basename(html_path),
        "size_bytes": os.path.getsize(html_path),
        "pdf_links_found": pdf_links,
        "substantive_content": "Single link to EHI_Export_Documentation.pdf; no additional EHI content",
        "page_published": "2023-11-09",
        "page_modified": "2023-11-09"
    }

def build_export_format_inventory():
    """
    Build the entity inventory from the PDF documentation.
    Since there's no data dictionary, we document the export components as described.
    """
    # The PDF describes exactly 4 export components in a ZIP
    export_components = [
        {
            "entity_name": "C-CDA (USCDI v1)",
            "format": "XML",
            "description": "C-CDA document in compliance with USCDI v1",
            "fields": "Not specified - standard C-CDA sections (problems, medications, allergies, immunizations, vitals, lab results, procedures, health concerns, goals, assessments, care teams, clinical notes)",
            "field_count": None,
            "field_descriptions": False,
            "types_documented": False,
            "relationships_documented": False,
            "value_sets_documented": False,
            "category": "Clinical Data",
            "computable": True,
            "notes": "USCDI v1 is a defined standard; the vendor does not document any extensions or customizations beyond the standard"
        },
        {
            "entity_name": "Demographics",
            "format": "PDF",
            "description": "Patient demographics exported as PDF",
            "fields": "Not specified",
            "field_count": None,
            "field_descriptions": False,
            "types_documented": False,
            "relationships_documented": False,
            "value_sets_documented": False,
            "category": "Demographics",
            "computable": False,
            "notes": "PDF format is not computable; contents and layout are undocumented"
        },
        {
            "entity_name": "Scanned Documents",
            "format": "PDF, JPG, PNG",
            "description": "Scanned documents in original formats",
            "fields": "Not specified",
            "field_count": None,
            "field_descriptions": False,
            "types_documented": False,
            "relationships_documented": False,
            "value_sets_documented": False,
            "category": "Documents",
            "computable": False,
            "notes": "Original scanned document files; no metadata schema documented"
        },
        {
            "entity_name": "Clinical Notes/Lab Results",
            "format": "PDF",
            "description": "Clinical notes and lab results exported as PDF",
            "fields": "Not specified",
            "field_count": None,
            "field_descriptions": False,
            "types_documented": False,
            "relationships_documented": False,
            "value_sets_documented": False,
            "category": "Clinical Data",
            "computable": False,
            "notes": "PDF format is not computable; unclear if this duplicates or supplements C-CDA content"
        }
    ]
    return export_components

def main():
    pdf_path = os.path.join(RESULTS_DIR, "downloads", "EHI_Export_Documentation.pdf")
    html_path = os.path.join(RESULTS_DIR, "downloads", "ehi-export-page.html")
    screenshot_path = os.path.join(RESULTS_DIR, "downloads", "ehi-export-page-screenshot.png")
    
    # Analyze artifacts
    pdf_info = get_pdf_info(pdf_path)
    pdf_text = get_pdf_text(pdf_path)
    html_analysis = analyze_html_page(html_path)
    
    # Build entity inventory
    export_components = build_export_format_inventory()
    
    # Full entity inventory
    inventory = {
        "vendor": "MedConnect, Inc.",
        "product": "MedConnectHealth 3.0",
        "chpl_id": 9183,
        "documentation_source": "EHI_Export_Documentation.pdf (1 page, 334,660 bytes)",
        "documentation_date": "2023-11-09",
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "export_format": "ZIP containing per-patient folders",
        "export_components": export_components,
        "total_entities": len(export_components),
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "No field-level documentation exists. The documentation describes only the top-level folder structure (4 components). No data dictionary, schema, sample data, or field definitions are provided."
    }
    
    # Save full entity inventory
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved full-entity-inventory.json")
    
    # Artifact summary
    artifact_summary = {
        "artifacts_reviewed": [
            {
                "file": "EHI_Export_Documentation.pdf",
                "type": "PDF",
                "size_bytes": os.path.getsize(pdf_path),
                "pages": int(pdf_info.get("Pages", 0)),
                "author": pdf_info.get("Author", ""),
                "created": pdf_info.get("CreationDate", ""),
                "description": "Single-page PDF describing EHI export compliance and format",
                "informativeness": "Primary source but minimal content",
                "content_summary": {
                    "sections": [
                        "Compliance statement (restates 170.315(b)(10) requirements)",
                        "Export format description (4-bullet folder structure)"
                    ],
                    "data_dictionary": False,
                    "schema": False,
                    "sample_data": False,
                    "field_level_docs": False,
                    "export_instructions": False,
                    "value_set_docs": False
                }
            },
            {
                "file": "ehi-export-page.html",
                "type": "HTML",
                "size_bytes": os.path.getsize(html_path),
                "description": "WordPress page with heading and single PDF link",
                "informativeness": "Minimal - just a container for the PDF link",
                "content_summary": {
                    "substantive_ehi_content": False,
                    "pdf_links": html_analysis["pdf_links_found"]
                }
            },
            {
                "file": "ehi-export-page-screenshot.png",
                "type": "PNG",
                "size_bytes": os.path.getsize(screenshot_path),
                "description": "Browser screenshot confirming page layout",
                "informativeness": "Corroborative only"
            }
        ],
        "pdf_full_text": pdf_text,
        "pdf_metadata": pdf_info,
        "html_analysis": html_analysis
    }
    
    with open(os.path.join(OUTPUT_DIR, "artifact-summary.json"), "w") as f:
        json.dump(artifact_summary, f, indent=2)
    print(f"Saved artifact-summary.json")
    
    # Print summary stats
    print(f"\n=== Summary ===")
    print(f"Artifacts reviewed: {len(artifact_summary['artifacts_reviewed'])}")
    print(f"PDF pages: {pdf_info.get('Pages', 'unknown')}")
    print(f"Export components described: {len(export_components)}")
    print(f"Has data dictionary: No")
    print(f"Has schema: No")
    print(f"Has sample data: No")
    print(f"Total fields documented: 0")
    print(f"Computable components: 1 of {len(export_components)} (C-CDA XML only)")

if __name__ == "__main__":
    main()
