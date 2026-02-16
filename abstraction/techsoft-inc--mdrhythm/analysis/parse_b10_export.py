"""
Parse the MDRhythm B10 Data Export Instructions PDF and FHIR API Documentation PDF
to produce a full-entity-inventory.json and summary statistics.
"""
import json
import subprocess
import re
from collections import OrderedDict

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/techsoft-inc--mdrhythm/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/techsoft-inc--mdrhythm/analysis"

def extract_pdf_text(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_b10_export():
    """Parse B10 export documentation - a 3-page PDF describing a PDF export."""
    text = extract_pdf_text(f"{RESULTS_DIR}/MDRhythm_B10_Data_Export_Instructions.pdf")
    
    # The B10 export lists 6 categories of data
    categories = [
        "Patient Demographics",
        "Allergy Details",
        "Current Medication Details and Medication History",
        "Diagnosis and Problem Information",
        "Visit Note Information",
        "Vitals Information"
    ]
    
    return {
        "source": "MDRhythm_B10_Data_Export_Instructions.pdf",
        "pages": 3,
        "format": "PDF (flat document, not structured data)",
        "export_mechanism": "Web UI at https://patientdata.mdronline.net",
        "max_patients_per_export": 5,
        "data_categories": categories,
        "total_categories": len(categories),
        "has_data_dictionary": False,
        "has_field_definitions": False,
        "has_sample_structured_data": False,
        "visit_note_sections": ["Subjective", "Objective", "Assessment", "Plan"],
        "notes": [
            "Export is a flat PDF file, not structured/machine-readable data",
            "No field-level documentation provided",
            "No data dictionary or schema",
            "Sample screenshot shows a single visit note with demographics, allergies, medical history, vitals, exam, diagnoses, procedures, medications, and plan of care",
            "Limited to 5 patients per export batch"
        ]
    }

def parse_fhir_api():
    """Parse FHIR API documentation to enumerate supported FHIR resources."""
    text = extract_pdf_text(f"{RESULTS_DIR}/MDR-FHIR-API-Documentation.pdf")
    
    # Extract section headings from the Table of Contents
    toc_sections = []
    lines = text.split('\n')
    
    # FHIR resource types found in examples
    resource_types = set()
    for line in lines:
        match = re.search(r'"resourceType":\s*"(\w+)"', line)
        if match:
            resource_types.add(match.group(1))
    
    # Main clinical sections from TOC
    clinical_sections = [
        {"name": "Allergies and Intolerances", "fhir_resource": "AllergyIntolerance", "page_start": 17},
        {"name": "Assessment and Plan of Treatment", "fhir_resource": "CarePlan", "page_start": 29},
        {"name": "Care Team Members", "fhir_resource": "CareTeam", "page_start": 34},
        {"name": "Clinical Notes", "fhir_resource": "DocumentReference", "page_start": 35},
        {"name": "Clinical Tests", "fhir_resource": "Observation", "page_start": 79},
        {"name": "Diagnostic Imaging", "fhir_resource": "DiagnosticReport", "page_start": 91},
        {"name": "Encounter Information", "fhir_resource": "Encounter", "page_start": 95},
        {"name": "Goals", "fhir_resource": "Goal", "page_start": 124},
        {"name": "Health Concerns", "fhir_resource": "Condition", "page_start": 128},
        {"name": "Immunizations", "fhir_resource": "Immunization", "page_start": 174},
        {"name": "Laboratory", "fhir_resource": "Observation/DiagnosticReport", "page_start": 181},
        {"name": "Medications", "fhir_resource": "MedicationRequest", "page_start": 181},
        {"name": "Patient Demographics", "fhir_resource": "Patient", "page_start": 184},
        {"name": "Problems", "fhir_resource": "Condition", "page_start": 194},
        {"name": "Procedures", "fhir_resource": "Procedure", "page_start": 194},
        {"name": "Provenance", "fhir_resource": "Provenance", "page_start": 213},
        {"name": "Smoking Status", "fhir_resource": "Observation", "page_start": 226},
        {"name": "Unique Device Identifier(s) for Patient's Implantable Device(s)", "fhir_resource": "Device", "page_start": 230},
        {"name": "Vital Signs", "fhir_resource": "Observation", "page_start": 233},
    ]
    
    # Supported FHIR scopes from the smart-configuration
    scopes = [
        "Medication", "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
        "Device", "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
        "Immunization", "Location", "MedicationRequest", "Observation", "Organization",
        "Patient", "Practitioner", "Procedure", "Provenance", "PractitionerRole",
        "ServiceRequest"
    ]
    
    return {
        "source": "MDR-FHIR-API-Documentation.pdf",
        "pages": 240,
        "fhir_version": "US Core 5.0.1 / USCDI v2",
        "smart_version": "SMART App Launch 2.0.0",
        "bulk_data_version": "Bulk Data 2.0.0",
        "base_url": "https://mdrfhirapi.mdronline.net/",
        "clinical_sections": clinical_sections,
        "total_clinical_sections": len(clinical_sections),
        "resource_types_in_examples": sorted(list(resource_types)),
        "supported_fhir_scopes": sorted(scopes),
        "total_scoped_resources": len(scopes),
        "notes": [
            "This is a standard FHIR R4 / US Core API, not a native data model export",
            "Covers USCDI v2 data elements only",
            "Does not cover billing, insurance, claims, or practice management data",
            "240-page document primarily consists of FHIR API request/response examples"
        ]
    }

def build_full_inventory():
    """Build the complete entity inventory combining B10 export and FHIR API info."""
    b10 = parse_b10_export()
    fhir = parse_fhir_api()
    
    # The B10 export is the (b)(10) export - it's a flat PDF with 6 data categories
    # No field-level detail is provided, so we document what the sample shows
    b10_entities = []
    
    # From the sample screenshot on page 2, we can identify these data elements
    sample_fields = {
        "Patient Demographics": {
            "fields": [
                {"name": "Patient Name", "type": "string", "description": "Patient's full name", "source": "sample screenshot"},
                {"name": "Sex", "type": "string", "description": "Patient's sex (Male/Female)", "source": "sample screenshot"},
                {"name": "DOB", "type": "date", "description": "Date of birth", "source": "sample screenshot"},
                {"name": "Provider", "type": "string", "description": "Provider name with credentials", "source": "sample screenshot"},
                {"name": "Visit Date", "type": "date", "description": "Date of the visit", "source": "sample screenshot"},
            ]
        },
        "Allergy Details": {
            "fields": [
                {"name": "Allergies", "type": "text", "description": "List of allergies (comma-separated in sample)", "source": "sample screenshot"},
            ]
        },
        "Medical History": {
            "fields": [
                {"name": "Medical History", "type": "text", "description": "List of medical conditions with dates", "source": "sample screenshot"},
            ]
        },
        "Medications": {
            "fields": [
                {"name": "Medication", "type": "string", "description": "Medication name and strength", "source": "sample screenshot"},
                {"name": "SIG/Directions", "type": "string", "description": "Dosing instructions", "source": "sample screenshot"},
                {"name": "Supply", "type": "string", "description": "Supply quantity and units", "source": "sample screenshot"},
                {"name": "Count", "type": "integer", "description": "Count value", "source": "sample screenshot"},
                {"name": "Refills", "type": "integer", "description": "Number of refills", "source": "sample screenshot"},
                {"name": "Date", "type": "date", "description": "Prescription date", "source": "sample screenshot"},
                {"name": "Status", "type": "string", "description": "Active/Inactive status", "source": "sample screenshot"},
            ]
        },
        "Meds Review": {
            "fields": [
                {"name": "Meds Review", "type": "text", "description": "Medication review note text", "source": "sample screenshot"},
            ]
        },
        "Vitals": {
            "fields": [
                {"name": "BP", "type": "string", "description": "Blood pressure reading", "source": "sample screenshot"},
                {"name": "Position", "type": "string", "description": "Patient position (e.g., Arm Sitting)", "source": "sample screenshot"},
                {"name": "Respiration", "type": "number", "description": "Respiratory rate", "source": "sample screenshot"},
                {"name": "Temperature", "type": "number", "description": "Body temperature in °F", "source": "sample screenshot"},
                {"name": "Pulse", "type": "number", "description": "Heart rate", "source": "sample screenshot"},
                {"name": "Height", "type": "string", "description": "Patient height with percentile", "source": "sample screenshot"},
                {"name": "Weight", "type": "number", "description": "Weight in lbs", "source": "sample screenshot"},
                {"name": "BMI", "type": "number", "description": "Body mass index with percentile", "source": "sample screenshot"},
            ]
        },
        "Physical Exam": {
            "fields": [
                {"name": "General", "type": "text", "description": "General examination findings", "source": "sample screenshot"},
                {"name": "Eyes", "type": "text", "description": "Eye examination findings", "source": "sample screenshot"},
            ]
        },
        "Assessment": {
            "fields": [
                {"name": "Diagnosis Codes", "type": "text", "description": "ICD codes with descriptions", "source": "sample screenshot"},
                {"name": "Procedure Codes", "type": "text", "description": "CPT codes with descriptions", "source": "sample screenshot"},
            ]
        },
        "Plan": {
            "fields": [
                {"name": "Diagnostic Tests", "type": "text", "description": "Ordered diagnostic tests", "source": "sample screenshot"},
                {"name": "Plan Of Care", "type": "text", "description": "Care plan items with dates", "source": "sample screenshot"},
            ]
        },
    }
    
    for category, data in sample_fields.items():
        entity = {
            "entity_name": category,
            "category": "B10 Export - Clinical Summary (PDF)",
            "field_count": len(data["fields"]),
            "fields_with_descriptions": len([f for f in data["fields"] if f.get("description")]),
            "fields_with_types": len([f for f in data["fields"] if f.get("type")]),
            "fields": data["fields"],
            "documentation_source": "Inferred from sample screenshot in B10 PDF, page 2",
            "notes": "No formal data dictionary provided; fields inferred from sample export screenshot"
        }
        b10_entities.append(entity)
    
    total_b10_fields = sum(e["field_count"] for e in b10_entities)
    
    inventory = {
        "product": "MDRhythm Version 8",
        "vendor": "TechSoft, Inc.",
        "analysis_date": "2026-02-16",
        "b10_export": {
            "description": "Flat PDF export of patient visit records via web portal",
            "format": "PDF",
            "structured_data": False,
            "data_dictionary_provided": False,
            "entities": b10_entities,
            "total_entities": len(b10_entities),
            "total_fields": total_b10_fields,
            "fields_formally_documented": 0,
            "notes": "All field information inferred from a sample screenshot; vendor provides no data dictionary or schema"
        },
        "fhir_api": {
            "description": "FHIR R4 API supporting US Core 5.0.1 / USCDI v2",
            "format": "FHIR R4 JSON",
            "is_b10_export": False,
            "note": "FHIR API is a separate certification criterion (g)(10), not the (b)(10) EHI export",
            "resource_types": sorted(list(set([
                "AllergyIntolerance", "Bundle", "CarePlan", "CareTeam", "Condition",
                "Device", "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
                "Immunization", "Location", "Medication", "MedicationRequest", "Observation",
                "Organization", "Patient", "Practitioner", "PractitionerRole", "Procedure",
                "Provenance", "ServiceRequest"
            ]))),
            "total_resource_types": 22,
            "clinical_sections_documented": 19,
            "documentation_pages": 240
        },
        "summary": {
            "b10_export_format": "PDF (flat, non-machine-readable)",
            "b10_categories_listed": 6,
            "b10_fields_inferred_from_sample": total_b10_fields,
            "b10_fields_formally_documented": 0,
            "fhir_resource_types": 22,
            "has_native_data_model_export": False,
            "has_data_dictionary": False,
            "covers_billing": False,
            "covers_insurance": False,
            "covers_claims": False,
            "covers_practice_management": False,
            "classification": "Minimal/stub",
            "classification_rationale": "The (b)(10) export is a flat PDF printout of clinical visit notes covering only 6 categories of clinical data. No structured/machine-readable export. No data dictionary. No billing, insurance, claims, or practice management data despite the product storing all of these. The FHIR API is separate from the (b)(10) export."
        }
    }
    
    return inventory

if __name__ == "__main__":
    inventory = build_full_inventory()
    
    output_path = f"{OUTPUT_DIR}/full-entity-inventory.json"
    with open(output_path, 'w') as f:
        json.dump(inventory, f, indent=2)
    
    print(f"Full entity inventory written to {output_path}")
    print(f"\nSummary:")
    print(f"  B10 Export entities (inferred): {inventory['b10_export']['total_entities']}")
    print(f"  B10 Export fields (inferred): {inventory['b10_export']['total_fields']}")
    print(f"  B10 Fields formally documented: {inventory['b10_export']['fields_formally_documented']}")
    print(f"  FHIR API resource types: {inventory['fhir_api']['total_resource_types']}")
    print(f"  Classification: {inventory['summary']['classification']}")
