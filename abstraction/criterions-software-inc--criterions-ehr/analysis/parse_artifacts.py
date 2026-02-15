#!/usr/bin/env python3
"""Parse Criterions EHR EHI export artifacts and produce structured summaries."""

import json
import re

# Parse the EHI Export Overview - extract the 22 C-CDA sections
with open("ehi-export-overview-text.txt") as f:
    overview_text = f.read()

# Extract bullet items (C-CDA sections)
ccda_sections = re.findall(r'•\s+(.+)', overview_text)
ccda_sections = [s.strip() for s in ccda_sections]

print("=== C-CDA Sections Listed in EHI Export Overview ===")
print(f"Total sections: {len(ccda_sections)}")
for i, s in enumerate(ccda_sections, 1):
    print(f"  {i}. {s}")

# Parse the Mandatory Disclosure - extract (b)(10) entry
with open("mandatory-disclosure-text.txt") as f:
    mandatory_text = f.read()

# Count total certification criteria listed
criteria = re.findall(r'170\.315\([a-z]\)\(\d+\)', mandatory_text)
# Deduplicate (some appear in description text of other criteria)
unique_criteria = sorted(set(criteria))
print(f"\n=== Mandatory Disclosure ===")
print(f"Total unique certification criteria referenced: {len(unique_criteria)}")

# Extract the (b)(10) entry
b10_match = re.search(r'§?170\.315\(b\)\(10\)[^\n]*\n(.*?)(?=\n\s*(?:§?170\.315|$))', mandatory_text, re.DOTALL)
if b10_match:
    b10_text = b10_match.group(0).strip()[:500]
    print(f"\n(b)(10) entry text:\n{b10_text}")

# Extract the (b)(6) entry for comparison
b6_match = re.search(r'170\.315\(b\)\(6\)[^\n]*\n(.*?)(?=\n\s*§?170\.315)', mandatory_text, re.DOTALL)
if b6_match:
    b6_text = b6_match.group(0).strip()[:500]
    print(f"\n(b)(6) entry text:\n{b6_text}")

# Summary output as JSON
summary = {
    "ccda_sections": ccda_sections,
    "ccda_section_count": len(ccda_sections),
    "b10_description": "Allow a practice to create individual and group exports of PHI without programming intervention.",
    "b6_description": "This functionality enables a user to electronically create a set of export summaries for all patients in C-CDA format that represents the most current clinical information about each patient.",
    "export_format": "C-CDA (XML)",
    "export_mechanism": "Email/Print Chart + CCDA download",
    "cost": "Included with Criterions EHR subscription (no additional charge for export itself)",
    "bulk_support": "Individual patients, groups of patients, or automated scheduled export",
    "data_dictionary": False,
    "sample_data": False,
    "schema_documentation": False,
    "total_artifacts": 3,
    "artifact_types": ["PDF (patient-facing overview)", "PDF (cures disclosure)", "PDF (mandatory disclosure)"]
}

with open("artifact-summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary saved to artifact-summary.json ===")
print(json.dumps(summary, indent=2))
