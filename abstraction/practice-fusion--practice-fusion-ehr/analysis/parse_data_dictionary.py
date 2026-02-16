#!/usr/bin/env python3
"""Parse Practice Fusion v9 EHI export data dictionary from HTML pages.

Reads:
  - downloads/v9-index.html (category structure)
  - downloads/v9-pages/*.html (per-table field definitions)
  - downloads/v9-data-dictionary.json (pre-extracted, for cross-validation)

Outputs:
  - analysis/entity-inventory-full.json (complete field-level inventory)
  - analysis/entity-inventory-summary.json (aggregated statistics)
"""

import json
import re
import os
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE, "downloads")
ANALYSIS = os.path.join(BASE, "analysis")


def parse_index_categories():
    """Extract category->tables mapping from v9-index.html."""
    with open(os.path.join(DOWNLOADS, "v9-index.html")) as f:
        html = f.read()

    categories = {}
    current_cat = None

    # Split by h3 headings
    parts = re.split(r'<h3[^>]*id="([^"]*)"[^>]*>(.*?)</h3>', html)
    # parts: [before, id1, text1, content1, id2, text2, content2, ...]
    i = 1
    while i < len(parts):
        cat_id = parts[i]
        cat_name = re.sub(r'<[^>]+>', '', parts[i + 1]).strip()
        content = parts[i + 2] if i + 2 < len(parts) else ""

        # Find all linked .tsv files in this section
        links = re.findall(r'<a[^>]*href="[^"]*?/v9/([^/"]+)/"[^>]*>\s*(.*?)\s*</a>', content, re.DOTALL)
        tables = []
        for slug, link_text in links:
            clean_text = re.sub(r'<[^>]+>', '', link_text).strip()
            tables.append({"slug": slug, "filename": clean_text})

        # Also extract description paragraphs for each table
        # Pattern: table link followed by description
        table_descs = re.findall(
            r'<a[^>]*href="[^"]*?/v9/([^/"]+)/"[^>]*>.*?</a>\s*(?:<[^>]*>)*\s*(?:<p[^>]*>(.*?)</p>)?',
            content, re.DOTALL
        )
        desc_map = {}
        for slug, desc in table_descs:
            if desc:
                desc_map[slug] = re.sub(r'<[^>]+>', '', desc).strip()

        for t in tables:
            t["category_description"] = desc_map.get(t["slug"], "")

        categories[cat_name] = tables
        i += 3

    return categories


def parse_table_page(slug):
    """Parse a single table's HTML page to extract field definitions."""
    filepath = os.path.join(DOWNLOADS, "v9-pages", f"{slug}.html")
    if not os.path.exists(filepath):
        return None

    with open(filepath) as f:
        html = f.read()

    # Extract table title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else slug

    # Extract table description (first <p> after intro or specific section)
    desc_match = re.search(r'<p[^>]*class="[^"]*intro[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
    if not desc_match:
        desc_match = re.search(r'<h1[^>]*>.*?</h1>\s*(?:<[^>]*>)*\s*<p[^>]*>(.*?)</p>', html, re.DOTALL)
    table_desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else ""

    # Extract fields from the HTML table
    fields = []
    # Find <table> with field definitions
    table_match = re.search(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
    if not table_match:
        return {"title": title, "description": table_desc, "fields": fields}

    table_html = table_match.group(1)

    # Parse header row to get column names
    thead_match = re.search(r'<thead[^>]*>(.*?)</thead>', table_html, re.DOTALL)
    headers = []
    if thead_match:
        headers = [re.sub(r'<[^>]+>', '', h).strip().lower()
                    for h in re.findall(r'<th[^>]*>(.*?)</th>', thead_match.group(1), re.DOTALL)]

    # Parse data rows
    tbody_match = re.search(r'<tbody[^>]*>(.*?)</tbody>', table_html, re.DOTALL)
    if tbody_match:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbody_match.group(1), re.DOTALL)
    else:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
        if rows:
            rows = rows[1:]  # skip header row

    for row in rows:
        cells = [re.sub(r'<[^>]+>', '', c).strip()
                 for c in re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)]
        if len(cells) >= 3:
            field = {
                "field_name": cells[0],
                "data_type": cells[1],
                "description": cells[2] if len(cells) > 2 else ""
            }
            # Some pages may have additional columns (nullable, etc.)
            if len(cells) > 3:
                for i, extra in enumerate(cells[3:], 3):
                    if i < len(headers):
                        field[headers[i]] = extra
                    else:
                        field[f"column_{i}"] = extra
            fields.append(field)

    return {"title": title, "description": table_desc, "fields": fields}


