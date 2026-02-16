#!/usr/bin/env python3
"""
Parse all EHI export artifacts for ezCaretech BESTCare and produce:
1. full-entity-inventory.json - complete machine-readable extraction
2. artifact-summary.json - summary statistics
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent.parent.parent / "results" / "ezcaretech-co-ltd--bestcare" / "downloads"
OUTPUT = Path(__file__).parent


# --- Parse FHIR CapabilityStatement ---
def parse_capability_statement():
    with open(DOWNLOADS / "fhir-capability-statement.json") as f:
        cs = json.load(f)

    resources = cs.get("rest", [{}])[0].get("resource", [])
    result = []
    for r in resources:
        interactions = [i["code"] for i in r.get("interaction", [])]
        search_params = [
            {"name": sp["name"], "type": sp.get("type", ""), "definition": sp.get("definition", "")}
            for sp in r.get("searchParam", [])
        ]
        profiles = [r.get("profile", "")] + r.get("supportedProfile", [])
        result.append({
            "resource_type": r["type"],
            "interactions": interactions,
            "search_params": search_params,
            "profiles": [p for p in profiles if p],
            "search_param_count": len(search_params),
        })
    return {
        "name": cs.get("name"),
        "fhir_version": cs.get("fhirVersion"),
        "status": cs.get("status"),
        "date": cs.get("date"),
        "resource_count": len(result),
        "resources": result,
    }


# --- Parse Single Patient API HTML for field-level detail ---
class SinglePatientAPIParser(HTMLParser):
    """Extract US Core profile details from single-patient-api.html"""
    def __init__(self):
        super().__init__()
        self.in_content = False
        self.text_parts = []
        self.skip_tags = {"script", "style"}
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth == 0:
            stripped = data.strip()
            if stripped:
                self.text_parts.append(stripped)


def parse_single_patient_api():
    with open(DOWNLOADS / "single-patient-api.html") as f:
        html = f.read()

    parser = SinglePatientAPIParser()
    parser.feed(html)
    full_text = "\n".join(parser.text_parts)

    # Extract profile sections with their must-have and must-support fields
    profiles = []

    # Pattern: "X. US Core <Name> Profile" followed by must-have and must-support sections
    profile_pattern = r'\d+\.\s+US Core ([\w\s]+?) Profile'
    profile_matches = list(re.finditer(profile_pattern, full_text))

    for i, match in enumerate(profile_matches):
        name = match.group(1).strip()
        start = match.end()
        end = profile_matches[i + 1].start() if i + 1 < len(profile_matches) else len(full_text)
        section = full_text[start:end]

        # Extract must-have fields
        must_have = []
        mh_match = re.search(r'must have:(.*?)(?:must support:|API:)', section, re.DOTALL)
        if mh_match:
            fields = re.findall(r'[\w.]+(?:\.\w+)+', mh_match.group(1))
            must_have = list(dict.fromkeys(fields))

        # Extract must-support fields
        must_support = []
        ms_match = re.search(r'must support:(.*?)(?:API:|$)', section, re.DOTALL)
        if ms_match:
            fields = re.findall(r'[\w.]+(?:\.\w+)+', ms_match.group(1))
            must_support = list(dict.fromkeys(fields))

        # Extract response fields from search/read sections
        response_fields = []
        rf_matches = re.findall(r'Response Fields\n(.*?)(?=\d+\.\d+\.\d+|\d+\.\s+US Core|\Z)', section, re.DOTALL)
        for rf in rf_matches:
            field_names = re.findall(r'^(\w[\w.]*)', rf, re.MULTILINE)
            for fn in field_names:
                if fn not in response_fields and not fn.startswith(('Table', 'Parameter', 'Type', 'Optional', 'Description', 'Request', 'Response', 'GET', 'HTTP')):
                    response_fields.append(fn)

        profiles.append({
            "profile_name": f"US Core {name} Profile",
            "must_have_fields": must_have,
            "must_support_fields": must_support,
            "must_have_count": len(must_have),
            "must_support_count": len(must_support),
            "total_documented_fields": len(set(must_have + must_support)),
            "response_fields": response_fields,
        })

    return profiles


# --- Parse Multi Patient API HTML ---
def parse_multi_patient_api():
    with open(DOWNLOADS / "multi-patient-api.html") as f:
        html = f.read()

    parser = SinglePatientAPIParser()
    parser.feed(html)
    full_text = "\n".join(parser.text_parts)

    # Extract export endpoints
    endpoints = []
    for ep in ["All Patients", "Group of Patients", "System Level Export"]:
        if ep in full_text:
            endpoints.append(ep)

    # Extract supported parameters
    params = re.findall(r'_\w+', full_text)
    unique_params = list(dict.fromkeys(params))

    return {
        "endpoints": endpoints,
        "parameters": unique_params[:10],  # first 10 unique params
        "output_format": "NDJSON (application/fhir+ndjson)",
    }


# --- Parse EHI Export PDF content ---
def parse_ehi_pdf():
    """Analyze the (b)(10) PDF content."""
    return {
        "source": "b.10_EHI_Export.pdf",
        "pages": 1,
        "created": "2023-09-30",
        "author": "Eunsol Lee",
        "sections": [
            {
                "title": "I. Electronic Health Information Export",
                "subsections": [
                    "1. Single Patient Export",
                    "2. Multi-Patient Export",
                    "3. File Formats (CSV, Oracle DMP)",
                ],
            },
            {
                "title": "II. API documentation",
                "link": "https://portal.ezcaretech.com:30112/baseUrls",
            },
        ],
        "export_formats": ["CSV", "Oracle DMP"],
        "data_dictionary_present": False,
        "schema_present": False,
        "sample_data_present": False,
        "field_definitions": 0,
        "table_definitions": 0,
        "word_count_approx": 150,
    }


# --- Build full entity inventory ---
def build_full_inventory():
    cs = parse_capability_statement()
    profiles = parse_single_patient_api()
    multi_api = parse_multi_patient_api()
    pdf_info = parse_ehi_pdf()

    # Build entity inventory from FHIR profiles
    entities = []
    for res in cs["resources"]:
        # Find matching profile detail
        profile_detail = None
        for p in profiles:
            if res["resource_type"] in p["profile_name"]:
                profile_detail = p
                break

        fields = []
        if profile_detail:
            for f in profile_detail["must_have_fields"]:
                fields.append({
                    "name": f,
                    "requirement": "must-have",
                    "type": None,
                    "description": None,
                })
            for f in profile_detail["must_support_fields"]:
                if f not in [x["name"] for x in fields]:
                    fields.append({
                        "name": f,
                        "requirement": "must-support",
                        "type": None,
                        "description": None,
                    })

        entities.append({
            "entity_name": res["resource_type"],
            "source": "FHIR CapabilityStatement + Single Patient API",
            "category": categorize_resource(res["resource_type"]),
            "interactions": res["interactions"],
            "search_params": res["search_params"],
            "field_count": len(fields) if fields else res["search_param_count"],
            "fields": fields,
            "profiles": res["profiles"],
        })

    inventory = {
        "export_type": "FHIR R4 US Core (API-based) + CSV/Oracle DMP (undocumented)",
        "fhir_api": {
            "server_name": cs["name"],
            "fhir_version": cs["fhir_version"],
            "date": cs["date"],
            "resource_type_count": cs["resource_count"],
            "entities": entities,
        },
        "native_export": {
            "formats": ["CSV", "Oracle DMP"],
            "documentation": "Single-page PDF with no data dictionary, no schema, no field definitions",
            "tables_documented": 0,
            "fields_documented": 0,
            "entities": [],  # No documented entities for native export
        },
        "pdf_analysis": pdf_info,
        "summary": {
            "total_fhir_resources": cs["resource_count"],
            "total_fhir_profiles_documented": len(profiles),
            "total_native_tables_documented": 0,
            "total_native_fields_documented": 0,
            "has_data_dictionary": False,
            "has_sample_data": False,
            "has_schema": True,  # FHIR CapabilityStatement counts
        },
    }

    return inventory


def categorize_resource(resource_type):
    categories = {
        "Patient": "Demographics",
        "AllergyIntolerance": "Clinical",
        "Condition": "Clinical",
        "Procedure": "Clinical",
        "Encounter": "Clinical",
        "CarePlan": "Clinical",
        "CareTeam": "Clinical",
        "Goal": "Clinical",
        "DiagnosticReport": "Diagnostics",
        "Observation": "Diagnostics",
        "Immunization": "Clinical",
        "MedicationRequest": "Medications",
        "Medication": "Medications",
        "Device": "Clinical",
        "DocumentReference": "Documents",
        "Provenance": "Administrative",
        "Location": "Administrative",
        "Organization": "Administrative",
        "Practitioner": "Administrative",
        "PractitionerRole": "Administrative",
        "Binary": "Infrastructure",
        "CodeSystem": "Infrastructure",
        "ValueSet": "Infrastructure",
        "OperationDefinition": "Infrastructure",
        "Endpoint": "Infrastructure",
        "Group": "Infrastructure",
    }
    return categories.get(resource_type, "Other")


if __name__ == "__main__":
    inventory = build_full_inventory()

    with open(OUTPUT / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote full-entity-inventory.json")

    # Summary statistics
    fhir = inventory["fhir_api"]
    clinical_resources = [e for e in fhir["entities"] if e["category"] in ("Clinical", "Diagnostics", "Medications", "Demographics", "Documents")]
    infra_resources = [e for e in fhir["entities"] if e["category"] in ("Infrastructure", "Administrative")]

    summary = {
        "fhir_api": {
            "total_resource_types": fhir["resource_type_count"],
            "clinical_resource_types": len(clinical_resources),
            "administrative_resource_types": len(infra_resources),
            "profiles_documented": inventory["summary"]["total_fhir_profiles_documented"],
        },
        "native_export": {
            "formats": ["CSV", "Oracle DMP"],
            "tables_documented": 0,
            "fields_documented": 0,
            "has_data_dictionary": False,
        },
        "overall": {
            "classification": "Minimal/stub",
            "model_type": "Standard projection (FHIR) + undocumented native",
            "documentation_quality": "Very poor",
        },
    }

    with open(OUTPUT / "artifact-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote artifact-summary.json")

    # Print key stats
    print(f"\n=== Key Statistics ===")
    print(f"FHIR resource types in CapabilityStatement: {fhir['resource_type_count']}")
    print(f"US Core profiles documented in Single Patient API: {inventory['summary']['total_fhir_profiles_documented']}")
    print(f"  Clinical: {len(clinical_resources)}")
    print(f"  Infrastructure/Admin: {len(infra_resources)}")
    print(f"Native export tables documented: 0")
    print(f"Native export fields documented: 0")
    print(f"Data dictionary present: No")
    print(f"Sample data present: No")
    print(f"(b)(10) PDF pages: 1")
    print(f"(b)(10) PDF word count: ~150")
