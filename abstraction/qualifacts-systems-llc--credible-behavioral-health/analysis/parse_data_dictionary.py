"""
Parse the Credible Behavioral Health data dictionary JSON and produce:
1. Summary statistics (entity count, field count, description quality)
2. Per-entity inventory with field counts and metadata
3. Domain categorization based on entity names
4. Data type distribution
5. Description quality analysis (tautological vs meaningful)
"""

import json
import re
from collections import Counter, defaultdict

INPUT = "../../../results/qualifacts-systems-llc--credible-behavioral-health/downloads/data-dictionary.json"
OUTPUT_INVENTORY = "full-entity-inventory.json"
OUTPUT_STATS = "data-dictionary-stats.txt"

with open(INPUT) as f:
    entities = json.load(f)

# --- Basic counts ---
total_entities = len(entities)
total_fields = sum(e["fieldCount"] for e in entities)
total_fields_actual = sum(len(e["fields"]) for e in entities)

# --- Description quality ---
def is_tautological(field_name, description):
    """Check if description just restates the field name."""
    if not description:
        return True
    fn = field_name.lower().strip()
    desc = description.lower().strip()
    # Exact match or trivially derived
    if fn == desc:
        return True
    # "Field Name" -> "Field Name" (with minor variations)
    fn_normalized = re.sub(r'[^a-z0-9]', '', fn)
    desc_normalized = re.sub(r'[^a-z0-9]', '', desc)
    if fn_normalized == desc_normalized:
        return True
    # Description is just "The <field name>"
    if desc.startswith("the ") and re.sub(r'[^a-z0-9]', '', desc[4:]) == fn_normalized:
        return True
    # Field name + "identifier" variations
    if desc in [fn + " identifier", fn + " id", fn + " number"]:
        return True
    return False

fields_with_description = 0
fields_tautological = 0
fields_meaningful = 0
fields_no_description = 0
fields_with_example = 0
all_data_types = Counter()
nullable_count = 0
non_nullable_count = 0

for entity in entities:
    for field in entity["fields"]:
        all_data_types[field.get("dataType", "unknown")] += 1
        
        if field.get("isNullable"):
            nullable_count += 1
        else:
            non_nullable_count += 1
        
        if field.get("exampleValue"):
            fields_with_example += 1
        
        desc = field.get("description", "")
        if desc and desc.strip():
            fields_with_description += 1
            if is_tautological(field["fieldName"], desc):
                fields_tautological += 1
            else:
                fields_meaningful += 1
        else:
            fields_no_description += 1

# --- Domain categorization ---
domain_keywords = {
    "Demographics / Profile": ["profile", "contact", "family", "education", "previous address", "previous full name", "geo area", "organization", "location"],
    "Clinical": ["allerg", "diagnosis", "immunization", "implantable", "medical profile", "lab", "clinical", "vital", "overview image", "procedure"],
    "Medications / Prescribing": ["medication", "erx", "emar"],
    "Billing / Financial": ["claim", "payment", "liability", "insurance", "payer", "statement", "277", "bed board billing", "funding"],
    "Treatment Planning / BH": ["treatment plan", "credible plan", "care plan", "care team", "asam", "questionnaire", "outcome", "episode"],
    "Notes / Documentation": ["note", "amendment", "warning"],
    "Visits / Encounters": ["visit service", "encounter", "scheduler"],
    "Residential / Facility": ["bed board", "foster home"],
    "Communication / Messaging": ["messaging", "notification", "portal", "direct sent", "direct received", "eligibility message"],
    "Administrative / Other": ["authorization", "order", "enrollment", "eligibility", "employee", "link", "attachment", "external provider", "record access", "834", "masshiway"],
}

def categorize_entity(name):
    name_lower = name.lower()
    for domain, keywords in domain_keywords.items():
        for kw in keywords:
            if kw in name_lower:
                return domain
    return "Administrative / Other"

domain_stats = defaultdict(lambda: {"entities": [], "field_count": 0})

