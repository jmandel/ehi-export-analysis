#!/usr/bin/env python3
"""
Parse all artifacts from the Minerva EHI export documentation and produce
a full-entity-inventory.json with all FHIR resource types and their data elements.

Sources:
1. Mphrx-EHI-export-documentation.pdf - lists supported FHIR resources for bulk export
2. FHIR-Data-Elements-mphrX.pdf - documents FHIR data type elements (not resource-specific)
3. Screenshot from PDF page 6 - shows ZIP file contents for single-patient export
"""

import json

# Resources explicitly listed in the bulk export documentation (Section 3.2.1, page 8)
bulk_export_resources = [
    "AllergyIntolerance", "CarePlan", "CareTeam", "Condition", "Device",
    "DiagnosticReport", "DocumentReference", "Encounter", "Goal",
    "Immunization", "Location", "Medication", "MedicationRequest",
    "Observation", "Organization", "Patient", "Practitioner",
    "PractitionerRole", "Procedure", "Provenance"
]

# Resources visible in the ZIP file screenshot (page 6 of EHI export doc)
# Note: ClinicalImpression appears in ZIP but NOT in the bulk API resource list
# Note: CarePlan, Condition, Device, Goal, Immunization, Organization, PractitionerRole
#       appear in bulk API list but NOT in the ZIP screenshot
single_patient_zip_files = [
    "allergyintolerance_file_1.ndjson",
    "careteam_file_1.ndjson",
    "clinicalimpression_file_1.ndjson",
    "diagnosticreport_file_1.ndjson",
    "documentreference_file_1.ndjson",
    "encounter_file_1.ndjson",
    "location_file_1.ndjson",
    "medication_file_1.ndjson",
    "medicationrequest_file_1.ndjson",
    "observation_file_1.ndjson",
    "patient_file_1.ndjson",
    "practitioner_file_1.ndjson",
    "procedure_file_1.ndjson",
    "provenance_file_1.ndjson",
    "readme.txt"
]

# Extract resource names from ZIP files
zip_resources = sorted(set(
    f.replace("_file_1.ndjson", "").title().replace("Allergyintolerance", "AllergyIntolerance")
    .replace("Careteam", "CareTeam").replace("Clinicalimpression", "ClinicalImpression")
    .replace("Diagnosticreport", "DiagnosticReport").replace("Documentreference", "DocumentReference")
    .replace("Medicationrequest", "MedicationRequest")
    for f in single_patient_zip_files if f.endswith(".ndjson")
))

# Union of all resources across both export methods
all_resources = sorted(set(bulk_export_resources) | set(zip_resources))

# The FHIR Data Elements document does NOT provide resource-specific field lists.
# It only documents FHIR complex data types (Coding, CodeableConcept, Attachment, etc.)
# and primitive types. No resource-level schema is provided.

