"""Parse the Pulse EHI Export DOCX to extract CDA sections and build entity inventory."""

import zipfile
import xml.etree.ElementTree as ET
import json

DOCX_PATH = "../downloads/Pulse-EHI-Export-Document-REV-06142024.docx"

# Extract all text paragraphs
with zipfile.ZipFile(DOCX_PATH) as z:
    tree = ET.parse(z.open("word/document.xml"))

ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# Extract table rows (the CDA sections table)
sections = []
for tbl in tree.findall(".//w:tbl", ns):
    for row in tbl.findall(".//w:tr", ns):
        cells = []
        for cell in row.findall(".//w:tc", ns):
            texts = [t.text for t in cell.findall(".//w:t", ns) if t.text]
            cells.append(" ".join(texts).strip())
        text = " | ".join(cells).strip()
        if text and text != "Section":  # skip header
            sections.append(text)

# Deduplicate (Health Concerns Section and Goals Section appear twice in the doc)
seen = set()
unique_sections = []
for s in sections:
    normalized = s.lower().strip()
    if normalized not in seen:
        seen.add(normalized)
        unique_sections.append(s)

# Map CDA sections to data domains
domain_map = {
    "Security and Privacy Prohibitions": "Administrative",
    "Allergies and Adverse Reactions": "Allergies",
    "Medications": "Medications",
    "Discharge Medications": "Medications",
    "Problems": "Problems/Diagnoses",
    "Hospital Discharge Diagnosis": "Problems/Diagnoses",
    "Encounters": "Encounters",
    "Admission Diagnosis": "Problems/Diagnoses",
    "Procedures": "Procedures",
    "Implants": "Medical Devices",
    "Immunizations": "Immunizations",
    "Vital Signs": "Vitals",
    "Social History": "Social History",
    "Results": "Lab Results",
    "Functional Status": "Health Status",
    "Mental Status": "Health Status",
    "Assessments": "Assessments",
    "PLAN OF CARE": "Care Plans/Goals",
    "Goals Section": "Care Plans/Goals",
    "Health Concerns Section": "Care Plans/Goals",
    "Hospital Discharge Instructions": "Clinical Notes",
    "Family History": "Family History",
    "Reason For Visit/Chief Complaint": "Clinical Notes",
    "General Status": "Clinical Notes",
    "Past Medical History": "Clinical Notes",
    "History Of Present Illness": "Clinical Notes",
    "Physical Examination": "Clinical Notes",
    "Review Of Systems": "Clinical Notes",
    "Progress Note": "Clinical Notes",
    "PreOperative Diagnosis": "Procedures",
    "PreOperative  Diagnosis": "Procedures",
    "Postprocedure Diagnosis": "Procedures",
    "Postprocedure  Diagnosis": "Procedures",
    "Planned Procedure": "Procedures",
    "Complications": "Clinical Notes",
    "Procedure Indications": "Procedures",
    "Procedure Description": "Procedures",
    "Procedure Note": "Procedures",
    "Reason for Referral": "Referrals",
    "Hospital Course": "Clinical Notes",
    "Interventions Section": "Care Plans/Goals",
    "Health Status Evaluations/Outcomes Section": "Health Status",
    "Discharge Summary Note": "Clinical Notes",
    "Consultation Note": "Clinical Notes",
    "Payers": "Insurance/Coverage",
    "Financial Data": "Billing/Financial",
}

# Build entity inventory
entities = []
for section in unique_sections:
    domain = domain_map.get(section, "Unknown")
    entities.append({
        "entity_name": section,
        "source": "CDA Section",
        "domain": domain,
        "fields": None,  # CDA sections - no field-level detail provided
        "field_count": None,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "description": f"CDA section listed in EHI export document. No field-level documentation provided.",
    })

inventory = {
    "source_file": "Pulse-EHI-Export-Document-REV-06142024.docx",
    "source_version": "Pulse v16.1 (CHS deployment)",
    "certified_version": "Pulse EHR v8.02",
    "format": "CDA XML (Clinical Document Architecture)",
    "total_sections": len(unique_sections),
    "duplicate_sections_removed": len(sections) - len(unique_sections),
    "field_level_documentation": False,
    "entities": entities,
}

# Domain summary
domain_counts = {}
for e in entities:
    d = e["domain"]
    domain_counts[d] = domain_counts.get(d, 0) + 1

summary = {
    "total_cda_sections": len(unique_sections),
    "total_cda_sections_before_dedup": len(sections),
    "duplicates_removed": len(sections) - len(unique_sections),
    "field_level_documentation": False,
    "fields_total": "N/A - no field-level documentation",
    "fields_with_descriptions": "N/A",
    "fields_with_types": "N/A",
    "domain_breakdown": domain_counts,
    "domains_represented": sorted(set(e["domain"] for e in entities)),
    "format": "CDA XML",
    "documentation_source": "CHS/CereCore (third-party, different version)",
}

with open("entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

with open("entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("=== CDA Sections (deduplicated) ===")
for i, s in enumerate(unique_sections, 1):
    print(f"  {i}. {s} [{domain_map.get(s, 'Unknown')}]")

print(f"\nTotal unique sections: {len(unique_sections)}")
print(f"Duplicates removed: {len(sections) - len(unique_sections)}")
print(f"\n=== Domain Breakdown ===")
for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
    print(f"  {domain}: {count} sections")

print(f"\nSaved entity-inventory-full.json and entity-inventory-summary.json")
