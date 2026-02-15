# EHI Export Analysis: Practice EHR LLC

**Product**: Practice EHR V12
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2997.Prac.12.01.1.220628 (CHPL listing #10923)

## 1. Product Context

Practice EHR is a cloud-based, all-in-one ambulatory EHR and practice management platform targeting small to mid-sized multi-specialty practices. It covers 23 named specialties (family medicine, cardiology, dermatology, orthopedics, psychiatry, etc.) with specialty-specific templates and workflows. The product integrates clinical documentation, e-prescribing (including EPCS), lab ordering/results, scheduling, patient portal, telehealth, billing/claims (professional, institutional, workers' comp, no-fault, dental), revenue cycle management, and reporting/analytics. Pricing ranges from $179–$449/provider/month, with optional staffed RCM services.

For EHI export completeness, the product stores at minimum:
- **Clinical**: demographics, vitals, problem lists, medication lists, allergies, clinical notes/progress notes, lab orders and results, prescriptions, immunizations, family/social history, diagnoses, implantable device data, care plans
- **Financial/Administrative**: insurance/eligibility, claims, remittance/ERA, payment records, patient statements, denial/appeal records, encounter/superbill forms, consent forms
- **Patient Engagement**: portal messages, appointment requests, prescription refill requests, patient-entered intake forms
- **Specialty**: specialty-specific templates and clinical assessments across 23 specialties
- **Telehealth**: virtual visit records, AI Scribe transcriptions

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Practice-EHR-B10-Electronic-Health-Information-Export.pdf` (116,552 bytes, 4 pages, 295 words) | The sole EHI export documentation. A cover page plus 3 content pages describing the ZIP export structure: C-CDA XML + documents folder + XLS index. Created 2023-11-22 with Microsoft Word. Version 1.0. No data dictionary, no schema, no sample data. | **Primary artifact**; extremely thin |
| `data-export-page.png` (256,660 bytes, 1920×1053 px) | Screenshot of https://www.practiceehr.com/data-export showing a "Data Export" banner and a single link to the PDF. No other content on the page. | Confirms the PDF is the only documentation offered |
| https://www.practiceehr.com/data-export (verified live 2026-02-15) | The vendor's data export page. Still contains exactly one link to the same PDF. No additional documentation, schemas, sample data, or supplementary materials. | Confirms no hidden/additional documentation |

**Total documentation**: 1 PDF (295 words of content across 3 pages). No data dictionary, no schema, no sample data, no machine-readable artifacts.

## 3. Export Mechanics

- **Format**: ZIP file per patient containing: (1) a `Clinical` folder with one C-CDA XML file, (2) a `Documents` folder with scanned/uploaded files in original formats (.jpg, .gif, .bmp, .png, .pdf, .txt), and (3) a `Patient Documents Detail.xls` index file
- **Mechanism**: User-initiated from within the application (no screenshots or step-by-step instructions provided)
- **Single-patient**: Yes — described as available "at any time without developer assistance"
- **Multi-patient (bulk)**: Yes — described as available "at any time without developer assistance"
- **Access constraints/fees**: Not documented in the export documentation. The mandatory disclosures page was not among the downloaded artifacts, so fee information is unverified.

## 4. Export Content: What's In It

The export documentation describes exactly three components with no field-level detail:

### 4a. C-CDA XML (Clinical folder)

A single C-CDA file per patient, described as compliant with "US Core Data for Interoperability (USCD), Version 1 requirements" (note: misspelled as "USCD" in the document). The document references three HL7 specifications:

- HL7 CDA R2 IHE Health Story Consolidation, DSTU Release 1.1 (July 2012)
- HL7 CDA R2 Consolidated CDA Templates, DSTU Release 2.1 (August 2015, June 2019 with Errata)
- HL7 CDA R2 C-CDA Templates R2.1 Companion Guide, Release 2 (October 2019)

No information is provided about which specific C-CDA sections or template IDs are populated. No vendor extensions are mentioned. Based on the USCDI v1 reference, the C-CDA would be expected to cover at most: demographics, problems/diagnoses, medications, allergies, lab results, vital signs, procedures, immunizations, care team, goals, health concerns, and smoking status.

**There is no data dictionary.** Zero entities, zero fields, zero type definitions, zero value sets, zero relationship documentation. The C-CDA standard is referenced by name only.

### 4b. Patient Documents (Documents folder)

Scanned and uploaded documents exported in their original formats. The document lists six types:
1. Signed progress notes
2. Available lab results
3. Radiology reports
4. Scanned documents
5. Imported documents
6. "Iploaded" documents (typo for "Uploaded")

This is a file dump — documents are exported as-is with no structured data extraction.

### 4c. Patient Documents Detail.xls

An Excel index file described as being included in the ZIP. **The document provides zero information about the structure or contents of this file** — no column names, no description of what it indexes, no sample data.

### Vendor's own content organization

The vendor does not organize the export into categories or provide an entity inventory. The entire export is described in terms of three folders/files:

| Component | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA XML file | Unknown (vendor provides no field-level detail) | N/A | N/A | Clinical Data |
| Documents folder | N/A (unstructured file dump) | N/A | N/A | Patient Documents |
| Patient Documents Detail.xls | Unknown (not described) | N/A | N/A | (Unnamed) |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes exactly two categories of exported data:

1. **"Clinical Data"** — A C-CDA XML file. By referencing USCDI v1, this would contain standard clinical summary data (demographics, problems, medications, allergies, labs, vitals, procedures, immunizations). However, the vendor provides no specifics about which C-CDA sections are actually populated, and C-CDA is inherently a clinical summary format — it cannot represent billing, scheduling, specialty-specific assessments, portal messages, or most administrative data.

2. **"Patient Documents"** — Scanned/uploaded files in original format. This captures documents that happen to have been attached to the patient record but provides no structured data from those documents.

There is no mention of any native database tables, custom data structures, or domain-specific exports. The export documentation is silent on billing, claims, insurance, scheduling, portal data, e-prescribing history, encounter/superbill data, specialty templates, telehealth records, and consent forms.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Included in C-CDA per USCDI v1 standard; limited to standard C-CDA demographic fields | Product stores richer demographics via kiosk intake (custom fields, intake forms); C-CDA captures only standard fields |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections, but no vendor documentation confirms this | Product stores detailed encounter data linked to billing; no structured encounter export documented |
| Problems / conditions / diagnoses | ⚠️ Partial | Expected in C-CDA per USCDI v1 | Standard C-CDA coverage only; no vendor-specific detail |
| Medications / prescriptions | ⚠️ Partial | Expected in C-CDA per USCDI v1 | C-CDA covers medication lists but not EPCS history, formulary checks, Surescripts medication history, or renewal workflows |
| Allergies | ⚠️ Partial | Expected in C-CDA per USCDI v1 | Standard coverage only |
| Immunizations | ⚠️ Partial | Expected in C-CDA per USCDI v1 | Standard coverage only |
| Vitals | ⚠️ Partial | Expected in C-CDA per USCDI v1 | Standard coverage only |
| Lab results | ⚠️ Partial | Expected in C-CDA per USCDI v1; "available lab results" also in Documents folder | Structured lab results in C-CDA limited to USCDI v1 scope; lab ordering data and electronic lab orders not covered |
| Imaging / diagnostic reports | ⚠️ Partial | "Radiology reports" listed in Documents folder | Unstructured document dump only, not structured radiology data |
| Procedures | ⚠️ Partial | Expected in C-CDA per USCDI v1 | Standard coverage only |
| Clinical notes / documents | ⚠️ Partial | "Signed progress notes" in Documents folder; C-CDA may include notes sections | Notes exported as scanned/uploaded files (unstructured), not as structured note data with metadata |
| Care plans / goals | ⚠️ Partial | May be in C-CDA per USCDI v1 | No confirmation these sections are populated |
| Orders / referrals | ❌ Not covered | No mention in export documentation | Product supports lab ordering and referral workflows; not represented in export |
| Insurance / coverage | ❌ Not covered | No mention in export documentation | Product stores insurance/eligibility data (real-time eligibility verification feature); significant gap |
| Claims / billing | ❌ Not covered | No mention in export documentation | Product handles professional, institutional, workers' comp, no-fault, and dental claims; major gap |
| Payments | ❌ Not covered | No mention in export documentation | Product handles ERA processing, payment posting, adjustments, patient statements; major gap |
| Consents / directives | ❌ Not covered | No mention in export documentation | Product collects consent forms via kiosk; not in export |
| Patient communications / portal messages | ❌ Not covered | No mention in export documentation | Product has patient portal with secure messaging, appointment requests, refill requests; not in export |
| Specialty-specific data (23 specialties) | ❌ Not covered | No mention in export documentation | Product markets specialty-specific templates and workflows for 23 specialties; C-CDA cannot represent this data |

**Summary**: Of 19 applicable domains, 0 are fully covered (✅), 10 are partially covered (⚠️, via C-CDA with no vendor confirmation of specific sections), and 9 are completely absent (❌). The partial ratings are generous — they assume the C-CDA includes standard sections per USCDI v1, which the vendor has not confirmed with any specifics.

## 6. Documentation Quality

The export documentation is among the thinnest possible:

- **Total content**: 295 words across 3 content pages (page 1 is a cover page)
- **Data dictionary**: None. Zero field-level documentation.
- **Schema**: None. No machine-readable format specifications.
- **Sample data**: None. No example exports.
- **Types/value sets**: None documented.
- **Relationships**: None documented.
- **User instructions**: None. No screenshots, no menu paths, no step-by-step guide.
- **XLS index file**: Mentioned but not described at all.
- **Typos**: "USCD" for "USCDI," "Iploaded" for "Uploaded" — suggesting minimal review.
- **Version**: 1.0, dated November 2023. No change history. The document has not been updated in over 2 years.

**Could a developer build an import from this documentation?** No. A developer would know the export contains a C-CDA XML file (which is a known standard, so the structure is inferrable from HL7 specs — but Practice EHR provides no information about which sections it populates or any vendor-specific extensions). The `Patient Documents Detail.xls` file is completely undocumented. The Documents folder is an unstructured file dump with no metadata schema.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a C-CDA clinical summary repackaged as a (b)(10) EHI export, supplemented with a dump of attached document files. This is functionally the same data a patient might receive through a transitions-of-care document or patient portal, not a comprehensive export of all electronic health information the system stores. The C-CDA format is inherently incapable of representing billing, scheduling, specialty-specific, or administrative data. For a full-featured ambulatory EHR + practice management platform, this approach captures a small fraction of stored EHI.

### Key Findings

1. **The export is a C-CDA document plus attached files — not a native data export.** The entire structured clinical data export is a single C-CDA XML file per patient, which by design covers only USCDI v1 clinical summary data. This is the classic (b)(10)/(g)(10) confusion: repurposing a transitions-of-care export as "all EHI." (Source: `Practice-EHR-B10-Electronic-Health-Information-Export.pdf`, pages 2–3)

2. **Billing, claims, and revenue cycle data are entirely absent.** Practice EHR handles professional, institutional, workers' comp, no-fault, and dental claims; ERA processing; payment posting; denial management; and patient statements. None of this data appears in the export. For a product that markets itself as an integrated EHR + practice management + RCM platform, this is the largest gap. (Source: product-research.md cross-referenced with PDF; no billing/financial entities in export documentation)

3. **There is no data dictionary, no schema, and no sample data.** The entire export documentation is 295 words (3 pages of content). No field names, no data types, no value sets, no relationships, no machine-readable artifacts. Even the `Patient Documents Detail.xls` index file included in the export is not described. (Source: `Practice-EHR-B10-Electronic-Health-Information-Export.pdf`, verified via pdftotext extraction)

4. **Specialty-specific data for 23 specialties is not represented.** Practice EHR markets specialty-specific templates and workflows for specialties including cardiology, psychiatry, orthopedics, and dermatology. C-CDA cannot represent specialty-specific assessment data. (Source: product-research.md; no specialty data in export documentation)

5. **Patient portal and engagement data are absent.** Secure messages, appointment requests, prescription refill requests, and patient-entered intake data are not mentioned in the export. (Source: product-research.md cross-referenced with PDF)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + original-format documents + XLS index, in ZIP
Model type:      Standard projection (C-CDA R2.1)
Entities:        N/A (no data dictionary; export is 1 C-CDA file + document dump)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient described)
Domains covered: 0 of 19 fully; 10 of 19 partially (via C-CDA); 9 of 19 not covered
```

### Bottom Line

Practice EHR's (b)(10) export is a C-CDA clinical summary with attached document files — essentially the same data available through transitions of care, repackaged as an "EHI export." For a product that stores rich billing/claims, RCM, specialty clinical, and patient engagement data, this covers only the USCDI v1 clinical summary layer. The documentation is 295 words with no data dictionary, no schema, and no sample data. This is a compliance checkbox, not a genuine effort to enable comprehensive data portability.
