#!/usr/bin/env python3
"""
Parse the eMedicalPractice EHI data dictionary from the WordPress API JSON
and produce entity-inventory-full.json and entity-inventory-summary.json.

Reads: downloads/ehi-data-dictionary-tables-api.json
       downloads/ehi-export-page-api.json
Outputs: analysis/entity-inventory-full.json
         analysis/entity-inventory-summary.json
"""

import json
import re
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).parent.parent

# --- Parse data dictionary tables ---

with open(BASE / "downloads/ehi-data-dictionary-tables-api.json") as f:
    api_data = json.load(f)

content = api_data[0]["content"]["rendered"] if isinstance(api_data, list) else api_data["content"]["rendered"]

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_row = []
        self.current_cell = ""
        self.in_td = False
        self.headers = []
        self.headings_before = []  # Track h3/h4 headings seen
        self.current_heading = ""
        self.in_heading = False
        self.table_names = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3", "h4"):
            self.in_heading = True
            self.current_heading = ""
        elif tag == "table":
            self.current_table = []
            self.headers = []
            self.table_names.append(self.current_heading)
        elif tag in ("td", "th"):
            self.in_td = True
            self.current_cell = ""

    def handle_endtag(self, tag):
        if tag in ("h2", "h3", "h4"):
            self.in_heading = False
        elif tag in ("td", "th"):
            self.in_td = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "tr":
            if self.current_row:
                if not self.headers:
                    self.headers = self.current_row[:]
                else:
                    self.current_table.append(dict(zip(self.headers, self.current_row)))
            self.current_row = []
        elif tag == "table":
            if self.current_table:
                self.tables.append({
                    "name": self.table_names[-1] if self.table_names else f"Table_{len(self.tables)}",
                    "rows": self.current_table,
                    "headers": self.headers,
                })

    def handle_data(self, data):
        if self.in_td:
            self.current_cell += data
        if self.in_heading:
            self.current_heading += data.strip()

parser = TableParser()
parser.feed(content)

# Deduplicate tables (HTML has each table twice due to responsive layout)
seen = set()
unique_tables = []
for t in parser.tables:
    key = (t["name"], len(t["rows"]))
    if key not in seen:
        seen.add(key)
        unique_tables.append(t)

# --- Parse export page for section descriptions ---

with open(BASE / "downloads/ehi-export-page-api.json") as f:
    export_api = json.load(f)

export_content = export_api["content"]["rendered"] if isinstance(export_api, dict) else export_api[0]["content"]["rendered"]

# Extract commented-out sections
comments = re.findall(r"<!--(.*?)-->", export_content, re.DOTALL)
has_documents_section = any("Documents" in c for c in comments)

# --- Build entity inventory ---

def _get_category(name):
    name_lower = name.lower()
    if "patient" in name_lower:
        return "Demographics"
    elif "insurance" in name_lower:
        return "Insurance"
    elif "appointment" in name_lower:
        return "Appointments"
    return "Other"

entities = []
total_fields = 0

for table in unique_tables:
    fields = []
    for row in table["rows"]:
        field = {
            "name": row.get("Column Name", ""),
            "dataType": row.get("Data Types", ""),
            "defaultValue": row.get("Default", "") or None,
            "notNull": row.get("Not Null", "") == "Not Null",
            "description": None,  # No descriptions provided
        }
        fields.append(field)

    entity = {
        "entityName": table["name"],
        "fieldCount": len(fields),
        "fields": fields,
        "category": _get_category(table["name"]),
        "hasDescriptions": False,
        "hasTypes": True,
    }
    entities.append(entity)
    total_fields += len(fields)

def _get_category(name):
    name_lower = name.lower()
    if "patient" in name_lower:
        return "Demographics"
    elif "insurance" in name_lower:
        return "Insurance"
    elif "appointment" in name_lower:
        return "Appointments"
    return "Other"

# Re-run category assignment
for e in entities:
    e["category"] = _get_category(e["entityName"])

# --- Build full inventory ---

inventory = {
    "product": "eMedicalPractice",
    "vendor": "eMedPractice LLC",
    "source": "https://emedpractice.com/electronic-health-information-data-dictionary-tables/",
    "exportComponents": [
        {
            "name": "Clinical Data (C-CDA)",
            "format": "XML (C-CDA)",
            "description": "Encounter-level and consolidated CDA documents organized by chart number. Claims to include USCDI v3 data elements plus other EHI.",
            "dataDictionary": False,
            "fieldLevelDetail": False,
        },
        {
            "name": "Patient Details CSV",
            "format": "CSV",
            "description": "Demographics, insurance, and appointment data. Data dictionary with 3 tables, 61 fields.",
            "dataDictionary": True,
            "fieldLevelDetail": True,
        },
        {
            "name": "Documents (commented out in HTML)",
            "format": "PDF, JPG, PNG",
            "description": "Signed progress notes, lab results, radiology reports, scanned documents. Section 4 is commented out in the page HTML, suggesting it may not be active.",
            "dataDictionary": False,
            "fieldLevelDetail": False,
        },
    ],
    "dataDictionary": {
        "totalEntities": len(entities),
        "totalFields": total_fields,
        "fieldsWithDescriptions": 0,
        "fieldsWithTypes": total_fields,
        "fieldsWithNullability": total_fields,
        "fieldsWithDefaultValues": 0,
        "descriptionCoverage": "0%",
    },
    "entities": entities,
}

# Write full inventory
out_dir = BASE / "analysis"
out_dir.mkdir(exist_ok=True)

with open(out_dir / "entity-inventory-full.json", "w") as f:
    json.dump(inventory, f, indent=2)

# --- Build summary ---

summary = {
    "product": inventory["product"],
    "vendor": inventory["vendor"],
    "totalEntities": len(entities),
    "totalFields": total_fields,
    "fieldsWithDescriptions": 0,
    "descriptionCoverage": "0%",
    "fieldsWithTypes": total_fields,
    "typeCoverage": "100%",
    "exportComponents": len(inventory["exportComponents"]),
    "categorySummary": {},
    "entitySummary": [],
}

for e in entities:
    cat = e["category"]
    if cat not in summary["categorySummary"]:
        summary["categorySummary"][cat] = {"entityCount": 0, "fieldCount": 0}
    summary["categorySummary"][cat]["entityCount"] += 1
    summary["categorySummary"][cat]["fieldCount"] += e["fieldCount"]
    summary["entitySummary"].append({
        "entityName": e["entityName"],
        "fieldCount": e["fieldCount"],
        "category": e["category"],
        "hasDescriptions": e["hasDescriptions"],
    })

with open(out_dir / "entity-inventory-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

# Print summary
print(f"Entities: {len(entities)}")
print(f"Total fields: {total_fields}")
print(f"Fields with descriptions: 0 (0%)")
print(f"Fields with types: {total_fields} (100%)")
print(f"Export components: {len(inventory['exportComponents'])}")
print(f"\nCategory breakdown:")
for cat, data in summary["categorySummary"].items():
    print(f"  {cat}: {data['entityCount']} entities, {data['fieldCount']} fields")
print(f"\nEntities:")
for e in summary["entitySummary"]:
    print(f"  {e['entityName']}: {e['fieldCount']} fields")
print(f"\nDocuments section commented out: {has_documents_section}")
