#!/usr/bin/env python3
"""
Enhanced parser for the inpatient clinical PDF. Extracts structured fields from
HTML template specifications using multiple patterns found in the document.

Patterns detected:
1. <td> Field: <b><<type>><<description>></b>  (Patient Demographics)
2. <label class="form-label"> Field </label>     (Admission Order summary)
3. <span class="clinicalsubsubheading">Section</span>  (clinical subsections)
4. <td class="rowlabel">Field</td><td><<Type>><<Description>></td>  (Lab/Imaging)
5. <th>Column</th> patterns  (table headers in lab analytes)
6. <td class="label">Field</td>  (Orders)
7. <span class='flowsheet-reading-section-name'> + measurement name/value
8. div class patterns (MAR, discharge summary sections)
9. Attribution metadata (Created By, Signed By, etc.)

Outputs a detailed JSON of all parsed fields per dataset.
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


def parse_section(name, content):
    """Parse a single dataset section and extract all fields found."""
    fields = []
    seen = set()

    def add_field(fname, ftype, fdesc, pattern_src):
        key = fname.strip()
        if key and key not in seen and key not in ["311 Arsenal", ""]:
            seen.add(key)
            fields.append({
                "name": key,
                "type": ftype.strip() if ftype else "string",
                "description": re.sub(r'\s+', ' ', fdesc.strip()) if fdesc else "",
                "source_pattern": pattern_src
            })

    # Pattern 1: <td> Field: <b><<type>><<description>></b>
    for m in re.finditer(r'<td>\s*(.+?):\s*<b>\s*<<(\w+)>>\s*<<(.+?)>>\s*</b>', content):
        add_field(m.group(1), m.group(2), m.group(3), "td_field")

    # Pattern 2: <label class="form-label"> Field </label>
    for m in re.finditer(r'<label\s+class="form-label\s*">\s*(.+?)\s*</label>', content):
        add_field(m.group(1), "string", "", "form_label")

    # Pattern 3: <span class="clinicalsubsubheading">Section</span>
    for m in re.finditer(r'<span\s+class="clinicalsubsubheading">(.+?)</span>', content):
        add_field(m.group(1), "section", f"Clinical subsection", "subheading")

    # Pattern 4: <td class="rowlabel">Field</td><td><<Type>><<Description>></td>
    for m in re.finditer(r'<td\s+class="rowlabel">(.+?)</td>\s*<td><<(\w+)>><<(.+?)>></td>', content):
        add_field(m.group(1), m.group(2), m.group(3), "rowlabel")

    # Pattern 5: <th>Column</th> in table headers
    for m in re.finditer(r'<th>(\w[\w\s.]*?)</th>', content):
        val = m.group(1).strip()
        if val and val not in ["colspan", "class"]:
            add_field(val, "column", "Table column header", "th_header")

    # Pattern 6: <td class="label">Field</td> <td class="value">
    for m in re.finditer(r'<td\s+class="label">(.+?)</td>\s*<td\s+class="value"><<(\w+)>><<(.+?)>></td>', content):
        add_field(m.group(1), m.group(2), m.group(3), "label_value")

    # Pattern 7: Flowsheet measurement structure
    if 'flowsheet-reading' in content:
        add_field("Date and time of measurement", "string", "Date and time when measurement was recorded", "flowsheet_structure")
        add_field("Section name", "string", "Name of the flowsheet section", "flowsheet_structure")
        add_field("Measurement name", "string", "Name of the measurement", "flowsheet_structure")
        add_field("Measurement value", "string", "Value of the measurement", "flowsheet_structure")

    # Pattern 8: MAR-specific fields
    if 'inpatient-mar-export' in content:
        add_field("Medication administration date range", "string", "Date range for medication administration", "mar_structure")
        add_field("Exported by and datetime", "string", "Who exported and when", "mar_structure")
        add_field("Type", "string", "Medication type grouping", "mar_structure")
        add_field("Medication", "string", "Medication name", "mar_structure")
        add_field("Dose", "string", "Medication dose", "mar_structure")
        add_field("Medication details", "key-value pairs", "Multiple detail rows (key/value)", "mar_structure")
        add_field("Actions taken", "string", "Administration actions", "mar_structure")
        add_field("Tasks", "string", "Administration task records", "mar_structure")

    # Pattern 9: Discharge summary sections
    if 'discharge-document' in content:
        sections_found = re.findall(r'class="([^"]*discharge[^"]*)"', content)
        for sec in sections_found:
            readable = sec.replace('-', ' ').replace('inpatient ', '').strip().title()
            if readable and readable not in seen:
                add_field(readable, "section", f"Discharge summary section: {sec}", "discharge_section")

    # Pattern 10: div class='note-thread' structure
    if 'note-thread' in content:
        add_field("Date and time", "string", "Date and time of the note/audit entry", "note_thread")
        add_field("Details/content", "string", "Content of the note entry", "note_thread")
        add_field("Entered by", "string", "User who entered the record", "note_thread")

    # Pattern 11: Order-specific
    if re.search(r'<h1>.*?Type of the order', content):
        add_field("Order type", "string", "Type of the order", "order_structure")
        add_field("Date ordered", "string", "Date and time of the order", "order_structure")
        add_field("Order description", "string", "Description of the order", "order_structure")
        add_field("Entered by", "string", "User who entered the order", "order_structure")
        add_field("Entered date/time", "string", "When the order was entered", "order_structure")

    # Pattern 12: Nursing tasks
    if 'task-log-row' in content or 'nursing-task' in content.lower():
        for m in re.finditer(r'class=[\'"]task-(\w+)[\'"]', content):
            field_name = m.group(1).replace('-', ' ').title()
            add_field(field_name, "string", f"Task field: {m.group(1)}", "task_structure")

    # Attribution metadata
    has_attribution = bool(re.search(r'attribution-details|Created By|Signed [Bb]y|Entered by|Dictated by', content))
    if has_attribution:
        for attr in ["Created By", "Created Date", "Signed By", "Signed Date"]:
            add_field(attr, "string", "Attribution metadata", "attribution")
        if re.search(r'Dictated by', content):
            add_field("Dictated by", "string", "Attribution metadata", "attribution")

    # Document image patterns
    if 'inpatient-document-image' in content or 'inpatient-document-print' in content:
        add_field("Document image URL", "string", "URL to get the image of the document", "doc_image")

    # sectionname attributes as reference
    for m in re.finditer(r'sectionname=[\'"](\w+)[\'"]', content):
        readable = re.sub(r'([A-Z])', r' \1', m.group(1)).strip()
        add_field(readable, "section_ref", f"HTML section reference: {m.group(1)}", "sectionname_attr")

    return {
        "fields": fields,
        "field_count": len(fields),
        "fields_with_descriptions": sum(1 for f in fields if f.get("description")),
        "has_attribution": has_attribution,
        "raw_content_length": len(content)
    }


def main():
    pdf_text = extract_pdf_text(os.path.join(RESULTS_DIR, "inpatient-clinical-ehi-export.pdf"))
    
    # Split into sections by numbered dataset headers
    sections = re.split(r'\n\s+(\d+)\.\s+(.+?):\s*\n', pdf_text)
    
    datasets = {}
    for i in range(1, len(sections) - 2, 3):
        num = sections[i].strip()
        name = sections[i + 1].strip()
        content = sections[i + 2]
        datasets[name] = parse_section(name, content)
    
    # Output
    total_fields = sum(d["field_count"] for d in datasets.values())
    total_described = sum(d["fields_with_descriptions"] for d in datasets.values())
    
    print(f"Parsed {len(datasets)} inpatient clinical datasets")
    print(f"Total fields extracted: {total_fields}")
    print(f"Fields with descriptions: {total_described}")
    print()
    
    for name, data in datasets.items():
        print(f"  {name}: {data['field_count']} fields ({data['fields_with_descriptions']} described)")
        for f in data["fields"]:
            desc_preview = f["description"][:60] if f["description"] else "(no desc)"
            print(f"    - {f['name']} [{f['type']}]: {desc_preview}")
    
    with open(os.path.join(ANALYSIS_DIR, "inpatient-clinical-fields.json"), "w") as f:
        json.dump(datasets, f, indent=2)
    
    return datasets


if __name__ == "__main__":
    main()
