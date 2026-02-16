#!/usr/bin/env python3
"""Parse the SMARTMD b(10) EHI export PDF data dictionary and sample JSON.

Extracts all documented sections, fields, and the sample JSON export,
then produces entity-inventory-full.json and entity-inventory-summary.json.
"""

import json
import re

# --- Data dictionary extracted from PDF (manually verified against pdftotext output) ---
# The PDF documents 5 sections with field-level detail, plus a sample JSON that
# reveals additional undocumented structure (CaseList).

entities = []

# 1. Patient section (14 documented fields)
patient_fields = [
    {"name": "PatientId", "type": "string", "description": "Universally unique identifier for this patient"},
    {"name": "PatientName", "type": "string", "description": "Formatted as lastname, firstname middle initial"},
    {"name": "ChartID", "type": "string", "description": "Human readable unique identifier for the patient chart"},
    {"name": "DOB", "type": "Date", "description": "Patient's date of birth \"m/d/yyyy\""},
    {"name": "Case", "type": "string", "description": "Service line (ex: hospice, palliative)"},
    {"name": "Address1", "type": "string", "description": "Patient's residence"},
    {"name": "City", "type": "string", "description": "Patient's residence"},
    {"name": "State", "type": "string", "description": "Patient's residence"},
    {"name": "Zip", "type": "string", "description": "Either 5 or 9 digit zip code (with \"-\" separator)"},
    {"name": "Country", "type": "string", "description": "Country of patient's residence (typically \"USA\")"},
    {"name": "HomePhone", "type": "string", "description": "Formatted patient's home number (ex: 888-555-1212)"},
    {"name": "WorkPhone", "type": "string", "description": "Formatted patient's work number (ex: 888-555-1212)"},
    {"name": "MobilePhone", "type": "string", "description": "Formatted patient's mobile number (ex: 888-555-1212)"},
    {"name": "Email", "type": "string", "description": "Patient's email address"},
]
entities.append({
    "name": "Patient",
    "category": "Demographics",
    "fields": patient_fields,
    "field_count": len(patient_fields),
    "documented_in": "170.315b10-Electronic-Health-Information-Export.pdf, page 3"
})

# 2. KinList section (10 documented fields)
kin_fields = [
    {"name": "PatientId", "type": "string", "description": "Universally unique identifier for this patient"},
    {"name": "KinId", "type": "string", "description": "Universally unique identifier for this kin"},
    {"name": "FirstName", "type": "string", "description": "Kin's first name"},
    {"name": "LastName", "type": "Date", "description": "Kin's last name"},  # Note: PDF says "Date" type - likely a typo
    {"name": "MobilePhone", "type": "string", "description": "Formatted contact mobile number (ex: 888-555-1212)"},
    {"name": "Email", "type": "string", "description": "Kin's email address"},
    {"name": "DeceasedFlag", "type": "bool", "description": "Flag that indicates alive or dead"},
    {"name": "Decisional", "type": "bool", "description": "Flag that indicates if this kin can make healthcare decisions on behalf of the patient"},
    {"name": "Country", "type": "string", "description": "Not used"},
    {"name": "RelationshipList", "type": "string", "description": "Comma separated list of relationship descriptors between kin and patient. For example, \"caregiver, spouse\"."},
]
entities.append({
    "name": "KinList",
    "category": "Demographics",
    "fields": kin_fields,
    "field_count": len(kin_fields),
    "documented_in": "170.315b10-Electronic-Health-Information-Export.pdf, page 4"
})

# 3. Meds section (14 documented fields)
meds_fields = [
    {"name": "Strength", "type": "string", "description": "Drug strength (without units)"},
    {"name": "StrengthUnit", "type": "string", "description": "Relevant drug strength unit"},
    {"name": "Form", "type": "string", "description": "Packaging of the drug (ex: tablet, capsule, etc)"},
    {"name": "DoseQuantity", "type": "string", "description": "Amount of the drug given per dose"},
    {"name": "StrengthForm", "type": "string", "description": "Concatenation of strength, strength units and form. Typically used for human readability."},
    {"name": "StartDate", "type": "date", "description": "Date patient started taking drug"},
    {"name": "EndDate", "type": "date", "description": "(optional) Date patient was ordered to discontinue taking drug"},
    {"name": "DoseUnit", "type": "string", "description": "Units for dosage"},
    {"name": "Drug", "type": "string", "description": "Name of drug. (ex: \"Lipitor\")"},
    {"name": "DrugId", "type": "Int", "description": "Unique internal serial number for the drug"},
    {"name": "DrugInstructions", "type": "string", "description": "Patient instructions for taking the drug (ex: \"with meal\")"},
    {"name": "WrittenAs", "type": "string", "description": "Human readable description of the medication order"},
    {"name": "Status", "type": "string", "description": "Current status (active or inactive)"},
]
# Note: sample JSON also includes RxNtCode and IsDiscontinued which are NOT in the data dictionary
entities.append({
    "name": "Meds",
    "category": "Medications",
    "fields": meds_fields,
    "field_count": len(meds_fields),
    "documented_in": "170.315b10-Electronic-Health-Information-Export.pdf, page 5",
    "notes": "Sample JSON reveals 2 additional undocumented fields: RxNtCode (RxNorm code), IsDiscontinued (bool)"
})

