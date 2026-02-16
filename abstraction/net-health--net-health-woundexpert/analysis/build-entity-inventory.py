#!/usr/bin/env python3
"""
Create the full entity inventory based on what's publicly documented.
Since Net Health does not publish their data dictionary (it's bundled in the export ZIP),
we can only document the export structure, not the CSV contents.
"""

import json

inventory = {
    "metadata": {
        "product": "Net Health® WoundExpert",
        "chpl_ids": [9836, 10234],
        "source": "https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/",
        "extraction_date": "2026-02-16",
        "note": (
            "No data dictionary is publicly available. The vendor bundles an Excel data dictionary "
            "(EHIDataExtract_DataDictionary.xlsx) inside each export ZIP, but it is not downloadable "
            "from their website. Zero CSV file names, zero field names, zero data types, and zero "
            "value sets are documented publicly."
        ),
    },
    "export_format": {
        "container": "ZIP file",
        "structure": "One folder per patient",
        "data_format": "CSV",
        "supplementary_files": [
            "EHIDataExtract_DataDictionary.xlsx",
            "ExportSummary.txt",
        ],
        "includes_images": True,
        "includes_custom_scans": True,
    },
    "entities": [],
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "data_dictionary_available": False,
    "parse_status": "no_data_dictionary_available",
    "parse_error_note": (
        "The vendor's data dictionary (EHIDataExtract_DataDictionary.xlsx) exists only inside "
        "the export ZIP. It is not hosted publicly, linked from the certification page, or "
        "available via WordPress media API. Without access to this file, no entities or fields "
        "can be inventoried. The public documentation consists of 87 words describing only the "
        "container format (ZIP with CSVs, images, scans, dictionary, summary)."
    ),
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print(json.dumps(inventory, indent=2))
print(f"\nEntities documented: {inventory['total_entities']}")
print(f"Fields documented: {inventory['total_fields']}")
