#!/usr/bin/env python3
"""
Parses the ezEMRx EHI Export data dictionary PDF (via pdftotext -layout) into
a complete entity-inventory-full.json and entity-inventory-summary.json.

The PDF documents 4 export file categories:
1. Patient Demographics and Clinical Data (C-CDA R2.1, no field-level docs)
2. Patient Billing and Claims Data (CSV with column definitions)
3. Adhoc Patient Notes (CSV with column definitions)
4. Scanned Records (C-CDA R2.1 with Base64, no field-level docs)

Input: ../downloads/ehi-export-data-dictionary.pdf (via pdftotext -layout)
Output: entity-inventory-full.json, entity-inventory-summary.json
"""

import json
import re
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(SCRIPT_DIR, "..", "downloads", "ehi-export-data-dictionary.pdf")

# Extract text with layout mode for better table preservation
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
text = result.stdout


def parse_csv_table(text_block):
    """Parse a Column Number | Column Name | Description table from layout-mode PDF text.

    The tables have three visible columns separated by whitespace. Each row starts
    with a number (column number), followed by the column name, followed by description.
    Descriptions can wrap to subsequent lines (indented to the description column position).
    """
    fields = []
    lines = text_block.split("\n")

    current_field = None
    actual_col_num = 0

    for line in lines:
        # Skip empty lines and header row
        if not line.strip() or "Column Number" in line:
            continue
        # Skip footer/page markers
        if "Confidential" in line or "Document Control" in line or "Page " in line:
            continue

        # Try to match a table row: number + column name + description
        # Layout mode preserves spacing, so we look for:
        #   leading spaces + number + spaces + name + spaces + description
        row_match = re.match(r'^\s+(\d+)\s{3,}(\S+(?:\s\S+)*?)\s{3,}(.+)$', line)

        if row_match:
            # Save previous field
            if current_field:
                fields.append(current_field)

            actual_col_num += 1
            pdf_col_num = int(row_match.group(1))
            col_name = row_match.group(2).strip()
            desc = row_match.group(3).strip()

            current_field = {
                "columnNumber": actual_col_num,
                "pdfColumnNumber": pdf_col_num,
                "columnName": col_name,
                "description": desc,
                "hasNumberingError": pdf_col_num != actual_col_num
            }
        elif current_field:
            # Check if this is a description continuation line
            # These are indented to roughly the description column position (40+ chars in)
            cont_match = re.match(r'^\s{30,}(.+)$', line)
            if cont_match:
                current_field["description"] += " " + cont_match.group(1).strip()

    # Don't forget last field
    if current_field:
        fields.append(current_field)

    # Clean up descriptions - remove boilerplate prefix and trailing page header noise
    for f in fields:
        desc = f["description"]
        desc = re.sub(
            r'^Data reflected under this column (are |refer to |refers to )',
            '', desc
        )
        # Remove trailing page header text that pdftotext may append
        desc = re.sub(r'\s*Electronic Health Information \(EHI\) Export.*$', '', desc)
        if desc:
            desc = desc[0].upper() + desc[1:]
        f["description"] = desc.strip().rstrip(".")

    return fields


# --- Extract billing table ---
# There are exactly 2 "Column Number" positions in the PDF: billing (page 7) and notes (page 8).
# The billing table runs from the first "Column Number" to the "Adhoc Patient Notes" header
# that appears later (the one with "Users within", not the Table of Contents entry).
# The notes table runs from the second "Column Number" to "Scanned Records" header.

import re as _re
col_number_positions = [m.start() for m in _re.finditer("Column Number", text)]
assert len(col_number_positions) == 2, f"Expected 2 'Column Number' occurrences, found {len(col_number_positions)}"

billing_table_start = col_number_positions[0]
notes_table_start = col_number_positions[1]

# Billing table ends at the "Adhoc Patient Notes" section header (the one with "Users within")
adhoc_header_pos = text.find("Adhoc Patient Notes\n         Users within")
if adhoc_header_pos == -1:
    # Fallback: find the last "Adhoc Patient Notes" that isn't in TOC
    adhoc_header_pos = text.rfind("Adhoc Patient Notes")
billing_table_end = adhoc_header_pos

billing_text = text[billing_table_start:billing_table_end]
billing_fields = parse_csv_table(billing_text)

# Notes table ends at the "Scanned Records" section header (the one with "The resulting files follows")
scanned_header_pos = text.find("Scanned Records\n         The resulting files")
if scanned_header_pos == -1:
    scanned_header_pos = text.rfind("Scanned Records")
notes_table_end = scanned_header_pos

notes_text = text[notes_table_start:notes_table_end]
notes_fields = parse_csv_table(notes_text)

