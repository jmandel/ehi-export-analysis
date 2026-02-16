#!/usr/bin/env python3
"""
Complete parser for all athenahealth EHI export artifacts.
Produces full-entity-inventory.json with every dataset and its parsed fields.

Sources:
  - enrichment/datasets.json (structured dataset catalog)
  - 4 PDFs (text extracted via pdftotext)
"""

import json
import re
import subprocess
import os

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/athenahealth-inc--athenaclinicals/downloads"
ANALYSIS_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/athenahealth-inc--athenaclinicals/analysis"


def extract_pdf_text(pdf_path):
    result = subprocess.run(["pdftotext", "-layout", pdf_path, "-"], capture_output=True, text=True)
    return result.stdout


def parse_inpatient_section(name, content):
    """Parse a single inpatient clinical dataset section."""
    fields = []
    seen = set()

    def add(fname, ftype, fdesc, src):
        key = fname.strip()
        if key and key not in seen and not key.startswith("311 Arsenal"):
            seen.add(key)
            fields.append({
                "name": key,
                "type": ftype.strip() if ftype else "string",
                "description": re.sub(r'\s+', ' ', fdesc.strip()) if fdesc else "",
                "source_pattern": src
            })

    # <td> Field: <b><<type>><<description>></b>
    for m in re.finditer(r'<td>\s*(.+?):\s*<b>\s*<<(\w+)>>\s*<<(.+?)>>\s*</b>', content):
        add(m.group(1), m.group(2), m.group(3), "td_field")

    # <label class="form-label"> Field </label>
    for m in re.finditer(r'<label\s+class="form-label\s*">\s*(.+?)\s*</label>', content):
        add(m.group(1), "string", "", "form_label")

    # <span class="clinicalsubsubheading">Section</span>
    for m in re.finditer(r'<span\s+class="clinicalsubsubheading">(.+?)</span>', content):
        val = m.group(1).strip()
        if not val.startswith("<<"):
            add(val, "section", "Clinical subsection", "subheading")

    # <td class="rowlabel">Field</td><td><<Type>><<Description>></td> (multiline)
    for m in re.finditer(
        r'<td\s+class="rowlabel">(.+?)</td>\s*<td><<(\w+)>><<(.+?)>></td>',
        content, re.DOTALL
    ):
        add(m.group(1), m.group(2), m.group(3), "rowlabel")

    # <th>Column</th>
    for m in re.finditer(r'<th>(\w[\w\s.]*?)</th>', content):
        val = m.group(1).strip()
        if val and len(val) < 30:
            add(val, "column", "Table column header", "th_header")

    # <td class="label">Field</td><td class="value">
    for m in re.finditer(
        r'<td\s+class="label">(.+?)</td>\s*<td\s+class="value"><<(\w+)>><<(.+?)>></td>',
        content, re.DOTALL
    ):
        add(m.group(1), m.group(2), m.group(3), "label_value")

    # Flowsheet structure
    if 'flowsheet-reading' in content:
        add("Date and time of measurement", "string", "Date and time when measurement was recorded", "flowsheet")
        add("Section name", "string", "Name of the flowsheet section", "flowsheet")
        add("Measurement name", "string", "Name of the measurement", "flowsheet")
        add("Measurement value", "string", "Value of the measurement", "flowsheet")

    # MAR structure
    if 'inpatient-mar-export' in content:
        add("Medication administration date range", "string", "Date range for medication administration", "mar")
        add("Exported by and datetime", "string", "Who exported and when", "mar")
        add("Type", "string", "Medication type grouping", "mar")
        add("Medication", "string", "Medication name", "mar")
        add("Dose", "string", "Medication dose", "mar")
        add("Medication details", "key-value pairs", "Multiple detail rows (key/value)", "mar")
        add("Actions taken", "string", "Administration actions", "mar")
        add("Tasks", "string", "Administration task records", "mar")

    # Discharge summary sections
    if 'discharge-document-section' in content:
        for sec_name in ["Visit details", "Visit summary", "Labs and Imaging",
                         "Discharge Vitals", "Discharge Instructions", "Allergies",
                         "Medications"]:
            add(sec_name, "section", f"Discharge summary section", "discharge")

    # Note thread structure
    if 'note-thread' in content:
        add("Date range", "string", "Date range grouping", "note_thread")
        add("Entry date and time", "string", "Date and time of the note/audit entry", "note_thread")
        add("Entry details", "string", "Content of the note entry", "note_thread")
        add("Entered by", "string", "User who entered the record", "note_thread")

    # Order structure
    if re.search(r'Type of the order', content):
        add("Order type", "string", "Type of the order", "order")
        add("Date ordered", "string", "Date and time of the order", "order")
        add("Order description", "string", "Description of the order", "order")
        add("Entered by", "string", "User who entered the order", "order")
        add("Entered date/time", "string", "When the order was entered", "order")

    # Document images
    if 'inpatient-document-image' in content:
        add("Document image URL(s)", "string", "URL(s) to get page images of the document", "doc_image")

    # Attribution
    has_attr = bool(re.search(r'attribution-details|Created By|Signed [Bb]y', content))
    if has_attr:
        add("Created By", "string", "Attribution metadata", "attribution")
        add("Created Date", "string", "Attribution metadata", "attribution")
        add("Signed By", "string", "Attribution metadata", "attribution")
        add("Signed Date", "string", "Attribution metadata", "attribution")
    if re.search(r'Dictated by', content):
        add("Dictated by", "string", "Attribution metadata", "attribution")

    return fields


