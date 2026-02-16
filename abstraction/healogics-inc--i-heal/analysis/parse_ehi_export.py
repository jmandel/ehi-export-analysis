#!/usr/bin/env python3
"""
Parse the EHI Export PDF (EHIExport-iheal-2.pdf) to extract document types,
categories, parent-child relationships, and all structural information.

Output: full-entity-inventory.json
"""

import json
import subprocess
import re
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.parent.parent / "results" / "healogics-inc--i-heal"
OUTPUT_DIR = Path(__file__).parent

# Extract text from the EHI export PDF
pdf_path = RESULTS_DIR / "downloads" / "EHIExport-iheal-2.pdf"
result = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"], capture_output=True, text=True)
pdf_text = result.stdout

# ---- Document Types ----
# Categorize based on the PDF's own sections
patient_info = [
    {
        "name": "PatientDocument",
        "description": "Describes demographic information for the patient as well as the clinical care team, emergency contact, and insurance information. Spans multiple encounters.",
        "category": "Patient Information",
        "spans_encounters": True,
        "supports_photos": True,
        "supports_files": False,
        "photo_notes": "Only 1 photo may be associated with the document."
    }
]

treatment_course = [
    {
        "name": "HBOTreatmentCourseDocument",
        "description": "Defines any HBO treatment courses that have been applied for the patient. Spans multiple encounters.",
        "category": "Treatment Course / Conditions",
        "spans_encounters": True,
        "supports_photos": False,
        "supports_files": False,
        "children": ["HBODocument"]
    },
    {
        "name": "NonWoundConditionDocument",
        "description": "Identifies any non-wound conditions the patient may have had; includes the condition and location. Spans multiple encounters.",
        "category": "Treatment Course / Conditions",
        "spans_encounters": True,
        "supports_photos": False,
        "supports_files": False,
        "children": ["BiopsyDocument", "CompressionTherapyDocument", "IncisionAndDrainageDocument",
                      "NonWoundConditionAssessmentDocument", "NonWoundTreatmentNotesDocument",
                      "OtherProcedureDocument", "TotalContactCastDocument"]
    },
    {
        "name": "StomaDocument",
        "description": "Identifies any Ostomy conditions the patient may have had; includes the type, location, and status. Spans multiple encounters.",
        "category": "Treatment Course / Conditions",
        "spans_encounters": True,
        "supports_photos": False,
        "supports_files": False,
        "children": ["OstomyPreOperativeDocument", "StomaAssessmentDocument", "StomaTreatmentNotesDocument"]
    },
    {
        "name": "WoundDocument",
        "description": "Identifies any wound conditions the patient may have had; includes etiologies, location, wounding event, and date acquired. Spans multiple encounters.",
        "category": "Treatment Course / Conditions",
        "spans_encounters": True,
        "supports_photos": False,
        "supports_files": False,
        "children": ["BiopsyDocument", "CompressionTherapyDocument", "DebridementDocument",
                      "DermalMatrixSubstituteDocument", "IncisionAndDrainageDocument",
                      "NPWTApplicationDocument", "OtherProcedureDocument",
                      "TopicalGrowthFactorDocument", "TotalContactCastDocument",
                      "WoundAssessmentDocument", "WoundTreatmentNotesDocument"]
    }
]

encounter_docs = [
    "AllergyListDocument",
    "AncillaryServiceDocument",
    "ArrivalInfoDocument",
    "BiopsyDocument",
    "ChiefComplaintDocument",
    "ClinicLevelOfCareDocument",
    "CompressionTherapyDocument",
    "ConservativePatientAssessmentDocument",
    "CustomForm1Document",
    "CustomForm2Document",
    "CustomForm3Document",
    "CustomForm5Document",
    "CustomForm6Document",
    "CustomForm7Document",
    "CustomForm8Document",
    "CustomForm9Document",
    "CustomForm10Document",
    "DebridementDocument",
    "DermalMatrixSubstituteDocument",
    "DischargeInfoDocument",
    "DischargeInstructionsDocument",
    "FallRiskDocument",
    "GeneralVisitNotesDocument",
    "HBODocument",
    "HBOPreTreatmentEvaluationDocument",
    "HBOSafetyChecklistDocument",
    "HBOScreeningChecklistDocument",
    "HPIDocument",
    "HROSDocument",
    "ImmunizationsDocument",
    "IncisionAndDrainageDocument",
    "LowerExtremityDocument",
    "MultiDisciplinaryCarePlanDocument",
    "MultiWoundChartNotesDocument",
    "NeuropathyDocument",
    "NH_EducationAssessmentDocument",
    "NH_PatientCaregiverEducationDocument",
    "NonWoundConditionAssessmentDocument",
    "NonWoundTreatmentNotesDocument",
    "NPWTApplicationDocument",
    "NPWTMaintenanceDocument",
    "NutritionRiskDocument",
    "OstomyPreOperativeDocument",
    "OtherProcedureDocument",
    "PainAssessmentDocument",
    "PhysicalExamDocument",
    "PhysicianOrdersDocument",
    "PrescriptionDocument",
    "PressureUlcerRiskDocument",
    "ProblemListDocument",
    "ProgressNoteDocument",
    "SkinPerfusionPressureDocument",
    "StomaAssessmentDocument",
    "StomaTreatmentNotesDocument",
    "SuperBillDocument",
    "TCOMDocument",
    "TopicalGrowthFactorDocument",
    "TotalContactCastDocument",
    "VitalSignsDocument",
    "WoundAssessmentDocument",
    "WoundTreatmentNotesDocument",
]

