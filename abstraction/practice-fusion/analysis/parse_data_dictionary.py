#!/usr/bin/env python3
"""Parse Practice Fusion v9 data dictionary JSON and produce summary statistics.

Input: results/practice-fusion/downloads/v9-data-dictionary.json
Output: Prints summary tables, field counts, domain categorization, and quality metrics.
"""

import json
import sys
from collections import Counter

DD_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/practice-fusion/downloads/v9-data-dictionary.json"

with open(DD_PATH) as f:
    dd = json.load(f)

# --- Basic stats ---
total_tables = len(dd)
total_fields = sum(t["field_count"] for t in dd.values())
fields_with_desc = sum(
    1 for t in dd.values() for f in t["fields"]
    if f.get("description", "").strip()
)
fields_with_type = sum(
    1 for t in dd.values() for f in t["fields"]
    if f.get("data_type", "").strip()
)

print("=" * 70)
print("PRACTICE FUSION v9 DATA DICTIONARY SUMMARY")
print("=" * 70)
print(f"Total tables (TSV files):     {total_tables}")
print(f"Total fields:                 {total_fields}")
print(f"Fields with descriptions:     {fields_with_desc} ({fields_with_desc*100//total_fields}%)")
print(f"Fields with data types:       {fields_with_type} ({fields_with_type*100//total_fields}%)")
print()

# --- Data type distribution ---
type_counter = Counter()
for t in dd.values():
    for f in t["fields"]:
        type_counter[f.get("data_type", "MISSING")] += 1

print("DATA TYPE DISTRIBUTION:")
for dtype, count in type_counter.most_common():
    print(f"  {dtype:25s} {count:4d}")
print()

# --- Category mapping (based on v9 index page organization) ---
categories = {
    "Demographics": [
        "communication-settings.tsv", "occupation-industry.tsv", "patient-appointments.tsv",
        "patient-contacts.tsv", "patient-demographics.tsv", "patient-ethnicity.tsv",
        "patient-financial-resources.tsv", "patient-gender-identity-sexual-orientation.tsv",
        "patient-race.tsv", "tribal-affiliation.tsv"
    ],
    "Patient Documents": [
        "patient-documents.tsv", "patient-questionnaire.tsv"
    ],
    "Clinical": [
        "care-team.tsv", "care-team-profiles.tsv", "facilities.tsv",
        "patient-advance-directives.tsv", "patient-allergy.tsv", "patient-allergy-reactions.tsv",
        "patient-clinical-worksheet-detail.tsv", "patient-clinical-worksheet-summaries.tsv",
        "patient-conditions.tsv", "patient-diagnoses.tsv", "patient-drug-alert-overrides.tsv",
        "patient-education.tsv", "patient-encounter-addendums.tsv",
        "patient-encounter-diagnoses.tsv", "patient-encounter-events.tsv",
        "patient-encounter-medications.tsv", "patient-encounter-observations.tsv",
        "patient-encounter-procedures.tsv", "patient-encounters.tsv",
        "patient-family-history-diagnoses.tsv", "patient-family-medical-history.tsv",
        "patient-goals.tsv", "patient-healthcare-devices.tsv", "patient-health-concerns.tsv",
        "patient-immunization-registry.tsv", "patient-immunizations.tsv",
        "patient-risk-scores.tsv", "patient-smokingstatus.tsv", "pinned-notes.tsv",
        "provider-profiles.tsv", "providers.tsv", "users.tsv"
    ],
    "Billing and Insurance": [
        "contact-profiles.tsv", "patient-encounter-documents.tsv", "patient-guarantor.tsv",
        "patient-insurance-eligibilities.tsv", "patient-insurances.tsv",
        "patient-restrictions.tsv", "patient-superbills.tsv", "superbill-diagnosis.tsv",
        "superbill-events.tsv", "superbill-insurances.tsv",
        "superbill-procedure-modifiers.tsv", "superbill-procedures.tsv"
    ],
    "Medications and Prescriptions": [
        "immunization-vis-editions.tsv", "patient-drug-alert-overrides.tsv",
        "patient-encounter-medications.tsv", "patient-immunization-transmission-history.tsv",
        "patient-med-history.tsv", "patient-medication-history-consent.tsv",
        "patient-medications.tsv", "patient-prescriptions.tsv", "pharmacies.tsv",
        "preferred-pharmacy.tsv", "prescription-transactions.tsv"
    ],
    "Labs": [
        "lab-result-item-specimen-data.tsv", "lab-result-tests-observation-notes.tsv",
        "labs.tsv", "patient-lab-order-documents.tsv", "patient-lab-order-item-answers.tsv",
        "patient-lab-order-item-diagnoses.tsv", "patient-lab-order-items.tsv",
        "patient-lab-order-item-specimens.tsv", "patient-lab-orders.tsv",
        "patient-lab-result-documents.tsv", "patient-lab-result-item-notes.tsv",
        "patient-lab-result-notes.tsv", "patient-lab-result-test-observation-diagnoses.tsv",
        "patient-lab-result-tests-observations.tsv", "patient-lab-results.tsv"
    ],
    "Referrals": [
        "patient-referral-recipients.tsv", "patient-referrals.tsv"
    ],
    "Messaging": [
        "patient-message-attachments.tsv", "patient-message-recipients.tsv",
        "patient-messages.tsv"
    ]
}

