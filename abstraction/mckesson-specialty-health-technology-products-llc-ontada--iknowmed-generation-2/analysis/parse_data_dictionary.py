#!/usr/bin/env python3
"""
Parse the Ontada b10_data_dictionary.xlsx and produce:
1. full-entity-inventory.json — complete machine-readable extraction of every entity and field
2. analysis-stats.json — summary statistics and category breakdowns
"""

import json
import os
from collections import defaultdict
from openpyxl import load_workbook

XLSX_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/mckesson-specialty-health-technology-products-llc-ontada--iknowmed-generation-2/downloads/b10_data_dictionary.xlsx"
OUTPUT_DIR = os.path.dirname(__file__)


def parse_relational_sheet(ws, sheet_name):
    """Parse iKnowMed, VBC, or Patient History sheets (relational table format)."""
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    if not rows:
        return []

    # Find header row
    headers = [str(h).strip() if h else "" for h in rows[0]]
    header_map = {h.upper(): i for i, h in enumerate(headers)}

    # Map expected columns
    col_map = {}
    for key, candidates in {
        "table_name": ["TABLE_NAME", "TABLE NAME"],
        "column_name": ["COLUMN_NAME", "COLUMN NAME"],
        "data_type": ["DATA_TYPE", "DATA TYPE"],
        "data_length": ["DATA_LENGTH", "DATA LENGTH", "CHAR_LENGTH"],
        "data_precision": ["DATA_PRECISION"],
        "data_scale": ["DATA_SCALE"],
        "char_used": ["CHAR_USED"],
        "table_desc": ["TABLE_DESC", "TABLE_DESCRIPTION", "TABLE DESCRIPTION"],
        "column_desc": ["COLUMN_DESC", "COLUMN_DESCRIPTION", "COLUMN DESCRIPTION"],
    }.items():
        for c in candidates:
            if c.upper() in header_map:
                col_map[key] = header_map[c.upper()]
                break

    # Parse rows into tables
    tables = {}
    for row in rows[1:]:
        def get(key):
            if key in col_map and col_map[key] < len(row):
                v = row[col_map[key]]
                if v is not None:
                    return str(v).strip()
            return None

        tname = get("table_name")
        if not tname:
            continue

        if tname not in tables:
            tables[tname] = {
                "entity_name": tname,
                "source_sheet": sheet_name,
                "entity_description": get("table_desc"),
                "fields": []
            }

        col_name = get("column_name")
        if not col_name:
            continue

        field = {
            "field_name": col_name,
            "data_type": get("data_type"),
            "data_length": get("data_length"),
            "description": get("column_desc"),
        }
        # Add optional metadata
        dp = get("data_precision")
        if dp:
            field["data_precision"] = dp
        ds = get("data_scale")
        if ds:
            field["data_scale"] = ds
        cu = get("char_used")
        if cu:
            field["char_used"] = cu

        # Determine if description is substantive vs just class name
        desc = field["description"]
        if desc:
            field["has_description"] = True
            # Check if it's a meaningful description vs just "ClassName field; (optional)"
            # A "thin" description is just a Java reference like "Patient patient; (optional)"
            field["description_is_substantive"] = not bool(
                len(desc) < 60 and
                (desc.count(";") >= 1 or desc.endswith(")")) and
                not any(word in desc.lower() for word in ["the ", "a ", "an ", "this ", "indicates", "represents", "stores", "contains", "used ", "flag", "date ", "time ", "number ", "name ", "code "])
            )
        else:
            field["has_description"] = False
            field["description_is_substantive"] = False

        tables[tname]["fields"].append(field)

    return list(tables.values())


