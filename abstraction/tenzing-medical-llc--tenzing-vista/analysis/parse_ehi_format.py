#!/usr/bin/env python3
"""Parse Tenzing EHI Format Info PDF (already extracted via pdftotext) into structured JSON.

The PDF documents two systems:
1. Tenzing VistA - C-CDA sections with HL7 template IDs
2. McKesson Series - Billing/account data sections
"""

import json

# VistA C-CDA sections parsed from TenzingEHIFormatInfo.pdf
vista_sections = [
    {"name": "Care Team", "template_id": "/ClinicalDocument/recordTarget/patientRole/documentationOf/serviceEvent/performer", "description": "Ordering providers, clinical care team"},
    {"name": "Problems", "template_id": "2.16.840.1.113883.10.20.22.2.5.1", "description": "Clinical problem list"},
    {"name": "Vitals", "template_id": "2.16.840.1.113883.10.20.22.2.4.1", "description": "Vital signs (eg blood pressure, heart rate, pulse, blood ox, etc.)"},
    {"name": "Medications", "template_id": "2.16.840.1.113883.10.20.22.2.1.1", "description": "Active and pertinent medication history."},
    {"name": "Admission Medications", "template_id": "2.16.840.1.113883.10.20.22.2.44", "description": "Medications administered during an inpatient stay"},
    {"name": "Ambulatory Medications", "template_id": "2.16.840.1.113883.10.20.22.2.38", "description": "Medications administered during a clinical visit."},
    {"name": "Discharge Medications", "template_id": "2.16.840.1.113883.10.20.22.2.11.1", "description": "Medications ordered upon discharge."},
    {"name": "Allergies and Intolerances", "template_id": "2.16.840.1.113883.10.20.22.2.6.1", "description": "Active and pertinent allergy list."},
    {"name": "Social History / Smoking Status", "template_id": "2.16.840.1.113883.10.20.22.2.17", "description": "Relevant social history and smoking status."},
    {"name": "Assessments", "template_id": "2.16.840.1.113883.10.20.22.2.8", "description": "Impressions/diagnoses guiding treatment."},
    {"name": "Encounter Diagnosis", "template_id": "2.16.840.1.113883.10.20.22.2.22.1", "description": "Relevant problems or diagnoses at the close of a visit w/ visit location and timeframes included."},
    {"name": "Procedures", "template_id": "2.16.840.1.113883.10.20.22.2.7.1", "description": "Interventional, surgical, diagnostic, and therapeutic procedures or treatments"},
    {"name": "Diagnostic Results", "template_id": "2.16.840.1.113883.10.20.22.2.3.1", "description": "Laboratory, radiological, and procedural results."},
    {"name": "Plan of Treatment", "template_id": "2.16.840.1.113883.10.20.22.2.10", "description": "Pending orders, interventions, encounters, services."},
    {"name": "Immunizations", "template_id": "2.16.840.1.113883.10.20.22.2.2.1", "description": "Current and pertinent immunization history."},
    {"name": "Reason For Referral", "template_id": "1.3.6.1.4.1.19376.1.5.3.1.3.1", "description": "Notes related to outside referrals"},
    {"name": "Chief Complaint", "template_id": "2.16.840.1.113883.10.20.22.2.13", "description": "Patient's own description of complaint"},
    {"name": "Admit Diagnosis", "template_id": "2.16.840.1.113883.10.20.22.2.43", "description": "Diagnosis at the time of inpatient admission."},
    {"name": "Discharge Diagnosis", "template_id": "", "description": "Diagnosis at the time of inpatient discharge."},
    {"name": "Instructions", "template_id": "2.16.840.1.113883.10.20.22.2.45", "description": "Provider notes directed to the patient."},
    {"name": "Functional Status", "template_id": "2.16.840.1.113883.10.20.22.2.14", "description": "Observations and assessments of a patient's physical abilities."},
    {"name": "Mental Status", "template_id": "2.16.840.1.113883.10.20.22.2.56", "description": "Observations and evaluations related to patients psychological and mental competency and deficits."},
    {"name": "Notes", "template_id": "2.16.840.1.113883.10.20.22.2.65", "description": "Free text based clinical documentation."},
    {"name": "Discharge Instructions", "template_id": "2.16.840.1.113883.10.20.22.2.41", "description": "Instruction at discharge"},
    {"name": "Medical Equipment", "template_id": "2.16.840.1.113883.10.20.22.2.23", "description": "Implanted and external health and medical devices and equipment."},
    {"name": "Health Concerns", "template_id": "2.16.840.1.113883.10.20.22.2.58", "description": "SDOH-related conditions"},
    {"name": "Goals", "template_id": "2.16.840.1.113883.10.20.22.2.60", "description": "Defined outcome or condition to be achieved in the process of patient care."},
    {"name": "Payers/Insurance", "template_id": "2.16.840.1.113883.10.20.22.2.18", "description": "Insurance and payer information"},
    {"name": "Family History", "template_id": "2.16.840.1.113883.10.20.22.2.15", "description": "Data related to patient's genetic relatives in terms of possible or relevant health risks/factors."},
]

