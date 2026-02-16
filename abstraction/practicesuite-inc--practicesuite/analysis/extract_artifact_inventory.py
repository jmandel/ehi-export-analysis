"""Extract a complete inventory of all artifacts and their content from the PracticeSuite EHI export documentation.
Produces full-entity-inventory.json and artifact-summary.json."""

import json
import os
import re
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/practicesuite-inc--practicesuite"
DOWNLOADS_DIR = os.path.join(RESULTS_DIR, "downloads")
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/practicesuite-inc--practicesuite/analysis"

# ---- Inventory all downloaded artifacts ----
artifacts = []
for root, dirs, files in os.walk(DOWNLOADS_DIR):
    for f in sorted(files):
        fpath = os.path.join(root, f)
        relpath = os.path.relpath(fpath, DOWNLOADS_DIR)
        size = os.path.getsize(fpath)
        artifacts.append({
            "file": relpath,
            "size_bytes": size,
            "type": os.path.splitext(f)[1].lower()
        })

# ---- Extract structured info from the HTML pages ----

# The EHI export page tells us:
# Export format: C-CDA XML (zip) + Documents (original format, zip)
# No data dictionary, no schema, no sample data files

# The K3 report page tells us about: search filters, export buttons, custom visit summary
# Custom Visit Summary sections (from screenshot analysis):
visit_summary_sections = [
    "Patient Demographics",
    "Documentation Demographics", 
    "Encounter Demographics",
    "Chief Complaint",
    "Past Medical History",
    "Allergies",
    "MED LIST",
    "Vital Signs",
    "Assessment/Diagnosis",
    "Plan / Recommended Action",
    "Special Situation",
    "Escalation and Emergency",
    "Provider Signature",
    "Care Coordinator Signature",
    "Custom Visit Summary",
    "Authorization for Med Administration - RX",
    "CareTeam Communication 1"
]

# K3 Report search filter categories (from screenshots):
k3_search_filters = [
    "Patient (Name/MR#, Age, Gender, Race, Ethnicity, Preferred Means of Contact)",
    "Diagnosis (Contains/Does Not Contain, date range)",
    "Medication (Contains/Does Not Contain, date range)",
    "Facesheet (ALLERGY dropdown type, Contains/Does Not Contain, date range)",
    "CPT Code (Contains/Does Not Contain, date)",
    "Lab Order (Contains/Does Not Contain, date)",
    "Lab Result (Contains, value comparison)",
    "Radiology (Contains/Does Not Contain, date)",
    "Body Vitals (40+ vital sign types with comparison operators and date ranges)"
]

# K3 Output list columns (from screenshot):
k3_output_columns = [
    "MR#", "PC Ref#", "LName", "FName", "Gender", "DOB", "Age", 
    "Address", "Home Ph.", "Work Ph.", "Pref. Means of Contact",
    "Race", "Ethnicity", "Lan. Spoken", "Last Seen", "PR. Ins.",
    "SE. Ins.", "TE. Ins.", "DOS", "Time"
]

# K3 Export options:
k3_export_options = [
    "Excel export of patient list",
    "PDF export of patient list",
    "Custom Visit Summary report (per encounter)",
    "Download C-CDA (ZIP with XML per patient)",
    "Download Documents (ZIP with original-format docs per patient)"
]

# Vital signs visible in search interface (from screenshots):
vitals_in_search = [
    "HEARTRATE", "HEIGHT", "HLDFR", "HLDM", "HTN",
    "Head Circumference", "Head Occipital frontal Circumference Percentile",
    "Heart Rate", "Height (Lying)", "Height loinc",
    "Inhaled Oxygen Concentration", "BMI Percentile", "Weight Percentile",
    "363636", "BMI (Body Mass Index)", "BMI Percentile", "BMI(loinc)",
    "BMI1", "Respiratory Rate", "Stature", "TEMPERATURE",
    "Weight Measured", "Weight for Length Percentile", "Weight loinc",
    "Weight percentile", "hc", "pgr_2006", "pmCode", "prgs_2004",
    "pro_2007", "prog2000", "prog_2001", "test123", "visit",
    "PAIN_SCALE", "Pulse"
]

