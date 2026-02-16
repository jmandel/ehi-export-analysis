#!/usr/bin/env python3
"""Parse SecureEMR+ EHI Export PDF text to extract worksheet names and field details.

Reads the extracted PDF text and produces:
- full-entity-inventory.json: Complete inventory of all worksheets and known fields
- summary-stats.json: Aggregate statistics
"""

import json
import re
from pathlib import Path

ANALYSIS_DIR = Path(__file__).parent

# All 43 worksheets from the PDF (pages 10-11)
STANDARD_WORKSHEETS = [
    "Insurance Master", "Medics", "Referring Provider", "Adjusters",
    "Attorneys", "Employers", "Guarantor", "Patient Demographics",
    "Patient Insurance", "Vaccination", "Health Maintenance", "Family History",
    "Past Medical Hist", "Surgery", "Allergy", "Current Medication",
    "Social History", "Legal Documents", "Other Documents", "Enc Attach Docs",
    "Old Progress Notes", "Messages", "Future Appointments", "Vitals",
    "Diagnosis Codes", "CPT Codes", "HCPC Codes", "CCD",
    "Prescriptions", "Lab Results", "Rad Results", "Procedure Orders",
    "Consults", "Enc Progress Notes", "Procedure Notes", "Letters",
    "All Vitals", "Lab Test Result Values", "Patient Cases", "Patient Notes",
    "Patient Alert", "Past Appointments"
]

BILLING_WORKSHEETS = [
    "Billing Ledger", "Billing Claims", "Billing Charges",
    "Patient Advance", "Statements"
]

# Field lists documented in the PDF (pages 13-14)
DOCUMENTED_FIELDS = {
    "Allergy": [
        {"name": "Last name", "type": None, "description": "Patient last name"},
        {"name": "First name", "type": None, "description": "Patient first name"},
        {"name": "Middle name", "type": None, "description": "Patient middle name"},
        {"name": "Chart no", "type": None, "description": "Patient chart number"},
        {"name": "Account no", "type": None, "description": "Patient account number"},
        {"name": "Birth date", "type": None, "description": "Patient birth date"},
        {"name": "Allergy", "type": None, "description": "Allergy name"},
        {"name": "Reaction", "type": None, "description": "Allergic reaction"},
        {"name": "Type", "type": None, "description": "Allergy type"},
        {"name": "Int Name", "type": None, "description": "Internal name"},
        {"name": "Status", "type": None, "description": "Allergy status"},
        {"name": "Rxnorm", "type": None, "description": "RxNorm code"},
    ],
    "Letters": [
        {"name": "Last name", "type": None, "description": "Patient last name"},
        {"name": "First name", "type": None, "description": "Patient first name"},
        {"name": "Middle name", "type": None, "description": "Patient middle name"},
        {"name": "Chart no", "type": None, "description": "Patient chart number"},
        {"name": "Account no", "type": None, "description": "Patient account number"},
        {"name": "Birth date", "type": None, "description": "Patient birth date"},
        {"name": "Letter Date", "type": None, "description": "Date of letter"},
        {"name": "Outward (O) Inward (I)", "type": None, "description": "Direction: outward or inward"},
        {"name": "To Name", "type": None, "description": "Recipient name"},
        {"name": "Subject", "type": None, "description": "Letter subject"},
        {"name": "List of To Names", "type": None, "description": "All recipient names"},
        {"name": "List of Cc Names", "type": None, "description": "All CC recipient names"},
        {"name": "List of To and Cc Names", "type": None, "description": "Combined To and CC names"},
        {"name": "Status Code", "type": None, "description": "Letter status code"},
        {"name": "Status Name", "type": None, "description": "Letter status name"},
        {"name": "FILE", "type": None, "description": "Path to attached document file (e.g., CHART01/LETOut_99.pdf)"},
    ],
    "CCD": [
        {"name": "Last name", "type": None, "description": "Patient last name"},
        {"name": "First name", "type": None, "description": "Patient first name"},
        {"name": "Middle name", "type": None, "description": "Patient middle name"},
        {"name": "Chart no", "type": None, "description": "Patient chart number"},
        {"name": "Account no", "type": None, "description": "Patient account number"},
        {"name": "Birth date", "type": None, "description": "Patient birth date"},
        {"name": "DOC_ID", "type": None, "description": "Document identifier"},
        {"name": "Date", "type": None, "description": "CCD date"},
        {"name": "Provider", "type": None, "description": "Provider name"},
        {"name": "HTML", "type": None, "description": "Path to HTML rendering of CCD"},
        {"name": "XML", "type": None, "description": "Path to XML CCD document"},
    ],
}

