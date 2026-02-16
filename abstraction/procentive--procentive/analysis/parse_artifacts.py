#!/usr/bin/env python3
"""Parse all Procentive EHI export artifacts and produce structured inventory."""

import json
import re
import os
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent.parent.parent / "results" / "procentive--procentive" / "downloads"
OUTPUT = Path(__file__).parent

def parse_fhir_capability_statement():
    """Extract resource types and capabilities from FHIR CapabilityStatement."""
    with open(DOWNLOADS / "fhir-capability-statement.json") as f:
        cs = json.load(f)
    
    rest = cs.get("rest", [{}])[0]
    resources = rest.get("resource", [])
    
    result = []
    for r in resources:
        entry = {
            "resource_type": r.get("type", "unknown"),
            "interactions": [i["code"] for i in r.get("interaction", [])],
            "operations": [o["name"] for o in r.get("operation", [])],
            "search_params": [s.get("name") for s in r.get("searchParam", [])],
        }
        result.append(entry)
    return result

def parse_uscdi_mapping():
    """Extract USCDI-to-FHIR mapping from the API documentation HTML."""
    with open(DOWNLOADS / "fhir-api-documentation.html") as f:
        content = f.read()
    
    tables = re.findall(r'<table[^>]*>(.*?)</table>', content, re.DOTALL)
    # Table 3 (index 2) is the USCDI mapping table
    if len(tables) < 3:
        return []
    
    table = tables[2]
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL)
    
    mappings = []
    for row in rows:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
        if len(cells) >= 2:
            uscdi = re.sub(r'<[^>]+>', '', cells[0]).strip()
            uscdi = ' '.join(uscdi.split())
            fhir_raw = re.sub(r'<[^>]+>', '', cells[1]).strip()
            fhir_resource = fhir_raw.split("Supported")[0].strip()
            fhir_resource = ' '.join(fhir_resource.split())
            
            if uscdi and fhir_resource and uscdi != "USCDI":
                mappings.append({
                    "uscdi_category": uscdi,
                    "fhir_resource": fhir_resource,
                })
    return mappings

def parse_pdf_content():
    """Parse the EHI File Formats PDF content."""
    return {
        "file": "PDF-for-Website-on-Formats-1.pdf",
        "pages": 1,
        "author": "Catherine Baker",
        "created": "2023-11-30",
        "creator": "Microsoft Word for Microsoft 365",
        "title": "Electronic Health Information (EHI) Export - File Formats",
        "content_summary": "Generic descriptions of three file formats: XML, CSV, PDF. No data dictionary, no field definitions, no schema, no entity descriptions.",
        "formats_described": [
            {"format": "XML", "description": "Generic description of XML markup language"},
            {"format": "CSV", "description": "Generic description of comma-separated values format"},
            {"format": "PDF documents", "description": "Generic description of Portable Document Format"},
        ],
        "data_dictionary_present": False,
        "field_definitions_present": False,
        "schema_present": False,
        "sample_data_present": False,
    }

def parse_onc_page():
    """Extract EHI export information from ONC page."""
    return {
        "file": "onc-procentive-page.html",
        "url": "https://ensorahealth.com/onc/procentive/",
        "status": "live (verified 2026-02-16)",
        "ehi_export_section": {
            "single_patient_export": {
                "description": "Procentive EHR allows a user to export electronic health information (EHI) for a single patient without developer assistance using the following standardized file formats.",
                "self_service": True,
            },
            "population_export": {
                "description": "Procentive EHR can export all the data for a patient population using the following standardized formats. This export can be requested by submitting a support ticket via Salesforce.",
                "self_service": False,
                "mechanism": "Support ticket via Salesforce",
            },
            "variability_factors": [
                "Software application(s) in use",
                "Software version in use",
                "Documentation and software use practices",
                "Configuration decisions",
                "Health system including materials not sourced from the application",
            ],
        },
        "linked_pdf": "PDF-for-Website-on-Formats-1.pdf",
        "fhir_endpoints_referenced": True,
    }

