"""
Build full-entity-inventory.json from:
1. The FHIR API PDF (resource-level USCDI mappings, extracted manually from pdftotext)
2. The Swagger/OpenAPI spec (resource types and endpoints)
3. The EHI Export PDF page 4 (Scope of EHI categories)

Since there is no native data dictionary, we document the FHIR resource types
as the "entities" with their USCDI data class mappings and search parameters.
"""
import json

# Scope of EHI from page 4 of EHI Export Documentation PDF (verified from image)
SCOPE_OF_EHI = [
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
    "Accounts"
]

# FHIR resources documented in the FHIR API PDF with their USCDI mappings
# Extracted from pdftotext of MaximEyes-FHIR-API-Documentation.pdf
PDF_RESOURCES = {
    "AllergyIntolerance": {
        "uscdi_data_classes": ["Allergies and Intolerances"],
        "uscdi_elements": ["Substance (Medication)", "Substance (Drug Class)", "Reaction"],
        "documented_in_pdf": True,
        "pdf_pages": "12-13",
        "search_params": ["_id", "patient", "patient+clinical-status"],
        "category": "Clinical"
    },
    "CarePlan": {
        "uscdi_data_classes": ["Assessment and Plan of Treatment"],
        "uscdi_elements": ["Assessment and Plan of Treatment"],
        "documented_in_pdf": True,
        "pdf_pages": "13-14",
        "search_params": ["patient+category", "patient+category+date", "patient+category+status", "patient+category+date+status"],
        "category": "Clinical"
    },
    "CareTeam": {
        "uscdi_data_classes": ["Care Team Member(s)"],
        "uscdi_elements": ["Care Team"],
        "documented_in_pdf": True,
        "pdf_pages": "15",
        "search_params": ["patient+status"],
        "category": "Clinical"
    },
    "Condition": {
        "uscdi_data_classes": ["Health Concerns", "Problems"],
        "uscdi_elements": ["Health Concerns", "Problems"],
        "documented_in_pdf": True,
        "pdf_pages": "15-16",
        "search_params": ["patient", "patient+status", "patient+category", "patient+code", "patient+onset-date"],
        "category": "Clinical"
    },
    "Device": {
        "uscdi_data_classes": ["Unique Device Identifier(s) for Patient's Implantable Device(s)"],
        "uscdi_elements": ["UDI"],
        "documented_in_pdf": True,
        "pdf_pages": "17",
        "search_params": ["patient", "patient+type"],
        "category": "Clinical"
    },
    "DiagnosticReport": {
        "uscdi_data_classes": ["Laboratory", "Clinical Notes"],
        "uscdi_elements": ["Imaging Narrative", "Laboratory Report Narrative", "Pathology Report Narrative", "Procedure Note"],
        "documented_in_pdf": True,
        "pdf_pages": "17-18",
        "search_params": ["patient", "patient+category", "patient+code", "patient+category+date", "patient+status", "patient+code+date"],
        "category": "Clinical"
    },
    "DocumentReference": {
        "uscdi_data_classes": ["Clinical Notes"],
        "uscdi_elements": ["Consultation Note", "Discharge Summary Note", "History & Physical", "Progress Note"],
        "documented_in_pdf": True,
        "pdf_pages": "19-20",
        "search_params": ["_id", "patient", "patient+type", "patient+category+date", "patient+category", "patient+status", "patient+type+period"],
        "category": "Clinical"
    },
    "Encounter": {
        "uscdi_data_classes": ["Encounter Information"],
        "uscdi_elements": ["Encounter Information"],
        "documented_in_pdf": True,
        "pdf_pages": "20-21",
        "search_params": ["_id", "patient", "date+patient", "identifier", "class+patient", "patient+type", "patient+status"],
        "category": "Clinical"
    },
    "Goal": {
        "uscdi_data_classes": ["Goals"],
        "uscdi_elements": ["Patient Goals"],
        "documented_in_pdf": True,
        "pdf_pages": "21",
        "search_params": ["patient", "patient+target-date", "patient+lifecycle-status"],
        "category": "Clinical"
    },
    "Immunization": {
        "uscdi_data_classes": ["Immunizations"],
        "uscdi_elements": ["Immunization"],
        "documented_in_pdf": True,
        "pdf_pages": "22",
        "search_params": ["patient", "patient+status", "patient+date"],
        "category": "Clinical"
    },
    "Location": {
        "uscdi_data_classes": [],
        "uscdi_elements": [],
        "documented_in_pdf": True,
        "pdf_pages": "23",
        "search_params": ["name", "address", "address-state", "address-city", "address-postalCode"],
        "category": "Administrative"
    },
    "Medication": {
        "uscdi_data_classes": ["Medications"],
        "uscdi_elements": ["Medications"],
        "documented_in_pdf": True,
        "pdf_pages": "23-24 (via MedicationRequest _include)",
        "search_params": [],
        "category": "Clinical"
    },
    "MedicationRequest": {
        "uscdi_data_classes": ["Medications"],
        "uscdi_elements": ["Medications"],
        "documented_in_pdf": True,
        "pdf_pages": "23-24",
        "search_params": ["patient+intent", "patient+intent+status", "patient+intent+encounter", "patient+intent+authoredon"],
        "category": "Clinical"
    },
    "Observation": {
        "uscdi_data_classes": ["Laboratory", "Vital Signs", "Social History"],
        "uscdi_elements": [
            "Tests", "Values/Results",
            "Smoking Status",
            "BMI Percentile (2-20 years)", "Weight-for-length Percentile",
            "Pulse Oximetry",
            "Head Occipital-frontal Circumference Percentile (Birth-36 Months)",
            "Body Height", "Body Temperature",
            "Systolic Blood Pressure", "Diastolic Blood Pressure",
            "Body Weight", "Heart Rate", "Respiratory Rate"
        ],
        "documented_in_pdf": True,
        "pdf_pages": "25-35",
        "search_params": ["patient+category", "patient+code", "patient+category+date", "patient+category+status", "patient+code+date"],
        "category": "Clinical"
    },
    "Organization": {
        "uscdi_data_classes": [],
        "uscdi_elements": [],
        "documented_in_pdf": True,
        "pdf_pages": "35-36",
        "search_params": ["name", "address"],
        "category": "Administrative"
    },
    "Patient": {
        "uscdi_data_classes": ["Patient Demographics/Information"],
        "uscdi_elements": [
            "First Name", "Middle Name", "Last Name", "Previous Name", "Suffix",
            "Birth Sex", "Date of Birth", "Race", "Ethnicity",
            "Preferred Language", "Address", "Phone Number"
        ],
        "documented_in_pdf": True,
        "pdf_pages": "36-37",
        "search_params": ["_id", "identifier", "name", "birthdate+name", "gender+name", "birthdate+family", "family+gender"],
        "category": "Demographics"
    },
    "Practitioner": {
        "uscdi_data_classes": [],
        "uscdi_elements": [],
        "documented_in_pdf": True,
        "pdf_pages": "37-38",
        "search_params": ["name", "identifier"],
        "category": "Administrative"
    },
    "PractitionerRole": {
        "uscdi_data_classes": [],
        "uscdi_elements": [],
        "documented_in_pdf": True,
        "pdf_pages": "38",
        "search_params": ["specialty", "practitioner"],
        "category": "Administrative"
    },
    "Procedure": {
        "uscdi_data_classes": ["Procedures"],
        "uscdi_elements": ["Procedures"],
        "documented_in_pdf": True,
        "pdf_pages": "38-39",
        "search_params": ["patient", "patient+date", "patient+status", "patient+code+date"],
        "category": "Clinical"
    },
    "Provenance": {
        "uscdi_data_classes": ["Provenance"],
        "uscdi_elements": ["Author Time Stamp", "Author Organization"],
        "documented_in_pdf": True,
        "pdf_pages": "39-40",
        "search_params": ["patient+_revinclude", "id+_revinclude"],
        "category": "Infrastructure"
    },
    # These 3 are in the Swagger API but NOT in the FHIR API PDF
    "Account": {
        "uscdi_data_classes": [],
        "uscdi_elements": [],
        "documented_in_pdf": False,
        "pdf_pages": None,
        "search_params": [],
        "category": "Billing",
        "note": "Present in Swagger API but not documented in the FHIR API PDF"
    },
    "ChargeItem": {
        "uscdi_data_classes": [],
        "uscdi_elements": [],
        "documented_in_pdf": False,
        "pdf_pages": None,
        "search_params": [],
        "category": "Billing",
        "note": "Present in Swagger API but not documented in the FHIR API PDF"
    },
    "Coverage": {
        "uscdi_data_classes": [],
        "uscdi_elements": [],
        "documented_in_pdf": False,
        "pdf_pages": None,
        "search_params": [],
        "category": "Billing/Insurance",
        "note": "Present in Swagger API but not documented in the FHIR API PDF"
    }
}

