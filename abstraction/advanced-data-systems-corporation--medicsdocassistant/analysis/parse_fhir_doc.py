"""
Parse FHIRMedicsDocAssistant.htm to extract:
- All FHIR resource types documented
- Section structure
- Count of search parameters per resource
- Whether Bulk Data/$export is documented
"""
import re
import json

FHIR_DOC = "/home/jmandel/hobby/ehi-export-analysis/results/advanced-data-systems-corporation--medicsdocassistant/downloads/FHIRMedicsDocAssistant.htm"

with open(FHIR_DOC, 'r', errors='replace') as f:
    content = f.read()

# Extract resource types from "Request:- <ResourceType>" patterns
resource_matches = re.findall(r'Request\s*:?\s*-?\s*([A-Z][A-Za-z\s&]+?)(?:<|$)', content)
resources = []
for r in resource_matches:
    r = r.strip()
    if r and len(r) > 2:
        resources.append(r)

# Count search parameters per resource
search_params = re.findall(r'Search Parameters\s*:?\s*-?', content)

# Check for Bulk Data documentation
bulk_mentions = re.findall(r'(?i)(bulk\s*data|[\$]export)', content)

# Check for any mention of billing, claims, charges
billing_mentions = re.findall(r'(?i)(billing|claim|charge|payment|insurance|coverage|superbill)', content)

# Count total lines
total_lines = content.count('\n')

# Count bold sections
bold_sections = re.findall(r'<b[^>]*>([^<]+)</b>', content)

results = {
    "total_lines": total_lines,
    "fhir_resource_types": resources,
    "resource_count": len(resources),
    "search_parameter_sections": len(search_params),
    "bulk_data_mentions": len(bulk_mentions),
    "bulk_data_context": [m for m in bulk_mentions],
    "billing_mentions": len(billing_mentions),
    "billing_context": [m for m in billing_mentions],
}

print(json.dumps(results, indent=2))

# Also check for specific FHIR resource types NOT present
standard_resources = [
    "FamilyMemberHistory", "Coverage", "Claim", "ExplanationOfBenefit",
    "MedicationAdministration", "MedicationDispense", "ServiceRequest",
    "Appointment", "Schedule", "Questionnaire", "QuestionnaireResponse",
    "Communication", "Consent", "RelatedPerson"
]

missing = []
for r in standard_resources:
    if r.lower() not in content.lower():
        missing.append(r)

print("\nFHIR resources NOT mentioned in documentation:")
for m in missing:
    print(f"  - {m}")

present = [r for r in standard_resources if r.lower() in content.lower()]
if present:
    print("\nAdditional FHIR resources mentioned (not in Request sections):")
    for p in present:
        print(f"  - {p}")