def parse_ontada_health_sheet(ws):
    """Parse the Ontada Health sheet (document/collection format)."""
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    if not rows:
        return []

    headers = [str(h).strip() if h else "" for h in rows[0]]
    header_map = {h.upper(): i for i, h in enumerate(headers)}

    col_indices = {}
    for key, candidates in {
        "collection": ["COLLECTION", "COLLECTION NAME"],
        "field_name": ["FIELD NAME", "FIELD_NAME", "FIELDNAME"],
        "data_type": ["DATA TYPE", "DATA_TYPE", "DATATYPE"],
        "description": ["DESCRIPTION", "DESC"],
        "notes": ["NOTES", "NOTE"],
    }.items():
        for c in candidates:
            if c.upper() in header_map:
                col_indices[key] = header_map[c.upper()]
                break

    collections = {}
    current_collection = None
    for row in rows[1:]:
        def get(key):
            if key in col_indices and col_indices[key] < len(row):
                v = row[col_indices[key]]
                if v is not None:
                    return str(v).strip()
            return None

        coll = get("collection")
        if coll:
            current_collection = coll

        if not current_collection:
            continue

        fname = get("field_name")
        if not fname:
            continue

        if current_collection not in collections:
            collections[current_collection] = {
                "entity_name": current_collection,
                "source_sheet": "Ontada Health",
                "entity_description": f"Ontada Health {current_collection} collection",
                "fields": []
            }

        desc = get("description")
        notes = get("notes")
        field = {
            "field_name": fname,
            "data_type": get("data_type"),
            "data_length": None,
            "description": desc,
            "has_description": bool(desc),
            "description_is_substantive": bool(desc and len(desc) > 5),
        }
        if notes:
            field["notes"] = notes

        collections[current_collection]["fields"].append(field)

    return list(collections.values())


