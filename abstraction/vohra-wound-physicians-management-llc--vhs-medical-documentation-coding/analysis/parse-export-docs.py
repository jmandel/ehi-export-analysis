#!/usr/bin/env python3
"""Parse the Vohra EHI export documentation HTML and extract structured info."""

import json
from html.parser import HTMLParser

# Read the HTML source
with open("../downloads/CompleteExport.html", "r") as f:
    html_content = f.read()

# Manual extraction since the page is simple static HTML with no data dictionary.
# The entire documentation consists of:
# 1. Export location (server + directory)
# 2. Two file types (PDF encounter notes, XML C-CDA)
# 3. Single-patient export procedure (8 steps)

export_doc = {
    "source_file": "downloads/CompleteExport.html",
    "source_url": "https://facilityportal.vohrawoundteam.com/CompleteExport.html",
    "page_title": "Export data format and location",
    "export_location": {
        "server": "IIS-PROD-02",
        "directory": "C:\\inetpub\\webapp\\ExportedPatientData"
    },
    "export_formats": [
        {
            "extension": "PDF",
            "description": "Encounter notes",
            "filename_template": "PATIENT_IDENTIFIER.pdf",
            "example_filename": "GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG.pdf",
            "identifier_scope": "patient",
            "notes": "One PDF per patient containing encounter notes. Not computable data."
        },
        {
            "extension": "XML",
            "description": "Data conforms to the CCDA standard",
            "filename_template": "ENCOUNTER_IDENTIFIER.xml",
            "example_filename": "HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH.xml",
            "identifier_scope": "encounter",
            "notes": "One XML file per encounter. C-CDA standard. No template OID or document type specified."
        }
    ],
    "export_procedure": {
        "type": "single_patient",
        "steps": [
            "Navigate to the administrative portal (https://med.vohrawoundteam.com/LogIn.aspx)",
            "Authenticate as a user who has been granted permissions to export",
            "Select the menu for Advanced / Data Portability",
            "Set 'Export Option' to Patient",
            "Enter the patient's First Name, Last Name and Date of Birth",
            "Press 'Export Patients' button",
            "You will see 'Successfully exported 1 patient records'",
            "Login to the server and retrieve files from C:\\inetpub\\webapp\\ExportedPatientData"
        ],
        "admin_portal_url": "https://med.vohrawoundteam.com/LogIn.aspx",
        "admin_portal_status": "NXDOMAIN - subdomain no longer exists"
    },
    "data_dictionary": None,
    "schema_files": None,
    "sample_data": None,
    "field_level_documentation": None,
    "ccda_template_specification": None,
    "bulk_export_procedure": None,
    "outbound_links": [
        {
            "url": "https://med.vohrawoundteam.com/LogIn.aspx",
            "text": "administrative portal",
            "status": "dead (NXDOMAIN)"
        }
    ],
    "assessment": {
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "has_field_definitions": False,
        "has_value_sets": False,
        "has_relationships": False,
        "total_entities_documented": 0,
        "total_fields_documented": 0,
        "documentation_completeness": "minimal - file-type level only, no content detail"
    }
}

# Write output
with open("export-documentation-parsed.json", "w") as f:
    json.dump(export_doc, f, indent=2)

print("Parsed export documentation:")
print(f"  Export formats: {len(export_doc['export_formats'])}")
print(f"  Data dictionary: {export_doc['assessment']['has_data_dictionary']}")
print(f"  Schema: {export_doc['assessment']['has_schema']}")
print(f"  Sample data: {export_doc['assessment']['has_sample_data']}")
print(f"  Field definitions: {export_doc['assessment']['has_field_definitions']}")
print(f"  Entities documented: {export_doc['assessment']['total_entities_documented']}")
print(f"  Fields documented: {export_doc['assessment']['total_fields_documented']}")
