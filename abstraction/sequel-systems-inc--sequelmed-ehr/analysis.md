# EHI Export Analysis: Sequel Systems, Inc.

**Product**: SequelMed EHR V12
**Analysis date**: 2026-02-16
**CHPL IDs**: 11143 (15.04.04.2846.Sequ.12.01.1.221227)

## 1. Product Context

SequelMed EHR is an integrated EHR and practice management (PM) platform developed by Sequel Systems, Inc. (Melville, NY), targeting ambulatory physician practices across 24+ specialties. The product combines clinical EHR, practice management, medical billing, document management, and a patient portal into a single platform. It was ONC-certified in December 2022 (Drummond-certified).

Key data domains the product stores, per vendor materials:

- **Clinical**: Demographics, problem lists, medications, allergies, immunizations, vital signs, lab results, diagnostic images (DICOM integration), clinical encounter notes via customizable specialty templates, clinical decision support alerts, e-prescribing (SureScripts)
- **Financial/Billing**: Claims, charges, payments, patient A/R, collections, denials management, eligibility verification, authorization records, claim scrubbing, revenue cycle management
- **Administrative**: Scheduling, document management (scanning, archiving), multi-office coordination, enterprise reporting
- **Patient Engagement**: Patient portal (via Data Motion), online registration, messaging
- **Interoperability**: HL7, DICOM, FHIR APIs, C-CDA transitions of care, public health reporting (immunization registries, syndromic surveillance, electronic case reporting)

This product context is critical: SequelMed is sold as a combined EHR+PM platform, meaning a compliant (b)(10) export should cover both clinical and financial/billing data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `SequelMed-EHR-B10-Electronic-Health-Information-Export.pdf` (96,891 bytes, 4 pages) | The sole export documentation artifact. Describes export as a per-patient ZIP containing a C-CDA XML, a documents folder, and an unexplained XLS file. Version 1.0, created 2023-11-22. | **Primary** — this is the only substantive artifact |
| `data-export-page-screenshot.png` (124,243 bytes) | Screenshot of https://www.sequelmed.com/data-export/ showing a single bullet link to the PDF. No other content. | **Confirmatory** — confirms the page has a single link and nothing else |
| Vendor data export page (live verification) | Verified https://www.sequelmed.com/data-export/ is still live as of 2026-02-16. Still shows only the single PDF link. No additional documentation has been added since the prior collection. | **Confirmatory** |

**Total artifacts**: 2 (1 PDF, 1 screenshot). No data dictionary, no schema, no sample data, no additional documentation pages.

## 3. Export Mechanics

- **Format**: Per-patient ZIP file containing:
  1. A `Clinical` folder with one C-CDA XML file
  2. A `Documents` folder with patient documents in original formats (.jpg, .gif, .bmp, .png, .pdf, .txt)
  3. A `Patient Documents Detail.xls` file (undocumented)
- **Mechanism**: UI-driven; the documentation states users can export "at any time without developer assistance" for both single-patient and multi-patient scenarios. No screenshots or further UI details provided.
- **Single-patient**: Yes, explicitly supported
- **Bulk/multi-patient**: Yes, explicitly stated as available
- **Access constraints or fees**: None mentioned in the documentation

## 4. Export Content: What's In It

### Overview

The export documentation is a 4-page PDF (including cover page) with approximately 1.5 pages of substantive content and 45 non-blank lines of text. It provides **zero field-level documentation**. There is no data dictionary, no schema, no sample data, and no vendor-specific documentation of what data is included or excluded.

The export consists of three components:

### 4.1 C-CDA XML File (Clinical folder)

The documentation states the Clinical folder contains "one XML based CCDA file for the concerned patient" that "comply to US Core Data for Interoperability (USCD) [sic], Version 1 requirements." Three external HL7 specification references are provided.

**No vendor-specific documentation is provided** — no list of which C-CDA sections are populated, no description of vendor extensions, no mapping of SequelMed data to C-CDA elements. The reader is directed entirely to external HL7 specifications. Based on the USCDI V1 compliance claim, the C-CDA would typically include standard sections for demographics, allergies, medications, problems, procedures, lab results, vital signs, immunizations, goals, health concerns, and smoking status. However, SequelMed does not confirm this.

### 4.2 Patient Documents (Documents folder)

