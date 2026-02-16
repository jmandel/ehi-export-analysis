#!/usr/bin/env python3
"""Produce the definitive entity inventory for OmniMD EHI export.

Reconciles sections across three sources:
1. EHI Export Word doc (20 C-CDA sections)
2. OpenAPI PDF GetPatientData params (33 section toggles)
3. Interactive API UI selected sections (20 sections)
"""

import json
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent

# 20 C-CDA sections from the EHI Export doc (primary/canonical list)
EHI_DOC_SECTIONS = [
    "ADVANCE DIRECTIVES",
    "ALLERGIES, ADVERSE REACTIONS, ALERTS",
    "ASSESSMENTS",
    "ENCOUNTERS",
    "FAMILY HISTORY",
    "FUNCTIONAL STATUS",
    "IMMUNIZATIONS",
    "INSTRUCTIONS",
    "MEDICAL EQUIPMENT",
    "HISTORY OF MEDICATION",
    "MEDICATION ADMINISTERED",
    "INSURANCE PROVIDERS",
    "TREATMENT PLAN",
    "PROBLEM LIST",
    "PROCEDURES",
    "PROGRESS NOTE",
    "CHIEF COMPLAINT AND REASON FOR VISIT",
    "LAB RESULTS",
    "SOCIAL HISTORY",
    "VITAL SIGNS",
]

# 20 sections from the interactive API UI (matching EHI doc)
API_UI_SECTIONS = [
    "AdvanceDirective", "Allergy", "Assessment", "Encounter",
    "FamilyHistory", "FunctionalStatus", "Immunization", "Instruction",
    "MedicalEquipment", "Medication", "MedicationsAdministered", "Payer",
    "PlanOfCare", "Problems", "Procedure", "ProgressNote",
    "ReasonForVisit", "Results", "SocialHistory", "Vital",
]

# 33 section toggles from OpenAPI PDF GetPatientData endpoint
PDF_SECTION_TOGGLES = [
    "PatientAll", "AdvanceDirective", "Allergy", "Encounter",
    "FamilyHistory", "Functional", "Immunization", "Instructions",
    "Results", "Medication", "MedicationAdministered", "Payer",
    "PlanOfCare", "Problem", "Procedure", "ReasonForReferral",
    "SocialHistory", "Vital", "Pregnancy", "ReasonForVisit",
    "CarePlan", "CareTeam", "EncompassingEncounter", "ClinicInformation",
    "ProgressNote", "Assessment", "FunctionStatus", "MedicalEquipment",
    "PlannedMedication", "PatientContact", "PlannedAppointments",
    "PlannedProcedure", "FunctionalStatus",
]

# Mapping from EHI doc section to API parameter name and domain
SECTION_MAP = [
    {"ehi_doc": "ADVANCE DIRECTIVES", "api_param": "AdvanceDirective", "domain": "Consents/Directives"},
    {"ehi_doc": "ALLERGIES, ADVERSE REACTIONS, ALERTS", "api_param": "Allergy", "domain": "Allergies"},
    {"ehi_doc": "ASSESSMENTS", "api_param": "Assessment", "domain": "Clinical Notes"},
    {"ehi_doc": "ENCOUNTERS", "api_param": "Encounter", "domain": "Encounters"},
    {"ehi_doc": "FAMILY HISTORY", "api_param": "FamilyHistory", "domain": "Family History"},
    {"ehi_doc": "FUNCTIONAL STATUS", "api_param": "FunctionalStatus", "domain": "Functional Status"},
    {"ehi_doc": "IMMUNIZATIONS", "api_param": "Immunization", "domain": "Immunizations"},
    {"ehi_doc": "INSTRUCTIONS", "api_param": "Instruction", "domain": "Patient Education"},
    {"ehi_doc": "MEDICAL EQUIPMENT", "api_param": "MedicalEquipment", "domain": "Medical Equipment"},
    {"ehi_doc": "HISTORY OF MEDICATION", "api_param": "Medication", "domain": "Medications"},
    {"ehi_doc": "MEDICATION ADMINISTERED", "api_param": "MedicationsAdministered", "domain": "Medications"},
    {"ehi_doc": "INSURANCE PROVIDERS", "api_param": "Payer", "domain": "Insurance/Coverage"},
    {"ehi_doc": "TREATMENT PLAN", "api_param": "PlanOfCare", "domain": "Care Plans"},
    {"ehi_doc": "PROBLEM LIST", "api_param": "Problems", "domain": "Problems/Conditions"},
    {"ehi_doc": "PROCEDURES", "api_param": "Procedure", "domain": "Procedures"},
    {"ehi_doc": "PROGRESS NOTE", "api_param": "ProgressNote", "domain": "Clinical Notes"},
    {"ehi_doc": "CHIEF COMPLAINT AND REASON FOR VISIT", "api_param": "ReasonForVisit", "domain": "Clinical Notes"},
    {"ehi_doc": "LAB RESULTS", "api_param": "Results", "domain": "Lab Results"},
    {"ehi_doc": "SOCIAL HISTORY", "api_param": "SocialHistory", "domain": "Social History"},
    {"ehi_doc": "VITAL SIGNS", "api_param": "Vital", "domain": "Vitals"},
]

