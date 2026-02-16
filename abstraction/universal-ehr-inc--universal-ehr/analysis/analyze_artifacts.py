#!/usr/bin/env python3
"""
Analyze Universal EHR's EHI export artifacts.

Since the only substantive artifact is a 6-page screenshot-based PDF user guide
with no data dictionary or schema, this script:
1. Extracts and verifies PDF metadata
2. Inventories the FHIR resource types visible in screenshots
3. Catalogs the document types visible in the Documents subfolder
4. Produces summary statistics
5. Generates full-entity-inventory.json
"""

import json
import subprocess
import os
from pathlib import Path

RESULTS_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/results/universal-ehr-inc--universal-ehr")
DOWNLOADS_DIR = RESULTS_DIR / "downloads"
OUTPUT_DIR = Path("/home/jmandel/hobby/ehi-export-analysis/abstraction/universal-ehr-inc--universal-ehr/analysis")

def get_pdf_info():
    """Extract PDF metadata."""
    pdf_path = DOWNLOADS_DIR / "EHI_Document.pdf"
    result = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True)
    info = {}
    for line in result.stdout.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            info[key.strip()] = val.strip()
    return info

def get_artifact_inventory():
    """Inventory all downloaded artifacts."""
    files_json = RESULTS_DIR / "files.json"
    with open(files_json) as f:
        data = json.load(f)
    
    file_list = data.get("files", data) if isinstance(data, dict) else data
    
    artifacts = []
    for entry in file_list:
        file_path = RESULTS_DIR / entry.get("path", "")
        size = file_path.stat().st_size if file_path.exists() else entry.get("size_bytes", 0)
        artifacts.append({
            "filename": entry.get("path", ""),
            "source_url": entry.get("source_url", ""),
            "description": entry.get("description", ""),
            "size_bytes": size,
        })
    return artifacts