# The Insurance Master screenshot on page 10 shows database column names
# visible in the Configure Export Fields UI: IM_ID, IM_NAME, IM_PAYER_ID, etc.
# These are partially visible but not fully enumerable from the PDF.
INSURANCE_MASTER_PARTIAL_FIELDS = [
    {"name": "IM_ID", "type": None, "description": None, "note": "Visible in Configure Export Fields screenshot (page 10); database column name"},
    {"name": "IM_NAME", "type": None, "description": None, "note": "Visible in Configure Export Fields screenshot (page 10); database column name"},
    {"name": "IM_PAYER_ID", "type": None, "description": None, "note": "Visible in Configure Export Fields screenshot (page 10); database column name"},
]

# Categorize worksheets by domain
DOMAIN_MAPPING = {
    "Demographics": ["Patient Demographics", "Guarantor", "Employers"],
    "Insurance / Coverage": ["Insurance Master", "Patient Insurance"],
    "Provider / Reference": ["Medics", "Referring Provider", "Adjusters", "Attorneys"],
    "Clinical - History": ["Family History", "Past Medical Hist", "Surgery", "Social History"],
    "Clinical - Allergies": ["Allergy"],
    "Clinical - Medications": ["Current Medication", "Prescriptions"],
    "Clinical - Immunizations": ["Vaccination", "Health Maintenance"],
    "Clinical - Vitals": ["Vitals", "All Vitals"],
    "Clinical - Labs": ["Lab Results", "Lab Test Result Values"],
    "Clinical - Imaging": ["Rad Results"],
    "Clinical - Procedures": ["Procedure Orders", "Procedure Notes"],
    "Clinical - Notes": ["Old Progress Notes", "Enc Progress Notes", "Patient Notes", "Patient Alert"],
    "Clinical - Diagnoses": ["Diagnosis Codes"],
    "Clinical - Codes": ["CPT Codes", "HCPC Codes"],
    "Clinical - Care Coordination": ["Consults", "Letters", "Messages"],
    "Clinical - Documents": ["Legal Documents", "Other Documents", "Enc Attach Docs", "CCD"],
    "Scheduling": ["Future Appointments", "Past Appointments"],
    "Patient Management": ["Patient Cases"],
    "Billing": ["Billing Ledger", "Billing Claims", "Billing Charges", "Patient Advance", "Statements"],
}


def build_entity(name: str, category: str, is_billing: bool) -> dict:
    """Build an entity dict for a worksheet."""
    fields = DOCUMENTED_FIELDS.get(name, [])
    
    # Special case: Insurance Master has partial field visibility from screenshot
    if name == "Insurance Master":
        fields = INSURANCE_MASTER_PARTIAL_FIELDS
    
    has_document_attachment = name in [
        "Lab Results", "Rad Results", "Old Progress Notes", 
        "Letters", "Legal Documents", "Other Documents", 
        "Enc Attach Docs", "CCD", "Enc Progress Notes",
        "Procedure Notes"
    ]
    
    return {
        "entity_name": name,
        "category": category,
        "is_billing_conditional": is_billing,
        "field_count": len(fields) if fields else None,
        "fields_documented": len(fields) > 0,
        "has_document_attachments": has_document_attachment,
        "fields": [
            {
                "name": f["name"],
                "type": f.get("type"),
                "description": f.get("description"),
                "note": f.get("note"),
            }
            for f in fields
        ],
        "documentation_source": "PDF page 13-14 field list" if fields and name != "Insurance Master" 
            else "PDF page 10 Configure Export Fields screenshot (partial)" if name == "Insurance Master"
            else "Worksheet name only (PDF page 11); no field-level documentation",
    }


