#!/usr/bin/env python3
"""Parse all HTML artifacts from CHN Tech Solutions and extract structured data.

Extracts:
- EHI export page content
- CCD sections documented
- FHIR API scopes and endpoints
- REST API scopes (OpenEMR native)
- FHIR resource types supported
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent.parent.parent / "results" / "chn-tech-solutions-llc--integrated-care-ehr" / "downloads"
OUTPUT = Path(__file__).parent


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.text.append(t)


def extract_text(filepath):
    e = TextExtractor()
    with open(filepath) as f:
        e.feed(f.read())
    return e.text


def parse_scopes(text_lines):
    """Extract OAuth2 scopes from the REST API page."""
    fhir_scopes = []
    oemr_scopes = []
    portal_scopes = []
    current_api = None

    for line in text_lines:
        if "api:fhir" in line and "endpoints" in line:
            current_api = "fhir"
            continue
        elif "api:oemr" in line and "endpoints" in line:
            current_api = "oemr"
            continue
        elif "api:port" in line and "endpoints" in line:
            current_api = "portal"
            continue
        elif line.startswith("Registration"):
            current_api = None
            continue

        if current_api == "fhir" and "/" in line and "." in line:
            scope = line.strip()
            if scope.startswith(("patient/", "system/", "user/")):
                fhir_scopes.append(scope)
        elif current_api == "oemr" and "/" in line and "." in line:
            scope = line.strip()
            if scope.startswith("user/"):
                oemr_scopes.append(scope)
        elif current_api == "portal" and "/" in line and "." in line:
            scope = line.strip()
            if scope.startswith("patient/"):
                portal_scopes.append(scope)

    return fhir_scopes, oemr_scopes, portal_scopes


def parse_ccd_sections(text_lines):
    """Extract CCD sections from the FHIR API page."""
    date_filtered = []
    full_record = []
    current = None

    for i, line in enumerate(text_lines):
        if "Start and end date filter" in line:
            current = "date_filtered"
            continue
        elif "entire medical record" in line:
            current = "full_record"
            continue
        elif "CCD is generated on demand" in line:
            current = None
            continue

        if current == "date_filtered" and line and not line.startswith(("The following", "Start and")):
            section = line.strip()
            if section and len(section) > 3 and not section.startswith(("Returns", "XSL", "Or xml", "Due to", "If no", "Dates")):
                date_filtered.append(section)
        elif current == "full_record" and line and not line.startswith("The following"):
            section = line.strip()
            if section and len(section) > 3 and "(" not in section[:2]:
                # Filter out non-section lines
                if not any(kw in section.lower() for kw in ["generated", "returns", "xsl", "xml", "browser", "start date", "end date", "dates must"]):
                    full_record.append(section)

    return date_filtered, full_record


def extract_fhir_resources(fhir_scopes):
    """Extract unique FHIR resource types from scopes."""
    resources = set()
    for scope in fhir_scopes:
        parts = scope.split("/")
        if len(parts) == 2:
            resource_part = parts[1].split(".")[0]
            if resource_part.startswith("$"):
                continue
            if resource_part != "*":
                resources.add(resource_part)
    return sorted(resources)


def extract_oemr_resources(oemr_scopes):
    """Extract unique OpenEMR native resource types."""
    resources = set()
    for scope in oemr_scopes:
        parts = scope.split("/")
        if len(parts) == 2:
            resource_part = parts[1].split(".")[0]
            resources.add(resource_part)
    return sorted(resources)


def main():
    result = {
        "vendor": "CHN Tech Solutions LLC",
        "product": "Integrated Care EHR",
        "artifacts_analyzed": [],
        "ehi_export_page": {},
        "ccd_sections": {},
        "fhir_api": {},
        "rest_api_oemr": {},
        "portal_api": {},
        "pdfs": {},
    }

    # 1. Analyze EHI export page
    ehi_text = extract_text(DOWNLOADS / "ehi-export-page.html")
    result["artifacts_analyzed"].append({
        "file": "ehi-export-page.html",
        "size_bytes": (DOWNLOADS / "ehi-export-page.html").stat().st_size,
        "description": "Main EHI export page describing (b)(10) mechanism",
        "content_summary": "States export uses C-CDA format, links to IHE Technical Framework and HL7 C-CDA IG standards"
    })
    result["ehi_export_page"] = {
        "format_declared": "C-CDA (Consolidated Clinical Document Architecture)",
        "transport_mechanism": "FHIR $docref operation",
        "key_claims": [
            "Exports patient data using C-CDA",
            "C-CDA documents represented in XML",
            "Export capabilities built upon IHE Technical Frameworks",
        ],
        "external_links": [
            "IHE Technical Framework",
            "HL7 C-CDA Implementation Guide (Vol 1 & 2)"
        ],
        "vendor_specific_documentation": False,
        "data_dictionary_present": False,
        "sample_data_present": False,
    }

    # 2. Analyze CCD Operation page
    ccd_text = extract_text(DOWNLOADS / "ccd-operation-in-fhir.html")
    result["artifacts_analyzed"].append({
        "file": "ccd-operation-in-fhir.html",
        "size_bytes": (DOWNLOADS / "ccd-operation-in-fhir.html").stat().st_size,
        "description": "Step-by-step tutorial for generating CCD via FHIR $docref",
        "content_summary": "11-step Swagger tutorial with screenshots for CCD generation"
    })

    # 3. Analyze FHIR API page
    fhir_text = extract_text(DOWNLOADS / "fhir-api-page.html")
    date_filtered, full_record = parse_ccd_sections(fhir_text)
    result["artifacts_analyzed"].append({
        "file": "fhir-api-page.html",
        "size_bytes": (DOWNLOADS / "fhir-api-page.html").stat().st_size,
        "description": "FHIR R4/US Core 3.1 API documentation",
        "content_summary": "FHIR API docs with Bulk FHIR, $docref CCD, SMART on FHIR, scope definitions"
    })
    result["ccd_sections"] = {
        "date_filterable_sections": date_filtered,
        "full_record_sections": full_record,
        "total_sections": len(date_filtered) + len(full_record),
    }

    # 4. Analyze REST API page
    rest_text = extract_text(DOWNLOADS / "rest-api-page.html")
    fhir_scopes, oemr_scopes, portal_scopes = parse_scopes(rest_text)

    result["artifacts_analyzed"].append({
        "file": "rest-api-page.html",
        "size_bytes": (DOWNLOADS / "rest-api-page.html").stat().st_size,
        "description": "OpenEMR REST API documentation with OIDC auth and scope listings",
        "content_summary": "REST API docs with FHIR + OpenEMR native scopes"
    })
    result["artifacts_analyzed"].append({
        "file": "standard-api-page.html",
        "size_bytes": (DOWNLOADS / "standard-api-page.html").stat().st_size,
        "description": "Duplicate of REST API page with minor formatting differences",
        "content_summary": "Same content as rest-api-page.html"
    })

    fhir_resources = extract_fhir_resources(fhir_scopes)
    oemr_resources = extract_oemr_resources(oemr_scopes)

    result["fhir_api"] = {
        "standard": "FHIR R4 / US Core 3.1",
        "scopes": fhir_scopes,
        "scope_count": len(fhir_scopes),
        "resource_types": fhir_resources,
        "resource_type_count": len(fhir_resources),
        "bulk_export_supported": True,
        "bulk_export_types": ["System ($export)", "Group (Group/$export)", "Patient (Patient/$export)"],
        "smart_on_fhir": True,
    }

    result["rest_api_oemr"] = {
        "description": "OpenEMR native REST API endpoints",
        "scopes": oemr_scopes,
        "scope_count": len(oemr_scopes),
        "resource_types": oemr_resources,
        "resource_type_count": len(oemr_resources),
        "note": "These scopes reveal data domains in the underlying OpenEMR system NOT covered by the C-CDA export"
    }

    result["portal_api"] = {
        "scopes": portal_scopes,
        "scope_count": len(portal_scopes),
        "status": "EXPERIMENTAL",
    }

    # 5. PDFs
    result["pdfs"] = {
        "CCDA_Vol1_2022SEP_errata.pdf": {
            "size_bytes": (DOWNLOADS / "CCDA_Vol1_2022SEP_errata.pdf").stat().st_size,
            "pages": 63,
            "description": "HL7 C-CDA IG Volume 1 - Introductory Material",
            "is_vendor_specific": False,
            "note": "Standard HL7 document, not vendor-specific"
        },
        "CCDA_Vol2_2022SEP_errata.pdf": {
            "size_bytes": (DOWNLOADS / "CCDA_Vol2_2022SEP_errata.pdf").stat().st_size,
            "pages": 913,
            "description": "HL7 C-CDA IG Volume 2 - Templates and Supporting Material",
            "is_vendor_specific": False,
            "note": "Standard HL7 document, not vendor-specific"
        }
    }

    # 6. Screenshots
    for png in ["ehi-export-page.png", "ccd-operation-in-fhir-screenshot.png"]:
        result["artifacts_analyzed"].append({
            "file": png,
            "size_bytes": (DOWNLOADS / png).stat().st_size,
            "description": f"Screenshot of {png.replace('.png','').replace('-',' ')}",
            "content_summary": "Visual reference only"
        })

    # Summary statistics
    result["summary"] = {
        "total_artifacts": len(result["artifacts_analyzed"]) + 2,  # +2 for PDFs
        "vendor_specific_artifacts": 5,  # 4 HTML pages + 1 CCD tutorial (screenshots are visual versions of same)
        "standard_documents": 2,  # C-CDA IG Vol 1 & 2
        "data_dictionary_present": False,
        "sample_data_present": False,
        "field_level_documentation": False,
        "export_format": "C-CDA XML (via FHIR $docref)",
        "ccd_sections_documented": len(date_filtered) + len(full_record),
        "fhir_resource_types": len(fhir_resources),
        "oemr_native_resource_types": len(oemr_resources),
        "oemr_native_resources_not_in_ccd": sorted(set(oemr_resources) - {
            r.lower() for r in fhir_resources
        }),
    }

    with open(OUTPUT / "full-entity-inventory.json", "w") as f:
        json.dump(result, f, indent=2)

    # Print summary
    print("=== Analysis Summary ===")
    print(f"Total artifacts: {result['summary']['total_artifacts']}")
    print(f"Vendor-specific artifacts: {result['summary']['vendor_specific_artifacts']}")
    print(f"\nExport format: {result['summary']['export_format']}")
    print(f"CCD sections documented: {result['summary']['ccd_sections_documented']}")
    print(f"  Date-filterable: {len(date_filtered)}")
    for s in date_filtered:
        print(f"    - {s}")
    print(f"  Full record: {len(full_record)}")
    for s in full_record:
        print(f"    - {s}")

    print(f"\nFHIR resource types: {result['summary']['fhir_resource_types']}")
    for r in fhir_resources:
        print(f"  - {r}")

    print(f"\nOpenEMR native API resource types: {result['summary']['oemr_native_resource_types']}")
    for r in oemr_resources:
        print(f"  - {r}")

    print(f"\nOEMR resources NOT in CCD export:")
    for r in result["summary"]["oemr_native_resources_not_in_ccd"]:
        print(f"  - {r}")

    print(f"\nData dictionary: {result['summary']['data_dictionary_present']}")
    print(f"Sample data: {result['summary']['sample_data_present']}")
    print(f"Field-level docs: {result['summary']['field_level_documentation']}")


if __name__ == "__main__":
    main()