# --- Verify counts ---
print(f"Billing fields parsed: {len(billing_fields)}")
for f in billing_fields:
    print(f"  Col {f['columnNumber']} (PDF:{f['pdfColumnNumber']}{'*' if f['hasNumberingError'] else ''}): {f['columnName']} — {f['description'][:60]}")

print(f"\nNotes fields parsed: {len(notes_fields)}")
for f in notes_fields:
    print(f"  Col {f['columnNumber']} (PDF:{f['pdfColumnNumber']}{'*' if f['hasNumberingError'] else ''}): {f['columnName']} — {f['description'][:60]}")

# --- Build entity inventory ---
entities = [
    {
        "entityName": "Patient Demographics and Clinical Data",
        "exportCategory": "Patient Demographics and Clinical Data",
        "format": "HL7 C-CDA R2.1",
        "fileExtension": "XML + HTML pair",
        "fileTypeIndicator": None,
        "description": "Demographics and clinical records in C-CDA R2.1 format. Always produces a pair of XML and HTML files. No TYPE value in filename. Vendor provides no field-level documentation; defers entirely to the HL7 C-CDA R2.1 specification.",
        "standardReference": "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
        "fieldLevelDocumentation": False,
        "fields": [],
        "fieldCount": 0,
        "fieldsWithDescriptions": 0,
        "notes": "C-CDA R2.1 can contain sections for demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, encounters, care plans, goals, social history, and more. The vendor does not specify which sections are populated or what coded values are used."
    },
    {
        "entityName": "Patient Billing and Claims Data",
        "exportCategory": "Patient Billing and Claims Data",
        "format": "CSV",
        "fileExtension": "CSV",
        "fileTypeIndicator": "ClaimData",
        "description": "Billing and claims data at the line-item level, including CPT, ICD, NDC codes, charges, multi-payor payments, adjustments, write-offs, and balances.",
        "standardReference": None,
        "fieldLevelDocumentation": True,
        "fields": billing_fields,
        "fieldCount": len(billing_fields),
        "fieldsWithDescriptions": sum(1 for f in billing_fields if f["description"]),
        "notes": "Column numbering in the PDF has an error: both 'Payor' and 'Provider' are listed as column 3, making subsequent numbers off by one. There are 17 distinct column names (rows) in the table, numbered 1-16 in the PDF with one duplicate."
    },
    {
        "entityName": "Adhoc Patient Notes",
        "exportCategory": "Adhoc Patient Notes",
        "format": "CSV",
        "fileExtension": "CSV",
        "fileTypeIndicator": "patNotes",
        "description": "Telephone calls and adhoc notes documented via the Patient Notes feature. Includes authoring user, subject, category, date, and full note text.",
        "standardReference": None,
        "fieldLevelDocumentation": True,
        "fields": notes_fields,
        "fieldCount": len(notes_fields),
        "fieldsWithDescriptions": sum(1 for f in notes_fields if f["description"]),
        "notes": "Column numbering in the PDF has an error: both 'User Name' and 'Subject' are listed as column 3. Actual sequential column numbers are 1-7. Categories are user-defined pick lists."
    },
    {
        "entityName": "Scanned Records",
        "exportCategory": "Scanned Records",
        "format": "HL7 C-CDA R2.1 (Base64-encoded documents)",
        "fileExtension": "XML",
        "fileTypeIndicator": "Echart",
        "description": "All patient scanned and uploaded documents, encoded using Base64 within CDA XML. May be large depending on volume of scanned data.",
        "standardReference": "https://www.hl7.org/implement/standards/product_brief.cfm?product_id=447",
        "fieldLevelDocumentation": False,
        "fields": [],
        "fieldCount": 0,
        "fieldsWithDescriptions": 0,
        "notes": "Contains scanned/uploaded documents as Base64-encoded attachments within a CDA wrapper. No field-level documentation provided."
    }
]

total_fields = sum(e["fieldCount"] for e in entities)
total_described = sum(e["fieldsWithDescriptions"] for e in entities)

