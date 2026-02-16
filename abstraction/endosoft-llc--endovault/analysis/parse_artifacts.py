#!/usr/bin/env python3
"""Parse all EndoVault EHI export artifacts and produce structured inventory."""

import json
import re
import subprocess
import os

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/endosoft-llc--endovault/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/endosoft-llc--endovault/analysis"

def parse_ephi_page():
    """Extract the data sections listed on the ePHI export page."""
    import html as html_mod
    with open(os.path.join(DOWNLOADS, "ephi-page.html"), "r") as f:
        content = f.read()
    
    # Remove style/script tags
    text = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html_mod.unescape(text)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Find sections listed on the page
    sections = []
    known_sections = [
        "Allergies", "Encounter", "Immunizations", "Medications",
        "Plan of treatment", "Referral reason", "Active problems",
        "Reason for visit", "Implants", "Health concerns", "Procedures",
        "Functional status", "Results", "Social history", "Vitals",
        "Goals", "Discharge instructions", "Assessments",
        "Cognitive status", "Media", "Diagnostic Report", "Documents",
        "Service Request"
    ]
    
    for line in lines:
        if line in known_sections:
            sections.append(line)
    
    return {
        "source": "ephi-page.html",
        "export_methods": [
            {
                "name": "Single/multi patient export",
                "format": "C-CDA 2.1 (XML)",
                "files": ["*.xml (discrete data elements)", "CDA.xsl (stylesheet)"]
            },
            {
                "name": "Bulk EHI export",
                "format": "FHIR NDJSON",
                "mechanism": "FHIR API bulk endpoints"
            }
        ],
        "data_sections": sections,
        "section_count": len(sections)
    }


