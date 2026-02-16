#!/usr/bin/env python3
"""
Recategorize and regenerate summary from the full entity inventory.
Uses more comprehensive pattern matching based on actual table names.
"""

import json
import re
from pathlib import Path

ANALYSIS = Path(__file__).parent

def categorize_table(table_name, description=""):
    """Assign a domain category based on table name and description."""
    name = table_name.upper()
    desc = (description or "").upper()
    
    # Lookup tables first
    if name.startswith("LK"):
        return "Lookup/Reference"
    
    # Pharmacy/Prescription (AU_ prefix from VistA heritage)
    if name.startswith("AU_"):
        return "Pharmacy/Prescription"
    
    # Billing / Revenue Cycle / Financial
    if any(x in name for x in ["BILLING", "ACCOUNT", "CHARGE", "CLAIM", "RCM", 
                                 "FINANCIALGROUP", "SLIDINGSCALE", "TRANSACTIONCODE",
                                 "MEDICALCODING"]):
        return "Billing/Financial"
    
    # Insurance / Coverage / Payers
    if any(x in name for x in ["COVERAGE", "PAYER", "INSURANCE", "MSPQ"]):
        return "Insurance/Coverage"
    
    # Care Plans
    if any(x in name for x in ["CAREPLAN", "CARE_PLAN"]):
        return "Care Plans"
    
    # Treatment Plans / Goals / Interventions
    if any(x in name for x in ["GOAL", "INTERVENTION", "TREATMENTPLAN"]):
        return "Goals/Interventions"
    
    # Conditions / Problems / Diagnoses
    if any(x in name for x in ["CONDITION", "PROBLEM", "DIAGNOS"]):
        return "Conditions/Problems"
    
    # Documents / Notes / Clinical Notes
    if any(x in name for x in ["DOCUMENT", "NOTE", "AMENDMENT", "NURSEBRAIN",
                                 "CLINICALNOTES", "CONSULTSNOTESREVIEW"]):
        return "Documents/Notes"
    
    # Encounters / Episodes / Visits / Admissions
    if any(x in name for x in ["ENCOUNTER", "VISIT", "ADMISSION", "EPISODEOFCARE",
                                 "ACCOMMODATION", "BEDSTATUS", "BEDALLOWED"]):
        return "Encounters"
    
    # Imaging
    if any(x in name for x in ["IMAGING"]):
        return "Imaging"
    
    # Diagnostic Reports
    if any(x in name for x in ["DIAGNOSTICREPORT"]):
        return "Diagnostic Reports"
    
    # Observations / Vitals / Detected Issues
    if any(x in name for x in ["OBSERVATION", "VITAL", "DETECTEDISSUE", "DRAFTOBSERVATION",
                                 "REFERENCERANGE", "QUANTITY", "VALUE"]):
        return "Observations/Vitals"
    
    # Laboratory / Specimens
    if any(x in name for x in ["LAB", "SPECIMEN"]):
        return "Laboratory/Specimens"
    
    # Orders / Service Requests / Pending Orders
    if any(x in name for x in ["ORDER", "SERVICEREQUEST", "PENDINGORDER"]):
        return "Orders"
    
    # Medications / Drugs / Dosage / Nutrition
    if any(x in name for x in ["MEDICATION", "MED_", "DRUG", "DOSAGE", "NUTRITIONREQUEST",
                                 "OUTPATIENT_MED", "INPATIENT_MED", "RECONCILIATION"]):
        return "Medications"
    
    # Patient Demographics / Related Persons / Identifiers / Addresses
    if any(x in name for x in ["PATIENT", "PERSON", "RELATEDPERSON", "ADDRESS",
                                 "CONTACTPOINT", "CONTACTDETAIL", "IDENTIFIER",
                                 "MEDICALRECORDNUMBER", "RACE", "ETHNICIT",
                                 "MERGED_PATIENT"]):
        return "Patient Demographics"
    
    # Allergies
    if any(x in name for x in ["ALLERG"]):
        return "Allergies"
    
    # Immunizations / Vaccines
    if any(x in name for x in ["IMMUNIZ", "VACCINE"]):
        return "Immunizations"
    
    # Procedures / Surgery
    if any(x in name for x in ["PROCEDURE", "SURGERY", "SURGICAL", "PERIOPERATIVE",
                                 "ANESTHESIA", "HCSLOCATION"]):
        return "Procedures/Surgery"
    
    # Questionnaires / Forms / Items / Assessments
    if any(x in name for x in ["QUESTIONNAIRE", "FORM", "ASSESSMENT", "ITEM"]):
        return "Questionnaires/Forms"
    
    # Scheduling / Appointments
    if any(x in name for x in ["SCHEDULE", "APPOINTMENT", "SLOT", "TIMING", "RECURRENCE"]):
        return "Scheduling"
    
    # Medical Devices / Implants
    if any(x in name for x in ["DEVICE", "IMPLANT"]):
        return "Medical Devices"
    
    # Referrals
    if any(x in name for x in ["REFERRAL"]):
        return "Referrals"
    
    # Behavioral Health / Group Sessions / Legal Status / Criminal Status
    if any(x in name for x in ["GROUP", "BEHAVIORAL", "LEGALSTATUS", "CRIMINALSTATUS",
                                 "CHARTRESTRICTION", "SENSITIVEPATIENT"]):
        return "Behavioral Health"
    
    # Care Team
    if any(x in name for x in ["CARETEAM"]):
        return "Care Team"
    
    # Consents / Release of Info
    if any(x in name for x in ["CONSENT", "RELEASEOFINFORMATION"]):
        return "Consents/ROI"
    
    # Communications / Messages
    if any(x in name for x in ["COMMUNICATION", "MESSAGE"]):
        return "Communications"
    
    # Family History
    if any(x in name for x in ["FAMILY"]):
        return "Family History"
    
    # Provenance
    if any(x in name for x in ["PROVENANCE"]):
        return "Provenance"
    
    # Media
    if any(x in name for x in ["MEDIA", "FILESTORAGE"]):
        return "Media/Attachments"
    
    # Tasks / Clinical Tasks
    if any(x in name for x in ["TASK", "CLINICALTASK"]):
        return "Tasks"
    
    # Organizations / Locations / Practitioners / Healthcare Services
    if any(x in name for x in ["ORGANIZATION", "LOCATION", "PRACTITIONER",
                                 "HEALTHCARESERVICE", "MANUFACTURER", "FACILIT",
                                 "PROGRAMCODE", "PHYSICIAN", "USER", "SESSION",
                                 "FREQUENC", "ROUTE"]):
        return "Organizations/Providers"
    
    return "Other"


