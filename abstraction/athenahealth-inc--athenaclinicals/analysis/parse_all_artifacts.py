#!/usr/bin/env python3
"""
Parse all athenahealth EHI export artifacts and produce full-entity-inventory.json
and summary statistics.

Reads:
  - downloads/enrichment/datasets.json (structured dataset catalog from Contentful API)
  - PDFs (text extracted via pdftotext) for field-level specs
  - API JSON files for additional inline specs

Outputs:
  - full-entity-inventory.json: complete machine-readable inventory
  - summary-stats.json: aggregate statistics
"""

import json
import re
import subprocess
import os
import sys

RESULTS_DIR = "/home/jmandel/hobby/ehi-export-analysis/results/athenahealth-inc--athenaclinicals/downloads"
ANALYSIS_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/athenahealth-inc--athenaclinicals/analysis"


def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout


def parse_inpatient_clinical_fields(text):
    """Parse the inpatient clinical PDF to extract fields per dataset."""
    datasets = {}
    
    # Split by numbered dataset sections
    # Pattern: number followed by period, space, dataset name, colon
    sections = re.split(r'\n\s+(\d+)\.\s+(.+?):\s*\n', text)
    
    # sections[0] is preamble, then groups of 3: (number, name, content)
    for i in range(1, len(sections) - 2, 3):
        num = sections[i].strip()
        name = sections[i + 1].strip()
        content = sections[i + 2]
        
        # Extract fields from the HTML template specs
        fields = []
        
        # Pattern 1: <td> Field: <b><<type>><<description>></b>
        td_fields = re.findall(
            r'<td>\s*(.+?):\s*<b>\s*<<(\w+)>>\s*<<(.+?)>>\s*</b>',
            content
        )
        for fname, ftype, fdesc in td_fields:
            fields.append({
                "name": fname.strip(),
                "type": ftype.strip(),
                "description": fdesc.strip()
            })
        
        # Pattern 2: <label class="form-label"> Field </label>
        label_fields = re.findall(
            r'<label\s+class="form-label\s*">\s*(.+?)\s*</label>',
            content
        )
        for lf in label_fields:
            if lf.strip() and lf.strip() not in [f["name"] for f in fields]:
                fields.append({
                    "name": lf.strip(),
                    "type": "string",
                    "description": ""
                })
        
        # Pattern 3: <span class="clinicalsubsubheading">Section</span>
        subheadings = re.findall(
            r'<span\s+class="clinicalsubsubheading">(.+?)</span>',
            content
        )
        for sh in subheadings:
            if sh.strip() and sh.strip() not in [f["name"] for f in fields]:
                fields.append({
                    "name": sh.strip(),
                    "type": "section",
                    "description": f"Clinical subsection: {sh.strip()}"
                })
        
        # Pattern 4: sectionname='XXX' attributes
        section_names = re.findall(
            r'sectionname=[\'"](\w+)[\'"]',
            content
        )
        for sn in section_names:
            readable = re.sub(r'([A-Z])', r' \1', sn).strip()
            if readable not in [f["name"] for f in fields]:
                fields.append({
                    "name": readable,
                    "type": "section_ref",
                    "description": f"HTML section reference: {sn}"
                })
        
        # Pattern 5: div class identifiers for structured sections
        div_sections = re.findall(
            r'<div\s+class=[\'"]([^"\']+?)[\'"]',
            content
        )
        
        # Attribution metadata
        has_attribution = bool(re.search(r'attribution-details|Created By|Signed [Bb]y|Entered by|Dictated by', content))
        if has_attribution:
            for attr in ["Created By", "Created Date", "Signed By", "Signed Date"]:
                if attr not in [f["name"] for f in fields]:
                    fields.append({
                        "name": attr,
                        "type": "string",
                        "description": "Attribution metadata"
                    })
        
        # Check for additional attributions
        if re.search(r'Dictated by', content):
            for attr in ["Dictated by", "Entered by"]:
                if attr not in [f["name"] for f in fields]:
                    fields.append({
                        "name": attr,
                        "type": "string",
                        "description": "Attribution metadata"
                    })
        
        datasets[name] = {
            "fields": fields,
            "field_count": len(fields),
            "has_attribution": has_attribution,
            "raw_content_length": len(content)
        }
    
    return datasets


