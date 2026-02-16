"""
Parse the Universal EHR EHI export documentation from the PDF and HTML artifacts.
Extracts FHIR resource types visible in screenshots, file sizes, and document listings.
"""
import json
import re

# FHIR NDJSON files visible in the 7-Zip screenshot on PDF page 4
# and confirmed with file sizes on PDF page 6
# Extracted by visual inspection of rendered PDF pages

ndjson_files = [
    {"filename": "Provenance_1.ndjson", "size_bytes": 1204004, "fhir_resource": "Provenance"},
    {"filename": "Practitioner_1.ndjson", "size_bytes": 4100, "fhir_resource": "Practitioner"},
    {"filename": "Patient_1.ndjson", "size_bytes": 31379, "fhir_resource": "Patient"},
    {"filename": "Organization_1.ndjson", "size_bytes": 330, "fhir_resource": "Organization"},
    {"filename": "Observation_1.ndjson", "size_bytes": 675261, "fhir_resource": "Observation"},
    {"filename": "MedicationRequest_1.ndjson", "size_bytes": 77098, "fhir_resource": "MedicationRequest"},
    {"filename": "Invoice_1.ndjson", "size_bytes": 232177, "fhir_resource": "Invoice"},
    {"filename": "Encounter_1.ndjson", "size_bytes": 54648, "fhir_resource": "Encounter"},
    {"filename": "DocumentReference_1.ndjson", "size_bytes": 163680, "fhir_resource": "DocumentReference"},
    {"filename": "Condition_1.ndjson", "size_bytes": 16663, "fhir_resource": "Condition"},
    {"filename": "CareTeam_1.ndjson", "size_bytes": 31180, "fhir_resource": "CareTeam"},
    {"filename": "Appointment_1.ndjson", "size_bytes": 58905, "fhir_resource": "Appointment"},
]

# Page 4 also shows "Device_1.r..." which is truncated - likely Device_1.ndjson
# But page 6 file size listing doesn't clearly show it in the visible portion
# The file list on page 4 clearly shows it between DocumentReference and Condition
# Adding it with unknown size
ndjson_files.insert(9, {"filename": "Device_1.ndjson", "size_bytes": None, "fhir_resource": "Device"})

# Also visible on page 6: Readme.txt (35 bytes) and a "304" folder (Patient ID folder)

# Document files visible in the Documents subfolder (page 6, bottom half)
# These are actual patient clinical documents
document_files = [
    {"prefix": "rOFF_", "description": "BREAST_US (breast ultrasound)", "suffix": "Viewed.pdf", "size": 100830, "date": "2021-01-14"},
    {"prefix": "rOFF_", "description": "BILATERAL_SCREENING_MMG (bilateral screening mammogram)", "suffix": "Viewed.pdf", "size": 96939, "date": "2020-03-11"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 61563, "date": "2021-02-08"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 50527, "date": "2018-05-08"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 313043, "date": "2018-02-19"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 251471, "date": "2021-09-11"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 67101, "date": "2017-02-03"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 304944, "date": "2021-01-14"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 83575, "date": "2016-05-23"},
    {"prefix": "rerr_", "description": "Unknown clinical document", "suffix": "Viewed.pdf", "size": 311801, "date": "2023-05-16"},
    {"prefix": "rerr_", "description": "hl7 document", "suffix": "Viewed.pdf", "size": 6125, "date": "2022-04-10"},
    {"prefix": "rerr_", "description": "hl7 document", "suffix": "Viewed.pdf", "size": 7476, "date": "2022-04-16"},
    {"prefix": "rerr_", "description": "hl7 document", "suffix": "Viewed.pdf", "size": 7864, "date": "2023-04-27"},
    {"prefix": "REF-", "description": "nle_bcbs_obgyn_providers (referral/insurance)", "suffix": ".pdf", "size": 55504, "date": "2023-04-14"},
    {"prefix": "REF-", "description": "nle_bcbs_gi_providers (referral/insurance)", "suffix": ".pdf", "size": 72053, "date": "2023-04-14"},
    {"prefix": "RAD-", "description": "cxr_result (chest x-ray result)", "suffix": ".pdf", "size": 95251, "date": "2023-09-13"},
    {"prefix": "RAD-", "description": "MAMMOGRAM_RESULT", "suffix": ".pdf", "size": 80077, "date": "2020-02-29"},
    {"prefix": "PAT-", "description": "OCM_RECORD (office/clinical management)", "suffix": ".pdf", "size": 141964, "date": "2022-04-05"},
    {"prefix": "LAB-", "description": "UA_DIPSTICK (urinalysis dipstick)", "suffix": ".pdf", "size": 14381, "date": "2021-11-16"},
    {"prefix": "LAB-", "description": "UA (urinalysis)", "suffix": ".pdf", "size": 32696, "date": "2021-01-14"},
    {"prefix": "HOS-", "description": "OTHERS_RECORD_FROM_OCM", "suffix": ".pdf", "size": 141964, "date": "2022-04-09"},
]

