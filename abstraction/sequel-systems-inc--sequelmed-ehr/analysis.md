# EHI Export Analysis: Sequel Systems, Inc.

**Product**: SequelMed EHR V12
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2846.Sequ.12.01.1.221227 (CHPL listing 11143)

## 1. Product Context

SequelMed EHR is an integrated EHR and practice management (PM) platform developed by Sequel Systems, Inc. (Melville, NY, founded 1995). It targets ambulatory physician practices across 24+ specialties, including cardiology, dermatology, gastroenterology, internal medicine, neurology, OB/GYN, orthopedics, pediatrics, physical therapy, podiatry, psychiatry, and urgent care. The product is sold as a combined EHR + PM suite or as standalone modules.

**Key data domains the product stores (per vendor website and product research):**

- **Clinical**: Demographics, problem lists, medication lists, allergies, immunizations, vital signs, H&P exams, clinical encounter notes via customizable specialty templates, clinical decision support alerts
- **Orders/results**: Lab orders, pharmacy orders, imaging orders, lab results, diagnostic imaging results (DICOM integration)
- **Medications**: E-prescribing via SureScripts, medication history
- **Documents**: Clinical documents, scanned/archived documents (document management module), C-CDA documents
- **Financial/billing**: Claims, charges, payments, patient A/R, collections, denials management, eligibility verification, authorization records, plan-specific billing edits, revenue cycle management, enterprise-wide reporting
- **Scheduling**: Appointment scheduling
- **Patient portal**: Messages, patient registration, accessible medication lists and immunization records (via Data Motion third-party integration)
- **Public health**: Immunization registry submissions, syndromic surveillance, electronic case reporting

The product is ONC-certified (certified 2022-12-27) for a broad set of criteria including (b)(10) EHI export, FHIR APIs (g)(7)–(g)(10), transitions of care (b)(1)–(b)(3), and patient portal (e)(1). This is a small vendor with a modest user base (only 7–9 reviews on third-party sites).

**Baseline expectation for (b)(10) completeness**: A comprehensive export should cover clinical data, billing/PM data, specialty-specific template data, orders, documents, insurance/coverage, and prescription history — reflecting the full breadth of the integrated EHR+PM system.

## 2. Artifacts Reviewed

| # | Artifact | Type | Size | Description | Informativeness |
|---|---|---|---|---|---|
| 1 | `SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf` | PDF | 96,891 bytes, 4 pages | The entire EHI export documentation. Describes export structure (ZIP per patient with C-CDA, documents, and an XLS). Version 1.0, created 2023-11-22. | **Primary artifact** — sole source of export documentation |
| 2 | `data-export-page-screenshot.png` | PNG | 124,243 bytes | Screenshot of the data export landing page on sequelmed.com. Shows a single bullet link to the PDF. | Low — confirms there is only one document |

**Additional verification**: The live data export page at `https://www.sequelmed.com/data-export/` was verified as accessible on 2026-02-15. It remains unchanged from collection: a single heading "Data Export" with one bullet link to the PDF. No additional documentation, schemas, sample data, or data dictionaries exist on the site.

**Total artifacts**: 2 (1 substantive PDF, 1 screenshot). This is an extremely thin artifact set.

## 3. Export Mechanics

- **Format**: ZIP archive per patient
- **Contents per ZIP**:
  1. `Clinical/` folder — one C-CDA XML file
  2. `Documents/` folder — patient documents in original file format
  3. `Patient Documents Detail.xls` — Excel file (contents undocumented)
- **Mechanism**: Appears to be a UI-driven export within the SequelMed EHR application. The documentation states users can export "at any time without developer assistance."
- **Single-patient**: Yes — explicitly supported
- **Bulk/multi-patient**: Yes — documentation states "multi patients" export is available "at any time without developer assistance"
- **Access constraints**: None documented; no mention of fees, special permissions, or rate limits
- **Data standard**: C-CDA (HL7 CDA R2, Consolidated CDA Templates R2.1), claiming USCDI V1 compliance

## 4. Export Content: What's In It

### 4.1 Overview

The export consists of exactly three components per patient. There is **no data dictionary**, **no field-level documentation**, **no schema files**, and **no sample data**. The entire documentation is 295 words across 3 content pages (page 1 is a cover page).

### 4.2 Component 1: C-CDA XML File (Clinical folder)

The clinical data is exported as a single C-CDA XML file per patient. The documentation states it is "standard based which comply to US Core Data for Interoperability (USCD), Version 1 requirements" (note: "USCD" is a typo for "USCDI").

Based on the C-CDA R2.1 standard referenced, a conformant C-CDA would typically include these sections:

- Demographics (patient header)
- Problems / conditions
- Medications
- Allergies and adverse reactions
- Immunizations
- Vital signs
- Lab results (within Results section)
- Procedures
- Encounters
- Plan of treatment
- Goals
- Social history
- Functional status