def main():
    with open(ANALYSIS / "entity-inventory-full.json") as f:
        entities = json.load(f)
    
    # Recategorize
    for e in entities:
        e["category"] = categorize_table(e["table_name"], e.get("description", ""))
    
    # Save updated full inventory
    with open(ANALYSIS / "entity-inventory-full.json", "w") as f:
        json.dump(entities, f, indent=2)
    
    # Build summary
    total_fields = sum(len(e["fields"]) for e in entities)
    fields_with_desc = sum(
        1 for e in entities for field in e["fields"] if field.get("description")
    )
    tables_with_desc = sum(1 for e in entities if e.get("description"))
    tables_with_fks = sum(1 for e in entities if e.get("foreign_keys"))
    tables_with_pks = sum(1 for e in entities if e.get("primary_keys"))
    
    # Category breakdown
    categories = {}
    for e in entities:
        cat = e["category"]
        if cat not in categories:
            categories[cat] = {"tables": 0, "fields": 0, "fields_with_desc": 0, "example_tables": []}
        categories[cat]["tables"] += 1
        categories[cat]["fields"] += len(e["fields"])
        categories[cat]["fields_with_desc"] += sum(
            1 for f in e["fields"] if f.get("description")
        )
        if len(categories[cat]["example_tables"]) < 5:
            categories[cat]["example_tables"].append(e["table_name"])
    
    # Source breakdown
    sources = {}
    for e in entities:
        src = e["source"]
        if src not in sources:
            sources[src] = {"tables": 0, "fields": 0}
        sources[src]["tables"] += 1
        sources[src]["fields"] += len(e["fields"])
    
    # Top 20 largest tables
    top_tables = sorted(entities, key=lambda e: len(e["fields"]), reverse=True)[:20]
    
    # Check what's still "Other"
    other = [e for e in entities if e["category"] == "Other"]
    
    summary = {
        "total_tables": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "description_percentage": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "tables_with_descriptions": tables_with_desc,
        "tables_with_primary_keys": tables_with_pks,
        "tables_with_foreign_keys": tables_with_fks,
        "by_source": sources,
        "by_category": dict(sorted(categories.items(), key=lambda x: x[1]["tables"], reverse=True)),
        "top_20_largest_tables": [
            {
                "table": t["table_name"],
                "source": t["source"],
                "category": t["category"],
                "field_count": len(t["fields"]),
                "fk_count": len(t.get("foreign_keys", [])),
                "description": t["description"][:120] + "..." if len(t.get("description", "")) > 120 else t.get("description", "")
            }
            for t in top_tables
        ],
        "uncategorized_tables": [e["table_name"] for e in other]
    }
    
    with open(ANALYSIS / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"=== Updated Summary ===")
    print(f"Total tables: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['description_percentage']}%)")
    print(f"Tables with descriptions: {tables_with_desc}")
    print(f"Tables with PKs: {tables_with_pks}")
    print(f"Tables with FKs: {tables_with_fks}")
    print(f"\nBy source:")
    for src, data in sources.items():
        print(f"  {src}: {data['tables']} tables, {data['fields']} fields")
    print(f"\nBy category (sorted by table count):")
    for cat, data in sorted(categories.items(), key=lambda x: x[1]["tables"], reverse=True):
        print(f"  {cat}: {data['tables']} tables, {data['fields']} fields")
    print(f"\nUncategorized ('Other'): {len(other)} tables")
    for e in other:
        print(f"  {e['table_name']}: {e.get('description','')[:80]}")
    print(f"\nTop 10 largest:")
    for t in top_tables[:10]:
        print(f"  {t['table_name']} ({t['source']}): {len(t['fields'])} fields - {t['category']}")


if __name__ == "__main__":
    main()
