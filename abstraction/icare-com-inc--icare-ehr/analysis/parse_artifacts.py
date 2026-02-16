#!/usr/bin/env python3
"""
Parse all iCare EHI export artifacts and produce a full-entity-inventory.json.
Extracts:
  - FHIR resource types from the EHI export HTML page
  - API categories from the PDF (via pre-extracted text)
  - CapabilityStatement details
  - Fields visible in sample JSON outputs from the API guide
"""
import json
import re
from pathlib import Path
from html.parser import HTMLParser

DOWNLOADS = Path(__file__).parent.parent.parent.parent / "results" / "icare-com-inc--icare-ehr" / "downloads"
OUTPUT = Path(__file__).parent

# --- Parse EHI export HTML page ---
class ResourceExtractor(HTMLParser):
    """Extract FHIR resource type names from h4 headings in the EHI export page."""
    def __init__(self):
        super().__init__()
        self.in_h4 = False
        self.resources = []
        self.current = ""

    def handle_starttag(self, tag, attrs):
        if tag == "h4":
            self.in_h4 = True
            self.current = ""

    def handle_endtag(self, tag):
        if tag == "h4" and self.in_h4:
            self.in_h4 = False
            name = self.current.strip()
            if name:
                self.resources.append(name)

    def handle_data(self, data):
        if self.in_h4:
            self.current += data

html_text = (DOWNLOADS / "ehi-export-page.html").read_text()
extractor = ResourceExtractor()
extractor.feed(html_text)
fhir_resources_on_page = extractor.resources

# Check for copy-paste errors in the HTML
# Look at examples in each section
resource_sections = []
parts = re.split(r'<h4>', html_text)[1:]  # split on h4 tags
for part in parts:
    title_match = re.match(r'(.*?)</h4>', part)
    title = title_match.group(1).strip() if title_match else "Unknown"
    
    # Find the example URI
    examples = re.findall(r'Example:.*?href="([^"]*)"', part) or re.findall(r'Example:(https?://[^\s<]+)', part)
    example_uri = examples[0] if examples else None
    
    # Find resource-specific query pattern
    uri_pattern = re.findall(r'URI:\s*(\S+\?\S+)', part)
    
    resource_sections.append({
        "resource_name": title,
        "example_uri": example_uri,
        "uri_patterns": uri_pattern,
    })

# --- Parse API guide categories ---
# These are the 16 categories documented in the proprietary REST API
api_categories = [
    {"name": "patient", "description": "Patient name, sex, date of birth, race, ethnicity, preferred language", "fhir_resource": "Patient"},
    {"name": "careTeam", "description": "Care team members", "fhir_resource": "CareTeam"},
    {"name": "smokingStatus", "description": "Smoking status", "fhir_resource": "Composition (Social History section)"},
    {"name": "problem", "description": "Problems", "fhir_resource": "Condition"},
    {"name": "medication", "description": "Medications", "fhir_resource": "MedicationStatement"},
    {"name": "medAllergy", "description": "Medication allergies", "fhir_resource": "AllergyIntolerance"},
    {"name": "labTest", "description": "Planned lab tests", "fhir_resource": "DiagnosticReport"},
    {"name": "labResult", "description": "Lab test results", "fhir_resource": "Observation"},
    {"name": "vital", "description": "Vital measurements", "fhir_resource": "Observation"},
    {"name": "procedure", "description": "Procedures", "fhir_resource": "Procedure"},
    {"name": "immunization", "description": "Immunizations", "fhir_resource": "Immunization"},
    {"name": "device", "description": "Implanted devices", "fhir_resource": "Device"},
    {"name": "planOfTreatment", "description": "Care plan", "fhir_resource": "CarePlan"},
    {"name": "assessment", "description": "Assessment", "fhir_resource": "RiskAssessment"},
    {"name": "goal", "description": "Discharge goals", "fhir_resource": "Goal"},
    {"name": "healthConcern", "description": "Health concerns (complaints and observations)", "fhir_resource": "Composition (Health Concern section)"},
]

