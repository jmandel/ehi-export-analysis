#!/usr/bin/env python3
"""
Parse all Pulse EHR EHI export artifacts and produce:
- full-entity-inventory.json: complete parse of all structured content
- summary_stats.json: aggregate statistics for analysis.md
"""

import json
import os
from docx import Document

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/pulse-systems-inc--pulse-ehr/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/pulse-systems-inc--pulse-ehr/analysis"

def parse_docx():
    """Parse the CHS-hosted EHI Export Document (DOCX)."""
    doc = Document(os.path.join(RESULTS_DIR, "Pulse-EHI-Export-Document-REV-06142024.docx"))

    # Extract CDA sections from the table
    table = doc.tables[0]
    raw_sections = []
    for ri, row in enumerate(table.rows):
        cell_text = row.cells[0].text.strip()
        if ri == 0:  # header row
            continue
        if cell_text:
            raw_sections.append(cell_text)

    # Deduplicate and categorize
    unique_sections = list(dict.fromkeys(raw_sections))  # preserve order, remove dupes
    duplicates = [s for s in raw_sections if raw_sections.count(s) > 1]
    duplicate_names = list(set(duplicates))

    # Map CDA sections to clinical domains
    domain_mapping = {
        "Security and Privacy Prohibitions": "Administrative",
        "Allergies and Adverse Reactions": "Allergies",
        "Medications": "Medications",
        "Discharge Medications": "Medications",
        "Problems": "Problems / Conditions",
        "Hospital Discharge Diagnosis": "Problems / Conditions",
        "Encounters": "Encounters",
        "Admission Diagnosis": "Problems / Conditions",
        "Procedures": "Procedures",
        "Implants": "Implantable Devices",
        "Immunizations": "Immunizations",
        "Vital Signs": "Vitals",
        "Social History": "Social History",
        "Results": "Lab Results",
        "Functional Status": "Functional Status",
        "Mental Status": "Mental Status",
        "Assessments": "Assessments",
        "PLAN OF CARE": "Care Plans / Goals",
        "Goals Section": "Care Plans / Goals",
        "Health Concerns Section": "Problems / Conditions",
        "Hospital Discharge Instructions": "Clinical Notes",
        "Family History": "Family History",
        "Reason For Visit/Chief Complaint": "Clinical Notes",
        "General Status": "Clinical Notes",
        "Past Medical History": "Clinical Notes",
        "History Of Present Illness": "Clinical Notes",
        "Physical Examination": "Clinical Notes",
        "Review Of Systems": "Clinical Notes",
        "Progress Note": "Clinical Notes",
        "PreOperative Diagnosis": "Procedures",
        "Postprocedure Diagnosis": "Procedures",
        "Planned Procedure": "Procedures",
        "Complications": "Clinical Notes",
        "Procedure Indications": "Procedures",
        "Procedure Description": "Procedures",
        "Procedure Note": "Procedures",
        "Reason for Referral": "Orders / Referrals",
        "Hospital Course": "Clinical Notes",
        "Interventions Section": "Care Plans / Goals",
        "Health Status Evaluations/Outcomes Section": "Care Plans / Goals",
        "Discharge Summary Note": "Clinical Notes",
        "Consultation Note": "Clinical Notes",
        "Payers": "Insurance / Coverage",
        "Financial Data": "Claims / Billing",
    }

    sections_with_domains = []
    for s in unique_sections:
        sections_with_domains.append({
            "section_name": s,
            "mapped_domain": domain_mapping.get(s, "Unknown"),
            "is_duplicate_in_source": s in duplicate_names,
        })

    # Count by domain
    domain_counts = {}
    for s in sections_with_domains:
        d = s["mapped_domain"]
        domain_counts[d] = domain_counts.get(d, 0) + 1

    # Extract prose content
    prose_content = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if text:
            prose_content.append({"style": p.style.name, "text": text})

    return {
        "source_file": "Pulse-EHI-Export-Document-REV-06142024.docx",
        "source_url": "https://www.chs.net/_assets/docs/Pulse-EHI-Export-Document-REV-06142024.docx",
        "document_type": "CHS/CereCore EHI Export Document for Pulse v16.1",
        "author": str(doc.core_properties.author),
        "created": str(doc.core_properties.created),
        "modified": str(doc.core_properties.modified),
        "export_format": "CDA XML (Clinical Document Architecture)",
        "total_raw_sections": len(raw_sections),
        "unique_sections": len(unique_sections),
        "duplicate_section_names": duplicate_names,
        "sections": sections_with_domains,
        "domain_counts": domain_counts,
        "prose_content": prose_content,
        "notes": [
            "This document is branded CHS/CereCore, NOT Pulse Systems Inc.",
            "It describes Pulse v16.1, not the certified v8.02 product",
            "No field-level documentation within any CDA section",
            "No data types, value sets, or constraints documented",
            "Sample XML is a screenshot image, not extractable text",
        ]
    }