def get_category(worksheet_name: str) -> str:
    """Find domain category for a worksheet."""
    for cat, members in DOMAIN_MAPPING.items():
        if worksheet_name in members:
            return cat
    return "Uncategorized"


def main():
    entities = []
    
    for ws in STANDARD_WORKSHEETS:
        entities.append(build_entity(ws, get_category(ws), is_billing=False))
    
    for ws in BILLING_WORKSHEETS:
        entities.append(build_entity(ws, get_category(ws), is_billing=True))
    
    inventory = {
        "product": "SecureEMR+",
        "vendor": "Inmediata Health Group, LLC",
        "source_artifact": "ehi-export-prognocis-self-attestation.pdf",
        "source_pages": 16,
        "export_format": "ZIP containing .xls, .txt, and .pdf files",
        "total_worksheets": len(entities),
        "standard_worksheets": len(STANDARD_WORKSHEETS),
        "billing_conditional_worksheets": len(BILLING_WORKSHEETS),
        "worksheets_with_documented_fields": sum(1 for e in entities if e["fields_documented"]),
        "worksheets_without_field_documentation": sum(1 for e in entities if not e["fields_documented"]),
        "total_documented_fields": sum(len(e["fields"]) for e in entities),
        "entities": entities,
    }
    
    # Write full inventory
    with open(ANALYSIS_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote full-entity-inventory.json: {len(entities)} entities")
    
    # Compute summary stats
    fields_with_descriptions = sum(
        1 for e in entities for field in e["fields"] 
        if field.get("description")
    )
    total_fields = sum(len(e["fields"]) for e in entities)
    
    # Category breakdown
    category_stats = {}
    for e in entities:
        cat = e["category"]
        if cat not in category_stats:
            category_stats[cat] = {"worksheets": 0, "documented_fields": 0}
        category_stats[cat]["worksheets"] += 1
        category_stats[cat]["documented_fields"] += len(e["fields"])
    
    summary = {
        "total_entities": len(entities),
        "standard_worksheets": len(STANDARD_WORKSHEETS),
        "billing_conditional_worksheets": len(BILLING_WORKSHEETS),
        "entities_with_field_lists": sum(1 for e in entities if e["fields_documented"]),
        "entities_without_field_lists": sum(1 for e in entities if not e["fields_documented"]),
        "total_documented_fields": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "fields_without_descriptions": total_fields - fields_with_descriptions,
        "description_coverage_pct": round(fields_with_descriptions / total_fields * 100, 1) if total_fields > 0 else 0,
        "entities_with_document_attachments": sum(1 for e in entities if e["has_document_attachments"]),
        "category_breakdown": category_stats,
    }
    
    with open(ANALYSIS_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote summary-stats.json")
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total worksheets: {len(entities)}")
    print(f"  Standard: {len(STANDARD_WORKSHEETS)}")
    print(f"  Billing (conditional): {len(BILLING_WORKSHEETS)}")
    print(f"Worksheets with documented fields: {summary['entities_with_field_lists']}")
    print(f"Total documented fields: {total_fields}")
    print(f"  With descriptions: {fields_with_descriptions}")
    print(f"  Without descriptions: {total_fields - fields_with_descriptions}")
    print(f"\nCategory breakdown:")
    for cat, stats in sorted(category_stats.items()):
        print(f"  {cat}: {stats['worksheets']} worksheets, {stats['documented_fields']} documented fields")


if __name__ == "__main__":
    main()
