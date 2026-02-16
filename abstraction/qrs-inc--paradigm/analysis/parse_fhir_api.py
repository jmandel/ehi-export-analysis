"""Parse PARADIGM FHIR API Documentation PDF to extract resource definitions and fields."""

import subprocess
import re
import json

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/PARADIGM_FHIR_API_Documentation.pdf", "-"],
    capture_output=True, text=True
)
text = result.stdout

# Split into resource sections
# Resources start on their own line as a single capitalized word
resource_names = [
    "Patient", "AllergyIntolerance", "CarePlan", "CareTeam", "Condition",
    "Device", "DiagnosticReport", "DocumentReference", "Goal", "Immunization",
    "MedicationRequest", "Observation", "Procedure", "Encounter", "Provenance"
]

# Additional supporting resources mentioned in scopes
supporting_resources = ["Medication", "Location", "Organization", "Practitioner", "PractitionerRole"]

resources = []

for i, name in enumerate(resource_names):
    # Find the section for this resource
    pattern = rf'^{name}\s*$'
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        continue
    
    start = match.start()
    
    # Find end (next resource or "Error" section)
    end = len(text)
    for next_name in resource_names:
        if next_name == name:
            continue
        next_match = re.search(rf'^{next_name}\s*$', text[start+len(name):], re.MULTILINE)
        if next_match:
            candidate = start + len(name) + next_match.start()
            if candidate < end and candidate > start:
                end = candidate
    
    # Also check for "Error and Exceptions"
    err_match = re.search(r'^Error and Exceptions', text[start:], re.MULTILINE)
    if err_match:
        candidate = start + err_match.start()
        if candidate < end:
            end = candidate
    
    section = text[start:end]
    
    # Parse response parameters table
    # Look for lines with Name/Type/Description pattern in the Response Parameters area
    resp_start = section.find("Response Parameters:")
    if resp_start == -1:
        resp_start = section.find("Response Parameters")
    
    fields = []
    if resp_start != -1:
        resp_section = section[resp_start:]
        # Parse table rows - they typically have Name, Type, Description columns
        # Look for lines that have at least two whitespace-separated columns
        lines = resp_section.split('\n')
        in_table = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("Name") and "Type" in stripped:
                in_table = True
                continue
            if in_table:
                # Stop at next section header or empty-ish content
                if stripped.startswith("Request:") or stripped.startswith("Error") or stripped.startswith("fhir_api_doc"):
                    break
                if re.match(r'^Page \d+', stripped):
                    continue
                if stripped.startswith("PARADIGM"):
                    continue
                    
                # Parse the field line - fields are separated by whitespace
                parts = re.split(r'\s{2,}', stripped)
                if len(parts) >= 2:
                    field = {
                        "name": parts[0].strip(),
                        "type": parts[1].strip() if len(parts) > 1 else "",
                        "description": parts[2].strip() if len(parts) > 2 else ""
                    }
                    if field["name"] and not field["name"].startswith("---"):
                        fields.append(field)
    
    # Extract search parameters
    search_params = []
    search_start = section.find("Request Parameters")
    if search_start != -1:
        search_section = section[search_start:]
        lines = search_section.split('\n')
        in_table = False
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("Name") and "Type" in stripped:
                in_table = True
                continue
            if in_table:
                if stripped.startswith("Response") or stripped.startswith("fhir_api_doc"):
                    break
                if re.match(r'^Page \d+', stripped):
                    continue
                if stripped.startswith("PARADIGM"):
                    continue
                parts = re.split(r'\s{2,}', stripped)
                if len(parts) >= 2:
                    param = {
                        "name": parts[0].strip(),
                        "type": parts[1].strip() if len(parts) > 1 else "",
                        "required": parts[2].strip() if len(parts) > 2 else "",
                        "description": parts[3].strip() if len(parts) > 3 else ""
                    }
                    if param["name"] and not param["name"].startswith("---"):
                        search_params.append(param)
    
    resources.append({
        "resource": name,
        "field_count": len(fields),
        "fields": fields,
        "search_parameter_count": len(search_params),
        "search_parameters": search_params
    })

# Build the full inventory
inventory = {
    "source": "PARADIGM_FHIR_API_Documentation.pdf",
    "format": "FHIR R4 (US Core)",
    "total_resources": len(resources),
    "total_fields": sum(r["field_count"] for r in resources),
    "resources": resources,
    "supporting_resources_in_scopes": supporting_resources,
    "notes": [
        "This is the (g)(10) FHIR API documentation, NOT the (b)(10) EHI export",
        "The EHI export uses C-CDA + supplemental JSON, documented separately",
        "No data dictionary provided for the EHI export content"
    ]
}

