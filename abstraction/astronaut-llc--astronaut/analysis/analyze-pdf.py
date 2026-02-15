"""
Analyze the Astronaut EHR Export Format Documentation PDF.
Extracts structured information about sections, format details, and documentation depth.
"""

import json
import re

# Read the extracted PDF text
with open("pdf-text-output.txt", "r") as f:
    text = f.read()

# Count pages (from pdfinfo: 10 pages)
page_count = 10

# Extract C-CDA sections listed in the document
ccda_sections = [
    "Allergies",
    "Immunizations",
    "Medications",
    "Plan of Treatment",
    "Goals",
    "Problem(s)",
    "Results (Lab)",
    "Vitals",
    "Procedures",
    "Social History",
    "Encounters",
    "Functional Status",
    "Medical Equipment",
    "Assessments",
]

# Additional sections mentioned
other_sections = [
    "Header Section (demographics, author info, timestamps)",
    "Advanced Demographics and Remaining EHI (CSV supplement)",
]

# What's NOT in the documentation
missing_documentation_elements = [
    "No data dictionary or field-level definitions",
    "No schema files (XSD, JSON Schema)",
    "No sample export files (C-CDA or CSV)",
    "No value set definitions or code system references",
    "No mapping between VistA/FileMan internal data model and C-CDA output",
    "No field names, data types, or cardinality specifications",
    "No foreign key or relationship documentation",
    "No CSV field listing beyond one fictional demographic example",
]

# CSV example fields mentioned
csv_example_fields = [
    "Place of Birth",
    "Mother's Maiden Name",
    "Spouse's Employer Name",
    "Date of Retirement",
]

# Word count of actual substantive content (excluding boilerplate, ToC, XML examples)
lines = text.strip().split("\n")
non_empty_lines = [l for l in lines if l.strip() and "Copyright" not in l]
word_count = sum(len(l.split()) for l in non_empty_lines)

# Count XML example lines vs prose lines
xml_lines = [l for l in lines if l.strip().startswith("<") or l.strip().startswith("<!--")]
prose_lines = [l for l in non_empty_lines if not l.strip().startswith("<") and not l.strip().startswith("<!--")]

results = {
    "pdf_metadata": {
        "title": "Astronaut EHR Export Format Documentation",
        "pages": page_count,
        "file_size_bytes": 222805,
        "producer": "Google Docs Renderer",
        "copyright_year": 2023,
    },
    "export_format": {
        "primary": "C-CDA (XML)",
        "secondary": "Proprietary CSV (name-value pairs)",
        "description": "Dual format: C-CDA for clinical data, CSV for 'advanced demographics and remaining EHI'",
    },
    "access_mechanism": {
        "method": "FHIR server extraction (IT staff-assisted)",
        "single_patient": True,
        "bulk_export": True,
        "self_service": False,
        "description": "Authorized user must be granted permission by Astronaut EHR IT staff who walk user through extraction",
    },
    "ccda_sections": ccda_sections,
    "ccda_section_count": len(ccda_sections),
    "other_sections": other_sections,
    "total_sections_documented": len(ccda_sections) + len(other_sections),
    "csv_supplement": {
        "format": "name-value pairs (comma-separated)",
        "example_fields": csv_example_fields,
        "example_field_count": len(csv_example_fields),
        "description": "Only demographic fields shown in example; claims to cover 'all available data'",
    },
    "documentation_gaps": missing_documentation_elements,
    "documentation_gap_count": len(missing_documentation_elements),
    "content_metrics": {
        "total_lines": len(lines),
        "non_empty_lines": len(non_empty_lines),
        "xml_example_lines": len(xml_lines),
        "prose_lines": len(prose_lines),
        "approx_word_count": word_count,
    },
    "entities_defined": 0,
    "fields_defined": 0,
    "fields_with_descriptions": 0,
    "sample_data_provided": False,
    "schema_provided": False,
    "data_dictionary_provided": False,
}

# Save results
with open("pdf-analysis-results.json", "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("=" * 60)
print("Astronaut EHR Export Format Documentation Analysis")
print("=" * 60)
print(f"PDF pages: {page_count}")
print(f"Approximate word count: {word_count}")
print(f"Export format: C-CDA (XML) + proprietary CSV")
print(f"C-CDA sections documented: {len(ccda_sections)}")
print(f"CSV example fields: {len(csv_example_fields)}")
print(f"Entities/tables defined: 0")
print(f"Fields defined: 0")
print(f"Data dictionary: No")
print(f"Schema files: No")
print(f"Sample data: No")
print(f"Documentation gaps: {len(missing_documentation_elements)}")
print()
print("C-CDA Sections:")
for i, s in enumerate(ccda_sections, 1):
    print(f"  {i:2d}. {s}")
print()
print("Documentation gaps:")
for g in missing_documentation_elements:
    print(f"  - {g}")
print()
print("CSV example fields (only ones shown in doc):")
for f_name in csv_example_fields:
    print(f"  - {f_name}")
