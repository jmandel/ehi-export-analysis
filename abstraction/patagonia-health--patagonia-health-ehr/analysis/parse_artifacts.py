#!/usr/bin/env python3
"""
Parse all Patagonia Health EHI export artifacts and produce:
1. full-entity-inventory.json — what the export contains
2. artifact-summary.json — metadata about each artifact
3. Console output with summary statistics
"""

import json
import os
import re
from html.parser import HTMLParser

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/patagonia-health--patagonia-health-ehr/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/patagonia-health--patagonia-health-ehr/analysis"


class TextExtractor(HTMLParser):
    """Simple HTML-to-text extractor."""
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        self.text.append(data.strip())
    def get_text(self):
        return " ".join(t for t in self.text if t)


def parse_ehi_section():
    """Parse the EHI export section HTML and extract structured info."""
    with open(os.path.join(DOWNLOADS, "ehi-export-section.html")) as f:
        html = f.read()

    extractor = TextExtractor()
    extractor.feed(html)
    text = extractor.get_text()
    word_count = len(text.split())

    return {
        "source": "ehi-export-section.html",
        "word_count": word_count,
        "html_size_bytes": len(html),
        "clinical_format": "CCDA 2.1 Release 2 USCDI v1 (XML)",
        "billing_format": "CSV, XLSX, or PDF",
        "single_patient": True,
        "multi_patient": True,
        "access_mechanism": "Reports > Medical Practice Reports > EHI Export",
        "billing_mechanism": "Dashboard > Billing > Search > Claims (single) or Reports > Claim > Detail (multi)",
        "role_based_access": True,
        "data_dictionary": False,
        "schema_provided": False,
        "sample_data_provided": False,
        "field_level_documentation": False,
    }


def parse_ccda_api_sections():
    """Extract the CCDA sections listed in the Patient Health Data API doc."""
    sections = [
        {"api_name": "demographics", "display": "Patient Demographics"},
        {"api_name": "allergies", "display": "Allergies and Intolerances"},
        {"api_name": "assessments", "display": "Assessment"},
        {"api_name": "encounters", "display": "Encounters"},
        {"api_name": "goals", "display": "Goals"},
        {"api_name": "immunizations", "display": "Immunizations"},
        {"api_name": "medications", "display": "Medications"},
        {"api_name": "procedures", "display": "Procedures"},
        {"api_name": "results", "display": "Results"},
        {"api_name": "vitalsigns", "display": "Vital Signs"},
    ]
    return sections


def parse_fhir_resources():
    """Extract the FHIR R4 resources from the SmartOnFHIR API doc."""
    resources = [
        "Patient",
        "AllergyIntolerance",
        "CarePlan",
        "CareTeam",
        "Condition",
        "Device",
        "DiagnosticReport",
        "DocumentReference",
        "Goal",
        "Immunization",
        "Medication",
        "MedicationDispense",
        "Observation",
        "Organization",
        "Procedure",
        "Provenance",
        "ServiceRequest",
        "Coverage",
        "Specimen",
        "RelatedPerson",
    ]
    return resources


def build_full_inventory():
    """Build complete inventory of what the EHI export provides."""
    inventory = {
        "export_type": "standard_based_projection",
        "export_description": "CCDA 2.1 XML for clinical data + CSV/XLSX for billing claims",
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,

        "clinical_export": {
            "format": "CCDA 2.1 Release 2 USCDI v1 (XML)",
            "standard": "C-CDA 2.1",
            "uscdi_version": "v1",
            "mechanism": "Reports > Medical Practice Reports > EHI Export",
            "single_patient": True,
            "multi_patient": True,
            "sections": parse_ccda_api_sections(),
            "section_count": len(parse_ccda_api_sections()),
            "note": "Sections inferred from Patient Health Data API v1.1 doc — the EHI export page itself does not enumerate sections.",
        },

        "billing_export": {
            "format": "CSV, XLSX, or PDF",
            "mechanism_single": "Dashboard > Billing > Search > Claims",
            "mechanism_multi": "Dashboard > Billing > Reports > Claim > Detail",
            "single_patient": True,
            "multi_patient": True,
            "schema_documented": False,
            "fields_documented": False,
            "note": "No field definitions, schema, or sample data provided for billing exports.",
        },

        "fhir_api": {
            "note": "The (g)(10) FHIR API is listed on the same page but is a separate certification criterion, not the (b)(10) EHI export.",
            "standard": "FHIR R4",
            "resources": parse_fhir_resources(),
            "resource_count": len(parse_fhir_resources()),
            "documentation_pages": 67,
        },

        "proprietary_api": {
            "note": "Patient Health Data API v1.1 is a proprietary REST API returning CCDA XML in JSON wrappers. Predates FHIR.",
            "version": "1.1",
            "date": "April 2018",
            "documentation_pages": 7,
            "sections_available": parse_ccda_api_sections(),
        },

        "documentation_quality": {
            "ehi_documentation_word_count": 408,
            "ehi_documentation_type": "inline HTML on certification page",
            "data_dictionary": False,
            "field_level_docs": False,
            "value_set_docs": False,
            "relationship_docs": False,
            "sample_data": False,
            "machine_readable_schema": False,
        },
    }
    return inventory


