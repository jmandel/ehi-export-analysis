#!/usr/bin/env python3
"""
Parse all available EHI export artifacts for HealUs EHR and produce
entity-inventory-full.json and entity-inventory-summary.json.

Sources:
  - downloads/EHI.pdf (pdftotext output) — lists data categories and formats
  - downloads/fhir-capability-statement.json — FHIR resource types
"""

import json
import subprocess

# ── 1. Parse EHI PDF data categories ─────────────────────────────────────────
# The PDF has no field-level data dictionary, only category-level descriptions.
# We extract the categories, their export formats, and any detail from the text.

pdf_categories = [
    {
        "entity": "Patient Demographics",
        "format": "CSV",
        "source": "EHI.pdf p.4",
        "description": "CSV format – comprehensive view of patient demographics, structured for clarity and ease of access.",
        "fields": [],
        "field_count": None,
        "notes": "No column specification provided. Field names and types are undocumented."
    },
    {
        "entity": "Appointments",
        "format": "PDF, CSV",
        "source": "EHI.pdf p.4",
        "description": "Comprehensive view of appointments in both PDF and CSV formats.",
        "fields": [],
        "field_count": None,
        "notes": "No column specification for CSV. No structure documented for PDF."
    },
    {
        "entity": "Lab Results",
        "format": "PDF",
        "source": "EHI.pdf p.4",
        "description": "Comprehensive view of laboratory results in PDF format.",
        "fields": [],
        "field_count": None,
        "notes": "PDF only — not computable. No field-level documentation."
    },
    {
        "entity": "Imaging Results",
        "format": "PDF",
        "source": "EHI.pdf p.4",
        "description": "Comprehensive view of imaging results in PDF format.",
        "fields": [],
        "field_count": None,
        "notes": "PDF only — not computable. No field-level documentation."
    },
    {
        "entity": "Procedure Results",
        "format": "PDF",
        "source": "EHI.pdf p.4",
        "description": "Comprehensive view of procedure results in PDF format.",
        "fields": [],
        "field_count": None,
        "notes": "PDF only — not computable. No field-level documentation."
    },
    {
        "entity": "Encounters",
        "format": "PDF",
        "source": "EHI.pdf p.5",
        "description": "Comprehensive view of all data associated with patient encounters in PDF format.",
        "fields": [],
        "field_count": None,
        "notes": "PDF only — not computable. No field-level documentation."
    },
    {
        "entity": "Referrals",
        "format": "PDF",
        "source": "EHI.pdf p.5",
        "description": "Comprehensive view of referrals in PDF format.",
        "fields": [],
        "field_count": None,
        "notes": "PDF only — not computable. No field-level documentation."
    },
    {
        "entity": "Advance Directives",
        "format": "PDF",
        "source": "EHI.pdf p.5",
        "description": "Comprehensive view of advance directives in PDF format.",
        "fields": [],
        "field_count": None,
        "notes": "PDF only — not computable. No field-level documentation."
    },
    {
        "entity": "Documents",
        "format": "PDF",
        "source": "EHI.pdf p.5",
        "description": "Lab results, imaging reports, and scanned/uploaded documents. Sorted into category subfolders (Lab Reports, Imaging Reports, Consents, etc.).",
        "fields": [],
        "field_count": None,
        "notes": "PDF copies of original documents. No metadata schema documented."
    },
    {
        "entity": "Clinical Data (C-CDA)",
        "format": "C-CDA XML",
        "source": "EHI.pdf p.3",
        "description": "Clinical data exported via HL7 CDA R2 IHE Health Story Consolidation DSTU 1.1. Single and bulk patient export.",
        "fields": [],
        "field_count": None,
        "notes": "Standard C-CDA — no vendor-specific extensions or customizations documented."
    },
    {
        "entity": "Clinical Data (FHIR)",
        "format": "FHIR R4 JSON",
        "source": "EHI.pdf p.3, fhir-capability-statement.json",
        "description": "Clinical data exported via HL7 FHIR US Core IG STU 4.0.0 and FHIR Bulk Data Access v1.0.1.",
        "fields": [],
        "field_count": None,
        "notes": "Standard US Core resource set (27 types). No vendor-specific resources or extensions."
    },
]

# ── 2. Parse FHIR CapabilityStatement ────────────────────────────────────────
with open("downloads/fhir-capability-statement.json") as f:
    cs = json.load(f)

fhir_resources = []
for r in cs.get("rest", [{}])[0].get("resource", []):
    fhir_resources.append({
        "resource_type": r["type"],
        "interactions": [i["code"] for i in r.get("interaction", [])],
        "search_params": [p["name"] for p in r.get("searchParam", [])],
        "profiles": r.get("supportedProfile", []),
    })

# ── 3. Build full inventory ──────────────────────────────────────────────────
inventory = {
    "product": "HealUs EHR",
    "version": "1.0",
    "source_artifacts": [
        "downloads/EHI.pdf",
        "downloads/fhir-capability-statement.json",
    ],
    "data_dictionary_available": False,
    "field_level_documentation": False,
    "sample_data_available": False,
    "schema_available": False,
    "export_categories": pdf_categories,
    "fhir_resources": fhir_resources,
    "fhir_resource_count": len(fhir_resources),
}

with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# ── 4. Build summary ────────────────────────────────────────────────────────
pdf_only = [c for c in pdf_categories if c["format"] == "PDF"]
csv_categories = [c for c in pdf_categories if "CSV" in c["format"]]
ccda_categories = [c for c in pdf_categories if "C-CDA" in c["format"]]
fhir_categories = [c for c in pdf_categories if "FHIR" in c["format"]]

summary = {
    "product": "HealUs EHR",
    "version": "1.0",
    "total_export_categories": len(pdf_categories),
    "categories_with_field_documentation": 0,
    "total_documented_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "format_breakdown": {
        "pdf_only": len(pdf_only),
        "csv": len(csv_categories),
        "ccda": len(ccda_categories),
        "fhir": len(fhir_categories),
    },
    "fhir_resource_types": len(fhir_resources),
    "fhir_resource_list": [r["resource_type"] for r in fhir_resources],
    "us_core_standard_resources": sorted([r["resource_type"] for r in fhir_resources]),
    "vendor_specific_resources": [],
    "vendor_specific_extensions": [],
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema": False,
    "notes": (
        "The entire EHI export documentation is a 6-page PDF with no data dictionary, "
        "no field definitions, no sample data, and no schemas. The FHIR export is a "
        "standard US Core implementation with 27 resource types and no vendor extensions. "
        "7 of 11 export categories use PDF as the only format."
    ),
}

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# ── Print summary ────────────────────────────────────────────────────────────
print("=== Entity Inventory Summary ===")
print(f"Export categories: {summary['total_export_categories']}")
print(f"Categories with field docs: {summary['categories_with_field_documentation']}")
print(f"Total documented fields: {summary['total_documented_fields']}")
print(f"FHIR resource types: {summary['fhir_resource_types']}")
print(f"\nFormat breakdown:")
for fmt, count in summary["format_breakdown"].items():
    print(f"  {fmt}: {count}")
print(f"\nFHIR resources: {', '.join(summary['fhir_resource_list'])}")
print(f"\nVendor-specific resources: {len(summary['vendor_specific_resources'])}")
print(f"Vendor-specific extensions: {len(summary['vendor_specific_extensions'])}")
print("\nFiles written:")
print("  analysis/entity-inventory-full.json")
print("  analysis/entity-inventory-summary.json")
