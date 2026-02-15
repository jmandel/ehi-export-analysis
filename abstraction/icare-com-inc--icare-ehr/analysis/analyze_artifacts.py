"""
Analyze iCare EHI export artifacts: HTML page, PDF API guide, FHIR CapabilityStatement.
Extracts structured data about export capabilities.
"""
import json
import re
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/icare-com-inc--icare-ehr/downloads"

# --- 1. Parse HTML EHI Export page ---
with open(f"{RESULTS_DIR}/ehi-export-page.html") as f:
    html_content = f.read()

# Extract FHIR resource types listed as H4 headers in Data Elements section
h4_pattern = re.compile(r'<h4>(.*?)</h4>', re.DOTALL)
fhir_resources = [m.group(1).strip() for m in h4_pattern.finditer(html_content)]

print("=" * 60)
print("EHI EXPORT PAGE ANALYSIS")
print("=" * 60)
print(f"\nFHIR resource types listed: {len(fhir_resources)}")
for r in fhir_resources:
    print(f"  - {r}")

# Count export methods
print(f"\nExport methods described: 3")
print("  1. CCD/HIM export (in-app, single patient)")
print("  2. CSC request for full data export (population, vendor-assisted)")
print("  3. FHIR REST API (single patient, population, group)")

# Check for copy-paste errors
# The Encounter section has URI for Patient and example for Procedure
encounter_section = html_content[html_content.find('<h4>Encounter</h4>'):]
encounter_section = encounter_section[:encounter_section.find('</div>')]
has_procedure_url = 'Procedure?patient=' in encounter_section
has_patient_uri = 'Patient?_id=' in encounter_section
print(f"\nCopy-paste errors detected:")
print(f"  - Encounter section URI says 'Patient?_id=': {has_patient_uri}")
print(f"  - Encounter section example links to Procedure: {has_procedure_url}")

# Check that every resource section has the same generic $export URI
export_uri_count = html_content.count('Patient/id/$export')
print(f"  - Generic 'Patient/id/$export' URI repeated: {export_uri_count} times")
print(f"    (same URI pasted into every resource section instead of resource-specific URIs)")

# --- 2. Parse FHIR CapabilityStatement ---
with open(f"{RESULTS_DIR}/fhir-capability-statement.json") as f:
    cap_stmt = json.load(f)

print(f"\n{'=' * 60}")
print("FHIR CAPABILITY STATEMENT ANALYSIS")
print("=" * 60)
print(f"FHIR version: {cap_stmt['fhirVersion']}")
print(f"Software: {cap_stmt['software']['name']} v{cap_stmt['software']['version']}")
print(f"Implementation: {cap_stmt['implementation']['description']}")
instantiates = cap_stmt.get('instantiates', [])
print(f"Conformance profiles: {len(instantiates)}")
for inst in instantiates:
    print(f"  - {inst}")

resources = cap_stmt.get('rest', [{}])[0].get('resource', [])
print(f"Resource types declared: {len(resources)}")
for r in resources:
    ops = [o['name'] for o in r.get('operation', [])]
    interactions = [i['code'] for i in r.get('interaction', [])]
    print(f"  - {r['type']}: operations={ops}, interactions={interactions}")

# --- 3. Analyze API Guide categories ---
print(f"\n{'=' * 60}")
print("API GUIDE (PDF) ANALYSIS")
print("=" * 60)

api_categories = [
    ("patient", "Patient name, sex, date of birth, race, ethnicity, preferred language"),
    ("careTeam", "Care team members"),
    ("smokingStatus", "Smoking status"),
    ("problem", "Problems"),
    ("medication", "Medications"),
    ("medAllergy", "Medication allergies"),
    ("labTest", "Planned lab tests"),
    ("labResult", "Lab test results"),
    ("vital", "Vital measurements"),
    ("procedure", "Procedures"),
    ("immunization", "Immunizations"),
    ("device", "Implanted devices"),
    ("planOfTreatment", "Care plan"),
    ("assessment", "Assessment"),
    ("goal", "Discharge goals"),
    ("healthConcern", "Health concerns (complaints and observations)")
]

print(f"API data categories: {len(api_categories)}")
for cat, desc in api_categories:
    print(f"  - {cat}: {desc}")

print(f"\nAPI output formats:")
print(f"  - Individual category requests: FHIR R4 JSON")
print(f"  - All Criteria Data Request: C-CDA XML")

# --- 4. Count fields in API Guide JSON examples ---
with open("/tmp/icare-api-guide.txt") as f:
    pdf_text = f.read()

# Count unique JSON field names across all example outputs
json_fields = set()
field_pattern = re.compile(r'"(\w+)"\s*:')
# Find all field names in the JSON examples
for m in field_pattern.finditer(pdf_text):
    field_name = m.group(1)
    if field_name not in ('resourceType', 'type', 'entry', 'resource', 'error',
                          'errorDescription', 'errorDetail', 'errorNumber'):
        json_fields.add(field_name)

