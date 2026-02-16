#!/usr/bin/env python3
"""Parse Harris CareTracker EHI Export PDF data dictionary into structured JSON.

Reads the PDF text via pdftotext and parses Data Classes and Column Headings.
"""

import json
import re
import subprocess
import os

PDF_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "downloads",
                        "CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Known multi-line entity names (from manual PDF review)
MULTILINE_CONTINUATIONS = {
    "Pending": "Allergies and Intolerances Pending",
    "History": None,  # Could be "Occupation and Industry History" or "FamilyHistory"
    "Capture": "Patient Health Information Capture",
}

def main():
    result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"],
                            capture_output=True, text=True)
    text = result.stdout
    lines = text.split("\n")

    raw_entities = []
    current_entity = None
    current_fields_text = ""
    in_table = False

    def save_current():
        nonlocal current_entity, current_fields_text
        if current_entity and current_fields_text:
            cleaned = re.sub(r'\s+', ' ', current_fields_text).strip().rstrip(',')
            raw_fields = [f.strip() for f in cleaned.split(',') if f.strip()]
            fields = [{"name": f, "type": None, "description": None} for f in raw_fields]
            raw_entities.append({
                "entity_name": current_entity,
                "field_count": len(fields),
                "fields": fields
            })
        current_entity = None
        current_fields_text = ""

    for line in lines:
        stripped = line.rstrip()
        if "CareTracker EHI Export: Folder Organization" in stripped:
            continue
        if re.match(r'^\s*\d+\s*$', stripped):
            continue
        if not stripped.strip():
            continue
        if "Data Class Name" in stripped and "Column Headings" in stripped:
            in_table = True
            continue
        if not in_table:
            continue

        leading_spaces = len(stripped) - len(stripped.lstrip())

        # New entity: text starts at left margin with fields after gap
        match = re.match(r'^(\s{0,29}\S.*?)\s{3,}(\w+.*)', stripped)
        if match and leading_spaces < 30:
            save_current()
            current_entity = match.group(1).strip()
            current_fields_text = match.group(2).strip()
        elif leading_spaces < 5 and current_entity:
            txt = stripped.strip()
            # Multi-line entity name continuation (short text, no commas)
            if ',' not in txt and len(txt.split()) <= 4:
                current_entity += " " + txt
            else:
                current_fields_text += " " + txt
        elif leading_spaces >= 5:
            current_fields_text += " " + stripped.strip()

    save_current()

    # Post-process: merge split entities
    # "Allergies and Intolerances" (6 fields) should merge with next "Pending" → 
    # Actually from the PDF: there are TWO separate data classes:
    #   "Allergies and Intolerances Pending" and "Allergies and Intolerances"
    # Similarly: "Occupation and Industry History" is one entity
    # "Patient Health Information Capture" is one entity

    entities = []
    i = 0
    while i < len(raw_entities):
        e = raw_entities[i]
        name = e["entity_name"]
        
        # Check if this entity's fields got split with the next entry being a continuation
        if i + 1 < len(raw_entities):
            next_e = raw_entities[i + 1]
            next_name = next_e["entity_name"]
            
            # "Allergies and Intolerances" (6 fields) + "Pending" → merge
            if name == "Allergies and Intolerances" and next_name == "Pending" and e["field_count"] < 10:
                merged_fields = e["fields"] + next_e["fields"]
                entities.append({
                    "entity_name": "Allergies and Intolerances Pending",
                    "field_count": len(merged_fields),
                    "fields": merged_fields
                })
                i += 2
                continue
            
            # "Occupation and Industry" + "History" → merge  
            if name == "Occupation and Industry" and next_name == "History":
                merged_fields = e["fields"] + next_e["fields"]
                entities.append({
                    "entity_name": "Occupation and Industry History",
                    "field_count": len(merged_fields),
                    "fields": merged_fields
                })
                i += 2
                continue
            
            # "Patient Health Information" + "Capture" → merge
            if name == "Patient Health Information" and next_name == "Capture":
                merged_fields = e["fields"] + next_e["fields"]
                entities.append({
                    "entity_name": "Patient Health Information Capture",
                    "field_count": len(merged_fields),
                    "fields": merged_fields
                })
                i += 2
                continue

        entities.append(e)
        i += 1

    total_fields = sum(e["field_count"] for e in entities)

    # Categorize entities
    categories = {
        "Demographics": ["Patient Demographics", "Next Of Kin", "Occupation and Industry History"],
        "Clinical": ["Addendum", "Assesments", "Clinical Notes", "FunctionalStatus", 
                     "Goals", "Health Concerns", "Plan of Treatment", "Risk Factors",
                     "Smoking Statuses", "Tracked Data", "Travel History", "Vital Signs",
                     "User Defined Fields"],
        "Problems & Diagnoses": ["List Problem", "List Problem Pending"],
        "Medications": ["Medications", "Medications Pending", "Injections"],
        "Allergies": ["Allergies and Intolerances", "Allergies and Intolerances Pending"],
        "Immunizations": ["Immunizations", "HM Rules", "HM Rules Ignored", "Demographic Immunization"],
        "Lab & Results": ["Lab Tests"],
        "Orders & Referrals": ["Orders", "Referrals"],
        "Procedures": ["Procedures"],
        "Devices": ["Implantable device"],
        "Documents & Records": ["Imported Items", "Patient Generated Data", 
                                "Patient Health Information Capture", "Patient Record Release",
                                "Advance Directives", "Alerts"],
        "Billing & Insurance": ["Billing History", "Health Insurance"],
        "Care Team": ["Care Team Members"],
        "Scheduling": ["Scheduling"],
        "Communications": ["Email"],
        "Family History": ["FamilyHistory"],
    }

    # Assign categories
    cat_lookup = {}
    for cat, names in categories.items():
        for n in names:
            cat_lookup[n] = cat

    for e in entities:
        e["category"] = cat_lookup.get(e["entity_name"], "Other")

    # Category summary
    cat_summary = {}
    for e in entities:
        cat = e["category"]
        if cat not in cat_summary:
            cat_summary[cat] = {"entity_count": 0, "field_count": 0, "entities": []}
        cat_summary[cat]["entity_count"] += 1
        cat_summary[cat]["field_count"] += e["field_count"]
        cat_summary[cat]["entities"].append(e["entity_name"])

    inventory = {
        "product": "Harris CareTracker",
        "source": "CareTracker-EHI-Export-Documentation-V1_0-1-1.pdf",
        "version": "v1.0",
        "export_formats": ["CSV", "JSON", "XML"],
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "entities": entities
    }

    with open(os.path.join(OUT_DIR, "entity-inventory-full.json"), "w") as f:
        json.dump(inventory, f, indent=2)

    summary = {
        "product": inventory["product"],
        "source": inventory["source"],
        "version": inventory["version"],
        "export_formats": inventory["export_formats"],
        "total_entities": inventory["total_entities"],
        "total_fields": inventory["total_fields"],
        "fields_with_descriptions": 0,
        "fields_with_types": 0,
        "pct_fields_with_descriptions": "0%",
        "category_breakdown": cat_summary,
        "entity_summary": [
            {"entity_name": e["entity_name"], "field_count": e["field_count"], "category": e["category"]}
            for e in entities
        ]
    }

    with open(os.path.join(OUT_DIR, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: 0")
    print(f"Fields with types: 0")
    print()
    print("Category breakdown:")
    for cat, info in sorted(cat_summary.items()):
        print(f"  {cat}: {info['entity_count']} entities, {info['field_count']} fields")
        for en in info['entities']:
            matching = [e for e in entities if e['entity_name'] == en]
            if matching:
                print(f"    - {en}: {matching[0]['field_count']} fields")
    print()

if __name__ == "__main__":
    main()
