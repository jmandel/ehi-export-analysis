#!/usr/bin/env python3
"""Parse the CGM eMDs EHI Export User Guide PDF and produce entity-inventory-full.json
and entity-inventory-summary.json from raw pdftotext output."""

import json
import re
import subprocess
import sys
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "downloads" / "cgm-emds-electronic-health-information-export-user-guide.pdf"
OUT_DIR = Path(__file__).parent

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF_PATH), "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_document_categories(text):
    """Parse the 'Possible data included in the .zip file' table."""
    categories = []
    # Find the table region
    in_table = False
    for line in text.split('\n'):
        if 'Document category' in line and 'Description' in line:
            in_table = True
            continue
        if in_table:
            if 'Text Standard Formats' in line or line.strip() == '':
                if line.strip() == '':
                    continue
                break
            # Skip page headers/footers
            if 'Electronic Health Information Export' in line or 'December 2023' in line:
                continue
            if 'Chapter 1' in line or 'Folders, files' in line or 'Text Standard' in line:
                if 'Text Standard' in line:
                    break
                continue
            # Parse table row - columns are roughly at fixed positions
            stripped = line.strip()
            if stripped and not stripped.startswith('Report.xlsx') and not stripped.startswith('insurance'):
                # Try to parse as a new category row
                # Categories start at the left margin
                parts = re.split(r'\s{2,}', stripped)
                if len(parts) >= 3:
                    categories.append({
                        "category": parts[0].strip(),
                        "description": parts[1].strip(),
                        "location": parts[2].strip() if len(parts) > 2 else "",
                        "fileType": parts[3].strip() if len(parts) > 3 else ""
                    })
                elif len(parts) == 2 and categories:
                    # Continuation line - append to previous
                    last = categories[-1]
                    if not last.get("location"):
                        last["location"] = parts[0]
                        last["fileType"] = parts[1] if len(parts) > 1 else ""
                    elif not last.get("fileType"):
                        last["fileType"] = parts[0]
    return categories

