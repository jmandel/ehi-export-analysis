"""Build entity inventory from FHIR API documentation - the only technical spec available."""
import json

# The FHIR API docs list these resource types with their USCDI data elements.
# This is the complete inventory of what's documented.

resources = [
    {
        "resource": "AllergyIntolerance",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Substance (Drug Class)", "uscdi": "v1"},
            {"name": "Substance (Medication)", "uscdi": "v1"},
            {"name": "Reaction", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/AllergyIntolerance/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/AllergyIntolerance/?patient={id}&date={date}", "description": "Search by patient, date"}
        ]
    },
    {
        "resource": "CarePlan",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Assessment and Plan of Treatment", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/CarePlan/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/CarePlan/?patient={id}&date={date}&status={status}", "description": "Search by patient, date, status"}
        ]
    },
    {
        "resource": "CareTeam",
        "category": "Clinical",
        "uscdi_version": "v1/v2",
        "data_elements": [
            {"name": "Care Team", "uscdi": "v1"},
            {"name": "Care Team Member Name", "uscdi": "v2"},
            {"name": "Care Team Member Identifier", "uscdi": "v2"},
            {"name": "Care Team Member Role", "uscdi": "v2"},
            {"name": "Care Team Member Location", "uscdi": "v2"},
            {"name": "Care Team Member Telecom", "uscdi": "v2"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/CareTeam/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/CareTeam/?patient={id}&date={date}&status={status}", "description": "Search by patient, date, status"}
        ]
    },
    {
        "resource": "Condition",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Health Concern", "uscdi": "v1"},
            {"name": "Problems", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Condition/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/Condition/?patient={id}&asserted-date={date}", "description": "Search by patient, date"}
        ]
    },
    {
        "resource": "Device",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Unique Device Identifier(s) for Implantable Device(s)", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Device/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/Device/?patient={id}", "description": "Search by patient"}
        ]
    },
    {
        "resource": "DocumentReference",
        "category": "Clinical Notes",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Consultation Note", "uscdi": "v1"},
            {"name": "Discharge Summary Note", "uscdi": "v1"},
            {"name": "History & Physical", "uscdi": "v1"},
            {"name": "Procedure Note", "uscdi": "v1"},
            {"name": "Progress Note", "uscdi": "v1"},
            {"name": "Imaging Narrative", "uscdi": "v1"},
            {"name": "Laboratory Report Narrative", "uscdi": "v1"},
            {"name": "Pathology Report Narrative", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/DocumentReference/{id}", "description": "Retrieve CCDA by id"},
            {"method": "GET", "path": "/DocumentReference/?patient={id}&period={period}&status={status}", "description": "Search by patient, period, status"}
        ],
        "notes": "Documents returned as encoded C-CDA in content.attachment field"
    },
    {
        "resource": "Encounter",
        "category": "Clinical",
        "uscdi_version": "v2",
        "data_elements": [
            {"name": "Encounter Type", "uscdi": "v2"},
            {"name": "Encounter Diagnosis", "uscdi": "v2"},
            {"name": "Encounter Time", "uscdi": "v2"},
            {"name": "Encounter Location", "uscdi": "v2"},
            {"name": "Encounter Disposition", "uscdi": "v2"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Encounter/{id}", "description": "Retrieve by id"}
        ]
    },
    {
        "resource": "Goal",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Goals", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Goal/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/Goal/?patient={id}&target-date={date}", "description": "Search by patient, target-date"}
        ]
    },
    {
        "resource": "Immunization",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Immunization", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Immunization/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/Immunization/?patient={id}&date={date}", "description": "Search by patient, date"}
        ]
    },
    {
        "resource": "Location",
        "category": "Administrative",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Facility", "uscdi": "v1"},
            {"name": "NPI", "uscdi": "v1"},
            {"name": "Status", "uscdi": "v1"},
            {"name": "Address", "uscdi": "v1"},
            {"name": "Telecom", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Location/{id}", "description": "Retrieve by id"}
        ]
    },
    {
        "resource": "Medication",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Medications", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Medication/{id}", "description": "Retrieve by id"}
        ]
    },
    {
        "resource": "MedicationRequest",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Medications", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/MedicationRequest?Patient={id}", "description": "Search by patient"}
        ]
    },
    {
        "resource": "Observation",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Laboratory Tests", "uscdi": "v1"},
            {"name": "Laboratory Values/Results", "uscdi": "v1"},
            {"name": "Smoking Status", "uscdi": "v1"},
            {"name": "Diastolic Blood Pressure", "uscdi": "v1"},
            {"name": "Systolic Blood Pressure", "uscdi": "v1"},
            {"name": "Body Height", "uscdi": "v1"},
            {"name": "Body Weight", "uscdi": "v1"},
            {"name": "Heart Rate", "uscdi": "v1"},
            {"name": "Respiratory Rate", "uscdi": "v1"},
            {"name": "Body Temperature", "uscdi": "v1"},
            {"name": "Pulse Oximetry", "uscdi": "v1"},
            {"name": "Inhaled Oxygen Concentration", "uscdi": "v1"},
            {"name": "BMI Percentile (2-20 years old)", "uscdi": "v1"},
            {"name": "Weight-for-Length Percentile (Birth-36 months)", "uscdi": "v1"},
            {"name": "Occipital-frontal Head Circumference Percentile (Birth-36 months)", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Observation/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/Observation/?patient={id}&date={date}&category={category}", "description": "Search by patient, date, category"}
        ]
    },
    {
        "resource": "Patient",
        "category": "Demographics",
        "uscdi_version": "v1/v2",
        "data_elements": [
            {"name": "First Name", "uscdi": "v1"},
            {"name": "Middle Name", "uscdi": "v1"},
            {"name": "Last Name", "uscdi": "v1"},
            {"name": "Previous Name", "uscdi": "v1"},
            {"name": "Suffix", "uscdi": "v1"},
            {"name": "Sex (Assigned at Birth)", "uscdi": "v1"},
            {"name": "Sexual Orientation", "uscdi": "v2"},
            {"name": "Gender Identity", "uscdi": "v2"},
            {"name": "Date of Birth", "uscdi": "v1"},
            {"name": "Race", "uscdi": "v1"},
            {"name": "Ethnicity", "uscdi": "v1"},
            {"name": "Preferred Language", "uscdi": "v1"},
            {"name": "Address", "uscdi": "v1"},
            {"name": "Phone Number", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Patient/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/Patient/{id}?versionId={versionId}", "description": "Retrieve historical version"},
            {"method": "GET", "path": "/Patient/?name={name}&birthdate={date}", "description": "Search by name, birthdate, gender, identifier"}
        ]
    },
    {
        "resource": "Practitioner",
        "category": "Administrative",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Role", "uscdi": "v1"},
            {"name": "Name", "uscdi": "v1"},
            {"name": "First Name", "uscdi": "v1"},
            {"name": "Last Name", "uscdi": "v1"},
            {"name": "DOB", "uscdi": "v1"},
            {"name": "NPI", "uscdi": "v1"},
            {"name": "Status", "uscdi": "v1"},
            {"name": "Address", "uscdi": "v1"},
            {"name": "Telecom", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Practitioner/{id}", "description": "Retrieve by id"}
        ]
    },
    {
        "resource": "Procedure",
        "category": "Clinical",
        "uscdi_version": "v1",
        "data_elements": [
            {"name": "Procedures", "uscdi": "v1"}
        ],
        "endpoints": [
            {"method": "GET", "path": "/Procedure/{id}", "description": "Retrieve by id"},
            {"method": "GET", "path": "/Procedure/?patient={id}&date={date}", "description": "Search by patient, date"}
        ]
    }
]

