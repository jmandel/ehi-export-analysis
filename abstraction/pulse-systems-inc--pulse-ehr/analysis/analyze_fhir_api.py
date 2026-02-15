"""Parse the FHIR API documentation PDF to enumerate supported resources."""
import subprocess, json, re

pdf_path = "/home/jmandel/hobby/ehi-export-analysis/results/pulse-systems-inc--pulse-ehr/downloads/Pulse-8.0-API-FHIR-Documentation.pdf"
text = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True).stdout

# Extract FHIR resource types from headings
resources = []
for line in text.split("\n"):
    line = line.strip()
    # Match headings like "ALLERGIES AND INTOLERANCES US CORE ALLERGYINTOLERANCE PROFILE"
    if "US CORE" in line.upper() or "FHIR CORE" in line.upper():
        resources.append(line.strip())

# Also extract resource names from GET examples
fhir_resources = set()
for match in re.finditer(r'GET\s+https?://[^/]+/(\w+)', text):
    resource = match.group(1)
    if resource not in ("FHIR_URL", "EHR_FHIR", "base"):
        fhir_resources.add(resource)

result = {
    "source_file": "Pulse-8.0-API-FHIR-Documentation.pdf",
    "pages": 41,
    "purpose": "§170.315(g)(10) FHIR API — NOT (b)(10) EHI export",
    "fhir_version": "R4",
    "heading_sections": resources,
    "fhir_resources_from_examples": sorted(fhir_resources),
    "resource_count": len(fhir_resources),
}

with open("fhir_api_analysis.json", "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))
