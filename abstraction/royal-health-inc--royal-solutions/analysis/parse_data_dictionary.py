#!/usr/bin/env python3
"""Parse the Royal Solutions B10 EHI Export PDF data dictionary into structured JSON.

Uses a known field list extracted from careful reading of the PDF to avoid
multi-line description fragments being parsed as field names.
"""

import json
import re
import subprocess
from pathlib import Path

PDF_PATH = Path(__file__).parent.parent / "downloads" / "DocumentationB10FormatExport.pdf"
OUTPUT_DIR = Path(__file__).parent

# Authoritative field list per entity, from manual review of PDF
KNOWN_FIELDS = {
    "Patients": [
        "PatientMRN", "PatientPrefix", "PatientFirstName", "PatientMiddleName",
        "PatientLastName", "PatientSSN", "PatientDOB", "PatientHomePhone",
        "PatientCellPhone", "PatientWorkPhone", "PatientAddress1", "PatientAddress2",
        "PatientCity", "PatientState", "PatientZip", "PatientCountry", "PatientEmail",
        "PatientGender", "PatientEthnicity", "MobilePhone", "PatientFRN",
        "PatientHeight", "PatientWeight", "Race", "Language", "MaritalStatus",
        "SmokingStatus", "GuarantorFirstName", "GuarantorLastName", "GuarantorRelation",
        "GuarantorAddress1", "GuarantorAddress2", "GuarantorCity", "GuarantorZip",
        "GuarantorState", "GuarantorDOB", "GuarantorHomePhone", "GuarantorCellPhone",
        "GuarantorWorkPhone", "Employer", "EmploymentStatus", "EmergencyContact",
        "EmergencyContactPhone", "EmergencyContactMobilePhone", "LastMammoDate",
        "LastDexaDate", "PatientsNotes", "LastCompletedMammoDate", "LastCompletedDexaDate"
    ],
    "Appointments": [
        "AccessionNumber", "PatientMRN", "VisitNumber", "AppointmentDateUTC",
        "ExamStatus", "ExamDescriptionDisplay", "ReferringPhysicianFullName",
        "ReferringProvider", "ReferringPhysicianCredentials", "ExamResultsStatus",
        "Location", "RefPhysNotes", "ExamFinalizedDate", "ExamCode", "ModalityType",
        "ExamResource", "EligibilityStatus", "Insurance_Relationship", "Insurance_Plan",
        "Insurance_SubcriberNumber", "Insurance_Name", "Insurance_GroupNumber",
        "Insurance_Authorization", "Insurance_AuthorizationSecondary",
        "Insurance_AuthorizationTertiary", "AuthorizationStatus", "AuthorizationICDCode",
        "AuthorizationDiagnosis", "AuthorizationRequestDate", "Insurance_ReferralNumber",
        "Insurance_ReferralNumberSecondary", "AuthorizationCaseNumber",
        "AuthorizationCaseNumberSecondary", "Insurance_PlanSecondary",
        "Insurance_SubcriberNumberSecondary", "Insurance_GroupNumberSecondary",
        "PatientDue", "IsESigned", "ESignedDate", "ESignLocation", "CPTCode",
        "CPTDescription", "ExamPriority", "RenderingProviderMDID",
        "ReferringPhysicianNotes", "VisitNotes", "VisitStatus", "Notes",
        "ScheduleNotes", "AdmittedDate", "DischargeDate", "AuthCPTCodes",
        "AuthCPTCodesSecondary", "Insurance_PlanTertiary",
        "Insurance_SubcriberNumberTertiary", "Insurance_GroupNumberTertiary",
        "Insurance_RelationshipTertiary", "InsuredFullName", "InsuredFirstName",
        "InsuredMiddleName", "InsuredLastName", "InsuredGender", "InsuredDOB",
        "InsuredSSN", "Insurance_NameSecondary", "InsuredFullNameSecondary",
        "InsuredFirstNameSecondary", "InsuredMiddleNameSecondary",
        "InsuredLastNameSecondary", "InsuredGenderSecondary", "InsuredDOBSecondary",
        "InsuredSSNSecondary", "Insurance_NameTertiary", "InsuredFullNameTertiary",
        "InsuredFirstNameTertiary", "InsuredMiddleNameTertiary",
        "InsuredLastNameTertiary", "InsuredGenderTertiary", "InsuredDOBTertiary",
        "InsuredSSNTertiary", "Insurance_PlanSecondaryPayerType",
        "Insurance_PlanTertiaryPayerType", "Insurance_CarrierNamePrimary",
        "Insurance_CarrierNameSecondary", "Insurance_CarrierNameTertiary",
        "ReferenceNumberPrimary", "ReferenceNumberSecondary", "BiradCode"
    ],
    "Transactions": [
        "PatientMRN", "AccessionNumber", "AccountNum", "AmountRequested",
        "AmountAuthorized", "AmountCaptured", "Message", "Timestamp", "Entity",
        "Comments", "ShortName", "SecondaryShortName", "FacilityName",
        "TransactionDate", "DepartmentName", "DateOfService", "State", "PaymentType"
    ],
    "Orders": [
        "PatientMRN", "ClientName", "OfficeAddress1", "OfficeAddress2", "OfficeCity",
        "OfficeState", "OfficeZip", "Phone", "MobilePhone", "Fax", "ClientEmail",
        "NPI", "Comment", "OrderSource", "FormID", "FormFieldPatientFirstName",
        "FormFieldPatientLastName", "FormSubmissionStatus",
        "FormSubmissionStatusModifiedDate", "OrderedExams", "ModalityType", "Priority",
        "Status", "FormContactEmail", "FormContactPhone", "IsCompleted",
        "OrderedPatientDOB", "OrderedInsurance", "ScheduleSource", "ProviderFullName"
    ],
    "Demographics2": [
        "MRN", "prevFirstName", "PrevLastName", "PrevMIName", "PrevAddress1",
        "PrevAddress2", "PrevCity", "PrevZipcode", "PrevState", "PrevCountry",
        "Races", "GranularRaces", "Ethnicity", "pcp"
    ],
    "Allergies": [
        "MRN", "Code", "Substance", "OnsetStartDate", "Status", "ReactionCode",
        "Reaction", "Severity"
    ],
    "Devices": [
        "MRN", "UDI", "AssignedAuthority", "Identifier", "DeviceCode", "Date",
        "DeviceName", "ManuDate", "ExpirationDate", "LotNumber", "SerialNumber",
        "Status"
    ],
    "Immunizations": [
        "MRN", "Code", "Name", "StartDate", "Lot", "Status", "Manufacturer", "Notes"
    ],
    "Medications": [
        "MRN", "Code", "Medication", "StartDate", "EndDate", "Frequency", "Route", "Dose"
    ],
    "Problems": [
        "MRN", "Code", "Problem", "StartDate", "EndDate", "Status"
    ],
    "Procedures": [
        "MRN", "Code", "ProcedureName", "Date", "Status", "Note", "Author"
    ],
    "Vitals": [
        "MRN", "Date", "Height", "Weight", "BloodPressureDiast", "BloodPressureSyst",
        "HeartRate", "O2Oximetry", "InhaledOxygen", "O2FlowRate", "BodyTemperature",
        "RespiratoryRate", "BMIPercentile", "WeightPercentile", "HeadPercentile"
    ]
}


