#!/usr/bin/env python3
"""
Parse all AdvancedMD export documentation artifacts and produce:
- entity-inventory-full.json: complete field-level extraction
- entity-inventory-summary.json: aggregated stats
"""

import json
import subprocess
import re
from collections import defaultdict

def extract_pdf_text(path):
    result = subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True)
    return result.stdout

def parse_ehr_export_pdf(text):
    """Parse the EHR Export Data Dictionary PDF (SQL .bak file tables)."""
    tables = []
    
    # Split into table sections
    # Tables: EHR_Allergies, EHR_Immunizations, EHR_Messages, EHR_PatientNoteDiagnosis,
    #         EHR_Problems, EHR_Prescriptions, EHR_LabResults, EHR_ResultItems,
    #         EHR_ResultSets, EHR_ResultValues, EHR_PatientNotes, EHR_WordMerge
    
    table_defs = [
        ("EHR_Allergies", "This table contains data for patient allergies."),
        ("EHR_Immunizations", "This table contains data for patient immunizations."),
        ("EHR_Messages", "This table contains data for patient messages from the EHR."),
        ("EHR_PatientNoteDiagnosis", None),
        ("EHR_Problems", None),
        ("EHR_Prescriptions", "This table contains data for patient prescriptions."),
        ("EHR_LabResults", None),
        ("EHR_ResultItems", None),
        ("EHR_ResultSets", None),
        ("EHR_ResultValues", None),
        ("EHR_PatientNotes", None),
        ("EHR_WordMerge", None),
    ]
    
    lines = text.split('\n')
    
    current_table = None
    current_fields = []
    in_column_section = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Detect table headers
        for tname, _ in table_defs:
            if stripped == tname:
                # Save previous table
                if current_table and current_fields:
                    tables.append({
                        "entity": current_table,
                        "fields": current_fields
                    })
                current_table = tname
                current_fields = []
                in_column_section = False
                break
        
        # Detect column header row
        if stripped.startswith('Column') and 'Description' in stripped:
            in_column_section = True
            continue
        
        # Parse column rows - they have format: ColumnName   Description
        if in_column_section and current_table and stripped:
            # Skip non-data lines / end-of-table markers
            stop_markers = [
                'LEGAL NOTICE', 'The following', 'For lab results',
                'dbo.', 'JOIN', 'ON ', 'AND ',
                'In AdvancedMD', 'In this table',
                'From there', 'By using',
                'This table contains', 'These tables contain',
                'For each unique', 'The template is stored',
                'Notes:', 'matching template', 'http',
                '* Dynamic', 'The blob', 'If you',
                'As you can see', 'The way this', 'Because these',
                'Since you see', 'And in a tree',
                'Scenario', 'blob-data', 'Example:',
                'o Male', 'o Female', 'o --',
                'Normal', 'Abnormal', 'Pe_Genito',
            ]
            if any(stripped.startswith(m) for m in stop_markers):
                in_column_section = False
                continue
            if 'EHR_PatientNoteDiagnosis' in stripped:
                in_column_section = False
                continue
            # Skip lines that look like narrative text (contain spaces and lowercase)
            if len(stripped.split()) > 4 and stripped[0].islower():
                continue
            if stripped.startswith('This is') or stripped.startswith('For items'):
                continue
                
            # Try to split into column name and description
            # The format uses significant whitespace to separate
            parts = re.split(r'\s{2,}', stripped, maxsplit=1)
            if len(parts) == 2:
                col_name = parts[0].strip()
                col_desc = parts[1].strip()
                # Valid column names are CamelCase or snake_case identifiers
                if col_name and not col_name.startswith('*') and not col_name.startswith('(') and re.match(r'^[A-Za-z_][A-Za-z0-9_ ]*$', col_name) and len(col_name.split()) <= 3:
                    current_fields.append({
                        "name": col_name,
                        "description": col_desc,
                        "type": None,
                        "nullable": None
                    })
            elif len(parts) == 1 and parts[0] and not parts[0].startswith('*'):
                # Column with no description
                col_name = parts[0].strip()
                if col_name and re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', col_name) and len(col_name.split()) == 1:
                    current_fields.append({
                        "name": col_name,
                        "description": "",
                        "type": None,
                        "nullable": None
                    })
    
    # Save last table
    if current_table and current_fields:
        tables.append({
            "entity": current_table,
            "fields": current_fields
        })
    
    return tables