# FHIR complex data types documented
complex_types = {
    "Coding": {
        "fields": [
            {"name": "system", "type": "String", "description": "Identity of the terminology system. In YYYY format.", "cardinality": "0..1"},
            {"name": "version", "type": "String", "description": "Version of the system - if relevant.", "cardinality": "0..1"},
            {"name": "code", "type": "code", "description": "Symbol in syntax defined by the system.", "cardinality": "0..1"},
            {"name": "display", "type": "String", "description": "Representation defined by the system.", "cardinality": "0..1"},
            {"name": "userSelected", "type": "Boolean", "description": "If this coding was chosen directly by the user.", "cardinality": "0..1"},
        ]
    },
    "CodeableConcept": {
        "fields": [
            {"name": "coding", "type": "Coding", "description": "Code defined by a terminology system.", "cardinality": "0..*"},
            {"name": "text", "type": "String", "description": "Plain text representation of the concept.", "cardinality": "0..1"},
        ]
    },
    "Attachment": {
        "fields": [
            {"name": "contentType", "type": "code", "description": "Mime type of the content, with charset etc.", "cardinality": "0..1"},
            {"name": "language", "type": "code", "description": "Human language of the content (BCP-47)", "cardinality": "0..1"},
            {"name": "data", "type": "base64Binary", "description": "Data inline, base64ed", "cardinality": "0..1"},
            {"name": "url", "type": "String", "description": "Uri where the data can be found", "cardinality": "0..1"},
            {"name": "size", "type": "unsignedInt", "description": "Number of bytes of content (if url provided)", "cardinality": "0..1"},
            {"name": "hash", "type": "base64Binary", "description": "Hash of the data (sha-1, base64ed)", "cardinality": "0..1"},
            {"name": "title", "type": "String", "description": "Label to display in place of data.", "cardinality": "0..1"},
            {"name": "creation", "type": "dateTime", "description": "Date attachment was first created.", "cardinality": "0..1"},
        ]
    },
    "Period": {
        "fields": [
            {"name": "start", "type": "dateTime", "description": "Starting time with inclusive boundary.", "cardinality": "0..1"},
            {"name": "end", "type": "dateTime", "description": "End time with inclusive boundary, if not ongoing.", "cardinality": "0..1"},
        ]
    },
    "Range": {
        "fields": [
            {"name": "low", "type": "SimpleQuantity", "description": "Low limit", "cardinality": "0..1"},
            {"name": "high", "type": "SimpleQuantity", "description": "High Limit", "cardinality": "0..1"},
        ]
    },
    "Ratio": {
        "fields": [
            {"name": "numerator", "type": "Quantity", "description": "Numerator value", "cardinality": "0..1"},
            {"name": "denominator", "type": "Quantity", "description": "Denominator value", "cardinality": "0..1"},
        ]
    },
    "SampledData": {
        "fields": [
            {"name": "origin", "type": "SimpleQuantity", "description": "Zero value and units", "cardinality": "1..1"},
            {"name": "period", "type": "decimal", "description": "Number of milliseconds between samples", "cardinality": "1..1"},
            {"name": "factor", "type": "decimal", "description": "Multiply data by this before adding to origin", "cardinality": "0..1"},
            {"name": "lowerLimit", "type": "decimal", "description": "Lower limit of detection", "cardinality": "0..1"},
            {"name": "upperLimit", "type": "decimal", "description": "Upper limit of detection", "cardinality": "0..1"},
            {"name": "dimensions", "type": "positiveInt", "description": "Number of sample points at each time point", "cardinality": "1..1"},
            {"name": "data", "type": "string", "description": "Decimal values with spaces, or 'E' | 'U' | 'L'", "cardinality": "0..1"},
        ]
    },
    "Quantity": {
        "fields": [
            {"name": "value", "type": "decimal", "description": "Numerical value (with implicit precision)", "cardinality": "0..1"},
            {"name": "comparator", "type": "code", "description": "< | <= | >= | > - how to understand the value", "cardinality": "0..1"},
            {"name": "unit", "type": "string", "description": "Unit representation", "cardinality": "0..1"},
            {"name": "system", "type": "uri", "description": "System that defines coded unit form", "cardinality": "0..1"},
            {"name": "code", "type": "code", "description": "Coded form of the unit", "cardinality": "0..1"},
        ]
    },
    "Duration": {
        "fields": [
            {"name": "value", "type": "decimal", "description": "Numerical value (with implicit precision)", "cardinality": "0..1"},
            {"name": "comparator", "type": "code", "description": "< | <= | >= | > - how to understand the value", "cardinality": "0..1"},
            {"name": "unit", "type": "string", "description": "Unit representation", "cardinality": "0..1"},
            {"name": "system", "type": "uri", "description": "System that defines coded unit form", "cardinality": "0..1"},
            {"name": "code", "type": "code", "description": "Coded form of the unit", "cardinality": "0..1"},
        ]
    },
    "Age": {
        "fields": [
            {"name": "value", "type": "decimal", "description": "Numerical value (with implicit precision)", "cardinality": "0..1"},
            {"name": "comparator", "type": "code", "description": "< | <= | >= | > - how to understand the value", "cardinality": "0..1"},
            {"name": "unit", "type": "string", "description": "Unit representation", "cardinality": "0..1"},
            {"name": "system", "type": "uri", "description": "System that defines coded unit form", "cardinality": "0..1"},
            {"name": "code", "type": "code", "description": "Coded form of the unit", "cardinality": "0..1"},
        ]
    },
    "Money": {
        "fields": [
            {"name": "value", "type": "decimal", "description": "Numerical value (with implicit precision)", "cardinality": "0..1"},
            {"name": "currency", "type": "code", "description": "IS0 4217 Currency Code (CurrencyCode)", "cardinality": "0..1"},
        ]
    },
    "Annotation": {
        "fields": [
            {"name": "author[x]", "type": "String|Reference", "description": "Individual responsible for the annotation", "cardinality": "0..1"},
            {"name": "time", "type": "dateTime", "description": "When the annotation was made", "cardinality": "0..1"},
            {"name": "text", "type": "markdown", "description": "The annotation - text content", "cardinality": "0..1"},
        ]
    },
    "Identifier": {
        "fields": [
            {"name": "use", "type": "code", "description": "IdentifierUse (Required) usual | official | temp | secondary (If known)", "cardinality": "0..1"},
            {"name": "type", "type": "CodeableConcept", "description": "Description of identifier.", "cardinality": "0..1"},
            {"name": "system", "type": "Uri", "description": "The namespace for the identifier value.", "cardinality": "0..1"},
            {"name": "value", "type": "String", "description": "The value that is unique.", "cardinality": "0..1"},
            {"name": "assigner", "type": "Reference(Organization)", "description": "Organization that issued id (may be just text).", "cardinality": "0..1"},
            {"name": "period", "type": "Period", "description": "Time period when ID is/was valid for use.", "cardinality": "0..1"},
        ]
    },
    "Address": {
        "fields": [
            {"name": "use", "type": "code", "description": "home | work | temp | old - purpose of this address.", "cardinality": "0..1"},
            {"name": "type", "type": "code", "description": "postal | physical | both", "cardinality": "0..1"},
            {"name": "text", "type": "String", "description": "Text representation of the address.", "cardinality": "0..1"},
            {"name": "line", "type": "String", "description": "Street name, number, direction & P.O. Box etc.", "cardinality": "0..*"},
            {"name": "city", "type": "String", "description": "Name of city, town etc.", "cardinality": "0..1"},
            {"name": "district", "type": "String", "description": "District name (aka county).", "cardinality": "0..1"},
            {"name": "state", "type": "String", "description": "Sub-unit of country (abbreviations ok).", "cardinality": "0..1"},
            {"name": "postalCode", "type": "String", "description": "Postal code for area.", "cardinality": "0..1"},
            {"name": "country", "type": "String", "description": "Country (e.g. can be ISO 3166 2 or 3 letter code).", "cardinality": "0..1"},
            {"name": "period", "type": "Period", "description": "Time period when address was/is in use.", "cardinality": "0..1"},
        ]
    },
    "HumanName": {
        "fields": [
            {"name": "use", "type": "code", "description": "usual | official | temp | nickname | anonymous | old | maiden", "cardinality": "0..1"},
            {"name": "text", "type": "String", "description": "Text representation of the full name.", "cardinality": "0..1"},
            {"name": "family", "type": "String", "description": "Family name (often called 'Surname').", "cardinality": "0..1"},
            {"name": "given", "type": "String", "description": "Given names (not always 'first'). Includes middle names.", "cardinality": "0..*"},
            {"name": "prefix", "type": "String", "description": "Parts that come before the name.", "cardinality": "0..*"},
            {"name": "suffix", "type": "String", "description": "Parts that come after the name.", "cardinality": "0..*"},
            {"name": "period", "type": "Period", "description": "Time period when the name was/is in use.", "cardinality": "0..1"},
        ]
    },
    "ContactPoint": {
        "fields": [
            {"name": "system", "type": "code", "description": "phone | fax | email | pager | url | sms | other", "cardinality": "0..1"},
            {"name": "value", "type": "String", "description": "The actual contact point details", "cardinality": "0..1"},
            {"name": "use", "type": "code", "description": "home | work | temp | old | mobile - purpose of this contact point", "cardinality": "0..1"},
            {"name": "rank", "type": "Positive Integer", "description": "The actual contact point details.", "cardinality": "0..1"},
            {"name": "period", "type": "Period", "description": "Time period when the contact point was/is in use.", "cardinality": "0..1"},
        ]
    },
    "Timing": {
        "fields": [
            {"name": "event", "type": "dateTime", "description": "When the event occurs", "cardinality": "0..*"},
            {"name": "code", "type": "CodeableConcept", "description": "BID | TID | QID | AM | PM | QD | QOD | +", "cardinality": "0..1"},
            {"name": "repeat", "type": "Element", "description": "When the event is to occur", "cardinality": "0..1"},
            {"name": "repeat.bounds[x]", "type": "Duration|Range|Period", "description": "Length/Range of lengths, or (Start and/or end) limits", "cardinality": "0..1"},
            {"name": "repeat.count", "type": "positiveInt", "description": "Number of times to repeat", "cardinality": "0..1"},
            {"name": "repeat.countMax", "type": "positiveInt", "description": "Maximum number of times to repeat", "cardinality": "0..1"},
            {"name": "repeat.duration", "type": "decimal", "description": "How long when it happens", "cardinality": "0..1"},
            {"name": "repeat.durationMax", "type": "decimal", "description": "How long when it happens (Max)", "cardinality": "0..1"},
            {"name": "repeat.durationUnit", "type": "code", "description": "s | min | h | d | wk | mo | a - unit of time (UCUM)", "cardinality": "0..1"},
            {"name": "repeat.frequency", "type": "positiveInt", "description": "Event occurs frequency times per period", "cardinality": "0..1"},
            {"name": "repeat.frequencyMax", "type": "positiveInt", "description": "Event occurs up to frequencyMax times per period", "cardinality": "0..1"},
            {"name": "repeat.period", "type": "decimal", "description": "Event occurs frequency times per period", "cardinality": "0..1"},
            {"name": "repeat.periodMax", "type": "decimal", "description": "Upper limit of period (3-4 hours)", "cardinality": "0..1"},
            {"name": "repeat.periodUnit", "type": "code", "description": "s | min | h | d | wk | mo | a - unit of time (UCUM)", "cardinality": "0..1"},
            {"name": "repeat.dayOfWeek", "type": "code", "description": "mon | tue | wed | thu | fri | sat | sun", "cardinality": "0..*"},
            {"name": "repeat.timeOfDay", "type": "time", "description": "Time of day for action", "cardinality": "0..*"},
            {"name": "repeat.when", "type": "unsignedInt", "description": "Code for time period of occurrence (EventTiming)", "cardinality": "0..*"},
            {"name": "repeat.offset", "type": "unsignedInt", "description": "BID | TID | QID | AM | PM | QD | QOD | +", "cardinality": "0..1"},
        ]
    },
    "Reference": {
        "fields": [
            {"name": "reference", "type": "String", "description": "Literal reference, Relative, internal or absolute URL", "cardinality": "0..1"},
        ]
    }
}

