#!/usr/bin/env python3
"""
Parse the Flatiron Health EHI Data Dictionary PDF into structured JSON.
Uses pdftotext -layout output and parses the fixed-width table format.
Outputs: entity-inventory-full.json, entity-inventory-summary.json
"""

import json
import re
import subprocess
import sys
from collections import defaultdict

PDF_PATH = "../downloads/ehi-data-dictionary.pdf"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True, check=True
    )
    return result.stdout

KNOWN_TYPES = {
    "datetime", "datetime2", "integer", "int", "binary", "varchar", "nvarchar",
    "bit", "float", "text", "decimal", "bigint", "boolean", "uniqueidentifier",
    "xml", "varbinary", "money", "smallint", "tinyint", "real", "numeric",
    "ntext", "image", "char", "nchar", "date", "time", "timestamp",
    "datetimeoffset",
}

def is_type(s):
    """Check if string looks like a SQL type."""
    base = re.sub(r'\(.*\)', '', s).strip().lower()
    return base in KNOWN_TYPES

def parse_pdf():
    text = extract_text()
    lines = text.split('\n')
    
    # Extract header info
    header_info = {
        "single_patient_format": "CSV",
        "population_format": "Parquet",
        "additional_formats": "XML, JPEG, PNG, TIFF, PDF",
        "access_method": "Single patient: self-service via OncoEMR UI; Population: requested via OncoEMR UI, downloaded via UI or SFTP",
        "last_modified": "",
    }
    
    for line in lines[:20]:
        m = re.search(r'Last Modified:\s*(.+)', line)
        if m:
            header_info["last_modified"] = m.group(1).strip()
    
    # Find where data starts (after first header row)
    start_idx = 0
    for i, line in enumerate(lines):
        if 'TableName' in line and 'ColumnName' in line and 'Type' in line:
            start_idx = i + 1
            break
    
    # Parse all data rows
    tables = {}  # normalized_name -> {name, description, columns}
    current_table_name = None
    current_col = None
    
    for i in range(start_idx, len(lines)):
        line = lines[i]
        
        # Skip empty and header lines
        if not line.strip():
            continue
        if 'TableName' in line and 'ColumnName' in line and 'Type' in line:
            continue
        
        trimmed = line.lstrip()
        leading = len(line) - len(trimmed)
        
        # Continuation line (heavily indented)
        if leading > 10 and current_col is not None:
            current_col["description"] += " " + trimmed.strip()
            continue
        
        # Try to parse as a data row
        parts = re.split(r'\s{2,}', line.strip())
        
        if len(parts) < 2:
            if current_col:
                current_col["description"] += " " + line.strip()
            continue
        
        table_name_raw = parts[0].strip()
        col_name_raw = parts[1].strip()
        
        # Normalize table name to PascalCase for grouping
        norm_name = table_name_raw
        if norm_name == norm_name.lower() and norm_name != "Table Description":
            # It's all lowercase - try to match existing table by case-insensitive
            matched = False
            for existing in tables:
                if existing.lower() == norm_name:
                    norm_name = existing
                    matched = True
                    break
            if not matched:
                # Convert to Title_Case
                norm_name = "_".join(w.capitalize() for w in norm_name.split("_"))
        
        # Handle Table Description entry
        if col_name_raw == "Table Description":
            desc = " ".join(parts[2:]).strip() if len(parts) > 2 else ""
            if norm_name not in tables:
                tables[norm_name] = {"name": norm_name, "description": desc, "columns": []}
            else:
                tables[norm_name]["description"] = desc
            current_col = None
            current_table_name = norm_name
            continue
        
        # Handle PARTITION_NAMESPACE (lowercase table name duplicate)
        if col_name_raw == "PARTITION_NAMESPACE":
            # Find the matching table
            matched = None
            for existing in tables:
                if existing.lower() == table_name_raw.lower():
                    matched = existing
                    break
            if matched is None:
                matched = table_name_raw
                tables[matched] = {"name": matched, "description": "", "columns": []}
            
            # Add as a column
            desc = " ".join(parts[3:]).strip() if len(parts) > 3 else ""
            type_str = parts[2].strip() if len(parts) > 2 else "varchar"
            col = {
                "column_name": "PARTITION_NAMESPACE",
                "data_type": type_str if is_type(type_str) else "varchar",
                "nullable": False,
                "description": desc if desc else "Represents the OncoEMR secure environment this practice is hosted on.",
            }
            tables[matched]["columns"].append(col)
            current_col = col
            current_table_name = matched
            continue
        
        # Regular column row - need to find type
        type_str = ""
        nullable = None
        description = ""
        
        if len(parts) >= 3 and is_type(parts[2].strip()):
            type_str = parts[2].strip()
            if len(parts) >= 4:
                null_str = parts[3].strip().upper()
                if null_str == "TRUE":
                    nullable = True
                elif null_str == "FALSE":
                    nullable = False
                else:
                    # parts[3] might be start of description
                    description = " ".join(parts[3:]).strip()
            if nullable is not None and len(parts) >= 5:
                description = " ".join(parts[4:]).strip()
        elif len(parts) >= 4 and is_type(parts[3].strip()):
            # Column name had a split
            col_name_raw = parts[1].strip() + " " + parts[2].strip()
            type_str = parts[3].strip()
            if len(parts) >= 5:
                null_str = parts[4].strip().upper()
                if null_str == "TRUE":
                    nullable = True
                elif null_str == "FALSE":
                    nullable = False
            if nullable is not None and len(parts) >= 6:
                description = " ".join(parts[5:]).strip()
        else:
            # Can't parse as data row - continuation
            if current_col:
                current_col["description"] += " " + line.strip()
            continue
        
        # Ensure table exists
        if norm_name not in tables:
            tables[norm_name] = {"name": norm_name, "description": "", "columns": []}
        
        col = {
            "column_name": col_name_raw,
            "data_type": type_str,
            "nullable": nullable,
            "description": description,
        }
        tables[norm_name]["columns"].append(col)
        current_col = col
        current_table_name = norm_name
    
    # Clean up descriptions
    for t in tables.values():
        t["description"] = re.sub(r'\s+', ' ', t["description"]).strip()
        for c in t["columns"]:
            c["description"] = re.sub(r'\s+', ' ', c["description"]).strip()
    
    return header_info, tables