Six document types are listed:
1. Signed progress notes
2. Available lab results
3. Radiology reports
4. Scanned documents
5. Imported documents
6. "Iploaded" [sic] documents

Documents are exported in their original upload/scan formats. No metadata schema, naming convention, or organizational structure is documented.

### 4.3 Patient Documents Detail.xls

Mentioned by name only. Its purpose, columns, and content are entirely undocumented. It may serve as a document manifest, but this is speculation.

### Vendor's own content organization

The vendor does not organize their export into categories or provide a data dictionary. The only structure is the three-component ZIP:

| Component | Fields Documented | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA XML file | 0 | N/A | N/A | "Clinical" |
| Documents folder | 0 | Only document types listed | N/A | "Patient Documents" |
| Patient Documents Detail.xls | 0 | N/A | N/A | Undocumented |

**Total vendor-documented fields: 0**. The vendor provides no field-level, entity-level, or column-level documentation for any component of the export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two categories of exported content:

1. **"Clinical"** — A single C-CDA XML file per patient. The C-CDA is a standardized clinical summary format designed for transitions of care. Per the USCDI V1 claim, it would cover demographics, allergies, medications, problems, procedures, lab results, vital signs, immunizations, goals, and smoking status. However, C-CDA is structurally limited to clinical summary data — it cannot represent billing records, scheduling data, custom specialty templates, or the full breadth of an EHR+PM system's data.

2. **"Patient Documents"** — Unstructured files (images, PDFs, text) representing signed notes, lab results, radiology reports, and scanned/imported/uploaded documents. These are binary files in original format with no structured metadata.

The clinical coverage via C-CDA is a **thin projection** of what SequelMed stores. The entire practice management / billing side of the product is absent. No specialty-specific template data is documented. No orders, referrals, or e-prescribing history beyond what C-CDA can represent.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA header (inferred from USCDI V1 claim; not vendor-documented) | C-CDA covers basic demographics. Product likely stores richer demographic/contact data in PM module that C-CDA doesn't capture. |
| Encounters / visits | ⚠️ Partial | C-CDA may include encounter sections (not vendor-confirmed) | C-CDA encounter data is typically a summary. Full visit history, visit-linked data likely richer in native system. |
| Problems / conditions | ⚠️ Partial | C-CDA problem list (inferred) | Standard C-CDA section likely included. Specialty-specific condition tracking (24+ specialties) unlikely to be fully captured. |
| Medications / prescriptions | ⚠️ Partial | C-CDA medication list (inferred) | C-CDA captures active/historical medication list. Full e-prescribing history (SureScripts integration) unlikely to be represented. |
| Allergies | ⚠️ Partial | C-CDA allergies section (inferred) | Likely covered via standard C-CDA section. |
| Immunizations | ⚠️ Partial | C-CDA immunizations section (inferred) | Likely covered via standard C-CDA section. |
| Vitals | ⚠️ Partial | C-CDA vital signs section (inferred) | Likely covered via standard C-CDA section. |
| Lab results | ⚠️ Partial | C-CDA results section (inferred) + lab result documents in Documents folder | Structured results in C-CDA plus original lab documents. May miss order-level detail. |
| Imaging / diagnostic reports | ⚠️ Partial | Radiology reports in Documents folder (as files) | Unstructured report documents only. DICOM images and structured imaging data from PACS integration not included. |
| Procedures | ⚠️ Partial | C-CDA procedures section (inferred) | Standard C-CDA section likely included. |
| Clinical notes / documents | ⚠️ Partial | Signed progress notes in Documents folder + C-CDA may contain note sections | Progress notes exported as document files. Custom specialty template data (24+ specialties) unlikely to be in C-CDA or structured form. |
| Care plans / goals | ⚠️ Partial | C-CDA may include goals/care plan sections (inferred) | USCDI V1 includes goals; coverage uncertain without vendor confirmation. |
| Orders / referrals | ❌ Not covered | No evidence in export documentation | Product supports lab, pharmacy, and imaging orders. Not documented in export. |
| Insurance / coverage | ❌ Not covered | No evidence in export documentation | Product stores insurance/eligibility data (PM module). Not in C-CDA export. Significant gap. |
| Claims / billing | ❌ Not covered | No evidence in export documentation | Product has full billing/claims/RCM capabilities. Entire PM financial dataset absent. **Major gap.** |
| Payments | ❌ Not covered | No evidence in export documentation | Product manages payments, A/R, collections. Not in export. |
| Consents / directives | ❌ Not covered | No evidence in export documentation | No mention in product materials either; may be N/A. |
| Patient communications / portal messages | ❌ Not covered | No evidence in export documentation | Product has patient portal (via Data Motion). Portal data not in export. |
| Specialty-specific data | ❌ Not covered | No evidence in export documentation | Product claims 24+ specialty-specific templates. None of this structured data is documented in export. **Major gap.** |