# Primitive types documented
primitive_types = {
    "boolean": "true | false",
    "integer": "A signed 32-bit integer",
    "string": "A sequence of Unicode characters",
    "decimal": "Rational numbers that have a decimal representation.",
    "uri": "A Uniform Resource Identifier Reference (RFC 3986). Note: URIs are case sensitive.",
    "url": "A Uniform Resource Locator.",
    "canonical": "A URI that refers to a resource by its canonical URL.",
    "base64Binary": "A stream of bytes, base64 encoded (RFC 4648)",
    "instant": "An instant in time - known at least to the second and always includes a time zone.",
    "date": "Dates SHALL be valid dates. Format: yyyy-MM-dd",
    "dateTime": "Dates SHALL be valid dates. Format: yyyy-MM-dd HH:mm:ss or yyyy-MM-dd'T'HH:mm:ssZ",
    "time": "A time during the day, with no date specified.",
    "code": "A code is restricted to a string which has at least one character and no leading or trailing whitespace.",
    "oid": "An OID represented as a URI (RFC 3001)",
    "id": "Any combination of ASCII letters, numerals, '-' and '.', length limit of 64 characters.",
    "markdown": "A string that may contain markdown syntax.",
    "unsignedInt": "Any non-negative integer (>= 0)",
    "positiveInt": "Any positive integer (>= 1)",
    "uuid": "A UUID (aka GUID) represented as a URI",
}

