"""
Build full-entity-inventory.json for PARADIGM EHI Export.

Since PARADIGM provides no native data dictionary, we document:
1. The EHI export components described in the EHI Export Documentation PDF
2. The FHIR API resources (which represent the C-CDA content available)
3. The undocumented JSON supplement ("invoice history")
"""

import json

# Load parsed FHIR resources
with open('/home/jmandel/hobby/ehi-export-analysis/abstraction/qrs-inc--paradigm/analysis/fhir_resources.json', 'r') as f:
    fhir_data = json.load(f)

inventory = {
    "vendor": "QRS, Inc.",
    "product": "PARADIGM®",
    "version": "22",
    "analysis_date": "2026-02-16",
    "source_artifacts": [
        {
            "file": "PARADIGM_EHI_Export_Documentation.pdf",
            "pages": 6,
            "technical_pages": 2,
            "boilerplate_pages": 4,
            "description": "Core (b)(10) EHI export documentation. Version 1.0, dated 2023-09-26."
        },
        {
            "file": "PARADIGM_FHIR_API_Documentation.pdf",
            "pages": 27,
            "technical_pages": 23,
            "boilerplate_pages": 4,
            "description": "(g)(10) FHIR R4 API documentation. Dated 2023-01-09."
        },
        {
            "file": "PARADIGM_Patient_API_Documentation.pdf",
            "pages": 6,
            "technical_pages": 2,
            "boilerplate_pages": 4,
            "description": "Patient search/C-CDA retrieval API. Dated 2022-12-15."
        },
        {
            "file": "qrshs-info-main-page.html",
            "description": "Disclosures page listing all PDF documents."
        }
    ],
    "export_description": {
        "mechanism": "EHR System Reports module, 'FHIR Data Portability' feature",
        "ehi_checkbox": "include all Electronic Healthcare Information (EHI) for each patient in the set",
        "output_format": "ZIP archive containing C-CDA XML + JSON supplements + imported files",
        "api_endpoints": [
            {
                "method": "GET",
                "url": "https://api.qrshs.com/v1/patient/search",
                "auth": "Basic",
                "purpose": "Patient lookup by name/DOB/SSN",
                "request_params": [
                    {"name": "first_name", "type": "string", "required": "conditional"},
                    {"name": "mid_name", "type": "string", "required": "conditional"},
                    {"name": "last_name", "type": "string", "required": "conditional"},
                    {"name": "birthdate", "type": "date", "required": "conditional"},
                    {"name": "ssn", "type": "string", "required": "conditional"}
                ],
                "response_params": [
                    {"name": "patient", "type": "string", "example": "10006-111-20180823"}
                ]
            },
            {
                "method": "GET",
                "url": "https://api.qrshs.com/v1/patient/ccda",
                "auth": "Basic",
                "purpose": "Retrieve C-CDA CCD document for a patient",
                "request_params": [
                    {"name": "patient", "type": "string", "required": "required"},
                    {"name": "date", "type": "date", "required": "optional"},
                    {"name": "start_date", "type": "date", "required": "optional"},
                    {"name": "end_date", "type": "date", "required": "optional"}
                ],
                "response": "C-CDA XML document (or JSON error)"
            }
        ],
        "export_components": [
            {
                "component": "C-CDA XML",
                "naming_pattern": "{patient_code}.xml",
                "example": "10000.xml",
                "documented": True,
                "documentation_quality": "minimal - no field-level documentation of C-CDA contents"
            },
            {
                "component": "Supplemental JSON",
                "naming_pattern": "{patient_code}_{info_type}.json",
                "example": "10000_invoice history.json",
                "documented": False,
                "documentation_quality": "none - format completely undocumented; only filename example given"
            },
            {
                "component": "Attached files",
                "naming_pattern": "{patient_code}_addt_files/",
                "example": "10000_addt_files/",
                "documented": True,
                "documentation_quality": "minimal - described as files imported into EHR in original format (PDF/PNG/etc)"
            }
        ]
    },
    "data_dictionary_exists": False,
    "sample_data_provided": False,
    "schema_provided": False,
    "fhir_api_resources": fhir_data["resources"],
    "fhir_api_summary": {
        "total_resources": fhir_data["total_resources"],
        "total_response_parameters": fhir_data["total_response_parameters"],
        "note": "These are (g)(10) FHIR API resources, not the (b)(10) EHI export. However, the C-CDA in the EHI export likely maps to the same clinical domains."
    },
    "documented_entities": [
        {
            "entity": "C-CDA Document",
            "category": "Clinical",
            "fields": "N/A - standard C-CDA sections",
            "fields_with_descriptions": "N/A",
            "documentation_source": "PARADIGM_EHI_Export_Documentation.pdf",
            "notes": "Standard C-CDA CCD document. No vendor-specific documentation of which sections are included or how they're populated."
        },
        {
            "entity": "Invoice History JSON",
            "category": "Billing",
            "fields": "unknown",
            "fields_with_descriptions": 0,
            "documentation_source": "PARADIGM_EHI_Export_Documentation.pdf",
            "notes": "Mentioned only by example filename ('10000_invoice history.json'). No schema, no field definitions, no sample structure provided."
        },
        {
            "entity": "Attached Files",
            "category": "Documents",
            "fields": "N/A - raw files",
            "fields_with_descriptions": "N/A",
            "documentation_source": "PARADIGM_EHI_Export_Documentation.pdf",
            "notes": "Files previously imported into EHR in original format (PDF, PNG, etc). No metadata schema documented."
        }
    ],
    "total_documented_entities": 3,
    "total_documented_fields": 0,
    "fields_with_descriptions": 0,
    "documentation_completeness": {
        "data_dictionary": False,
        "field_names": False,
        "field_types": False,
        "field_descriptions": False,
        "value_sets": False,
        "relationships": False,
        "sample_data": False,
        "machine_readable_schema": False
    }
}

output_path = '/home/jmandel/hobby/ehi-export-analysis/abstraction/qrs-inc--paradigm/analysis/full-entity-inventory.json'
with open(output_path, 'w') as f:
    json.dump(inventory, f, indent=2)

print(f"Inventory saved to {output_path}")
print(f"Documented entities: {inventory['total_documented_entities']}")
print(f"Documented fields: {inventory['total_documented_fields']}")
print(f"FHIR API resources: {inventory['fhir_api_summary']['total_resources']}")
print(f"FHIR response parameters: {inventory['fhir_api_summary']['total_response_parameters']}")
print(f"Data dictionary exists: {inventory['data_dictionary_exists']}")
print(f"Sample data: {inventory['sample_data_provided']}")
print(f"Schema: {inventory['schema_provided']}")
