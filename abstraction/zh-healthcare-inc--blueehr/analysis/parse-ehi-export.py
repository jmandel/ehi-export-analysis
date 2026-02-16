#!/usr/bin/env python3
"""
Parse the BlueEHR EHI Export PDF and produce structured JSON inventories.

The PDF is only 2 pages with no data dictionary — just 3 export mechanisms
described at category level. This script extracts what's there and produces
the entity-inventory-full.json and entity-inventory-summary.json files.
"""

import json
import subprocess
import os

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(WORK_DIR)

# Extract PDF text for reference
pdf_path = os.path.join(PARENT_DIR, "downloads", "EHI_Export.pdf")
result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
pdf_text = result.stdout

# Save extracted text
with open(os.path.join(WORK_DIR, "ehi-export-pdf-text.txt"), "w") as f:
    f.write(pdf_text)

# C-CDA export components (from screenshot inspection of Care Coordination UI)
ccda_components = [
    "Allergies",
    "Problems",
    "Procedures",
    "Plan Of Care",
    "Social History",
    "Functional Status",
    "Instructions",
    "Mental Status",
    "Progress Notes",
    "Medications",
    "Immunizations",
    "Results",
    "Vitals",
    "Encounters",
    "Reason for Referral",
    "Implanted Devices",
    "Goals",
    "Health Concerns",
]

# Analytics CSV/XLS export categories (from PDF text)
analytics_categories = [
    "Demographic details",
    "Insurance details",
    "Payments",
    "Lab results",
    "Encounters",
    "Appointment details",
]

# Document export (from PDF text)
document_export = ["Patient documents"]

# Billing Manager items visible in screenshot (not mentioned as part of EHI export)
billing_manager_visible = [
    "Payment",
    "Payment Return",
    "Claims Manager",
    "Claims History",
    "Payment Manager",
    "Patient Ledger",
    "Batch Charge",
    "ERA Posting",
    "ERA Download",
    "Patient Statement",
]

# Main Menu items visible in screenshot
main_menu_visible = [
    "Analytics", "Calendar", "Insurance", "Users", "Messaging", "Tasks",
    "Facility", "Tel Upgrade", "Care Coordination", "Address Book", "Lab",
    "Pharmacy", "Rule Engine", "CDR Engine", "Pending Appointments",
    "Amendments", "Merge Patients", "Inventory", "Inventory Dispense",
    "Renew Med Requests", "Forms Tracker", "Forms Template Manager",
    "Referral Management", "Signature Dashboard", "Settings", "Fax",
    "IP Settings",
]

# Build entity inventory
# Since there is NO data dictionary, we document what the vendor describes
# at category level only. No field-level information exists.

entities = []

# C-CDA components as "entities" (category-level only)
for comp in ccda_components:
    entities.append({
        "name": comp,
        "export_mechanism": "C-CDA via Care Coordination",
        "format": "C-CDA (XML)",
        "category": "Clinical Data",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "No field-level documentation provided. This is a C-CDA section/component — fields follow the C-CDA standard but vendor provides no product-specific mapping or data dictionary."
    })

# Analytics export categories
for cat in analytics_categories:
    entities.append({
        "name": cat,
        "export_mechanism": "CSV/XLS via Analytics",
        "format": "CSV or XLS",
        "category": "Administrative/Financial Data",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "notes": "No field-level documentation provided. No column definitions, no sample data, no schema."
    })

# Document export
entities.append({
    "name": "Patient Documents",
    "export_mechanism": "Document Module",
    "format": "Unknown (original document formats)",
    "category": "Documents",
    "fields": [],
    "field_count": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "notes": "No details provided about document types, formats, or metadata exported."
})

# Full inventory
inventory_full = {
    "product": "BlueEHR 3",
    "vendor": "ZH Healthcare, Inc.",
    "source_artifact": "downloads/EHI_Export.pdf",
    "source_artifact_pages": 2,
    "source_artifact_date": "2023-09-15",
    "has_data_dictionary": False,
    "has_field_level_documentation": False,
    "has_sample_data": False,
    "has_schema": False,
    "total_entities": len(entities),
    "total_fields": 0,
    "total_fields_with_descriptions": 0,
    "total_fields_with_types": 0,
    "export_mechanisms": [
        {
            "name": "C-CDA via Care Coordination",
            "format": "C-CDA (XML)",
            "scope": "Clinical data",
            "components": ccda_components,
            "component_count": len(ccda_components),
            "supports_multi_patient": True,
            "notes": "Users select data categories via checkboxes. This appears to be the same Care Coordination / Transitions of Care feature used for (b)(1) certification."
        },
        {
            "name": "CSV/XLS via Analytics",
            "format": "CSV or XLS",
            "scope": "Demographics, insurance, payments, labs, encounters, appointments",
            "categories": analytics_categories,
            "category_count": len(analytics_categories),
            "supports_multi_patient": True,
            "notes": "Export via the Analytics reporting feature. No field definitions provided."
        },
        {
            "name": "Document Module",
            "format": "Unknown",
            "scope": "Patient-attached documents",
            "notes": "Brief mention only. No details on process, format, or metadata."
        }
    ],
    "entities": entities,
    "billing_manager_modules_visible_in_screenshot_but_not_in_export": billing_manager_visible,
    "main_menu_modules_visible_in_screenshot": main_menu_visible
}

with open(os.path.join(WORK_DIR, "entity-inventory-full.json"), "w") as f:
    json.dump(inventory_full, f, indent=2)

# Summary
summary = {
    "product": "BlueEHR 3",
    "vendor": "ZH Healthcare, Inc.",
    "has_data_dictionary": False,
    "has_field_level_documentation": False,
    "has_sample_data": False,
    "has_schema": False,
    "total_documented_categories": len(entities),
    "total_fields_documented": 0,
    "export_mechanisms_count": 3,
    "by_export_mechanism": {
        "C-CDA via Care Coordination": {
            "category_count": len(ccda_components),
            "categories": ccda_components,
            "format": "C-CDA (XML)",
            "field_count": 0
        },
        "CSV/XLS via Analytics": {
            "category_count": len(analytics_categories),
            "categories": analytics_categories,
            "format": "CSV or XLS",
            "field_count": 0
        },
        "Document Module": {
            "category_count": 1,
            "categories": ["Patient Documents"],
            "format": "Unknown",
            "field_count": 0
        }
    },
    "by_vendor_category": {
        "Clinical Data (C-CDA)": {
            "entity_count": len(ccda_components),
            "field_count": 0,
            "description": "18 C-CDA component categories selectable via checkboxes"
        },
        "Administrative/Financial Data (CSV/XLS)": {
            "entity_count": len(analytics_categories),
            "field_count": 0,
            "description": "6 data categories exportable via Analytics feature"
        },
        "Documents": {
            "entity_count": 1,
            "field_count": 0,
            "description": "Patient-attached documents via document module"
        }
    },
    "documentation_quality": {
        "pages": 2,
        "pages_with_content": 1,
        "screenshots": 2,
        "field_definitions": 0,
        "sample_exports": 0,
        "schema_files": 0,
        "data_dictionary_entries": 0
    }
}

with open(os.path.join(WORK_DIR, "entity-inventory-summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

print(f"Total documented categories: {len(entities)}")
print(f"  C-CDA components: {len(ccda_components)}")
print(f"  Analytics categories: {len(analytics_categories)}")
print(f"  Document export: 1")
print(f"Total field-level documentation: 0")
print(f"Output: entity-inventory-full.json, entity-inventory-summary.json")
