#!/usr/bin/env python3
"""Parse WebChart EHR EHI export artifacts to produce entity-inventory-full.json and summary."""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

DOWNLOADS = Path(__file__).parent.parent / "downloads"


def parse_drs_table(md_text: str) -> list[dict]:
    """Parse the DRS content table from the markdown."""
    objects = []
    # Find the table between "## Designated Record Set Content" and the next ##
    in_table = False
    for line in md_text.splitlines():
        if "<td>" in line and not "<strong>" in line:
            if not in_table:
                in_table = True
                current_name = line.strip().replace("<td>", "").replace("</td>", "").strip()
            else:
                current_desc = line.strip().replace("<td>", "").replace("</td>", "").strip()
                objects.append({
                    "object_name": current_name,
                    "description": current_desc
                })
                in_table = False
    return objects


def infer_field_type(value) -> str:
    """Infer a field type from a sample value."""
    if value is None:
        return "unknown"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, list):
        return "array"
    s = str(value)
    if re.match(r'^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$', s):
        return "datetime"
    if re.match(r'^\d+$', s):
        return "integer_string"
    return "string"


def extract_fields_from_records(records: list[dict], obj_name: str) -> list[dict]:
    """Extract field inventory from a list of records."""
    all_fields = {}
    for record in records:
        if not isinstance(record, dict):
            continue
        for key, value in record.items():
            if key not in all_fields:
                field_type = infer_field_type(value)
                sample = value
                if isinstance(value, (dict, list)):
                    sample = None  # skip complex nested for sample
                elif isinstance(value, str) and len(value) > 200:
                    sample = value[:200] + "..."
                all_fields[key] = {
                    "field_name": key,
                    "type": field_type,
                    "sample_value": str(sample) if sample is not None else None,
                    "is_nested_object": isinstance(value, (dict, list))
                }
            else:
                # Update type if we have a non-null value and current is unknown
                if all_fields[key]["type"] == "unknown" and value is not None:
                    all_fields[key]["type"] = infer_field_type(value)
                    if not isinstance(value, (dict, list)):
                        sv = value
                        if isinstance(sv, str) and len(sv) > 200:
                            sv = sv[:200] + "..."
                        all_fields[key]["sample_value"] = str(sv)
    return list(all_fields.values())


def categorize_object(name: str, description: str) -> str:
    """Assign a category based on object name and description."""
    name_lower = name.lower()
    desc_lower = description.lower()

    # Occupational health
    occ_keywords = ["occupational", "workplace", "employee", "respirator", "audiogram",
                     "pft", "pulmonary", "panel", "surveillance", "decertif",
                     "accommodation", "restriction", "incident", "injury",
                     "body_part", "nature_of_injury"]
    if any(k in name_lower or k in desc_lower for k in occ_keywords):
        return "Occupational Health"

    # Demographics / Patient
    if name_lower in ["patients", "patient_mrns", "patient_extended_values",
                       "patient_extended_index", "patient_partitions",
                       "patient_additional_info", "patient_targets",
                       "pat_pat_relations", "pat_pat_relflat", "relation_types",
                       "user_patients", "users", "locations"]:
        return "Demographics & Administration"

    # Encounters
    if "encounter" in name_lower:
        return "Encounters"

    # Documents
    if "document" in name_lower or "dictation" in name_lower or "storage_types" in name_lower:
        return "Documents & Dictation"

    # Medications / Prescriptions
    if "rxlist" in name_lower or "escript" in name_lower:
        return "Medications & Prescriptions"

    # Orders / Labs
    if "order" in name_lower or "lab_request" in name_lower:
        return "Orders & Lab Results"

    # Observations / Results
    if "observation" in name_lower:
        return "Observations & Results"

    # Conditions / Problems
    if "condition" in name_lower or "procedure" in name_lower:
        return "Conditions & Procedures"

    # Insurance
    if "insurance" in name_lower:
        return "Insurance & Coverage"

    # Appointments / Scheduling
    if "appoint" in name_lower or "apt" in name_lower:
        return "Scheduling"

    # Imaging
    if "dicom" in name_lower:
        return "Imaging (DICOM)"

    # Communications
    if "conversation" in name_lower or "task" in name_lower:
        return "Communications & Tasks"

    # Warnings
    if "warning" in name_lower:
        return "Clinical Alerts"

    # Audit
    if "audit" in name_lower:
        return "Audit"

    # Coding
    if "coding" in name_lower:
        return "Coding & Terminology"

    return "Other"


