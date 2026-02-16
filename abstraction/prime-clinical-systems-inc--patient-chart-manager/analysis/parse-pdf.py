#!/usr/bin/env python3
"""Parse the EHI Export PDF and extract all structured information.

The PDF is only 3 pages and contains no data dictionary — just file naming
conventions, directory structure, and VB6 code examples. This script extracts
the table names mentioned, file structure details, and produces a structured
JSON inventory of what's documented.
"""

import json
import subprocess
import re

pdf_path = "../downloads/EHI_Export_170.315_b10.pdf"

# Extract text
result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
text = result.stdout

# Extract table/entity names from the PDF text and screenshots
# These are the ADO XML data tables mentioned in the documentation
tables_mentioned = []

# From the XMLDATAExport section (page 1 text + screenshot)
tables_mentioned.append({
    "name": "CHART_DOCS",
    "source": "XMLDATAExport ZIP, page 1 text and screenshot",
    "description_from_pdf": "contains all chart docs details for the exported date and Medical Record Number (MR) range",
    "file_format": "ADO XML recordset",
    "file_name": "CHART_DOCS;DataTable.xml",
    "compressed_size": "2 KB",
    "uncompressed_size": "10 KB",
    "fields": [],
    "field_count": 0,
    "fields_documented": False,
    "notes": "Chart document metadata"
})

tables_mentioned.append({
    "name": "CHART_STORE",
    "source": "XMLDATAExport ZIP, page 1 text and screenshot",
    "description_from_pdf": "contains all chart store details for the exported date and MR number range",
    "file_format": "ADO XML recordset",
    "file_name": "CHART_STORE;DataTable.xml",
    "compressed_size": "1 KB",
    "uncompressed_size": "7 KB",
    "fields": [],
    "field_count": 0,
    "fields_documented": False,
    "notes": "Chart storage details. Fields cs_mr_num and cs_cl_key referenced in naming conventions."
})

tables_mentioned.append({
    "name": "PATIENT",
    "source": "XMLDATAExport ZIP, page 1 text and screenshot",
    "description_from_pdf": "contains all patient data table details for the exported date and MR number range. All patient data tables included (except those hidden via HIDE option)",
    "file_format": "ADO XML recordset",
    "file_name": "PATIENT;DataTable.xml",
    "compressed_size": "4 KB",
    "uncompressed_size": "39 KB",
    "fields": [],
    "field_count": 0,
    "fields_documented": False,
    "notes": "Patient demographics. Fields pa_clinic and pa_account referenced in naming conventions."
})

tables_mentioned.append({
    "name": "PT_ALLERGIES",
    "source": "XMLDATAExport ZIP, page 1 screenshot and page 2 example",
    "description_from_pdf": None,
    "file_format": "ADO XML recordset",
    "file_name": "PT_ALLERGIES;DataTable.xml",
    "compressed_size": "2 KB",
    "uncompressed_size": "11 KB",
    "fields": [],
    "field_count": 0,
    "fields_documented": False,
    "notes": "Patient allergies data"
})

tables_mentioned.append({
    "name": "PT_COMPLAINTS",
    "source": "XMLDATAExport ZIP, page 1 screenshot",
    "description_from_pdf": None,
    "file_format": "ADO XML recordset",
    "file_name": "PT_COMPLAINTS;DataTable.xml",
    "compressed_size": "1 KB",
    "uncompressed_size": "6 KB",
    "fields": [],
    "field_count": 0,
    "fields_documented": False,
    "notes": "Patient complaints/chief complaints"
})

# Additional file visible in page 2 screenshot (CDASUMDATA.Zip contents)
tables_mentioned.append({
    "name": "CDAFULSUM",
    "source": "Page 2 screenshot showing CDASUMDATA.Zip contents",
    "description_from_pdf": None,
    "file_format": "ADO XML recordset",
    "file_name": "303735,9,9,129,CDAFULSUM.xml",
    "compressed_size": "6 KB",
    "uncompressed_size": None,
    "fields": [],
    "field_count": 0,
    "fields_documented": False,
    "notes": "CDA full summary data, visible in screenshot of CDASUMDATA.Zip"
})

# Additional fields referenced in naming conventions (page 2)
referenced_fields = [
    {"table": "PATIENT", "field": "pa_clinic", "context": "naming convention for chart documents"},
    {"table": "PATIENT", "field": "pa_account", "context": "naming convention for chart documents"},
    {"table": "CHART_STORE", "field": "cs_mr_num", "context": "naming convention for chart documents"},
    {"table": "CHART_STORE", "field": "cs_cl_key", "context": "naming convention for chart documents"},
    {"table": "PT_CHART_DOCS", "field": "cd_doc_id", "context": "naming convention, from cdview_cddocid field"},
]

