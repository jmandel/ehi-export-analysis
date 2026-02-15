#!/usr/bin/env python3
"""Parse the entity-data-dictionary.json and produce comprehensive statistics."""

import json
import sys
from collections import Counter

DICT_PATH = "../../../results/allegiancemd-software-inc/downloads/entity-data-dictionary.json"

with open(DICT_PATH) as f:
    data = json.load(f)

total_entities = len(data)
total_fields = 0
fields_with_desc = 0
fields_without_desc = 0
entity_stats = []
type_counter = Counter()

for entity_name, fields in data.items():
    n_fields = len(fields)
    n_described = sum(1 for f in fields if f.get("description", "").strip())
    n_undescribed = n_fields - n_described
    total_fields += n_fields
    fields_with_desc += n_described
    fields_without_desc += n_undescribed
    
    for f in fields:
        type_counter[f["type"]] += 1
    
    entity_stats.append({
        "entity": entity_name,
        "fields": n_fields,
        "described": n_described,
        "undescribed": n_undescribed,
        "pct_described": round(100 * n_described / n_fields, 1) if n_fields > 0 else 0,
    })

# Sort by field count descending
entity_stats.sort(key=lambda x: x["fields"], reverse=True)

print("=" * 80)
print("EHI EXPORT DATA DICTIONARY ANALYSIS — AllegianceMD Veracity")
print("=" * 80)
print(f"\nTotal entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({round(100*fields_with_desc/total_fields, 1)}%)")
print(f"Fields without descriptions: {fields_without_desc} ({round(100*fields_without_desc/total_fields, 1)}%)")

print(f"\nEntities with 100% description coverage:")
for e in entity_stats:
    if e["pct_described"] == 100:
        print(f"  {e['entity']}: {e['fields']} fields")

print(f"\nEntities with 0% description coverage:")
for e in entity_stats:
    if e["pct_described"] == 0:
        print(f"  {e['entity']}: {e['fields']} fields")

print(f"\nEntities with partial description coverage:")
for e in entity_stats:
    if 0 < e["pct_described"] < 100:
        print(f"  {e['entity']}: {e['described']}/{e['fields']} fields ({e['pct_described']}%)")

print(f"\nField type distribution:")
for t, count in type_counter.most_common():
    print(f"  {t}: {count}")

print(f"\n{'Entity':<45} {'Fields':>6} {'Described':>10} {'%':>6}")
print("-" * 70)
for e in entity_stats:
    print(f"{e['entity']:<45} {e['fields']:>6} {e['described']:>10} {e['pct_described']:>5}%")
print("-" * 70)
print(f"{'TOTAL':<45} {total_fields:>6} {fields_with_desc:>10} {round(100*fields_with_desc/total_fields,1):>5}%")

# Categorize entities by domain
domain_mapping = {
    "Demographics": ["PatientEntity", "GuarantorEntity", "PatientCustomFieldsEntity"],
    "Clinical - Encounters": ["EncountersEntity", "EncountersDiagEntity", "EmrEncounterEntity"],
    "Clinical - Problems": ["EmrProblemEntity"],
    "Clinical - Medications": ["EmrMedicationEntity"],
    "Clinical - Allergies": ["EmrAllergyEntity"],
    "Clinical - Vitals": ["EmrVitalsEntity", "EmrVitalsCategoryEntity"],
    "Clinical - Immunizations": ["EmrInjectionEntity"],
    "Clinical - Devices": ["EmrImplantableDeviceEntity"],
    "Clinical - Orders/Labs": ["EmrPatientOrderItemEntity", "EmrPatientOrderPanelEntity"],
    "Clinical - Screenings": ["ScreeningEntity"],
    "Clinical - Medical Forms": ["PatientMedicalFormEntity"],
    "Insurance/Coverage": ["InsuranceDataEntity", "InsuranceDataAuthorizationsEntity"],
    "Billing/Transactions": ["TransactionsEntity", "PaymentEntity"],
    "Cases (Workers Comp etc)": ["CasesEntity"],
    "Scheduling": ["AppointmentsEntity"],
    "Care Team/Referrals": ["PatientCareTeamEntity", "EmrRefToProvidersEntity"],
    "Communications": ["MessagesEntity", "InternalNotesEntity", "NotesEntity"],
    "Tasks": ["TasksEntity", "TaskCommentsEntity"],
    "Pharmacy": ["PatientPharmacyEntity"],
}

print(f"\n\n{'Domain':<30} {'Entities':>8} {'Fields':>7} {'Described':>10} {'%':>6}")
print("-" * 65)
for domain, entities in domain_mapping.items():
    d_fields = sum(e["fields"] for e in entity_stats if e["entity"] in entities)
    d_desc = sum(e["described"] for e in entity_stats if e["entity"] in entities)
    pct = round(100 * d_desc / d_fields, 1) if d_fields > 0 else 0
    print(f"{domain:<30} {len(entities):>8} {d_fields:>7} {d_desc:>10} {pct:>5}%")

# Save full inventory as JSON
inventory = {
    "summary": {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_without_descriptions": fields_without_desc,
        "pct_described": round(100 * fields_with_desc / total_fields, 1),
    },
    "entities": entity_stats,
    "type_distribution": dict(type_counter.most_common()),
    "domain_mapping": domain_mapping,
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print("\n\nFull inventory saved to full-entity-inventory.json")
