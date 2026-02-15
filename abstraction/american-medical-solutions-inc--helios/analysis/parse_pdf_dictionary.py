#!/usr/bin/env python3
"""Parse the EHI export PDF data dictionary and produce structured inventory."""

import json
import re
import subprocess
import sys

PDF_PATH = "../../../results/american-medical-solutions-inc/downloads/170.315b10-EHI-Export-Documentation.pdf"

# Extract text from PDF
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Parse sections by looking for "2.X SectionName" pattern
section_pattern = re.compile(r"^2\.(\d+)\s+(.+)$", re.MULTILINE)
sections = []

matches = list(section_pattern.finditer(text))
for i, m in enumerate(matches):
    sec_num = m.group(1)
    sec_name = m.group(2).strip()
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    block = text[start:end]

    # Extract column names from the table rows
    # Columns appear as first word/phrase in table rows, followed by DataType
    # Look for lines with column names followed by type keywords
    fields = []
    col_pattern = re.compile(
        r"^\s{5,}(\S[\w\s/&|()-]*?)\s{3,}(long|varchar|numeric|decimal|DateTime)\b",
        re.MULTILINE,
    )
    for cm in col_pattern.finditer(block):
        field_name = cm.group(1).strip().rstrip("|")
        field_type = cm.group(2).strip()
        # Check if there's a note after the type
        rest_of_line = block[cm.end():].split("\n")[0].strip()
        note = rest_of_line if rest_of_line else ""
        # Also check the next line for continuation of notes
        next_lines = block[cm.end():].split("\n")[1:3]
        for nl in next_lines:
            nl_stripped = nl.strip()
            if nl_stripped and not col_pattern.match(nl) and not nl_stripped.startswith("Table"):
                if not any(kw in nl_stripped.lower() for kw in ["column", "datatype", "notes", "public", "approved"]):
                    if note:
                        note += " " + nl_stripped
                    else:
                        note = nl_stripped
            else:
                break

        fields.append({
            "name": field_name,
            "type": field_type,
            "note": note if note else None,
        })

    sections.append({
        "section_number": f"2.{sec_num}",
        "name": sec_name,
        "field_count": len(fields),
        "fields": fields,
        "fields_with_notes": sum(1 for f in fields if f["note"]),
        "fields_without_notes": sum(1 for f in fields if not f["note"]),
    })

# Summary stats
total_fields = sum(s["field_count"] for s in sections)
total_with_notes = sum(s["fields_with_notes"] for s in sections)
# Unique non-trivial notes (excluding the repeated Id description)
unique_notes = set()
for s in sections:
    for f in s["fields"]:
        if f["note"] and f["name"] != "Id":
            unique_notes.add(f["note"])

summary = {
    "total_sections": len(sections),
    "total_fields": total_fields,
    "fields_with_notes": total_with_notes,
    "fields_without_notes": total_fields - total_with_notes,
    "unique_non_id_notes": len(unique_notes),
    "non_id_note_texts": sorted(unique_notes),
    "sections": sections,
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Sections: {len(sections)}")
print(f"Total fields: {total_fields}")
print(f"Fields with notes: {total_with_notes}")
print(f"Fields without notes: {total_fields - total_with_notes}")
print(f"Unique non-Id notes: {len(unique_notes)}")
print()
for s in sections:
    print(f"  {s['section_number']} {s['name']}: {s['field_count']} fields ({s['fields_with_notes']} with notes)")
    for f in s["fields"]:
        note_str = f" -- {f['note']}" if f["note"] else ""
        print(f"    - {f['name']} ({f['type']}){note_str}")