print("TABLES AND FIELDS BY CATEGORY:")
print(f"{'Category':<30s} {'Tables':>7s} {'Fields':>7s}")
print("-" * 50)
cat_totals = {}
for cat, tables in categories.items():
    # Deduplicate (drug-alert-overrides appears in both Clinical and Meds)
    unique_tables = [t for t in tables if t in dd]
    n_fields = sum(dd[t]["field_count"] for t in unique_tables)
    cat_totals[cat] = (len(unique_tables), n_fields)
    print(f"  {cat:<28s} {len(unique_tables):>7d} {n_fields:>7d}")
print("-" * 50)
print(f"  {'(unique tables)':<28s} {total_tables:>7d} {total_fields:>7d}")
print()

# --- Per-table detail ---
print("ALL TABLES (sorted by field count, descending):")
print(f"{'Table Name':<55s} {'Fields':>6s} {'Desc?':>6s} {'Types?':>6s}")
print("-" * 75)
for name, t in sorted(dd.items(), key=lambda x: -x[1]["field_count"]):
    n = t["field_count"]
    n_desc = sum(1 for f in t["fields"] if f.get("description", "").strip())
    n_type = sum(1 for f in t["fields"] if f.get("data_type", "").strip())
    print(f"  {name:<53s} {n:>6d} {n_desc:>6d} {n_type:>6d}")
print()

# --- Relationship analysis: count GUID foreign keys ---
guid_fields = []
for name, t in dd.items():
    for f in t["fields"]:
        if f["data_type"] in ("Guid", "Guid?") and f["field_name"] != "PatientPracticeGuid":
            guid_fields.append((name, f["field_name"]))

# Find GUID field names that appear in multiple tables (likely FK relationships)
guid_name_counter = Counter(fn for _, fn in guid_fields)
shared_guids = {k: v for k, v in guid_name_counter.items() if v > 1}

print(f"RELATIONSHIP INDICATORS:")
print(f"  Total GUID/Guid? fields (excl PatientPracticeGuid): {len(guid_fields)}")
print(f"  GUID field names appearing in 2+ tables: {len(shared_guids)}")
print(f"  These likely represent foreign key relationships:")
for gname, cnt in sorted(shared_guids.items(), key=lambda x: -x[1]):
    print(f"    {gname}: appears in {cnt} tables")
print()

# --- Quality: check for thin descriptions ---
thin_descs = []
for name, t in dd.items():
    for f in t["fields"]:
        desc = f.get("description", "").strip()
        if len(desc) < 10 and desc:
            thin_descs.append((name, f["field_name"], desc))

print(f"DESCRIPTION QUALITY:")
print(f"  Fields with description < 10 chars: {len(thin_descs)}")
if thin_descs:
    for tname, fname, desc in thin_descs[:10]:
        print(f"    {tname} → {fname}: '{desc}'")
print()

# --- Fields that reference code systems ---
code_fields = []
for name, t in dd.items():
    for f in t["fields"]:
        fn = f["field_name"].lower()
        if any(kw in fn for kw in ["codesystem", "code_system", "valueset", "codeset"]):
            code_fields.append((name, f["field_name"], f.get("description", "")))

print(f"CODE SYSTEM REFERENCE FIELDS:")
print(f"  Total fields referencing code systems: {len(code_fields)}")
for tname, fname, desc in code_fields:
    print(f"    {tname} → {fname}: {desc[:80]}")
print()

# --- Value set / enum documentation ---
enum_fields = []
for name, t in dd.items():
    for f in t["fields"]:
        desc = f.get("description", "")
        if any(kw in desc.lower() for kw in ["valid values", "possible values", "enum", "one of"]):
            enum_fields.append((name, f["field_name"], desc[:100]))

print(f"FIELDS WITH VALUE ENUMERATION IN DESCRIPTION: {len(enum_fields)}")
for tname, fname, desc in enum_fields:
    print(f"    {tname} → {fname}: {desc}")
