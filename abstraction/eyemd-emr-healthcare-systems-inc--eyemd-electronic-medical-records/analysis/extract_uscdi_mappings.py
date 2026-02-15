"""Extract complete USCDI mapping table and FHIR resource inventory from the Postman collection."""
import json
import re

COLLECTION_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/eyemd-emr-healthcare-systems-inc--eyemd-electronic-medical-records/downloads/eyemd-fhir-api-postman-collection.json"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/eyemd-emr-healthcare-systems-inc--eyemd-electronic-medical-records/analysis"

with open(COLLECTION_PATH) as f:
    data = json.load(f)

collection = data.get("collection", data)
desc = collection["info"]["description"]

# Extract USCDI section
uscdi_start = desc.lower().find('<h1 id="uscdi-mappings">')
uscdi_section = desc[uscdi_start:]

# Parse each category with its data elements
categories = re.split(r'<h2[^>]*>(.*?)</h2>', uscdi_section)
# categories[0] is the h1, then alternating: header, content, header, content...

uscdi_mappings = []
current_category = None

for i in range(1, len(categories), 2):
    category_name = re.sub(r'<[^>]+>', '', categories[i]).strip()
    content = categories[i+1] if i+1 < len(categories) else ""
    
    # Parse table rows
    rows = re.findall(r'<tr>(.*?)</tr>', content, re.DOTALL)
    for row in rows[1:]:  # Skip header
        cells = re.findall(r'<td>(.*?)</td>', row, re.DOTALL)
        if len(cells) >= 3:
            element = re.sub(r'<[^>]+>', '', cells[0]).strip()
            profile = re.sub(r'<[^>]+>', '', cells[1]).strip()
            resource = re.sub(r'<[^>]+>', '', cells[2]).strip()
            if element:
                uscdi_mappings.append({
                    "category": category_name,
                    "element": element,
                    "us_core_profile": profile,
                    "fhir_resource": resource
                })

# Extract folder-level search parameter documentation
items = collection.get("item", [])

def extract_resource_info(item, path=""):
    """Extract detailed info about each FHIR resource folder."""
    results = []
    name = item.get("name", "")
    current_path = f"{path}/{name}" if path else name
    folder_desc = item.get("description", "") or ""
    
    info = {
        "name": name,
        "path": current_path,
        "description_length": len(folder_desc),
        "has_description": bool(folder_desc.strip()),
        "search_params": [],
        "endpoints": [],
        "children_count": 0
    }
    
    # Extract search parameters from description tables
    if folder_desc:
        param_rows = re.findall(
            r'<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>',
            folder_desc, re.DOTALL
        )
        for row in param_rows:
            p_name = re.sub(r'<[^>]+>', '', row[0]).strip()
            p_type = re.sub(r'<[^>]+>', '', row[1]).strip()
            p_desc = re.sub(r'<[^>]+>', '', row[2]).strip()
            if p_name and p_name not in ("Parameter", "**Parameter**"):
                info["search_params"].append({
                    "name": p_name,
                    "type": p_type,
                    "description": p_desc
                })
    
    if "item" in item:
        info["children_count"] = len(item["item"])
        for child in item["item"]:
            if "request" in child:
                req = child["request"]
                endpoint = {
                    "name": child.get("name", ""),
                    "method": req.get("method", ""),
                    "has_description": bool(req.get("description", "").strip()),
                    "description_preview": re.sub(r'<[^>]+>', '', req.get("description", ""))[:200].strip()
                }
                url = req.get("url", {})
                if isinstance(url, dict):
                    endpoint["url"] = url.get("raw", "")
                else:
                    endpoint["url"] = url
                info["endpoints"].append(endpoint)
            child_results = extract_resource_info(child, current_path)
            results.extend(child_results)
    
    results.insert(0, info)
    return results

all_resources = []
for item in items:
    all_resources.extend(extract_resource_info(item))

# Filter to top-level resource folders (skip nested)
top_level = [r for r in all_resources if "/" not in r["path"]]

# Build summary
fhir_resource_folders = [r for r in top_level 
                          if r["name"] not in ("System Level Operations", "Export", "App Registration")]

summary = {
    "total_uscdi_categories": len(set(m["category"] for m in uscdi_mappings)),
    "total_uscdi_elements": len(uscdi_mappings),
    "uscdi_categories": list(set(m["category"] for m in uscdi_mappings)),
    "total_fhir_resource_folders": len(fhir_resource_folders),
    "total_search_params": sum(len(r["search_params"]) for r in fhir_resource_folders),
    "fhir_resources": [],
    "uscdi_mappings": uscdi_mappings,
    "export_folder": next((r for r in top_level if r["name"] == "Export"), None),
    "all_folders": top_level
}

for r in fhir_resource_folders:
    summary["fhir_resources"].append({
        "name": r["name"],
        "search_params": len(r["search_params"]),
        "endpoints": len(r["endpoints"]),
        "has_description": r["has_description"],
        "param_details": r["search_params"]
    })

# Print summary
print("=" * 70)
print("EYEMD EMR FHIR API - COMPLETE INVENTORY")
print("=" * 70)

print(f"\nUSCDI v3 Mapping Categories: {summary['total_uscdi_categories']}")
print(f"USCDI v3 Data Elements Mapped: {summary['total_uscdi_elements']}")
print(f"FHIR Resource Folders: {summary['total_fhir_resource_folders']}")
print(f"Total Search Parameters Documented: {summary['total_search_params']}")

print("\n--- USCDI v3 MAPPING TABLE ---")
for cat in sorted(set(m["category"] for m in uscdi_mappings)):
    elements = [m for m in uscdi_mappings if m["category"] == cat]
    print(f"\n{cat} ({len(elements)} elements):")
    for e in elements:
        print(f"  {e['element']} → {e['fhir_resource']}")

print("\n--- FHIR RESOURCE FOLDERS ---")
for r in sorted(summary["fhir_resources"], key=lambda x: x["name"]):
    print(f"  {r['name']}: {r['search_params']} search params, {r['endpoints']} endpoints, desc={r['has_description']}")

print("\n--- EXPORT SECTION ---")
export = summary["export_folder"]
if export:
    print(f"  Name: {export['name']}")
    print(f"  Has description: {export['has_description']}")
    print(f"  Endpoints: {len(export['endpoints'])}")
    for ep in export["endpoints"]:
        print(f"    {ep['method']} {ep['url']}")
        print(f"    Has description: {ep['has_description']}")
        print(f"    Preview: {ep['description_preview'][:200]}")

# Unique FHIR resources actually used
actual_resources = set()
for m in uscdi_mappings:
    for r in re.split(r'\s+', m["fhir_resource"]):
        r = r.strip()
        if r and r[0].isupper() and len(r) > 3:
            actual_resources.add(r)
print(f"\nUnique FHIR Resources in USCDI mappings: {len(actual_resources)}")
for r in sorted(actual_resources):
    print(f"  {r}")

# Save full inventory
with open(f"{OUTPUT_DIR}/full-entity-inventory.json", "w") as f:
    json.dump(summary, f, indent=2)
print(f"\nSaved full inventory to {OUTPUT_DIR}/full-entity-inventory.json")
