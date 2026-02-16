#!/usr/bin/env python3
"""
Parse all TriMed Complete EHI export artifacts and produce:
- entity-inventory-full.json: complete entity/field inventory
- entity-inventory-summary.json: summary statistics
"""

import json
import os
import re
from html.parser import HTMLParser
from collections import defaultdict, OrderedDict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE, "downloads")

# ============================================================
# 1. Parse FHIR Capability Statement resources
# ============================================================
def parse_fhir_capability_statement():
    with open(os.path.join(DOWNLOADS, "fhir-capability-statement.json")) as f:
        cs = json.load(f)
    
    resources = []
    for r in cs.get("rest", [{}])[0].get("resource", []):
        resource = {
            "type": r["type"],
            "interactions": [i["code"] for i in r.get("interaction", [])],
            "searchParams": [],
            "profiles": r.get("supportedProfile", []),
        }
        for sp in r.get("searchParam", []):
            resource["searchParams"].append({
                "name": sp.get("name"),
                "type": sp.get("type"),
                "definition": sp.get("definition"),
            })
        resources.append(resource)
    
    return {
        "fhirVersion": cs.get("fhirVersion"),
        "instantiates": cs.get("instantiates", []),
        "resourceCount": len(resources),
        "resources": resources,
    }


# ============================================================
# 2. Parse FHIR PDF for resource types documented
# ============================================================
def parse_fhir_pdf():
    """Extract resource types from the FHIR Documentation PDF."""
    import subprocess
    result = subprocess.run(
        ["pdftotext", "-layout", os.path.join(DOWNLOADS, "FHIR-Documentation.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # Find numbered sections like "1.AllergyIntolerance"
    resource_pattern = re.compile(r'^(\d+)\.\s*(\w+)', re.MULTILINE)
    resources = []
    for m in resource_pattern.finditer(text):
        num = m.group(1)
        name = m.group(2)
        # Filter out false positives (hl7.org lines)
        if name[0].isupper() and not name.startswith("org"):
            resources.append({"number": int(num), "resourceType": name})
    
    # Deduplicate
    seen = set()
    unique = []
    for r in resources:
        if r["resourceType"] not in seen:
            seen.add(r["resourceType"])
            unique.append(r)
    
    return {
        "source": "FHIR-Documentation.pdf",
        "resourceCount": len(unique),
        "resources": unique,
    }


# ============================================================
# 3. Parse Swagger/OpenAPI spec
# ============================================================
def parse_swagger():
    with open(os.path.join(DOWNLOADS, "swagger-api-spec.json")) as f:
        spec = json.load(f)
    
    paths = spec.get("paths", {})
    
    # Group paths by resource type
    resource_paths = defaultdict(list)
    for path in sorted(paths.keys()):
        parts = path.strip("/").split("/")
        if parts:
            resource_paths[parts[0]].append({
                "path": path,
                "methods": list(paths[path].keys()),
            })
    
    # Identify clinical vs infrastructure paths
    clinical_resources = []
    infrastructure_paths = []
    for resource, ps in sorted(resource_paths.items()):
        if resource[0].isupper() and resource not in (
            "RenewSinglePatientRegister", "RevokeSinglePatientRegister",
            "SinglePatientRegister", "VerifyPatientRegistration"
        ):
            clinical_resources.append({
                "resourceType": resource,
                "pathCount": len(ps),
                "paths": ps,
            })
        else:
            infrastructure_paths.append({
                "name": resource,
                "pathCount": len(ps),
            })
    
    return {
        "source": "swagger-api-spec.json",
        "totalPaths": len(paths),
        "clinicalResourceCount": len(clinical_resources),
        "clinicalResources": clinical_resources,
        "infrastructurePathCount": len(infrastructure_paths),
    }


# ============================================================
# 4. Parse Patient API HTML for methods, params, SQL
# ============================================================
class PatientAPIParser(HTMLParser):
    """Parse the Patient API HTML page to extract methods, parameters, and SQL."""
    
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_row = []
        self.current_cell = ""
        self.tables = []
        self.current_table = []
        self.all_text = []
        self.skip_tags = set()
        self.tag_stack = []
        
    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag == "table":
            self.in_table = True
            self.current_table = []
        elif tag == "tr":
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = ""
        elif tag in ("script", "style"):
            self.skip_tags.add(tag)
    
    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag in ("script", "style"):
            self.skip_tags.discard(tag)
        elif tag in ("td", "th"):
            self.in_cell = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "tr":
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
        elif tag == "table":
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)
    
    def handle_data(self, data):
        if self.skip_tags:
            return
        if self.in_cell:
            self.current_cell += data
        self.all_text.append(data)


def parse_patient_api():
    with open(os.path.join(DOWNLOADS, "patientapi-homepage.html"), encoding="utf-8") as f:
        html = f.read()
    
    parser = PatientAPIParser()
    parser.feed(html)
    
    full_text = "".join(parser.all_text)
    
    # Extract method names from the HTML
    method_pattern = re.compile(r'(LookupPatientId|GetPatient\w+)')
    methods_found = sorted(set(method_pattern.findall(full_text)))
    
    # Extract SQL queries from hidden sections
    sql_pattern = re.compile(r'(SELECT\s+.+?(?:FROM|from).+?)(?:\n\s*\n|$)', re.DOTALL | re.IGNORECASE)
    sql_queries = []
    for m in sql_pattern.finditer(full_text):
        sql_text = m.group(1).strip()
        if len(sql_text) > 20:
            sql_queries.append(sql_text[:500])
    
    # Parse tables for parameter info
    param_tables = []
    for table in parser.tables:
        if len(table) > 1:
            headers = [h.lower().strip() for h in table[0]]
            if any(h in ("parameter", "name", "param") for h in headers):
                rows = []
                for row in table[1:]:
                    if len(row) >= len(headers):
                        rows.append(dict(zip(headers, row)))
                    elif row:
                        padded = row + [""] * (len(headers) - len(row))
                        rows.append(dict(zip(headers, padded)))
                param_tables.append({
                    "headers": headers,
                    "rowCount": len(rows),
                    "rows": rows,
                })
    
    return {
        "source": "patientapi-homepage.html",
        "apiVersion": "1.3",
        "format": "SOAP/XML returning C-CDA",
        "methodCount": len(methods_found),
        "methods": methods_found,
        "parameterTableCount": len(param_tables),
        "parameterTables": param_tables,
        "sqlQueryCount": len(sql_queries),
    }


# ============================================================
# 5. Parse C-CDA sample XML files
# ============================================================
def parse_ccda_samples():
    import xml.etree.ElementTree as ET
    
    xml_dir = os.path.join(DOWNLOADS, "xml-samples")
    samples = []
    
    for fname in sorted(os.listdir(xml_dir)):
        if not fname.endswith(".xml"):
            continue
        
        fpath = os.path.join(xml_dir, fname)
        size = os.path.getsize(fpath)
        
        try:
            tree = ET.parse(fpath)
            root = tree.getroot()
            
            # Handle CDA namespace
            ns = {"cda": "urn:hl7-org:v3"}
            
            # Find all sections
            sections = []
            for section in root.findall(".//{urn:hl7-org:v3}section"):
                title_elem = section.find("{urn:hl7-org:v3}title")
                code_elem = section.find("{urn:hl7-org:v3}code")
                
                title = title_elem.text if title_elem is not None else "Unknown"
                code = code_elem.get("code") if code_elem is not None else None
                display = code_elem.get("displayName") if code_elem is not None else None
                
                # Count entries
                entries = section.findall("{urn:hl7-org:v3}entry")
                
                sections.append({
                    "title": title,
                    "code": code,
                    "displayName": display,
                    "entryCount": len(entries),
                })
            
            samples.append({
                "filename": fname,
                "sizeBytes": size,
                "sectionCount": len(sections),
                "sections": sections,
            })
        except ET.ParseError as e:
            samples.append({
                "filename": fname,
                "sizeBytes": size,
                "parseError": str(e),
            })
    
    return {
        "source": "xml-samples/",
        "fileCount": len(samples),
        "samples": samples,
    }


# ============================================================
# 6. Parse WSDL for method definitions
# ============================================================
def parse_wsdl():
    import xml.etree.ElementTree as ET
    
    fpath = os.path.join(DOWNLOADS, "PatientAPI-WSDL.xml")
    tree = ET.parse(fpath)
    root = tree.getroot()
    
    # WSDL namespaces
    wsdl_ns = "http://schemas.xmlsoap.org/wsdl/"
    xsd_ns = "http://www.w3.org/2001/XMLSchema"
    
    # Find all operations
    operations = []
    for portType in root.findall(f".//{{{wsdl_ns}}}portType"):
        for op in portType.findall(f"{{{wsdl_ns}}}operation"):
            operations.append(op.get("name"))
    
    # Find all complex types (data structures)
    complex_types = []
    for ct in root.findall(f".//{{{xsd_ns}}}complexType"):
        name = ct.get("name", "anonymous")
        elements = []
        for elem in ct.findall(f".//{{{xsd_ns}}}element"):
            elements.append({
                "name": elem.get("name"),
                "type": elem.get("type"),
                "minOccurs": elem.get("minOccurs"),
                "maxOccurs": elem.get("maxOccurs"),
            })
        if elements:
            complex_types.append({
                "name": name,
                "elementCount": len(elements),
                "elements": elements,
            })
    
    return {
        "source": "PatientAPI-WSDL.xml",
        "operationCount": len(operations),
        "operations": operations,
        "complexTypeCount": len(complex_types),
        "complexTypes": complex_types,
    }


# ============================================================
# 7. Parse database schema from enrichment (verify/extend)
# ============================================================
def parse_database_schema():
    fpath = os.path.join(DOWNLOADS, "enrichment", "database-schema-from-sql.json")
    with open(fpath) as f:
        schema = json.load(f)
    
    tables = schema.get("tables", {})
    total_columns = sum(len(t.get("columns", [])) for t in tables.values())
    
    return {
        "source": "enrichment/database-schema-from-sql.json (from hidden SQL in Patient API docs)",
        "databaseType": schema.get("databaseType", "Oracle"),
        "tableCount": len(tables),
        "totalColumns": total_columns,
        "tables": tables,
    }


# ============================================================
# 8. Build unified entity inventory
# ============================================================
def build_entity_inventory(fhir_cs, fhir_pdf, swagger, patient_api, ccda, wsdl, db_schema):
    """Build a comprehensive entity inventory combining all sources."""
    
    entities = []
    
    # --- FHIR Resources (from Capability Statement) ---
    for r in fhir_cs["resources"]:
        fields = []
        for sp in r.get("searchParams", []):
            fields.append({
                "name": sp["name"],
                "type": sp.get("type", ""),
                "description": f"Search parameter: {sp.get('definition', '')}",
                "source": "FHIR CapabilityStatement searchParam",
            })
        
        entities.append({
            "name": f"FHIR:{r['type']}",
            "category": "FHIR API (g)(10)",
            "description": f"FHIR R4 {r['type']} resource (US Core profile)",
            "fieldCount": len(fields),
            "fields": fields,
            "interactions": r.get("interactions", []),
            "profiles": r.get("profiles", []),
            "source": "fhir-capability-statement.json",
        })
    
    # --- SOAP API Methods (from Patient API) ---
    # Use the enrichment data for detailed method info
    enrichment_path = os.path.join(DOWNLOADS, "enrichment", "patient-api-methods.json")
    if os.path.exists(enrichment_path):
        with open(enrichment_path) as f:
            enrichment = json.load(f)
        
        if isinstance(enrichment, dict):
            methods = enrichment.get("methods", [])
        else:
            methods = enrichment
        
        for method in methods:
            if isinstance(method, str):
                continue
            method_name = method.get("name", "Unknown")
            
            fields = []
            for p in method.get("requestParams", []):
                fields.append({
                    "name": p.get("name", ""),
                    "type": p.get("type", ""),
                    "description": p.get("description", ""),
                    "required": p.get("required", ""),
                    "direction": "request",
                    "source": "Patient API documentation",
                })
            for p in method.get("responseParams", []):
                fields.append({
                    "name": p.get("name", "") if isinstance(p, dict) else str(p),
                    "type": p.get("type", "") if isinstance(p, dict) else "",
                    "description": p.get("description", "") if isinstance(p, dict) else "",
                    "direction": "response",
                    "source": "Patient API documentation",
                })
            
            entities.append({
                "name": f"SOAP:{method_name}",
                "category": "SOAP Patient Data API",
                "description": f"SOAP API method returning C-CDA data",
                "fieldCount": len(fields),
                "fields": fields,
                "source": "patientapi-homepage.html",
            })
    
    # --- C-CDA Sections (from sample XML) ---
    # Get sections from the comprehensive GetPatientData sample
    for sample in ccda["samples"]:
        if sample["filename"] == "GetPatientData.xml" and "sections" in sample:
            for section in sample["sections"]:
                entities.append({
                    "name": f"CCDA:{section.get('title', 'Unknown')}",
                    "category": "C-CDA Section",
                    "description": f"C-CDA section: {section.get('displayName', section.get('title', ''))}",
                    "code": section.get("code"),
                    "entryCount": section.get("entryCount", 0),
                    "fieldCount": 0,  # C-CDA sections don't have vendor-defined fields
                    "fields": [],
                    "source": "xml-samples/GetPatientData.xml",
                })
    
    # --- Database Tables (from hidden SQL) ---
    for table_name, table_info in db_schema["tables"].items():
        fields = []
        for col in table_info.get("columns", []):
            fields.append({
                "name": col,
                "type": "",
                "description": "",
                "source": "Hidden SQL queries in Patient API docs",
            })
        
        entities.append({
            "name": f"DB:{table_name}",
            "category": "Oracle Database (internal)",
            "description": table_info.get("description", ""),
            "usedBy": table_info.get("usedBy", ""),
            "fieldCount": len(fields),
            "fields": fields,
            "source": "database-schema-from-sql.json",
        })
    
    return entities


# ============================================================
# 9. Build summary statistics
# ============================================================
def build_summary(entities, fhir_cs, swagger, patient_api, ccda, wsdl, db_schema):
    """Build summary statistics from the entity inventory."""
    
    # Count by category
    by_category = defaultdict(lambda: {"entityCount": 0, "fieldCount": 0, "fieldsWithDescription": 0})
    
    for entity in entities:
        cat = entity.get("category", "Unknown")
        by_category[cat]["entityCount"] += 1
        by_category[cat]["fieldCount"] += entity.get("fieldCount", 0)
        for field in entity.get("fields", []):
            desc = field.get("description", "")
            if desc and desc.strip() and not desc.startswith("Search parameter:"):
                by_category[cat]["fieldsWithDescription"] += 1
    
    total_entities = len(entities)
    total_fields = sum(e.get("fieldCount", 0) for e in entities)
    total_with_desc = sum(
        1 for e in entities
        for f in e.get("fields", [])
        if f.get("description", "").strip() and not f["description"].startswith("Search parameter:")
    )
    
    # C-CDA section coverage
    ccda_sections = []
    for sample in ccda["samples"]:
        if sample["filename"] == "GetPatientData.xml" and "sections" in sample:
            ccda_sections = [s["title"] for s in sample["sections"]]
    
    # FHIR resource types
    fhir_types = [r["type"] for r in fhir_cs["resources"]]
    
    # SOAP methods
    soap_methods = patient_api.get("methods", [])
    
    # WSDL operations
    wsdl_ops = wsdl.get("operations", [])
    
    return {
        "totalEntities": total_entities,
        "totalFields": total_fields,
        "fieldsWithDescription": total_with_desc,
        "descriptionPercent": round(total_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
        "byCategory": dict(by_category),
        "fhirResourceTypes": fhir_types,
        "fhirResourceCount": len(fhir_types),
        "soapMethods": soap_methods,
        "soapMethodCount": len(soap_methods),
        "ccdaSections": ccda_sections,
        "ccdaSectionCount": len(ccda_sections),
        "wsdlOperations": wsdl_ops,
        "wsdlOperationCount": len(wsdl_ops),
        "databaseTables": list(db_schema["tables"].keys()),
        "databaseTableCount": db_schema["tableCount"],
        "databaseColumnCount": db_schema["totalColumns"],
        "swaggerPathCount": swagger["totalPaths"],
        "swaggerClinicalResourceCount": swagger["clinicalResourceCount"],
    }


# ============================================================
# Main
# ============================================================
def main():
    print("Parsing FHIR Capability Statement...")
    fhir_cs = parse_fhir_capability_statement()
    
    print("Parsing FHIR Documentation PDF...")
    fhir_pdf = parse_fhir_pdf()
    
    print("Parsing Swagger/OpenAPI spec...")
    swagger = parse_swagger()
    
    print("Parsing Patient Data API HTML...")
    patient_api = parse_patient_api()
    
    print("Parsing C-CDA sample XML files...")
    ccda = parse_ccda_samples()
    
    print("Parsing WSDL...")
    wsdl = parse_wsdl()
    
    print("Parsing database schema...")
    db_schema = parse_database_schema()
    
    print("Building entity inventory...")
    entities = build_entity_inventory(fhir_cs, fhir_pdf, swagger, patient_api, ccda, wsdl, db_schema)
    
    print("Building summary...")
    summary = build_summary(entities, fhir_cs, swagger, patient_api, ccda, wsdl, db_schema)
    
    # Write outputs
    out_dir = os.path.dirname(os.path.abspath(__file__))
    
    full_path = os.path.join(out_dir, "entity-inventory-full.json")
    with open(full_path, "w") as f:
        json.dump(entities, f, indent=2)
    print(f"Wrote {len(entities)} entities to {full_path}")
    
    summary_path = os.path.join(out_dir, "entity-inventory-summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote summary to {summary_path}")
    
    # Also write intermediate parsed artifacts
    artifacts = {
        "fhir_capability_statement": fhir_cs,
        "fhir_pdf": fhir_pdf,
        "swagger": swagger,
        "patient_api": patient_api,
        "ccda_samples": ccda,
        "wsdl": wsdl,
        "database_schema": db_schema,
    }
    
    artifacts_path = os.path.join(out_dir, "parsed-artifacts.json")
    with open(artifacts_path, "w") as f:
        json.dump(artifacts, f, indent=2)
    print(f"Wrote parsed artifacts to {artifacts_path}")
    
    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Total entities: {summary['totalEntities']}")
    print(f"Total fields: {summary['totalFields']}")
    print(f"Fields with descriptions: {summary['fieldsWithDescription']} ({summary['descriptionPercent']}%)")
    print(f"\nBy category:")
    for cat, stats in sorted(summary["byCategory"].items()):
        print(f"  {cat}: {stats['entityCount']} entities, {stats['fieldCount']} fields, {stats['fieldsWithDescription']} described")
    print(f"\nFHIR resources: {summary['fhirResourceCount']}")
    print(f"SOAP methods: {summary['soapMethodCount']}")
    print(f"C-CDA sections (GetPatientData): {summary['ccdaSectionCount']}")
    print(f"Database tables (from SQL): {summary['databaseTableCount']} ({summary['databaseColumnCount']} columns)")
    print(f"Swagger paths: {summary['swaggerPathCount']}")


if __name__ == "__main__":
    main()
