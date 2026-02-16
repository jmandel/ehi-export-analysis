#!/usr/bin/env python3
"""Parse the FHIR resources browser extract and produce a full entity inventory."""

import json
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.parent.parent / "results" / "medpharm-services-llc--intelligent-medical-software-ims"
DOWNLOADS = RESULTS_DIR / "downloads"
ENRICHMENT = DOWNLOADS / "enrichment"
OUTPUT_DIR = Path(__file__).parent

def load_fhir_resources():
    """Load and normalize the FHIR resources from the browser extract."""
    with open(ENRICHMENT / "fhir-resources.json") as f:
        data = json.load(f)
    return data

def build_inventory(resources):
    """Build a full entity inventory from FHIR resources."""
    inventory = {
        "source": "Meditab FHIR API Specification (browser-extracted from https://www.meditab.com/fhir/specifications)",
        "extraction_method": "Browser DevTools evaluation of rendered Duda SPA page",
        "resource_count": len(resources),
        "total_fields": sum(len(r.get("fields", [])) for r in resources),
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "entities": []
    }

    for r in resources:
        rt = r.get("resourceType", r.get("name", "unknown"))
        fields = r.get("fields", [])
        search_params = r.get("searchParams", [])
        description = r.get("description", "")

        entity = {
            "name": rt,
            "description": description,
            "field_count": len(fields),
            "search_param_count": len(search_params),
            "fields": [],
            "search_params": []
        }

        for field in fields:
            field_obj = {
                "name": field.get("name", ""),
                "type": field.get("dataType", field.get("type", "")),
                "description": field.get("description", ""),
                "required": field.get("required", field.get("Required/Optional", "")),
            }
            entity["fields"].append(field_obj)
            if field_obj["description"]:
                inventory["fields_with_descriptions"] += 1
            if field_obj["type"]:
                inventory["fields_with_types"] += 1

        for sp in search_params:
            entity["search_params"].append({
                "name": sp.get("name", ""),
                "type": sp.get("type", ""),
                "description": sp.get("description", ""),
            })

        inventory["entities"].append(entity)

    return inventory

def print_summary(inventory):
    """Print summary statistics."""
    print(f"=== FHIR Resource Inventory Summary ===")
    print(f"Total resources: {inventory['resource_count']}")
    print(f"Total fields: {inventory['total_fields']}")
    print(f"Fields with descriptions: {inventory['fields_with_descriptions']}")
    print(f"Fields with types: {inventory['fields_with_types']}")
    print()
    print(f"{'Resource':<25} {'Fields':>6} {'Search Params':>13}")
    print("-" * 50)
    for entity in inventory["entities"]:
        print(f"{entity['name']:<25} {entity['field_count']:>6} {entity['search_param_count']:>13}")
    print("-" * 50)
    print(f"{'TOTAL':<25} {inventory['total_fields']:>6}")

def main():
    resources = load_fhir_resources()
    inventory = build_inventory(resources)

    # Save full inventory
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Saved full-entity-inventory.json")

    # Print summary
    print_summary(inventory)

    # Save summary stats
    stats = {
        "resource_count": inventory["resource_count"],
        "total_fields": inventory["total_fields"],
        "fields_with_descriptions": inventory["fields_with_descriptions"],
        "fields_with_types": inventory["fields_with_types"],
        "description_coverage_pct": round(inventory["fields_with_descriptions"] / inventory["total_fields"] * 100, 1) if inventory["total_fields"] > 0 else 0,
        "type_coverage_pct": round(inventory["fields_with_types"] / inventory["total_fields"] * 100, 1) if inventory["total_fields"] > 0 else 0,
        "resources_by_size": sorted(
            [{"name": e["name"], "fields": e["field_count"]} for e in inventory["entities"]],
            key=lambda x: x["fields"],
            reverse=True
        )
    }
    with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(f"\nSaved summary-stats.json")

if __name__ == "__main__":
    main()
