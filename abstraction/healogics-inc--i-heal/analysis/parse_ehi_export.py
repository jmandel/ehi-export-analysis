#!/usr/bin/env python3
"""Parse the EHI Export PDF to extract document types and build entity inventory.

The i-heal EHI export documentation describes a proprietary XML-based export
with 70+ document types. This script extracts all document types, their
categories, parent-child relationships, and known fields from the PDF text.

Note: The PDF references a companion "EHIExport – Data Dictionary" document
that is NOT publicly available. We can only extract what's in this PDF.
"""

import json
import subprocess
import re

def extract_pdf_text(pdf_path):
    result = subprocess.run(
        ["pdftotext", "-layout", pdf_path, "-"],
        capture_output=True, text=True
    )
    return result.stdout

def parse_document_types(text):
    """Extract all document type names from the PDF."""
    doc_types = []
    
    # Categories and their document types
    categories = {
        "Patient Information": [],
        "Treatment Course / Conditions": [],
        "Encounter Documentation": [],
        "Non-Encounter Documentation": [],
    }
    
    current_category = None
    lines = text.split("\n")
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if line == "Patient Information":
            current_category = "Patient Information"
        elif line == "Treatment Course / Conditions":
            current_category = "Treatment Course / Conditions"
        elif line == "Encounter Documentation":
            current_category = "Encounter Documentation"
        elif line == "Non-Encounter Documentation":
            current_category = "Non-Encounter Documentation"
        elif line == "Document Properties":
            current_category = None
        
        # Match document type names (ending with "Document")
        match = re.match(r'^(\w+Document)\s*(?:–.*)?$', line)
        if match and current_category:
            doc_name = match.group(1)
            if doc_name not in ["PatientDocument"] or current_category == "Patient Information":
                categories[current_category].append(doc_name)
    
    return categories

def parse_parent_child(text):
    """Extract parent-child relationships from the PDF."""
    relationships = {}
    current_parent = None
    
    lines = text.split("\n")
    in_relationships = False
    
    for line in lines:
        stripped = line.strip()
        
        if "Parent / Child Relationships" in stripped:
            in_relationships = True
            continue
        
        if in_relationships:
            if stripped == "Document Signatures":
                break
            
            # Parent (bullet point)
            parent_match = re.match(r'^[•]\s+(\w+Document)', stripped)
            if parent_match:
                current_parent = parent_match.group(1)
                relationships[current_parent] = []
                continue
            
            # Child (indented with o)
            child_match = re.match(r'^o\s+(\w+Document)', stripped)
            if child_match and current_parent:
                relationships[current_parent].append(child_match.group(1))
    
    return relationships

def parse_descriptions(text):
    """Extract document descriptions from the PDF text."""
    descriptions = {}
    
    # Patient Information section descriptions
    desc_patterns = [
        ("PatientDocument", "describes demographic information for the patient as well as the clinical care team, emergency contact, and insurance information"),
        ("HBOTreatmentCourseDocument", "defines any HBO treatment courses that have been applied for the patient"),
        ("NonWoundConditionDocument", "identifies any non-wound conditions the patient may have had; includes the condition and location"),
        ("StomaDocument", "identifies any Ostomy conditions the patient may have had; includes the type, location, and status"),
        ("WoundDocument", "identifies any wound conditions the patient may have had; includes etiologies, location, wounding event, and date acquired"),
    ]
    
    for name, desc in desc_patterns:
        descriptions[name] = desc
    
    return descriptions

def get_common_fields():
    """Return the common fields present in DocumentProperties across all documents."""
    return [
        {"name": "DocumentID", "type": "integer", "description": "Unique document identifier"},
        {"name": "VisitID", "type": "integer", "description": "Visit/encounter identifier"},
        {"name": "Patient.ID", "type": "integer", "description": "Internal patient identifier"},
        {"name": "Patient.FirstName", "type": "string", "description": "Patient first name"},
        {"name": "Patient.LastName", "type": "string", "description": "Patient last name"},
        {"name": "Patient.MiddleName", "type": "string", "description": "Patient middle name"},
        {"name": "Patient.PatientNumber", "type": "string", "description": "Patient number/MRN"},
        {"name": "Patient.PatientDOB", "type": "date", "description": "Patient date of birth"},
        {"name": "ParentDocumentID", "type": "integer", "description": "Parent document identifier for condition/treatment course association"},
        {"name": "DocumentDate", "type": "date", "description": "Date of service"},
        {"name": "PreviousDocumentID", "type": "integer", "description": "Previous document identifier"},
        {"name": "FacilityID", "type": "integer", "description": "Facility identifier"},
        {"name": "ProviderID", "type": "integer", "description": "Provider identifier"},
        {"name": "SecondaryProviderID", "type": "integer", "description": "Secondary provider identifier"},
        {"name": "ClinicianID", "type": "integer", "description": "Clinician identifier"},
        {"name": "SecondaryClinicianID", "type": "integer", "description": "Secondary clinician identifier"},
        {"name": "DocumentDateAdded", "type": "datetime", "description": "Date/time document was added"},
        {"name": "RecordActive", "type": "boolean", "description": "Whether record is active"},
        {"name": "Physician", "type": "object", "description": "Physician information"},
        {"name": "Clinician", "type": "object", "description": "Clinician information"},
        {"name": "DateAdded", "type": "datetime", "description": "Date/time added"},
        {"name": "User", "type": "object", "description": "Data entry user information"},
        {"name": "LastUpdated", "type": "datetime", "description": "Last update timestamp"},
        {"name": "LastUpdatedBy", "type": "object", "description": "Last updated by user"},
        {"name": "FacilitySettingsInstanceID", "type": "integer", "description": "Facility settings instance identifier"},
    ]

