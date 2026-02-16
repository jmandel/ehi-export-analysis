#!/usr/bin/env python3
"""
Parse all Tebra EHI export artifacts and produce structured inventories.

Tebra has NO data dictionary or schema. This script extracts what little 
structured information exists from:
1. The EHI Export section on the MACRA/MIPS page (1 paragraph)
2. The Cures Act Request Form (19 selectable data categories)
3. The Help Center article on Export Patient Clinical Data
4. The FHIR API User Guide (g(10), not b(10) - for comparison)
5. The General Clinical API Documentation (for comparison)
6. The 2024 Real World Test Results (b(10) usage data)
"""

import json
import subprocess
import re
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path("../downloads")
OUTPUT = Path(".")

# --- 1. Extract EHI Export paragraph from MACRA page ---
with open(DOWNLOADS / "macra_mips_page.html") as f:
    html = f.read()

# Find the EHI Export section
ehi_match = re.search(
    r'<h3><strong>EHI Export Functionality</strong></h3>\s*<p>(.*?)</p>',
    html, re.DOTALL
)
ehi_paragraph = ehi_match.group(1).strip() if ehi_match else ""
ehi_paragraph = re.sub(r'\s+', ' ', ehi_paragraph)

# --- 2. Extract categories from Cures Act Request Form screenshot ---
# Categories verified from screenshot (19 total):
cures_act_categories = [
    "Allergies and Intolerances",
    "Assessment and Plan of Treatment",
    "Care Team Members",
    "Clinical Notes",
    "Immunizations",
    "Laboratory Tests & Results",
    "Medications",
    "Patient Demographics",
    "Problems",
    "Procedures",
    "Patient's Implantable Device(s)",
    "Vital Signs",
    "Past Medical History",
    "Past Surgical History",
    "Family History",
    "Social History",
    "OB/Pregnancy History",
    "Account/Insurance Information",
    "Documents",
]

# --- 3. Extract export help article info ---
with open(DOWNLOADS / "help_export_patient_clinical_data.html") as f:
    help_html = f.read()

class SimpleTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        self.skip_depth = 0
    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1
    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1
    def handle_data(self, data):
        if self.skip_depth == 0:
            t = data.strip()
            if t:
                self.text_parts.append(t)

ext = SimpleTextExtractor()
ext.feed(help_html)
help_text = "\n".join(ext.text_parts)

# Key facts from help article
help_facts = {
    "export_format": "Individual XML Summary of Care files (.ccda) per patient + patient documents",
    "access_path": "Practice Settings > Data Management > Export Patient Data",
    "filtering": "Date range and provider selection",
    "scheduling": "One-time or recurring (monthly on 1st, weekly on Mondays)",
    "delivery": "Zip file download",
    "includes_documents": True,
    "field_level_detail": False,
}

# --- 4. Extract FHIR API resource types (g(10) comparison) ---
fhir_text = subprocess.run(
    ["pdftotext", "-layout", str(DOWNLOADS / "fhir_api_guide.pdf"), "-"],
    capture_output=True, text=True
).stdout

fhir_resources = []
# Extract resource names from section headers
for line in fhir_text.split("\n"):
    line = line.strip()
    # Match resource section headers
    if re.match(r'^(Patient|Allergy Intolerance|Care Plan|Care Team|Condition|'
                r'Diagnostic Report|Document Reference|Encounter|Goal|'
                r'Immunization|Implantable Device|Laboratory Result Observation|'
                r'Location|Medication Request|Medication\b|Observation|'
                r'Organization|Practitioner Role|Practitioner\b|Procedure|'
                r'Provenance)', line):
        resource = line.split("...")[0].strip()
        if resource and resource not in fhir_resources and len(resource) < 50:
            fhir_resources.append(resource)

# Manually verified list from PDF TOC
fhir_resources_verified = [
    "Patient", "Allergy Intolerance", "Care Plan", "Care Team",
    "Condition", "Diagnostic Report for Lab Results",
    "Diagnostic Report for Report and Note", "Document Reference",
    "Encounter", "Goal", "Immunization", "Implantable Device",
    "Laboratory Result Observation", "Location", "Medication",
    "Medication Request", "Observation", "Organization",
    "Practitioner", "Practitioner Role", "Procedure", "Provenance"
]

