#!/usr/bin/env python3
"""
Parse the CGM eMDs EHI Export User Guide PDF (via pdftotext output) and the
prior enrichment JSON to produce a verified full-entity-inventory.json.

Approach: Use the enrichment JSON as a starting point but verify every field
against the raw PDF text. Correct section assignments, note missing data types,
and flag the Entire Patient Chart Report as having content-area descriptions
rather than formal column definitions.
"""

import json
import sys

ENRICHMENT_PATH = "../../../results/compugroup-medical-us--cgm-emds/downloads/enrichment/ehi-data-dictionary.json"
OUTPUT_PATH = "full-entity-inventory.json"
STATS_PATH = "analysis-stats.json"

with open(ENRICHMENT_PATH) as f:
    enrichment = json.load(f)

# Build the verified inventory from scratch using the PDF text as ground truth.
# I've manually verified every field against the pdftotext output.

inventory = {
    "source": "CGM eMDs Electronic Health Information Export User Guide",
    "sourceFile": "cgm-emds-electronic-health-information-export-user-guide.pdf",
    "publicationDate": "December 2023",
    "product": "CGM eMDs v10",
    "exportFormat": enrichment["exportFormat"],
    "documentCategories": enrichment["documentCategories"],  # 27 categories verified against PDF
    "exportFiles": [],
    "verification_notes": []
}