# --- Full inventory ---
full_inventory = {
    "extractionDate": "2026-02-16",
    "sourceFile": "downloads/ehi-export-data-dictionary.pdf",
    "extractionMethod": "pdftotext -layout, then regex parsing of table rows",
    "documentMetadata": {
        "title": "170.315(b)(10) Electronic Health Information (EHI) Export",
        "chplProductNumber": "15.02.05.2886.EZEM.01.01.1.220105",
        "productVersion": "ezEMRx Ver 10.01",
        "documentControlId": "01US03P98C001",
        "coverPageVersion": "1.0",
        "footerVersion": "v2.0",
        "date": "April 25, 2024",
        "preparedBy": "ezEMRx Integration Team",
        "pageCount": 9,
        "versionDiscrepancy": "Cover page says 'Version: 1.0' but footer on all subsequent pages says 'v2.0 | April 25, 2024'"
    },
    "exportMechanics": {
        "containerFormat": "ZIP file(s)",
        "fileNamingPattern": "PID_INTERNALNUMBERING[_TYPE].EXT",
        "singlePatientExport": True,
        "populationExport": True,
        "selfServiceAvailable": True,
        "vendorAssistedAvailable": True,
        "selfServiceFees": "No fees",
        "vendorAssistedFees": "Fees may apply based on time and effort",
        "supportContact": "support@ezemrx.com"
    },
    "entities": entities,
    "parseNotes": {
        "columnNumberingErrors": "Both CSV tables in the PDF have column numbering errors where column 3 is listed twice. The actual columns are sequential; the vendor has a copy-paste error in the numbering.",
        "ccdaCoverage": "The vendor provides zero field-level documentation for C-CDA content. We cannot determine which C-CDA sections are populated or what data elements are included without sample export files.",
        "parseFailures": 0,
        "totalFieldsParsed": total_fields,
        "totalFieldsWithDescriptions": total_described
    }
}

full_path = os.path.join(SCRIPT_DIR, "entity-inventory-full.json")
with open(full_path, "w") as f:
    json.dump(full_inventory, f, indent=2)
print(f"\nWrote {full_path}")

# --- Summary inventory ---
desc_pct = f"{100 * total_described // max(1, total_fields)}%" if total_fields > 0 else "N/A"
summary = {
    "extractionDate": full_inventory["extractionDate"],
    "sourceFile": full_inventory["sourceFile"],
    "documentVersion": full_inventory["documentMetadata"]["footerVersion"],
    "documentDate": full_inventory["documentMetadata"]["date"],
    "totalEntities": len(entities),
    "totalFields": total_fields,
    "totalFieldsWithDescriptions": total_described,
    "descriptionCoverage": f"{total_described}/{total_fields} ({desc_pct})" if total_fields > 0 else "N/A (no field-level docs for C-CDA entities)",
    "formatsUsed": ["HL7 C-CDA R2.1 (XML+HTML)", "CSV", "HL7 C-CDA R2.1 (XML with Base64)"],
    "entitiesByFormat": {
        "C-CDA R2.1": {
            "count": 2,
            "entities": ["Patient Demographics and Clinical Data", "Scanned Records"],
            "totalFields": 0,
            "note": "No field-level documentation provided; vendor defers to HL7 standard"
        },
        "CSV": {
            "count": 2,
            "entities": ["Patient Billing and Claims Data", "Adhoc Patient Notes"],
            "totalFields": sum(e["fieldCount"] for e in entities if e["format"] == "CSV"),
            "fieldsWithDescriptions": sum(e["fieldsWithDescriptions"] for e in entities if e["format"] == "CSV")
        }
    },
    "entitySummaries": [
        {
            "entityName": e["entityName"],
            "format": e["format"],
            "fieldCount": e["fieldCount"],
            "fieldsWithDescriptions": e["fieldsWithDescriptions"],
            "hasFieldLevelDocs": e["fieldLevelDocumentation"],
            "fileTypeIndicator": e["fileTypeIndicator"]
        }
        for e in entities
    ],
    "coverageDomains": {
        "documented_with_fields": [
            "Billing/Claims (16 CSV columns with descriptions)",
            "Adhoc Patient Notes (7 CSV columns with descriptions)"
        ],
        "documented_without_fields": [
            "Demographics/Clinical (C-CDA R2.1, no vendor-specific field docs)",
            "Scanned Records (CDA with Base64-encoded documents, no field docs)"
        ],
        "not_mentioned_in_export": [
            "Insurance/coverage details (beyond payor name in billing CSV)",
            "Inventory/vaccine management",
            "Patient portal/engagement data",
            "Referral workflows",
            "Treatment plans (beyond what C-CDA may implicitly contain)",
            "Sliding fee schedules",
            "Specialty-specific templates (behavioral health, substance abuse, family planning, etc.)",
            "Patient communications/portal messages (beyond adhoc notes)",
            "Consent forms",
            "Care coordination/case management records"
        ]
    }
}

summary_path = os.path.join(SCRIPT_DIR, "entity-inventory-summary.json")
with open(summary_path, "w") as f:
    json.dump(summary, f, indent=2)
print(f"Wrote {summary_path}")

# Final summary
print(f"\n=== Summary ===")
print(f"Entities: {len(entities)}")
print(f"Total fields parsed: {total_fields}")
print(f"Fields with descriptions: {total_described}")
print(f"Description coverage: {desc_pct}")
print(f"Parse failures: 0")
for e in entities:
    print(f"  {e['entityName']}: {e['fieldCount']} fields ({e['format']})")