# --- 5. Extract General API endpoints ---
gen_api_text = subprocess.run(
    ["pdftotext", "-layout", str(DOWNLOADS / "general_api_docs.pdf"), "-"],
    capture_output=True, text=True
).stdout

gen_api_endpoints = []
for line in gen_api_text.split("\n"):
    m = re.search(r'https://api\.tebra\.com/clinical/v1/api/patient(/\S+)?', line)
    if m:
        endpoint = m.group(0)
        if endpoint not in gen_api_endpoints:
            gen_api_endpoints.append(endpoint)

# --- 6. Extract RWT Measure #4 data ---
rwt_text = subprocess.run(
    ["pdftotext", "-layout", str(DOWNLOADS / "2024_test_results.pdf"), "-"],
    capture_output=True, text=True
).stdout

rwt_measure4 = {
    "associated_criteria": "315(b)(10)",
    "providers_tested": 755,
    "reporting_interval": "3 months (April-June 2024)",
    "total_ehi_exports": 3931,
    "total_practices": 790,
    "exports_per_practice_avg": 4.98,
    "export_content": "C-CDAs and other patient documents",
    "note": "Originally measured as 315(b)(6) Patient Batch Export, substituted for broader (b)(10)"
}

# --- 7. Extract Cures Act FAQ key statements ---
with open(DOWNLOADS / "help_cures_act_faqs.html") as f:
    faq_html = f.read()

ext2 = SimpleTextExtractor()
ext2.feed(faq_html)
faq_text = "\n".join(ext2.text_parts)

faq_key_statements = {
    "uscdi_via_portal": "If a patient has access to Tebra's patient portal, he or she has access to the EHI defined by the USCDI",
    "other_ehi": "For other categories of EHI, Tebra can provide access through other means",
    "sharefile": "Tebra utilizes other technologies to provide patient access to EHI, including a secure ShareFile service through which exports of EHI may be shared",
    "request_form_url": "https://www.tebra.com/cures-act-request/",
    "evolving": "As requirements under the Cures Act continue to evolve, Tebra will develop additional processes to facilitate EHI access, exchange, and use"
}

# --- 8. Costs & Guidance - check for (b)(10) ---
costs_text = subprocess.run(
    ["pdftotext", "-layout", str(DOWNLOADS / "costs_and_guidance.pdf"), "-"],
    capture_output=True, text=True
).stdout

costs_mentions_b10 = "b)(10)" in costs_text or "(b)(10)" in costs_text
costs_mentions_ehi = "EHI" in costs_text or "electronic health information" in costs_text.lower()
costs_mentions_b6 = "(b)(6)" in costs_text

# --- Build entity inventory ---
# Since there is NO data dictionary, we construct a minimal inventory from 
# the 19 Cures Act request categories and the 3 export formats described.

entities = []

# The only "entities" we can document are the request form categories
for i, cat in enumerate(cures_act_categories, 1):
    entities.append({
        "id": i,
        "name": cat,
        "source": "Cures Act Request Form (https://www.tebra.com/cures-act-request/)",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "types_documented": False,
        "format": "Unknown - no documentation of export format per category",
        "category": "EHI Request Category",
        "notes": "Selectable category on OneTrust privacy portal form; no field-level detail provided"
    })

# Add the three known export format types
export_formats = [
    {
        "id": 20,
        "name": "C-CDA Summary of Care (XML)",
        "source": "MACRA/MIPS page + Help Center article",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "types_documented": False,
        "format": "XML (C-CDA)",
        "category": "Clinical Records Export",
        "notes": "Individual .ccda files per patient; standard C-CDA content; no vendor-specific field documentation"
    },
    {
        "id": 21,
        "name": "PDF Claims/Billing",
        "source": "MACRA/MIPS page EHI Export paragraph",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "types_documented": False,
        "format": "PDF (non-computable)",
        "category": "Billing Export",
        "notes": "PDFs for claims and billing information; not machine-readable; no field-level detail"
    },
    {
        "id": 22,
        "name": "Native Format Documents",
        "source": "MACRA/MIPS page EHI Export paragraph",
        "fields": [],
        "field_count": 0,
        "fields_with_descriptions": 0,
        "types_documented": False,
        "format": "Original upload format",
        "category": "Document Export",
        "notes": "Documents in the original native format which they were uploaded"
    }
]
entities.extend(export_formats)

