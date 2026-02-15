"""
Parse data dictionary from PDF text (pdftotext -layout output).
The PDF has two sections: Clinical Data Exports and Practice Management Data Exports.
Each section has columns: Export Name, FIELD, Description (which may span multiple lines).
"""
import json, re
from pathlib import Path

OUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/isalus-healthcare--officeemr/analysis")

with open("/tmp/isalus-ehi-export.txt") as f:
    lines = f.readlines()

# Find section boundaries
clinical_start = None
pm_start = None
for i, line in enumerate(lines):
    if "Clinical Data Exports" in line and clinical_start is None:
        clinical_start = i
    if "Practice Management Data Exports" in line:
        pm_start = i

print(f"Clinical section starts at line {clinical_start}")
print(f"PM section starts at line {pm_start}")

def parse_section(lines, start_line, end_line, category):
    """Parse a data dictionary section from PDF text."""
    entries = []
    current_entity = ""
    current_field = ""
    current_desc = ""
    
    i = start_line
    # Skip header lines
    while i < end_line:
        line = lines[i]
        if "Export Name" in line and "FIELD" in line:
            i += 1
            break
        i += 1
    
    while i < end_line:
        line = lines[i].rstrip()
        
        # Skip empty lines and page headers/footers
        if not line.strip():
            i += 1
            continue
        if line.strip().startswith("EHI Export"):
            i += 1
            continue
        if re.match(r'^\s*\d+/\d+\s*$', line.strip()):
            i += 1
            continue
        if "Export Name" in line and "FIELD" in line:
            i += 1
            continue
        
        # Check if this line starts a new entry (has entity name in first column)
        # Entity names end in .json and appear at the start of the line
        entity_match = re.match(r'^(\S+\.json)\s+(\S+)\s+(.*)', line)
        
        if entity_match:
            # Save previous entry
            if current_field:
                entries.append({
                    "entity": current_entity.replace(".json", ""),
                    "field": current_field,
                    "description": current_desc.strip(),
                    "category": category
                })
            current_entity = entity_match.group(1)
            current_field = entity_match.group(2)
            current_desc = entity_match.group(3).strip()
        else:
            # Check if this is a continuation line with just field + description
            # (entity column empty, field + description present)
            field_match = re.match(r'^\S+\.json\s+', line)
            if not field_match:
                # Could be a new field (indented) or continuation of description
                stripped = line.strip()
                # Check if it looks like a field name (single word, camelCase or snake_case)
                parts = line.split()
                if parts:
                    # Determine column position - fields tend to start at a certain indent
                    leading_spaces = len(line) - len(line.lstrip())
                    if leading_spaces > 0 and leading_spaces < 30:
                        # This might be a field name with entity implied
                        potential_field = parts[0]
                        if re.match(r'^[a-zA-Z][a-zA-Z0-9_]+$', potential_field) and len(potential_field) < 40:
                            # Save previous
                            if current_field:
                                entries.append({
                                    "entity": current_entity.replace(".json", ""),
                                    "field": current_field,
                                    "description": current_desc.strip(),
                                    "category": category
                                })
                            current_field = potential_field
                            current_desc = " ".join(parts[1:]).strip()
                        else:
                            # Continuation of description
                            current_desc += " " + stripped
                    elif leading_spaces >= 30:
                        # Description continuation (far right column)
                        current_desc += " " + stripped
                    else:
                        # Continuation of description
                        current_desc += " " + stripped
        i += 1
    
    # Save last entry
    if current_field:
        entries.append({
            "entity": current_entity.replace(".json", ""),
            "field": current_field,
            "description": current_desc.strip(),
            "category": category
        })
    
    return entries

# Parse both sections
clinical_entries = parse_section(lines, clinical_start, pm_start, "Clinical")
pm_entries = parse_section(lines, pm_start, len(lines), "Practice Management")

all_entries = clinical_entries + pm_entries

# Build entity summary
from collections import defaultdict
entities = defaultdict(lambda: {"fields": [], "category": ""})
for e in all_entries:
    entities[e["entity"]]["fields"].append({
        "field": e["field"],
        "description": e["description"],
        "has_description": bool(e["description"])
    })
    entities[e["entity"]]["category"] = e["category"]

entity_summary = []
for name, data in sorted(entities.items()):
    entity_summary.append({
        "entity": name,
        "category": data["category"],
        "field_count": len(data["fields"]),
        "fields_with_descriptions": sum(1 for f in data["fields"] if f["has_description"]),
        "fields": [f["field"] for f in data["fields"]]
    })

# Save
with open(OUT / "pdf-data-dictionary.json", "w") as fh:
    json.dump(all_entries, fh, indent=2)

with open(OUT / "pdf-entity-summary.json", "w") as fh:
    json.dump(entity_summary, fh, indent=2)

# Print summary
print(f"\nTotal entries parsed: {len(all_entries)}")
print(f"Clinical entries: {len(clinical_entries)}")
print(f"PM entries: {len(pm_entries)}")
print(f"Distinct entities: {len(entities)}")

cat_summary = defaultdict(lambda: {"entities": 0, "fields": 0})
for e in entity_summary:
    cat_summary[e["category"]]["entities"] += 1
    cat_summary[e["category"]]["fields"] += e["field_count"]

print(f"\n{'Category':<25} {'Entities':>10} {'Fields':>10}")
for cat, stats in sorted(cat_summary.items()):
    print(f"{cat:<25} {stats['entities']:>10} {stats['fields']:>10}")

print(f"\n{'Entity':<45} {'Cat':<20} {'Fields':>8}")
print("-" * 80)
for e in sorted(entity_summary, key=lambda x: -x["field_count"]):
    print(f"{e['entity']:<45} {e['category']:<20} {e['field_count']:>8}")
