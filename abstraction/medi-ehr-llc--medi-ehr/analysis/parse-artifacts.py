#!/usr/bin/env python3
"""Parse all Medi-EHR EHI export artifacts and produce a structured inventory."""

import json
import re
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/medi-ehr-llc--medi-ehr")
DOWNLOADS_DIR = RESULTS_DIR / "downloads"
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/medi-ehr-llc--medi-ehr/analysis")

def parse_compliance_page():
    """Extract the EHI export documentation text from compliance-page.html."""
    with open(DOWNLOADS_DIR / "compliance-page.html", "r", errors="replace") as f:
        content = f.read()
    
    # Find the EHI section
    start = content.find("Electronic Health Information")
    if start < 0:
        return {"error": "EHI section not found"}
    
    # Get text up to footer
    end = min(len(content), start + 5000)
    chunk = content[start:end]
    
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '\n', chunk)
    text = re.sub(r'\n\s*\n', '\n', text)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Stop at footer/contacts
    ehi_lines = []
    for line in lines:
        if line.startswith("Contacts") or line.startswith("Support (24/7"):
            break
        ehi_lines.append(line)
    
    return {
        "source": "compliance-page.html",
        "section_title": "I. Electronic Health Information Export",
        "full_text": "\n".join(ehi_lines),
        "mentions_csv": True,
        "mentions_html": True,
        "csv_description": "Generic definition of CSV format. No field list, no data dictionary, no schema.",
        "html_description": "Generic definition of HTML format. No structure details.",
        "single_patient_export": True,
        "multi_patient_export": True,
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_field_definitions": False,
        "has_schema": False,
        "api_documentation_link": "https://proda.mediemr.net:8443/pls/htmldb/f?p=300:10"
    }

def parse_api_docs():
    """Parse the enrichment/api-docs.json for structured API information."""
    with open(DOWNLOADS_DIR / "enrichment" / "api-docs.json", "r") as f:
        api_data = json.load(f)
    
    # Extract C-CDA section toggles from the patient data endpoint
    patient_data_endpoint = None
    for ep in api_data["endpoints"]:
        if ep["path"] == "/mediehrgetpatientdata.php":
            patient_data_endpoint = ep
            break
    
    ccda_sections = []
    if patient_data_endpoint:
        for param in patient_data_endpoint["parameters"]:
            if param["name"].startswith("PAT_"):
                section_name = param["description"].split("the ")[-1].split(" component")[0].split(" section")[0] if "component" in param["description"] or "section" in param["description"] else param["name"]
                ccda_sections.append({
                    "parameter": param["name"],
                    "section_name": section_name,
                    "toggle": "S (show) / H (hide)"
                })
    
    return {
        "source": "API_Document.html (parsed via enrichment/api-docs.json)",
        "api_title": api_data.get("title", ""),
        "api_version": api_data.get("version", ""),
        "server_url": api_data.get("serverUrl", ""),
        "endpoint_count": len(api_data["endpoints"]),
        "endpoints": [
            {
                "method": ep["method"],
                "path": ep["path"],
                "summary": ep["summary"],
                "parameter_count": len(ep["parameters"]),
                "parameters": [p["name"] for p in ep["parameters"]]
            }
            for ep in api_data["endpoints"]
        ],
        "ccda_sections": ccda_sections,
        "ccda_section_count": len(ccda_sections),
        "error_codes": api_data.get("errorCodes", []),
        "authentication": "Proprietary access/refresh token (not OAuth 2.0, not SMART on FHIR)",
        "response_format": "C-CDA 2.1 XML",
        "has_duplicate_username_param": True,  # USERNAME appears twice in mediehrgetpatientdata.php
    }