def build_full_inventory():
    """Build the complete artifact inventory."""
    fhir_resources = parse_fhir_capability_statement()
    uscdi_mapping = parse_uscdi_mapping()
    pdf_content = parse_pdf_content()
    onc_page = parse_onc_page()
    
    inventory = {
        "product": "Procentive",
        "developer": "Procentive (Ensora Health / Therapy Brands)",
        "analysis_date": "2026-02-16",
        "ehi_export_documentation": {
            "has_data_dictionary": False,
            "has_field_definitions": False,
            "has_schema": False,
            "has_sample_data": False,
            "has_entity_list": False,
            "total_entities_documented": 0,
            "total_fields_documented": 0,
            "b10_specific_documentation": pdf_content,
            "onc_page": onc_page,
        },
        "fhir_api_g10": {
            "server": "Dynamic FHIR Server 4.0.1 / ConnectEHR v4 + BulkFHIR4",
            "base_url": "https://fhir.procentive.com/fhir/procentive/basepractice/r4",
            "resource_types_count": len(fhir_resources),
            "resources": fhir_resources,
            "uscdi_mapping_count": len(uscdi_mapping),
            "uscdi_mapping": uscdi_mapping,
            "bulk_export_supported": True,
            "bulk_export_operations": ["Patient/$export", "Group/[id]/$export"],
            "output_format": "NDJSON (application/fhir+ndjson)",
            "explicitly_limited_to_uscdi": True,
            "uscdi_limitation_quote": "Available data via the API interface is limited by the data defined by the USCDI.",
        },
        "artifacts_reviewed": [
            {
                "file": "PDF-for-Website-on-Formats-1.pdf",
                "type": "PDF",
                "size_bytes": 112441,
                "pages": 1,
                "relevance": "primary_b10",
                "informativeness": "very_low",
                "description": "The sole (b)(10) documentation artifact. Single page describing XML, CSV, and PDF as export formats in generic terms. No data dictionary, no field definitions, no schema.",
            },
            {
                "file": "onc-procentive-page.html",
                "type": "HTML",
                "size_bytes": 83386,
                "relevance": "primary_b10",
                "informativeness": "low",
                "description": "ONC certification landing page. Contains EHI export description (single-patient and population export), attestation disclosure, FHIR endpoint links.",
            },
            {
                "file": "fhir-api-documentation.html",
                "type": "HTML",
                "size_bytes": 686494,
                "relevance": "g10_only",
                "informativeness": "high_for_g10",
                "description": "Complete FHIR API documentation. Covers USCDI-to-FHIR resource mapping, search parameters, example payloads, authentication, and Bulk Export. Explicitly limited to USCDI data.",
            },
            {
                "file": "fhir-capability-statement.json",
                "type": "JSON",
                "size_bytes": 18940,
                "relevance": "g10_only",
                "informativeness": "medium",
                "description": f"FHIR CapabilityStatement listing {len(fhir_resources)} resource types.",
            },
            {
                "file": "smart-configuration.json",
                "type": "JSON",
                "size_bytes": 3309,
                "relevance": "g10_only",
                "informativeness": "low",
                "description": "SMART on FHIR configuration with supported scopes and capabilities.",
            },
            {
                "file": "fhir-endpoints.json",
                "type": "JSON",
                "size_bytes": 2072,
                "relevance": "g10_only",
                "informativeness": "low",
                "description": "FHIR Endpoint Bundle with one endpoint for Procentive base practice.",
            },
            {
                "file": "fhir-home-page.html",
                "type": "HTML",
                "size_bytes": 14938,
                "relevance": "g10_only",
                "informativeness": "low",
                "description": "FHIR server home page showing Dynamic FHIR Server 4.0.1.",
            },
        ],
        "summary_statistics": {
            "b10_entities_documented": 0,
            "b10_fields_documented": 0,
            "b10_fields_with_descriptions": 0,
            "b10_sample_data_files": 0,
            "g10_fhir_resource_types": len(fhir_resources),
            "g10_uscdi_categories_mapped": len(uscdi_mapping),
            "total_artifacts": 11,  # including screenshots
            "informative_artifacts": 4,  # excluding screenshots and minimal JSON files
        },
    }
    return inventory

if __name__ == "__main__":
    inventory = build_full_inventory()
    
    output_path = OUTPUT / "full-entity-inventory.json"
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    
    print(f"Inventory written to {output_path}")
    print(f"\nSummary:")
    print(f"  (b)(10) entities documented: {inventory['summary_statistics']['b10_entities_documented']}")
    print(f"  (b)(10) fields documented: {inventory['summary_statistics']['b10_fields_documented']}")
    print(f"  (g)(10) FHIR resource types: {inventory['summary_statistics']['g10_fhir_resource_types']}")
    print(f"  (g)(10) USCDI categories mapped: {inventory['summary_statistics']['g10_uscdi_categories_mapped']}")
    print(f"  Data dictionary present: {inventory['ehi_export_documentation']['has_data_dictionary']}")
    print(f"  Sample data present: {inventory['ehi_export_documentation']['has_sample_data']}")
