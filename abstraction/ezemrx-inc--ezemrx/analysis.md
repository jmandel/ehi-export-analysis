# EHI Export Analysis: ezEMRx Inc

**Product**: ezEMRx (version 10.01)
**Analysis date**: 2026-02-16
**CHPL IDs**: 10779 (CHPL Product Number: 15.02.05.2886.EZEM.01.01.1.220105)

## 1. Product Context

ezEMRx is an ONC-ACB certified electronic health record with integrated practice management, billing, and inventory management built by ezEMRx Inc (Elgin, Illinois). It serves two primary markets: **public health departments** (via an exclusive partnership with Custom Data Processing, Inc. [CDP], deployed in 1,000+ locations) and **private ambulatory clinics** across multiple specialties including primary care, OB/GYN, behavioral health, substance abuse, and immunization clinics.

The product is a full-featured ambulatory EHR certified against 40+ ONC criteria. Its functional scope includes:

- **Clinical**: Patient charting, clinical documentation, e-prescribing, clinical decision support, treatment plans, immunization tracking, customizable templates for specialties (behavioral health, substance abuse, TB/STD/HIV, family planning, home health)
- **Practice management**: Appointment scheduling, patient registration, household management
- **Billing & revenue cycle**: Integrated billing with claims scrubbing, electronic claims submission, real-time eligibility verification, sliding fee schedules, auto-adjudication, payment posting, denial tracking, patient statements, merchant services (credit card/check processing), optional outsourced RCM services
- **Inventory**: Medication/supply tracking with barcode scanning, vaccine batch management
- **Patient engagement**: Patient portal, appointment reminders, self-registration with QR codes
- **Interoperability**: HIE portal, HL7/CCD/CDA, DIRECT messaging, FHIR APIs
- **Public health reporting**: Immunization registry, syndromic surveillance, cancer case reporting

Given this breadth, a complete EHI export should cover clinical records across multiple specialties, billing/claims data, insurance/coverage information, medications, labs, immunizations, inventory records linked to patients, and patient portal communications.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informative? |
|---|---|---|---|
| `ehi-export-page-text.txt` | 2,144 bytes (24 lines) | Extracted text from the rendered EHI export page. Contains regulatory definition of EHI (45 CFR), §170.315(b)(10) compliance bullet points, and a paragraph promising documentation about export files. | Low — no technical content |
| `ehi-export-page-full.png` | 820,944 bytes | Full-page screenshot of https://www.ezemrx.com/ehi-export. Shows header, dark compliance section, large blank area (empty PDF Viewer Pro widget), and introductory text for documentation that was never published. | Low — confirms page structure and empty state |
| `ehi-export-page-blank-area.png` | 89,506 bytes | Screenshot of the PDF Viewer Pro widget area. Contrary to the prior agent's description of this area as "blank," this screenshot actually shows a PDF cover page with document metadata (see below). However, the PDF content beyond the cover page is not visible or accessible. | Moderate — confirms a PDF document exists/existed |

### Key observation: PDF cover page visible in screenshot

The `ehi-export-page-blank-area.png` screenshot shows a PDF document loaded in the PDF Viewer Pro widget with the following cover page metadata:

- **Title**: 170.315(b) (10) Electronic Health Information (EHI) Export
- **Certification ID**: CHPL ID# 15.02.05.2886.EZEM.01.01.1.220105
- **Product Version**: ezEMRx Ver 10.01
- **Prepared By**: ezEMRx Integration Team
- **Document Control ID**: 01US03P98C001
- **Version**: 1.0
- **Approved By**: Technology Office – Siri Kumar; Product Development – Balamurugan Jayaraj; Product Management – Balaji Venkatesh

This indicates that an EHI export documentation PDF was created and at one point loaded into the page's PDF viewer widget. However, this PDF is **not currently accessible**: verification on 2026-02-16 using both headless Puppeteer and visible Chrome confirmed that the PDF Viewer Pro iframe has no `src` attribute and renders as empty white space. The PDF appears to have been removed or its configuration broken since the Feb 15 collection screenshot.

Only the cover page is visible in the screenshot; **no data dictionary content, schema information, or technical documentation** is visible or accessible from this artifact.

