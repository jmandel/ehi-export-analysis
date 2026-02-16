"""
Parse all three Nextech EHI data dictionary XLSX files into a unified JSON inventory.
Produces entity-inventory-full.json and entity-inventory-summary.json.
"""
import json
import os
import openpyxl

DOWNLOADS = os.path.join(os.path.dirname(__file__), '..', 'downloads')

FILES = {
    "SRSPro": os.path.join(DOWNLOADS, "srspro-ehi-data-dictionary.xlsx"),
    "Nextech EHR (ICP)": os.path.join(DOWNLOADS, "nextech-ehr-icp-ehi-data-dictionary.xlsx"),
    "Nextech Select/NexCloud": os.path.join(DOWNLOADS, "nextech-select-nexcloud-ehi-data-dictionary.xlsx"),
}

def parse_workbook(path, platform):
    """Parse an XLSX data dictionary into a list of entity dicts."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    entities = []
    
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            entities.append({
                "platform": platform,
                "entity_name": sheet_name,
                "sheet_name": sheet_name,
                "export_format": "unknown",
                "fields": [],
                "field_count": 0,
            })
            continue
        
        # Find header row - look for rows containing common header keywords
        header_row_idx = None
        header = None
        for i, row in enumerate(rows):
            row_strs = [str(c).strip().lower() if c else "" for c in row]
            # Look for field/column name headers
            if any(h in row_strs for h in ["field name", "field", "column name", "column", "element", "element name", "name", "attribute"]):
                header_row_idx = i
                header = [str(c).strip() if c else f"col_{j}" for j, c in enumerate(row)]
                break
        
        if header_row_idx is None:
            # Try first row as header
            header_row_idx = 0
            header = [str(c).strip() if c else f"col_{j}" for j, c in enumerate(rows[0])]
        
        # Parse fields
        fields = []
        for row in rows[header_row_idx + 1:]:
            if not row or all(c is None or str(c).strip() == "" for c in row):
                continue
            
            field = {}
            for j, val in enumerate(row):
                if j < len(header):
                    key = header[j]
                    if val is not None:
                        field[key] = str(val).strip()
            
            # Normalize field names
            normalized = {}
            for k, v in field.items():
                kl = k.lower().replace(" ", "_")
                if kl in ("field_name", "field", "column_name", "column", "element", "element_name", "name", "attribute"):
                    normalized["field_name"] = v
                elif kl in ("data_type", "type", "datatype"):
                    normalized["data_type"] = v
                elif kl in ("description", "desc", "definition", "notes"):
                    if "description" not in normalized:
                        normalized["description"] = v
                    else:
                        normalized["description"] += " | " + v
                elif kl in ("max_length", "length", "size"):
                    normalized["max_length"] = v
                elif kl in ("nullable", "null", "required", "optional"):
                    normalized["nullable"] = v
                elif kl in ("parent", "parent_element"):
                    normalized["parent_element"] = v
                else:
                    normalized[k] = v
            
            # Skip rows that are clearly not fields (e.g., section headers)
            if "field_name" not in normalized:
                # Check if any value looks like a field name
                first_val = None
                for v in field.values():
                    if v and v.strip():
                        first_val = v
                        break
                if first_val:
                    normalized["field_name"] = first_val
                else:
                    continue
            
            fields.append(normalized)
        
        # Detect export format from sheet name or content
        export_format = "CSV"
        sn_lower = sheet_name.lower()
        if "xml" in sn_lower or "vitals" in sn_lower or "encounter" in sn_lower or "result" in sn_lower:
            if platform == "SRSPro":
                export_format = "XML"
        if "ccda" in sn_lower:
            export_format = "C-CDA"
        if "json" in sn_lower:
            export_format = "JSON"
        
        entities.append({
            "platform": platform,
            "entity_name": sheet_name,
            "sheet_name": sheet_name,
            "export_format": export_format,
            "header": header,
            "fields": fields,
            "field_count": len(fields),
        })
    
    wb.close()
    return entities

def main():
    all_entities = []
    for platform, path in FILES.items():
        if os.path.exists(path):
            entities = parse_workbook(path, platform)
            all_entities.extend(entities)
            print(f"\n{platform}: {len(entities)} sheets")
            for e in entities:
                desc_count = sum(1 for f in e["fields"] if f.get("description", "").strip())
                type_count = sum(1 for f in e["fields"] if f.get("data_type", "").strip())
                print(f"  {e['entity_name']}: {e['field_count']} fields, {desc_count} with desc, {type_count} with type")
    
    # Save full inventory
    out_path = os.path.join(os.path.dirname(__file__), "entity-inventory-full.json")
    with open(out_path, "w") as f:
        json.dump(all_entities, f, indent=2)
    print(f"\nSaved {len(all_entities)} entities to {out_path}")
    
    # Generate summary
    summary = {"platforms": {}}
    for platform in FILES:
        platform_entities = [e for e in all_entities if e["platform"] == platform]
        total_fields = sum(e["field_count"] for e in platform_entities)
        total_described = sum(
            sum(1 for f in e["fields"] if f.get("description", "").strip())
            for e in platform_entities
        )
        total_typed = sum(
            sum(1 for f in e["fields"] if f.get("data_type", "").strip())
            for e in platform_entities
        )
        
        # Categorize entities by domain
        categories = {}
        for e in platform_entities:
            cat = categorize_entity(e["entity_name"])
            if cat not in categories:
                categories[cat] = {"entities": [], "field_count": 0}
            categories[cat]["entities"].append(e["entity_name"])
            categories[cat]["field_count"] += e["field_count"]
        
        summary["platforms"][platform] = {
            "entity_count": len(platform_entities),
            "total_fields": total_fields,
            "fields_with_descriptions": total_described,
            "fields_with_types": total_typed,
            "description_pct": round(total_described / total_fields * 100, 1) if total_fields else 0,
            "type_pct": round(total_typed / total_fields * 100, 1) if total_fields else 0,
            "entities": [
                {
                    "name": e["entity_name"],
                    "field_count": e["field_count"],
                    "fields_with_descriptions": sum(1 for f in e["fields"] if f.get("description", "").strip()),
                    "fields_with_types": sum(1 for f in e["fields"] if f.get("data_type", "").strip()),
                    "export_format": e["export_format"],
                }
                for e in platform_entities
            ],
            "categories": categories,
        }
    
    # Grand totals
    all_fields = sum(e["field_count"] for e in all_entities)
    all_described = sum(
        sum(1 for f in e["fields"] if f.get("description", "").strip())
        for e in all_entities
    )
    summary["grand_totals"] = {
        "total_platforms": len(FILES),
        "total_entities": len(all_entities),
        "total_fields": all_fields,
        "fields_with_descriptions": all_described,
        "description_pct": round(all_described / all_fields * 100, 1) if all_fields else 0,
    }
    
    summary_path = os.path.join(os.path.dirname(__file__), "entity-inventory-summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved summary to {summary_path}")

def categorize_entity(name):
    """Categorize entity by domain based on name."""
    nl = name.lower()
    if any(w in nl for w in ["demograph", "patient"]):
        return "Demographics"
    if any(w in nl for w in ["appointment", "encounter"]):
        return "Encounters/Appointments"
    if any(w in nl for w in ["diagnos", "problem"]):
        return "Problems/Diagnoses"
    if any(w in nl for w in ["medication", "prescription", "injection", "specialty med"]):
        return "Medications/Injections"
    if any(w in nl for w in ["allerg"]):
        return "Allergies"
    if any(w in nl for w in ["immuniz"]):
        return "Immunizations"
    if any(w in nl for w in ["vital"]):
        return "Vitals"
    if any(w in nl for w in ["lab", "result"]):
        return "Lab/Results"
    if any(w in nl for w in ["order"]):
        return "Orders"
    if any(w in nl for w in ["chart", "note", "emn"]):
        return "Clinical Notes"
    if any(w in nl for w in ["document", "image", "form"]):
        return "Documents/Images"
    if any(w in nl for w in ["insurance", "auth", "guarantor"]):
        return "Insurance/Authorization"
    if any(w in nl for w in ["charge", "billing", "payment", "claim"]):
        return "Billing/Financial"
    if any(w in nl for w in ["referral", "shared care"]):
        return "Referrals/Care Coordination"
    if any(w in nl for w in ["message", "communication", "secure", "pracyakker", "task", "todo"]):
        return "Communications/Messaging"
    if any(w in nl for w in ["family"]):
        return "Family History"
    if any(w in nl for w in ["smoking", "social"]):
        return "Social History"
    if any(w in nl for w in ["implant", "device"]):
        return "Implantable Devices"
    if any(w in nl for w in ["alert", "custom"]):
        return "Custom/Alerts"
    if any(w in nl for w in ["recall", "follow"]):
        return "Recalls/Follow-up"
    if any(w in nl for w in ["procedure", "surgery"]):
        return "Procedures"
    if any(w in nl for w in ["refraction", "glaucoma", "retina"]):
        return "Ophthalmology-Specific"
    if any(w in nl for w in ["code", "vocabulary"]):
        return "Reference/Code Systems"
    return "Other"

if __name__ == "__main__":
    main()
