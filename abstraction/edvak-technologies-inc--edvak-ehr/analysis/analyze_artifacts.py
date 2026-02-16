"""
Analyze all EHI export artifacts for Edvak EHR.
Produces structured JSON inventory and summary statistics.
"""
import json, os, re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/edvak-technologies-inc--edvak-ehr/downloads")
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/edvak-technologies-inc--edvak-ehr/analysis")

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip = True
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = False
    def handle_data(self, data):
        if not self.skip:
            stripped = data.strip()
            if stripped:
                self.text.append(stripped)

def extract_html_text(filepath):
    with open(filepath) as f:
        content = f.read()
    parser = TextExtractor()
    parser.feed(content)
    return '\n'.join(parser.text)

def extract_sample_ccda_xml(filepath):
    """Extract the sample C-CDA XML from the API docs HTML."""
    class XMLCodeExtractor(HTMLParser):
        def __init__(self):
            super().__init__()
            self.text = []
            self.in_code = False
            self.skip = False
        def handle_starttag(self, tag, attrs):
            if tag == 'code':
                self.in_code = True
            if tag in ('script', 'style'):
                self.skip = True
        def handle_endtag(self, tag):
            if tag == 'code':
                self.in_code = False
            if tag in ('script', 'style'):
                self.skip = False
        def handle_data(self, data):
            if self.in_code and not self.skip:
                self.text.append(data)

    with open(filepath) as f:
        content = f.read()
    start = content.find('&lt;?xml')
    if start == -1:
        start = content.find('<?xml')
    if start == -1:
        return None
    chunk = content[start-200:start+10000]
    parser = XMLCodeExtractor()
    parser.feed(chunk)
    return ''.join(parser.text)

# Analyze all artifacts
results = {
    "vendor": "Edvak Technologies Inc",
    "product": "Edvak EHR v1",
    "chpl_id": "15.04.04.3230.Edva.0v.00.1.250613",
    "chpl_listing_id": 11656,
    "analysis_date": "2026-02-15",
    "artifacts": [],
    "export_format": "C-CDA (Continuity of Care Document)",
    "data_dictionary": None,
    "sample_data": None,
    "schema_files": None,
    "claimed_data_domains": [],
    "ccda_sections_documented": [],
    "api_endpoints": [],
    "export_mechanisms": [],
    "sample_ccda_analysis": {}
}

# 1. EHI Export Page
ehi_text = extract_html_text(DOWNLOADS / "ehi-export-page.html")
results["artifacts"].append({
    "file": "ehi-export-page.html",
    "type": "HTML",
    "size_bytes": os.path.getsize(DOWNLOADS / "ehi-export-page.html"),
    "source_url": "https://edvak.com/ehi-export",
    "description": "Main EHI export documentation page",
    "informativeness": "Primary - describes export workflow and data domains",
    "content_summary": "Step-by-step screenshots for single-patient and bulk C-CDA export"
})

# Extract claimed domains from page text
claimed_domains = [
    "demographics", "medications", "problems", "allergies", 
    "vitals", "immunizations", "lab results", "procedures",
    "care plans", "clinical notes"
]
results["claimed_data_domains"] = claimed_domains

# Export mechanisms
results["export_mechanisms"] = [
    {
        "type": "Single Patient UI Export",
        "description": "Export CCDA button on patient Facesheet",
        "output": "Single C-CDA XML file",
        "filename_pattern": "PATIENTNAME-TIMESTAMP"
    },
    {
        "type": "Population/Bulk UI Export",
        "description": "CCDA tab in Analytics → select patients → Export",
        "output": "ZIP file containing individual C-CDA XML files per patient",
        "filename_pattern": "ccda-bulk-TIMESTAMP.zip"
    },
    {
        "type": "CCDA API (programmatic)",
        "description": "REST API at darwinapi.edvak.com/ccda/ccda/patient_data",
        "output": "Single C-CDA XML per patient",
        "authentication": "OAuth 2.0 bearer token (ROPC flow, 900s TTL)"
    }
]

# 2. Screenshots
screenshot_files = sorted(os.listdir(DOWNLOADS / "screenshots"))
for sf in screenshot_files:
    fpath = DOWNLOADS / "screenshots" / sf
    results["artifacts"].append({
        "file": f"screenshots/{sf}",
        "type": "PNG screenshot",
        "size_bytes": os.path.getsize(fpath),
        "informativeness": "Supporting - shows UI workflow"
    })

# 3. CCDA API docs
api_files = [f for f in os.listdir(DOWNLOADS) if f.startswith("ccda-api-")]
for af in sorted(api_files):
    fpath = DOWNLOADS / af
    results["artifacts"].append({
        "file": af,
        "type": "HTML (Apidog-hosted API docs)",
        "size_bytes": os.path.getsize(fpath),
        "description": f"CCDA API documentation page: {af.replace('ccda-api-', '').replace('.html', '')}",
        "informativeness": "Secondary - documents programmatic C-CDA access"
    })

