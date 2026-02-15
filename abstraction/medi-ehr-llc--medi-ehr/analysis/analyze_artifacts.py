#!/usr/bin/env python3
"""Analyze all Medi-EHR EHI export artifacts and produce structured inventory."""

import json
import os
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/medi-ehr-llc--medi-ehr")
DOWNLOADS_DIR = RESULTS_DIR / "downloads"
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/medi-ehr-llc--medi-ehr/analysis")

def analyze_files_manifest():
    """Parse files.json and inventory all artifacts."""
    with open(RESULTS_DIR / "files.json") as f:
        data = json.load(f)
    
    artifacts = []
    for file_info in data.get("files", []):
        path = DOWNLOADS_DIR / file_info["path"].replace("downloads/", "")
        size = file_info.get("size_bytes", 0)
        artifacts.append({
            "filename": os.path.basename(file_info["path"]),
            "path": file_info["path"],
            "source_url": file_info.get("source_url", "n/a"),
            "size_bytes": size,
            "description": file_info.get("description", ""),
            "exists_on_disk": path.exists() if not file_info["path"].startswith("downloads/enrichment") 
                             else (DOWNLOADS_DIR / "enrichment" / os.path.basename(file_info["path"])).exists()
        })
    return artifacts

def analyze_api_docs():
    """Parse the extracted API documentation JSON."""
    api_path = DOWNLOADS_DIR / "enrichment" / "api-docs.json"
    with open(api_path) as f:
        data = json.load(f)
    
    endpoints = data.get("endpoints", [])
    ccda_sections = []
    total_params = 0
    
    for ep in endpoints:
        params = ep.get("parameters", [])
        total_params += len(params)
        if ep["path"] == "/mediehrgetpatientdata.php":
            ccda_sections = ep.get("responseSections", [])
    
    return {
        "api_title": data.get("title", ""),
        "api_version": data.get("version", ""),
        "server_url": data.get("serverUrl", ""),
        "endpoint_count": len(endpoints),
        "total_parameters": total_params,
        "ccda_section_count": len(ccda_sections),
        "ccda_sections": ccda_sections,
        "error_code_count": len(data.get("errorCodes", [])),
        "endpoints": [
            {
                "method": ep["method"],
                "path": ep["path"],
                "summary": ep["summary"],
                "param_count": len(ep.get("parameters", [])),
                "response_format": ep.get("responseFormat", "unknown")
            }
            for ep in endpoints
        ]
    }

def analyze_compliance_page():
    """Extract key facts from compliance page content."""
    return {
        "sections": [
            {
                "number": "I",
                "title": "Electronic Health Information Export",
                "subsections": [
                    {"title": "Single Patient Export", "content": "Allows user to export EHI for single patient without developer assistance"},
                    {"title": "Multi-Patient Export", "content": "Can export all data for patient population"},
                    {"title": "File Formats - CSV", "content": "Generic CSV format description (no data dictionary)"},
                    {"title": "File Formats - HTML", "content": "Generic HTML format description (no data dictionary)"}
                ]
            },
            {
                "number": "II",
                "title": "API documentation",
                "subsections": [
                    {"title": "Click Here link", "content": "Links to Oracle APEX developer portal with Swagger UI"}
                ]
            }
        ],
        "data_dictionary_present": False,
        "field_list_present": False,
        "sample_data_present": False,
        "schema_present": False,
        "export_format_details": "CSV and HTML mentioned but only generically described; API returns C-CDA 2.1 XML"
    }