# Build the full entity inventory
inventory = {
    "product": "Minerva V4",
    "vendor": "agilon health inc. (formerly MphRx)",
    "export_format": "FHIR R4 NDJSON",
    "export_mechanism": {
        "single_patient": "UI-based export from Minerva portal (Clinical Admin/Admin role)",
        "bulk_export": "FHIR Bulk Data Export API using SMART Backend Services Authorization",
        "file_format": "NDJSON (one file per resource type, split at 10,000 records)",
        "delivery": "Single patient: ZIP download via notification; Bulk: async polling then download URLs (expire in 48hrs)"
    },
    "documentation_sources": [
        {
            "file": "Mphrx-EHI-export-documentation.pdf",
            "pages": 12,
            "description": "EHI export process documentation with UI screenshots and API details",
            "date": "2021-06-04"
        },
        {
            "file": "FHIR-Data-Elements-mphrX.pdf",
            "pages": 8,
            "description": "FHIR complex and primitive data type definitions (NOT resource-specific fields)",
            "date": "2021-05-21",
            "note": "This document only covers generic FHIR data types, not the specific fields/elements of each exported resource"
        },
        {
            "file": "FHIR-Search-Guide-mphrX.pdf",
            "pages": 10,
            "description": "FHIR search parameter documentation for the API",
            "date": "2021-05-21"
        },
        {
            "file": "Mandatory-Disclosures-Letter_MphRx.pdf",
            "pages": 5,
            "description": "ONC mandatory disclosures letter with cost/fee information",
            "date": "2021-05-25"
        }
    ],
    "fhir_resources": {},
    "discrepancies": {
        "ui_vs_api": {
            "description": "The single-patient UI export ZIP screenshot (page 6) shows different resources than the bulk API supported list (page 8)",
            "in_zip_not_in_api": ["ClinicalImpression"],
            "in_api_not_in_zip": ["CarePlan", "Condition", "Device", "Goal", "Immunization", "Organization", "PractitionerRole"],
            "note": "ZIP screenshot may reflect a specific patient's data (empty resources omitted) rather than a true difference in supported types"
        }
    },
    "data_types_documented": {
        "complex_types": complex_types,
        "primitive_types": primitive_types,
        "total_complex_types": len(complex_types),
        "total_primitive_types": len(primitive_types),
        "total_complex_type_fields": sum(len(t["fields"]) for t in complex_types.values())
    }
}

