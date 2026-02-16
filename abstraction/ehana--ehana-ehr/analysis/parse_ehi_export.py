#!/usr/bin/env python3
"""
Parse eHana EHI Export PDF content into structured JSON inventories.

The EHI_Export.pdf is image-based (no extractable text), so this script
encodes the 18 C-CDA sections and their XML elements as cataloged from
visual inspection of all 15 rendered pages.

Each section's fields are derived from the XML snippets shown in the PDF.
"""

import json
from pathlib import Path

SECTIONS = [
    {
        "section_name": "Electronic Chart / Patient Data",
        "ccda_section": "recordTarget / patientRole",
        "pdf_page": 3,
        "description": "Patient demographics including name, DOB, sex, race, ethnicity, language, address, and telecom",
        "fields": [
            {"name": "name/given", "type": "string", "description": "Patient first name", "code_system": None, "example": "Alice"},
            {"name": "name/family", "type": "string", "description": "Patient last name", "code_system": None, "example": "Newman"},
            {"name": "birthTime", "type": "date", "description": "Date of birth", "code_system": None, "example": "19700501"},
            {"name": "administrativeGenderCode", "type": "code", "description": "Administrative gender", "code_system": "HL7 AdministrativeGender", "example": "F"},
            {"name": "raceCode", "type": "code", "description": "Patient race", "code_system": "CDC Race and Ethnicity", "example": "2106-3 (White)"},
            {"name": "ethnicGroupCode", "type": "code", "description": "Patient ethnicity", "code_system": "CDC Race and Ethnicity", "example": "2186-5 (Not Hispanic or Latino)"},
            {"name": "languageCommunication/languageCode", "type": "code", "description": "Preferred language", "code_system": None, "example": "en"},
            {"name": "addr/streetAddressLine", "type": "string", "description": "Street address", "code_system": None, "example": "1357 Amber Dr"},
            {"name": "addr/city", "type": "string", "description": "City", "code_system": None, "example": "Beaverton"},
            {"name": "addr/state", "type": "string", "description": "State", "code_system": None, "example": "OR"},
            {"name": "addr/postalCode", "type": "string", "description": "Postal code", "code_system": None, "example": "97006"},
            {"name": "addr/country", "type": "string", "description": "Country", "code_system": None, "example": "US"},
            {"name": "telecom", "type": "string", "description": "Phone number", "code_system": None, "example": "tel:+1(555)777-1234"},
        ]
    },
    {
        "section_name": "Vital Signs",
        "ccda_section": "Vital Signs Section (entries required) 2.16.840.1.113883.10.20.22.2.4.1",
        "pdf_page": 4,
        "description": "Vital sign observations with LOINC codes, values, units, and interpretation",
        "fields": [
            {"name": "code", "type": "code", "description": "Vital sign type", "code_system": "LOINC", "example": "85354-9 (Blood pressure panel)"},
            {"name": "effectiveTime", "type": "datetime", "description": "Observation date/time", "code_system": None, "example": "201908151030-0800"},
            {"name": "component/code", "type": "code", "description": "Component type (e.g., systolic, diastolic)", "code_system": "LOINC", "example": "8480-6 (Systolic BP)"},
            {"name": "component/value", "type": "physical_quantity", "description": "Measured value with units", "code_system": "UCUM", "example": "120 mm[Hg]"},
            {"name": "interpretationCode", "type": "code", "description": "Interpretation of result", "code_system": "HL7 ObservationInterpretation", "example": "N (Normal)"},
            {"name": "statusCode", "type": "code", "description": "Status of the observation", "code_system": None, "example": "completed"},
        ]
    },
    {
        "section_name": "Immunization",
        "ccda_section": "Immunizations Section (entries required) 2.16.840.1.113883.10.20.22.2.2.1",
        "pdf_page": 4,
        "description": "Immunization records with vaccine codes, lot numbers, and manufacturers",
        "fields": [
            {"name": "vaccineCode", "type": "code", "description": "Vaccine administered (CVX code)", "code_system": "CVX", "example": "88 (Influenza)"},
            {"name": "effectiveTime", "type": "datetime", "description": "Administration date", "code_system": None, "example": "20190815"},
            {"name": "lotNumberText", "type": "string", "description": "Vaccine lot number", "code_system": None, "example": "1"},
            {"name": "manufacturerOrganization/name", "type": "string", "description": "Vaccine manufacturer", "code_system": None, "example": "Manufacturer Name"},
            {"name": "statusCode", "type": "code", "description": "Administration status", "code_system": None, "example": "completed"},
            {"name": "routeCode", "type": "code", "description": "Route of administration", "code_system": None, "example": "C28161 (Intramuscular)"},
        ]
    },
    {
        "section_name": "Allergies, Adverse Reactions, Alerts",
        "ccda_section": "Allergies and Intolerances Section (entries required) 2.16.840.1.113883.10.20.22.2.6.1",
        "pdf_page": 5,
        "description": "Patient allergies with substance, severity, reaction, and status",
        "fields": [
            {"name": "participant/playingEntity/code", "type": "code", "description": "Allergen substance", "code_system": "RxNorm/SNOMED-CT", "example": "Penicillin"},
            {"name": "value", "type": "code", "description": "Allergy type (drug, food, etc.)", "code_system": "SNOMED-CT", "example": "419199007 (Allergy to substance)"},
            {"name": "effectiveTime/low", "type": "date", "description": "Onset date", "code_system": None, "example": "20140103"},
            {"name": "entryRelationship/observation (severity)", "type": "code", "description": "Severity of allergy", "code_system": "SNOMED-CT", "example": "24484000 (Severe)"},
            {"name": "entryRelationship/observation (reaction)", "type": "code", "description": "Allergic reaction", "code_system": "SNOMED-CT", "example": "Hives"},
            {"name": "statusCode", "type": "code", "description": "Allergy status", "code_system": None, "example": "active"},
        ]
    },
    {
        "section_name": "History of Medication Use",
        "ccda_section": "Medications Section (entries required) 2.16.840.1.113883.10.20.22.2.1.1",
        "pdf_page": 6,
        "description": "Medication history with RxNorm codes, dosing, route, and frequency",
        "fields": [
            {"name": "manufacturedMaterial/code", "type": "code", "description": "Medication code", "code_system": "RxNorm", "example": "Clopidogrel 75 MG"},
            {"name": "effectiveTime/low", "type": "date", "description": "Start date", "code_system": None, "example": "20120806"},
            {"name": "effectiveTime/high", "type": "date", "description": "End date", "code_system": None, "example": None},
            {"name": "doseQuantity", "type": "physical_quantity", "description": "Dose amount", "code_system": None, "example": "1"},
            {"name": "routeCode", "type": "code", "description": "Route of administration", "code_system": "NCI Thesaurus", "example": "C38288 (Oral)"},
            {"name": "effectiveTime (frequency)", "type": "period", "description": "Dosing frequency", "code_system": None, "example": "every 12 hours"},
            {"name": "statusCode", "type": "code", "description": "Medication status", "code_system": None, "example": "active"},
        ]
    },
    {
        "section_name": "Instructions",
        "ccda_section": "Instructions Section 2.16.840.1.113883.10.20.22.2.45",
        "pdf_page": 7,
        "description": "Patient instructions as free text",
        "fields": [
            {"name": "text", "type": "string", "description": "Instruction text content", "code_system": None, "example": "Patient care instructions"},
            {"name": "code", "type": "code", "description": "Instruction type code", "code_system": "SNOMED-CT", "example": None},
        ]
    },
    {
        "section_name": "Functional and Cognitive Status",
        "ccda_section": "Functional Status Section 2.16.840.1.113883.10.20.22.2.14",
        "pdf_page": 7,
        "description": "Functional and cognitive status observations with SNOMED codes",
        "fields": [
            {"name": "code", "type": "code", "description": "Status type (functional/cognitive)", "code_system": "SNOMED-CT", "example": "Cognitive function finding"},
            {"name": "value", "type": "code", "description": "Status finding", "code_system": "SNOMED-CT", "example": "Cognitive function finding"},
            {"name": "effectiveTime", "type": "datetime", "description": "Assessment date", "code_system": None, "example": "20190815"},
            {"name": "statusCode", "type": "code", "description": "Observation status", "code_system": None, "example": "completed"},
        ]
    },
    {
        "section_name": "Chief Complaint / Reason For Visit",
        "ccda_section": "Chief Complaint Section 1.3.6.1.4.1.19376.1.5.3.1.1.13.2.1",
        "pdf_page": 8,
        "description": "Chief complaint or reason for visit as free text",
        "fields": [
            {"name": "text", "type": "string", "description": "Chief complaint narrative", "code_system": None, "example": "Dark stools"},
        ]
    },
    {
        "section_name": "Problem List",
        "ccda_section": "Problem Section (entries required) 2.16.840.1.113883.10.20.22.2.5.1",
        "pdf_page": 8,
        "description": "Active and resolved problems/diagnoses with SNOMED codes and status",
        "fields": [
            {"name": "value", "type": "code", "description": "Problem/diagnosis code", "code_system": "SNOMED-CT", "example": "233604007 (Pneumonia)"},
            {"name": "effectiveTime/low", "type": "date", "description": "Onset date", "code_system": None, "example": "20120806"},
            {"name": "effectiveTime/high", "type": "date", "description": "Resolution date", "code_system": None, "example": None},
            {"name": "statusCode", "type": "code", "description": "Problem status", "code_system": None, "example": "active"},
            {"name": "entryRelationship/observation (status)", "type": "code", "description": "Clinical status observation", "code_system": "SNOMED-CT", "example": "55561003 (Active)"},
        ]
    },
    {
        "section_name": "Social History",
        "ccda_section": "Social History Section 2.16.840.1.113883.10.20.22.2.17",
        "pdf_page": 9,
        "description": "Social history including smoking status and birth sex",
        "fields": [
            {"name": "code (smoking)", "type": "code", "description": "Smoking status observation code", "code_system": "SNOMED-CT", "example": "72166-2"},
            {"name": "value (smoking)", "type": "code", "description": "Smoking status value", "code_system": "SNOMED-CT", "example": "449868002 (Current every day smoker)"},
            {"name": "effectiveTime (smoking)", "type": "date", "description": "Observation date", "code_system": None, "example": "20190815"},
            {"name": "code (birth sex)", "type": "code", "description": "Birth sex observation code", "code_system": "LOINC", "example": "76689-9"},
            {"name": "value (birth sex)", "type": "code", "description": "Birth sex value", "code_system": "HL7 AdministrativeGender", "example": "F (Female)"},
        ]
    },
    {
        "section_name": "Encounters",
        "ccda_section": "Encounters Section (entries required) 2.16.840.1.113883.10.20.22.2.22.1",
        "pdf_page": 10,
        "description": "Encounter records with diagnoses, providers, and facility information",
        "fields": [
            {"name": "code", "type": "code", "description": "Encounter type", "code_system": "CPT", "example": "99213 (Office visit)"},
            {"name": "effectiveTime", "type": "datetime", "description": "Encounter date/time", "code_system": None, "example": "20190815"},
            {"name": "performer/assignedEntity", "type": "complex", "description": "Performing provider", "code_system": None, "example": "Provider name and NPI"},
            {"name": "participant/location", "type": "complex", "description": "Facility/location", "code_system": None, "example": "Facility name and address"},
            {"name": "entryRelationship/act (diagnosis)", "type": "code", "description": "Encounter diagnosis", "code_system": "SNOMED-CT", "example": "Diagnosis code"},
        ]
    },
    {
        "section_name": "Results",
        "ccda_section": "Results Section (entries required) 2.16.840.1.113883.10.20.22.2.3.1",
        "pdf_page": 11,
        "description": "Laboratory results with LOINC codes, values, units, reference ranges, and interpretation",
        "fields": [
            {"name": "code (organizer)", "type": "code", "description": "Result panel/battery code", "code_system": "LOINC", "example": "57021-8 (CBC W Auto Differential panel)"},
            {"name": "code (observation)", "type": "code", "description": "Individual test code", "code_system": "LOINC", "example": "718-7 (Hemoglobin)"},
            {"name": "value", "type": "physical_quantity", "description": "Result value with units", "code_system": "UCUM", "example": "13.2 g/dL"},
            {"name": "referenceRange/value", "type": "range", "description": "Normal reference range", "code_system": None, "example": "12.0-15.5 g/dL"},
            {"name": "interpretationCode", "type": "code", "description": "Result interpretation", "code_system": "HL7 ObservationInterpretation", "example": "N (Normal)"},
            {"name": "effectiveTime", "type": "datetime", "description": "Result date/time", "code_system": None, "example": "20190815"},
            {"name": "statusCode", "type": "code", "description": "Result status", "code_system": None, "example": "completed"},
        ]
    },
    {
        "section_name": "Procedures",
        "ccda_section": "Procedures Section (entries required) 2.16.840.1.113883.10.20.22.2.7.1",
        "pdf_page": 12,
        "description": "Procedures performed with SNOMED codes and dates",
        "fields": [
            {"name": "code", "type": "code", "description": "Procedure code", "code_system": "SNOMED-CT", "example": "Procedure code"},
            {"name": "effectiveTime", "type": "datetime", "description": "Procedure date", "code_system": None, "example": "20190815"},
            {"name": "statusCode", "type": "code", "description": "Procedure status", "code_system": None, "example": "completed"},
            {"name": "targetSiteCode", "type": "code", "description": "Body site", "code_system": "SNOMED-CT", "example": None},
            {"name": "performer", "type": "complex", "description": "Performing provider", "code_system": None, "example": None},
        ]
    },
    {
        "section_name": "Reason for Referral",
        "ccda_section": "Reason for Referral Section 1.3.6.1.4.1.19376.1.5.3.1.3.1",
        "pdf_page": 12,
        "description": "Referral reason as narrative text",
        "fields": [
            {"name": "text", "type": "string", "description": "Referral reason narrative", "code_system": None, "example": "Referral text"},
        ]
    },
    {
        "section_name": "Implantable Devices",
        "ccda_section": "Medical Equipment Section 2.16.840.1.113883.10.20.22.2.23",
        "pdf_page": 13,
        "description": "Implantable device records with UDI and device descriptions",
        "fields": [
            {"name": "id (UDI)", "type": "string", "description": "Unique Device Identifier", "code_system": None, "example": "UDI string"},
            {"name": "code", "type": "code", "description": "Device type code", "code_system": "SNOMED-CT", "example": "Device type"},
            {"name": "playingDevice/code", "type": "code", "description": "Device code", "code_system": None, "example": "Device code"},
            {"name": "playingDevice/name", "type": "string", "description": "Device description/name", "code_system": None, "example": None},
            {"name": "effectiveTime", "type": "date", "description": "Implant date", "code_system": None, "example": None},
            {"name": "statusCode", "type": "code", "description": "Device status", "code_system": None, "example": "completed"},
        ]
    },
    {
        "section_name": "Health Concerns",
        "ccda_section": "Health Concerns Section 2.16.840.1.113883.10.20.22.2.58",
        "pdf_page": 14,
        "description": "Health concern observations with SNOMED codes",
        "fields": [
            {"name": "code", "type": "code", "description": "Health concern code", "code_system": "SNOMED-CT", "example": "Health concern"},
            {"name": "value", "type": "code", "description": "Concern value/finding", "code_system": "SNOMED-CT", "example": None},
            {"name": "effectiveTime", "type": "date", "description": "Concern date", "code_system": None, "example": None},
            {"name": "statusCode", "type": "code", "description": "Concern status", "code_system": None, "example": "active"},
        ]
    },
    {
        "section_name": "Assessment and Plan",
        "ccda_section": "Assessment and Plan Section 2.16.840.1.113883.10.20.22.2.9",
        "pdf_page": 14,
        "description": "Clinical assessment narrative and structured plan entries",
        "fields": [
            {"name": "text (assessment)", "type": "string", "description": "Assessment narrative text", "code_system": None, "example": "The patient was found to..."},
            {"name": "act/code (plan)", "type": "code", "description": "Plan activity code", "code_system": None, "example": None},
            {"name": "act/text (plan)", "type": "string", "description": "Plan activity description", "code_system": None, "example": None},
            {"name": "effectiveTime", "type": "date", "description": "Plan date", "code_system": None, "example": None},
        ]
    },
    {
        "section_name": "Goals",
        "ccda_section": "Goals Section 2.16.840.1.113883.10.20.22.2.60",
        "pdf_page": 15,
        "description": "Patient goals with status and target dates",
        "fields": [
            {"name": "code", "type": "code", "description": "Goal code", "code_system": "SNOMED-CT", "example": None},
            {"name": "value", "type": "string", "description": "Goal description/target", "code_system": None, "example": None},
            {"name": "effectiveTime", "type": "date", "description": "Goal target date", "code_system": None, "example": None},
            {"name": "statusCode", "type": "code", "description": "Goal status", "code_system": None, "example": "active"},
        ]
    },
]