def parse_ccda_export_pdf(text):
    """Parse the C-CDA Data Dictionary PDF (single patient export)."""
    fields = []
    lines = text.split('\n')
    
    current_field = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith('LEGAL NOTICE') or stripped.startswith('DATA EXPORT'):
            continue
        
        # Look for field name patterns - they start at the left margin and have info after
        # Format: FieldName   Information on Field   Vocabulary Code   Required Text
        # But first line also has headers
        if stripped.startswith('Field Name'):
            continue
        
        # Main field entries start with a known field name
        known_fields = [
            'Allergies', 'Medications', 'Problem List', 'Encounters', 'Procedure List',
            'Procedure Note', 'Immunization', 'Functional Status', 'Mental (Cognitive) Status',
            'Assessments', 'Goals', 'Health Concerns', 'Plan of Treatment', 'Social History/Sex',
            'Lab Results', 'Lab Narrative', 'Medical Equipment', 'Vital Signs',
            'Pediatric Vital Signs', 'Care Team Information', 'Consultation Notes',
            'History and Physical Notes', 'Discharge Summary', 'Progress Note',
            'Imaging Narrative', 'Pathology Narrative', 'Advanced Directives'
        ]
        
        for fname in known_fields:
            if stripped.startswith(fname) and (len(stripped) == len(fname) or stripped[len(fname)] == ' '):
                current_field = fname
                # Extract description from the rest of the line
                rest = stripped[len(fname):].strip()
                # Get vocabulary code if present
                vocab = None
                for code in ['RxNorm', 'SNOMED', 'ICD10', 'CPT', 'LOINC']:
                    if code in stripped:
                        vocab = code
                
                fields.append({
                    "name": fname,
                    "vocabulary_code": vocab,
                    "source": "C-CDA single patient export"
                })
                break
    
    return [{
        "entity": "C-CDA_SinglePatientExport",
        "category": "Single Patient C-CDA Export",
        "fields": fields
    }]

def parse_single_patient_csv_exports(html_text):
    """Parse the CSV export field lists from the HTML page."""
    entities = []
    
    # Patient Transaction Report
    ptr_header = [
        "Patient", "Chart Number", "Address", "Birthdate", "Responsible Party",
        "Phone", "Email", "Provider", "SSN", "Sex",
        "Insurance (Primary, Secondary, Tertiary)"
    ]
    ptr_body = [
        "Transaction Type", "Visit Number", "Facility Name", "Provider",
        "Charge Code", "Transaction Code", "Transaction Code Description",
        "Modifiers", "Visit Primary", "Visit Secondary", "Transaction Carrier",
        "Primary Diagnosis", "Payment Method", "Check Number", "Date of Service",
        "Date of Entry", "Date of Deposit", "Void", "Units", "Charges",
        "Patient Payments", "Insurance Payments", "Total Payments", "Adjustments"
    ]
    
    entities.append({
        "entity": "PatientTransactionReport_CSV",
        "category": "Single Patient PM Export",
        "description": "CSV export from PM Report Center - Patient Transaction Report",
        "fields": [{"name": f, "section": "header", "description": "", "type": None} for f in ptr_header] +
                  [{"name": f, "section": "body", "description": "", "type": None} for f in ptr_body]
    })
    
    # Patient Visit Summary Report
    pvs_header = ["Patient", "Birthdate", "Chart Number", "Email"]
    pvs_body = [
        "Visit Number", "Date of Service", "Charge Code",
        "Charge Code Description", "Claim Charge Code",
        "Claim Charge Code Description", "CPT Code", "CPT Code Description",
        "Diagnosis Codes", "Modifiers", "Place of Service", "Carrier",
        "Copay", "Current Balance", "Billing Provider", "Group Name",
        "Provider Name", "Facility Name", "Facility Code",
        "Appointment Status", "Appointment Date", "Appointment Time",
        "Appointment Type"
    ]
    
    entities.append({
        "entity": "PatientVisitSummary_CSV",
        "category": "Single Patient PM Export",
        "description": "CSV export from PM Report Center - Patient Visit Summary",
        "fields": [{"name": f, "section": "header", "description": "", "type": None} for f in pvs_header] +
                  [{"name": f, "section": "body", "description": "", "type": None} for f in pvs_body]
    })
    
    # EHR Patient Chart Print Tool
    chart_print_items = [
        "Demographics", "Insurance", "Patient Allergies", "Problems List",
        "Immunization History", "Risk Factors", "Advanced Directives",
        "Misc Info Note", "Audit Trail", "Messages", "Annotations",
        "Healthwatcher Items", "Education Lists",
        "Patient Portal and Staff Messages",
        "Current and Historical Medications", "Orders/Tests",
        "Appointments", "Documents Saved to Chart", "Results",
        "Patient Notes"
    ]
    
    entities.append({
        "entity": "EHRPatientChartPrint_PDF",
        "category": "Single Patient EHR Export",
        "description": "PDF export from EHR Patient Chart Print Tool - includes selectable sections",
        "fields": [{"name": item, "description": "Selectable section for chart print", "type": "section"} for item in chart_print_items]
    })
    
    return entities

