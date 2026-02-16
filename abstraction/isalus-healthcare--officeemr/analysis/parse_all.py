"""
Parse all EHI export artifacts for OfficeEMR:
- JSON Schema files (80 files) -> entity/field inventory
- XLSX data dictionary -> field descriptions
- Sample export files (58 files) -> record counts and field coverage
Produces entity-inventory-full.json and entity-inventory-summary.json
"""
import json
import os
import glob as globmod
import codecs
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(BASE, "downloads/schema/OfficeEMR_B10_Schema_v1-OCT2023")
SAMPLE_DIR = os.path.join(BASE, "downloads/sample-export")
XLSX_PATH = os.path.join(BASE, "downloads/data-elements/iSalus_EHI_ExportDataElements_published_version1_Oct2023_pristine.xlsx")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ── 1. Parse XLSX data dictionary ──────────────────────────────────────────
import openpyxl

def parse_xlsx():
    """Parse XLSX data dictionary. Returns {entity_name: {field_name: description}}"""
    wb = openpyxl.load_workbook(XLSX_PATH, read_only=True)
    result = {}  # {entity: {field: {description, example, data_type}}}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        headers = [str(c).strip().lower() if c else "" for c in rows[0]]
        
        # Headers: Export Name, Field Items, FIELD Position, FIELD, Description, Example:, Data Type
        export_col = None
        field_col = None
        desc_col = None
        example_col = None
        dtype_col = None
        for i, h in enumerate(headers):
            if "export" in h and "name" in h:
                export_col = i
            elif h == "field":
                field_col = i
            elif "description" in h:
                desc_col = i
            elif "example" in h:
                example_col = i
            elif "data type" in h:
                dtype_col = i
        
        if field_col is None:
            for i, h in enumerate(headers):
                if "field" in h and "position" not in h and "items" not in h:
                    field_col = i
                    break
        
        if field_col is None:
            print(f"  Sheet '{ws.title}': no field column found, headers={headers}")
            continue
            
        print(f"  Sheet '{ws.title}': cols export={export_col} field={field_col} desc={desc_col} example={example_col} dtype={dtype_col}, rows={len(rows)-1}")
        
        current_entity = None
        for row in rows[1:]:
            vals = list(row)
            if export_col is not None and vals[export_col]:
                raw_name = str(vals[export_col]).strip().replace(".json", "")
                # Fix known vendor typo
                if raw_name == "responsiPMle_party":
                    raw_name = "responsible_party"
                # Fix systematic "PM" corruption in entity names  
                raw_name = raw_name.replace("PM", "b")
                current_entity = raw_name
            
            field_name = str(vals[field_col]).strip() if vals[field_col] else None
            if not field_name or field_name == "None":
                continue
            # Fix systematic "PM" corruption in field names
            field_name = field_name.replace("PM", "b")
                
            description = str(vals[desc_col]).strip() if desc_col is not None and vals[desc_col] else ""
            if description == "None":
                description = ""
            
            example = str(vals[example_col]).strip() if example_col is not None and vals[example_col] else ""
            if example == "None":
                example = ""
                
            data_type = str(vals[dtype_col]).strip() if dtype_col is not None and vals[dtype_col] else ""
            if data_type == "None":
                data_type = ""
            
            if current_entity:
                if current_entity not in result:
                    result[current_entity] = {}
                result[current_entity][field_name] = {
                    "description": description,
                    "example": example,
                    "vendor_category": data_type  # "Clinical" or "PM"
                }
    
    wb.close()
    return result

