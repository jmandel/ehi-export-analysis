#!/usr/bin/env python3
"""Parse all StructureDefinitions from the FHIR IG package and CSV schemas from HTML pages."""

import json
import os
import glob
from html.parser import HTMLParser

PACKAGE_DIR = "package_extract/package"
DOWNLOADS_DIR = "../downloads"

def parse_structure_definition(filepath):
    with open(filepath) as f:
        sd = json.load(f)
    name = sd.get("name", "")
    sd_type = sd.get("type", "")
    kind = sd.get("kind", "")
    description = sd.get("description", "")
    base = sd.get("baseDefinition", "")
    elements = sd.get("snapshot", {}).get("element", [])
    
    fields = []
    for elem in elements:
        path = elem.get("path", "")
        short = elem.get("short", "")
        definition = elem.get("definition", "")
        min_val = elem.get("min", None)
        max_val = elem.get("max", "")
        types = [t.get("code", "") for t in elem.get("type", []) if t.get("code")]
        binding = elem.get("binding", {})
        if path == sd_type and "." not in path:
            continue
        fields.append({
            "path": path, "short": short, "definition": definition,
            "min": min_val, "max": max_val, "types": types,
            "has_description": bool(short or definition), "has_type": bool(types),
            "binding_value_set": binding.get("valueSet", ""),
            "binding_strength": binding.get("strength", ""),
        })
    
    custom = {"Authorization","BillingStatement","CareProfile","Census","Claim","InvoiceTransaction","Order","Payment"}
    uscdi = {"AllergyIntolerance","CarePlan","CareTeam","Condition","Coverage","DiagnosticReport",
             "DocumentReference","Encounter","FamilyMemberHistory","Goal","Immunization","Location",
             "Medication","MedicationDispense","MedicationRequest","Observation","Organization",
             "Patient","Practitioner","PractitionerRole","Procedure","Provenance","RelatedPerson",
             "ServiceRequest","Specimen"}
    
    if kind == "complex-type": category = "Extension"
    elif sd_type in custom: category = "Custom Resource (Beyond USCDI)"
    elif sd_type in uscdi: category = "FHIR Resource Profile (USCDI-aligned)"
    else: category = "Other Resource"
    
    direct = [f for f in fields if f["path"].count(".") == 1]
    return {
        "name": name, "fhir_type": sd_type, "kind": kind, "description": description,
        "base_definition": base, "category": category,
        "total_elements": len(fields), "direct_fields": len(direct),
        "fields_with_description": sum(1 for f in fields if f["has_description"]),
        "fields_with_type": sum(1 for f in fields if f["has_type"]),
        "fields": fields,
    }

class DetailedTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables = []
        self.cur_table = None
        self.cur_row = None
        self.cur_cell = ''
        self.in_cell = False
        self.in_thead = False
        self.tag_stack = []
        self.h_before = []
        self.cur_h = ''
        self.in_h = False
    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        if tag == 'table':
            self.cur_table = {'header':[], 'rows':[], 'section': self.h_before[-1] if self.h_before else ''}
        elif tag == 'thead': self.in_thead = True
        elif tag == 'tr': self.cur_row = []
        elif tag in ('td','th'):
            self.cur_cell = ''
            self.in_cell = True
        elif tag in ('h2','h3','h4'):
            self.in_h = True
            self.cur_h = ''
    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag: self.tag_stack.pop()
        if tag in ('td','th'):
            self.in_cell = False
            if self.cur_row is not None: self.cur_row.append(self.cur_cell.strip())
        elif tag == 'tr':
            if self.cur_row is not None and self.cur_table is not None:
                if self.in_thead or (not self.cur_table['header'] and self.cur_row):
                    self.cur_table['header'] = self.cur_row
                else:
                    self.cur_table['rows'].append(self.cur_row)
            self.cur_row = None
        elif tag == 'thead': self.in_thead = False
        elif tag == 'table':
            if self.cur_table and (self.cur_table['rows'] or self.cur_table['header']):
                self.tables.append(self.cur_table)
            self.cur_table = None
        elif tag in ('h2','h3','h4') and self.in_h:
            self.in_h = False
            self.h_before.append(self.cur_h.strip())
    def handle_data(self, d):
        if self.in_cell: self.cur_cell += d
        if self.in_h: self.cur_h += d