# 4. Allergies section (4 documented fields)
allergy_fields = [
    {"name": "Allergen", "type": "string", "description": "Drug, food, or environmental factor the patient is allergic to"},
    {"name": "Reaction", "type": "string", "description": "Patient's reaction to allergen"},
    {"name": "WrittenAs", "type": "string", "description": "Human readable description of allergy"},
    {"name": "Status", "type": "string", "description": "Current status (active or inactive)"},
]
entities.append({
    "name": "Allergies",
    "category": "Clinical",
    "fields": allergy_fields,
    "field_count": len(allergy_fields),
    "documented_in": "170.315b10-Electronic-Health-Information-Export.pdf, page 6"
})

# 5. Problems (ClinicalSummaryProblemDetailsList) section (6 documented fields)
problems_fields = [
    {"name": "DictionaryCode", "type": "string", "description": "ICD10 code of the disease"},
    {"name": "Problems", "type": "string", "description": "ICD10 description of the disease"},
    {"name": "ActiveDate", "type": "date", "description": "Date of onset for the disease"},
    {"name": "ResolvedDate", "type": "Date", "description": "Date disease was resolved (optional)"},
    {"name": "ProblemId", "type": "string", "description": "Universally unique identifier for this problem related to this patient"},
    {"name": "isResolved", "type": "bool", "description": "Indicator of whether the disease is resolved (true or false)"},
    {"name": "isPrimaryDx", "type": "bool", "description": "Indicator of whether this disease is the primary reason for treatment (true or false)"},
]
entities.append({
    "name": "Problems (ClinicalSummaryProblemDetailsList)",
    "category": "Clinical",
    "fields": problems_fields,
    "field_count": len(problems_fields),
    "documented_in": "170.315b10-Electronic-Health-Information-Export.pdf, page 6"
})

# 6. CaseList - UNDOCUMENTED but present in sample JSON (pages 7-9)
# Extract fields from the sample JSON structure
caselist_fields = [
    {"name": "Notes", "type": "string", "description": "Undocumented - appears in sample JSON"},
    {"name": "ProviderId", "type": "string", "description": "Undocumented - UUID of provider"},
    {"name": "AddressId", "type": "string", "description": "Undocumented - UUID of address"},
    {"name": "Address1", "type": "string", "description": "Undocumented - patient address"},
    {"name": "City", "type": "string", "description": "Undocumented - city"},
    {"name": "State", "type": "string", "description": "Undocumented - state"},
    {"name": "Zip", "type": "string", "description": "Undocumented - zip code"},
    {"name": "Country", "type": "string", "description": "Undocumented - country"},
    {"name": "HomePhone", "type": "string", "description": "Undocumented - home phone"},
    {"name": "MobilePhone", "type": "string", "description": "Undocumented - mobile phone"},
    {"name": "EMail", "type": "string", "description": "Undocumented - email"},
    {"name": "CaseProvider", "type": "object", "description": "Undocumented - nested object with ResourceId, ProviderId, ProviderName, ProviderNameFML, FirstName, LastName"},
    {"name": "PatientId", "type": "string", "description": "Undocumented - patient UUID"},
    {"name": "PatientLocationId", "type": "string", "description": "Undocumented - location UUID"},
    {"name": "FullName", "type": "string", "description": "Undocumented - patient full name"},
    {"name": "LastName", "type": "string", "description": "Undocumented - patient last name"},
    {"name": "FirstName", "type": "string", "description": "Undocumented - patient first name"},
    {"name": "Middle", "type": "string", "description": "Undocumented - middle name"},
    {"name": "ChartId", "type": "string", "description": "Undocumented - chart ID"},
    {"name": "DOB", "type": "string", "description": "Undocumented - date of birth (ISO format)"},
    {"name": "CreatedOn", "type": "string", "description": "Undocumented - case creation timestamp"},
    {"name": "DOBStr", "type": "string", "description": "Undocumented - DOB as string"},
    {"name": "CaseClosedFlag", "type": "bool", "description": "Undocumented - whether case is closed"},
    {"name": "CaseDescription", "type": "string", "description": "Undocumented - e.g. 'Hospice'"},
    {"name": "Diagnosis1", "type": "string", "description": "Undocumented - primary diagnosis"},
    {"name": "CaseId", "type": "string", "description": "Undocumented - case UUID"},
    {"name": "Score", "type": "number", "description": "Undocumented - numeric score (possibly acuity)"},
    {"name": "InsuranceList", "type": "array", "description": "Undocumented - array (empty in sample)"},
    {"name": "ExternalContactList", "type": "array", "description": "Undocumented - array (empty in sample)"},
    {"name": "InternalContactList", "type": "array", "description": "Undocumented - array (empty in sample)"},
]
entities.append({
    "name": "CaseList",
    "category": "Case/Encounter Management",
    "fields": caselist_fields,
    "field_count": len(caselist_fields),
    "documented_in": "170.315b10-Electronic-Health-Information-Export.pdf, pages 7-9 (sample JSON only)",
    "notes": "NOT documented in data dictionary tables. Only visible in sample JSON export. Contains nested CaseProvider object (6 sub-fields). InsuranceList, ExternalContactList, InternalContactList are empty arrays in sample."
})