def parse_bulk_pm_export():
    """Document the PM Data Export (Microsoft Access .mdb)."""
    return [{
        "entity": "PracticeManagementDataExport_MDB",
        "category": "Bulk PM Export",
        "description": "Microsoft Access database export from PM. Includes demographics, transactions, appointments. Contains charges, payments, write-offs, patient demographics, provider, appointments, and carrier information.",
        "fields": [
            {"name": "Demographics data", "description": "Always included", "type": "section"},
            {"name": "Transactions data", "description": "Optional - charges, payments, write-offs", "type": "section"},
            {"name": "Appointment data", "description": "Optional", "type": "section"},
            {"name": "Provider information", "description": "Included with transactions", "type": "section"},
            {"name": "Carrier information", "description": "Insurance carrier data", "type": "section"},
        ]
    }]

def parse_scanned_docs_export():
    """Document the Scanned Documents & Images export."""
    return [{
        "entity": "ScannedDocuments_PM",
        "category": "Bulk Scanned Documents Export",
        "description": "PM scanned documents and images in folder hierarchy with index file (PM.Export.XXXXXX)",
        "fields": [
            {"name": "FileType", "description": "Type of file (doc/file/images)", "type": "folder"},
            {"name": "FileLocation", "description": "Content organized by YYYY/MM/DD", "type": "folder"},
            {"name": "FileName", "description": "Name of the content file", "type": "file"},
        ]
    }, {
        "entity": "ScannedDocuments_EHR",
        "category": "Bulk Scanned Documents Export",
        "description": "EHR scanned documents and images with index file (EHR.docmap.Export.XXXXXX)",
        "fields": [
            {"name": "File_Key_Ptr", "description": "File structure pointer", "type": "index"},
            {"name": "Document_UID", "description": "ID of Document", "type": "index"},
            {"name": "Year/Month/Day folders", "description": "Hierarchical date organization", "type": "folder"},
        ]
    }]


