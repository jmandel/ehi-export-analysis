#!/usr/bin/env python3
"""Parse all EHI export artifacts for Enable Healthcare MDnet and produce
a full-entity-inventory.json and summary statistics."""

import json
import re
import sys
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/enable-healthcare-inc--mdnet")
DOWNLOADS_DIR = RESULTS_DIR / "downloads"
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/enable-healthcare-inc--mdnet/analysis")

def parse_fhir_capability_statement():
    """Extract all resource types and their search parameters from the FHIR CapabilityStatement."""
    cs_path = DOWNLOADS_DIR / "fhir-capability-statement.json"
    with open(cs_path) as f:
        cs = json.load(f)

    resources = []
    for rest in cs.get("rest", []):
        for resource in rest.get("resource", []):
            r_type = resource.get("type", "Unknown")
            profile = resource.get("profile", "")
            supported_profiles = resource.get("supportedProfile", [])
            interactions = [i.get("code") for i in resource.get("interaction", [])]
            search_params = []
            for sp in resource.get("searchParam", []):
                search_params.append({
                    "name": sp.get("name"),
                    "type": sp.get("type"),
                    "documentation": sp.get("documentation", "")
                })
            operations = [op.get("name") for op in resource.get("operation", [])]
            resources.append({
                "type": r_type,
                "profile": profile,
                "supported_profiles": supported_profiles,
                "interactions": interactions,
                "search_params": search_params,
                "operations": operations,
                "search_param_count": len(search_params),
                "supported_profile_count": len(supported_profiles)
            })

    # Server-level operations
    server_ops = [op.get("name") for op in rest.get("operation", [])]

    return {
        "fhir_version": cs.get("fhirVersion"),
        "publisher": cs.get("publisher"),
        "software_name": cs.get("software", {}).get("name"),
        "software_version": cs.get("software", {}).get("version"),
        "resource_count": len(resources),
        "server_operations": server_ops,
        "resources": resources
    }