**Summary**: Of 19 applicable domains, 0 are fully confirmed as covered, 11 are partially covered via inferred C-CDA content (none vendor-confirmed), and 8 are not covered at all. The most significant gaps are billing/claims data and specialty-specific clinical data — both core capabilities of the product.

## 6. Documentation Quality

The documentation quality is **extremely poor**:

- **4 pages total** including cover page; approximately 1.5 pages of substantive content
- **Zero field-level documentation** — no data dictionary, no field names, no types, no descriptions
- **Zero schema artifacts** — no machine-readable schemas, no C-CDA profiles, no mapping documents
- **Zero sample data** — no example exports, no worked examples
- **Zero screenshots** — no illustration of the export UI or workflow
- **Undocumented component** — the `Patient Documents Detail.xls` file is listed but never described
- **Typographical errors** — "Iploaded" instead of "Uploaded," "USCD" instead of "USCDI"
- **No scope statement** — the document never states what data is included in or excluded from the export, or why

A developer could **not** build an import from this documentation alone. They would need to rely entirely on external HL7 C-CDA specifications for the clinical data, and would have no guidance whatsoever on the documents folder or the XLS file. The documentation provides no information about what SequelMed-specific data is mapped to which C-CDA elements, what code systems are used, or how to reconstruct a patient record from the export.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a C-CDA clinical summary packaged with unstructured document files. This is essentially a transitions-of-care export relabeled as a (b)(10) export. It covers only what C-CDA can structurally represent (clinical summary data) and misses the entire practice management / billing side of the product, plus all specialty-specific clinical data captured through custom templates.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The entire structured export is a single C-CDA XML file per patient — a format designed for clinical summaries in transitions of care, not comprehensive EHI export. This is the classic failure mode of conflating (b)(10) with existing (b)(1)/(g)(10) functionality. *(Source: PDF page 2, "Clinical Data" section)*

2. **Complete absence of billing/financial data**: SequelMed is marketed and sold as an integrated EHR+PM platform with full billing, claims, A/R, collections, and RCM capabilities. None of this data appears in the export documentation. This is the single largest gap. *(Source: PDF contains no mention of billing, claims, payments, or financial data; product-research.md §Modules confirms extensive PM capabilities)*

3. **No data dictionary whatsoever**: The documentation provides zero field-level information. Not a single field name, type, or description is documented across the entire export. A vendor exporting native database tables typically documents hundreds of fields; SequelMed documents none. *(Source: full text of the 4-page PDF contains no field definitions)*

4. **Specialty-specific data missing**: The product claims to serve 24+ specialties with customizable clinical templates, implying structured specialty-specific data capture. None of this data is represented in the C-CDA format or documented in the export. *(Source: product-research.md §Modules; PDF contains no specialty references)*

5. **Undocumented XLS component**: The `Patient Documents Detail.xls` file is listed as part of the export but never described, suggesting minimal review of the documentation itself (further evidenced by the "Iploaded" typo). *(Source: PDF page 2, item 3)*

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + unstructured document files + undocumented XLS
Model type:      Standard projection (C-CDA R2.1)
Entities:        0 vendor-documented (C-CDA sections inferred from USCDI V1 claim: ~17)
Fields:          0 vendor-documented
Descriptions:    N/A (no field-level documentation)
Sample data:     No
Bulk export:     Yes (multi-patient stated)
Domains covered: 0 of 19 fully confirmed; ~11 of 19 partially inferred via C-CDA
```

### Bottom Line

A patient or provider would receive a C-CDA clinical summary and a folder of scanned/uploaded documents — essentially the same data available through transitions-of-care exchange, not a comprehensive export of all EHI. The entire billing/financial dataset from the practice management module and all specialty-specific clinical template data are absent. This is a textbook case of repackaging an existing C-CDA export as (b)(10) compliance, with documentation so thin (zero fields documented across 4 pages) that it's impossible to independently verify what data is actually included.