# Build the inventory - since there's no data dictionary, we document what the export contains
inventory = {
    "vendor": "PracticeSuite, Inc.",
    "product": "PracticeSuite",
    "export_format": "C-CDA XML + original-format documents",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_level_documentation": False,
    "export_mechanism": {
        "type": "UI-based (Report Central > K3 Patient Clinical Analysis Report)",
        "single_patient": True,
        "patient_population": True,
        "api_access": False,
        "access_control": "Report Central menu permission required"
    },
    "export_components": [
        {
            "name": "C-CDA Export",
            "format": "XML (C-CDA / HL7 CDA R2)",
            "delivery": "ZIP file containing one XML per patient plus cda.xsl stylesheet",
            "naming": "<AccountNo>_<PracticeName>_CCDA_<date>.zip containing <FirstName>_<LastName>_<MR#>_CCDAhl7V3Xml_<timestamp>.xml",
            "content_description": "Full CCDA Summary per patient",
            "sections_documented": "Not specified - documentation says 'full CCDA Summary' without listing sections",
            "ccda_version": "Not specified"
        },
        {
            "name": "Documents Export", 
            "format": "Original file formats (PDF, images, etc.)",
            "delivery": "ZIP file with per-patient subfolders",
            "naming": "<AccountNo>_<PracticeName>_PatDocs_<date>.zip containing <FirstName>_<LastName>_<MR#>.zip/<FileName>_<Category>[file]",
            "content_description": "All documents associated with patient(s) in original format"
        },
        {
            "name": "Custom Visit Summary (supplemental)",
            "format": "PDF report",
            "delivery": "Download via K3 report button",
            "content_description": "Per-encounter visit summary report with structured sections",
            "sections": visit_summary_sections
        }
    ],
    "k3_report": {
        "search_filters": k3_search_filters,
        "output_columns": k3_output_columns,
        "export_options": k3_export_options,
        "vitals_in_search_interface": vitals_in_search
    },
    "artifacts_reviewed": artifacts,
    "documentation_page": {
        "url": "https://academy.practicesuite.com/%c2%a7-170-315b10-electronic-health-information-ehi-export/",
        "created": "2023-11-14",
        "last_modified": "2024-05-20",
        "platform": "WordPress on WP Engine behind Cloudflare",
        "content_type": "Step-by-step instructions with screenshots (no technical specification)"
    }
}

# Write the full inventory
with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
    json.dump(inventory, f, indent=2)

# Summary statistics
summary = {
    "total_artifacts": len(artifacts),
    "html_pages": sum(1 for a in artifacts if a["type"] == ".html"),
    "png_screenshots": sum(1 for a in artifacts if a["type"] == ".png"),
    "other_files": sum(1 for a in artifacts if a["type"] not in (".html", ".png")),
    "total_size_bytes": sum(a["size_bytes"] for a in artifacts),
    "export_entities": 0,
    "export_fields": 0,
    "fields_with_descriptions": 0,
    "data_dictionary_present": False,
    "schema_present": False,
    "sample_data_present": False,
    "export_format": "C-CDA XML + original-format documents",
    "model_type": "Standard projection (C-CDA)",
    "visit_summary_sections": len(visit_summary_sections),
    "k3_search_filter_categories": len(k3_search_filters),
    "k3_output_columns": len(k3_output_columns),
    "vitals_in_search": len(vitals_in_search)
}

with open(os.path.join(OUTPUT_DIR, "artifact-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("=== Artifact Inventory ===")
for a in artifacts:
    print(f"  {a['file']:50s} {a['size_bytes']:>10,} bytes  ({a['type']})")
print(f"\nTotal: {len(artifacts)} files, {sum(a['size_bytes'] for a in artifacts):,} bytes")
print(f"\n=== Summary ===")
for k, v in summary.items():
    print(f"  {k}: {v}")
print(f"\nOutput: full-entity-inventory.json, artifact-summary.json")
