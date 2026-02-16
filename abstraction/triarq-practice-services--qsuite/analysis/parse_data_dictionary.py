#!/usr/bin/env python3
"""
Parse the TRIARQ QSuite EHI export data dictionary (extracted from the Angular JS bundle)
and produce:
  1. full-entity-inventory.json — complete machine-readable extraction
  2. summary-stats.json — aggregate statistics for analysis.md
"""
import json
import re
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent.parent.parent / "results" / "triarq-practice-services--qsuite"
DATA_DICT = RESULTS_DIR / "downloads" / "enrichment" / "data-dictionary.json"
OUTPUT_DIR = Path(__file__).resolve().parent

def is_trivial_description(name: str, desc: str) -> bool:
    """Check if description is just a reformatting of the field name."""
    if not desc:
        return True
    norm_desc = desc.lower().strip()
    norm_name = name.lower().strip()
    # CamelCase expansion: "PatientID" -> "patient id"
    expanded = re.sub(r'([a-z])([A-Z])', r'\1 \2', name).lower()
    # Replace common suffixes
    expanded2 = expanded.replace(' i d', ' identifier').replace(' id', ' identifier')
    # Normalize spaces
    if norm_desc.replace(' ', '') == norm_name.replace(' ', ''):
        return True
    if norm_desc == expanded:
        return True
    if norm_desc == expanded2:
        return True
    # "NDCCode" -> "NDC Code" -> "ndc code"
    spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    spaced = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', spaced)
    if norm_desc == spaced.lower():
        return True
    return False

def main():
    with open(DATA_DICT) as f:
        data = json.load(f)

    entities = data.get("csvEntities", [])
    export_file_types = data.get("exportFileTypes", [])

    # Build full inventory
    inventory = {
        "source": data.get("source"),
        "product": data.get("product"),
        "developer": data.get("developer"),
        "extraction_date": data.get("extractionDate"),
        "summary_description": data.get("summary", {}).get("description"),
        "entities": [],
        "non_csv_exports": [],
    }

    total_fields = 0
    total_with_desc = 0
    total_trivial_desc = 0
    total_with_type = 0
    type_counts = {}
    category_stats = {}  # We'll try to categorize by domain

    for entity in entities:
        module = entity.get("module", "")
        fields = entity.get("fields", [])
        entity_record = {
            "name": module,
            "description": entity.get("description", ""),
            "resource_id": entity.get("resourceId"),
            "field_count": len(fields),
            "fields": [],
        }

        for field in fields:
            fname = field.get("name", "")
            fdesc = field.get("description", "")
            ftype = field.get("type", "")
            trivial = is_trivial_description(fname, fdesc)

            field_record = {
                "name": fname,
                "description": fdesc,
                "type": ftype,
                "description_is_trivial": trivial,
            }
            entity_record["fields"].append(field_record)

            total_fields += 1
            if fdesc:
                total_with_desc += 1
            if trivial:
                total_trivial_desc += 1
            if ftype:
                total_with_type += 1
                norm_type = ftype.lower()
                type_counts[norm_type] = type_counts.get(norm_type, 0) + 1

        inventory["entities"].append(entity_record)

    # Non-CSV exports
    for ft in export_file_types:
        inventory["non_csv_exports"].append({
            "format": ft.get("format", ""),
            "category": ft.get("category", ""),
            "document_types": ft.get("documentTypes", []),
        })

    # Compute summary stats
    entities_with_fields = [e for e in inventory["entities"] if e["field_count"] > 0]
    entities_without_fields = [e for e in inventory["entities"] if e["field_count"] == 0]

    non_csv_doc_count = sum(len(nc["document_types"]) for nc in inventory["non_csv_exports"])

    summary = {
        "total_csv_entities": len(inventory["entities"]),
        "entities_with_fields": len(entities_with_fields),
        "entities_without_fields": len(entities_without_fields),
        "entities_without_fields_names": [e["name"] for e in entities_without_fields],
        "total_fields": total_fields,
        "fields_with_any_description": total_with_desc,
        "fields_with_trivial_description": total_trivial_desc,
        "fields_with_meaningful_description": total_with_desc - total_trivial_desc,
        "pct_with_any_description": round(total_with_desc / total_fields * 100, 1) if total_fields else 0,
        "pct_with_meaningful_description": round((total_with_desc - total_trivial_desc) / total_fields * 100, 1) if total_fields else 0,
        "fields_with_type": total_with_type,
        "type_distribution": type_counts,
        "non_csv_format_categories": len(inventory["non_csv_exports"]),
        "non_csv_document_types": non_csv_doc_count,
        "entities_by_size": sorted(
            [{"name": e["name"], "fields": e["field_count"]} for e in inventory["entities"]],
            key=lambda x: x["fields"],
            reverse=True,
        ),
        "has_foreign_keys": False,
        "has_value_sets": False,
        "has_sample_data": False,
        "has_relationships": False,
    }

    # Write outputs
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote full-entity-inventory.json ({len(inventory['entities'])} entities, {total_fields} fields)")

    with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote summary-stats.json")

    # Print summary to stdout
    print(f"\n=== Summary ===")
    print(f"CSV entities: {summary['total_csv_entities']} ({summary['entities_with_fields']} with fields)")
    print(f"Total fields: {summary['total_fields']}")
    print(f"Fields with any description: {summary['fields_with_any_description']} ({summary['pct_with_any_description']}%)")
    print(f"Fields with meaningful description: {summary['fields_with_meaningful_description']} ({summary['pct_with_meaningful_description']}%)")
    print(f"Type distribution: {summary['type_distribution']}")
    print(f"Non-CSV exports: {summary['non_csv_format_categories']} categories, {summary['non_csv_document_types']} document types")
    print(f"\nTop 10 entities by field count:")
    for e in summary['entities_by_size'][:10]:
        print(f"  {e['name']}: {e['fields']} fields")

if __name__ == "__main__":
    main()
