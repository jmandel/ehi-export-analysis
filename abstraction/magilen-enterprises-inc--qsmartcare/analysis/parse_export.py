"""
Parse the QSmartCare EHI export artifacts (PDF text + JSON sample) to produce
a full entity/field inventory (full-entity-inventory.json) and summary stats.
"""
import json
import re
import subprocess
import os

RESULTS = "/home/jmandel/hobby/ehi-export-analysis/results/magilen-enterprises-inc--qsmartcare/downloads"
OUT = os.path.dirname(os.path.abspath(__file__))

# ── 1. Parse the JSON sample ──
with open(os.path.join(RESULTS, "sample-ehi-export.json")) as f:
    raw_json = json.load(f)

org = raw_json["object"]["organization"]

def flatten_json_entity(key, value):
    """Extract fields from a JSON entity value."""
    fields = []
    if isinstance(value, dict):
        # Check for resourceType
        resource_type = value.get("resourceType", None)
        # Iterate top-level keys
        for k, v in value.items():
            if k == "resourceType":
                continue
            if k == "content":
                # Content can be list, dict, or string
                if isinstance(v, list):
                    if len(v) > 0 and isinstance(v[0], dict):
                        for sk in v[0]:
                            fields.append({
                                "name": f"content[].{sk}",
                                "sample_value": str(v[0][sk])[:100],
                                "type": type(v[0][sk]).__name__
                            })
                    elif len(v) > 0:
                        fields.append({
                            "name": "content[]",
                            "sample_value": str(v[0])[:100],
                            "type": type(v[0]).__name__
                        })
                elif isinstance(v, dict):
                    for sk, sv in v.items():
                        fields.append({
                            "name": f"content.{sk}",
                            "sample_value": str(sv)[:100],
                            "type": type(sv).__name__
                        })
                else:
                    fields.append({
                        "name": "content",
                        "sample_value": str(v)[:100],
                        "type": type(v).__name__
                    })
            elif isinstance(v, dict):
                for sk, sv in v.items():
                    fields.append({
                        "name": f"{k}.{sk}",
                        "sample_value": str(sv)[:100],
                        "type": type(sv).__name__
                    })
            elif isinstance(v, list):
                if len(v) > 0 and isinstance(v[0], dict):
                    for sk in v[0]:
                        fields.append({
                            "name": f"{k}[].{sk}",
                            "sample_value": str(v[0][sk])[:100],
                            "type": type(v[0][sk]).__name__
                        })
                else:
                    fields.append({
                        "name": k,
                        "sample_value": str(v)[:100],
                        "type": "list"
                    })
            else:
                fields.append({
                    "name": k,
                    "sample_value": str(v)[:100] if v is not None else "",
                    "type": type(v).__name__
                })
    return fields

# Build JSON entities
json_entities = {}
# Top-level org fields
for key in org:
    if key in ("resourceType", "identifier", "active", "type", "name", "alias",
               "phoneNumber", "repository", "address"):
        continue  # org-level metadata
    val = org[key]
    if isinstance(val, dict) and ("resourceType" in val or key in ("location", "careTeam")):
        json_entities[key] = {
            "resourceType": val.get("resourceType", key),
            "fields": flatten_json_entity(key, val)
        }

# Also add org itself and patient
json_entities["organization"] = {
    "resourceType": "Organization",
    "fields": [
        {"name": "identifier", "sample_value": org.get("identifier", ""), "type": "str"},
        {"name": "active", "sample_value": str(org.get("active", "")), "type": "bool"},
        {"name": "type", "sample_value": org.get("type", ""), "type": "str"},
        {"name": "name", "sample_value": org.get("name", ""), "type": "str"},
        {"name": "alias", "sample_value": org.get("alias", ""), "type": "str"},
        {"name": "phoneNumber", "sample_value": org.get("phoneNumber", ""), "type": "str"},
        {"name": "repository", "sample_value": org.get("repository", ""), "type": "str"},
        {"name": "address.streetAddress", "sample_value": org["address"].get("streetAddress", ""), "type": "str"},
        {"name": "address.city", "sample_value": org["address"].get("city", ""), "type": "str"},
        {"name": "address.state", "sample_value": org["address"].get("state", ""), "type": "str"},
        {"name": "address.postalCode", "sample_value": org["address"].get("postalCode", ""), "type": "str"},
        {"name": "address.country", "sample_value": org["address"].get("country", ""), "type": "str"},
    ]
}

