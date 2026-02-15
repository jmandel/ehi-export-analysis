"""
Categorize GEHRIMED EHI export tables by domain and generate a domain summary.
"""

import json

INPUT_FILE = "/home/jmandel/hobby/ehi-export-analysis/abstraction/netsmart-technologies--gehrimed/analysis/full-entity-inventory.json"
OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/netsmart-technologies--gehrimed/analysis"

# Domain categorization based on table names and their documented descriptions
DOMAIN_MAP = {
    "Demographics": ["Patientinfo", "HL7_Patient", "Patient_Relationships"],
    "Encounters / Clinical Notes": ["Dictations", "Dictation_Items", "Dictation_Roles", "Dictation_ICD"],
    "Problems / Diagnoses": ["Patient_ProblemList"],
    "Medications": ["Patient_Medications"],
    "Allergies": ["Patient_MedicationAllergy"],
    "Immunizations": ["Patient_Immunizations", "Patient_ImmunizationDetails"],
    "Vitals": ["Patient_Vitals"],
    "Lab Results": ["LabOrder", "LabResult", "LabSpecimen", "Patient_Labs"],
    "Imaging / Diagnostic Reports": ["Patient_Imaging"],
    "Procedures": ["Patient_Procedures"],
    "Assessments": ["Patient_Assessments"],
    "Patient History": ["Patient_History"],
    "Insurance / Coverage": ["HL7_PatientInsurance"],
    "Implantable Devices": ["PatientImplantableDevice"],
    "Smoking Status": ["Patientinfo_Smoking", "SmokingCessation", "SmokingStatus"],
    "Documents / Attachments": ["Attachments", "Document"],
    "Scheduling": ["Patient_Schedule"],
    "User / Provider Info": ["aspnet_Users"],
    "Organization / Facility": ["Companyinfo", "groups"],
    "Reference Data": ["EnumTypes", "EnumValues"],
    "Interfaces / Integration": ["Interfaces", "Interfaces_Outbound"],
}

def main():
    with open(INPUT_FILE) as f:
        tables = json.load(f)
    
    table_lookup = {t['name']: t for t in tables}
    
    print("=== GEHRIMED EHI Export: Domain Categorization ===\n")
    print(f"{'Domain':<35} {'Tables':>6} {'Fields':>6}")
    print("-" * 55)
    
    total_t = 0
    total_f = 0
    categorized = set()
    
    results = []
    for domain, table_names in DOMAIN_MAP.items():
        n_tables = 0
        n_fields = 0
        for tn in table_names:
            if tn in table_lookup:
                n_tables += 1
                n_fields += len(table_lookup[tn]['columns'])
                categorized.add(tn)
        results.append((domain, n_tables, n_fields, table_names))
        total_t += n_tables
        total_f += n_fields
        print(f"{domain:<35} {n_tables:>6} {n_fields:>6}")
    
    print(f"{'-'*55}")
    print(f"{'TOTAL':<35} {total_t:>6} {total_f:>6}")
    
    # Check for uncategorized
    uncategorized = [t['name'] for t in tables if t['name'] not in categorized]
    if uncategorized:
        print(f"\nUncategorized tables: {uncategorized}")
    
    # Save results
    with open(f"{OUTPUT_DIR}/domain-summary.json", 'w') as f:
        json.dump({
            "domains": [
                {
                    "domain": r[0],
                    "table_count": r[1],
                    "field_count": r[2],
                    "tables": r[3]
                }
                for r in results
            ],
            "total_tables": total_t,
            "total_fields": total_f,
            "uncategorized": uncategorized
        }, f, indent=2)
    
    print(f"\nDomain summary saved to {OUTPUT_DIR}/domain-summary.json")

if __name__ == '__main__':
    main()
