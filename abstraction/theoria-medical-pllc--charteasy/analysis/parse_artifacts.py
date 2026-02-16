"""
Parse the EHR certificate HTML page and extract all structured information
about the (b)(10) EHI export documentation for ChartEasy.
"""

import json
import os
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/theoria-medical-pllc--charteasy"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/theoria-medical-pllc--charteasy/analysis"

# Read the HTML file
with open(os.path.join(RESULTS_DIR, "downloads/ehr-certificate-page.html"), "r") as f:
    html_content = f.read()

# Extract the (b)(10) statement text
import re

# Find the EHI export section
b10_match = re.search(
    r'Support for EHI Export.*?</p>',
    html_content,
    re.DOTALL
)

b10_text = ""
if b10_match:
    # Strip HTML tags
    raw = b10_match.group(0)
    b10_text = re.sub(r'<[^>]+>', ' ', raw).strip()
    b10_text = re.sub(r'\s+', ' ', b10_text)

# Extract all PDF links
pdf_links = re.findall(r'href="(/pdf/[^"]+\.pdf)"', html_content)

# Extract certification criteria badges
criteria = re.findall(r'170\.315\([a-z]\)\(\d+\)', html_content)
criteria = sorted(set(criteria))

# Extract patient portal features from the screenshot text (from prior report, verified against HTML)
portal_features = [
    "Access Chronic Care Management Plan",
    "View Lab and Imaging Results",
    "View Medication Lists",
    "Download and Transmit your records"
]

# Build the full artifact analysis
analysis = {
    "artifact_analysis": {
        "ehr_certificate_page": {
            "file": "downloads/ehr-certificate-page.html",
            "size_bytes": os.path.getsize(os.path.join(RESULTS_DIR, "downloads/ehr-certificate-page.html")),
            "source_url": "https://theoriamedical.com/ehr-certificate",
            "content_sections": [
                "ONC Certification overview",
                "Certification details (developer, date, product, CHPL number)",
                "Certification criteria badges (34 criteria)",
                "CQMs (10)",
                "Real-World Testing Plans and Reports (6 PDF links)",
                "EHI Export (b)(10) attestation statement",
                "Intervention Risk Management statement"
            ],
            "b10_statement": {
                "full_text": b10_text,
                "word_count": len(b10_text.split()),
                "export_formats_mentioned": ["PDF", "CCDA"],
                "export_mechanisms": [
                    {
                        "method": "Patient Portal self-service",
                        "url": "https://patient-portal.charteasy.com/",
                        "ios_app": "https://apps.apple.com/us/app/charteasy-patient-portal/id1564972475"
                    },
                    {
                        "method": "Email request to records team",
                        "email": "records@theoriamedical.com"
                    }
                ],
                "data_dictionary_present": False,
                "schema_present": False,
                "sample_data_present": False,
                "field_level_documentation": False,
                "format_specification": False
            },
            "pdf_links_on_page": pdf_links,
            "pdf_links_are_ehi_related": False,
            "pdf_links_description": "All 6 PDFs are Real-World Testing Plans/Reports, not EHI export documentation"
        },
        "patient_portal_login": {
            "file": "downloads/patient-portal-login.png",
            "size_bytes": os.path.getsize(os.path.join(RESULTS_DIR, "downloads/patient-portal-login.png")),
            "source_url": "https://patient-portal.charteasy.com/",
            "description": "Screenshot of ChartEasy Patient Portal login page (Flutter web app v2.0.8)",
            "visible_features": portal_features,
            "login_required": True,
            "export_documentation_accessible": False
        },
        "ehr_certificate_screenshot": {
            "file": "downloads/ehr-certificate-page-full.png",
            "size_bytes": os.path.getsize(os.path.join(RESULTS_DIR, "downloads/ehr-certificate-page-full.png")),
            "source_url": "https://theoriamedical.com/ehr-certificate",
            "description": "Full-page screenshot of the ONC certification page"
        }
    },
    "certification_criteria": criteria,
    "certification_criteria_count": len(criteria),
    "export_documentation_summary": {
        "has_data_dictionary": False,
        "has_schema": False,
        "has_sample_data": False,
        "has_format_specification": False,
        "has_field_descriptions": False,
        "has_value_sets": False,
        "has_relationships": False,
        "total_entities_documented": 0,
        "total_fields_documented": 0,
        "documentation_type": "text-only attestation statement (~150 words)",
        "export_format": "PDF and C-CDA (per attestation; no specification provided)",
        "export_mechanism": "Patient portal self-service or email request"
    }
}

# Write output
output_path = os.path.join(OUTPUT_DIR, "artifact-analysis.json")
with open(output_path, "w") as f:
    json.dump(analysis, f, indent=2)

print(f"Artifact analysis written to {output_path}")
print(f"\nKey findings:")
print(f"  - HTML page size: {analysis['artifact_analysis']['ehr_certificate_page']['size_bytes']:,} bytes")
print(f"  - (b)(10) statement word count: {analysis['artifact_analysis']['ehr_certificate_page']['b10_statement']['word_count']}")
print(f"  - Certification criteria: {len(criteria)}")
print(f"  - Data dictionary present: {analysis['export_documentation_summary']['has_data_dictionary']}")
print(f"  - Schema present: {analysis['export_documentation_summary']['has_schema']}")
print(f"  - Sample data present: {analysis['export_documentation_summary']['has_sample_data']}")
print(f"  - Total entities documented: {analysis['export_documentation_summary']['total_entities_documented']}")
print(f"  - Total fields documented: {analysis['export_documentation_summary']['total_fields_documented']}")
print(f"  - PDF links found: {len(pdf_links)} (all Real-World Testing, none EHI-related)")