def validate_against_preextracted(inventory, preextracted_path):
    """Cross-validate our parse against the pre-extracted JSON."""
    with open(preextracted_path) as f:
        preextracted = json.load(f)

    discrepancies = []
    for table_name, pre_data in preextracted.items():
        found = False
        for entity in inventory:
            if entity["filename"] == table_name:
                found = True
                if len(entity["fields"]) != pre_data["field_count"]:
                    discrepancies.append({
                        "table": table_name,
                        "our_count": len(entity["fields"]),
                        "pre_count": pre_data["field_count"],
                        "type": "field_count_mismatch"
                    })
                break
        if not found:
            discrepancies.append({"table": table_name, "type": "missing_in_our_parse"})

    return discrepancies


def main():
    categories = parse_index_categories()

    print(f"Found {len(categories)} categories:")
    for cat, tables in categories.items():
        print(f"  {cat}: {len(tables)} tables")

    # Parse each table page
    inventory = []
    for cat_name, tables in categories.items():
        for table_info in tables:
            slug = table_info["slug"]
            parsed = parse_table_page(slug)
            if parsed is None:
                print(f"  WARNING: Could not find page for {slug}")
                continue

            entity = {
                "filename": f"{slug}.tsv",
                "slug": slug,
                "category": cat_name,
                "title": parsed["title"],
                "table_description": parsed.get("description", ""),
                "category_description": table_info.get("category_description", ""),
                "field_count": len(parsed["fields"]),
                "fields": parsed["fields"]
            }
            inventory.append(entity)

    total_fields = sum(e["field_count"] for e in inventory)
    fields_with_desc = sum(
        1 for e in inventory for f in e["fields"] if f.get("description", "").strip()
    )
    fields_with_type = sum(
        1 for e in inventory for f in e["fields"] if f.get("data_type", "").strip()
    )

    print(f"\nTotal entities: {len(inventory)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc}")
    print(f"Fields with types: {fields_with_type}")

    # Cross-validate
    pre_path = os.path.join(DOWNLOADS, "v9-data-dictionary.json")
    if os.path.exists(pre_path):
        discrepancies = validate_against_preextracted(inventory, pre_path)
        if discrepancies:
            print(f"\nDiscrepancies with pre-extracted JSON: {len(discrepancies)}")
            for d in discrepancies:
                print(f"  {d}")
        else:
            print("\nNo discrepancies with pre-extracted JSON.")

    # Save full inventory
    full_path = os.path.join(ANALYSIS, "entity-inventory-full.json")
    with open(full_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nSaved full inventory to {full_path}")

    # Generate summary
    summary = {
        "total_entities": len(inventory),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "categories": {}
    }

    for cat_name in categories:
        cat_entities = [e for e in inventory if e["category"] == cat_name]
        cat_fields = sum(e["field_count"] for e in cat_entities)
        cat_desc = sum(
            1 for e in cat_entities for f in e["fields"] if f.get("description", "").strip()
        )
        summary["categories"][cat_name] = {
            "entity_count": len(cat_entities),
            "field_count": cat_fields,
            "fields_with_descriptions": cat_desc,
            "entities": [
                {
                    "filename": e["filename"],
                    "field_count": e["field_count"],
                    "fields_described": sum(1 for f in e["fields"] if f.get("description", "").strip()),
                    "fields_typed": sum(1 for f in e["fields"] if f.get("data_type", "").strip()),
                }
                for e in cat_entities
            ]
        }

    # Data types breakdown
    type_counts = {}
    for e in inventory:
        for f in e["fields"]:
            dt = f.get("data_type", "unknown")
            type_counts[dt] = type_counts.get(dt, 0) + 1
    summary["data_types"] = dict(sorted(type_counts.items(), key=lambda x: -x[1]))

    # Largest entities
    summary["largest_entities"] = sorted(
        [{"filename": e["filename"], "category": e["category"], "field_count": e["field_count"]}
         for e in inventory],
        key=lambda x: -x["field_count"]
    )[:15]

    sum_path = os.path.join(ANALYSIS, "entity-inventory-summary.json")
    with open(sum_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary to {sum_path}")


if __name__ == "__main__":
    main()