def main():
    # 1. Parse DRS table from markdown
    md_text = (DOWNLOADS / "ehi-export-technical-details.md").read_text()
    drs_objects = parse_drs_table(md_text)
    print(f"Parsed {len(drs_objects)} DRS objects from markdown table")

    # 2. Load sample export
    with open(DOWNLOADS / "sample-single-patient-export.json") as f:
        sample = json.load(f)

    patient = sample["db"][0]

    # 3. Build entity inventory
    # DRS table gives us object names + descriptions
    # Sample export gives us field-level detail
    drs_lookup = {o["object_name"]: o["description"] for o in drs_objects}

    entities = []

    # Patient scalar fields (the 'patients' entity)
    patient_scalar = {}
    patient_nested = {}
    for k, v in patient.items():
        if isinstance(v, list):
            patient_nested[k] = v
        elif isinstance(v, dict):
            # revised_by is a nested user object
            patient_nested[k] = [v]
        else:
            patient_scalar[k] = v

    # Add 'patients' entity
    patient_fields = extract_fields_from_records([patient_scalar], "patients")
    entities.append({
        "entity_name": "patients",
        "description": drs_lookup.get("patients", ""),
        "category": "Demographics & Administration",
        "field_count": len(patient_fields),
        "record_count_in_sample": 1,
        "fields": patient_fields,
        "source": "drs_table+sample_export"
    })

    # Process nested arrays from sample
    sample_obj_names = set()
    for key, records in patient_nested.items():
        # Key format is like "encounters.pat_id" - extract object name
        obj_name = key.split(".")[0]
        sample_obj_names.add(obj_name)

        # If we already have this entity, merge fields
        existing = next((e for e in entities if e["entity_name"] == obj_name), None)
        if existing:
            # Merge records
            if isinstance(records, list):
                new_fields = extract_fields_from_records(records, obj_name)
                existing_names = {f["field_name"] for f in existing["fields"]}
                for f in new_fields:
                    if f["field_name"] not in existing_names:
                        existing["fields"].append(f)
                        existing_names.add(f["field_name"])
                existing["field_count"] = len(existing["fields"])
                existing["record_count_in_sample"] = max(
                    existing["record_count_in_sample"],
                    len(records) if isinstance(records, list) else 1
                )
        else:
            fields = extract_fields_from_records(records, obj_name) if isinstance(records, list) else extract_fields_from_records(records, obj_name)
            desc = drs_lookup.get(obj_name, "")
            entities.append({
                "entity_name": obj_name,
                "description": desc,
                "category": categorize_object(obj_name, desc),
                "field_count": len(fields),
                "record_count_in_sample": len(records) if isinstance(records, list) else 1,
                "fields": fields,
                "source": "drs_table+sample_export" if obj_name in drs_lookup else "sample_export_only"
            })

    # Add DRS objects that are NOT in the sample export (no field info)
    for obj in drs_objects:
        name = obj["object_name"]
        if name == "patients":
            continue
        if not any(e["entity_name"] == name for e in entities):
            desc = obj["description"]
            entities.append({
                "entity_name": name,
                "description": desc,
                "category": categorize_object(name, desc),
                "field_count": 0,
                "record_count_in_sample": 0,
                "fields": [],
                "source": "drs_table_only"
            })

    # Sort by category then name
    entities.sort(key=lambda e: (e["category"], e["entity_name"]))

    # 4. Compute summary statistics
    total_entities = len(entities)
    total_fields = sum(e["field_count"] for e in entities)
    entities_with_fields = sum(1 for e in entities if e["field_count"] > 0)
    entities_without_fields = sum(1 for e in entities if e["field_count"] == 0)
    entities_with_desc = sum(1 for e in entities if e["description"])
    entities_without_desc = sum(1 for e in entities if not e["description"])

    # Category breakdown
    categories = defaultdict(lambda: {"entity_count": 0, "field_count": 0, "entities": []})
    for e in entities:
        cat = e["category"]
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += e["field_count"]
        categories[cat]["entities"].append(e["entity_name"])

    # Entities with sample data
    entities_with_data = sum(1 for e in entities if e["record_count_in_sample"] > 0)

    # 5. Save full inventory
    output_dir = Path(__file__).parent
    with open(output_dir / "entity-inventory-full.json", "w") as f:
        json.dump({
            "product": "WebChart EHR",
            "vendor": "Medical Informatics Engineering",
            "export_format": "JSON",
            "total_entities": total_entities,
            "total_fields": total_fields,
            "entities": entities
        }, f, indent=2)

    # 6. Save summary
    summary = {
        "product": "WebChart EHR",
        "vendor": "Medical Informatics Engineering",
        "export_format": "JSON (single file per patient)",
        "total_entities": total_entities,
        "total_fields": total_fields,
        "entities_with_field_detail": entities_with_fields,
        "entities_without_field_detail": entities_without_fields,
        "entities_with_description": entities_with_desc,
        "entities_without_description": entities_without_desc,
        "entities_with_sample_data": entities_with_data,
        "category_breakdown": {
            cat: {
                "entity_count": info["entity_count"],
                "field_count": info["field_count"],
                "entities": info["entities"]
            }
            for cat, info in sorted(categories.items())
        },
        "top_entities_by_field_count": [
            {"entity": e["entity_name"], "fields": e["field_count"], "category": e["category"]}
            for e in sorted(entities, key=lambda x: -x["field_count"])[:20]
        ]
    }
    with open(output_dir / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"\n=== SUMMARY ===")
    print(f"Total entities: {total_entities}")
    print(f"Total fields (from sample): {total_fields}")
    print(f"Entities with field detail: {entities_with_fields}")
    print(f"Entities without field detail (DRS table only): {entities_without_fields}")
    print(f"Entities with description: {entities_with_desc}")
    print(f"Entities without description: {entities_without_desc}")
    print(f"Entities with sample data: {entities_with_data}")
    print(f"\n--- Category Breakdown ---")
    for cat in sorted(categories.keys()):
        info = categories[cat]
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
    print(f"\n--- Top 20 entities by field count ---")
    for e in sorted(entities, key=lambda x: -x["field_count"])[:20]:
        print(f"  {e['entity_name']}: {e['field_count']} fields ({e['category']})")


if __name__ == "__main__":
    main()
