"""
Detailed field inventory for the Vital Dataset, which has nested structure
where element names (Value, Unit) repeat under different parent elements.
Counts unique field paths rather than unique element names.
"""

# Manual enumeration of Vital Dataset fields from the XML sample
# (necessary because automated parsing collapses duplicate element names)

vital_fields = [
    {"path": "PatientId", "sample": "25152"},
    {"path": "EncounterId", "sample": "3224"},
    {"path": "BodyTemperature/Temperature/Value", "sample": "98"},
    {"path": "BodyTemperature/Temperature/Unit", "sample": "C"},
    {"path": "BodyTemperature/Location", "sample": "Oral"},
    {"path": "BloodPressure/Systolic/Value", "sample": "120"},
    {"path": "BloodPressure/Diastolic/Value", "sample": "85"},
    {"path": "Pulse/Value", "sample": "125"},
    {"path": "Pulse/Unit", "sample": "%"},
    {"path": "Respiration/Value", "sample": "102"},
    {"path": "Respiration/Unit", "sample": "/min"},
    {"path": "SpO2/Value", "sample": "98"},
    {"path": "SpO2/Unit", "sample": "%"},
    {"path": "FiO2/Value", "sample": "98"},
    {"path": "FiO2/Unit", "sample": "%"},
    {"path": "Height/Value", "sample": "25"},
    {"path": "Height/Unit", "sample": "in"},
    {"path": "Weight/Value", "sample": "120"},
    {"path": "Weight/Unit", "sample": "lbs"},
    {"path": "BMI", "sample": "132.88"},
    {"path": "TimeRecorded", "sample": "2022-09-06T13:00:25"},
]

print(f"Vital Dataset: {len(vital_fields)} leaf fields (by path)")
for f in vital_fields:
    print(f"  - {f['path']} = {f['sample']}")

# Corrected total across all datasets
# Patient: 22, Encounter: 10, Device: 11, Immunization: 7, Allergy: 7, 
# Procedure: 9, Vital: 21 (corrected from 7), Condition: 9
corrected_total = 22 + 10 + 11 + 7 + 7 + 9 + 21 + 9
print(f"\nCorrected total leaf fields across all 8 datasets: {corrected_total}")
# vs original count of 82 (due to Vital undercount)
# Difference: {corrected_total - 82} fields undercounted in Vital
print(f"Vital undercount was: {21 - 7} = 14 fields (shared element names)")
