"""
Parse the EHI Export PDF for ezPractice and extract structured information.
Outputs summary statistics about the documentation.
"""
import subprocess
import json
import re

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/perk-medical-systems-llc-pcb-apps-llc--ezpractice/downloads/EHI Export.pdf"

# Get PDF info
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
pdf_info = {}
for line in result.stdout.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        pdf_info[key.strip()] = val.strip()

# Extract text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Count sections
sections = re.findall(r'^[A-Z][A-Za-z &/]+$', text, re.MULTILINE)

# Identify the CSV field documentation (patient notes)
csv_fields = []
# Parse the table from the PDF text
in_table = False
for line in text.split("\n"):
    if "Column Number" in line and "Column Name" in line:
        in_table = True
        continue
    if in_table:
        # Match lines with column number at start
        match = re.match(r'\s+(\d+)\s+(\S[\w\s]+?)\s{3,}(.+)', line)
        if match:
            csv_fields.append({
                "column_number": int(match.group(1)),
                "column_name": match.group(2).strip(),
                "description": match.group(3).strip()
            })
        if "Scanned Records" in line:
            in_table = False

# Export file categories described
export_categories = [
    {
        "category": "Patient Demographics and Clinical Data",
        "format": "HL7 C-CDA R2.1 XML + HTML rendering",
        "file_type_indicator": "(none - no TYPE in filename)",
        "documentation_depth": "Defers entirely to C-CDA R2.1 specification; no field-level documentation"
    },
    {
        "category": "Adhoc Patient Notes",
        "format": "CSV",
        "file_type_indicator": "patNotes",
        "documentation_depth": f"{len(csv_fields)} columns documented with descriptions"
    },
    {
        "category": "Scanned Records",
        "format": "HL7 CDA XML with Base64 encoding",
        "file_type_indicator": "Echart",
        "documentation_depth": "Defers to CDA specification; no field-level documentation"
    },
    {
        "category": "Claim Data",
        "format": "Unknown (mentioned in naming convention only)",
        "file_type_indicator": "Claim Data",
        "documentation_depth": "Mentioned as a TYPE value but completely undocumented - no format, no fields, no description"
    }
]

# File naming conventions
naming = {
    "pattern": "PID_INTERNALNUMBERING.EXT or PID_INTERNALNUMBERING_TYPE.EXT",
    "type_values_mentioned": ["Claim Data", "Echart", "patNotes"],
    "extensions_mentioned": ["XML", "HTML", "CSV"]
}

# Product portfolio from executive summary
product_portfolio = {
    "products": [
        "Certified Health Information Technology – EHR",
        "Practice Management",
        "Patient Portal",
        "Health Information Exchange"
    ],
    "services": [
        "Revenue Cycle Management",
        "Professional Services"
    ]
}

output = {
    "pdf_metadata": pdf_info,
    "total_pages": int(pdf_info.get("Pages", 0)),
    "substantive_pages": 3,  # Pages 4-6 after cover, copyright, TOC
    "csv_fields_documented": csv_fields,
    "csv_field_count": len(csv_fields),
    "export_categories": export_categories,
    "naming_convention": naming,
    "product_portfolio": product_portfolio,
    "total_entities_documented": 0,  # No data dictionary
    "total_fields_documented": len(csv_fields),  # Only CSV fields
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema": False,
    "export_format": "Mixed: C-CDA R2.1 XML, CSV, CDA XML",
    "model_type": "Standard-based projection (C-CDA)",
    "notes": [
        "PDF has a column numbering error: columns 3 and 4 are both labeled '3' in the table",
        "Claim Data is mentioned as a TYPE value but has zero documentation",
        "Clinical data documentation defers entirely to external C-CDA R2.1 spec",
        "No sample data, no schemas, no machine-readable artifacts"
    ]
}

with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/perk-medical-systems-llc-pcb-apps-llc--ezpractice/analysis/pdf_analysis.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
