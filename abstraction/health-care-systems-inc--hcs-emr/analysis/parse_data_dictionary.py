#!/usr/bin/env python3
"""Parse HCS Data Dictionary CSV and produce detailed statistics."""

import csv
import json
import re
from collections import defaultdict

CSV_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/health-care-systems-inc--hcs-emr/downloads/HCSDataDictionary.csv"
OUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/health-care-systems-inc--hcs-emr/analysis"

tables = {}  # table_name -> {description, columns: [{name, type, size, description}]}
current_table = None

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # Table,Column,Type,Size,Description
    
    for row in reader:
        if len(row) < 5:
            # Blank or short row — skip
            continue
        
        table, column, dtype, size, desc = row[0], row[1], row[2], row[3], row[4]
        
        if table and not column and not dtype and not size:
            # Table header row
            current_table = table
            tables[current_table] = {"description": desc, "columns": []}
        elif table and column:
            # Column row
            if table not in tables:
                tables[table] = {"description": "", "columns": []}
                current_table = table
            tables[table]["columns"].append({
                "name": column,
                "type": dtype,
                "size": size,
                "description": desc
            })

# Compute statistics
total_tables = len(tables)
total_fields = sum(len(t["columns"]) for t in tables.values())
fields_with_desc = sum(
    1 for t in tables.values() 
    for c in t["columns"] 
    if c["description"] and c["description"].strip()
)
fields_with_types = sum(
    1 for t in tables.values() 
    for c in t["columns"] 
    if c["type"] and c["type"].strip()
)

# FK references
fk_pattern = re.compile(r'Reference to (\w+)', re.IGNORECASE)
fk_count = 0
fk_targets = set()
for t in tables.values():
    for c in t["columns"]:
        m = fk_pattern.search(c["description"])
        if m:
            fk_count += 1
            fk_targets.add(m.group(1))

# Data type distribution
type_dist = defaultdict(int)
for t in tables.values():
    for c in t["columns"]:
        dtype = c["type"].strip().lower() if c["type"] else "(none)"
        type_dist[dtype] += 1

# Description quality: how many are just the column name restated?
trivial_desc_count = 0
meaningful_desc_count = 0
for t in tables.values():
    for c in t["columns"]:
        desc = c["description"].strip() if c["description"] else ""
        name = c["name"].strip() if c["name"] else ""
        if not desc:
            continue
        # Check if description is just the column name with spaces inserted
        # e.g., "RowVersionNumber" -> "Row Version Number"
        name_spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        name_spaced2 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', name_spaced)
        if desc.lower() == name_spaced2.lower() or desc.lower() == name.lower():
            trivial_desc_count += 1
        elif fk_pattern.search(desc):
            # FK reference descriptions
            pass  # Count separately
        else:
            meaningful_desc_count += 1

# Tables sorted by column count
table_sizes = [(name, len(t["columns"])) for name, t in tables.items()]
table_sizes.sort(key=lambda x: -x[1])

# Categorize tables by domain based on naming patterns
domain_patterns = {
    "Patient Demographics": ["Patient$", "PatientAddress", "PatientAlias", "PatientContact", 
                              "PatientIdentifier", "PatientRace", "PatientLanguage"],
    "Encounters/Visits": ["PatientVisit", "VisitTransfer", "VisitServiceLevel", "VisitCareLevel",
                           "VisitFlag", "VisitTeam"],
    "Diagnoses/Problems": ["VisitDiagnosis", "VisitProblem", "VisitProspectiveProblem", 
                            "Condition", "ConditionCode"],
    "Medications/Orders": ["PatientOrder", "OrderComponent", "OrderDetail", "OrderField",
                            "OrderSIG", "OrderObservation", "OrderMedication", "OrderStaff",
                            "HCS_MedList", "MedRecItem", "MedRecPrescription"],
    "Medication Admin (MAR)": ["TherapyAdmin", "AdminProduct", "AdminVolume", "AdminComponent",
                                "AdminField", "AdminObservation"],
    "Pharmacy/Drug Products": ["DispensableProduct", "RoutedProduct", "PackagedProduct", 
                                "NamedProduct", "ProductComponent", "DispenseBatch",
                                "AlternativeProduct", "DrugInteraction"],
    "PBM/Formulary": ["PBM"],
    "Allergies": ["PatientAllergy", "AllergyProduct"],
    "Observations/Vitals/Labs": ["Observation$", "ObservationGroup", "ObservationGroupItem",
                                  "VisitObservation", "VisitObservationSet"],
    "Clinical Notes/Documents": ["PatientDocument", "VisitDocument", "VisitNote", 
                                  "ConsentDocument"],
    "Billing/Charges": ["VisitCharge", "ChargeClaim", "ClaimObservation", "ChargeCode",
                         "PatientClaimResponse"],
    "Insurance/Coverage": ["PatientInsuranceCoverage", "InsuranceCompany", "InsuranceContract",
                            "VisitInsuranceCoverage", "VisitInsuranceAuthorization",
                            "VisitEligibilityQuery"],
    "Payments": ["Payment$", "CopayProduct", "CopaySummary"],
    "Care Plans/Treatment": ["VisitIntervention", "VisitCarePlan", "VisitConcern", 
                              "ConcernItem", "InterventionTemplate"],
    "Consent": ["PatientConsent", "VisitConsent"],
    "Immunizations": ["VisitImmunizationQuery", "ImmunizationQuery"],
    "Patient Devices": ["PatientDevice", "DeviceIdentifier"],
    "Safety/Location": ["VisitPhysicalLocation", "NearMiss", "ClinicalAlert"],
    "Staff/Providers": ["Staff$", "StaffPractitionerID", "StaffSpecialty", "StaffIDCode",
                         "StaffAuthorization"],
    "Scheduling/Events": ["Event$", "EventOccurrence", "EventItem", "CalendarDay"],
    "Facilities/Locations": ["Facility", "Unit$", "UnitBed", "Location"],
    "Messaging": ["Chat$", "ChatMessage", "ChatParticipant"],
    "Public Health Reporting": ["AUBatch", "AUBatchReport", "SyndromicSurveillance",
                                 "CaseReport"],
    "Authorization/Roles": ["AuthorizationRole", "AuthorizationAction", "AuthorizationAreaAction",
                             "RoleAuthorizationArea"],
    "Images": ["NamedImage"],
    "Family History": ["PatientFamilyHistoryItem"],
    "Procedures": ["VisitProcedure"],
    "Discharge/Instructions": ["VisitInstruction"],
    "Work Tasks": ["WorkTask"],
}

