#!/usr/bin/env python3
"""
Manually structured parse of the (b)(10) EHI export PDF sections and data elements.
Source: 170.315(b)(10)-EHI-export-v3.pdf (9 pages, dated Sep 5, 2023)

The PDF documents a C-CDA (CCD) export with specific sections and data elements.
This script creates a clean, accurate inventory based on manual review of the PDF text.
"""

import json

# Sections and their data elements, parsed directly from the PDF text
sections = [
    {
        "section": "Patient Demographics/Information",
        "oid": None,
        "data_elements": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system": "AdministrativeGender (2.16.840.1.113883.5.1)"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system": "Race & Ethnicity - CDC (2.16.840.1.113883.6.238)"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system": "Race & Ethnicity - CDC (2.16.840.1.113883.6.238)"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system": None},
        ]
    },
    {
        "section": "Provider's name and office contact information",
        "oid": None,
        "data_elements": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system": None},
            {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system": None},
        ]
    },
    {
        "section": "Date and Location of visit",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "data_elements": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system": None},
        ]
    },
    {
        "section": "Chief Complaint and Reason for visit",
        "oid": "2.16.840.1.113883.10.20.22.2.13 : 2014-06-09",
        "data_elements": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Encounters",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "data_elements": [
            {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system": "CPT (2.16.840.1.113883.6.12)"},
            {"name": "Performer", "xpath": None, "code_system": None},
            {"name": "Diagnosis", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96) and ICD10 (2.16.840.1.113883.6.3)"},
            {"name": "Location", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Immunizations",
        "oid": "2.16.840.1.113883.10.20.22.2.2.1 : 2015-08-01",
        "data_elements": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52: 2015-08-01", "code_system": "CVX (2.16.840.1.113883.12.292) and CPT-4"},
            {"name": "Date", "xpath": None, "code_system": None},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Route", "xpath": None, "code_system": "NCI Thesaurus (2.16.840.1.113883.3.26.1.1)"},
            {"name": "Site", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Manufacturer", "xpath": None, "code_system": None},
            {"name": "Dose", "xpath": None, "code_system": None},
            {"name": "Lot Number", "xpath": None, "code_system": None},
            {"name": "Notes", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Instructions",
        "oid": "2.16.840.1.113883.10.20.22.2.45 : 2014-06-09",
        "data_elements": [
            {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section": "Treatment Plan",
        "oid": "2.16.840.1.113883.10.20.22.2.10 : 2014-06-09",
        "data_elements": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40: 2014-06-09", "code_system": None},
        ]
    },
    {
        "section": "Social History",
        "oid": "2.16.840.1.113883.10.20.22.2.17 : 2015-08-01",
        "data_elements": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Description", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Dates Observed", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Problems",
        "oid": "2.16.840.1.113883.10.20.22.2.5.1 : 2015-08-01",
        "data_elements": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system": "SNOMED (2.16.840.1.113883.6.96) and ICD10"},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Active date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Medications",
        "oid": "2.16.840.1.113883.10.20.22.2.1.1 : 2014-06-09",
        "data_elements": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", "code_system": "RxNorm (2.16.840.1.113883.6.88) and NDC"},
            {"name": "Directions", "xpath": None, "code_system": None},
            {"name": "Start Date", "xpath": None, "code_system": None},
            {"name": "End Date", "xpath": None, "code_system": None},
            {"name": "Status", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Medication Allergies",
        "oid": "2.16.840.1.113883.10.20.22.2.6.1 : 2015-08-01",
        "data_elements": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system": "RxNorm (2.16.840.1.113883.6.88)"},
            {"name": "Reaction", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Severity", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Status", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section": "Laboratory Tests",
        "oid": None,
        "data_elements": [
            {"name": "Test Code", "xpath": None, "code_system": None},
            {"name": "Code System", "xpath": None, "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Name", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Laboratory Information",
        "oid": None,
        "data_elements": [
            {"name": "Lab Name", "xpath": None, "code_system": None},
            {"name": "Lab Address", "xpath": None, "code_system": None},
            {"name": "Test Report Date", "xpath": None, "code_system": None},
            {"name": "Test Performed", "xpath": None, "code_system": None},
            {"name": "Specimen Source", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Laboratory value(s)/result(s)",
        "oid": "2.16.840.1.113883.10.20.22.2.3.1 : 2015-08-01",
        "data_elements": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Result Value", "xpath": None, "code_system": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system": None},
            {"name": "Interpretation", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Vitals",
        "oid": "2.16.840.1.113883.10.20.22.2.4.1 : 2015-08-01",
        "data_elements": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Observation Date/Time", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Goal",
        "oid": "2.16.840.1.113883.10.20.22.2.60",
        "data_elements": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system": None},
            {"name": "Value", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Procedures",
        "oid": "2.16.840.1.113883.10.20.22.2.7.1 : 2014-06-09",
        "data_elements": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system": "CPT-4 or SNOMED or HCPCS"},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Care team member(s)",
        "oid": "2.16.840.1.113883.10.20.22.2.500 : 2019-07-01",
        "data_elements": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system": None},
            {"name": "Specialty", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Reason for Referral",
        "oid": "1.3.6.1.4.1.19376.1.5.3.1.3.1 : 2014-06-09",
        "data_elements": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section": "Medical Equipment",
        "oid": "2.16.840.1.113883.10.20.22.2.23 : 2014-06-09",
        "data_elements": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "GMDN PT Description", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Mental Status",
        "oid": "2.16.840.1.113883.10.20.22.2.56 : 2015-08-01",
        "data_elements": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None},
            {"name": "Results", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Comments", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Functional Status",
        "oid": "2.16.840.1.113883.10.20.22.2.14 : 2014-06-09",
        "data_elements": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None},
            {"name": "Results", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Comments", "xpath": None, "code_system": None},
        ]
    },
    {
        "section": "Health Concern",
        "oid": "2.16.840.1.113883.10.20.22.2.58 : 2015-08-01",
        "data_elements": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
]

# Build full inventory
entities = []
total_fields = 0
for s in sections:
    fields = []
    for elem in s["data_elements"]:
        fields.append({
            "name": elem["name"],
            "type": None,
            "description": None,
            "xpath": elem.get("xpath"),
            "code_system": elem.get("code_system"),
            "nullable": None,
        })
    total_fields += len(fields)
    entities.append({
        "entity": s["section"],
        "oid": s["oid"],
        "field_count": len(fields),
        "fields": fields,
        "category": "CCD Section"
    })

inventory = {
    "source_file": "downloads/170.315(b)(10)-EHI-export-v3.pdf",
    "export_format": "C-CDA (CCD)",
    "export_standard": "HL7 CDA R2 Consolidated CDA Templates, DSTU R2.1, August 2015",
    "total_sections": len(entities),
    "total_data_elements": total_fields,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "fields_with_code_systems": sum(1 for e in entities for f in e["fields"] if f["code_system"]),
    "entities": entities
}

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Write summary
summary = {
    "source_file": inventory["source_file"],
    "export_format": inventory["export_format"],
    "total_sections": inventory["total_sections"],
    "total_data_elements": inventory["total_data_elements"],
    "fields_with_descriptions": inventory["fields_with_descriptions"],
    "fields_with_types": inventory["fields_with_types"],
    "fields_with_code_systems": inventory["fields_with_code_systems"],
    "sections_summary": [
        {
            "section": e["entity"],
            "oid": e["oid"],
            "field_count": e["field_count"]
        }
        for e in entities
    ]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Export Format: {inventory['export_format']}")
print(f"Total CCD Sections: {inventory['total_sections']}")
print(f"Total Data Elements: {inventory['total_data_elements']}")
print(f"Fields with code systems: {inventory['fields_with_code_systems']}")
print(f"Fields with descriptions: {inventory['fields_with_descriptions']}")
print(f"Fields with types: {inventory['fields_with_types']}")
print()
for e in entities:
    print(f"  {e['entity']}: {e['field_count']} elements")
