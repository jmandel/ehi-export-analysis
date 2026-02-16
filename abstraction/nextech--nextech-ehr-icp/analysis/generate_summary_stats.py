#!/usr/bin/env python3
"""Generate summary statistics from the full entity inventory."""

import json
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent

with open(OUTPUT / "full-entity-inventory.json") as f:
    data = json.load(f)

# Per-platform summaries
for p in data['platforms']:
    print(f"\n{'='*60}")
    print(f"Platform: {p['platform']}")
    print(f"Certified Product: {p['certified_product']}")
    print(f"CHPL ID: {p['chpl_id']}")
    print(f"Source: {p['source_file']}")
    print(f"{'='*60}")
    print(f"Total entities: {p['entity_count']}")
    print(f"Total fields: {p['total_fields']}")
    print(f"Fields with descriptions: {p['fields_with_descriptions']} ({p['fields_with_descriptions']/p['total_fields']*100:.1f}%)")
    print()

    # Sort entities by field count descending
    sorted_entities = sorted(p['entities'], key=lambda e: e['field_count'], reverse=True)
    print(f"{'Entity':<40} {'Fields':>6} {'Described':>9} {'%':>5}")
    print(f"{'-'*40} {'-'*6} {'-'*9} {'-'*5}")
    for e in sorted_entities:
        pct = f"{e['fields_with_descriptions']/e['field_count']*100:.0f}%" if e['field_count'] > 0 else "N/A"
        print(f"{e['entity_name']:<40} {e['field_count']:>6} {e['fields_with_descriptions']:>9} {pct:>5}")


# Cross-platform comparison
print(f"\n{'='*60}")
print("CROSS-PLATFORM COMPARISON")
print(f"{'='*60}")
print(f"{'Platform':<30} {'Entities':>8} {'Fields':>8} {'Described':>10} {'Rate':>6}")
print(f"{'-'*30} {'-'*8} {'-'*8} {'-'*10} {'-'*6}")
for p in data['platforms']:
    rate = f"{p['fields_with_descriptions']/p['total_fields']*100:.1f}%" if p['total_fields'] > 0 else "N/A"
    print(f"{p['platform']:<30} {p['entity_count']:>8} {p['total_fields']:>8} {p['fields_with_descriptions']:>10} {rate:>6}")

print(f"\n{'TOTAL':<30} {data['summary']['total_entities']:>8} {data['summary']['total_fields']:>8} {data['summary']['total_fields_with_descriptions']:>10} {data['summary']['description_rate']:>6}")

# Domain coverage analysis
print(f"\n{'='*60}")
print("DOMAIN COVERAGE BY PLATFORM")
print(f"{'='*60}")

# SRSPro domains
srspro = next(p for p in data['platforms'] if p['platform'] == 'SRSPro')
print("\nSRSPro Data Domains:")
domain_map = {
    'Appointments': ['Appointment List (CSV)'],
    'Custom Alerts': ['Custom Alerts (CSV)'],
    'Diagnoses': ['Diagnoses (CSV)'],
    'Family History': ['Family History (CSV)', 'Family History Codes (CSV)', 'Family History Statuses (CSV)'],
    'Implantable Devices': ['Implantable Devices (CSV)'],
    'Injections/Medications': ['Injections (CSV)', 'Medication (CCDA)'],
    'Insurance/Guarantor': ['GuarantorInformation (CSV)', 'Insurance Information (CSV)'],
    'User Defined Fields': ['UDFs (CSV)'],
    'Smoking/Social History': ['Smoking Status (CSV)'],
    'Orders': ['Orders (CSV)'],
    'Messages': ['Messages (CSV)'],
    'Code Reference': ['CodeSystemNames (CSV)'],
    'Encounter Data (XML)': ['Encounter Data Capture (XMLs)'],
    'Vitals (XML)': ['Vitals (XML) 2'],
    'Results (XML)': ['Results(XML)'],
}

entities_by_name = {e['entity_name']: e for e in srspro['entities']}
for domain, enames in domain_map.items():
    total_f = sum(entities_by_name.get(en, {}).get('field_count', 0) for en in enames)
    total_d = sum(entities_by_name.get(en, {}).get('fields_with_descriptions', 0) for en in enames)
    count = len([en for en in enames if en in entities_by_name])
    print(f"  {domain}: {count} entities, {total_f} fields ({total_d} described)")

# ICP domains
icp = next(p for p in data['platforms'] if p['platform'] == 'IntelleChartPRO (ICP)')
print("\nICP Data Domains:")
icp_domain_map = {
    'Appointments': ['Appointments (JSON)'],
    'Chart Notes': ['ChartNote (PDF)'],
    'Communications': ['Communications (PDF)', 'Internal Communication (JSON)', 'Secure Messages (JSON)'],
    'Demographics': ['Patient Demographics (JSON)'],
    'Documents/Images': ['Documents (TXT)', 'Images (TXT)'],
    'Insurance': ['Insurance & Auth (JSON)'],
    'Laboratory': ['Laboratory (JSON)'],
    'Procedures': ['Procedures (JSON)'],
    'Referrals': ['Referrals (JSON)'],
    'Ophthalmology': ['Glaucoma Flowsheet (JSON)', 'Refractions (JSON)', 'Retina Injection Log (JSON)', 'Shared Care Comments (JSON)'],
    'Medications': ['Specialty Medications'],
    'Tasks': ['Patient Tasks', 'Tasking_Microservice (JSON_CSV)'],
}

entities_by_name_icp = {e['entity_name']: e for e in icp['entities']}
for domain, enames in icp_domain_map.items():
    total_f = sum(entities_by_name_icp.get(en, {}).get('field_count', 0) for en in enames)
    total_d = sum(entities_by_name_icp.get(en, {}).get('fields_with_descriptions', 0) for en in enames)
    count = len([en for en in enames if en in entities_by_name_icp])
    print(f"  {domain}: {count} entities, {total_f} fields ({total_d} described)")

if __name__ == "__main__":
    pass
