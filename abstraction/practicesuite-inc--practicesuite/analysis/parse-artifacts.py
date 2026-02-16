#!/usr/bin/env python3
"""
Parse PracticeSuite EHI export documentation artifacts.
Since there is no data dictionary or structured schema, this script
extracts what information is available from the HTML documentation
pages and screenshots to build an inventory of what the export contains.
"""

import json
import os
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE, "downloads")
ANALYSIS = os.path.join(BASE, "analysis")


class ContentExtractor(HTMLParser):
    """Extract text content from WordPress entry-content div."""
    def __init__(self):
        super().__init__()
        self.text_blocks = []
        self.in_content = False
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer'}
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_depth += 1
        d = dict(attrs)
        cls = d.get('class', '')
        if 'entry-content' in cls:
            self.in_content = True

    def handle_endtag(self, tag):
        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth == 0 and self.in_content:
            t = data.strip()
            if t:
                self.text_blocks.append(t)


def extract_page_text(filename):
    """Extract text from an HTML file."""
    p = ContentExtractor()
    with open(os.path.join(DOWNLOADS, filename)) as f:
        p.feed(f.read())
    return p.text_blocks


# Standard C-CDA sections that would be in a "full CCDA Summary"
# Based on HL7 C-CDA R2.1 standard sections
CCDA_SECTIONS = [
    {"name": "Patient Demographics", "templateId": "2.16.840.1.113883.10.20.22.1.1",
     "description": "Patient name, DOB, gender, race, ethnicity, language, address, phone, insurance"},
    {"name": "Allergies and Intolerances", "templateId": "2.16.840.1.113883.10.20.22.2.6.1",
     "description": "Allergy substances, reaction types, severity"},
    {"name": "Medications", "templateId": "2.16.840.1.113883.10.20.22.2.1.1",
     "description": "Active and historical medications"},
    {"name": "Problem List", "templateId": "2.16.840.1.113883.10.20.22.2.5.1",
     "description": "Active diagnoses and conditions"},
    {"name": "Procedures", "templateId": "2.16.840.1.113883.10.20.22.2.7.1",
     "description": "Performed procedures"},
    {"name": "Results", "templateId": "2.16.840.1.113883.10.20.22.2.3.1",
     "description": "Lab and diagnostic test results"},
    {"name": "Vital Signs", "templateId": "2.16.840.1.113883.10.20.22.2.4.1",
     "description": "Height, weight, BMI, BP, heart rate, temperature, respiratory rate, SpO2"},
    {"name": "Immunizations", "templateId": "2.16.840.1.113883.10.20.22.2.2.1",
     "description": "Vaccination records"},
    {"name": "Encounters", "templateId": "2.16.840.1.113883.10.20.22.2.22.1",
     "description": "Visit/encounter history"},
    {"name": "Plan of Treatment", "templateId": "2.16.840.1.113883.10.20.22.2.10",
     "description": "Treatment plans and care plans"},
    {"name": "Goals", "templateId": "2.16.840.1.113883.10.20.22.2.60",
     "description": "Patient health goals"},
    {"name": "Social History", "templateId": "2.16.840.1.113883.10.20.22.2.17",
     "description": "Smoking status, social determinants"},
    {"name": "Family History", "templateId": "2.16.840.1.113883.10.20.22.2.15",
     "description": "Family medical history"},
    {"name": "Medical Equipment", "templateId": "2.16.840.1.113883.10.20.22.2.23",
     "description": "Implantable devices and medical equipment"},
    {"name": "Functional Status", "templateId": "2.16.840.1.113883.10.20.22.2.14",
     "description": "Functional and cognitive status"},
    {"name": "Reason for Referral", "templateId": "2.16.840.1.113883.10.20.22.2.56",
     "description": "Referral reason"},
    {"name": "Assessment", "templateId": "2.16.840.1.113883.10.20.22.2.8",
     "description": "Clinical assessment"},
]

# Additional export component: raw documents
DOCUMENT_EXPORT = {
    "name": "Patient Documents (raw files)",
    "description": "All documents associated with patient in original format (PDFs, images, scanned docs, etc.)",
    "format": "Original file formats in ZIP",
    "documented_fields": 0,
    "note": "No field-level documentation; files exported as-is"
}

# Data visible in the Custom Visit Summary screenshot (K3CustomVisitSummary.png)
VISIT_SUMMARY_FIELDS = [
    "Patient Demographics (Name, DOB, Age, Gender, Location)",
    "Documentation Demographics (Provider, DOS, Enc Sheet Type, Canned Sheet Type)",
    "Encounter Demographics (Start Time, Encounter Type, Tele Health Type, Transaction Service, Participant Roster, SHS Eng Level)",
    "Chief Complaint",
    "Past Medical History (Notes, Significant conditions)",
    "Allergies (by category: Medications, Food, Environmental, Animals & Insects, Other)",
    "Med List",
    "Vital Signs (Temperature, Heart Rate, Respiratory Rate, Blood Pressure, Pain, Pulse Ox, Height)",
    "Assessment/Diagnosis (ICD codes)",
    "Plan/Recommended Action (Medications School Administered, OTC Medications, Prescription Medications, Actions Instructions, Follow Up Care, Communication Visit Summary, Patient Education, Student Disposition)",
    "Special Situation",
    "Escalation and Emergency",
    "Provider Signature (Physician, Nurse Practitioner, Registered Nurse)",
    "Care Coordinator Signature",
    "Custom Visit Summary status",
    "Authorization for Med Administration - RX status",
    "CareTeam Communication 1 status",
]