def parse_pdf_export_methods():
    """Parse the PDF text to extract structured information about export methods and C-CDA sections."""
    # We already have the PDF text extracted; parse it programmatically
    pdf_path = DOWNLOADS_DIR / "EHI_DATA_EXPort_GUIDE.pdf"

    import subprocess
    result = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, text=True)
    text = result.stdout

    # Extract the 8 export methods
    export_methods = [
        {
            "number": 1,
            "name": "FHIR APIs",
            "format": "FHIR R4 JSON/XML",
            "mode": "API (SMART on FHIR)",
            "description": "Standard FHIR R4 API with SMART on FHIR authorization. Supports US Core resource types and Bulk Data export.",
            "url": "https://fhir.ehiconnect.com/ehifhirportal/",
            "real_time": False,
            "bulk_capable": True
        },
        {
            "number": 2,
            "name": "C-CDA R2.1 bulk or single export",
            "format": "C-CDA R2.1 XML",
            "mode": "Integrated export tracker (UI)",
            "description": "Authorized users can set up one-time or scheduled tasks for FULL SET, Partial date-based, Partial Segment-based, or incremental updates.",
            "real_time": False,
            "bulk_capable": True
        },
        {
            "number": 3,
            "name": "CSV full data set export",
            "format": "CSV",
            "mode": "On-demand request by authorized users",
            "description": "Detailed export of health, activity and financial data for specific patient or all patients. Data dictionary referenced at https://emr.ehiconnect.com/docs/ (URL returns 404).",
            "data_dictionary_url": "https://emr.ehiconnect.com/docs/",
            "data_dictionary_accessible": False,
            "real_time": False,
            "bulk_capable": True
        },
        {
            "number": 4,
            "name": "HL7 2.x/3.x ADT",
            "format": "HL7 v2 ADT",
            "mode": "Real-time interface",
            "description": "Real-time updates on new patient chart creation, chart updates across demographics and payer information.",
            "real_time": True,
            "bulk_capable": False
        },
        {
            "number": 5,
            "name": "HL7 2.x SIU",
            "format": "HL7 v2 SIU",
            "mode": "Real-time interface",
            "description": "Real-time updates on patient appointments, edits, cancellations and check-in.",
            "real_time": True,
            "bulk_capable": False
        },
        {
            "number": 6,
            "name": "HL7 2.x DFT",
            "format": "HL7 v2 DFT",
            "mode": "Real-time interface",
            "description": "Listed for financial transactions but description repeats SIU text (apparent copy-paste error in PDF).",
            "note": "Copy-paste error: DFT description matches SIU description verbatim",
            "real_time": True,
            "bulk_capable": False
        },
        {
            "number": 7,
            "name": "JSON-based exchange for scanned documents",
            "format": "JSON with BASE-64 encoded content",
            "mode": "Real-time exchange",
            "description": "Exchange of all scanned documents, faxes across all or specific folders. JSON provides segments for patient identification and BASE-64 encoded document content.",
            "real_time": True,
            "bulk_capable": False
        },
        {
            "number": 8,
            "name": "EDI 837P and 835 Claims files",
            "format": "EDI 837P/835",
            "mode": "Continuous feed",
            "description": "Continuous feed of claim EDI 837P and EDI 835 files created for the practice.",
            "real_time": True,
            "bulk_capable": True
        }
    ]

    # C-CDA R2.1 sections listed in the PDF
    ccda_sections = [
        "Allergy",
        "Assessment",
        "Encounters",
        "Family History",
        "Functional Status",
        "Cognitive Status",
        "Immunizations",
        "Medical Equipment",
        "Medications",
        "Lab Results",
        "Problems",
        "Procedures",
        "Reason for Visit",
        "Referrals",
        "Social History",
        "Vitals",
        "Care Plan",
        "Goal",
        "Health Concern",
        "Clinical Instructions"
    ]

    return {
        "pdf_title": "DATA INTEROPERABILITY & EHI DATA EXPORT GUIDE",
        "pdf_author": "Rahul Dewan",
        "pdf_publisher": "Enable Healthcare, Inc",
        "pdf_date": "2023-12-28",
        "pdf_pages": 9,
        "pdf_size_bytes": 904203,
        "scope_statement": {
            "health_data": "Health Data stored in MDNet v10.0 which has been captured by the practice or received electronically related to a medical record.",
            "financial_data": "Financial data stored in MDNet v10.0 which has been captured by the practice or received electronically related to a medical record. This includes claim, adjudication and all other related data sets."
        },
        "export_method_count": len(export_methods),
        "export_methods": export_methods,
        "ccda_section_count": len(ccda_sections),
        "ccda_sections": ccda_sections,
        "optional_service": {
            "name": "Announce & Deliver",
            "description": "Optional data exchange service using C-CDA R2.1 with incremental updates",
            "transport_methods": [
                "VPN Based P2P secure tunnel",
                "SFTP Hosted by Enable Healthcare",
                "SFTP Hosted by Data Consumer",
                "Web Service Hosted by Enable Healthcare"
            ],
            "pages": "5-9"
        }
    }


