#!/usr/bin/env python3
"""Parse all Veradigm View v6 EHI export entity HTML pages into a structured inventory."""

import json
import os
import re
from pathlib import Path

BASE = Path(__file__).parent.parent
ENTITIES_DIR = BASE / "downloads" / "v6-entities"
INDEX_FILE = BASE / "downloads" / "v6-index.html"
OUT_FULL = Path(__file__).parent / "entity-inventory-full.json"
OUT_SUMMARY = Path(__file__).parent / "entity-inventory-summary.json"


def parse_index():
    """Parse the index page to get categories and entity->category mapping."""
    with open(INDEX_FILE) as f:
        content = f.read()

    # Find category headings and the entities listed under them
    # Categories are h3 tags, entities are links to /v6/<slug>/
    categories = {}
    current_category = None

    # Split by h3 tags to get sections
    parts = re.split(r'<h3[^>]*>', content)
    for part in parts[1:]:  # skip before first h3
        # Get category name
        h3_end = part.find('</h3>')
        if h3_end == -1:
            continue
        cat_name = re.sub(r'<[^>]+>', '', part[:h3_end]).strip()
        if cat_name in ('Demographics', 'Patient', 'Clinical', 'Billing and insurance',
                        'Medications and prescriptions', 'Labs', 'Referrals', 'Messaging'):
            # Find entity links in this section
            links = re.findall(r'/v6/([^/]+)/', part[:part.find('<h3') if '<h3' in part else len(part)])
            for slug in links:
                categories[slug] = cat_name

    return categories


def parse_entity_page(filepath):
    """Parse a single entity HTML page to extract field definitions."""
    with open(filepath) as f:
        content = f.read()

    entity_name = filepath.stem  # e.g. 'patient-demographics'

    # Extract entity description from h4 tag
    desc_match = re.search(r'<h4[^>]*>(.*?)</h4>', content, re.S)
    entity_desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip() if desc_match else ""

    # Extract table
    table_match = re.search(r'<table[^>]*>(.*?)</table>', content, re.S)
    if not table_match:
        return {
            "entity": entity_name,
            "tsv_file": f"{entity_name}.tsv",
            "description": entity_desc,
            "fields": [],
            "parse_error": True,
            "parse_error_detail": "No table found in HTML"
        }

    table_html = table_match.group(0)
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.S)

    if not rows:
        return {
            "entity": entity_name,
            "tsv_file": f"{entity_name}.tsv",
            "description": entity_desc,
            "fields": [],
            "parse_error": True,
            "parse_error_detail": "No rows found in table"
        }

    # Parse header row
    header_cells = re.findall(r'<th[^>]*>(.*?)</th>', rows[0], re.S)
    if not header_cells:
        header_cells = re.findall(r'<td[^>]*>(.*?)</td>', rows[0], re.S)
    headers = [re.sub(r'<[^>]+>', '', h).strip().lower().replace(' ', '_') for h in header_cells]

    fields = []
    for row in rows[1:]:
        cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)
        clean_cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]

        if len(clean_cells) < 2:
            continue

        field = {}
        for i, header in enumerate(headers):
            if i < len(clean_cells):
                field[header] = clean_cells[i]

        # Normalize to standard keys
        normalized = {
            "name": field.get("field_name", field.get("field", field.get("name", ""))),
            "type": field.get("data_type", field.get("type", "")),
            "description": field.get("field_description", field.get("description", "")),
        }
        # Keep any extra columns
        for k, v in field.items():
            if k not in ("field_name", "data_type", "field_description", "field", "type", "description", "name"):
                normalized[k] = v

        if normalized["name"]:
            fields.append(normalized)

    return {
        "entity": entity_name,
        "tsv_file": f"{entity_name}.tsv",
        "description": entity_desc,
        "fields": fields,
        "field_count": len(fields),
    }


def main():
    categories = parse_index()

    entities = []
    parse_errors = []

    for html_file in sorted(ENTITIES_DIR.glob("*.html")):
        entity = parse_entity_page(html_file)
        slug = html_file.stem
        entity["category"] = categories.get(slug, "Uncategorized")

        if entity.get("parse_error"):
            parse_errors.append(entity)
        entities.append(entity)

    # Write full inventory
    with open(OUT_FULL, 'w') as f:
        json.dump(entities, f, indent=2)

    # Compute summary statistics
    total_fields = sum(len(e["fields"]) for e in entities)
    fields_with_desc = sum(1 for e in entities for fld in e["fields"] if fld.get("description"))
    fields_with_type = sum(1 for e in entities for fld in e["fields"] if fld.get("type"))

    # Category breakdown
    cat_stats = {}
    for e in entities:
        cat = e["category"]
        if cat not in cat_stats:
            cat_stats[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
        cat_stats[cat]["entity_count"] += 1
        cat_stats[cat]["field_count"] += len(e["fields"])
        cat_stats[cat]["entities"].append(e["entity"])

    # Data type distribution
    type_dist = {}
    for e in entities:
        for fld in e["fields"]:
            t = fld.get("type", "unknown")
            type_dist[t] = type_dist.get(t, 0) + 1

    # Top entities by field count
    top_entities = sorted(entities, key=lambda e: len(e["fields"]), reverse=True)[:20]

    summary = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "description_coverage_pct": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
        "type_coverage_pct": round(100 * fields_with_type / total_fields, 1) if total_fields else 0,
        "parse_errors": len(parse_errors),
        "categories": cat_stats,
        "data_type_distribution": dict(sorted(type_dist.items(), key=lambda x: -x[1])),
        "top_entities_by_field_count": [
            {"entity": e["entity"], "category": e["category"], "field_count": len(e["fields"])}
            for e in top_entities
        ],
    }

    with open(OUT_SUMMARY, 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['description_coverage_pct']}%)")
    print(f"Fields with types: {fields_with_type} ({summary['type_coverage_pct']}%)")
    print(f"Parse errors: {len(parse_errors)}")
    print(f"\nCategories:")
    for cat, stats in sorted(cat_stats.items()):
        print(f"  {cat}: {stats['entity_count']} entities, {stats['field_count']} fields")
    print(f"\nTop 10 entities by field count:")
    for e in top_entities[:10]:
        print(f"  {e['entity']}: {len(e['fields'])} fields ({e['category']})")


if __name__ == "__main__":
    main()
