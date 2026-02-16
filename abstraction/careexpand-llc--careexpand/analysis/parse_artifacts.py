#!/usr/bin/env python3
"""
Analyze all EHI export artifacts for Careexpand.
Parses the HTML, markdown, and PDF documentation to extract hard numbers.
"""

import json
import os
from html.parser import HTMLParser

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/careexpand-llc--careexpand"
DOWNLOADS_DIR = os.path.join(RESULTS_DIR, "downloads")
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data dictionary fields extracted from the PNG image (manually verified)
DATA_DICTIONARY_FIELDS = [
    {"field": "patient_name", "description": "Full name of the patient", "data_type": "String", "required": True},
    {"field": "dob", "description": "Date of birth of the patient", "data_type": "Date (YYYY-MM-DD)", "required": True},
    {"field": "gender", "description": "Patient's gender", "data_type": "String (M/F/Other)", "required": True},
    {"field": "race", "description": "Race of the patient", "data_type": "String", "required": False},
    {"field": "ethnicity", "description": "Ethnicity of the patient", "data_type": "String", "required": False},
    {"field": "language", "description": "Preferred language of communication", "data_type": "String", "required": False},
    {"field": "address", "description": "Patient's home address", "data_type": "String", "required": False},
    {"field": "phone", "description": "Contact number", "data_type": "String", "required": False},
    {"field": "emergency_contact", "description": "Emergency contact name and phone", "data_type": "String", "required": False},
    {"field": "smoking_status", "description": "Patient's smoking habits", "data_type": "String", "required": False},
    {"field": "problem_list", "description": "List of active and past medical problems", "data_type": "Array (Structured)", "required": True},
    {"field": "medications", "description": "Active and past medications", "data_type": "Array (Structured)", "required": True},
    {"field": "allergies", "description": "Patient allergies", "data_type": "Array (Structured)", "required": True},
    {"field": "lab_results", "description": "Laboratory test results", "data_type": "Array (Structured)", "required": False},
    {"field": "procedures", "description": "Medical procedures performed", "data_type": "Array (Structured)", "required": False},
    {"field": "encounters", "description": "Clinical encounters and visits", "data_type": "Array (Structured)", "required": True},
    {"field": "vital_signs", "description": "Blood pressure, heart rate, temperature, etc.", "data_type": "Array (Structured)", "required": False},
]

def analyze_html():
    """Analyze the HTML export for structure."""
    path = os.path.join(DOWNLOADS_DIR, "b10-ehi-export-ccda.html")
    with open(path) as f:
        content = f.read()
    
    class Counter(HTMLParser):
        def __init__(self):
            super().__init__()
            self.tables = 0
            self.images = 0
            self.code_blocks = 0
            self.headings = []
            self.in_heading = False
            self.heading_tag = ''
            self.heading_text = ''
        def handle_starttag(self, tag, attrs):
            if tag == 'table': self.tables += 1
            if tag == 'img': self.images += 1
            if tag == 'pre': self.code_blocks += 1
            if tag in ('h1','h2','h3','h4','h5'):
                self.in_heading = True
                self.heading_tag = tag
                self.heading_text = ''
        def handle_data(self, data):
            if self.in_heading:
                self.heading_text += data
        def handle_endtag(self, tag):
            if self.in_heading and tag == self.heading_tag:
                self.headings.append({"level": self.heading_tag, "text": self.heading_text.strip()})
                self.in_heading = False
    
    c = Counter()
    c.feed(content)
    return {
        "file": "b10-ehi-export-ccda.html",
        "size_bytes": len(content),
        "tables": c.tables,
        "images": c.images,
        "code_blocks": c.code_blocks,
        "headings": c.headings,
    }

def analyze_artifacts():
    """Produce a comprehensive artifact inventory."""
    files = []
    for fname in sorted(os.listdir(DOWNLOADS_DIR)):
        fpath = os.path.join(DOWNLOADS_DIR, fname)
        size = os.path.getsize(fpath)
        files.append({"filename": fname, "size_bytes": size, "size_human": f"{size/1024:.1f} KB"})
    return files