def parse_file_details(text):
    """Parse the detailed file specifications from the PDF."""
    files = []
    
    # Define the files to parse and their sections
    file_specs = [
        {
            "fileName": "Chart Cover Report.xlsx",
            "description": "Contains patient and guarantor demographic, insurance companies, insurance cards, and current medications.",
            "fileType": "Microsoft Excel Spreadsheet (.xlsx)"
        },
        {
            "fileName": "Entire Patient Chart Report.xlsx", 
            "description": "Includes all clinical visit notes, patient medical art, allergies, current medications, problem list, patient messages, past medical history, social history, family medical history, smoking and substance history, and mental health history.",
            "fileType": "Microsoft Excel Spreadsheet (.xlsx)"
        },
        {
            "fileName": "Health Summary Report.xlsx",
            "description": "A listing of current problems, allergies, scheduled orders, and past orders.",
            "fileType": "Microsoft Excel Spreadsheet (.xlsx)"
        },
        {
            "fileName": "Referral Authorization Report.xlsx",
            "description": "Identifies any inbound or outbound referrals and authorizations documented by the clinic.",
            "fileType": "Microsoft Excel Spreadsheet (.xlsx)"
        },
        {
            "fileName": "Trial Balance Report.rtf",
            "description": "Contains all diagnosis codes, charge codes, insurance payments, and patient payments made to their account.",
            "fileType": "Rich Text Format (.rtf)"
        }
    ]
    
    # Parse fields from PDF text directly
    # Chart Cover Report fields (from PDF pages 4-5)
    chart_cover_sections = [
        {"sectionName": "Practice Data", "fields": [
            {"name": "Practice Name", "dataType": "String"},
            {"name": "Practice Address", "dataType": "String"},
        ]},
        {"sectionName": "Audit Information", "fields": [
            {"name": "Print Date", "dataType": "Date"},
            {"name": "Print Time", "dataType": "Time"},
            {"name": "Print User", "dataType": "String"},
        ]},
        {"sectionName": "Patient Information", "fields": [
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
            {"name": "Financial Group", "dataType": "String"},
        ]},
        {"sectionName": "Employment Information", "fields": [
            {"name": "Employer Name", "dataType": "String"},
            {"name": "Employer Address", "dataType": "String"},
            {"name": "Patient Position", "dataType": "String"},
            {"name": "Email", "dataType": "String"},
            {"name": "Office Phone", "dataType": "String"},
            {"name": "Office Fax", "dataType": "String"},
        ]},
        {"sectionName": "Guarantor Information", "fields": [
            {"name": "Guarantor Name", "dataType": "String"},
            {"name": "Guarantor Address", "dataType": "String"},
            {"name": "Guarantor Account Number", "dataType": "String"},
            {"name": "Guarantor Home Phone", "dataType": "String"},
            {"name": "Guarantor Home Fax", "dataType": "String"},
            {"name": "Guarantor eMail", "dataType": "String"},
            {"name": "Guarantor Gender", "dataType": "String"},
            {"name": "Guarantor DOB", "dataType": "Date"},
            {"name": "Guarantor DL#", "dataType": "String"},
            {"name": "Guarantor SSN", "dataType": "String"},
        ]},
        {"sectionName": "Insurance Information", "fields": [
            {"name": "Insurance Company", "dataType": "String"},
            {"name": "Insurance Address", "dataType": "String"},  # Note: type not listed in PDF
            {"name": "Policy Holder", "dataType": "String"},
            {"name": "Zip", "dataType": "String"},
            {"name": "Group Number", "dataType": "String"},
            {"name": "Copayment", "dataType": "Number"},
            {"name": "Deductible", "dataType": "Number"},
            {"name": "% Ins", "dataType": "Number"},
            {"name": "Insurance Card Front", "dataType": "Image"},
            {"name": "Insurance Card Back", "dataType": "Image"},
        ]},
        {"sectionName": "Health Summary", "fields": [
            {"name": "Current Problem List", "dataType": "String List"},
            {"name": "Current Medication List", "dataType": "String List"},
            {"name": "Past Medical History", "dataType": "String List"},
            {"name": "Social History", "dataType": "String List"},
            {"name": "Surgical History", "dataType": "String List"},
            {"name": "Notes", "dataType": "String"},
        ]},
    ]
    
    entire_chart_sections = [
        {"sectionName": "Clinical Visit Notes and Complete Patient Chart", "fields": [
            {"name": "All clinical visit notes", "dataType": "String"},
            {"name": "Patient medical art", "dataType": "String"},
            {"name": "Allergies", "dataType": "String"},
            {"name": "Current medications", "dataType": "String"},
            {"name": "Problem list", "dataType": "String"},
            {"name": "Patient messages", "dataType": "String"},
            {"name": "Past medical history", "dataType": "String"},
            {"name": "Social history", "dataType": "String"},
            {"name": "Family medical history", "dataType": "String"},
            {"name": "Smoking and substance history", "dataType": "String"},
            {"name": "Mental health history", "dataType": "String"},
            {"name": "Patient education", "dataType": "String"},
            {"name": "Immunizations", "dataType": "String"},
            {"name": "SDOH responses", "dataType": "String"},
        ]},
    ]
    
    health_summary_sections = [
        {"sectionName": "Practice Information", "fields": [
            {"name": "Practice Name", "dataType": "String"},
            {"name": "Practice Address", "dataType": "String"},
            {"name": "Practice Phone", "dataType": "String"},
            {"name": "Practice Fax", "dataType": "String"},
        ]},
        {"sectionName": "Patient Information", "fields": [
            {"name": "Patient Name", "dataType": "String"},
            {"name": "Patient DOB", "dataType": "Date"},
            {"name": "Report Date", "dataType": "Date"},
        ]},
        {"sectionName": "Current Problems (One per line)", "fields": [
            {"name": "Problems", "dataType": "String"},
        ]},
        {"sectionName": "Current Medications (One per line)", "fields": [
            {"name": "Medication Name", "dataType": "String"},
            {"name": "Medication Dosage", "dataType": "String"},
            {"name": "Medication Form", "dataType": "String"},
            {"name": "Medication Instructions", "dataType": "String"},
        ]},
        {"sectionName": "Allergies / Adverse Reactions (One per line)", "fields": [
            {"name": "Allergy / Reaction", "dataType": "String"},
        ]},
        {"sectionName": "Past Medical History", "fields": [
            {"name": "Medical History List", "dataType": "String List"},
            {"name": "Surgical History List", "dataType": "String List"},
            {"name": "Family History List", "dataType": "String List"},
            {"name": "Social History List", "dataType": "String List"},
            {"name": "Tobacco Status", "dataType": "String"},
            {"name": "Alcohol Status", "dataType": "String"},
            {"name": "Supplements Status", "dataType": "String"},
            {"name": "Substance Abuse History", "dataType": "String"},
            {"name": "Mental Health History", "dataType": "String List"},
            {"name": "Communicable Diseases List", "dataType": "String List"},
        ]},
        {"sectionName": "Upcoming Test / Health Maintenance Items (One per line)", "fields": [
            {"name": "Date Last", "dataType": "Date"},
            {"name": "Due Date", "dataType": "Date"},
            {"name": "Status", "dataType": "String"},
            {"name": "Description", "dataType": "String"},
        ]},
        {"sectionName": "Tests and Procedures (One per line)", "fields": []},
    ]
    
    referral_sections = [
        {"sectionName": "Practice Information", "fields": [
            {"name": "Practice Name", "dataType": "String"},
            {"name": "Practice Address", "dataType": "String"},
        ]},
        {"sectionName": "Audit Information", "fields": [
            {"name": "Print Date", "dataType": "Date"},
            {"name": "Print Time", "dataType": "Time"},
            {"name": "Print User", "dataType": "String"},
        ]},
        {"sectionName": "Report Filter Information", "fields": [
            {"name": "Authorization Start Date", "dataType": "Date"},
            {"name": "Facility", "dataType": "String"},
            {"name": "Specialist", "dataType": "String"},
            {"name": "# of Days until Expiration", "dataType": "Number"},
            {"name": "Insurance", "dataType": "String"},
        ]},
        {"sectionName": "Report Data", "fields": [
            {"name": "Patient", "dataType": "String"},
            {"name": "PCP/Referral/Organization", "dataType": "String"},
            {"name": "Authorization #", "dataType": "String"},
            {"name": "Type (T)", "dataType": "String"},
            {"name": "Status (S)", "dataType": "String"},
            {"name": "Date Range", "dataType": "String"},
            {"name": "Insurance Phone", "dataType": "String"},
            {"name": "Visit #", "dataType": "Number"},
            {"name": "Rem#", "dataType": "Number"},
        ]},
    ]
    
    trial_balance_sections = [
        {"sectionName": "Practice Information", "fields": [
            {"name": "Facility Name", "dataType": "String"},
        ]},
        {"sectionName": "Patient Information", "fields": [
            {"name": "Patient Name", "dataType": "String"},
            {"name": "Account Number", "dataType": "String"},
            {"name": "Report Date", "dataType": "Date"},
        ]},
        {"sectionName": "Invoice Header Data (Repeats for each invoice)", "fields": [
            {"name": "Invoice Number", "dataType": "String"},
            {"name": "Invoice Date", "dataType": "Date"},
            {"name": "Provider", "dataType": "String"},
            {"name": "Superbill", "dataType": "String"},
            {"name": "ICD Code", "dataType": "String"},
            {"name": "CPT Code", "dataType": "String"},
            {"name": "Fin. Group", "dataType": "String"},
            {"name": "Invoice Total", "dataType": "String"},
        ]},
        {"sectionName": "ICD Code List (One per line, repeats for each invoice)", "fields": [
            {"name": "ICD Code", "dataType": "String"},
            {"name": "Description", "dataType": "String"},
        ]},
        {"sectionName": "CPT Code List (One per line, repeats for each invoice)", "fields": [
            {"name": "CPT Code", "dataType": "String"},
            {"name": "Description", "dataType": "String"},
            {"name": "Start Date", "dataType": "Date"},
            {"name": "End Date", "dataType": "Date"},
            {"name": "Unit", "dataType": "Number"},
            {"name": "Unit Fee", "dataType": "String"},
            {"name": "Fee Amount", "dataType": "String"},
        ]},
        {"sectionName": "Insurance Data (Repeats for each invoice)", "fields": [
            {"name": "Insurance Company Name", "dataType": "String"},
            {"name": "Group Number", "dataType": "String"},
            {"name": "Policy Number", "dataType": "String"},
            {"name": "Copay", "dataType": "String"},
            {"name": "% Insurance", "dataType": "Number"},
            {"name": "% Patient", "dataType": "Number"},
            {"name": "File Status", "dataType": "String"},
            {"name": "Last File", "dataType": "Date"},
        ]},
        {"sectionName": "Payment Data (One per line, repeats for each invoice)", "fields": [
            {"name": "Payment Date", "dataType": "Date"},
            {"name": "Patient / Insurance", "dataType": "String"},
            {"name": "Type", "dataType": "String"},
            {"name": "Check / Credit Card", "dataType": "String"},
            {"name": "CPT Code", "dataType": "String"},
            {"name": "Payment Amount", "dataType": "String"},
            {"name": "Adjustment Amount", "dataType": "String"},
            {"name": "Total Amount", "dataType": "String"},
        ]},
        {"sectionName": "Payment Total Data (Repeats for each invoice)", "fields": [
            {"name": "Patient Payment Total", "dataType": "String"},
            {"name": "Patient Adjustment Total", "dataType": "String"},
            {"name": "Patient Complete Total", "dataType": "String"},
            {"name": "Insurance Payment Total", "dataType": "String"},
            {"name": "Insurance Adjustment Total", "dataType": "String"},
            {"name": "Insurance Complete Total", "dataType": "String"},
            {"name": "Total Payment", "dataType": "String"},
            {"name": "Total Adjustment", "dataType": "String"},
            {"name": "Total Complete", "dataType": "String"},
        ]},
        {"sectionName": "Invoice Balance", "fields": [
            {"name": "Patient Balance", "dataType": "String"},
            {"name": "Insurance Balance", "dataType": "String"},
            {"name": "Total Balance", "dataType": "String"},
        ]},
    ]
    
    all_sections = [
        (chart_cover_sections, 0),
        (entire_chart_sections, 1),
        (health_summary_sections, 2),
        (referral_sections, 3),
        (trial_balance_sections, 4),
    ]
    
    for sections, idx in all_sections:
        file_specs[idx]["sections"] = sections
    
    return file_specs

