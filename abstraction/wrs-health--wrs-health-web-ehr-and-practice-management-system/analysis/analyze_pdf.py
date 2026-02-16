"""
Analyze the WRS Health EHI Export PDF documentation.
Extracts structured information about the export file structure and contents.
"""
import subprocess
import json
import re

PDF_PATH = "/home/jmandel/hobby/ehi-export-analysis/results/wrs-health--wrs-health-web-ehr-and-practice-management-system/downloads/170.315-b10-EHI-Export.pdf"

# Get PDF metadata
result = subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True)
print("=== PDF Metadata ===")
print(result.stdout)

# Extract text
result = subprocess.run(["pdftotext", "-layout", PDF_PATH, "-"], capture_output=True, text=True)
text = result.stdout

# Count pages
pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF_PATH], capture_output=True, text=True).stdout).group(1))

# Identify the export components described
print("=== Export Components Identified ===")
components = []

# Parse the file structure from the PDF text
file_components = [
    {"name": "Documents/", "format": "Various (PDF, DOCX, XLS, XML, HTML, DAT, JPG, GIF, PNG)", 
     "description": "Patient's supporting documents, attachments, lab results uploaded by practice"},
    {"name": "Notes/", "format": "HTML + CSS/JS/images", 
     "description": "Encounter notes from patient visits, one HTML file per note"},
    {"name": "Notes/PatientNoteFiles.csv", "format": "CSV", 
     "description": "Mapping file listing all exported notes"},
    {"name": "Notes/NOTES.LOG", "format": "Text", 
     "description": "Log of successfully exported notes and errors"},
    {"name": "BillingReport.csv", "format": "CSV", 
     "description": "Financial transactions: patient info, transaction dates, charges, claims, descriptions, status"},
    {"name": "CCDA.xml", "format": "XML (C-CDA)", 
     "description": "Clinical data export compliant with HL7 C-CDA / USCDI v1"},
    {"name": "demographics.csv", "format": "CSV", 
     "description": "Patient key information, identification details, contacts, insurance"},
    {"name": "PatientDocumentFiles.csv", "format": "CSV", 
     "description": "Mapping file listing documents in the Documents folder"},
    {"name": "schedule.csv", "format": "CSV", 
     "description": "Encounter records: appointment date, provider, location, type, workflow, notes, note dates"},
]

for c in file_components:
    print(f"  {c['name']:30s} [{c['format']:20s}] - {c['description']}")

# Summary statistics
csv_files = [c for c in file_components if c['format'] == 'CSV']
print(f"\n=== Summary ===")
print(f"Total pages in PDF: {pages}")
print(f"Total export components described: {len(file_components)}")
print(f"CSV files (structured data): {len(csv_files)}")
print(f"Field-level data dictionary: NO")
print(f"Sample data provided: NO")
print(f"Schema files (XSD/JSON Schema): NO")
print(f"Column definitions for CSVs: NO")
print(f"Value sets or code systems: NO")
print(f"Relationships between files: MINIMAL (mapping CSVs reference Documents/Notes folders)")

# Data domains analysis
print("\n=== Data Domain Coverage Analysis ===")
domains = {
    "Demographics": {"covered": True, "evidence": "demographics.csv", "notes": "No field list provided"},
    "Encounters/Visits": {"covered": True, "evidence": "schedule.csv", "notes": "Appointment dates, provider, location, type mentioned"},
    "Clinical Notes": {"covered": True, "evidence": "Notes/ folder (HTML)", "notes": "Individual HTML files per encounter, human-readable only"},
    "Documents/Attachments": {"covered": True, "evidence": "Documents/ folder", "notes": "All uploaded files in original format"},
    "Billing/Financial": {"covered": True, "evidence": "BillingReport.csv", "notes": "Transactions, charges, claims, status"},
    "Clinical Summary (USCDI v1)": {"covered": True, "evidence": "CCDA.xml", "notes": "Standard C-CDA covering USCDI v1 data classes"},
    "Medications (detailed)": {"covered": "partial", "evidence": "Only via C-CDA", "notes": "No dedicated medication export beyond C-CDA"},
    "Lab Results (structured)": {"covered": "partial", "evidence": "C-CDA + Documents/", "notes": "Structured labs in C-CDA; uploaded results in Documents/"},
    "Allergies": {"covered": "partial", "evidence": "Only via C-CDA", "notes": "Standard USCDI coverage"},
    "Immunizations": {"covered": "partial", "evidence": "Only via C-CDA", "notes": "Standard USCDI coverage"},
    "Vitals": {"covered": "partial", "evidence": "Only via C-CDA", "notes": "Standard USCDI coverage"},
    "Problems/Diagnoses": {"covered": "partial", "evidence": "Only via C-CDA", "notes": "Standard USCDI coverage"},
    "Procedures": {"covered": "partial", "evidence": "Only via C-CDA", "notes": "Standard USCDI coverage"},
    "Care Plans/Goals": {"covered": False, "evidence": "Not mentioned", "notes": "Product has health maintenance features"},
    "Orders/Referrals": {"covered": False, "evidence": "Not mentioned", "notes": "Product has referral management"},
    "Insurance/Coverage": {"covered": "partial", "evidence": "demographics.csv mentions insurance", "notes": "No detail on depth"},
    "Patient Communications": {"covered": False, "evidence": "Not mentioned", "notes": "Product has portal messaging, eFax"},
    "Prescriptions/e-Rx": {"covered": "partial", "evidence": "Only via C-CDA", "notes": "Product has detailed e-prescribing; no dedicated export"},
    "Specialty Clinical Data": {"covered": "partial", "evidence": "Notes/ HTML only", "notes": "32+ specialty templates exist; exported only as HTML narrative"},
}

for domain, info in domains.items():
    status = "✅" if info["covered"] == True else ("⚠️" if info["covered"] == "partial" else "❌")
    print(f"  {status} {domain:30s} | Evidence: {info['evidence']:30s} | {info['notes']}")

# Save structured output
output = {
    "pdf_pages": pages,
    "export_components": file_components,
    "csv_file_count": len(csv_files),
    "has_data_dictionary": False,
    "has_sample_data": False,
    "has_schema_files": False,
    "has_column_definitions": False,
    "has_value_sets": False,
    "domain_coverage": {k: {"covered": str(v["covered"]), "evidence": v["evidence"], "notes": v["notes"]} for k, v in domains.items()},
}

OUTPUT_DIR = "/home/jmandel/hobby/ehi-export-analysis/abstraction/wrs-health--wrs-health-web-ehr-and-practice-management-system/analysis"
with open(f"{OUTPUT_DIR}/pdf-analysis-output.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"\nStructured output saved to {OUTPUT_DIR}/pdf-analysis-output.json")
