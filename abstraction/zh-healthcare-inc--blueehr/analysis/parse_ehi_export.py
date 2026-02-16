#!/usr/bin/env python3
"""
Parse the BlueEHR EHI Export PDF and extract structured data about
the export mechanisms and data categories mentioned.

Input: EHI_Export.pdf (via pdftotext output + manual image analysis)
Output: full-entity-inventory.json, export_summary.json
"""
import json
import os

# Data extracted from the PDF text and rendered page images.
# The PDF has exactly 2 pages: a cover page and one content page.

# C-CDA export checkboxes visible in the Care Coordination screenshot (page 2)
ccda_components = [
    "Allergies",
    "Problems",
    "Procedures",
    "Plan Of Care",
    "Social History",
    "Functional Status",
    "Deformities",
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

# Analytics/CSV export categories mentioned in PDF text
analytics_categories = [
    "Demographic details",
    "Insurance details",
    "Payments",
    "Lab results",
    "Encounters",
    "Appointment details",
]

# Document export
document_export = ["Patient documents (attached records)"]

# Main menu items visible in the second screenshot (the Analytics menu screenshot)
# This reveals what modules BlueEHR actually has
main_menu_items = {
    "Main Menu": [
        "Calendar", "Users", "Messaging", "Tasks", "Facility",
        "Insurance", "Rx Upgrade", "Care Coordination", "Address Book", "Lab",
        "Analytics", "Pharmacy", "Rule Engine", "CDR Engine", "Pending Appointments",
        "Amendments", "Merge Patients", "Inventory", "Inventory Dispenser", "Review Med Requests",
        "Forms Tracker", "Forms Template Manager", "Referral Management", "Signature Dashboard", "Settings",
        "Fax", "IP Settings",
    ],
    "Billing Manager": [
        "Payment", "Payment Return", "Claims Manager", "Claims History", "Payment Manager",
        "Patient Ledger", "Batch Charge", "ERA Posting", "ERA Download", "Patient Statement",
        "Re-bill", "AR Posting", "Posting Document Details", "Eligibility Report", "Transaction Log",
    ],
}

# Build the full entity inventory
# Since there is NO data dictionary, we document what the PDF describes at category level
entities = []

# C-CDA components as "entities" (no field-level detail available)
for comp in ccda_components:
    entities.append({
        "name": comp,
        "export_mechanism": "C-CDA (Care Coordination)",
        "format": "C-CDA XML",
        "fields": None,
        "field_count": None,
        "fields_with_descriptions": 0,
        "types_documented": False,
        "description": f"C-CDA section: {comp}. No field-level documentation provided.",
        "category": "Clinical (C-CDA)",
    })

# Analytics CSV categories
for cat in analytics_categories:
    entities.append({
        "name": cat,
        "export_mechanism": "Analytics (CSV/XLS)",
        "format": "CSV or XLS",
        "fields": None,
        "field_count": None,
        "fields_with_descriptions": 0,
        "types_documented": False,
        "description": f"Analytics export category: {cat}. No field-level documentation provided.",
        "category": "Administrative/Analytics (CSV)",
    })

# Document export
entities.append({
    "name": "Patient Documents",
    "export_mechanism": "Document Module",
    "format": "Unknown (original document format)",
    "fields": None,
    "field_count": None,
    "fields_with_descriptions": 0,
    "types_documented": False,
    "description": "Documents attached to patient records. No further detail provided.",
    "category": "Documents",
})

# Summary
summary = {
    "product": "BlueEHR Version 3",
    "vendor": "ZH Healthcare, Inc.",
    "documentation_artifact": "EHI_Export.pdf",
    "documentation_pages": 2,
    "documentation_content_pages": 1,
    "documentation_date": "2023-09-15",
    "documentation_author": "Munawar Peringadi Vayalil",
    "export_mechanisms": [
        {
            "name": "C-CDA Clinical Export",
            "feature": "Care Coordination",
            "format": "C-CDA XML",
            "components": ccda_components,
            "component_count": len(ccda_components),
        },
        {
            "name": "Analytics Export",
            "feature": "Analytics",
            "format": "CSV or XLS",
            "categories": analytics_categories,
            "category_count": len(analytics_categories),
        },
        {
            "name": "Document Export",
            "feature": "Document Module",
            "format": "Original document format",
            "description": "Documents attached to patient records",
        },
    ],
    "data_dictionary_provided": False,
    "field_level_documentation": False,
    "schema_provided": False,
    "sample_data_provided": False,
    "total_documented_categories": len(ccda_components) + len(analytics_categories) + 1,
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "relationships_documented": False,
    "value_sets_documented": False,
    "main_menu_modules_visible": main_menu_items,
    "billing_modules_visible_but_not_in_export": main_menu_items["Billing Manager"],
}

# Write outputs
output_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(output_dir, "full-entity-inventory.json"), "w") as f:
    json.dump(entities, f, indent=2)

with open(os.path.join(output_dir, "export_summary.json"), "w") as f:
    json.dump(summary, f, indent=2)

# Print summary stats
print(f"Total export categories documented: {summary['total_documented_categories']}")
print(f"  C-CDA components: {len(ccda_components)}")
print(f"  Analytics categories: {len(analytics_categories)}")
print(f"  Document export: 1")
print(f"Field-level documentation: NONE")
print(f"Data dictionary: NONE")
print(f"Schema files: NONE")
print(f"Sample data: NONE")
print(f"\nBilling modules visible in screenshot but NOT in export:")
for m in main_menu_items["Billing Manager"]:
    print(f"  - {m}")
print(f"\nTotal billing modules visible: {len(main_menu_items['Billing Manager'])}")