# Also the top-level wrapper
wrapper_fields = [
    {"name": "PracticeName", "type": "string", "description": "Name of the practice/agency (from sample JSON)"},
    {"name": "PatientList", "type": "array", "description": "Array of patient records (from sample JSON)"},
]
entities.append({
    "name": "ExportWrapper",
    "category": "Metadata",
    "fields": wrapper_fields,
    "field_count": len(wrapper_fields),
    "documented_in": "170.315b10-Electronic-Health-Information-Export.pdf, page 7 (sample JSON)",
    "notes": "Top-level JSON wrapper containing practice name and patient list"
})

# Compute summary statistics
total_fields = sum(e["field_count"] for e in entities)
documented_entities = [e for e in entities if "Undocumented" not in e.get("notes", "") and e["name"] != "ExportWrapper"]
undocumented_entities = [e for e in entities if "Undocumented" in str(e.get("notes", "")) or "NOT documented" in str(e.get("notes", ""))]

fields_with_descriptions = sum(
    1 for e in entities for f in e["fields"]
    if f["description"] and "Undocumented" not in f["description"]
)
total_field_count = sum(len(e["fields"]) for e in entities)

summary = {
    "product": "SMARTMD Palliative",
    "version": "6",
    "export_format": "JSON",
    "total_entities": len(entities),
    "documented_entities": len(documented_entities),
    "undocumented_entities_in_sample": len(undocumented_entities),
    "total_fields": total_field_count,
    "fields_with_real_descriptions": fields_with_descriptions,
    "fields_undocumented_from_sample": total_field_count - fields_with_descriptions,
    "description_coverage_pct": round(fields_with_descriptions / total_field_count * 100, 1),
    "categories": {},
    "entities_by_category": {}
}

for e in entities:
    cat = e["category"]
    if cat not in summary["categories"]:
        summary["categories"][cat] = {"entity_count": 0, "field_count": 0}
        summary["entities_by_category"][cat] = []
    summary["categories"][cat]["entity_count"] += 1
    summary["categories"][cat]["field_count"] += e["field_count"]
    summary["entities_by_category"][cat].append(e["name"])

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump({"entities": entities, "source": "170.315b10-Electronic-Health-Information-Export.pdf"}, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== SMARTMD Palliative EHI Export Data Dictionary Summary ===")
print(f"Total entities (sections): {len(entities)}")
print(f"  Documented in data dictionary: {len(documented_entities)}")
print(f"  Undocumented (from sample JSON only): {len(undocumented_entities)}")
print(f"Total fields: {total_field_count}")
print(f"  With real descriptions: {fields_with_descriptions}")
print(f"  Undocumented: {total_field_count - fields_with_descriptions}")
print(f"Description coverage: {summary['description_coverage_pct']}%")
print()
print("By category:")
for cat, info in summary["categories"].items():
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
print()
print("Documented sections: Patient (14 fields), KinList (10), Meds (13), Allergies (4), Problems (7)")
print("Undocumented sections from sample: CaseList (30 fields), ExportWrapper (2)")
