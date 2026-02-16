#!/usr/bin/env python3
"""
Parse the Praxis EMR EHI Export Documentation PDF and extract
structured information about the export components.

The PDF is a procedural guide (how to run the export), not a data dictionary.
We extract the documented output file types and their described contents.
"""
import json
import subprocess
import re

# Extract text from PDF
result = subprocess.run(
    ["pdftotext", "-layout", "../downloads/Infor-Med-Medical-Information-Systems-DataExportDocumentation.pdf", "-"],
    capture_output=True, text=True
)
pdf_text = result.stdout

# The export produces these documented output components:
# We treat each output file type as an "entity" since there's no data dictionary.
entities = [
    {
        "entity_name": "index.html",
        "category": "Demographics / Patient Index",
        "description": "HTML page serving as master index of all exported patients",
        "format": "HTML",
        "fields": [
            {"name": "Patient Name", "type": "text", "description": "Full name of the patient (last name is hyperlink to patient folder)"},
            {"name": "Patient Chart Number", "type": "text", "description": "Chart number / registration number"},
            {"name": "Date of Birth", "type": "date", "description": "Patient date of birth"},
            {"name": "Date of Death", "type": "date", "description": "Date of death if applicable"},
            {"name": "Status", "type": "text", "description": "Active/Inactive status"},
            {"name": "Gender", "type": "text", "description": "Patient gender"},
            {"name": "SSN", "type": "text", "description": "Social Security Number"},
            {"name": "Last Attending Physician", "type": "text", "description": "Last attending physician"},
            {"name": "Primary Physician", "type": "text", "description": "Primary physician"},
            {"name": "Referring Physician", "type": "text", "description": "Referring physician"},
            {"name": "Address", "type": "text", "description": "Patient address"},
            {"name": "Phone Numbers", "type": "text", "description": "Patient phone numbers (all corresponding demographic information)"},
        ],
        "source": "PDF page 7: 'This page serves as an index of all the exported patients, displaying their name, patient chart number, date of birth, date of death (if applicable), status (Active/Inactive), gender, SSN, last attending physician, primary physician, referring physician, and all corresponding demographic information (address, phone numbers, etc).'"
    },
    {
        "entity_name": "PatientSummary.xml",
        "category": "Clinical Summary (CDA)",
        "description": "Complete patient summary in CDA (C-CDA) XML format. Suitable for importing into another EMR compliant with the standard certified by ONC.",
        "format": "CDA XML",
        "fields": [],  # No field-level documentation provided
        "field_note": "No field-level documentation. C-CDA standard sections presumed (problems, medications, allergies, vitals, labs, procedures, etc.) but specific sections populated are not documented.",
        "naming_convention": "LASTNAME_[MIDDLENAME]_FIRSTNAME_GENDER(REG_NO)_MM-DD-YYYY_PatientSummary.xml",
        "source": "PDF page 5 and 8"
    },
    {
        "entity_name": "PatientSummary.xml.html",
        "category": "Clinical Summary (Human-Readable)",
        "description": "Human-readable HTML rendering of the CDA patient summary.",
        "format": "HTML",
        "fields": [],
        "field_note": "Human-readable rendering of the CDA XML. No independent field documentation.",
        "naming_convention": "LASTNAME_[MIDDLENAME]_FIRSTNAME_GENDER(REG_NO)_MM-DD-YYYY_PatientSummary.xml.html",
        "source": "PDF page 8"
    },
    {
        "entity_name": "VisitSummary.xml",
        "category": "Visit Summary (CDA)",
        "description": "Per-visit summary in CDA format. Does not include inserted notes. Suitable for importing and reconciling with any other EMR compliant with the standard certified by ONC.",
        "format": "CDA XML",
        "fields": [],
        "field_note": "No field-level documentation. C-CDA standard sections presumed but specific sections populated per visit are not documented.",
        "naming_convention": "YYYY-MM-DD-HH-MM_VISIT_TITLE_VisitSummary.xml",
        "source": "PDF page 8"
    },
    {
        "entity_name": "VisitSummary.xml.html",
        "category": "Visit Summary (Human-Readable)",
        "description": "Human-readable HTML rendering of the per-visit CDA summary.",
        "format": "HTML",
        "fields": [],
        "field_note": "Human-readable rendering of the CDA XML. No independent field documentation.",
        "naming_convention": "YYYY-MM-DD-HH-MM_VISIT_TITLE_VisitSummary.xml.html",
        "source": "PDF page 8"
    },
    {
        "entity_name": "Visit.doc",
        "category": "Visit Narrative",
        "description": "Microsoft Word document containing all the text from a visit, including separately printed texts. One file per visit.",
        "format": "DOC (Microsoft Word)",
        "fields": [],
        "field_note": "Unstructured free-text narrative. No field-level documentation. Contains the physician's narrative documentation (Concept Processor output).",
        "naming_convention": "YYYY-MM-DD-HH-MM_VISIT_TITLE_Visit.doc",
        "source": "PDF page 8"
    },
    {
        "entity_name": "InsertedNote.doc",
        "category": "Inserted Notes",
        "description": "Microsoft Word document containing the text of each inserted note. One file per inserted note.",
        "format": "DOC (Microsoft Word)",
        "fields": [],
        "field_note": "Unstructured free-text. No field-level documentation.",
        "naming_convention": "YYYY-MM-DD-HH-MM_INSERTED_NOTE_TITLE_InsertedNote.doc",
        "source": "PDF page 8"
    },
    {
        "entity_name": "InsertedNote_attachments",
        "category": "Attachments",
        "description": "Files attached to inserted notes, exported in their original format (PDF, XLSX, PNG, etc.).",
        "format": "Original format (PDF, XLSX, PNG, etc.)",
        "fields": [],
        "field_note": "Binary attachments in original format. No metadata documentation beyond filename convention.",
        "naming_convention": "YYYY-MM-DD-HH-MM_INSERTED_NOTE_TITLE_InsertedNote_fileX.ext",
        "source": "PDF page 8"
    },
]

