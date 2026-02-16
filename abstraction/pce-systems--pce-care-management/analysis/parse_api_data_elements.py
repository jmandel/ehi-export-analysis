#!/usr/bin/env python3
"""
Parse the Data Elements section from the PIX 9.4 API Documentation PDF.
Uses column-position-based parsing for better handling of wrapped lines.
"""

import json
import re
import subprocess

KNOWN_ENTITIES = [
    "Address", "AllergyIntolerance", "CarePlan", "CareTeam", "Claim",
    "Coded Element", "Condition", "Coverage", "Device", "Diagnostic Report",
    "Document Reference", "Encounter", "Goal", "Healthcare Service",
    "Immunization", "Location", "Medication Request", "Message",
    "Observation", "Organization", "Patient", "Practitioner",
    "Practitioner Role", "Procedure", "Provenance", "Failed Response Header"
]

UTILITY_TYPES = {"Message", "Failed Response Header", "Coded Element"}

def get_indent(line):
    """Return number of leading spaces."""
    return len(line) - len(line.lstrip())

def parse_table_block(raw_lines):
    """Parse a table of Attribute / Data Type / Description from raw lines."""
    fields = []
    current = None
    
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        indent = get_indent(line)
        
        # Heuristic: a new field row starts with moderate indentation (4-10 spaces)
        # and has content that looks like an attribute name (contains letters/colons/brackets)
        # followed by type and description separated by 3+ spaces
        
        parts = re.split(r'\s{3,}', stripped)
        
        if len(parts) >= 3 and re.match(r'^[a-z]', parts[0]):
            # New field: name, type, description
            current = {
                "name": parts[0].strip(),
                "type": parts[1].strip(),
                "description": " ".join(parts[2:]).strip()
            }
            fields.append(current)
        elif len(parts) == 2 and current:
            first, second = parts[0].strip(), parts[1].strip()
            # Could be: type_continuation + description_continuation
            # Or: name + type (missing description)
            # Or: description split across two columns
            if first in ('Element', 'Element List', 'List', 'Point'):
                current["type"] += " " + first
                current["description"] += " " + second
            elif re.match(r'^[a-z]', first) and indent < 20:
                # Looks like a new field with only name + type
                current = {"name": first, "type": second, "description": ""}
                fields.append(current)
            else:
                # Continuation line — likely wrapping description
                current["description"] += " " + stripped
        elif len(parts) == 1 and current:
            tok = stripped
            if tok in ('Element', 'Element List', 'List', 'Point'):
                current["type"] += " " + tok
            elif tok.startswith('o ') or tok.startswith('o\t'):
                pass  # Sub-profile bullets in Observation
            else:
                current["description"] += " " + tok
        elif len(parts) >= 3 and not re.match(r'^[a-z]', parts[0]):
            # Could be a field with uppercase start (resourceType)
            if re.match(r'^[a-zA-Z]', parts[0]) and any(c.islower() for c in parts[0]):
                current = {
                    "name": parts[0].strip(),
                    "type": parts[1].strip(),
                    "description": " ".join(parts[2:]).strip()
                }
                fields.append(current)
            elif current:
                current["description"] += " " + stripped
    
    # Clean up descriptions
    for f in fields:
        f["description"] = re.sub(r'\s+', ' ', f["description"]).strip()
    
    return fields

