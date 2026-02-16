#!/usr/bin/env python3
"""
Parse the CareLogic EHI Export Data Dictionary XLS independently.
Produces:
  - full-entity-inventory.json: complete machine-readable extraction of all tables/columns
  - summary-stats.json: aggregate statistics for analysis.md
"""
import json
import xlrd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
XLS_PATH = SCRIPT_DIR / "../../../results/qualifacts-systems-llc--carelogic/downloads/CareLogic_EHI_Export_Data_Dictionary.xls"
OUTPUT_INVENTORY = SCRIPT_DIR / "full-entity-inventory.json"
OUTPUT_STATS = SCRIPT_DIR / "summary-stats.json"

# Domain categorization - maps table name patterns to domains
DOMAIN_RULES = [
    (r"CLIENT_DEMO|CLIENT_NAME|CLIENT_MISC|CLIENT_PICTURE|CLIENT_ADDRESS|CLIENT_CONTACT|CLIENT_RELATIONSHIP", "Demographics & Contacts"),
    (r"CLIENT_PROGRAM|CLIENT_EPISODE|CLIENT_STAFF|CLIENT_GROUP|CLIENT_REGULATION", "Program Enrollment"),
    (r"CLIENT_PAYER|CLIENT_GUARANTOR|CLIENT_BALANCE|CLIENT_LIABILITY|CLIENT_SLIDING|CLIENT_SERVICE_CHARGE|CLIENT_ASSIST", "Insurance & Coverage"),
    (r"ACTIVITY_DETAIL|CLAIM_|COLLECTION_|CS_BATCH|GL_DETAIL|EDI_835|EDI_270|FFS_|STMT_|CASH_SHEET", "Billing & Claims"),
    (r"PAYMENT_|REFUND", "Payments"),
    (r"DOCUMENT|ADDENDUM|MOD_VITALS", "Service Documents & Assessments"),
    (r"MOD_IMMUNE", "Immunizations"),
    (r"MOD_LAB_RESULT", "Lab Results"),
    (r"MOD_DIAG_IMG", "Imaging / Diagnostic Reports"),
    (r"MOD_TPLAN|MOD_TX_PLAN|MOD_REC_GOAL|MOD_GOALS", "Treatment Plans / Care Plans"),
    (r"MOD_REFERRAL|MOD_TX_REFER", "Orders / Referrals"),
    (r"MOD_SUBSTANCE_ABUSE|MOD_CAGE_AID|MOD_CIWA|MOD_DDAP|MOD_DACODS|MOD_DARTS", "Substance Abuse Assessments"),
    (r"MOD_BPS|MOD_MSE|MOD_LOCUS|MOD_MGAF|MOD_CFARS|MOD_APS|MOD_CANS|MOD_CAFAS|MOD_CRG|MOD_CLINICAL|MOD_ASSESSMENT|MOD_ASSESS|MOD_MEASURE|MOD_MOD_MINI|MOD_RISK|MOD_PERSON_CENTERED|MOD_PRESENTING|MOD_PREG", "Behavioral Health Assessments"),
    (r"MOD_CONSENT|MOD_ROI|MOD_WITHDRAW_ROI|MOD_EXT_CONSENT", "Consent / ROI Documents"),
    (r"MOD_MEDICATION|MOD_MED_RECON|MOD_MED_CONSENT|MOD_MED_DIAG|MOD_ALLERGY|MOD_MANUAL_ALLE|MOD_MANUAL_MED|MOD_MANUAL_DIAG|MOD_MAN_INT", "Medication Modules"),
    (r"MOD_DIAGNOSIS_RECON|MOD_TX_DIAG|MOD_TX_DX", "Diagnosis Modules"),
    (r"MOD_IMPLANTABLE", "Implantable Devices"),
    (r"MOD_CRS|MOD_USTF|MOD_CPMS|MOD_CQM|MOD_EVAL|MOD_LIVING|MOD_VOCATION|MOD_LEGAL|MOD_MEMO|MOD_DAP|MOD_DD_MEMO|MOD_GRPNOTE|MOD_COPY|MOD_DOC_AMEND|MOD_FOLLOW|MOD_APPT|MOD_ATTENDEE|MOD_CLIENT_AWAY|MOD_CLIENT_SIGN|MOD_CALL_LOG|MOD_COMM_OUTREACH|MOD_CONSUMER|MOD_DISPATCH|MOD_DISPOSITION|MOD_EXT_PROCEDURE|MOD_ORBEON|MOD_PCP|MOD_RECOMM|MOD_TRANS|MOD_UR_|MOD_ADMISSION|MOD_ADMIT|MOD_CRISIS|MOD_CF_|MOD_COAL|MOD_NUTRI|MOD_ARREST|MOD_ABUSE_TRAUMA|MOD_CCAR|MOD_SR|MOD_AZ|MOD_WV_", "Other Clinical Modules"),
    (r"ALLERGY_ENTRY|ERX_|CLINICIAN_ALLERGY|CLINICIAN_ORD_MED|MEDICATION|MED_RECON|CLIENT_MED_ALLERGY|CLIENT_ALLERGY|CLIENT_MEDICATION|RXNORM|NO_ALLERGY|NO_CURRENT_MEDS", "Medications & Allergies"),
    (r"ACKNOWLEDGE_MED|MAR_", "Medication Administration (eMAR)"),
    (r"CLINICAL_RECON|CXDECISION", "Clinical Decision Support"),
    (r"CLIENT_EXTERNAL_DIAG|CLIENT_PROGRAM_CODE", "Diagnoses"),
    (r"CCD_|CCDA_|EXT_MSG|SCHEDULED_CCDA", "Clinical Document Exchange"),
    (r"ADT_|HL7_", "HL7 / ADT Events"),
    (r"BED_", "Inpatient / Bed Management"),
    (r"DWI_", "DWI Programs"),
    (r"HAP_|MACSIS_", "State Programs"),
    (r"INTAKE_|APPOINTMENT_TRACK|CLIENT_SRL", "Intake & Referral Tracking"),
    (r"TASK_LIST", "Task Management"),
    (r"ALERT|MOB_ALERT", "Alerts & Notifications"),
    (r"^MESSAGE", "Internal Messaging"),
    (r"CLIENT_PHARMACY|CLIENT_PCP|CLIENT_PROVIDER|CLIENT_REL_REF", "Provider & Pharmacy Relationships"),
    (r"CLIENT_CONSENT", "Consent Records"),
    (r"CLIENT_PREGNANCY", "Pregnancy Records"),
    (r"CLIENT_SCANNED|CLIENT_ATTACHMENT|CLIENT_RECORD_INV|SCANNED_DOCUMENT", "Document Management"),
    (r"^CF_", "Configurable Forms"),
    (r"CQM_|CRG_BATCH", "Quality Measures"),
    (r"^IMPLANTABLE_DEVICE$", "Implantable Devices"),
    (r"INVENTORY_", "Inventory"),
    (r"IL_REG|GA_CSU|ADMIN_SR|STATE_REPORTING", "State Reporting"),
    (r"AUDIT_|DEBUG|API_ACCESS|CLIENT_VIEW", "Audit & Access Logging"),
    (r"AUTO_PROCESS", "Auto-Processing Rules"),
    (r"SVCDOC_|TPG_", "Service Document Config"),
    (r"EDU_", "Education & Employment"),
    (r"ENCOUNTER_", "Encounter Details"),
    (r"^WV_", "Waiver / Authorization"),
    (r"CSO_ORDER", "Orders"),
    (r"MOB_SYNC", "Mobile Sync"),
    (r"MICP_", "MICP Integration"),
    (r"ADMIN_", "Administration"),
    (r"CASE_AUDIT", "Case Audit"),
    (r"CLIENT_DD_|CLIENT_UMDAP", "DD/IDD Services"),
    (r"CLIENT_BLACK_BOX|CLIENT_CACS", "Client Access & Follow-up"),
    (r"CLIENT_MESSAGE", "Client Messages"),
    (r"CLIENT_AUTH_", "Authorizations"),
    (r"ORD_", "Orders (Clinical)"),
    (r"ORDER_", "Orders (Clinical)"),
    (r"PORTAL_", "Patient Portal"),
    (r"PAYROLL_", "Payroll"),
    (r"MY_HEALTH_", "Patient Portal"),
    (r"MU_API_", "Meaningful Use API"),
    (r"PAT_ED_", "Patient Education"),
    (r"STAFF_", "Staff Records"),
    (r"SERVICE_DOC_REJECT", "Service Documents & Assessments"),
    (r"SRBD_|SRP_|SR_", "Service Documents & Assessments"),
    (r"NON_BILLABLE_|OFFERED_INTAKE|CPP_P_MATRIX|ACTIVITY_ERROR|ADM_ACTIVITY|ASSESSMENT_BATCH|CIH_LOG|CLIENT_CSI|CLIENT_EXTERNAL_LINK|CLIENT_MODIFIER|CLIENT_PROG_UNBILL|QCMR_", "Other / Uncategorized"),
]