# ── 2. Parse JSON Schema files ─────────────────────────────────────────────
def parse_schemas():
    """Parse all JSON Schema files. Returns list of entity dicts."""
    entities = []
    schema_files = sorted(globmod.glob(os.path.join(SCHEMA_DIR, "*.json")) + 
                          globmod.glob(os.path.join(SCHEMA_DIR, "*.schema.json")))
    seen = set()
    
    for fpath in schema_files:
        fname = os.path.basename(fpath)
        if fname in seen:
            continue
        seen.add(fname)
        
        entity_name = fname.replace(".schema.json", "").replace(".json", "")
        
        try:
            with open(fpath, 'r', encoding='utf-8-sig') as f:
                schema = json.load(f)
        except Exception as e:
            entities.append({
                "entity": entity_name,
                "source_file": fname,
                "parse_error": True,
                "error": str(e),
                "fields": []
            })
            continue
        
        # Extract properties from items.properties (array of objects pattern)
        properties = {}
        if schema.get("type") == "array" and "items" in schema:
            properties = schema["items"].get("properties", {})
        elif schema.get("type") == "object":
            properties = schema.get("properties", {})
        elif "properties" in schema:
            properties = schema["properties"]
        
        fields = []
        for prop_name, prop_def in properties.items():
            field = {
                "name": prop_name,
                "type": prop_def.get("type", "unknown"),
                "schema_description": prop_def.get("description", ""),
            }
            fields.append(field)
        
        entities.append({
            "entity": entity_name,
            "source_file": fname,
            "field_count": len(fields),
            "fields": fields
        })
    
    return entities

# ── 3. Parse sample export files ───────────────────────────────────────────
def parse_sample_export():
    """Parse sample export files. Returns {entity_name: {record_count, fields_populated, sample_fields}}"""
    result = {}
    sample_files = sorted(globmod.glob(os.path.join(SAMPLE_DIR, "*.json")))
    
    for fpath in sample_files:
        fname = os.path.basename(fpath)
        entity_name = fname.replace(".json", "")
        
        try:
            with open(fpath, 'rb') as f:
                raw = f.read()
            text = raw.decode('utf-8-sig')
            data = json.loads(text)
        except Exception as e:
            result[entity_name] = {"parse_error": True, "error": str(e)}
            continue
        
        if isinstance(data, list):
            record_count = len(data)
            # Collect all field names across all records
            all_fields = set()
            populated_fields = set()
            for record in data:
                if isinstance(record, dict):
                    all_fields.update(record.keys())
                    for k, v in record.items():
                        if v is not None and v != "" and v != []:
                            populated_fields.add(k)
            
            result[entity_name] = {
                "record_count": record_count,
                "total_fields": len(all_fields),
                "populated_fields": len(populated_fields),
                "field_names": sorted(all_fields)
            }
        elif isinstance(data, dict):
            # readme.json or similar
            result[entity_name] = {
                "record_count": 1,
                "total_fields": len(data.keys()),
                "populated_fields": sum(1 for v in data.values() if v is not None and v != ""),
                "field_names": sorted(data.keys()),
                "is_object": True
            }
        else:
            result[entity_name] = {"record_count": 0, "type": str(type(data).__name__)}
    
    return result

# ── 4. Categorize entities ─────────────────────────────────────────────────
CLINICAL_ENTITIES = {
    "accident", "allergy", "allergy_symptom", "appointment", "care_plan_goal",
    "care_team", "case_management", "case_management_ckcc_note",
    "chart_share", "chart_share_detail_all", "chart_share_detail_individual",
    "chart_share_detail_individual_1", "chart_share_note",
    "chronic_care_management", "ckcc_status", "comment", "communication",
    "communication_recipient", "consent", "demographics", "dialysis_setup",
    "dialysis_visit", "education", "emergency_contact", "epa",
    "extension_encounter", "extension_results",
    "goal", "goal_barrier", "goal_intervention", "goal_target",
    "health_concern", "hie", "image_document", "image_xref",
    "immunization", "immunization_registry", "implantable_device",
    "insurance", "lab_result", "letter", "md_revolution_status",
    "medication", "optimize_rx", "order", "order_finding", "pharmacy",
    "phone_encounter", "portal_message", "pregnancy", "pregnancy_visit",
    "problem_list", "problem_list_note", "progress_note",
    "referral_tracking", "responsible_party",
    "template_encounter", "template_encounter_assessment",
    "template_encounter_exam", "template_encounter_history",
    "template_encounter_hpi", "template_encounter_order_fulfillment",
    "template_encounter_ros", "template_encounter_treatment_plan",
    "vital"
}

PM_ENTITIES = {
    "claim", "claim_procedure", "denial", "eligibility", "fee_schedule",
    "payment", "preschool_billing", "price_estimate", "price_estimate_line",
    "prior_authorization", "prior_authorization_code",
    "prior_authorization_rendering", "sliding_fee", "statement"
}