# Additional toggles in PDF that go beyond the 20 core EHI doc sections
ADDITIONAL_PDF_SECTIONS = [
    {"api_param": "PatientAll", "domain": "Meta", "note": "Toggle to return full C-CDA; not a section itself"},
    {"api_param": "ReasonForReferral", "domain": "Referrals", "note": "Additional C-CDA section not in EHI doc"},
    {"api_param": "Pregnancy", "domain": "Clinical Notes", "note": "Additional toggle not in EHI doc"},
    {"api_param": "CarePlan", "domain": "Care Plans", "note": "Likely same as PlanOfCare/Treatment Plan"},
    {"api_param": "CareTeam", "domain": "Care Team", "note": "Additional toggle not in EHI doc"},
    {"api_param": "EncompassingEncounter", "domain": "Encounters", "note": "CDA encompassing encounter header element"},
    {"api_param": "ClinicInformation", "domain": "Practice Information", "note": "Practice/clinic metadata"},
    {"api_param": "PlannedMedication", "domain": "Medications", "note": "Future/planned medications"},
    {"api_param": "PatientContact", "domain": "Demographics", "note": "Patient contact information"},
    {"api_param": "PlannedAppointments", "domain": "Scheduling", "note": "Future appointments"},
    {"api_param": "PlannedProcedure", "domain": "Procedures", "note": "Future/planned procedures"},
]

def build_inventory():
    entities = []
    
    # Core 20 sections from EHI doc
    for s in SECTION_MAP:
        entities.append({
            "name": s["ehi_doc"],
            "api_parameter": s["api_param"],
            "domain": s["domain"],
            "source": "EHI Export Document + API UI + OpenAPI PDF",
            "format": "C-CDA XML section (CDA 2.1)",
            "field_count": None,
            "fields_with_descriptions": 0,
            "types_documented": False,
            "value_sets_documented": False,
            "relationships_documented": False,
            "sample_data": False,
            "documentation_level": "section name only"
        })
    
    # Additional sections from PDF only
    for s in ADDITIONAL_PDF_SECTIONS:
        entities.append({
            "name": s["api_param"],
            "api_parameter": s["api_param"],
            "domain": s["domain"],
            "source": "OpenAPI PDF only (not in EHI export doc)",
            "format": "C-CDA XML section/element",
            "field_count": None,
            "fields_with_descriptions": 0,
            "types_documented": False,
            "value_sets_documented": False,
            "relationships_documented": False,
            "sample_data": False,
            "documentation_level": "parameter name only",
            "note": s["note"]
        })
    
    # Domain summary
    domains = {}
    for e in entities:
        d = e["domain"]
        if d not in domains:
            domains[d] = {"count": 0, "entities": []}
        domains[d]["count"] += 1
        domains[d]["entities"].append(e["name"])
    
    inventory = {
        "vendor": "OmniMD Inc.",
        "product": "OmniMD",
        "export_type": "Standard-based projection (C-CDA + FHIR reference)",
        "has_data_dictionary": False,
        "has_native_model": False,
        "export_format": "HL7 C-CDA XML (CDA 2.1), USCDI v1",
        "secondary_format": "FHIR R4 Bulk Data (by reference to g(10) only)",
        "core_section_count": 20,
        "additional_pdf_sections": len(ADDITIONAL_PDF_SECTIONS),
        "total_entities": len(entities),
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "percent_fields_with_descriptions": "N/A",
        "entities": entities,
        "domain_summary": domains,
        "source_reconciliation": {
            "ehi_doc_sections": 20,
            "api_ui_sections": 20,
            "pdf_section_toggles": 33,
            "note": "EHI doc and API UI list identical 20 sections. PDF has 33 toggles including 11 additional sections (some are aliases like PatientAll, some are genuinely additional like Pregnancy, CareTeam, PlannedMedication)."
        },
        "missing_from_export": [
            "Billing/claims data (claims, charges, payments, denials)",
            "E-prescribing transaction records (EPCS, pharmacy network)",
            "Patient portal messages and communications",
            "Telehealth/video visit records",
            "Remote patient monitoring data",
            "Documents/attachments/scanned records",
            "Specialty-specific templates and assessments (40+ specialties claimed)",
            "AI-generated documentation (AI Scribe, AI Clinician)",
            "Custom forms and questionnaires",
            "Order history and referral tracking"
        ]
    }
    
    with open(OUTPUT / "full-entity-inventory.json", 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(json.dumps({
        "core_sections": inventory["core_section_count"],
        "additional_pdf_sections": inventory["additional_pdf_sections"],
        "total_entities": inventory["total_entities"],
        "total_fields": inventory["total_fields"],
        "has_data_dictionary": inventory["has_data_dictionary"],
        "domain_count": len(domains),
        "domains": {k: v["count"] for k, v in domains.items()}
    }, indent=2))

if __name__ == "__main__":
    build_inventory()
