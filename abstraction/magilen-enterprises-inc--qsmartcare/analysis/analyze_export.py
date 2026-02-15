"""
Analyze QSmartCare EHI export sample files (PDF and JSON).
Produces structured inventory of sections, fields, and discrepancies.
"""

import json
import re
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/magilen-enterprises-inc--qsmartcare/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/magilen-enterprises-inc--qsmartcare/analysis"

# ── Analyze JSON sample ──
with open(os.path.join(RESULTS_DIR, "sample-ehi-export.json"), "r") as f:
    data = json.load(f)

org = data["object"]["organization"]

def count_fields(obj, prefix=""):
    """Recursively count leaf fields in a JSON object."""
    count = 0
    fields = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                sub_count, sub_fields = count_fields(v, f"{prefix}.{k}" if prefix else k)
                count += sub_count
                fields.extend(sub_fields)
            else:
                count += 1
                fields.append(f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            sub_count, sub_fields = count_fields(item, f"{prefix}[{i}]")
            count += sub_count
            fields.extend(sub_fields)
    else:
        count = 1
        fields = [prefix]
    return count, fields

# Top-level sections in the JSON
json_sections = {}
for key, value in org.items():
    if key in ("resourceType", "identifier", "active", "type", "name", "alias",
               "phoneNumber", "repository"):
        continue
    if key == "address" and not isinstance(value, dict) or (isinstance(value, dict) and "resourceType" not in value and key == "address"):
        json_sections["organization_address"] = {"resourceType": "OrganizationAddress", "fields": count_fields(value)}
        continue
    rt = value.get("resourceType", key) if isinstance(value, dict) else key
    fc, fl = count_fields(value)
    json_sections[key] = {
        "resourceType": rt,
        "field_count": fc,
        "fields": fl
    }

print("=" * 60)
print("JSON EXPORT ANALYSIS")
print("=" * 60)
print(f"\nTotal top-level keys in organization: {len(org.keys())}")
print(f"\nSections with resourceType or structured data:")
total_fields = 0
for key, info in json_sections.items():
    rt = info.get("resourceType", key)
    fc = info.get("field_count", info.get("fields", (0,))[0] if isinstance(info.get("fields"), tuple) else len(info.get("fields", [])))
    total_fields += fc
    print(f"  {key:25s} resourceType={rt:30s} fields={fc}")

print(f"\nTotal leaf fields across all sections: {total_fields}")

# ── Analyze PDF sections ──
pdf_text_file = os.path.join(OUTPUT_DIR, "pdf_text.txt")
os.system(f"pdftotext -layout '{os.path.join(RESULTS_DIR, 'Single-Patient-PDF-Download.pdf')}' '{pdf_text_file}' 2>/dev/null")

with open(pdf_text_file, "r") as f:
    pdf_text = f.read()

# Find all section headers (ALL CAPS followed by INFO or HISTORIES or IMMUNIZATION etc.)
section_pattern = r'^[ \t]*([A-Z][A-Z\s/]+(?:INFO|HISTORIES|IMMUNIZATION|STATUS))\s*$'
pdf_sections = re.findall(section_pattern, pdf_text, re.MULTILINE)
pdf_sections = [s.strip() for s in pdf_sections]

print("\n" + "=" * 60)
print("PDF EXPORT ANALYSIS")
print("=" * 60)
print(f"\nPages: 7")
print(f"\nSections found in PDF ({len(pdf_sections)}):")
for s in pdf_sections:
    print(f"  - {s}")

# ── Discrepancy analysis: PDF sections vs JSON sections ──
print("\n" + "=" * 60)
print("PDF vs JSON DISCREPANCY ANALYSIS")
print("=" * 60)

pdf_only = [
    "INSURANCE INFO",
    "SPOUSE INFO",
    "PATIENT RELATIONSHIP INFO",
    "PAST MEDICAL HISTORY INFO",
    "ANTICOAGULANT INFO",
    "LAB INFO",
    "BLOOD SUGAR INFO",
    "BLOOD PRESSURE INFO",
    "BMI INFO",
    "PULSE INFO",
    "PULSE OXIMETRY INFO",
    "BODY TEMPERATURE INFO",
    "HEART RATE INFO",
    "RESPIRATORY RATE INFO",
    "OXYGEN CONCENTRATION INFO",
    "FUNCTIONAL STATUS",
    "COGNITIVE STATUS",
]

json_only = [
    "goals",
    "healthConcerns",
    "assessments",
]

print("\nSections in PDF but NOT in JSON:")
for s in pdf_only:
    print(f"  ❌ {s}")

print(f"\nSections in JSON but NOT in PDF:")
for s in json_only:
    print(f"  ❌ {s}")

print(f"\nTotal PDF-only sections: {len(pdf_only)}")
print(f"Total JSON-only sections: {len(json_only)}")

# ── JSON quality issues ──
print("\n" + "=" * 60)
print("JSON QUALITY ISSUES")
print("=" * 60)

null_string_count = 0
empty_string_count = 0
numbered_key_count = 0

def find_issues(obj, path=""):
    global null_string_count, empty_string_count, numbered_key_count
    if isinstance(obj, dict):
        for k, v in obj.items():
            if re.match(r'.*\d+$', k) and not k.startswith('urn'):
                numbered_key_count += 1
            find_issues(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_issues(item, f"{path}[{i}]")
    elif isinstance(obj, str):
        if obj == "null":
            null_string_count += 1
        elif obj == "":
            empty_string_count += 1

find_issues(data)
print(f'String "null" values: {null_string_count}')
print(f'Empty string values: {empty_string_count}')
print(f'Numbered key patterns (e.g., codeSystemICD100): {numbered_key_count}')

# ── Save full inventory as JSON ──
inventory = {
    "json_analysis": {
        "total_sections": len(json_sections),
        "sections": {k: {"resourceType": v.get("resourceType", k), "field_count": v.get("field_count", 0)} for k, v in json_sections.items()},
        "quality_issues": {
            "string_null_values": null_string_count,
            "empty_string_values": empty_string_count,
            "numbered_key_patterns": numbered_key_count,
        }
    },
    "pdf_analysis": {
        "pages": 7,
        "total_sections": len(pdf_sections),
        "sections": pdf_sections,
    },
    "discrepancies": {
        "pdf_only_sections": pdf_only,
        "json_only_sections": json_only,
    }
}

with open(os.path.join(OUTPUT_DIR, "export-inventory.json"), "w") as f:
    json.dump(inventory, f, indent=2)

print(f"\n✅ Full inventory saved to {os.path.join(OUTPUT_DIR, 'export-inventory.json')}")