# Export capabilities summary
export_capabilities = {
    "mechanism": "Desktop utility (Praxis Data Export Utility) accessible from Praxis Control Panel",
    "patient_selection": [
        "Export All patients",
        "Continue from selected patient (resume interrupted export)",
        "Only Selected patient (single patient by chart number)"
    ],
    "export_options": [
        "Export Patient Summary (CDA XML + HTML)",
        "Export Documents (visit text .doc, inserted notes .doc, attachments in original format)",
        "Export Visit Summaries (per-visit CDA XML + HTML)"
    ],
    "bulk_capable": True,
    "single_patient_capable": True,
    "api_access": False,
    "programmatic_access": False,
    "fees_documented": False,
    "resume_capability": True,
    "output_structure": "Folder hierarchy: root/index.html + patient folders containing CDA Files subfolder and doc/attachment files"
}

# Build inventory
inventory = {
    "product": "Praxis EMR",
    "version": "9",
    "chpl_id": "15.02.05.2766.INFO.01.02.1.220310",
    "documentation_source": "Infor-Med-Medical-Information-Systems-DataExportDocumentation.pdf",
    "documentation_type": "Procedural guide (how to run the export utility)",
    "documentation_pages": 10,
    "documentation_revision_date": "2023-11-14",
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "has_field_descriptions": False,
    "export_capabilities": export_capabilities,
    "entities": entities,
    "total_entities": len(entities),
    "total_documented_fields": sum(len(e["fields"]) for e in entities),
    "fields_with_descriptions": sum(1 for e in entities for f in e["fields"] if f.get("description")),
    "notes": [
        "The documentation is purely procedural - it describes HOW to use the export utility, not WHAT data fields are exported.",
        "No data dictionary, schema, or field-level documentation is provided for the CDA documents.",
        "The only fields explicitly documented are the 12 demographic fields shown in index.html.",
        "CDA content is not specified beyond 'patient summary' and 'visit summary' - no sections, templates, or coded values are documented.",
        "The export is document-oriented (CDA + .doc files), not a database export.",
        "The export does not cover: e-prescribing history, patient portal data, scheduling, billing/coding, clinical decision support, knowledge bases, or messaging."
    ]
}

# Write full inventory
with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Write summary
summary = {
    "total_entities": inventory["total_entities"],
    "total_documented_fields": inventory["total_documented_fields"],
    "fields_with_descriptions": inventory["fields_with_descriptions"],
    "pct_fields_with_descriptions": round(100 * inventory["fields_with_descriptions"] / max(1, inventory["total_documented_fields"]), 1),
    "has_data_dictionary": False,
    "has_schema": False,
    "has_sample_data": False,
    "export_formats": ["CDA XML", "HTML", "DOC (Microsoft Word)", "Original format attachments"],
    "categories": {},
    "documentation_quality": {
        "pages": 10,
        "effective_content_pages": 7,
        "type": "Procedural guide with screenshots",
        "field_level_docs": "Only for index.html demographics (12 fields)",
        "cda_section_docs": "None - no specification of which CDA sections are populated",
        "schema_or_template_docs": "None",
        "value_set_docs": "None",
        "sample_data": "None"
    }
}

# Summarize by category
for e in entities:
    cat = e["category"]
    if cat not in summary["categories"]:
        summary["categories"][cat] = {"entity_count": 0, "field_count": 0}
    summary["categories"][cat]["entity_count"] += 1
    summary["categories"][cat]["field_count"] += len(e["fields"])

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Generated entity-inventory-full.json and entity-inventory-summary.json")
print(f"Total entities: {inventory['total_entities']}")
print(f"Total documented fields: {inventory['total_documented_fields']}")
print(f"Fields with descriptions: {inventory['fields_with_descriptions']}")
