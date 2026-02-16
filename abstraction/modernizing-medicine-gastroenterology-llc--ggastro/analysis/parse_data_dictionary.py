"""
Parses the gGastro EHI Patient Export Specifications PDF text (extracted via pdftotext -layout)
and produces entity-inventory-full.json and entity-inventory-summary.json.

Input: analysis/main-pdf-layout.txt
Output: analysis/entity-inventory-full.json, analysis/entity-inventory-summary.json
"""

import json
import re
import os
from collections import defaultdict

DIR = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(DIR, "main-pdf-layout.txt")
full_output = os.path.join(DIR, "entity-inventory-full.json")
summary_output = os.path.join(DIR, "entity-inventory-summary.json")

with open(input_file) as f:
    text = f.read()
lines = text.split("\n")


# ============================================================
# 1. Parse CSV Files Dictionary section
# ============================================================
def find_section(start_marker, end_marker, after_line=0):
    start = None
    for i, line in enumerate(lines):
        if i < after_line:
            continue
        if line.strip() == start_marker:
            start = i + 1
            break
    if start is None:
        return 0, len(lines)
    end = len(lines)
    for i in range(start, len(lines)):
        if lines[i].strip() == end_marker:
            end = i
            break
    return start, end


csv_start, csv_end = find_section("CSV Files Dictionary", "Data Schema", after_line=5)

# Known types in the document
KNOWN_TYPES = {"GUID", "Boolean", "Numeric", "Decimal", "Alphanumeric", "Date & Time", "Date", "Time", "Score", "XML"}

tables = []
current_table = None

# Some table names have spaces or special chars — need to handle "Column Number - Name" header lines
SKIP_LINES = {"Column Number - Name", "Type", "Length", "Format/Translation/Comments"}

i = csv_start
while i < csv_end:
    line = lines[i]
    trimmed = line.strip()
    i += 1

    if not trimmed:
        continue
    if trimmed in SKIP_LINES:
        continue

    # Field line: starts with digit(s) followed by " - "
    field_match = re.match(r'^(\d+)\s+-\s+(\S+)', trimmed)
    if field_match:
        idx = int(field_match.group(1))
        field_name = field_match.group(2)

        # Parse type from the rest of the line using column positions
        field_type = ""
        length = None
        format_translation = None

        # Search for known types in the line
        type_match = re.search(r'\s+(GUID|Boolean|Numeric|Decimal|Alphanumeric|Date & Time|Date|Time|Score|XML)\s*', line)
        if type_match:
            field_type = type_match.group(1)
            after = line[type_match.end():].strip()
            # Check for length (number at start)
            len_match = re.match(r'^(\d+)\s*(.*)', after)
            if len_match:
                length = int(len_match.group(1))
                rest = len_match.group(2).strip()
                if rest:
                    format_translation = rest
            elif after:
                format_translation = after

        # Handle multi-line format/translation (continuation lines)
        # Check if next line(s) are continuation (don't match field or table patterns)
        while i < csv_end:
            next_line = lines[i]
            next_trimmed = next_line.strip()
            if not next_trimmed:
                break
            if re.match(r'^\d+\s+-\s+\S+', next_trimmed):
                break
            if next_trimmed in SKIP_LINES:
                break
            # Check if it's a new table name
            if re.match(r'^[A-Z][a-zA-Z0-9]+$', next_trimmed) and next_trimmed not in KNOWN_TYPES:
                break
            # It's a continuation line
            if format_translation:
                format_translation += " " + next_trimmed
            else:
                format_translation = next_trimmed
            i += 1

        if current_table is not None:
            current_table["fields"].append({
                "index": idx,
                "name": field_name,
                "type": field_type,
                "length": length,
                "format_or_translation": format_translation,
            })
        continue

    # Table name line: PascalCase identifier not a type keyword
    if re.match(r'^[A-Z][a-zA-Z0-9]+$', trimmed) and trimmed not in KNOWN_TYPES:
        # Verify next non-empty line starts with "0 - " or "Column Number"
        is_table = False
        for j in range(i, min(i + 5, csv_end)):
            nt = lines[j].strip()
            if not nt:
                continue
            if nt.startswith("0 - ") or nt.startswith("Column Number"):
                is_table = True
            break

        if is_table:
            if current_table:
                tables.append(current_table)
            current_table = {"name": trimmed, "fields": [], "line_number": i}

if current_table:
    tables.append(current_table)


