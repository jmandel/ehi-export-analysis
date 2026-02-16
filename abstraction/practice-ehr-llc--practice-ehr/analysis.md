# EHI Export Analysis: Practice EHR LLC

**Product**: Practice EHR V12
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2997.Prac.12.01.1.220628

## 1. Product Context

Practice EHR is a cloud-based, all-in-one ambulatory EHR and practice management platform targeting small to mid-sized medical practices across 23+ specialties (family medicine, cardiology, orthopedics, psychiatry, etc.). The product is a single integrated platform covering:

- **Clinical documentation**: Specialty-specific templates, progress notes, AI Scribe transcription, point-and-click and free-text charting
- **E-prescribing**: Surescripts-certified including EPCS, formulary/eligibility checking, drug interaction alerts
- **Lab integration**: Electronic ordering and results (Quest, Labcorp, regional labs)
- **Billing & claims**: Electronic superbills, claim scrubbing, submission to 16,000+ payers, ERA processing, denial management, payment posting
- **Revenue cycle management**: Eligibility verification, KPI dashboards, optional staffed RCM services
- **Patient portal**: Secure messaging, appointment requests, refill requests, statement viewing/payment
- **Patient check-in kiosk**: iPad-based intake, demographics, insurance, consent forms
- **Telehealth**: Integrated virtual visits
- **Scheduling**: Multi-provider, multi-location with automated reminders
- **Reporting**: Practice dashboards, financial analytics, MIPS/CQM reporting

