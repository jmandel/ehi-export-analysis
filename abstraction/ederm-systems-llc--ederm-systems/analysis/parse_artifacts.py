"""
Parse eDerm Systems EHI export artifacts and produce structured analysis.
Extracts data from the API documentation PDF and certification page HTML.
"""
import json
import re
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/ederm-systems-llc--ederm-systems/downloads"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/ederm-systems-llc--ederm-systems/analysis"

# Artifact inventory
artifacts = []

for fname in sorted(os.listdir(DOWNLOADS)):
    fpath = os.path.join(DOWNLOADS, fname)
    size = os.path.getsize(fpath)
    artifacts.append({
        "filename": fname,
        "size_bytes": size,
        "size_human": f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
    })

# API parameter extraction from PDF text
api_params = [
    "patientid", "medications", "medicationallergies", "labresults",
    "vitalsigns", "procedures", "careteammembers", "immunizations",
    "udiforpatientdevices", "planoftreatment", "goals", "healthconcerns",
    "labtest", "assessment", "problems", "patientname", "patientgender",
    "patientdob", "patientrace", "patientethnicity", "patientpreferredlanguage",
    "smokingstatus", "ccdafromdate", "ccdatodate", "returnformat"
]

# Separate clinical data params from control params
clinical_params = [p for p in api_params if p not in 
    ["patientid", "ccdafromdate", "ccdatodate", "returnformat"]]

# C-CDA sections identified from displayName values
ccda_sections = [
    "Allergies, adverse reactions, alerts",
    "History of immunizations",
    "Medications Administered",
    "Problem List",
    "History of Procedures",
    "Results (Lab)",
    "Vital Signs",
    "Goals",
    "Health Concerns",
    "Assessments",
    "Social History",
    "Encounter Diagnosis",
    "Referrals",
    "Complaint (Chief Complaint)",
]

# Map API params to clinical data categories
param_categories = {
    "Demographics": ["patientname", "patientgender", "patientdob", "patientrace", 
                     "patientethnicity", "patientpreferredlanguage"],
    "Medications": ["medications"],
    "Allergies": ["medicationallergies"],
    "Lab results": ["labtest", "labresults"],
    "Vital signs": ["vitalsigns"],
    "Procedures": ["procedures"],
    "Care team": ["careteammembers"],
    "Immunizations": ["immunizations"],
    "Devices": ["udiforpatientdevices"],
    "Treatment plan": ["planoftreatment"],
    "Goals": ["goals"],
    "Health concerns": ["healthconcerns"],
    "Assessment": ["assessment"],
    "Problems": ["problems"],
    "Social history": ["smokingstatus"],
}

results = {
    "artifacts": artifacts,
    "api_endpoints": [
        {"method": "POST", "path": "/ederm/Authenticate", "purpose": "OAuth token acquisition"},
        {"method": "POST", "path": "/ederm/api/SearchPatient", "purpose": "Patient search by demographics"},
        {"method": "POST", "path": "/ederm/api/GetPatientEncounters", "purpose": "List encounters for patient"},
        {"method": "POST", "path": "/ederm/api/GetPatientData", "purpose": "Fetch patient data as C-CDA/JSON/HTML"},
    ],
    "clinical_parameters": clinical_params,
    "clinical_parameter_count": len(clinical_params),
    "clinical_categories": param_categories,
    "clinical_category_count": len(param_categories),
    "ccda_sections_identified": ccda_sections,
    "ccda_section_count": len(ccda_sections),
    "output_formats": ["XML (C-CDA)", "JSON", "HTML"],
    "bulk_export": False,
    "data_dictionary": False,
    "field_definitions": False,
    "value_sets": False,
    "sample_data_files": False,
    "native_database_export": False,
    "fhir_endpoint_status": "dead (SSL expired Feb 10 2026, 404 on all paths)",
    "ehi_specific_docs": False,
}

with open(os.path.join(OUTPUT, "artifact_analysis.json"), "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("=== eDerm Systems EHI Export Artifact Analysis ===\n")
print(f"Total artifacts: {len(artifacts)}")
for a in artifacts:
    print(f"  {a['filename']}: {a['size_human']}")

print(f"\nAPI endpoints documented: {len(results['api_endpoints'])}")
for ep in results['api_endpoints']:
    print(f"  {ep['method']} {ep['path']} — {ep['purpose']}")

print(f"\nClinical data parameters: {len(clinical_params)}")
print(f"Clinical categories: {len(param_categories)}")
for cat, params in param_categories.items():
    print(f"  {cat}: {', '.join(params)}")

print(f"\nC-CDA sections in sample: {len(ccda_sections)}")
for s in ccda_sections:
    print(f"  - {s}")

print(f"\nKey findings:")
print(f"  Data dictionary: {'Yes' if results['data_dictionary'] else 'No'}")
print(f"  Field definitions: {'Yes' if results['field_definitions'] else 'No'}")
print(f"  Value sets: {'Yes' if results['value_sets'] else 'No'}")
print(f"  Sample data files: {'Yes' if results['sample_data_files'] else 'No'}")
print(f"  Native database export: {'Yes' if results['native_database_export'] else 'No'}")
print(f"  Bulk export: {'Yes' if results['bulk_export'] else 'No'}")
print(f"  EHI-specific documentation: {'Yes' if results['ehi_specific_docs'] else 'No'}")
print(f"  FHIR endpoint: {results['fhir_endpoint_status']}")