def main():
    # Parse EHR Export PDF
    ehr_text = extract_pdf_text('../downloads/advancedmd-ehrExport-dataDictionary.pdf')
    ehr_tables = parse_ehr_export_pdf(ehr_text)
    
    # Parse C-CDA PDF
    ccda_text = extract_pdf_text('../downloads/advancedmd-dataExport-dataDictionary.pdf')
    ccda_entities = parse_ccda_export_pdf(ccda_text)
    
    # Parse single patient CSV exports from HTML page content
    csv_entities = parse_single_patient_csv_exports(None)
    
    # Parse bulk PM export
    pm_entities = parse_bulk_pm_export()
    
    # Parse scanned docs export
    docs_entities = parse_scanned_docs_export()
    
    # Combine all entities
    all_entities = []
    
    # EHR Bulk Export tables (SQL .bak)
    for table in ehr_tables:
        all_entities.append({
            "entity": table["entity"],
            "category": "EHR Bulk Data Export (SQL .bak)",
            "format": "SQL Server backup",
            "field_count": len(table["fields"]),
            "fields": table["fields"]
        })
    
    # C-CDA single patient export
    for entity in ccda_entities:
        all_entities.append({
            "entity": entity["entity"],
            "category": entity.get("category", "C-CDA Export"),
            "format": "C-CDA XML + HTML",
            "field_count": len(entity["fields"]),
            "fields": entity["fields"]
        })
    
    # CSV exports
    for entity in csv_entities:
        all_entities.append({
            "entity": entity["entity"],
            "category": entity["category"],
            "format": "CSV" if "CSV" in entity["entity"] else "PDF",
            "description": entity.get("description", ""),
            "field_count": len(entity["fields"]),
            "fields": entity["fields"]
        })
    
    # PM bulk export
    for entity in pm_entities:
        all_entities.append({
            "entity": entity["entity"],
            "category": entity["category"],
            "format": "Microsoft Access (.mdb)",
            "description": entity.get("description", ""),
            "field_count": len(entity["fields"]),
            "fields": entity["fields"]
        })
    
    # Scanned docs
    for entity in docs_entities:
        all_entities.append({
            "entity": entity["entity"],
            "category": entity["category"],
            "format": "File system with index",
            "description": entity.get("description", ""),
            "field_count": len(entity["fields"]),
            "fields": entity["fields"]
        })
    
    # Write full inventory
    with open('entity-inventory-full.json', 'w') as f:
        json.dump(all_entities, f, indent=2)
    
    # Generate summary
    summary = {
        "total_entities": len(all_entities),
        "total_fields": sum(e["field_count"] for e in all_entities),
        "fields_with_descriptions": sum(
            1 for e in all_entities
            for f in e["fields"]
            if f.get("description") and f["description"].strip()
        ),
        "by_category": {},
        "by_format": {}
    }
    
    for e in all_entities:
        cat = e["category"]
        if cat not in summary["by_category"]:
            summary["by_category"][cat] = {"entity_count": 0, "field_count": 0}
        summary["by_category"][cat]["entity_count"] += 1
        summary["by_category"][cat]["field_count"] += e["field_count"]
        
        fmt = e.get("format", "unknown")
        if fmt not in summary["by_format"]:
            summary["by_format"][fmt] = {"entity_count": 0, "field_count": 0}
        summary["by_format"][fmt]["entity_count"] += 1
        summary["by_format"][fmt]["field_count"] += e["field_count"]
    
    # Per-entity summary
    summary["entities"] = []
    for e in all_entities:
        desc_count = sum(1 for f in e["fields"] if f.get("description") and f["description"].strip())
        summary["entities"].append({
            "entity": e["entity"],
            "category": e["category"],
            "format": e.get("format", ""),
            "field_count": e["field_count"],
            "fields_with_descriptions": desc_count,
            "description_coverage": f"{desc_count}/{e['field_count']}" if e["field_count"] > 0 else "N/A"
        })
    
    with open('entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary stats
    print(f"Total entities: {summary['total_entities']}")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Fields with descriptions: {summary['fields_with_descriptions']}")
    print()
    print("By Category:")
    for cat, stats in summary["by_category"].items():
        print(f"  {cat}: {stats['entity_count']} entities, {stats['field_count']} fields")
    print()
    print("Per Entity:")
    for e in summary["entities"]:
        print(f"  {e['entity']}: {e['field_count']} fields ({e['description_coverage']} described)")


if __name__ == "__main__":
    main()