**However**: The SequelMed documentation does not specify which C-CDA sections are populated, which are optional, or what vendor-specific data (if any) is included. There is no mention of vendor extensions, custom sections, or specialty-specific data mapped into the C-CDA. The documentation simply references the external HL7 specifications and provides no SequelMed-specific detail.

**What is NOT in a C-CDA by design**: Billing data, claims, charges, payments, A/R records, scheduling data, orders (as discrete records — some may appear in Plan of Treatment), e-prescribing history (beyond current medication list), insurance/coverage details, custom specialty template data, patient portal messages, document management metadata.

### 4.3 Component 2: Patient Documents (Documents folder)

Six types of documents are listed:
1. Signed progress notes
2. Available lab results
3. Radiology reports
4. Scanned documents
5. Imported documents
6. "Iploaded" [sic] documents

Documents are exported in their original uploaded/scanned format: `.jpg`, `.gif`, `.bmp`, `.png`, `.pdf`, `.txt`.

These are **unstructured files** — scans, images, text documents. No structured metadata about the documents is described (though see Component 3 below). There is no documentation of how documents are named, organized, or cross-referenced to clinical encounters.

### 4.4 Component 3: Patient Documents Detail.xls

An Excel file described only by its filename. The documentation provides **zero explanation** of what this file contains — no column names, no sample rows, no description of its purpose. It presumably serves as a manifest or index for the documents in the Documents folder, but this is inference, not documentation.

### Vendor's own content organization

The vendor does not organize their export documentation into categories or provide a data dictionary. The only structure is the three-component ZIP described above:

| Component | Type | Fields Documented | Types Documented | Category |
|---|---|---|---|---|
| C-CDA XML file | XML (C-CDA R2.1) | None (defers to external HL7 spec) | N/A | Clinical |
| Documents folder | Mixed file formats | None | N/A | Documents |
| Patient Documents Detail.xls | Excel | None | N/A | Unknown |

**There are zero vendor-documented entities, zero vendor-documented fields, and zero field-level descriptions.** The clinical data format is delegated entirely to the external C-CDA standard with no vendor-specific documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation describes two data flows:

1. **Structured clinical data via C-CDA**: The vendor claims USCDI V1 compliance, which means the C-CDA should include demographics, problems, medications, allergies, immunizations, vital signs, lab results, clinical notes, procedures, and care team. However, no vendor-specific documentation confirms which sections are actually populated, and C-CDA cannot represent the full breadth of data an EHR+PM system stores.

2. **Unstructured document files**: Progress notes, lab results, radiology reports, and scanned/imported/uploaded documents are exported as raw files. This captures some clinical content in unstructured form but provides no structured data.

**Completely absent from the export documentation**: The entire practice management (PM) module — billing, claims, charges, payments, A/R, collections, denials, insurance/coverage, eligibility, authorization. Also absent: scheduling data, orders, e-prescribing history, specialty-specific template data, patient portal data, referrals.

The vendor's export is structurally identical to a transitions-of-care (ToC) export — a C-CDA clinical summary plus attached documents. This is a standard-based projection of clinical data, not a comprehensive export of the product's native data model.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA patient header (inferred from standard, not vendor-documented) | C-CDA includes basic demographics; product likely stores more (contacts, employer, etc.) |
| Encounters / visits | ⚠️ Partial | C-CDA Encounters section (inferred) | Only what C-CDA captures; no visit-level billing or scheduling linkage |
| Problems / conditions | ⚠️ Partial | C-CDA Problems section (inferred) | Standard C-CDA coverage; no vendor confirmation of completeness |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications section (inferred) | Current medication list only; product does e-prescribing via SureScripts — full Rx history likely not in C-CDA |
| Allergies | ⚠️ Partial | C-CDA Allergies section (inferred) | Standard C-CDA coverage |
| Immunizations | ⚠️ Partial | C-CDA Immunizations section (inferred) | Standard C-CDA coverage |
| Vitals | ⚠️ Partial | C-CDA Vital Signs section (inferred) | Standard C-CDA coverage |
| Lab results | ⚠️ Partial | C-CDA Results section (inferred) + document files (lab results) | Structured results in C-CDA limited to what C-CDA supports; raw lab documents also exported |
| Imaging / diagnostic reports | ⚠️ Partial | Document files (radiology reports) | Unstructured only; no DICOM images, no structured radiology data |
| Procedures | ⚠️ Partial | C-CDA Procedures section (inferred) | Standard C-CDA coverage |
| Clinical notes / documents | ⚠️ Partial | Document files (signed progress notes, scanned documents, imported/uploaded documents) | Unstructured file export; no structured note data beyond what's in C-CDA |
| Care plans / goals | ⚠️ Partial | C-CDA Plan of Treatment/Goals sections (inferred) | Standard C-CDA coverage if populated |
| Orders / referrals | ❌ Not covered | No evidence in export | Product supports lab, pharmacy, and imaging orders — not mentioned in export |
| Insurance / coverage | ❌ Not covered | No evidence in export | Product stores insurance/enrollment data for billing — not exported |
| Claims / billing | ❌ Not covered | No evidence in export | Product has full billing/PM module (claims, charges, payments, A/R, denials) — **significant gap** |
| Payments | ❌ Not covered | No evidence in export | Product processes payments — not exported |
| Consents / directives | ❌ Not covered | No evidence in export | Unknown if product stores these |
| Patient communications / portal messages | ❌ Not covered | No evidence in export | Product has patient portal via Data Motion — not exported |
| Specialty-specific data | ❌ Not covered | No evidence in export | Product claims 24+ specialty templates with customizable clinical forms — **significant gap** |