def parse_ambulatory_clinical_inline_specs(pdf_text):
    """Extract the inline field specs for Care Plan Events and Eye Care Measurements."""
    specs = {}
    
    # Care Plan Events - extract input and output parameters
    care_plan_match = re.search(
        r'Care Plan Events.*?Input Parameters(.*?)Output parameters(.*?)Eye Care',
        pdf_text, re.DOTALL
    )
    if care_plan_match:
        input_text = care_plan_match.group(1)
        output_text = care_plan_match.group(2)
        
        fields = []
        # Parse table rows: Name Type Description
        for section, text_block in [("input", input_text), ("output", output_text)]:
            rows = re.findall(
                r'\{?(\w+)\}?\s+(?:\(required\)\s+)?(integer|string)\s+(.+?)(?=\n\s*\{|\n\s*$|\Z)',
                text_block, re.DOTALL
            )
            for fname, ftype, fdesc in rows:
                fields.append({
                    "name": fname.strip(),
                    "type": ftype.strip(),
                    "description": re.sub(r'\s+', ' ', fdesc.strip()),
                    "parameter_type": section
                })
        
        specs["Care Plan Events"] = fields
    
    # Eye Care Measurements
    eye_care_match = re.search(
        r'Eye Care Measurement(.*?)$',
        pdf_text, re.DOTALL
    )
    if eye_care_match:
        eye_text = eye_care_match.group(1)
        rows = re.findall(
            r'([\w\s]+?)\s+(string|N/A)\s+(.+?)(?=\n\s*[\w]|\Z)',
            eye_text, re.DOTALL
        )
        fields = []
        for fname, ftype, fdesc in rows:
            fname = fname.strip()
            if fname and fname not in ["Name", "311 Arsenal"]:
                fields.append({
                    "name": fname,
                    "type": ftype.strip(),
                    "description": re.sub(r'\s+', ' ', fdesc.strip())
                })
        specs["Eye Care Specific Measurements"] = fields
    
    return specs


def parse_collector_inline_specs(pdf_text):
    """Extract referral auth and claim attachment specs from collector PDFs."""
    specs = {}
    
    # Referral Authorization Attachments
    ref_match = re.search(
        r'Referral Authorization Attachments.*?Input Parameters(.*?)Output parameters(.*?)(?:Additional information|$)',
        pdf_text, re.DOTALL
    )
    if ref_match:
        fields = []
        input_rows = re.findall(r'(Order ID|Context ID)\s+(\w+)\s+(.+?)(?=\n\s*\w|\n\s*$)', ref_match.group(1))
        for fname, ftype, fdesc in input_rows:
            fields.append({"name": fname.strip(), "type": ftype.strip(), "description": fdesc.strip(), "parameter_type": "input"})
        output_rows = re.findall(r'(Response elements)\s+(\w+)\s+(.+?)(?=\n\s*$)', ref_match.group(2), re.DOTALL)
        for fname, ftype, fdesc in output_rows:
            fields.append({"name": fname.strip(), "type": ftype.strip(), "description": re.sub(r'\s+', ' ', fdesc.strip()), "parameter_type": "output"})
        specs["Referral Authorization Attachments"] = fields
    
    # Claim Attachments
    claim_match = re.search(
        r'exporting original attachment files of claims.*?Input Parameters(.*?)Output parameters(.*?)$',
        pdf_text, re.DOTALL
    )
    if claim_match:
        fields = []
        input_rows = re.findall(r'(Claimattachmentid)\s+(\w+)\s+(.+?)(?=\n)', claim_match.group(1))
        for fname, ftype, fdesc in input_rows:
            fields.append({"name": fname.strip(), "type": ftype.strip(), "description": fdesc.strip(), "parameter_type": "input"})
        output_rows = re.findall(r'(Filecontent|Filetype)\s+(\w+)\s+(.+?)(?=\n\s*\w|\Z)', claim_match.group(2))
        for fname, ftype, fdesc in output_rows:
            fields.append({"name": fname.strip(), "type": ftype.strip(), "description": fdesc.strip(), "parameter_type": "output"})
        specs["Claim Attachment Specs"] = fields
    
    return specs


