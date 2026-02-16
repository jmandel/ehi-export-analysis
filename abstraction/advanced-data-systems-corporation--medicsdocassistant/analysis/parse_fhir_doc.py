"""Parse the FHIR API documentation HTML to extract resource types and details."""
import re
from html.parser import HTMLParser
import json

with open('../downloads/FHIRMedicsDocAssistant.htm', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Extract headings that mention resource types
# Look for patterns like "Patient", "AllergyIntolerance" etc. in headings
resource_pattern = re.compile(r'<h[1-4][^>]*>(.*?)</h[1-4]>', re.IGNORECASE | re.DOTALL)
headings = resource_pattern.findall(content)

# Clean HTML tags from headings
clean = re.compile(r'<[^>]+>')
headings_clean = [clean.sub('', h).strip() for h in headings]

# Filter for FHIR resource-related headings
fhir_resources = []
for h in headings_clean:
    if h and len(h) < 200:
        fhir_resources.append(h)

print("=== All headings found ===")
for h in fhir_resources:
    print(f"  - {h}")

# Also look for US Core profile references
uscore_refs = re.findall(r'US Core\s+(\w+)', content)
uscore_unique = sorted(set(uscore_refs))
print(f"\n=== US Core references ({len(uscore_unique)}) ===")
for r in uscore_unique:
    print(f"  - {r}")

# Look for specific FHIR resource type mentions
resource_types = ['Patient', 'AllergyIntolerance', 'CarePlan', 'CareTeam', 'Condition',
    'Device', 'DiagnosticReport', 'DocumentReference', 'Encounter', 'Goal',
    'Immunization', 'Location', 'Medication', 'MedicationRequest', 'Observation',
    'Organization', 'Practitioner', 'PractitionerRole', 'Procedure', 'Provenance',
    'Coverage', 'Claim', 'ExplanationOfBenefit', 'ServiceRequest', 'FamilyMemberHistory',
    'QuestionnaireResponse', 'Questionnaire', 'Specimen', 'RelatedPerson',
    'MedicationDispense', 'MedicationAdministration', 'Consent', 'Communication',
    'Appointment', 'Schedule', 'Slot', 'ChargeItem', 'Invoice', 'Account',
    'Binary', 'Bundle', 'Group', 'OperationOutcome']

print("\n=== FHIR Resource type mentions ===")
found_resources = {}
for rt in resource_types:
    # Match as standalone word
    count = len(re.findall(r'\b' + rt + r'\b', content))
    if count > 0:
        found_resources[rt] = count
        print(f"  {rt}: {count} mentions")

# Look for search parameter documentation
search_params = re.findall(r'_id|_lastUpdated|_revinclude|_include|_count|_sort', content)
print(f"\n=== Search parameters found: {len(search_params)} occurrences ===")

# Check for Bulk Data / $export mentions
bulk_mentions = re.findall(r'(?i)(bulk|export|\$export|kickoff|polling)', content)
print(f"\n=== Bulk/export mentions: {len(bulk_mentions)} ===")
for m in set(bulk_mentions):
    count = bulk_mentions.count(m)
    print(f"  '{m}': {count}")

# Save results
results = {
    'headings': fhir_resources,
    'us_core_references': uscore_unique,
    'resource_mentions': found_resources,
    'total_lines': 10568
}
with open('fhir_doc_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nSaved to fhir_doc_analysis.json")