def categorize_entity(entity_name, entity_desc, source_sheet=None):
    """Assign a domain category based on entity name and description."""
    name = entity_name.upper()
    
    # Sheet-level overrides
    if source_sheet == "VBC":
        return "Value-Based Care"
    if source_sheet == "Patient History":
        return "Social Determinants (Patient History)"
    if source_sheet == "Ontada Health":
        return "Patient Portal (Ontada Health)"
    
    categories = {
        "Demographics": ["PATIENT", "PAT_RACE", "PAT_ETHNICITY", "PAT_LANGUAGE",
                         "PAT_GENDER_IDENTITY", "PATIENT_CONTACT", "PATIENT_IDENTIFICATION",
                         "ADDRESS_CONTACT", "EMERGENCY_CONTACT", "PAT_COGNITIVE_STATUS",
                         "PAT_DEPRESSION_STATUS", "EMAIL_CONTACT", "PHONE_CONTACT",
                         "PATIENT_PREFERENCE", "PATIENT_PHYSICIAN", "PATIENT_PROVIDER"],
        "Encounters / Appointments": ["APPOINTMENT", "APPOINTMENT_RESOURCE",
                                       "APPOINTMENT_SCHEDULE", "APPOINTMENT_EMCODE",
                                       "APPOINTMENT_EMCODE_PROBLEM", "NURSING_APPOINTMENT_RESOURCE",
                                       "PAT_DOS_BILLING_SESSION", "PAT_VISIT_TRACKING",
                                       "PAT_ADMIN_DETAIL", "PAT_ADMIN_DETAIL_VIS",
                                       "PAT_ADMIN_TIMESPAN"],
        "Problems / Diagnoses": ["PAT_PROBLEM", "PAT_PROBLEM_INFERENCE", "PROBLEM_DEF",
                                  "BILLING_DIAG_DEF"],
        "Medications / Prescriptions": ["MEDICATION", "PATIENT_MEDICATION", "PRESCRIPTION",
                                         "MEDICATION_PREFERENCE", "DISPENSABLE",
                                         "NEWDRUGRXTEMPLATE", "RXRENEWALREQUEST",
                                         "RX_CHANGE_REQUEST", "RX_FILL_NOTIFICATION",
                                         "RXALERT", "PAT_DRUGDOSE_ALERT", "ERXMESSAGEQUEUEITEM",
                                         "OUTBOUND_ORDER_TX", "DRUG_MONOGRAPH", "DRUGCLASS",
                                         "MEDICATION_PACKAGE_PREFERENCE",
                                         "DISPENSABLE_ALIAS", "DISPENSABLE_CATALOG",
                                         "DISPENSABLE_INVENTORY", "DISPENSABLE_PREFERENCE",
                                         "PAT_PHARMACY", "PAT_PHARMACY_DISPENSE",
                                         "PAT_PHARMACY_PLAN", "PHARMACY_DEF", "SUPPLY"],
        "Allergies": ["PAT_ALLERGY", "PAT_ALLERGY_REACTION", "PAT_ALLERGY_ALERT",
                       "ALLERGEN_DEF", "ALLERGEN_REACTION_DEF", "ALLERGEN_SEVERITY_DEF"],
        "Immunizations": ["PAT_IMMUNIZATION", "PAT_IMMUNIZATION_EVENT",
                           "PAT_IMMUNIZATION_REGISTRY", "CVX_VIS_LINK"],
        "Vitals / Observations": ["DAILY_VITALS", "BASELINE_VITAL", "TREATMENT_VITAL",
                                   "TREATMENT_VITAL_SET", "PAT_PERFORMANCE_STATUS",
                                   "PATIENT_SMOKING_STATUS"],
        "Lab Results": ["PAT_RESULT_HEADER", "PAT_RESULT_VALUE", "PAT_RESULT_ATTACHMENT",
                         "LAB_ANALYTE_DEF", "LAB_PANEL_DEF", "EXTERNAL_RESULT_PANEL_DEF",
                         "EXTERNAL_RESULT_VALUE_DEF"],
        "Orders": ["PAT_ORDER", "PAT_ORDER_DOSE", "PAT_ORDER_ADMINISTRATION",
                    "PAT_ORDER_SESSION", "PAT_ORDER_GROUP", "PAT_ORDER_DISCONTINUATION",
                    "PAT_ORDER_INFERENCE", "PAT_ORDER_MODIFIER", "PAT_ORDER_ADDL_INFO",
                    "PAT_ORDER_HOLD", "ORDER_QUEUE_NOTE", "ORDER_QUEUE_ROLE",
                    "ORDER_QUEUE_STATUS"],
        "Oncology Treatment / Regimens": ["PAT_REGIMEN", "PAT_REGIMEN_CYCLE_DAYS",
                                           "PAT_REGIMEN_INFERENCE", "PAT_REGIMEN_SEQUENCE",
                                           "PAT_REGIMEN_TREATMENT_GROUP", "REGIMEN_DEF",
                                           "PAT_CHEMO_TREATMENT", "DATE_CYCLE_DAY",
                                           "CYCLE_DAY_DELAY", "CYCLE_DAY_MOVE",
                                           "PATIENT_RADIATION_TREATMENT", "PATIENT_SURGERY_TREATMENT",
                                           "PAT_HOSPITAL_TREATMENT", "PAT_OTHER_TREATMENT",
                                           "PAT_PROCEDURE_TREATMENT", "PAT_TRANSFUSN_TREATMENT",
                                           "PAT_TREATMENT", "PAT_TREATMENT_HISTORY",
                                           "PAT_TREATMENT_PROBLEM", "PAT_TREATMENT_ANNOTATION",
                                           "PAT_TREATMENT_BILLABLEITEMS"],
        "Documents / Notes": ["PAT_DOCUMENT", "PAT_DOCUMENT_LOB", "PAT_DOCUMENT_ANNOTATION",
                               "PAT_DOCUMENT_ENTITY_REF", "PAT_DOCUMENT_RECIPIENT",
                               "TRANSCRIPTION", "TRANSCRIPTION_LOB", "CLINICAL_NOTE_ADDENDUM",
                               "CLINICAL_NOTE_DM_STATUS", "PAT_DISCHARGE_NOTE",
                               "FILE_ATTACHMENT", "FILE_ATTACHMENT_LOB", "AUDIO_RECORDING",
                               "OUTBOUND_FAX", "OUTBOUND_FAX_LOB", "OUTBOUND_FAX_SOURCE"],
        "Billing / Charges": ["CHARGE_HEADER", "CHARGE_LINE", "CHARGE_LINE_ICD",
                               "CHARGE_LINE_NDC", "CHARGE_HEADER_SENT", "CHARGE_LINE_SENT",
                               "CHARGE_LINE_SENT_ICD", "CHARGE_LINE_SENT_NDC",
                               "CHARGE_COMMENT", "CHARGE_ERROR", "CHARGE_SOURCE",
                               "BILLABLE_ITEM", "BILLING_CODE_DEF", "BILLING_ORG",
                               "NURSINGCARE_BILLABLE_ITEM"],
        "Financial Auth / Insurance": ["PAT_FIN_AUTH", "PAT_FIN_AUTH_BILLINGCODE",
                                        "PAT_FIN_AUTH_ICD", "PAT_FIN_AUTH_ORDER",
                                        "PAT_FIN_AUTH_TEMPLATE_ORDER", "INSURANCE",
                                        "PATIENT_INSURANCE"],
        "Care Coordination": ["PAT_CARE_PLAN", "PATIENT_TRANSFER", "PATIENT_TRANSFER_PROBLEM",
                               "CCD_RECONCILIATION", "CCD_MANUAL_RECONCILIATION",
                               "CQ_DOC_SEARCH_QUERY", "CQ_DOC_SEARCH_RESULT",
                               "CQ_DOC_RETRIEVE_RESULT"],
        "Nursing Care": ["NURSINGCARE_IVACCESS", "NURSINGCARE_IVDEACCESS",
                          "NURSINGCARE_PATIENTASSESS", "NURSINGCARE_PATIENTNOTE",
                          "NURSINGCARE_INCIDENTTODET", "NURSINGCARE_BILLABLE_ITEM",
                          "PATIENT_VASCULAR_ACCESS"],
        "Adverse Events": ["PATIENT_ADVERSEEVENT"],
        "Clinical Trials": ["CLINICAL_TRIAL_DEF", "CLINICAL_TRIAL_DEF_PREF"],
        "Surveys / Screenings": ["PAT_SURVEY", "PAT_SURVEY_ITEM", "PAT_SURVEY_LINE_ITEM",
                                  "PAT_SURVEY_TEMPLATE", "PAT_SCREENING", "PAT_SCREENING_EVENT",
                                  "PAT_COVID19_SCREENING", "PAT_SURV_TEMPL_LOB",
                                  "PAT_SERVICE", "PAT_SERVICE_DAY", "PAT_SERVICE_EVENT"],
        "Oncology Care Model": ["PAT_OCM_EPISODE", "PAT_OCM_HEADER", "PAT_OCM_MONTHLY",
                                "PAT_OCM_HEADER_LOB"],
        "Patient Engagement / Portal": ["PAT_EDUCATION_EVENT", "PAT_ED_SESSION",
                                         "PATIENT_MESSAGE", "MAIL_MESSAGE",
                                         "MAIL_MSG_ABOUT_PATIENT", "MAIL_MSG_ATTACHMENT",
                                         "MAIL_MSG_BODY", "MAIL_MSG_RECIPIENT",
                                         "MAIL_MSG_REC_PAT_DATA", "MESSAGE",
                                         "MESSAGE_PAYLOAD", "MESSAGE_RECIPIENT"],
        "Family / Social History": ["PAT_RELATIVE", "PAT_RELATIVE_PROBLEM", "OBGYN_HISTORY"],
        "Social Determinants (Patient History)": ["G2_DISTRESS_THERMOMETER",
                                                    "G2_SOCIALHX_INT_TRAVEL_HX",
                                                    "G2_SOCIALHX_LIFESTYLE",
                                                    "G2_SOCIALHX_LIVING_ENV",
                                                    "G2_SOCIALHX_SUBSTANCE_USE",
                                                    "G2_SOCIALHX_WORKING_ENV"],
        "Value-Based Care": ["VBC_PATIENT", "PAT_ATTACHMENT", "PAT_ELIGIBLE_BY_PROGRAM",
                              "PAT_LOGGED_TASKS", "PAT_STATUS_BY_PROGRAM"],
        "Administrative / Reference": ["PRACTICE", "PROVIDER", "LOCATION", "RESOURCES",
                                        "RESOURCE_GROUP", "RESOURCE_SCHEDULE", "ADMIN_RULE",
                                        "IMAGING_DEF", "RESOURCE_GROUP_MBR",
                                        "EXTERNAL_CODING_SYSTEM", "INTERFACE_PATIENT_MAPPING",
                                        "INTERFACE_SOURCE", "OTHER_SERVICE_DEF",
                                        "OTHER_SERVICE_DEF_PREFERENCE", "FLOWSHEET_CATEGORY"],
        "Devices": ["IMPLANTABLE_DEVICE"],
        "Patient Portal (Ontada Health)": ["conversation", "Patient_appointment_request"],
    }

    for cat, names in categories.items():
        if name in [n.upper() for n in names]:
            return cat

    # Fallback heuristics
    if "VBC" in name or entity_name in ["VBC_PATIENT_ELIGIBILITY", "VBC_PATIENT_PROGRAM_STATUS",
                                          "VBC_LOGGED_TASK", "VBC_ATTACHMENT", "VBC_TASK_TYPE"]:
        return "Value-Based Care"
    if name.startswith("G2_SOCIAL") or name.startswith("G2_DISTRESS"):
        return "Social Determinants (Patient History)"
    if "CHARGE" in name or "BILLING" in name or "BILLABLE" in name:
        return "Billing / Charges"
    if "ALLERG" in name:
        return "Allergies"
    if "IMMUNIZ" in name:
        return "Immunizations"
    if "DOCUMENT" in name or "NOTE" in name or "TRANSCR" in name:
        return "Documents / Notes"
    if "TREATMENT" in name or "REGIMEN" in name or "CHEMO" in name:
        return "Oncology Treatment / Regimens"
    if "ORDER" in name:
        return "Orders"
    if "MEDIC" in name or "PRESCRIPT" in name or "DRUG" in name or "RX" in name:
        return "Medications / Prescriptions"
    if "RESULT" in name or "LAB" in name:
        return "Lab Results"
    if "APPOINT" in name:
        return "Encounters / Appointments"
    if "VITAL" in name:
        return "Vitals / Observations"
    if "PROBLEM" in name:
        return "Problems / Diagnoses"
    if "INSUR" in name or "FIN_AUTH" in name:
        return "Financial Auth / Insurance"
    if "SURVEY" in name or "SCREENING" in name:
        return "Surveys / Screenings"
    if "OCM" in name:
        return "Oncology Care Model"
    if "NURSING" in name:
        return "Nursing Care"
    if "PATIENT" in name and ("CONTACT" in name or "IDENT" in name):
        return "Demographics"
    if "CARE_PLAN" in name or "TRANSFER" in name or "CCD" in name or "CQ_DOC" in name:
        return "Care Coordination"

    return "Other / Uncategorized"


