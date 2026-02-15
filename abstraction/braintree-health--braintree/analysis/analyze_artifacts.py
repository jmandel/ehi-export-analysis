#!/usr/bin/env python3
"""Analyze Braintree Health EHI export artifacts and produce structured inventory."""

import json
import re
import os
from pathlib import Path

DOWNLOADS = Path("/home/jmandel/hobby/ehi-export-analysis/results/braintree-health--braintree/downloads")
OUTPUT = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/braintree-health--braintree/analysis")

def analyze_certification_page():
    """Extract and analyze the b(10) section from the certification page HTML."""
    with open(DOWNLOADS / "certification-page.html") as f:
        content = f.read()

    # Extract b(10) section
    match = re.search(
        r'<h3>Electronic Health Information export b\(10\)</h3>(.*?)(?=<h3>|$)',
        content, re.DOTALL
    )
    if not match:
        return {"error": "b(10) section not found"}

    section_html = match.group(1)
    # Extract bullet points
    bullets = re.findall(r'<li>(.*?)</li>', section_html, re.DOTALL)
    bullets = [re.sub(r'<[^>]+>', '', b).strip() for b in bullets]

    # Extract intro paragraph
    paragraphs = re.findall(r'<p>(.*?)</p>', section_html, re.DOTALL)
    paragraphs = [re.sub(r'<[^>]+>', '', p).strip() for p in paragraphs if p.strip() and p.strip() != '&nbsp;']

    return {
        "heading": "Electronic Health Information export b(10)",
        "paragraphs": paragraphs,
        "bullet_points": bullets,
        "bullet_count": len(bullets),
        "total_words": sum(len(b.split()) for b in bullets) + sum(len(p.split()) for p in paragraphs)
    }


def analyze_fhir_resources():
    """Count and list FHIR resources documented in the API PDF."""
    import subprocess
    result = subprocess.run(
        ["pdftotext", "-layout", str(DOWNLOADS / "Braintree-FHIR-API-Documentation-1.pdf"), "-"],
        capture_output=True, text=True
    )
    text = result.stdout

    # Extract unique resource types from "Request:" lines
    resources = set()
    for line in text.split('\n'):
        m = re.match(r'^Request\s*:\s*(.+?)(?:\s*\.{2,}.*)?$', line.strip())
        if m:
            name = m.group(1).strip().rstrip('.')
            if name:
                resources.add(name)

    return {
        "pdf_pages": 76,
        "resources": sorted(resources),
        "resource_count": len(resources),
    }


def analyze_all_links():
    """Extract all downloadable file links from the certification page."""
    with open(DOWNLOADS / "certification-page.html") as f:
        content = f.read()

    links = re.findall(
        r'href=["\']([^"\']*\.(?:pdf|zip|xlsx|csv|json|doc|docx|htm|html)[^"\']*)["\']',
        content, re.IGNORECASE
    )
    categorized = []
    for url in links:
        filename = url.split('/')[-1]
        if 'fhir' in filename.lower() or 'fhir' in url.lower():
            category = "FHIR/g(10)"
        elif 'rwt' in filename.lower() or 'real-world' in filename.lower() or 'testplan' in filename.lower():
            category = "Real World Testing"
        elif 'transparency' in filename.lower():
            category = "Cost Transparency"
        elif 'terms' in filename.lower() or 'access-application' in filename.lower():
            category = "Administrative"
        else:
            category = "Other"
        categorized.append({"url": url, "filename": filename, "category": category})

    return {
        "total_links": len(categorized),
        "ehi_export_specific_links": sum(1 for l in categorized if 'ehi' in l['filename'].lower() or 'b10' in l['filename'].lower()),
        "links": categorized
    }


