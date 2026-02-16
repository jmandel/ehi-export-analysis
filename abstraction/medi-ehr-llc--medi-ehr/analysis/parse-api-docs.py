#!/usr/bin/env python3
"""Parse the Medi-EHR API documentation and compliance page to extract
all available export entity/field information for entity-inventory-full.json."""

import json
import re
from html.parser import HTMLParser

# Load the enrichment JSON (pre-parsed API docs)
with open("../downloads/enrichment/api-docs.json") as f:
    api_docs = json.load(f)

# Extract the C-CDA export endpoint details
ccda_endpoint = None
for ep in api_docs["endpoints"]:
    if ep["path"] == "/mediehrgetpatientdata.php":
        ccda_endpoint = ep
        break

# The 19 C-CDA sections are the only "entities" documented
ccda_sections = ccda_endpoint["responseSections"]

# Map API parameter names to section names
param_to_section = {}
for param in ccda_endpoint["parameters"]:
    if param["name"].startswith("PAT_"):
        # Find the matching section from responseSections
        param_to_section[param["name"]] = param["description"].split(" component")[0].split(" section")[0]
        # Clean up: extract the actual component name
        desc = param["description"]
        match = re.search(r"the (\w[\w\s]+?) (?:component|section) will be included", desc, re.IGNORECASE)
        if match:
            param_to_section[param["name"]] = match.group(1).strip()

# Build entity inventory
entities = []
for i, section in enumerate(ccda_sections):
    # Find matching parameter
    matching_param = None
    for param in ccda_endpoint["parameters"]:
        if param["name"].startswith("PAT_"):
            desc = param["description"]
            if section.lower().replace(" and ", " ").split()[0] in desc.lower():
                matching_param = param["name"]
                break

    entity = {
        "entity_name": section,
        "source": "C-CDA 2.1 API response section",
        "api_parameter": matching_param,
        "toggle_values": "S (show) / H (hide)",
        "fields": [],  # No field-level documentation exists
        "field_count": 0,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "category": "Clinical (C-CDA Section)",
        "notes": "No field-level documentation provided. Only section name is documented."
    }
    entities.append(entity)

# Also document the patient search endpoint's return fields (limited)
patient_search_fields = []
for param in api_docs["endpoints"][1]["parameters"]:  # mediehrgetpatient.php
    patient_search_fields.append({
        "name": param["name"],
        "type": param["type"],
        "required": param["required"],
        "description": param["description"],
        "direction": "input"
    })

patient_search_entity = {
    "entity_name": "Patient Search (API input parameters)",
    "source": "mediehrgetpatient.php endpoint",
    "api_parameter": None,
    "fields": patient_search_fields,
    "field_count": len(patient_search_fields),
    "fields_with_descriptions": sum(1 for f in patient_search_fields if f["description"]),
    "fields_with_types": sum(1 for f in patient_search_fields if f["type"]),
    "category": "Demographics (API Parameters)",
    "notes": "These are input parameters for patient lookup, not export fields. Included for completeness."
}

# Build the full inventory
inventory = {
    "product": "Medi-EHR",
    "version": "2.1",
    "extraction_source": "downloads/enrichment/api-docs.json + downloads/compliance-page.html",
    "extraction_date": "2026-02-16",
    "export_format": "C-CDA 2.1 XML (API); CSV and HTML mentioned but undocumented",
    "total_entities": len(entities) + 1,  # +1 for patient search
    "total_fields_documented": sum(e["field_count"] for e in entities) + patient_search_entity["field_count"],
    "data_dictionary_exists": False,
    "field_level_documentation": False,
    "notes": [
        "No data dictionary or field-level schema is provided.",
        "The only structured export documented is C-CDA 2.1 via a proprietary REST API.",
        "19 C-CDA sections can be toggled on/off but no field-level detail is given.",
        "CSV and HTML formats are mentioned on the compliance page but have zero documentation.",
        "The compliance page describes CSV and HTML generically (what the formats are), not what data they contain."
    ],
    "entities": entities + [patient_search_entity]
}

# Write outputs
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Summary
summary = {
    "total_entities": inventory["total_entities"],
    "ccda_sections": len(ccda_sections),
    "total_fields_documented": inventory["total_fields_documented"],
    "fields_in_ccda_sections": 0,
    "fields_in_api_params": patient_search_entity["field_count"],
    "data_dictionary_exists": False,
    "field_level_documentation": False,
    "export_formats_mentioned": ["C-CDA 2.1 XML", "CSV", "HTML"],
    "export_formats_documented": ["C-CDA 2.1 XML (section-level only)"],
    "categories": {
        "Clinical (C-CDA Section)": {
            "entity_count": len(entities),
            "field_count": 0,
            "note": "19 sections documented at section level only, no field detail"
        },
        "Demographics (API Parameters)": {
            "entity_count": 1,
            "field_count": patient_search_entity["field_count"],
            "note": "Patient search input parameters only"
        }
    },
    "ccda_section_list": ccda_sections,
    "api_endpoints": [
        {"path": ep["path"], "method": ep["method"], "summary": ep["summary"]}
        for ep in api_docs["endpoints"]
    ],
    "error_codes": api_docs["errorCodes"]
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Entities: {inventory['total_entities']}")
print(f"C-CDA sections: {len(ccda_sections)}")
print(f"Fields documented: {inventory['total_fields_documented']}")
print(f"Data dictionary exists: {inventory['data_dictionary_exists']}")
print(f"Sections: {', '.join(ccda_sections)}")
