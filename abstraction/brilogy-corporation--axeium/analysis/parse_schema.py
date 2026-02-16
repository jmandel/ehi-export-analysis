#!/usr/bin/env python3
"""Parse the AXEIUM Schema.pdf extracted text into structured JSON inventory."""

import json
import re
from collections import defaultdict

def parse_schema(filepath):
    tables = defaultdict(list)
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('TABLE_NAME'):
                continue
            parts = line.split()
            if len(parts) >= 3:
                table = parts[0]
                col = parts[1]
                dtype = parts[2]
                tables[table].append({
                    "name": col,
                    "type": dtype
                })
    
    return tables

def categorize_table(table_name):
    """Categorize tables based on naming and known content."""
    name = table_name.lower()
    
    # Specific table overrides first
    overrides = {
        'mchart': 'Patient Demographics & Chart',
        'mpatient': 'Patient Demographics & Chart',
        'mpatientadditional': 'Patient Demographics & Chart',
        'mpatientcdp': 'Patient Demographics & Chart',
        'mpatientchartinformation': 'Patient Demographics & Chart',
        'mpatientdescriptor': 'Patient Demographics & Chart',
        'mpatientemployment': 'Patient Demographics & Chart',
        'mpatientethnic': 'Patient Demographics & Chart',
        'mpatientfamilymember': 'Patient Demographics & Chart',
        'mpatientsealthmeasure': 'Patient Demographics & Chart',
        'mpatientinsurance': 'Insurance',
        'mpatientneedymed': 'Patient Assistance Programs',
        'mpatientnote': 'Clinical Notes',
        'mpatientotherinformation': 'Patient Demographics & Chart',
        'mpatientpayerdescriptor': 'Insurance',
        'mpatientportal': 'Patient Portal',
        'mpatientpreference': 'Patient Demographics & Chart',
        'mpatientprescribedmedicine': 'Medications',
        'mpatientprogram': 'Patient Programs',
        'mpatientrace': 'Patient Demographics & Chart',
        'mpatientregistration': 'Patient Demographics & Chart',
        'mpatientreleaseauthorization': 'Consents & Authorizations',
        'mpatientrepresentative': 'Patient Demographics & Chart',
        'mpatientupi': 'Patient Demographics & Chart',
        'mpatientappttypefee': 'Scheduling / Fees',
        'mpatienthealthmeasure': 'Health Measures / Vitals',
        'msignature': 'Signatures',
        'mscpatient': 'Scorecard / Quality',
        'mscbaselinepatientvalue': 'Scorecard / Quality',
        'tpregnancy': 'Pregnancy / OB',
        'tcbeexam': 'Clinical Breast Exam',
        'trefill': 'Medications',
        'tevent': 'Scheduling / Events',
        'texam': 'Clinical Exams',
        'texamhistory': 'Clinical Exams',
        'texamsurvey': 'Clinical Exams / Surveys',
        'tcallqueueitem': 'Patient Communications',
        'temailmessage': 'Patient Communications',
        'tsmsmessage': 'Patient Communications',
        'tpatientfax': 'Patient Communications',
        'tvideosession': 'Telehealth',
        'tvideosessionparticipant': 'Telehealth',
        'tpatientcase': 'Case Management',
        'tpatientcasemanagement': 'Case Management',
        'tpatientclinicalinfo': 'Vitals / Clinical Info',
        'tpatientclinicalmeasuredw': 'Clinical Measures',
        'tpatientdisclosure': 'Disclosures',
        'tpatienteducationlist': 'Patient Education',
        'tpatientexternalhealthmeasure': 'External Health Measures',
        'tpatientform': 'Custom Forms',
        'tpatienthealthmeasure': 'Health Measures / Vitals',
        'tpatientlog': 'Patient Audit',
        'tpatientauditlog': 'Patient Audit',
        'tpatientprintobject': 'Print / Documents',
        'tpatienttickie': 'Reminders / Follow-up',
        'tpatienttickie': 'Reminders / Follow-up',
        'tpatienttreatmentplan': 'Treatment Plans',
        'tpatientworksheet': 'Clinical Worksheets',
        'tprintstatement': 'Billing Statements',
        'tpurchaseorder': 'Purchase Orders',
        'ttaskitem': 'Tasks / Workflow',
        'tudstableinfotemp': 'UDS Reporting',
        'toshpdexception': 'OSHPD Reporting',
        'tbhtreatmentplan': 'Behavioral Health',
        'tarreceipt': 'Accounts Receivable',
        'tarcloseagingtemp': 'Accounts Receivable',
        'tarcloseiagingtempdetail': 'Accounts Receivable',
    }
    
    if name in overrides:
        return overrides[name]
    
    # Pattern-based fallback
    if 'cpsp' in name:
        return 'CPSP (Prenatal/Perinatal)'
    elif 'dental' in name or 'tooth' in name or 'perio' in name:
        return 'Dental'
    elif 'vision' in name or 'refract' in name:
        return 'Vision'
    elif 'insurance' in name:
        return 'Insurance'
    elif 'billing' in name or 'hcfa' in name:
        return 'Billing'
    elif 'visit' in name and 'chdp' not in name:
        return 'Visits / Encounters'
    elif 'chdp' in name:
        return 'CHDP (Child Health)'
    elif 'lab' in name or 'observation' in name:
        return 'Laboratory'
    elif 'rx' in name or 'medication' in name or 'refill' in name:
        return 'Medications'
    elif 'immuniz' in name:
        return 'Immunizations'
    elif 'allergy' in name:
        return 'Allergies'
    elif 'vital' in name:
        return 'Vitals'
    elif 'problem' in name or 'diagnosis' in name:
        return 'Problems / Diagnoses'
    elif 'document' in name or 'scan' in name:
        return 'Documents'
    elif 'referral' in name:
        return 'Referrals'
    elif 'contact' in name:
        return 'Patient Contacts'
    elif name.startswith('mpatient'):
        return 'Patient Demographics & Chart'
    else:
        return 'Other'