def analyze_artifacts():
    """Inventory all downloaded artifacts."""
    artifacts = []
    for f in sorted(DOWNLOADS.iterdir()):
        info = {
            "filename": f.name,
            "size_bytes": f.stat().st_size,
            "extension": f.suffix.lower(),
        }
        if f.suffix.lower() == '.html':
            with open(f) as fh:
                content = fh.read()
            info["type"] = "HTML"
            info["size_chars"] = len(content)
        elif f.suffix.lower() == '.pdf':
            import subprocess
            result = subprocess.run(["pdfinfo", str(f)], capture_output=True, text=True)
            pages_match = re.search(r'Pages:\s+(\d+)', result.stdout)
            info["type"] = "PDF"
            info["pages"] = int(pages_match.group(1)) if pages_match else None
        elif f.suffix.lower() == '.png':
            info["type"] = "Screenshot"
        elif f.suffix.lower() == '.htm':
            info["type"] = "HTML (Excel export)"
        artifacts.append(info)

    return artifacts


def build_export_format_inventory():
    """Summarize what the b(10) export claims to include based on bullet points."""
    return {
        "export_formats": [
            {
                "data_category": "General EHI (images, documents, reports)",
                "format": "HTML/PDF",
                "notes": "Human-readable format where applicable"
            },
            {
                "data_category": "Patient demographics",
                "format": "C-CDA XML",
                "notes": "Standard clinical document format"
            },
            {
                "data_category": "Consent forms",
                "format": "HTML",
                "notes": "Human-readable"
            },
            {
                "data_category": "Clinical and billing reports, encounter documentation",
                "format": "PDF",
                "notes": "Described as 'computable format'"
            },
            {
                "data_category": "Patient attachments",
                "format": "Original format",
                "notes": "As uploaded into EMR"
            },
            {
                "data_category": "Patient images",
                "format": "DICOM",
                "notes": "Medical imaging standard"
            }
        ],
        "total_categories": 6,
        "has_data_dictionary": False,
        "has_sample_data": False,
        "has_schema": False,
        "has_field_documentation": False,
        "has_user_guide": False,
        "has_export_instructions": False
    }


if __name__ == "__main__":
    results = {
        "b10_section": analyze_certification_page(),
        "fhir_api": analyze_fhir_resources(),
        "downloadable_links": analyze_all_links(),
        "artifacts": analyze_artifacts(),
        "export_inventory": build_export_format_inventory(),
    }

    output_file = OUTPUT / "artifact_analysis.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("=== Braintree Health EHI Export Artifact Analysis ===\n")

    b10 = results["b10_section"]
    print(f"b(10) Section:")
    print(f"  Bullet points: {b10['bullet_count']}")
    print(f"  Total words: {b10['total_words']}")
    print(f"  Paragraphs: {len(b10['paragraphs'])}")
    for i, b in enumerate(b10['bullet_points'], 1):
        print(f"  [{i}] {b}")

    print(f"\nFHIR API (g(10)) Resources: {results['fhir_api']['resource_count']}")
    for r in results['fhir_api']['resources']:
        print(f"  - {r}")

    print(f"\nDownloadable Links on Cert Page: {results['downloadable_links']['total_links']}")
    print(f"  EHI-export-specific links: {results['downloadable_links']['ehi_export_specific_links']}")
    for link in results['downloadable_links']['links']:
        print(f"  [{link['category']}] {link['filename']}")

    print(f"\nArtifacts in downloads/:")
    for a in results['artifacts']:
        extra = f" ({a.get('pages', '')} pages)" if a.get('pages') else ""
        print(f"  {a['filename']} - {a['size_bytes']:,} bytes{extra}")

    print(f"\nExport Documentation Completeness:")
    inv = results['export_inventory']
    print(f"  Data dictionary: {'Yes' if inv['has_data_dictionary'] else 'No'}")
    print(f"  Sample data: {'Yes' if inv['has_sample_data'] else 'No'}")
    print(f"  Schema: {'Yes' if inv['has_schema'] else 'No'}")
    print(f"  Field documentation: {'Yes' if inv['has_field_documentation'] else 'No'}")
    print(f"  User guide: {'Yes' if inv['has_user_guide'] else 'No'}")
    print(f"  Export instructions: {'Yes' if inv['has_export_instructions'] else 'No'}")
    print(f"  Export format categories described: {inv['total_categories']}")

    print(f"\nResults saved to: {output_file}")
