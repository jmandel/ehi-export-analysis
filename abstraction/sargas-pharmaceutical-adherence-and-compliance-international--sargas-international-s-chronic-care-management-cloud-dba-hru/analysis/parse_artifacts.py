#!/usr/bin/env python3
"""
Parse and inventory all EHI export artifacts for Sargas/hru2day.
Extracts full text from the PDF, verifies artifact metadata, and produces
a structured JSON inventory of everything available.
"""

import json
import os
import subprocess

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/sargas-pharmaceutical-adherence-and-compliance-international--sargas-international-s-chronic-care-management-cloud-dba-hru"
DOWNLOADS_DIR = os.path.join(RESULTS_DIR, "downloads")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def get_pdf_info(pdf_path):
    """Get PDF metadata using pdfinfo."""
    result = subprocess.run(
        ["pdfinfo", pdf_path],
        capture_output=True, text=True
    )
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            info[key.strip()] = val.strip()
    return info

def analyze_artifacts():
    """Analyze all downloaded artifacts."""
    artifacts = []

    # 1. SPAC-Export.pdf - the primary EHI export documentation
    pdf_path = os.path.join(DOWNLOADS_DIR, "SPAC-Export.pdf")
    if os.path.exists(pdf_path):
        pdf_info = get_pdf_info(pdf_path)
        pdf_text = extract_pdf_text(pdf_path)
        
        # Count sentences (rough)
        sentences = [s.strip() for s in pdf_text.replace("\n", " ").split(".") if s.strip() and len(s.strip()) > 5]
        
        # Count words
        words = pdf_text.split()
        
        artifacts.append({
            "file": "SPAC-Export.pdf",
            "type": "PDF",
            "description": "Primary EHI export documentation",
            "size_bytes": os.path.getsize(pdf_path),
            "pages": int(pdf_info.get("Pages", 0)),
            "title": pdf_info.get("Title", ""),
            "created": pdf_info.get("CreationDate", ""),
            "modified": pdf_info.get("ModDate", ""),
            "word_count": len(words),
            "approximate_sentences": len(sentences),
            "full_text": pdf_text,
            "contains_data_dictionary": False,
            "contains_field_definitions": False,
            "contains_sample_data": False,
            "contains_schema": False,
            "export_format_described": "ZIP containing C-CDA XML documents and PDF attachments",
            "informative_rating": "minimal"
        })

    # 2. Screenshot of certification page
    screenshot_path = os.path.join(DOWNLOADS_DIR, "screenshot-certification-page.png")
    if os.path.exists(screenshot_path):
        artifacts.append({
            "file": "screenshot-certification-page.png",
            "type": "PNG screenshot",
            "description": "Screenshot of vendor's certified EHR technology page",
            "size_bytes": os.path.getsize(screenshot_path),
            "contains_data_dictionary": False,
            "contains_field_definitions": False,
            "contains_sample_data": False,
            "contains_schema": False,
            "informative_rating": "not_informative"
        })

    return artifacts

def build_inventory():
    """Build full entity inventory. Since there is no data dictionary,
    the inventory reflects what can be inferred from the documentation."""
    
    # The only export format described is C-CDA per encounter + PDF attachments
    # No entity/table/field inventory is possible from this documentation
    inventory = {
        "source": "SPAC-Export.pdf",
        "source_type": "PDF documentation (1 page, 6 sentences)",
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_sample_data": False,
        "has_schema": False,
        "export_format": {
            "container": "ZIP archive",
            "contents": [
                {
                    "type": "C-CDA XML",
                    "description": "Clinical Document Architecture documents, one per encounter",
                    "nested_in": "ZIP archives within the outer ZIP"
                },
                {
                    "type": "PDF",
                    "description": "PDF files attached to the patient's chart (machine readable PDF)",
                    "nested_in": "outer ZIP"
                }
            ]
        },
        "entities": [],
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "note": "No data dictionary or field-level documentation exists. The vendor provides only a high-level description of the export format (ZIP with C-CDAs and PDFs). No entities, tables, or fields are enumerable from the available documentation."
    }
    
    return inventory

def main():
    artifacts = analyze_artifacts()
    inventory = build_inventory()
    
    # Save artifacts analysis
    artifacts_path = os.path.join(OUTPUT_DIR, "artifacts-analysis.json")
    with open(artifacts_path, "w") as f:
        json.dump(artifacts, f, indent=2)
    print(f"Artifacts analysis saved to {artifacts_path}")
    print(f"  Total artifacts: {len(artifacts)}")
    for a in artifacts:
        print(f"  - {a['file']}: {a['description']} ({a['informative_rating']})")
    
    # Save full entity inventory
    inventory_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(inventory_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nFull entity inventory saved to {inventory_path}")
    print(f"  Has data dictionary: {inventory['has_data_dictionary']}")
    print(f"  Total entities: {inventory['total_entities']}")
    print(f"  Total fields: {inventory['total_fields']}")
    
    # Summary stats
    stats = {
        "artifact_count": len(artifacts),
        "primary_artifact": "SPAC-Export.pdf",
        "primary_artifact_pages": 1,
        "primary_artifact_words": artifacts[0]["word_count"] if artifacts else 0,
        "data_dictionary_present": False,
        "field_definitions_present": False,
        "sample_data_present": False,
        "schema_present": False,
        "total_entities_documented": 0,
        "total_fields_documented": 0,
        "export_format": "ZIP (C-CDA XML + PDF)",
        "export_model_type": "standard_projection",
        "classification": "minimal_stub"
    }
    
    stats_path = os.path.join(OUTPUT_DIR, "summary-stats.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"\nSummary stats saved to {stats_path}")

if __name__ == "__main__":
    main()
