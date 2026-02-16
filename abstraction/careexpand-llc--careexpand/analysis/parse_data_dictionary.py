"""
Parse the Careexpand EHI export data dictionary from the PNG image.
The data dictionary is an image (not structured data), so we manually
transcribe the 17 fields visible in data-dictionary-table.png.
This is the complete content of the only data dictionary provided.
"""

import json

# Transcribed from data-dictionary-table.png (verified against image)
fields = [
    {"field": "patient_name", "description": "Full name of the patient", "data_type": "String", "required": True},
    {"field": "dob", "description": "Date of birth of the patient", "data_type": "Date (YYYY-MM-DD)", "required": True},
    {"field": "gender", "description": "Patient's gender", "data_type": "String (M/F/Other)", "required": True},
    {"field": "race", "description": "Race of the patient", "data_type": "String", "required": False},
    {"field": "ethnicity", "description": "Ethnicity of the patient", "data_type": "String", "required": False},
    {"field": "language", "description": "Preferred language of communication", "data_type": "String", "required": False},
    {"field": "address", "description": "Patient's home address", "data_type": "String", "required": False},
    {"field": "phone", "description": "Contact number", "data_type": "String", "required": False},
    {"field": "emergency_contact", "description": "Emergency contact name and phone", "data_type": "String", "required": False},
    {"field": "smoking_status", "description": "Patient's smoking habits", "data_type": "String", "required": False},
    {"field": "problem_list", "description": "List of active and past medical problems", "data_type": "Array (Structured)", "required": True},
    {"field": "medications", "description": "Active and past medications", "data_type": "Array (Structured)", "required": True},
    {"field": "allergies", "description": "Patient allergies", "data_type": "Array (Structured)", "required": True},
    {"field": "lab_results", "description": "Laboratory test results", "data_type": "Array (Structured)", "required": False},
    {"field": "procedures", "description": "Medical procedures performed", "data_type": "Array (Structured)", "required": False},
    {"field": "encounters", "description": "Clinical encounters and visits", "data_type": "Array (Structured)", "required": True},
    {"field": "vital_signs", "description": "Blood pressure, heart rate, temperature, etc.", "data_type": "Array (Structured)", "required": False},
]

# Build the full inventory
inventory = {
    "source": "data-dictionary-table.png (manually transcribed from image)",
    "source_document": "b10-ehi-export-ccda (HTML/PDF/Markdown)",
    "export_format": "C-CDA 2.1 XML",
    "total_fields": len(fields),
    "fields_with_descriptions": sum(1 for f in fields if f["description"]),
    "fields_required": sum(1 for f in fields if f["required"]),
    "fields_optional": sum(1 for f in fields if not f["required"]),
    "demographic_fields": sum(1 for f in fields if f["data_type"].startswith("String") or f["data_type"].startswith("Date")),
    "structured_array_fields": sum(1 for f in fields if "Array" in f["data_type"]),
    "note": "Additional fields may be included depending on the data available for the patient.",
    "fields": fields
}

# Summary stats
print("=== Careexpand EHI Export Data Dictionary Summary ===")
print(f"Total fields:              {inventory['total_fields']}")
print(f"Fields with descriptions:  {inventory['fields_with_descriptions']} ({inventory['fields_with_descriptions']/inventory['total_fields']*100:.0f}%)")
print(f"Required fields:           {inventory['fields_required']}")
print(f"Optional fields:           {inventory['fields_optional']}")
print(f"Demographic fields:        {inventory['demographic_fields']}")
print(f"Structured array fields:   {inventory['structured_array_fields']}")
print()
print("Field categories:")
print(f"  Demographics (simple strings/dates): {inventory['demographic_fields']}")
print(f"  Clinical data (Array Structured):    {inventory['structured_array_fields']}")
print()
print("Note: The 7 'Array (Structured)' fields have NO sub-field documentation.")
print("Note: No value sets, code systems, or foreign keys are documented.")
print("Note: The data dictionary is an IMAGE (PNG), not structured/machine-readable data.")

# Write full inventory
with open("full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)
print(f"\nWrote full-entity-inventory.json")

# Write summary stats
with open("summary-stats.txt", "w") as f:
    f.write("Careexpand EHI Export - Summary Statistics\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Source: Single BookStack wiki page (b10 EHI Export - CCDA)\n")
    f.write(f"Export format: C-CDA 2.1 XML via API\n")
    f.write(f"API endpoint: POST /patient/:idPatient/getPatientCCDAData\n")
    f.write(f"Authentication: JWT Bearer Token\n\n")
    f.write(f"Data Dictionary:\n")
    f.write(f"  Total fields:              {inventory['total_fields']}\n")
    f.write(f"  Fields with descriptions:  {inventory['fields_with_descriptions']} (100%)\n")
    f.write(f"  Fields with types:         {inventory['total_fields']} (100%)\n")
    f.write(f"  Value sets documented:     0\n")
    f.write(f"  Relationships documented:  0\n")
    f.write(f"  Sub-fields documented:     0 (7 Array fields have no sub-field detail)\n\n")
    f.write(f"Entities/tables:  1 (single flat list)\n")
    f.write(f"Total fields:     17\n")
    f.write(f"Sample data:      No\n")
    f.write(f"Machine-readable: No (data dictionary is a PNG image)\n")
print("Wrote summary-stats.txt")
