"""
Analyze all EHI export artifacts for ezCaretech BESTCare.
Produces a structured JSON summary of each artifact's content and key metrics.
"""
import json
import os
import subprocess

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/ezcaretech-co-ltd--bestcare/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/ezcaretech-co-ltd--bestcare/analysis"

results = {}

# 1. Analyze the main (b)(10) PDF
pdf_text = subprocess.run(
    ["pdftotext", "-layout", os.path.join(DOWNLOADS, "b.10_EHI_Export.pdf"), "-"],
    capture_output=True, text=True
).stdout
pdf_info = subprocess.run(
    ["pdfinfo", os.path.join(DOWNLOADS, "b.10_EHI_Export.pdf")],
    capture_output=True, text=True
).stdout

results["b10_ehi_export_pdf"] = {
    "file": "b.10_EHI_Export.pdf",
    "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "b.10_EHI_Export.pdf")),
    "pages": 1,
    "word_count": len(pdf_text.split()),
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_schema": False,
    "has_export_instructions": False,
    "mentions_csv": "CSV" in pdf_text,
    "mentions_oracle_dmp": "Oracle DMP" in pdf_text or "DMP" in pdf_text,
    "mentions_single_patient": "Single Patient" in pdf_text,
    "mentions_multi_patient": "Multi-Patient" in pdf_text or "Multi Patient" in pdf_text,
    "full_text": pdf_text.strip(),
}

# 2. Analyze Certified Health IT PDF
cert_text = subprocess.run(
    ["pdftotext", "-layout", os.path.join(DOWNLOADS, "BESTCare2.0B_Certified_Health_IT_v3.0.pdf"), "-"],
    capture_output=True, text=True
).stdout

import re
criteria = re.findall(r'170\.315 \([a-z]\)\(\d+\)', cert_text)
cqms = re.findall(r'CMS\d+', cert_text)
results["certified_health_it_pdf"] = {
    "file": "BESTCare2.0B_Certified_Health_IT_v3.0.pdf",
    "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "BESTCare2.0B_Certified_Health_IT_v3.0.pdf")),
    "pages": 3,
    "certified_criteria_count": len(set(criteria)),
    "cqm_count": len(set(cqms)),
    "has_ehi_export_detail": False,
}

# 3. Analyze FHIR Capability Statement
with open(os.path.join(DOWNLOADS, "fhir-capability-statement.json")) as f:
    cs = json.load(f)

resource_types = []
for rest in cs.get("rest", []):
    for res in rest.get("resource", []):
        interactions = [i["code"] for i in res.get("interaction", [])]
        search_params = [p["name"] for p in res.get("searchParam", [])]
        resource_types.append({
            "type": res["type"],
            "interactions": interactions,
            "search_params": search_params,
        })

# Separate clinical resources from infrastructure
clinical_resources = [r for r in resource_types if r["type"] not in
    ("Binary", "CodeSystem", "Endpoint", "Group", "OperationDefinition", "ValueSet")]
infra_resources = [r for r in resource_types if r["type"] in
    ("Binary", "CodeSystem", "Endpoint", "Group", "OperationDefinition", "ValueSet")]

results["fhir_capability_statement"] = {
    "file": "fhir-capability-statement.json",
    "server_name": cs.get("name"),
    "fhir_version": cs.get("fhirVersion"),
    "date": cs.get("date"),
    "total_resource_types": len(resource_types),
    "clinical_resource_types": len(clinical_resources),
    "infrastructure_resource_types": len(infra_resources),
    "resource_list": [r["type"] for r in resource_types],
    "clinical_resource_list": [r["type"] for r in clinical_resources],
}

# 4. Analyze Single Patient API HTML
with open(os.path.join(DOWNLOADS, "single-patient-api.html")) as f:
    spa_content = f.read()

# Count US Core profiles documented
profiles = re.findall(r'US Core (\w[\w\s\-]+?) Profile', spa_content)
vital_profiles = re.findall(r'Vital Signs - US Core ([\w\s\-]+?) Profile', spa_content)

results["single_patient_api"] = {
    "file": "single-patient-api.html",
    "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "single-patient-api.html")),
    "us_core_profiles_documented": len(set(profiles)),
    "vital_sign_sub_profiles": len(set(vital_profiles)),
    "profile_names": sorted(set(profiles)),
    "vital_sign_profile_names": sorted(set(vital_profiles)),
    "is_g10_documentation": True,
    "is_b10_documentation": False,
}

# 5. Analyze Multi Patient API HTML
with open(os.path.join(DOWNLOADS, "multi-patient-api.html")) as f:
    mpa_content = f.read()

bulk_endpoints = []
for ep in ["Patient/$export", "Group/[id]/$export", "/$export"]:
    if ep in mpa_content:
        bulk_endpoints.append(ep)

results["multi_patient_api"] = {
    "file": "multi-patient-api.html",
    "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "multi-patient-api.html")),
    "bulk_endpoints": bulk_endpoints,
    "output_format": "NDJSON (application/fhir+ndjson)",
    "is_g10_documentation": True,
    "is_b10_documentation": False,
}

# Summary
results["summary"] = {
    "total_artifacts": 9,
    "informative_artifacts": 3,  # PDF, FHIR CS, API docs
    "data_dictionary_present": False,
    "schema_present": False,
    "sample_data_present": False,
    "field_count_documented": 0,
    "table_count_documented": 0,
    "export_formats_mentioned": ["CSV", "Oracle DMP", "FHIR NDJSON"],
    "native_export_documented": False,
    "fhir_resource_types": len(resource_types),
    "fhir_clinical_resource_types": len(clinical_resources),
}

with open(os.path.join(OUTPUT_DIR, "artifact_analysis.json"), "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results["summary"], indent=2))
print("\nFull analysis saved to artifact_analysis.json")