import re

def categorize(table_name):
    for pattern, domain in DOMAIN_RULES:
        if re.search(pattern, table_name):
            return domain
    return "Other / Uncategorized"


def main():
    wb = xlrd.open_workbook(str(XLS_PATH.resolve()))
    ws = wb.sheet_by_index(0)
    
    tables = []
    current_table = None
    
    for i in range(1, ws.nrows):
        row = [ws.cell_value(i, c) for c in range(ws.ncols)]
        
        col0 = str(row[0]).strip() if row[0] else ""
        col1 = str(row[1]).strip() if row[1] else ""
        col2 = str(row[2]).strip() if row[2] else ""
        col3 = str(row[3]).strip() if row[3] else ""
        col4 = str(row[4]).strip() if row[4] else ""
        
        if col0:
            if current_table:
                tables.append(current_table)
            current_table = {
                "name": col0,
                "description": col1,
                "domain": "",
                "columns": []
            }
        elif col2 and current_table:
            current_table["columns"].append({
                "name": col2,
                "description": col3,
                "data_type": col4 if col4 else None,
            })
    
    if current_table:
        tables.append(current_table)
    
    # Assign domains
    for t in tables:
        t["domain"] = categorize(t["name"])
    
    # Compute stats
    total_tables = len(tables)
    total_columns = sum(len(t["columns"]) for t in tables)
    cols_with_desc = sum(1 for t in tables for c in t["columns"] if c["description"])
    cols_with_type = sum(1 for t in tables for c in t["columns"] if c["data_type"])
    tables_with_desc = sum(1 for t in tables if t["description"])
    tables_no_cols = [t["name"] for t in tables if len(t["columns"]) == 0]
    tables_no_desc = [t["name"] for t in tables if not t["description"]]
    
    # FK analysis: count columns whose description mentions "Link to" 
    fk_columns = sum(1 for t in tables for c in t["columns"] 
                     if "link to" in c["description"].lower())
    
    # Domain breakdown
    domain_breakdown = {}
    for t in tables:
        d = t["domain"]
        if d not in domain_breakdown:
            domain_breakdown[d] = {"table_count": 0, "field_count": 0, "tables": []}
        domain_breakdown[d]["table_count"] += 1
        domain_breakdown[d]["field_count"] += len(t["columns"])
        domain_breakdown[d]["tables"].append(t["name"])
    
    # Sort domain breakdown by table count descending
    domain_breakdown = dict(sorted(domain_breakdown.items(), key=lambda x: -x[1]["table_count"]))
    
    # Write full inventory
    inventory = {
        "source_file": "CareLogic_EHI_Export_Data_Dictionary.xls",
        "total_tables": total_tables,
        "total_columns": total_columns,
        "columns_with_descriptions": cols_with_desc,
        "columns_with_types": cols_with_type,
        "tables_with_descriptions": tables_with_desc,
        "foreign_key_references": fk_columns,
        "tables": tables
    }
    
    with open(OUTPUT_INVENTORY, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote {OUTPUT_INVENTORY}: {total_tables} tables, {total_columns} columns")
    
    # Write summary stats
    stats = {
        "total_tables": total_tables,
        "total_columns": total_columns,
        "columns_with_descriptions": cols_with_desc,
        "columns_without_descriptions": total_columns - cols_with_desc,
        "pct_columns_with_descriptions": round(cols_with_desc / total_columns * 100, 1) if total_columns else 0,
        "columns_with_types": cols_with_type,
        "pct_columns_with_types": round(cols_with_type / total_columns * 100, 1) if total_columns else 0,
        "tables_with_descriptions": tables_with_desc,
        "tables_without_descriptions": total_tables - tables_with_desc,
        "tables_with_no_columns": tables_no_cols,
        "tables_without_descriptions_list": tables_no_desc,
        "foreign_key_references": fk_columns,
        "domain_breakdown": domain_breakdown,
        "top_20_largest_tables": sorted(
            [{"name": t["name"], "columns": len(t["columns"]), "domain": t["domain"]} for t in tables],
            key=lambda x: -x["columns"]
        )[:20],
        "tables_with_most_fks": sorted(
            [{"name": t["name"], 
              "fk_count": sum(1 for c in t["columns"] if "link to" in c["description"].lower()),
              "total_columns": len(t["columns"])} 
             for t in tables if any("link to" in c["description"].lower() for c in t["columns"])],
            key=lambda x: -x["fk_count"]
        )[:10]
    }
    
    with open(OUTPUT_STATS, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Wrote {OUTPUT_STATS}")
    print(f"\nSummary:")
    print(f"  Tables: {total_tables}")
    print(f"  Columns: {total_columns}")
    print(f"  Columns with descriptions: {cols_with_desc} ({stats['pct_columns_with_descriptions']}%)")
    print(f"  Columns with types: {cols_with_type} ({stats['pct_columns_with_types']}%)")
    print(f"  FK references: {fk_columns}")
    print(f"  Domains: {len(domain_breakdown)}")
    print(f"\nDomain breakdown:")
    for domain, info in domain_breakdown.items():
        print(f"  {domain}: {info['table_count']} tables, {info['field_count']} fields")


if __name__ == "__main__":
    main()