# ── 2. Parse PDF sections ──
pdf_text = subprocess.run(
    ["pdftotext", "-layout", os.path.join(RESULTS, "Single-Patient-PDF-Download.pdf"), "-"],
    capture_output=True, text=True
).stdout

# Extract sections and their fields from the PDF
pdf_sections = []
current_section = None
current_fields = []

# Pattern for section headers (ALL CAPS followed by INFO or similar)
section_pattern = re.compile(r'^([A-Z][A-Z /&]+(?:INFO|HISTORIES|HISTORY|STATUS|TREATMENT|IMMUNIZATION))\s*$', re.MULTILINE)

# Find all sections
for match in section_pattern.finditer(pdf_text):
    if current_section:
        pdf_sections.append({"name": current_section, "raw_start": match.start()})
    current_section = match.group(1).strip()

if current_section:
    pdf_sections.append({"name": current_section, "raw_start": len(pdf_text)})

# Parse field names from PDF tabular data
# Field pattern: "Field Name    : Value" or table headers
pdf_section_details = {}
lines = pdf_text.split('\n')

# Track sections with their content
section_headers = [
    "DEMOGRAPHIC INFO",
    "ORGANIZATION INFO",
    "ORGANIZATION ADDRESS INFO",
    "LOCATION INFO",
    "CARE TEAM INFO",
    "ENCOUNTERS INFO",
    "HISTORY OF PRESENT ILLNESS INFO",
    "ASSESSMENT AND PLAN OF TREATMENT INFO",
    "PATIENT RELATIONSHIP INFO",
    "INSURANCE INFO",
    "SPOUSE INFO",
    "PAST MEDICAL HISTORY INFO",
    "ANTICOAGULANT INFO",
    "PATIENT WOUND INFO",
    "IMPLANTABLE DEVICE INFO",
    "ALLERGY INFO",
    "MEDICATION INFO",
    "DIAGNOSIS INFO",
    "LAB INFO",
    "BLOOD PRESSURE INFO",
    "BLOOD SUGAR INFO",
    "BMI INFO",
    "PULSE INFO",
    "PULSE OXIMETRY INFO",
    "BODY TEMPERATURE INFO",
    "HEART RATE INFO",
    "RESPIRATORY RATE INFO",
    "OXYGEN CONCENTRATION INFO",
    "PAST SURGICAL HISTORIES",
    "IMMUNIZATION",
    "FUNCTIONAL STATUS",
    "COGNITIVE STATUS",
]

# For each PDF section, identify field names
def extract_pdf_fields(section_name, text_block):
    fields = []
    # Pattern 1: "Field Name    : Value" (key-value pairs)
    kv_pattern = re.compile(r'([A-Za-z][A-Za-z &/]+?)\s{2,}:\s+(.+?)(?:\s{2,}|$)')
    # Pattern 2: Table headers (consecutive capitalized words separated by spaces)
    
    for m in kv_pattern.finditer(text_block):
        fname = m.group(1).strip()
        fval = m.group(2).strip()
        if fname and len(fname) > 1 and fname not in ("Page", "Website"):
            fields.append({"name": fname, "sample_value": fval[:100]})
    
    # Also look for table column headers
    # These are rows with multiple capitalized words
    return fields

# Find section boundaries
section_bounds = []
for i, line in enumerate(lines):
    stripped = line.strip()
    for sh in section_headers:
        if stripped == sh:
            section_bounds.append((sh, i))

# Extract field info for each section
for idx, (sec_name, start_line) in enumerate(section_bounds):
    end_line = section_bounds[idx + 1][1] if idx + 1 < len(section_bounds) else len(lines)
    block = '\n'.join(lines[start_line:end_line])
    fields = extract_pdf_fields(sec_name, block)
    pdf_section_details[sec_name] = fields

# ── 3. Build unified inventory ──
# Combine PDF and JSON into a unified entity inventory