entity_inventory = []
for entity in entities:
    domain = categorize_entity(entity["entityName"])
    
    desc_meaningful = 0
    desc_tautological = 0
    desc_missing = 0
    for field in entity["fields"]:
        desc = field.get("description", "")
        if not desc or not desc.strip():
            desc_missing += 1
        elif is_tautological(field["fieldName"], desc):
            desc_tautological += 1
        else:
            desc_meaningful += 1
    
    entry = {
        "entityName": entity["entityName"],
        "fileName": entity["fileName"],
        "fieldCount": entity["fieldCount"],
        "actualFieldCount": len(entity["fields"]),
        "isCustomOnly": entity.get("isCustomOnly", False),
        "hasCustomFields": entity.get("hasCustomFields", False),
        "domain": domain,
        "descriptionsTotal": desc_meaningful + desc_tautological,
        "descriptionsMeaningful": desc_meaningful,
        "descriptionsTautological": desc_tautological,
        "descriptionsMissing": desc_missing,
    }
    entity_inventory.append(entry)
    
    domain_stats[domain]["entities"].append(entity["entityName"])
    domain_stats[domain]["field_count"] += len(entity["fields"])

# Sort inventory by field count descending
entity_inventory.sort(key=lambda x: x["actualFieldCount"], reverse=True)

# --- Custom fields entities ---
custom_only = [e for e in entities if e.get("isCustomOnly")]
has_custom = [e for e in entities if e.get("hasCustomFields") and not e.get("isCustomOnly")]

# --- Output stats ---
stats_lines = []
stats_lines.append("=" * 70)
stats_lines.append("CREDIBLE BEHAVIORAL HEALTH - DATA DICTIONARY ANALYSIS")
stats_lines.append("=" * 70)
stats_lines.append("")
stats_lines.append(f"Total entities:           {total_entities}")
stats_lines.append(f"Total fields (declared):  {total_fields}")
stats_lines.append(f"Total fields (actual):    {total_fields_actual}")
stats_lines.append("")
stats_lines.append("--- Description Quality ---")
stats_lines.append(f"Fields with description:  {fields_with_description} ({fields_with_description*100//total_fields_actual}%)")
stats_lines.append(f"  Meaningful:             {fields_meaningful} ({fields_meaningful*100//total_fields_actual}%)")
stats_lines.append(f"  Tautological:           {fields_tautological} ({fields_tautological*100//total_fields_actual}%)")
stats_lines.append(f"Fields without desc:      {fields_no_description} ({fields_no_description*100//total_fields_actual}%)")
stats_lines.append(f"Fields with example:      {fields_with_example} ({fields_with_example*100//total_fields_actual}%)")
stats_lines.append("")
stats_lines.append("--- Nullability ---")
stats_lines.append(f"Nullable:                 {nullable_count}")
stats_lines.append(f"Non-nullable:             {non_nullable_count}")
stats_lines.append("")
stats_lines.append("--- Data Types ---")
for dt, count in all_data_types.most_common():
    stats_lines.append(f"  {dt:20s}  {count:4d}")
stats_lines.append("")
stats_lines.append("--- Custom Fields ---")
stats_lines.append(f"Custom-only entities:     {len(custom_only)} ({', '.join(e['entityName'] for e in custom_only)})")
stats_lines.append(f"Entities with custom:     {len(has_custom)} ({', '.join(e['entityName'] for e in has_custom)})")
stats_lines.append("")
stats_lines.append("--- Domain Breakdown ---")
stats_lines.append(f"{'Domain':<35} {'Entities':>8} {'Fields':>8}")
stats_lines.append("-" * 55)
for domain in sorted(domain_stats.keys()):
    ds = domain_stats[domain]
    stats_lines.append(f"{domain:<35} {len(ds['entities']):>8} {ds['field_count']:>8}")
stats_lines.append("")
stats_lines.append("--- Top 20 Entities by Field Count ---")
stats_lines.append(f"{'Entity':<40} {'Fields':>6} {'Meaningful Desc':>15} {'Domain':<30}")
stats_lines.append("-" * 95)
for entry in entity_inventory[:20]:
    stats_lines.append(f"{entry['entityName']:<40} {entry['actualFieldCount']:>6} {entry['descriptionsMeaningful']:>15} {entry['domain']:<30}")
stats_lines.append("")
stats_lines.append("--- Entities with 0 Meaningful Descriptions ---")
for entry in entity_inventory:
    if entry['descriptionsMeaningful'] == 0 and entry['actualFieldCount'] > 1:
        stats_lines.append(f"  {entry['entityName']} ({entry['actualFieldCount']} fields)")

stats_text = "\n".join(stats_lines)
print(stats_text)

with open(OUTPUT_STATS, "w") as f:
    f.write(stats_text + "\n")

with open(OUTPUT_INVENTORY, "w") as f:
    json.dump(entity_inventory, f, indent=2)

print(f"\nSaved: {OUTPUT_STATS}, {OUTPUT_INVENTORY}")