non_encounter_docs = [
    "CustomScanDocument",
    "PatientCommunicationDocument",
    "TestResultDocument",
]

# Build photo/file support info
photo_docs = {
    "NonWoundConditionAssessmentDocument": "0 or more photos may be associated with the document.",
    "PatientDocument": "Only 1 photo may be associated with the document.",
    "StomaAssessmentDocument": "0 or more photos may be associated with the document.",
    "TCOMDocument": "0 or more photos may be associated with the document.",
    "WoundAssessmentDocument": "0 or more photos may be associated with the document.",
}

file_docs = {
    "CustomScanDocument": "1 file may be associated with the document.",
    "TestResultDocument": "1 file may be associated with the document.",
}

# Parent-child relationships (additional to treatment course children)
additional_parents = {
    "NPWTApplicationDocument": ["NPWTMaintenanceDocument"],
    "PhysicianOrdersDocument": ["PrescriptionDocument", "TestResultDocument"],
}

# Build encounter doc entries
encounter_entries = []
for name in encounter_docs:
    entry = {
        "name": name,
        "description": None,  # No field-level descriptions available (data dictionary missing)
        "category": "Encounter Documentation",
        "spans_encounters": False,
        "supports_photos": name in photo_docs,
        "supports_files": name in file_docs,
    }
    if name in photo_docs:
        entry["photo_notes"] = photo_docs[name]
    if name in file_docs:
        entry["file_notes"] = file_docs[name]
    # Check if it's a parent
    if name in additional_parents:
        entry["children"] = additional_parents[name]
    encounter_entries.append(entry)

non_encounter_entries = []
for name in non_encounter_docs:
    entry = {
        "name": name,
        "description": None,
        "category": "Non-Encounter Documentation",
        "spans_encounters": False,
        "supports_photos": name in photo_docs,
        "supports_files": name in file_docs,
    }
    if name in file_docs:
        entry["file_notes"] = file_docs[name]
    non_encounter_entries.append(entry)

all_entities = patient_info + treatment_course + encounter_entries + non_encounter_entries

# Common document properties (fields present in all documents)
common_fields = [
    {"name": "DocumentID", "type": "integer", "description": "Unique document identifier of the archive"},
    {"name": "VisitID", "type": "integer", "description": "Unique, internal visit identifier; groups clinical records with the visit/encounter"},
    {"name": "Patient.ID", "type": "integer", "description": "Unique, internal patient identifier"},
    {"name": "Patient.FirstName", "type": "string", "description": "Patient first name"},
    {"name": "Patient.LastName", "type": "string", "description": "Patient last name"},
    {"name": "Patient.MiddleName", "type": "string", "description": "Patient middle name"},
    {"name": "Patient.PatientNumber", "type": "string", "description": "Patient number / MRN"},
    {"name": "Patient.PatientDOB", "type": "date", "description": "Patient date of birth"},
    {"name": "ParentDocumentID", "type": "integer", "description": "Parent document identifier linking to condition or treatment course"},
    {"name": "DocumentDate", "type": "date", "description": "Date of service"},
    {"name": "PreviousDocumentID", "type": "integer", "description": "Previous document identifier (nullable)"},
    {"name": "FacilityID", "type": "integer", "description": "Facility identifier"},
    {"name": "ProviderID", "type": "integer", "description": "Provider identifier (nullable)"},
    {"name": "SecondaryProviderID", "type": "integer", "description": "Secondary provider identifier (nullable)"},
    {"name": "ClinicianID", "type": "integer", "description": "Clinician identifier (nullable)"},
    {"name": "SecondaryClinicianID", "type": "integer", "description": "Secondary clinician identifier (nullable)"},
    {"name": "DocumentDateAdded", "type": "datetime", "description": "Timestamp when document was added"},
    {"name": "RecordActive", "type": "boolean", "description": "Whether record is active (nullable)"},
    {"name": "Physician", "type": "object", "description": "Physician details (name, credentials)"},
    {"name": "Clinician", "type": "object", "description": "Clinician details (name, credentials)"},
    {"name": "DateAdded", "type": "datetime", "description": "Date/time added"},
    {"name": "User", "type": "object", "description": "Data entry user details"},
    {"name": "LastUpdated", "type": "datetime", "description": "Last update timestamp"},
    {"name": "LastUpdatedBy", "type": "object", "description": "Last update user"},
    {"name": "FacilitySettingsInstanceID", "type": "integer", "description": "Facility settings instance identifier"},
]