# Map from PDF sections to entity names
pdf_to_entity = {
    "DEMOGRAPHIC INFO": "patient",
    "ORGANIZATION INFO": "organization",
    "ORGANIZATION ADDRESS INFO": "organization_address",
    "LOCATION INFO": "location",
    "CARE TEAM INFO": "careTeam",
    "ENCOUNTERS INFO": "encounter",
    "HISTORY OF PRESENT ILLNESS INFO": "hpi",
    "ASSESSMENT AND PLAN OF TREATMENT INFO": "planOfCare",
    "PATIENT RELATIONSHIP INFO": "patientRelationship",
    "INSURANCE INFO": "insurance",
    "SPOUSE INFO": "spouse",
    "PAST MEDICAL HISTORY INFO": "pastMedicalHistory",
    "ANTICOAGULANT INFO": "anticoagulants",
    "PATIENT WOUND INFO": "wounds",
    "IMPLANTABLE DEVICE INFO": "devices",
    "ALLERGY INFO": "allergies",
    "MEDICATION INFO": "medications",
    "DIAGNOSIS INFO": "diagnosis",
    "LAB INFO": "labs",
    "BLOOD PRESSURE INFO": "vitalSigns_bp",
    "BLOOD SUGAR INFO": "bloodSugar",
    "BMI INFO": "vitalSigns_bmi",
    "PULSE INFO": "vitalSigns_pulse",
    "PULSE OXIMETRY INFO": "vitalSigns_pulseOx",
    "BODY TEMPERATURE INFO": "vitalSigns_temp",
    "HEART RATE INFO": "vitalSigns_hr",
    "RESPIRATORY RATE INFO": "vitalSigns_rr",
    "OXYGEN CONCENTRATION INFO": "vitalSigns_o2",
    "PAST SURGICAL HISTORIES": "procedures",
    "IMMUNIZATION": "immunizations",
    "FUNCTIONAL STATUS": "functionalStatus",
    "COGNITIVE STATUS": "cognitiveStatus",
}

# Domain categorization
entity_domain = {
    "organization": "Organization",
    "organization_address": "Organization",
    "location": "Organization",
    "careTeam": "Care Team",
    "patient": "Demographics",
    "encounter": "Encounters",
    "hpi": "Clinical Notes",
    "planOfCare": "Care Plans",
    "patientRelationship": "Demographics",
    "insurance": "Insurance",
    "spouse": "Demographics",
    "pastMedicalHistory": "Problems / Conditions",
    "anticoagulants": "Medications",
    "wounds": "Wound Care (Specialty)",
    "devices": "Devices",
    "allergies": "Allergies",
    "medications": "Medications",
    "diagnosis": "Problems / Conditions",
    "labs": "Lab Results",
    "vitalSigns_bp": "Vital Signs",
    "bloodSugar": "Lab Results",
    "vitalSigns_bmi": "Vital Signs",
    "vitalSigns_pulse": "Vital Signs",
    "vitalSigns_pulseOx": "Vital Signs",
    "vitalSigns_temp": "Vital Signs",
    "vitalSigns_hr": "Vital Signs",
    "vitalSigns_rr": "Vital Signs",
    "vitalSigns_o2": "Vital Signs",
    "procedures": "Procedures",
    "immunizations": "Immunizations",
    "functionalStatus": "Assessments",
    "cognitiveStatus": "Assessments",
    "socialHistory": "Social History",
    "goals": "Care Plans",
    "healthConcerns": "Problems / Conditions",
    "assessments": "Assessments",
}

# Build full inventory
inventory = []

# PDF-only sections not in JSON
pdf_only_sections = {"INSURANCE INFO", "SPOUSE INFO", "PATIENT RELATIONSHIP INFO",
                     "PAST MEDICAL HISTORY INFO", "ANTICOAGULANT INFO", "LAB INFO",
                     "BLOOD SUGAR INFO", "FUNCTIONAL STATUS", "COGNITIVE STATUS",
                     "BLOOD PRESSURE INFO", "BMI INFO", "PULSE INFO",
                     "PULSE OXIMETRY INFO", "BODY TEMPERATURE INFO", "HEART RATE INFO",
                     "RESPIRATORY RATE INFO", "OXYGEN CONCENTRATION INFO",
                     "ORGANIZATION ADDRESS INFO"}

# JSON-only keys not directly in PDF
json_only_keys = {"socialHistory", "goals", "healthConcerns", "assessments"}

# Track all entities
all_entities = set()

# Add PDF sections
for sec_name, entity_name in pdf_to_entity.items():
    all_entities.add(entity_name)
    pdf_fields = pdf_section_details.get(sec_name, [])
    json_fields = json_entities.get(entity_name, {}).get("fields", [])
    
    in_pdf = True
    in_json = entity_name in json_entities
    
    entry = {
        "entity_name": entity_name,
        "pdf_section": sec_name,
        "domain": entity_domain.get(entity_name, "Other"),
        "in_pdf": in_pdf,
        "in_json": in_json,
        "pdf_field_count": len(pdf_fields),
        "json_field_count": len(json_fields),
        "pdf_fields": pdf_fields,
        "json_fields": json_fields,
    }
    inventory.append(entry)