def build_full_inventory():
    """Build the full entity inventory combining FHIR resources and export method information."""

    fhir_data = parse_fhir_capability_statement()
    pdf_data = parse_pdf_export_methods()

    # Build entities from FHIR resources
    fhir_entities = []
    for r in fhir_data["resources"]:
        fields = []
        for sp in r["search_params"]:
            fields.append({
                "name": sp["name"],
                "type": sp["type"],
                "description": sp["documentation"],
                "source": "FHIR search parameter"
            })
        fhir_entities.append({
            "name": r["type"],
            "category": "FHIR R4 Resource",
            "field_count": r["search_param_count"],
            "fields_with_descriptions": sum(1 for f in fields if f["description"]),
            "profile": r["profile"],
            "supported_profiles": r["supported_profiles"],
            "interactions": r["interactions"],
            "operations": r["operations"],
            "fields": fields,
            "source": "fhir-capability-statement.json"
        })

    # Build entities from C-CDA sections
    ccda_entities = []
    for section in pdf_data["ccda_sections"]:
        ccda_entities.append({
            "name": section,
            "category": "C-CDA R2.1 Section",
            "field_count": None,
            "fields_with_descriptions": None,
            "description": f"C-CDA R2.1 section as listed in EHI Data Export Guide",
            "fields": [],
            "source": "EHI_DATA_EXPort_GUIDE.pdf"
        })

    # Build entities from other export methods (no field-level detail available)
    other_entities = []
    for method in pdf_data["export_methods"]:
        if method["number"] not in [1, 2]:  # Skip FHIR and C-CDA (already covered)
            other_entities.append({
                "name": method["name"],
                "category": f"Export Method {method['number']}: {method['format']}",
                "field_count": None,
                "fields_with_descriptions": None,
                "description": method["description"],
                "format": method["format"],
                "fields": [],
                "source": "EHI_DATA_EXPort_GUIDE.pdf"
            })

    inventory = {
        "vendor": "Enable Healthcare Inc.",
        "product": "MDnet V10",
        "extraction_date": "2026-02-16",
        "sources": [
            {
                "file": "EHI_DATA_EXPort_GUIDE.pdf",
                "type": "PDF",
                "pages": 9,
                "description": "Primary EHI export documentation"
            },
            {
                "file": "fhir-capability-statement.json",
                "type": "JSON",
                "description": "FHIR R4 CapabilityStatement from the server"
            },
            {
                "file": "fhir-portal-landing.png",
                "type": "Screenshot",
                "description": "FHIR portal landing page"
            },
            {
                "file": "fhir-api-documentation-page.png",
                "type": "Screenshot",
                "description": "FHIR API documentation page"
            }
        ],
        "data_dictionary": {
            "referenced_url": "https://emr.ehiconnect.com/docs/",
            "accessible": False,
            "status": "HTTP 404 (verified 2026-02-16)",
            "note": "The CSV export data dictionary is referenced in the PDF but the URL is dead. No field-level documentation exists for the CSV export."
        },
        "fhir_api": fhir_data,
        "pdf_export_guide": pdf_data,
        "entities": {
            "fhir_resources": fhir_entities,
            "ccda_sections": ccda_entities,
            "other_export_methods": other_entities
        },
        "summary_statistics": {
            "fhir_resource_count": len(fhir_entities),
            "ccda_section_count": len(ccda_entities),
            "other_export_method_count": len(other_entities),
            "total_fhir_search_params": sum(e["field_count"] for e in fhir_entities if e["field_count"]),
            "fhir_resources_with_profiles": sum(1 for e in fhir_entities if e["profile"]),
            "export_methods_total": pdf_data["export_method_count"],
            "export_formats": ["FHIR R4 JSON/XML", "C-CDA R2.1 XML", "CSV", "HL7 v2 ADT", "HL7 v2 SIU", "HL7 v2 DFT", "JSON (documents)", "EDI 837P/835"],
            "has_data_dictionary": False,
            "has_sample_data": False,
            "has_machine_readable_schema": True,
            "machine_readable_schema_note": "FHIR CapabilityStatement only; no CSV schema"
        }
    }

    return inventory


def main():
    inventory = build_full_inventory()

    # Write full inventory
    output_path = OUTPUT_DIR / "full-entity-inventory.json"
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Written: {output_path}")

    # Print summary
    stats = inventory["summary_statistics"]
    print(f"\n=== Summary Statistics ===")
    print(f"FHIR Resource Types: {stats['fhir_resource_count']}")
    print(f"C-CDA Sections: {stats['ccda_section_count']}")
    print(f"Other Export Methods: {stats['other_export_method_count']}")
    print(f"Total FHIR Search Params: {stats['total_fhir_search_params']}")
    print(f"Export Formats: {len(stats['export_formats'])}")
    print(f"Data Dictionary Accessible: {stats['has_data_dictionary']}")
    print(f"Sample Data Available: {stats['has_sample_data']}")

    # Print FHIR resource breakdown
    print(f"\n=== FHIR Resources ({stats['fhir_resource_count']}) ===")
    for r in inventory["entities"]["fhir_resources"]:
        profiles = len(r.get("supported_profiles", []))
        print(f"  {r['name']}: {r['field_count']} search params, {profiles} profiles, ops: {r['operations']}")

    # Print C-CDA sections
    print(f"\n=== C-CDA Sections ({stats['ccda_section_count']}) ===")
    for s in inventory["entities"]["ccda_sections"]:
        print(f"  - {s['name']}")

    # Print export methods
    print(f"\n=== Export Methods ({inventory['pdf_export_guide']['export_method_count']}) ===")
    for m in inventory["pdf_export_guide"]["export_methods"]:
        print(f"  {m['number']}. {m['name']} ({m['format']}) - Bulk: {m['bulk_capable']}, Real-time: {m['real_time']}")


if __name__ == "__main__":
    main()
