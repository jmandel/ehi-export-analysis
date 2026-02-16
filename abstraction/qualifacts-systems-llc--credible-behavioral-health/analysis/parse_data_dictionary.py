#!/usr/bin/env python3
"""Parse the Credible Behavioral Health EHI Export data dictionary JSON
and produce entity-inventory-full.json and entity-inventory-summary.json."""

import json
from collections import Counter

INPUT = "../downloads/data-dictionary.json"

with open(INPUT) as f:
    raw = json.load(f)

# Build full inventory
entities = []
for entity in raw:
    fields = []
    for field in entity.get("fields", []):
        fields.append({
            "name": field.get("fieldName", ""),
            "type": field.get("dataType", ""),
            "nullable": field.get("isNullable"),
            "example_value": field.get("exampleValue"),
            "description": field.get("description", ""),
        })
    entities.append({
        "entity_name": entity["entityName"],
        "file_name": entity.get("fileName", ""),
        "is_custom_only": entity.get("isCustomOnly", False),
        "has_custom_fields": entity.get("hasCustomFields", False),
        "field_count": entity["fieldCount"],
        "fields": fields,
    })

with open("entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

# Build summary
total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)
fields_with_desc = 0
fields_with_type = 0
fields_with_example = 0
fields_with_nullable = 0
type_counts = Counter()
custom_only_entities = []
entities_with_custom = []

for e in entities:
    if e["is_custom_only"]:
        custom_only_entities.append(e["entity_name"])
    if e["has_custom_fields"]:
        entities_with_custom.append(e["entity_name"])
    for field in e["fields"]:
        if field["description"] and field["description"].strip():
            fields_with_desc += 1
        if field["type"] and field["type"].strip():
            fields_with_type += 1
            type_counts[field["type"]] += 1
        if field["example_value"] is not None and str(field["example_value"]).strip():
            fields_with_example += 1
        if field["nullable"] is not None:
            fields_with_nullable += 1

# Categorize entities by domain
domain_mapping = {
    "Demographics": ["Profile", "Profile Extended", "Profile Previous Address",
                     "Profile Previous FullName", "Contact", "Family", "Family History",
                     "Overview Image"],
    "Clinical - Diagnoses": ["Client Diagnosis", "Client Diagnosis Detail",
                             "Visit Service Diagnosis"],
    "Clinical - Medications": ["Medication Request", "Medication History",
                                "Medication Notes", "Medication Prior Authorization",
                                "Medication List Reconciliation", "Medication Verification",
                                "eRx Messages", "eRx Eligibility", "EMAR", "EMAR Reconciliation"],
    "Clinical - Allergies": ["Allergies"],
    "Clinical - Immunizations": ["Immunizations"],
    "Clinical - Lab": ["Lab Test Results", "Lab Report"],
    "Clinical - Medical Profile": ["Medical Profile", "Medical Profile Conditions",
                                    "Implantable Device"],
    "Clinical - Family Medical History": ["Family Medical History",
                                           "Family Medical History Detail"],
    "Clinical - Notes & Documentation": ["Clinical Notes", "Notes", "Amendments",
                                          "Attachments", "Clinical Procedure",
                                          "Questionnaire", "Questionnaire Category",
                                          "Questionnaire Signature",
                                          "PortalQuestionnaire",
                                          "Portal Questionnaire Signature"],
    "Clinical - Treatment Plans": ["Treatment Plan", " Treatment Plan Plus",
                                    " Treatment Plan Plus Details",
                                    " Treatment Plan Plus Extended",
                                    "Credible Plan Header", "Credible Plan Component",
                                    "Credible Plan Custom Extended",
                                    "Credible Plan Documentation",
                                    "Credible Plan Signature"],
    "Clinical - Goals & Outcomes": ["Clinical Goal", "Outcomes"],
    "Clinical - Care Team": ["Care Team"],
    "Clinical - Care Plan": ["Care Plan"],
    "Clinical - Orders": ["Orders", "Order Notes"],
    "Clinical - Assessments": ["ASAM Assessment", "Education"],
    "Encounters / Visits": ["Visit Service", "Visit Service Transportation",
                             "Visit Service Claim Note", "Visit Service Insurance",
                             "Visit Service Approval", "Encounters",
                             "Scheduler Appointment", "SchedulerPlanner",
                             "Appointment Notification"],
    "Insurance & Eligibility": ["Insurance", "Insurance Subscriber",
                                  "Insurance Visit Type", "Eligibility",
                                  "Eligibility Messages", "Eligibility Message Details",
                                  "Authorization", "Authorization Provider",
                                  "Authorization Visit Type", "834 Load"],
    "Billing & Payments": ["Claims", "Payments", "Liability", "Funding Activity",
                            "PaymentPlan", "Statement Header", "Statement Detail",
                            "277 Response", "Bed Board Billing",
                            "Bed Board Billing Header"],
    "Residential / Bed Board": ["Bed Board Shift Notes", "Bed Board Whiteboard Notes",
                                 "FosterHome"],
    "Communications": ["Messaging", "Direct Sent Message", "Direct Received Message",
                        "Notification", "MassHiway"],
    "Administrative": ["Enrollment", "Payer", "Organization", "Location",
                        "Geo Area", "Employee", "Links", "External Provider",
                        "External Provider History", "Record Access", "Warnings",
                        "Episode"],
}