# Build resource entries - we have NO vendor-specific field documentation per resource
# The vendor only documents FHIR data types, not resource schemas
for resource in all_resources:
    in_bulk_api = resource in bulk_export_resources
    in_zip = resource in zip_resources

    # Map resources to EHI domains
    domain_map = {
        "AllergyIntolerance": "Allergies",
        "CarePlan": "Care plans / goals",
        "CareTeam": "Care plans / goals",
        "ClinicalImpression": "Clinical notes / documents",
        "Condition": "Problems / conditions / diagnoses",
        "Device": "Procedures",
        "DiagnosticReport": "Lab results / diagnostic reports",
        "DocumentReference": "Clinical notes / documents",
        "Encounter": "Encounters / visits",
        "Goal": "Care plans / goals",
        "Immunization": "Immunizations",
        "Location": "Encounters / visits (supporting)",
        "Medication": "Medications / prescriptions",
        "MedicationRequest": "Medications / prescriptions",
        "Observation": "Vitals / lab results / clinical observations",
        "Organization": "Demographics (supporting)",
        "Patient": "Demographics",
        "Practitioner": "Encounters / visits (supporting)",
        "PractitionerRole": "Encounters / visits (supporting)",
        "Procedure": "Procedures",
        "Provenance": "Data provenance / audit",
    }

    inventory["fhir_resources"][resource] = {
        "resource_type": resource,
        "in_bulk_api": in_bulk_api,
        "in_single_patient_zip": in_zip,
        "ehi_domain": domain_map.get(resource, "Unknown"),
        "vendor_field_documentation": None,
        "note": "No resource-specific field documentation provided by vendor. Standard FHIR R4 resource definitions apply."
    }

# Summary statistics
inventory["summary"] = {
    "total_fhir_resources_supported": len(all_resources),
    "resources_in_bulk_api": len(bulk_export_resources),
    "resources_in_single_patient_zip": len(zip_resources),
    "resource_specific_field_docs": 0,
    "vendor_data_dictionary": False,
    "sample_data_provided": False,
    "native_database_export": False,
    "export_is_fhir_projection": True,
    "domains_with_dedicated_resources": [
        "Demographics",
        "Encounters / visits",
        "Problems / conditions / diagnoses",
        "Medications / prescriptions",
        "Allergies",
        "Immunizations",
        "Vitals / lab results",
        "Diagnostic reports",
        "Clinical notes / documents",
        "Care plans / goals",
        "Procedures"
    ],
    "domains_missing": [
        "Insurance / coverage",
        "Claims / billing",
        "Payments",
        "Orders / referrals",
        "Patient communications / portal messages",
        "Consents / directives",
        "Scheduling / appointments (natively generated)",
        "Care coordination tasks (natively generated)",
        "Patient-reported outcomes (natively generated)"
    ]
}

output_path = "/home/jmandel/hobby/ehi-export-analysis/abstraction/agilon-health-inc--minerva/analysis/full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

print(f"Written to {output_path}")
print(f"\nSummary:")
print(f"  Total FHIR resources: {inventory['summary']['total_fhir_resources_supported']}")
print(f"  In bulk API: {inventory['summary']['resources_in_bulk_api']}")
print(f"  In single-patient ZIP: {inventory['summary']['resources_in_single_patient_zip']}")
print(f"  Resource-specific field docs: {inventory['summary']['resource_specific_field_docs']}")
print(f"  Vendor data dictionary: {inventory['summary']['vendor_data_dictionary']}")
print(f"  Complex data types documented: {inventory['data_types_documented']['total_complex_types']}")
print(f"  Complex type fields: {inventory['data_types_documented']['total_complex_type_fields']}")
print(f"  Primitive types documented: {inventory['data_types_documented']['total_primitive_types']}")
print(f"  Domains covered: {len(inventory['summary']['domains_with_dedicated_resources'])}")
print(f"  Domains missing: {len(inventory['summary']['domains_missing'])}")