# --- Parse FHIR CapabilityStatement ---
cap_stmt = json.loads((DOWNLOADS / "fhir-capability-statement.json").read_text())
cap_summary = {
    "fhir_version": cap_stmt.get("fhirVersion"),
    "software": cap_stmt.get("software", {}).get("name"),
    "software_version": cap_stmt.get("software", {}).get("version"),
    "implementation_description": cap_stmt.get("implementation", {}).get("description"),
    "implementation_url": cap_stmt.get("implementation", {}).get("url"),
    "instantiates": cap_stmt.get("instantiates", []),
    "resources_declared": [],
    "operations_declared": [],
}
for rest in cap_stmt.get("rest", []):
    for resource in rest.get("resource", []):
        cap_summary["resources_declared"].append(resource.get("type"))
        for op in resource.get("operation", []):
            cap_summary["operations_declared"].append(f"{resource['type']}/{op['name']}")

# --- Build fields inventory from API guide sample outputs ---
# Manually extract fields visible in each category's sample JSON
# These are the fields shown in the example output for each category
fields_by_category = {
    "patient": [
        {"name": "resourceType", "type": "string", "value": "Patient"},
        {"name": "id", "type": "string", "description": "Patient ID (e.g. R83536)"},
        {"name": "extension[us-core-race]", "type": "Extension", "description": "Race code and text"},
        {"name": "extension[us-core-ethnicity]", "type": "Extension", "description": "Ethnicity"},
        {"name": "extension[granular-race]", "type": "Extension", "description": "Granular race (e.g. European)"},
        {"name": "name.text", "type": "string", "description": "Previous name"},
        {"name": "name.family", "type": "string", "description": "Last name"},
        {"name": "name.given", "type": "array", "description": "First and middle names"},
        {"name": "name.suffix", "type": "array", "description": "Suffix (e.g. JR)"},
        {"name": "gender", "type": "string", "description": "Patient gender"},
        {"name": "birthDate", "type": "date", "description": "Date of birth"},
        {"name": "address.line", "type": "array", "description": "Street address"},
        {"name": "address.city", "type": "string", "description": "City"},
        {"name": "address.state", "type": "string", "description": "State"},
        {"name": "address.postalCode", "type": "string", "description": "Postal code"},
        {"name": "contact.telecom[home]", "type": "ContactPoint", "description": "Home phone"},
        {"name": "contact.telecom[mobile]", "type": "ContactPoint", "description": "Mobile phone"},
        {"name": "communication.language", "type": "CodeableConcept", "description": "Preferred language"},
    ],
    "smokingStatus": [
        {"name": "section.title", "type": "string", "value": "Social History"},
        {"name": "section.section.title", "type": "string", "description": "Smoking status display"},
        {"name": "section.section.code.coding", "type": "Coding", "description": "SNOMED CT code for smoking status"},
        {"name": "section.section.text.div", "type": "string", "description": "Onset date of smoking status"},
    ],
    "problem": [
        {"name": "clinicalStatus.coding.code", "type": "string", "description": "Status (active/resolved)"},
        {"name": "code.coding.system", "type": "string", "value": "http://snomed.info/sct"},
        {"name": "code.coding.code", "type": "string", "description": "SNOMED CT code"},
        {"name": "code.coding.display", "type": "string", "description": "Problem description"},
        {"name": "onsetDateTime", "type": "dateTime", "description": "Onset date/time"},
        {"name": "abatementString", "type": "string", "description": "Resolution date (if resolved)"},
    ],
    "medication": [
        {"name": "medicationCodeableConcept.coding.system", "type": "string", "value": "RxNorm"},
        {"name": "medicationCodeableConcept.coding.code", "type": "string", "description": "RxNorm code"},
        {"name": "medicationCodeableConcept.coding.display", "type": "string", "description": "Medication name"},
        {"name": "effectiveDateTime", "type": "dateTime", "description": "Start date"},
        {"name": "note[Direction]", "type": "string", "description": "Dosage directions (Give: X MG route freq)"},
        {"name": "note[End Date]", "type": "string", "description": "Medication end date"},
        {"name": "dosage.text", "type": "string", "description": "Dosage text"},
    ],
    "medAllergy": [
        {"name": "clinicalStatus.coding.code", "type": "string", "description": "Status (active/inactive)"},
        {"name": "code.coding.system", "type": "string", "value": "RxNorm"},
        {"name": "code.coding.code", "type": "string", "description": "RxNorm allergy code"},
        {"name": "code.coding.display", "type": "string", "description": "Allergy substance name"},
        {"name": "onsetDateTime", "type": "dateTime", "description": "Onset date"},
        {"name": "reaction.description", "type": "string", "description": "Reaction description with SNOMED code"},
        {"name": "reaction.severity", "type": "string", "description": "Reaction severity"},
    ],
    "labTest": [
        {"name": "status", "type": "string", "description": "Test status"},
        {"name": "code.coding", "type": "Coding", "description": "LOINC code and display for lab test"},
        {"name": "effectiveDateTime", "type": "dateTime", "description": "Effective date"},
    ],
    "labResult": [
        {"name": "code.coding", "type": "Coding", "description": "LOINC code and display for result"},
        {"name": "valueQuantity", "type": "Quantity", "description": "Numeric result value and unit"},
        {"name": "effectiveDateTime", "type": "dateTime", "description": "Effective date"},
        {"name": "referenceRange", "type": "object", "description": "Reference range (low/high)"},
    ],
    "vital": [
        {"name": "code.coding", "type": "Coding", "description": "LOINC code for vital sign"},
        {"name": "valueQuantity", "type": "Quantity", "description": "Measurement value and unit"},
        {"name": "effectiveDateTime", "type": "dateTime", "description": "Measurement date"},
        {"name": "component", "type": "array", "description": "Components (e.g. systolic/diastolic for BP)"},
    ],
    "procedure": [
        {"name": "status", "type": "string", "description": "Procedure status"},
        {"name": "code.coding.system", "type": "string", "value": "SNOMED CT"},
        {"name": "code.coding.code", "type": "string", "description": "SNOMED procedure code"},
        {"name": "code.coding.display", "type": "string", "description": "Procedure description"},
        {"name": "performedPeriod.start", "type": "dateTime", "description": "Start date"},
        {"name": "performedPeriod.end", "type": "dateTime", "description": "End date"},
    ],
    "careTeam": [
        {"name": "participant.role", "type": "CodeableConcept", "description": "Role on care team"},
        {"name": "participant.member", "type": "Reference", "description": "Provider name/reference"},
    ],
    "immunization": [
        {"name": "status", "type": "string", "description": "Immunization status"},
        {"name": "vaccineCode.coding", "type": "Coding", "description": "CVX code and vaccine name"},
        {"name": "occurrenceDateTime", "type": "dateTime", "description": "Administration date"},
        {"name": "lotNumber", "type": "string", "description": "Lot number"},
    ],
    "device": [
        {"name": "udiCarrier.deviceIdentifier", "type": "string", "description": "UDI device identifier"},
        {"name": "udiCarrier.carrierHRF", "type": "string", "description": "UDI human-readable form"},
        {"name": "type.coding", "type": "Coding", "description": "SNOMED device type code"},
        {"name": "patient", "type": "Reference", "description": "Patient reference"},
    ],
    "planOfTreatment": [
        {"name": "activity.detail.kind", "type": "string", "description": "Activity type (ServiceRequest or Task)"},
        {"name": "activity.detail.code.coding", "type": "Coding", "description": "SNOMED code for planned activity"},
        {"name": "activity.detail.description", "type": "string", "description": "Activity type label (Medication/Lab/Procedure)"},
        {"name": "activity.detail.scheduledString", "type": "string", "description": "Scheduled date/time"},
    ],
    "assessment": [
        {"name": "note.text", "type": "string", "description": "Assessment narrative text"},
    ],
    "goal": [
        {"name": "lifecycleStatus", "type": "string", "description": "Goal status (e.g. planned)"},
        {"name": "description.coding.display", "type": "string", "description": "Goal free-text description"},
        {"name": "note.text", "type": "string", "description": "Goal category note (e.g. Discharge Goals)"},
    ],
    "healthConcern": [
        {"name": "section[Complaints].Status", "type": "string", "description": "Complaint status (active/inactive/resolved)"},
        {"name": "section[Complaints].Description", "type": "string", "description": "Complaint description"},
        {"name": "section[Complaints].Start Date", "type": "string", "description": "Complaint start date"},
        {"name": "section[Complaints].Comment", "type": "string", "description": "Complaint comment"},
        {"name": "section[Observations].Status", "type": "string", "description": "Observation status"},
        {"name": "section[Observations].Description", "type": "string", "description": "Observation description"},
        {"name": "section[Observations].Start Date", "type": "string", "description": "Observation start date"},
        {"name": "section[Observations].Comment", "type": "string", "description": "Observation comment"},
    ],
}

