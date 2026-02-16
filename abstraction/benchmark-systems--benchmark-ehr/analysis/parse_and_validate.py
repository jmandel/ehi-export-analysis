#!/usr/bin/env python3
"""
Parse the Benchmark EHR (b)(10) PDF export schema independently.
Validates against the pre-existing enrichment JSON and produces:
  - full-entity-inventory.json (complete field-level extraction)
  - entity-summary.txt (human-readable summary stats)
"""

import json
import re
import sys
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/benchmark-systems--benchmark-ehr")
ANALYSIS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/benchmark-systems--benchmark-ehr/analysis")

# Read the full PDF text
pdf_text = (ANALYSIS_DIR / "pdf-full-text.txt").read_text()

# Read the pre-existing enrichment JSON for comparison
enrichment = json.loads((RESULTS_DIR / "downloads/enrichment/benchmark-ehr-export-schema.json").read_text())

# Strip page headers/footers
pdf_text = re.sub(r'\n\s*147 Crossings Centre Drive.*?\n', '\n', pdf_text)
pdf_text = re.sub(r'\n\s*§170\.315\(b\)\(10\).*?Document\n', '\n', pdf_text)
pdf_text = re.sub(r'\n\s*\d+\s*\n', '\n', pdf_text)  # standalone page numbers

# Normalize smart quotes
pdf_text = pdf_text.replace('\u201c', '"').replace('\u201d', '"')
pdf_text = pdf_text.replace('\u2019', "'").replace('\u2018', "'")

# Find the "Detailed Description" section - use the second occurrence (first is TOC)
detail_positions = [m.start() for m in re.finditer("Detailed Description of the Data Export Contents", pdf_text)]
if len(detail_positions) < 2:
    detail_start = detail_positions[0] if detail_positions else -1
else:
    detail_start = detail_positions[1]  # Skip TOC entry

if detail_start == -1:
    print("ERROR: Could not find 'Detailed Description' section")
    sys.exit(1)

detail_text = pdf_text[detail_start:]

# Parse numbered entities (1-47) - match lines starting with 1-2 digit number followed by entity name
# Only match entities with proper names (capitalized words), not regulation text
entity_pattern = re.compile(r'^\s{0,4}(\d{1,2})\.\s+([A-Z][A-Za-z][\w\s]+?)$', re.MULTILINE)
matches = list(entity_pattern.finditer(detail_text))

# Filter: only keep matches where numbers go 1-47 sequentially (or close)
# and names look like entity names
filtered_matches = []
for m in matches:
    num = int(m.group(1))
    name = m.group(2).strip()
    # Skip if it looks like regulatory text
    if any(kw in name.lower() for kw in ['electronic health', 'enable a user', 'execute this', 
                                           'the export', 'documentation']):
        continue
    filtered_matches.append(m)

matches = filtered_matches

entities = []
billing_names = {"Billing Ledger", "Billing Claims", "Billing Charges", "Patient Advance", "Statements"}

for i, match in enumerate(matches):
    num = int(match.group(1))
    name = match.group(2).strip()
    
    # Get text until next entity or end
    start = match.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(detail_text)
    body = detail_text[start:end]
    
    # Extract description (text before field list)
    desc_match = re.search(r'Exported field list is', body)
    if desc_match:
        description = body[:desc_match.start()].strip()
    else:
        description = body.strip()
    
    # Clean up description
    description = re.sub(r'\s+', ' ', description).strip()
    
    # Extract fields from quoted field lists
    fields = []
    # Find all quoted strings that look like field lists
    quoted_blocks = re.findall(r'"([^"]+)"', body)
    for block in quoted_blocks:
        # Split by comma, strip whitespace
        raw_fields = [f.strip().rstrip('.') for f in block.split(',')]
        for f in raw_fields:
            f = f.strip()
            if f and re.match(r'^[A-Z][A-Z0-9_]+$', f):
                fields.append(f)
    
    # Determine if has file attachments
    has_attachments = bool(re.search(r'(\.pdf|file.*path|FILE|attached.*document|document.*attached)', body, re.IGNORECASE))
    
    # Determine billing-only
    is_billing = name in billing_names
    
    # Extract any notes about constraints
    notes = []
    if re.search(r'active\s+(only|patient|medic)', body, re.IGNORECASE):
        notes.append("Active records only")
    if re.search(r'latest\s+encounter', body, re.IGNORECASE):
        notes.append("Latest encounter only")
    if re.search(r'deleted\s+encounter', body, re.IGNORECASE):
        notes.append("Option to include deleted encounters")
    if re.search(r'billing.*turned on|when billing', body, re.IGNORECASE):
        notes.append("Requires billing module")
    
    entity = {
        "number": num,
        "name": name,
        "description": description,
        "field_count": len(fields),
        "fields": [{"name": f, "index": idx} for idx, f in enumerate(fields)],
        "has_file_attachments": has_attachments,
        "billing_only": is_billing,
        "notes": notes
    }
    entities.append(entity)

