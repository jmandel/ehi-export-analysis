#!/usr/bin/env python3
"""Parse the SmartCare EHI export documentation page and extract structured data."""

import json
import re
from html.parser import HTMLParser

# Parse the WP API JSON for cleaner content
with open("../downloads/ehi-export-page-wp-api.json") as f:
    wp_data = json.load(f)

page_meta = {
    "title": wp_data.get("title", {}).get("rendered", ""),
    "published": wp_data.get("date", ""),
    "modified": wp_data.get("modified", ""),
    "slug": wp_data.get("slug", ""),
}

content_html = wp_data.get("content", {}).get("rendered", "")

# Extract all links and their text
link_pattern = re.compile(r'<a\s+[^>]*href="([^"]*)"[^>]*>(.*?)</a>', re.DOTALL)
links = []
for match in link_pattern.finditer(content_html):
    url = match.group(1)
    text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
    # Extract OID from URL
    oid_match = re.search(r'StructureDefinition-(.+?)\.html', url)
    oid = oid_match.group(1) if oid_match else None
    links.append({"text": text, "url": url, "oid": oid})

# Classify sections
ccda_sections = []
for link in links:
    if link["oid"]:
        entry_status = "unknown"
        if "entries required" in link["text"].lower():
            entry_status = "entries_required"
        elif "entries optional" in link["text"].lower():
            entry_status = "entries_optional"
        else:
            entry_status = "no_entry_constraint"
        
        section_name = re.sub(r'\s*\(entries (?:required|optional)\)', '', link["text"]).strip()
        ccda_sections.append({
            "name": section_name,
            "oid": link["oid"],
            "entry_status": entry_status,
            "spec_url": link["url"],
        })

# Extract bullet points (export process description)
bullet_pattern = re.compile(r'<li>(.*?)</li>', re.DOTALL)
bullets = [re.sub(r'<[^>]+>', '', b).strip() for b in bullet_pattern.findall(content_html)]
process_bullets = [b for b in bullets if not any(link["text"] in b for link in links)]

# Build the full inventory
# For a C-CDA export with no data dictionary, we document what the C-CDA spec defines
# for each section (standard fields per HL7 C-CDA 2.2)
ccda_section_fields = {
    "Allergies and Intolerances Section": {
        "standard_fields": ["substance", "reaction", "severity", "status", "effectiveTime", "author"],
        "maps_to_uscdi": True,
        "domain": "Allergies",
    },
    "Medications Section": {
        "standard_fields": ["medication", "dose", "route", "frequency", "effectiveTime", "status", "author"],
        "maps_to_uscdi": True,
        "domain": "Medications",
    },
    "Problem Section": {
        "standard_fields": ["condition", "code", "status", "effectiveTime", "author"],
        "maps_to_uscdi": True,
        "domain": "Problems / conditions",
    },
    "Procedures Section": {
        "standard_fields": ["procedure", "code", "status", "effectiveTime", "targetSiteCode", "performer"],
        "maps_to_uscdi": True,
        "domain": "Procedures",
    },
    "Results Section": {
        "standard_fields": ["organizer", "observation", "code", "value", "unit", "referenceRange", "effectiveTime", "status"],
        "maps_to_uscdi": True,
        "domain": "Lab results",
    },
    "Advance Directives Section": {
        "standard_fields": ["directive", "code", "effectiveTime", "author"],
        "maps_to_uscdi": False,
        "domain": "Consents / directives",
    },
    "Encounters Section": {
        "standard_fields": ["encounter", "code", "effectiveTime", "performer", "location"],
        "maps_to_uscdi": True,
        "domain": "Encounters",
    },
    "Family History Section": {
        "standard_fields": ["relative", "relationship", "condition", "age", "deceased"],
        "maps_to_uscdi": True,
        "domain": "Family history",
    },
    "Functional Status Section": {
        "standard_fields": ["observation", "code", "value", "effectiveTime"],
        "maps_to_uscdi": True,
        "domain": "Health status assessments",
    },
    "Immunizations Section": {
        "standard_fields": ["vaccine", "date", "route", "dose", "manufacturer", "lotNumber", "status"],
        "maps_to_uscdi": True,
        "domain": "Immunizations",
    },
    "Medical Equipment Section": {
        "standard_fields": ["device", "code", "effectiveTime", "quantity"],
        "maps_to_uscdi": True,
        "domain": "Medical devices",
    },
    "Payers Section": {
        "standard_fields": ["payer", "coverageType", "memberId", "effectiveTime", "performer"],
        "maps_to_uscdi": True,
        "domain": "Insurance / coverage",
    },
    "Plan of Treatment Section": {
        "standard_fields": ["plannedAct", "code", "effectiveTime", "author"],
        "maps_to_uscdi": True,
        "domain": "Care plans / goals",
    },
    "Social History Section": {
        "standard_fields": ["observation", "code", "value", "effectiveTime"],
        "maps_to_uscdi": True,
        "domain": "Demographics",
    },
    "Vital Signs Section": {
        "standard_fields": ["observation", "code", "value", "unit", "effectiveTime"],
        "maps_to_uscdi": True,
        "domain": "Vitals",
    },
    "Mental Status Section": {
        "standard_fields": ["observation", "code", "value", "effectiveTime"],
        "maps_to_uscdi": False,
        "domain": "Health status assessments",
    },
    "Nutrition Section": {
        "standard_fields": ["observation", "code", "value", "effectiveTime"],
        "maps_to_uscdi": False,
        "domain": "Nutrition",
    },
}