def build_artifact_summary():
    """Summarize each artifact."""
    artifacts = [
        {
            "file": "ehi-export-section.html",
            "type": "HTML fragment",
            "size_bytes": 3139,
            "description": "EHI Export section extracted from ONC certification page",
            "relevance": "primary — contains all EHI export documentation",
            "content": "~408 words describing export workflow, formats, and access control",
        },
        {
            "file": "onc-certified-hit-page.html",
            "type": "HTML page",
            "size_bytes": 50851,
            "description": "Full ONC certification page (includes EHI section plus MU, API, etc.)",
            "relevance": "secondary — EHI section is a small part of this page",
        },
        {
            "file": "PatientHealth-Data-API-Documentation-v1.1.pdf",
            "type": "PDF",
            "size_bytes": 372240,
            "pages": 7,
            "description": "Proprietary REST API for patient data access, returns CCDA XML in JSON",
            "relevance": "supplementary — not the (b)(10) export, but shows available CCDA sections",
            "date": "April 2018",
        },
        {
            "file": "SmartOnFHIR-API-Documentation.pdf",
            "type": "PDF",
            "size_bytes": 860317,
            "pages": 67,
            "description": "SMART on FHIR / (g)(10) API documentation, FHIR R4",
            "relevance": "supplementary — this is the (g)(10) API, not the (b)(10) EHI export",
            "date": "February 2026",
        },
        {
            "file": "FHIRBaseURL.json",
            "type": "JSON",
            "size_bytes": 4827,
            "description": "FHIR Bundle with Endpoint and Organization resources for API discovery",
            "relevance": "minimal — FHIR endpoint configuration, not EHI export content",
        },
        {
            "file": "PatagoniaHealth-MeaningfulUse-Stage3-CostsandLimitations-May2018.pdf",
            "type": "PDF",
            "size_bytes": 119937,
            "pages": 2,
            "description": "Supplemental costs and technical limitations for MU Stage 3 capabilities",
            "relevance": "minimal — covers Direct Messaging and lab costs, not EHI export",
            "date": "May 2018",
        },
        {
            "file": "screenshot-ehi-export-section-1.png",
            "type": "Screenshot",
            "size_bytes": 255511,
            "description": "Screenshot of EHI Export section (role access and single patient export)",
            "relevance": "supplementary — visual confirmation of text content",
        },
        {
            "file": "screenshot-ehi-export-section-2.png",
            "type": "Screenshot",
            "size_bytes": 233574,
            "description": "Screenshot of EHI Export section (multi-patient export and formats)",
            "relevance": "supplementary — visual confirmation of text content",
        },
        {
            "file": "screenshot-ehi-export-section-3.png",
            "type": "Screenshot",
            "size_bytes": 264974,
            "description": "Screenshot of bottom of page (FHIR API links and footer)",
            "relevance": "minimal",
        },
        {
            "file": "screenshot-main-page-top.png",
            "type": "Screenshot",
            "size_bytes": 851061,
            "description": "Screenshot of top of ONC certification page",
            "relevance": "minimal",
        },
    ]
    return artifacts


def main():
    ehi_info = parse_ehi_section()
    inventory = build_full_inventory()
    artifacts = build_artifact_summary()

    # Save outputs
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "artifact-summary.json"), "w") as f:
        json.dump(artifacts, f, indent=2)

    # Print summary
    print("=== EHI Export Analysis: Patagonia Health EHR ===\n")
    print(f"EHI documentation: {ehi_info['word_count']} words, {ehi_info['html_size_bytes']} bytes HTML")
    print(f"Clinical format: {ehi_info['clinical_format']}")
    print(f"Billing format: {ehi_info['billing_format']}")
    print(f"Data dictionary: {'Yes' if ehi_info['data_dictionary'] else 'No'}")
    print(f"Schema provided: {'Yes' if ehi_info['schema_provided'] else 'No'}")
    print(f"Sample data: {'Yes' if ehi_info['sample_data_provided'] else 'No'}")
    print(f"Field-level docs: {'Yes' if ehi_info['field_level_documentation'] else 'No'}")
    print()
    print(f"CCDA sections (from API doc): {inventory['clinical_export']['section_count']}")
    for s in inventory['clinical_export']['sections']:
        print(f"  - {s['api_name']}: {s['display']}")
    print()
    print(f"FHIR resources (g)(10) API: {inventory['fhir_api']['resource_count']}")
    for r in inventory['fhir_api']['resources']:
        print(f"  - {r}")
    print()
    print(f"Total artifacts: {len(artifacts)}")
    total_bytes = sum(a['size_bytes'] for a in artifacts)
    print(f"Total artifact size: {total_bytes:,} bytes ({total_bytes/1024:.0f} KB)")
    print()
    print("Entities/tables documented: 0 (no data dictionary)")
    print("Fields documented: 0 (no field-level documentation)")
    print("Native database model: Not exposed")
    print()
    print(f"Output saved to: {OUTPUT_DIR}/full-entity-inventory.json")
    print(f"Output saved to: {OUTPUT_DIR}/artifact-summary.json")


if __name__ == "__main__":
    main()
