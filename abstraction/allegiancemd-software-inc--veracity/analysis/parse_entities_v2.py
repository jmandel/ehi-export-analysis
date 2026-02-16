#!/usr/bin/env python3
"""
Parse all Javadoc entity HTML files from AllegianceMD's EHI export documentation.
Uses regex-based extraction for reliability.
Produces full-entity-inventory.json and summary-statistics.json.
"""

import json
import os
import re

DOWNLOADS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/allegiancemd-software-inc--veracity/downloads"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/allegiancemd-software-inc--veracity/analysis"

ENTITY_FILES = sorted([
    f for f in os.listdir(DOWNLOADS_DIR)
    if f.endswith("Entity.html")
])


def extract_text(html_fragment):
    """Strip HTML tags and decode entities, return clean text."""
    text = re.sub(r'<[^>]+>', '', html_fragment)
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    return text.strip()


def parse_entity_file(filepath):
    """Parse a Javadoc entity HTML file using regex to extract fields."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    fields = []
    
    # Pattern for three-column rows: type | field name | description
    # Each row has three divs: col-first, col-second, col-last
    # We match triplets of these divs
    
    # First, find the summary-table section
    table_match = re.search(r'<div class="summary-table[^"]*">(.*?)</section>', html, re.DOTALL)
    if not table_match:
        return fields, ""
    
    table_html = table_match.group(1)
    
    # Check if it's three-column or two-column
    is_three_col = "three-column-summary" in html
    
    if is_three_col:
        # Match row triplets: col-first, col-second, col-last
        row_pattern = re.compile(
            r'<div class="col-first (?:even|odd)-row-color">\s*(.*?)\s*</div>\s*'
            r'<div class="col-second (?:even|odd)-row-color">\s*(.*?)\s*</div>\s*'
            r'<div class="col-last (?:even|odd)-row-color">\s*(.*?)\s*</div>',
            re.DOTALL
        )
        
        for match in row_pattern.finditer(table_html):
            type_html = match.group(1)
            name_html = match.group(2)
            desc_html = match.group(3)
            
            # Extract type
            type_text = extract_text(type_html)
            # Handle List<Entity> types by looking for wbr pattern
            if '<wbr>' in type_html:
                # e.g., List<wbr>&lt;<a href="...">SomeEntity</a>&gt;
                list_match = re.search(r'>List</a><wbr>&lt;<a[^>]*>(\w+)</a>&gt;', type_html)
                if list_match:
                    type_text = f"List<{list_match.group(1)}>"
            
            # Extract field name
            name_match = re.search(r'class="member-name-link">(\w+)</a>', name_html)
            field_name = name_match.group(1) if name_match else extract_text(name_html)
            
            # Extract description — note: the outer regex's lazy .*? captures
            # the block div content but the closing </div> is consumed by the outer regex
            desc_match = re.search(r'<div class="block">\s*(.*)', desc_html, re.DOTALL)
            description = extract_text(desc_match.group(1)).strip() if desc_match else ""
            
            if field_name and field_name not in ("Field", "Description"):
                fields.append({
                    "name": field_name,
                    "type": type_text,
                    "description": description
                })
    else:
        # Two-column: col-first (type+name?), col-last (description?)
        row_pattern = re.compile(
            r'<div class="col-first (?:even|odd)-row-color[^"]*">\s*(.*?)\s*</div>\s*'
            r'<div class="col-last (?:even|odd)-row-color[^"]*">\s*(.*?)\s*</div>',
            re.DOTALL
        )
        for match in row_pattern.finditer(table_html):
            first = match.group(1)
            last = match.group(2)
            # This is for the index page, not entity fields
    
    # Extract entity-level description from the class description block
    entity_desc = ""
    desc_block = re.search(r'<div class="block">\s*(.*?)\s*</div>', html, re.DOTALL)
    # The first block div before the summary table might be the entity description
    # But in entity pages, the description (if any) appears in the class description section
    # Let's look for it specifically
    class_desc = re.search(r'<section class="class-description"[^>]*>.*?<div class="block">\s*(.*?)\s*</div>', html, re.DOTALL)
    if class_desc:
        entity_desc = extract_text(class_desc.group(1))
    
    return fields, entity_desc


def main():
    inventory = {}
    
    for filename in ENTITY_FILES:
        entity_name = filename.replace('.html', '')
        filepath = os.path.join(DOWNLOADS_DIR, filename)
        
        fields, entity_desc = parse_entity_file(filepath)
        
        # Identify list references (relationships to other entities)
        list_references = []
        for f in fields:
            list_match = re.match(r'List<(\w+)>', f["type"])
            if list_match:
                list_references.append({
                    "field_name": f["name"],
                    "referenced_entity": list_match.group(1),
                    "description": f["description"]
                })
        
        inventory[entity_name] = {
            "entity_name": entity_name,
            "entity_description": entity_desc,
            "source_file": filename,
            "source_url": f"https://allegiancemd.com/ehi-export/{filename}",
            "field_count": len(fields),
            "fields_with_descriptions": sum(1 for f in fields if f["description"]),
            "list_references": list_references,
            "fields": fields
        }
    
    # Parse index page for entity-level descriptions
    index_path = os.path.join(DOWNLOADS_DIR, "ehi-export-index.html")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_html = f.read()
    
    # Extract entity descriptions from index using regex
    index_pattern = re.compile(
        r'<a href="(\w+Entity)\.html"[^>]*>\1</a>\s*</div>\s*'
        r'<div class="col-last[^"]*"[^>]*>\s*'
        r'(?:<div class="block">\s*(.*?)\s*</div>|&nbsp;)\s*</div>',
        re.DOTALL
    )
    for match in index_pattern.finditer(index_html):
        name = match.group(1)
        desc = extract_text(match.group(2)) if match.group(2) else ""
        if desc and name in inventory and not inventory[name]["entity_description"]:
            inventory[name]["entity_description"] = desc
    
    # Write full inventory
    with open(os.path.join(OUTPUT_DIR, "full-entity-inventory.json"), 'w') as f:
        json.dump(inventory, f, indent=2)
    
    # Generate summary statistics
    total_entities = len(inventory)
    total_fields = sum(e["field_count"] for e in inventory.values())
    total_described = sum(e["fields_with_descriptions"] for e in inventory.values())
    
    categories = {
        "Demographics": ["PatientEntity", "GuarantorEntity", "PatientCustomFieldsEntity"],
        "Clinical - Encounters": ["EncountersEntity", "EncountersDiagEntity", "EmrEncounterEntity"],
        "Clinical - Problems & Conditions": ["EmrProblemEntity"],
        "Clinical - Medications": ["EmrMedicationEntity"],
        "Clinical - Allergies": ["EmrAllergyEntity"],
        "Clinical - Immunizations": ["EmrInjectionEntity"],
        "Clinical - Vitals": ["EmrVitalsEntity", "EmrVitalsCategoryEntity"],
        "Clinical - Orders & Results": ["EmrPatientOrderItemEntity", "EmrPatientOrderPanelEntity"],
        "Clinical - Devices": ["EmrImplantableDeviceEntity"],
        "Clinical - Screenings & Forms": ["ScreeningEntity", "PatientMedicalFormEntity"],
        "Insurance & Coverage": ["InsuranceDataEntity", "InsuranceDataAuthorizationsEntity"],
        "Billing & Transactions": ["TransactionsEntity", "PaymentEntity"],
        "Cases": ["CasesEntity"],
        "Appointments": ["AppointmentsEntity"],
        "Care Team & Referrals": ["PatientCareTeamEntity", "EmrRefToProvidersEntity"],
        "Messages & Notes": ["MessagesEntity", "InternalNotesEntity", "NotesEntity"],
        "Tasks": ["TasksEntity", "TaskCommentsEntity"],
        "Pharmacy": ["PatientPharmacyEntity"],
    }
    
    summary = {
        "total_entities": total_entities,
        "total_fields": total_fields,
        "total_fields_with_descriptions": total_described,
        "description_coverage_pct": round(total_described / total_fields * 100, 1) if total_fields else 0,
        "entities_fully_documented": [],
        "entities_no_descriptions": [],
        "entities_partial_descriptions": [],
        "category_breakdown": {},
        "entity_summary": []
    }
    
    for name, data in sorted(inventory.items(), key=lambda x: -x[1]["field_count"]):
        pct = round(data["fields_with_descriptions"] / data["field_count"] * 100, 1) if data["field_count"] else 0
        entry = {
            "entity": name,
            "fields": data["field_count"],
            "described": data["fields_with_descriptions"],
            "pct": pct,
            "list_refs": len(data["list_references"]),
            "entity_description": data["entity_description"]
        }
        summary["entity_summary"].append(entry)
        
        if pct == 100 and data["field_count"] > 0:
            summary["entities_fully_documented"].append(name)
        elif pct == 0:
            summary["entities_no_descriptions"].append(name)
        else:
            summary["entities_partial_descriptions"].append(name)
    
    for cat, entities in categories.items():
        cat_fields = sum(inventory[e]["field_count"] for e in entities if e in inventory)
        cat_described = sum(inventory[e]["fields_with_descriptions"] for e in entities if e in inventory)
        summary["category_breakdown"][cat] = {
            "entities": len([e for e in entities if e in inventory]),
            "entity_names": [e for e in entities if e in inventory],
            "fields": cat_fields,
            "described": cat_described,
            "pct": round(cat_described / cat_fields * 100, 1) if cat_fields else 0
        }
    
    with open(os.path.join(OUTPUT_DIR, "summary-statistics.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Compare with prior extraction
    with open(os.path.join(DOWNLOADS_DIR, "entity-data-dictionary.json"), 'r') as f:
        prior = json.load(f)
    
    print("=== Independent Parse Results ===")
    print(f"Total entities: {total_entities}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {total_described} ({summary['description_coverage_pct']}%)")
    print()
    print(f"Fully documented entities ({len(summary['entities_fully_documented'])}): {', '.join(summary['entities_fully_documented'])}")
    print(f"Partial descriptions ({len(summary['entities_partial_descriptions'])}): {', '.join(summary['entities_partial_descriptions'])}")
    print(f"No descriptions ({len(summary['entities_no_descriptions'])}): {', '.join(summary['entities_no_descriptions'])}")
    print()
    
    print("=== Comparison with Prior Extraction ===")
    prior_entities = set(prior.keys())
    my_entities = set(inventory.keys())
    print(f"Prior entities: {len(prior_entities)}, My entities: {len(my_entities)}")
    
    mismatches = []
    for entity_name in sorted(my_entities):
        my_count = inventory[entity_name]["field_count"]
        my_desc = inventory[entity_name]["fields_with_descriptions"]
        prior_fields = prior.get(entity_name, [])
        prior_count = len(prior_fields)
        prior_desc = sum(1 for f in prior_fields if f.get("description", "").strip())
        if my_count != prior_count or my_desc != prior_desc:
            mismatches.append(f"  {entity_name}: mine={my_count} fields/{my_desc} desc, prior={prior_count} fields/{prior_desc} desc")
    
    if mismatches:
        print("Field/description count mismatches:")
        for m in mismatches:
            print(m)
    else:
        print("All counts match prior extraction.")
    
    print()
    print("=== Category Breakdown ===")
    for cat, info in summary["category_breakdown"].items():
        print(f"  {cat}: {info['entities']} entities, {info['fields']} fields, {info['described']} described ({info['pct']}%)")
    
    print()
    print("=== Entity Detail (sorted by field count) ===")
    for entry in summary["entity_summary"]:
        desc_label = f" - \"{entry['entity_description']}\"" if entry['entity_description'] else ""
        print(f"  {entry['entity']}: {entry['fields']} fields, {entry['described']} described ({entry['pct']}%), {entry['list_refs']} list refs{desc_label}")


if __name__ == "__main__":
    main()
