#!/usr/bin/env python3
"""
Analyze the SequelMed EHI Export PDF.
Extracts text, counts pages, and summarizes content structure.
"""

import subprocess
import json
import sys

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/sequel-systems-inc--sequelmed-ehr/downloads/SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf"

# Get PDF info
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
info_lines = result.stdout.strip().split("\n")
pdf_info = {}
for line in info_lines:
    if ":" in line:
        key, val = line.split(":", 1)
        pdf_info[key.strip()] = val.strip()

# Extract text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Count content
lines = [l for l in text.split("\n") if l.strip()]
words = len(text.split())

# Identify sections
sections = []
for line in text.split("\n"):
    stripped = line.strip()
    if stripped and (stripped.isupper() or stripped.endswith(":") or stripped.startswith("170.315")):
        if len(stripped) > 5 and len(stripped) < 100:
            sections.append(stripped)

# Document types mentioned
doc_types = [
    "Signed progress notes",
    "available lab results",
    "radiology reports",
    "scanned documents",
    "Imported documents",
    "Iploaded documents"  # sic - typo in original
]

# File formats mentioned
file_formats = [".jpg", ".gif", ".bmp", ".png", ".pdf", ".txt"]

# Export components
export_components = [
    {"name": "Clinical folder", "description": "One XML-based C-CDA file per patient"},
    {"name": "Documents folder", "description": "Patient documents in original format"},
    {"name": "Patient Documents Detail.xls", "description": "Excel file - undocumented contents"}
]

analysis = {
    "pdf_metadata": pdf_info,
    "page_count": int(pdf_info.get("Pages", 0)),
    "file_size_bytes": int(pdf_info.get("File size", "0").replace(" bytes", "")),
    "creator": pdf_info.get("Creator", ""),
    "creation_date": pdf_info.get("CreationDate", ""),
    "content_stats": {
        "non_empty_lines": len(lines),
        "total_words": words,
        "content_pages": 3,  # Page 1 is cover, pages 2-4 have content
        "actual_content_words": words  # Approximate - includes headers/footers
    },
    "export_modes": ["Single patient", "Multi-patient"],
    "export_format": "ZIP per patient",
    "export_components": export_components,
    "clinical_data_format": "C-CDA XML (USCDI V1)",
    "ccda_specs_referenced": [
        "HL7 CDA Release 2: IHE Health Story Consolidation, DSTU Release 1.1 (July 2012)",
        "HL7 CDA Release 2: Consolidated CDA Templates R2.1 (August 2015, June 2019 with Errata)",
        "HL7 CDA R2 IG: C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2 (October 2019)"
    ],
    "document_types_listed": doc_types,
    "document_formats": file_formats,
    "data_dictionary": False,
    "field_level_documentation": False,
    "sample_data": False,
    "schema_provided": False,
    "screenshots": False,
    "value_sets_documented": False,
    "relationships_documented": False,
    "typos": ["'Iploaded' instead of 'Uploaded' on page 3"],
    "notable_gaps": [
        "No data dictionary or field-level documentation",
        "No sample data or example exports",
        "No schema files or machine-readable documentation",
        "No description of Patient Documents Detail.xls contents",
        "No mention of billing/PM data export",
        "No mention of scheduling data export",
        "No mention of specialty-specific clinical template data",
        "No mention of orders data",
        "No mention of e-prescribing history",
        "No mention of insurance/coverage data beyond C-CDA",
        "No mention of patient portal data"
    ]
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/sequel-systems-inc--sequelmed-ehr/analysis/pdf_analysis.json"
with open(output_path, "w") as f:
    json.dump(analysis, f, indent=2)

print(json.dumps(analysis, indent=2))
