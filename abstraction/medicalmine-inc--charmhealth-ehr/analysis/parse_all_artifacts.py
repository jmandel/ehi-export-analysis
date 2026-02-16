"""
Parse all CharmHealth EHI export artifacts and produce a full entity inventory.

Inputs:
  - downloads/enrichment/fhir-api-extracted.json (FHIR API docs)
  - downloads/billing-reports.html (billing report types)
  - downloads/claims.html (claims report types)
  - downloads/analytics.html (analytics report types)
  - downloads/export-encounters-as-hl7-messages.html (HL7 segment descriptions)
  - downloads/electronic-health-information-export.html (main EHI page)

Outputs:
  - analysis/full-entity-inventory.json
  - analysis/summary-stats.json
"""

import json
import re
import os
import sys
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/medicalmine-inc--charmhealth-ehr/downloads")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/medicalmine-inc--charmhealth-ehr/analysis")


def parse_fhir_resources(fhir_json):
    """Extract all FHIR resources with their fields from sample responses."""
    entities = []
    
    for resource in fhir_json["resources"]:
        name = resource["name"]
        operations = resource.get("operations", [])
        
        # Extract fields from sample response examples
        fields = []
        sample_fields = set()
        
        for op in operations:
            resp = op.get("responseExample", "")
            if resp:
                # Try to extract JSON from the response example
                json_match = re.search(r'\{.*\}', resp, re.DOTALL)
                if json_match:
                    try:
                        resp_json = json.loads(json_match.group())
                        # For Bundle responses, look at the first entry's resource
                        if resp_json.get("resourceType") == "Bundle":
                            entries = resp_json.get("entry", [])
                            if entries:
                                res = entries[0].get("resource", {})
                                extract_fields(res, "", sample_fields)
                        else:
                            extract_fields(resp_json, "", sample_fields)
                    except json.JSONDecodeError:
                        pass
        
        # Extract search parameters as documented fields
        search_params = []
        for op in operations:
            for param in op.get("parameters", []):
                search_params.append({
                    "name": param["name"],
                    "type": param.get("type", ""),
                    "required": param.get("required", "optional"),
                    "description": param.get("description", ""),
                    "operation": op["name"]
                })
        
        # Build field list from sample data
        for field_path in sorted(sample_fields):
            fields.append({
                "name": field_path,
                "source": "sample_response",
                "description": "",  # FHIR standard fields - no custom descriptions provided
                "type": ""  # Types inferred from FHIR spec, not explicitly documented
            })
        
        entity = {
            "name": name,
            "category": "Clinical Data (FHIR R4)",
            "source_format": "FHIR R4 JSON / NDJSON",
            "us_core_profile": resource.get("usCorProfile"),
            "description": resource.get("description", ""),
            "operations": [{"name": o["name"], "type": o["type"], "api_url": o["apiUrl"]} for o in operations],
            "search_parameters": search_params,
            "sample_response_fields": fields,
            "field_count": len(fields),
            "search_param_count": len(search_params)
        }
        entities.append(entity)
    
    return entities