def parse_fhir_pdf():
    """Parse the FHIR API PDF to extract resource types and their details."""
    result = subprocess.run(
        ["pdftotext", "-layout", os.path.join(DOWNLOADS, "170.315-g10-Standardized-API-FHIR-2.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    lines = text.split('\n')
    
    # Extract individual API resources from Table 4-1
    api_resources = []
    in_table = False
    for line in lines:
        if "REST Resource" in line and "Description" in line:
            in_table = True
            continue
        if in_table:
            if "Table 4-1" in line:
                break
            # Parse table rows like: /Patient     Return the patient information...
            match = re.match(r'\s+(/\w+)\s+(.*)', line)
            if match:
                resource = match.group(1).strip()
                desc = match.group(2).strip()
                api_resources.append({"resource": resource, "description": desc})
    
    # Extract bulk data resources
    bulk_resources = []
    bulk_section = text[text.find("Bulk Data Access"):]
    ndjson_pattern = re.compile(r'/bulk/(\w+)-bulkfile\.ndjson')
    for match in ndjson_pattern.finditer(bulk_section):
        resource_name = match.group(1)
        bulk_resources.append(resource_name)
    # Deduplicate preserving order
    seen = set()
    unique_bulk = []
    for r in bulk_resources:
        if r not in seen:
            seen.add(r)
            unique_bulk.append(r)
    bulk_resources = unique_bulk
    
    # Extract sample JSON responses from bulk section
    bulk_samples = {}
    for resource in bulk_resources:
        pattern = rf'{resource}-bulkfile\.ndjson'
        idx = bulk_section.find(pattern)
        if idx != -1:
            # Find the Response block after this
            response_area = bulk_section[idx:idx+3000]
            # Try to extract JSON from the response area
            json_match = re.search(r'\{"resourceType":"(\w+)"', response_area)
            if json_match:
                bulk_samples[resource] = json_match.group(1)
    
    # Count pages for individual resource documentation
    # Parse the TOC for page ranges
    toc_entries = []
    for line in lines:
        toc_match = re.match(r'\s+(\w[\w\s/]+?)\s*\.{3,}\s*(\d+)', line)
        if toc_match:
            name = toc_match.group(1).strip()
            page = int(toc_match.group(2))
            toc_entries.append({"name": name, "page": page})
    
    # Extract individual resource details from the main API section
    individual_resources = []
    resource_names = [
        "Patient", "Practitioner", "RelatedPerson", "Organization",
        "Encounter", "AllergyIntolerance", "Condition", "Procedure",
        "DiagnosticReport", "Observation", "MedicationRequest",
        "Immunization", "CarePlan", "CareTeam", "Goal", "ServiceRequest",
        "DocumentReference", "Device"
    ]
    
    for rname in resource_names:
        # Count search parameters
        search_params = []
        # Find the section for this resource
        section_pattern = rf'(?:^|\n)\s*{rname}\s*\n'
        section_match = re.search(section_pattern, text)
        if section_match:
            section_start = section_match.start()
            # Find next resource section
            next_section = len(text)
            for other in resource_names:
                if other != rname:
                    other_pattern = rf'(?:^|\n)\s*{other}\s*\n'
                    other_match = re.search(other_pattern, text[section_start+100:])
                    if other_match:
                        candidate = section_start + 100 + other_match.start()
                        if candidate < next_section and candidate > section_start:
                            next_section = candidate
            
            section_text = text[section_start:next_section]
            # Count search parameters
            param_matches = re.findall(r'search by (\w+)', section_text, re.IGNORECASE)
            search_params = list(set(param_matches))
        
        individual_resources.append({
            "name": rname,
            "search_parameters": search_params,
            "has_sample_response": True  # All resources have sample JSON in the PDF
        })
    
    return {
        "source": "170.315-g10-Standardized-API-FHIR-2.pdf",
        "pages": 138,
        "date": "2022-11-25",
        "title": "API Definition",
        "toc_entries": toc_entries,
        "individual_api_resources": individual_resources,
        "individual_resource_count": len(individual_resources),
        "bulk_resources": bulk_resources,
        "bulk_resource_count": len(bulk_resources),
        "bulk_resource_types": bulk_samples,
        "api_resource_table": api_resources,
        "api_resource_table_count": len(api_resources)
    }


def parse_xlsx_disclosure():
    """Parse the cost disclosure XLSX."""
    try:
        import openpyxl
    except ImportError:
        return {"error": "openpyxl not installed", "source": "endovault_ehr_disclosure_onc_2015-10_15_25.xlsx"}
    
    wb = openpyxl.load_workbook(
        os.path.join(DOWNLOADS, "endovault_ehr_disclosure_onc_2015-10_15_25.xlsx"),
        data_only=True
    )
    
    result = {
        "source": "endovault_ehr_disclosure_onc_2015-10_15_25.xlsx",
        "sheets": [],
        "ehi_related_entries": []
    }
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = []
        for row in ws.iter_rows(values_only=True):
            row_data = [str(cell) if cell is not None else "" for cell in row]
            if any(cell.strip() for cell in row_data):
                rows.append(row_data)
        
        result["sheets"].append({
            "name": sheet_name,
            "row_count": len(rows),
            "column_count": ws.max_column,
            "headers": rows[0] if rows else [],
            "sample_rows": rows[1:6] if len(rows) > 1 else []
        })
        
        # Find EHI-related entries
        for row in rows:
            row_text = " ".join(row).lower()
            if "ehi" in row_text or "b)(10" in row_text or "export" in row_text or "ephi" in row_text:
                result["ehi_related_entries"].append(row)
    
    return result


def build_full_inventory():
    """Build the complete entity inventory from FHIR resources."""
    result = subprocess.run(
        ["pdftotext", "-layout", os.path.join(DOWNLOADS, "170.315-g10-Standardized-API-FHIR-2.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout
    
    # For each FHIR resource, extract the sample JSON and parse its fields
    resources = []
    
    # The bulk data section has sample NDJSON responses. Extract them.
    bulk_section = text[text.find("Bulk Data Access"):]
    
    resource_configs = [
        ("AllergyIntolerance", "Clinical"),
        ("CarePlan", "Clinical"),
        ("CareTeam", "Clinical"),
        ("Condition", "Clinical"),
        ("Device", "Clinical"),
        ("DiagnosticReport", "Clinical"),
        ("DocumentReference", "Clinical"),
        ("Encounter", "Management"),
        ("Goal", "Clinical"),
        ("Immunization", "Clinical"),
        ("MedicationRequest", "Clinical"),
        ("Observation", "Clinical"),
        ("Organization", "Entities"),
        ("Practitioner", "Individual"),
        ("Procedure", "Clinical"),
        ("Provenance", "Security"),
        ("RelatedPerson", "Individual"),
        ("ServiceRequest", "Clinical"),
    ]
    
    # Also extract Patient from individual API section
    resource_configs.insert(0, ("Patient", "Individual"))
    
    for resource_name, category in resource_configs:
        # Try to extract fields from sample JSON in the PDF
        # Find sample JSON for this resource
        pattern = rf'"resourceType"\s*:\s*"{resource_name}"'
        matches = list(re.finditer(pattern, text))
        
        fields = set()
        if matches:
            # Get the first sample response area
            for match in matches[:2]:
                start = match.start()
                # Go back to find the opening brace
                brace_start = text.rfind('{', max(0, start-10), start+1)
                if brace_start == -1:
                    continue
                # Find matching closing brace (rough extraction)
                depth = 0
                pos = brace_start
                while pos < len(text) and pos < brace_start + 5000:
                    if text[pos] == '{':
                        depth += 1
                    elif text[pos] == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    pos += 1
                
                json_str = text[brace_start:pos+1]
                # Clean up the JSON string for parsing
                json_str = json_str.replace('\n', ' ')
                json_str = re.sub(r'\s+', ' ', json_str)
                
                try:
                    obj = json.loads(json_str)
                    fields.update(extract_field_paths(obj))
                except json.JSONDecodeError:
                    # Try to extract field names with regex
                    field_matches = re.findall(r'"(\w+)"\s*:', json_str)
                    fields.update(field_matches)
        
        # Extract search parameters from individual API section
        search_params = []
        individual_section = text[:text.find("Bulk Data Access")]
        resource_section_match = re.search(rf'\b{resource_name}\b\s*\n\s*HTTP verb', individual_section)
        if resource_section_match:
            section_start = resource_section_match.start()
            # Find next resource section
            remaining = individual_section[section_start+50:]
            next_resource = re.search(r'\n\s*\w+\s*\n\s*HTTP verb', remaining)
            if next_resource:
                section_end = section_start + 50 + next_resource.start()
            else:
                section_end = len(individual_section)
            section_text = individual_section[section_start:section_end]
            
            # Extract search parameters
            param_matches = re.findall(r'(?:search\s+by|Search\s+by)\s+(\w+)', section_text)
            search_params = list(set(param_matches))
            
            # Also try to extract field definitions from sample responses in individual section
            ind_json_matches = re.finditer(r'\{"resourceType"\s*:\s*"' + resource_name + '"', section_text)
            for jm in ind_json_matches:
                jstart = jm.start()
                depth = 0
                pos = jstart
                while pos < len(section_text) and pos < jstart + 5000:
                    if section_text[pos] == '{':
                        depth += 1
                    elif section_text[pos] == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    pos += 1
                json_str = section_text[jstart:pos+1].replace('\n', ' ')
                json_str = re.sub(r'\s+', ' ', json_str)
                try:
                    obj = json.loads(json_str)
                    fields.update(extract_field_paths(obj))
                except json.JSONDecodeError:
                    pass
        
        resources.append({
            "name": resource_name,
            "category": category,
            "fields": sorted(list(fields)),
            "field_count": len(fields),
            "search_parameters": search_params,
            "has_bulk_endpoint": resource_name != "Patient",  # Patient only in individual API
            "has_individual_endpoint": True,
            "description": get_resource_description(resource_name),
            "fhir_profile": f"http://hl7.org/fhir/us/core/StructureDefinition/us-core-{resource_name.lower()}"
        })
    
    return resources


def extract_field_paths(obj, prefix=""):
    """Recursively extract field paths from a JSON object."""
    fields = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            fields.add(path)
            if isinstance(value, dict):
                fields.update(extract_field_paths(value, path))
            elif isinstance(value, list) and value:
                if isinstance(value[0], dict):
                    fields.update(extract_field_paths(value[0], path))
    return fields


def get_resource_description(name):
    """Get a brief description for each FHIR resource type."""
    descriptions = {
        "Patient": "Demographics and administrative information about a patient",
        "AllergyIntolerance": "Allergy and intolerance information",
        "CarePlan": "Care plans including treatment plans",
        "CareTeam": "Care team members and their roles",
        "Condition": "Diagnoses, problems, and health concerns",
        "Device": "Implantable devices",
        "DiagnosticReport": "Diagnostic reports including lab and imaging results",
        "DocumentReference": "Clinical documents and notes",
        "Encounter": "Healthcare encounters/visits",
        "Goal": "Patient care goals",
        "Immunization": "Immunization records",
        "MedicationRequest": "Medication orders and prescriptions",
        "Observation": "Clinical observations including vitals, labs, social history",
        "Organization": "Healthcare organizations",
        "Practitioner": "Healthcare practitioners",
        "Procedure": "Clinical procedures performed",
        "Provenance": "Data provenance and audit trail",
        "RelatedPerson": "Related persons (next of kin, emergency contacts)",
        "ServiceRequest": "Service requests and orders",
    }
    return descriptions.get(name, "")


def main():
    print("Parsing ePHI export page...")
    ephi_data = parse_ephi_page()
    
    print("Parsing FHIR API PDF...")
    fhir_data = parse_fhir_pdf()
    
    print("Parsing cost disclosure XLSX...")
    xlsx_data = parse_xlsx_disclosure()
    
    print("Building full entity inventory...")
    inventory = build_full_inventory()
    
    # Save all results
    full_output = {
        "ephi_page": ephi_data,
        "fhir_api_pdf": fhir_data,
        "cost_disclosure": xlsx_data,
        "entity_inventory": inventory,
        "summary": {
            "total_fhir_resources": len(inventory),
            "total_fields_extracted": sum(r["field_count"] for r in inventory),
            "resources_with_bulk_endpoint": sum(1 for r in inventory if r["has_bulk_endpoint"]),
            "resources_with_individual_endpoint": sum(1 for r in inventory if r["has_individual_endpoint"]),
            "ccda_sections": ephi_data["section_count"],
            "categories": {}
        }
    }
    
    # Category breakdown
    for r in inventory:
        cat = r["category"]
        if cat not in full_output["summary"]["categories"]:
            full_output["summary"]["categories"][cat] = {"count": 0, "fields": 0}
        full_output["summary"]["categories"][cat]["count"] += 1
        full_output["summary"]["categories"][cat]["fields"] += r["field_count"]
    
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(full_output, f, indent=2)
    
    print(f"\nSaved full inventory to {OUTPUT_DIR}/full-entity-inventory.json")
    print(f"\nSummary:")
    print(f"  FHIR resource types: {len(inventory)}")
    print(f"  Total fields extracted from samples: {sum(r['field_count'] for r in inventory)}")
    print(f"  Resources with bulk endpoint: {sum(1 for r in inventory if r['has_bulk_endpoint'])}")
    print(f"  C-CDA sections listed: {ephi_data['section_count']}")
    print(f"  Cost disclosure sheets: {len(xlsx_data.get('sheets', []))}")
    
    for r in inventory:
        print(f"  {r['name']:25s} {r['field_count']:3d} fields  ({r['category']})")


if __name__ == "__main__":
    main()