# Build category summary
category_summary = {}
assigned = set()
for category, entity_names in domain_mapping.items():
    cat_entities = []
    cat_fields = 0
    for e in entities:
        if e["entity_name"] in entity_names:
            cat_entities.append(e["entity_name"])
            cat_fields += e["field_count"]
            assigned.add(e["entity_name"])
    category_summary[category] = {
        "entity_count": len(cat_entities),
        "field_count": cat_fields,
        "entities": cat_entities,
    }

unassigned = [e["entity_name"] for e in entities if e["entity_name"] not in assigned]
if unassigned:
    category_summary["Uncategorized"] = {
        "entity_count": len(unassigned),
        "field_count": sum(e["field_count"] for e in entities if e["entity_name"] in unassigned),
        "entities": unassigned,
    }

# Top entities by field count
top_entities = sorted(entities, key=lambda e: e["field_count"], reverse=True)[:20]

summary = {
    "total_entities": total_entities,
    "total_fields": total_fields,
    "fields_with_description": fields_with_desc,
    "fields_with_description_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
    "fields_with_type": fields_with_type,
    "fields_with_type_pct": round(fields_with_type / total_fields * 100, 1) if total_fields else 0,
    "fields_with_example": fields_with_example,
    "fields_with_example_pct": round(fields_with_example / total_fields * 100, 1) if total_fields else 0,
    "fields_with_nullable_info": fields_with_nullable,
    "custom_only_entities": custom_only_entities,
    "entities_with_custom_fields": entities_with_custom,
    "data_type_distribution": dict(type_counts.most_common()),
    "category_summary": category_summary,
    "top_20_entities_by_field_count": [
        {"entity": e["entity_name"], "fields": e["field_count"]} for e in top_entities
    ],
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Total entities: {total_entities}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['fields_with_description_pct']}%)")
print(f"Fields with types: {fields_with_type} ({summary['fields_with_type_pct']}%)")
print(f"Fields with examples: {fields_with_example} ({summary['fields_with_example_pct']}%)")
print(f"Fields with nullable info: {fields_with_nullable}")
print(f"\nCustom-only entities (agency-configurable): {custom_only_entities}")
print(f"Entities with custom fields: {entities_with_custom}")
print(f"\nData type distribution:")
for t, c in type_counts.most_common():
    print(f"  {t}: {c}")
print(f"\nCategory summary:")
for cat, info in category_summary.items():
    print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
print(f"\nTop 20 entities by field count:")
for e in top_entities:
    print(f"  {e['entity_name']}: {e['field_count']} fields")
