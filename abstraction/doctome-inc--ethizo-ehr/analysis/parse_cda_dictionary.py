#!/usr/bin/env python3
"""Parse the CDA data dictionary from the ethizo EHI Export PDF.

Extracts sections, data elements, code systems from the pdftotext output.
Produces structured counts and a summary JSON.
"""

import json
import re
import subprocess
import sys

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/doctome-inc--ethizo-ehr/downloads/EHI-Export-b.10-Documentation-v2.pdf"

def extract_text():
    result = subprocess.run(
        ["pdftotext", "-layout", PDF_PATH, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_sections(text):
    """Parse CDA sections and their data elements from the PDF text."""
    sections = []
    current_section = None
    
    # Lines from the CDA data dictionary portion (pages 4-8)
    lines = text.split("\n")
    
    # Section headers are identified by bracketed OIDs or known section names
    section_pattern = re.compile(
        r'^([\w\s/()]+?)\s*\[([0-9.]+)\s*(?::\s*[\d-]+)?\]',
        re.IGNORECASE
    )
    # Also match sections without OIDs
    known_sections = [
        "Patient Demographics/Information",
        "Provider's name and office contact information",
        "Date and Location of visit",
        "Chief Complaint and Reason for visit",
    ]
    
    in_cda_section = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        # Detect start of CDA dictionary
        if "Sections in the CCD output" in stripped:
            in_cda_section = True
            continue
        
        # Detect end of CDA dictionary
        if "Patient Demographics and Insurance Details" in stripped and "2." in stripped:
            in_cda_section = False
            break
            
        if not in_cda_section:
            continue
        
        # Skip header rows
        if "Data Elements" in stripped and "XPATH" in stripped:
            continue
        if "Code System Name" in stripped:
            continue
            
        # Check for section header with OID
        match = section_pattern.match(stripped)
        if match:
            section_name = match.group(1).strip()
            oid = match.group(2).strip()
            current_section = {
                "name": section_name,
                "oid": oid,
                "elements": [],
                "code_systems": set()
            }
            sections.append(current_section)
            continue
        
        # Check for known sections without OID
        for ks in known_sections:
            if stripped.startswith(ks):
                current_section = {
                    "name": ks,
                    "oid": None,
                    "elements": [],
                    "code_systems": set()
                }
                sections.append(current_section)
                break
        
        # If we have a current section, try to parse data elements
        if current_section:
            # Data elements are typically the first column before whitespace
            # Skip lines that look like OIDs or xpath entries
            if stripped.startswith("2.16.840") or stripped.startswith("0.22."):
                continue
            
            # Extract code system names from the line
            code_systems_found = []
            for cs in ["SNOMED", "ICD10", "ICD-10", "CPT", "CPT-4", "LOINC", 
                       "RxNorm", "NDC", "CVX", "HCPCS", "GMDN",
                       "AdministrativeGender", "NCI"]:
                if cs in stripped:
                    code_systems_found.append(cs)
            
            for cs in code_systems_found:
                current_section["code_systems"].add(cs)
            
            # Check if this looks like a data element name (not a sub-xpath)
            # Elements are typically at the start of a line, may have xpath after
            parts = re.split(r'\s{2,}', stripped)
            if parts and len(parts[0]) > 1:
                element_name = parts[0].strip()
                # Filter out non-element lines
                if (not element_name.startswith("(") and 
                    not element_name.startswith("§") and
                    element_name not in ["Standard Referenced:", "Sections in the CCD output"] and
                    not element_name.startswith("2.16.840") and
                    not element_name.startswith("0.22.")):
                    current_section["elements"].append(element_name)
    
    return sections

def main():
    text = extract_text()
    sections = parse_sections(text)
    
    # Convert sets to lists for JSON serialization
    total_elements = 0
    total_code_systems = set()
    
    output = {
        "sections": [],
        "summary": {}
    }
    
    print("=" * 70)
    print("CDA DATA DICTIONARY ANALYSIS - ethizo EHR")
    print("=" * 70)
    print()
    
    for s in sections:
        element_count = len(s["elements"])
        total_elements += element_count
        total_code_systems.update(s["code_systems"])
        
        section_data = {
            "name": s["name"],
            "oid": s["oid"],
            "element_count": element_count,
            "elements": s["elements"],
            "code_systems": sorted(s["code_systems"])
        }
        output["sections"].append(section_data)
        
        print(f"Section: {s['name']}")
        if s["oid"]:
            print(f"  OID: {s['oid']}")
        print(f"  Elements: {element_count}")
        if s["code_systems"]:
            print(f"  Code Systems: {', '.join(sorted(s['code_systems']))}")
        for e in s["elements"]:
            print(f"    - {e}")
        print()
    
    output["summary"] = {
        "total_sections": len(sections),
        "total_elements": total_elements,
        "total_code_systems": len(total_code_systems),
        "code_systems_list": sorted(total_code_systems),
        "non_cda_exports": [
            {
                "name": "Patient Demographics and Insurance Details",
                "format": "CSV",
                "field_documentation": False,
                "notes": "No field-level documentation provided"
            },
            {
                "name": "Appointments",
                "format": "CSV",
                "field_documentation": False,
                "notes": "Future appointments only; no field-level documentation"
            },
            {
                "name": "Documents",
                "format": "PDF/JPG/PNG",
                "field_documentation": False,
                "notes": "Scanned/uploaded documents organized by patient chart number"
            },
            {
                "name": "FHIR Bulk Data Export",
                "format": "FHIR",
                "field_documentation": False,
                "notes": "Single sentence mention; no detailed documentation"
            }
        ]
    }
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total CDA sections: {len(sections)}")
    print(f"Total CDA data elements: {total_elements}")
    print(f"Total unique code systems: {len(total_code_systems)}")
    print(f"Code systems: {', '.join(sorted(total_code_systems))}")
    print()
    print("Non-CDA exports (no field documentation):")
    for item in output["summary"]["non_cda_exports"]:
        print(f"  - {item['name']} ({item['format']})")
    
    # Save JSON output
    with open("/home/jmandel/hobby/ehi-export-analysis/abstraction/doctome-inc--ethizo-ehr/analysis/cda_dictionary_analysis.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print()
    print("JSON output saved to analysis/cda_dictionary_analysis.json")

if __name__ == "__main__":
    main()