# Export components
export_components = [
    {
        "name": "XMLDATAExport",
        "format": "ZIP containing ADO XML recordset files",
        "description": "Core data export with database tables as XML",
        "always_included": True,
        "tables_visible": ["CHART_DOCS", "CHART_STORE", "PATIENT", "PT_ALLERGIES", "PT_COMPLAINTS"]
    },
    {
        "name": "CDAXMLExport",
        "format": "ZIP containing C-CDA XML files",
        "description": "C-CDA documents, included only with Bulk CCDA Export",
        "always_included": False,
        "condition": "Bulk CCDA Export checkbox selected"
    },
    {
        "name": "CDAXMLDOC",
        "format": "ZIP containing chart document XML files with embedded PDFs in C-CDA format",
        "description": "Chart documents exported as embedded PDFs in CCDA format",
        "always_included": True,
        "notes": "Multiple XML files per patient, one for each chart document"
    },
    {
        "name": "CDASUMDATA",
        "format": "ZIP containing CDA summary XML",
        "description": "CDA full summary data (visible in page 2 screenshot)",
        "always_included": None,
        "notes": "Visible in screenshot but not described in text"
    }
]

inventory = {
    "product": "Patient Chart Manager",
    "vendor": "Prime Clinical Systems, Inc.",
    "version": "7.1.1877",
    "document_date": "12/23/2025",
    "document_title": "Export Format & Naming Conventions",
    "document_pages": 3,
    "source_file": "EHI_Export_170.315_b10.pdf",
    "has_data_dictionary": False,
    "has_field_definitions": False,
    "has_sample_data": False,
    "has_value_sets": False,
    "has_relationship_documentation": False,
    "export_format": "Microsoft ADO XML recordsets (VB6 adPersistXML) + C-CDA R2.1",
    "export_components": export_components,
    "entities": tables_mentioned,
    "entity_count": len(tables_mentioned),
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "referenced_fields": referenced_fields,
    "referenced_field_count": len(referenced_fields),
    "notes": [
        "The PDF contains NO data dictionary — no listing of fields, types, or value sets for any table.",
        "Only 5 table names are visible in the XMLDATAExport screenshot (CHART_DOCS, CHART_STORE, PATIENT, PT_ALLERGIES, PT_COMPLAINTS).",
        "A 6th entity (CDAFULSUM) is visible in a separate screenshot showing CDASUMDATA.Zip contents.",
        "The text states 'All patient data tables included (except those hidden via HIDE option)' but does not enumerate what those tables are.",
        "5 field names are referenced in naming convention examples but no field definitions are provided.",
        "PT_CHART_DOCS is referenced as a data table in the naming convention section but is not visible in the export screenshot.",
        "The document references 'Including and Excluding Data' companion documentation that was not found online.",
        "No billing, medication, lab, immunization, vital signs, or procedure tables are mentioned anywhere.",
        "The ADO XML format is self-describing (embeds schema in each file), so field names/types would be discoverable from actual export files — but none are provided as samples."
    ]
}

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Write summary
summary = {
    "product": inventory["product"],
    "vendor": inventory["vendor"],
    "version": inventory["version"],
    "document_date": inventory["document_date"],
    "has_data_dictionary": False,
    "entity_count": inventory["entity_count"],
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "percent_fields_described": "N/A",
    "export_format": inventory["export_format"],
    "export_components_count": len(export_components),
    "entities_by_category": {
        "patient_data_tables": {
            "count": 5,
            "names": ["CHART_DOCS", "CHART_STORE", "PATIENT", "PT_ALLERGIES", "PT_COMPLAINTS"]
        },
        "cda_summary": {
            "count": 1,
            "names": ["CDAFULSUM"]
        }
    },
    "domains_with_evidence": [
        "Demographics (PATIENT table)",
        "Allergies (PT_ALLERGIES table)",
        "Chief complaints (PT_COMPLAINTS table)",
        "Chart documents/clinical notes (CHART_DOCS, CHART_STORE tables + CDAXMLDOC embedded PDFs)",
        "Clinical summaries (CDAXMLExport C-CDA, CDAFULSUM)"
    ],
    "domains_not_evidenced": [
        "Medications/prescriptions",
        "Lab results",
        "Immunizations",
        "Vital signs",
        "Procedures",
        "Diagnoses/problems (beyond complaints)",
        "Billing/claims",
        "Insurance/coverage",
        "Payments",
        "Orders/referrals",
        "Care plans",
        "Imaging"
    ],
    "critical_ambiguity": "The text claims 'all patient data tables included' but only 5 tables are shown. It is unknown whether additional tables (medications, labs, billing, etc.) exist in the actual export but are simply not listed in this documentation."
}

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Generated entity-inventory-full.json and entity-inventory-summary.json")
print(f"Entities documented: {inventory['entity_count']}")
print(f"Fields documented: {inventory['total_fields_documented']}")
print(f"Export components: {len(export_components)}")
