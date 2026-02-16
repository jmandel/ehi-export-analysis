"""Parse the ehrTHOMAS EHI export HTML page to extract all XML dataset samples
and produce entity-inventory-full.json and entity-inventory-summary.json."""

import json
import re
from html.parser import HTMLParser
from xml.etree import ElementTree as ET
from pathlib import Path

HTML_PATH = Path(__file__).parent.parent / "downloads" / "ehi-export-page.html"
OUT_DIR = Path(__file__).parent

html = HTML_PATH.read_text(encoding="utf-8")

# Extract dataset titles and their XML content from <pre> blocks
# Pattern: <h4 class="titleBackground">TITLE</h4> ... <pre>XML</pre>
title_pattern = re.compile(
    r'<h4 class="titleBackground">\s*(.*?)\s*</h4>\s*(?:</div>\s*)?<pre>(.*?)</pre>',
    re.DOTALL
)

matches = title_pattern.findall(html)

entities = []

for title, xml_raw in matches:
    dataset_name = title.replace(" Dataset", "").strip()
    
    # Clean XML: unescape HTML entities
    xml_text = xml_raw.strip()
    xml_text = re.sub(r'&lt;', '<', xml_text)
    xml_text = re.sub(r'&gt;', '>', xml_text)
    xml_text = re.sub(r'&quot;', '"', xml_text)
    xml_text = re.sub(r'&amp;', '&', xml_text)
    # Re-escape bare & for XML validity
    xml_text = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#)', '&amp;', xml_text)
    
    # Wrap in root if needed for parsing
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        # Try wrapping
        try:
            root = ET.fromstring(f"<root>{xml_text}</root>")
        except ET.ParseError as e:
            print(f"Failed to parse {dataset_name}: {e}")
            entities.append({
                "entity_name": dataset_name,
                "parse_error": True,
                "raw_text": xml_text[:500],
                "field_count": 0,
                "fields": []
            })
            continue
    
    # Find the first actual record element (skip the collection wrapper)
    # e.g., <Encounters><Encounter>...</Encounter></Encounters> -> use <Encounter>
    record_elem = None
    if len(list(root)) > 0:
        first_child = list(root)[0]
        # Check if this is a collection wrapper
        if root.tag.endswith('s') and len(list(first_child)) > 0:
            record_elem = first_child
        else:
            record_elem = root
    else:
        record_elem = root
    
    fields = []
    
    def walk(elem, prefix=""):
        for child in elem:
            tag = child.tag
            full_path = f"{prefix}.{tag}" if prefix else tag
            children = list(child)
            if children:
                walk(child, full_path)
            else:
                field = {
                    "name": full_path,
                    "leaf_name": tag,
                    "type": child.attrib.get("type", "string"),
                    "sample_value": (child.text or "").strip(),
                    "description": None
                }
                fields.append(field)
    
    walk(record_elem)
    
    # Deduplicate fields by name (multiple records may have same fields)
    seen = set()
    unique_fields = []
    for f in fields:
        if f["name"] not in seen:
            seen.add(f["name"])
            unique_fields.append(f)
    
    entities.append({
        "entity_name": dataset_name,
        "xml_root_tag": root.tag,
        "record_tag": record_elem.tag if record_elem is not None else None,
        "field_count": len(unique_fields),
        "fields": unique_fields,
        "parse_error": False
    })

# Full inventory
full_inventory = {
    "source": "downloads/ehi-export-page.html",
    "export_format": "XML",
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "fields_with_descriptions": 0,
    "entities": entities
}

with open(OUT_DIR / "entity-inventory-full.json", "w") as f:
    json.dump(full_inventory, f, indent=2)

# Summary
summary = {
    "source": "downloads/ehi-export-page.html",
    "export_format": "XML",
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "fields_with_descriptions": 0,
    "pct_fields_with_descriptions": 0.0,
    "fields_with_types": sum(
        1 for e in entities for f in e["fields"] if f["type"] != "string"
    ),
    "fields_with_sample_values": sum(
        1 for e in entities for f in e["fields"] if f["sample_value"]
    ),
    "entity_summary": [
        {
            "entity_name": e["entity_name"],
            "field_count": e["field_count"],
            "fields_described": 0,
            "fields_with_types": sum(1 for f in e["fields"] if f["type"] != "string"),
            "fields_with_samples": sum(1 for f in e["fields"] if f["sample_value"]),
        }
        for e in entities
    ]
}

with open(OUT_DIR / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Entities found: {len(entities)}")
print(f"Total unique fields: {full_inventory['total_fields']}")
print(f"Fields with descriptions: 0")
print(f"Fields with explicit types: {summary['fields_with_types']}")
print(f"Fields with sample values: {summary['fields_with_sample_values']}")
print()
for e in entities:
    print(f"  {e['entity_name']}: {e['field_count']} fields")
    for f in e["fields"]:
        sample = f['sample_value'][:40] if f['sample_value'] else "(empty)"
        print(f"    - {f['name']} [{f['type']}]: {sample}")