def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", str(PDF_PATH), "-"],
        capture_output=True, text=True
    )
    return result.stdout


def extract_descriptions(text: str) -> dict[str, dict[str, str]]:
    """Extract field descriptions from the PDF text using known field list."""
    descriptions = {}
    
    for entity_name, fields in KNOWN_FIELDS.items():
        descriptions[entity_name] = {}
        
        # Find the entity section in the text
        pattern = re.escape(entity_name) + r'\.csv'
        match = re.search(pattern, text)
        if not match:
            continue
        
        # Find the next entity to bound our search
        entity_names = list(KNOWN_FIELDS.keys())
        idx = entity_names.index(entity_name)
        if idx + 1 < len(entity_names):
            next_pattern = re.escape(entity_names[idx + 1]) + r'\.csv'
            next_match = re.search(next_pattern, text[match.end():])
            if next_match:
                section = text[match.start():match.end() + next_match.start()]
            else:
                section = text[match.start():]
        else:
            section = text[match.start():]
        
        # For each field, find its description
        for i, field in enumerate(fields):
            # Find the field name in the section
            # The description follows the field name, possibly on the same line or continuation lines
            field_pattern = re.escape(field) + r'\s{2,}(.+?)(?=\n\s{0,2}[A-Z]\w|$)'
            field_match = re.search(field_pattern, section, re.DOTALL)
            
            if field_match:
                raw_desc = field_match.group(1)
                # Clean up: remove excessive whitespace, join continuation lines
                desc = re.sub(r'\s+', ' ', raw_desc).strip()
                # Trim at the start of the next field (if captured)
                for next_field in fields[i+1:i+2]:
                    if next_field in desc:
                        desc = desc[:desc.index(next_field)].strip()
                descriptions[entity_name][field] = desc
            else:
                # Try simpler pattern
                simple_match = re.search(re.escape(field) + r'\s{2,}(.+)', section)
                if simple_match:
                    desc = simple_match.group(1).strip()
                    descriptions[entity_name][field] = desc
                else:
                    descriptions[entity_name][field] = ""
    
    return descriptions


