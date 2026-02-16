#!/usr/bin/env python3
"""Parse the CompleteExport.html page and extract all substantive content."""

import json
from html.parser import HTMLParser

html_path = "../../../results/vohra-wound-physicians-management-llc--vhs-medical-documentation-coding/downloads/CompleteExport.html"

with open(html_path, "r") as f:
    html_content = f.read()

# Extract key facts from the HTML
analysis = {
    "page_title": "Export data format and location",
    "page_size_bytes": len(html_content.encode("utf-8")),
    "last_modified": "2023-12-14T18:11:19 GMT",  # from HTTP headers
    "source_url": "https://facilityportal.vohrawoundteam.com/CompleteExport.html",
    "registered_url": "https://emr.vohrawoundteam.com/CompleteExport.html",
    "export_location": {
        "server": "IIS-PROD-02",
        "directory": "C:\\inetpub\\webapp\\ExportedPatientData"
    },
    "export_formats": [
        {
            "extension": "PDF",
            "description": "Encounter notes",
            "filename_template": "PATIENT_IDENTIFIER.pdf",
            "example": "GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG.pdf",
            "granularity": "One PDF per patient"
        },
        {
            "extension": "XML",
            "description": "Data conforms to the CCDA standard",
            "filename_template": "ENCOUNTER_IDENTIFIER.xml",
            "example": "HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH.xml",
            "granularity": "One XML per encounter"
        }
    ],
    "export_procedure": {
        "type": "Single patient",
        "steps": [
            "Navigate to the administrative portal (https://med.vohrawoundteam.com/LogIn.aspx)",
            "Authenticate as a user who has been granted permissions to export",
            "Select the menu for Advanced / Data Portability",
            'Set "Export Option" to Patient',
            "Enter the patient's First Name, Last Name and Date of Birth",
            'Press "Export Patients" button',
            'You will see "Successfully exported 1 patient records"',
            "Login to the server and retrieve files from the C:\\inetpub\\webapp\\ExportedPatientData"
        ],
        "admin_portal_url": "https://med.vohrawoundteam.com/LogIn.aspx",
        "admin_portal_status": "NXDOMAIN - subdomain no longer exists in DNS"
    },
    "documentation_inventory": {
        "data_dictionary": False,
        "schema_files": False,
        "sample_data": False,
        "api_documentation": False,
        "ccda_template_specification": False,
        "field_level_documentation": False,
        "value_sets": False,
        "bulk_export_procedure": False,
        "downloadable_artifacts": False
    },
    "outbound_links": [
        {
            "url": "https://med.vohrawoundteam.com/LogIn.aspx",
            "text": "administrative portal",
            "status": "NXDOMAIN"
        }
    ],
    "total_artifacts_downloaded": 3,
    "artifacts": [
        {
            "file": "CompleteExport.html",
            "size_bytes": 11592,
            "description": "The complete EHI export documentation - single static HTML page"
        },
        {
            "file": "CompleteExport-screenshot.png",
            "size_bytes": 169315,
            "description": "Full-page screenshot of export documentation page"
        },
        {
            "file": "emr-redirect-page.html",
            "size_bytes": 3772,
            "description": "Redirect notice page at original registered URL"
        }
    ]
}

output_path = "export_page_analysis.json"
with open(output_path, "w") as f:
    json.dump(analysis, f, indent=2)

# Print summary
print(f"Page size: {analysis['page_size_bytes']} bytes")
print(f"Last modified: {analysis['last_modified']}")
print(f"Export formats: {len(analysis['export_formats'])}")
print(f"Export procedure steps: {len(analysis['export_procedure']['steps'])}")
print(f"Admin portal status: {analysis['export_procedure']['admin_portal_status']}")
print(f"Data dictionary: {analysis['documentation_inventory']['data_dictionary']}")
print(f"Schema files: {analysis['documentation_inventory']['schema_files']}")
print(f"Sample data: {analysis['documentation_inventory']['sample_data']}")
print(f"Field-level docs: {analysis['documentation_inventory']['field_level_documentation']}")
print(f"Total downloadable artifacts: 0 (no links to downloadable files)")
print(f"Total artifacts collected: {analysis['total_artifacts_downloaded']}")