# FHIR resource analysis: which are US Core and which go beyond
us_core_resources = {
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
    "Immunization", "Location", "Medication", "MedicationRequest",
    "Observation", "Organization", "Patient", "Practitioner",
    "PractitionerRole", "Procedure", "Provenance"
}

resource_analysis = []
for f in ndjson_files:
    r = f["fhir_resource"]
    is_us_core = r in us_core_resources
    resource_analysis.append({
        "resource": r,
        "filename": f["filename"],
        "size_bytes": f["size_bytes"],
        "is_us_core": is_us_core,
        "beyond_uscdi": not is_us_core,
        "notes": ""
    })

# Add notes
for ra in resource_analysis:
    if ra["resource"] == "Invoice":
        ra["notes"] = "Not a US Core resource; indicates some billing data export"
    elif ra["resource"] == "Appointment":
        ra["notes"] = "Not a US Core resource; scheduling data"
    elif ra["resource"] == "Observation":
        ra["notes"] = "US Core; likely includes vitals, labs, social history"
    elif ra["resource"] == "MedicationRequest":
        ra["notes"] = "US Core; prescriptions/medication orders"
    elif ra["resource"] == "DocumentReference":
        ra["notes"] = "US Core; references to clinical documents in Documents subfolder"
    elif ra["resource"] == "Device":
        ra["notes"] = "US Core; medical devices"

# Summary
total_resources = len(ndjson_files)
us_core_count = sum(1 for ra in resource_analysis if ra["is_us_core"])
beyond_us_core_count = sum(1 for ra in resource_analysis if ra["beyond_uscdi"])

# Missing US Core resources (present in g(10) but not in export)
missing_from_export = us_core_resources - {f["fhir_resource"] for f in ndjson_files}

summary = {
    "product": "Universal EHR",
    "export_format": "FHIR R4 NDJSON + patient document files (PDF/images)",
    "total_fhir_resource_types": total_resources,
    "us_core_resources_present": us_core_count,
    "non_us_core_resources_present": beyond_us_core_count,
    "missing_us_core_resources": sorted(list(missing_from_export)),
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_documentation": False,
    "documentation_pages": 6,
    "documentation_type": "Screenshot-based user guide (print-to-PDF)",
    "patient_documents_in_export": len(document_files),
    "document_types_visible": ["Breast ultrasound", "Mammogram", "Lab results (UA)", 
                                "Chest X-ray", "OCM records", "HL7 documents",
                                "Referral/insurance documents", "Clinical documents"],
    "resource_details": resource_analysis,
    "ndjson_files": ndjson_files,
    "document_files_visible": document_files
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(summary, f, indent=2)

# Summary version
summary_compact = {
    "product": summary["product"],
    "export_format": summary["export_format"],
    "total_fhir_resource_types": summary["total_fhir_resource_types"],
    "us_core_resources_present": summary["us_core_resources_present"],
    "non_us_core_resources_present": summary["non_us_core_resources_present"],
    "missing_us_core_resources": summary["missing_us_core_resources"],
    "has_data_dictionary": summary["has_data_dictionary"],
    "has_field_documentation": summary["has_field_documentation"],
    "documentation_pages": summary["documentation_pages"],
    "resource_list": [r["resource"] for r in resource_analysis],
    "non_us_core_resources": [r["resource"] for r in resource_analysis if r["beyond_uscdi"]],
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary_compact, f, indent=2)

print("=== Export Structure Summary ===")
print(f"Total FHIR resource types in export: {total_resources}")
print(f"  US Core resources: {us_core_count}")
print(f"  Non-US Core resources: {beyond_us_core_count}")
print(f"Missing US Core resources: {', '.join(sorted(missing_from_export))}")
print(f"Patient document files visible: {len(document_files)}")
print(f"Data dictionary: No")
print(f"Field-level documentation: No")
print(f"Sample data: No (only redacted screenshots)")
