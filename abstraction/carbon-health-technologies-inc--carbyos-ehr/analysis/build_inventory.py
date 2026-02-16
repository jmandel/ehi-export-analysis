#!/usr/bin/env python3
"""Build entity inventory for CarbyOS EHR EHI export.

Since CarbyOS has NO data dictionary for its (b)(10) export, the only structured
data we can extract is from the (g)(10) FHIR API documentation. This represents
the USCDI clinical data surface, NOT the (b)(10) EHI export.

We document this to show:
1. What the FHIR API covers (the clinical floor)
2. What the (b)(10) export CLAIMS to cover (prose only, no details)
3. The gap between what the product stores and what's documented
"""

import json
import re

# Load the parsed FHIR API resources
with open("analysis/fhir-api-resources.json") as f:
    fhir_resources = json.load(f)

# Build entity inventory
# Since there's no (b)(10) data dictionary, we document what we know:
# 1. The FHIR API resources (from g(10) doc)
# 2. The claimed export formats (from certification disclosures prose)

entities = []

# FHIR API resources from g(10)
for resource in fhir_resources:
    entity = {
        "name": resource["name"],
        "source": "FHIR API (g)(10) documentation",
        "source_file": "carbonhealth-fhir-api-doc-v1_2.pdf",
        "field_count": len(resource["data_elements"]),
        "fields": [],
        "category": "Clinical (USCDI v3)",
        "note": "This is from the (g)(10) API doc, NOT the (b)(10) EHI export. No (b)(10) data dictionary exists."
    }
    
    for elem in resource["data_elements"]:
        field = {
            "name": elem["name"],
            "type": elem.get("type", ""),
            "description": elem.get("description", ""),
            "has_description": bool(elem.get("description", "").strip()),
            "has_type": bool(elem.get("type", "").strip())
        }
        entity["fields"].append(field)
    
    entities.append(entity)

# Claimed (b)(10) export content - prose only, no structured documentation
b10_claims = {
    "clinical_records": {
        "format": "C-CDA documents",
        "detail_level": "none - no templates, sections, or fields specified",
        "documentation": "Single sentence: 'C-CDA documents for clinical records'"
    },
    "billing_claims": {
        "format": "PDF",
        "detail_level": "none - no content description",
        "documentation": "Single phrase: 'PDFs for billing and claims information'",
        "concern": "PDF is not computable; violates spirit of electronic/computable requirement"
    },
    "uploaded_documents": {
        "format": "Original native formats",
        "detail_level": "none",
        "documentation": "Single phrase: 'original native formats for uploaded documents'"
    }
}

# Summary stats
total_entities = len(entities)
total_fields = sum(e["field_count"] for e in entities)
fields_with_descriptions = sum(
    1 for e in entities for f in e["fields"] if f["has_description"]
)
fields_with_types = sum(
    1 for e in entities for f in e["fields"] if f["has_type"]
)

summary = {
    "product": "CarbyOs EHR",
    "vendor": "Carbon Health Technologies, Inc.",
    "analysis_date": "2026-02-16",
    "has_b10_data_dictionary": False,
    "b10_documentation_word_count": 157,
    "b10_claimed_formats": ["C-CDA (clinical)", "PDF (billing)", "Native (uploads)"],
    "b10_export_entities": "Unknown - no data dictionary provided",
    "b10_export_fields": "Unknown - no data dictionary provided",
    "g10_fhir_api": {
        "resources": total_entities,
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_descriptions,
        "fields_with_types": fields_with_types,
        "description_coverage_pct": round(fields_with_descriptions / total_fields * 100, 1) if total_fields > 0 else 0,
        "note": "These are from the (g)(10) FHIR API doc, the only structured documentation available"
    },
    "b10_claims": b10_claims,
    "assessment": {
        "coverage_breadth": "Minimal/stub/unclear",
        "export_approach": "Unclear/undetermined",
        "rationale": "No data dictionary exists for the (b)(10) export. The only structured documentation is for the (g)(10) FHIR API covering USCDI v3. The (b)(10) export claims C-CDA for clinical and PDF for billing, but provides zero detail about content."
    }
}

# Save full inventory
with open("analysis/entity-inventory-full.json", "w") as f:
    json.dump({
        "metadata": {
            "product": "CarbyOs EHR",
            "vendor": "Carbon Health Technologies, Inc.",
            "note": "NO (b)(10) data dictionary exists. The entities below are from the (g)(10) FHIR API documentation only.",
            "source_file": "carbonhealth-fhir-api-doc-v1_2.pdf",
            "has_b10_data_dictionary": False
        },
        "g10_fhir_resources": entities,
        "b10_claims": b10_claims
    }, f, indent=2)

# Save summary
with open("analysis/entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Entity Inventory Summary")
print("=" * 60)
print(f"(b)(10) EHI Export Data Dictionary: NONE")
print(f"(b)(10) Documentation: ~157 words of prose, no technical detail")
print(f"(b)(10) Claimed formats: C-CDA, PDF, native uploads")
print()
print(f"(g)(10) FHIR API Resources: {total_entities}")
print(f"(g)(10) Total Fields: {total_fields}")
print(f"(g)(10) Fields with descriptions: {fields_with_descriptions} ({round(fields_with_descriptions/total_fields*100,1)}%)")
print(f"(g)(10) Fields with types: {fields_with_types} ({round(fields_with_types/total_fields*100,1)}%)")
print()
print("FHIR Resources:")
for e in entities:
    print(f"  {e['name']}: {e['field_count']} fields")

print()
print("Saved: analysis/entity-inventory-full.json")
print("Saved: analysis/entity-inventory-summary.json")