# Assign tables to domains
table_domain_map = {}
for domain, patterns in domain_patterns.items():
    for tname in tables:
        for pat in patterns:
            if re.match(pat, tname):
                table_domain_map[tname] = domain
                break

# Unassigned tables
unassigned = [t for t in tables if t not in table_domain_map]

# Domain summary
domain_summary = defaultdict(lambda: {"tables": [], "total_fields": 0})
for tname, domain in table_domain_map.items():
    domain_summary[domain]["tables"].append(tname)
    domain_summary[domain]["total_fields"] += len(tables[tname]["columns"])

# Print results
print("=" * 70)
print("HCS DATA DICTIONARY ANALYSIS")
print("=" * 70)
print(f"\nTotal tables: {total_tables}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: {fields_with_desc} ({fields_with_desc*100//total_fields}%)")
print(f"Fields with types: {fields_with_types} ({fields_with_types*100//total_fields}%)")
print(f"FK references: {fk_count}")
print(f"Distinct FK targets: {len(fk_targets)}")
print(f"Trivial descriptions (just column name re-spaced): {trivial_desc_count}")
print(f"FK reference descriptions: {fk_count}")
print(f"Meaningful descriptions (beyond name/FK): {meaningful_desc_count}")

print(f"\n--- Data Type Distribution ---")
for dtype, count in sorted(type_dist.items(), key=lambda x: -x[1]):
    print(f"  {dtype:20s} {count:5d}")

print(f"\n--- Top 25 Tables by Column Count ---")
for name, count in table_sizes[:25]:
    desc = tables[name]["description"][:60] if tables[name]["description"] else ""
    print(f"  {name:45s} {count:4d} cols  {desc}")

print(f"\n--- Domain Summary ---")
for domain in sorted(domain_summary.keys()):
    info = domain_summary[domain]
    tnames = ", ".join(sorted(info["tables"]))
    print(f"  {domain:35s} {len(info['tables']):3d} tables  {info['total_fields']:5d} fields")

print(f"\n--- Unassigned Tables ({len(unassigned)}) ---")
for t in sorted(unassigned):
    desc = tables[t]["description"][:70] if tables[t]["description"] else ""
    cols = len(tables[t]["columns"])
    print(f"  {t:45s} {cols:4d} cols  {desc}")

# Save full inventory as JSON
inventory = []
for tname in sorted(tables.keys()):
    t = tables[tname]
    domain = table_domain_map.get(tname, "Unassigned")
    fk_refs = []
    for c in t["columns"]:
        m = fk_pattern.search(c["description"])
        if m:
            fk_refs.append({"column": c["name"], "references": m.group(1)})
    inventory.append({
        "table": tname,
        "description": t["description"],
        "domain": domain,
        "column_count": len(t["columns"]),
        "columns": t["columns"],
        "foreign_keys": fk_refs
    })

with open(f"{OUT_DIR}/full-entity-inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

# Save summary stats as JSON
stats = {
    "total_tables": total_tables,
    "total_fields": total_fields,
    "fields_with_descriptions": fields_with_desc,
    "fields_with_types": fields_with_types,
    "description_percentage": round(fields_with_desc * 100 / total_fields, 1),
    "fk_references": fk_count,
    "distinct_fk_targets": len(fk_targets),
    "trivial_descriptions": trivial_desc_count,
    "meaningful_descriptions": meaningful_desc_count,
    "type_distribution": dict(sorted(type_dist.items(), key=lambda x: -x[1])),
    "top_25_tables": [{"table": n, "columns": c} for n, c in table_sizes[:25]],
    "domain_summary": {
        d: {"table_count": len(v["tables"]), "field_count": v["total_fields"], "tables": sorted(v["tables"])}
        for d, v in sorted(domain_summary.items())
    },
    "unassigned_tables": sorted(unassigned)
}

with open(f"{OUT_DIR}/summary-stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print(f"\n\nSaved full-entity-inventory.json and summary-stats.json to {OUT_DIR}")
