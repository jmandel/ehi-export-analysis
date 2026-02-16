#!/usr/bin/env python3
"""
Parse the enrichment data-dictionary.json and produce:
1. full-entity-inventory.json — complete machine-readable extraction
2. category-summary.json — per-category statistics
3. stats.json — aggregate statistics for analysis.md
"""

import json
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.parent.parent / "results" / "flatiron-health--oncoemr"
DATA_DICT = RESULTS_DIR / "downloads" / "enrichment" / "data-dictionary.json"
COVERAGE = RESULTS_DIR / "downloads" / "enrichment" / "coverage-summary.json"
OUT_DIR = Path(__file__).parent

def main():
    with open(DATA_DICT) as f:
        dd = json.load(f)
    with open(COVERAGE) as f:
        cov = json.load(f)

    tables = dd["tables"]
    categories = cov["data_domain_categories"]

    # Build category lookup
    table_to_category = {}
    for cat, tbl_list in categories.items():
        for t in tbl_list:
            table_to_category[t] = cat

    # Build full inventory
    inventory = {
        "export_format": dd["export_format"],
        "last_modified": dd["last_modified"],
        "summary": {},
        "entities": []
    }

    total_fields = 0
    fields_with_desc = 0
    fields_with_type = 0
    fields_nullable_known = 0
    deprecated_fields = 0
    empty_tables = []

    for tbl in tables:
        cols = tbl["columns"]
        entity = {
            "name": tbl["name"],
            "description": tbl.get("description", ""),
            "category": table_to_category.get(tbl["name"], "uncategorized"),
            "field_count": len(cols),
            "fields": []
        }

        for col in cols:
            desc = col.get("description", "") or ""
            is_deprecated = "deprecated" in desc.lower() if desc else False
            field = {
                "name": col["column_name"],
                "type": col.get("data_type", ""),
                "nullable": col.get("nullable"),
                "description": desc,
                "deprecated": is_deprecated
            }
            entity["fields"].append(field)

            total_fields += 1
            if desc.strip():
                fields_with_desc += 1
            if col.get("data_type"):
                fields_with_type += 1
            if col.get("nullable") is not None:
                fields_nullable_known += 1
            if is_deprecated:
                deprecated_fields += 1

        if len(cols) == 0:
            empty_tables.append(tbl["name"])

        inventory["entities"].append(entity)

    # Category summary
    cat_summary = {}
    for cat, tbl_list in categories.items():
        cat_fields = 0
        cat_described = 0
        for tname in tbl_list:
            for tbl in tables:
                if tbl["name"] == tname:
                    for c in tbl["columns"]:
                        cat_fields += 1
                        if (c.get("description") or "").strip():
                            cat_described += 1
                    break
        cat_summary[cat] = {
            "table_count": len(tbl_list),
            "field_count": cat_fields,
            "fields_with_descriptions": cat_described,
            "tables": tbl_list
        }

    # Compute stats
    stats = {
        "total_tables": len(tables),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_without_descriptions": total_fields - fields_with_desc,
        "description_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "fields_with_types": fields_with_type,
        "fields_nullable_known": fields_nullable_known,
        "deprecated_fields": deprecated_fields,
        "tables_with_descriptions": sum(1 for t in tables if (t.get("description") or "").strip()),
        "empty_tables": empty_tables,
        "largest_tables": sorted(
            [{"name": t["name"], "fields": len(t["columns"]), "category": table_to_category.get(t["name"], "?")} for t in tables],
            key=lambda x: -x["fields"]
        )[:20],
        "category_breakdown": cat_summary
    }

    inventory["summary"] = {
        "total_entities": stats["total_tables"],
        "total_fields": stats["total_fields"],
        "fields_with_descriptions": stats["fields_with_descriptions"],
        "description_coverage_pct": stats["description_pct"],
        "deprecated_fields": stats["deprecated_fields"]
    }

    # Write outputs
    with open(OUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    with open(OUT_DIR / "category-summary.json", "w") as f:
        json.dump(cat_summary, f, indent=2)
    with open(OUT_DIR / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    # Print summary for verification
    print(f"Tables: {stats['total_tables']}")
    print(f"Fields: {stats['total_fields']}")
    print(f"Fields with descriptions: {stats['fields_with_descriptions']} ({stats['description_pct']}%)")
    print(f"Fields with types: {stats['fields_with_types']}")
    print(f"Deprecated fields: {stats['deprecated_fields']}")
    print(f"Empty tables: {stats['empty_tables']}")
    print(f"\nTop 20 largest tables:")
    for t in stats["largest_tables"]:
        print(f"  {t['name']}: {t['fields']} fields ({t['category']})")
    print(f"\nCategory breakdown:")
    for cat, info in sorted(cat_summary.items(), key=lambda x: -x[1]["field_count"]):
        print(f"  {cat}: {info['table_count']} tables, {info['field_count']} fields, {info['fields_with_descriptions']} described")

if __name__ == "__main__":
    main()
