"""Build a full inventory of what's known about the EHI export content.

Since AWARDS provides no data dictionary, this inventory captures:
1. ExportBuilder modules mentioned in documentation
2. Sub-export modules explicitly listed
3. HMIS CSV files from the HMIS Data Export
4. FHIR resources from the (g)(10) API (NOT the (b)(10) export, but for comparison)
"""
import json

inventory = {
    "product": "AWARDS 3.0",
    "vendor": "Foothold Technology, Inc.",
    "export_mechanism": "ExportBuilder (ad-hoc, user-configured data export tool)",
    "data_dictionary_available": False,
    "sample_data_available": False,
    "schema_available": False,
    
    "exportbuilder_modules_confirmed": [
        {
            "name": "Demographics ExportBuilder",
            "evidence": "Explicitly used as example throughout ExportBuilders article",
            "supports_sub_exports": True,
            "sub_export_sources": [
                "Hospital > Episodes",
                "Medical > Allergies",
                "Medical > Medications",
                "Employment > Jobs > Job Placements",
                "Employment > Jobs > Job Interviews"
            ],
            "fields_documented": False,
            "field_count": None
        },
        {
            "name": "HMIS History ExportBuilder",
            "evidence": "Mentioned as exception to 2-year date range limit",
            "supports_sub_exports": False,
            "fields_documented": False,
            "field_count": None
        },
        {
            "name": "HMIS ExportBuilder",
            "evidence": "Mentioned in article text referencing HMIS or Demographics ExportBuilders",
            "supports_sub_exports": False,
            "fields_documented": False,
            "field_count": None
        },
        {
            "name": "Progress Notes ExportBuilder",
            "evidence": "Mentioned in FormBuilder integration context",
            "supports_sub_exports": False,
            "fields_documented": False,
            "field_count": None
        }
    ],
    
    "exportbuilder_modules_implied": [
        {
            "name": "Hospital Episodes ExportBuilder",
            "evidence": "Listed as sub-export source, implying its own ExportBuilder exists",
            "fields_documented": False
        },
        {
            "name": "Medical Allergies ExportBuilder",
            "evidence": "Listed as sub-export source",
            "fields_documented": False
        },
        {
            "name": "Medical Medications ExportBuilder",
            "evidence": "Listed as sub-export source",
            "fields_documented": False
        },
        {
            "name": "Employment Job Placements ExportBuilder",
            "evidence": "Listed as sub-export source",
            "fields_documented": False
        },
        {
            "name": "Employment Job Interviews ExportBuilder",
            "evidence": "Listed as sub-export source",
            "fields_documented": False
        },
        {
            "name": "Intake/Admission ExportBuilder",
            "evidence": "Mentioned in permissions context: 'you will not have access to Intake reports if you do not have access to the Intake/Admission module'",
            "fields_documented": False
        }
    ],
    
    "hmis_data_export": {
        "description": "Separate HMIS-specific CSV export feature (not ExportBuilder)",
        "format": "Zipped CSV files per HUD HMIS CSV specification",
        "export_types": ["Full", "HIC", "RHY", "Full+"],
        "csv_files_in_full_export": [
            "Client.csv",
            "Enrollment.csv",
            "EnrollmentCoC.csv",
            "Export.csv",
            "Event.csv",
            "Services.csv",
            "Assessment.csv",
            "AssessmentQuestions.csv",
            "AssessmentResults.csv",
            "Project.csv",
            "ProgramCoC.csv",
            "Inventory.csv",
            "Site.csv",
            "User.csv"
        ],
        "full_plus_additions": [
            "FB_[unique number]_[FormBuilder name].csv (custom form data)",
            "ServicesOther.csv (service contact details)"
        ],
        "services_other_fields": [
            "Date of Contact",
            "Service Type",
            "Unit",
            "Cost",
            "End Date",
            "Service Details (up to 50 chars)",
            "Funding Sources"
        ],
        "services_other_excluded": [
            "Time",
            "Duration",
            "Location",
            "Primary Problem Area",
            "Attached progress notes"
        ],
        "standard_reference": "HUD HMIS CSV specification at hudhdx.info/VendorResources.aspx"
    },
    
    "fhir_api_resources_g10": {
        "description": "FHIR R4 API for (g)(10) compliance - NOT the (b)(10) EHI export",
        "standard": "US Core STU 6.1.0, USCDI v3",
        "resources": [
            "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
            "Coverage", "Device", "DiagnosticReport", "DocumentReference",
            "Encounter", "Goal", "Immunization", "Location",
            "Medication", "MedicationDispense", "MedicationRequest",
            "Observation", "Organization", "Patient", "Practitioner",
            "Procedure", "Provenance", "RelatedPerson", "ServiceRequest",
            "Specimen"
        ],
        "resource_count": 24,  # excluding CapabilityStatement
        "supports_bulk_data": True,
        "bulk_data_standard": "Bulk Data Access (Flat FHIR) STU 1"
    },
    
    "documentation_gaps": [
        "No data dictionary listing available fields in any ExportBuilder",
        "No sample export files provided",
        "No schema or format specification for export files",
        "ReportBuilder documentation (which lists available fields) is behind login wall (HTTP 403)",
        "No guidance on which ExportBuilders to use for complete EHI export",
        "No documentation of how many ExportBuilder modules exist",
        "Total number of exportable fields is unknown",
        "No relationship/foreign key documentation",
        "No value set documentation",
        "Billing, treatment plans, vitals, lab results, immunizations not mentioned in ExportBuilder docs"
    ]
}

with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary stats
print("=== Full Entity Inventory Summary ===")
print(f"Confirmed ExportBuilder modules: {len(inventory['exportbuilder_modules_confirmed'])}")
print(f"Implied ExportBuilder modules: {len(inventory['exportbuilder_modules_implied'])}")
print(f"Total ExportBuilder modules known: {len(inventory['exportbuilder_modules_confirmed']) + len(inventory['exportbuilder_modules_implied'])}")
print(f"Fields documented in any module: 0")
print(f"HMIS CSV files in Full export: {len(inventory['hmis_data_export']['csv_files_in_full_export'])}")
print(f"FHIR (g)(10) resources: {inventory['fhir_api_resources_g10']['resource_count']}")
print(f"Documentation gaps: {len(inventory['documentation_gaps'])}")
print(f"Data dictionary available: {inventory['data_dictionary_available']}")
print(f"Sample data available: {inventory['sample_data_available']}")