# Summary stats
total_resources = len(resources)
total_elements = sum(len(r['data_elements']) for r in resources)
total_endpoints = sum(len(r['endpoints']) for r in resources)

# Unique FHIR resource types (some share like Medication/MedicationRequest)
unique_fhir_types = set()
for r in resources:
    unique_fhir_types.add(r['resource'])

# Category breakdown
categories = {}
for r in resources:
    cat = r['category']
    if cat not in categories:
        categories[cat] = {'resources': 0, 'elements': 0}
    categories[cat]['resources'] += 1
    categories[cat]['elements'] += len(r['data_elements'])

summary = {
    "source": "cures-update-fhir-api-docs.html (FHIR API documentation)",
    "source_url": "https://thesnfist.com/cures-update/",
    "analysis_notes": "This is the (g)(10) FHIR API documentation. No separate (b)(10) data dictionary exists.",
    "total_fhir_resource_types": total_resources,
    "total_uscdi_data_elements": total_elements,
    "total_api_endpoints": total_endpoints,
    "unique_endpoint_resource_types": len(unique_fhir_types),
    "category_breakdown": categories,
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema": False,
    "has_value_sets": False,
    "has_field_descriptions": False,
    "has_relationships": False,
    "documentation_type": "FHIR API endpoint documentation only"
}

# Write full inventory
with open('entity-inventory-full.json', 'w') as f:
    json.dump({"resources": resources, "summary": summary}, f, indent=2)

# Write summary
with open('entity-inventory-summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