### Independent verification (2026-02-16)

- **Web fetch**: Page returns 200 but Wix SPA renders only regulatory text client-side; no PDF URLs in HTML source
- **Puppeteer headless**: PDF Viewer Pro iframe has empty `src` attribute; no PDF-related network requests observed
- **Visible Chrome**: Full page renders with large empty white area where PDF viewer sits; no PDF content displayed
- **Wix media search**: Checked all 36 Wix media IDs (`3276af_*`) found in page source against `media.wixstatic.com/ugd/` PDF URL pattern — none returned a PDF
- **Wayback Machine**: No PDF files archived for ezemrx.com domain
- **Web search**: No publicly available EHI export documentation found for ezEMRx anywhere online

## 3. Export Mechanics

**What can be determined from available documentation:**

- The page text states that users can "Export EHI for a single patient at any time the user chooses without Developer assistance" and that the export "must be electronic and in a computable format" — but these are regulatory requirements being restated, not descriptions of actual implementation.
- The text states: "It is assumed that the user is familiar with the functions and features within ezEMRx to access and execute the EHI export capability from within ezEMRx." — This implies a UI-based export mechanism exists within the product.
- Single-patient and patient-population export capabilities are claimed.

**What cannot be determined:**

- Export format (CSV, JSON, FHIR, C-CDA, XML, SQL dump, or other)
- Whether the export is the native data model or a standard projection
- Specific UI mechanism for initiating export
- Access constraints, role requirements, or fees
- Whether bulk/population export is truly supported vs. just claimed
- Timeline or performance characteristics

## 4. Export Content: What's In It

**No content information is available.** The documentation page provides zero information about what data the export contains. Specifically:

- **No data dictionary**: No table definitions, entity listings, or field inventories
- **No schema**: No JSON Schema, XSD, DDL, or other machine-readable structure definitions
- **No format specification**: No description of file formats, encoding, delimiters, or data organization
- **No sample data**: No example export files or sample records
- **No field descriptions**: No documentation of field names, types, constraints, value sets, or relationships
- **No entity listing**: Not even a high-level list of what categories of data are included in the export

### Vendor's own content organization

Cannot be assessed. The vendor provides no information about how the export data is organized, categorized, or structured.

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| *(none documented)* | — | — | — | — |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Cannot be assessed.** The vendor provides no documentation of export content. The only content on the EHI export page is:
1. A regulatory definition of EHI copied from 45 CFR
2. Bullet points restating §170.315(b)(10) requirements
3. A promise that "documentation listed on this page" will explain the export files — but no such documentation exists

The presence of a PDF cover page (visible in a Feb 15 screenshot) suggests a documentation effort was started (Document Control ID: 01US03P98C001, Version 1.0), but the document is not publicly accessible.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❓ Unknown | No documentation | Product stores demographics; cannot assess export coverage |
| Encounters / visits | ❓ Unknown | No documentation | Product stores encounter data; cannot assess export coverage |
| Problems / conditions / diagnoses | ❓ Unknown | No documentation | Certified for (a)(4) Problem List; cannot assess export coverage |
| Medications / prescriptions | ❓ Unknown | No documentation | Certified for (a)(1) CPOE Medications; cannot assess export coverage |
| Allergies | ❓ Unknown | No documentation | Certified for (a)(3) Demographics; cannot assess export coverage |
| Immunizations | ❓ Unknown | No documentation | Certified for (f)(1) Immunization Registry; product is heavily used for immunization clinics; cannot assess export coverage |
| Vitals | ❓ Unknown | No documentation | Certified for (a)(2) CPOE Lab; cannot assess export coverage |
| Lab results | ❓ Unknown | No documentation | Certified for lab-related criteria; cannot assess export coverage |
| Clinical notes / documents | ❓ Unknown | No documentation | Product supports clinical documentation; cannot assess export coverage |
| Care plans / goals | ❓ Unknown | No documentation | Product supports treatment plans; cannot assess export coverage |
| Insurance / coverage | ❓ Unknown | No documentation | Product does eligibility verification and billing; cannot assess export coverage |
| Claims / billing | ❓ Unknown | No documentation | Product has full billing/RCM capabilities; cannot assess export coverage |
| Payments | ❓ Unknown | No documentation | Product processes payments; cannot assess export coverage |
| Medications inventory | ❓ Unknown | No documentation | Product tracks medication inventory with barcodes; cannot assess export coverage |
| Behavioral health / substance abuse | ❓ Unknown | No documentation | Product explicitly supports behavioral health and substance abuse workflows; cannot assess export coverage |
| Patient portal / communications | ❓ Unknown | No documentation | Product has patient portal; cannot assess export coverage |

