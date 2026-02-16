"""
Parse all KanTime Health EHI export artifacts and produce a full inventory JSON.

Since KanTime provides no data dictionary, this script documents what is actually
available: the C-CDA sections from the Patient API, the patient search fields,
and the FHIR resources from the SMART on FHIR doc.
"""

import json

# C-CDA sections available via Patient API (from KanTime_Patient_API.pdf)
ccda_sections = [
    {"section_api_name": "all", "display_name": "All", "type": "C-CDA 2.1"},
    {"section_api_name": "demographics", "display_name": "Patient Demographics", "type": "C-CDA 2.1"},
    {"section_api_name": "careteam", "display_name": "Care Team", "type": "C-CDA 2.1"},
    {"section_api_name": "allergies", "display_name": "Allergies and Intolerances", "type": "C-CDA 2.1"},
    {"section_api_name": "assessments", "display_name": "Assessment", "type": "C-CDA 2.1"},
    {"section_api_name": "encounters", "display_name": "Encounters", "type": "C-CDA 2.1"},
    {"section_api_name": "functionalstatus", "display_name": "Functional Status", "type": "C-CDA 2.1"},
    {"section_api_name": "goals", "display_name": "Goals", "type": "C-CDA 2.1"},
    {"section_api_name": "healthconcerns", "display_name": "Health Concerns", "type": "C-CDA 2.1"},
    {"section_api_name": "immunizations", "display_name": "Immunizations", "type": "C-CDA 2.1"},
    {"section_api_name": "medicalequipment", "display_name": "Medical Equipment", "type": "C-CDA 2.1"},
    {"section_api_name": "medications", "display_name": "Medications", "type": "C-CDA 2.1"},
    {"section_api_name": "mentalstatus", "display_name": "Mental Status", "type": "C-CDA 2.1"},
    {"section_api_name": "planoftreatment", "display_name": "Plan of Treatment", "type": "C-CDA 2.1"},
    {"section_api_name": "problem", "display_name": "Problem", "type": "C-CDA 2.1"},
    {"section_api_name": "procedures", "display_name": "Procedures", "type": "C-CDA 2.1"},
    {"section_api_name": "reasonforreferral", "display_name": "Reason for Referral", "type": "C-CDA 2.1"},
    {"section_api_name": "results", "display_name": "Results", "type": "C-CDA 2.1"},
    {"section_api_name": "socialhistory", "display_name": "Social History", "type": "C-CDA 2.1"},
    {"section_api_name": "vitalsigns", "display_name": "Vital Signs", "type": "C-CDA 2.1"},
    {"section_api_name": "consultationnote", "display_name": "Consultation Note", "type": "C-CDA 2.1"},
    {"section_api_name": "progressnote", "display_name": "Progress Note", "type": "C-CDA 2.1"},
    {"section_api_name": "historyandphysicalnote", "display_name": "History and Physical Note", "type": "C-CDA 2.1"},
]

# Patient search response fields (from sample in KanTime_Patient_API.pdf)
patient_search_fields = [
    {"name": "PaperChartNumber", "type": "string", "description": "Paper chart number / identifier"},
    {"name": "MRN", "type": "string", "description": "Medical Record Number"},
    {"name": "DateOfBirth", "type": "string", "description": "Date of birth (MM/DD/YYYY)"},
    {"name": "Gender", "type": "string", "description": "Gender code (M/F)"},
    {"name": "FirstName", "type": "string", "description": "Patient first name"},
    {"name": "LastName", "type": "string", "description": "Patient last name"},
    {"name": "MiddleName", "type": "string", "description": "Patient middle name"},
    {"name": "AddressLine1", "type": "string", "description": "Address line 1"},
    {"name": "AddressLine2", "type": "string", "description": "Address line 2"},
    {"name": "City", "type": "string", "description": "City"},
    {"name": "State", "type": "string", "description": "State"},
    {"name": "Zipcode", "type": "string", "description": "ZIP code"},
    {"name": "EmailAddress", "type": "string", "description": "Email address"},
    {"name": "HomePhoneNumber", "type": "string", "description": "Home phone number"},
    {"name": "WorkPhoneNumber", "type": "string", "description": "Work phone number (nullable)"},
    {"name": "MobileNumber", "type": "string", "description": "Mobile phone number"},
    {"name": "SSN", "type": "string", "description": "Social Security Number"},
    {"name": "MaritalStatus", "type": "string", "description": "Marital status (nullable)"},
]

