#!/usr/bin/env python3
"""Parse VertexDr EHI Export Documentation PDF to extract all data elements.

Reads the PDF text and extracts:
1. C-CDA section definitions with data elements (pages 6-10)
2. Non-CCD PDF export sections (page 11)
3. FHIR export mention (page 11)
"""

import json
import re
import subprocess

result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/VertexDr-b10-EHI-Export-Documentation.pdf", "-"],
    capture_output=True, text=True
)
text = result.stdout
lines = text.split('\n')

# Manually define the C-CDA sections based on careful reading of the PDF
# The table on pages 6-10 has sections with OIDs and data elements
ccda_sections = [
    {
        "name": "Patient Demographics/Information",
        "oid": None,
        "fields": [
            {"name": "Patient Name", "xpath": "patient/name", "code_system_oid": None, "code_system_name": None},
            {"name": "Sex", "xpath": "patient/administrativeGenderCode", "code_system_oid": "2.16.840.1.113883.5.1", "code_system_name": "AdministrativeGender"},
            {"name": "Date of Birth", "xpath": "patient/birthTime", "code_system_oid": None, "code_system_name": None},
            {"name": "Race", "xpath": "patient/raceCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Ethnicity", "xpath": "patient/ethnicGroupCode", "code_system_oid": "2.16.840.1.113883.6.238", "code_system_name": "Race & Ethnicity - CDC"},
            {"name": "Preferred Language", "xpath": "patient/languageCommunication/languageCode", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Provider's name and office contact information",
        "oid": None,
        "fields": [
            {"name": "Performer Name", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/assignedPerson/name", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Phone", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/telecom", "code_system_oid": None, "code_system_name": None},
            {"name": "Performer Address", "xpath": "documentationOf/serviceEvent/performer/assignedEntity/addr", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Date and Location of visit",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "fields": [
            {"name": "Encounter Date", "xpath": "entry/encounter/effectiveTime/@value", "code_system_oid": None, "code_system_name": None},
            {"name": "Encounter Location", "xpath": "entry/encounter/participant/participantRole/addr", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Chief Complaint and Reason for visit",
        "oid": "2.16.840.1.113883.10.20.22.2.13 : 2014-06-09",
        "fields": [
            {"name": "Patient visit details/complaints", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Encounters",
        "oid": "2.16.840.1.113883.10.20.22.2.22.1 : 2015-08-01",
        "fields": [
            {"name": "Encounter Code and Code Description", "xpath": "2.16.840.1.113883.10.20.22.4.49: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.12", "code_system_name": "CPT"},
            {"name": "Performer", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Diagnosis", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Location", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Immunizations",
        "oid": "2.16.840.1.113883.10.20.22.2.2.1 : 2015-08-01",
        "fields": [
            {"name": "Vaccine", "xpath": "2.16.840.1.113883.10.20.22.4.52: 2015-08-01", "code_system_oid": "2.16.840.1.113883.12.292 and 2.16.840.1.113883.6.12", "code_system_name": "CVX and CPT-4"},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Route", "xpath": None, "code_system_oid": "2.16.840.1.113883.3.26.1.1", "code_system_name": "NCI Thesaurus"},
            {"name": "Site", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Manufacturer", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Dose", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lot Number", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Notes", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Instructions",
        "oid": "2.16.840.1.113883.10.20.22.2.45 : 2014-06-09",
        "fields": [
            {"name": "Patient Instructions/FollowupReasons", "xpath": "2.16.840.1.113883.10.20.22.4.20: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "name": "Treatment Plan",
        "oid": "2.16.840.1.113883.10.20.22.2.10 : 2014-06-09",
        "fields": [
            {"name": "Planned Observation", "xpath": "2.16.840.1.113883.10.20.22.4.44: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Planned Date", "xpath": "2.16.840.1.113883.10.20.22.4.40: 2014-06-09", "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Social History",
        "oid": "2.16.840.1.113883.10.20.22.2.17 : 2015-08-01",
        "fields": [
            {"name": "Social History Observation", "xpath": "2.16.840.1.113883.10.20.22.4.78: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Description", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Dates Observed", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Problems",
        "oid": "2.16.840.1.113883.10.20.22.2.5.1 : 2015-08-01",
        "fields": [
            {"name": "Problem", "xpath": "2.16.840.1.113883.10.20.22.4.3: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96 and 2.16.840.1.113883.6.3", "code_system_name": "SNOMED and ICD10"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Active date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Medications",
        "oid": "2.16.840.1.113883.10.20.22.2.1.1 : 2014-06-09",
        "fields": [
            {"name": "Medication", "xpath": "2.16.840.1.113883.10.20.22.4.16: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.88 and 2.16.840.1.113883.6.69", "code_system_name": "RxNorm and NDC"},
            {"name": "Directions", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Start Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "End Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Medication Allergies",
        "oid": "2.16.840.1.113883.10.20.22.2.6.1 : 2015-08-01",
        "fields": [
            {"name": "Substance", "xpath": "2.16.840.1.113883.10.20.22.4.30: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.88", "code_system_name": "RxNorm"},
            {"name": "Reaction", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Severity", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "name": "Laboratory Tests",
        "oid": None,
        "fields": [
            {"name": "Test Code", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Code System", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Laboratory Information",
        "oid": None,
        "fields": [
            {"name": "Lab Name", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Lab Address", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Report Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Test Performed", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Specimen Source", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Laboratory value(s)/result(s)",
        "oid": "2.16.840.1.113883.10.20.22.2.3.1 : 2015-08-01",
        "fields": [
            {"name": "Result Type", "xpath": "2.16.840.1.113883.10.20.22.4.1: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Result Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Relevant Reference Range", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Interpretation", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Vitals",
        "oid": "2.16.840.1.113883.10.20.22.2.4.1 : 2015-08-01",
        "fields": [
            {"name": "Observation", "xpath": "2.16.840.1.113883.10.20.22.4.26: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.1", "code_system_name": "LOINC"},
            {"name": "Observation Date/Time", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Goal",
        "oid": "2.16.840.1.113883.10.20.22.2.60",
        "fields": [
            {"name": "Goal", "xpath": "2.16.840.1.113883.10.20.22.4.121", "code_system_oid": None, "code_system_name": None},
            {"name": "Value", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Procedures",
        "oid": "2.16.840.1.113883.10.20.22.2.7.1 : 2014-06-09",
        "fields": [
            {"name": "Procedure", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.12 or 2.16.840.1.113883.6.96 or 2.16.840.1.113883.6.13", "code_system_name": "CPT-4 or SNOMED or HCPCS"},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Care team member(s)",
        "oid": "2.16.840.1.113883.10.20.22.2.500 : 2019-07-01",
        "fields": [
            {"name": "Care Giver Name", "xpath": "2.16.840.1.113883.10.20.22.4.500: 2019-07-01", "code_system_oid": None, "code_system_name": None},
            {"name": "Specialty", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Reason for Referral",
        "oid": "1.3.6.1.4.1.19376.1.5.3.1.3.1 : 2014-06-09",
        "fields": [
            {"name": "Reason for visit", "xpath": "2.16.840.1.113883.10.20.22.4.140", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
        ]
    },
    {
        "name": "Medical Equipment",
        "oid": "2.16.840.1.113883.10.20.22.2.23 : 2014-06-09",
        "fields": [
            {"name": "Implanted Device", "xpath": "2.16.840.1.113883.10.20.22.4.14: 2014-06-09", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "GMDN PT Description", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Mental Status",
        "oid": "2.16.840.1.113883.10.20.22.2.56 : 2015-08-01",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.74: 2015-08-01", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Functional Status",
        "oid": "2.16.840.1.113883.10.20.22.2.14 : 2014-06-09",
        "fields": [
            {"name": "Assessment", "xpath": "2.16.840.1.113883.10.20.22.4.67: 2014-06-09", "code_system_oid": None, "code_system_name": None},
            {"name": "Assessment Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Results", "xpath": None, "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Comments", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
    {
        "name": "Health Concern",
        "oid": "2.16.840.1.113883.10.20.22.2.58 : 2015-08-01",
        "fields": [
            {"name": "Concern / Observation", "xpath": "2.16.840.1.113883.10.20.22.4.132: 2015-08-01", "code_system_oid": "2.16.840.1.113883.6.96", "code_system_name": "SNOMED"},
            {"name": "Status", "xpath": None, "code_system_oid": None, "code_system_name": None},
            {"name": "Date", "xpath": None, "code_system_oid": None, "code_system_name": None},
        ]
    },
]

# Non-CCD PDF export sections (page 11) - only category-level descriptions, no field detail
pdf_sections = [
    {
        "name": "Patient Demographic/Insurance",
        "format": "PDF",
        "description": "Comprehensive view of demographics and insurance details, structured for clarity and ease of access",
        "fields": [
            {"name": "Demographics (unspecified)", "description": "No field-level detail provided"},
            {"name": "Insurance Details (unspecified)", "description": "No field-level detail provided"},
        ]
    },
    {
        "name": "Advance Directive",
        "format": "PDF",
        "description": "Comprehensive view of Advance Directive, structured for clarity and ease of access",
        "fields": [
            {"name": "Advance Directive (unspecified)", "description": "No field-level detail provided"},
        ]
    },
    {
        "name": "Appointments",
        "format": "PDF",
        "description": "Comprehensive view of appointments, structured for clarity and ease of access",
        "fields": [
            {"name": "Appointments (unspecified)", "description": "No field-level detail provided"},
        ]
    },
    {
        "name": "Provider-to-Patient Messages",
        "format": "PDF",
        "description": "Comprehensive view of messages, structured for clarity and ease of access",
        "fields": [
            {"name": "Messages (unspecified)", "description": "No field-level detail provided"},
        ]
    },
    {
        "name": "Billing Data (Claim)",
        "format": "PDF",
        "description": "Comprehensive view of billing data (CPT, ICD, Modifier), structured for clarity and ease of access",
        "fields": [
            {"name": "CPT Codes", "description": "Procedure codes on claims"},
            {"name": "ICD Codes", "description": "Diagnosis codes on claims"},
            {"name": "Modifiers", "description": "Procedure modifiers on claims"},
        ]
    },
    {
        "name": "Documents",
        "format": "PDF",
        "description": "Signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document",
        "fields": [
            {"name": "Signed Progress Notes", "description": "Clinical progress notes"},
            {"name": "Lab Results (documents)", "description": "Lab result documents"},
            {"name": "Radiology Reports", "description": "Radiology report documents"},
            {"name": "Scanned/Uploaded Documents", "description": "Any other scanned or uploaded documents"},
        ]
    },
]

# Build full inventory
entity_inventory = []

for sec in ccda_sections:
    entity = {
        "entity_name": sec["name"],
        "source": "C-CDA Export",
        "format": "XML (C-CDA)",
        "oid": sec["oid"],
        "field_count": len(sec["fields"]),
        "fields": []
    }
    for f in sec["fields"]:
        entity["fields"].append({
            "name": f["name"],
            "xpath": f["xpath"],
            "code_system_oid": f["code_system_oid"],
            "code_system_name": f["code_system_name"],
            "has_description": False,
            "type": "coded" if f["code_system_oid"] else "text"
        })
    entity_inventory.append(entity)

for sec in pdf_sections:
    entity = {
        "entity_name": sec["name"],
        "source": "PDF Export",
        "format": "PDF",
        "oid": None,
        "field_count": len(sec["fields"]),
        "description": sec["description"],
        "fields": []
    }
    for f in sec["fields"]:
        entity["fields"].append({
            "name": f["name"],
            "description": f.get("description"),
            "has_description": bool(f.get("description")),
            "type": "text",
            "xpath": None,
            "code_system_oid": None,
            "code_system_name": None
        })
    entity_inventory.append(entity)

# FHIR stub
entity_inventory.append({
    "entity_name": "FHIR Data Export",
    "source": "FHIR Bulk Data",
    "format": "FHIR",
    "oid": None,
    "field_count": 0,
    "description": "VertexDr FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population. No further documentation provided.",
    "fields": []
})

# Save full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(entity_inventory, f, indent=2)

# Compute summary
total_entities = len(entity_inventory)
total_fields = sum(e["field_count"] for e in entity_inventory)

ccda_entities = [e for e in entity_inventory if e["source"] == "C-CDA Export"]
pdf_entities = [e for e in entity_inventory if e["source"] == "PDF Export"]
fhir_entities = [e for e in entity_inventory if e["source"] == "FHIR Bulk Data"]

ccda_fields = sum(e["field_count"] for e in ccda_entities)
pdf_fields = sum(e["field_count"] for e in pdf_entities)

fields_with_code_system = sum(
    1 for e in entity_inventory for f in e["fields"]
    if f.get("code_system_oid")
)
fields_with_xpath = sum(
    1 for e in entity_inventory for f in e["fields"]
    if f.get("xpath")
)
fields_with_description = sum(
    1 for e in entity_inventory for f in e["fields"]
    if f.get("has_description")
)

summary = {
    "total_entities": total_entities,
    "total_fields": total_fields,
    "by_source": {
        "C-CDA Export": {"entities": len(ccda_entities), "fields": ccda_fields},
        "PDF Export": {"entities": len(pdf_entities), "fields": pdf_fields},
        "FHIR Bulk Data": {"entities": len(fhir_entities), "fields": 0},
    },
    "fields_with_code_system": fields_with_code_system,
    "fields_with_xpath": fields_with_xpath,
    "fields_with_description": fields_with_description,
    "pct_with_code_system": round(fields_with_code_system / total_fields * 100, 1) if total_fields else 0,
    "pct_with_xpath": round(fields_with_xpath / total_fields * 100, 1) if total_fields else 0,
    "pct_with_description": round(fields_with_description / total_fields * 100, 1) if total_fields else 0,
    "entity_details": [
        {"entity_name": e["entity_name"], "source": e["source"], "field_count": e["field_count"]}
        for e in entity_inventory
    ]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total entities: {total_entities}")
print(f"  C-CDA sections: {len(ccda_entities)} ({ccda_fields} fields)")
print(f"  PDF exports: {len(pdf_entities)} ({pdf_fields} fields)")
print(f"  FHIR (undocumented): {len(fhir_entities)}")
print(f"Total fields: {total_fields}")
print(f"  With code system OID: {fields_with_code_system} ({summary['pct_with_code_system']}%)")
print(f"  With XPATH: {fields_with_xpath} ({summary['pct_with_xpath']}%)")
print(f"  With description: {fields_with_description} ({summary['pct_with_description']}%)")
print()
for e in entity_inventory:
    print(f"  {e['entity_name']:45s} [{e['source']:15s}] {e['field_count']:3d} fields")