def categorize_dataset(name, export_type):
    """Assign a clinical domain category based on dataset name."""
    name_lower = name.lower()
    
    clinical_doc = ["admin documents", "clinical documents", "encounter documents", 
                    "encounter summary", "office note", "letters", "letter action notes",
                    "medical record documents", "prescription documents", "other ccdas",
                    "patient cases", "paper forms", "corrective lens", "physician authorization"]
    
    clinical_notes = ["admission h&p", "consult notes", "discharge summary", 
                      "discharge planning", "ed course", "ed nursing", "ed provider",
                      "ed triage", "hospital notes", "nursing admission notes",
                      "nursing notes", "nursing care plan", "surgical pre-op notes",
                      "topic of discussion"]
    
    encounters = ["encounters", "encounter phone call"]
    
    demographics_admin = ["demographics", "patient demographics", "care team members",
                         "default clinical providers"]
    
    medications = ["medications", "medication administration"]
    
    conditions = ["health concerns", "assessment and plan", "chief complaint"]
    
    procedures = ["procedures", "procedure roles", "procedure times", 
                  "procedure timeout", "procedure vitals", "pre-sedation",
                  "surgical orders", "surgical results", "surgery action",
                  "dme orders"]
    
    history = ["family history", "social history", "past medical history",
               "surgical history", "history of present illness", "perinatal history",
               "ob history", "ob episode", "gyn history"]
    
    observations = ["observations", "vitals", "flowsheet", "screening",
                    "eye care", "review of systems", "physical exam"]
    
    orders = ["orders", "transfer orders", "admission order"]
    
    care_plan = ["care plan", "goals", "nursing care plan", "nursing tasks",
                 "respiratory tasks", "therapy tasks", "pt episode"]
    
    billing = ["appointments", "appointment ticklers", "claim", "demographics",
               "payment", "patient insurance", "patient outstanding",
               "billing statements", "payment plans", "pre-payment plans",
               "referral/auth", "return to office", "visits and charge"]
    
    for keyword in clinical_doc:
        if keyword in name_lower:
            return "Clinical Documents"
    for keyword in clinical_notes:
        if keyword in name_lower:
            return "Clinical Notes"
    for keyword in encounters:
        if keyword in name_lower:
            return "Encounters"
    for keyword in medications:
        if keyword in name_lower:
            return "Medications"
    for keyword in conditions:
        if keyword in name_lower:
            return "Conditions / Diagnoses"
    for keyword in procedures:
        if keyword in name_lower:
            return "Procedures / Surgery"
    for keyword in history:
        if keyword in name_lower:
            return "Patient History"
    for keyword in observations:
        if keyword in name_lower:
            return "Observations / Vitals"
    for keyword in orders:
        if keyword in name_lower:
            return "Orders"
    for keyword in care_plan:
        if keyword in name_lower:
            return "Care Plans / Tasks"
    
    if "collector" in export_type:
        for keyword in billing:
            if keyword in name_lower:
                return "Billing / Financial"
    
    if "allergies" in name_lower:
        return "Allergies"
    if "immuniz" in name_lower:
        return "Immunizations"
    if "cancer" in name_lower:
        return "Specialty Clinical"
    if "imaging" in name_lower or "lab result" in name_lower or "interpretation" in name_lower:
        return "Lab / Imaging Results"
    if "devices" in name_lower:
        return "Devices"
    if "discharge" in name_lower:
        return "Clinical Notes"
    
    return "Other"