# ============================================================
# 2. Parse Data Schema (relationships)
# ============================================================
schema_start, schema_end = find_section("Data Schema", "Translations", after_line=100)
# Adjust: find "Translations" after schema_start
for si in range(schema_start, len(lines)):
    if lines[si].strip() == "Translations":
        schema_end = si
        break

relationships = []
table_stack = []

for i in range(schema_start, schema_end):
    line = lines[i]
    trimmed = line.strip()
    if not trimmed or trimmed in ("Related Tables", "Related Field"):
        continue

    match = re.match(r'^([\s|+\-]*?)(?:[|+]-{4,8})\s+(\S+)\s+(\S+)\s*$', line)
    if match:
        prefix = match.group(1)
        table_name = match.group(2)
        field_name = match.group(3)
        depth = prefix.count('|')

        parent = "Patient"
        if depth > 0 and len(table_stack) >= depth:
            parent = table_stack[depth - 1]

        table_stack = table_stack[:depth]
        table_stack.append(table_name)

        relationships.append({
            "parent": parent,
            "child": table_name,
            "foreign_key": field_name,
            "depth": depth,
        })


# ============================================================
# 3. Parse Translations (value sets)
# ============================================================
trans_start = schema_end
for ti in range(schema_end, len(lines)):
    if lines[ti].strip() == "Translations":
        trans_start = ti + 1
        break

trans_end = len(lines)
for ti in range(trans_start, len(lines)):
    if lines[ti].strip() == "Patient Documents":
        trans_end = ti
        break

translations = []
current_trans = None

for i in range(trans_start, trans_end):
    line = lines[i]
    trimmed = line.strip()

    if not trimmed:
        if current_trans and current_trans["entries"]:
            translations.append(current_trans)
            current_trans = None
        continue

    has_guid = bool(re.search(r'[0-9a-f]{8}-[0-9a-f]{4}', trimmed))
    has_numeric = bool(re.match(r'^\d+\s{2,}\S', trimmed))

    if not has_guid and not has_numeric and len(trimmed) < 120 and re.match(r'^[A-Z]', trimmed):
        if current_trans and current_trans["entries"]:
            translations.append(current_trans)
        current_trans = {"name": trimmed, "entries": []}
        continue

    if not current_trans:
        continue

    # GUID-based entries
    if has_guid:
        for m in re.finditer(
            r'([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}):\s*(.+?)(?=\s{2,}[0-9a-fA-F]{8}-|\s*$)',
            trimmed
        ):
            current_trans["entries"].append({"code": m.group(1), "value": m.group(2).strip()})
    else:
        # Numeric entries
        for m in re.finditer(r'(\d+)\s{2,}([A-Za-z][A-Za-z0-9 /\-&\(\)\'\.]*?)(?=\s{2,}\d|\s*$)', trimmed):
            current_trans["entries"].append({"code": m.group(1), "value": m.group(2).strip()})

if current_trans and current_trans["entries"]:
    translations.append(current_trans)


# ============================================================
# 4. Parse Glossary
# ============================================================
glossary = {}
glossary_start = 0
for i in range(len(lines) - 1, -1, -1):
    if lines[i].strip() == "Glossary":
        glossary_start = i + 1
        break

for i in range(glossary_start, len(lines)):
    trimmed = lines[i].strip()
    if not trimmed:
        continue
    match = re.match(r'^(\S[\S ]*?)\s{3,}(.+)$', lines[i])
    if match:
        glossary[match.group(1).strip()] = match.group(2).strip()