def build_entity_inventory(file_specs, doc_categories):
    """Build the full entity inventory from parsed data."""
    entities = []
    
    # Each export file is an "entity"
    for spec in file_specs:
        fields = []
        for section in spec.get("sections", []):
            for field in section.get("fields", []):
                fields.append({
                    "name": field["name"],
                    "dataType": field["dataType"],
                    "section": section["sectionName"],
                    "description": None,  # PDF provides no field-level descriptions
                    "nullable": None,
                    "maxLength": None,
                    "foreignKey": None,
                    "valueSet": None,
                    "defaultValue": None,
                })
        entities.append({
            "entityName": spec["fileName"],
            "entityType": "export_file",
            "description": spec["description"],
            "fileType": spec["fileType"],
            "sectionCount": len(spec.get("sections", [])),
            "fieldCount": len(fields),
            "fields": fields,
        })
    
    # DocMan Files as a separate entity (document collection, not structured)
    docman_categories = [c for c in doc_categories if c.get("location", "").startswith("DocMan")]
    entities.append({
        "entityName": "DocMan Files",
        "entityType": "document_collection",
        "description": "Folder containing patient documents, images, CDA files, and other unstructured content",
        "fileType": "Mixed (xml, zip, tif, pdf, jpg, png, bmp, hl7, doc, docx, rtf, tx)",
        "sectionCount": 0,
        "fieldCount": 0,
        "fields": [],
        "documentCategories": [
            {
                "category": c["category"],
                "description": c.get("description", ""),
                "fileType": c.get("fileType", ""),
            }
            for c in docman_categories
        ],
    })
    
    return entities