# Add JSON-only entities
for key in json_only_keys:
    if key not in all_entities and key in json_entities:
        json_fields = json_entities[key]["fields"]
        entry = {
            "entity_name": key,
            "pdf_section": None,
            "domain": entity_domain.get(key, "Other"),
            "in_pdf": False,
            "in_json": True,
            "pdf_field_count": 0,
            "json_field_count": len(json_fields),
            "pdf_fields": [],
            "json_fields": json_fields,
        }
        inventory.append(entry)

# ── 4. Manually supplement with known fields from PDF inspection ──
# The regex-based extraction misses table headers; add them manually based on PDF reading

manual_pdf_fields = {
    "DEMOGRAPHIC INFO": [
        "First Name", "Last Name", "Middle Name", "Previous Name", "Suffix", "Sex",
        "Dob", "Marital Status", "Pref Language", "PCare Provider", "Race", "Ethnicity",
        "Current Address", "Previous Address", "Ssn", "Granular Race", "Phone", "Mobile",
        "Email", "Fax", "City", "State", "Address", "ZipCode"
    ],
    "ORGANIZATION INFO": [
        "Name", "Alias Name", "Phone No", "Fax No", "Repository"
    ],
    "ORGANIZATION ADDRESS INFO": [
        "Street Address", "City", "State", "Postal Code", "Country", "Website"
    ],
    "LOCATION INFO": [
        "Name", "Phone No", "Street Address", "City", "State", "Postal Code", "Country"
    ],
    "CARE TEAM INFO": [
        "First Name", "Last Name", "Phone No", "Role"
    ],
    "ENCOUNTERS INFO": [
        "Consult For", "Chief Complaints", "DOS", "Smoking Status"
    ],
    "HISTORY OF PRESENT ILLNESS INFO": [
        "History of Present Illness"
    ],
    "ASSESSMENT AND PLAN OF TREATMENT INFO": [
        "Assessment", "Plan Of Treatment"
    ],
    "PATIENT RELATIONSHIP INFO": [
        "Name", "Relationship"
    ],
    "INSURANCE INFO": [
        "Primary Insurance", "Secondary Insurance"
    ],
    "SPOUSE INFO": [
        "Name", "Occupation", "Workplace", "Work Phone", "Organization Name"
    ],
    "PAST MEDICAL HISTORY INFO": [
        "Diagnosis Code", "Diagnosis Name", "Start Date", "End Date", "Status"
    ],
    "ANTICOAGULANT INFO": [
        "Anticoagulant Name"
    ],
    "PATIENT WOUND INFO": [
        "Wound number", "Wound DOS", "Wound Location", "Wound Side",
        "Sub Location", "Vertical Plane", "Horizontal Plane", "Status"
    ],
    "IMPLANTABLE DEVICE INFO": [
        "Unique Device Identifiers", "Company Name", "Brand Name", "Version/Model",
        "MRI Safety Info", "Labeled Contains NRL", "GMDN PT Name", "Manufactured Date",
        "Expiration Date", "FDA Product Code", "FDA Product Name", "Status"
    ],
    "ALLERGY INFO": [
        "Allergies", "Allergy Reaction", "Updated", "Start Date", "End Date",
        "Severity", "Reaction Severity", "Types of Allergies", "Status"
    ],
    "MEDICATION INFO": [
        "Medication", "Medication Type", "Dosage", "Route", "Frequency",
        "RxNorm Code", "Status"
    ],
    "DIAGNOSIS INFO": [
        "Diagnosis Code", "Diagnosis Name", "Start Date", "End Date", "Status"
    ],
    "LAB INFO": [
        "Date", "Path", "Lab Name", "Lab Location"
    ],
    "BLOOD PRESSURE INFO": [
        "Date", "Systolic", "Diastolic"
    ],
    "BLOOD SUGAR INFO": [
        "Date", "Fasting", "Random", "HbA1c"
    ],
    "BMI INFO": [
        "Date", "Height", "Weight", "HbA1c"
    ],
    "PULSE INFO": [
        "Date", "Pulse"
    ],
    "PULSE OXIMETRY INFO": [
        "Date", "Pulse Oximetry"
    ],
    "BODY TEMPERATURE INFO": [
        "Date", "Temperature"
    ],
    "HEART RATE INFO": [
        "Date", "Heart Rate"
    ],
    "RESPIRATORY RATE INFO": [
        "Date", "Respiratory Rate"
    ],
    "OXYGEN CONCENTRATION INFO": [
        "Date", "Oxygen Concentration"
    ],
    "PAST SURGICAL HISTORIES": [
        "Procedure Code", "Procedure Name", "Start Date", "End Date", "OutCome", "Status"
    ],
    "IMMUNIZATION": [
        "Vaccine Code", "Code System", "Vaccine Name", "Date", "Status", "Additional Notes"
    ],
    "FUNCTIONAL STATUS": [
        "Code", "Code System", "Name", "Date"
    ],
    "COGNITIVE STATUS": [
        "Code", "Code System", "Name", "Date"
    ],
}