# ============================================================
# 5. Categorize tables by domain
# ============================================================
def categorize_table(name):
    """Heuristic categorization based on table name patterns."""
    name_lower = name.lower()

    # Billing / Financial
    billing_keywords = ["billing", "claim", "charge", "payment", "invoice", "superbill",
                        "copay", "adjustment", "revenue", "fee", "balance", "era",
                        "eligibility", "authorization", "patientaccountnumber"]
    if any(k in name_lower for k in billing_keywords):
        return "Billing & Financial"

    # Insurance
    if "insurance" in name_lower or "coverage" in name_lower or "payer" in name_lower:
        return "Insurance"

    # Scheduling / Appointments
    if "appointment" in name_lower or "schedule" in name_lower or "waitlist" in name_lower or "kiosk" in name_lower:
        return "Scheduling & Appointments"

    # Procedures / Endoscopy
    endo_keywords = ["procedure", "endoscop", "colonoscop", "biopsy", "polyp", "finding",
                     "sedation", "anesthesia", "aldrete", "recovery", "scope",
                     "servicephase", "servicecomponent", "serviceprocedure", "servicefinding",
                     "servicediagnos", "servicedocument", "servicetemplate", "servicerecovery"]
    if any(k in name_lower for k in endo_keywords):
        return "Procedures & Endoscopy"

    # Service (encounter) related
    if name_lower.startswith("service") or "encounter" in name_lower:
        return "Encounters & Services"

    # Labs & Results
    if "lab" in name_lower or "result" in name_lower or "specimen" in name_lower or "pathology" in name_lower:
        return "Labs & Results"

    # Medications
    if "medication" in name_lower or "prescription" in name_lower or "drug" in name_lower or "pharmacy" in name_lower or "administered" in name_lower:
        return "Medications"

    # Patient Demographics
    if name_lower.startswith("patient") or "person" in name_lower or "demographic" in name_lower or "address" in name_lower or "ethnicity" in name_lower or "race" in name_lower:
        return "Patient Demographics"

    # Clinical Notes / Documents
    if "document" in name_lower or "note" in name_lower or "addendum" in name_lower or "letter" in name_lower:
        return "Clinical Notes & Documents"

    # Vital Signs
    if "vital" in name_lower:
        return "Vital Signs"

    # Allergies
    if "allerg" in name_lower:
        return "Allergies"

    # Problems / Diagnoses
    if "problem" in name_lower or "diagnos" in name_lower or "condition" in name_lower:
        return "Problems & Diagnoses"

    # Immunizations
    if "immuniz" in name_lower or "vaccin" in name_lower:
        return "Immunizations"

    # Orders / Referrals
    if "order" in name_lower or "referral" in name_lower or "request" in name_lower:
        return "Orders & Referrals"

    # Tasks / Communications
    if "task" in name_lower or "message" in name_lower or "communication" in name_lower or "recall" in name_lower or "reminder" in name_lower:
        return "Tasks & Communications"

    # Care Plans / Goals
    if "careplan" in name_lower or "goal" in name_lower:
        return "Care Plans & Goals"

    # Templates / Configuration
    if "template" in name_lower or "config" in name_lower or "setting" in name_lower:
        return "Templates & Configuration"

    # Imaging
    if "image" in name_lower or "imaging" in name_lower:
        return "Imaging & Media"

    # GI-Specific / Registry
    if "aga" in name_lower or "registry" in name_lower or "quality" in name_lower:
        return "GI Registry & Quality"

    # Staff / Providers
    if "staff" in name_lower or "provider" in name_lower or "user" in name_lower:
        return "Staff & Providers"

    # Location / Facility
    if "location" in name_lower or "facility" in name_lower or "room" in name_lower:
        return "Locations & Facilities"

    # History
    if "history" in name_lower:
        return "History"

    # Consent / Legal
    if "consent" in name_lower or "directive" in name_lower:
        return "Consents & Directives"

    # Device
    if "device" in name_lower or "implant" in name_lower or "equipment" in name_lower:
        return "Devices & Equipment"

    # Telehealth
    if "telehealth" in name_lower:
        return "Telehealth"

    return "Other"


# ============================================================
# 6. Build outputs
# ============================================================

# Build relationship lookup
parent_to_children = defaultdict(list)
child_to_parent = {}
for rel in relationships:
    parent_to_children[rel["parent"]].append(rel["child"])
    child_to_parent[rel["child"]] = {"parent": rel["parent"], "foreign_key": rel["foreign_key"]}

# Build translation lookup (which tables reference which translations)
translation_lookup = {t["name"]: t for t in translations}

# Enrich tables with category and relationship info
enriched_tables = []
for table in tables:
    category = categorize_table(table["name"])
    parent_info = child_to_parent.get(table["name"])
    children = parent_to_children.get(table["name"], [])

    # Check which fields reference translations
    for field in table["fields"]:
        ft = field.get("format_or_translation", "")
        if ft and ft in translation_lookup:
            field["has_value_set"] = True
            field["value_set_name"] = ft
        else:
            field["has_value_set"] = False

    enriched_tables.append({
        "name": table["name"],
        "category": category,
        "field_count": len(table["fields"]),
        "fields": table["fields"],
        "parent": parent_info,
        "children": children,
        "line_number": table["line_number"],
    })