# Build category assignments
categories = {}
for e in entities:
    name = e["name"]
    if e["billing_only"]:
        cat = "Billing"
    elif name in {"Insurance Master", "Medics", "Referring Doctor", "Adjusters", "Attorneys", 
                   "Employers", "Guarantor"}:
        cat = "Reference/Administrative"
    elif name in {"Patient Demographics", "Patient Insurance", "Patient Cases", "Patient Notes", 
                   "Patient Alert"}:
        cat = "Patient Administrative"
    elif name in {"Legal Documents", "Other Documents", "Enc Attach Docs", "Old Progress Notes", 
                   "Letters", "Messages"}:
        cat = "Documents & Correspondence"
    elif name in {"Enc Progress Notes", "Procedure Notes", "CCD"}:
        cat = "Clinical Notes"
    elif name in {"Vaccination", "Health Maintenance", "Family History", "Past Medical Hist", 
                   "Surgery", "Allergy", "Current Medication", "Social History"}:
        cat = "Patient Clinical History"
    elif name in {"Vitals", "All Vitals", "Diagnosis Code", "CPT Codes", "HCPC Codes"}:
        cat = "Clinical Encounter Data"
    elif name in {"Prescriptions"}:
        cat = "Medications"
    elif name in {"Lab Results", "Lab Test Result Values", "Rad Results"}:
        cat = "Results"
    elif name in {"Procedure Orders", "Consults"}:
        cat = "Orders & Referrals"
    elif name in {"Future Appointments", "Past Appointments"}:
        cat = "Scheduling"
    else:
        cat = "Other"
    e["category"] = cat

# Summary statistics
total_fields = sum(e["field_count"] for e in entities)
entities_with_fields = sum(1 for e in entities if e["field_count"] > 0)
entities_without_fields = sum(1 for e in entities if e["field_count"] == 0)

# Compare with enrichment JSON
enrichment_entities = enrichment["entities"]
print("=== VALIDATION AGAINST ENRICHMENT JSON ===")
print(f"Our parse: {len(entities)} entities, {total_fields} total fields")
print(f"Enrichment: {enrichment['entity_count']} entities, {enrichment['total_field_count']} total fields")
print()

discrepancies = []
for our_e in entities:
    match = [e for e in enrichment_entities if e["number"] == our_e["number"]]
    if not match:
        discrepancies.append(f"Entity #{our_e['number']} '{our_e['name']}' not found in enrichment")
        continue
    enr_e = match[0]
    enr_field_count = len(enr_e["fields"]) if isinstance(enr_e["fields"], list) else 0
    if our_e["field_count"] != enr_field_count:
        discrepancies.append(
            f"Entity #{our_e['number']} '{our_e['name']}': "
            f"our={our_e['field_count']} fields vs enrichment={enr_field_count} fields"
        )

if discrepancies:
    print("DISCREPANCIES:")
    for d in discrepancies:
        print(f"  - {d}")
else:
    print("No discrepancies found — all field counts match.")

print()

# Category breakdown
print("=== CATEGORY BREAKDOWN ===")
cat_stats = {}
for e in entities:
    cat = e["category"]
    if cat not in cat_stats:
        cat_stats[cat] = {"entities": 0, "fields": 0}
    cat_stats[cat]["entities"] += 1
    cat_stats[cat]["fields"] += e["field_count"]

for cat, stats in sorted(cat_stats.items()):
    print(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields")

print()
print(f"Total: {len(entities)} entities, {total_fields} fields")
print(f"Entities with field lists: {entities_with_fields}")
print(f"Entities without field lists: {entities_without_fields}")

# Entities without fields
print("\n=== ENTITIES WITHOUT EXPLICIT FIELD LISTS ===")
for e in entities:
    if e["field_count"] == 0:
        print(f"  #{e['number']} {e['name']}: {e['description'][:100]}...")

# Build the full inventory JSON
inventory = {
    "source": "b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf",
    "product": "Benchmark EHR",
    "version": "Denali 3.1",
    "parse_date": "2026-02-16",
    "summary": {
        "total_entities": len(entities),
        "entities_with_fields": entities_with_fields,
        "entities_without_fields": entities_without_fields,
        "total_fields": total_fields,
        "fields_with_descriptions": 0,  # PDF doesn't provide per-field descriptions
        "fields_with_types": 0,  # PDF doesn't provide data types
    },
    "category_breakdown": {
        cat: stats for cat, stats in sorted(cat_stats.items())
    },
    "entities": entities
}

# Save
out_path = ANALYSIS_DIR / "full-entity-inventory.json"
out_path.write_text(json.dumps(inventory, indent=2))
print(f"\nSaved full inventory to {out_path}")

# Also save a summary text
summary_lines = [
    "Benchmark EHR (b)(10) Export Schema Summary",
    "=" * 50,
    f"Source: {inventory['source']}",
    f"Product: {inventory['product']} v{inventory['version']}",
    f"Total entities: {len(entities)}",
    f"Entities with field lists: {entities_with_fields}",
    f"Entities without field lists: {entities_without_fields}",
    f"Total fields: {total_fields}",
    f"Fields with descriptions: 0 (not provided per-field)",
    f"Fields with data types: 0 (not provided)",
    "",
    "Category Breakdown:",
]
for cat, stats in sorted(cat_stats.items()):
    summary_lines.append(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields")

summary_lines.extend(["", "Top 15 Entities by Field Count:"])
for e in sorted(entities, key=lambda x: x["field_count"], reverse=True)[:15]:
    summary_lines.append(f"  {e['name']}: {e['field_count']} fields ({e['category']})")

summary_lines.extend(["", "Entities Without Field Lists:"])
for e in entities:
    if e["field_count"] == 0:
        summary_lines.append(f"  #{e['number']} {e['name']}")

summary_path = ANALYSIS_DIR / "entity-summary.txt"
summary_path.write_text("\n".join(summary_lines))
print(f"Saved summary to {summary_path}")