def parse_fhir_bundle():
    """Parse fhir-service-base-bundle.json."""
    with open(DOWNLOADS_DIR / "fhir-service-base-bundle.json", "r") as f:
        bundle = json.load(f)
    
    entries = bundle.get("entry", [])
    return {
        "source": "fhir-service-base-bundle.json",
        "bundle_type": bundle.get("type", ""),
        "entry_count": len(entries),
        "resources": [
            {
                "resourceType": e["resource"]["resourceType"],
                "id": e["resource"].get("id", ""),
                "name": e["resource"].get("name", "")
            }
            for e in entries if "resource" in e
        ],
        "fhir_server": "sandbox-r4.interopengine.com (InteropEngine - third party)",
        "is_production": False,
        "note": "This is the (g)(10) standardized FHIR API, separate from (b)(10) EHI export"
    }

def build_full_inventory():
    """Build the complete entity inventory from all artifacts."""
    
    # The C-CDA sections are the only documented "entities" in this export
    ccda_section_map = {
        "PAT_ALLERGY": "Allergies and Adverse Reactions",
        "PAT_MEDS": "Medications",
        "PAT_PROBLEM": "Problems / Diagnoses",
        "PAT_ENCOUNTER": "Encounters",
        "PAT_IMMUNIZATION": "Immunizations",
        "PAT_VITALS": "Vital Signs",
        "PAT_SOCHX": "Social History",
        "PAT_PROCEDURES": "Procedures",
        "PAT_LABS": "Laboratory Results",
        "PAT_IMPLANTABLEDEVICES": "Implantable Devices",
        "PAT_GOALS": "Goals",
        "PAT_FUNCTIONALSTATUS": "Functional Status",
        "PAT_COGNITIVESTATUS": "Cognitive Status",
        "PAT_REFERRAL": "Referrals",
        "PAT_ASSESSMENT": "Assessment",
        "PAT_CARETEAM": "Care Team Members",
        "PAT_HEALTH_CONCERNS": "Health Concerns",
        "PAT_PLANOFTREAT": "Plan of Treatment",
        "PAT_DI_REPORT": "Diagnostic and Imaging Reports"
    }
    
    entities = []
    for param, section_name in ccda_section_map.items():
        entities.append({
            "entity_name": param,
            "display_name": section_name,
            "format": "C-CDA 2.1 XML section",
            "fields": "N/A - no field-level documentation provided",
            "field_count": None,
            "fields_with_descriptions": 0,
            "types_documented": False,
            "relationships_documented": False,
            "value_sets_documented": False,
            "category": "Clinical",
            "documentation_level": "section-name-only",
            "notes": "Only the section name and toggle parameter (S/H) are documented. No field-level detail."
        })
    
    return {
        "export_type": "C-CDA 2.1 clinical document (standard-based projection)",
        "total_entities": len(entities),
        "total_fields": 0,
        "fields_with_descriptions": 0,
        "documentation_level": "section-name-only (no field-level detail)",
        "entities": entities,
        "additional_formats_claimed": {
            "csv": {
                "documented": False,
                "description": "Mentioned on compliance page but no field list, no schema, no sample data"
            },
            "html": {
                "documented": False,
                "description": "Mentioned on compliance page but no structure details"
            }
        },
        "missing_domains": [
            "Billing / Claims / Payments",
            "Insurance / Coverage",
            "Consent forms",
            "Clinical notes / documents (beyond C-CDA structured sections)",
            "Patient portal messages",
            "Workers compensation / no-fault claims",
            "Behavioral health assessments",
            "ASC surgical data",
            "Residential treatment records",
            "Scanned documents / images",
            "Telemedicine records",
            "Prescription / e-prescribing history"
        ]
    }