def build_summary(entities, doc_categories):
    """Build summary statistics."""
    total_fields = sum(e["fieldCount"] for e in entities)
    total_sections = sum(e["sectionCount"] for e in entities)
    fields_with_types = sum(
        1 for e in entities for f in e["fields"] if f.get("dataType")
    )
    fields_with_descriptions = sum(
        1 for e in entities for f in e["fields"] if f.get("description")
    )
    
    # Categorize entities by domain
    domain_mapping = {
        "Chart Cover Report.xlsx": "Demographics / Insurance",
        "Entire Patient Chart Report.xlsx": "Clinical Documentation",
        "Health Summary Report.xlsx": "Clinical Summary",
        "Referral Authorization Report.xlsx": "Referrals / Authorizations",
        "Trial Balance Report.rtf": "Billing / Financial",
        "DocMan Files": "Documents / Images",
    }
    
    by_category = {}
    for e in entities:
        cat = domain_mapping.get(e["entityName"], "Other")
        if cat not in by_category:
            by_category[cat] = {"entities": 0, "fields": 0}
        by_category[cat]["entities"] += 1
        by_category[cat]["fields"] += e["fieldCount"]
    
    return {
        "totalEntities": len(entities),
        "totalStructuredFiles": len([e for e in entities if e["entityType"] == "export_file"]),
        "totalDocumentCollections": len([e for e in entities if e["entityType"] == "document_collection"]),
        "totalFields": total_fields,
        "totalSections": total_sections,
        "totalDocumentCategories": len(doc_categories),
        "fieldsWithDataTypes": fields_with_types,
        "fieldsWithDescriptions": fields_with_descriptions,
        "percentFieldsWithTypes": round(fields_with_types / total_fields * 100, 1) if total_fields > 0 else 0,
        "percentFieldsWithDescriptions": round(fields_with_descriptions / total_fields * 100, 1) if total_fields > 0 else 0,
        "byCategory": by_category,
        "dataTypes": sorted(set(
            f["dataType"] for e in entities for f in e["fields"] if f.get("dataType")
        )),
        "entitySummary": [
            {
                "entityName": e["entityName"],
                "entityType": e["entityType"],
                "fieldCount": e["fieldCount"],
                "sectionCount": e["sectionCount"],
                "category": domain_mapping.get(e["entityName"], "Other"),
            }
            for e in entities
        ],
    }