def parse_fhir_api_resources():
    """Extract FHIR resource types from the (g)(10) API documentation."""
    resources = [
        {"name": "AllergyIntolerance", "profile": "US Core AllergyIntolerance", "domain": "Allergies"},
        {"name": "CarePlan", "profile": "US Core CarePlan", "domain": "Care Plans / Goals"},
        {"name": "CareTeam", "profile": "US Core CareTeam", "domain": "Care Plans / Goals"},
        {"name": "DocumentReference", "profile": "US Core DocumentReference", "domain": "Clinical Notes"},
        {"name": "Encounter", "profile": "US Core Encounter", "domain": "Encounters"},
        {"name": "Goal", "profile": "US Core Goal", "domain": "Care Plans / Goals"},
        {"name": "Condition", "profile": "US Core Condition", "domain": "Problems / Conditions"},
        {"name": "Immunization", "profile": "US Core Immunization", "domain": "Immunizations"},
        {"name": "Observation (Laboratory)", "profile": "US Core Laboratory Result Observation", "domain": "Lab Results"},
        {"name": "DiagnosticReport", "profile": "US Core DiagnosticReport", "domain": "Lab Results"},
        {"name": "Medication", "profile": "US Core Medication", "domain": "Medications"},
        {"name": "MedicationRequest", "profile": "US Core MedicationRequest", "domain": "Medications"},
        {"name": "Patient", "profile": "US Core Patient", "domain": "Demographics"},
        {"name": "Procedure", "profile": "US Core Procedure", "domain": "Procedures"},
        {"name": "Provenance", "profile": "US Core Provenance", "domain": "Administrative"},
        {"name": "Observation (General)", "profile": "US Core Observation", "domain": "Vitals"},
        {"name": "ImplantableDevice", "profile": "US Core ImplantableDevice", "domain": "Implantable Devices"},
        {"name": "Location", "profile": "US Core Location", "domain": "Administrative"},
        {"name": "Organization", "profile": "US Core Organization", "domain": "Administrative"},
        {"name": "Practitioner", "profile": "US Core Practitioner", "domain": "Administrative"},
        {"name": "Observation (Vital Signs)", "profile": "FHIR Core VitalSigns", "domain": "Vitals"},
    ]
    return {
        "source_file": "Pulse-8.0-API-FHIR-Documentation.pdf",
        "document_type": "FHIR R4 API Documentation for §170.315(g)(10)",
        "pages": 41,
        "is_ehi_export": False,
        "note": "This is the (g)(10) FHIR API, NOT the (b)(10) EHI export",
        "resource_count": len(resources),
        "resources": resources,
    }


def parse_common_clinical_api():
    """Document the proprietary Common Clinical Data API."""
    return {
        "source_file": "Pulse_CommonClinicalDataAPI-002.pdf",
        "document_type": "Proprietary REST API for CCD/CCDA retrieval",
        "pages": 10,
        "is_ehi_export": False,
        "note": "This is a (g)(7)/(g)(9) API, NOT the (b)(10) EHI export",
        "api_details": {
            "method": "POST",
            "auth": "OAuth 2.0",
            "output_format": "base64-encoded XML CCD",
            "parameters": ["PersonNo", "FamilyNo", "StartDate", "EndDate"],
            "endpoints": {
                "auth": "https://{host}/PulseAuthenticationToken/token/generate",
                "data": "https://{host}/pulseunifiedapiToken/api/EXECUTE",
            }
        }
    }


