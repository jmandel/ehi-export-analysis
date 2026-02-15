"""
Analyze EHI export artifacts for CHN Tech Solutions / Integrated Care EHR.
Extracts scope listings, CCD sections, and produces structured inventory.
"""
import json
import os
from html.parser import HTMLParser

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/chn-tech-solutions-llc--integrated-care-ehr/downloads"
OUTPUT = "/home/jmandel/hobby/ehi-export-analysis/abstraction/chn-tech-solutions-llc--integrated-care-ehr/analysis"


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'head'):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'head'):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.text.append(t)


def extract_text(filepath):
    with open(filepath) as f:
        p = TextExtractor()
        p.feed(f.read())
        return "\n".join(p.text)


def extract_scopes(text):
    """Extract API scopes from REST API page text."""
    fhir_scopes = []
    oemr_scopes = []
    portal_scopes = []
    
    lines = text.split("\n")
    current_section = None
    for line in lines:
        line = line.strip()
        if "api:fhir" in line and "endpoints" in line:
            current_section = "fhir"
            continue
        if "api:oemr" in line and "endpoints" in line:
            current_section = "oemr"
            continue
        if "api:port" in line and "endpoints" in line:
            current_section = "portal"
            continue
        if line.startswith("Registration"):
            current_section = None
            continue
        
        if current_section == "fhir" and "/" in line and "." in line and not line.startswith("http"):
            fhir_scopes.append(line)
        elif current_section == "oemr" and "/" in line and "." in line and not line.startswith("http"):
            oemr_scopes.append(line)
        elif current_section == "portal" and "/" in line and "." in line and not line.startswith("http"):
            portal_scopes.append(line)
    
    return {
        "fhir_scopes": fhir_scopes,
        "oemr_scopes": oemr_scopes,
        "portal_scopes": portal_scopes
    }


def extract_oemr_resources(scopes):
    """Extract unique resource types from OpenEMR native API scopes."""
    resources = set()
    for scope in scopes:
        # Format: user/resource.read or user/resource.write
        parts = scope.split("/")
        if len(parts) == 2:
            resource = parts[1].split(".")[0]
            resources.add(resource)
    return sorted(resources)


def extract_fhir_resources(scopes):
    """Extract unique FHIR resource types from FHIR scopes."""
    resources = set()
    for scope in scopes:
        parts = scope.split("/")
        if len(parts) == 2:
            resource = parts[1].split(".")[0]
            if resource != "*":
                resources.add(resource)
    return sorted(resources)


def extract_ccd_sections(text):
    """Extract CCD sections from FHIR API page."""
    date_filtered = []
    full_record = []
    
    lines = text.split("\n")
    in_date_filtered = False
    in_full_record = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        if "Start and end date filter encounter related events" in line:
            in_date_filtered = True
            in_full_record = False
            continue
        if "entire medical record sent" in line:
            in_date_filtered = False
            in_full_record = True
            continue
        if "CCD is generated on demand" in line:
            in_full_record = False
            continue
        
        if in_date_filtered and line and not line.startswith("The following"):
            date_filtered.append(line)
        elif in_full_record and line and not line.startswith("The following"):
            full_record.append(line)
    
    return {
        "date_filtered_sections": date_filtered,
        "full_record_sections": full_record
    }


# --- Main analysis ---

results = {}

# 1. Analyze artifact inventory
artifacts = []
for fname in sorted(os.listdir(DOWNLOADS)):
    fpath = os.path.join(DOWNLOADS, fname)
    size = os.path.getsize(fpath)
    artifacts.append({"filename": fname, "size_bytes": size, "size_human": f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"})
results["artifacts"] = artifacts

# 2. Extract scopes from REST API page
rest_text = extract_text(os.path.join(DOWNLOADS, "rest-api-page.html"))
scopes = extract_scopes(rest_text)
results["scopes"] = scopes

# 3. Extract unique resource types
oemr_resources = extract_oemr_resources(scopes["oemr_scopes"])
fhir_resources = extract_fhir_resources(scopes["fhir_scopes"])
results["oemr_api_resources"] = oemr_resources
results["fhir_api_resources"] = fhir_resources

# 4. Extract CCD sections from FHIR API page
fhir_text = extract_text(os.path.join(DOWNLOADS, "fhir-api-page.html"))
ccd_sections = extract_ccd_sections(fhir_text)
results["ccd_sections"] = ccd_sections

# 5. Summary statistics
results["summary"] = {
    "total_artifacts": len(artifacts),
    "total_fhir_scopes": len(scopes["fhir_scopes"]),
    "total_oemr_scopes": len(scopes["oemr_scopes"]),
    "total_portal_scopes": len(scopes["portal_scopes"]),
    "unique_fhir_resources": len(fhir_resources),
    "unique_oemr_resources": len(oemr_resources),
    "ccd_date_filtered_sections": len(ccd_sections["date_filtered_sections"]),
    "ccd_full_record_sections": len(ccd_sections["full_record_sections"]),
    "total_ccd_sections": len(ccd_sections["date_filtered_sections"]) + len(ccd_sections["full_record_sections"])
}

# Save results
with open(os.path.join(OUTPUT, "artifact_analysis.json"), "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print("=" * 60)
print("CHN Tech Solutions - Integrated Care EHR")
print("EHI Export Artifact Analysis")
print("=" * 60)

print(f"\n--- Artifacts ({len(artifacts)} files) ---")
for a in artifacts:
    print(f"  {a['filename']:50s} {a['size_human']:>10s}")

print(f"\n--- CCD Sections ({results['summary']['total_ccd_sections']} total) ---")
print(f"  Date-filtered ({len(ccd_sections['date_filtered_sections'])}):")
for s in ccd_sections['date_filtered_sections']:
    print(f"    - {s}")
print(f"  Full record ({len(ccd_sections['full_record_sections'])}):")
for s in ccd_sections['full_record_sections']:
    print(f"    - {s}")

print(f"\n--- FHIR API Resources ({len(fhir_resources)}) ---")
for r in fhir_resources:
    print(f"  - {r}")

print(f"\n--- OpenEMR Native API Resources ({len(oemr_resources)}) ---")
for r in oemr_resources:
    print(f"  - {r}")

print(f"\n--- Portal API Scopes ({len(scopes['portal_scopes'])}) ---")
for s in scopes['portal_scopes']:
    print(f"  - {s}")

print(f"\n--- Scope Counts ---")
print(f"  FHIR scopes:   {results['summary']['total_fhir_scopes']}")
print(f"  OEMR scopes:   {results['summary']['total_oemr_scopes']}")
print(f"  Portal scopes: {results['summary']['total_portal_scopes']}")