def get_signature_fields():
    """Return fields in the ElectronicSignatures container."""
    return [
        {"name": "ElectronicSignature.UserID", "type": "integer", "description": "Signer's internal user identifier"},
        {"name": "ElectronicSignature.FirstName", "type": "string", "description": "Signer's first name"},
        {"name": "ElectronicSignature.LastName", "type": "string", "description": "Signer's last name"},
        {"name": "ElectronicSignature.DateSigned", "type": "datetime", "description": "Date/time signed"},
        {"name": "ElectronicSignature.Credentials", "type": "string", "description": "Signer's credentials"},
    ]

def get_file_reference_fields():
    """Return fields in the FileReferences container."""
    return [
        {"name": "FileReference", "type": "url", "description": "Secure URL to retrieve associated photo or file (expires 90 days from export)"},
    ]

def build_inventory(categories, relationships, descriptions):
    """Build the full entity inventory."""
    entities = []
    
    # Documents that support photos
    docs_with_photos = [
        "NonWoundConditionAssessmentDocument",
        "PatientDocument",
        "StomaAssessmentDocument",
        "TCOMDocument",
        "WoundAssessmentDocument",
    ]
    
    # Documents that support files
    docs_with_files = [
        "CustomScanDocument",
        "TestResultDocument",
    ]
    
    # Documents that are NOT signable (condition/treatment course docs)
    non_signable = [
        "HBOTreatmentCourseDocument",
        "NonWoundConditionDocument",
        "StomaDocument",
        "WoundDocument",
    ]
    
    common = get_common_fields()
    sig_fields = get_signature_fields()
    file_ref_fields = get_file_reference_fields()
    
    for category, doc_names in categories.items():
        for doc_name in doc_names:
            fields = list(common)  # copy common fields
            
            # Add signature fields for signable documents
            if doc_name not in non_signable:
                fields.extend(sig_fields)
            
            # Add file reference fields where applicable
            if doc_name in docs_with_photos or doc_name in docs_with_files:
                fields.extend(file_ref_fields)
            
            # Find parent relationships
            parents = []
            children = []
            for parent, child_list in relationships.items():
                if doc_name == parent:
                    children = child_list
                if doc_name in child_list:
                    parents.append(parent)
            
            entity = {
                "entity_name": doc_name,
                "category": category,
                "description": descriptions.get(doc_name, ""),
                "field_count_common": len(common),
                "field_count_total": len(fields),
                "fields": fields,
                "has_signatures": doc_name not in non_signable,
                "has_photos": doc_name in docs_with_photos,
                "has_files": doc_name in docs_with_files,
                "parent_documents": parents,
                "child_documents": children,
                "note": "Only common/structural fields are documented in the public PDF. The companion Data Dictionary (not publicly available) contains document-specific fields."
            }
            
            entities.append(entity)
    
    return entities

def main():
    pdf_path = "../downloads/EHIExport-iheal-2.pdf"
    text = extract_pdf_text(pdf_path)
    
    categories = parse_document_types(text)
    relationships = parse_parent_child(text)
    descriptions = parse_descriptions(text)
    
    # Count totals
    total_docs = sum(len(docs) for docs in categories.values())
    print(f"Total document types found: {total_docs}")
    for cat, docs in categories.items():
        print(f"  {cat}: {len(docs)}")
    
    print(f"\nParent-child relationships: {len(relationships)}")
    for parent, children in relationships.items():
        print(f"  {parent} -> {children}")
    
    entities = build_inventory(categories, relationships, descriptions)
    
    # Save full inventory
    inventory = {
        "source": "EHIExport-iheal-2.pdf",
        "source_description": "i-heal 2.0 EHI Export documentation (10-page PDF). Note: references companion Data Dictionary not publicly available.",
        "export_format": "Proprietary XML in ZIP archive",
        "total_document_types": len(entities),
        "categories": {cat: len(docs) for cat, docs in categories.items()},
        "common_fields_per_document": len(get_common_fields()),
        "data_dictionary_available": False,
        "data_dictionary_note": "The PDF references 'EHIExport – Data Dictionary' as a companion document providing detailed field definitions for each document type. This document is NOT publicly available.",
        "entities": entities,
    }
    
    with open("entity-inventory-full.json", "w") as f:
        json.dump(inventory, f, indent=2)
    
    # Build summary
    summary = {
        "total_document_types": len(entities),
        "categories": {},
        "common_fields_per_document": len(get_common_fields()),
        "total_fields_documented": len(get_common_fields()) + len(get_signature_fields()) + len(get_file_reference_fields()),
        "fields_with_descriptions": len(get_common_fields()) + len(get_signature_fields()) + len(get_file_reference_fields()),
        "description_percentage": 100.0,
        "data_dictionary_publicly_available": False,
        "export_format": "Proprietary XML in ZIP archive",
        "export_mechanism": "UI feature in i-heal 2.0 (Facility Administration or Emergency Access role)",
        "single_patient": True,
        "bulk_export": True,
        "document_types_with_photos": len([e for e in entities if e["has_photos"]]),
        "document_types_with_files": len([e for e in entities if e["has_files"]]),
        "document_types_with_signatures": len([e for e in entities if e["has_signatures"]]),
    }
    
    for cat, docs in categories.items():
        summary["categories"][cat] = {
            "count": len(docs),
            "documents": docs,
        }
    
    with open("entity-inventory-summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSaved entity-inventory-full.json ({len(entities)} entities)")
    print(f"Saved entity-inventory-summary.json")

if __name__ == "__main__":
    main()
