#!/usr/bin/env python3
"""Parse the EHI Export Documentation PDF and produce entity-inventory-full.json and summary."""

import json
import re
import subprocess
import sys

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/170.315b10-EHI-Export-Documentation.pdf", "-"],
    capture_output=True, text=True
)
text = result.stdout

# Parse sections: each starts with "2.X Section Name"
section_pattern = re.compile(r'^2\.(\d+)\s+(.+)$', re.MULTILINE)
sections = list(section_pattern.finditer(text))

# Verified schemas from careful PDF reading (fixing parsing issues)
KNOWN_SCHEMAS = {
    "Patient Demographics": [
        {"name": "Id", "type": "long", "description": "Unique identifier for each record in the table."},
        {"name": "ChartNumber", "type": "varchar", "description": "Unique identifier for the patient"},
        {"name": "FirstName", "type": "varchar", "description": None},
        {"name": "LastName", "type": "varchar", "description": None},
        {"name": "MiddleName", "type": "varchar", "description": None},
        {"name": "Suffix", "type": "varchar", "description": None},
        {"name": "PreviousName", "type": "varchar", "description": None},
        {"name": "DateofBirth", "type": "DateTime", "description": "yyyy/mm/dd"},
        {"name": "Race", "type": "varchar", "description": None},
        {"name": "Ethnicity", "type": "varchar", "description": None},
        {"name": "BirthSex", "type": "varchar", "description": None},
        {"name": "PreferredLanguage", "type": "varchar", "description": None},
        {"name": "CurrentAddress", "type": "varchar", "description": None},
        {"name": "PreviousAddress", "type": "varchar", "description": None},
        {"name": "PhoneNumber", "type": "varchar", "description": None},
        {"name": "PhoneNumberType", "type": "varchar", "description": None},
        {"name": "EmailAddress", "type": "varchar", "description": None},
    ],
    "Allergies": [
        {"name": "Id", "type": "long", "description": "Unique identifier for each record in the table."},
        {"name": "Substance", "type": "varchar", "description": None},
        {"name": "Reaction", "type": "varchar", "description": None},
        {"name": "Severity", "type": "varchar", "description": None},
        {"name": "Status", "type": "varchar", "description": None},
        {"name": "Non-Medication", "type": "varchar", "description": None},
    ],
    "Vitals": [
        {"name": "Id", "type": "long", "description": "Unique identifier for each record in the table."},
        {"name": "SystolicBloodPressure", "type": "numeric", "description": None},
        {"name": "DiastolicBloodPressure", "type": "numeric", "description": None},
        {"name": "HeartRate", "type": "numeric", "description": None},
        {"name": "RespiratoryRate", "type": "numeric", "description": None},
        {"name": "BodyTemperature", "type": "numeric", "description": None},
        {"name": "BodyHeight", "type": "numeric", "description": None},
        {"name": "BodyWeight", "type": "numeric", "description": None},
        {"name": "PulseOximetry", "type": "numeric", "description": None},
        {"name": "InhaledOxygenConcentration", "type": "numeric", "description": None},
        {"name": "BMIPercentile", "type": "varchar", "description": None},
        {"name": "Weight-for-lengthPercentile", "type": "numeric", "description": None},
        {"name": "HeadOccipital-frontalCircumferencePercentile", "type": "decimal", "description": None},
    ],
    "Problems": [
        {"name": "Id", "type": "long", "description": "Unique identifier for each record in the table."},
        {"name": "Problems", "type": "varchar", "description": None},
    ],
}

entities = []

for i, match in enumerate(sections):
    sec_num = match.group(1)
    sec_name = match.group(2).strip()
    start = match.end()
    end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
    block = text[start:end]

    # Manually define the known schema based on PDF verification.
    # The PDF layout causes parsing issues with column-aligned text, so we
    # define the verified structure directly from careful reading.
    fields = KNOWN_SCHEMAS.get(sec_name, [])
    if not fields:
        # Fallback: try to parse from text
        lines = block.split('\n')
        current_field = None
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith('Column') or stripped.startswith('DataType'):
                continue
            if stripped.startswith('Notes') or stripped.startswith('Table ') or stripped.startswith('PUBLIC') or stripped.startswith('Approved'):
                continue
            if re.match(r'^\d+ of \d+$', stripped) or stripped.startswith('American Medical') or stripped.startswith('Electronic Health'):
                continue
            field_match = re.match(
                r'\s{2,}(\S[\w&\-/\s]*?)\s{3,}(long|varchar|numeric|decimal|DateTime)\s*(.*)',
                line
            )
            if field_match:
                name = field_match.group(1).strip()
                dtype = field_match.group(2).strip()
                notes = field_match.group(3).strip()
                current_field = {"name": name, "type": dtype, "description": notes if notes else None}
                fields.append(current_field)

    entity = {
        "entity_name": sec_name,
        "section_number": f"2.{sec_num}",
        "field_count": len(fields),
        "fields": fields
    }
    entities.append(entity)

# Build full inventory
inventory = {
    "source": "170.315b10-EHI-Export-Documentation.pdf",
    "product": "Helios",
    "vendor": "American Medical Solutions, Inc.",
    "export_format": "CSV (ZIP archive)",
    "total_entities": len(entities),
    "total_fields": sum(e["field_count"] for e in entities),
    "entities": entities
}

# Count fields with descriptions
fields_with_desc = sum(
    1 for e in entities for f in e["fields"] if f.get("description")
)
inventory["fields_with_descriptions"] = fields_with_desc

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Build summary
summary = {
    "source": inventory["source"],
    "product": inventory["product"],
    "vendor": inventory["vendor"],
    "export_format": inventory["export_format"],
    "total_entities": inventory["total_entities"],
    "total_fields": inventory["total_fields"],
    "fields_with_descriptions": fields_with_desc,
    "pct_fields_with_descriptions": round(100 * fields_with_desc / inventory["total_fields"], 1) if inventory["total_fields"] > 0 else 0,
    "entities_summary": [
        {
            "entity_name": e["entity_name"],
            "section_number": e["section_number"],
            "field_count": e["field_count"],
            "fields_with_descriptions": sum(1 for f in e["fields"] if f.get("description")),
            "field_names": [f["name"] for f in e["fields"]]
        }
        for e in entities
    ]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary to stdout
print(f"Entities: {inventory['total_entities']}")
print(f"Total fields: {inventory['total_fields']}")
print(f"Fields with descriptions: {fields_with_desc} ({summary['pct_fields_with_descriptions']}%)")
print()
for e in entities:
    desc_count = sum(1 for f in e["fields"] if f.get("description"))
    print(f"  {e['section_number']} {e['entity_name']}: {e['field_count']} fields ({desc_count} with descriptions)")
    for f in e["fields"]:
        print(f"    - {f['name']} ({f['type']}){': ' + f['description'] if f.get('description') else ''}")
