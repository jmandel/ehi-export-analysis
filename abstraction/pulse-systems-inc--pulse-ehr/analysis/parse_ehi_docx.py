"""Parse the Pulse EHI Export DOCX from CHS and catalog CDA sections."""
import json
from docx import Document

DOCX_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/pulse-systems-inc--pulse-ehr/downloads/Pulse-EHI-Export-Document-REV-06142024.docx"

doc = Document(DOCX_PATH)

# Extract all paragraph text with styles
paragraphs = []
for p in doc.paragraphs:
    if p.text.strip():
        paragraphs.append({"style": p.style.name, "text": p.text.strip()})

# Extract table data
sections = []
for table in doc.tables:
    for i, row in enumerate(table.rows):
        cell_text = row.cells[0].text.strip()
        if i == 0:  # header row
            continue
        if cell_text:
            sections.append(cell_text)

unique_sections = list(dict.fromkeys(sections))  # preserve order, remove dupes
duplicates = [s for s in sections if sections.count(s) > 1]
dup_names = list(set(duplicates))

result = {
    "source_file": "Pulse-EHI-Export-Document-REV-06142024.docx",
    "source_url": "https://www.chs.net/_assets/docs/Pulse-EHI-Export-Document-REV-06142024.docx",
    "note": "This document is from CHS (Community Health Systems) for Pulse v16.1 — a DIFFERENT product/developer than Pulse Systems Inc. v8.02",
    "document_metadata": {
        "created": "May 16, 2023",
        "revised": "September 7, 2023",
        "format": "CDA XML (Clinical Document Architecture)",
        "paragraph_count": len(paragraphs),
        "table_count": len(doc.tables),
    },
    "cda_sections": {
        "total_rows_in_table": len(sections),
        "unique_sections": len(unique_sections),
        "duplicate_sections": dup_names,
        "sections": unique_sections,
    },
    "section_categories": {
        "clinical_notes": [s for s in unique_sections if any(k in s.lower() for k in ["note", "history of present", "physical examination", "review of systems", "hospital course", "discharge summary", "consultation"])],
        "diagnoses_problems": [s for s in unique_sections if any(k in s.lower() for k in ["problem", "diagnosis", "diagnos"])],
        "medications": [s for s in unique_sections if "medic" in s.lower()],
        "procedures": [s for s in unique_sections if any(k in s.lower() for k in ["procedure", "implant"])],
        "vitals_labs": [s for s in unique_sections if any(k in s.lower() for k in ["vital", "result"])],
        "allergies": [s for s in unique_sections if "allerg" in s.lower()],
        "immunizations": [s for s in unique_sections if "immun" in s.lower()],
        "care_planning": [s for s in unique_sections if any(k in s.lower() for k in ["plan", "goal", "concern", "intervention", "assessment", "outcome", "status eval"])],
        "social_family": [s for s in unique_sections if any(k in s.lower() for k in ["social", "family"])],
        "encounter_visit": [s for s in unique_sections if any(k in s.lower() for k in ["encounter", "reason for visit", "chief complaint", "admission", "discharge instruct"])],
        "financial_payer": [s for s in unique_sections if any(k in s.lower() for k in ["payer", "financial"])],
        "security": [s for s in unique_sections if "security" in s.lower() or "privacy" in s.lower()],
    }
}

with open("ehi_docx_analysis.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