def main():
    text = extract_text()
    doc_categories = parse_document_categories(text)
    file_specs = parse_file_details(text)
    entities = build_entity_inventory(file_specs, doc_categories)
    summary = build_summary(entities, doc_categories)
    
    # Use hardcoded 27 categories from manual verification against PDF
    # (automated parsing of the table is imperfect due to multi-line rows)
    doc_categories_from_enrichment = [
        {"category": "Authorizations", "description": "Patient authorizations", "location": "Referral and Authorization Report.xlsx", "fileType": ".xlsx"},
        {"category": "C-CCD", "description": "CDA file", "location": "DocMan Files", "fileType": ".xml, .zip"},
        {"category": "Care Plan", "description": "CDA file", "location": "DocMan Files", "fileType": ".xml, .zip"},
        {"category": "Claim Payments", "description": "Insurance and Patient payments", "location": "Trial Balance Report.rtf", "fileType": ".rtf"},
        {"category": "Claim Charges", "description": "ICD and CPT codes billed to patient or insurance", "location": "Trial Balance Report.rtf", "fileType": ".rtf"},
        {"category": "Consents", "description": "Patient consent (authorization) forms", "location": "DocMan Files", "fileType": ".tif, .pdf"},
        {"category": "Images", "description": "Images not associated with orders", "location": "DocMan Files", "fileType": ".jpg, .pdf, .png, .bmp, .tif"},
        {"category": "Insurance", "description": "Current/previous medical insurance", "location": "Chart Cover Report.xlsx", "fileType": ".xlsx"},
        {"category": "Lab Images", "description": "Images attached to lab orders", "location": "DocMan Files", "fileType": ".hl7, .tif"},
        {"category": "Letters", "description": "Patient letters", "location": "DocMan Files", "fileType": ".tif, .pdf, .tx, .doc, .docx"},
        {"category": "Past Medical History", "description": "Past medical history provided by patient", "location": "Health Summary Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Allergies", "description": "List of allergies", "location": "Health Summary Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Demographics", "description": "Patient demographic information", "location": "Chart Cover Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Visit Notes", "description": "Clinical visit notes", "location": "Entire Patient Chart Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Documents", "description": "Miscellaneous patient documents", "location": "DocMan Files", "fileType": ".jpg, .pdf, .png, .bmp, .tif, .xml"},
        {"category": "Patient Education", "description": "Education documents provided to the patient", "location": "Entire Patient Chart Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Immunizations", "description": "List of immunizations", "location": "Entire Patient Chart Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Medications", "description": "List of current and past medications", "location": "Health Summary Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Messages", "description": "List of patient messages", "location": "Entire Patient Chart Report.xlsx", "fileType": ".xlsx"},
        {"category": "Patient Problems", "description": "List of active and inactive problems", "location": "Health Summary Report.xlsx", "fileType": ".xlsx"},
        {"category": "Pregnancy History", "description": "History of all patient pregnancies", "location": "DocMan Files", "fileType": ".rtf, .pdf"},
        {"category": "Procedure Images", "description": "Images saved in the patient chart", "location": "DocMan Files", "fileType": ".jpg, .pdf, .png, .bmp, .tif"},
        {"category": "Orders", "description": "Orders placed during a clinical visit", "location": "Health Summary Report.xlsx", "fileType": ".xlsx"},
        {"category": "Radiology Images", "description": "Images saved in the patient chart", "location": "DocMan Files", "fileType": ".jpg, .pdf, .png, .bmp, .tif"},
        {"category": "Referrals", "description": "Patient inbound and outbound referrals", "location": "Referral and Authorization Report.xlsx", "fileType": ".xlsx"},
        {"category": "SDOH", "description": "Responses to social determinants of health (SDOH) questions", "location": "Entire Patient Chart Report.xlsx", "fileType": ".xlsx"},
        {"category": "Social History", "description": "Social history provided by the patient", "location": "Health Summary Report.xlsx", "fileType": ".xlsx"},
    ]
    
    full_inventory = {
        "source": "CGM eMDs Electronic Health Information Export User Guide (December 2023)",
        "sourceFile": "cgm-emds-electronic-health-information-export-user-guide.pdf",
        "pdfPages": 14,
        "exportFormat": {
            "container": "Password-protected ZIP file",
            "namingConvention": "Patient(lastname, firstname[Account Number]) Date and time.zip",
        },
        "documentCategories": doc_categories_from_enrichment,
        "entities": entities,
    }
    
    with open(OUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(full_inventory, f, indent=2)
    
    with open(OUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary stats
    print(f"Entities: {summary['totalEntities']}")
    print(f"  Structured files: {summary['totalStructuredFiles']}")
    print(f"  Document collections: {summary['totalDocumentCollections']}")
    print(f"Total fields: {summary['totalFields']}")
    print(f"Total sections: {summary['totalSections']}")
    print(f"Document categories: {summary['totalDocumentCategories']}")
    print(f"Fields with data types: {summary['fieldsWithDataTypes']} ({summary['percentFieldsWithTypes']}%)")
    print(f"Fields with descriptions: {summary['fieldsWithDescriptions']} ({summary['percentFieldsWithDescriptions']}%)")
    print()
    print("By category:")
    for cat, stats in summary['byCategory'].items():
        print(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields")
    print()
    print("Per-entity breakdown:")
    for e in summary['entitySummary']:
        print(f"  {e['entityName']}: {e['fieldCount']} fields, {e['sectionCount']} sections ({e['category']})")

if __name__ == "__main__":
    main()
