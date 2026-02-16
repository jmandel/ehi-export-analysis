"""
Extract and structure all content from the ASP.MD EHI export documentation artifacts.
Produces full-entity-inventory.json (minimal in this case) and artifact-analysis.json.
"""
import json
import os
import re
from datetime import datetime

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/asp-md-inc--asp-md-medical-office-system/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/asp-md-inc--asp-md-medical-office-system/analysis"

# 1. Parse the export page (WP API JSON is the cleanest source)
with open(os.path.join(DOWNLOADS, "export-page-wp-api.json"), "r") as f:
    wp_data = json.load(f)

rendered = wp_data["content"]["rendered"]
# Strip HTML tags to get plain text
plain = re.sub(r'<[^>]+>', '\n', rendered)
plain = re.sub(r'\n{2,}', '\n', plain).strip()
export_lines = [l.strip() for l in plain.split('\n') if l.strip()]

export_page_analysis = {
    "source_file": "export-page-wp-api.json",
    "source_url": "https://www.asp.md/export/",
    "page_id": wp_data["id"],
    "title": wp_data["title"]["rendered"],
    "date_published": wp_data["date"],
    "date_modified": wp_data["modified"],
    "never_modified": wp_data["date"] == wp_data["modified"],
    "content_lines": export_lines,
    "total_content_sentences": len(export_lines),
    "mentioned_formats": ["C-CDA", "Text files", "PDF files"],
    "external_links": ["http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf"],
    "folder_structure": "LASTNAME_FIRSTNAME_DOB_MRN (DOB=YYYYMMDD, MRN=integer)",
    "data_dictionary_present": False,
    "schema_present": False,
    "sample_data_present": False,
    "field_level_documentation": False,
    "api_documentation": False,
    "export_initiation_instructions": False,
    "data_domain_specification": False,
}

# 2. Parse the disclosures page for (b)(10) confirmation
with open(os.path.join(DOWNLOADS, "disclosures-page.html"), "r") as f:
    disc_html = f.read()

text = re.sub(r'<script[^>]*>.*?</script>', '', disc_html, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', text)

b10_lines = []
for line in text.split('\n'):
    line = line.strip()
    if 'b)(10' in line or 'export' in line.lower():
        if len(line) > 5:
            b10_lines.append(line)

disclosures_analysis = {
    "source_file": "disclosures-page.html",
    "source_url": "https://www.asp.md/disclosures-2/",
    "b10_mentioned": any('b)(10' in l for l in b10_lines),
    "b10_relevant_lines": b10_lines,
    "additional_export_documentation": False,
    "export_related_links": [],
}

# 3. Compile artifact analysis
artifacts = {
    "analysis_date": datetime.now().isoformat(),
    "artifacts_examined": [
        {
            "file": "export-page.html",
            "type": "HTML",
            "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "export-page.html")),
            "description": "Full HTML of the EHI export documentation page",
            "informative": True,
            "content_summary": "5 lines of text describing 3 export formats and folder naming convention",
        },
        {
            "file": "export-page-wp-api.json",
            "type": "JSON",
            "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "export-page-wp-api.json")),
            "description": "WordPress REST API JSON of the export page",
            "informative": True,
            "content_summary": "Confirms page published 2023-11-14, never modified. Same content as HTML.",
        },
        {
            "file": "export-page-screenshot.png",
            "type": "PNG",
            "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "export-page-screenshot.png")),
            "description": "Full-page screenshot of the export page",
            "informative": True,
            "content_summary": "Confirms visual layout: heading, 5 lines of text, site footer. No hidden content.",
        },
        {
            "file": "disclosures-page.html",
            "type": "HTML",
            "size_bytes": os.path.getsize(os.path.join(DOWNLOADS, "disclosures-page.html")),
            "description": "Mandatory disclosures page",
            "informative": False,
            "content_summary": "Confirms (b)(10) certification listing. No additional export documentation.",
        },
    ],
    "export_page_analysis": export_page_analysis,
    "disclosures_analysis": disclosures_analysis,
}

# 4. Since there is no data dictionary, the "entity inventory" reflects only what is
#    described on the export page (three unnamed output formats)
entity_inventory = {
    "extraction_date": datetime.now().isoformat(),
    "source": "https://www.asp.md/export/",
    "source_type": "web_page",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "total_entities": 0,
    "total_fields": 0,
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "export_formats_mentioned": [
        {
            "format": "C-CDA",
            "description": "C-CDA Documentation referenced via HL7 Companion Guide link",
            "documentation_detail": "External link only (http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf). No vendor-specific mapping, section list, or customization documented.",
            "field_count": "N/A - no vendor-specific field documentation",
        },
        {
            "format": "Text files",
            "description": "Described as 'industry standard'",
            "documentation_detail": "No specification of content, structure, encoding, delimiter, or fields. Completely undefined.",
            "field_count": "N/A",
        },
        {
            "format": "PDF files",
            "description": "Described as 'industry standard'",
            "documentation_detail": "No specification of content or structure. Could be rendered clinical notes, reports, forms, or anything else.",
            "field_count": "N/A",
        },
    ],
    "folder_structure": {
        "pattern": "LASTNAME_FIRSTNAME_DOB_MRN",
        "dob_format": "YYYYMMDD",
        "mrn_description": "integer linking to the MRN in C-CDA",
    },
    "entities": [],
    "notes": "No data dictionary, schema, or entity/field-level documentation exists. The export page describes three output formats without specifying what data each contains.",
}

# Write outputs
with open(os.path.join(OUTPUT_DIR, "artifact-analysis.json"), "w") as f:
    json.dump(artifacts, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), "w") as f:
    json.dump(entity_inventory, f, indent=2)

# Print summary
print("=== ARTIFACT ANALYSIS SUMMARY ===")
print(f"Artifacts examined: {len(artifacts['artifacts_examined'])}")
print(f"Export page content: {export_page_analysis['total_content_sentences']} sentences")
print(f"Formats mentioned: {', '.join(export_page_analysis['mentioned_formats'])}")
print(f"Data dictionary present: {export_page_analysis['data_dictionary_present']}")
print(f"Schema present: {export_page_analysis['schema_present']}")
print(f"Sample data present: {export_page_analysis['sample_data_present']}")
print(f"Field-level documentation: {export_page_analysis['field_level_documentation']}")
print(f"Page published: {export_page_analysis['date_published']}")
print(f"Page modified since publication: {not export_page_analysis['never_modified']}")
print(f"\n=== ENTITY INVENTORY ===")
print(f"Total entities: {entity_inventory['total_entities']}")
print(f"Total fields: {entity_inventory['total_fields']}")
print(f"Fields with descriptions: {entity_inventory['fields_with_descriptions']}")
print(f"\nOutputs written to {OUTPUT_DIR}/")
