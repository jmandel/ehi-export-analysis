"""
Extract all example responses from the Swagger spec to understand
what fields are actually present in each FHIR resource type.
"""
import json
from collections import defaultdict

DOWNLOADS = "/home/jmandel/hobby/ehi-export-analysis/results/first-insight-corporation--maximeyes-com/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/first-insight-corporation--maximeyes-com/analysis"

with open(f"{DOWNLOADS}/swagger-v1.json") as f:
    spec = json.load(f)

examples = {}
field_counts = {}

for path, methods in spec.get("paths", {}).items():
    for method, detail in methods.items():
        if method not in ("get", "post"):
            continue
        responses = detail.get("responses", {})
        for code, resp in responses.items():
            if code != "200":
                continue
            content = resp.get("content", {})
            for ct, ct_detail in content.items():
                example_str = ct_detail.get("example", "")
                if not example_str:
                    continue
                try:
                    ex_data = json.loads(example_str)
                except:
                    continue

                # Extract resource type
                if "resourceType" in ex_data:
                    rt = ex_data["resourceType"]
                elif ex_data.get("type") == "searchset" and "entry" in ex_data:
                    entries = ex_data.get("entry", [])
                    if entries:
                        resource = entries[0].get("resource", {})
                        rt = resource.get("resourceType", "Unknown")
                    else:
                        continue
                else:
                    continue

                # Extract actual resource from bundle
                if ex_data.get("resourceType") == "Bundle":
                    entries = ex_data.get("entry", [])
                    if entries:
                        resource = entries[0].get("resource", {})
                        if rt not in examples or len(json.dumps(resource)) > len(json.dumps(examples.get(rt, {}))):
                            examples[rt] = resource
                else:
                    if rt not in examples or len(json.dumps(ex_data)) > len(json.dumps(examples.get(rt, {}))):
                        examples[rt] = ex_data

def count_fields(obj, prefix=""):
    """Count leaf fields in a FHIR resource"""
    fields = set()
    if isinstance(obj, dict):
        for key, val in obj.items():
            if key in ("resourceType", "meta", "text"):
                continue
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(val, dict):
                fields.update(count_fields(val, full_key))
            elif isinstance(val, list):
                if val:
                    if isinstance(val[0], dict):
                        for item in val:
                            fields.update(count_fields(item, full_key))
                    else:
                        fields.add(full_key)
                else:
                    fields.add(full_key)
            else:
                fields.add(full_key)
    return fields

# Analyze each resource
results = {}
for rt, resource in sorted(examples.items()):
    fields = count_fields(resource)
    results[rt] = {
        "field_count": len(fields),
        "fields": sorted(fields),
        "top_level_keys": sorted([k for k in resource.keys() if k not in ("resourceType", "meta", "text")])
    }

# Save examples and field analysis
with open(f"{OUTPUT_DIR}/swagger-examples.json", "w") as f:
    json.dump(examples, f, indent=2)

with open(f"{OUTPUT_DIR}/swagger-field-analysis.json", "w") as f:
    json.dump(results, f, indent=2)

# Print summary
print(f"Resources with examples: {len(examples)}")
for rt, info in sorted(results.items()):
    print(f"  {rt}: {info['field_count']} fields, top-level keys: {info['top_level_keys']}")