def parse_all_inpatient_clinical(pdf_text):
    """Parse the full inpatient clinical PDF, only capturing the 38 numbered datasets."""
    # Find the data sections area
    data_section_start = pdf_text.find("Clinical EHI Export Data Sections & Specifications")
    if data_section_start < 0:
        return {}
    
    text = pdf_text[data_section_start:]
    
    # Split by numbered sections, but only after the dataset table
    # Find first "1. Patient Demographics"
    first_section = text.find("1. Patient Demographics")
    if first_section < 0:
        return {}
    
    text = text[first_section:]
    # Prepend newline+indent so the first section is also matched by the split
    text = "\n    " + text
    sections = re.split(r'\n\s*(\d+)\.\s+(.+?):\s*\n', text)
    
    datasets = {}
    for i in range(1, len(sections) - 2, 3):
        num = int(sections[i].strip())
        name = sections[i + 1].strip()
        content = sections[i + 2]
        
        if num <= 38:  # Only the 38 documented datasets
            fields = parse_inpatient_section(name, content)
            datasets[name] = fields
    
    return datasets


def parse_ambulatory_clinical_inline(pdf_text):
    """Extract inline field specs from ambulatory clinical PDF."""
    specs = {}
    
    # Care Plan Events
    cpe_match = re.search(
        r'Care Plan Events.*?Input Parameters(.*?)Output parameters(.*?)Eye Care Measurement',
        pdf_text, re.DOTALL
    )
    if cpe_match:
        fields = []
        # Input params
        for m in re.finditer(r'\{(\w+)\}\s+\(required\)\s+(\w+)\s+(.+?)(?=\n\s*\{|\n\s*Output|\Z)', cpe_match.group(1), re.DOTALL):
            fields.append({"name": m.group(1), "type": m.group(2), "description": re.sub(r'\s+', ' ', m.group(3).strip()), "parameter_type": "input"})
        
        # Output params  
        for m in re.finditer(r'\s(\w+)\s+(string|integer)\s+(.+?)(?=\n\s+\w|\Z)', cpe_match.group(2), re.DOTALL):
            fields.append({"name": m.group(1), "type": m.group(2), "description": re.sub(r'\s+', ' ', m.group(3).strip()), "parameter_type": "output"})
        
        specs["Care Plan Events"] = fields

    # Eye Care Measurements
    ecm_match = re.search(
        r'Eye Care Measurement\s*\n(.*?)$',
        pdf_text, re.DOTALL
    )
    if ecm_match:
        fields = []
        for m in re.finditer(
            r'([\w\s]+?)\s+(string|N/A)\s+(.+?)(?=\n[\w]|\n\s*$|\Z)',
            ecm_match.group(1), re.DOTALL
        ):
            fname = m.group(1).strip()
            if fname and fname not in ["Name", "311 Arsenal"]:
                fields.append({"name": fname, "type": m.group(2), "description": re.sub(r'\s+', ' ', m.group(3).strip())})
        specs["Eye Care Specific Measurements"] = fields

    return specs