def parse_csv_schemas(html_file, source_label):
    with open(html_file) as f:
        html = f.read()
    p = DetailedTableParser()
    p.feed(html)
    file_descriptions = {}
    csv_schemas = []
    for table in p.tables:
        hl = [h.lower() for h in table['header']]
        if 'file' in hl and 'description' in hl:
            fi, di = hl.index('file'), hl.index('description')
            for row in table['rows']:
                if len(row) > max(fi,di): file_descriptions[row[fi]] = row[di]
        elif 'column' in hl:
            ci = hl.index('column')
            ti = hl.index('type') if 'type' in hl else -1
            ni = hl.index('nullable') if 'nullable' in hl else -1
            di = hl.index('description') if 'description' in hl else -1
            section = table['section']
            columns = []
            for row in table['rows']:
                if len(row) <= ci: continue
                col = {
                    "name": row[ci] if ci<len(row) else "",
                    "type": row[ti] if ti>=0 and ti<len(row) else "",
                    "nullable": row[ni].lower()=="yes" if ni>=0 and ni<len(row) else None,
                    "description": row[di] if di>=0 and di<len(row) else "",
                }
                col["has_description"] = bool(col["description"])
                col["has_type"] = bool(col["type"])
                if col["name"]: columns.append(col)
            if columns:
                file_desc = file_descriptions.get(section, "")
                csv_schemas.append({
                    "name": f"{source_label}: {section}",
                    "file_name": section, "file_description": file_desc,
                    "fhir_type": "CSV", "kind": "csv-schema",
                    "description": file_desc or f"CSV export from {source_label}",
                    "base_definition": "", "category": f"CSV Assessment Export ({source_label})",
                    "total_elements": len(columns), "direct_fields": len(columns),
                    "fields_with_description": sum(1 for c in columns if c["has_description"]),
                    "fields_with_type": sum(1 for c in columns if c["has_type"]),
                    "fields": [{
                        "path": c["name"], "short": c["description"], "definition": c["description"],
                        "min": 0 if c.get("nullable") else 1, "max": "1",
                        "types": [c["type"]] if c["type"] else [],
                        "has_description": c["has_description"], "has_type": c["has_type"],
                        "binding_value_set": "", "binding_strength": "",
                    } for c in columns],
                })
    return csv_schemas

def main():
    sd_files = sorted(glob.glob(os.path.join(PACKAGE_DIR, "StructureDefinition-*.json")))
    resources, extensions = [], []
    for fp in sd_files:
        e = parse_structure_definition(fp)
        (resources if e["kind"]=="resource" else extensions).append(e)
    
    csv_entities = []
    for hf, sl in [(os.path.join(DOWNLOADS_DIR,"site","MDS.html"),"MDS"),
                    (os.path.join(DOWNLOADS_DIR,"site","NonMDS.html"),"Non-MDS")]:
        if os.path.exists(hf): csv_entities.extend(parse_csv_schemas(hf, sl))
    
    all_combined = resources + csv_entities
    
    inventory = {
        "extraction_date": "2026-02-16",
        "source": "PointClickCare EHI Export FHIR IG v0.1.0 + CSV Assessment Schemas",
        "fhir_version": "4.0.1",
        "entities": all_combined,
        "extensions": [{"name":e["name"],"fhir_type":e["fhir_type"],
                        "description":e["description"][:300],"total_elements":e["total_elements"],
                        "fields":e["fields"]} for e in extensions],
    }
    with open("entity-inventory-full.json","w") as f: json.dump(inventory, f, indent=2)
    
    total_fields = sum(e["total_elements"] for e in all_combined)
    fields_desc = sum(e["fields_with_description"] for e in all_combined)
    fields_type = sum(e["fields_with_type"] for e in all_combined)
    cats = {}
    for e in all_combined:
        c = e["category"]
        if c not in cats: cats[c] = {"count":0,"total_fields":0,"fields_with_desc":0,"entities":[]}
        cats[c]["count"] += 1
        cats[c]["total_fields"] += e["total_elements"]
        cats[c]["fields_with_desc"] += e["fields_with_description"]
        cats[c]["entities"].append(e["name"])
    
    summary = {
        "extraction_date": "2026-02-16",
        "total_resource_profiles": len(resources),
        "total_extensions": len(extensions),
        "total_csv_schemas": len(csv_entities),
        "total_entities": len(all_combined),
        "total_fields_all_entities": total_fields,
        "fields_with_description": fields_desc,
        "fields_with_type": fields_type,
        "description_percentage": round(fields_desc/total_fields*100,1) if total_fields else 0,
        "categories": cats,
        "resource_profiles": [{"name":e["name"],"fhir_type":e["fhir_type"],"category":e["category"],
                               "total_elements":e["total_elements"],"direct_fields":e["direct_fields"],
                               "fields_with_description":e["fields_with_description"],
                               "description":e["description"][:200]} for e in all_combined],
        "extensions_list": [{"name":e["name"],"description":e["description"][:200]} for e in extensions],
    }
    with open("entity-inventory-summary.json","w") as f: json.dump(summary, f, indent=2)
    
    print(f"=== PointClickCare EHI Export Inventory ===")
    print(f"FHIR Resource Profiles: {len(resources)}")
    print(f"  Custom (Beyond USCDI): {sum(1 for r in resources if 'Custom' in r['category'])}")
    print(f"  USCDI-aligned: {sum(1 for r in resources if 'USCDI' in r['category'])}")
    print(f"  Other: {sum(1 for r in resources if r['category']=='Other Resource')}")
    print(f"FHIR Extensions: {len(extensions)}")
    print(f"CSV Schemas: {len(csv_entities)} ({sum(e['total_elements'] for e in csv_entities)} columns)")
    print(f"Total Entities: {len(all_combined)}")
    print(f"Total Fields: {total_fields}")
    print(f"Fields with Description: {fields_desc} ({round(fields_desc/total_fields*100,1)}%)")
    print(f"Fields with Type: {fields_type} ({round(fields_type/total_fields*100,1)}%)")
    print()
    for cat, d in sorted(cats.items()):
        print(f"  {cat}: {d['count']} entities, {d['total_fields']} fields")
    print()
    for e in sorted(all_combined, key=lambda x: x["total_elements"], reverse=True):
        m = "★" if "Custom" in e["category"] else "◆" if "CSV" in e["category"] else " "
        print(f" {m} {e['name']:55s} {e['total_elements']:4d} fields  {e['category']}")

if __name__ == "__main__":
    main()
