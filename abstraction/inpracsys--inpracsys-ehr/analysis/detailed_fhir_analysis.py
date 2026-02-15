"""Detailed analysis of FHIR API docs: map tables to resources, count fields, check descriptions."""

from html.parser import HTMLParser
import json
import re

class DetailedParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []  # list of (tag, attrs, text) in order
        self.current_text = ""
        self.tag_stack = []
        
    def handle_starttag(self, tag, attrs):
        if self.current_text.strip():
            self.elements.append(("text", {}, self.current_text))
            self.current_text = ""
        self.elements.append(("start", tag, dict(attrs)))
        self.tag_stack.append(tag)
        
    def handle_endtag(self, tag):
        if self.current_text.strip():
            self.elements.append(("text", {}, self.current_text))
            self.current_text = ""
        self.elements.append(("end", tag, {}))
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
            
    def handle_data(self, data):
        self.current_text += data


with open("/home/jmandel/hobby/ehi-export-analysis/results/inpracsys--inpracsys-ehr/downloads/fhir-api-documentation-page.html") as f:
    html = f.read()

# Strategy: Parse section by section using h2 headings as resource boundaries
# Then find field definition tables within each section

# Extract sections by h2 headings
sections = re.split(r'<h2[^>]*>', html)
resources = []

for section in sections[1:]:  # skip content before first h2
    # Get section title
    title_match = re.match(r'([^<]+)', section)
    if not title_match:
        continue
    title = title_match.group(1).strip()
    
    # Find field definition tables (with 4 columns: Name, Type, Cardinality, Description)
    table_pattern = r'<table[^>]*>(.*?)</table>'
    tables = re.findall(table_pattern, section, re.DOTALL)
    
    section_fields = []
    param_tables = []
    response_tables = []
    
    for table_html in tables:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
        if not rows:
            continue
        
        # Parse header
        header_cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', rows[0], re.DOTALL)
        header = [re.sub(r'<[^>]+>', '', c).strip() for c in header_cells]
        
        if 'Cardinality' in header:
            # This is a response field definition table
            for row in rows[1:]:
                cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
                cells_clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
                if len(cells_clean) >= 4:
                    field = {
                        "name": cells_clean[0],
                        "type": cells_clean[1],
                        "cardinality": cells_clean[2],
                        "description": cells_clean[3]
                    }
                    section_fields.append(field)
            response_tables.append(len(rows) - 1)
        elif 'Required' in ' '.join(header):
            param_tables.append(len(rows) - 1)
    
    if section_fields:
        # Check description quality
        fields_with_desc = sum(1 for f in section_fields if f["description"] and len(f["description"]) > 2)
        fields_with_type = sum(1 for f in section_fields if f["type"] and len(f["type"]) > 0)
        
        resource = {
            "section_title": title,
            "field_count": len(section_fields),
            "fields_with_descriptions": fields_with_desc,
            "fields_with_types": fields_with_type,
            "fields": section_fields
        }
        resources.append(resource)

# Print summary
print("=" * 80)
print("INPRACSYS FHIR API DOCUMENTATION - FIELD ANALYSIS")
print("=" * 80)

total_fields = 0
total_described = 0
total_typed = 0

for r in resources:
    total_fields += r["field_count"]
    total_described += r["fields_with_descriptions"]
    total_typed += r["fields_with_types"]
    desc_pct = (r["fields_with_descriptions"] / r["field_count"] * 100) if r["field_count"] > 0 else 0
    print(f"\n{r['section_title']}")
    print(f"  Fields: {r['field_count']}, Described: {r['fields_with_descriptions']} ({desc_pct:.0f}%), Typed: {r['fields_with_types']}")
    for f in r["fields"]:
        desc_preview = f["description"][:60] + "..." if len(f["description"]) > 60 else f["description"]
        print(f"    {f['name']:30s} {f['type']:20s} {f['cardinality']:10s} {desc_preview}")

print(f"\n{'=' * 80}")
print(f"TOTALS: {len(resources)} resources, {total_fields} fields, "
      f"{total_described} described ({total_described/total_fields*100:.0f}%), "
      f"{total_typed} typed ({total_typed/total_fields*100:.0f}%)")

# Map to standard FHIR resource types
print(f"\n{'=' * 80}")
print("MAPPING TO STANDARD FHIR RESOURCES")
print("=" * 80)
fhir_mapping = {
    "Patients": "Patient",
    "Smoking status": "Observation (smoking)",
    "Condition(Problem)": "Condition",
    "Medications": "MedicationStatement",
    "Allergy or Intolerance": "AllergyIntolerance",
    "Laboratory Result DiagnosticReport": "DiagnosticReport (labs)",
    "Laboratory Result Observations": "DiagnosticOrder",
    "VitalSign": "Observation (vitals)",
    "Procedure": "Procedure",
    "Care Team": "Practitioner/CareTeam",
    "Immunization": "Immunization",
    "Implantable Devices/UDI": "Device",
    "Assessment and Plan of Treatment": "CarePlan",
    "Goal": "Goal",
    "Health Concern": "HealthcareService/Condition"
}

for r in resources:
    mapped = fhir_mapping.get(r["section_title"], "UNKNOWN")
    print(f"  {r['section_title']:45s} -> {mapped}")

# Save detailed output
with open("field_inventory.json", "w") as f:
    json.dump(resources, f, indent=2)

# Summary stats for the analysis.md
summary = {
    "resource_count": len(resources),
    "total_fields": total_fields,
    "total_described": total_described,
    "total_typed": total_typed,
    "description_pct": round(total_described / total_fields * 100, 1) if total_fields else 0,
    "resources": [{
        "name": r["section_title"],
        "field_count": r["field_count"],
        "fields_with_descriptions": r["fields_with_descriptions"]
    } for r in resources]
}

with open("summary_stats.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\nDetailed field inventory saved to field_inventory.json")
print(f"Summary stats saved to summary_stats.json")