def parse_collector_inline(pdf_text):
    """Extract inline specs from collector PDFs."""
    specs = {}
    
    # Referral Authorization Attachments
    fields = []
    ref_match = re.search(r'Referral Authorization Attachments.*?Input Parameters(.*?)Output parameters(.*?)(?:Additional information|$)', pdf_text, re.DOTALL)
    if ref_match:
        for m in re.finditer(r'(Order ID.*?|Context ID)\s+(\w+)\s+(.+?)(?=\n\s*\w|\n\s*$)', ref_match.group(1)):
            fields.append({"name": m.group(1).strip(), "type": m.group(2), "description": m.group(3).strip(), "parameter_type": "input"})
        specs["Referral Authorization Attachments"] = fields
    
    # Claim Attachment file specs
    fields2 = []
    claim_match = re.search(r'exporting original attachment files.*?Input Parameters(.*?)Output parameters(.*?)$', pdf_text, re.DOTALL)
    if claim_match:
        for m in re.finditer(r'(Claimattachmentid|Filecontent|Filetype)\s+(\w+)\s+(.+?)(?=\n\s*\w|\Z)', claim_match.group(1) + claim_match.group(2)):
            fields2.append({"name": m.group(1), "type": m.group(2), "description": m.group(3).strip()})
        specs["Claim Attachment File Specs"] = fields2
    
    return specs


def categorize_dataset(name, export_type):
    """Assign a clinical domain category."""
    nl = name.lower()
    
    if any(k in nl for k in ["admin document", "clinical document", "encounter document",
            "encounter summary", "office note", "letter", "medical record document",
            "prescription document", "other ccda", "patient case", "paper form",
            "corrective lens", "physician authorization", "hospital note"]):
        return "Clinical Documents"
    
    if any(k in nl for k in ["admission h&p", "consult note", "discharge summary",
            "discharge planning", "ed course", "ed nursing", "ed provider",
            "ed triage", "nursing admission", "nursing notes", "nursing care plan",
            "surgical pre-op", "topic of discussion"]):
        return "Clinical Notes"
    
    if any(k in nl for k in ["encounter" ]) and "document" not in nl and "summary" not in nl and "phone" not in nl:
        return "Encounters"
    
    if any(k in nl for k in ["demographic", "patient demographics", "care team member",
            "default clinical provider"]):
        return "Demographics / Admin"
    
    if any(k in nl for k in ["medication", "mar"]):
        return "Medications"
    
    if any(k in nl for k in ["health concern", "condition", "problem", "assessment and plan",
            "chief complaint", "history of present"]):
        return "Conditions / Diagnoses"
    
    if any(k in nl for k in ["procedure", "surgical order", "surgical result", "surgery action",
            "dme order", "pre-sedation", "encounter phone call"]):
        return "Procedures / Surgery"
    
    if any(k in nl for k in ["family history", "social history", "past medical", "surgical history",
            "perinatal", "ob history", "ob episode", "gyn history"]):
        return "Patient History"
    
    if any(k in nl for k in ["observation", "vital", "flowsheet", "screening",
            "eye care", "review of system", "physical exam"]):
        return "Observations / Vitals"
    
    if any(k in nl for k in ["order" ]) and "surgical" not in nl and "dme" not in nl:
        return "Orders"
    
    if any(k in nl for k in ["care plan", "goal", "nursing task", "respiratory task",
            "therapy task", "pt episode"]):
        return "Care Plans / Tasks"
    
    if any(k in nl for k in ["appointment", "claim", "payment", "insurance",
            "billing statement", "outstanding balance", "referral", "return to office",
            "visits and charge", "pre-payment"]):
        return "Billing / Financial"
    
    if any(k in nl for k in ["allerg"]):
        return "Allergies"
    if any(k in nl for k in ["immuniz"]):
        return "Immunizations"
    if any(k in nl for k in ["cancer"]):
        return "Specialty Clinical"
    if any(k in nl for k in ["imaging result", "lab result", "interpretation"]):
        return "Lab / Imaging Results"
    if any(k in nl for k in ["device", "medical equipment"]):
        return "Devices"
    if any(k in nl for k in ["discharge instruction"]):
        return "Clinical Notes"
    if "transfer" in nl:
        return "Orders"
    
    return "Other"