def build_full_inventory():
    """Build the complete entity inventory."""
    docx_data = parse_docx()
    fhir_data = parse_fhir_api_resources()
    api_data = parse_common_clinical_api()

    inventory = {
        "product": "Pulse EHR",
        "developer": "Pulse Systems, Inc",
        "version_certified": "8.02",
        "chpl_id": "15.04.04.2837.Puls.08.03.1.240806",
        "analysis_date": "2026-02-16",
        "ehi_export_documentation_url": "https://pulseinc.com/terms-conditions-certification-costs-and-limitations/",
        "ehi_export_link_target": "https://www.hl7.org/fhir/us/core/uscdi.html",
        "ehi_export_link_target_is_vendor_docs": False,
        "ehi_export_link_target_description": "HL7 FHIR US Core USCDI reference page (external standard, not vendor documentation)",

        "vendor_hosted_ehi_documentation": None,
        "third_party_ehi_documentation": docx_data,

        "fhir_api_documentation": fhir_data,
        "proprietary_api_documentation": api_data,

        "export_format": "CDA XML",
        "export_type": "standard_projection",
        "model_type": "C-CDA / CDA clinical document",

        "summary_statistics": {
            "total_cda_sections_raw": docx_data["total_raw_sections"],
            "unique_cda_sections": docx_data["unique_sections"],
            "duplicate_sections": docx_data["duplicate_section_names"],
            "field_level_documentation": False,
            "data_types_documented": False,
            "value_sets_documented": False,
            "relationships_documented": False,
            "sample_data_provided": True,
            "sample_data_format": "XML screenshot image in DOCX (not extractable text)",
            "fhir_resources_in_g10_api": fhir_data["resource_count"],
        },

        "coverage_assessment": {
            "domains_with_evidence": [
                "Demographics", "Encounters", "Problems / Conditions",
                "Medications", "Allergies", "Immunizations", "Vitals",
                "Lab Results", "Procedures", "Clinical Notes",
                "Care Plans / Goals", "Insurance / Coverage",
                "Implantable Devices", "Social History", "Family History",
                "Orders / Referrals",
            ],
            "domains_missing": [
                "Claims / Billing (detailed)",
                "Payments",
                "Patient Communications / Portal Messages",
                "Specialty-specific data (custom flowsheets)",
            ],
            "domains_uncertain": [
                "Financial Data (section listed but CDA cannot represent detailed billing)",
            ],
        },

        "red_flags": [
            "Vendor's EHI export link points to HL7.org, not vendor documentation",
            "No vendor-hosted EHI export documentation exists",
            "Only substantive documentation is from a different organization (CHS) for a different version (16.1)",
            "Export is CDA XML — a clinical document standard, not a database export",
            "CDA format cannot represent billing, scheduling, or practice management data",
            "No field-level documentation for any CDA section",
            "No data dictionary of any kind",
            "Sample data is an image screenshot, not machine-readable",
        ]
    }

    return inventory


def build_summary_stats(inventory):
    """Build summary statistics for quick reference."""
    return {
        "classification": "Standard-based projection",
        "export_format": "CDA XML (Clinical Document Architecture)",
        "model_type": "Standard projection (C-CDA)",
        "entities": f"{inventory['summary_statistics']['unique_cda_sections']} CDA sections (not database entities)",
        "fields": "N/A (no field-level documentation)",
        "descriptions": "N/A (section names only, no field descriptions)",
        "sample_data": "Yes (XML screenshot in DOCX, not machine-readable)",
        "bulk_export": "Unclear (mentioned 'mass export' should be scheduled off-peak)",
        "domains_covered": "~13 of 17 applicable domains (clinical only, not billing/PM)",
        "documentation_quality": "Minimal/Absent from vendor; thin from third party",
    }


if __name__ == "__main__":
    inventory = build_full_inventory()
    stats = build_summary_stats(inventory)

    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "summary_stats.json"), "w") as f:
        json.dump(stats, f, indent=2)

    # Print summary
    print("=== SUMMARY ===")
    print(f"CDA sections (raw): {inventory['summary_statistics']['total_cda_sections_raw']}")
    print(f"CDA sections (unique): {inventory['summary_statistics']['unique_cda_sections']}")
    print(f"Duplicate sections: {inventory['summary_statistics']['duplicate_sections']}")
    print(f"Field-level docs: {inventory['summary_statistics']['field_level_documentation']}")
    print(f"FHIR resources in (g)(10) API: {inventory['summary_statistics']['fhir_resources_in_g10_api']}")
    print(f"\nDomain counts:")
    for d, c in sorted(inventory['third_party_ehi_documentation']['domain_counts'].items()):
        print(f"  {d}: {c} sections")
    print(f"\nRed flags: {len(inventory['red_flags'])}")
    for rf in inventory['red_flags']:
        print(f"  - {rf}")
    print(f"\nFiles written:")
    print(f"  full-entity-inventory.json")
    print(f"  summary_stats.json")