def main():
    pdf_path = "../downloads/PIX_9_4_API_Documentation.pdf"
    result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
    text = result.stdout
    lines = text.split("\n")

    # Find the Data Elements section (not TOC)
    start_idx = None
    end_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "Data Elements" and i > 100:
            start_idx = i + 1
        if start_idx and re.match(r'^Appendix', line.strip()):
            end_idx = i
            break

    section = lines[start_idx:end_idx]

    # Remove page headers/footers
    cleaned = []
    skip_patterns = [
        r'^Page \d+ of \d+',
        r'^PCE Care Management v9\.4',
        r'^PCE Systems$',
        r'^(January|February|March|April|May|June|July|August|September|October|November|December) \d+, \d{4}$',
    ]
    for line in section:
        s = line.strip()
        if any(re.match(p, s) for p in skip_patterns):
            continue
        if '© 20' in line and 'PCE Systems' in line:
            continue
        cleaned.append(line)

    full_text = "\n".join(cleaned)

    # Split into entity blocks
    entity_positions = []
    for entity_name in KNOWN_ENTITIES:
        pattern = re.compile(r'^' + re.escape(entity_name) + r'\s*$', re.MULTILINE)
        match = pattern.search(full_text)
        if match:
            entity_positions.append((match.start(), match.end(), entity_name))
        else:
            print(f"WARNING: Could not find entity '{entity_name}'")

    entity_positions.sort(key=lambda x: x[0])

    entities = []
    for idx, (start, end, name) in enumerate(entity_positions):
        next_start = entity_positions[idx + 1][0] if idx + 1 < len(entity_positions) else len(full_text)
        block_text = full_text[end:next_start]
        block_lines = block_text.split("\n")

        # Split into description and table
        desc_lines = []
        table_lines = []
        table_found = False
        for i, bline in enumerate(block_lines):
            if re.match(r'\s*Attribute\s+Data Type', bline.strip()):
                table_found = True
                # Skip header line(s)
                j = i + 1
                while j < len(block_lines) and block_lines[j].strip() in ("Description", ""):
                    j += 1
                table_lines = block_lines[j:]
                break
            s = bline.strip()
            if s:
                desc_lines.append(s)

        description = " ".join(desc_lines)
        conforms_to = None
        cm = re.search(r'Conforms to the (US Core [\w\s\-().,]+Profile)', description)
        if cm:
            conforms_to = cm.group(1).strip()

        fields = parse_table_block(table_lines) if table_found else []

        entities.append({
            "name": name,
            "description": description,
            "conforms_to": conforms_to,
            "fields": fields
        })

    # Stats
    patient_entities = [e for e in entities if e["name"] not in UTILITY_TYPES]
    all_fields = sum(len(e["fields"]) for e in entities)
    patient_fields = sum(len(e["fields"]) for e in patient_entities)
    desc_count = sum(1 for e in entities for f in e["fields"] if f.get("description","").strip())
    typed_count = sum(1 for e in entities for f in e["fields"] if f.get("type","").strip())

    inventory = {
        "source": "PIX_9_4_API_Documentation.pdf",
        "source_type": "FHIR (g)(10) API documentation",
        "note": "The (b)(10) EHI export uses a separate, non-public data dictionary (documentation.json within export ZIP). This represents the FHIR API surface only.",
        "total_entities": len(entities),
        "patient_data_entities": len(patient_entities),
        "utility_types": len(entities) - len(patient_entities),
        "total_fields": all_fields,
        "total_patient_fields": patient_fields,
        "fields_with_descriptions": desc_count,
        "fields_with_types": typed_count,
        "entities": entities
    }

    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)

    summary = {
        "source": inventory["source"],
        "source_type": inventory["source_type"],
        "note": inventory["note"],
        "total_entities": len(entities),
        "patient_data_entities": len(patient_entities),
        "utility_types": len(entities) - len(patient_entities),
        "total_fields": all_fields,
        "total_patient_fields": patient_fields,
        "fields_with_descriptions": desc_count,
        "fields_with_types": typed_count,
        "entity_summary": [
            {
                "name": e["name"],
                "field_count": len(e["fields"]),
                "fields_with_descriptions": sum(1 for f in e["fields"] if f.get("description","").strip()),
                "conforms_to": e.get("conforms_to"),
                "is_utility": e["name"] in UTILITY_TYPES,
                "description": e["description"][:200]
            }
            for e in entities
        ]
    }

    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Total entities: {len(entities)}")
    print(f"  Patient data entities: {len(patient_entities)}")
    print(f"  Utility types: {len(entities) - len(patient_entities)}")
    print(f"Total fields: {all_fields}")
    print(f"  With descriptions: {desc_count}")
    print(f"  With types: {typed_count}")
    print()
    for e in entities:
        marker = " [utility]" if e["name"] in UTILITY_TYPES else ""
        print(f"  {e['name']}: {len(e['fields'])} fields{marker}")

if __name__ == "__main__":
    main()
