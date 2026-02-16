#!/usr/bin/env python3
"""
Parse all HTML artifacts from the CHN Tech Solutions EHI export documentation.
Extracts:
- CCD sections documented on the FHIR API page
- REST API scopes (FHIR and OpenEMR native)
- FHIR resources supported
- Export mechanism details
Outputs entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.text.append(t)

def extract_text(filepath):
    with open(filepath) as f:
        p = TextExtractor()
        p.feed(f.read())
    return p.text

# Parse the FHIR API page for CCD sections
fhir_text = extract_text(DOWNLOADS / "fhir-api-page.html")

# CCD sections - date filterable
date_filterable_sections = [
    "History of Procedures",
    "Relevant DX Tests / LAB Data",
    "Functional Status",
    "Progress Notes",
    "Procedure Notes",
    "Laboratory Report Narrative",
    "Encounters",
    "Assessments",
    "Treatment Plan",
    "Goals",
    "Health Concerns",
    "Document Reason for Referral",
    "Mental Status",
]

# CCD sections - full record
full_record_sections = [
    "Demographics",
    "Allergies, Adverse Reactions, Alerts",
    "History of Medication Use",
    "Problem List",
    "Immunizations",
    "Social History",
    "Medical Equipment",
    "Vital Signs",
]

# Parse REST API page for scopes
rest_text = extract_text(DOWNLOADS / "rest-api-page.html")

# Extract FHIR scopes
fhir_patient_scopes = []
fhir_system_scopes = []
fhir_user_scopes = []
oemr_user_scopes = []
portal_patient_scopes = []

scope_section = None
for line in rest_text:
    line = line.strip()
    if line == "api:fhir (fhir which are the /fhir/ endpoints)":
        scope_section = "fhir"
        continue
    elif line == "api:oemr (user api which are the /api/ endpoints)":
        scope_section = "oemr"
        continue
    elif line == "api:port (patient api which are the /portal/ endpoints) (EXPERIMENTAL)":
        scope_section = "port"
        continue
    elif line.startswith("Registration"):
        scope_section = None
        continue

    if scope_section == "fhir":
        if line.startswith("patient/"):
            fhir_patient_scopes.append(line)
        elif line.startswith("system/"):
            fhir_system_scopes.append(line)
        elif line.startswith("user/"):
            fhir_user_scopes.append(line)
    elif scope_section == "oemr":
        if line.startswith("user/"):
            oemr_user_scopes.append(line)
    elif scope_section == "port":
        if line.startswith("patient/"):
            portal_patient_scopes.append(line)

# Extract unique FHIR resource types from scopes
fhir_resources = set()
for scope in fhir_patient_scopes + fhir_system_scopes + fhir_user_scopes:
    parts = scope.split("/")
    if len(parts) == 2:
        resource = parts[1].split(".")[0]
        if resource != "*" and not resource.startswith("$"):
            fhir_resources.add(resource)

# Extract OpenEMR native data types from scopes
oemr_data_types = set()
for scope in oemr_user_scopes:
    parts = scope.split("/")
    if len(parts) == 2:
        dtype = parts[1].split(".")[0]
        oemr_data_types.add(dtype)

# Build entity inventory
entities = []

# CCD sections as entities
for section in date_filterable_sections:
    entities.append({
        "entity_name": f"CCD Section: {section}",
        "category": "C-CDA CCD Export (Date-Filterable)",
        "source": "fhir-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"CCD section '{section}' - contents filtered by encounter date range when start/end dates specified in $docref operation",
        "notes": "No field-level documentation provided; relies on C-CDA R2.1 standard templates"
    })

for section in full_record_sections:
    entities.append({
        "entity_name": f"CCD Section: {section}",
        "category": "C-CDA CCD Export (Full Record)",
        "source": "fhir-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"CCD section '{section}' - always includes complete patient history regardless of date filters",
        "notes": "No field-level documentation provided; relies on C-CDA R2.1 standard templates"
    })

# FHIR resources as entities
for resource in sorted(fhir_resources):
    entities.append({
        "entity_name": f"FHIR Resource: {resource}",
        "category": "FHIR API Resources",
        "source": "rest-api-page.html / fhir-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"FHIR R4 {resource} resource accessible via FHIR API (US Core 3.1 conformant)",
        "notes": "No vendor-specific field documentation; standard US Core profiles"
    })

# OpenEMR native API data types as entities
for dtype in sorted(oemr_data_types):
    entities.append({
        "entity_name": f"OpenEMR API: {dtype}",
        "category": "OpenEMR Native REST API",
        "source": "rest-api-page.html",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "description": f"OpenEMR native REST API endpoint for '{dtype}' data",
        "notes": "Available via REST API but NOT part of the documented (b)(10) EHI export"
    })

# Build full inventory
inventory = {
    "product": "Integrated Care EHR",
    "vendor": "CHN Tech Solutions LLC",
    "export_format": "C-CDA CCD (XML) via FHIR $docref operation",
    "data_dictionary_available": False,
    "entities": entities,
    "total_entities": len(entities),
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "ccd_sections": {
        "date_filterable": date_filterable_sections,
        "full_record": full_record_sections,
        "total_sections": len(date_filterable_sections) + len(full_record_sections)
    },
    "fhir_resources": sorted(fhir_resources),
    "fhir_resource_count": len(fhir_resources),
    "oemr_data_types": sorted(oemr_data_types),
    "oemr_data_type_count": len(oemr_data_types),
    "scopes": {
        "fhir_patient": fhir_patient_scopes,
        "fhir_system": fhir_system_scopes,
        "fhir_user": fhir_user_scopes,
        "oemr_user": oemr_user_scopes,
        "portal_patient": portal_patient_scopes,
        "total_fhir_patient": len(fhir_patient_scopes),
        "total_fhir_system": len(fhir_system_scopes),
        "total_fhir_user": len(fhir_user_scopes),
        "total_oemr_user": len(oemr_user_scopes),
        "total_portal_patient": len(portal_patient_scopes),
    }
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Build summary
summary = {
    "product": "Integrated Care EHR",
    "vendor": "CHN Tech Solutions LLC",
    "export_mechanism": "C-CDA CCD via FHIR $docref operation",
    "data_dictionary": "None - no field-level documentation provided",
    "total_ccd_sections": inventory["ccd_sections"]["total_sections"],
    "ccd_date_filterable_sections": len(date_filterable_sections),
    "ccd_full_record_sections": len(full_record_sections),
    "fhir_resource_types": inventory["fhir_resource_count"],
    "oemr_native_data_types": inventory["oemr_data_type_count"],
    "category_breakdown": {},
    "key_findings": [
        "No data dictionary exists - zero field-level documentation",
        "EHI export is a standard C-CDA CCD document (21 sections)",
        "Export is generated via FHIR $docref - same as (g)(10) clinical exchange",
        "OpenEMR REST API exposes additional data types (dental, insurance, SOAP notes, surgeries) not in CCD export",
        "No sample data or machine-readable schemas provided",
        "Two hosted PDFs are standard HL7 C-CDA IG documents, not vendor-specific"
    ]
}

# Category breakdown
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"entity_count": 0, "total_fields": 0}
    categories[cat]["entity_count"] += 1
    categories[cat]["total_fields"] += e["field_count"]
summary["category_breakdown"] = categories

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== Entity Inventory Summary ===")
print(f"Total CCD sections: {inventory['ccd_sections']['total_sections']}")
print(f"  Date-filterable: {len(date_filterable_sections)}")
print(f"  Full record: {len(full_record_sections)}")
print(f"\nFHIR Resources accessible: {inventory['fhir_resource_count']}")
print(f"  Resources: {', '.join(sorted(fhir_resources))}")
print(f"\nOpenEMR native data types: {inventory['oemr_data_type_count']}")
print(f"  Types: {', '.join(sorted(oemr_data_types))}")
print(f"\nScope counts:")
print(f"  FHIR patient scopes: {len(fhir_patient_scopes)}")
print(f"  FHIR system scopes: {len(fhir_system_scopes)}")
print(f"  FHIR user scopes: {len(fhir_user_scopes)}")
print(f"  OpenEMR user scopes: {len(oemr_user_scopes)}")
print(f"  Portal patient scopes: {len(portal_patient_scopes)}")
print(f"\nData dictionary: NONE")
print(f"Sample data: NONE")
print(f"Field-level documentation: NONE")
print(f"\nFiles written: entity-inventory-full.json, entity-inventory-summary.json")
