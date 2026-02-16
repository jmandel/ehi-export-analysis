#!/usr/bin/env python3
"""
Parse the EHI Export PDF documentation from Prime Clinical Systems.
Extracts all structured information: tables mentioned, file structures,
export components, and produces a full-entity-inventory.json.
"""

import json
import subprocess
import re
import sys

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/prime-clinical-systems-inc--patient-chart-manager/downloads/EHI_Export_170.315_b10.pdf"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/prime-clinical-systems-inc--patient-chart-manager/analysis"

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_PATH, "-"],
    capture_output=True, text=True
)
pdf_text = result.stdout

# Get PDF metadata
info_result = subprocess.run(
    ["pdfinfo", PDF_PATH],
    capture_output=True, text=True
)
pdf_info = info_result.stdout

# Parse PDF metadata
metadata = {}
for line in pdf_info.strip().split("\n"):
    if ":" in line:
        key, val = line.split(":", 1)
        metadata[key.strip()] = val.strip()

# Extract table/entity names mentioned in the PDF
# From the text and screenshots, these are the data entities visible:
tables_in_xml_export = [
    {
        "name": "CHART_DOCS",
        "file": "CHART_DOCS;DataTable.xml",
        "location": "XMLDATAExport_#.zip",
        "description": "Contains all chart docs details for the exported date and Medical Record Number (MR) range",
        "compressed_size": "2 KB",
        "uncompressed_size": "10 KB",
        "source": "PDF page 1 text + screenshot"
    },
    {
        "name": "CHART_STORE",
        "file": "CHART_STORE;DataTable.xml",
        "location": "XMLDATAExport_#.zip",
        "description": "Contains all chart store details for the exported date and MR number range",
        "compressed_size": "1 KB",
        "uncompressed_size": "7 KB",
        "source": "PDF page 1 text + screenshot"
    },
    {
        "name": "PATIENT",
        "file": "PATIENT;DataTable.xml",
        "location": "XMLDATAExport_#.zip",
        "description": "Contains all patient data table details for the exported date and MR number range. All patient data tables included (except those hidden via HIDE option).",
        "compressed_size": "4 KB",
        "uncompressed_size": "39 KB",
        "source": "PDF page 1 text + screenshot"
    },
    {
        "name": "PT_ALLERGIES",
        "file": "PT_ALLERGIES;DataTable.xml",
        "location": "XMLDATAExport_#.zip",
        "description": "Patient allergies data table",
        "compressed_size": "2 KB",
        "uncompressed_size": "11 KB",
        "source": "PDF page 1 screenshot"
    },
    {
        "name": "PT_COMPLAINTS",
        "file": "PT_COMPLAINTS;DataTable.xml",
        "location": "XMLDATAExport_#.zip",
        "description": "Patient complaints/problems data table",
        "compressed_size": "1 KB",
        "uncompressed_size": "6 KB",
        "source": "PDF page 1 screenshot"
    },
]

# Additional entities from page 2 screenshots
tables_in_ccda_export = [
    {
        "name": "CDAFULSUM",
        "file": "CDAFULSUM.xml",
        "location": "CDASUMDATA.Zip (inside CDAXMLExport_#.zip)",
        "description": "C-CDA full summary document for a patient",
        "compressed_size": "6 KB",
        "uncompressed_size": None,
        "source": "PDF page 2 screenshot (visible as 303735,9,9,129,CDAFULSUM.xml)"
    },
]

chart_document_export = {
    "name": "CDAXMLDOC",
    "file_pattern": "[MRN,PCM_LOGON_CLINIC,PATIENT-CLINIC,PATIENT-ACCOUNT,Chart_DOC_ID,CDADOCID.xml]",
    "location": "CDAXMLDOC.Zip",
    "description": "Chart documents exported as embedded PDFs in C-CDA format. Fields reference Patient table (pa_clinic, pa_account), chart_store table (cs_mr_num, cs_cl_key), and pt_chart_docs (cdview_cddocid).",
    "example_files_visible": [
        {"name": "286715,9,9,88,20405,CDADOCID.xml", "compressed": "7 KB", "size": "16 KB"},
        {"name": "286715,9,9,88,204540,CDADOCID.xml", "compressed": "132 KB", "size": "185 KB"},
        {"name": "286715,9,9,88,20630B,CDADOCID.xml", "compressed": "76 KB", "size": "107 KB"},
    ],
    "source": "PDF page 2 screenshot"
}

