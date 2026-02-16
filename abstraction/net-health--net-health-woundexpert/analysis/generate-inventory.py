"""
Generate entity-inventory-full.json and entity-inventory-summary.json
Since no data dictionary is publicly available, we document what is known
from the certification page and RWT plan about the export structure.
"""
import json

# No data dictionary is available. The export includes:
# - CSV files (unnamed/undocumented)
# - Image files
# - Custom scans
# - EHIDataExtract_DataDictionary.xlsx (inside the ZIP only)
# - ExportSummary.txt

# We can only document what is mentioned, not actual entities/fields
inventory = {
    "source": "No public data dictionary available",
    "data_dictionary_exists": True,
    "data_dictionary_public": False,
    "data_dictionary_location": "EHIDataExtract_DataDictionary.xlsx bundled inside each export ZIP file",
    "entities": [],
    "known_export_components": [
        {
            "component": "CSV files",
            "description": "CSV files of EHI data - specific files and fields are not publicly documented",
            "format": "CSV",
            "count": "unknown"
        },
        {
            "component": "Image files",
            "description": "All image files from the patient record (likely wound photographs)",
            "format": "image (format unspecified)",
            "count": "varies per patient"
        },
        {
            "component": "Custom scans",
            "description": "All custom scans on file for the patient",
            "format": "unspecified",
            "count": "varies per patient"
        },
        {
            "component": "EHIDataExtract_DataDictionary.xlsx",
            "description": "Excel data dictionary describing the CSV file structure",
            "format": "XLSX",
            "count": "1 per export"
        },
        {
            "component": "ExportSummary.txt",
            "description": "Text summary of the export",
            "format": "TXT",
            "count": "1 per export"
        }
    ],
    "notes": [
        "The data dictionary (EHIDataExtract_DataDictionary.xlsx) is only available inside the export ZIP, not publicly downloadable.",
        "No CSV file names, field names, data types, relationships, or value sets are publicly documented.",
        "The RWT Plan 2025 mentions two export types: CDA files (Facility Administrator) and full EHI exports with CSV+PDF (Net Health Administrator).",
        "The certification page states content varies 'depending on number of patients selected and software functionality in use'.",
        "Without access to the actual data dictionary or a sample export, it is impossible to enumerate entities or fields."
    ]
}

with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

summary = {
    "total_entities": "N/A - no public data dictionary",
    "total_fields": "N/A",
    "fields_with_descriptions": "N/A",
    "fields_with_types": "N/A",
    "categories": "N/A",
    "data_dictionary_format": "XLSX (inside export ZIP only)",
    "public_documentation_word_count": 97,  # approximate word count of the EHI section
    "export_components": 5,
    "export_format": "ZIP containing: CSVs, images, scans, XLSX data dictionary, TXT summary"
}

with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("entity-inventory-full.json and entity-inventory-summary.json generated.")
print(json.dumps(summary, indent=2))
