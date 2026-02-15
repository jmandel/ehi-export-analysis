"""
Parse the ehrTHOMAS EHI export HTML page to extract XML dataset structures.
Counts entities, fields, and documents the structure of each dataset.
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

HTML_PATH = Path(__file__).parent.parent.parent.parent / "results/genius-solutions-inc--ehrthomas/downloads/ehi-export-page.html"
OUTPUT_PATH = Path(__file__).parent / "parsed_datasets.json"
SUMMARY_PATH = Path(__file__).parent / "field_summary.txt"

html_content = HTML_PATH.read_text(encoding="utf-8")

# Extract all <pre> blocks (contain XML samples)
pre_blocks = re.findall(r'<pre>(.*?)</pre>', html_content, re.DOTALL)

# Extract dataset titles (h4 with titleBackground class)
titles = re.findall(r'<h4 class="titleBackground">(.*?)</h4>', html_content)

def extract_xml_fields(xml_text):
    """Extract unique XML element names from sample XML, building a nested structure."""
    # Decode HTML entities
    xml_text = xml_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    
    # Find all XML tags (opening)
    tags = re.findall(r'<(\w+)(?:\s[^>]*)?>([^<]*)', xml_text)
    
    # Build field list with values
    fields = []
    seen = set()
    for tag_name, value in tags:
        if tag_name not in seen:
            seen.add(tag_name)
            has_value = bool(value.strip())
            fields.append({
                "name": tag_name,
                "sample_value": value.strip() if has_value else None,
                "has_sample_data": has_value
            })
    
    return fields

def extract_leaf_fields(xml_text):
    """Extract only leaf-level fields (those that contain text, not child elements)."""
    xml_text = xml_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    
    # Find elements that have text content (leaf nodes)
    leaf_pattern = r'<(\w+)(?:\s[^>]*)?>([^<]+)</\1>'
    matches = re.findall(leaf_pattern, xml_text)
    
    fields = []
    seen = set()
    for tag_name, value in matches:
        if tag_name not in seen:
            seen.add(tag_name)
            fields.append({
                "name": tag_name,
                "sample_value": value.strip(),
            })
    
    # Also find self-closing or empty elements
    empty_pattern = r'<(\w+)(?:\s[^>]*)?>\s*</\1>'
    empties = re.findall(empty_pattern, xml_text)
    for tag_name in empties:
        if tag_name not in seen:
            seen.add(tag_name)
            fields.append({
                "name": tag_name,
                "sample_value": None,
            })
    
    return fields

def count_type_annotations(xml_text):
    """Count fields with type annotations like type='date' or type='time'."""
    xml_text = xml_text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    typed = re.findall(r'<(\w+)\s+type="(\w+)"', xml_text)
    return typed

datasets = []
for i, (title, pre_block) in enumerate(zip(titles, pre_blocks)):
    all_fields = extract_xml_fields(pre_block)
    leaf_fields = extract_leaf_fields(pre_block)
    type_annotations = count_type_annotations(pre_block)
    
    # Identify container elements (those not in leaf fields)
    leaf_names = {f["name"] for f in leaf_fields}
    all_names = {f["name"] for f in all_fields}
    container_names = all_names - leaf_names
    
    dataset = {
        "name": title,
        "total_elements": len(all_fields),
        "leaf_fields": len(leaf_fields),
        "container_elements": len(container_names),
        "typed_fields": len(type_annotations),
        "type_annotations": [{"field": t[0], "type": t[1]} for t in type_annotations],
        "fields": leaf_fields,
        "containers": sorted(container_names),
    }
    datasets.append(dataset)

# Summary
total_datasets = len(datasets)
total_leaf_fields = sum(d["leaf_fields"] for d in datasets)
total_typed = sum(d["typed_fields"] for d in datasets)

summary = {
    "total_datasets": total_datasets,
    "total_leaf_fields": total_leaf_fields,
    "total_typed_fields": total_typed,
    "datasets": datasets,
}

# Write JSON output
OUTPUT_PATH.write_text(json.dumps(summary, indent=2))

# Write human-readable summary
lines = []
lines.append("ehrTHOMAS EHI Export - Dataset Analysis")
lines.append("=" * 50)
lines.append(f"Total datasets: {total_datasets}")
lines.append(f"Total leaf fields (across all datasets): {total_leaf_fields}")
lines.append(f"Total fields with type annotations: {total_typed}")
lines.append("")

for ds in datasets:
    lines.append(f"\n--- {ds['name']} ---")
    lines.append(f"  Leaf fields: {ds['leaf_fields']}")
    lines.append(f"  Container elements: {ds['container_elements']}")
    lines.append(f"  Typed fields: {ds['typed_fields']}")
    lines.append(f"  Fields:")
    for f in ds['fields']:
        val = f"= {f['sample_value']}" if f['sample_value'] else "(empty)"
        lines.append(f"    - {f['name']} {val}")

lines.append("\n\n--- Data Quality Notes ---")
lines.append("- No formal schema (XSD/DTD) provided")
lines.append("- No field descriptions beyond element names")
lines.append("- No value set documentation")
lines.append("- No cardinality/optionality documentation")
lines.append("- No relationship documentation beyond ID references")

SUMMARY_PATH.write_text("\n".join(lines))
print("\n".join(lines))