def build_coverage_assessment():
    """Map C-CDA sections to EHI domains and assess gaps."""
    # C-CDA sections from API
    ccda_to_domain = {
        "Allergies": "Allergies",
        "Medications": "Medications / prescriptions",
        "Problems": "Problems / conditions / diagnoses",
        "Encounters": "Encounters / visits",
        "Immunizations": "Immunizations",
        "Vitals": "Vitals",
        "Social History": "Demographics (partial)",
        "Procedures": "Procedures",
        "Labs": "Lab results",
        "Implantable Devices": "Procedures (partial)",
        "Goals": "Care plans / goals",
        "Functional Status": "Clinical notes / documents (partial)",
        "Cognitive Status": "Clinical notes / documents (partial)",
        "Referrals": "Orders / referrals",
        "Assessment": "Clinical notes / documents (partial)",
        "Care Team": "Care plans / goals (partial)",
        "Health Concerns": "Problems / conditions / diagnoses (partial)",
        "Plan of Treatment": "Care plans / goals (partial)",
        "Diagnostic and Imaging Reports": "Imaging / diagnostic reports"
    }
    
    domains = [
        {"domain": "Demographics", "coverage": "⚠️ Partial", 
         "evidence": "Patient search params (name, DOB, SSN, email, mobile); Social History C-CDA section; no dedicated demographics export",
         "gap": "Basic demographics in patient search; no address, race, ethnicity, language, or insurance fields documented"},
        {"domain": "Encounters / visits", "coverage": "⚠️ Partial",
         "evidence": "PAT_ENCOUNTER C-CDA section",
         "gap": "C-CDA encounter section present but no field-level detail; unknown depth"},
        {"domain": "Problems / conditions / diagnoses", "coverage": "⚠️ Partial",
         "evidence": "PAT_PROBLEM, PAT_HEALTH_CONCERNS C-CDA sections",
         "gap": "Standard C-CDA sections; no detail on completeness vs native problem list"},
        {"domain": "Medications / prescriptions", "coverage": "⚠️ Partial",
         "evidence": "PAT_MEDS C-CDA section",
         "gap": "C-CDA medications section; e-prescribing history and EPCS records not specifically addressed"},
        {"domain": "Allergies", "coverage": "⚠️ Partial",
         "evidence": "PAT_ALLERGY C-CDA section",
         "gap": "Standard C-CDA section present"},
        {"domain": "Immunizations", "coverage": "⚠️ Partial",
         "evidence": "PAT_IMMUNIZATION C-CDA section",
         "gap": "Standard C-CDA section present"},
        {"domain": "Vitals", "coverage": "⚠️ Partial",
         "evidence": "PAT_VITALS C-CDA section",
         "gap": "Standard C-CDA section present"},
        {"domain": "Lab results", "coverage": "⚠️ Partial",
         "evidence": "PAT_LABS C-CDA section",
         "gap": "C-CDA section present; unknown if full discrete results or summaries"},
        {"domain": "Imaging / diagnostic reports", "coverage": "⚠️ Partial",
         "evidence": "PAT_DI_REPORT C-CDA section",
         "gap": "C-CDA section present; likely report text only, not images"},
        {"domain": "Procedures", "coverage": "⚠️ Partial",
         "evidence": "PAT_PROCEDURES, PAT_IMPLANTABLEDEVICES C-CDA sections",
         "gap": "Standard C-CDA sections; ASC surgical detail unclear"},
        {"domain": "Clinical notes / documents", "coverage": "⚠️ Partial",
         "evidence": "PAT_ASSESSMENT, PAT_FUNCTIONALSTATUS, PAT_COGNITIVESTATUS C-CDA sections",
         "gap": "No dedicated clinical notes section; progress notes, H&P, specialty templates not explicitly represented"},
        {"domain": "Care plans / goals", "coverage": "⚠️ Partial",
         "evidence": "PAT_GOALS, PAT_PLANOFTREAT, PAT_CARETEAM C-CDA sections",
         "gap": "Standard C-CDA sections present"},
        {"domain": "Orders / referrals", "coverage": "⚠️ Partial",
         "evidence": "PAT_REFERRAL C-CDA section",
         "gap": "Referrals section present; CPOE orders not explicitly addressed"},
        {"domain": "Insurance / coverage", "coverage": "❌ Not covered",
         "evidence": "No insurance entities in documented export",
         "gap": "Product has insurance benefits verification; not in export"},
        {"domain": "Claims / billing", "coverage": "❌ Not covered",
         "evidence": "No billing entities in documented export",
         "gap": "Product has integrated billing/PM with superbills, claims, RCM; significant gap"},
        {"domain": "Payments", "coverage": "❌ Not covered",
         "evidence": "No payment entities in documented export",
         "gap": "Product processes payments; not in export"},
        {"domain": "Consents / directives", "coverage": "❌ Not covered",
         "evidence": "No consent entities in documented export",
         "gap": "Product has dedicated Consent Module; consent forms not in export"},
        {"domain": "Patient communications / portal messages", "coverage": "❌ Not covered",
         "evidence": "No portal/messaging entities in documented export",
         "gap": "Product has patient portal with secure messaging; not in export"},
        {"domain": "Specialty-specific (Behavioral Health)", "coverage": "❌ Not covered",
         "evidence": "No behavioral health entities in documented export",
         "gap": "Product has dedicated BH module; BH assessments/treatment plans not in export"},
        {"domain": "Specialty-specific (ASC/Surgical)", "coverage": "❌ Not covered",
         "evidence": "No ASC-specific entities in documented export",
         "gap": "Product has ASC module; surgical data not specifically addressed"},
        {"domain": "Specialty-specific (Residential Treatment)", "coverage": "❌ Not covered",
         "evidence": "No residential treatment entities in documented export",
         "gap": "Product has residential treatment module; not in export"},
    ]
    
    covered = sum(1 for d in domains if d["coverage"].startswith("✅"))
    partial = sum(1 for d in domains if d["coverage"].startswith("⚠️"))
    not_covered = sum(1 for d in domains if d["coverage"].startswith("❌"))
    
    return {
        "domains": domains,
        "summary": {
            "total_domains": len(domains),
            "covered": covered,
            "partial": partial,
            "not_covered": not_covered,
            "applicable_domains": len(domains),
            "domains_with_any_coverage": covered + partial
        }
    }