def main():
    # Load the enrichment datasets.json
    with open(os.path.join(RESULTS_DIR, "enrichment", "datasets.json")) as f:
        catalog = json.load(f)
    
    # Extract PDF text
    pdf_texts = {}
    for pdf_name in ["ambulatory-clinical-ehi-export.pdf", "ambulatory-collector-ehi-export.pdf",
                     "inpatient-clinical-ehi-export.pdf", "inpatient-collector-ehi-export.pdf"]:
        pdf_path = os.path.join(RESULTS_DIR, pdf_name)
        pdf_texts[pdf_name] = extract_pdf_text(pdf_path)
    
    # Parse inpatient clinical field specs
    inpatient_fields = parse_inpatient_clinical_fields(
        pdf_texts["inpatient-clinical-ehi-export.pdf"]
    )
    
    # Parse ambulatory clinical inline specs
    amb_clinical_specs = parse_ambulatory_clinical_inline_specs(
        pdf_texts["ambulatory-clinical-ehi-export.pdf"]
    )
    
    # Parse collector inline specs
    amb_collector_specs = parse_collector_inline_specs(
        pdf_texts["ambulatory-collector-ehi-export.pdf"]
    )
    inp_collector_specs = parse_collector_inline_specs(
        pdf_texts["inpatient-collector-ehi-export.pdf"]
    )
    
    # Build the full entity inventory
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
                "spec_type": "external_api_ref" if ds.get("specUrl") else "inline_pdf",
                "domain_category": categorize_dataset(ds["name"], export_type["category"]),
                "fields": [],
                "field_count": 0,
                "fields_with_descriptions": 0
            }
            
            # Add parsed fields from inpatient clinical PDF
            if export_type["category"] == "inpatient-clinical":
                matching = inpatient_fields.get(ds["name"])
                if matching:
                    entity["fields"] = matching["fields"]
                    entity["field_count"] = matching["field_count"]
                    entity["fields_with_descriptions"] = sum(
                        1 for f in matching["fields"] if f.get("description")
                    )
                    entity["has_attribution"] = matching.get("has_attribution", False)
                    entity["spec_type"] = "inline_pdf_parsed"
            
            # Add inline specs for ambulatory clinical
            if ds["name"] in amb_clinical_specs:
                entity["fields"] = amb_clinical_specs[ds["name"]]
                entity["field_count"] = len(entity["fields"])
                entity["fields_with_descriptions"] = sum(
                    1 for f in entity["fields"] if f.get("description")
                )
                entity["spec_type"] = "inline_pdf_parsed"
            
            # Add inline specs for eye care
            if ds["name"] in amb_clinical_specs:
                pass  # already handled above
            
            # Determine if FHIR-based
            if ds.get("specUrl") and "/fhir-r4/" in ds["specUrl"]:
                entity["spec_standard"] = "FHIR R4"
            elif ds.get("specUrl") and "/api-ref/" in ds["specUrl"]:
                entity["spec_standard"] = "athena REST API"
            else:
                entity["spec_standard"] = "inline documentation"
            
            entities.append(entity)
    
    # Count unique datasets (deduplicate across ambulatory/inpatient collector)
    all_names = [e["name"] for e in entities]
    unique_names = set(all_names)
    
    # Compute summary statistics
    by_module = {}
    for e in entities:
        mod = e["export_module"]
        if mod not in by_module:
            by_module[mod] = {"count": 0, "with_attachments": 0}
        by_module[mod]["count"] += 1
        if e["includes_attachments"]:
            by_module[mod]["with_attachments"] += 1
    
    by_domain = {}
    for e in entities:
        dom = e["domain_category"]
        if dom not in by_domain:
            by_domain[dom] = {"count": 0, "entities": []}
        by_domain[dom]["count"] += 1
        by_domain[dom]["entities"].append(e["name"])
    
    by_spec_standard = {}
    for e in entities:
        std = e.get("spec_standard", "unknown")
        by_spec_standard[std] = by_spec_standard.get(std, 0) + 1
    
    # Count fields from parsed entities
    total_parsed_fields = sum(e["field_count"] for e in entities)
    total_described = sum(e["fields_with_descriptions"] for e in entities)
    entities_with_parsed_fields = sum(1 for e in entities if e["field_count"] > 0)
    
    # FHIR vs proprietary breakdown
    fhir_datasets = [e for e in entities if e.get("spec_standard") == "FHIR R4"]
    api_datasets = [e for e in entities if e.get("spec_standard") == "athena REST API"]
    inline_datasets = [e for e in entities if e.get("spec_standard") == "inline documentation"]
    
    # Ambulatory clinical dataset count from PDF (verify)
    amb_clin_pdf_datasets = []
    for line in pdf_texts["ambulatory-clinical-ehi-export.pdf"].split("\n"):
        # Look for dataset name rows in the table
        pass
    
    summary = {
        "total_datasets": len(entities),
        "unique_dataset_names": len(unique_names),
        "by_module": by_module,
        "by_domain": {k: {"count": v["count"], "entities": v["entities"]} for k, v in sorted(by_domain.items())},
        "by_spec_standard": by_spec_standard,
        "parsed_field_stats": {
            "entities_with_parsed_fields": entities_with_parsed_fields,
            "total_parsed_fields": total_parsed_fields,
            "total_described_fields": total_described
        },
        "fhir_datasets": [e["name"] for e in fhir_datasets],
        "fhir_dataset_count": len(fhir_datasets),
        "api_ref_dataset_count": len(api_datasets),
        "inline_doc_dataset_count": len(inline_datasets),
        "datasets_with_attachments": sum(1 for e in entities if e["includes_attachments"]),
        "pdf_metadata": {
            "ambulatory_clinical": {"pages": 10, "created": "2023-09-22"},
            "ambulatory_collector": {"pages": 7, "created": "2023-09-22"},
            "inpatient_clinical": {"pages": 37, "created": "2023-09-22"},
            "inpatient_collector": {"pages": 7, "created": "2023-09-22"}
        }
    }
    
    # Write outputs
    inventory = {
        "extraction_date": "2026-02-16",
        "source": "athenahealth EHI Export Documentation",
        "artifacts_parsed": [
            "downloads/enrichment/datasets.json",
            "downloads/ambulatory-clinical-ehi-export.pdf",
            "downloads/ambulatory-collector-ehi-export.pdf", 
            "downloads/inpatient-clinical-ehi-export.pdf",
            "downloads/inpatient-collector-ehi-export.pdf"
        ],
        "entities": entities,
        "summary": summary
    }
    
    with open(os.path.join(ANALYSIS_DIR, "full-entity-inventory.json"), "w") as f:
        json.dump(inventory, f, indent=2)
    
    with open(os.path.join(ANALYSIS_DIR, "summary-stats.json"), "w") as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print(f"Total datasets: {len(entities)}")
    print(f"Unique dataset names: {len(unique_names)}")
    print(f"\nBy module:")
    for mod, stats in by_module.items():
        print(f"  {mod}: {stats['count']} datasets ({stats['with_attachments']} with attachments)")
    print(f"\nBy domain category:")
    for dom, stats in sorted(by_domain.items(), key=lambda x: -x[1]["count"]):
        print(f"  {dom}: {stats['count']} datasets")
    print(f"\nBy spec standard:")
    for std, count in by_spec_standard.items():
        print(f"  {std}: {count}")
    print(f"\nParsed fields (from inpatient clinical PDF + inline specs):")
    print(f"  Entities with parsed fields: {entities_with_parsed_fields}")
    print(f"  Total parsed fields: {total_parsed_fields}")
    print(f"  Fields with descriptions: {total_described}")
    print(f"\nFHIR R4 datasets: {[e['name'] for e in fhir_datasets]}")


if __name__ == "__main__":
    main()
