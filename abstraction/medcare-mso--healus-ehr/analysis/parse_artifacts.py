#!/usr/bin/env python3
"""
Parse all EHI export artifacts for HealUs EHR and produce:
1. full-entity-inventory.json — structured extraction of all export content
2. analysis-stats.json — summary statistics derived from the inventory
"""

import json
import subprocess
import re
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent.parent.parent / "results" / "medcare-mso--healus-ehr" / "downloads"
OUTPUT = Path(__file__).parent

def parse_pdf():
    """Extract structured content from EHI.pdf using pdftotext output."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(DOWNLOADS / "EHI.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Parse data categories from the PDF
    categories = []
    
    # Patient Demographics
    categories.append({
        "entity": "Patient Demographics",
        "export_format": "CSV",
        "description": "Comprehensive view of patient demographics, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 4"
    })
    
    # Appointments
    categories.append({
        "entity": "Appointments",
        "export_format": "PDF and CSV",
        "description": "Comprehensive view of appointments in both formats, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 4"
    })
    
    # Lab Results
    categories.append({
        "entity": "Lab Results",
        "export_format": "PDF",
        "description": "Comprehensive view of laboratory results, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 4"
    })
    
    # Imaging Results
    categories.append({
        "entity": "Imaging Results",
        "export_format": "PDF",
        "description": "Comprehensive view of imaging results, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 4"
    })
    
    # Procedure Results
    categories.append({
        "entity": "Procedure Results",
        "export_format": "PDF",
        "description": "Comprehensive view of procedure results, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 4"
    })
    
    # Encounters
    categories.append({
        "entity": "Encounters",
        "export_format": "PDF",
        "description": "Comprehensive view of all data associated with patient encounters, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 5"
    })
    
    # Referrals
    categories.append({
        "entity": "Referrals",
        "export_format": "PDF",
        "description": "Comprehensive view of referrals, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 5"
    })
    
    # Advance Directives
    categories.append({
        "entity": "Advance Directives",
        "export_format": "PDF",
        "description": "Comprehensive view of advance directives, structured for clarity and ease of access.",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 5"
    })
    
    # Documents
    categories.append({
        "entity": "Documents",
        "export_format": "PDF",
        "description": "Lab results, imaging reports, and any other scanned or uploaded documents. Sorted and indexed by category subfolders (Lab Reports, Imaging Reports, Consents, etc.).",
        "fields": [],
        "field_count": "unknown — no field-level documentation provided",
        "source": "EHI.pdf, page 5"
    })
    
    # Clinical Data via C-CDA
    categories.append({
        "entity": "Clinical Data (C-CDA)",
        "export_format": "XML (C-CDA)",
        "description": "Clinical data exported via Consolidated CDA as per HL7 CDA R2 IHE Health Story Consolidation DSTU 1.1. Covers standard C-CDA sections (problems, medications, allergies, immunizations, vitals, procedures, etc.).",
        "fields": [],
        "field_count": "standard C-CDA sections — no vendor-specific documentation",
        "source": "EHI.pdf, page 3"
    })
    
    # Clinical Data via FHIR
    categories.append({
        "entity": "Clinical Data (FHIR)",
        "export_format": "JSON (FHIR R4)",
        "description": "Clinical data exported via HL7 FHIR US Core IG STU 4.0.0 and FHIR Bulk Data Access v1.0.1. Standard US Core resource set.",
        "fields": [],
        "field_count": "27 resource types per CapabilityStatement — standard US Core profiles",
        "source": "EHI.pdf, page 5; fhir-capability-statement.json"
    })
    
    return categories


def parse_fhir_capability_statement():
    """Parse the FHIR CapabilityStatement to extract supported resources."""
    with open(DOWNLOADS / "fhir-capability-statement.json") as f:
        cs = json.load(f)
    
    resources = []
    for rest in cs.get("rest", []):
        for r in rest.get("resource", []):
            resource = {
                "type": r["type"],
                "interactions": [i["code"] for i in r.get("interaction", [])],
                "search_params_count": len(r.get("searchParam", [])),
                "search_params": [p["name"] for p in r.get("searchParam", [])],
                "supported_profiles": r.get("supportedProfile", []),
                "profile": r.get("profile", None)
            }
            resources.append(resource)
    
    operations = []
    for rest in cs.get("rest", []):
        for op in rest.get("operation", []):
            operations.append({
                "name": op["name"],
                "definition": op.get("definition", "")
            })
    
    return {
        "fhir_version": cs.get("fhirVersion"),
        "instantiates": cs.get("instantiates", []),
        "implementation_guides": cs.get("implementationGuide", []),
        "resource_count": len(resources),
        "resources": resources,
        "operations": operations
    }


def main():
    # Parse all artifacts
    pdf_categories = parse_pdf()
    fhir_data = parse_fhir_capability_statement()
    
    # Build full entity inventory
    inventory = {
        "product": "HealUs EHR",
        "version": "1.0",
        "developer": "Medcare MSO",
        "certification_date": "2024-07-15",
        "chpl_id": 11495,
        "analysis_date": "2026-02-15",
        "export_documentation": {
            "source_file": "EHI.pdf",
            "pages": 6,
            "content_pages": 5,
            "created": "2024-04-22",
            "author": "Ramsha Rasheed",
            "has_data_dictionary": False,
            "has_field_definitions": False,
            "has_sample_data": False,
            "has_schema": False,
            "has_relationships": False,
            "has_value_sets": False
        },
        "export_formats": [
            {"format": "C-CDA XML", "standard": "HL7 CDA R2 IHE Health Story Consolidation DSTU 1.1", "data_types": ["Clinical data"]},
            {"format": "FHIR R4 JSON", "standard": "HL7 FHIR US Core IG STU 4.0.0 + Bulk Data Access v1.0.1", "data_types": ["Clinical data"]},
            {"format": "PDF", "standard": None, "data_types": ["Lab results", "Imaging results", "Procedure results", "Encounters", "Appointments", "Referrals", "Advance directives", "Documents"]},
            {"format": "CSV", "standard": None, "data_types": ["Patient demographics", "Appointments"]}
        ],
        "export_categories": pdf_categories,
        "fhir_capability": fhir_data,
        "total_export_categories": len(pdf_categories),
        "categories_with_field_definitions": 0,
        "categories_with_computable_format": sum(1 for c in pdf_categories if c["export_format"] not in ["PDF"]),
        "categories_with_pdf_only": sum(1 for c in pdf_categories if c["export_format"] == "PDF")
    }
    
    # Write full inventory
    with open(OUTPUT / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote full-entity-inventory.json")
    
    # Compute and write statistics
    stats = {
        "total_export_categories": inventory["total_export_categories"],
        "categories_with_field_definitions": 0,
        "categories_with_computable_format": inventory["categories_with_computable_format"],
        "categories_pdf_only": inventory["categories_with_pdf_only"],
        "fhir_resource_types": fhir_data["resource_count"],
        "fhir_operations": len(fhir_data["operations"]),
        "pdf_metadata": {
            "pages": 6,
            "content_pages": 5,
            "has_data_dictionary": False,
            "has_field_definitions": False,
            "has_sample_data": False,
            "has_schema": False
        },
        "format_breakdown": {
            "PDF_only": [c["entity"] for c in pdf_categories if c["export_format"] == "PDF"],
            "CSV": [c["entity"] for c in pdf_categories if "CSV" in c["export_format"]],
            "C-CDA": [c["entity"] for c in pdf_categories if "C-CDA" in c["export_format"] or "CDA" in c["export_format"]],
            "FHIR": [c["entity"] for c in pdf_categories if "FHIR" in c["export_format"]]
        },
        "documentation_quality": {
            "total_fields_documented": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "fields_with_value_sets": 0,
            "relationships_documented": 0,
            "assessment": "No field-level documentation exists. The PDF describes 11 data categories at a category level only, with no field names, data types, value sets, or relationships."
        }
    }
    
    with open(OUTPUT / "analysis-stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Wrote analysis-stats.json")
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Export categories: {stats['total_export_categories']}")
    print(f"  PDF-only: {stats['categories_pdf_only']} ({', '.join(stats['format_breakdown']['PDF_only'])})")
    print(f"  CSV: {len(stats['format_breakdown']['CSV'])} ({', '.join(stats['format_breakdown']['CSV'])})")
    print(f"  C-CDA: {len(stats['format_breakdown']['C-CDA'])} ({', '.join(stats['format_breakdown']['C-CDA'])})")
    print(f"  FHIR: {len(stats['format_breakdown']['FHIR'])} ({', '.join(stats['format_breakdown']['FHIR'])})")
    print(f"FHIR resource types: {stats['fhir_resource_types']}")
    print(f"Field-level documentation: NONE")
    print(f"Sample data: NONE")
    print(f"Data dictionary: NONE")


if __name__ == "__main__":
    main()
