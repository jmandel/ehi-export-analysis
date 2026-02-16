#!/usr/bin/env python3
"""
Produce the full entity inventory for Carbon Health CarbyOs EHR export analysis.

This vendor has NO data dictionary for the (b)(10) EHI export. The only structured
documentation available is the FHIR API PDF for (g)(10), which covers USCDI v3
data classes mapped to US Core 6.1.0 profiles. The (b)(10) EHI export documentation
consists of ~150 words of prose on the certification disclosures page stating that
the export uses "C-CDA documents for clinical records, PDFs for billing and claims
information, and original native formats for uploaded documents."

Since there is no EHI export-specific data dictionary, this inventory captures:
1. The EHI export documentation text (from the certification disclosures page)
2. The FHIR resource inventory (from the g(10) API PDF) as the only reference
   for what clinical data the system can expose
"""

import json

# The complete EHI export documentation text
ehi_export_documentation = {
    "source": "certification-disclosures.html",
    "section": "EHI Export Functionality",
    "full_text": (
        "CarbyOs EHR meets the certification criterion §170.315(b)(10) for Electronic "
        "Health Information (EHI) export by enabling users to export EHI in an electronic "
        "and computable format. The EHI Export functionality supports both single-patient "
        "and patient population exports.\n\n"
        "1. Single-Patient EHI Export\n"
        "- Users can export all EHI for an individual patient at any time without requiring "
        "developer assistance.\n"
        "- Export formats include C-CDA documents for clinical records, PDFs for billing and "
        "claims information, and original native formats for uploaded documents.\n"
        "- The export is electronic, computable, ensuring accessibility without preconditions.\n\n"
        "2. Patient Population EHI Export\n"
        "- Users can export all EHI for their entire patient population in bulk.\n"
        "- The export is electronic, computable, and supports system migration or data transfer "
        "to other health IT products.\n\n"
        "3. Limitations and Exclusions\n"
        "- EHI exports exclude psychotherapy notes as defined in 45 CFR 164.501 and information "
        "compiled for legal proceedings.\n"
        "- System administrators manage the ability to perform EHI exports to maintain data security.\n\n"
        "4. Benefits of EHI Export in CarbyOs EHR\n"
        "- Facilitates patient access to their records in a timely and computable manner.\n"
        "- Supports healthcare organizations in transitioning to other health IT systems or "
        "performing bulk data migrations.\n"
        "- Aligns with the interoperability and data access goals of the 21st Century Cures Act, "
        "ensuring compliance with federal requirements and enabling standardized data exchange."
    ),
    "export_formats": [
        {
            "format": "C-CDA",
            "scope": "clinical records",
            "detail_level": "none - no C-CDA sections, templates, or field-level detail provided"
        },
        {
            "format": "PDF",
            "scope": "billing and claims information",
            "detail_level": "none - no detail on what billing data is included; PDF is not computable"
        },
        {
            "format": "original native formats",
            "scope": "uploaded documents",
            "detail_level": "none - no detail on what document types are included"
        }
    ],
    "data_dictionary_exists": False,
    "schema_provided": False,
    "sample_data_provided": False,
    "field_level_documentation": False,
    "entities_documented": 0,
    "fields_documented": 0
}

# Load the FHIR resource inventory for reference
fhir_inventory_path = '/home/jmandel/hobby/ehi-export-analysis/abstraction/carbon-health-technologies-inc--carbyos-ehr/analysis/fhir-resources-inventory.json'
with open(fhir_inventory_path, 'r') as f:
    fhir_inventory = json.load(f)

# FHIR resources (g)(10) - for reference only
fhir_resources = []
for r in fhir_inventory['resources']:
    # De-duplicate (Practitioner appears twice in parse)
    if r['resource'] == 'Practitioner' and len(r['data_elements']) == 0:
        continue
    if r['resource'] == 'Specimen' and r.get('profile', '').startswith('audience'):
        r['profile'] = 'US Core Specimen'
    fhir_resources.append({
        'resource_name': r['resource'],
        'profile': r['profile'],
        'element_count': len(r['data_elements']),
        'elements': r['data_elements']
    })

full_inventory = {
    "vendor": "Carbon Health Technologies, Inc.",
    "product": "CarbyOs EHR",
    "analysis_date": "2026-02-16",
    "inventory_type": "minimal_stub",
    "note": (
        "This vendor provides NO data dictionary, schema, or sample data for the (b)(10) EHI export. "
        "The only EHI export documentation is ~150 words of prose on the certification disclosures page. "
        "The FHIR API documentation (74 pages) covers the (g)(10) API only and is included here as the "
        "only available reference for what clinical data elements the system can expose."
    ),
    "ehi_export_b10": {
        "documentation": ehi_export_documentation,
        "entities": [],
        "total_entities": 0,
        "total_fields": 0,
        "fields_with_descriptions": 0
    },
    "fhir_api_g10_reference": {
        "source": "carbonhealth-fhir-api-doc-v1_2.pdf",
        "pages": 74,
        "standard": "US Core 6.1.0 / USCDI v3",
        "total_resources": len(fhir_resources),
        "total_data_elements": sum(r['element_count'] for r in fhir_resources),
        "resources": fhir_resources
    }
}

output_path = '/home/jmandel/hobby/ehi-export-analysis/abstraction/carbon-health-technologies-inc--carbyos-ehr/analysis/full-entity-inventory.json'
with open(output_path, 'w') as f:
    json.dump(full_inventory, f, indent=2)

# Print summary
print("=== Full Entity Inventory Summary ===")
print(f"\nEHI Export (b)(10) Documentation:")
print(f"  Entities documented: {full_inventory['ehi_export_b10']['total_entities']}")
print(f"  Fields documented: {full_inventory['ehi_export_b10']['total_fields']}")
print(f"  Data dictionary: NO")
print(f"  Schema: NO")
print(f"  Sample data: NO")
print(f"  Export formats: C-CDA (clinical), PDF (billing), native (uploads)")

print(f"\nFHIR API (g)(10) Reference (NOT b(10)):")
print(f"  Resources: {len(fhir_resources)}")
print(f"  Total data elements: {sum(r['element_count'] for r in fhir_resources)}")
print(f"\n  {'Resource':<25} {'Elements':>8}")
print(f"  {'-'*35}")
for r in fhir_resources:
    print(f"  {r['resource_name']:<25} {r['element_count']:>8}")
