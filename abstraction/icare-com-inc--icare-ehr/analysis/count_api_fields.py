"""
Count fields per API category from the PDF's JSON example outputs.
Parses each category section and counts unique field names in examples.
"""
import re
import json

with open("/tmp/icare-api-guide.txt") as f:
    text = f.read()

# Define category sections based on the PDF structure
categories = [
    "patient", "smokingStatus", "problem", "medication", "medAllergy",
    "labTest", "labResult", "vital", "procedure", "careTeam",
    "immunization", "device", "planOfTreatment", "assessment",
    "assessment,planOfTreatment", "goal", "healthConcern"
]

# For each category, find section boundaries and count unique JSON field names
results = {}
for i, cat in enumerate(categories):
    # Find the section header (category name as a standalone section)
    pattern = rf'^\s+{re.escape(cat)}\s*$'
    matches = list(re.finditer(pattern, text, re.MULTILINE))
    if not matches:
        continue
    
    start = matches[0].start()
    
    # Find end: next category or "All Criteria Data Request"
    if i + 1 < len(categories):
        next_cat = categories[i + 1]
        next_pattern = rf'^\s+{re.escape(next_cat)}\s*$'
        next_matches = list(re.finditer(next_pattern, text, re.MULTILINE))
        if next_matches:
            end = next_matches[0].start()
        else:
            end = len(text)
    else:
        end_match = text.find("All Criteria Data Request", start)
        end = end_match if end_match > 0 else len(text)
    
    section = text[start:end]
    
    # Count unique field names in JSON examples
    field_pattern = re.compile(r'"(\w+)"\s*:')
    fields = set()
    for m in field_pattern.finditer(section):
        fname = m.group(1)
        # Skip structural/error fields
        if fname not in ('resourceType', 'type', 'entry', 'resource', 'error',
                         'errorDescription', 'errorDetail', 'errorNumber',
                         'total', 'link', 'url', 'relation'):
            fields.add(fname)
    
    results[cat] = {
        "field_count": len(fields),
        "fields": sorted(fields),
        "section_length_chars": len(section)
    }

print("=" * 60)
print("FIELDS PER API CATEGORY (from PDF JSON examples)")
print("=" * 60)
total_fields = 0
for cat, data in results.items():
    print(f"\n{cat} ({data['field_count']} fields):")
    for f in data['fields']:
        print(f"  - {f}")
    total_fields += data['field_count']

print(f"\n{'=' * 60}")
print(f"TOTAL: {len(results)} categories, {total_fields} field instances")
print(f"(Some fields appear in multiple categories)")

# Deduplicate to get unique fields across all categories
all_fields = set()
for data in results.values():
    all_fields.update(data['fields'])
print(f"Unique fields across all categories: {len(all_fields)}")

with open("api-fields-by-category.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nSaved to api-fields-by-category.json")