# McKesson Series sections
series_sections = [
    {"name": "Patient", "path": "/Patient", "description": "Patient demographics"},
    {"name": "Payer/Insurance", "path": "/Patient/Payer", "description": "Insurance, payer information"},
    {"name": "Enrollment/Account Information", "path": "/Patient/Account", "description": "Enrollment, account information"},
    {"name": "Billing History", "path": "/Patient/Billing", "description": "Billing history, adjudication, etc."},
]

# Build entity inventory
entities = []

for s in vista_sections:
    entities.append({
        "entity_name": s["name"],
        "system": "Tenzing VistA",
        "category": "Clinical (C-CDA Section)",
        "format": "C-CDA XML",
        "template_id": s["template_id"],
        "description": s["description"],
        "fields": [],  # No field-level detail provided
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "Section-level documentation only; no individual field/element definitions provided"
    })

for s in series_sections:
    entities.append({
        "entity_name": s["name"],
        "system": "McKesson Series",
        "category": "Billing/Administrative",
        "format": "Structured delimited",
        "path": s["path"],
        "description": s["description"],
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "Section-level documentation only; no individual field/element definitions provided"
    })

# Full inventory
full_inventory = {
    "product": "Tenzing VistA",
    "source_file": "downloads/TenzingEHIFormatInfo.pdf",
    "extraction_notes": "Parsed from 3-page PDF. Documentation provides section-level information only (section name, C-CDA template ID, brief description). No field-level data dictionary exists.",
    "systems": [
        {
            "name": "Tenzing VistA",
            "format": "C-CDA XML (CDA R2.1)",
            "section_count": len(vista_sections),
            "description": "Clinical data exported as C-CDA structured XML"
        },
        {
            "name": "McKesson Series",
            "format": "Structured delimited",
            "section_count": len(series_sections),
            "description": "Billing, account, and payer data"
        }
    ],
    "total_entities": len(entities),
    "total_fields_documented": 0,
    "entities": entities
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary
summary = {
    "product": "Tenzing VistA",
    "total_sections": len(entities),
    "vista_ccda_sections": len(vista_sections),
    "series_billing_sections": len(series_sections),
    "total_fields_documented": 0,
    "field_level_documentation": False,
    "sections_with_descriptions": sum(1 for e in entities if e["description"]),
    "sections_with_template_ids": sum(1 for s in vista_sections if s["template_id"]),
    "documentation_depth": "section-level only (no field/element definitions)",
    "clinical_format": "C-CDA XML (CDA R2.1, USCDI v2)",
    "billing_format": "Structured delimited (McKesson Series)",
    "by_system": {
        "Tenzing VistA": {
            "section_count": len(vista_sections),
            "sections": [s["name"] for s in vista_sections]
        },
        "McKesson Series": {
            "section_count": len(series_sections),
            "sections": [s["name"] for s in series_sections]
        }
    }
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total sections/entities: {len(entities)}")
print(f"  Tenzing VistA C-CDA sections: {len(vista_sections)}")
print(f"  McKesson Series sections: {len(series_sections)}")
print(f"Field-level documentation: None (0 individual fields documented)")
print(f"All {len(entities)} sections have descriptions")
print(f"{sum(1 for s in vista_sections if s['template_id'])} of {len(vista_sections)} VistA sections have template IDs")