def categorize_table(name, desc):
    """Assign a table to a domain category."""
    n = name.lower()
    d = (desc or "").lower()
    
    if any(x in n for x in ["demographics", "address", "phone", "email", "contact", "patientother", "sexparameter", "patient_location", "patient_information", "patient_provider", "patient_userxref", "patientaccess"]):
        return "Demographics"
    if any(x in n for x in ["document", "visit_note", "data_history", "datanew", "ccdavalidation", "interventions"]):
        return "Clinical Notes & Documents"
    if any(x in n for x in ["diagnosis", "condition"]):
        return "Diagnoses & Staging"
    if any(x in n for x in ["staging"]):
        return "Diagnoses & Staging"
    if any(x in n for x in ["medication", "order", "dose", "drug_rule", "inventory_dispense", "lifetimedose", "substitution_log", "orderset"]):
        return "Medications & Orders"
    if any(x in n for x in ["lab_result", "test_history", "test_aoe"]):
        return "Labs & Results"
    if "allergy" in n:
        return "Allergies"
    if "immunization" in n:
        return "Immunizations"
    if "vital_sign" in n:
        return "Vital Signs"
    if "familyhist" in n:
        return "Family History"
    if any(x in n for x in ["care_plan", "patientgoals"]):
        return "Care Plans & Goals"
    if any(x in n for x in ["charge", "claim", "transaction", "invoice", "insurercredits", "billing"]):
        return "Billing & Financial"
    if any(x in n for x in ["insurance", "eligibility", "guarantor", "pbm", "apm_", "cdg_enrollment", "cdgenrollment"]):
        return "Insurance & Coverage"
    if "appointment" in n:
        return "Appointments"
    if "image" in n or "radiology" in n:
        return "Imaging"
    if any(x in n for x in ["message", "msgstosend", "task", "reminder", "linkclick"]):
        return "Messaging & Tasks"
    if any(x in n for x in ["pathway", "treatment", "regimen"]):
        return "Treatment & Pathways"
    if any(x in n for x in ["encounter", "externalencounter", "internaltoexternal"]):
        return "Encounters"
    if any(x in n for x in ["implantable", "device"]):
        return "Devices"
    if "questionnaire" in n:
        return "Questionnaires"
    if "careteam" in n:
        return "Care Team"
    if any(x in n for x in ["surescripts", "preferred_pharmacy"]):
        return "Prescriptions / E-Prescribing"
    if any(x in n for x in ["patientassistance"]):
        return "Patient Assistance"
    if "patient_request" in n:
        return "Patient Requests"
    return "Other"