def build_full_inventory():
    """Build entity-inventory-full.json from cataloged sections."""
    entities = []
    for section in SECTIONS:
        entity = {
            "entity_name": section["section_name"],
            "ccda_template_id": section["ccda_section"],
            "pdf_page": section["pdf_page"],
            "description": section["description"],
            "vendor_category": "Clinical (C-CDA)",
            "field_count": len(section["fields"]),
            "fields": []
        }
        for field in section["fields"]:
            entity["fields"].append({
                "name": field["name"],
                "type": field["type"],
                "description": field["description"],
                "code_system": field["code_system"],
                "example_value": field["example"],
                "has_description": bool(field["description"]),
                "has_type": bool(field["type"]),
            })
        entities.append(entity)
    return entities


def build_summary(entities):
    """Build entity-inventory-summary.json from full inventory."""
    total_fields = sum(e["field_count"] for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e["fields"] if f["has_description"]
    )
    fields_with_type = sum(
        1 for e in entities for f in e["fields"] if f["has_type"]
    )
    fields_with_code_system = sum(
        1 for e in entities for f in e["fields"] if f.get("code_system")
    )
    fields_with_example = sum(
        1 for e in entities for f in e["fields"] if f.get("example_value")
    )

    return {
        "product": "eHana EHR",
        "export_format": "C-CDA (CDA R2) XML",
        "source_artifact": "downloads/EHI_Export.pdf (15 pages, image-based)",
        "total_sections": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "fields_with_code_systems": fields_with_code_system,
        "fields_with_examples": fields_with_example,
        "description_coverage_pct": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
        "sections": [
            {
                "name": e["entity_name"],
                "ccda_template": e["ccda_template_id"],
                "pdf_page": e["pdf_page"],
                "field_count": e["field_count"],
                "description": e["description"],
            }
            for e in entities
        ],
        "assessment": {
            "is_data_dictionary": False,
            "is_standard_ccda": True,
            "documentation_type": "XML examples with screenshots — not a field-level data dictionary",
            "notable_gaps": [
                "No billing/claims data (837/835 — product handles claims submission)",
                "No behavioral health service notes (product generates 600K+ docs/month)",
                "No program enrollment records (multi-program tracking is a core feature)",
                "No CANS assessments (child/adolescent needs — key MA behavioral health tool)",
                "No scanned/uploaded documents",
                "No secure messaging / patient communications",
                "No e-prescribing detail beyond medication list",
                "No scheduling/appointment data",
                "No incident reports",
                "No care coordination records beyond referral reason text",
                "No insurance/coverage details beyond what's in C-CDA header",
            ],
        },
    }


if __name__ == "__main__":
    out_dir = Path(__file__).parent

    entities = build_full_inventory()
    full_path = out_dir / "entity-inventory-full.json"
    full_path.write_text(json.dumps(entities, indent=2))
    print(f"Wrote {full_path} ({len(entities)} entities)")

    summary = build_summary(entities)
    summary_path = out_dir / "entity-inventory-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"Wrote {summary_path}")
    print(f"  Sections: {summary['total_sections']}")
    print(f"  Fields: {summary['total_fields']}")
    print(f"  With descriptions: {summary['fields_with_descriptions']} ({summary['description_coverage_pct']}%)")
    print(f"  With code systems: {summary['fields_with_code_systems']}")
    print(f"  With examples: {summary['fields_with_examples']}")