def build_fhir_resource_inventory():
    """
    Build inventory of FHIR resource types visible in the export screenshots.
    
    From visual inspection of PDF pages 3-6, the export ZIP contains per-patient
    folders with these NDJSON files (confirmed from 7-Zip file listing screenshots):
    """
    # These resource types are confirmed from the 7-Zip file listing visible
    # on PDF pages 3-4 and the detailed file listing on page 6
    resources = [
        {
            "resource_type": "Appointment",
            "file_pattern": "Appointment_1.ndjson",
            "fhir_version": "R4",
            "us_core": False,
            "description": "Patient appointment records",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "CareTeam",
            "file_pattern": "CareTeam_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Care team assignments for the patient",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "Condition",
            "file_pattern": "Condition_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Patient conditions/diagnoses",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "DocumentReference",
            "file_pattern": "DocumentReference_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "References to patient documents",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "Encounter",
            "file_pattern": "Encounter_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Patient encounters/visits",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "Invoice",
            "file_pattern": "Invoice_1.ndjson",
            "fhir_version": "R4",
            "us_core": False,
            "description": "Patient invoice/billing records",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "MedicationRequest",
            "file_pattern": "MedicationRequest_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Medication orders/prescriptions",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4; NDJSON content partially visible on page 3"
        },
        {
            "resource_type": "Observation",
            "file_pattern": "Observation_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Clinical observations (vitals, lab results, etc.)",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "Organization",
            "file_pattern": "Organization_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Healthcare organization information",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "Patient",
            "file_pattern": "Patient_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Patient demographics",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "Practitioner",
            "file_pattern": "Practitioner_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Practitioner/provider information",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
        {
            "resource_type": "Provenance",
            "file_pattern": "Provenance_1.ndjson",
            "fhir_version": "R4",
            "us_core": True,
            "description": "Provenance/audit trail for resources",
            "fields_documented": 0,
            "source_evidence": "Visible in 7-Zip file listing on PDF page 4"
        },
    ]
    return resources

def build_documents_inventory():
    """
    Documents visible in the Documents/ subfolder on PDF page 6.
    These are actual patient documents (PDFs, images) included in the export.
    """
    return {
        "description": "Actual patient document files (PDFs, images) stored in a Documents/ subfolder per patient",
        "source_evidence": "Visible in detailed file listing on PDF page 6",
        "visible_documents": [
            "Breast screening mammogram records",
            "OCM records",
            "Lab results (dipstick)",
            "CXR (chest X-ray) results",
            "BCBS provider documents",
            "Referral documents",
            "HL7 viewed PDFs",
        ],
        "file_formats": ["PDF"],
        "date_range": "2016-2023 (based on visible dates in file listing)",
        "size_range": "~4.9 KB to ~313 KB (based on visible file sizes)"
    }

def build_full_inventory():
    """Build the complete entity inventory."""
    resources = build_fhir_resource_inventory()
    documents = build_documents_inventory()
    pdf_info = get_pdf_info()
    artifacts = get_artifact_inventory()
    
    # Standard FHIR R4 field counts (approximate, from spec)
    # Since vendor provides zero field documentation, we note standard spec field counts
    fhir_r4_field_counts = {
        "Appointment": 26,
        "CareTeam": 16,
        "Condition": 23,
        "DocumentReference": 22,
        "Encounter": 30,
        "Invoice": 20,
        "MedicationRequest": 38,
        "Observation": 32,
        "Organization": 14,
        "Patient": 28,
        "Practitioner": 14,
        "Provenance": 14,
    }
    
    for r in resources:
        r["fhir_r4_standard_fields"] = fhir_r4_field_counts.get(r["resource_type"], 0)
    
    inventory = {
        "vendor": "Universal EHR, Inc.",
        "product": "Universal EHR",
        "chpl_id": 9333,
        "export_format": "FHIR R4 NDJSON + patient documents",
        "data_dictionary_available": False,
        "field_level_documentation": False,
        "schema_available": False,
        "sample_data_available": False,
        "documentation_source": "6-page screenshot-based PDF user guide (EHI_Document.pdf)",
        "total_resource_types": len(resources),
        "total_vendor_documented_fields": 0,
        "total_fhir_r4_standard_fields": sum(fhir_r4_field_counts.values()),
        "resources": resources,
        "documents_subfolder": documents,
        "artifacts_reviewed": artifacts,
        "pdf_metadata": pdf_info,
        "analysis_notes": {
            "no_data_dictionary": "No data dictionary, schema, or field-level documentation exists. The only artifact is a screenshot-based PDF showing the export UI workflow.",
            "field_counts_from_spec": "Field counts listed as 'fhir_r4_standard_fields' are from the FHIR R4 specification, NOT from vendor documentation. The vendor documents zero fields.",
            "non_us_core_resources": "Invoice and Appointment are NOT US Core resources, suggesting slight vendor extension beyond standard (g)(10) FHIR API.",
            "missing_us_core_types": "Several common US Core resource types are absent: AllergyIntolerance, Immunization, Procedure, DiagnosticReport, CarePlan, Goal, Device, Location, MedicationAdministration.",
            "documents_included": "The export includes a Documents/ subfolder with actual patient files (PDFs, images), which goes beyond standard FHIR export."
        }
    }
    return inventory

def main():
    inventory = build_full_inventory()
    
    output_path = OUTPUT_DIR / "full-entity-inventory.json"
    with open(output_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"Wrote {output_path}")
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"FHIR resource types in export: {inventory['total_resource_types']}")
    print(f"Vendor-documented fields: {inventory['total_vendor_documented_fields']}")
    print(f"FHIR R4 standard fields (for reference): {inventory['total_fhir_r4_standard_fields']}")
    print(f"US Core resources: {sum(1 for r in inventory['resources'] if r['us_core'])}")
    print(f"Non-US Core resources: {sum(1 for r in inventory['resources'] if not r['us_core'])}")
    print(f"Documents subfolder: Yes (actual patient files)")
    print(f"Data dictionary: No")
    print(f"Schema: No")
    print(f"Sample data: No")
    
    # Resource breakdown
    print(f"\n=== Resource Types ===")
    for r in inventory["resources"]:
        us_core_tag = "US Core" if r["us_core"] else "NON-US Core"
        print(f"  {r['resource_type']:25s} | {us_core_tag:12s} | ~{r['fhir_r4_standard_fields']} std fields")
    
    # Save summary text
    summary_path = OUTPUT_DIR / "analysis-summary.txt"
    with open(summary_path, "w") as f:
        f.write(f"Universal EHR - EHI Export Analysis Summary\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"Artifacts: 3 files (1 PDF, 2 HTML)\n")
        f.write(f"Primary artifact: EHI_Document.pdf (6 pages, screenshot walkthrough)\n")
        f.write(f"Export format: FHIR R4 NDJSON + Documents/ subfolder\n")
        f.write(f"Resource types: {inventory['total_resource_types']}\n")
        f.write(f"  US Core: {sum(1 for r in inventory['resources'] if r['us_core'])}\n")
        f.write(f"  Non-US Core: {sum(1 for r in inventory['resources'] if not r['us_core'])} (Invoice, Appointment)\n")
        f.write(f"Vendor-documented fields: 0\n")
        f.write(f"Data dictionary: None\n")
        f.write(f"Schema: None\n")
        f.write(f"Sample data: None\n\n")
        f.write(f"Classification: Standard-based projection\n")
        f.write(f"Rationale: Export is FHIR R4 NDJSON, closely aligned with (g)(10)\n")
        f.write(f"  FHIR API output. Two non-US-Core resources (Invoice, Appointment)\n")
        f.write(f"  suggest minor extension. No native database model exposure.\n")
    print(f"\nWrote {summary_path}")

if __name__ == "__main__":
    main()