def main():
    header_info, tables = parse_pdf()
    
    # Build full inventory
    entities = []
    for name, tbl in sorted(tables.items(), key=lambda x: x[0].lower()):
        category = categorize_table(name, tbl["description"])
        # Filter out PARTITION_NAMESPACE from field count for analysis
        regular_cols = [c for c in tbl["columns"] if c["column_name"] != "PARTITION_NAMESPACE"]
        all_cols = tbl["columns"]
        
        entity = {
            "entity_name": name,
            "category": category,
            "description": tbl["description"],
            "field_count": len(all_cols),
            "fields": []
        }
        for c in all_cols:
            field = {
                "name": c["column_name"],
                "type": c["data_type"],
                "nullable": c["nullable"],
                "description": c["description"],
            }
            entity["fields"].append(field)
        entities.append(entity)
    
    total_fields = sum(e["field_count"] for e in entities)
    fields_with_desc = sum(
        1 for e in entities for f in e["fields"]
        if f["description"] and f["description"].strip()
    )
    fields_with_type = sum(
        1 for e in entities for f in e["fields"]
        if f["type"] and f["type"].strip()
    )
    tables_with_desc = sum(1 for e in entities if e["description"])
    
    full_inventory = {
        "source": "downloads/ehi-data-dictionary.pdf",
        "source_type": "PDF data dictionary",
        "export_format": header_info,
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_with_types": fields_with_type,
        "entities_with_descriptions": tables_with_desc,
        "entities": entities,
    }
    
    with open("entity-inventory-full.json", "w") as f:
        json.dump(full_inventory, f, indent=2)
    print(f"Wrote entity-inventory-full.json: {len(entities)} entities, {total_fields} fields")
    
    # Build summary
    category_stats = defaultdict(lambda: {"tables": 0, "fields": 0, "table_names": []})
    for e in entities:
        cat = e["category"]
        category_stats[cat]["tables"] += 1
        category_stats[cat]["fields"] += e["field_count"]
        category_stats[cat]["table_names"].append(e["entity_name"])
    
    # Top 20 largest entities
    largest = sorted(entities, key=lambda e: e["field_count"], reverse=True)[:20]
    
    summary = {
        "total_entities": len(entities),
        "total_fields": total_fields,
        "fields_with_descriptions": fields_with_desc,
        "fields_without_descriptions": total_fields - fields_with_desc,
        "description_coverage_pct": round(fields_with_desc / total_fields * 100, 1) if total_fields else 0,
        "fields_with_types": fields_with_type,
        "entities_with_descriptions": tables_with_desc,
        "entities_without_descriptions": len(entities) - tables_with_desc,
        "category_breakdown": {
            cat: {
                "tables": stats["tables"],
                "fields": stats["fields"],
                "table_names": stats["table_names"],
            }
            for cat, stats in sorted(category_stats.items())
        },
        "largest_entities": [
            {"name": e["entity_name"], "fields": e["field_count"], "category": e["category"]}
            for e in largest
        ],
    }
    
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote entity-inventory-summary.json")
    
    # Print summary to stdout
    print(f"\n=== Summary ===")
    print(f"Entities: {len(entities)}")
    print(f"Fields: {total_fields}")
    print(f"Fields with descriptions: {fields_with_desc} ({summary['description_coverage_pct']}%)")
    print(f"Entities with descriptions: {tables_with_desc}/{len(entities)}")
    print(f"\n=== Category Breakdown ===")
    for cat, stats in sorted(category_stats.items(), key=lambda x: -x[1]["fields"]):
        print(f"  {cat}: {stats['tables']} tables, {stats['fields']} fields")
    print(f"\n=== 20 Largest Entities ===")
    for e in largest:
        print(f"  {e['entity_name']}: {e['field_count']} fields ({e['category']})")

if __name__ == "__main__":
    main()
