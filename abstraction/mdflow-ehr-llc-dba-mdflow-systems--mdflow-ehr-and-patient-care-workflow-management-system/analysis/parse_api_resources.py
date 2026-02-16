"""Parse FHIR resource types from the API Documentation PDF."""
import subprocess, re, json

text = subprocess.check_output(
    ["pdftotext", "-layout", "../downloads/API-Documentation-g7910.pdf", "-"],
    text=True
)

# Find all "Request : ResourceType" or "Request: ResourceType" lines
resources = []
for m in re.finditer(r'Request\s*:\s*(.+?)(?:\s*\.{3,}|\s*$)', text, re.MULTILINE):
    name = m.group(1).strip().rstrip('.')
    if name and name not in resources and len(name) < 80:
        resources.append(name)

# Also find Search lines
for m in re.finditer(r'Search\s+(\w+)', text):
    name = f"Search: {m.group(1)}"
    if name not in resources:
        resources.append(name)

print("FHIR Resource Endpoints in (g)(10) API Documentation:")
for r in resources:
    print(f"  - {r}")
print(f"\nTotal: {len(resources)} endpoints")

with open("api_resources.json", "w") as f:
    json.dump(resources, f, indent=2)
