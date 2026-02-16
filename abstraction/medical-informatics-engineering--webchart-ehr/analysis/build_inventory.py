#!/usr/bin/env python3
"""
Build the definitive full-entity-inventory.json for WebChart EHR EHI export.

Combines:
  1. DRS data dictionary (99 objects with table-level descriptions)
  2. Sample export JSON (field-level detail for populated entities)
  3. Enrichment schema (field names/types for all sample entities)

Output: full-entity-inventory.json with every entity and every field.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/medical-informatics-engineering--webchart-ehr/downloads")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/medical-informatics-engineering--webchart-ehr/analysis")

def categorize_entity(name):
    """Assign a category to each entity."""
    n = name.lower()
    if n == 'patients' or n.startswith('patient_') or n.startswith('pat_pat_'):
        if any(x in n for x in ['condition', 'procedure']):
            return "Conditions & Procedures"
        if any(x in n for x in ['clinical_restriction', 'respirator', 'panel_status', 'targets']):
            return "Occupational Health"
        if any(x in n for x in ['warning']):
            return "Clinical Alerts"
        return "Demographics & Patient"
    if n.startswith('encounter') or n == 'encounters_link':
        return "Encounters"
    if n.startswith('rxlist') or n.startswith('escript'):
        return "Medications & Prescriptions"
    if any(x in n for x in ['document', 'dictation', 'storage_type']):
        return "Documents & Imaging"
    if n.startswith('dicom'):
        return "Documents & Imaging"
    if any(x in n for x in ['order_', 'lab_request']):
        return "Orders & Labs"
    if n.startswith('observation') or n == 'observations_snomed':
        return "Observations & Results"
    if any(x in n for x in ['incident', 'accommodation', 'body_part_type',
                             'nature_of_injury', 'clinical_restriction_type']):
        return "Occupational Health"
    if any(x in n for x in ['audio', 'pft']):
        return "Occupational Health"
    if n.startswith('panel'):
        return "Health Surveillance"
    if n.startswith('insurance') or n == 'insurance_pre_cert':
        return "Insurance"
    if any(x in n for x in ['appointment', 'apt_type', 'multi_referrer', 'multi_resource', 'multi_type']):
        return "Appointments"
    if n == 'injections':
        return "Immunizations"
    if any(x in n for x in ['task', 'conversation', 'extended_value_names']):
        return "Tasks & Messaging"
    if any(x in n for x in ['user', 'location', 'relation_type', 'coding_link']):
        return "Reference & Lookup"
    if n == 'audit_log_chart':
        return "Audit"
    return "Other"

def infer_field_type(value):
    """Infer data type from sample value."""
    if value is None:
        return "null"
    s = str(value)
    if s == "":
        return "string"
    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', s):
        return "datetime"
    if re.match(r'^\d{4}-\d{2}-\d{2}$', s):
        return "date"
    if re.match(r'^-?\d+$', s):
        return "integer"
    if re.match(r'^-?\d+\.\d+$', s):
        return "decimal"
    if len(s) > 500 and re.match(r'^[A-Za-z0-9+/=\s]+$', s[:200]):
        return "base64"
    return "string"

def extract_fields(record):
    """Extract field definitions from a sample record, separating scalar from nested."""
    scalar_fields = []
    nested_arrays = []
    for key in sorted(record.keys()):
        value = record[key]
        if isinstance(value, list):
            entity_name = key.split('.')[0]
            nested_arrays.append({
                "array_key": key,
                "entity_name": entity_name,
                "record_count": len(value),
            })
        elif isinstance(value, dict):
            scalar_fields.append({
                "name": key,
                "inferred_type": "embedded_reference",
                "description": None,
                "sample_value": f"<embedded user object, {len(value)} fields>",
            })
        else:
            sample = str(value) if value is not None else None
            if sample and len(sample) > 200:
                sample = sample[:100] + f"... ({len(str(value))} chars total)"
            scalar_fields.append({
                "name": key,
                "inferred_type": infer_field_type(value),
                "description": None,
                "sample_value": sample,
            })
    return scalar_fields, nested_arrays

def main():
    # Load sources
    with open(RESULTS_DIR / "enrichment" / "drs-data-dictionary.json") as f:
        drs_objects = json.load(f)
    with open(RESULTS_DIR / "sample-single-patient-export.json") as f:
        sample = json.load(f)

    drs_lookup = {obj["object_name"]: obj["description"] for obj in drs_objects}
    patient = sample["db"][0]

    # Separate patient fields from nested arrays
    patient_scalars = {k: v for k, v in patient.items() if not isinstance(v, list)}
    patient_arrays = {k: v for k, v in patient.items() if isinstance(v, list)}

    entities = []
    all_entity_names = set()

    # 1. patients entity (top-level)
    p_fields, p_nested = extract_fields(patient)
    entities.append({
        "entity_name": "patients",
        "description": drs_lookup.get("patients", ""),
        "category": "Demographics & Patient",
        "in_drs_table": True,
        "in_sample_export": True,
        "field_count": len(p_fields),
        "fields_with_descriptions": 0,
        "nested_entity_count": len(p_nested),
        "record_count_in_sample": 1,
        "fields": p_fields,
        "nested_entities": [n["array_key"] for n in p_nested],
    })
    all_entity_names.add("patients")

    # 2. All nested array entities from sample
    seen_entities = {}  # entity_name -> best record
    for array_key, array_value in sorted(patient_arrays.items()):
        entity_name = array_key.split(".")
        ename = entity_name[0]
        fk = entity_name[1] if len(entity_name) > 1 else None

        if array_value and isinstance(array_value[0], dict):
            record = array_value[0]
            s_fields, s_nested = extract_fields(record)

            if ename not in seen_entities or len(s_fields) > seen_entities[ename]["field_count"]:
                seen_entities[ename] = {
                    "entity_name": ename,
                    "description": drs_lookup.get(ename, ""),
                    "category": categorize_entity(ename),
                    "in_drs_table": ename in drs_lookup,
                    "in_sample_export": True,
                    "foreign_keys_observed": [],
                    "field_count": len(s_fields),
                    "fields_with_descriptions": 0,
                    "nested_entity_count": len(s_nested),
                    "record_count_in_sample": len(array_value),
                    "fields": s_fields,
                    "nested_entities": [n["array_key"] for n in s_nested],
                }
            seen_entities[ename]["foreign_keys_observed"].append(fk)
        else:
            if ename not in seen_entities:
                seen_entities[ename] = {
                    "entity_name": ename,
                    "description": drs_lookup.get(ename, ""),
                    "category": categorize_entity(ename),
                    "in_drs_table": ename in drs_lookup,
                    "in_sample_export": True,
                    "foreign_keys_observed": [],
                    "field_count": 0,
                    "fields_with_descriptions": 0,
                    "nested_entity_count": 0,
                    "record_count_in_sample": 0,
                    "fields": [],
                    "nested_entities": [],
                }
            if ename in seen_entities:
                seen_entities[ename]["foreign_keys_observed"].append(fk)

        all_entity_names.add(ename)

    # Also check nested entities within documents
    if patient_arrays.get("documents.pat_id"):
        doc = patient_arrays["documents.pat_id"][0]
        for k, v in doc.items():
            if isinstance(v, list):
                sub_ename = k.split(".")[0]
                if sub_ename not in seen_entities:
                    seen_entities[sub_ename] = {
                        "entity_name": sub_ename,
                        "description": drs_lookup.get(sub_ename, ""),
                        "category": categorize_entity(sub_ename),
                        "in_drs_table": sub_ename in drs_lookup,
                        "in_sample_export": True,
                        "foreign_keys_observed": [k.split(".")[1] if "." in k else None],
                        "field_count": 0,
                        "fields_with_descriptions": 0,
                        "nested_entity_count": 0,
                        "record_count_in_sample": 0,
                        "fields": [],
                        "nested_entities": [],
                        "note": "Nested within documents entity; empty in sample",
                    }
                    all_entity_names.add(sub_ename)

    for ename in sorted(seen_entities.keys()):
        entities.append(seen_entities[ename])

    # 3. DRS objects not in sample
    for obj in drs_objects:
        name = obj["object_name"]
        if name not in all_entity_names:
            entities.append({
                "entity_name": name,
                "description": obj["description"],
                "category": categorize_entity(name),
                "in_drs_table": True,
                "in_sample_export": False,
                "field_count": 0,
                "fields_with_descriptions": 0,
                "record_count_in_sample": 0,
                "fields": [],
                "note": "Listed in DRS table but not present in sample export",
            })

    # Sort entities by category then name
    entities.sort(key=lambda e: (e["category"], e["entity_name"]))

    # Compute summary statistics
    total_entities = len(entities)
    total_fields = sum(e["field_count"] for e in entities)
    in_drs = sum(1 for e in entities if e.get("in_drs_table"))
    in_sample = sum(1 for e in entities if e.get("in_sample_export"))
    with_desc = sum(1 for e in entities if e.get("description"))
    without_desc = sum(1 for e in entities if not e.get("description"))
    with_data = sum(1 for e in entities if e.get("record_count_in_sample", 0) > 0)

    categories = defaultdict(lambda: {"entities": 0, "fields": 0, "with_descriptions": 0, "entity_names": []})
    for e in entities:
        cat = e["category"]
        categories[cat]["entities"] += 1
        categories[cat]["fields"] += e["field_count"]
        if e.get("description"):
            categories[cat]["with_descriptions"] += 1
        categories[cat]["entity_names"].append(e["entity_name"])

    summary = {
        "total_entities": total_entities,
        "entities_in_drs_table": in_drs,
        "entities_in_sample_export": in_sample,
        "entities_with_populated_data": with_data,
        "entities_with_description": with_desc,
        "entities_without_description": without_desc,
        "total_fields_observed": total_fields,
        "fields_with_vendor_descriptions": 0,
        "patient_scalar_fields": len(p_fields),
        "category_breakdown": {k: dict(v) for k, v in sorted(categories.items())},
        "sample_export_stats": {
            "format": "JSON",
            "file_size_bytes": 482271,
            "test_patient": "William S. Hart (pat_id 18)",
            "top_level_keys": ["request", "documentation", "db", "meta"],
            "request_pattern": "db/patients/{pat_id}/drs",
        },
        "drs_table_stats": {
            "total_objects": 99,
            "with_descriptions": 81,
            "without_descriptions": 18,
        },
    }

    # Write outputs
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(entities, f, indent=2)

    with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"=== WebChart EHR EHI Export Inventory ===")
    print(f"Total unique entities: {total_entities}")
    print(f"  In DRS table: {in_drs}")
    print(f"  In sample export: {in_sample}")
    print(f"  With populated data: {with_data}")
    print(f"  With descriptions: {with_desc}")
    print(f"  Without descriptions: {without_desc}")
    print(f"Total fields observed: {total_fields}")
    print(f"Fields with vendor descriptions: 0 (table-level only)")
    print()
    print("Category breakdown:")
    for cat in sorted(categories.keys()):
        c = categories[cat]
        print(f"  {cat}: {c['entities']} entities, {c['fields']} fields, {c['with_descriptions']} described")
    print()
    print("Top entities by field count:")
    top = sorted(entities, key=lambda e: e["field_count"], reverse=True)[:15]
    for e in top:
        desc_flag = "✓" if e.get("description") else "✗"
        data_flag = "✓" if e.get("record_count_in_sample", 0) > 0 else "✗"
        print(f"  {e['entity_name']:40s} {e['field_count']:4d} fields  desc:{desc_flag}  data:{data_flag}  [{e['category']}]")

if __name__ == "__main__":
    main()