def extract_fields(obj, prefix, field_set):
    """Recursively extract field paths from a JSON object."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            field_set.add(path)
            if isinstance(value, dict):
                extract_fields(value, path, field_set)
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    extract_fields(value[0], f"{path}[]", field_set)


def parse_billing_reports(html_path):
    """Parse billing-reports.html to extract report types. Uses h2=categories, h3=reports."""
    with open(html_path) as f:
        content = f.read()
    
    reports = []
    # Split by h2 to get category sections
    sections = re.split(r'<h2[^>]*>', content)
    
    for section in sections[1:]:  # skip before first h2
        cat_match = re.match(r'(.*?)</h2>', section, re.DOTALL)
        if not cat_match:
            continue
        category = re.sub(r'<[^>]+>', '', cat_match.group(1)).strip()
        if category == 'Reports':
            continue  # Skip the top-level "Reports" heading
        
        # Find h3 subsections (individual reports)
        h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', section, re.DOTALL)
        report_names = [re.sub(r'<[^>]+>', '', h).strip() for h in h3s]
        
        has_csv = bool(re.search(r'CSV|csv', section))
        has_export = bool(re.search(r'[Ee]xport', section))
        
        if report_names:
            for rname in report_names:
                if rname:
                    reports.append({
                        "name": rname,
                        "category": category,
                        "has_csv_export": has_csv,
                        "has_export_mention": has_export,
                        "source": "billing-reports.html"
                    })
        else:
            # Category with no sub-reports — the category itself is the report
            reports.append({
                "name": category,
                "category": "Billing Reports",
                "has_csv_export": has_csv,
                "has_export_mention": has_export,
                "source": "billing-reports.html"
            })
    
    return reports


def parse_claims_reports(html_path):
    """Parse claims.html: h2=sections, h3 under 'Claims - Reports'=individual reports."""
    with open(html_path) as f:
        content = f.read()
    
    reports = []
    
    # Split by h2 and find the "Claims - Reports" section
    sections = re.split(r'<h2[^>]*>', content)
    for section in sections:
        if re.match(r'Claims\s*-\s*Reports', section):
            h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', section, re.DOTALL)
            for h in h3s:
                name = re.sub(r'<[^>]+>', '', h).strip()
                if name:
                    reports.append({
                        "name": name,
                        "category": "Claims Reports",
                        "has_csv_export": True,
                        "source": "claims.html"
                    })
    
    # Extract all h2 workflow sections
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    claim_sections = [re.sub(r'<[^>]+>', '', h).strip() for h in h2s]
    
    return reports, claim_sections


def parse_analytics_reports(html_path):
    """Parse analytics.html: h2 headings are the report types."""
    with open(html_path) as f:
        content = f.read()
    
    reports = []
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    
    for h in h2s:
        name = re.sub(r'<[^>]+>', '', h).strip()
        if name and name != 'Analytics and Reporting':
            reports.append({
                "name": name,
                "category": "Analytics",
                "source": "analytics.html"
            })
    
    return reports


def parse_hl7_segments(html_path):
    """Parse the HL7 message export page to extract segment definitions."""
    with open(html_path) as f:
        content = f.read()
    
    tables_data = []
    tables = re.findall(r'<table[^>]*>(.*?)</table>', content, re.DOTALL)
    
    # Find table titles
    table_titles = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    table_titles = [re.sub(r'<[^>]+>', '', t).strip() for t in table_titles]
    
    for i, table in enumerate(tables):
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL)
        parsed_rows = []
        for row in rows:
            cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
            cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
            parsed_rows.append(cells)
        
        title = table_titles[i] if i < len(table_titles) else f"Table {i+1}"
        tables_data.append({
            "title": title,
            "header": parsed_rows[0] if parsed_rows else [],
            "rows": parsed_rows[1:] if len(parsed_rows) > 1 else [],
            "row_count": len(parsed_rows) - 1 if parsed_rows else 0
        })
    
    return tables_data


def main():
    # 1. Parse FHIR resources
    with open(RESULTS_DIR / "enrichment" / "fhir-api-extracted.json") as f:
        fhir_data = json.load(f)
    
    fhir_entities = parse_fhir_resources(fhir_data)
    
    # 2. Parse billing reports
    billing_reports = parse_billing_reports(RESULTS_DIR / "billing-reports.html")
    
    # 3. Parse claims reports
    claims_reports, claims_sections = parse_claims_reports(RESULTS_DIR / "claims.html")
    
    # 4. Parse analytics reports
    analytics_reports = parse_analytics_reports(RESULTS_DIR / "analytics.html")
    
    # 5. Parse HL7 segment definitions
    hl7_segments = parse_hl7_segments(RESULTS_DIR / "export-encounters-as-hl7-messages.html")
    
    # Build full inventory
    inventory = {
        "extraction_date": "2026-02-16",
        "source_product": "CharmHealth EHR v1.2",
        "export_mechanisms": [
            {
                "name": "FHIR R4 API",
                "format": "FHIR R4 JSON",
                "scope": "Clinical data",
                "mechanism": "REST API (individual + Bulk Export)",
                "documentation_quality": "API-level documentation with sample responses"
            },
            {
                "name": "FHIR Bulk Export",
                "format": "NDJSON",
                "scope": "Clinical data (bulk)",
                "mechanism": "REST API (async)",
                "documentation_quality": "API endpoint documentation"
            },
            {
                "name": "HL7 CCDA Export",
                "format": "HL7 CCDA v2.1 XML",
                "scope": "Clinical summary",
                "mechanism": "API + EHR UI",
                "documentation_quality": "API endpoint + UI screenshots"
            },
            {
                "name": "CSV Billing Export",
                "format": "CSV",
                "scope": "Billing, claims, insurance data",
                "mechanism": "EHR UI (manual report generation)",
                "documentation_quality": "User guide help pages, no schema documentation"
            },
            {
                "name": "HL7 Billing Messages",
                "format": "HL7 v2 DFT-P03 / ADT-A03",
                "scope": "Encounter billing data for external systems",
                "mechanism": "EHR UI export",
                "documentation_quality": "Segment-level field documentation with 2 tables"
            },
            {
                "name": "PDF Export",
                "format": "PDF",
                "scope": "Individual encounters",
                "mechanism": "EHR UI",
                "documentation_quality": "UI screenshots only"
            }
        ],
        "fhir_resources": fhir_entities,
        "billing_csv_reports": billing_reports,
        "claims_reports": claims_reports,
        "claims_workflow_sections": claims_sections,
        "analytics_reports": analytics_reports,
        "hl7_billing_message_segments": hl7_segments,
        "bulk_export": fhir_data.get("bulkExport", {}),
        "ccda_export": fhir_data.get("ccda", {})
    }
    
    # Compute summary stats
    total_fhir_fields = sum(e["field_count"] for e in fhir_entities)
    total_search_params = sum(e["search_param_count"] for e in fhir_entities)
    # Unique search param names (de-duped across resources)
    unique_params = set()
    for e in fhir_entities:
        for p in e["search_parameters"]:
            unique_params.add(f"{e['name']}.{p['name']}")
    
    # Fields with descriptions from search params
    params_with_desc = sum(1 for e in fhir_entities for p in e["search_parameters"] if p.get("description"))
    
    # Resources with US Core profile
    us_core_count = sum(1 for e in fhir_entities if e.get("us_core_profile"))
    
    hl7_total_fields = sum(t["row_count"] for t in hl7_segments)
    
    summary = {
        "fhir_resources": {
            "count": len(fhir_entities),
            "total_sample_response_fields": total_fhir_fields,
            "total_search_parameters": len(unique_params),
            "search_params_with_descriptions": params_with_desc,
            "resources_with_us_core_profile": us_core_count,
            "resources_without_us_core_profile": len(fhir_entities) - us_core_count,
            "resources_list": [e["name"] for e in fhir_entities]
        },
        "billing_csv_reports": {
            "count": len(billing_reports),
            "categories": list(set(r["category"] for r in billing_reports)),
            "reports_with_csv": sum(1 for r in billing_reports if r.get("has_csv_export"))
        },
        "claims_reports": {
            "count": len(claims_reports),
            "workflow_sections": len(claims_sections)
        },
        "analytics_reports": {
            "count": len(analytics_reports)
        },
        "hl7_billing_messages": {
            "table_count": len(hl7_segments),
            "total_field_definitions": hl7_total_fields,
            "tables": [{"title": t["title"], "field_count": t["row_count"]} for t in hl7_segments]
        },
        "export_mechanisms": len(inventory["export_mechanisms"]),
        "documentation_artifacts": {
            "total_files": 15,  # from files.json
            "html_pages": 6,
            "screenshots": 5,
            "json_extractions": 1,
            "scripts": 1
        }
    }
    
    # Write outputs
    with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(OUTPUT_DIR / "summary-stats.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("=== CharmHealth EHI Export Analysis Summary ===")
    print(f"\nFHIR Resources: {len(fhir_entities)}")
    print(f"  US Core profiled: {us_core_count}")
    print(f"  Total fields from sample responses: {total_fhir_fields}")
    print(f"  Total unique search parameters: {len(unique_params)}")
    print(f"  Search params with descriptions: {params_with_desc}")
    print()
    
    print("FHIR Resources by field count (from samples):")
    for e in sorted(fhir_entities, key=lambda x: x["field_count"], reverse=True):
        profile = "US Core" if e.get("us_core_profile") else "No profile"
        print(f"  {e['name']:30s} {e['field_count']:3d} fields, {e['search_param_count']:2d} search params ({profile})")
    
    print(f"\nBilling CSV Reports: {len(billing_reports)}")
    for cat in set(r["category"] for r in billing_reports):
        cat_reports = [r for r in billing_reports if r["category"] == cat]
        print(f"  {cat}: {len(cat_reports)} reports")
    
    print(f"\nClaims Reports: {len(claims_reports)}")
    for r in claims_reports:
        print(f"  {r['name']}")
    
    print(f"\nAnalytics Reports: {len(analytics_reports)}")
    for r in analytics_reports:
        print(f"  {r['name']}")
    
    print(f"\nHL7 Billing Message Segments:")
    for t in hl7_segments:
        print(f"  {t['title']}: {t['row_count']} field definitions")
    
    print(f"\nExport Mechanisms: {len(inventory['export_mechanisms'])}")
    for m in inventory["export_mechanisms"]:
        print(f"  {m['name']} ({m['format']}): {m['scope']}")
    
    print("\n=== Files written ===")
    print(f"  {OUTPUT_DIR / 'full-entity-inventory.json'}")
    print(f"  {OUTPUT_DIR / 'summary-stats.json'}")


if __name__ == "__main__":
    main()
