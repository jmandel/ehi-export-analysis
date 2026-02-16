#!/usr/bin/env python3
"""
Parse the 18 C-CDA sections from eHana's EHI Export PDF into a structured JSON inventory.

Since the PDF is image-based, we construct the inventory from visual inspection of 
the rendered page images and OCR text. Each section documents fields visible in the 
UI screenshots and XML element examples shown in the PDF.
"""

import json
from pathlib import Path

# The 18 C-CDA sections as documented in the EHI_Export.pdf
# Each section includes: name, page(s), overview text, fields visible in UI/XML, 
# code systems referenced, and C-CDA template OIDs where visible.

sections = [
    {
        "section_number": 1,
        "name": "Electronic Chart / Patient Data",
        "pages": [2, 3],
        "overview": "Stores all manually entered (or imported) client Demographic information.",
        "ccda_category": "Demographics",
        "fields": [
            {"name": "name", "type": "PN (person name)", "description": "Patient full name", "sample_value": "Alice Newman", "xml_element": "name"},
            {"name": "birthTime", "type": "TS (timestamp)", "description": "Date of birth", "sample_value": "19700501", "xml_element": "birthTime"},
            {"name": "administrativeGenderCode", "type": "CE (coded element)", "description": "Gender/sex", "sample_value": "F", "xml_element": "administrativeGenderCode", "code_system": "2.16.840.1.113883.5.1 (AdministrativeGender)"},
            {"name": "raceCode", "type": "CE (coded element)", "description": "Race", "sample_value": "2106-3 (White)", "xml_element": "raceCode", "code_system": "2.16.840.1.113883.6.238 (Race and Ethnicity CDC)"},
            {"name": "ethnicGroupCode", "type": "CE (coded element)", "description": "Ethnicity", "sample_value": "2186-5 (Not Hispanic or Latino)", "xml_element": "ethnicGroupCode", "code_system": "2.16.840.1.113883.6.238 (Race and Ethnicity CDC)"},
            {"name": "languageCommunication", "type": "CS (coded simple)", "description": "Preferred language", "sample_value": "en (English)", "xml_element": "languageCode"},
            {"name": "addr", "type": "AD (address)", "description": "Street address", "sample_value": "Main Street, Boston", "xml_element": "addr"},
            {"name": "telecom", "type": "TEL (telecom)", "description": "Phone/contact info", "sample_value": "tel:+1(555)-777-1234", "xml_element": "telecom"}
        ]
    },
    {
        "section_number": 2,
        "name": "Vital Signs",
        "pages": [4],
        "overview": "Manually entered Vital Signs associated with the client record.",
        "ccda_category": "Clinical Observations",
        "fields": [
            {"name": "code", "type": "CE (coded element)", "description": "Vital sign type", "sample_value": "Blood Pressure Systolic", "xml_element": "code", "code_system": "LOINC"},
            {"name": "value", "type": "PQ (physical quantity)", "description": "Measured value with unit", "sample_value": "145 mm[Hg]", "xml_element": "value"},
            {"name": "effectiveTime", "type": "TS (timestamp)", "description": "Date/time of measurement", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Status of observation", "sample_value": "completed", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 3,
        "name": "Immunization",
        "pages": [5],
        "overview": "Immunizations Given and/or Reported associated with the client record.",
        "ccda_category": "Clinical Observations",
        "fields": [
            {"name": "vaccineCode", "type": "CE (coded element)", "description": "Vaccine administered", "xml_element": "code", "code_system": "CVX"},
            {"name": "effectiveTime", "type": "TS (timestamp)", "description": "Date of immunization", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Status (completed/refused)", "xml_element": "statusCode"},
            {"name": "routeCode", "type": "CE", "description": "Route of administration", "xml_element": "routeCode"}
        ]
    },
    {
        "section_number": 4,
        "name": "Allergies, Adverse Reactions, Alerts",
        "pages": [5, 6],
        "overview": "Allergies, Adverse Reactions, and Alerts associated with the client record.",
        "ccda_category": "Clinical Observations",
        "fields": [
            {"name": "substance", "type": "CE (coded element)", "description": "Allergen substance", "xml_element": "code", "code_system": "RxNorm"},
            {"name": "reaction", "type": "CE (coded element)", "description": "Reaction observed", "xml_element": "value", "code_system": "SNOMED-CT"},
            {"name": "severity", "type": "CE (coded element)", "description": "Severity of reaction", "xml_element": "value", "code_system": "SNOMED-CT"},
            {"name": "effectiveTime", "type": "IVL_TS (interval)", "description": "Date range of allergy", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Status (active/inactive)", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 5,
        "name": "History of Medication Use",
        "pages": [6, 7],
        "overview": "Medications prescribed and/or taken concurrently associated with the client record.",
        "ccda_category": "Medications",
        "fields": [
            {"name": "medication", "type": "CE (coded element)", "description": "Medication name and code", "xml_element": "code", "code_system": "RxNorm, NDC"},
            {"name": "doseQuantity", "type": "PQ (physical quantity)", "description": "Dose amount", "xml_element": "doseQuantity"},
            {"name": "routeCode", "type": "CE", "description": "Route of administration", "xml_element": "routeCode"},
            {"name": "effectiveTime", "type": "IVL_TS (interval)", "description": "Date range of medication use", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Active/completed status", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 6,
        "name": "Instructions",
        "pages": [7, 8],
        "overview": "Instructions given by clinicians during encounters.",
        "ccda_category": "Clinical Documentation",
        "fields": [
            {"name": "text", "type": "ED (encapsulated data)", "description": "Instruction text content", "xml_element": "text"},
            {"name": "effectiveTime", "type": "TS", "description": "Date of instruction", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Status", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 7,
        "name": "Functional and Cognitive Status",
        "pages": [8],
        "overview": "Functional and Cognitive Status assessments associated with the client record.",
        "ccda_category": "Clinical Assessments",
        "fields": [
            {"name": "code", "type": "CE (coded element)", "description": "Assessment type", "xml_element": "code", "code_system": "SNOMED-CT"},
            {"name": "value", "type": "CD (concept descriptor)", "description": "Assessment result/finding", "xml_element": "value"},
            {"name": "effectiveTime", "type": "TS", "description": "Date of assessment", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Status", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 8,
        "name": "Chief Complaint / Reason For Visit",
        "pages": [9],
        "overview": "Chief complaint or reason for visit recorded during encounters.",
        "ccda_category": "Encounters",
        "fields": [
            {"name": "text", "type": "ED (encapsulated data)", "description": "Free-text chief complaint", "xml_element": "text"},
            {"name": "code", "type": "CE", "description": "Coded reason for visit", "xml_element": "code"}
        ]
    },
    {
        "section_number": 9,
        "name": "Problem List",
        "pages": [9, 10],
        "overview": "Active and historical diagnoses/problems associated with the client record.",
        "ccda_category": "Clinical Observations",
        "fields": [
            {"name": "code", "type": "CE (coded element)", "description": "Problem/diagnosis code", "xml_element": "value", "code_system": "SNOMED-CT"},
            {"name": "translation", "type": "CE", "description": "ICD-10-CM translation", "xml_element": "translation", "code_system": "ICD-10-CM"},
            {"name": "effectiveTime", "type": "IVL_TS (interval)", "description": "Onset date range", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Active/resolved/inactive", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 10,
        "name": "Social History",
        "pages": [10],
        "overview": "Social history observations including smoking status and birth sex.",
        "ccda_category": "Social/Behavioral",
        "fields": [
            {"name": "smokingStatus", "type": "CE (coded element)", "description": "Smoking status observation", "xml_element": "value", "code_system": "SNOMED-CT"},
            {"name": "birthSex", "type": "CE (coded element)", "description": "Sex assigned at birth", "xml_element": "value", "code_system": "AdministrativeSex"}
        ]
    },
    {
        "section_number": 11,
        "name": "Encounters",
        "pages": [11],
        "overview": "Encounter records with associated problems/diagnoses.",
        "ccda_category": "Encounters",
        "fields": [
            {"name": "code", "type": "CE (coded element)", "description": "Encounter type", "xml_element": "code", "code_system": "CPT"},
            {"name": "effectiveTime", "type": "IVL_TS (interval)", "description": "Encounter date/time range", "xml_element": "effectiveTime"},
            {"name": "performer", "type": "ASSIGNED", "description": "Provider performing encounter", "xml_element": "performer"},
            {"name": "entryRelationship", "type": "ACT", "description": "Associated diagnoses/problems", "xml_element": "entryRelationship"}
        ]
    },
    {
        "section_number": 12,
        "name": "Results",
        "pages": [12],
        "overview": "Lab and test results associated with the client record.",
        "ccda_category": "Lab/Diagnostics",
        "fields": [
            {"name": "code", "type": "CE (coded element)", "description": "Test/result type", "xml_element": "code", "code_system": "LOINC"},
            {"name": "value", "type": "PQ/ST", "description": "Result value", "xml_element": "value"},
            {"name": "referenceRange", "type": "IVL_PQ", "description": "Normal reference range", "xml_element": "referenceRange"},
            {"name": "effectiveTime", "type": "TS", "description": "Result date", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Final/preliminary status", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 13,
        "name": "Procedures",
        "pages": [13],
        "overview": "Scheduled or performed procedures associated with the client record.",
        "ccda_category": "Procedures",
        "template_oid": "2.16.840.1.113883.10.20.22.4.14",
        "fields": [
            {"name": "code", "type": "CE (coded element)", "description": "Procedure type", "xml_element": "code", "code_system": "SNOMED-CT"},
            {"name": "effectiveTime", "type": "TS", "description": "Date of procedure", "xml_element": "effectiveTime"},
            {"name": "statusCode", "type": "CS", "description": "Completed/active/aborted", "xml_element": "statusCode"},
            {"name": "targetSiteCode", "type": "CE", "description": "Body site", "xml_element": "targetSiteCode", "code_system": "SNOMED-CT"}
        ]
    },
    {
        "section_number": 14,
        "name": "Reason for Referral",
        "pages": [13, 14],
        "overview": "Referral documentation associated with the client record.",
        "ccda_category": "Care Coordination",
        "fields": [
            {"name": "text", "type": "ED (encapsulated data)", "description": "Referral reason text", "xml_element": "text"},
            {"name": "code", "type": "CE", "description": "Referral type code", "xml_element": "code"}
        ]
    },
    {
        "section_number": 15,
        "name": "Implantable Devices",
        "pages": [14],
        "overview": "Implantable device records (UDI) associated with the client record.",
        "ccda_category": "Devices",
        "fields": [
            {"name": "id", "type": "II (instance identifier)", "description": "Unique Device Identifier (UDI)", "xml_element": "id"},
            {"name": "code", "type": "CE", "description": "Device type", "xml_element": "code"},
            {"name": "statusCode", "type": "CS", "description": "Active/inactive status", "xml_element": "statusCode"},
            {"name": "effectiveTime", "type": "TS", "description": "Implant date", "xml_element": "effectiveTime"}
        ]
    },
    {
        "section_number": 16,
        "name": "Health Concerns",
        "pages": [14, 15],
        "overview": "Documented health concerns associated with the client record.",
        "ccda_category": "Care Planning",
        "fields": [
            {"name": "text", "type": "ED (encapsulated data)", "description": "Health concern narrative", "xml_element": "text"},
            {"name": "code", "type": "CE", "description": "Concern type code", "xml_element": "code"},
            {"name": "statusCode", "type": "CS", "description": "Active/resolved", "xml_element": "statusCode"}
        ]
    },
    {
        "section_number": 17,
        "name": "Assessment and Plan",
        "pages": [15],
        "overview": "Clinician assessment and plan of care.",
        "ccda_category": "Care Planning",
        "fields": [
            {"name": "text", "type": "ED (encapsulated data)", "description": "Assessment and plan narrative (free text)", "xml_element": "text"}
        ]
    },
    {
        "section_number": 18,
        "name": "Goals",
        "pages": [15],
        "overview": "Client goals documented in the care plan.",
        "ccda_category": "Care Planning",
        "template_oid": "2.16.840.1.113883.10.20.22.2.60",
        "fields": [
            {"name": "text", "type": "ED (encapsulated data)", "description": "Goal description (free text)", "xml_element": "text"},
            {"name": "statusCode", "type": "CS", "description": "Goal status", "xml_element": "statusCode"},
            {"name": "effectiveTime", "type": "TS", "description": "Target date", "xml_element": "effectiveTime"}
        ]
    }
]

# Build the full inventory
inventory = {
    "source_artifact": "EHI_Export.pdf",
    "source_format": "Image-based PDF (15 pages), rendered and OCR'd",
    "export_format": "CDA R2 / C-CDA XML",
    "extraction_method": "Visual inspection of rendered page images + OCR text from Tesseract",
    "total_sections": len(sections),
    "total_fields": sum(len(s["fields"]) for s in sections),
    "fields_with_descriptions": sum(
        1 for s in sections for f in s["fields"] if f.get("description")
    ),
    "fields_with_types": sum(
        1 for s in sections for f in s["fields"] if f.get("type")
    ),
    "fields_with_sample_values": sum(
        1 for s in sections for f in s["fields"] if f.get("sample_value")
    ),
    "fields_with_code_systems": sum(
        1 for s in sections for f in s["fields"] if f.get("code_system")
    ),
    "category_summary": {},
    "sections": sections
}

# Build category summary
categories = {}
for s in sections:
    cat = s["ccda_category"]
    if cat not in categories:
        categories[cat] = {"section_count": 0, "field_count": 0, "sections": []}
    categories[cat]["section_count"] += 1
    categories[cat]["field_count"] += len(s["fields"])
    categories[cat]["sections"].append(s["name"])
inventory["category_summary"] = categories

# Write output
output_path = Path(__file__).parent / "full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary stats
print(f"Total C-CDA sections: {inventory['total_sections']}")
print(f"Total fields across all sections: {inventory['total_fields']}")
print(f"Fields with descriptions: {inventory['fields_with_descriptions']}")
print(f"Fields with data types: {inventory['fields_with_types']}")
print(f"Fields with sample values: {inventory['fields_with_sample_values']}")
print(f"Fields with code systems: {inventory['fields_with_code_systems']}")
print()
print("Category breakdown:")
for cat, info in categories.items():
    print(f"  {cat}: {info['section_count']} sections, {info['field_count']} fields")
    for s in info["sections"]:
        print(f"    - {s}")

print(f"\nInventory written to {output_path}")
