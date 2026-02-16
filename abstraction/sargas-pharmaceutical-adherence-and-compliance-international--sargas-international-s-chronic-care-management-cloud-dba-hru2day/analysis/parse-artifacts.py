#!/usr/bin/env python3
"""
Parse all artifacts from the Sargas/hru2day EHI export documentation.

The entire EHI export documentation is a single 1-page PDF (SPAC-Export.pdf)
containing 6 sentences. There is no data dictionary, no schema, no sample data.

This script extracts what little structured information exists and produces
a JSON inventory for downstream analysis.
"""

import json
import subprocess
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/sargas-pharmaceutical-adherence-and-compliance-international--sargas-international-s-chronic-care-management-cloud-dba-hru2day"
ANALYSIS_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def extract_pdf_info(pdf_path):
    """Extract metadata from PDF using pdfinfo."""
    result = subprocess.run(
        ["pdfinfo", pdf_path],
        capture_output=True, text=True
    )
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            info[key.strip()] = value.strip()
    return info

def main():
    downloads_dir = os.path.join(RESULTS_DIR, "downloads")

    # Parse the main EHI export PDF
    pdf_path = os.path.join(downloads_dir, "SPAC-Export.pdf")
    pdf_text = extract_pdf_text(pdf_path)
    pdf_info = extract_pdf_info(pdf_path)

    # Parse the sentences from the PDF
    sentences = [s.strip() for s in pdf_text.split("\n") if s.strip()]

    artifact_analysis = {
        "vendor": "Sargas Pharmaceutical Adherence and Compliance International",
        "product": "Sargas International's Chronic Care Management Cloud dba hru2day",
        "chpl_id": 10702,
        "analysis_date": "2026-02-16",
        "artifacts": [
            {
                "file": "SPAC-Export.pdf",
                "type": "EHI export documentation",
                "source_url": "https://www.spacinternational.com/SPAC-Export.pdf",
                "access_status": "accessible (HTTP 200)",
                "size_bytes": os.path.getsize(pdf_path),
                "pages": int(pdf_info.get("Pages", 0)),
                "created": pdf_info.get("CreationDate", ""),
                "modified": pdf_info.get("ModDate", ""),
                "producer": pdf_info.get("Producer", ""),
                "title": pdf_info.get("Title", ""),
                "full_text": pdf_text,
                "sentence_count": len(sentences),
                "sentences": sentences,
                "contains_data_dictionary": False,
                "contains_field_definitions": False,
                "contains_sample_data": False,
                "contains_schema": False,
                "contains_export_instructions": False,
            },
            {
                "file": "screenshot-certification-page.png",
                "type": "Screenshot of vendor certification page",
                "source_url": "https://www.spacinternational.com/certified-ehr-technology.php",
                "size_bytes": os.path.getsize(os.path.join(downloads_dir, "screenshot-certification-page.png")),
                "contains_data_dictionary": False,
                "contains_field_definitions": False,
                "contains_export_instructions": False,
                "note": "Certification boilerplate only; no additional EHI export documentation."
            }
        ],
        "export_description": {
            "format": "ZIP archive",
            "contents": [
                "C-CDA XML documents (one per patient encounter, in nested ZIP archives)",
                "PDF files attached to the patient's chart"
            ],
            "standard": "C-CDA (Consolidated Clinical Document Architecture)",
            "granularity": "per-encounter",
            "documented_ccda_sections": [],
            "documented_fields": 0,
            "documented_entities": 0,
            "sample_data_provided": False,
            "export_mechanism_described": False,
            "bulk_export_described": False
        },
        "documentation_quality": {
            "total_pages": 1,
            "total_sentences": len(sentences),
            "has_data_dictionary": False,
            "has_field_definitions": False,
            "has_type_definitions": False,
            "has_value_sets": False,
            "has_relationships": False,
            "has_sample_data": False,
            "has_schema": False,
            "has_export_instructions": False,
            "has_api_documentation": False,
            "informational_sentences": len([s for s in sentences if s not in [
                "ZIP is an archive file format.",
                "PDF or Portable Document Format is a file format that is used to present text or image based documents.",
                "C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange."
            ]]),
            "filler_sentences": 3,
            "filler_sentence_note": "3 of the 7 lines are generic definitions of ZIP, PDF, and C-CDA formats"
        },
        "additional_searches": {
            "open_pdf_directory": {
                "url": "https://www.spacinternational.com/pdf/",
                "total_pdfs_found": 109,
                "ehi_export_related": 0,
                "note": "All 109 PDFs are CCM/RPM brochures, consent forms, white papers, billing guides, Real World Testing plans, and disclosure documents. None contain additional EHI export documentation."
            },
            "probed_paths": {
                "/ehi": 404,
                "/ehi-export": 404,
                "/api": 404,
                "/fhir": 404,
                "/interoperability": 404,
                "/data-export": 404,
                "/documentation": 404
            },
            "disclosure_pdf_checked": {
                "file": "ONC-HIT-CERTIFICATE-DISCLOSURE_ver_21_9_Revised-25.pdf",
                "contains_ehi_export_detail": False,
                "note": "Lists certified criteria and pricing. No additional EHI export technical detail."
            }
        }
    }

    # Since there's no data dictionary, the "full entity inventory" is empty
    full_entity_inventory = {
        "vendor": artifact_analysis["vendor"],
        "product": artifact_analysis["product"],
        "extraction_date": "2026-02-16",
        "source_artifact": "SPAC-Export.pdf",
        "note": "No data dictionary, schema, or field-level documentation exists. The entire EHI export documentation is 7 lines of text describing the export as a ZIP of C-CDAs and PDFs. No entities, tables, or fields are documented.",
        "entities": [],
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "ccda_sections_documented": [],
        "export_format": "ZIP containing C-CDA XML (per encounter) + PDF attachments"
    }

    # Write outputs
    with open(os.path.join(ANALYSIS_DIR, "artifact-analysis.json"), "w") as f:
        json.dump(artifact_analysis, f, indent=2)
    print(f"Wrote artifact-analysis.json")

    with open(os.path.join(ANALYSIS_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(full_entity_inventory, f, indent=2)
    print(f"Wrote full-entity-inventory.json")

    # Print summary
    print(f"\n=== Artifact Analysis Summary ===")
    print(f"Artifacts examined: {len(artifact_analysis['artifacts'])}")
    print(f"Total documentation pages: {artifact_analysis['documentation_quality']['total_pages']}")
    print(f"Total sentences: {artifact_analysis['documentation_quality']['total_sentences']}")
    print(f"Informational sentences: {artifact_analysis['documentation_quality']['informational_sentences']}")
    print(f"Filler sentences (generic format definitions): {artifact_analysis['documentation_quality']['filler_sentences']}")
    print(f"Data dictionary: {'Yes' if artifact_analysis['documentation_quality']['has_data_dictionary'] else 'No'}")
    print(f"Field definitions: {'Yes' if artifact_analysis['documentation_quality']['has_field_definitions'] else 'No'}")
    print(f"Sample data: {'Yes' if artifact_analysis['documentation_quality']['has_sample_data'] else 'No'}")
    print(f"Schema: {'Yes' if artifact_analysis['documentation_quality']['has_schema'] else 'No'}")
    print(f"Export format: {artifact_analysis['export_description']['format']}")
    print(f"Standard: {artifact_analysis['export_description']['standard']}")
    print(f"Documented entities: {artifact_analysis['export_description']['documented_entities']}")
    print(f"Documented fields: {artifact_analysis['export_description']['documented_fields']}")
    print(f"Additional PDFs on vendor site: {artifact_analysis['additional_searches']['open_pdf_directory']['total_pdfs_found']}")
    print(f"EHI-related PDFs found: {artifact_analysis['additional_searches']['open_pdf_directory']['ehi_export_related']}")

if __name__ == "__main__":
    main()
