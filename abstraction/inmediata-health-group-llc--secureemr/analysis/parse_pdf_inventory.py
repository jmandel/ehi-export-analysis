"""
Parse the SecureEMR+ EHI Export PDF to extract all worksheets, field examples,
and produce entity-inventory-full.json and entity-inventory-summary.json.

The PDF provides:
- 43 base worksheets + 5 conditional billing worksheets = 48 total
- Field-level detail for only 3 worksheets (Insurance Master from screenshot, Allergy and Letters from examples)
- CCD export fields from example
"""

import json

# All worksheets listed on page 11 of the PDF
base_worksheets = [
    "Insurance Master",
    "Medics",
    "Referring Provider",
    "Adjusters",
    "Attorneys",
    "Employers",
    "Guarantor",
    "Patient Demographics",
    "Patient Insurance",
    "Vaccination",
    "Health Maintenance",
    "Family History",
    "Past Medical Hist",
    "Surgery",
    "Allergy",
    "Current Medication",
    "Social History",
    "Legal Documents",
    "Other Documents",
    "Enc Attach Docs",
    "Old Progress Notes",
    "Messages",
    "Future Appointments",
    "Vitals",
    "Diagnosis Codes",
    "CPT Codes",
    "HCPC Codes",
    "CCD",
    "Prescriptions",
    "Lab Results",
    "Rad Results",
    "Procedure Orders",
    "Consults",
    "Enc Progress Notes",
    "Procedure Notes",
    "Letters",
    "All Vitals",
    "Lab Test Result Values",
    "Patient Cases",
    "Patient Notes",
    "Patient Alert",
    "Past Appointments",
]

# Billing worksheets (conditional - when billing is turned on)
billing_worksheets = [
    "Billing Ledger",
    "Billing Claims",
    "Billing Charges",
    "Patient Advance",
    "Statements",
]

# Fields visible in the Insurance Master screenshot (page 10)
insurance_master_fields = [
    {"field": "IM_ID", "name": "Id", "title": "Id"},
    {"field": "IM_NAME", "name": "Insurance Co Name", "title": "Insurance Co Name"},
    {"field": "IM_PAYER_ID", "name": "Payer Id. Unique", "title": "Payer Id. Unique"},
    {"field": "IM_ADDRESS_LINE1", "name": "Address Line1", "title": "Address Line1"},
    {"field": "IM_ADDRESS_LINE2", "name": "Address Line2", "title": "Address Line2"},
    {"field": "IM_ADDRESS_CITY", "name": "Address City", "title": "Address City"},
    {"field": "IM_ADDRESS_STATE", "name": "Address State Code", "title": "Address State Code"},
    {"field": "IM_ADDRESS_ZIP", "name": "Address Zip", "title": "Address Zip"},
    {"field": "IM_ADDRESS_EMAIL", "name": "Address Email", "title": "Address Email"},
    {"field": "IM_ADDRESS_WORKTEL1", "name": "Address Tel Off1", "title": "Address Tel Off1"},
    {"field": "IM_ADDRESS_WORKTEL2", "name": "Address Tel Off2", "title": "Address Tel Off2"},
    {"field": "IM_ADDRESS_TEL_FAX", "name": "Address Fax", "title": "Address Fax"},
    {"field": "IM_BOOL_INACTIVE", "name": "Status", "title": "Status"},
]

# Fields from Allergy export example (page 14)
allergy_fields = [
    {"field": "Last name", "name": "Last name"},
    {"field": "First name", "name": "First name"},
    {"field": "Middle name", "name": "Middle name"},
    {"field": "Chart no", "name": "Chart no"},
    {"field": "Account no", "name": "Account no"},
    {"field": "Birth date", "name": "Birth date"},
    {"field": "Allergy", "name": "Allergy"},
    {"field": "Reaction", "name": "Reaction"},
    {"field": "Type", "name": "Type"},
    {"field": "Int Name", "name": "Int Name"},
    {"field": "Status", "name": "Status"},
    {"field": "Rxnorm", "name": "Rxnorm"},
]

# Fields from Letters export example (page 14)
letters_fields = [
    {"field": "Last name", "name": "Last name"},
    {"field": "First name", "name": "First name"},
    {"field": "Middle name", "name": "Middle name"},
    {"field": "Chart no", "name": "Chart no"},
    {"field": "Account no", "name": "Account no"},
    {"field": "Birth date", "name": "Birth date"},
    {"field": "Letter Date", "name": "Letter Date"},
    {"field": "Outward (O) Inward (I)", "name": "Outward (O) Inward (I)"},
    {"field": "To Name", "name": "To Name"},
    {"field": "Subject", "name": "Subject"},
    {"field": "List of To Names", "name": "List of To Names"},
    {"field": "List of Cc Names", "name": "List of Cc Names"},
    {"field": "List of To and Cc Names", "name": "List of To and Cc Names"},
    {"field": "Status Code", "name": "Status Code"},
    {"field": "Status Name", "name": "Status Name"},
    {"field": "FILE", "name": "FILE"},
]

