#!/usr/bin/env python3
"""Parse MaximEyes EHI export artifacts and produce entity inventory."""

import json
import subprocess
import re

def parse_fhir_api_pdf():
    """Extract FHIR resource types and their USCDI mappings from the FHIR API PDF."""
    result = subprocess.run(
        ["pdftotext", "-layout", "../downloads/MaximEyes-FHIR-API-Documentation.pdf", "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Resources documented in the FHIR API PDF with their USCDI data elements
    resources = {
        "AllergyIntolerance": {
            "uscdi_classes": ["Allergies and Intolerances"],
            "uscdi_elements": ["Substance (Medication)", "Substance (Drug Class)", "Reaction"],
            "documented_in_pdf": True,
            "search_params": ["_id", "patient", "patient+clinical-status"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.12-13"
        },
        "CarePlan": {
            "uscdi_classes": ["Assessment and Plan of Treatment"],
            "uscdi_elements": ["Assessment and Plan of Treatment"],
            "documented_in_pdf": True,
            "search_params": ["patient+category", "patient+category+date", "patient+category+status", "patient+category+date+status"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.13-14"
        },
        "CareTeam": {
            "uscdi_classes": ["Care Team Members"],
            "uscdi_elements": ["Care Team"],
            "documented_in_pdf": True,
            "search_params": ["patient+status"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.15"
        },
        "Condition": {
            "uscdi_classes": ["Problems", "Health Concerns", "Encounter Diagnoses"],
            "uscdi_elements": ["Health Concerns", "Problems"],
            "documented_in_pdf": True,
            "search_params": ["patient", "patient+status", "patient+category", "patient+code", "patient+onset-date"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.15-16"
        },
        "Device": {
            "uscdi_classes": ["Implantable Devices"],
            "uscdi_elements": ["Unique Device Identifier(s) for Patients' Implantable Device(s)"],
            "documented_in_pdf": True,
            "search_params": ["patient", "patient+type"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.17"
        },
        "DiagnosticReport": {
            "uscdi_classes": ["Laboratory", "Clinical Notes"],
            "uscdi_elements": ["Imaging Narrative", "Laboratory Report Narrative", "Pathology Report Narrative", "Procedure Note"],
            "documented_in_pdf": True,
            "search_params": ["patient", "patient+category", "patient+code", "patient+category+date", "patient+status", "patient+code+date"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.17-18"
        },
        "DocumentReference": {
            "uscdi_classes": ["Clinical Notes"],
            "uscdi_elements": ["Consultation Note", "Discharge Summary Note", "History & Physical", "Progress Note"],
            "documented_in_pdf": True,
            "search_params": ["_id", "patient", "patient+type", "patient+category+date", "patient+category", "patient+status", "patient+type+period"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.19-20"
        },
        "Encounter": {
            "uscdi_classes": ["Encounters"],
            "uscdi_elements": ["Encounter Information"],
            "documented_in_pdf": True,
            "search_params": ["_id", "patient", "date+patient", "identifier", "class+patient", "patient+type", "patient+status"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.20"
        },
        "Goal": {
            "uscdi_classes": ["Goals"],
            "uscdi_elements": ["Patient Goals"],
            "documented_in_pdf": True,
            "search_params": ["patient", "patient+target-date", "patient+lifecycle-status"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.21"
        },
        "Immunization": {
            "uscdi_classes": ["Immunizations"],
            "uscdi_elements": ["Immunization"],
            "documented_in_pdf": True,
            "search_params": ["patient", "patient+status", "patient+date"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.22"
        },
        "Location": {
            "uscdi_classes": ["Facility Information"],
            "uscdi_elements": [],
            "documented_in_pdf": True,
            "search_params": ["name", "address", "address-state", "address-city", "address-postalCode"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.22-23"
        },
        "Medication": {
            "uscdi_classes": ["Medications"],
            "uscdi_elements": [],
            "documented_in_pdf": True,
            "search_params": ["_id"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf (referenced via MedicationRequest _include)"
        },
        "MedicationRequest": {
            "uscdi_classes": ["Medications"],
            "uscdi_elements": [],
            "documented_in_pdf": True,
            "search_params": ["patient+intent", "patient+intent+status", "patient+intent+encounter", "patient+intent+authoredon"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.23-24"
        },
        "Observation": {
            "uscdi_classes": ["Laboratory", "Vital Signs", "Social History", "Clinical Tests"],
            "uscdi_elements": ["Tests", "Values/Results", "Smoking Status", "Vital Signs (multiple profiles)"],
            "documented_in_pdf": True,
            "search_params": ["patient+category", "patient+code", "patient+category+date", "patient+category+status"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.25-35"
        },
        "Organization": {
            "uscdi_classes": ["Insurance/Payer"],
            "uscdi_elements": [],
            "documented_in_pdf": True,
            "search_params": ["name", "address"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.35-36"
        },
        "Patient": {
            "uscdi_classes": ["Patient Demographics"],
            "uscdi_elements": ["First Name", "Middle Name", "Last Name", "Previous Name", "Suffix", "Birth Sex", "Date of Birth", "Race", "Ethnicity", "Preferred Language", "Address", "Phone Number"],
            "documented_in_pdf": True,
            "search_params": ["_id", "identifier", "name", "birthdate+name", "gender+name", "birthdate+family", "family+gender"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.36-37"
        },
        "Practitioner": {
            "uscdi_classes": ["Care Team Members"],
            "uscdi_elements": [],
            "documented_in_pdf": True,
            "search_params": ["name", "identifier"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.37-38"
        },
        "PractitionerRole": {
            "uscdi_classes": ["Care Team Members"],
            "uscdi_elements": [],
            "documented_in_pdf": True,
            "search_params": ["specialty", "practitioner"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.38"
        },
        "Procedure": {
            "uscdi_classes": ["Procedures"],
            "uscdi_elements": ["Procedures"],
            "documented_in_pdf": True,
            "search_params": ["patient", "patient+date", "patient+status", "patient+code+date"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.38-39"
        },
        "Provenance": {
            "uscdi_classes": ["Provenance"],
            "uscdi_elements": ["Author Time Stamp", "Author Organization"],
            "documented_in_pdf": True,
            "search_params": ["patient+_revinclude", "id+_revinclude"],
            "source": "MaximEyes-FHIR-API-Documentation.pdf p.39-40"
        },
        # These 3 are in Swagger but NOT in the FHIR API PDF
        "Account": {
            "uscdi_classes": [],
            "uscdi_elements": [],
            "documented_in_pdf": False,
            "search_params": ["id", "QueryString"],
            "source": "swagger-v1.json only (not in PDF)",
            "notes": "Billing account resource - beyond US Core. Present in Swagger API but undocumented in FHIR API PDF."
        },
        "ChargeItem": {
            "uscdi_classes": [],
            "uscdi_elements": [],
            "documented_in_pdf": False,
            "search_params": ["id", "QueryString"],
            "source": "swagger-v1.json only (not in PDF)",
            "notes": "Individual billing charge resource - beyond US Core. Present in Swagger API but undocumented in FHIR API PDF."
        },
        "Coverage": {
            "uscdi_classes": ["Health Insurance Information"],
            "uscdi_elements": [],
            "documented_in_pdf": False,
            "search_params": ["id", "QueryString"],
            "source": "swagger-v1.json only (not in PDF)",
            "notes": "Insurance coverage resource - beyond US Core. Present in Swagger API but undocumented in FHIR API PDF."
        },
    }
    return resources


def parse_ehi_scope():
    """Extract the Scope of EHI from the EHI Export Documentation PDF."""
    # From page 4 of MaximEyes-EHI-Export-Documentation.pdf (verified via rendered image)
    return [
        "Patient Demographic",
        "Social History",
        "Problems",
        "Medications",
        "Allergies and Reactions",
        "Diagnostic Results",
        "Vital signs",
        "Encounter Diagnoses",
        "Procedures",
        "Care team members",
        "Immunizations",
        "Assessment and plan of treatment",
        "Goals",
        "Insurance Providers",
        "Accounts",
    ]


def parse_swagger_endpoints():
    """Extract resource-level endpoints from the Swagger spec."""
    with open("../downloads/swagger-v1.json") as f:
        spec = json.load(f)
    
    endpoints = {}
    for path, methods in spec.get("paths", {}).items():
        # Extract resource type from path
        match = re.search(r'/R4/(\w+)', path)
        if match:
            resource = match.group(1)
            if resource not in ["metadata", "Export", "Status", "Download"]:
                if resource not in endpoints:
                    endpoints[resource] = {"paths": [], "methods": []}
                for method in methods:
                    endpoints[resource]["paths"].append(f"{method.upper()} {path}")
                    endpoints[resource]["methods"].append(method.upper())
    
    return endpoints


def build_entity_inventory():
    """Build the full entity inventory."""
    resources = parse_fhir_api_pdf()
    ehi_scope = parse_ehi_scope()
    swagger_endpoints = parse_swagger_endpoints()
    
    entities = []
    for name, info in resources.items():
        entity = {
            "entity_name": name,
            "fhir_resource_type": name,
            "documented_in_pdf": info["documented_in_pdf"],
            "in_swagger": name in swagger_endpoints,
            "in_ehi_scope": any(
                uscdi.lower() in [s.lower() for s in ehi_scope]
                for uscdi in info.get("uscdi_classes", [])
            ) or name.lower() in [s.lower().replace(" ", "") for s in ehi_scope],
            "uscdi_data_classes": info["uscdi_classes"],
            "uscdi_data_elements": info["uscdi_elements"],
            "search_parameters": info["search_params"],
            "fields": [],  # No field-level documentation exists
            "field_count": 0,  # No data dictionary
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "category": categorize_resource(name),
            "source": info["source"],
            "notes": info.get("notes", "")
        }
        entities.append(entity)
    
    return {
        "product": "MaximEyes.com v1.1",
        "vendor": "First Insight Corporation",
        "export_format": "FHIR R4 NDJSON (Bulk Data 1.0.1)",
        "ehi_scope_categories": ehi_scope,
        "total_resource_types": len(entities),
        "resource_types_in_pdf": sum(1 for e in entities if e["documented_in_pdf"]),
        "resource_types_swagger_only": sum(1 for e in entities if not e["documented_in_pdf"]),
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "entities": entities
    }


def categorize_resource(name):
    """Assign a high-level category to each FHIR resource type."""
    categories = {
        "Patient": "Demographics",
        "AllergyIntolerance": "Clinical",
        "CarePlan": "Clinical",
        "CareTeam": "Clinical",
        "Condition": "Clinical",
        "Device": "Clinical",
        "DiagnosticReport": "Clinical",
        "DocumentReference": "Clinical Notes",
        "Encounter": "Clinical",
        "Goal": "Clinical",
        "Immunization": "Clinical",
        "Location": "Administrative",
        "Medication": "Medications",
        "MedicationRequest": "Medications",
        "Observation": "Clinical",
        "Organization": "Administrative",
        "Practitioner": "Administrative",
        "PractitionerRole": "Administrative",
        "Procedure": "Clinical",
        "Provenance": "Administrative",
        "Account": "Billing",
        "ChargeItem": "Billing",
        "Coverage": "Insurance",
    }
    return categories.get(name, "Other")


def build_summary(inventory):
    """Build summary statistics from the inventory."""
    entities = inventory["entities"]
    
    by_category = {}
    for e in entities:
        cat = e["category"]
        if cat not in by_category:
            by_category[cat] = {"count": 0, "documented_in_pdf": 0, "resources": []}
        by_category[cat]["count"] += 1
        if e["documented_in_pdf"]:
            by_category[cat]["documented_in_pdf"] += 1
        by_category[cat]["resources"].append(e["entity_name"])
    
    return {
        "product": inventory["product"],
        "vendor": inventory["vendor"],
        "export_format": inventory["export_format"],
        "total_resource_types": inventory["total_resource_types"],
        "resource_types_documented_in_pdf": inventory["resource_types_in_pdf"],
        "resource_types_swagger_only": inventory["resource_types_swagger_only"],
        "ehi_scope_categories_count": len(inventory["ehi_scope_categories"]),
        "ehi_scope_categories": inventory["ehi_scope_categories"],
        "has_data_dictionary": False,
        "has_field_level_documentation": False,
        "has_sample_data": False,
        "has_machine_readable_schema": True,  # Swagger, but no response schemas
        "swagger_has_response_schemas": False,
        "categories": by_category,
        "notes": [
            "No field-level data dictionary exists - only resource-type-level USCDI mappings",
            "Swagger spec has endpoints for Account, ChargeItem, Coverage (billing) but these are undocumented in the FHIR API PDF",
            "Swagger response schemas are empty (all 200 responses just say 'Success')",
            "No sample export data provided",
            "Export uses same FHIR Bulk Data endpoint as (g)(10) API"
        ]
    }


if __name__ == "__main__":
    inventory = build_entity_inventory()
    summary = build_summary(inventory)
    
    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Total resource types: {inventory['total_resource_types']}")
    print(f"  Documented in PDF: {inventory['resource_types_in_pdf']}")
    print(f"  Swagger-only: {inventory['resource_types_swagger_only']}")
    print(f"EHI Scope categories: {len(inventory['ehi_scope_categories'])}")
    print(f"Has data dictionary: {inventory['has_data_dictionary']}")
    print(f"Has sample data: {inventory['has_sample_data']}")
    print()
    for cat, info in summary["categories"].items():
        print(f"  {cat}: {info['count']} resources ({', '.join(info['resources'])})")
