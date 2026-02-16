"""
Analyze the ZoomMD EHI Export Format Specification PDF.
Extracts text, counts pages, identifies sections, and catalogs what information
is present vs absent. Outputs a structured JSON summary.
"""
import subprocess
import json
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/metasolutions-inc--zoommd"
PDF_PATH = os.path.join(RESULTS_DIR, "downloads", "ZoomMD_EHI_Export_Format_Specification.pdf")
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/metasolutions-inc--zoommd/analysis"

# Get PDF metadata
pdfinfo = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
info_lines = pdfinfo.stdout.strip().split("\n")
metadata = {}
for line in info_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Extract full text
pdftext = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
full_text = pdftext.stdout

# Analyze content
lines = [l.strip() for l in full_text.split("\n") if l.strip()]
total_lines = len(lines)

# Identify what the PDF documents
export_formats_mentioned = []
if "C-CDA" in full_text:
    export_formats_mentioned.append("C-CDA R2.1")
if "PDF" in full_text:
    export_formats_mentioned.append("PDF documents")
if "html" in full_text.lower():
    export_formats_mentioned.append("HTML clinical notes")
if "JPEG" in full_text or "JPG" in full_text or "PNG" in full_text:
    export_formats_mentioned.append("Image files (JPEG, JPG, PNG)")

# Count screenshots (steps mentioned)
steps = [l for l in lines if l and l[0].isdigit() and "." in l[:4]]

# Check for data dictionary elements
has_data_dictionary = False
has_field_definitions = False
has_schema = False
has_sample_data = False
has_table_definitions = False
has_value_sets = False
has_relationships = False

for indicator in ["field", "column", "attribute", "property", "element"]:
    if indicator in full_text.lower():
        # Check context - is it describing data fields or UI elements?
        pass

# Build inventory of what IS documented
documented_items = {
    "export_mechanism": True,  # UI navigation path described
    "export_format_container": True,  # ZIP file
    "export_format_contents": ["C-CDA R2.1", "PDF", "HTML", "Images"],
    "single_patient_export": True,
    "multi_patient_export": True,
    "scheduled_export": True,
    "role_based_access": True,
    "re_download_capability": True,
    "no_developer_assistance_needed": True,
}

not_documented = {
    "data_dictionary": True,
    "field_level_specification": True,
    "schema_files": True,
    "sample_data": True,
    "ccda_sections_populated": True,
    "ccda_template_customizations": True,
    "billing_data_handling": True,
    "scheduling_data_handling": True,
    "insurance_data_handling": True,
    "portal_data_handling": True,
    "data_model_mapping": True,
    "value_sets": True,
    "foreign_key_relationships": True,
    "versioning_or_changelog": True,
}

# UI modules visible in screenshots (from page 2 and 4 navigation menus)
ui_modules_visible = [
    "Settings",
    "Demographics",
    "Charting",
    "Scheduler",
    "Billing",
    "Reports",
    "Messages",
    "Dashboard",
    "Admin",
    "Manage List",
    "Clinical Settings",
    "Interoperability",
    "Ordering Portlets",
    "Transition of Care",
    "Data Export",
]

result = {
    "pdf_metadata": {
        "title": metadata.get("Title", ""),
        "author": metadata.get("Author", ""),
        "pages": int(metadata.get("Pages", 0)),
        "creation_date": metadata.get("CreationDate", ""),
        "file_size_bytes": int(metadata.get("File size", "0").split()[0]),
        "pdf_version": metadata.get("PDF version", ""),
    },
    "content_analysis": {
        "total_text_lines": total_lines,
        "numbered_steps": len(steps),
        "export_formats_mentioned": export_formats_mentioned,
        "pages_with_screenshots": 3,  # Pages 2, 3, 4 have screenshots
        "pages_with_text_only": 1,    # Page 1 is header + brief description
    },
    "what_is_documented": documented_items,
    "what_is_not_documented": not_documented,
    "ui_modules_visible_in_screenshots": ui_modules_visible,
    "standards_referenced": [
        "C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2"
    ],
    "export_ui_path": "Settings > Interoperability > Data Export > Generate Summaries",
    "patient_search_fields": [
        "Practice Physician",
        "Referring Physician",
        "First Name",
        "Last Name",
        "SSN",
        "DOB",
        "Gender",
        "Site Name",
        "Start Date / End Date / Time",
        "Relative Data"
    ],
}

# Write output
output_path = os.path.join(OUTPUT_DIR, "pdf-analysis.json")
with open(output_path, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
print(f"\nSaved to {output_path}")