# Electronic signature fields
signature_fields = [
    {"name": "ElectronicSignatures.ElectronicSignature.UserID", "type": "integer", "description": "Signer's internal user identifier"},
    {"name": "ElectronicSignatures.ElectronicSignature.FirstName", "type": "string", "description": "Signer's first name"},
    {"name": "ElectronicSignatures.ElectronicSignature.LastName", "type": "string", "description": "Signer's last name"},
    {"name": "ElectronicSignatures.ElectronicSignature.DateSigned", "type": "datetime", "description": "Date/time signed"},
    {"name": "ElectronicSignatures.ElectronicSignature.Credentials", "type": "string", "description": "Signer's credentials"},
]

# File reference fields
file_reference_fields = [
    {"name": "FileReferences.FileReference", "type": "url", "description": "HTTPS URL to retrieve associated photo or file from Azure Blob Storage (expires 90 days from export)"},
]

inventory = {
    "source": "EHIExport-iheal-2.pdf",
    "source_date": "2023-11-16",
    "export_format": "Proprietary XML",
    "export_delivery": "ZIP file via i-heal UI",
    "companion_data_dictionary": {
        "referenced": True,
        "available": False,
        "note": "The PDF states 'A companion document, EHIExport – Data Dictionary, provides a data dictionary and identifies the elements within each document.' This document is not publicly available."
    },
    "common_document_properties": {
        "fields": common_fields,
        "field_count": len(common_fields),
    },
    "electronic_signature_properties": {
        "fields": signature_fields,
        "field_count": len(signature_fields),
        "note": "Most documents except condition/treatment course documents are signable. One or more signatures may be applied."
    },
    "file_reference_properties": {
        "fields": file_reference_fields,
        "field_count": len(file_reference_fields),
        "note": "Photo/file URLs expire 90 days from export date."
    },
    "entities": all_entities,
    "summary": {
        "total_document_types": len(all_entities),
        "by_category": {},
        "with_descriptions": sum(1 for e in all_entities if e.get("description")),
        "without_descriptions": sum(1 for e in all_entities if not e.get("description")),
        "with_photo_support": sum(1 for e in all_entities if e.get("supports_photos")),
        "with_file_support": sum(1 for e in all_entities if e.get("supports_files")),
        "common_field_count": len(common_fields),
        "signature_field_count": len(signature_fields),
        "note": "Field-level details for individual document types are not available — they are in the missing companion Data Dictionary."
    }
}

# Category breakdown
categories = {}
for entity in all_entities:
    cat = entity["category"]
    if cat not in categories:
        categories[cat] = {"count": 0, "entities": []}
    categories[cat]["count"] += 1
    categories[cat]["entities"].append(entity["name"])
inventory["summary"]["by_category"] = categories

# Parent-child relationship summary
parent_child = {}
for entity in all_entities:
    if "children" in entity:
        parent_child[entity["name"]] = entity["children"]
inventory["parent_child_relationships"] = parent_child

# Write output
output_path = OUTPUT_DIR / "full-entity-inventory.json"
with open(output_path, "w") as f:
    json.dump(inventory, f, indent=2)

# Print summary
print(f"Total document types: {inventory['summary']['total_document_types']}")
print(f"Common fields per document: {len(common_fields)}")
print(f"Signature fields: {len(signature_fields)}")
print(f"With descriptions (from PDF): {inventory['summary']['with_descriptions']}")
print(f"Without descriptions (need data dictionary): {inventory['summary']['without_descriptions']}")
print()
print("By category:")
for cat, info in categories.items():
    print(f"  {cat}: {info['count']} document types")
print()
print("Parent-child relationships:")
for parent, children in parent_child.items():
    print(f"  {parent} -> {', '.join(children)}")
print()
print(f"Documents supporting photos: {inventory['summary']['with_photo_support']}")
print(f"Documents supporting files: {inventory['summary']['with_file_support']}")
print(f"\nOutput written to: {output_path}")