def categorize(entity_name):
    if entity_name in PM_ENTITIES:
        return "Practice Management"
    if entity_name in CLINICAL_ENTITIES:
        return "Clinical Data"
    if entity_name == "readme":
        return "Metadata"
    return "Clinical Data"  # default

# ── 5. Merge and produce output ───────────────────────────────────────────
def main():
    print("Parsing XLSX data dictionary...")
    xlsx_data = parse_xlsx()
    print(f"  Found {len(xlsx_data)} entities in XLSX")
    
    # Also parse PDF for supplemental descriptions
    print("\nParsing PDF data dictionary for supplemental descriptions...")
    import subprocess
    pdf_path = os.path.join(BASE, "downloads/ehi-export-page.pdf")
    pdf_text_path = os.path.join(OUT_DIR, "pdf-text.txt")
    subprocess.run(["pdftotext", "-layout", pdf_path, pdf_text_path], check=True)
    from parse_pdf import parse_pdf_dictionary
    pdf_data = parse_pdf_dictionary(pdf_text_path)
    print(f"  Found {len(pdf_data)} entities in PDF, {sum(len(v) for v in pdf_data.values())} fields")

    print("\nParsing JSON Schema files...")
    schema_entities = parse_schemas()
    print(f"  Found {len(schema_entities)} schema files")
    
    print("\nParsing sample export...")
    sample_data = parse_sample_export()
    print(f"  Found {len(sample_data)} sample files")
    
    # Merge everything
    full_inventory = []
    all_entity_names = set()
    
    for se in schema_entities:
        all_entity_names.add(se["entity"])
    for en in xlsx_data:
        all_entity_names.add(en)
    for en in sample_data:
        all_entity_names.add(en)
    
    for entity_name in sorted(all_entity_names):
        if entity_name == "readme":
            continue
            
        # Find schema entry
        schema_entry = None
        for se in schema_entities:
            if se["entity"] == entity_name:
                schema_entry = se
                break
        
        xlsx_fields = xlsx_data.get(entity_name, {})
        pdf_fields = pdf_data.get(entity_name, {})
        sample_info = sample_data.get(entity_name, None)
        
        # Use vendor's category from XLSX if available, else our heuristic
        vendor_cat = None
        for fn, info in xlsx_fields.items():
            if info.get("vendor_category"):
                vendor_cat = info["vendor_category"]
                break
        category = "Practice Management" if vendor_cat == "PM" else "Clinical Data"
        if entity_name == "readme":
            category = "Metadata"
        
        # Build field list
        fields = []
        if schema_entry and not schema_entry.get("parse_error"):
            for sf in schema_entry["fields"]:
                xlsx_info = xlsx_fields.get(sf["name"], {})
                desc = xlsx_info.get("description", "") if isinstance(xlsx_info, dict) else ""
                example = xlsx_info.get("example", "") if isinstance(xlsx_info, dict) else ""
                # Fallback to PDF description if XLSX is empty
                if not desc:
                    desc = pdf_fields.get(sf["name"], "")
                field = {
                    "name": sf["name"],
                    "type": sf["type"],
                    "description": desc,
                    "example": example,
                    "has_description": bool(desc and desc.strip()),
                    "in_schema": True,
                    "in_xlsx": sf["name"] in xlsx_fields,
                    "in_sample": sample_info is not None and sf["name"] in sample_info.get("field_names", [])
                }
                fields.append(field)
            
            # Add fields in XLSX but not in schema
            schema_field_names = {sf["name"] for sf in schema_entry["fields"]}
            for fn, info in xlsx_fields.items():
                if fn not in schema_field_names:
                    desc = info.get("description", "") if isinstance(info, dict) else ""
                    example = info.get("example", "") if isinstance(info, dict) else ""
                    fields.append({
                        "name": fn,
                        "type": "unknown",
                        "description": desc,
                        "example": example,
                        "has_description": bool(desc and desc.strip()),
                        "in_schema": False,
                        "in_xlsx": True,
                        "in_sample": sample_info is not None and fn in sample_info.get("field_names", [])
                    })
        elif xlsx_fields:
            for fn, info in xlsx_fields.items():
                desc = info.get("description", "") if isinstance(info, dict) else ""
                example = info.get("example", "") if isinstance(info, dict) else ""
                fields.append({
                    "name": fn,
                    "type": "unknown",
                    "description": desc,
                    "example": example,
                    "has_description": bool(desc and desc.strip()),
                    "in_schema": False,
                    "in_xlsx": True,
                    "in_sample": sample_info is not None and fn in sample_info.get("field_names", [])
                })
        
        entity_record = {
            "entity": entity_name,
            "category": category,
            "field_count": len(fields),
            "fields_with_description": sum(1 for f in fields if f["has_description"]),
            "in_schema": schema_entry is not None,
            "in_xlsx": entity_name in xlsx_data,
            "in_sample": entity_name in sample_data,
            "sample_record_count": sample_info.get("record_count") if sample_info else None,
            "fields": fields
        }
        
        if schema_entry and schema_entry.get("parse_error"):
            entity_record["schema_parse_error"] = True
        
        full_inventory.append(entity_record)
    
    # Write full inventory
    with open(os.path.join(OUT_DIR, "entity-inventory-full.json"), "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"\nWrote entity-inventory-full.json ({len(full_inventory)} entities)")
    
    # ── Summary stats ──
    total_entities = len(full_inventory)
    total_fields = sum(e["field_count"] for e in full_inventory)
    total_described = sum(e["fields_with_description"] for e in full_inventory)
    entities_in_schema = sum(1 for e in full_inventory if e["in_schema"])
    entities_in_xlsx = sum(1 for e in full_inventory if e["in_xlsx"])
    entities_in_sample = sum(1 for e in full_inventory if e["in_sample"])
    
    # Category breakdown
    by_category = defaultdict(lambda: {"entities": 0, "fields": 0, "described": 0})
    for e in full_inventory:
        cat = e["category"]
        by_category[cat]["entities"] += 1
        by_category[cat]["fields"] += e["field_count"]
        by_category[cat]["described"] += e["fields_with_description"]
    
    # Top entities by field count
    top_entities = sorted(full_inventory, key=lambda e: e["field_count"], reverse=True)[:20]
    
    summary = {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "total_fields_with_description": total_described,
        "description_pct": round(total_described / total_fields * 100, 1) if total_fields else 0,
        "entities_in_schema": entities_in_schema,
        "entities_in_xlsx": entities_in_xlsx,
        "entities_in_sample": entities_in_sample,
        "by_category": dict(by_category),
        "top_entities_by_field_count": [
            {"entity": e["entity"], "category": e["category"], 
             "fields": e["field_count"], "described": e["fields_with_description"],
             "sample_records": e["sample_record_count"]}
            for e in top_entities
        ],
        "entities_without_descriptions": [
            {"entity": e["entity"], "fields": e["field_count"]}
            for e in full_inventory if e["fields_with_description"] == 0 and e["field_count"] > 0
        ],
        "sample_export_coverage": {
            "entities_with_data": sum(1 for e in full_inventory if e["in_sample"] and e.get("sample_record_count", 0) and e["sample_record_count"] > 0),
            "entities_empty_in_sample": [
                e["entity"] for e in full_inventory 
                if e["in_sample"] and (e.get("sample_record_count") == 0 or e.get("sample_record_count") is None)
            ],
            "entities_not_in_sample": [
                e["entity"] for e in full_inventory if not e["in_sample"]
            ]
        }
    }
    
    with open(os.path.join(OUT_DIR, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")
    
    # Print summary to console
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total entities: {total_entities}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({summary['description_pct']}%)")
    print(f"Entities in schema: {entities_in_schema}")
    print(f"Entities in XLSX: {entities_in_xlsx}")
    print(f"Entities in sample: {entities_in_sample}")
    print(f"\nBy category:")
    for cat, stats in sorted(by_category.items()):
        print(f"  {cat}: {stats['entities']} entities, {stats['fields']} fields, {stats['described']} described")
    print(f"\nTop 10 entities by field count:")
    for e in top_entities[:10]:
        print(f"  {e['entity']}: {e['field_count']} fields ({e['fields_with_description']} described), sample={e['sample_record_count']}")
    if summary["entities_without_descriptions"]:
        print(f"\nEntities with 0 descriptions:")
        for e in summary["entities_without_descriptions"]:
            print(f"  {e['entity']}: {e['fields']} fields")

if __name__ == "__main__":
    main()
