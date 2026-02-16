#!/usr/bin/env python3
"""
Parse the WebChart EHR EHI export artifacts to produce a full entity inventory.

Inputs:
  - downloads/enrichment/drs-data-dictionary.json (99 DRS objects with descriptions)
  - downloads/sample-single-patient-export.json (sample single-patient export)
  - downloads/ehi-export-technical-details.md (raw markdown source)

Outputs:
  - full-entity-inventory.json (complete field-level extraction)
  - summary-stats.json (aggregate statistics)
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/medical-informatics-engineering--webchart-ehr/downloads")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/medical-informatics-engineering--webchart-ehr/analysis")

def load_drs_dictionary():
    """Load the 99 DRS objects from the pre-extracted dictionary."""
    with open(RESULTS_DIR / "enrichment" / "drs-data-dictionary.json") as f:
        return json.load(f)

def load_sample_export():
    """Load the sample single-patient JSON export."""
    with open(RESULTS_DIR / "sample-single-patient-export.json") as f:
        return json.load(f)

def infer_type(value):
    """Infer the likely data type from a sample value."""
    if isinstance(value, dict):
        return "object (embedded reference)"
    if isinstance(value, list):
        return "array"
    if value is None:
        return "null"
    s = str(value)
    if s == "":
        return "string (empty)"
    # Date patterns
    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', s):
        return "datetime"
    if re.match(r'^\d{4}-\d{2}-\d{2}$', s):
        return "date"
    # Numeric
    if re.match(r'^-?\d+$', s):
        return "integer"
    if re.match(r'^-?\d+\.\d+$', s):
        return "decimal"
    # Base64 (long strings starting with common patterns)
    if len(s) > 200 and re.match(r'^[A-Za-z0-9+/=]+$', s[:100]):
        return "base64 (binary content)"
    return "string"

def categorize_entity(name, description):
    """Assign a category to each entity based on name and description."""
    name_lower = name.lower()
    desc_lower = (description or "").lower()
    
    if any(x in name_lower for x in ['patient_condition', 'coding_link']):
        return "Conditions & Diagnoses"
    if any(x in name_lower for x in ['rxlist', 'escript']):
        return "Medications & Prescriptions"
    if any(x in name_lower for x in ['encounter', 'visit_type']):
        return "Encounters"
    if any(x in name_lower for x in ['document', 'dictation', 'storage_type']):
        return "Documents & Imaging"
    if any(x in name_lower for x in ['dicom']):
        return "Documents & Imaging"
    if any(x in name_lower for x in ['order', 'lab_request']):
        return "Orders & Labs"
    if any(x in name_lower for x in ['observation']):
        return "Observations & Results"
    if any(x in name_lower for x in ['incident', 'accommodation', 'clinical_restriction',
                                       'body_part', 'nature_of_injury']):
        return "Occupational Health"
    if any(x in name_lower for x in ['audio', 'pft', 'respirator']):
        return "Occupational Health"
    if any(x in name_lower for x in ['panel']):
        return "Health Surveillance"
    if any(x in name_lower for x in ['insurance', 'pre_cert']):
        return "Insurance"
    if any(x in name_lower for x in ['appointment', 'apt_type', 'multi_referrer', 'multi_resource', 'multi_type']):
        return "Appointments"
    if any(x in name_lower for x in ['injection']):
        return "Immunizations"
    if any(x in name_lower for x in ['task', 'extended_value_names']):
        return "Tasks & Messaging"
    if any(x in name_lower for x in ['conversation']):
        return "Tasks & Messaging"
    if any(x in name_lower for x in ['patient', 'pat_pat_rel']):
        return "Demographics & Patient"
    if any(x in name_lower for x in ['user']):
        return "Users & References"
    if any(x in name_lower for x in ['location', 'relation_type']):
        return "Users & References"
    return "Other"

def extract_fields_from_record(record):
    """Extract field-level information from a sample record."""
    fields = []
    for key, value in sorted(record.items()):
        field = {
            "name": key,
            "inferred_type": infer_type(value),
            "sample_value": None,
            "is_nested_array": isinstance(value, list),
            "is_embedded_reference": isinstance(value, dict),
        }
        # Capture sample value (truncated for large content)
        if isinstance(value, dict):
            field["sample_value"] = f"<embedded object with {len(value)} fields>"
        elif isinstance(value, list):
            field["sample_value"] = f"<array with {len(value)} items>"
        elif isinstance(value, str) and len(value) > 200:
            field["sample_value"] = value[:100] + "..."
        else:
            field["sample_value"] = value
        fields.append(field)
    return fields

def main():
    drs_objects = load_drs_dictionary()
    sample = load_sample_export()
    patient = sample["db"][0]
    
    # Build lookup of DRS descriptions
    drs_lookup = {obj["object_name"]: obj["description"] for obj in drs_objects}
    
    # Extract patient scalar fields
    scalar_fields = {}
    array_fields = {}
    for key, value in patient.items():
        if isinstance(value, list):
            array_fields[key] = value
        else:
            scalar_fields[key] = value
    
    # Build the full entity inventory
    entities = []
    
    # 1. patients (top-level scalar fields)
    patient_fields = extract_fields_from_record(
        {k: v for k, v in patient.items() if not isinstance(v, list)}
    )
    entities.append({
        "entity_name": "patients",
        "description": drs_lookup.get("patients", ""),
        "category": "Demographics & Patient",
        "field_count": len(patient_fields),
        "fields_with_descriptions": 0,  # No field-level descriptions provided
        "has_types_documented": False,
        "has_sample_data": True,
        "record_count_in_sample": 1,
        "source": "sample export (top-level scalar fields)",
        "fields": patient_fields,
    })
    
    # 2. Nested array entities from sample export
    for array_key, array_value in sorted(array_fields.items()):
        # Parse entity name from key (format: "table_name.foreign_key")
        parts = array_key.split(".")
        entity_name = parts[0]
        fk_name = parts[1] if len(parts) > 1 else None
        
        # Get fields from first record if available
        fields = []
        if array_value and len(array_value) > 0:
            fields = extract_fields_from_record(array_value[0])
        
        entities.append({
            "entity_name": entity_name,
            "array_key": array_key,
            "foreign_key": fk_name,
            "description": drs_lookup.get(entity_name, ""),
            "category": categorize_entity(entity_name, drs_lookup.get(entity_name, "")),
            "field_count": len(fields),
            "fields_with_descriptions": 0,
            "has_types_documented": False,
            "has_sample_data": len(array_value) > 0,
            "record_count_in_sample": len(array_value),
            "source": "sample export (nested array)",
            "fields": fields,
        })
    
    # 3. DRS objects not found in sample (add them with no field info)
    sample_entity_names = set()
    sample_entity_names.add("patients")
    for key in array_fields:
        sample_entity_names.add(key.split(".")[0])
    
    for obj in drs_objects:
        name = obj["object_name"]
        if name not in sample_entity_names:
            entities.append({
                "entity_name": name,
                "description": obj["description"],
                "category": categorize_entity(name, obj["description"]),
                "field_count": 0,
                "fields_with_descriptions": 0,
                "has_types_documented": False,
                "has_sample_data": False,
                "record_count_in_sample": 0,
                "source": "DRS table only (not in sample export)",
                "fields": [],
            })
    
    # Deduplicate entities by name (keep the one with fields)
    seen = {}
    deduplicated = []
    for e in entities:
        name = e["entity_name"]
        if name not in seen or (e["field_count"] > seen[name]["field_count"]):
            seen[name] = e
    for e in entities:
        name = e["entity_name"]
        if seen[name] is e:
            deduplicated.append(e)
    entities = deduplicated
    
    # Compute summary statistics
    total_entities = len(entities)
    total_fields = sum(e["field_count"] for e in entities)
    entities_with_data = sum(1 for e in entities if e["has_sample_data"])
    entities_with_description = sum(1 for e in entities if e["description"])
    entities_without_description = sum(1 for e in entities if not e["description"])
    
    # Category breakdown
    categories = defaultdict(lambda: {"entities": 0, "fields": 0, "entity_names": []})
    for e in entities:
        cat = e["category"]
        categories[cat]["entities"] += 1
        categories[cat]["fields"] += e["field_count"]
        categories[cat]["entity_names"].append(e["entity_name"])
    
    # Top entities by field count
    top_entities = sorted(entities, key=lambda x: x["field_count"], reverse=True)[:20]
    
    summary = {
        "total_entities_in_drs": len(drs_objects),
        "total_entities_in_sample": len(sample_entity_names),
        "total_unique_entities": total_entities,
        "total_fields_observed": total_fields,
        "total_patient_scalar_fields": len(patient_fields),
        "entities_with_sample_data": entities_with_data,
        "entities_without_sample_data": total_entities - entities_with_data,
        "entities_with_description": entities_with_description,
        "entities_without_description": entities_without_description,
        "fields_with_descriptions": 0,  # No field-level descriptions in any source
        "category_breakdown": dict(categories),
        "top_20_entities_by_field_count": [
            {"name": e["entity_name"], "fields": e["field_count"], "category": e["category"]}
            for e in top_entities
        ],
        "entities_without_description_list": [
            e["entity_name"] for e in entities if not e["description"]
        ],
    }
    
    # Write outputs
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(entities, f, indent=2)
    
    with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Total unique entities: {total_entities}")
    print(f"Total fields observed (from sample data): {total_fields}")
    print(f"Patient scalar fields: {len(patient_fields)}")
    print(f"Entities with sample data: {entities_with_data}")
    print(f"Entities with descriptions: {entities_with_description}")
    print(f"Entities without descriptions: {entities_without_description}")
    print(f"\nCategory breakdown:")
    for cat in sorted(categories.keys()):
        c = categories[cat]
        print(f"  {cat}: {c['entities']} entities, {c['fields']} fields")
    print(f"\nTop 10 entities by field count:")
    for e in top_entities[:10]:
        print(f"  {e['entity_name']}: {e['field_count']} fields ({e['category']})")

if __name__ == "__main__":
    main()
