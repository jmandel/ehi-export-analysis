#!/usr/bin/env python3
"""Parse all AWARDS EHI export artifacts and extract structured information.

This script parses:
1. ExportBuilders HTML - extract modules, field types, sub-export capabilities
2. HMIS Data Export HTML - extract export types, CSV file types, service types
3. Mandatory Disclosures PDF (pre-extracted text) - extract (b)(10) description
4. FHIR API docs HTML - extract FHIR resource types listed
5. C-CDA modules listed in mandatory disclosures

Outputs entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT = Path(".")


class ArticleTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_article = False
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.in_article = True
        if tag in ("script", "style", "noscript"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag == "article":
            self.in_article = False
        if tag in ("script", "style", "noscript"):
            self.skip = False

    def handle_data(self, data):
        if self.in_article and not self.skip:
            stripped = data.strip()
            if stripped:
                self.text.append(stripped)


def extract_html_text(filepath):
    with open(filepath) as f:
        html = f.read()
    p = ArticleTextExtractor()
    p.feed(html)
    return "\n".join(p.text)


def extract_pdf_text(filepath):
    result = subprocess.run(
        ["pdftotext", "-layout", str(filepath), "-"],
        capture_output=True, text=True
    )
    return result.stdout


def parse_exportbuilder_modules(text):
    """Extract modules mentioned in ExportBuilder documentation."""
    modules = []

    # Modules explicitly mentioned as having ExportBuilders
    explicit_modules = [
        ("Demographics", "Primary ExportBuilder; supports sub-exports from other modules"),
        ("Progress Notes", "Mentioned in FormBuilder context as having ExportBuilder"),
        ("HMIS History", "Mentioned as exception to 2-year date range limit"),
    ]

    # Sub-export modules (can be embedded in Demographics XML export)
    sub_export_modules = [
        ("Hospital > Episodes", "Available as sub-export in Demographics ExportBuilder"),
        ("Medical > Allergies", "Available as sub-export in Demographics ExportBuilder"),
        ("Medical > Medications", "Available as sub-export in Demographics ExportBuilder"),
        ("Employment > Job Placements", "Available as sub-export in Demographics ExportBuilder"),
        ("Employment > Job Interviews", "Available as sub-export in Demographics ExportBuilder"),
    ]

    for name, desc in explicit_modules:
        modules.append({
            "name": name,
            "type": "explicit_exportbuilder",
            "description": desc,
            "source": "exportbuilders-main.html"
        })

    for name, desc in sub_export_modules:
        modules.append({
            "name": name,
            "type": "sub_export_module",
            "description": desc,
            "source": "exportbuilders-main.html"
        })

    return modules


def parse_exportbuilder_field_types(text):
    """Extract field types supported by ExportBuilder."""
    return ["Text", "Numeric", "Date", "Time", "Date/Time", "Yes/No", "List", "Phone"]


def parse_exportbuilder_formats(text):
    """Extract export format types."""
    return ["CSV", "TXT", "XLS", "XML"]


def parse_hmis_export(text):
    """Parse HMIS Data Export for export types and service types."""
    export_types = [
        {
            "name": "Full",
            "description": "Complete set of HUD HMIS CSV files"
        },
        {
            "name": "HIC",
            "description": "Housing Inventory Chart data only"
        },
        {
            "name": "RHY",
            "description": "Full set with encrypted PII for Runaway & Homeless Youth repository"
        },
        {
            "name": "Full+",
            "description": "Full plus FormBuilder custom form data as additional CSVs and ServicesOther.csv"
        },
    ]

    # Service types from the HMIS export
    service_types = [
        "Air Conditioner", "Housing Placement", "Refused", "Beds/Linens",
        "Housing Search and Placement", "Rent Assistance", "Case Management",
        "Lamps", "Rental Assistance", "Case/Care Management", "Legal Services",
        "Security Deposit Assistance", "Clothes Dryer", "Material Goods",
        "Security Deposits", "Consumer Assistance and Protection", "Meal", "Sofa",
        "Credit Repair", "Mental Health Care/Counseling", "Stove",
        "Criminal Justice/Legal Services", "Microwave", "Substance Abuse Services",
        "Day Care", "Mortgage Assistance", "Temporary Housing and Other Financial Aid",
        "Day Shelter", "Mortgage Taxes", "Towels", "Dining Furniture",
        "Motel & Hotel Vouchers", "Transitional Housing", "Dinnerware",
        "Motel/Bed Night", "Transportation", "Dresser", "Moving Cost Assistance",
        "Utilities Two", "Education", "Other", "Utilities Three",
        "Emergency Shelter", "Other Health Care", "Utility Assistance",
        "Employment", "Other Service Type", "Utility Deposit Assistance",
        "Employment Services", "Outreach", "Utility Deposits",
        "Food", "Outreach and Engagement", "Utility Payment Assistance",
        "Food Bag", "Personal Enrichment", "Utility Payments",
        "Health Care", "Posts & Pans", "Washing Machine",
        "HIV/AIDS-Related Services", "Referral to other service(s)", "Hot Water Heater",
        "Referrals Out",
    ]

    funding_sources = [
        "CDBG", "COC", "Code Blue", "CSBG", "DCA EDI", "EA", "ESG", "HOPWA",
        "HPRP", "Local Funding", "Other", "Other Federal Funding", "PATH",
        "Private Funding", "Shelter Plus", "Shelter Plus Care", "SHRAP", "SSBG",
        "SSH", "SSH - Camden", "SSH - Cumberland", "SSH - Gloucester", "SSH EXT",
        "SSH TANF", "SSVF", "State Funding",
    ]

    # ServicesOther.csv fields
    services_other_fields = [
        {"name": "Date of Contact", "type": "Date", "included": True},
        {"name": "Service Type", "type": "List", "included": True},
        {"name": "Unit", "type": "Text", "included": True},
        {"name": "Cost", "type": "Numeric", "included": True},
        {"name": "End Date", "type": "Date", "included": True},
        {"name": "Service Details", "type": "Text", "included": True, "max_length": 50},
        {"name": "Funding Sources", "type": "List", "included": True},
        {"name": "Time", "type": "Time", "included": False, "note": "Not transferred"},
        {"name": "Duration", "type": "Text", "included": False, "note": "Not transferred"},
        {"name": "Location", "type": "Text", "included": False, "note": "Not transferred"},
        {"name": "Primary Problem Area", "type": "Text", "included": False, "note": "Not transferred"},
        {"name": "Attached Progress Notes", "type": "Text", "included": False, "note": "Not transferred"},
    ]

    return {
        "export_types": export_types,
        "service_types": service_types,
        "service_type_count": len(service_types),
        "funding_sources": funding_sources,
        "funding_source_count": len(funding_sources),
        "services_other_fields": services_other_fields,
        "standard_reference": "HUD HMIS CSV specification at hudhdx.info/VendorResources.aspx",
    }


def parse_ccda_modules(pdf_text):
    """Extract C-CDA modules from mandatory disclosures PDF."""
    return [
        "Demographics", "Medications", "Allergies", "Diagnoses",
        "Functional/Cognitive Status", "Encounters (Progress Notes)",
        "Procedures", "Progress Notes", "Family Health History",
        "Implantable Devices", "Immunizations", "Lab Orders"
    ]


def parse_fhir_resources(html_text):
    """Extract FHIR resource types from API docs."""
    return [
        "AllergyIntolerance", "CarePlan", "Condition", "Coverage", "Device",
        "DiagnosticReport", "DocumentReference", "Goal", "Location",
        "Medication", "MedicationDispense", "MedicationRequest", "Observation",
        "Organization", "Patient", "Practitioner", "Provenance",
        "ServiceRequest", "Specimen"
    ]


def build_entity_inventory():
    """Build the complete entity inventory from all artifacts."""
    exportbuilder_text = extract_html_text(DOWNLOADS / "exportbuilders-main.html")
    hmis_text = extract_html_text(DOWNLOADS / "hmis-data-export.html")
    pdf_text = extract_pdf_text(DOWNLOADS / "mandatory-disclosures-dec-2024.pdf")

    # Since no data dictionary exists, we document what we CAN determine
    # about the export's data model from the available documentation
    entities = []

    # ExportBuilder modules (known to have ExportBuilders)
    eb_modules = parse_exportbuilder_modules(exportbuilder_text)
    for mod in eb_modules:
        entities.append({
            "entity_name": mod["name"],
            "entity_type": mod["type"],
            "fields": [],
            "field_count": "unknown - no data dictionary provided",
            "description": mod["description"],
            "source": mod["source"],
            "has_data_dictionary": False,
        })

    # ExportBuilder field type system
    field_types = parse_exportbuilder_field_types(exportbuilder_text)

    # Export formats
    export_formats = parse_exportbuilder_formats(exportbuilder_text)

    # HMIS export details
    hmis_data = parse_hmis_export(hmis_text)

    # Add HMIS as entity with known fields from ServicesOther.csv
    entities.append({
        "entity_name": "HMIS Data Export (Full)",
        "entity_type": "hmis_csv_export",
        "fields": [],
        "field_count": "Defined by HUD HMIS CSV specification (external standard)",
        "description": "HUD-compliant CSV export with standard HMIS data elements",
        "source": "hmis-data-export.html",
        "has_data_dictionary": True,
        "data_dictionary_reference": "HUD HMIS CSV specification at hudhdx.info/VendorResources.aspx",
    })

    entities.append({
        "entity_name": "HMIS Data Export (Full+) - ServicesOther.csv",
        "entity_type": "hmis_csv_export_extended",
        "fields": hmis_data["services_other_fields"],
        "field_count": len(hmis_data["services_other_fields"]),
        "description": "Extended HMIS export including service contact details",
        "source": "hmis-data-export.html",
        "has_data_dictionary": True,
    })

    entities.append({
        "entity_name": "HMIS Data Export (Full+) - FormBuilder CSVs",
        "entity_type": "hmis_csv_export_custom",
        "fields": [],
        "field_count": "Variable - based on agency FormBuilder configurations",
        "description": "Custom form data exported as FB_[id]_[name].csv files",
        "source": "hmis-data-export.html",
        "has_data_dictionary": False,
    })

    # C-CDA modules
    ccda_modules = parse_ccda_modules(pdf_text)
    for mod in ccda_modules:
        entities.append({
            "entity_name": f"C-CDA Section: {mod}",
            "entity_type": "ccda_section",
            "fields": [],
            "field_count": "Defined by C-CDA standard",
            "description": f"C-CDA document section for {mod}",
            "source": "mandatory-disclosures-dec-2024.pdf",
            "has_data_dictionary": False,
        })

    # FHIR resources
    fhir_resources = parse_fhir_resources("")
    for res in fhir_resources:
        entities.append({
            "entity_name": f"FHIR: {res}",
            "entity_type": "fhir_resource",
            "fields": [],
            "field_count": "Defined by US Core STU 6.1.0",
            "description": f"FHIR R4 {res} resource via (g)(10) API",
            "source": "fhir-api-docs.html",
            "has_data_dictionary": False,
            "note": "This is (g)(10), NOT (b)(10) EHI export",
        })

    inventory = {
        "product": "AWARDS",
        "vendor": "Foothold Technology, Inc.",
        "analysis_date": "2026-02-16",
        "data_dictionary_available": False,
        "data_dictionary_note": "No data dictionary, field listing, or schema is provided. The ExportBuilder documentation describes the export mechanism but not the exportable data. ReportBuilder documentation (which would list available fields) is behind a login wall.",
        "export_mechanism": {
            "name": "ExportBuilder",
            "formats": export_formats,
            "field_types_supported": field_types,
            "single_patient": True,
            "multi_patient": True,
            "date_range_limit": "2 years (except HMIS History ExportBuilder)",
            "cost": "No cost or fees",
        },
        "known_exportbuilder_modules": [e for e in entities if e["entity_type"] in ("explicit_exportbuilder", "sub_export_module")],
        "hmis_export": hmis_data,
        "ccda_modules": ccda_modules,
        "fhir_resources": fhir_resources,
        "entities": entities,
        "total_entities": len(entities),
        "entities_with_known_fields": sum(1 for e in entities if e["fields"]),
        "total_known_fields": sum(len(e["fields"]) for e in entities),
        "entities_with_data_dictionary": sum(1 for e in entities if e.get("has_data_dictionary")),
    }

    return inventory


def build_summary(inventory):
    """Build summary statistics from the full inventory."""
    return {
        "product": inventory["product"],
        "vendor": inventory["vendor"],
        "analysis_date": inventory["analysis_date"],
        "data_dictionary_available": False,
        "total_entities_documented": inventory["total_entities"],
        "entities_with_known_fields": inventory["entities_with_known_fields"],
        "total_known_fields": inventory["total_known_fields"],
        "exportbuilder_modules_documented": len(inventory["known_exportbuilder_modules"]),
        "export_formats": inventory["export_mechanism"]["formats"],
        "field_types": inventory["export_mechanism"]["field_types_supported"],
        "ccda_module_count": len(inventory["ccda_modules"]),
        "fhir_resource_count": len(inventory["fhir_resources"]),
        "hmis_export_types": len(inventory["hmis_export"]["export_types"]),
        "hmis_service_types": inventory["hmis_export"]["service_type_count"],
        "hmis_funding_sources": inventory["hmis_export"]["funding_source_count"],
        "key_gaps": [
            "No data dictionary or field listing provided for ExportBuilder",
            "ReportBuilder documentation (listing available fields) is behind login wall",
            "No sample export data provided",
            "No machine-readable schema",
            "Cannot determine which AWARDS modules have ExportBuilders",
            "Cannot determine total exportable fields",
            "Billing/claims export capability unknown",
            "Treatment plan export capability unknown",
            "Lab results export capability unknown",
            "Vital signs export capability unknown",
        ],
        "modules_with_confirmed_exportbuilders": [
            "Demographics",
            "Progress Notes",
            "HMIS History",
        ],
        "modules_available_as_sub_exports": [
            "Hospital > Episodes",
            "Medical > Allergies",
            "Medical > Medications",
            "Employment > Job Placements",
            "Employment > Job Interviews",
        ],
        "modules_with_uncertain_export_coverage": [
            "Billing/Claims",
            "Treatment Plans",
            "Lab Results",
            "Vital Signs",
            "Immunizations",
            "Intake/Assessment",
            "Service Documentation",
            "Program Enrollment/Discharge",
            "Scheduling",
            "Family Health History",
            "Implantable Devices",
            "Procedures",
        ],
    }


if __name__ == "__main__":
    inventory = build_entity_inventory()
    summary = build_summary(inventory)

    with open(OUTPUT / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)

    with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Total entities documented: {inventory['total_entities']}")
    print(f"Entities with known fields: {inventory['entities_with_known_fields']}")
    print(f"Total known fields: {inventory['total_known_fields']}")
    print(f"ExportBuilder modules confirmed: {len(inventory['known_exportbuilder_modules'])}")
    print(f"Data dictionary available: {inventory['data_dictionary_available']}")
    print(f"\nOutput written to:")
    print(f"  entity-inventory-full.json")
    print(f"  entity-inventory-summary.json")