**Summary**: All "Partial" ratings are cautious because the vendor provides no documentation confirming which C-CDA sections are actually populated. The coverage ratings are based on what a conformant C-CDA R2.1 *could* include, not on what SequelMed's C-CDA actually includes.

**Major gaps**: The entire billing/PM domain (claims, charges, payments, A/R, collections, denials, insurance) and specialty-specific clinical template data are absent from the export despite being core features of the product.

## 6. Documentation Quality

The export documentation is **extremely poor** by any standard:

- **Total documentation**: 295 words across 3 content pages of a 4-page PDF (page 1 is a cover). This is approximately one page of actual informational content.
- **Data dictionary**: None. Zero fields are documented.
- **Schema/profiles**: None. The vendor defers entirely to external HL7 C-CDA specifications without documenting any SequelMed-specific constraints, extensions, or mappings.
- **Sample data**: None. No example exports, worked examples, or screenshots of the export interface.
- **Machine-readable artifacts**: None.
- **Value sets/code systems**: Not mentioned.
- **Relationships**: Not documented.
- **Patient Documents Detail.xls**: Completely undocumented — not even a single sentence explaining its contents.
- **Typos**: "Iploaded" instead of "Uploaded" (page 3), "USCD" instead of "USCDI" (page 2) — suggests minimal review.

**Could a developer build an import from this documentation?** No. A developer would need to independently implement a C-CDA parser (using the external HL7 specs), guess at the structure of the XLS file, and manually correlate document files to clinical records. There is no SequelMed-specific guidance whatsoever.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a C-CDA clinical summary packaged with attached document files. This is functionally identical to a transitions-of-care export repackaged as a (b)(10) export. It covers the USCDI V1 clinical summary data subset but cannot represent the full breadth of data the EHR+PM system stores (billing, specialty templates, orders, scheduling, insurance). There is no native data model export.

### Key Findings

1. **The export is a C-CDA repackaged as (b)(10).** The structured clinical data is a single C-CDA XML file — a transitions-of-care format designed for clinical summaries, not comprehensive data export. This is the most common (b)(10) failure mode. *(Source: `SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf`, page 2)*

2. **The entire billing/PM domain is absent.** SequelMed is marketed and sold as an integrated EHR + Practice Management platform with full billing, claims, payments, A/R, and revenue cycle management. None of this data is mentioned in the export documentation. *(Source: vendor website features vs. export PDF)*

3. **Zero field-level documentation.** The documentation contains no data dictionary, no field names, no types, no descriptions, no value sets, and no relationships. The vendor provides 295 words total to describe an export of "all electronic health information." *(Source: `pdf_analysis.json` — 295 words, 0 fields documented)*

4. **Specialty-specific clinical data is not exported.** The product claims to serve 24+ specialties with customizable clinical templates. This specialty-specific data cannot be represented in a standard C-CDA and is not mentioned in the export. *(Source: vendor website claims 24+ specialties; export PDF mentions only C-CDA)*

5. **The Patient Documents Detail.xls is completely undocumented.** One of the three export components is an Excel file whose contents are never described — not even a single sentence. *(Source: `SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf`, page 2)*

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + document files (mixed formats) + XLS, packaged as ZIP
Model type:      Standard projection (C-CDA R2.1 / USCDI V1)
Entities:        N/A (no data dictionary; 1 C-CDA document + attached files)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient documented)
Domains covered: 0 of 15 confirmed; ~10 of 15 inferred from C-CDA standard (not vendor-verified)
```

### Bottom Line

SequelMed's (b)(10) export is a textbook case of C-CDA repackaging: a transitions-of-care clinical summary plus document attachments, presented as a comprehensive EHI export. A patient or provider receiving this export would get a clinical summary and their scanned documents, but would be missing all billing/financial records, specialty-specific clinical data, orders, prescription history, insurance information, and portal communications — the majority of what a combined EHR+PM system stores about them. The documentation is among the thinnest possible while technically existing (295 words, no data dictionary, no schema, no sample data).
