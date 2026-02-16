#!/usr/bin/env python3
"""Parse all EHI export artifacts and produce entity-inventory-full.json and summary."""

import json
import os
import re
from pathlib import Path

BASE = Path(__file__).parent.parent

# Since there is NO public data dictionary (EHIDataExtract_DataDictionary.xlsx is only
# bundled inside actual export ZIPs), we cannot produce a field-level inventory.
# Instead, we document what we CAN extract from the available artifacts.

artifacts = []

# 1. Parse the HTML page for EHI export section
html_path = BASE / "downloads" / "drummond-certified-woundexpert.html"
with open(html_path, "r", encoding="utf-8", errors="replace") as f:
    html_content = f.read()

# Extract the EHI export description text
ehi_section = ""
# Simple extraction of text between "Electronic Health Information Export" and next section
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.text_parts.append(t)

parser = TextExtractor()
parser.feed(html_content)
full_text = "\n".join(parser.text_parts)

# Find the EHI section
ehi_match = re.search(
    r'Electronic Health Information Export\s*(.*?)(?=Costs and Criteria|$)',
    full_text, re.DOTALL
)
ehi_text = ehi_match.group(1).strip() if ehi_match else "Not found"

artifacts.append({
    "file": "drummond-certified-woundexpert.html",
    "type": "HTML page",
    "size_bytes": os.path.getsize(html_path),
    "description": "ONC certification page with EHI Export section",
    "ehi_export_text": ehi_text,
    "key_claims": [
        "Single patient and patient population export supported",
        "Export format: ZIP file containing CSV files, images, custom scans",
        "Includes EHIDataExtract_DataDictionary.xlsx in each export",
        "Includes ExportSummary.txt",
        "Content varies by number of patients and software functionality in use"
    ]
})

# 2. Parse RWT Plan 2026 for Measure 8 details
import subprocess
rwt_plan_path = BASE / "downloads" / "Real-World-Testing-Plan-2026.pdf"
result = subprocess.run(
    ["pdftotext", "-layout", str(rwt_plan_path), "-"],
    capture_output=True, text=True
)
rwt_plan_text = result.stdout

m8_match = re.search(
    r'Measure 8: Electronic Health Record Export(.*?)(?=Measure 9|$)',
    rwt_plan_text, re.DOTALL
)
m8_text = m8_match.group(1).strip() if m8_match else "Not found"

artifacts.append({
    "file": "Real-World-Testing-Plan-2026.pdf",
    "type": "PDF (18 pages)",
    "size_bytes": os.path.getsize(rwt_plan_path),
    "description": "2026 Real World Testing Plan; Measure 8 describes b(10) export",
    "measure_8_text": m8_text[:2000],
    "key_claims": [
        "Facility Administrator: can generate CDA file with treatment info for date range",
        "Net Health Administrator: full facility EHI export with PDF medical records + CSV files",
        "Export can be imported into another CEHRT or EMR supporting the format",
        "Both single-patient and patient population export supported"
    ]
})

# 3. Parse RWT Results 2025
rwt_results_path = BASE / "downloads" / "Real-World-Testing-Results-2025.pdf"
result2 = subprocess.run(
    ["pdftotext", "-layout", str(rwt_results_path), "-"],
    capture_output=True, text=True
)
rwt_results_text = result2.stdout

# Find Measure 8 section
m8_results = re.search(
    r'8\.\s*Data Export(.*?)(?=Key Milestones|Standards Updates|Attestation|$)',
    rwt_results_text, re.DOTALL
)

artifacts.append({
    "file": "Real-World-Testing-Results-2025.pdf",
    "type": "PDF (11 pages)",
    "size_bytes": os.path.getsize(rwt_results_path),
    "description": "2025 Real World Testing Results; b(10) Measure 8 dropped per EO 14192",
    "key_claims": [
        "Data Export metric ceased collection after Q2 2025 per Executive Order 14192",
        "Only g(10) metrics (3 & 5) collected for full year",
        "Zero real production customer usage of FHIR API in 2025",
        "Darena Health migration completed in Q4 2025"
    ]
})

