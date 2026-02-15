"""
Generate a detailed domain-level breakdown of the Credible data dictionary
for use in the analysis.md coverage table.
"""

import json
from collections import defaultdict

INPUT = "../../../results/qualifacts-systems-llc--credible-behavioral-health/downloads/data-dictionary.json"

with open(INPUT) as f:
    entities = json.load(f)

# Manual domain categorization based on entity names and field inspection
domain_map = {
    # Demographics / Profile
    "Profile": "Demographics / Profile",
    "Profile Extended": "Demographics / Profile",
    "Profile Previous Address": "Demographics / Profile",
    "Profile Previous FullName": "Demographics / Profile",
    "Contact": "Demographics / Profile",
    "Family": "Demographics / Profile",
    "Family History": "Demographics / Profile",
    "Family Medical History": "Demographics / Profile",
    "Family Medical History Detail": "Demographics / Profile",
    "Education": "Demographics / Profile",
    "Geo Area": "Demographics / Profile",
    "Organization": "Demographics / Profile",
    "Location": "Demographics / Profile",
    "Links": "Demographics / Profile",

    # Clinical
    "Allergies": "Clinical",
    "Client Diagnosis": "Clinical",
    "Client Diagnosis Detail": "Clinical",
    "Visit Service Diagnosis": "Clinical",
    "Immunizations": "Clinical",
    "Implantable Device": "Clinical",
    "Medical Profile": "Clinical / Vitals",
    "Medical Profile Conditions": "Clinical",
    "Lab Report": "Clinical / Labs",
    "Lab Test Results": "Clinical / Labs",
    "Clinical Goal": "Clinical",
    "Clinical Notes": "Clinical / Notes",
    "Clinical Procedure": "Clinical",
    "Overview Image": "Clinical",
    "Outcomes": "Clinical / Outcomes",

    # Medications
    "eRx Eligibility": "Medications / Prescribing",
    "eRx Messages": "Medications / Prescribing",
    "Medication Request": "Medications / Prescribing",
    "Medication List Reconciliation": "Medications / Prescribing",
    "Medication History": "Medications / Prescribing",
    "Medication Notes": "Medications / Prescribing",
    "Medication Prior Authorization": "Medications / Prescribing",
    "EMAR": "Medications / Prescribing",
    "EMAR Reconciliation": "Medications / Prescribing",
    "Medication Verification": "Medications / Prescribing",

    # Billing / Financial
    "Claims": "Billing / Financial",
    "Payments": "Billing / Financial",
    "PaymentPlan": "Billing / Financial",
    "Liability": "Billing / Financial",
    "Funding Activity": "Billing / Financial",
    "Visit Service Claim Note": "Billing / Financial",
    "Visit Service Insurance": "Billing / Financial",
    "277 Response": "Billing / Financial",
    "Statement Header": "Billing / Financial",
    "Statement Detail": "Billing / Financial",
    "Bed Board Billing": "Billing / Financial",
    "Bed Board Billing Header": "Billing / Financial",

    # Insurance
    "Insurance": "Insurance / Coverage",
    "Insurance Subscriber": "Insurance / Coverage",
    "Insurance Visit Type": "Insurance / Coverage",
    "Payer": "Insurance / Coverage",
    "Eligibility": "Insurance / Coverage",

    # Treatment Planning / BH Specialty
    "ASAM Assessment": "Treatment Planning / BH",
    "Care Plan": "Treatment Planning / BH",
    "Care Team": "Treatment Planning / BH",
    "Treatment Plan": "Treatment Planning / BH",
    " Treatment Plan Plus": "Treatment Planning / BH",
    " Treatment Plan Plus Details": "Treatment Planning / BH",
    " Treatment Plan Plus Extended": "Treatment Planning / BH",
    "Credible Plan Header": "Treatment Planning / BH",
    "Credible Plan Component": "Treatment Planning / BH",
    "Credible Plan Custom Extended": "Treatment Planning / BH",
    "Credible Plan Documentation": "Treatment Planning / BH",
    "Credible Plan Signature": "Treatment Planning / BH",
    "Questionnaire": "Treatment Planning / BH",
    "Questionnaire Category": "Treatment Planning / BH",
    "Questionnaire Signature": "Treatment Planning / BH",
    "Episode": "Treatment Planning / BH",

    # Notes / Documentation
    "Notes": "Notes / Documentation",
    "Amendments": "Notes / Documentation",
    "Warnings": "Notes / Documentation",
    "Order Notes": "Notes / Documentation",

    # Visits / Encounters
    "Visit Service": "Visits / Encounters",
    "Visit Service Approval": "Visits / Encounters",
    "Visit Service Transportation": "Visits / Encounters",
    "Encounters": "Visits / Encounters",
    "Scheduler Appointment": "Visits / Encounters",
    "SchedulerPlanner": "Visits / Encounters",

    # Residential
    "Bed Board Shift Notes": "Residential / Facility",
    "Bed Board Whiteboard Notes": "Residential / Facility",
    "FosterHome": "Residential / Facility",

    # Communication
    "Appointment Notification": "Communication / Messaging",
    "Messaging": "Communication / Messaging",
    "Notification": "Communication / Messaging",
    "PortalQuestionnaire": "Communication / Messaging",
    "Portal Questionnaire Signature": "Communication / Messaging",
    "Direct Sent Message": "Communication / Messaging",
    "Direct Received Message": "Communication / Messaging",
    "Eligibility Messages": "Communication / Messaging",
    "Eligibility Message Details": "Communication / Messaging",

    # Administrative
    "Authorization": "Administrative",
    "Authorization Provider": "Administrative",
    "Authorization Visit Type": "Administrative",
    "Orders": "Administrative",
    "Enrollment": "Administrative",
    "Employee": "Administrative",
    "Attachments": "Administrative",
    "External Provider": "Administrative",
    "External Provider History": "Administrative",
    "Record Access": "Administrative",
    "834 Load": "Administrative",
    "MassHiway": "Administrative",
}

# Build domain breakdown
domains = defaultdict(lambda: {"entities": [], "field_count": 0})

for e in entities:
    name = e["entityName"]
    domain = domain_map.get(name, "Uncategorized")
    domains[domain]["entities"].append({
        "name": name,
        "fields": len(e["fields"]),
        "fileName": e["fileName"],
        "customOnly": e.get("isCustomOnly", False),
        "hasCustom": e.get("hasCustomFields", False),
    })
    domains[domain]["field_count"] += len(e["fields"])

# Print domain breakdown
print(f"{'Domain':<30} {'Entities':>8} {'Fields':>8}")
print("-" * 50)
total_e = 0
total_f = 0
for domain in sorted(domains.keys()):
    ds = domains[domain]
    print(f"{domain:<30} {len(ds['entities']):>8} {ds['field_count']:>8}")
    for ent in sorted(ds["entities"], key=lambda x: -x["fields"]):
        custom_note = " [custom-only]" if ent["customOnly"] else (" [+custom]" if ent["hasCustom"] else "")
        print(f"  {ent['name']:<28} {ent['fields']:>6}{custom_note}")
    total_e += len(ds["entities"])
    total_f += ds["field_count"]

print("-" * 50)
print(f"{'TOTAL':<30} {total_e:>8} {total_f:>8}")

# Save to JSON
with open("domain-breakdown.json", "w") as f:
    json.dump(dict(domains), f, indent=2)

print("\nSaved: domain-breakdown.json")
