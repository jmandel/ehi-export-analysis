"""Parse the EyeMD EMR Postman collection to extract:
- All FHIR resource types / folders
- All endpoints with their methods and descriptions
- USCDI mappings
- Export-related documentation
- Search parameters and their documentation quality
"""
import json
import sys
import os

COLLECTION_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/eyemd-emr-healthcare-systems-inc--eyemd-electronic-medical-records/downloads/eyemd-fhir-api-postman-collection.json"

def extract_items(item, path=""):
    """Recursively extract all items from the Postman collection."""
    results = []
    name = item.get("name", "")
    current_path = f"{path}/{name}" if path else name
    
    if "item" in item:
        # It's a folder
        folder_info = {
            "type": "folder",
            "name": name,
            "path": current_path,
            "description": "",
            "children_count": len(item["item"])
        }
        # Check for description
        if "description" in item:
            folder_info["description"] = item["description"][:500] if item["description"] else ""
        results.append(folder_info)
        for child in item["item"]:
            results.extend(extract_items(child, current_path))
    else:
        # It's a request
        request = item.get("request", {})
        req_info = {
            "type": "request",
            "name": name,
            "path": current_path,
            "method": request.get("method", ""),
            "url": "",
            "description": "",
            "has_description": False,
            "query_params": [],
        }
        
        # Extract URL
        url = request.get("url", {})
        if isinstance(url, dict):
            raw = url.get("raw", "")
            req_info["url"] = raw
            # Extract query parameters
            for param in url.get("query", []):
                req_info["query_params"].append({
                    "key": param.get("key", ""),
                    "description": param.get("description", ""),
                    "disabled": param.get("disabled", False)
                })
        elif isinstance(url, str):
            req_info["url"] = url
        
        # Extract description
        desc = request.get("description", "")
        if desc:
            req_info["description"] = desc[:1000]
            req_info["has_description"] = True
        
        results.append(req_info)
    
    return results

def main():
    with open(COLLECTION_PATH, "r") as f:
        data = json.load(f)
    
    collection = data.get("collection", data)
    info = collection.get("info", {})
    
    print("=" * 80)
    print(f"Collection: {info.get('name', 'Unknown')}")
    print(f"Description length: {len(info.get('description', ''))} chars")
    print("=" * 80)
    
    # Extract all items
    all_items = []
    for item in collection.get("item", []):
        all_items.extend(extract_items(item))
    
    # Separate folders and requests
    folders = [i for i in all_items if i["type"] == "folder"]
    requests = [i for i in all_items if i["type"] == "request"]
    
    print(f"\nTotal folders: {len(folders)}")
    print(f"Total requests/endpoints: {len(requests)}")
    
    # Top-level folders
    print("\n--- TOP-LEVEL FOLDERS ---")
    top_folders = [f for f in folders if f["path"].count("/") == 0]
    for f in top_folders:
        print(f"  {f['name']} ({f['children_count']} children)")
        if f["description"]:
            print(f"    Desc: {f['description'][:200]}...")
    
    # All folders
    print("\n--- ALL FOLDERS ---")
    for f in folders:
        desc_indicator = "✓" if f["description"] else "✗"
        print(f"  [{desc_indicator}] {f['path']} ({f['children_count']} items)")
    
    # All requests
    print("\n--- ALL REQUESTS ---")
    for r in requests:
        desc_indicator = "✓" if r["has_description"] else "✗"
        params_count = len(r["query_params"])
        params_with_desc = len([p for p in r["query_params"] if p.get("description")])
        print(f"  [{desc_indicator}] {r['method']} {r['path']}")
        if params_count > 0:
            print(f"       Params: {params_count} total, {params_with_desc} with descriptions")
    
    # Export-related items
    print("\n--- EXPORT-RELATED ITEMS ---")
    for item in all_items:
        name_lower = item.get("name", "").lower()
        desc_lower = item.get("description", "").lower()
        if any(kw in name_lower or kw in desc_lower for kw in ["export", "bulk", "b(10)", "b10", "ehi"]):
            print(f"  {item['type']}: {item.get('path', item.get('name'))}")
            if item.get("description"):
                print(f"    Description: {item['description'][:300]}")
            if item.get("url"):
                print(f"    URL: {item['url']}")
    
    # USCDI-related content
    print("\n--- USCDI/MAPPING CONTENT ---")
    for item in all_items:
        name_lower = item.get("name", "").lower()
        desc_lower = item.get("description", "").lower()
        if any(kw in name_lower or kw in desc_lower for kw in ["uscdi", "mapping", "us core"]):
            print(f"  {item['type']}: {item.get('path', item.get('name'))}")
            if item.get("description"):
                print(f"    Description: {item['description'][:500]}")
    
    # CCD/CCDA-related content
    print("\n--- CCD/CCDA CONTENT ---")
    for item in all_items:
        name_lower = item.get("name", "").lower()
        desc_lower = item.get("description", "").lower()
        url_lower = item.get("url", "").lower()
        if any(kw in name_lower or kw in desc_lower or kw in url_lower for kw in ["ccd", "ccda", "c-cda", "alldata"]):
            print(f"  {item['type']}: {item.get('path', item.get('name'))}")
            if item.get("description"):
                print(f"    Description: {item['description'][:500]}")
            if item.get("url"):
                print(f"    URL: {item['url']}")
    
    # Summary of FHIR resource types
    print("\n--- FHIR RESOURCE TYPES (from folder names) ---")
    fhir_resources = set()
    for f in folders:
        # Top-level folders that look like FHIR resources
        name = f["name"]
        if name[0].isupper() and not name.startswith("USCDI") and "Introduction" not in name:
            fhir_resources.add(name)
    for r in sorted(fhir_resources):
        # Count endpoints under this resource
        endpoints = [req for req in requests if req["path"].startswith(r + "/") or req["path"].startswith(f"FHIR Resources/{r}")]
        print(f"  {r}: {len(endpoints)} endpoints")
    
    # Count search parameters across all resources
    total_params = 0
    params_with_desc = 0
    for r in requests:
        for p in r["query_params"]:
            total_params += 1
            if p.get("description"):
                params_with_desc += 1
    
    print(f"\n--- SEARCH PARAMETER SUMMARY ---")
    print(f"Total search parameters: {total_params}")
    print(f"Parameters with descriptions: {params_with_desc}")
    print(f"Parameters without descriptions: {total_params - params_with_desc}")
    
    # Save full inventory as JSON
    output = {
        "collection_name": info.get("name", "Unknown"),
        "total_folders": len(folders),
        "total_requests": len(requests),
        "folders": folders,
        "requests": [{
            "name": r["name"],
            "path": r["path"],
            "method": r["method"],
            "url": r["url"],
            "has_description": r["has_description"],
            "param_count": len(r["query_params"]),
            "params_with_desc": len([p for p in r["query_params"] if p.get("description")])
        } for r in requests],
        "fhir_resources": sorted(fhir_resources),
        "total_search_params": total_params,
        "search_params_with_desc": params_with_desc
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "postman_inventory.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nFull inventory saved to {output_path}")

if __name__ == "__main__":
    main()
