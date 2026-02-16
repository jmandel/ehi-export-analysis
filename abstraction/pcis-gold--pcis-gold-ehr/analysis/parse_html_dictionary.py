#!/usr/bin/env python3
"""Parse the PCIS GOLD EHI Export HTML data dictionary independently.
Produces full-entity-inventory.json and summary statistics."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HTML_PATH = Path("/home/jmandel/hobby/ehi-export-analysis/results/pcis-gold--pcis-gold-ehr/downloads/ehi-export-data-table-definitions.html")
OUTPUT_DIR = Path(__file__).parent

class TableParser(HTMLParser):
    """Parse the HTML data dictionary into structured table/field data."""
    
    def __init__(self):
        super().__init__()
        self.tables = []
        self.current_table = None
        self.current_field = None
        self.in_h2 = False
        self.in_p = False
        self.in_th = False
        self.in_td = False
        self.td_index = 0
        self.in_table = False
        self.text_buffer = ""
        self.intro_text = ""
        self.found_first_h2 = False
        self.last_updated = None
        self.in_b = False
        self.skip_table_header = False
        
    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.in_h2 = True
            self.text_buffer = ""
            attrs_dict = dict(attrs)
            if self.current_table is not None:
                self.tables.append(self.current_table)
            self.current_table = {"name": "", "anchor": attrs_dict.get("id", ""), "description": "", "fields": []}
        elif tag == "p" and self.current_table is not None:
            self.in_p = True
            self.text_buffer = ""
        elif tag == "table":
            self.in_table = True
            self.skip_table_header = True
        elif tag == "th":
            self.in_th = True
        elif tag == "tr" and self.in_table:
            self.td_index = 0
            if self.skip_table_header:
                pass
            else:
                self.current_field = {"name": "", "type": "", "description": ""}
        elif tag == "td":
            self.in_td = True
            self.text_buffer = ""
        elif tag == "b":
            self.in_b = True
            
    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_h2 = False
            if self.current_table is not None:
                # Strip "EHI_" prefix from name if present
                name = self.text_buffer.strip()
                if name.startswith("EHI_"):
                    name = name[4:]
                self.current_table["name"] = name
                self.found_first_h2 = True
        elif tag == "p" and self.in_p:
            self.in_p = False
            if self.current_table is not None and not self.current_table["description"]:
                desc = self.text_buffer.strip()
                # Check for "Last Updated" in the description
                if "Last Updated" in desc:
                    match = re.search(r"Last Updated:\s*(.+)", desc)
                    if match:
                        self.last_updated = match.group(1).strip()
                else:
                    self.current_table["description"] = desc
        elif tag == "table":
            self.in_table = False
        elif tag == "th":
            self.in_th = False
        elif tag == "tr" and self.in_table:
            if self.skip_table_header:
                self.skip_table_header = False
            elif self.current_field and self.current_table is not None:
                self.current_table["fields"].append(self.current_field)
                self.current_field = None
        elif tag == "td":
            self.in_td = False
            if self.current_field is not None:
                val = self.text_buffer.strip()
                if self.td_index == 0:
                    self.current_field["name"] = val
                elif self.td_index == 1:
                    self.current_field["type"] = val
                elif self.td_index == 2:
                    self.current_field["description"] = val
                self.td_index += 1
        elif tag == "b":
            self.in_b = False
            
    def handle_data(self, data):
        if self.in_h2 or self.in_p or self.in_td:
            self.text_buffer += data

    def finish(self):
        if self.current_table is not None:
            self.tables.append(self.current_table)
            self.current_table = None

def categorize_table(name, description):
    """Assign a domain category based on table name patterns."""
    n = name.lower()
    d = description.lower() if description else ""
    
    if n.startswith("allergy_"):
        return "Allergy/Immunotherapy"
    if n.startswith("lab_"):
        return "Laboratory"
    if n.startswith("problem_"):
        return "Problem List"
    if n.startswith("colbased_"):
        return "Custom/Column-Based Data"
    if n.startswith("demo_"):
        return "Demographics"
    if n.startswith("etask_"):
        return "E-Tasking/Communication"
    if n.startswith("toc_"):
        return "Transitions of Care"
    if n.startswith("screening"):
        return "Screening/Assessment"
    if n.startswith("patientscreening"):
        return "Screening/Assessment"
    
    # Eye care
    eye_keywords = ["eye", "iop", "refraction", "keratometry", "visualacuity", "contactlens", "dilation", "ocular"]
    if any(k in n for k in eye_keywords):
        return "Ophthalmology/Eye Care"
    
    # Cancer
    if "cancer" in n:
        return "Oncology/Cancer"
    
    # Vitals
    if "vital" in n:
        return "Vitals"
    
    # Immunizations
    if "immun" in n:
        return "Immunizations"
    
    # Visits
    if "visit" in n:
        return "Visits/Encounters"
    
    # Medications
    med_keywords = ["medication", "erx", "rxhistory", "printrx", "renewal"]
    if any(k in n for k in med_keywords):
        return "Medications/Prescriptions"
    
    # Allergies/Alerts
    if "allerg" in n or "alert" in n:
        return "Allergies/Alerts"
    
    # Referrals
    if "referral" in n:
        return "Referrals"
    
    # Family history
    if "family" in n or "familyhist" in n:
        return "Family History"
    
    # Billing/Financial
    billing_names = ["trans", "allocatedtrans", "claimhistory", "eobrecs", "estimatedtl", 
                     "estimatehdr", "paymentplans", "statements", "dunningmessages"]
    if any(n == bn or n.startswith(bn + "_") for bn in billing_names):
        return "Billing/Financial"
    
    # Accounts
    if n.startswith("acct") or n.startswith("accounts"):
        return "Accounts"
    
    # Orders
    if "order" in n:
        return "Orders"
    
    # Flowsheets
    if "flowsheet" in n:
        return "Flowsheets"
    
    # Midmark (before blob check)
    if "midmark" in n:
        return "Device Integration (Midmark)"

    # Documents/Attachments
    if "blob" in n:
        return "Documents/Attachments"
    
    # Fax
    if "fax" in n:
        return "Fax"
    
    # Scribble
    if "scribble" in n:
        return "Scribble/Drawing Notes"
    
    # Portal
    if "portal" in n:
        return "Patient Portal"
    
    # Patient Forms
    if "patientform" in n:
        return "Patient Forms"
    
    # HRI
    if n.startswith("t_hri"):
        return "Health Record Items"
    
    # Recalls
    if "recall" in n:
        return "Recalls"
    
    # Midmark
    if "midmark" in n:
        return "Device Integration (Midmark)"
    
    # Info Release
    if "inforelease" in n:
        return "Information Release"
    
    # Patient clinical data
    patient_clinical = ["t_patientaddress", "t_patientccda", "t_patientcognitive",
                       "t_patienteducation", "t_patientemergency", "t_patientethnicity",
                       "t_patientfunctional", "t_patienthistory", "t_patientimplant",
                       "t_patientindustries", "t_patientletter", "t_patientnextofkin",
                       "t_patientoccupations", "t_patientpharmacy", "t_patientphones",
                       "t_patientpmh", "t_patientproviders", "t_patientraces",
                       "t_patientrecord", "t_patients", "t_patientsection",
                       "t_patienttransitions"]
    if any(n.startswith(pc) for pc in patient_clinical):
        return "Patient Clinical Data"
    
    # Patient notes
    if "patientnotes" in n:
        return "Patient Notes"
    
    # Tasks
    if "task" in n:
        return "Tasks"
    
    # Panels  
    if "panel" in n:
        return "Panels"
    
    # Patient admin (legacy)
    if n == "patients" or n == "patients_reps" or n == "patienthipaa":
        return "Patient Administrative"
    
    # Misc address
    if n == "miscaddress":
        return "Addresses"
    
    # Record requests
    if "recordrequest" in n:
        return "Record Requests"
    
    # System/Reference for everything else with T_ prefix
    return "System/Reference"


def analyze():
    html_content = HTML_PATH.read_text(encoding="utf-8")
    
    parser = TableParser()
    parser.feed(html_content)
    parser.finish()
    
    # Filter out the "Data Table Index" h2 which is the TOC
    tables = [t for t in parser.tables if t["name"] != "Data Table Index" and t["fields"]]
    
    # Categorize tables
    for t in tables:
        t["category"] = categorize_table(t["name"], t["description"])
    
    # Build full entity inventory
    total_fields = sum(len(t["fields"]) for t in tables)
    fields_with_desc = sum(1 for t in tables for f in t["fields"] if f["description"].strip())
    fields_with_type = sum(1 for t in tables for f in t["fields"] if f["type"].strip())
    
    # Type distribution
    type_dist = {}
    for t in tables:
        for f in t["fields"]:
            ft = f["type"].strip().lower()
            # Normalize - extract base type
            base_type = ft.split("(")[0].strip() if ft else "(empty)"
            type_dist[base_type] = type_dist.get(base_type, 0) + 1
    
    # Category summary
    category_summary = {}
    for t in tables:
        cat = t["category"]
        if cat not in category_summary:
            category_summary[cat] = {"table_count": 0, "field_count": 0, "tables": []}
        category_summary[cat]["table_count"] += 1
        category_summary[cat]["field_count"] += sum(1 for _ in t["fields"])
        category_summary[cat]["tables"].append(t["name"])
    
    # Sort categories by field count desc
    sorted_categories = sorted(category_summary.items(), key=lambda x: -x[1]["field_count"])
    
    # Largest tables
    largest_tables = sorted(tables, key=lambda t: -len(t["fields"]))[:20]
    
    # Tables with empty descriptions on fields
    tables_with_empty_desc_fields = []
    for t in tables:
        empty_count = sum(1 for f in t["fields"] if not f["description"].strip())
        if empty_count > 0:
            tables_with_empty_desc_fields.append({
                "name": t["name"],
                "total_fields": len(t["fields"]),
                "empty_description_count": empty_count
            })
    
    # Save full entity inventory
    inventory = {
        "metadata": {
            "source": "ehi-export-data-table-definitions.html",
            "last_updated": parser.last_updated,
            "total_tables": len(tables),
            "total_fields": total_fields,
            "fields_with_descriptions": fields_with_desc,
            "fields_without_descriptions": total_fields - fields_with_desc,
            "description_coverage_pct": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
            "fields_with_types": fields_with_type,
        },
        "type_distribution": dict(sorted(type_dist.items(), key=lambda x: -x[1])),
        "category_summary": {cat: info for cat, info in sorted_categories},
        "tables": tables
    }
    
    (OUTPUT_DIR / "full-entity-inventory.json").write_text(json.dumps(inventory, indent=2))
    
    # Save summary stats
    stats = {
        "total_tables": len(tables),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_without_descriptions": total_fields - fields_with_desc,
        "description_coverage_pct": round(100 * fields_with_desc / total_fields, 1) if total_fields else 0,
        "fields_with_types": fields_with_type,
        "type_coverage_pct": round(100 * fields_with_type / total_fields, 1) if total_fields else 0,
        "last_updated": parser.last_updated,
        "category_summary": {cat: {"tables": info["table_count"], "fields": info["field_count"]} for cat, info in sorted_categories},
        "largest_tables": [{"name": t["name"], "fields": len(t["fields"]), "category": t["category"]} for t in largest_tables],
        "tables_with_undescribed_fields": sorted(tables_with_empty_desc_fields, key=lambda x: -x["empty_description_count"]),
    }
    
    (OUTPUT_DIR / "summary-stats.json").write_text(json.dumps(stats, indent=2))
    
    # Print summary
    print(f"Tables parsed: {len(tables)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({stats['description_coverage_pct']}%)")
    print(f"Fields with types: {fields_with_type} ({stats['type_coverage_pct']}%)")
    print(f"Last updated: {parser.last_updated}")
    print(f"\nCategory breakdown:")
    for cat, info in sorted_categories:
        print(f"  {cat}: {info['table_count']} tables, {info['field_count']} fields")
    print(f"\nTop 10 largest tables:")
    for t in largest_tables[:10]:
        print(f"  {t['name']}: {len(t['fields'])} fields")
    print(f"\nTables with undescribed fields: {len(tables_with_empty_desc_fields)}")
    if tables_with_empty_desc_fields:
        for t in sorted(tables_with_empty_desc_fields, key=lambda x: -x["empty_description_count"])[:5]:
            print(f"  {t['name']}: {t['empty_description_count']}/{t['total_fields']} undescribed")

if __name__ == "__main__":
    analyze()