def main():
    print("=" * 60)
    print("Medi-EHR EHI Export Artifact Analysis")
    print("=" * 60)
    
    # 1. Artifacts inventory
    artifacts = analyze_files_manifest()
    print(f"\n## Artifacts: {len(artifacts)} files")
    for a in artifacts:
        print(f"  - {a['filename']} ({a['size_bytes']:,} bytes) - {a['description'][:80]}")
    
    # 2. API documentation analysis
    api = analyze_api_docs()
    print(f"\n## API Documentation")
    print(f"  Title: {api['api_title']}")
    print(f"  Server: {api['server_url']}")
    print(f"  Endpoints: {api['endpoint_count']}")
    print(f"  Total parameters across all endpoints: {api['total_parameters']}")
    print(f"  C-CDA sections: {api['ccda_section_count']}")
    for s in api['ccda_sections']:
        print(f"    - {s}")
    print(f"  Error codes: {api['error_code_count']}")
    
    # 3. Compliance page analysis
    compliance = analyze_compliance_page()
    print(f"\n## Compliance Page")
    print(f"  Data dictionary: {compliance['data_dictionary_present']}")
    print(f"  Field list: {compliance['field_list_present']}")
    print(f"  Sample data: {compliance['sample_data_present']}")
    print(f"  Schema: {compliance['schema_present']}")
    print(f"  Format details: {compliance['export_format_details']}")
    
    # 4. Coverage assessment
    coverage = build_coverage_assessment()
    print(f"\n## Coverage Assessment")
    print(f"  Total applicable domains: {coverage['summary']['total_domains']}")
    print(f"  Fully covered: {coverage['summary']['covered']}")
    print(f"  Partially covered: {coverage['summary']['partial']}")
    print(f"  Not covered: {coverage['summary']['not_covered']}")
    
    for d in coverage['domains']:
        print(f"  {d['coverage']} {d['domain']}: {d['gap'][:80]}")
    
    # Save full analysis as JSON
    full_analysis = {
        "artifacts": artifacts,
        "api_documentation": api,
        "compliance_page": compliance,
        "coverage_assessment": coverage
    }
    
    output_path = OUTPUT_DIR / "full-analysis.json"
    with open(output_path, "w") as f:
        json.dump(full_analysis, f, indent=2)
    print(f"\nFull analysis saved to {output_path}")

if __name__ == "__main__":
    main()
