"""Extract FHIR resource types from the Postman collection JSON for AWARDS FHIR API."""
import json
import urllib.request
import sys

url = "https://fhir-docs.footholdtechnology.com/api/collections/44925376/2sB34ZrQJU?segregateAuth=true&versionTag=latest"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())

# Save full collection for reference
with open("fhir-postman-collection.json", "w") as f:
    json.dump(data, f, indent=2)

# Extract resource folder names (top-level items under "FHIR Resources")
resources = []
for top_item in data.get("item", []):
    if top_item.get("name") == "FHIR Resources":
        for resource_folder in top_item.get("item", []):
            name = resource_folder.get("name", "")
            # Count endpoints in each folder
            endpoints = []
            for ep in resource_folder.get("item", []):
                ep_name = ep.get("name", "")
                method = ep.get("request", {}).get("method", "")
                url_path = ep.get("request", {}).get("url", "")
                if isinstance(url_path, dict):
                    url_path = url_path.get("raw", "")
                endpoints.append({"name": ep_name, "method": method, "url": url_path})
            
            # Extract description
            desc = resource_folder.get("description", "")
            
            resources.append({
                "name": name,
                "endpoint_count": len(endpoints),
                "endpoints": endpoints,
                "description_length": len(desc)
            })

print(f"Total FHIR resource folders: {len(resources)}")
print()
for r in resources:
    print(f"  {r['name']}: {r['endpoint_count']} endpoints")

# Save extracted resources
with open("fhir-resources-summary.json", "w") as f:
    json.dump(resources, f, indent=2)

# Also extract from Bulk Data section
for top_item in data.get("item", []):
    if "bulk" in top_item.get("name", "").lower():
        print(f"\nBulk Data section: {top_item.get('name')}")
        for sub in top_item.get("item", []):
            print(f"  {sub.get('name')}")