# FHIR resources from SMART on FHIR API doc (g)(10) - NOT the EHI export
fhir_resources = [
    "Patient", "AllergyIntolerance", "CarePlan", "CareTeam",
    "Condition (Problems/Health Concern)", "Device (Implantable)",
    "DiagnosticReport", "DocumentReference", "Goal", "Immunization",
    "Medication", "MedicationDispense", "Observation (Lab Results)",
    "Observation (Smoking Status)", "Observation (Vital Signs)",
    "Observation (General)", "Organization", "Procedure", "Provenance",
    "ServiceRequest", "Coverage", "Specimen", "RelatedPerson",
]

# Billing export - from EHI_Tool_Documentation.pdf
billing_export = {
    "description": "Patient claims and payments",
    "formats": ["CSV", "XLSX", "PDF"],
    "fields_documented": 0,
    "field_names_listed": False,
    "schema_provided": False,
    "sample_data_provided": False,
    "note": "The EHI documentation states billing data can be exported but provides zero detail about what fields, columns, or data elements are included."
}

# Build the full inventory
inventory = {
    "vendor": "Kanrad Technologies Inc",
    "product": "KanTime Health",
    "version": "1.0",
    "chpl_id": "15.04.04.3096.KanH.01.01.1.230118",
    "analysis_date": "2026-02-15",
    "summary": {
        "total_artifacts": 4,
        "ehi_specific_artifacts": 2,
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "clinical_export_format": "C-CDA 2.1 Release 2 (USCDI v1)",
        "billing_export_format": "CSV, XLSX, or PDF (undocumented)",
        "ccda_sections_count": len([s for s in ccda_sections if s["section_api_name"] != "all"]),
        "patient_search_fields_count": len(patient_search_fields),
        "billing_fields_documented": 0,
        "total_documented_fields": len(patient_search_fields),
        "fields_with_descriptions": len(patient_search_fields),
    },
    "clinical_export": {
        "mechanism": "REST API (Patient API)",
        "format": "C-CDA 2.1 Release 2",
        "standard": "USCDI v1",
        "authentication": "Basic Auth -> JWT Bearer token",
        "per_patient": True,
        "bulk_export": False,
        "date_range_filtering": True,
        "sections": ccda_sections,
    },
    "billing_export": billing_export,
    "patient_search_api": {
        "fields": patient_search_fields,
        "max_results": 30,
        "search_parameters": ["MRN", "Date of birth", "First name", "Last name"],
    },
    "fhir_api_g10": {
        "note": "This is the (g)(10) FHIR API, NOT the (b)(10) EHI export",
        "resources": fhir_resources,
        "resource_count": len(fhir_resources),
    },
    "artifacts": [
        {
            "filename": "EHI_Tool_Documentation.pdf",
            "pages": 1,
            "size_bytes": 42570,
            "description": "Core EHI export documentation - 5 sentences describing clinical (C-CDA) and billing (CSV/XLSX/PDF) exports. No data dictionary, no field definitions, no schema.",
            "relevance": "primary",
            "content_type": "prose_only",
        },
        {
            "filename": "KanTime_Patient_API.pdf",
            "pages": 14,
            "size_bytes": 255054,
            "description": "REST API documentation for retrieving patient clinical data as C-CDA XML. Includes authentication, search, and CCDA retrieval endpoints with curl examples and sample responses.",
            "relevance": "primary",
            "content_type": "api_documentation",
        },
        {
            "filename": "SmartOnFHIRAPIDoc.pdf",
            "pages": 66,
            "size_bytes": 685961,
            "description": "SMART on FHIR API documentation for (g)(10) compliance. NOT the (b)(10) EHI export. Covers standard US Core FHIR resources.",
            "relevance": "contextual_only",
            "content_type": "api_documentation",
        },
        {
            "filename": "fhir-base-urls-1.json",
            "pages": None,
            "size_bytes": 3719,
            "description": "FHIR R4 endpoint Bundle JSON listing 2 KanTime FHIR service base URLs. Part of (g)(10) compliance.",
            "relevance": "contextual_only",
            "content_type": "json",
        },
    ],
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/kanrad-technologies-inc--kantime-health/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary stats
print(f"Artifacts: {inventory['summary']['total_artifacts']}")
print(f"EHI-specific artifacts: {inventory['summary']['ehi_specific_artifacts']}")
print(f"C-CDA sections: {inventory['summary']['ccda_sections_count']}")
print(f"Patient search fields documented: {inventory['summary']['patient_search_fields_count']}")
print(f"Billing fields documented: {inventory['summary']['billing_fields_documented']}")
print(f"Has data dictionary: {inventory['summary']['has_data_dictionary']}")
print(f"Has sample data: {inventory['summary']['has_sample_data']}")
print(f"Has schema: {inventory['summary']['has_schema']}")
print(f"\nFull inventory written to: {output_path}")