# Also add Social History and Family History from PDF (they appear inline in Encounters)
manual_pdf_fields["SOCIAL HISTORY"] = ["Social History"]
manual_pdf_fields["FAMILY HISTORY"] = ["Family History"]

# Rebuild inventory with manual fields
final_inventory = []
total_pdf_fields = 0
total_json_fields = 0

for sec_name, field_names in manual_pdf_fields.items():
    entity_name = pdf_to_entity.get(sec_name, sec_name.lower().replace(" ", "_"))
    json_ent = json_entities.get(entity_name, {})
    json_flds = json_ent.get("fields", [])
    
    pdf_fields = [{"name": fn, "description": None, "type": None} for fn in field_names]
    
    entry = {
        "entity_name": entity_name,
        "pdf_section": sec_name,
        "domain": entity_domain.get(entity_name, "Other"),
        "in_pdf": True,
        "in_json": entity_name in json_entities,
        "field_count": len(field_names),
        "json_field_count": len(json_flds),
        "fields": pdf_fields,
        "json_fields": json_flds,
    }
    final_inventory.append(entry)
    total_pdf_fields += len(field_names)
    total_json_fields += len(json_flds)

# Add JSON-only entities
for key in json_only_keys:
    if key in json_entities:
        json_flds = json_entities[key]["fields"]
        entry = {
            "entity_name": key,
            "pdf_section": None,
            "domain": entity_domain.get(key, "Other"),
            "in_pdf": False,
            "in_json": True,
            "field_count": len(json_flds),
            "json_field_count": len(json_flds),
            "fields": [{"name": f["name"], "description": None, "type": f.get("type")} for f in json_flds],
            "json_fields": json_flds,
        }
        final_inventory.append(entry)
        total_json_fields += len(json_flds)

# ── 5. Write outputs ──
with open(os.path.join(OUT, "full-entity-inventory.json"), "w") as f:
    json.dump(final_inventory, f, indent=2)

# Summary stats
unique_entities = len(final_inventory)
all_field_names = set()
for e in final_inventory:
    for fld in e["fields"]:
        all_field_names.add(f"{e['entity_name']}.{fld['name']}")

# Count by domain
domain_counts = {}
for e in final_inventory:
    d = e["domain"]
    if d not in domain_counts:
        domain_counts[d] = {"entities": 0, "fields": 0}
    domain_counts[d]["entities"] += 1
    domain_counts[d]["fields"] += e["field_count"]

# Entities in PDF but not JSON
pdf_not_json = [e["entity_name"] for e in final_inventory if e["in_pdf"] and not e["in_json"]]
json_not_pdf = [e["entity_name"] for e in final_inventory if e["in_json"] and not e["in_pdf"]]

summary = {
    "total_entities": unique_entities,
    "total_fields": len(all_field_names),
    "fields_with_descriptions": 0,  # No descriptions provided by vendor
    "fields_with_types": 0,  # No type documentation from vendor
    "in_pdf_only": pdf_not_json,
    "in_json_only": json_not_pdf,
    "domain_breakdown": domain_counts,
    "pdf_pages": 7,
    "json_file_size_bytes": 8413,
    "pdf_file_size_bytes": 39659,
}

with open(os.path.join(OUT, "summary-stats.json"), "w") as f:
    json.dump(summary, f, indent=2)

print("=== Summary Stats ===")
print(f"Total entities (PDF sections + JSON-only): {unique_entities}")
print(f"Total unique fields: {len(all_field_names)}")
print(f"Fields with descriptions: 0 (no data dictionary)")
print(f"Fields with types: 0 (no type documentation)")
print()
print("=== Domain Breakdown ===")
for d, c in sorted(domain_counts.items()):
    print(f"  {d}: {c['entities']} entities, {c['fields']} fields")
print()
print(f"=== PDF-only entities (not in JSON): {len(pdf_not_json)} ===")
for e in pdf_not_json:
    print(f"  - {e}")
print()
print(f"=== JSON-only entities (not in PDF): {len(json_not_pdf)} ===")
for e in json_not_pdf:
    print(f"  - {e}")
