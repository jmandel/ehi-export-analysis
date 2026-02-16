#!/usr/bin/env python3
"""Extract the complete list of selectable data categories from the EHI Export UI screenshots.

From the PDF screenshots (pages 4 and 9), the EHI-Export-Request window shows:
- Top-level checkboxes: Medical Records, Patient Demographics, All POS Documents
- Message Type: CCD or Referral
- C-CDA/Referral Summary section with individual checkboxes

This script documents all visible checkboxes from the UI screenshots and maps them
to the C-CDA data dictionary sections.
"""

import json

# Extracted from visual inspection of page 4 and page 9 screenshots
# Both single-patient and bulk-patient UIs show identical checkbox sets

ui_checkboxes = {
    "top_level_checkboxes": [
        "Medical Records",
        "Patient Demographics", 
        "All POS Documents"
    ],
    "message_type": ["CCD", "Referral"],
    "ccda_referral_summary_checkboxes": [
        # Row 1
        "Patient Name",
        "Sex",
        "DOB",
        "Race",
        # Row 2
        "Ethnicity",
        "Preferred Language",
        "Social History/Smoking Status",
        "Problems",
        # Row 3
        "Medications",
        "Medication Allergies",
        "Lab Tests",
        "Lab Values/Results",
        # Row 4
        "Vital Signs",
        "Care Plan (Goals and Instructions)",
        "Procedures",
        "Care team Members",
        # Row 5
        "Provider's name and office Contact info",
        "Date and Location of Visit",
        "Chief Complaint/Reason for visit",
        "Immunizations",
        # Row 6
        "Medication Administered",
        "Diagnostic Pending Test",
        "Clinical Instructions",
        "Future Appointments",
        # Row 7
        "Referrals",
        "Future Scheduled Tests",
        "Recommended Patient decision Aids",
        "Encounter/Final Diagnosis",
        # Row 8
        "Functional and Status",
        "Assessment",
        "Goals",
        "HealthConcerns",
        # Row 9
        "MentalStatus",
        "Interventions",
        "Medical Device Equipment",
        "HPI",
        # Row 10
        "General Status",
        "Physical Exam",
        "ROS",
        "Past Medical History",
        # Row 11
        "Clinical Notes"
    ],
    "total_ccda_checkboxes": 0,  # will be computed
    "notes": [
        "All checkboxes appear checked by default in screenshots",
        "UI also has 'Legal Authenticator' dropdown and 'Reason' text field",
        "Single Patient mode: search by Patient Name, select encounters",
        "Multiple Patients mode: search by date range, Resource, Physicians",
        "'Decline to Specify' checkbox visible at bottom"
    ]
}

ui_checkboxes["total_ccda_checkboxes"] = len(ui_checkboxes["ccda_referral_summary_checkboxes"])

print(f"=== EHI Export UI Checkbox Inventory ===")
print(f"Top-level checkboxes: {len(ui_checkboxes['top_level_checkboxes'])}")
print(f"  " + ", ".join(ui_checkboxes['top_level_checkboxes']))
print(f"Message types: {len(ui_checkboxes['message_type'])}")
print(f"C-CDA/Referral Summary checkboxes: {ui_checkboxes['total_ccda_checkboxes']}")
for i, cb in enumerate(ui_checkboxes['ccda_referral_summary_checkboxes'], 1):
    print(f"  {i:2d}. {cb}")

with open('ui-checkbox-inventory.json', 'w') as f:
    json.dump(ui_checkboxes, f, indent=2)

print(f"\nUI inventory written to ui-checkbox-inventory.json")