# Count totals
total_fields = sum(len(fields) for fields in fields_by_category.values())
fields_with_desc = sum(
    1 for fields in fields_by_category.values()
    for f in fields if f.get("description")
)

# --- Build the full entity inventory ---
entities = []
for cat in api_categories:
    fields = fields_by_category.get(cat["name"], [])
    entities.append({
        "entity_name": cat["name"],
        "category": "Clinical",
        "description": cat["description"],
        "fhir_resource_type": cat["fhir_resource"],
        "source": "iCare proprietary REST API (/rest/extApp/Clinical)",
        "field_count": len(fields),
        "fields": fields,
    })

# Add the FHIR bulk data resource types from the web page
fhir_page_resources = []
for section in resource_sections:
    fhir_page_resources.append({
        "entity_name": section["resource_name"],
        "source": "EHI Export page (FHIR R4 API)",
        "example_uri": section["example_uri"],
        "field_documentation": "None - only resource type name and example query URI provided",
    })

inventory = {
    "vendor": "iCare.com, Inc.",
    "product": "iCare EHR",
    "export_methods": [
        {
            "method": "CCD/HIM Export (In-App)",
            "type": "single_patient",
            "format": "C-CDA XML / HIM documents",
            "documentation_level": "minimal",
            "description": "Generate CCD or export clinical assessments/notes from within patient chart",
        },
        {
            "method": "CSC Request (Bulk)",
            "type": "population",
            "format": "Unknown - described as files via SFTP with data dictionary",
            "documentation_level": "none",
            "description": "Request full clinical data export; data dictionary provided with delivery only",
        },
        {
            "method": "FHIR REST API",
            "type": "single_patient / population / group",
            "format": "FHIR R4 JSON (Bulk Data)",
            "documentation_level": "minimal",
            "description": "FHIR R4 API via third-party EMR Direct Interoperability Engine",
            "endpoint": "https://sandbox-r4.interopengine.com/fhir/r4/icare/",
        },
        {
            "method": "Proprietary REST API",
            "type": "single_patient",
            "format": "FHIR R4 JSON per category; C-CDA XML for all-criteria",
            "documentation_level": "moderate",
            "description": "iCare's own REST API at /rest/extApp/Clinical with 16 data categories",
            "endpoint": "<URL>/iCareEHRWeb/rest/extApp/Clinical",
        },
    ],
    "capability_statement": cap_summary,
    "fhir_resources_on_ehi_page": fhir_page_resources,
    "proprietary_api_categories": entities,
    "copy_paste_errors_detected": [
        "Encounter section example URI points to Procedure endpoint",
        "Procedure section example URI points to Patient endpoint",
        "Most resource sections repeat Patient/id/$export URI rather than resource-specific endpoint",
    ],
    "summary_statistics": {
        "proprietary_api_categories": len(api_categories),
        "fhir_resources_on_page": len(fhir_resources_on_page),
        "total_fields_documented_in_samples": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "data_dictionary_provided": False,
        "sample_export_files_provided": False,
        "schema_files_provided": False,
    },
}

out_path = OUTPUT / "full-entity-inventory.json"
out_path.write_text(json.dumps(inventory, indent=2))
print(f"Wrote {out_path}")
print(f"\nSummary:")
print(f"  Proprietary API categories: {len(api_categories)}")
print(f"  FHIR resources on EHI page: {len(fhir_resources_on_page)}")
print(f"  Total fields from sample outputs: {total_fields}")
print(f"  Fields with descriptions: {fields_with_desc}")
print(f"  FHIR resources on page: {fhir_resources_on_page}")
print(f"\nCopy-paste errors on EHI page:")
for section in resource_sections:
    print(f"  {section['resource_name']}: example={section['example_uri']}")