def main():
    tables = parse_schema('schema-raw.txt')
    
    entities = []
    for table_name, columns in sorted(tables.items()):
        category = categorize_table(table_name)
        entities.append({
            "entity": table_name,
            "category": category,
            "field_count": len(columns),
            "fields": [{"name": f["name"], "type": f["type"], "description": ""} for f in columns]
        })
    
    full_inventory = {
        "product": "AXEIUM",
        "source": "Schema.pdf (extracted via pdftotext)",
        "total_entities": len(entities),
        "total_fields": sum(e["field_count"] for e in entities),
        "fields_with_descriptions": 0,
        "note": "Schema.pdf provides only TABLE_NAME, COLUMN_NAME, DATA_TYPE — no field descriptions, no value sets, no foreign key documentation",
        "entities": entities
    }
    
    with open('entity-inventory-full.json', 'w') as f:
        json.dump(full_inventory, f, indent=2)
    
    # Summary
    category_stats = defaultdict(lambda: {"tables": 0, "fields": 0, "table_names": []})
    for e in entities:
        cat = e["category"]
        category_stats[cat]["tables"] += 1
        category_stats[cat]["fields"] += e["field_count"]
        category_stats[cat]["table_names"].append(e["entity"])
    
    type_counts = defaultdict(int)
    for e in entities:
        for f in e["fields"]:
            type_counts[f["type"]] += 1
    
    summary = {
        "product": "AXEIUM",
        "total_entities": len(entities),
        "total_fields": sum(e["field_count"] for e in entities),
        "fields_with_descriptions": 0,
        "fields_with_types": sum(e["field_count"] for e in entities),
        "description_coverage_pct": 0.0,
        "type_coverage_pct": 100.0,
        "data_type_distribution": dict(sorted(type_counts.items(), key=lambda x: -x[1])),
        "categories": {
            cat: {
                "tables": stats["tables"],
                "fields": stats["fields"],
                "table_names": stats["table_names"]
            }
            for cat, stats in sorted(category_stats.items())
        },
        "top_entities_by_field_count": [
            {"entity": e["entity"], "field_count": e["field_count"], "category": e["category"]}
            for e in sorted(entities, key=lambda x: -x["field_count"])[:20]
        ]
    }
    
    with open('entity-inventory-summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Console output
    print(f"Total entities: {len(entities)}")
    print(f"Total fields: {sum(e['field_count'] for e in entities)}")
    print(f"\nCategory breakdown:")
    for cat, stats in sorted(category_stats.items(), key=lambda x: -x[1]['fields']):
        print(f"  {cat}: {stats['tables']} tables, {stats['fields']} fields")
        for t in stats['table_names']:
            matching = [e for e in entities if e['entity'] == t]
            if matching:
                print(f"    - {t} ({matching[0]['field_count']} fields)")

if __name__ == '__main__':
    main()