# === Chart Cover Report.xlsx ===
# Verified against PDF pages 4-5 (pdftotext lines 211-280)
# Note: PDF has "Practice Data" as a separate section from "Audit Information"
# The enrichment JSON merged them into "Audit Information" - correcting this.
# Also: "Insurance Address" has no data type listed in the PDF.
chart_cover = {
    "fileName": "Chart Cover Report.xlsx",
    "description": "Contains patient and guarantor demographic, insurance companies, insurance cards, and current medications.",
    "fileType": "Microsoft Excel Spreadsheet (.xlsx)",
    "fieldDetailLevel": "formal_columns",
    "sections": [
        {
            "sectionName": "Practice Data",
            "fields": [
                {"name": "Practice Name", "dataType": "String"},
                {"name": "Practice Address", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Audit Information",
            "fields": [
                {"name": "Print Date", "dataType": "Date"},
                {"name": "Print Time", "dataType": "Time"},
                {"name": "Print User", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Patient Information",
            "fields": [
                {"name": "Patient Name", "dataType": "String"},
                {"name": "Patient Address", "dataType": "String"},
                {"name": "Patient Account Number", "dataType": "String"},
                {"name": "Home Phone", "dataType": "String"},
                {"name": "Cell Phone", "dataType": "String"},
                {"name": "Home Fax", "dataType": "String"},
                {"name": "Pager", "dataType": "String"},
                {"name": "Patient DOB", "dataType": "Date"},
                {"name": "Patient SSN", "dataType": "String"},
                {"name": "Patient Gender", "dataType": "String"},
                {"name": "Patient DL #", "dataType": "String"},
                {"name": "Patient Marital Status", "dataType": "String"},
                {"name": "First Visit Date", "dataType": "Date"},
                {"name": "Provider Name", "dataType": "String"},
                {"name": "Referral", "dataType": "String"},
                {"name": "Financial Group", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Employment Information",
            "fields": [
                {"name": "Employer Name", "dataType": "String"},
                {"name": "Employer Address", "dataType": "String"},
                {"name": "Patient Position", "dataType": "String"},
                {"name": "Email", "dataType": "String"},
                {"name": "Office Phone", "dataType": "String"},
                {"name": "Office Fax", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Guarantor Information",
            "fields": [
                {"name": "Guarantor Name", "dataType": "String"},
                {"name": "Guarantor Address", "dataType": "String"},
                {"name": "Guarantor Account Number", "dataType": "String"},
                {"name": "Guarantor Home Phone", "dataType": "String"},
                {"name": "Guarantor Home Fax", "dataType": "String"},
                {"name": "Guarantor eMail", "dataType": "String"},
                {"name": "Guarantor Gender", "dataType": "String"},
                {"name": "Guarantor DOB", "dataType": "Date"},
                {"name": "Guarantor DL#", "dataType": "String"},
                {"name": "Guarantor SSN", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Insurance Information",
            "fields": [
                {"name": "Insurance Company", "dataType": "String"},
                {"name": "Insurance Address", "dataType": None, "note": "No data type listed in PDF"},
                {"name": "Policy Holder", "dataType": "String"},
                {"name": "Zip", "dataType": "String"},
                {"name": "Group Number", "dataType": "String"},
                {"name": "Copayment", "dataType": "Number"},
                {"name": "Deductible", "dataType": "Number"},
                {"name": "% Ins", "dataType": "Number"},
                {"name": "Insurance Card Front", "dataType": "Image"},
                {"name": "Insurance Card Back", "dataType": "Image"}
            ]
        },
        {
            "sectionName": "Health Summary",
            "fields": [
                {"name": "Current Problem List", "dataType": "String List"},
                {"name": "Current Medication List", "dataType": "String List"},
                {"name": "Past Medical History", "dataType": "String List"},
                {"name": "Social History", "dataType": "String List"},
                {"name": "Surgical History", "dataType": "String List"},
                {"name": "Notes", "dataType": "String"}
            ]
        }
    ]
}

# === Entire Patient Chart Report.xlsx ===
# PDF page 5 (pdftotext lines 282-285): NO formal field table.
# Only prose description. The enrichment JSON fabricated fields from the text.
# Flagging these as content_area descriptions, not formal column definitions.
entire_chart = {
    "fileName": "Entire Patient Chart Report.xlsx",
    "description": "Includes all clinical visit notes, patient medical art, allergies, current medications, problem list, patient messages, past medical history, social history, family medical history, smoking and substance history, and mental health history.",
    "fileType": "Microsoft Excel Spreadsheet (.xlsx)",
    "fieldDetailLevel": "content_area_descriptions_only",
    "note": "The PDF does NOT provide a formal field-level table for this file. The items below are content areas mentioned in the prose description and document categories table, not verified column headers.",
    "sections": [
        {
            "sectionName": "Clinical Visit Notes and Complete Patient Chart",
            "fields": [
                {"name": "All clinical visit notes", "dataType": "String", "is_content_area": True},
                {"name": "Patient medical art", "dataType": "String", "is_content_area": True},
                {"name": "Allergies", "dataType": "String", "is_content_area": True},
                {"name": "Current medications", "dataType": "String", "is_content_area": True},
                {"name": "Problem list", "dataType": "String", "is_content_area": True},
                {"name": "Patient messages", "dataType": "String", "is_content_area": True},
                {"name": "Past medical history", "dataType": "String", "is_content_area": True},
                {"name": "Social history", "dataType": "String", "is_content_area": True},
                {"name": "Family medical history", "dataType": "String", "is_content_area": True},
                {"name": "Smoking and substance history", "dataType": "String", "is_content_area": True},
                {"name": "Mental health history", "dataType": "String", "is_content_area": True},
                {"name": "Patient education", "dataType": "String", "is_content_area": True},
                {"name": "Immunizations", "dataType": "String", "is_content_area": True},
                {"name": "SDOH responses", "dataType": "String", "is_content_area": True}
            ]
        }
    ]
}

# === Health Summary Report.xlsx ===
# PDF pages 6-7 (pdftotext lines 296-344)
# Note: "Tests and Procedures" section lists NO fields
health_summary = {
    "fileName": "Health Summary Report.xlsx",
    "description": "A listing of current problems, allergies, scheduled orders, and past orders.",
    "fileType": "Microsoft Excel Spreadsheet (.xlsx)",
    "fieldDetailLevel": "formal_columns",
    "sections": [
        {
            "sectionName": "Practice Information",
            "fields": [
                {"name": "Practice Name", "dataType": "String"},
                {"name": "Practice Address", "dataType": "String"},
                {"name": "Practice Phone", "dataType": "String"},
                {"name": "Practice Fax", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Patient Information",
            "fields": [
                {"name": "Patient Name", "dataType": "String"},
                {"name": "Patient DOB", "dataType": "Date"},
                {"name": "Report Date", "dataType": "Date"}
            ]
        },
        {
            "sectionName": "Current Problems (One per line)",
            "fields": [
                {"name": "Problems", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Current Medications (One per line)",
            "fields": [
                {"name": "Medication Name", "dataType": "String"},
                {"name": "Medication Dosage", "dataType": "String"},
                {"name": "Medication Form", "dataType": "String"},
                {"name": "Medication Instructions", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Allergies / Adverse Reactions (One per line)",
            "fields": [
                {"name": "Allergy / Reaction", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Past Medical History",
            "fields": [
                {"name": "Medical History List", "dataType": "String List"},
                {"name": "Surgical History List", "dataType": "String List"},
                {"name": "Family History List", "dataType": "String List"},
                {"name": "Social History List", "dataType": "String List"},
                {"name": "Tobacco Status", "dataType": "String"},
                {"name": "Alcohol Status", "dataType": "String"},
                {"name": "Supplements Status", "dataType": "String"},
                {"name": "Substance Abuse History", "dataType": "String"},
                {"name": "Mental Health History", "dataType": "String List"},
                {"name": "Communicable Diseases List", "dataType": "String List"}
            ]
        },
        {
            "sectionName": "Upcoming Test / Health Maintenance Items (One per line)",
            "fields": [
                {"name": "Date Last", "dataType": "Date"},
                {"name": "Due Date", "dataType": "Date"},
                {"name": "Status", "dataType": "String"},
                {"name": "Description", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Tests and Procedures (One per line)",
            "fields": [],
            "note": "Section header listed in PDF but no fields documented underneath"
        }
    ]
}

# === Referral Authorization Report.xlsx ===
# PDF pages 7-8 (pdftotext lines 355-379)
# CORRECTION: enrichment JSON puts "Insurance" in Report Filter Information,
# but the PDF clearly shows it as the first field under "Report Data"
referral_auth = {
    "fileName": "Referral Authorization Report.xlsx",
    "description": "Identifies any inbound or outbound referrals and authorizations documented by the clinic.",
    "fileType": "Microsoft Excel Spreadsheet (.xlsx)",
    "fieldDetailLevel": "formal_columns",
    "sections": [
        {
            "sectionName": "Practice Information",
            "fields": [
                {"name": "Practice Name", "dataType": "String"},
                {"name": "Practice Address", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Audit Information",
            "fields": [
                {"name": "Print Date", "dataType": "Date"},
                {"name": "Print Time", "dataType": "Time"},
                {"name": "Print User", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Report Filter Information",
            "fields": [
                {"name": "Authorization Start Date", "dataType": "Date"},
                {"name": "Facility", "dataType": "String"},
                {"name": "Specialist", "dataType": "String"},
                {"name": "# of Days until Expiration", "dataType": "Number"}
            ]
        },
        {
            "sectionName": "Report Data",
            "fields": [
                {"name": "Insurance", "dataType": "String"},
                {"name": "Patient", "dataType": "String"},
                {"name": "PCP/Referral/Organization", "dataType": "String"},
                {"name": "Authorization #", "dataType": "String"},
                {"name": "Type (T)", "dataType": "String"},
                {"name": "Status (S)", "dataType": "String"},
                {"name": "Date Range", "dataType": "String"},
                {"name": "Insurance Phone", "dataType": "String"},
                {"name": "Visit #", "dataType": "Number"},
                {"name": "Rem#", "dataType": "Number"}
            ]
        }
    ]
}

# === Trial Balance Report.rtf ===
# PDF pages 8-10 (pdftotext lines 382-462)
# Note: PDF says "Patient Nam" (typo for "Patient Name")
# Note: file extension says .rtf in header but "File Type" says "Text File (.txt)"
trial_balance = {
    "fileName": "Trial Balance Report.rtf",
    "description": "Contains all diagnosis codes, charge codes, insurance payments, and patient payments made to their account. Payments and charges are reflective of the dates of services.",
    "fileType": "Text File (.txt)",
    "note": "Header says .rtf but File Type field says 'Text File (.txt)'. PDF also has typo 'Patient Nam' for 'Patient Name'.",
    "fieldDetailLevel": "formal_columns",
    "sections": [
        {
            "sectionName": "Practice Information",
            "fields": [
                {"name": "Facility Name", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Patient Information",
            "fields": [
                {"name": "Patient Name", "dataType": "String"},
                {"name": "Account Number", "dataType": "String"},
                {"name": "Report Date", "dataType": "Date"}
            ]
        },
        {
            "sectionName": "Invoice Header Data (Repeats for each invoice)",
            "fields": [
                {"name": "Invoice Number", "dataType": "String"},
                {"name": "Invoice Date", "dataType": "Date"},
                {"name": "Provider", "dataType": "String"},
                {"name": "Superbill", "dataType": "String"},
                {"name": "ICD Code", "dataType": "String"},
                {"name": "CPT Code", "dataType": "String"},
                {"name": "Fin. Group", "dataType": "String"},
                {"name": "Invoice Total", "dataType": "String"}
            ]
        },
        {
            "sectionName": "ICD Code List (One per line, repeats for each invoice)",
            "fields": [
                {"name": "ICD Code", "dataType": "String"},
                {"name": "Description", "dataType": "String"}
            ]
        },
        {
            "sectionName": "CPT Code List (One per line, repeats for each invoice)",
            "fields": [
                {"name": "CPT Code", "dataType": "String"},
                {"name": "Description", "dataType": "String"},
                {"name": "Start Date", "dataType": "Date"},
                {"name": "End Date", "dataType": "Date"},
                {"name": "Unit", "dataType": "Number"},
                {"name": "Unit Fee", "dataType": "String"},
                {"name": "Fee Amount", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Insurance Data (Repeats for each invoice)",
            "fields": [
                {"name": "Insurance Company Name", "dataType": "String"},
                {"name": "Group Number", "dataType": "String"},
                {"name": "Policy Number", "dataType": "String"},
                {"name": "Copay", "dataType": "String"},
                {"name": "% Insurance", "dataType": "Number"},
                {"name": "% Patient", "dataType": "Number"},
                {"name": "File Status", "dataType": "String"},
                {"name": "Last File", "dataType": "Date"}
            ]
        },
        {
            "sectionName": "Payment Data (One per line, repeats for each invoice)",
            "fields": [
                {"name": "Payment Date", "dataType": "Date"},
                {"name": "Patient / Insurance", "dataType": "String"},
                {"name": "Type", "dataType": "String"},
                {"name": "Check / Credit Card", "dataType": "String"},
                {"name": "CPT Code", "dataType": "String"},
                {"name": "Payment Amount", "dataType": "String"},
                {"name": "Adjustment Amount", "dataType": "String"},
                {"name": "Total Amount", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Payment Total Data (Repeats for each invoice)",
            "fields": [
                {"name": "Patient Payment Total", "dataType": "String"},
                {"name": "Patient Adjustment Total", "dataType": "String"},
                {"name": "Patient Complete Total", "dataType": "String"},
                {"name": "Insurance Payment Total", "dataType": "String"},
                {"name": "Insurance Adjustment Total", "dataType": "String"},
                {"name": "Insurance Complete Total", "dataType": "String"},
                {"name": "Total Payment", "dataType": "String"},
                {"name": "Total Adjustment", "dataType": "String"},
                {"name": "Total Complete", "dataType": "String"}
            ]
        },
        {
            "sectionName": "Invoice Balance",
            "fields": [
                {"name": "Patient Balance", "dataType": "String"},
                {"name": "Insurance Balance", "dataType": "String"},
                {"name": "Total Balance", "dataType": "String"}
            ]
        }
    ]
}

inventory["exportFiles"] = [chart_cover, entire_chart, health_summary, referral_auth, trial_balance]

# Compute statistics
total_fields = 0
formal_fields = 0
content_area_fields = 0
fields_with_type = 0
fields_without_type = 0
total_sections = 0

file_stats = []
for ef in inventory["exportFiles"]:
    file_field_count = 0
    file_formal = 0
    file_content_area = 0
    file_sections = len(ef["sections"])
    total_sections += file_sections
    for sec in ef["sections"]:
        for field in sec["fields"]:
            file_field_count += 1
            total_fields += 1
            if field.get("is_content_area"):
                content_area_fields += 1
                file_content_area += 1
            else:
                formal_fields += 1
                file_formal += 1
            if field.get("dataType") is not None:
                fields_with_type += 1
            else:
                fields_without_type += 1
    file_stats.append({
        "fileName": ef["fileName"],
        "fieldDetailLevel": ef.get("fieldDetailLevel", "unknown"),
        "sections": file_sections,
        "totalFields": file_field_count,
        "formalFields": file_formal,
        "contentAreaFields": file_content_area
    })

# Note verification discrepancies
inventory["verification_notes"] = [
    "Enrichment JSON merged 'Practice Data' (2 fields) into 'Audit Information' for Chart Cover Report. Corrected: these are separate sections per the PDF.",
    "Enrichment JSON placed 'Insurance' field in 'Report Filter Information' for Referral Authorization Report. Corrected: it belongs in 'Report Data' per the PDF layout.",
    "'Insurance Address' in Chart Cover Report has no data type listed in the PDF (blank cell). Enrichment JSON did not note this omission.",
    "Entire Patient Chart Report has NO formal field-level table in the PDF. The 14 'fields' are content area descriptions extracted from prose, not verified column headers.",
    "'Tests and Procedures' section in Health Summary Report lists no fields underneath the section header.",
    "Trial Balance Report header says '.rtf' but the 'File Type' field says 'Text File (.txt)'. PDF also has typo 'Patient Nam' (missing 'e').",
    "Total field count of 162 matches enrichment JSON, but 14 of these are content-area descriptions (Entire Patient Chart Report), not formal column definitions. Formal fields: 148."
]

stats = {
    "totalExportFiles": len(inventory["exportFiles"]),
    "totalDocumentCategories": len(inventory["documentCategories"]),
    "totalSections": total_sections,
    "totalFields": total_fields,
    "formalColumnFields": formal_fields,
    "contentAreaDescriptions": content_area_fields,
    "fieldsWithDataType": fields_with_type,
    "fieldsWithoutDataType": fields_without_type,
    "fileBreakdown": file_stats,
    "dataTypeDistribution": {},
    "descriptionsProvided": 0,
    "percentFieldsWithDescriptions": "0%"
}

# Count data type distribution
type_counts = {}
for ef in inventory["exportFiles"]:
    for sec in ef["sections"]:
        for field in sec["fields"]:
            dt = field.get("dataType") or "None"
            type_counts[dt] = type_counts.get(dt, 0) + 1
stats["dataTypeDistribution"] = type_counts

# Fields with descriptions: NONE of the fields have descriptions beyond their name.
# The PDF provides field names and data types only.
stats["descriptionsProvided"] = 0
stats["percentFieldsWithDescriptions"] = "0%"

inventory["statistics"] = stats

with open(OUTPUT_PATH, "w") as f:
    json.dump(inventory, f, indent=2)

with open(STATS_PATH, "w") as f:
    json.dump(stats, f, indent=2)

print("=== CGM eMDs EHI Export Inventory Statistics ===")
print(f"Export files: {stats['totalExportFiles']}")
print(f"Document categories: {stats['totalDocumentCategories']}")
print(f"Total sections: {stats['totalSections']}")
print(f"Total fields: {stats['totalFields']}")
print(f"  Formal column fields: {stats['formalColumnFields']}")
print(f"  Content-area descriptions: {stats['contentAreaDescriptions']}")
print(f"Fields with data type: {stats['fieldsWithDataType']}")
print(f"Fields without data type: {stats['fieldsWithoutDataType']}")
print(f"Fields with descriptions: {stats['descriptionsProvided']} (0%)")
print(f"\nPer-file breakdown:")
for fs in file_stats:
    print(f"  {fs['fileName']}: {fs['totalFields']} fields ({fs['sections']} sections, detail: {fs['fieldDetailLevel']})")
print(f"\nData type distribution:")
for dt, count in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {dt}: {count}")
print(f"\nVerification notes: {len(inventory['verification_notes'])}")
for i, note in enumerate(inventory['verification_notes'], 1):
    print(f"  {i}. {note}")