# Fields from CCD export example (page 15)
ccd_fields = [
    {"field": "Last name", "name": "Last name"},
    {"field": "First name", "name": "First name"},
    {"field": "Middle name", "name": "Middle name"},
    {"field": "Chart no", "name": "Chart no"},
    {"field": "Account no", "name": "Account no"},
    {"field": "Birth date", "name": "Birth date"},
    {"field": "DOC_ID", "name": "DOC_ID"},
    {"field": "Date", "name": "Date"},
    {"field": "Provider", "name": "Provider"},
    {"field": "HTML", "name": "HTML"},
    {"field": "XML", "name": "XML"},
]

# Categorize worksheets
def categorize(ws_name):
    clinical = [
        "Patient Demographics", "Patient Insurance", "Vaccination", "Health Maintenance",
        "Family History", "Past Medical Hist", "Surgery", "Allergy", "Current Medication",
        "Social History", "Vitals", "All Vitals", "Diagnosis Codes", "CPT Codes", "HCPC Codes",
        "Prescriptions", "Lab Results", "Lab Test Result Values", "Rad Results",
        "Procedure Orders", "Consults", "Enc Progress Notes", "Procedure Notes",
        "Old Progress Notes", "Patient Cases", "Patient Notes", "Patient Alert", "CCD",
    ]
    documents = ["Legal Documents", "Other Documents", "Enc Attach Docs"]
    correspondence = ["Letters", "Messages"]
    administrative = [
        "Insurance Master", "Medics", "Referring Provider", "Adjusters", "Attorneys",
        "Employers", "Guarantor", "Future Appointments", "Past Appointments",
    ]
    billing = ["Billing Ledger", "Billing Claims", "Billing Charges", "Patient Advance", "Statements"]

    if ws_name in clinical:
        return "Clinical"
    elif ws_name in documents:
        return "Documents"
    elif ws_name in correspondence:
        return "Correspondence"
    elif ws_name in administrative:
        return "Administrative/Reference"
    elif ws_name in billing:
        return "Billing (conditional)"
    return "Unknown"

# Build full inventory
entities = []
all_worksheets = base_worksheets + billing_worksheets

known_fields = {
    "Insurance Master": insurance_master_fields,
    "Allergy": allergy_fields,
    "Letters": letters_fields,
    "CCD": ccd_fields,
}

for ws in all_worksheets:
    fields = known_fields.get(ws, None)
    entity = {
        "entity_name": ws,
        "category": categorize(ws),
        "conditional": ws in billing_worksheets,
        "fields_documented": fields is not None,
        "field_count": len(fields) if fields else None,
        "fields": fields if fields else [],
        "has_descriptions": False,
        "has_types": False,
        "has_value_sets": False,
        "source": "PDF page 11 worksheet list" + (
            "; PDF page 10 screenshot" if ws == "Insurance Master" else
            "; PDF page 14 export example" if ws in ("Allergy", "Letters") else
            "; PDF page 15 export example" if ws == "CCD" else ""
        ),
    }
    if fields:
        # Insurance Master has Field/Name/Title columns; others have just field names
        entity["has_descriptions"] = ws == "Insurance Master"  # Name column serves as description
    entities.append(entity)

# Save full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

# Build summary
total_entities = len(entities)
entities_with_fields = sum(1 for e in entities if e["fields_documented"])
total_documented_fields = sum(e["field_count"] or 0 for e in entities)
conditional_entities = sum(1 for e in entities if e["conditional"])

categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"count": 0, "fields_documented": 0, "total_fields": 0}
    categories[cat]["count"] += 1
    if e["fields_documented"]:
        categories[cat]["fields_documented"] += 1
        categories[cat]["total_fields"] += e["field_count"]

summary = {
    "product": "SecureEMR+",
    "version": "Denali 3.1 / v4.0",
    "source_artifact": "ehi-export-prognocis-self-attestation.pdf (16 pages)",
    "total_entities": total_entities,
    "base_entities": total_entities - conditional_entities,
    "conditional_billing_entities": conditional_entities,
    "entities_with_field_detail": entities_with_fields,
    "entities_without_field_detail": total_entities - entities_with_fields,
    "total_documented_fields": total_documented_fields,
    "fields_with_descriptions": 13,  # Only Insurance Master fields have Name column
    "fields_with_types": 0,
    "fields_with_value_sets": 0,
    "categories": categories,
    "export_format": "ZIP containing XLS, TXT, PDF, HTML/XML (CCD)",
    "single_patient_self_service": True,
    "bulk_export_requires_vendor": True,
    "data_dictionary_completeness": "4 of 48 worksheets have field lists documented (8.3%)",
    "notes": [
        "43 base worksheets always available + 5 billing worksheets conditional on billing being enabled",
        "Only Insurance Master (13 fields from screenshot), Allergy (12 fields), Letters (16 fields), and CCD (11 fields) have field-level detail",
        "No data types, value sets, relationships, or foreign keys documented for any field",
        "Configure Export Fields UI exists in the product but field metadata is not published in documentation",
        "The remaining 44 worksheets have no field-level documentation at all",
    ],
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
