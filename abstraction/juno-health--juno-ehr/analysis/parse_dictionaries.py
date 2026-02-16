#!/usr/bin/env python3
"""
Parse Juno Health EHI export data dictionaries.
1. Extract table names from index pages (jehr + rtvx)
2. Fetch each individual table page from ehiexports.junohealth.com
3. Parse field-level detail (name, type, description, primary/foreign keys)
4. Output entity-inventory-full.json and entity-inventory-summary.json
"""

import json
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

DOWNLOADS = Path(__file__).parent.parent / "downloads"
ANALYSIS = Path(__file__).parent
CACHE_DIR = ANALYSIS / "table_pages_cache"

# --- Step 1: Extract table names from index pages ---

def extract_table_names(index_html_path):
    """Extract table names and their .html filenames from an index page."""
    with open(index_html_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Pattern: href="./TABLE_NAME.html"
    matches = re.findall(r'href="\./([^"]+)\.html"', content)
    # Deduplicate while preserving order
    seen = set()
    tables = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            tables.append(m)
    return tables


# --- Step 2: Fetch individual table pages ---

def fetch_table_page(base_url, table_name, cache_dir):
    """Fetch a table documentation page, with caching."""
    cache_file = cache_dir / f"{table_name}.html"
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    
    url = f"{base_url}/{table_name}.html"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read().decode("utf-8", errors="replace")
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(content)
        return content
    except Exception as e:
        print(f"  ERROR fetching {table_name}: {e}", file=sys.stderr)
        return None


# --- Step 3: Parse a table page ---

def parse_table_page(html_content, table_name):
    """Parse a table documentation page to extract fields, keys, description."""
    result = {
        "table_name": table_name,
        "description": "",
        "primary_keys": [],
        "foreign_keys": [],
        "fields": [],
        "parse_errors": []
    }
    
    if not html_content:
        result["parse_errors"].append("No HTML content")
        return result
    
    # Extract description
    desc_match = re.search(
        r'<b>Description:</b>\s*(.*?)</div>',
        html_content, re.DOTALL
    )
    if desc_match:
        desc = desc_match.group(1).strip()
        desc = re.sub(r'<[^>]+>', '', desc)
        desc = re.sub(r'\s+', ' ', desc).strip()
        result["description"] = desc
    
    # Extract primary keys
    pk_section = re.search(
        r'Primary Key.*?<table[^>]*>(.*?)</table>',
        html_content, re.DOTALL
    )
    if pk_section:
        pk_rows = re.findall(
            r'<tr[^>]*>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>',
            pk_section.group(1), re.DOTALL
        )
        for col_name, ordinal in pk_rows:
            col_name = re.sub(r'<[^>]+>', '', col_name).strip()
            if col_name and col_name != "Column Name":
                result["primary_keys"].append(col_name)
    
    # Extract foreign keys
    fk_section = re.search(
        r'Foreign Key.*?<table[^>]*>(.*?)</table>',
        html_content, re.DOTALL
    )
    if fk_section:
        fk_rows = re.findall(
            r'<tr[^>]*>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>.*?<td[^>]*>(.*?)</td>',
            fk_section.group(1), re.DOTALL
        )
        for col_name, ordinal, ref_table in fk_rows:
            col_name = re.sub(r'<[^>]+>', '', col_name).strip()
            ref_table = re.sub(r'<[^>]+>', '', ref_table).strip()
            if col_name and col_name != "Column Name":
                result["foreign_keys"].append({
                    "column": col_name,
                    "references": ref_table
                })
    
    # Extract fields from Column Information section
    # Each field is in its own <table class="detail-field-item ...">
    field_tables = re.findall(
        r'<table class="detail-field-item[^"]*">(.*?)</table>',
        html_content, re.DOTALL
    )
    
    for ft in field_tables:
        field = {}
        # Extract position, name, type from first data row
        data_row = re.search(
            r'<td[^>]*class="[^"]*field-position[^"]*"[^>]*>(.*?)</td>.*?'
            r'<td[^>]*class="[^"]*field-name[^"]*"[^>]*>(.*?)</td>.*?'
            r'<td[^>]*class="[^"]*field-type[^"]*"[^>]*>(.*?)</td>',
            ft, re.DOTALL
        )
        if data_row:
            field["ordinal"] = int(re.sub(r'<[^>]+>', '', data_row.group(1)).strip() or 0)
            field["name"] = re.sub(r'<[^>]+>', '', data_row.group(2)).strip()
            field["type"] = re.sub(r'<[^>]+>', '', data_row.group(3)).strip()
        else:
            continue
        
        # Extract description
        desc_match = re.search(
            r'class="[^"]*field-description[^"]*"[^>]*>\s*Description:\s*(.*?)</div>',
            ft, re.DOTALL
        )
        if desc_match:
            desc = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()
            desc = re.sub(r'\s+', ' ', desc).strip()
            field["description"] = desc
        else:
            field["description"] = ""
        
        result["fields"].append(field)
    
    return result


def categorize_table(table_name):
    """Assign a domain category based on table name prefix/pattern."""
    name = table_name.upper()
    
    # Lookup tables
    if name.startswith("LK"):
        return "Lookup/Reference"
    
    # Pharmacy/Prescription (AU_ prefix from VistA)
    if name.startswith("AU_"):
        return "Pharmacy/Prescription"
    
    # Specific domain prefixes
    prefixes = {
        "ALLERGY": "Allergies",
        "BILLING": "Billing/Financial",
        "ACCOUNT": "Billing/Financial",
        "CHARGE": "Billing/Financial",
        "CLAIM": "Billing/Financial",
        "COVERAGE": "Insurance/Coverage",
        "PAYER": "Insurance/Coverage",
        "INSURANCE": "Insurance/Coverage",
        "CAREPLAN": "Care Plans",
        "CARE_PLAN": "Care Plans",
        "CONDITION": "Conditions/Problems",
        "PROBLEM": "Conditions/Problems",
        "DIAGNOSIS": "Conditions/Problems",
        "DOCUMENT": "Documents/Notes",
        "NOTE": "Documents/Notes",
        "ENCOUNTER": "Encounters",
        "VISIT": "Encounters",
        "ADMISSION": "Encounters",
        "GOAL": "Goals",
        "IMMUNIZATION": "Immunizations",
        "VACCINE": "Immunizations",
        "LAB": "Laboratory",
        "MEDICATION": "Medications",
        "MED_": "Medications",
        "DRUG": "Medications",
        "OBSERVATION": "Observations/Vitals",
        "VITAL": "Observations/Vitals",
        "ORDER": "Orders",
        "PATIENT": "Patient Demographics",
        "PERSON": "Patient Demographics",
        "PROCEDURE": "Procedures",
        "SURGERY": "Procedures/Surgery",
        "PERIOPERATIVE": "Procedures/Surgery",
        "QUESTIONNAIRE": "Questionnaires/Forms",
        "FORM": "Questionnaires/Forms",
        "ASSESSMENT": "Questionnaires/Forms",
        "SCHEDULE": "Scheduling",
        "APPOINTMENT": "Scheduling",
        "SLOT": "Scheduling",
        "REFERRAL": "Referrals",
        "TREATMENT": "Treatment Plans",
        "GROUP_SESSION": "Behavioral Health",
        "BEHAVIORAL": "Behavioral Health",
        "CONSENT": "Consents",
        "COMMUNICATION": "Communications",
        "MESSAGE": "Communications",
        "DEVICE": "Medical Devices",
        "IMPLANT": "Medical Devices",
        "FAMILY": "Family History",
        "PROVENANCE": "Provenance",
    }
    
    for prefix, category in prefixes.items():
        if name.startswith(prefix):
            return category
    
    # Check contains for less specific matches
    if any(x in name for x in ["BILL", "CHARGE", "CLAIM", "PAYMENT", "INVOICE", "FEE"]):
        return "Billing/Financial"
    if any(x in name for x in ["ALLERG"]):
        return "Allergies"
    if any(x in name for x in ["IMMUNIZ", "VACCINE"]):
        return "Immunizations"
    if any(x in name for x in ["ENCOUNTER", "VISIT", "ADMISSION", "DISCHARGE", "TRANSFER"]):
        return "Encounters"
    if any(x in name for x in ["MEDICATION", "PRESCRI", "PHARMACY", "DRUG"]):
        return "Medications"
    if any(x in name for x in ["SURGERY", "SURGICAL", "OPERATIVE", "PERIOP"]):
        return "Procedures/Surgery"
    
    return "Other/Administrative"


def main():
    os.makedirs(CACHE_DIR / "jehr", exist_ok=True)
    os.makedirs(CACHE_DIR / "rtvx", exist_ok=True)
    
    # Extract table names
    jehr_tables = extract_table_names(DOWNLOADS / "jehr-data-dictionary.html")
    rtvx_tables = extract_table_names(DOWNLOADS / "rtvx-data-dictionary.html")
    
    print(f"JEHR tables: {len(jehr_tables)}")
    print(f"RTVX tables: {len(rtvx_tables)}")
    
    all_entities = []
    
    # Process JEHR tables
    print("\nFetching JEHR table pages...")
    for i, table_name in enumerate(jehr_tables):
        if i % 100 == 0:
            print(f"  Progress: {i}/{len(jehr_tables)}")
        html = fetch_table_page(
            "https://ehiexports.junohealth.com/jehr",
            table_name,
            CACHE_DIR / "jehr"
        )
        parsed = parse_table_page(html, table_name)
        parsed["source"] = "jehr"
        parsed["category"] = categorize_table(table_name)
        all_entities.append(parsed)
        # Small delay to be polite
        if not (CACHE_DIR / "jehr" / f"{table_name}.html").exists():
            time.sleep(0.1)
    
    # Process RTVX tables
    print("\nFetching RTVX table pages...")
    for i, table_name in enumerate(rtvx_tables):
        html = fetch_table_page(
            "https://ehiexports.junohealth.com/rtvx",
            table_name,
            CACHE_DIR / "rtvx"
        )
        parsed = parse_table_page(html, table_name)
        parsed["source"] = "rtvx"
        parsed["category"] = categorize_table(table_name)
        all_entities.append(parsed)
        if not (CACHE_DIR / "rtvx" / f"{table_name}.html").exists():
            time.sleep(0.1)
    
    # Save full inventory
    with open(ANALYSIS / "entity-inventory-full.json", "w") as f:
        json.dump(all_entities, f, indent=2)
    
    # Build summary
    total_fields = sum(len(e["fields"]) for e in all_entities)
    fields_with_desc = sum(
        1 for e in all_entities for field in e["fields"] if field.get("description")
    )
    tables_with_desc = sum(1 for e in all_entities if e.get("description"))
    tables_with_errors = sum(1 for e in all_entities if e.get("parse_errors"))
    
    # Category breakdown
    categories = {}
    for e in all_entities:
        cat = e["category"]
        if cat not in categories:
            categories[cat] = {"tables": 0, "fields": 0, "fields_with_desc": 0}
        categories[cat]["tables"] += 1
        categories[cat]["fields"] += len(e["fields"])
        categories[cat]["fields_with_desc"] += sum(
            1 for f in e["fields"] if f.get("description")
        )
    
    # Source breakdown
    sources = {}
    for e in all_entities:
        src = e["source"]
        if src not in sources:
            sources[src] = {"tables": 0, "fields": 0}
        sources[src]["tables"] += 1
        sources[src]["fields"] += len(e["fields"])
    
    # Top 20 largest tables
    top_tables = sorted(all_entities, key=lambda e: len(e["fields"]), reverse=True)[:20]
    
    summary = {
        "total_tables": len(all_entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "description_percentage": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "tables_with_descriptions": tables_with_desc,
        "tables_with_parse_errors": tables_with_errors,
        "by_source": sources,
        "by_category": dict(sorted(categories.items(), key=lambda x: x[1]["tables"], reverse=True)),
        "top_20_largest_tables": [
            {
                "table": t["table_name"],
                "source": t["source"],
                "category": t["category"],
                "field_count": len(t["fields"]),
                "description": t["description"][:100] + "..." if len(t.get("description", "")) > 100 else t.get("description", "")
            }
            for t in top_tables
        ]
    }
    
    with open(ANALYSIS / "entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n=== Summary ===")
    print(f"Total tables: {len(all_entities)}")
    print(f"Total fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['description_percentage']}%)")
    print(f"Tables with descriptions: {tables_with_desc}")
    print(f"\nBy source:")
    for src, data in sources.items():
        print(f"  {src}: {data['tables']} tables, {data['fields']} fields")
    print(f"\nBy category:")
    for cat, data in sorted(categories.items(), key=lambda x: x[1]["tables"], reverse=True):
        print(f"  {cat}: {data['tables']} tables, {data['fields']} fields ({data['fields_with_desc']} described)")
    print(f"\nTop 10 largest tables:")
    for t in top_tables[:10]:
        print(f"  {t['table_name']} ({t['source']}): {len(t['fields'])} fields")


if __name__ == "__main__":
    main()
