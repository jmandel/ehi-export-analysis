#!/usr/bin/env python3
"""
Parse all FHIR-related artifacts from Varian ARIA downloads.
Produces full-entity-inventory.json and summary statistics.
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).resolve().parent.parent.parent.parent / "results" / "varian-medical-systems--aria" / "downloads"
OUTPUT = Path(__file__).resolve().parent


class TableParser(HTMLParser):
    """Extract all HTML tables as lists of rows."""
    def __init__(self):
        super().__init__()
        self.tables = []
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.current_table = []
        self.current_row = []
        self.current_cell = []

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.in_table = True
            self.current_table = []
        elif tag == "tr" and self.in_table:
            self.in_row = True
            self.current_row = []
        elif tag in ("td", "th") and self.in_row:
            self.in_cell = True
            self.current_cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.in_cell:
            self.in_cell = False
            self.current_row.append("".join(self.current_cell).strip())
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if self.current_row:
                self.current_table.append(self.current_row)
        elif tag == "table" and self.in_table:
            self.in_table = False
            if self.current_table:
                self.tables.append(self.current_table)

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell.append(data)


def parse_fhir_html():
    """Parse FHIR API documentation HTML and extract mapping table."""
    html_path = DOWNLOADS / "fhir-api-documentation.html"
    content = html_path.read_text()

    parser = TableParser()
    parser.feed(content)

    # Table 3 (index 2) is the FHIR mapping table
    mapping_table = parser.tables[2]
    header = mapping_table[0]

    entities = []
    current_uscdi = None
    for row in mapping_table[1:]:
        if len(row) < 2:
            continue
        uscdi = row[0].strip()
        fhir_resource = row[1].strip()
        details = row[2].strip() if len(row) > 2 else ""

        # Skip JSON example rows (they start with { and are continuation data)
        if uscdi.startswith("{") or fhir_resource.startswith("{"):
            continue

        if uscdi:
            current_uscdi = uscdi
        if not fhir_resource or fhir_resource == "FHIR® Resource":
            continue

        # Parse search parameters from details
        search_params = []
        supported_interaction = ""
        if "Supported Search:" in details:
            match = re.search(r"Supported Search:\s*(.+?)(?:URL Syntax|$)", details, re.DOTALL)
            if match:
                params_str = match.group(1).strip()
                search_params = [p.strip().split()[0] for p in params_str.split(",") if p.strip()]

        if "Supported Interaction:" in details:
            match = re.search(r"Supported Interaction:\s*(\w+)", details)
            if match:
                supported_interaction = match.group(1)

        entities.append({
            "uscdi_category": current_uscdi or "",
            "fhir_resource": fhir_resource,
            "supported_interaction": supported_interaction,
            "search_parameters": search_params,
            "has_example": "Example:" in details or "example" in details.lower(),
        })

    return entities


def parse_capability_statement():
    """Parse FHIR CapabilityStatement for resource details."""
    cs_path = DOWNLOADS / "fhir-capability-statement.json"
    cs = json.loads(cs_path.read_text())

    resources = []
    for rest in cs.get("rest", []):
        for resource in rest.get("resource", []):
            res_type = resource.get("type", "")
            interactions = [i["code"] for i in resource.get("interaction", [])]
            search_params = [
                {
                    "name": sp.get("name"),
                    "type": sp.get("type"),
                    "documentation": sp.get("documentation", ""),
                }
                for sp in resource.get("searchParam", [])
            ]
            resources.append({
                "resource_type": res_type,
                "interactions": interactions,
                "search_parameters": search_params,
                "search_param_count": len(search_params),
            })

    return resources


def parse_smart_config():
    """Parse SMART configuration for scope details."""
    smart_path = DOWNLOADS / "fhir-smart-configuration.json"
    smart = json.loads(smart_path.read_text())

    scopes = smart.get("scopes_supported", [])
    resource_types = set()
    for scope in scopes:
        parts = scope.split("/")
        if len(parts) == 2:
            res = parts[1].split(".")[0]
            resource_types.add(res)

    return {
        "total_scopes": len(scopes),
        "unique_resource_types": sorted(resource_types),
        "capabilities": smart.get("capabilities", []),
        "grant_types": smart.get("grant_types_supported", []),
    }


def main():
    print("Parsing FHIR API HTML documentation...")
    fhir_mappings = parse_fhir_html()
    print(f"  Found {len(fhir_mappings)} USCDI-to-FHIR mappings")

    print("Parsing CapabilityStatement...")
    cap_resources = parse_capability_statement()
    print(f"  Found {len(cap_resources)} resource types")

    print("Parsing SMART configuration...")
    smart_info = parse_smart_config()
    print(f"  Found {smart_info['total_scopes']} scopes, {len(smart_info['unique_resource_types'])} resource types")

    # Deduplicate USCDI categories
    uscdi_categories = sorted(set(m["uscdi_category"] for m in fhir_mappings if m["uscdi_category"]))
    fhir_resources_in_mapping = sorted(set(m["fhir_resource"] for m in fhir_mappings))

    # Build full inventory
    inventory = {
        "source": "Varian ARIA CORE FHIR API Documentation",
        "documentation_type": "FHIR R4 API (g)(10) - NOT a (b)(10) EHI export data dictionary",
        "note": "No dedicated (b)(10) EHI export documentation exists. The registered URL (https://varian.com/aria/ehi) returns 404. The only data export documentation available is the FHIR API for (g)(10) USCDI access.",
        "fhir_mapping_table": {
            "total_mappings": len(fhir_mappings),
            "uscdi_categories": uscdi_categories,
            "uscdi_category_count": len(uscdi_categories),
            "fhir_resources_referenced": fhir_resources_in_mapping,
            "fhir_resource_count": len(fhir_resources_in_mapping),
            "mappings": fhir_mappings,
        },
        "capability_statement": {
            "resource_count": len(cap_resources),
            "resources": cap_resources,
            "total_search_parameters": sum(r["search_param_count"] for r in cap_resources),
        },
        "smart_configuration": smart_info,
        "critical_finding": (
            "The FHIR API documentation explicitly states: 'Available data via the API interface "
            "is limited by the data defined by the USCDI.' and 'Varian FHIR API assumes the use of "
            "a cumulative C-CDA with patient data.' This means the API is a C-CDA pass-through that "
            "re-exposes C-CDA content as FHIR resources. It does NOT query the native ARIA database. "
            "Oncology-specific data (radiation therapy plans, fraction logs, beam parameters, cancer staging, "
            "toxicity grading, DICOM images) has no representation in this API."
        ),
    }

    # Summary statistics
    summary = {
        "uscdi_categories": len(uscdi_categories),
        "fhir_resources_in_mapping": len(fhir_resources_in_mapping),
        "fhir_resources_in_capability_statement": len(cap_resources),
        "total_search_parameters": sum(r["search_param_count"] for r in cap_resources),
        "smart_scopes": smart_info["total_scopes"],
        "smart_resource_types": len(smart_info["unique_resource_types"]),
        "has_dedicated_b10_documentation": False,
        "ehi_url_status": "404 (dead)",
        "conformance_method": "Attestation",
        "relied_upon_software": "Winzip",
    }

    # Write outputs
    inventory_path = OUTPUT / "full-entity-inventory.json"
    with open(inventory_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"\nWrote inventory to {inventory_path}")

    summary_path = OUTPUT / "summary-statistics.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote summary to {summary_path}")

    # Print summary
    print("\n=== Summary ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    # Print USCDI categories
    print(f"\n=== USCDI Categories ({len(uscdi_categories)}) ===")
    for c in uscdi_categories:
        print(f"  - {c}")

    # Print CapabilityStatement resources with search param counts
    print(f"\n=== CapabilityStatement Resources ({len(cap_resources)}) ===")
    for r in sorted(cap_resources, key=lambda x: x["resource_type"]):
        print(f"  {r['resource_type']}: {r['search_param_count']} search params, interactions: {', '.join(r['interactions'])}")


if __name__ == "__main__":
    main()
