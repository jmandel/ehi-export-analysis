#!/usr/bin/env python3
"""Parse the Astronaut EHR Export Format Documentation PDF and extract
structured information about documented C-CDA sections and the CSV supplement."""

import json
import subprocess
import re

PDF_PATH = "../../../results/astronaut-llc--astronaut/downloads/Astronaut-EHR-Export-Format-Documentation.pdf"

# Extract text
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
text = result.stdout

# Extract PDF metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH],
    capture_output=True, text=True
)

# Parse pages
pages = text.split("\x0c")
total_pages = len([p for p in pages if p.strip()])

# Define the C-CDA sections documented
ccda_sections = [
    "Allergies",
    "Immunizations",
    "Medications",
    "Plan of Treatment",
    "Goals",
    "Problems",
    "Results (Lab)",
    "Vitals",
    "Procedures",
    "Social History",
    "Encounters",
    "Functional Status",
    "Medical Equipment",
    "Assessments",
]

# The "Header" section covers demographics
header_section = "Header (Demographics, Author, Timestamps)"
csv_section = "Advanced Demographics and Remaining EHI (CSV)"

# Check for data dictionary elements
has_field_names = False
has_data_types = False
has_descriptions = False  # Section-level only
has_value_sets = False
has_relationships = False
has_sample_data = False
has_schema = False

# Check text for any field-level detail
field_pattern = re.compile(r'(field|column|attribute|property)\s*name', re.I)
type_pattern = re.compile(r'data\s*type|varchar|integer|boolean|string|number', re.I)
has_field_names = bool(field_pattern.search(text))
has_data_types = bool(type_pattern.search(text))

# Count words in section descriptions (rough measure of documentation depth)
section_word_counts = {}
for section in ccda_sections:
    # Find the section header and extract text until next section
    pattern = re.compile(
        rf'^{re.escape(section)}.*?\n(.*?)(?=\n(?:{"|".join(re.escape(s) for s in ccda_sections)}|Advanced Demographics|Acknowledgements))',
        re.DOTALL | re.MULTILINE
    )
    match = pattern.search(text)
    if match:
        desc = match.group(1).strip()
        words = len(desc.split())
        section_word_counts[section] = words

output = {
    "pdf_metadata": {
        "title": "Astronaut EHR Export Format Documentation",
        "pages": total_pages,
        "producer": "Google Docs Renderer",
        "copyright": "2023, Astronaut, LLC",
        "file_size_bytes": 222805,
    },
    "export_format": {
        "primary": "C-CDA (XML)",
        "supplemental": "Proprietary CSV (name-value pairs)",
        "mechanism": "FHIR server extraction with IT staff assistance",
        "single_patient": True,
        "bulk_export": True,
    },
    "ccda_sections": [
        {"name": header_section, "type": "ccda_header"},
    ] + [
        {"name": s, "type": "ccda_section", "description_word_count": section_word_counts.get(s, 0)}
        for s in ccda_sections
    ] + [
        {"name": csv_section, "type": "csv_supplement"},
    ],
    "documentation_quality": {
        "has_data_dictionary": False,
        "has_field_level_definitions": False,
        "has_data_types": has_data_types,
        "has_value_sets": False,
        "has_relationships": False,
        "has_sample_export_files": False,
        "has_machine_readable_schema": False,
        "has_field_names": has_field_names,
        "documentation_level": "section-level summaries only",
        "total_sections_documented": len(ccda_sections) + 2,  # +header +CSV
        "total_fields_documented": 0,  # No field-level documentation
        "csv_example_fields": [
            "Place of Birth",
            "Mother's Maiden Name",
            "Spouse's Employer Name",
            "Date of Retirement",
        ],
    },
    "coverage_claims": {
        "clinical_via_ccda": True,
        "remaining_ehi_via_csv": True,
        "billing_mentioned": False,
        "scheduling_mentioned": False,
        "e_prescribing_mentioned": False,
        "orders_mentioned": True,  # Plan of Treatment covers pending orders
        "notes_mentioned": False,  # No explicit clinical notes section
        "images_mentioned": False,
        "consults_mentioned": False,
        "scope_reference": "45 CFR 164.502 designated record set, excluding psychotherapy notes",
    },
}

# Write output
with open("full-entity-inventory.json", "w") as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))

# Summary stats
print("\n=== SUMMARY ===")
print(f"PDF pages: {total_pages}")
print(f"C-CDA sections documented: {len(ccda_sections)}")
print(f"Additional sections: Header + CSV supplement = 2")
print(f"Total sections: {len(ccda_sections) + 2}")
print(f"Field-level definitions: 0")
print(f"Sample export files: 0")
print(f"Machine-readable schemas: 0")
print(f"CSV example fields shown: {len(output['documentation_quality']['csv_example_fields'])}")
for s, wc in section_word_counts.items():
    print(f"  {s}: ~{wc} words of description")
