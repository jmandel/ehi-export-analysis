"""
Parse the Net Health WoundExpert certification page to extract the EHI export section
and any other structured content relevant to the (b)(10) analysis.
"""
import json
import re
from html.parser import HTMLParser

# Read the certification page text
with open("downloads/certification-page-text.txt", "r") as f:
    text = f.read()

# Extract the EHI Export section
ehi_section = {}

# The text contains the EHI export description
lines = text.split('\n')
in_ehi = False
ehi_lines = []
for line in lines:
    if 'Electronic Health Information Export' in line:
        in_ehi = True
        continue
    if in_ehi:
        if 'Costs and Criteria' in line:
            in_ehi = False
            continue
        ehi_lines.append(line.strip())

ehi_text = '\n'.join(l for l in ehi_lines if l)

# Extract key facts
ehi_section = {
    "section_title": "Electronic Health Information Export",
    "raw_text": ehi_text,
    "export_format": "ZIP file",
    "export_contents": [
        "CSV files of EHI data",
        "All image files from the patient record",
        "All custom scans on file",
        "EHIDataExtract_DataDictionary.xlsx (Excel data dictionary)",
        "ExportSummary.txt (export summary)"
    ],
    "patient_scope": ["single patient", "patient population"],
    "standard_reference": "§170.315(b)(10)",
    "data_dictionary_public": False,
    "data_dictionary_location": "Inside export ZIP only",
    "downloadable_artifacts": [],
    "sample_data_available": False,
    "csv_file_names_documented": False,
    "field_definitions_documented": False,
    "value_sets_documented": False,
    "relationships_documented": False,
}

# Additional info from RWT Plan (OCR'd)
rwt_plan_info = {
    "source": "Real World Testing Plan 2025 (OCR of PDF)",
    "export_tool_description": (
        "Net Health has built a data export tool to meet this certification criterion. "
        "Users with a Facility Administrator user role can generate and download a CDA file "
        "containing relevant treatment information for one or more patients in a specific date and time range. "
        "Additionally, Net Health Administrators can execute full facility EHI exports, "
        "that include the patient medical records in PDF format and all EHI in CSV files."
    ),
    "user_roles_for_export": ["Facility Administrator (CDA files)", "Net Health Administrator (full EHI exports)"],
    "export_types": [
        {"type": "CDA file", "scope": "one or more patients", "role": "Facility Administrator", "content": "relevant treatment information"},
        {"type": "Full EHI export", "scope": "full facility", "role": "Net Health Administrator", "content": "patient medical records in PDF + all EHI in CSV"}
    ],
    "import_support": "File can be imported into another CEHRT or EMR that supports the file format"
}

output = {
    "product": "Net Health® WoundExpert",
    "chpl_id": "15.04.04.2815.Woun.07.00.1.181231",
    "ehi_export_section": ehi_section,
    "rwt_plan_additional_info": rwt_plan_info,
    "artifacts_available": {
        "certification_page": True,
        "certification_page_text": True,
        "certification_page_screenshot": True,
        "rwt_results_2025_pdf": True,
        "rwt_plan_2025_pdf": True,
        "data_dictionary": False,
        "sample_export": False,
        "user_guide": False,
        "schema": False,
    }
}

with open("analysis/certification-page-parsed.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
