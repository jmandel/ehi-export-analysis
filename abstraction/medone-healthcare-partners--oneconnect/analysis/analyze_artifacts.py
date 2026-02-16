"""
Analyze all EHI export artifacts for MedOne Healthcare Partners / OneConnect.
Produces full-entity-inventory.json and summary statistics.
"""
import json
import os
import re

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/medone-healthcare-partners--oneconnect"
ANALYSIS_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/medone-healthcare-partners--oneconnect/analysis"

# 1. Load the FHIR API text (already extracted via pdftotext)
with open(os.path.join(ANALYSIS_DIR, "fhir-api-full-text.txt")) as f:
    fhir_text = f.read()

# 2. Extract FHIR resource types documented in the FHIR API PDF
# Look for "Request : ResourceType" or "Request: ResourceType" patterns in the TOC
resource_pattern = re.compile(r'Request\s*:\s*(.+?)(?:\s*\.{2,}|\s*$)', re.MULTILINE)
resources_found = set()
for m in resource_pattern.finditer(fhir_text):
    name = m.group(1).strip().rstrip('.')
    if name and len(name) < 80:
        resources_found.add(name)

# Also look for explicit FHIR resource type references in API calls
fhir_resource_pattern = re.compile(r'GET\s+\d+\s+https://[^/]+/fhir-server/api/v\d+/(\w+)')
for m in fhir_resource_pattern.finditer(fhir_text):
    resources_found.add(m.group(1))

# Clean up resource names
cleaned_resources = []
for r in sorted(resources_found):
    # Skip generic items
    if r.lower() in ('complete patient summary (ccda)', 'patient'):
        cleaned_resources.append(r)
    elif any(x in r.lower() for x in ['error', 'search', 'get doc']):
        continue
    else:
        cleaned_resources.append(r)

# 3. Build inventory - since the export is C-CDA based with no data dictionary,
# we document what we CAN determine from the FHIR API specs about data the system stores
inventory = {
    "export_type": "C-CDA documents in ZIP archive",
    "export_format": "C-CDA (per encounter) in ZIP",
    "data_dictionary_provided": False,
    "schema_provided": False,
    "sample_data_provided": False,
    "documentation_pages": 1,
    "documentation_sentences": 6,
    "documentation_date": "2023-11-07",
    "fhir_api_pages": 58,
    "fhir_api_date": "2023-11-28",
    "fhir_resource_types_in_api": cleaned_resources,
    "fhir_resource_count": len(cleaned_resources),
    "ehi_export_pdf_text": (
        "Product Name and Version : OneConnect Version 0\n\n"
        "The patient EHI export contains data from the patient's chart. "
        "Multiple file formats are used to store this information.\n\n"
        "ZIP is an archive file format.\n\n"
        "PDF or Portable Document Format is a file format that is used to present "
        "text or image based documents.\n\n"
        "C-CDA or Consolidated Clinical Document Architecture is a file format used "
        "for health information exchange.\n\n"
        "The export file itself is a zip file. It contains zip files of C-CDAs for now "
        "and other files attached to the patient's chart will be added later (e.g. PDF and images)\n\n"
        "Information for each patient encounter is available C-CDA format in zip archive."
    ),
    "entities": [],  # No data dictionary exists - no entities to enumerate
    "artifacts_reviewed": [
        {
            "file": "EHI-Export.pdf",
            "type": "PDF",
            "pages": 1,
            "size_bytes": 282272,
            "description": "Entire EHI export documentation. Single page, 6 sentences. No data dictionary, no schema, no sample data.",
            "informativeness": "Primary but extremely thin"
        },
        {
            "file": "FHIR-API-Specifications.pdf",
            "type": "PDF",
            "pages": 58,
            "size_bytes": 1296059,
            "description": "FHIR (g)(10) API documentation. Smart on FHIR OAuth2 flow and US Core resource access. NOT the (b)(10) EHI export.",
            "informativeness": "Supplementary - shows what data the system stores via FHIR"
        },
        {
            "file": "FHIR_Valid_URLs.json",
            "type": "JSON",
            "size_bytes": 2235,
            "description": "FHIR Bundle with Endpoint and Organization resources. Infrastructure metadata only.",
            "informativeness": "Minimal - confirms FHIR server endpoint exists"
        },
        {
            "file": "certifications-page-screenshot.png",
            "type": "PNG",
            "size_bytes": 366699,
            "description": "Screenshot of MedOne certifications page showing certification details and footer links to EHI Export PDF, FHIR URLs, and FHIR API Specifications.",
            "informativeness": "Confirms documentation availability and navigation"
        }
    ]
}

# Write full inventory
with open(os.path.join(ANALYSIS_DIR, "full-entity-inventory.json"), "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print("=== Artifact Analysis Summary ===")
print(f"Total artifacts: {len(inventory['artifacts_reviewed'])}")
print(f"EHI Export doc pages: {inventory['documentation_pages']}")
print(f"EHI Export doc sentences: {inventory['documentation_sentences']}")
print(f"Data dictionary provided: {inventory['data_dictionary_provided']}")
print(f"Schema provided: {inventory['schema_provided']}")
print(f"Sample data provided: {inventory['sample_data_provided']}")
print(f"Export format: {inventory['export_format']}")
print(f"\nFHIR API resource types documented ({inventory['fhir_resource_count']}):")
for r in cleaned_resources:
    print(f"  - {r}")
print(f"\nFull inventory written to: {os.path.join(ANALYSIS_DIR, 'full-entity-inventory.json')}")