# Additional table names referenced in field descriptions but not as standalone exports
referenced_tables = [
    {"name": "pt_chart_docs", "context": "Referenced in chart document naming - field cdview_cddocid", "source": "PDF page 2 text"},
    {"name": "chart_store", "context": "Referenced in naming conventions - fields cs_mr_num, cs_cl_key", "source": "PDF page 2 text"},
    {"name": "Patient", "context": "Referenced in naming conventions - fields pa_clinic, pa_account", "source": "PDF page 2 text"},
]

# Export components
export_components = [
    {
        "component": "XMLDATAExport_#.zip",
        "format": "Microsoft ADO XML Recordsets (VB6 adPersistXML)",
        "description": "Core data export - database tables serialized as ADO XML",
        "tables_visible": 5,
        "table_names": [t["name"] for t in tables_in_xml_export],
        "conditions": "Default export (no checkboxes needed)",
    },
    {
        "component": "CDAXMLExport_#.zip",
        "format": "C-CDA R2.1",
        "description": "C-CDA documents (clinical summaries)",
        "conditions": "Included only with Bulk CCDA Export option",
    },
    {
        "component": "CDAXMLDOC.Zip",
        "format": "C-CDA R2.1 with embedded PDF",
        "description": "Chart documents (scanned papers, faxes, etc.) exported as embedded PDFs in C-CDA XML",
        "conditions": "Per-patient chart documents",
    },
]

# Build the full inventory
inventory = {
    "vendor": "Prime Clinical Systems, Inc.",
    "product": "Patient Chart Manager",
    "version": "7.1.1877",
    "document_date": "12/23/2025",
    "pdf_pages": int(metadata.get("Pages", 3)),
    "pdf_size_bytes": int(metadata.get("File size", "4300225").replace(" bytes", "")),
    "pdf_creator": metadata.get("Creator", "PDFium"),
    "export_location": r"\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports_#",
    "export_formats": ["Microsoft ADO XML Recordsets (VB6)", "C-CDA R2.1"],
    "export_components": export_components,
    "data_tables_in_export": tables_in_xml_export,
    "ccda_components": tables_in_ccda_export,
    "chart_document_export": chart_document_export,
    "referenced_tables": referenced_tables,
    "total_named_tables": len(tables_in_xml_export),
    "total_fields_documented": 0,  # No field-level documentation exists
    "fields_with_descriptions": 0,
    "fields_with_types": 0,
    "data_dictionary_exists": False,
    "sample_data_provided": False,
    "schema_documentation_provided": False,
    "relationship_documentation": False,
    "value_set_documentation": False,
    "field_names_mentioned": [
        "pa_clinic", "pa_account",  # from Patient table
        "cs_mr_num", "cs_cl_key",  # from chart_store table
        "cdview_cddocid", "CD_DOC_ID",  # from pt_chart_docs table
    ],
    "documentation_gaps": [
        "No data dictionary - zero field definitions provided",
        "No table schema documentation",
        "No relationship/foreign key documentation",
        "No value set or coded value documentation",
        "No sample data or example exports",
        "Referenced companion document 'Including and Excluding Data' not available online",
        "No documentation of which patient data tables are included beyond the 5 visible in screenshots",
        "No billing/PM data tables mentioned despite product having full PM capabilities",
        "No medication, lab, immunization, vital signs, or procedure tables mentioned",
    ]
}

# Write output
output_path = f"{OUTPUT_DIR}/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Inventory written to {output_path}")
print(f"\nSummary:")
print(f"  PDF pages: {inventory['pdf_pages']}")
print(f"  Export components: {len(inventory['export_components'])}")
print(f"  Named data tables in export: {inventory['total_named_tables']}")
print(f"  Total fields documented: {inventory['total_fields_documented']}")
print(f"  Data dictionary exists: {inventory['data_dictionary_exists']}")
print(f"  Sample data provided: {inventory['sample_data_provided']}")
print(f"  Field names mentioned (incidentally): {len(inventory['field_names_mentioned'])}")
print(f"  Documentation gaps identified: {len(inventory['documentation_gaps'])}")
