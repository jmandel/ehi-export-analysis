#!/usr/bin/env python3
"""Parse the SolidPractice b10 exportable data content PDF into structured JSON."""

import json
import re
import subprocess
import sys

def parse_b10_pdf():
    result = subprocess.run(
        ["pdftotext", "-layout", "../downloads/SolidPractice-b10-exportable-data-content.pdf", "-"],
        capture_output=True, text=True
    )
    text = result.stdout

    entries = []
    # Parse each numbered line
    # Pattern: number, data element name, data description, then X marks for formats
    lines = text.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Match lines starting with a number
        m = re.match(r'^\s*(\d+)\s+(.+)', lines[i])
        if m:
            num = int(m.group(1))
            rest = m.group(2)
            
            # Need to parse the data element, description, and format columns
            # The PDF is laid out with columns; let's use positional parsing on raw line
            raw = lines[i]
            
            # Determine format support from X marks in the rightmost columns
            # Based on PDF layout, columns are roughly:
            # Col ~0-3: No
            # Col ~4-40: Data Element
            # Col ~41-85: Data Description  
            # Col ~86-107: Computable PDF Export
            # Col ~108-125: CCD XML Export
            # Col ~126+: JSON
            
            # Let's look at the raw positions
            computable_pdf = False
            ccd_xml = False
            json_export = False
            
            # Check for X/x marks in the format columns
            # For the first page (items 1-30), layout is different from pages 2-3
            # Let's just check if X appears after the description
            
            # Simple approach: find all X/x positions
            upper_x_positions = [j for j, c in enumerate(raw) if c == 'X']
            lower_x_positions = [j for j, c in enumerate(raw) if c == 'x']
            
            # Determine column boundaries from the header
            # From the extracted text, the header shows:
            # "Computable PDF Export CCD XML Export   JSON"
            # These appear at different positions on different pages
            
            # For page 1 items 1-30: X marks appear in CCD XML column (~pos 85+)
            # Item 30 has both CCD XML X and JSON X
            # For page 2-3 items 31+: X marks appear in Computable PDF or CCD XML columns
            
            # Let's use a heuristic based on position
            all_x_pos = upper_x_positions + lower_x_positions
            
            if num <= 30:
                # Page 1: format columns start around pos 85
                for pos in all_x_pos:
                    if pos > 70:
                        ccd_xml = True
                # Item 30 also has JSON
                if num == 30:
                    json_export = True  # Per documentation
            else:
                # Pages 2-3: different layout
                for pos in all_x_pos:
                    if pos > 50:
                        # Determine which column based on position
                        if pos < 70:
                            computable_pdf = True
                        else:
                            ccd_xml = True
            
            # Parse data element name and description
            # Remove the number prefix
            rest_text = rest.strip()
            
            # For items 1-30, format is: "Name    Description    X"
            # Split on multiple spaces
            parts = re.split(r'\s{3,}', rest_text)
            
            data_element = parts[0].strip() if len(parts) > 0 else ""
            data_description = parts[1].strip() if len(parts) > 1 else ""
            
            # Clean up: remove trailing X marks from description
            data_description = re.sub(r'\s+[Xx]\s*$', '', data_description)
            data_description = re.sub(r'\s+X\s+[Xx]?\s*$', '', data_description)
            
            # Handle multi-line entries (item 48, 75 have continuation lines)
            while i + 1 < len(lines):
                next_line = lines[i + 1]
                # Check if next line is NOT a new numbered entry and is not blank header
                next_m = re.match(r'^\s*(\d+)\s+', next_line)
                if next_m or next_line.strip() == '' or 'exportable data' in next_line.lower() or 'data element' in next_line.lower():
                    break
                # It's a continuation line
                continuation = next_line.strip()
                if continuation and not re.match(r'^No\s+Data', continuation):
                    # Remove any X marks
                    continuation = re.sub(r'\s+[Xx]\s*$', '', continuation)
                    if continuation.startswith('- ') or continuation.startswith('('):
                        data_description += ' ' + continuation
                    else:
                        data_description += ' ' + continuation
                i += 1
            
            entries.append({
                "number": num,
                "data_element": data_element,
                "description": data_description.strip(),
                "computable_pdf_export": computable_pdf,
                "ccd_xml_export": ccd_xml,
                "json_export": json_export
            })
        i += 1
    
    return entries

def main():
    entries = parse_b10_pdf()
    
    # Manual corrections based on careful reading of the PDF
    # Fix format columns based on the actual PDF content
    format_corrections = {
        # Items 1-29: CCD XML = True (all demographics in CCD XML)
        # Items 31-42: Computable PDF = True
        # Items 43-44: varying
        # Items 45-46: CCD XML with lowercase x
        # Item 47: Computable PDF = True, CCD XML = True  
        # Item 48: Computable PDF = True
        # Items 49-56: CCD XML = True
        # Items 57-62: CCD XML = True
        # Items 63-71: Computable PDF = True
        # Items 72-87: Computable PDF = True
    }
    
    # Based on careful re-reading of the extracted text:
    for e in entries:
        n = e["number"]
        if 1 <= n <= 29:
            e["ccd_xml_export"] = True
            e["computable_pdf_export"] = False
        elif n == 30:
            e["ccd_xml_export"] = True
            e["json_export"] = True
            e["computable_pdf_export"] = False
        elif 31 <= n <= 42:
            e["computable_pdf_export"] = False
            e["ccd_xml_export"] = True
        elif n == 43:
            e["computable_pdf_export"] = False
            e["ccd_xml_export"] = True
        elif n == 44:
            e["computable_pdf_export"] = False
            e["ccd_xml_export"] = True
        elif n in (45, 46):
            e["computable_pdf_export"] = False
            e["ccd_xml_export"] = True  # lowercase x
        elif n == 47:
            e["computable_pdf_export"] = True
            e["ccd_xml_export"] = False
        elif n == 48:
            e["computable_pdf_export"] = True
            e["ccd_xml_export"] = False
        elif 49 <= n <= 56:
            e["computable_pdf_export"] = False
            e["ccd_xml_export"] = True
        elif 57 <= n <= 62:
            e["computable_pdf_export"] = False
            e["ccd_xml_export"] = True
        elif 63 <= n <= 65:
            e["computable_pdf_export"] = True
            e["ccd_xml_export"] = False
        elif 66 <= n <= 71:
            e["computable_pdf_export"] = True
            e["ccd_xml_export"] = False
        elif 72 <= n <= 87:
            e["computable_pdf_export"] = True
            e["ccd_xml_export"] = False
    
    # Assign categories
    for e in entries:
        n = e["number"]
        if 1 <= n <= 29:
            e["category"] = "Patient Demographics"
        elif 30 <= n <= 35:
            e["category"] = "Medications & Pharmacy"
        elif 36 <= n <= 44:
            e["category"] = "Clinical Data"
        elif 45 <= n <= 47:
            e["category"] = "Labs & Imaging"
        elif n == 48:
            e["category"] = "Uploaded Documents"
        elif 49 <= n <= 56:
            e["category"] = "Insurance"
        elif 57 <= n <= 65:
            e["category"] = "Guarantor"
        elif 66 <= n <= 71:
            e["category"] = "Appointments"
        elif 72 <= n <= 87:
            e["category"] = "Billing / Receipts"
    
    # Output
    print(json.dumps(entries, indent=2))
    return entries

if __name__ == "__main__":
    main()
