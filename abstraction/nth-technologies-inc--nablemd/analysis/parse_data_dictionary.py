"""Parse all CSV data dictionary files from the nAbleMD EHI export and produce
an inventory of entities, fields, and documentation quality metrics."""

import csv
import json
import os
import sys

CSV_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/nth-technologies-inc--nablemd/downloads/csv-sheets"
SKIP_FILES = {"read_me.csv", "table_of_contents.csv", "revision_history.csv"}

entities = []
total_fields = 0
total_described = 0

for fname in sorted(os.listdir(CSV_DIR)):
    if fname in SKIP_FILES or not fname.endswith(".csv"):
        continue

    filepath = os.path.join(CSV_DIR, fname)
    entity_name = fname.replace(".csv", "")

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # Parse the structure: first rows may be table description, then FieldName/Description header
    table_desc = ""
    fields = []
    header_idx = None

    for i, row in enumerate(rows):
        if len(row) >= 2 and row[0].strip().lower() == "fieldname":
            header_idx = i
            break
        if len(row) >= 1 and row[0].strip() == "Table Description":
            # Next row should be the description
            if i + 1 < len(rows) and rows[i + 1]:
                table_desc = rows[i + 1][0].strip() if rows[i + 1] else ""

    if header_idx is not None:
        for row in rows[header_idx + 1:]:
            if len(row) >= 2:
                field_name = row[0].strip()
                field_desc = row[1].strip() if len(row) > 1 else ""
                if field_name:  # Skip empty rows
                    fields.append({
                        "name": field_name,
                        "description": field_desc,
                        "has_description": bool(field_desc)
                    })

    n_fields = len(fields)
    n_described = sum(1 for f in fields if f["has_description"])
    total_fields += n_fields
    total_described += n_described

    entities.append({
        "entity": entity_name,
        "file": fname,
        "table_description": table_desc,
        "has_table_description": bool(table_desc),
        "field_count": n_fields,
        "fields_with_descriptions": n_described,
        "description_pct": round(n_described / n_fields * 100, 1) if n_fields > 0 else 0,
        "fields": fields
    })

# Category assignment based on naming patterns
def categorize(name):
    n = name.lower()
    if any(x in n for x in ["ivf", "oocyte", "cycle", "semen", "follicular", "culture", "cryo", "donor", "embryo", "transfer", "disclosureinfo", "infertility"]):
        return "IVF/Fertility"
    if any(x in n for x in ["obgyn", "obhistory", "obstetric", "pregnancy", "contraception", "multibirth", "estimatedduedate", "obultrasound"]):
        return "OB/GYN"
    if any(x in n for x in ["ledger", "payment", "prepayment", "procedurecharge", "insurance", "priorauth", "visitpayment"]):
        return "Billing/Financial"
    if any(x in n for x in ["patient", "relative", "kiosk"]):
        return "Patient/Demographics"
    if any(x in n for x in ["visit", "appointment", "waitlist", "action", "task", "dailyworklist"]):
        return "Scheduling/Workflow"
    if any(x in n for x in ["immunization"]):
        return "Immunizations"
    if any(x in n for x in ["newcrop", "drug", "allergy"]):
        return "Medications/Allergies"
    if any(x in n for x in ["laborder", "measurement"]):
        return "Labs/Results"
    if any(x in n for x in ["document", "chartnote", "cosign", "chart"]):
        return "Documents/Notes"
    if any(x in n for x in ["patmail", "smsnavi", "patientrequest"]):
        return "Communications"
    if any(x in n for x in ["consent"]):
        return "Consent"
    if any(x in n for x in ["emrproblem", "emrvisitproblem", "emrhealthconcern"]):
        return "Problems/Conditions"
    if any(x in n for x in ["emrplan", "emrwellness"]):
        return "Care Plans"
    if any(x in n for x in ["emrreviews", "emrhpi", "emrassessment", "emranswer", "emrmedical", "emrsurg", "emrencounter", "emrnotes", "emrchecklist", "emrchiefcomplaint", "emrdvtrisk", "emrrestrict", "emrbiological"]):
        return "Clinical/EMR"
    if any(x in n for x in ["survey"]):
        return "Surveys"
    if any(x in n for x in ["procedure"]):
        return "Procedures"
    if any(x in n for x in ["ivfquote"]):
        return "IVF/Fertility"
    return "Other"

for e in entities:
    e["category"] = categorize(e["entity"])

# Summary stats
categories = {}
for e in entities:
    cat = e["category"]
    if cat not in categories:
        categories[cat] = {"entity_count": 0, "field_count": 0, "described_count": 0}
    categories[cat]["entity_count"] += 1
    categories[cat]["field_count"] += e["field_count"]
    categories[cat]["described_count"] += e["fields_with_descriptions"]

# Output
output = {
    "summary": {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "total_described": total_described,
        "description_pct": round(total_described / total_fields * 100, 1) if total_fields > 0 else 0,
    },
    "categories": {k: v for k, v in sorted(categories.items())},
    "entities": entities
}

# Save full inventory (without individual fields for readability)
inventory = [{k: v for k, v in e.items() if k != "fields"} for e in entities]
with open(os.path.join(os.path.dirname(__file__), "full-entity-inventory.json"), "w") as f:
    json.dump(inventory, f, indent=2)

# Save summary
with open(os.path.join(os.path.dirname(__file__), "summary-stats.json"), "w") as f:
    json.dump({"summary": output["summary"], "categories": output["categories"]}, f, indent=2)

# Print summary
print(f"\n=== nAbleMD Data Dictionary Summary ===")
print(f"Total entities: {output['summary']['total_entities']}")
print(f"Total fields: {output['summary']['total_fields']}")
print(f"Fields with descriptions: {output['summary']['total_described']} ({output['summary']['description_pct']}%)")
print(f"\n--- By Category ---")
for cat, stats in sorted(categories.items()):
    desc_pct = round(stats["described_count"] / stats["field_count"] * 100, 1) if stats["field_count"] > 0 else 0
    print(f"  {cat}: {stats['entity_count']} entities, {stats['field_count']} fields, {stats['described_count']} described ({desc_pct}%)")
print(f"\n--- Top 20 Entities by Field Count ---")
sorted_entities = sorted(entities, key=lambda e: e["field_count"], reverse=True)
for e in sorted_entities[:20]:
    print(f"  {e['entity']:40s} {e['field_count']:4d} fields, {e['fields_with_descriptions']:4d} described ({e['description_pct']:5.1f}%), [{e['category']}]")
print(f"\n--- Entities with <100% description rate ---")
for e in sorted_entities:
    if e["description_pct"] < 100 and e["field_count"] > 0:
        print(f"  {e['entity']:40s} {e['fields_with_descriptions']}/{e['field_count']} described ({e['description_pct']}%)")