def summarize_data_dictionary():
    """Summarize the data dictionary fields."""
    total = len(DATA_DICTIONARY_FIELDS)
    required = sum(1 for f in DATA_DICTIONARY_FIELDS if f["required"])
    optional = total - required
    string_fields = sum(1 for f in DATA_DICTIONARY_FIELDS if f["data_type"].startswith("String"))
    array_fields = sum(1 for f in DATA_DICTIONARY_FIELDS if f["data_type"].startswith("Array"))
    date_fields = sum(1 for f in DATA_DICTIONARY_FIELDS if f["data_type"].startswith("Date"))
    described = sum(1 for f in DATA_DICTIONARY_FIELDS if f["description"])

    # Categorize by domain
    demographic_fields = ["patient_name", "dob", "gender", "race", "ethnicity", "language", "address", "phone", "emergency_contact"]
    social_fields = ["smoking_status"]
    clinical_fields = ["problem_list", "medications", "allergies", "lab_results", "procedures", "encounters", "vital_signs"]

    return {
        "total_fields": total,
        "required_fields": required,
        "optional_fields": optional,
        "fields_with_descriptions": described,
        "description_pct": f"{described/total*100:.0f}%",
        "type_breakdown": {
            "String": string_fields,
            "Array (Structured)": array_fields,
            "Date": date_fields,
        },
        "domain_breakdown": {
            "Demographics": len(demographic_fields),
            "Social History": len(social_fields),
            "Clinical (structured arrays)": len(clinical_fields),
        },
        "fields": DATA_DICTIONARY_FIELDS,
    }

def main():
    results = {
        "product": "Careexpand",
        "analysis_date": "2026-02-15",
        "artifacts": analyze_artifacts(),
        "html_structure": analyze_html(),
        "data_dictionary": summarize_data_dictionary(),
        "key_findings": {
            "export_format": "C-CDA 2.1 XML",
            "total_documented_fields": 17,
            "data_dictionary_format": "PNG image (not machine-readable)",
            "documentation_pages": 4,
            "documentation_source": "Single BookStack wiki page",
            "sample_data_provided": False,
            "schema_files_provided": False,
            "bulk_export_support": "unclear (single-patient API only documented)",
            "native_data_model": False,
            "is_standard_projection": True,
        }
    }

    output_path = os.path.join(OUTPUT_DIR, "artifact-analysis.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("=" * 60)
    print("CAREEXPAND EHI EXPORT ARTIFACT ANALYSIS")
    print("=" * 60)
    print(f"\nArtifacts in downloads/:")
    for a in results["artifacts"]:
        print(f"  {a['filename']:40s} {a['size_human']:>10s}")
    
    print(f"\nHTML Structure:")
    hs = results["html_structure"]
    print(f"  Size: {hs['size_bytes']} bytes")
    print(f"  Tables: {hs['tables']} (data dictionary is an image, not a table)")
    print(f"  Images: {hs['images']} (the data dictionary PNG)")
    print(f"  Code blocks: {hs['code_blocks']}")
    print(f"  Headings: {len(hs['headings'])}")
    
    dd = results["data_dictionary"]
    print(f"\nData Dictionary:")
    print(f"  Total fields: {dd['total_fields']}")
    print(f"  Required: {dd['required_fields']}, Optional: {dd['optional_fields']}")
    print(f"  Fields with descriptions: {dd['fields_with_descriptions']} ({dd['description_pct']})")
    print(f"  Type breakdown: {dd['type_breakdown']}")
    print(f"  Domain breakdown: {dd['domain_breakdown']}")
    
    kf = results["key_findings"]
    print(f"\nKey Findings:")
    for k, v in kf.items():
        print(f"  {k}: {v}")
    
    print(f"\nFull results saved to: {output_path}")

if __name__ == "__main__":
    main()