# Also parse the EHI export doc structure
ehi_doc = {
    "source": "PARADIGM_EHI_Export_Documentation.pdf",
    "total_pages": 6,
    "legal_boilerplate_pages": 4,
    "technical_pages": 2,
    "export_format": "ZIP containing C-CDA XML + supplemental JSON + attached files",
    "components": [
        {
            "name": "C-CDA XML",
            "description": "Standard C-CDA CCD document per patient, named by patient code (e.g., 10000.xml)",
            "documented_fields": 0,
            "has_data_dictionary": False
        },
        {
            "name": "Supplemental JSON",
            "description": "Additional information in JSON format, named by info type (e.g., 10000_invoice history.json)",
            "documented_fields": 0,
            "has_data_dictionary": False,
            "example_mentioned": "invoice history"
        },
        {
            "name": "Attached files",
            "description": "Files imported into the EHR in original format (PDF/PNG/etc), in _addt_files directory",
            "documented_fields": 0,
            "has_data_dictionary": False
        }
    ],
    "access_mechanism": {
        "ui": "EHR System Reports > Data Portability module, checkbox for 'include all EHI'",
        "api": "REST API at api.qrshs.com/v1/ for patient search and C-CDA retrieval (Basic auth)",
        "api_endpoints": [
            {
                "endpoint": "GET https://api.qrshs.com/v1/patient/search",
                "parameters": ["first_name", "mid_name", "last_name", "birthdate", "ssn"],
                "auth": "Basic"
            },
            {
                "endpoint": "GET https://api.qrshs.com/v1/patient/ccda",
                "parameters": ["patient", "date", "start_date", "end_date"],
                "auth": "Basic"
            }
        ]
    },
    "data_dictionary": None,
    "sample_data": None,
    "schema": None
}

# Combine into entity inventory
entity_inventory = []

# C-CDA component (the primary export)
entity_inventory.append({
    "entity": "C-CDA CCD Document",
    "source": "EHI Export (b)(10)",
    "category": "Clinical Summary",
    "fields": [],
    "field_count": 0,
    "description": "Standard C-CDA Continuity of Care Document containing clinical summary data. No product-specific field documentation provided.",
    "has_descriptions": False,
    "has_types": False
})

# Supplemental JSON
entity_inventory.append({
    "entity": "Supplemental JSON (invoice history)",
    "source": "EHI Export (b)(10)",
    "category": "Billing/Additional",
    "fields": [],
    "field_count": 0,
    "description": "JSON file with additional information such as invoice history. Only mentioned by example name; no schema or field documentation provided.",
    "has_descriptions": False,
    "has_types": False
})

# Attached files
entity_inventory.append({
    "entity": "Attached Files",
    "source": "EHI Export (b)(10)",
    "category": "Documents",
    "fields": [],
    "field_count": 0,
    "description": "Files imported into the EHR (PDF, PNG, etc.) included in original format. No documentation of file types or metadata.",
    "has_descriptions": False,
    "has_types": False
})

# FHIR API resources (for reference - these are (g)(10), not (b)(10))
for r in resources:
    entity_inventory.append({
        "entity": f"FHIR {r['resource']}",
        "source": "FHIR API (g)(10) - NOT EHI export",
        "category": "FHIR US Core",
        "fields": r["fields"],
        "field_count": r["field_count"],
        "description": f"US Core FHIR resource with {r['field_count']} documented response fields",
        "has_descriptions": True if any(f.get("description") for f in r["fields"]) else False,
        "has_types": True if any(f.get("type") for f in r["fields"]) else False
    })

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump({
        "product": "PARADIGM®",
        "vendor": "QRS, Inc.",
        "ehi_export_documentation": ehi_doc,
        "fhir_api_documentation": inventory,
        "entities": entity_inventory,
        "summary": {
            "ehi_export_entities": 3,
            "ehi_export_documented_fields": 0,
            "fhir_api_resources": len(resources),
            "fhir_api_total_fields": sum(r["field_count"] for r in resources),
            "total_entities": len(entity_inventory),
            "has_data_dictionary": False,
            "has_sample_data": False,
            "has_schema": False
        }
    }, f, indent=2)

# Summary
summary = {
    "product": "PARADIGM®",
    "vendor": "QRS, Inc.",
    "ehi_export": {
        "format": "ZIP (C-CDA XML + JSON + attached files)",
        "entities_mentioned": 3,
        "documented_fields": 0,
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "key_finding": "No data dictionary, no schema, no sample data. Only a brief description of the export structure (2 technical pages out of 6)."
    },
    "fhir_api_for_reference": {
        "resources": [r["resource"] for r in resources],
        "resource_count": len(resources),
        "total_response_fields": sum(r["field_count"] for r in resources),
        "note": "This is the (g)(10) FHIR API, separate from the (b)(10) EHI export"
    },
    "field_counts_by_resource": {r["resource"]: r["field_count"] for r in resources}
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"EHI Export: {summary['ehi_export']['format']}")
print(f"  Entities mentioned: {summary['ehi_export']['entities_mentioned']}")
print(f"  Documented fields: {summary['ehi_export']['documented_fields']}")
print(f"  Data dictionary: {summary['ehi_export']['has_data_dictionary']}")
print(f"\nFHIR API (g)(10) for reference:")
print(f"  Resources: {summary['fhir_api_for_reference']['resource_count']}")
print(f"  Total response fields: {summary['fhir_api_for_reference']['total_response_fields']}")
print(f"\nPer-resource field counts:")
for r, c in summary['field_counts_by_resource'].items():
    print(f"  {r}: {c} fields")
