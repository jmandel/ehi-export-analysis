#!/usr/bin/env python3
"""
Parse all structured artifacts from TriMed Technologies EHI export documentation
and produce a full-entity-inventory.json combining:
1. SOAP Patient API methods and their response fields (the C-CDA export)
2. Database tables revealed in hidden SQL queries
3. FHIR API resources from CapabilityStatement
4. C-CDA sections from sample XML files
"""

import json
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), 
    "../../../results/trimed-technologies--trimed-complete/downloads")
OUT_DIR = os.path.dirname(__file__)

def load_json(path):
    with open(os.path.join(RESULTS_DIR, path)) as f:
        return json.load(f)

# 1. SOAP Patient API methods
patient_api = load_json("enrichment/patient-api-methods.json")

# 2. Database schema from hidden SQL
db_schema = load_json("enrichment/database-schema-from-sql.json")

# 3. FHIR resources
fhir_resources = load_json("enrichment/fhir-resources.json")

# 4. C-CDA sections
ccda_sections = load_json("enrichment/ccda-sections.json")

# 5. FHIR API coverage (OpenAPI endpoints)
fhir_api = load_json("enrichment/fhir-api-coverage.json")

def categorize_method(name):
    mapping = {
        "LookupPatientId": "Demographics",
        "GetPatientData": "Comprehensive Clinical",
        "GetPatientAllergy": "Allergies",
        "GetPatientProblemList": "Problems/Conditions",
        "GetPatientMedication": "Medications",
        "GetPatientImmunization": "Immunizations",
        "GetPatientLabResult": "Lab Results",
        "GetPatientEncounter": "Encounters",
        "GetPatientEncompassingEncounter": "Encounters",
        "GetPatientVitals": "Vitals"
    }
    return mapping.get(name, "Other")

# Build the inventory
inventory = {
    "product": "TriMed Complete",
    "analysis_date": "2026-02-16",
    "sources": {
        "soap_api": {
            "source_file": "enrichment/patient-api-methods.json",
            "description": "SOAP Patient Data API v1.3 - 10 methods returning C-CDA XML",
            "base_url": "https://svcs-ccd.trimed.cloud/PatientAPI.asmx"
        },
        "database_schema": {
            "source_file": "enrichment/database-schema-from-sql.json",
            "description": "Oracle database tables extracted from hidden SQL queries",
            "database_type": "Oracle"
        },
        "fhir_api": {
            "source_file": "enrichment/fhir-resources.json",
            "description": "FHIR R4 API - CapabilityStatement resources",
            "base_url": "https://fhir.trimed.cloud"
        },
        "ccda_samples": {
            "source_file": "enrichment/ccda-sections.json",
            "description": "C-CDA sections extracted from 9 sample XML responses"
        }
    },
    "soap_api_methods": [],
    "database_tables": [],
    "fhir_resources": [],
    "ccda_sections": [],
    "summary": {}
}

# Process SOAP API methods
total_soap_req_params = 0
total_soap_resp_params = 0
for method in patient_api["methods"]:
    req_params = []
    for p in method.get("requestParams", []):
        req_params.append({
            "name": p.get("name", ""),
            "type": p.get("type", ""),
            "required": p.get("required", ""),
            "description": p.get("description", "")
        })
    resp_params = []
    for p in method.get("responseParams", []):
        resp_params.append({
            "name": p.get("name", ""),
            "type": p.get("type", ""),
            "description": p.get("description", "")
        })
    
    # Count non-auth request params (exclude sAuthKey, IEnterpriseID, ICompanyID, ResponseCode, Message)
    auth_params = {"sAuthKey", "IEnterpriseID", "ICompanyID", "ResponseCode", "Message", "sRequestFrom"}
    clinical_req = [p for p in req_params if p["name"] not in auth_params]
    
    total_soap_req_params += len(req_params)
    total_soap_resp_params += len(resp_params)
    
    inventory["soap_api_methods"].append({
        "name": method["name"],
        "endpoint": method.get("endpoint", ""),
        "http_verb": method.get("httpVerb", ""),
        "request_params_total": len(req_params),
        "request_params_clinical": len(clinical_req),
        "response_params": len(resp_params),
        "request_parameters": req_params,
        "response_parameters": resp_params,
        "category": categorize_method(method["name"]),
        "has_date_filter": any(p["name"].startswith("dStart") or p["name"].startswith("dEnd") or p["name"] == "lRelativeDays" for p in req_params)
    })