def main():
    wb = load_workbook(XLSX_PATH, read_only=True, data_only=True)

    all_entities = []

    # Parse each sheet
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        print(f"Parsing sheet: {sheet_name}")

        if sheet_name == "Ontada Health":
            entities = parse_ontada_health_sheet(ws)
        else:
            entities = parse_relational_sheet(ws, sheet_name)

        print(f"  Found {len(entities)} entities, {sum(len(e['fields']) for e in entities)} fields")
        all_entities.extend(entities)

    wb.close()

    # Categorize entities
    for entity in all_entities:
        entity["category"] = categorize_entity(entity["entity_name"], entity.get("entity_description"), entity.get("source_sheet"))

    # Compute statistics
    total_entities = len(all_entities)
    total_fields = sum(len(e["fields"]) for e in all_entities)
    fields_with_desc = sum(1 for e in all_entities for f in e["fields"] if f.get("has_description"))
    fields_with_substantive_desc = sum(1 for e in all_entities for f in e["fields"] if f.get("description_is_substantive"))

    # Category breakdown
    category_stats = defaultdict(lambda: {"entities": 0, "fields": 0, "fields_with_desc": 0})
    for entity in all_entities:
        cat = entity["category"]
        category_stats[cat]["entities"] += 1
        category_stats[cat]["fields"] += len(entity["fields"])
        category_stats[cat]["fields_with_desc"] += sum(1 for f in entity["fields"] if f.get("has_description"))

    # Sheet breakdown
    sheet_stats = defaultdict(lambda: {"entities": 0, "fields": 0, "fields_with_desc": 0})
    for entity in all_entities:
        sheet = entity["source_sheet"]
        sheet_stats[sheet]["entities"] += 1
        sheet_stats[sheet]["fields"] += len(entity["fields"])
        sheet_stats[sheet]["fields_with_desc"] += sum(1 for f in entity["fields"] if f.get("has_description"))

    # Top 20 largest entities
    sorted_by_size = sorted(all_entities, key=lambda e: len(e["fields"]), reverse=True)
    top_20 = [{
        "entity_name": e["entity_name"],
        "source_sheet": e["source_sheet"],
        "category": e["category"],
        "field_count": len(e["fields"]),
        "fields_with_desc": sum(1 for f in e["fields"] if f.get("has_description")),
        "entity_description": e.get("entity_description")
    } for e in sorted_by_size[:20]]

    # Entities with 0 descriptions
    no_desc_entities = [{
        "entity_name": e["entity_name"],
        "source_sheet": e["source_sheet"],
        "category": e["category"],
        "field_count": len(e["fields"]),
    } for e in all_entities if not any(f.get("has_description") for f in e["fields"])]

    stats = {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "fields_with_description": fields_with_desc,
        "fields_with_substantive_description": fields_with_substantive_desc,
        "pct_fields_with_description": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
        "pct_fields_with_substantive_description": round(100 * fields_with_substantive_desc / total_fields, 1) if total_fields else 0,
        "by_sheet": dict(sheet_stats),
        "by_category": {k: dict(v) for k, v in sorted(category_stats.items(), key=lambda x: -x[1]["fields"])},
        "top_20_largest_entities": top_20,
        "entities_with_no_descriptions": no_desc_entities,
        "entities_with_no_descriptions_count": len(no_desc_entities),
    }

    # Write full inventory
    inventory_path = os.path.join(OUTPUT_DIR, "full-entity-inventory.json")
    with open(inventory_path, "w") as f:
        json.dump(all_entities, f, indent=2)
    print(f"\nWrote {inventory_path} ({total_entities} entities, {total_fields} fields)")

    # Write stats
    stats_path = os.path.join(OUTPUT_DIR, "analysis-stats.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Wrote {stats_path}")

    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total entities: {total_entities}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with any description: {fields_with_desc} ({stats['pct_fields_with_description']}%)")
    print(f"Fields with substantive description: {fields_with_substantive_desc} ({stats['pct_fields_with_substantive_description']}%)")

    print(f"\n=== By Sheet ===")
    for sheet, s in sheet_stats.items():
        print(f"  {sheet}: {s['entities']} entities, {s['fields']} fields, {s['fields_with_desc']} with desc")

    print(f"\n=== By Category ===")
    for cat, s in sorted(category_stats.items(), key=lambda x: -x[1]["fields"]):
        print(f"  {cat}: {s['entities']} entities, {s['fields']} fields")

    print(f"\n=== Top 10 Largest Entities ===")
    for e in top_20[:10]:
        print(f"  {e['entity_name']}: {e['field_count']} fields ({e['category']})")

    print(f"\n=== Entities with no descriptions: {len(no_desc_entities)} ===")
    for e in no_desc_entities[:10]:
        print(f"  {e['entity_name']} ({e['source_sheet']}): {e['field_count']} fields")


if __name__ == "__main__":
    main()