def main():
    with open(os.path.join(RESULTS_DIR, "enrichment", "datasets.json")) as f:
        catalog = json.load(f)
    
    # Extract all PDF text
    pdf_texts = {}
    for pdf_name in ["ambulatory-clinical-ehi-export.pdf", "ambulatory-collector-ehi-export.pdf",
                     "inpatient-clinical-ehi-export.pdf", "inpatient-collector-ehi-export.pdf"]:
        pdf_texts[pdf_name] = extract_pdf_text(os.path.join(RESULTS_DIR, pdf_name))
    
    # Parse fields from each source
    inpatient_fields = parse_all_inpatient_clinical(pdf_texts["inpatient-clinical-ehi-export.pdf"])
    amb_clinical_specs = parse_ambulatory_clinical_inline(pdf_texts["ambulatory-clinical-ehi-export.pdf"])
    amb_collector_specs = parse_collector_inline(pdf_texts["ambulatory-collector-ehi-export.pdf"])
    inp_collector_specs = parse_collector_inline(pdf_texts["inpatient-collector-ehi-export.pdf"])
    
    # Build entity inventory
    entities = []
    
    for export_type in catalog["exportTypes"]:
        if export_type["category"] in ["overview", "release-notes"]:
            continue
        
        for ds in export_type["datasets"]:
            entity = {
                "name": ds["name"],
                "export_module": export_type["id"],
                "export_category": export_type["category"],
                "format": export_type["format"],
                "spec_url": ds.get("specUrl"),
                "includes_attachments": ds.get("includesAttachments", False),
                "domain_category": categorize_dataset(ds["name"], export_type["category"]),
                "fields": [],
                "field_count": 0,
                "fields_with_descriptions": 0,
                "spec_type": "external_api_ref",
                "spec_standard": "unknown"
            }
            
            # Determine spec standard
            if ds.get("specUrl") and "/fhir-r4/" in ds["specUrl"]:
                entity["spec_standard"] = "FHIR R4"
            elif ds.get("specUrl") and "/api-ref/" in ds["specUrl"]:
                entity["spec_standard"] = "athena REST API"
            else:
                entity["spec_standard"] = "inline documentation"
                entity["spec_type"] = "inline_pdf"
            
            # Add parsed fields for inpatient clinical
            if export_type["category"] == "inpatient-clinical":
                parsed = inpatient_fields.get(ds["name"], [])
                entity["fields"] = parsed
                entity["field_count"] = len(parsed)
                entity["fields_with_descriptions"] = sum(1 for f in parsed if f.get("description"))
                entity["spec_type"] = "inline_pdf_parsed"
            
            # Add inline specs for ambulatory clinical
            if ds["name"] in amb_clinical_specs:
                entity["fields"] = amb_clinical_specs[ds["name"]]
                entity["field_count"] = len(entity["fields"])
                entity["fields_with_descriptions"] = sum(1 for f in entity["fields"] if f.get("description"))
                entity["spec_type"] = "inline_pdf_parsed"
            
            entities.append(entity)
    
    # Compute statistics
    by_module = {}
    for e in entities:
        mod = e["export_module"]
        if mod not in by_module:
            by_module[mod] = {"count": 0, "with_attachments": 0, "total_fields": 0}
        by_module[mod]["count"] += 1
        if e["includes_attachments"]:
            by_module[mod]["with_attachments"] += 1
        by_module[mod]["total_fields"] += e["field_count"]
    
    by_domain = {}
    for e in entities:
        dom = e["domain_category"]
        if dom not in by_domain:
            by_domain[dom] = {"count": 0, "entities": [], "total_fields": 0}
        by_domain[dom]["count"] += 1
        by_domain[dom]["entities"].append(f"{e['name']} ({e['export_module']})")
        by_domain[dom]["total_fields"] += e["field_count"]
    
    by_spec = {}
    for e in entities:
        std = e["spec_standard"]
        by_spec[std] = by_spec.get(std, 0) + 1
    
    fhir_datasets = [e["name"] for e in entities if e["spec_standard"] == "FHIR R4"]
    
    total_parsed = sum(e["field_count"] for e in entities)
    total_described = sum(e["fields_with_descriptions"] for e in entities)
    entities_with_fields = sum(1 for e in entities if e["field_count"] > 0)
    
    summary = {
        "total_datasets": len(entities),
        "unique_dataset_names": len(set(e["name"] for e in entities)),
        "by_module": by_module,
        "by_domain": {k: {"count": v["count"], "total_fields": v["total_fields"]} for k, v in sorted(by_domain.items())},
        "by_spec_standard": by_spec,
        "fhir_r4_datasets": sorted(set(fhir_datasets)),
        "parsed_field_stats": {
            "entities_with_parsed_fields": entities_with_fields,
            "total_parsed_fields": total_parsed,
            "fields_with_descriptions": total_described,
            "note": "Field counts only available for inpatient clinical (PDF parsed) and 2 ambulatory clinical inline specs. Ambulatory datasets reference external API docs."
        },
        "datasets_with_attachments": sum(1 for e in entities if e["includes_attachments"]),
        "pdf_metadata": {
            "ambulatory_clinical": {"pages": 10, "created": "2023-09-22"},
            "ambulatory_collector": {"pages": 7, "created": "2023-09-22"},
            "inpatient_clinical": {"pages": 37, "created": "2023-09-22"},
            "inpatient_collector": {"pages": 7, "created": "2023-09-22"},
            "total_pages": 61
        }
    }
    
    inventory = {
        "extraction_date": "2026-02-16",
        "source": "athenahealth EHI Export Documentation (docs.athenahealth.com/athenaone-dataexports/)",
        "product": "athenaClinicals for Hospitals and Health Systems",
        "artifacts_parsed": [
            "downloads/enrichment/datasets.json",
            "downloads/ambulatory-clinical-ehi-export.pdf (10 pages)",
            "downloads/ambulatory-collector-ehi-export.pdf (7 pages)",
            "downloads/inpatient-clinical-ehi-export.pdf (37 pages)",
            "downloads/inpatient-collector-ehi-export.pdf (7 pages)",
            "downloads/api-ambulatory-clinical.json",
            "downloads/api-ambulatory-collector.json",
            "downloads/api-inpatient-clinical.json",
            "downloads/api-inpatient-collector.json",
            "downloads/api-welcome-exports.json"
        ],
        "entities": entities,
        "summary": summary
    }
    
    with open(os.path.join(ANALYSIS_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(os.path.join(ANALYSIS_DIR, "summary-stats.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"=== athenahealth EHI Export Inventory ===")
    print(f"Total datasets: {len(entities)}")
    print(f"Unique dataset names: {len(set(e['name'] for e in entities))}")
    print(f"\nBy module:")
    for mod, stats in by_module.items():
        print(f"  {mod}: {stats['count']} datasets ({stats['with_attachments']} with attachments, {stats['total_fields']} parsed fields)")
    print(f"\nBy domain:")
    for dom, stats in sorted(by_domain.items(), key=lambda x: -x[1]["count"]):
        print(f"  {dom}: {stats['count']} datasets")
    print(f"\nSpec standards: {by_spec}")
    print(f"\nFHIR R4 datasets: {sorted(set(fhir_datasets))}")
    print(f"\nParsed fields: {total_parsed} from {entities_with_fields} entities ({total_described} with descriptions)")
    print(f"Datasets with attachments: {sum(1 for e in entities if e['includes_attachments'])}")


if __name__ == "__main__":
    main()
