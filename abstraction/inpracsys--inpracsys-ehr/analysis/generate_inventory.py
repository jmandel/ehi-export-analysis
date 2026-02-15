"""Generate a complete resource/field inventory table for the analysis."""
import json

with open("field_inventory.json") as f:
    resources = json.load(f)

print("| Resource Section | FHIR Resource | Fields | Described | Types | Category |")
print("|---|---|---|---|---|---|")

fhir_map = {
    "Patients": ("Patient", "Demographics"),
    "Smoking status": ("Observation", "Social History"),
    "Condition(Problem)": ("Condition", "Problems/Diagnoses"),
    "Medications": ("MedicationStatement", "Medications"),
    "Allergy or Intolerance": ("AllergyIntolerance", "Allergies"),
    "Laboratory Result DiagnosticReport": ("DiagnosticReport", "Lab Results"),
    "Laboratory Result Observations": ("DiagnosticOrder", "Lab Results"),
    "VitalSign": ("Observation", "Vitals"),
    "Procedure": ("Procedure", "Procedures"),
    "Care Team": ("Practitioner", "Care Team"),
    "Immunization": ("Immunization", "Immunizations"),
    "Implantable Devices/UDI": ("Device", "Devices"),
    "Assessment and Plan of Treatment": ("CarePlan", "Care Plans"),
    "Goal": ("Goal", "Goals"),
    "Health Concern": ("Condition/HealthcareService", "Problems/Diagnoses"),
}

total_f = 0
total_d = 0
total_t = 0
for r in resources:
    fhir, cat = fhir_map.get(r["section_title"], ("Unknown", "Unknown"))
    desc = r["fields_with_descriptions"]
    typed = r["fields_with_types"]
    fc = r["field_count"]
    total_f += fc
    total_d += desc
    total_t += typed
    type_str = "Yes" if typed == fc else f"{typed}/{fc}"
    print(f"| {r['section_title']} | {fhir} | {fc} | {desc} | {type_str} | {cat} |")

print(f"| **TOTAL** | **15 resources** | **{total_f}** | **{total_d}** | **{total_t}/{total_f}** | |")