# Full inventory
full_inventory = {
    "metadata": {
        "source": "gGastro EHI Patient Export Specifications",
        "version": "6.5.3.20251230",
        "source_pdf": "gGastro-EHI-Patient-Export-Specifications.pdf",
        "extraction_date": "2026-02-16",
        "pages": 167,
    },
    "tables": enriched_tables,
    "relationships": relationships,
    "translations": translations,
    "glossary": glossary,
}

with open(full_output, "w") as f:
    json.dump(full_inventory, f, indent=2)


# ============================================================
# 7. Generate summary
# ============================================================
total_tables = len(enriched_tables)
total_fields = sum(t["field_count"] for t in enriched_tables)

# Fields with types
fields_with_types = sum(
    1 for t in enriched_tables for f in t["fields"] if f.get("type")
)

# Fields with format/translation
fields_with_format = sum(
    1 for t in enriched_tables for f in t["fields"]
    if f.get("format_or_translation")
)

# Fields with value sets
fields_with_value_sets = sum(
    1 for t in enriched_tables for f in t["fields"]
    if f.get("has_value_set")
)

# Fields with lengths
fields_with_lengths = sum(
    1 for t in enriched_tables for f in t["fields"]
    if f.get("length") is not None
)

# Category breakdown
category_stats = defaultdict(lambda: {"tables": 0, "fields": 0, "table_names": []})
for t in enriched_tables:
    cat = t["category"]
    category_stats[cat]["tables"] += 1
    category_stats[cat]["fields"] += t["field_count"]
    category_stats[cat]["table_names"].append(t["name"])

# Sort categories by field count desc
sorted_categories = sorted(category_stats.items(), key=lambda x: -x[1]["fields"])

# Tables with relationships
tables_with_parents = sum(1 for t in enriched_tables if t["parent"])
tables_with_children = sum(1 for t in enriched_tables if t["children"])

# Top 20 tables by field count
top_tables = sorted(enriched_tables, key=lambda t: -t["field_count"])[:20]

# Field type distribution
type_dist = defaultdict(int)
for t in enriched_tables:
    for f in t["fields"]:
        type_dist[f.get("type", "(unknown)")] += 1

summary = {
    "total_tables": total_tables,
    "total_fields": total_fields,
    "fields_with_types": fields_with_types,
    "fields_with_types_pct": round(100 * fields_with_types / total_fields, 1) if total_fields else 0,
    "fields_with_format_or_translation": fields_with_format,
    "fields_with_value_sets": fields_with_value_sets,
    "fields_with_lengths": fields_with_lengths,
    "total_relationships": len(relationships),
    "tables_with_parent_relationship": tables_with_parents,
    "tables_with_children": tables_with_children,
    "total_translation_tables": len(translations),
    "total_translation_entries": sum(len(t["entries"]) for t in translations),
    "glossary_terms": len(glossary),
    "field_type_distribution": dict(sorted(type_dist.items(), key=lambda x: -x[1])),
    "category_breakdown": [
        {
            "category": cat,
            "tables": stats["tables"],
            "fields": stats["fields"],
            "table_names": stats["table_names"],
        }
        for cat, stats in sorted_categories
    ],
    "top_20_tables_by_field_count": [
        {"name": t["name"], "fields": t["field_count"], "category": t["category"]}
        for t in top_tables
    ],
}

with open(summary_output, "w") as f:
    json.dump(summary, f, indent=2)


# Print summary
print(f"=== gGastro EHI Export Data Dictionary Summary ===")
print(f"Tables: {total_tables}")
print(f"Fields: {total_fields}")
print(f"Fields with types: {fields_with_types} ({summary['fields_with_types_pct']}%)")
print(f"Fields with format/translation: {fields_with_format}")
print(f"Fields with value sets: {fields_with_value_sets}")
print(f"Fields with lengths: {fields_with_lengths}")
print(f"Relationships: {len(relationships)}")
print(f"Translation tables: {len(translations)}")
print(f"Translation entries: {sum(len(t['entries']) for t in translations)}")
print(f"Glossary terms: {len(glossary)}")
print()
print("=== Category Breakdown ===")
for cat, stats in sorted_categories:
    print(f"  {cat}: {stats['tables']} tables, {stats['fields']} fields")
print()
print("=== Top 20 Tables by Field Count ===")
for t in top_tables:
    print(f"  {t['name']}: {t['field_count']} fields [{t['category']}]")
