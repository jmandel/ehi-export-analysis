#!/usr/bin/env python3
"""
Parse the C-CDA data dictionary from the EHIexport.pdf text extraction.
Produces entity-inventory-full.json and entity-inventory-summary.json.
"""

import json
import re

# Read the extracted text
with open("analysis/EHIexport.txt", "r") as f:
    text = f.read()

# The data dictionary starts at "Sections in the CCD output" (page 12)
# Each section is identified by a header like:
#   Section Name [OID : date]
# followed by data element rows

# Define the sections we found in the PDF
sections = []

# Parse section by section from the PDF text
# We'll manually structure this based on the PDF content since the layout is tabular

current_section = None
entities = []

# Define all sections with their data elements based on the PDF
# This is parsed from the extracted text

sections_data = [
    {
        "name": "Patient Demographics/Information",
        "oid": None,
        "fields": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system": None, "code_system_name": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system": "2.16.840.1.113883.5.1", "code_system_name": "AdministrativeGender"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system": None, "code_system_name": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Provider Information",
        "oid": None,
        "fields": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system": None, "code_system_name": None},
            {"name": "Performer Phone", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system": None, "code_system_name": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Date and Location of Visit",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1",
        "fields": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system": None, "code_system_name": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Chief Complaint and Reason for Visit",
        "oid": "2.16.840.1.113883.10.20.22.2.13",
        "fields": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Encounters",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1",
        "fields": [
            {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49", "code_system": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
            {"name": "Performer", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Diagnosis", "xpath": None, "code_system": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Location", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Immunizations",
        "oid": "2.16.840.1.113883.10.20.22.2.2.1",
        "fields": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52", "code_system": "2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12", "code_system_name": "CVX and CPT-4"},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Route", "xpath": None, "code_system": "2.16.840.1.113883.3.26.1.1", "code_system_name": "NCI Thesaurus"},
            {"name": "Site", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Manufacturer", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Dose", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Lot Number", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Notes", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Instructions",
        "oid": "2.16.840.1.113883.10.20.22.2.45",
        "fields": [
            {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "name": "Treatment Plan",
        "oid": "2.16.840.1.113883.10.20.22.2.10",
        "fields": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40 / 2.16.840.1.113883.10.20.22.4.39 / 2.16.840.1.113883.10.20.22.4.121", "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Social History",
        "oid": "2.16.840.1.113883.10.20.22.2.17",
        "fields": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Description", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Dates Observed", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Problems",
        "oid": "2.16.840.1.113883.10.20.22.2.5.1",
        "fields": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3", "code_system": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Active date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Medications",
        "oid": "2.16.840.1.113883.10.20.22.2.1.1",
        "fields": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16", "code_system": "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69", "code_system_name": "RxNorm and NDC"},
            {"name": "Directions", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Start Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "End Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Medication Allergies",
        "oid": "2.16.840.1.113883.10.20.22.2.6.1",
        "fields": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30", "code_system": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
            {"name": "Reaction", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Severity", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "name": "Laboratory Tests",
        "oid": None,
        "fields": [
            {"name": "Test Code", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Code System", "xpath": None, "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Name", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Laboratory Information",
        "oid": None,
        "fields": [
            {"name": "Lab Name", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Lab Address", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Test Report Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Test Performed", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Specimen Source", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Laboratory Values/Results",
        "oid": "2.16.840.1.113883.10.20.22.2.3.1",
        "fields": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Result Value", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Interpretation", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Vitals",
        "oid": "2.16.840.1.113883.10.20.22.2.4.1",
        "fields": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26", "code_system": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Observation Date/Time", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Goals",
        "oid": "2.16.840.1.113883.10.20.22.2.60",
        "fields": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system": None, "code_system_name": None},
            {"name": "Value", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Procedures",
        "oid": "2.16.840.1.113883.10.20.22.2.7.1",
        "fields": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Care Team Members",
        "oid": "2.16.840.1.113883.10.20.22.2.500",
        "fields": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500", "code_system": None, "code_system_name": None},
            {"name": "Specialty", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Reason for Referral",
        "oid": "1.3.6.1.4.1.19376.1.5.3.1.3.1",
        "fields": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "name": "Medical Equipment",
        "oid": "2.16.840.1.113883.10.20.22.2.23",
        "fields": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "GMDN PT Description", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Mental Status",
        "oid": "2.16.840.1.113883.10.20.22.2.56",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74", "code_system": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Functional Status",
        "oid": "2.16.840.1.113883.10.20.22.2.14",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67", "code_system": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
    {
        "name": "Health Concern",
        "oid": "2.16.840.1.113883.10.20.22.2.58",
        "fields": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132", "code_system": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system": None, "code_system_name": None},
        ]
    },
]

# Build the full inventory
total_fields = 0
total_with_xpath = 0
total_with_code_system = 0

for section in sections_data:
    for field in section["fields"]:
        total_fields += 1
        if field["xpath"]:
            total_with_xpath += 1
        if field["code_system"]:
            total_with_code_system += 1

# Write full inventory
with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump({
        "source": "downloads/EHIexport.pdf",
        "format": "C-CDA (Consolidated CDA)",
        "standard": "HL7 CDA R2: C-CDA Templates DSTU R2.1 (Aug 2015)",
        "uscdi_version": "USCDI Version 1",
        "product_version": "MDCare EMR/PMS V5.1",
        "document_date": "2023-11-29",
        "total_sections": len(sections_data),
        "total_fields": total_fields,
        "fields_with_xpath": total_with_xpath,
        "fields_with_code_system": total_with_code_system,
        "sections": sections_data
    }, f, indent=2)

# Write summary
summary = {
    "total_sections": len(sections_data),
    "total_fields": total_fields,
    "fields_with_xpath": total_with_xpath,
    "fields_with_code_system": total_with_code_system,
    "fields_without_xpath": total_fields - total_with_xpath,
    "fields_without_code_system": total_fields - total_with_code_system,
    "pct_with_xpath": round(100 * total_with_xpath / total_fields, 1) if total_fields else 0,
    "pct_with_code_system": round(100 * total_with_code_system / total_fields, 1) if total_fields else 0,
    "sections_summary": []
}

for section in sections_data:
    n = len(section["fields"])
    n_xpath = sum(1 for f in section["fields"] if f["xpath"])
    n_code = sum(1 for f in section["fields"] if f["code_system"])
    summary["sections_summary"].append({
        "name": section["name"],
        "oid": section["oid"],
        "field_count": n,
        "fields_with_xpath": n_xpath,
        "fields_with_code_system": n_code,
    })

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Sections: {len(sections_data)}")
print(f"Total fields: {total_fields}")
print(f"Fields with XPATH: {total_with_xpath} ({summary['pct_with_xpath']}%)")
print(f"Fields with code system: {total_with_code_system} ({summary['pct_with_code_system']}%)")
print()
for s in summary["sections_summary"]:
    print(f"  {s['name']}: {s['field_count']} fields ({s['fields_with_xpath']} w/xpath, {s['fields_with_code_system']} w/code)")
