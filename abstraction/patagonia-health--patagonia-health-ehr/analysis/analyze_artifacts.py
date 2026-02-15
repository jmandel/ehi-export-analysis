"""
Analyze all EHI export artifacts for Patagonia Health EHR.
Produces a structured summary of all artifacts, their content, and coverage.
"""
import json
import os
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/patagonia-health--patagonia-health-ehr"
DOWNLOADS_DIR = os.path.join(RESULTS_DIR, "downloads")

# --- EHI Export Section Analysis ---
class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
    def handle_data(self, data):
        s = data.strip()
        if s:
            self.text.append(s)

with open(os.path.join(DOWNLOADS_DIR, "ehi-export-section.html")) as f:
    p = TextExtractor()
    p.feed(f.read())
    ehi_text = " ".join(p.text)
    ehi_words = ehi_text.split()

print("=== EHI Export Section ===")
print(f"Word count: {len(ehi_words)}")
print(f"Character count: {len(ehi_text)}")
print()

# --- CCDA Sections from Patient Health Data API ---
ccda_sections = [
    ("all", "All"),
    ("demographics", "Patient Demographics"),
    ("careteam", "Care Team"),
    ("allergies", "Allergies and Intolerances"),
    ("assessments", "Assessment"),
    ("encounters", "Encounters"),
    ("functionalstatus", "Functional Status"),
    ("goals", "Goals"),
    ("healthconcerns", "Health Concerns"),
    ("immunizations", "Immunizations"),
    ("medicalequipment", "Medical Equipment"),
    ("medications", "Medications"),
    ("mentalstatus", "Mental Status"),
    ("planoftreatment", "Plan of Treatment"),
    ("problem", "Problem"),
    ("procedures", "Procedures"),
    ("reasonforreferral", "Reason for Referral"),
    ("results", "Results"),
    ("socialhistory", "Social History"),
    ("vitalsigns", "Vital Signs"),
]

print("=== CCDA Sections Available (from Patient Health Data API v1.1) ===")
print(f"Total sections: {len(ccda_sections) - 1}")  # excluding "all"
for key, label in ccda_sections:
    if key != "all":
        print(f"  {key}: {label}")
print()

# --- FHIR Resources (from SmartOnFHIR doc) ---
fhir_resources = [
    "Patient",
    "AllergyIntolerance",
    "CarePlan",
    "CareTeam",
    "Condition (Problems/Health Concerns)",
    "Device (Implantable)",
    "DiagnosticReport / Clinical Notes",
    "DocumentReference",
    "Goal",
    "Immunization",
    "Medication",
    "MedicationDispense",
    "Observation (Labs, Vitals, Smoking Status)",
    "Organization",
    "Procedure",
    "Provenance",
    "ServiceRequest",
    "Coverage",
    "Specimen",
    "RelatedPerson",
]

print("=== FHIR Resources (from SmartOnFHIR API Documentation) ===")
print(f"Total distinct resources: {len(fhir_resources)}")
for r in fhir_resources:
    print(f"  {r}")
print()

# --- Artifact inventory ---
with open(os.path.join(RESULTS_DIR, "files.json")) as f:
    files_data = json.load(f)

print("=== Artifact Inventory ===")
for entry in files_data["files"]:
    size_kb = entry["size_bytes"] / 1024
    print(f"  {entry['path']} ({size_kb:.1f} KB)")
    print(f"    Source: {entry['source_url']}")
    print(f"    Description: {entry['description'][:120]}...")
    print()

# --- Coverage analysis ---
print("=== Coverage Gap Analysis ===")
product_domains = {
    "Demographics": {"in_export": True, "evidence": "CCDA demographics section"},
    "Encounters/Visits": {"in_export": True, "evidence": "CCDA encounters section"},
    "Problems/Conditions": {"in_export": True, "evidence": "CCDA problem section"},
    "Medications/Prescriptions": {"in_export": True, "evidence": "CCDA medications section"},
    "Allergies": {"in_export": True, "evidence": "CCDA allergies section"},
    "Immunizations": {"in_export": True, "evidence": "CCDA immunizations section"},
    "Vitals": {"in_export": True, "evidence": "CCDA vital signs section"},
    "Lab Results": {"in_export": True, "evidence": "CCDA results section"},
    "Procedures": {"in_export": True, "evidence": "CCDA procedures section"},
    "Clinical Notes/Documents": {"in_export": "partial", "evidence": "CCDA supports some notes; no mention of uploaded documents"},
    "Care Plans/Goals": {"in_export": True, "evidence": "CCDA goals and plan of treatment sections"},
    "Orders/Referrals": {"in_export": "partial", "evidence": "CCDA reason for referral section only"},
    "Insurance/Coverage": {"in_export": False, "evidence": "No insurance data in CCDA; billing export has claims but no coverage detail documented"},
    "Claims/Billing": {"in_export": "partial", "evidence": "Separate billing export in CSV/XLSX but no schema or field documentation"},
    "Payments": {"in_export": False, "evidence": "No payment data mentioned in export"},
    "Consents/Directives": {"in_export": False, "evidence": "No consent forms mentioned in export"},
    "Patient Communications/Portal Messages": {"in_export": False, "evidence": "No portal data in export"},
    "Behavioral Health Assessments": {"in_export": False, "evidence": "CCDA has limited BH support; custom assessments not addressed"},
    "Public Health Program Data": {"in_export": False, "evidence": "Disease surveillance, contact tracing, outreach not in export"},
    "Custom Clinical Templates": {"in_export": False, "evidence": "No documentation of custom form data export"},
}

covered = sum(1 for v in product_domains.values() if v["in_export"] is True)
partial = sum(1 for v in product_domains.values() if v["in_export"] == "partial")
not_covered = sum(1 for v in product_domains.values() if v["in_export"] is False)

print(f"Domains fully covered: {covered}")
print(f"Domains partially covered: {partial}")
print(f"Domains not covered: {not_covered}")
print(f"Total applicable domains: {len(product_domains)}")
print()

for domain, info in product_domains.items():
    status = "✅" if info["in_export"] is True else ("⚠️" if info["in_export"] == "partial" else "❌")
    print(f"  {status} {domain}: {info['evidence']}")

# Save structured output
output = {
    "ehi_section_word_count": len(ehi_words),
    "ccda_section_count": len(ccda_sections) - 1,
    "ccda_sections": [{"key": k, "label": l} for k, l in ccda_sections if k != "all"],
    "fhir_resource_count": len(fhir_resources),
    "fhir_resources": fhir_resources,
    "artifact_count": len(files_data["files"]),
    "coverage": {
        "fully_covered": covered,
        "partially_covered": partial,
        "not_covered": not_covered,
        "total_applicable": len(product_domains),
        "domains": {k: {"status": "covered" if v["in_export"] is True else ("partial" if v["in_export"] == "partial" else "not_covered"), "evidence": v["evidence"]} for k, v in product_domains.items()}
    }
}

output_path = os.path.join(os.path.dirname(__file__), "analysis_output.json")
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nStructured output saved to {output_path}")
