#!/usr/bin/env python3
"""
Parse all athenahealth EHI export artifacts and produce entity-inventory-full.json
and entity-inventory-summary.json.

Sources:
  - downloads/enrichment/datasets.json (structured dataset catalog from Contentful API)
  - downloads/inpatient-clinical-ehi-export.pdf (PDF data dictionary, 37 pages, HTML template specs)
  - downloads/ambulatory-clinical-ehi-export.pdf (PDF data dictionary, 10 pages)
  - downloads/ambulatory-collector-ehi-export.pdf (PDF data dictionary, 7 pages)
  - downloads/inpatient-collector-ehi-export.pdf (PDF data dictionary, 7 pages)
"""

import json
import re
import subprocess
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS = os.path.join(BASE, "downloads")
ANALYSIS = os.path.join(BASE, "analysis")


def extract_pdf_text(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout


def parse_inpatient_clinical_fields(text):
    """Parse inpatient clinical PDF HTML template specs to extract fields per dataset."""
    datasets = []
    # Split by numbered dataset sections
    sections = re.split(r'\n\s+(\d+)\.\s+(.+?):\n', text)
    
    i = 1  # skip preamble
    while i < len(sections) - 1:
        num = sections[i].strip()
        name = sections[i+1].strip()
        body = sections[i+2] if i+2 < len(sections) else ""
        
        fields = []
        # Extract fields from <td> tags with descriptions
        td_matches = re.findall(r'<td>\s*(.+?):\s*<b><<(\w+)>>\s*<<(.+?)>>\s*</b>', body)
        for field_name, field_type, field_desc in td_matches:
            fields.append({
                "name": field_name.strip(),
                "type": field_type.strip(),
                "description": field_desc.strip()
            })
        
        # Extract fields from <span> headings (sections within a dataset)
        span_matches = re.findall(r'<span\s+class="clinicalsubsubheading">(.+?)</span>', body)
        for heading in span_matches:
            fields.append({
                "name": heading.strip(),
                "type": "section",
                "description": f"Section heading within {name}"
            })
        
        # Extract dynamic key-value fields <<Name of X>>: <<Value of X>>
        kv_matches = re.findall(r'<<string>><<(Name of (?:the )?(?:measurement|reading)(?:#\d+)?)>>', body)
        kv_val_matches = re.findall(r'<<string>><<(Value of (?:the )?(?:measurement|reading)(?:#\d+)?)>>', body)
        
        # Deduplicate
        seen_kv = set()
        for m in kv_matches:
            base = re.sub(r'#\d+', '', m).strip()
            if base not in seen_kv:
                seen_kv.add(base)
                fields.append({
                    "name": base,
                    "type": "string",
                    "description": f"Dynamic measurement/reading name in {name}"
                })
        seen_val = set()
        for m in kv_val_matches:
            base = re.sub(r'#\d+', '', m).strip()
            if base not in seen_val:
                seen_val.add(base)
                fields.append({
                    "name": base,
                    "type": "string",
                    "description": f"Dynamic measurement/reading value in {name}"
                })
        
        # Extract datetime fields
        dt_matches = re.findall(r'<<string>><<(Date (?:and time )?of (?:the )?(?:\w+\s*)+?)>>', body)
        seen_dt = set()
        for m in dt_matches:
            clean = m.strip().rstrip('>')
            if clean not in seen_dt:
                seen_dt.add(clean)
                fields.append({
                    "name": clean,
                    "type": "string",
                    "description": f"Timestamp field in {name}"
                })
        
        # Extract other <<string>><<Description>> patterns
        other_matches = re.findall(r'<<string>><<(.+?)>>', body)
        seen_other = set()
        for m in other_matches:
            clean = m.strip().rstrip('>')
            # Skip ones already captured
            if any(clean.startswith(prefix) for prefix in ('Name of', 'Value of', 'Date')):
                continue
            if clean not in seen_other and clean not in seen_kv and clean not in seen_val:
                seen_other.add(clean)
                fields.append({
                    "name": clean,
                    "type": "string",
                    "description": f"Field in {name}"
                })
        
        # Extract attribution fields
        if 'attribution' in body.lower():
            if not any(f['name'].startswith('Created') or f['name'].startswith('Signed') or f['name'].startswith('Reviewed') for f in fields):
                # Check for specific attribution patterns
                attr_matches = re.findall(r'<<string>><<((?:Created|Signed|Entered|Reviewed|Ordered)\s+(?:by|By|date|Date).+?)>>', body)
                for m in attr_matches:
                    clean = m.strip().rstrip('>')
                    if clean not in seen_other:
                        seen_other.add(clean)
                        fields.append({
                            "name": clean,
                            "type": "string", 
                            "description": f"Attribution field in {name}"
                        })

        datasets.append({
            "name": name,
            "number": int(num),
            "fields": fields,
            "field_count": len(fields),
            "source": "inpatient-clinical-ehi-export.pdf"
        })
        
        i += 3
    
    return datasets


def load_enrichment_datasets():
    """Load the pre-parsed enrichment datasets.json."""
    with open(os.path.join(DOWNLOADS, "enrichment", "datasets.json")) as f:
        data = json.load(f)
    return data


def build_entity_inventory():
    """Build the complete entity inventory from all sources."""
    enrichment = load_enrichment_datasets()
    
    entities = []
    
    for et in enrichment["exportTypes"]:
        category = et.get("category", "")
        if category in ("overview", "release-notes"):
            continue
        
        export_title = et["title"]
        export_format = et.get("format", "unknown")
        
        for ds in et.get("datasets", []):
            entity = {
                "name": ds["name"],
                "export_type": export_title,
                "category": category,
                "format": export_format,
                "spec_url": ds.get("specUrl"),
                "includes_attachments": ds.get("includesAttachments", False),
                "source": ds.get("source", ""),
                "fields": [],
                "field_count": 0,
                "has_external_spec": bool(ds.get("specUrl")),
                "description": ""
            }
            entities.append(entity)
        
        # Add inline specs as field details
        for spec in et.get("inlineSpecs", []):
            dataset_name = spec["datasetName"]
            # Find matching entity
            matching = [e for e in entities if e["name"] == dataset_name and e["category"] == category]
            if not matching:
                # Create new entity for inline spec
                entity = {
                    "name": dataset_name,
                    "export_type": export_title,
                    "category": category,
                    "format": export_format,
                    "spec_url": None,
                    "includes_attachments": False,
                    "source": spec.get("source", ""),
                    "fields": [],
                    "field_count": 0,
                    "has_external_spec": False,
                    "description": f"Inline specification from {spec.get('source', '')}"
                }
                entities.append(entity)
                matching = [entity]
            
            target = matching[0]
            for param in spec.get("outputParameters", []):
                target["fields"].append({
                    "name": param.get("name", ""),
                    "type": param.get("type", ""),
                    "description": param.get("description", ""),
                    "source": "inline_spec"
                })
            for param in spec.get("inputParameters", []):
                target["fields"].append({
                    "name": param.get("name", ""),
                    "type": param.get("type", ""),
                    "description": param.get("description", ""),
                    "source": "inline_spec_input"
                })
            target["field_count"] = len(target["fields"])
    
    # Now parse inpatient clinical PDF for field-level detail
    inp_text = extract_pdf_text(os.path.join(DOWNLOADS, "inpatient-clinical-ehi-export.pdf"))
    inp_datasets = parse_inpatient_clinical_fields(inp_text)
    
    # Merge PDF-parsed fields into existing entities
    for pdf_ds in inp_datasets:
        matching = [e for e in entities if e["name"] == pdf_ds["name"] and e["category"] == "inpatient-clinical"]
        if matching:
            target = matching[0]
            target["fields"] = pdf_ds["fields"]
            target["field_count"] = len(pdf_ds["fields"])
            target["description"] = f"Parsed from PDF page, {len(pdf_ds['fields'])} fields extracted from HTML template spec"
        else:
            print(f"WARNING: PDF dataset '{pdf_ds['name']}' not found in enrichment data")
    
    # Parse ambulatory clinical PDF for the dataset list
    amb_text = extract_pdf_text(os.path.join(DOWNLOADS, "ambulatory-clinical-ehi-export.pdf"))
    # Ambulatory clinical has 64 datasets but specs are via API links, not inline
    # The PDF mainly lists dataset names and links to API specs
    
    # Update field counts
    for e in entities:
        e["field_count"] = len(e["fields"])
        e["fields_with_descriptions"] = sum(1 for f in e["fields"] if f.get("description"))
        e["fields_with_types"] = sum(1 for f in e["fields"] if f.get("type"))
    
    return entities


def compute_summary(entities):
    """Compute summary statistics from the entity inventory."""
    
    # By export type
    by_export = {}
    for e in entities:
        et = e["export_type"]
        if et not in by_export:
            by_export[et] = {"entity_count": 0, "total_fields": 0, "fields_with_desc": 0, "format": e["format"]}
        by_export[et]["entity_count"] += 1
        by_export[et]["total_fields"] += e["field_count"]
        by_export[et]["fields_with_desc"] += e["fields_with_descriptions"]
    
    # By domain mapping
    domain_mapping = {
        "Demographics": ["Patient Demographics information", "Demographics"],
        "Encounters / Visits": ["Encounters", "Visits and Charge Details", "Appointments", "ED Course", "ED Provider Assessment", "ED Provider Notes", "ED Triage Notes", "ED Nursing Initial Assessment Notes"],
        "Problems / Conditions": ["Health Concerns – Conditions & Problems", "Assessment and Plan"],
        "Medications": ["Medications", "Medication Administration Record"],
        "Allergies": ["Allergies"],
        "Immunizations": ["Immunizations"],
        "Vitals": ["Vitals", "Flowsheet Vitals", "Procedure Vitals"],
        "Lab Results": ["Lab Results", "Interpretations"],
        "Imaging / Diagnostic": ["Imaging Results"],
        "Procedures": ["Procedures", "Procedures Documentation", "Procedure Roles", "Procedure Times", "Procedure Timeout Checklist", "Pre-sedation Assessment", "Surgical Orders", "Surgical Results", "Surgical Pre-Op Notes", "Surgery Action Notes"],
        "Clinical Notes / Documents": ["Admin Documents", "Clinical Documents", "Encounter Documents", "Office Notes", "Letters", "Medical Record Documents", "Other CCDAs", "Hospital Notes", "Consult Notes", "Nursing Notes", "Nursing Admission Notes", "Nursing Care Plan", "Nursing Tasks", "Admission H&P", "Discharge Summary", "Discharge Planning Notes", "Discharge Planning Audit", "Patient Discharge Instructions", "Paper Forms"],
        "Care Plans / Goals": ["Care Plan", "Care Plan Events", "Goals", "Topic of Discussion", "Nursing Care Plan"],
        "Orders / Referrals": ["Orders", "Orders – Labs, Imaging, Consult & Procedures", "Admission Order", "Transfer Orders", "DME Orders", "Referral/Auth", "Default Clinical Providers – Lab", "Default Clinical Providers - Imaging", "Default Clinical Providers – Pharmacy"],
        "Insurance / Coverage": ["Patient Insurance"],
        "Claims / Billing": ["Claim Details", "Claim Notes", "Claim Transactions", "Claim Attachments"],
        "Payments": ["Payment History", "Payment plans", "Pre-payment plans", "Patient Outstanding Balance & Patient Unapplied", "Patient - Billing statements and Summaries"],
        "Family History": ["Family History"],
        "Social History": ["Social History"],
        "Screening / Assessments": ["Screening"],
        "OB/GYN": ["GYN History", "OB Episodes", "OB Episode Summary", "OB Episode Summary Documents", "OB History", "Perinatal History"],
        "Eye Care": ["Eye Care Specific Measurements", "Corrective Lens"],
        "Physical Therapy": ["PT Episode"],
        "Cancer": ["Cancer Cases"],
        "Encounter Detail": ["Chief Complaint", "History of Present Illness", "Physical Exam", "Review of Systems", "Encounter Summary", "Encounter Phone Call Checklists", "Past Medical History", "Surgical History"],
        "Care Team": ["Care Team Members"],
        "Devices": ["Devices or Medical Equipment"],
        "Flowsheets (Inpatient)": ["Flowsheet ADL", "Flowsheet ADLs", "Flowsheet Airways", "Flowsheet Drains", "Flowsheet Head to Toe", "Flowsheet Intake & Output", "Flowsheet Lines", "Flowsheet Measurements", "Flowsheet Vitals"],
        "Tasks (Inpatient)": ["Respiratory Tasks", "Therapy Tasks"],
        "Physician Authorization": ["Physician Authorization"],
        "Letters / Communications": ["Letters", "Letter Action Notes", "Return to Office", "Appointment Ticklers & Reminders"],
        "Consents / Directives": [],
        "Patient Portal Messages": [],
    }
    
    # Check coverage
    all_entity_names = set(e["name"] for e in entities)
    domain_coverage = {}
    for domain, entity_names in domain_mapping.items():
        matched = [n for n in entity_names if n in all_entity_names]
        matched_entities = [e for e in entities if e["name"] in entity_names]
        total_fields = sum(e["field_count"] for e in matched_entities)
        domain_coverage[domain] = {
            "matched_entities": matched,
            "entity_count": len(matched),
            "total_fields": total_fields,
            "covered": len(matched) > 0
        }
    
    # Find unmapped entities
    mapped_names = set()
    for names in domain_mapping.values():
        mapped_names.update(names)
    unmapped = [e["name"] for e in entities if e["name"] not in mapped_names]
    
    total_entities = len(entities)
    total_fields = sum(e["field_count"] for e in entities)
    total_with_desc = sum(e["fields_with_descriptions"] for e in entities)
    entities_with_ext_spec = sum(1 for e in entities if e.get("has_external_spec"))
    entities_with_fields = sum(1 for e in entities if e["field_count"] > 0)
    
    summary = {
        "total_entities": total_entities,
        "total_fields_documented_inline": total_fields,
        "total_fields_with_descriptions": total_with_desc,
        "entities_with_external_api_spec": entities_with_ext_spec,
        "entities_with_inline_fields": entities_with_fields,
        "by_export_type": by_export,
        "domain_coverage": domain_coverage,
        "unmapped_entities": unmapped,
        "unique_entity_names": len(set(e["name"] for e in entities)),
        "deduplicated_across_ambulatory_inpatient": True,
    }
    
    return summary


def main():
    entities = build_entity_inventory()
    summary = compute_summary(entities)
    
    # Save full inventory
    with open(os.path.join(ANALYSIS, "entity-inventory-full.json"), "w") as f:
        json.dump(entities, f, indent=2)
    
    # Save summary
    with open(os.path.join(ANALYSIS, "entity-inventory-summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary stats
    print(f"Total entities (across all export types): {summary['total_entities']}")
    print(f"Unique entity names: {summary['unique_entity_names']}")
    print(f"Entities with external API spec links: {summary['entities_with_external_api_spec']}")
    print(f"Entities with inline field detail: {summary['entities_with_inline_fields']}")
    print(f"Total inline fields documented: {summary['total_fields_documented_inline']}")
    print(f"Fields with descriptions: {summary['total_fields_with_descriptions']}")
    print()
    
    print("By export type:")
    for et_name, et_stats in summary["by_export_type"].items():
        print(f"  {et_name}: {et_stats['entity_count']} entities, {et_stats['total_fields']} inline fields ({et_stats['format']})")
    
    print()
    print("Domain coverage:")
    covered = sum(1 for d in summary["domain_coverage"].values() if d["covered"])
    total_domains = len(summary["domain_coverage"])
    print(f"  {covered}/{total_domains} domains have at least one entity")
    
    for domain, info in sorted(summary["domain_coverage"].items()):
        status = "✅" if info["covered"] else "❌"
        print(f"  {status} {domain}: {info['entity_count']} entities, {info['total_fields']} fields")
    
    if summary["unmapped_entities"]:
        print(f"\n  Unmapped entities: {summary['unmapped_entities']}")


if __name__ == "__main__":
    main()
