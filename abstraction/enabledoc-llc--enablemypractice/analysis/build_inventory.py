#!/usr/bin/env python3
"""Build entity-inventory-full.json and entity-inventory-summary.json from 
the enrichment data dictionary, with verification against PDF text.

Uses downloads/enrichment/data-dictionary.json as the parsed source (verified
against pdftotext output in analysis/pdf-text.txt).
"""

import json
from pathlib import Path

BASE = Path(__file__).parent.parent
ENRICHMENT = BASE / "downloads" / "enrichment" / "data-dictionary.json"
OUT_DIR = Path(__file__).parent

def main():
    d = json.load(open(ENRICHMENT))
    
    entities = d["excelEntities"]
    value_sets = d["valueSets"]
    
    # Build full inventory
    inventory_entities = []
    for e in entities:
        fields = []
        for f in e["fields"]:
            field = {
                "name": f["name"],
                "description": f.get("description"),
                "requirement": f.get("required", "").lower() if f.get("required") else None,
                "type": f.get("dataType"),
            }
            # Add optional fields if present
            if f.get("valueSet"):
                field["value_set"] = f["valueSet"]
            if f.get("reference"):
                field["reference"] = f["reference"]
            fields.append(field)
        
        inventory_entities.append({
            "entity": e["name"],
            "field_count": len(fields),
            "fields": fields
        })
    
    full_inventory = {
        "product": "Enablemypractice",
        "version": "EHR 5.0",
        "developer": "EnableDoc LLC",
        "source_document": "Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf",
        "source_url": "https://www.enabledoc.com/wp-content/uploads/2023/11/Enabledoc-Exporting-Data-Guide-2023-updated-11202023.pdf",
        "entities": inventory_entities,
        "value_sets": value_sets,
        "export_formats": d.get("exportFormats", []),
        "excel_tab_names": d.get("excelTabNames", [])
    }
    
    # Write full inventory
    full_path = OUT_DIR / "entity-inventory-full.json"
    with open(full_path, "w") as f:
        json.dump(full_inventory, f, indent=2)
    
    # Build summary
    total_fields = sum(e["field_count"] for e in inventory_entities)
    fields_with_desc = sum(
        1 for e in inventory_entities for f in e["fields"]
        if f.get("description") and len(f["description"].strip()) > 0
    )
    fields_with_types = sum(
        1 for e in inventory_entities for f in e["fields"]
        if f.get("type") and f["type"] not in ("unknown", "")
    )
    fields_with_req = sum(
        1 for e in inventory_entities for f in e["fields"]
        if f.get("requirement")
    )
    fields_with_vs = sum(
        1 for e in inventory_entities for f in e["fields"]
        if f.get("value_set")
    )
    fields_with_ref = sum(
        1 for e in inventory_entities for f in e["fields"]
        if f.get("reference")
    )
    
    # Categories
    admin_names = ["Organization", "Patient", "Location", "Practitioner"]
    clinical_names = ["Encounter Data", "Procedure", "Service Request", 
                      "Family Member History", "Immunization", "AllergyIntolerance",
                      "Care Plan", "Observation"]
    med_names = ["Medication Administration", "MedicationRequest", "Medication Statement"]
    
    categories = {}
    for cat_name, cat_entities in [("Administrative", admin_names), 
                                     ("Clinical", clinical_names),
                                     ("Medication", med_names)]:
        matching = [e for e in inventory_entities if e["entity"] in cat_entities]
        categories[cat_name] = {
            "entity_count": len(matching),
            "entities": [e["entity"] for e in matching],
            "field_count": sum(e["field_count"] for e in matching)
        }
    
    summary = {
        "total_entities_with_field_definitions": len(inventory_entities),
        "total_excel_tabs_listed": len(d.get("excelTabNames", [])),
        "excel_tabs_listed": d.get("excelTabNames", []),
        "tabs_without_field_definitions": ["Condition", "Coverage"],
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_types,
        "fields_with_requirements": fields_with_req,
        "fields_with_value_sets": fields_with_vs,
        "fields_with_references": fields_with_ref,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1),
        "type_coverage_pct": round(fields_with_types / total_fields * 100, 1),
        "categories": categories,
        "value_sets_count": len(value_sets),
        "total_value_set_entries": sum(len(vs.get("values", [])) for vs in value_sets),
        "export_formats": [
            {"name": "C-CDA Files", "standard": "USCDI v1 / HL7 CDA R2"},
            {"name": "Excel File", "standard": "FHIR-influenced tabular format, 15 tabs"},
            {"name": "Notes", "format": "PDF files in ZIP archives by patient"},
            {"name": "Attachments", "format": "Mixed files in ZIP archives by patient"}
        ],
        "entity_table": []
    }
    
    for e in inventory_entities:
        desc_count = sum(1 for f in e["fields"] if f.get("description") and len(f["description"].strip()) > 0)
        type_count = sum(1 for f in e["fields"] if f.get("type") and f["type"] not in ("unknown", ""))
        summary["entity_table"].append({
            "entity": e["entity"],
            "fields": e["field_count"],
            "with_descriptions": desc_count,
            "with_types": type_count,
        })
    
    summary_path = OUT_DIR / "entity-inventory-summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Entities with field definitions: {len(inventory_entities)}")
    print(f"Excel tabs listed: {len(d.get('excelTabNames', []))}")
    print(f"Tabs without definitions: Condition, Coverage")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({round(fields_with_desc/total_fields*100,1)}%)")
    print(f"Fields with types: {fields_with_types} ({round(fields_with_types/total_fields*100,1)}%)")
    print(f"Fields with requirements: {fields_with_req}")
    print(f"Value sets: {len(value_sets)} with {sum(len(vs.get('values',[])) for vs in value_sets)} entries")
    print()
    print(f"{'Entity':<30} {'Fields':>6} {'Desc':>6} {'Types':>6}")
    print("-" * 55)
    for e in inventory_entities:
        desc_count = sum(1 for f in e["fields"] if f.get("description") and len(f["description"].strip()) > 0)
        type_count = sum(1 for f in e["fields"] if f.get("type") and f["type"] not in ("unknown", ""))
        print(f"{e['entity']:<30} {e['field_count']:>6} {desc_count:>6} {type_count:>6}")
    print("-" * 55)
    print(f"{'TOTAL':<30} {total_fields:>6} {fields_with_desc:>6} {fields_with_types:>6}")
    
    print(f"\nWritten: {full_path}")
    print(f"Written: {summary_path}")


if __name__ == "__main__":
    main()
