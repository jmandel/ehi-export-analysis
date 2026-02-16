#!/usr/bin/env python3
"""
Parse RWT Measure #3 (b)(10) data from the CY 2025 Real World Testing PDF.
Extracts the EHI export usage statistics.
"""

import json
import subprocess
import re

PDF_FILE = "../../../results/patient-first--pas/downloads/PatientFirst_Real_World_Test_Results_CY2025.pdf"
OUTPUT_FILE = "rwt_b10_data.json"

# Extract text from the PDF
result = subprocess.run(
    ["pdftotext", "-layout", PDF_FILE, "-"],
    capture_output=True, text=True
)
pdf_text = result.stdout

# Find the b(10) section - skip the TOC entry, find the actual section header
# The TOC has "RWT Measure #3. Number of EHI Exports Run ......." 
# The actual section starts with "RWT Measure #3.               Number of EHI Exports Run"
b10_matches = [m.start() for m in re.finditer(r'RWT Measure #3', pdf_text)]
# Use the last occurrence (actual section, not TOC)
b10_start = b10_matches[-1] if b10_matches else -1
b10_end_matches = [m.start() for m in re.finditer(r'RWT Measure #4', pdf_text)]
b10_end = b10_end_matches[-1] if b10_end_matches else -1
b10_section = pdf_text[b10_start:b10_end] if b10_end != -1 else pdf_text[b10_start:]

# Extract the metric name (handle extra whitespace from PDF layout)
metric_match = re.search(r'Testing Metric/Measurement:\s*(.+)', b10_section)
metric_name = metric_match.group(1).strip() if metric_match else "Unknown"

# Extract state results
state_results = {}
for match in re.finditer(r'^\s*(VA|MD|PA|NJ)\s+(\d+|-)\s*$', b10_section, re.MULTILINE):
    state = match.group(1)
    value = 0 if match.group(2) == '-' else int(match.group(2))
    state_results[state] = value

total = sum(state_results.values())

# Extract the reporting interval
interval_match = re.search(r'Reporting Interval:\s*(.+)', b10_section)
interval = interval_match.group(1).strip() if interval_match else "Unknown"

# Extract analysis text
analysis_match = re.search(r'Analysis and Key Findings\s*\n(.+?)(?:Non-Conformities|$)', b10_section, re.DOTALL)
analysis_text = analysis_match.group(1).strip() if analysis_match else ""

data = {
    "measure": "RWT Measure #3",
    "criteria": "315(b)(10)",
    "title": "Number of EHI Exports Run",
    "metric_label": metric_name,
    "reporting_interval": interval,
    "state_results": state_results,
    "total_exports": total,
    "annualized_estimate": total * 4,
    "analysis_text": analysis_text,
    "red_flag": "The metric is labeled 'Number of C-CDA Batch Exports Sent' despite being associated with b(10) EHI Export. This suggests the vendor may be conflating C-CDA batch export with the full EHI export (which per their own documentation is a multi-format ZIP with 7 categories including DICOM, EML, JSON, etc.).",
    "pdf_source": "PatientFirst_Real_World_Test_Results_CY2025.pdf",
    "pdf_pages": "13-14 of 23"
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(data, f, indent=2)

print(f"RWT Measure #3 - b(10) EHI Export")
print(f"Metric label: {metric_name}")
print(f"Reporting interval: {interval}")
print(f"Results by state:")
for state, count in state_results.items():
    print(f"  {state}: {count}")
print(f"Total Q1 2025: {total}")
print(f"Annualized: ~{total * 4}")
print(f"\nRed flag: Metric labeled '{metric_name}' for b(10)")
print(f"\nOutput written to {OUTPUT_FILE}")