def main():
    compliance = parse_compliance_page()
    api = parse_api_docs()
    fhir = parse_fhir_bundle()
    inventory = build_full_inventory()
    
    # Artifact summary
    artifacts = {
        "artifacts_reviewed": [
            {
                "file": "compliance-page.html",
                "size_bytes": (DOWNLOADS_DIR / "compliance-page.html").stat().st_size,
                "type": "HTML page",
                "description": "Main EHI compliance page. Contains ~3 paragraphs on EHI export plus generic CSV/HTML format definitions. No data dictionary.",
                "informativeness": "low"
            },
            {
                "file": "compliance-page.png",
                "size_bytes": (DOWNLOADS_DIR / "compliance-page.png").stat().st_size,
                "type": "Screenshot",
                "description": "Full-page screenshot of compliance page confirming rendered content matches HTML parse.",
                "informativeness": "low (confirmatory)"
            },
            {
                "file": "API_Document.html",
                "size_bytes": (DOWNLOADS_DIR / "API_Document.html").stat().st_size,
                "type": "Swagger UI HTML",
                "description": "Pre-rendered Swagger UI documenting 4 REST API endpoints. The main export endpoint returns C-CDA 2.1 with 19 toggleable sections.",
                "informativeness": "medium (most informative artifact)"
            },
            {
                "file": "developer-portal-api-docs.png",
                "size_bytes": (DOWNLOADS_DIR / "developer-portal-api-docs.png").stat().st_size,
                "type": "Screenshot",
                "description": "Screenshot of Oracle APEX developer portal with embedded Swagger UI iframe.",
                "informativeness": "low (confirmatory)"
            },
            {
                "file": "fhir-service-base-bundle.json",
                "size_bytes": (DOWNLOADS_DIR / "fhir-service-base-bundle.json").stat().st_size,
                "type": "FHIR Bundle JSON",
                "description": "FHIR R4 service base URL bundle pointing to InteropEngine sandbox. Separate from (b)(10) export.",
                "informativeness": "low (not EHI export)"
            },
            {
                "file": "enrichment/api-docs.json",
                "size_bytes": (DOWNLOADS_DIR / "enrichment" / "api-docs.json").stat().st_size,
                "type": "Extracted JSON",
                "description": "Structured extraction of API_Document.html: 4 endpoints, all parameters, 19 C-CDA sections, 8 error codes.",
                "informativeness": "medium (structured version of API_Document.html)"
            },
            {
                "file": "public-fhir-api-page.html",
                "size_bytes": (DOWNLOADS_DIR / "public-fhir-api-page.html").stat().st_size,
                "type": "HTML page",
                "description": "Public FHIR API page. Documents (g)(10) FHIR API via InteropEngine, not (b)(10) EHI export.",
                "informativeness": "low (not EHI export)"
            }
        ],
        "compliance_page": compliance,
        "api_documentation": api,
        "fhir_bundle": fhir,
        "full_entity_inventory": inventory
    }
    
    # Summary statistics
    summary = {
        "classification": "Standard-based projection",
        "export_format": "C-CDA 2.1 XML (via proprietary REST API); CSV and HTML mentioned but undocumented",
        "model_type": "Standard projection (C-CDA clinical document)",
        "documented_entities": 19,
        "documented_fields": 0,
        "fields_with_descriptions_pct": "N/A (no field-level documentation)",
        "sample_data": False,
        "bulk_export": "Claimed on compliance page but no API mechanism documented",
        "data_dictionary": False,
        "domains_covered": "7 of 15 applicable domains (clinical only, via C-CDA sections)",
        "domains_applicable": 15,
        "domains_with_evidence": 7,
        "api_endpoints": 4,
        "ccda_sections": 19,
        "authentication": "Proprietary token-based (not OAuth/SMART)"
    }
    
    # Write outputs
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(OUTPUT_DIR / "artifact-analysis.json", "w") as f:
        json.dump(artifacts, f, indent=2)
    
    with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("=== Medi-EHR EHI Export Analysis ===")
    print(f"Classification: {summary['classification']}")
    print(f"Export format: {summary['export_format']}")
    print(f"Documented entities (C-CDA sections): {summary['documented_entities']}")
    print(f"Field-level documentation: None")
    print(f"Data dictionary: No")
    print(f"Sample data: No")
    print(f"Domains covered: {summary['domains_covered']}")
    print(f"\nArtifacts reviewed: {len(artifacts['artifacts_reviewed'])}")
    print(f"API endpoints: {summary['api_endpoints']}")
    print(f"C-CDA sections: {summary['ccda_sections']}")
    print(f"\nOutput files:")
    print(f"  - full-entity-inventory.json")
    print(f"  - artifact-analysis.json")
    print(f"  - summary-stats.json")

if __name__ == "__main__":
    main()