def build_inventory():
    """Build the entity inventory from available evidence."""
    entities = []

    # C-CDA sections as "entities"
    for section in CCDA_SECTIONS:
        entities.append({
            "entity_name": f"C-CDA Section: {section['name']}",
            "category": "C-CDA Clinical Data",
            "fields": [],  # No field-level documentation available
            "field_count": 0,
            "fields_with_descriptions": 0,
            "fields_with_types": 0,
            "source": "Inferred from C-CDA standard (vendor does not document specific sections)",
            "templateId": section.get("templateId"),
            "description": section["description"],
            "vendor_documented": False,
            "note": "PracticeSuite says 'full CCDA Summary' but does not specify which sections are populated"
        })

    # Document export
    entities.append({
        "entity_name": "Patient Documents (ZIP)",
        "category": "Document Export",
        "fields": [
            {"name": "FileName", "type": "string", "description": "Original file name"},
            {"name": "Category", "type": "string", "description": "Document category tag"},
        ],
        "field_count": 2,
        "fields_with_descriptions": 2,
        "fields_with_types": 2,
        "source": "downloads/ehi-export-page.html - naming convention documentation",
        "vendor_documented": True,
        "note": "Documents exported in original format with filename and category metadata"
    })

    return entities


def build_summary(entities):
    """Build summary statistics from the entity inventory."""
    total_entities = len(entities)
    vendor_documented = sum(1 for e in entities if e.get("vendor_documented"))
    total_fields = sum(e.get("field_count", 0) for e in entities)
    fields_with_desc = sum(e.get("fields_with_descriptions", 0) for e in entities)
    fields_with_types = sum(e.get("fields_with_types", 0) for e in entities)

    categories = {}
    for e in entities:
        cat = e.get("category", "Unknown")
        if cat not in categories:
            categories[cat] = {"entity_count": 0, "field_count": 0}
        categories[cat]["entity_count"] += 1
        categories[cat]["field_count"] += e.get("field_count", 0)

    return {
        "product": "PracticeSuite",
        "export_format": "C-CDA XML + raw documents ZIP",
        "data_dictionary_provided": False,
        "field_level_documentation": False,
        "total_entities_inferred": total_entities,
        "vendor_documented_entities": vendor_documented,
        "total_fields_documented": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_types,
        "description_percentage": round(fields_with_desc / total_fields * 100, 1) if total_fields > 0 else 0,
        "categories": categories,
        "key_finding": "No data dictionary or schema provided. Export is C-CDA (standard clinical summary) plus raw document files. No vendor-specific field mapping, no billing data, no product-specific documentation beyond workflow screenshots.",
        "artifacts_analyzed": [
            {"file": "downloads/ehi-export-page.html", "type": "HTML", "size_bytes": 159057, "description": "Main EHI export documentation page"},
            {"file": "downloads/k3-report-page.html", "type": "HTML", "size_bytes": 160822, "description": "K3 Report documentation page"},
            {"file": "downloads/page-screenshot-full.png", "type": "PNG", "size_bytes": 1346963, "description": "Full-page screenshot of EHI export page"},
            {"file": "downloads/k3-images/K3CustomVisitSummary.png", "type": "PNG", "size_bytes": 81406, "description": "Custom Visit Summary report sample"},
            {"file": "downloads/k3-images/K3OutputList.png", "type": "PNG", "size_bytes": 36094, "description": "K3 report output showing patient list and export buttons"},
            {"file": "downloads/singlepatsearch.png", "type": "PNG", "size_bytes": 158162, "description": "Single patient search interface"},
            {"file": "downloads/patpopulationsrch.png", "type": "PNG", "size_bytes": 132152, "description": "Population search interface"},
            {"file": "downloads/ccdadownloadzip.png", "type": "PNG", "size_bytes": 84695, "description": "C-CDA ZIP contents screenshot"},
            {"file": "downloads/docdownloadzip.png", "type": "PNG", "size_bytes": 147707, "description": "Documents ZIP contents screenshot"},
        ],
        "visit_summary_fields_observed": VISIT_SUMMARY_FIELDS,
    }


if __name__ == "__main__":
    # Extract text from both HTML pages for reference
    ehi_text = extract_page_text("ehi-export-page.html")
    k3_text = extract_page_text("k3-report-page.html")

    # Build inventory
    entities = build_inventory()
    with open(os.path.join(ANALYSIS, "entity-inventory-full.json"), "w") as f:
        json.dump(entities, f, indent=2)
    print(f"Wrote entity-inventory-full.json: {len(entities)} entities")

    # Build summary
    summary = build_summary(entities)
    with open(os.path.join(ANALYSIS, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")
    print(f"  Total entities (inferred): {summary['total_entities_inferred']}")
    print(f"  Vendor-documented entities: {summary['vendor_documented_entities']}")
    print(f"  Total documented fields: {summary['total_fields_documented']}")
    print(f"  Data dictionary provided: {summary['data_dictionary_provided']}")

    # Save extracted page text for reference
    with open(os.path.join(ANALYSIS, "ehi-page-text.txt"), "w") as f:
        f.write("\n".join(ehi_text))
    with open(os.path.join(ANALYSIS, "k3-page-text.txt"), "w") as f:
        f.write("\n".join(k3_text))
    print("Wrote page text extractions")
