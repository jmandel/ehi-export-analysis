"""Parse FHIR-Documentation.html to extract resource types, endpoints, and profiles."""
import json
import re
from html.parser import HTMLParser

class ResourceExtractor(HTMLParser):
    """Extract FHIR resource sections from the documentation HTML."""
    def __init__(self):
        super().__init__()
        self.in_heading = False
        self.heading_level = 0
        self.current_text = ''
        self.headings = []
        self.in_body = False
        self.body_text = []
        self.all_text = []
        
    def handle_starttag(self, tag, attrs):
        if tag in ('h1','h2','h3','h4','h5','h6'):
            self.in_heading = True
            self.heading_level = int(tag[1])
            self.current_text = ''
        if tag == 'body':
            self.in_body = True
            
    def handle_endtag(self, tag):
        if tag in ('h1','h2','h3','h4','h5','h6') and self.in_heading:
            self.headings.append({
                'level': self.heading_level,
                'text': self.current_text.strip()
            })
            self.in_heading = False
            
    def handle_data(self, data):
        if self.in_heading:
            self.current_text += data
        if self.in_body:
            self.all_text.append(data.strip())

with open('../downloads/FHIR-Documentation.html') as f:
    html = f.read()

parser = ResourceExtractor()
parser.feed(html)

# Extract resource types from pattern: "conforms to USCDI profile for X"
profile_pattern = re.compile(r'conforms to USCDI profile for ([A-Za-z\s]+?)[\s\-–—]+refer to', re.IGNORECASE)
profiles = profile_pattern.findall(html)

# Extract GET/POST endpoint patterns
endpoint_pattern = re.compile(r'(GET|POST)\s+[^\s<]+')
endpoints = endpoint_pattern.findall(html)

# Extract resource names from section headings
resource_sections = []
# Look for patterns like "AllergyIntolerance" as standalone headings or section markers
resource_name_pattern = re.compile(r'\b(AllergyIntolerance|CarePlan|CareTeam|Condition|Device|DiagnosticReport|DocumentReference|Encounter|Goal|Immunization|Location|MedicationRequest|Observation|Organization|Patient|Practitioner|Procedure|Provenance|Coverage|Claim|ExplanationOfBenefit|ServiceRequest|FamilyMemberHistory|Medication|MedicationDispense|Specimen|RelatedPerson|QuestionnaireResponse)\b')

resources_in_doc = sorted(set(resource_name_pattern.findall(html)))

# Build entity inventory from what we can extract
entities = []
for resource in resources_in_doc:
    entities.append({
        "name": resource,
        "source": "FHIR-Documentation.html",
        "type": "FHIR Resource (US Core / USCDI)",
        "fields": [],
        "field_count": 0,
        "has_descriptions": False,
        "notes": f"Standard US Core profile for {resource}; no product-specific field documentation provided"
    })

# Also add the supplemental exports from the PDF
supplemental = [
    {
        "name": "Patient Demographics & Insurance (Excel)",
        "source": "B10-Electronic-Health-information-Export.pdf",
        "type": "Excel export",
        "fields": [],
        "field_count": 0,
        "has_descriptions": False,
        "notes": "Described as 'comprehensive view of demographics and insurance details' but no field-level documentation"
    },
    {
        "name": "Appointments (Excel)",
        "source": "B10-Electronic-Health-information-Export.pdf",
        "type": "Excel export",
        "fields": [],
        "field_count": 0,
        "has_descriptions": False,
        "notes": "Described as 'comprehensive view of all appointment details' but no field-level documentation"
    },
    {
        "name": "Documents (Scanned/Imported)",
        "source": "B10-Electronic-Health-information-Export.pdf",
        "type": "File export (PDF, JPG, PNG)",
        "fields": [],
        "field_count": 0,
        "has_descriptions": False,
        "notes": "Signed progress notes, lab results, radiology reports, scanned documents organized in patient chart folders by category"
    }
]

all_entities = entities + supplemental

result = {
    "product": "CursaHealth EHR v2.0",
    "analysis_date": "2026-02-16",
    "sources": [
        "downloads/B10-Electronic-Health-information-Export.pdf",
        "downloads/FHIR-Documentation.html"
    ],
    "summary": {
        "total_entities": len(all_entities),
        "fhir_resources": len(entities),
        "supplemental_exports": len(supplemental),
        "total_fields_documented": 0,
        "fields_with_descriptions": 0,
        "has_data_dictionary": False,
        "has_sample_data": False
    },
    "fhir_resources_listed": resources_in_doc,
    "uscdi_profiles_referenced": [p.strip() for p in profiles],
    "headings_in_fhir_doc": [h['text'] for h in parser.headings],
    "entities": all_entities
}

with open('entity-inventory-full.json', 'w') as f:
    json.dump(result, f, indent=2)

# Summary
summary = {
    "product": result["product"],
    "analysis_date": result["analysis_date"],
    "total_entities": result["summary"]["total_entities"],
    "fhir_resources": result["summary"]["fhir_resources"],
    "supplemental_exports": result["summary"]["supplemental_exports"],
    "total_fields_documented": 0,
    "fields_with_descriptions": 0,
    "pct_fields_with_descriptions": "N/A",
    "has_data_dictionary": False,
    "has_sample_data": False,
    "export_formats": ["C-CDA XML", "FHIR R4 Bulk Data", "Excel (XLSX)", "Document files (PDF/JPG/PNG)"],
    "categories": {
        "FHIR/C-CDA (standard clinical)": {
            "entities": len(entities),
            "fields": 0,
            "notes": "Standard US Core USCDI resources, no vendor-specific extensions documented"
        },
        "Supplemental Excel exports": {
            "entities": 2,
            "fields": 0,
            "notes": "Demographics/Insurance and Appointments; no field-level detail"
        },
        "Document files": {
            "entities": 1,
            "fields": 0,
            "notes": "Scanned/uploaded documents organized by patient and category"
        }
    }
}

with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