# Build the full inventory
inventory = {
    "source": "MaximEyes FHIR API - Swagger spec + FHIR API PDF",
    "format": "FHIR R4 NDJSON",
    "note": "No native data dictionary exists. This inventory documents the FHIR resource types available in the export. There are no field-level definitions, value sets, or relationship documentation beyond what FHIR R4 US Core 3.1.1 profiles define.",
    "scope_of_ehi_categories": SCOPE_OF_EHI,
    "total_resource_types": len(PDF_RESOURCES),
    "resource_types_documented_in_pdf": sum(1 for r in PDF_RESOURCES.values() if r["documented_in_pdf"]),
    "resource_types_swagger_only": sum(1 for r in PDF_RESOURCES.values() if not r["documented_in_pdf"]),
    "entities": []
}

# Category counts
category_counts = {}
for resource, info in PDF_RESOURCES.items():
    cat = info["category"]
    if cat not in category_counts:
        category_counts[cat] = {"count": 0, "resources": []}
    category_counts[cat]["count"] += 1
    category_counts[cat]["resources"].append(resource)

inventory["categories"] = category_counts

for resource, info in sorted(PDF_RESOURCES.items()):
    entity = {
        "resource_type": resource,
        "category": info["category"],
        "documented_in_pdf": info["documented_in_pdf"],
        "pdf_pages": info["pdf_pages"],
        "uscdi_data_classes": info["uscdi_data_classes"],
        "uscdi_elements": info["uscdi_elements"],
        "search_parameters": info["search_params"],
        "fields": "Not documented — FHIR R4 US Core profile fields assumed but not explicitly listed",
        "field_count": "N/A — no field-level documentation provided",
        "descriptions": "N/A — no field-level descriptions provided",
        "value_sets": "N/A — no value set documentation provided",
        "relationships": "FHIR references only (e.g., patient, encounter) — no explicit relationship documentation"
    }
    if "note" in info:
        entity["note"] = info["note"]
    inventory["entities"].append(entity)

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/first-insight-corporation--maximeyes-com/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print(f"Total resource types: {inventory['total_resource_types']}")
print(f"  Documented in PDF: {inventory['resource_types_documented_in_pdf']}")
print(f"  Swagger-only (undocumented): {inventory['resource_types_swagger_only']}")
print(f"\nCategories:")
for cat, info in sorted(category_counts.items()):
    print(f"  {cat}: {info['count']} resources — {', '.join(info['resources'])}")
print(f"\nScope of EHI categories: {len(SCOPE_OF_EHI)}")
for s in SCOPE_OF_EHI:
    print(f"  - {s}")
