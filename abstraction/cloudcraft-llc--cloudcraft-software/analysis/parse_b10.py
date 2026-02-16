#!/usr/bin/env python3
"""
Parse the B10.html EHI export documentation page from CloudCraft Software.
Extracts all structured content into JSON for downstream analysis.
"""

import json
import re
import html
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/cloudcraft-llc--cloudcraft-software/downloads"
OUTPUT_DIR = os.path.dirname(__file__)

def parse_b10():
    with open(os.path.join(DOWNLOADS, "B10.html"), "r") as f:
        content = f.read()

    # Extract sections
    result = {
        "source_file": "B10.html",
        "source_url": "https://cloudcraftsoftware.com/certification/B10.html",
        "file_size_bytes": len(content.encode("utf-8")),
        "last_modified": "2023-12-14T09:56:10Z",
        "page_title": "Cloudcraft",
        "heading": "CloudCraft 170.315 (b)(10) EHI Export",
        "sections": [],
        "artifacts_referenced": [],
        "data_dictionary": None,
        "schema_files": None,
        "sample_data": None,
        "api_documentation": None,
    }

    # Provider Export section
    provider_section = {
        "title": "Provider Export",
        "description": "CloudCraft supports secure, one-time bulk export of all primary care provider patient data, including meme document types for PDF, TIF, PNG, and WORD.",
        "description_note": "Contains typo: 'meme' should be 'MIME'",
        "workflow_steps": [
            {"step": 1, "label": "Patient(s) submit requests", "icon": "img1.gif"},
            {"step": 2, "label": "Access Bulk Download From Admin Console", "icon": "img2.png"},
            {"step": 3, "label": "Select Patients requesting Primary care provider Access", "icon": "img3.gif"},
            {"step": 4, "label": "User selects secure Download location", "icon": "img4.gif"},
            {"step": 5, "label": "User give provider Secure access.", "icon": "img5.gif"},
        ],
        "bulk_data_types": [
            "C-CDA USCDI v3.",
            "PDF documents, including scanned paper and digital records of faxes.",
            "Image files (JPEG, GIF, TIF)",
            "Word documents",
            "Internal correspondence such as tasks, notes",
        ],
    }

    # Patient Export Requests section
    patient_section = {
        "title": "Patient Export Requests",
        "description": "CloudCraft FHIR supports the FHIR R4 DocumentReference resource. This resource can be used with any document format with a recognized mime type.",
        "fhir_app_connections": "MyLinks, Apple Health, etc.",
        "bulk_data_types": [
            "C-CDA USCDI v3.",
            "PDF documents, including scanned paper and digital records of faxes.",
            "Image files (JPEG, GIF, TIF)",
            "Word documents",
            "Internal correspondence such as tasks, notes",
        ],
    }

    result["sections"] = [provider_section, patient_section]

    # List all artifacts
    artifacts = []
    for root, dirs, files in os.walk(DOWNLOADS):
        for fname in files:
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, DOWNLOADS)
            artifacts.append({
                "filename": rel,
                "size_bytes": os.path.getsize(fpath),
                "type": os.path.splitext(fname)[1].lower(),
            })
    result["artifacts_referenced"] = sorted(artifacts, key=lambda x: x["filename"])

    # Compute word count of visible prose
    text = content
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<svg[^>]*>.*?</svg>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    words = text.split()
    result["visible_word_count"] = len(words)

    return result


def generate_entity_inventory():
    """
    Generate full-entity-inventory.json.
    Since CloudCraft provides NO data dictionary, schema, or field-level documentation,
    the inventory reflects only what can be inferred from the high-level bullet list.
    """
    inventory = {
        "vendor": "CloudCraft, LLC",
        "product": "CloudCraft Software",
        "version": "9.0",
        "source": "B10.html - inferred from 5 bullet items (no data dictionary provided)",
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "note": "CloudCraft provides NO entity/table/field-level documentation. "
                "The export is described only as 5 categories of bulk data types. "
                "No structured data dictionary exists to parse.",
        "inferred_data_categories": [
            {
                "category": "C-CDA USCDI v3",
                "description": "Structured clinical summary document conforming to C-CDA USCDI v3 standard",
                "format": "C-CDA XML",
                "is_standard": True,
                "standard_name": "C-CDA (HL7 Consolidated Clinical Document Architecture)",
                "uscdi_version": "v3",
                "estimated_clinical_domains": [
                    "Patient Demographics",
                    "Problems/Conditions",
                    "Medications",
                    "Allergies and Intolerances",
                    "Lab Results",
                    "Vital Signs",
                    "Immunizations",
                    "Procedures",
                    "Clinical Notes",
                    "Care Plans/Goals",
                    "Implantable Devices",
                    "Family Health History",
                    "Health Concerns",
                    "Assessment and Plan",
                ],
                "note": "These are standard USCDI v3 data classes; actual CloudCraft implementation may vary"
            },
            {
                "category": "PDF documents",
                "description": "PDF documents, including scanned paper and digital records of faxes",
                "format": "PDF",
                "is_standard": False,
                "entities": 0,
                "fields": 0,
            },
            {
                "category": "Image files",
                "description": "Image files (JPEG, GIF, TIF)",
                "format": "JPEG, GIF, TIF",
                "is_standard": False,
                "entities": 0,
                "fields": 0,
            },
            {
                "category": "Word documents",
                "description": "Word documents",
                "format": "DOC/DOCX",
                "is_standard": False,
                "entities": 0,
                "fields": 0,
            },
            {
                "category": "Internal correspondence",
                "description": "Internal correspondence such as tasks, notes",
                "format": "Unknown",
                "is_standard": False,
                "entities": 0,
                "fields": 0,
                "note": "No detail on structure or format of internal correspondence export"
            },
        ],
    }
    return inventory


def main():
    parsed = parse_b10()
    inventory = generate_entity_inventory()

    # Summary stats
    stats = {
        "total_artifacts_downloaded": len(parsed["artifacts_referenced"]),
        "substantive_artifacts": 1,  # Only B10.html has content
        "supporting_artifacts": len(parsed["artifacts_referenced"]) - 1,  # images, CSS, screenshots
        "data_dictionary_present": False,
        "schema_present": False,
        "sample_data_present": False,
        "api_documentation_present": False,
        "visible_prose_word_count": parsed["visible_word_count"],
        "bulk_data_categories_listed": 5,
        "workflow_steps": 5,
        "export_sections": 2,
        "total_entities_documented": 0,
        "total_fields_documented": 0,
    }

    with open(os.path.join(OUTPUT_DIR, "parsed-b10.json"), "w") as f:
        json.dump(parsed, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "summary-stats.json"), "w") as f:
        json.dump(stats, f, indent=2)

    print("=== Summary Stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print("\n=== Parsed Sections ===")
    for s in parsed["sections"]:
        print(f"  Section: {s['title']}")
        print(f"    Bulk data types: {len(s['bulk_data_types'])}")

    print("\n=== Artifacts ===")
    for a in parsed["artifacts_referenced"]:
        print(f"  {a['filename']} ({a['size_bytes']} bytes)")

    print("\nOutput files written:")
    print(f"  {os.path.join(OUTPUT_DIR, 'parsed-b10.json')}")
    print(f"  {os.path.join(OUTPUT_DIR, 'full-entity-inventory.json')}")
    print(f"  {os.path.join(OUTPUT_DIR, 'summary-stats.json')}")


if __name__ == "__main__":
    main()