**Note**: Every domain is marked "Unknown" because the vendor provides no information whatsoever about what the export contains. This is not a case of partial or thin documentation — it is a complete absence of documentation.

## 6. Documentation Quality

The documentation quality is **effectively nonexistent**. The EHI export page at https://www.ezemrx.com/ehi-export:

- **Cannot support any developer workflow**: A developer receiving an EHI export from ezEMRx would have zero public documentation to help interpret the data. There is no data dictionary, no schema, no format specification, and no sample data.
- **Contains only regulatory boilerplate**: The page text consists entirely of regulatory definitions (45 CFR quotes) and compliance requirement bullet points (§170.315(b)(10) restated). None of this is technical documentation about the actual export.
- **Has an empty PDF viewer**: A Wix PDF Viewer Pro widget is present on the page, intended to display export documentation, but currently has no PDF loaded. A screenshot from 2026-02-15 shows a PDF cover page was visible at one point, but the document is not accessible.
- **Promises documentation it doesn't deliver**: The page explicitly states "The documentation listed on this page is intended to provide the user an understanding of the resulting files from the EHI Export" — but no such documentation exists on the page.
- **No machine-readable artifacts**: No JSON Schema, no XSD, no DDL, no API specs, no sample files.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The EHI export documentation page is a compliance placeholder. It exists at the registered URL, contains regulatory language, but provides no technical content whatsoever. The export itself may or may not exist in the product (the system was certified for (b)(10) in January 2022), but there is no public documentation to describe what it exports, in what format, or how to interpret the results.

### Key Findings

1. **Empty documentation shell**: The EHI export page contains zero technical documentation — no data dictionary, no schema, no format spec, no sample data. The page consists entirely of regulatory text copied from 45 CFR and ONC requirements. (Source: `ehi-export-page-text.txt`, 2,144 bytes / 24 lines of text, independently verified 2026-02-16)

2. **PDF viewer widget with no PDF loaded**: The page includes a Wix PDF Viewer Pro widget where export documentation was intended to be displayed, but the widget currently has no document configured. A screenshot from 2026-02-15 (`ehi-export-page-blank-area.png`) shows a PDF cover page (Document Control ID: 01US03P98C001, Version 1.0) was visible at one point, suggesting documentation was created but is no longer accessible.

3. **Introductory text promises undelivered documentation**: The page contains a paragraph explicitly promising documentation about "resulting files from the EHI Export" that would "explain how to read the files, understand the meaning behind fields." This documentation does not exist on the page — it is a forward reference to content that was never published.

4. **Significant scope mismatch**: ezEMRx is a full-featured EHR + PM + billing + inventory system serving 1,000+ public health locations with specialized workflows for immunization, behavioral health, substance abuse, and more. The complete absence of export documentation makes it impossible to assess whether the export covers the full breadth of data the system stores.

5. **Four-year certification gap**: The product was certified for §170.315(b)(10) in January 2022 — over 4 years ago. The absence of public documentation after this period suggests this is not a temporary oversight but a persistent compliance gap.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Unknown (no documentation)
Model type:      Unknown (no documentation)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Claimed but unverifiable
Domains covered: 0 of 16 verifiable (all unknown due to no documentation)
```

### Bottom Line

A patient or provider requesting an EHI export from ezEMRx would receive data with no publicly available documentation to interpret it. The export page is a compliance checkbox — a shell with regulatory text, an empty PDF viewer, and a paragraph promising documentation that was never delivered. For a system deployed across 1,000+ public health locations handling clinical, billing, behavioral health, and immunization data, the complete absence of export documentation represents a significant gap in transparency and usability.
