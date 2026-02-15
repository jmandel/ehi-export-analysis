#!/usr/bin/env python3
"""Parse the MDVita EHI Export Data Format PDF text to extract
entity/field counts and descriptions."""

import re
import json

with open("pdf_text.txt", "r") as f:
    text = f.read()

# Split by section headers like "3. Data file. Patients"
section_pattern = re.compile(
    r'(\d+)\.\s+Data\s+file\.\s+(\w+)\s*\n', re.IGNORECASE
)

sections = []
matches = list(section_pattern.finditer(text))

for i, m in enumerate(matches):
    section_num = int(m.group(1))
    entity_name = m.group(2)
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    section_text = text[start:end]
    sections.append({
        "section_num": section_num,
        "entity": entity_name,
        "text": section_text
    })

# Parse columns from each section
# Column lines typically look like:
#  ColumnName    DataType    Description
column_pattern = re.compile(
    r'^\s+(\w+)\s+(Numeric|String|DateTime|Boolean|Date|string)\s+(.+?)$',
    re.MULTILINE | re.IGNORECASE
)

results = []
total_fields = 0
total_described = 0

for sec in sections:
    entity = sec["entity"]
    cols = column_pattern.findall(sec["text"])
    
    fields = []
    for col_name, data_type, desc in cols:
        # Skip header/footer noise
        if col_name in ("Page", "Information", "Health", "Email"):
            continue
        desc = desc.strip()
        has_description = len(desc) > 0 and desc.lower() != col_name.lower()
        fields.append({
            "name": col_name,
            "type": data_type,
            "description": desc,
            "has_description": has_description
        })
    
    field_count = len(fields)
    described_count = sum(1 for f in fields if f["has_description"])
    has_types = all(f["type"] for f in fields)
    
    total_fields += field_count
    total_described += described_count
    
    results.append({
        "entity": entity,
        "section_num": sec["section_num"],
        "field_count": field_count,
        "described_count": described_count,
        "has_types": has_types,
        "fields": fields
    })

# Categorize entities by domain
domain_map = {
    "Patients": "Demographics",
    "ProviderNetwork": "Provider Reference",
    "ProviderPCPs": "Provider Reference",
    "Locations": "Provider Reference",
    "PatientPlans": "Insurance / Coverage",
    "Appointments": "Encounters / Visits",
    "SOAPNotesIndex": "Clinical Notes",
    "Orders": "Orders / Referrals",
    "ProblemList": "Problems / Diagnoses",
    "Allergies": "Allergies",
    "MedicationList": "Medications",
    "ProcedureList": "Procedures",
    "DocumentsIndex": "Documents",
    "LabResults": "Lab Results",
    "Claims": "Claims / Billing",
    "Referrals": "Orders / Referrals",
    "Emails": "Communications",
    "Immunizations": "Immunizations",
    "Vitals": "Vitals",
    "DocumentSignatures": "Documents",
    "ClaimsInsurancePayments": "Claims / Billing",
    "MemberCharges": "Claims / Billing",
    "MemberPayments": "Payments",
    "DocumentAnnotations": "Documents",
}

for r in results:
    r["domain"] = domain_map.get(r["entity"], "Unknown")

# Summary stats
print("=" * 70)
print("MDVita EHI Export Data Dictionary Summary")
print("=" * 70)
print(f"Total entities: {len(results)}")
print(f"Total fields:   {total_fields}")
print(f"Fields with descriptions: {total_described} ({100*total_described/total_fields:.0f}%)")
print()

# By domain
print("\nDomain Breakdown:")
print(f"{'Domain':<30} {'Entities':>10} {'Fields':>10}")
print("-" * 52)
domain_summary = {}
for r in results:
    d = r["domain"]
    if d not in domain_summary:
        domain_summary[d] = {"entities": 0, "fields": 0}
    domain_summary[d]["entities"] += 1
    domain_summary[d]["fields"] += r["field_count"]

for d, s in sorted(domain_summary.items()):
    print(f"{d:<30} {s['entities']:>10} {s['fields']:>10}")

print()
print("\nEntity Detail:")
print(f"{'Entity':<30} {'Fields':>8} {'Described':>10} {'Types':>8} {'Domain':<25}")
print("-" * 85)
for r in results:
    print(f"{r['entity']:<30} {r['field_count']:>8} {r['described_count']:>10} {'yes' if r['has_types'] else 'no':>8} {r['domain']:<25}")

# Save full inventory as JSON
output = {
    "summary": {
        "total_entities": len(results),
        "total_fields": total_fields,
        "fields_with_descriptions": total_described,
        "description_pct": round(100 * total_described / total_fields, 1),
        "domain_breakdown": domain_summary,
    },
    "entities": [{k: v for k, v in r.items()} for r in results]
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(output, f, indent=2)
    
print("\nSaved full-entity-inventory.json")