print(f"\nUnique data field names in JSON examples: {len(json_fields)}")
sorted_fields = sorted(json_fields)
for f in sorted_fields:
    print(f"  - {f}")

# --- 5. Summary comparison: EHI page vs API Guide ---
ehi_resources = set(fhir_resources)
api_cats = set(c for c, _ in api_categories)

print(f"\n{'=' * 60}")
print("COMPARISON: EHI PAGE vs API GUIDE")
print("=" * 60)
print(f"EHI page FHIR resources: {len(ehi_resources)}")
print(f"API Guide categories: {len(api_cats)}")

# Map API categories to FHIR resources
api_to_fhir = {
    "patient": "Patient",
    "careTeam": "CareTeam",
    "smokingStatus": "Observation",
    "problem": "Condition",
    "medication": "MedicationRequest",
    "medAllergy": "AllergyIntolerance",
    "labTest": "DiagnosticReport",
    "labResult": "Observation",
    "vital": "Observation",
    "procedure": "Procedure",
    "immunization": "Immunization",
    "device": "Device",
    "planOfTreatment": "CarePlan",
    "assessment": "DocumentReference",
    "goal": "Goal",
    "healthConcern": "Condition"
}

mapped_fhir = set(api_to_fhir.values())
ehi_only = ehi_resources - mapped_fhir
api_only_fhir = mapped_fhir - ehi_resources

print(f"\nOn EHI page but not clearly in API Guide: {ehi_only}")
print(f"In API Guide (as FHIR) but not on EHI page: {api_only_fhir}")
print(f"\nNote: Encounter is on EHI page AND in the API Guide as a separate endpoint")

# --- 6. Coverage assessment ---
print(f"\n{'=' * 60}")
print("COVERAGE GAP ANALYSIS")
print("=" * 60)

product_capabilities = [
    ("Demographics", True, "patient category in API, Patient resource in FHIR"),
    ("Encounters / visits", True, "Encounter endpoint in API and FHIR page"),
    ("Problems / conditions / diagnoses", True, "problem category, Condition resource"),
    ("Medications / prescriptions", True, "medication category, MedicationRequest resource"),
    ("Allergies", True, "medAllergy category, AllergyIntolerance resource"),
    ("Immunizations", True, "immunization category, Immunization resource"),
    ("Vitals", True, "vital category, Observation resource"),
    ("Lab results", True, "labResult/labTest categories, DiagnosticReport resource"),
    ("Imaging / diagnostic reports", False, "No radiology/imaging resources in export"),
    ("Procedures", True, "procedure category, Procedure resource"),
    ("Clinical notes / documents", True, "assessment category, DocumentReference resource"),
    ("Care plans / goals", True, "planOfTreatment/goal categories, CarePlan/Goal resources"),
    ("Orders / referrals", False, "No order resources beyond MedicationRequest"),
    ("Insurance / coverage", False, "No insurance/coverage data in any export method"),
    ("Claims / billing", False, "No billing/claims data in any export method"),
    ("Payments", False, "No payment data in any export method"),
    ("Consents / directives", False, "No consent resources in export"),
    ("Patient communications / portal messages", False, "No messaging data in export"),
    ("E-prescribing data", False, "No EPCS/Surescripts transaction data"),
]

covered = sum(1 for _, c, _ in product_capabilities if c)
total = len(product_capabilities)
print(f"Domains covered: {covered} of {total}")
for domain, is_covered, evidence in product_capabilities:
    status = "✅" if is_covered else "❌"
    print(f"  {status} {domain}: {evidence}")

# Save structured output
output = {
    "ehi_page": {
        "fhir_resources": fhir_resources,
        "resource_count": len(fhir_resources),
        "export_methods": 3,
        "copy_paste_errors": True,
        "generic_export_uri_count": export_uri_count,
    },
    "api_guide": {
        "categories": [{"name": c, "description": d} for c, d in api_categories],
        "category_count": len(api_categories),
        "page_count": 67,
        "date": "2020-03-26",
        "output_formats": ["FHIR R4 JSON", "C-CDA XML"],
    },
    "capability_statement": {
        "fhir_version": cap_stmt["fhirVersion"],
        "software": cap_stmt["software"]["name"],
        "resource_types": [r["type"] for r in resources],
        "conformance_profiles": instantiates,
    },
    "coverage": {
        "covered_domains": covered,
        "total_domains": total,
        "domains": [
            {"name": d, "covered": c, "evidence": e}
            for d, c, e in product_capabilities
        ],
    },
    "unique_field_names_in_examples": sorted_fields,
    "unique_field_count": len(json_fields),
}

with open("artifact-analysis.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nSaved structured analysis to artifact-analysis.json")