# categorize_method already defined above

# Process database tables
total_db_columns = 0
for table_name, table_info in db_schema.get("tables", {}).items():
    columns = table_info.get("columns", [])
    total_db_columns += len(columns)
    inventory["database_tables"].append({
        "table_name": table_name,
        "description": table_info.get("description", ""),
        "column_count": len(columns),
        "columns": columns,
        "used_by": table_info.get("usedBy", "")
    })

# Process FHIR resources
for res in fhir_resources.get("resources", []):
    inventory["fhir_resources"].append({
        "type": res["type"],
        "profile": res.get("profile"),
        "interactions": res.get("interactions", []),
        "search_params": res.get("searchParams", []),
        "search_param_count": len(res.get("searchParams", []))
    })

# Process C-CDA sections (from GetPatientData.xml, the comprehensive export)
for sample in ccda_sections.get("samples", []):
    if sample["filename"] == "GetPatientData.xml":
        for section in sample.get("sections", []):
            unique_templates = list(set(section.get("templateIds", [])))
            inventory["ccda_sections"].append({
                "title": section["title"],
                "loinc_code": section.get("code", ""),
                "display_name": section.get("displayName", ""),
                "template_count": len(unique_templates),
                "template_ids": unique_templates
            })

# Compute summary statistics
resp_params_with_desc = 0
resp_params_total = 0
for m in inventory["soap_api_methods"]:
    for p in m["response_parameters"]:
        resp_params_total += 1
        if p.get("description", "").strip():
            resp_params_with_desc += 1

inventory["summary"] = {
    "soap_api": {
        "method_count": len(inventory["soap_api_methods"]),
        "total_request_params": total_soap_req_params,
        "total_response_params": total_soap_resp_params,
        "response_params_with_descriptions": resp_params_with_desc,
        "response_params_without_descriptions": resp_params_total - resp_params_with_desc,
        "description_coverage_pct": round(resp_params_with_desc / resp_params_total * 100, 1) if resp_params_total > 0 else 0
    },
    "database_schema": {
        "table_count": len(inventory["database_tables"]),
        "total_columns": total_db_columns,
        "database_type": "Oracle"
    },
    "fhir_api": {
        "resource_count": len(inventory["fhir_resources"]),
        "total_search_params": sum(r["search_param_count"] for r in inventory["fhir_resources"]),
        "fhir_version": fhir_resources.get("fhirVersion", ""),
        "bulk_data_support": "export" in fhir_resources.get("systemOperations", [])
    },
    "ccda_sections": {
        "section_count": len(inventory["ccda_sections"]),
        "sample_files_parsed": ccda_sections.get("totalFiles", 0)
    },
    "fhir_openapi_endpoints": len(fhir_api.get("endpoints", [])) if isinstance(fhir_api, dict) else 0
}

# Write output
output_path = os.path.join(OUT_DIR, "full-entity-inventory.json")
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Written to {output_path}")
print(f"\n=== Summary ===")
print(f"SOAP API methods: {inventory['summary']['soap_api']['method_count']}")
print(f"  Total request params: {inventory['summary']['soap_api']['total_request_params']}")
print(f"  Total response params: {inventory['summary']['soap_api']['total_response_params']}")
print(f"  Response params with descriptions: {resp_params_with_desc}/{resp_params_total} ({inventory['summary']['soap_api']['description_coverage_pct']}%)")
print(f"Database tables (from SQL): {inventory['summary']['database_schema']['table_count']}")
print(f"  Total columns: {inventory['summary']['database_schema']['total_columns']}")
print(f"FHIR resources: {inventory['summary']['fhir_api']['resource_count']}")
print(f"  Bulk data: {inventory['summary']['fhir_api']['bulk_data_support']}")
print(f"C-CDA sections (in GetPatientData.xml): {inventory['summary']['ccda_sections']['section_count']}")
print(f"FHIR OpenAPI endpoints: {inventory['summary']['fhir_openapi_endpoints']}")