def extract_descriptions_v2(text: str) -> dict[str, dict[str, str]]:
    """Line-by-line approach using known fields to anchor descriptions."""
    lines = text.split('\n')
    descriptions = {}
    
    current_entity = None
    current_field = None
    current_desc_parts = []
    
    entity_start_pattern = re.compile(r'^(\w+)\.csv\s*$')
    
    for line in lines:
        stripped = line.strip()
        
        # Check for entity header
        m = entity_start_pattern.match(stripped)
        if m and m.group(1) in KNOWN_FIELDS:
            # Save previous field
            if current_entity and current_field:
                if current_entity not in descriptions:
                    descriptions[current_entity] = {}
                descriptions[current_entity][current_field] = ' '.join(current_desc_parts).strip()
            current_entity = m.group(1)
            current_field = None
            current_desc_parts = []
            continue
        
        if current_entity is None:
            continue
        
        # Skip header row
        if re.match(r'^\s*Field\s+Description\s*$', stripped):
            continue
        
        # Skip empty lines
        if not stripped:
            continue
        
        # Check if line starts with a known field
        known = KNOWN_FIELDS.get(current_entity, [])
        found_field = None
        for f in known:
            # Field should appear at the start of the line (with optional leading whitespace)
            if re.match(r'^\s{0,4}' + re.escape(f) + r'(\s|$)', line):
                found_field = f
                break
        
        if found_field:
            # Save previous field
            if current_field:
                if current_entity not in descriptions:
                    descriptions[current_entity] = {}
                descriptions[current_entity][current_field] = ' '.join(current_desc_parts).strip()
            
            current_field = found_field
            # Extract description from same line
            rest = line.split(found_field, 1)[1].strip()
            current_desc_parts = [rest] if rest else []
        elif current_field:
            # Continuation line for current field's description
            current_desc_parts.append(stripped)
    
    # Save the very last field
    if current_entity and current_field:
        if current_entity not in descriptions:
            descriptions[current_entity] = {}
        descriptions[current_entity][current_field] = ' '.join(current_desc_parts).strip()
    
    return descriptions


