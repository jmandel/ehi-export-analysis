#!/usr/bin/env python3
"""
Parse all Edvak EHR EHI export artifacts and produce entity-inventory-full.json
and entity-inventory-summary.json.

Edvak's (b)(10) export is a C-CDA document with no data dictionary provided.
We reconstruct the "entities" from:
1. The EHI export page's listed data domains
2. The C-CDA response example (API docs)
3. The Facesheet screenshot sections (visible UI data areas)
4. The C-CDA standard sections implied by CCD templateId 2.16.840.1.113883.10.20.22.1.1

Since there is no vendor-provided data dictionary, schema, or sample export file,
we document what the vendor *claims* to export based on their documentation text.
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT = Path(".")


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
    p = TextExtractor()
    with open(filepath) as f:
        p.feed(f.read())
    return "\n".join(p.text)


# 1. Parse EHI export page for claimed data domains
ehi_text = extract_text(DOWNLOADS / "ehi-export-page.html")

# Extract the listed data domains from the single-patient description
claimed_domains = []
# The page says: "demographics, medications, problems, allergies, vitals,
# immunizations, lab results, procedures, care plans, and clinical notes"
domain_match = re.search(
    r"includes data such as ([^.]+)\.", ehi_text, re.IGNORECASE
)
if domain_match:
    raw = domain_match.group(1)
    # Split on commas and "and"
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+", raw)
    claimed_domains = [p.strip() for p in parts if p.strip()]

# 2. Parse CCDA API introduction for document types
intro_text = extract_text(DOWNLOADS / "ccda-api-introduction-1018024m0.html")
ccda_doc_types = []
for dtype in [
    "Continuity of Care Document (CCD)",
    "Discharge Summary",
    "Referral Note",
    "Consultation Note",
    "Progress Note",
]:
    if dtype.lower() in intro_text.lower():
        ccda_doc_types.append(dtype)

# 3. Parse CCDA retrieval for the example XML structure
retrieval_text = extract_text(DOWNLOADS / "ccda-api-ccda-retrieval-16935528e0.html")

# Extract templateId from example
template_ids = re.findall(r'templateId.*?root\s*=\s*"([^"]+)"', retrieval_text)

# 4. Build the entity inventory
# Since there is NO data dictionary, we document what the vendor claims.
# Each "entity" is a claimed data domain mapped to standard C-CDA sections.

ccda_section_map = {
    "demographics": {
        "ccda_section": "recordTarget/patientRole",
        "ccda_template": "N/A (header element)",
        "standard_fields": [
            "name (given, family)",
            "administrativeGenderCode",
            "birthTime",
            "raceCode",
            "addr (streetAddressLine, city, state, postalCode, country)",
            "telecom",
            "languageCommunication",
        ],
        "notes": "Confirmed in API example XML response",
    },
    "medications": {
        "ccda_section": "Medications Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.1.1",
        "standard_fields": [
            "medication",
            "dose",
            "route",
            "frequency",
            "effectiveTime",
            "statusCode",
        ],
        "notes": "Listed in export page; visible on Facesheet",
    },
    "problems": {
        "ccda_section": "Problem Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.5.1",
        "standard_fields": [
            "problemCode",
            "problemStatus",
            "effectiveTime",
            "severity",
        ],
        "notes": "Listed in export page; visible on Facesheet",
    },
    "allergies": {
        "ccda_section": "Allergies and Intolerances Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.6.1",
        "standard_fields": [
            "allergen",
            "reaction",
            "severity",
            "statusCode",
            "effectiveTime",
        ],
        "notes": "Listed in export page; visible on Facesheet",
    },
    "vitals": {
        "ccda_section": "Vital Signs Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.4.1",
        "standard_fields": [
            "code (LOINC)",
            "value",
            "unit",
            "effectiveTime",
            "interpretationCode",
        ],
        "notes": "Listed in export page; visible on Facesheet",
    },
    "immunizations": {
        "ccda_section": "Immunizations Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.2.1",
        "standard_fields": [
            "vaccineCode",
            "effectiveTime",
            "statusCode",
            "routeCode",
            "doseQuantity",
        ],
        "notes": "Listed in export page; visible on Facesheet",
    },
    "lab results": {
        "ccda_section": "Results Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.3.1",
        "standard_fields": [
            "code (LOINC)",
            "value",
            "unit",
            "referenceRange",
            "effectiveTime",
            "statusCode",
        ],
        "notes": "Listed in export page; Facesheet shows 'Labs & Imaging'",
    },
    "procedures": {
        "ccda_section": "Procedures Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.7.1",
        "standard_fields": [
            "procedureCode",
            "effectiveTime",
            "statusCode",
            "targetSiteCode",
        ],
        "notes": "Listed in export page",
    },
    "care plans": {
        "ccda_section": "Plan of Treatment Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.10",
        "standard_fields": [
            "planOfCareActivity",
            "effectiveTime",
            "statusCode",
        ],
        "notes": "Listed in export page",
    },
    "clinical notes": {
        "ccda_section": "Notes Section / embedded narrative",
        "ccda_template": "Various",
        "standard_fields": ["text/narrative", "code", "effectiveTime", "author"],
        "notes": "Listed in export page; Facesheet shows 'Encounter Notes' tab",
    },
}

# Facesheet sections visible in screenshot SP_2.png but NOT listed in export text
facesheet_only_sections = {
    "past history": {
        "ccda_section": "Past Medical History Section (possible)",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.20",
        "standard_fields": ["observation", "effectiveTime"],
        "notes": "Visible on Facesheet but NOT listed in export documentation text",
    },
    "goals": {
        "ccda_section": "Goals Section",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.60",
        "standard_fields": ["goal", "effectiveTime", "statusCode"],
        "notes": "Visible on Facesheet but NOT listed in export documentation text (care plans may include)",
    },
    "assessments": {
        "ccda_section": "Assessment Section (possible)",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.8",
        "standard_fields": ["assessment text"],
        "notes": "Visible on Facesheet but NOT listed in export documentation text",
    },
    "interventions": {
        "ccda_section": "Interventions Section (possible)",
        "ccda_template": "2.16.840.1.113883.10.20.22.2.24",
        "standard_fields": ["intervention", "effectiveTime"],
        "notes": "Visible on Facesheet but NOT listed in export documentation text",
    },
}

# Product tabs visible but not in export
product_tabs_not_in_export = [
    "Documents",
    "Billing",
    "Referrals",
]

# Build full inventory
entities = []
for domain, info in ccda_section_map.items():
    entities.append(
        {
            "entity_name": domain,
            "category": "Claimed in export documentation",
            "ccda_section": info["ccda_section"],
            "ccda_template_id": info["ccda_template"],
            "fields": [
                {
                    "name": f,
                    "type": "C-CDA standard (no vendor-specific documentation)",
                    "description": None,
                    "documented_by_vendor": False,
                }
                for f in info["standard_fields"]
            ],
            "field_count": len(info["standard_fields"]),
            "fields_with_descriptions": 0,
            "notes": info["notes"],
            "source": "ehi-export-page.html text + C-CDA standard inference",
        }
    )

for domain, info in facesheet_only_sections.items():
    entities.append(
        {
            "entity_name": domain,
            "category": "Visible on Facesheet UI but not explicitly listed in export",
            "ccda_section": info["ccda_section"],
            "ccda_template_id": info["ccda_template"],
            "fields": [
                {
                    "name": f,
                    "type": "C-CDA standard (no vendor-specific documentation)",
                    "description": None,
                    "documented_by_vendor": False,
                }
                for f in info["standard_fields"]
            ],
            "field_count": len(info["standard_fields"]),
            "fields_with_descriptions": 0,
            "notes": info["notes"],
            "source": "Screenshot SP_2.png (Facesheet view)",
        }
    )

# Full inventory
inventory = {
    "vendor": "Edvak Technologies Inc",
    "product": "Edvak EHR",
    "export_format": "C-CDA (Continuity of Care Document)",
    "data_dictionary_provided": False,
    "sample_export_provided": False,
    "schema_provided": False,
    "claimed_domains_from_text": claimed_domains,
    "ccda_template_id": "2.16.840.1.113883.10.20.22.1.1 (CCD, 2015-08-01)",
    "ccda_document_types_mentioned": ccda_doc_types,
    "entity_count": len(entities),
    "total_inferred_fields": sum(e["field_count"] for e in entities),
    "fields_with_vendor_descriptions": 0,
    "product_tabs_not_in_export": product_tabs_not_in_export,
    "entities": entities,
    "notes": (
        "No vendor-provided data dictionary exists. All fields are inferred from "
        "C-CDA standard sections corresponding to the domains the vendor claims to export. "
        "The actual fields in the vendor's C-CDA output cannot be verified without a sample file."
    ),
}

with open(OUTPUT / "entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Summary
summary = {
    "vendor": inventory["vendor"],
    "product": inventory["product"],
    "export_format": inventory["export_format"],
    "data_dictionary_provided": inventory["data_dictionary_provided"],
    "sample_export_provided": inventory["sample_export_provided"],
    "schema_provided": inventory["schema_provided"],
    "entity_count": inventory["entity_count"],
    "total_inferred_fields": inventory["total_inferred_fields"],
    "fields_with_vendor_descriptions": inventory["fields_with_vendor_descriptions"],
    "description_percentage": "0%",
    "claimed_domains": inventory["claimed_domains_from_text"],
    "domains_explicitly_claimed": len(ccda_section_map),
    "domains_visible_on_ui_only": len(facesheet_only_sections),
    "product_tabs_absent_from_export": inventory["product_tabs_not_in_export"],
    "category_breakdown": {
        "Claimed in export documentation": {
            "entities": len(ccda_section_map),
            "fields": sum(
                e["field_count"]
                for e in entities
                if e["category"] == "Claimed in export documentation"
            ),
        },
        "Visible on Facesheet UI but not in export": {
            "entities": len(facesheet_only_sections),
            "fields": sum(
                e["field_count"]
                for e in entities
                if e["category"] != "Claimed in export documentation"
            ),
        },
    },
}

with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== Entity Inventory Summary ===")
print(f"Export format: {summary['export_format']}")
print(f"Data dictionary provided: {summary['data_dictionary_provided']}")
print(f"Sample export provided: {summary['sample_export_provided']}")
print(f"Entity count (inferred): {summary['entity_count']}")
print(f"Total inferred fields: {summary['total_inferred_fields']}")
print(f"Fields with vendor descriptions: {summary['fields_with_vendor_descriptions']}")
print(f"Domains explicitly claimed: {summary['domains_explicitly_claimed']}")
print(f"Domains visible on UI only: {summary['domains_visible_on_ui_only']}")
print(f"Product tabs absent from export: {summary['product_tabs_absent_from_export']}")
print(f"\nClaimed domains: {summary['claimed_domains']}")