# 4. API endpoints
results["api_endpoints"] = [
    {
        "method": "POST",
        "path": "/ccda/ccda/generate-token",
        "description": "Generate OAuth 2.0 bearer token",
        "parameters": ["client_id", "client_secret", "username", "password"],
        "response": "Bearer token (900s TTL)"
    },
    {
        "method": "GET",
        "path": "/ccda/ccda/patient_data",
        "description": "Retrieve C-CDA document for a patient",
        "parameters": ["patient_token (required)", "date (optional)", "start_date (optional)", "end_date (optional)"],
        "response": "C-CDA XML (application/xml)"
    }
]

# 5. Sample C-CDA analysis
sample_xml = extract_sample_ccda_xml(DOWNLOADS / "ccda-api-ccda-retrieval-16935528e0.html")
if sample_xml:
    results["sample_ccda_analysis"] = {
        "source": "ccda-api-ccda-retrieval-16935528e0.html (embedded example)",
        "is_complete": False,
        "is_truncated": True,
        "truncation_note": "Example only contains document header and recordTarget (patient demographics). No structuredBody or clinical sections present.",
        "template_id": "2.16.840.1.113883.10.20.22.1.1 (extension 2015-08-01)",
        "template_name": "US Realm Header (C-CDA R2.1)",
        "document_type_code": "34133-9 (Summarization of Episode Note)",
        "document_title": "Continuity of Care Document",
        "patient_elements_shown": [
            "id (MRN: M3PK1HBA1194)",
            "addr (streetAddressLine, city, state, postalCode, country)",
            "telecom (phone, email)",
            "name (given, family)",
            "administrativeGenderCode",
            "birthTime",
            "raceCode",
            "languageCommunication"
        ],
        "clinical_sections_shown": [],
        "raw_xml_length": len(sample_xml)
    }

# 6. Facesheet sections visible in SP_2.png screenshot
results["facesheet_sections_visible"] = [
    "Medications", "Problems", "Vitals", "Allergies",
    "Labs & Imaging", "Past History", "Immunizations", "Goals",
    "Assessments", "Interventions"
]
results["facesheet_tabs_visible"] = [
    "Facesheet", "Demographics", "Documents", "Encounter Notes", "Billing", "Referrals"
]
results["facesheet_action_buttons_visible"] = [
    "Export CCDA", "Copy Patient Self-Registration Link",
    "Forms & Letters", "Patient Education", "Tasks", "Notes", "Print"
]

# 7. ZIP contents from MP_7.png screenshot
results["bulk_export_sample"] = {
    "zip_filename": "ccda-bulk-1747301769867",
    "files": [
        {"name": "ALICE_NOMEN-1747301769142", "type": "Microsoft Edge HTML Document", "size_kb": 15},
        {"name": "AMY_BAXTER-1747301769124", "type": "Microsoft Edge HTML Document", "size_kb": 14},
        {"name": "CLIFFORD_DENNIS-1747301769573", "type": "Microsoft Edge HTML Document", "size_kb": 30},
        {"name": "HARVEY_HAMMOND-174730176988", "type": "Microsoft Edge HTML Document", "size_kb": 33}
    ],
    "total_files": 4,
    "date": "5/15/2025",
    "note": "Files shown as HTML Documents in Windows Explorer, consistent with XML/HTML rendering. Sizes range 14-33 KB."
}

# Save results
with open(OUTPUT_DIR / "full-entity-inventory.json", "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("=== Edvak EHR EHI Export Analysis ===")
print(f"Total artifacts: {len(results['artifacts'])}")
print(f"  - HTML pages: {sum(1 for a in results['artifacts'] if a['type'] == 'HTML')}")
print(f"  - API doc pages: {sum(1 for a in results['artifacts'] if 'Apidog' in a.get('type', ''))}")
print(f"  - Screenshots: {sum(1 for a in results['artifacts'] if 'screenshot' in a.get('type', '').lower())}")
print(f"\nExport format: {results['export_format']}")
print(f"Data dictionary: {'None provided' if not results['data_dictionary'] else 'Yes'}")
print(f"Schema files: {'None provided' if not results['schema_files'] else 'Yes'}")
print(f"Sample data: {'Truncated header-only example in API docs' if results['sample_ccda_analysis'] else 'None'}")
print(f"\nClaimed data domains: {len(results['claimed_data_domains'])}")
for d in results['claimed_data_domains']:
    print(f"  - {d}")
print(f"\nExport mechanisms: {len(results['export_mechanisms'])}")
for m in results['export_mechanisms']:
    print(f"  - {m['type']}: {m['description']}")
print(f"\nFacesheet tabs visible (SP_2.png): {', '.join(results['facesheet_tabs_visible'])}")
print(f"Facesheet clinical sections (SP_2.png): {', '.join(results['facesheet_sections_visible'])}")
print(f"\nSample CCDA: truncated={results['sample_ccda_analysis'].get('is_truncated', 'N/A')}")
print(f"  Template: {results['sample_ccda_analysis'].get('template_id', 'N/A')}")
print(f"  Document type: {results['sample_ccda_analysis'].get('document_type_code', 'N/A')}")
print(f"  Clinical sections in example: {len(results['sample_ccda_analysis'].get('clinical_sections_shown', []))}")