def build_full_inventory(descriptions: dict) -> dict:
    """Build the complete entity-inventory-full.json."""
    inventory = {
        "product": "Royal Solutions v5",
        "source": "DocumentationB10FormatExport.pdf",
        "export_format": "CSV files in ZIP archive",
        "entities": []
    }
    
    for entity_name, fields in KNOWN_FIELDS.items():
        entity_descs = descriptions.get(entity_name, {})
        entry = {
            "entity_name": entity_name,
            "file_name": f"{entity_name}.csv",
            "field_count": len(fields),
            "fields": []
        }
        
        for f in fields:
            desc = entity_descs.get(f, "")
            field_entry = {
                "field_name": f,
                "description": desc if desc else None,
                "type": None,
                "nullable": None,
                "max_length": None,
                "foreign_keys": [],
                "value_sets": None,
                "default_value": None
            }
            
            # Foreign key hints
            if f in ("PatientMRN", "MRN"):
                field_entry["foreign_keys"] = ["Patients.PatientMRN"]
            elif f == "AccessionNumber" and entity_name != "Appointments":
                field_entry["foreign_keys"] = ["Appointments.AccessionNumber"]
            
            # Extract value sets from description
            if desc:
                if "Values:" in desc:
                    vs_match = re.search(r'Values:\s*(.+?)(?:\.\s|$)', desc)
                    if vs_match:
                        field_entry["value_sets"] = [v.strip() for v in vs_match.group(1).split("|")]
                
                if f == "State" and entity_name == "Transactions":
                    field_entry["value_sets"] = ["1=Created", "2=Declined", "3=Approved", "4=Voided", "5=Refunded"]
                
                if f == "OrderSource":
                    field_entry["value_sets"] = ["Hub", "Fax", "RoyalMD", "Print", "Migrated", "Manual"]
            
            entry["fields"].append(field_entry)
        
        inventory["entities"].append(entry)
    
    return inventory


def build_summary(inventory: dict) -> dict:
    """Build summary statistics."""
    total_fields = 0
    fields_with_desc = 0
    fields_with_value_sets = 0
    
    categories = {
        "Patients": "Demographics",
        "Demographics2": "Demographics",
        "Appointments": "Radiology Operations / Scheduling / Insurance",
        "Transactions": "Billing / Payments",
        "Orders": "Orders / Referrals",
        "Allergies": "Clinical",
        "Devices": "Clinical",
        "Immunizations": "Clinical",
        "Medications": "Clinical",
        "Problems": "Clinical",
        "Procedures": "Clinical",
        "Vitals": "Clinical",
    }
    
    category_stats = {}
    entity_summaries = []
    
    for entity in inventory["entities"]:
        fc = entity["field_count"]
        desc_count = sum(1 for f in entity["fields"] if f["description"])
        vs_count = sum(1 for f in entity["fields"] if f["value_sets"])
        total_fields += fc
        fields_with_desc += desc_count
        fields_with_value_sets += vs_count
        
        cat = categories.get(entity["entity_name"], "Other")
        if cat not in category_stats:
            category_stats[cat] = {"entity_count": 0, "field_count": 0, "described_count": 0}
        category_stats[cat]["entity_count"] += 1
        category_stats[cat]["field_count"] += fc
        category_stats[cat]["described_count"] += desc_count
        
        entity_summaries.append({
            "entity_name": entity["entity_name"],
            "file_name": entity["file_name"],
            "field_count": fc,
            "fields_with_description": desc_count,
            "fields_with_value_sets": vs_count,
            "category": cat
        })
    
    return {
        "product": inventory["product"],
        "source": inventory["source"],
        "export_format": inventory["export_format"],
        "total_entities": len(inventory["entities"]),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_descriptions_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "fields_with_types": 0,
        "fields_with_value_sets": fields_with_value_sets,
        "category_breakdown": category_stats,
        "entities": entity_summaries
    }


def main():
    text = extract_text()
    descriptions = extract_descriptions_v2(text)
    inventory = build_full_inventory(descriptions)
    summary = build_summary(inventory)
    
    with open(OUTPUT_DIR / "entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(OUTPUT_DIR / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"Entities: {summary['total_entities']}")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Fields with descriptions: {summary['fields_with_descriptions']} ({summary['fields_with_descriptions_pct']}%)")
    print(f"Fields with value sets: {summary['fields_with_value_sets']}")
    print()
    print("Per-entity breakdown:")
    for e in summary["entities"]:
        print(f"  {e['file_name']:25s} {e['field_count']:3d} fields, {e['fields_with_description']:3d} described")
    print()
    print("Category breakdown:")
    for cat, stats in summary["category_breakdown"].items():
        print(f"  {cat:50s} {stats['entity_count']:2d} entities, {stats['field_count']:3d} fields")
    
    # Show any fields missing descriptions
    print("\nFields without descriptions:")
    for entity in inventory["entities"]:
        for field in entity["fields"]:
            if not field["description"]:
                print(f"  {entity['entity_name']}.{field['field_name']}")


if __name__ == "__main__":
    main()