# --- Summary statistics ---
summary = {
    "total_entities_documented": 0,
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "ehi_export_documentation_length": len(ehi_paragraph) if ehi_paragraph else 0,
    "ehi_export_documentation_word_count": len(ehi_paragraph.split()) if ehi_paragraph else 0,
    "ehi_paragraph_text": ehi_paragraph,
    "cures_act_request_categories": len(cures_act_categories),
    "cures_act_category_names": cures_act_categories,
    "export_formats": ["C-CDA (XML)", "PDF", "Native format"],
    "fhir_api_resources_g10": fhir_resources_verified,
    "fhir_api_resource_count_g10": len(fhir_resources_verified),
    "general_api_endpoints": gen_api_endpoints,
    "general_api_endpoint_count": len(gen_api_endpoints),
    "rwt_measure4_b10": rwt_measure4,
    "faq_key_statements": faq_key_statements,
    "help_article_facts": help_facts,
    "costs_guidance": {
        "mentions_b10": costs_mentions_b10,
        "mentions_ehi_export": costs_mentions_ehi,
        "mentions_b6": costs_mentions_b6,
        "note": "Outdated (Dec 2022); references Kareo EHR and (b)(6), not (b)(10)"
    },
    "categories_mapping_to_uscdi": {
        "uscdi_aligned": [
            "Allergies and Intolerances",
            "Assessment and Plan of Treatment", 
            "Care Team Members",
            "Clinical Notes",
            "Immunizations",
            "Laboratory Tests & Results",
            "Medications",
            "Patient Demographics",
            "Problems",
            "Procedures",
            "Patient's Implantable Device(s)",
            "Vital Signs",
            "Social History",
        ],
        "beyond_uscdi": [
            "Past Medical History",
            "Past Surgical History",
            "Family History",
            "OB/Pregnancy History",
            "Account/Insurance Information",
            "Documents",
        ],
        "uscdi_aligned_count": 13,
        "beyond_uscdi_count": 6,
    }
}

# Write outputs
with open(OUTPUT / "entity-inventory-full.json", "w") as f:
    json.dump(entities, f, indent=2)

with open(OUTPUT / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print("=== Tebra EHI Export Artifact Analysis ===")
print()
print(f"EHI Export documentation: {summary['ehi_export_documentation_word_count']} words (1 paragraph)")
print(f"Cures Act Request Form categories: {summary['cures_act_request_categories']}")
print(f"  - USCDI-aligned: {summary['categories_mapping_to_uscdi']['uscdi_aligned_count']}")
print(f"  - Beyond USCDI: {summary['categories_mapping_to_uscdi']['beyond_uscdi_count']}")
print(f"Export formats: {', '.join(summary['export_formats'])}")
print(f"Data dictionary: {'Yes' if summary['has_data_dictionary'] else 'NO'}")
print(f"Schema: {'Yes' if summary['has_schema'] else 'NO'}")
print(f"Sample data: {'Yes' if summary['has_sample_data'] else 'NO'}")
print(f"Total fields documented: {summary['total_fields_documented']}")
print()
print(f"FHIR API (g)(10) resources: {summary['fhir_api_resource_count_g10']}")
print(f"General API endpoints: {summary['general_api_endpoint_count']}")
print()
print("RWT Measure #4 (b)(10):")
for k, v in rwt_measure4.items():
    print(f"  {k}: {v}")
print()
print("Cures Act Request Categories:")
for i, cat in enumerate(cures_act_categories, 1):
    print(f"  {i}. {cat}")
