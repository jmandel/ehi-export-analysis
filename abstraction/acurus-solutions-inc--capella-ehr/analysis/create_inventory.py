#!/usr/bin/env python3
"""Create a clean, hand-verified inventory of the CCD sections and fields
from the (b)(10) EHI export PDF.

The PDF table layout causes line wrapping that breaks automatic parsing.
This script produces a manually-verified structure based on direct reading
of the PDF text.
"""

import json

# Each section is manually verified against the pdftotext output of
# 170.315(b)(10)-EHI-export-v3.pdf (pages 4-8)

sections = [
    {
        "section_name": "Patient Demographics/Information",
        "template_id": None,
        "fields": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system": "AdministrativeGender (2.16.840.1.113883.5.1)"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system": "Race & Ethnicity - CDC (2.16.840.1.113883.6.238)"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system": "Race & Ethnicity - CDC (2.16.840.1.113883.6.238)"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system": None},
        ]
    },
    {
        "section_name": "Provider's name and office contact information",
        "template_id": None,
        "fields": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system": None},
            {"name": "Performer Telecom", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system": None},
        ]
    },
    {
        "section_name": "Date and Location of visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "fields": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system": None},
        ]
    },
    {
        "section_name": "Chief Complaint and Reason for visit",
        "template_id": "2.16.840.1.113883.10.20.22.2.13 : 2014-06-09",
        "fields": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Encounters",
        "template_id": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "fields": [
            {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system": "CPT (2.16.840.1.113883.6.12)"},
            {"name": "Performer", "xpath": None, "code_system": None},
            {"name": "Diagnosis", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96) and ICD-10 (2.16.840.1.113883.6.3)"},
            {"name": "Location", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Immunizations",
        "template_id": "2.16.840.1.113883.10.20.22.2.2.1 : 2015-08-01",
        "fields": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52: 2015-08-01", "code_system": "CVX (2.16.840.1.113883.12.292) and CPT-4 (2.16.840.1.113883.6.12)"},
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
        "section_name": "Instructions",
        "template_id": "2.16.840.1.113883.10.20.22.2.45 : 2014-06-09",
        "fields": [
            {"name": "Patient Instructions/Followup Reasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section_name": "Treatment Plan",
        "template_id": "2.16.840.1.113883.10.20.22.2.10 : 2014-06-09",
        "fields": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.39: 2014-06-09 / 2.16.840.1.113883.10.20.22.4.121", "code_system": None},
        ]
    },
    {
        "section_name": "Social History",
        "template_id": "2.16.840.1.113883.10.20.22.2.17 : 2015-08-01",
        "fields": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Description", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Dates Observed", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Problems",
        "template_id": "2.16.840.1.113883.10.20.22.2.5.1 : 2015-08-01",
        "fields": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system": "SNOMED (2.16.840.1.113883.6.96) and ICD-10 (2.16.840.1.113883.6.3)"},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Active date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Medications",
        "template_id": "2.16.840.1.113883.10.20.22.2.1.1 : 2014-06-09",
        "fields": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", "code_system": "RxNorm (2.16.840.1.113883.6.88) and NDC (2.16.840.1.113883.6.69)"},
            {"name": "Directions", "xpath": None, "code_system": None},
            {"name": "Start Date", "xpath": None, "code_system": None},
            {"name": "End Date", "xpath": None, "code_system": None},
            {"name": "Status", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Medication Allergies",
        "template_id": "2.16.840.1.113883.10.20.22.2.6.1 : 2015-08-01",
        "fields": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system": "RxNorm (2.16.840.1.113883.6.88)"},
            {"name": "Reaction", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Severity", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Status", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section_name": "Laboratory Tests",
        "template_id": None,
        "fields": [
            {"name": "Test Code", "xpath": None, "code_system": None},
            {"name": "Code System", "xpath": None, "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Name", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Laboratory Information",
        "template_id": None,
        "fields": [
            {"name": "Lab Name", "xpath": None, "code_system": None},
            {"name": "Lab Address", "xpath": None, "code_system": None},
            {"name": "Test Report Date", "xpath": None, "code_system": None},
            {"name": "Test Performed", "xpath": None, "code_system": None},
            {"name": "Specimen Source", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Laboratory value(s)/result(s)",
        "template_id": "2.16.840.1.113883.10.20.22.2.3.1 : 2015-08-01",
        "fields": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Result Value", "xpath": None, "code_system": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system": None},
            {"name": "Interpretation", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Vitals",
        "template_id": "2.16.840.1.113883.10.20.22.2.4.1 : 2015-08-01",
        "fields": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system": "LOINC (2.16.840.1.113883.6.1)"},
            {"name": "Observation Date/Time", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Goal",
        "template_id": "2.16.840.1.113883.10.20.22.2.60",
        "fields": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system": None},
            {"name": "Value", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Procedures",
        "template_id": "2.16.840.1.113883.10.20.22.2.7.1 : 2014-06-09",
        "fields": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system": "CPT-4 (2.16.840.1.113883.6.12) or SNOMED (2.16.840.1.113883.6.96) or HCPCS (2.16.840.1.113883.6.13)"},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Care team member(s)",
        "template_id": "2.16.840.1.113883.10.20.22.2.500 : 2019-07-01",
        "fields": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system": None},
            {"name": "Specialty", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Reason for Referral",
        "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1 : 2014-06-09",
        "fields": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
        ]
    },
    {
        "section_name": "Medical Equipment (Implanted Devices)",
        "template_id": "2.16.840.1.113883.10.20.22.2.23 : 2014-06-09",
        "fields": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "GMDN PT Description", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Mental Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.56 : 2015-08-01",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None},
            {"name": "Results", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Comments", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Functional Status",
        "template_id": "2.16.840.1.113883.10.20.22.2.14 : 2014-06-09",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system": None},
            {"name": "Assessment Date", "xpath": None, "code_system": None},
            {"name": "Results", "xpath": None, "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Comments", "xpath": None, "code_system": None},
        ]
    },
    {
        "section_name": "Health Concern",
        "template_id": "2.16.840.1.113883.10.20.22.2.58 : 2015-08-01",
        "fields": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system": "SNOMED (2.16.840.1.113883.6.96)"},
            {"name": "Status", "xpath": None, "code_system": None},
            {"name": "Date", "xpath": None, "code_system": None},
        ]
    },
]

# Compute stats
total_fields = sum(len(s["fields"]) for s in sections)
fields_with_code_system = sum(
    1 for s in sections for f in s["fields"] if f.get("code_system")
)
fields_with_xpath = sum(
    1 for s in sections for f in s["fields"] if f.get("xpath")
)

inventory = {
    "source_file": "170.315(b)(10)-EHI-export-v3.pdf",
    "source_date": "2023-09-05",
    "document_version": "v3",
    "document_pages": 9,
    "export_format": "C-CDA CCD (Consolidated CDA Release 2.1 DSTU)",
    "standard_reference": "§170.205(a)(4) HL7 CDA R2 Consolidated CDA Templates for Clinical Notes (US Realm) DSTU 2.1 August 2015",
    "export_modes": [
        {
            "mode": "Single Patient Export",
            "description": "User selects sections via checkboxes and clicks 'Generate CCD'. Outputs CCD XML and Adobe PDF."
        },
        {
            "mode": "Bulk Export",
            "description": "User selects multiple patients by provider and/or date range. Generates CCD for all selected patients."
        },
        {
            "mode": "Export Scheduler",
            "description": "Non-recurring (specific date/time) or recurring (start date, frequency) export to a configurable destination path."
        }
    ],
    "additional_capabilities": "Ability to download Images / Clinical notes on demand (separate from CCD export, printed in Adobe PDF format).",
    "summary": {
        "total_sections": len(sections),
        "total_fields": total_fields,
        "fields_with_xpath_or_template": fields_with_xpath,
        "fields_with_code_system": fields_with_code_system,
    },
    "sections": sections
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Total sections: {len(sections)}")
print(f"Total fields: {total_fields}")
print(f"Fields with XPATH/template ID: {fields_with_xpath}")
print(f"Fields with code system: {fields_with_code_system}")
print()
for s in sections:
    coded = sum(1 for f in s["fields"] if f.get("code_system"))
    print(f"  {s['section_name']:45s} {len(s['fields']):2d} fields  ({coded} coded)")

print(f"\nSaved to full-entity-inventory.json")