This baseline is critical: Practice EHR stores extensive clinical, billing, scheduling, patient engagement, and practice management data. A compliant (b)(10) export should cover all patient-facing data across these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Practice-EHR-B10-Electronic-Health-Information-Export.pdf` (116 KB, 4 pages) | The sole EHI export documentation. A cover page plus 3 pages describing export structure at the folder/file level. Created with Microsoft Word on 2023-11-22, Version 1.0. No data dictionary, no schema, no sample data. | **Primary artifact** — contains all available export documentation |
| `data-export-page.png` (257 KB) | Screenshot of the vendor's data export landing page at `practiceehr.com/data-export`. Shows a "Data Export" banner heading with a single link to the PDF. | Confirms the page has no additional content |
| Live web page at `practiceehr.com/data-export` | Verified live on 2026-02-16. Still contains only the single PDF download link. No additional documentation, schemas, or sample data have been added since the 2026-02-14 collection. | Confirms no updates |

## 3. Export Mechanics

- **Format**: ZIP file per patient containing: (1) a Clinical folder with one C-CDA XML file, (2) a Documents folder with scanned/uploaded files in original formats, (3) a `Patient Documents Detail.xls` index file
- **Mechanism**: Described as user-initiated ("at any time without developer assistance") but no UI screenshots, menu paths, or step-by-step instructions are provided
- **Single-patient**: Supported
- **Bulk/multi-patient**: Supported (described as "Multi-Patient Export")
- **Access constraints or fees**: Not documented in the PDF; no mention of fees or access restrictions

## 4. Export Content: What's In It

The export contains exactly three components per patient, none of which have field-level documentation:

### 4a. Clinical folder (C-CDA XML)

A single C-CDA XML file per patient conforming to C-CDA R2.1 / USCDI v1 (the document misspells "USCDI" as "USCD"). The PDF references three HL7 specifications but provides:

- **No list of C-CDA sections populated** (e.g., no indication of which of the ~17 possible C-CDA sections are included)
- **No template IDs** used
- **No vendor-specific extensions** documented
- **No field mapping** from Practice EHR's internal data model to C-CDA elements
- **No sample C-CDA file**

Based solely on the USCDI v1 / C-CDA R2.1 standard reference, the clinical data likely covers at most: demographics, problems, medications, allergies, immunizations, vitals, lab results, procedures, care team, goals, health concerns, and smoking status. This is the standard clinical summary content — the same data available through any C-CDA Transitions of Care export.

### 4b. Documents folder

Unstructured document files exported in their original upload/scan formats (.jpg, .gif, .bmp, .png, .pdf, .txt). The PDF lists six document types:

1. Signed progress notes
2. Available lab results
3. Radiology reports
4. Scanned documents
5. Imported documents
6. Uploaded documents (typo: "Iploaded" in original)

No documentation describes how these files are named, organized, or linked to encounters/dates.

### 4c. Patient Documents Detail.xls

An Excel spreadsheet included in the ZIP. **Its structure, columns, and contents are completely undocumented.** The PDF mentions it by name only.

### Vendor's own content organization

The vendor does not organize export content into categories or provide a data dictionary. The entire export is described at the container level only:

| Component | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA XML file | N/A (standard reference only) | No | No | "Clinical Data" |
| Documents folder | N/A (unstructured files) | No | No | "Patient Documents" |
| Patient Documents Detail.xls | Unknown | No | No | (not categorized) |

There are **0 entities/tables documented**, **0 fields documented**, and **0 field descriptions** provided. The entire documentation operates at the file-format level, not the data-element level.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes two categories of export content:

1. **"Clinical Data"** — A single C-CDA file per patient. By referencing C-CDA R2.1 / USCDI v1, this implicitly covers standard clinical summary data classes. However, C-CDA is a clinical summary standard designed for care transitions — it captures a subset of structured clinical data but excludes billing, scheduling, detailed prescription history, custom forms, patient communications, and specialty-specific assessments.

2. **"Patient Documents"** — A dump of uploaded/scanned files in their original formats. This potentially captures signed notes, lab results, and radiology reports as document images — but as unstructured files, not queryable data. These are supplementary attachments, not structured EHI.

The vendor provides no documentation of what fields are in the C-CDA, no description of the XLS index file, and no indication that any data beyond C-CDA and document attachments is exported.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implicitly in C-CDA patient header; no field-level detail | C-CDA demographics are limited (name, DOB, address, phone, race, ethnicity, language). Product stores richer data via kiosk intake (emergency contacts, employer, etc.) |
| Encounters / visits | ⚠️ Partial | Implicitly in C-CDA encounters section, if populated | No confirmation encounters section is populated; no encounter-level detail documented |
| Problems / conditions | ⚠️ Partial | Implicitly in C-CDA problems section | Standard C-CDA section; likely present but unconfirmed |
| Medications / prescriptions | ⚠️ Partial | Implicitly in C-CDA medications section | C-CDA captures active medications but not full prescription history, EPCS records, formulary checks, renewal workflows |
| Allergies | ⚠️ Partial | Implicitly in C-CDA allergies section | Standard C-CDA section; likely present but unconfirmed |
| Immunizations | ⚠️ Partial | Implicitly in C-CDA immunizations section | Standard C-CDA section; likely present but unconfirmed |
| Vitals | ⚠️ Partial | Implicitly in C-CDA vital signs section | Standard C-CDA section; likely present but unconfirmed |
| Lab results | ⚠️ Partial | Implicitly in C-CDA results section; also document attachments | Structured results in C-CDA, some as document images. Lab ordering data not included |
| Imaging / diagnostic reports | ⚠️ Partial | Document attachments only ("radiology reports") | Unstructured image/PDF files only; no structured imaging data |
| Procedures | ⚠️ Partial | Implicitly in C-CDA procedures section | Standard C-CDA section; likely present but unconfirmed |
| Clinical notes / documents | ⚠️ Partial | "Signed progress notes" as document attachments | Notes exported as unstructured files (images/PDFs), not as structured text. Adequate for reading but not for data migration |
| Care plans / goals | ⚠️ Partial | Implicitly in C-CDA if populated | USCDI v1 includes goals; presence in this vendor's C-CDA is unconfirmed |
| Orders / referrals | ❌ Not covered | No evidence in export documentation | Product supports lab ordering and referrals; significant gap |
| Insurance / coverage | ❌ Not covered | No mention of insurance data in export | Product stores insurance/eligibility data via kiosk and billing; significant gap |
| Claims / billing | ❌ Not covered | No mention of claims, superbills, or billing data | Product has extensive billing/claims features (claim submission, scrubbing, ERA); **major gap** |
| Payments | ❌ Not covered | No mention of payment records | Product handles payment posting, adjustments, patient statements; significant gap |
| Consents / directives | ❌ Not covered | No mention of consent forms | Product collects consent forms via kiosk; gap |
| Patient communications / portal messages | ❌ Not covered | No mention of portal messages or patient communications | Product has patient portal with secure messaging; significant gap |
| Specialty-specific data | ❌ Not covered | No mention of specialty templates or custom data | Product markets 23+ specialty-specific templates and workflows; **major gap** |

**Summary**: Of 19 applicable domains, 0 are fully covered, 11 have partial implicit coverage via C-CDA reference (without any confirmation of which sections are actually populated), and 8 have no coverage at all. The 8 missing domains include billing, payments, insurance, orders, communications, consents, and specialty-specific data — all data types that Practice EHR stores as core functionality.

## 6. Documentation Quality

The export documentation quality is extremely poor:

- **Data dictionary**: None. Zero entities, tables, or fields are documented.
- **Field names/types/descriptions**: None provided for any component.
- **Schema or machine-readable artifacts**: None.
- **Sample data**: None. No example C-CDA files, no example XLS files, no example document structures.
- **Relationships**: Not applicable — no data model is described.
- **Value sets / code systems**: Not documented; C-CDA standard is referenced but vendor-specific mappings are absent.
- **Developer usability**: A developer could not build an import from this documentation. The C-CDA sections populated are unknown, the XLS structure is unknown, and the document naming/organization is unknown.
- **Quality issues**: Two typos in a 3-page document ("USCD" for "USCDI" on page 3, "Iploaded" for "Uploaded" on page 4), suggesting minimal review.

The documentation reads as a compliance checkbox — enough to claim (b)(10) documentation exists, but insufficient for any practical use.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The export is a C-CDA clinical summary repackaged as an EHI export, supplemented by a document dump. This is the classic (b)(10) anti-pattern where a vendor points to their existing Transitions of Care C-CDA export and calls it "all electronic health information." The C-CDA covers at most USCDI v1 clinical summary data — approximately 15-20% of what this full-featured ambulatory EHR + practice management platform stores about patients.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The entire "EHI export" is a C-CDA XML file (the same format used for transitions of care under (b)(1)-(b)(3)) plus a folder of scanned document files. This is not a comprehensive data export — it's a clinical summary with attachments.

2. **Zero field-level documentation**: The 3-page PDF contains no data dictionary, no field definitions, no table/entity descriptions, no schemas, and no sample data. The XLS index file included in the export is mentioned by name but its contents are completely undescribed.

3. **Entire billing/PM domain missing**: Practice EHR is a combined EHR + practice management platform with extensive billing, claims, ERA, denial management, and payment capabilities. None of this data appears in the export — a significant gap given that billing records are explicitly part of the HIPAA Designated Record Set.

4. **Patient engagement data absent**: Portal messages, appointment requests, refill requests, kiosk intake data, and consent forms — all patient-facing data the product collects — are not in the export.

5. **Specialty-specific clinical data missing**: The product markets 23 specialty-specific template sets and workflows. C-CDA has no mechanism for custom specialty assessments. Any specialty-specific structured data beyond standard clinical summaries would be lost.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + original-format document files + XLS index, in ZIP
Model type:      Standard projection (C-CDA R2.1 / USCDI v1)
Entities:        0 (no data dictionary; export described at file level only)
Fields:          N/A
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (multi-patient mode described)
Domains covered: 0 of 19 fully; 11 of 19 partially (implicit via C-CDA reference)
```

### Bottom Line

Practice EHR's (b)(10) export is a C-CDA clinical summary with attached document files — the same data available through any Transitions of Care export, presented as "all electronic health information." For a product that stores billing records, claims, payments, insurance data, patient portal communications, specialty-specific assessments, and detailed prescription histories, this export captures a small fraction of patient data. The biggest gap is the complete absence of billing and financial data, which is explicitly defined as part of the HIPAA Designated Record Set and thus falls squarely within the EHI definition.