# 4. Screenshots
for img in ["registered-url-fullpage.png", "fhir-api-page.png"]:
    img_path = BASE / "downloads" / img
    artifacts.append({
        "file": img,
        "type": "Screenshot (PNG)",
        "size_bytes": os.path.getsize(img_path),
        "description": f"Screenshot of {'registered URL' if 'registered' in img else 'FHIR API specs page'}"
    })

# Since the data dictionary is not publicly available, we document what we know
# about the export structure from the available documentation
export_structure = {
    "format": "ZIP archive",
    "contents_per_patient": [
        {"type": "CSV files", "description": "Machine-readable EHI data"},
        {"type": "Image files", "description": "All clinical images from patient record (wound photos)"},
        {"type": "Custom scans", "description": "All scanned documents on file"},
        {"type": "EHIDataExtract_DataDictionary.xlsx", "description": "Excel data dictionary documenting CSV contents"},
        {"type": "ExportSummary.txt", "description": "Plain text summary of the export"}
    ],
    "export_modes": [
        {
            "role": "Facility Administrator",
            "capability": "Generate CDA file with treatment information for date/time range",
            "scope": "One or more patients"
        },
        {
            "role": "Net Health Administrator",
            "capability": "Full facility EHI export with PDF medical records and all EHI in CSV files",
            "scope": "Full facility"
        }
    ],
    "data_dictionary_publicly_available": False,
    "sample_data_available": False,
    "schema_available": False,
    "field_level_documentation_available": False
}

# Produce the output
output = {
    "product": "WoundDocs (WoundExpert)",
    "developer": "Net Health",
    "chpl_id": "15.04.04.2272.Woun.07.01.1.191224",
    "analysis_date": "2026-02-16",
    "data_dictionary_available": False,
    "data_dictionary_note": "EHIDataExtract_DataDictionary.xlsx is bundled inside export ZIPs only; not publicly downloadable",
    "artifacts_reviewed": artifacts,
    "export_structure": export_structure,
    "entities": "N/A - no public data dictionary",
    "fields": "N/A - no public data dictionary",
    "entity_inventory": None
}

# Write full inventory (which is essentially empty since no data dictionary is available)
with open(Path(__file__).parent / "entity-inventory-full.json", "w") as f:
    json.dump({
        "product": "WoundDocs (WoundExpert)",
        "developer": "Net Health",
        "data_dictionary_available": False,
        "reason": "The data dictionary (EHIDataExtract_DataDictionary.xlsx) is only included inside actual export ZIP files and is not publicly downloadable. No sample exports, schemas, or field-level documentation are publicly available.",
        "entities": [],
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0
    }, f, indent=2)

# Write summary
summary = {
    "product": "WoundDocs (WoundExpert)",
    "developer": "Net Health",
    "chpl_product_number": "15.04.04.2272.Woun.07.01.1.191224",
    "analysis_date": "2026-02-16",
    "total_entities": "N/A",
    "total_fields": "N/A",
    "fields_with_descriptions": "N/A",
    "pct_fields_with_descriptions": "N/A",
    "export_format": "ZIP (CSV + images + scans + XLSX data dictionary + TXT summary)",
    "data_dictionary_public": False,
    "sample_data_available": False,
    "export_modes": 2,
    "single_patient_export": True,
    "bulk_export": True,
    "documented_export_contents": [
        "CSV files of EHI data",
        "All image files from patient record",
        "All custom scans on file",
        "EHIDataExtract_DataDictionary.xlsx",
        "ExportSummary.txt"
    ],
    "artifacts_reviewed_count": len(artifacts),
    "key_finding": "No public data dictionary or field-level documentation. The EHI export appears purpose-built (CSV+images in ZIP, separate from FHIR API), but its actual content scope cannot be verified without access to an actual export."
}

with open(Path(__file__).parent / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

with open(Path(__file__).parent / "artifacts-analysis.json", "w") as f:
    json.dump(output, f, indent=2)

print("Analysis complete.")
print(f"Artifacts reviewed: {len(artifacts)}")
print(f"Data dictionary publicly available: No")
print(f"Entity inventory: N/A (no public data dictionary)")
print(f"Output files: entity-inventory-full.json, entity-inventory-summary.json, artifacts-analysis.json")
