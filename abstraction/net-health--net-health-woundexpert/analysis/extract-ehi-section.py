#!/usr/bin/env python3
"""Extract and structure all EHI-related content from the certification page HTML."""

import re
import json

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/net-health--net-health-woundexpert"

with open(f"{RESULTS_DIR}/downloads/certification-page.html") as f:
    html = f.read()

with open(f"{RESULTS_DIR}/downloads/certification-page-text.txt") as f:
    text = f.read()

# Extract key info
output = {
    "source_file": "downloads/certification-page.html",
    "source_url": "https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/",
    "html_size_bytes": len(html.encode('utf-8')),
    "text_size_bytes": len(text.encode('utf-8')),
    "ehi_section": {
        "title": "Electronic Health Information Export",
        "description": (
            'Single patient and patient population electronic health information '
            'can be exported in the form of an "export zip" file which contains '
            'files in a machine-readable format in accordance with §170.315(b)(10) '
            '– Electronic Health Information export of the ONC 2015 Edition Cures '
            'Update Certification Criteria.'
        ),
        "variability_note": (
            "The content and format of the data contained within the export zip "
            "file depending on number of patients selected and software "
            "functionality in use."
        ),
        "export_contents": [
            {"item": "csv files of EHI data", "description": "CSV files containing electronic health information"},
            {"item": "all image files from the patient record", "description": "Image files (wound photos, etc.)"},
            {"item": "all custom scans on file", "description": "Custom scanned documents"},
            {"item": "EHIDataExtract_DataDictionary.xlsx", "description": "Excel data dictionary (bundled in export, not publicly available)"},
            {"item": "ExportSummary.txt", "description": "Text summary of the export"}
        ],
        "structure": "ZIP file containing one folder per patient",
        "supports_single_patient": True,
        "supports_bulk_population": True,
        "export_format": "CSV (within ZIP)",
        "data_dictionary_format": "XLSX (bundled in export)",
    },
    "publicly_documented_csv_names": [],
    "publicly_documented_fields": [],
    "publicly_documented_value_sets": [],
    "sample_data_available": False,
    "data_dictionary_publicly_available": False,
    "export_instructions_available": False,
    "downloadable_artifacts": [],
    "total_ehi_documentation_words": None,
}

# Count words in EHI section
ehi_text = (
    output["ehi_section"]["description"] + " " +
    output["ehi_section"]["variability_note"] + " " +
    " ".join(item["item"] for item in output["ehi_section"]["export_contents"])
)
output["total_ehi_documentation_words"] = len(ehi_text.split())

# Check for any downloadable file links
file_patterns = re.findall(
    r'href="([^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*)"',
    html, re.IGNORECASE
)
output["downloadable_artifacts"] = [{"url": url, "type": ext} for url, ext in file_patterns]

print(json.dumps(output, indent=2))

with open("ehi-section-extract.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nTotal EHI documentation: {output['total_ehi_documentation_words']} words")
print(f"Downloadable artifacts found on page: {len(output['downloadable_artifacts'])}")
print(f"CSV names documented: {len(output['publicly_documented_csv_names'])}")
print(f"Fields documented: {len(output['publicly_documented_fields'])}")
print(f"Data dictionary publicly available: {output['data_dictionary_publicly_available']}")