# Build entity inventory
entities = []
total_fields = 0
for section in ccda_sections:
    section_info = ccda_section_fields.get(section["name"], {})
    fields = section_info.get("standard_fields", [])
    field_objects = []
    for f in fields:
        field_objects.append({
            "name": f,
            "type": "varies (per C-CDA 2.2 spec)",
            "description": f"Standard C-CDA 2.2 field - no vendor-specific documentation provided",
            "vendor_documented": False,
        })
    
    entity = {
        "name": section["name"],
        "oid": section["oid"],
        "entry_status": section["entry_status"],
        "spec_url": section["spec_url"],
        "domain": section_info.get("domain", "Unknown"),
        "maps_to_uscdi": section_info.get("maps_to_uscdi", False),
        "field_count": len(field_objects),
        "fields": field_objects,
        "vendor_documentation": "none - only links to generic HL7 C-CDA 2.2 spec",
    }
    entities.append(entity)
    total_fields += len(field_objects)

# Build full inventory
inventory = {
    "product": "SmartCare",
    "vendor": "Streamline Healthcare Solutions",
    "export_format": "C-CDA 2.2 (XML)",
    "documentation_source": "downloads/ehi-export-page-wp-api.json",
    "page_published": page_meta["published"],
    "page_modified": page_meta["modified"],
    "total_sections": len(entities),
    "total_fields_documented": 0,
    "total_fields_from_spec": total_fields,
    "has_vendor_data_dictionary": False,
    "has_sample_data": False,
    "has_machine_readable_schema": False,
    "export_process": {
        "single_patient": True,
        "bulk_population": True,
        "access_control": "System administrators and permissioned users",
        "cost": "No additional cost",
        "instructions": "Available in customer help desk (not public)",
    },
    "entities": entities,
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Build summary
uscdi_count = sum(1 for e in entities if e["maps_to_uscdi"])
domain_coverage = {}
for e in entities:
    d = e["domain"]
    if d not in domain_coverage:
        domain_coverage[d] = {"sections": 0, "fields_from_spec": 0}
    domain_coverage[d]["sections"] += 1
    domain_coverage[d]["fields_from_spec"] += e["field_count"]

summary = {
    "total_ccda_sections": len(entities),
    "sections_entries_required": sum(1 for e in entities if e["entry_status"] == "entries_required"),
    "sections_entries_optional": sum(1 for e in entities if e["entry_status"] == "entries_optional"),
    "sections_no_constraint": sum(1 for e in entities if e["entry_status"] == "no_entry_constraint"),
    "sections_mapping_to_uscdi": uscdi_count,
    "sections_beyond_uscdi": len(entities) - uscdi_count,
    "vendor_documented_fields": 0,
    "spec_referenced_fields": total_fields,
    "has_vendor_data_dictionary": False,
    "has_sample_data": False,
    "domain_coverage": domain_coverage,
    "domains_covered": list(domain_coverage.keys()),
    "domains_not_covered": [
        "Claims / billing",
        "Payments",
        "Patient communications / portal messages",
        "Behavioral health assessments",
        "Treatment plans (behavioral health)",
        "Progress notes",
        "Case management",
        "Substance use disorder records",
        "Foster care / adoption data",
        "IDD service data",
        "MCO management data",
        "Orders / referrals (detailed)",
        "Custom forms / screening tools",
    ],
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"=== EXTRACTION SUMMARY ===")
print(f"Total C-CDA sections: {summary['total_ccda_sections']}")
print(f"  Entries required: {summary['sections_entries_required']}")
print(f"  Entries optional: {summary['sections_entries_optional']}")
print(f"  No constraint: {summary['sections_no_constraint']}")
print(f"Maps to USCDI: {uscdi_count}/{len(entities)}")
print(f"Vendor-documented fields: 0 (no data dictionary)")
print(f"Spec-referenced fields: {total_fields}")
print(f"\nDomains covered: {len(domain_coverage)}")
for d, info in sorted(domain_coverage.items()):
    print(f"  {d}: {info['sections']} section(s)")
print(f"\nDomains NOT covered: {len(summary['domains_not_covered'])}")
for d in summary["domains_not_covered"]:
    print(f"  ❌ {d}")
