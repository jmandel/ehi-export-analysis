# EHI Export Analysis: Health Systems Technology, Inc.

**Product**: MedPointe v13
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.1597.MedP.13.01.1.230216 (CHPL #11238)

## 1. Product Context

MedPointe is a cloud-based, all-in-one ambulatory EHR and practice management suite developed by Health Systems Technology, Inc. (HST), a small Rochester, NY company that has been in the medical software business since 1989. The product targets small to mid-sized practices in family medicine, internal medicine, pediatrics, urgent care, and sleep medicine.

MedPointe is a **comprehensive platform** that integrates:
- **Clinical/EHR**: Full clinical documentation with an "Intelligent Text Generation" engine, problem lists, medication lists, allergy lists with drug interaction checking, e-prescribing, bidirectional lab integration, imaging ordering, referral management, immunization records, preventive care tracking, document management, and picture archiving.
- **Practice Management**: Patient scheduling with automated reminders, demographics management, insurance eligibility verification, custom reporting, and analytics.
- **Billing/RCM**: Fully integrated medical billing, claims submission and tracking, integrated clearinghouse, ERA/EOB posting, denial management, and payment collection.
- **Patient Portal**: Messaging, scheduling, intake forms, lab result notifications, and records access.
- **Telemedicine**: Virtual visits via ZoomVisit integration.

The product holds 37 ONC-certified criteria including (b)(10) for EHI export and (g)(10) for FHIR API. Given this breadth, the EHI export should cover clinical records, billing/claims data, medications, labs, demographics, insurance, and patient communications — essentially all data used to make decisions about patients.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|----------|-------------|-----------------|
| `Providers - Exporting Computer Readable Documents.pdf` (475 KB, 2 pages) | The **sole EHI export documentation**. Step-by-step UI instructions for exporting clinical documents using a proprietary "C62" format. Created 2023-11-16 by Tim Schmidt. Contains no data dictionary, no schema, no format specification. | **Primary artifact** — but extremely thin |
| `help-documents-page.png` (564 KB) | Screenshot of the registered EHI documentation URL (hstspot.com/help-documents.php). Shows 3 categories: Exporting Documents (1 PDF), Tutorials (12 MP4 videos), e-Prescribing (7 PDFs). | Confirms the PDF is the only export-related document |

**Verification performed:**
- Confirmed the help documents page is still live (HTTP 200, verified 2026-02-15)
- Confirmed via Apache directory listing at `downloads.hstcentral.com/helpdocs/Exporting Documents/` that only one file exists in the export directory
- Extracted PDF text with `pdftotext -layout` and verified 2 pages, author Tim Schmidt, created 2023-11-16
- Verified PDF metadata title: "Microsoft Word - Exporting Documents via C62"
- The page HTML source shows the content is dynamically generated from PHP but the document list is static — no hidden documents

**No additional artifacts found:** No data dictionary, no schema document, no sample export files, no format specification for C62, and no API documentation were available at any of the vendor's three domains (hstspot.com, hstcentral.com, medpointemr.com).

## 3. Export Mechanics

- **Format**: Proprietary "C62" file format. No specification, schema, or description of what C62 files contain or how they are structured. The format name appears nowhere outside this vendor's documentation. It is not a recognized healthcare standard.
- **Mechanism**: UI-based (right-click menu in MedPointe's Clinical window). Three methods:
  1. **Single Document**: Right-click a document in the patient's Table of Contents → "Export via C62"
  2. **Chart Export**: From patient's Overview Page → right-click → "Export Chart" → select date range and document types → "Export to C62 file"
  3. **Batch Export**: Main Menu → Tools → Clinical → Export → select patient criteria (last name range, DOB, classification, provider), document types, and date range
- **Single-patient vs bulk**: Supports both (single chart export and batch multi-patient export)
- **Access constraints**: Appears to require provider-level access to the MedPointe Clinical window. No mention of patient-initiated export.
- **Fees**: Not mentioned in documentation.

The export dialog offers checkboxes for document types: **Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents, Include Restricted Documents**. These are document categories, not data domains — the export appears to be a document-level export, not a structured data export.

## 4. Export Content: What's In It

### What the documentation tells us

The 2-page PDF describes **how to click the export button** but not **what comes out**. The entirety of the content specification is the list of document type checkboxes in the export dialog:

- Cover Sheet
- Notes
- Text Documents
- Scanned/Faxed Documents
- Include Restricted Documents

There is:
- **No data dictionary** — zero tables, zero fields documented
- **No schema** — no description of C62 file structure
- **No field definitions** — no data types, no value sets, no constraints
- **No sample data** — no example files or records
- **No format specification** — C62 is named but never defined
- **No relationship documentation** — no description of how records relate
- **No mention of structured clinical data** (problems, meds, allergies, labs, vitals) as discrete fields
- **No mention of billing, claims, insurance, or financial data**

### Vendor's own content organization

The vendor does not organize export content into categories beyond the 5 document type checkboxes. There is no entity/table listing to present.

| Document Type Checkbox | Fields Documented | Description Provided | Category |
|---|---|---|---|
| Cover Sheet | 0 | No | Clinical documents |
| Notes | 0 | No | Clinical documents |
| Text Documents | 0 | No | Clinical documents |
| Scanned/Faxed Documents | 0 | No | Clinical documents |
| Include Restricted Documents | 0 | No | Clinical documents |

**Total entities/tables documented: 0**
**Total fields documented: 0**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation covers exactly one thing: exporting clinical documents (notes, cover sheets, text documents, scanned/faxed documents) in a proprietary C62 format. The documentation operates entirely at the document level — it treats the patient chart as a collection of documents to be exported as files, with no indication that the underlying structured data (coded diagnoses, discrete lab values, medication records, etc.) is included in a computable form.

Even within the clinical domain, the coverage is unclear. The document type checkboxes suggest document-oriented output, but without a C62 format specification, it is impossible to determine:
- Whether structured data fields (coded diagnoses, lab values, medication dosages) are preserved
- Whether only rendered document images are exported
- Whether relationships between records are maintained

The vendor provides **zero information** about billing, insurance, scheduling, or any administrative data in the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❌ Not covered | Not mentioned in export docs | Product stores demographics (required for all patient records); significant gap |
| Encounters / visits | ⚠️ Unclear | "Notes" checkbox may include encounter docs, but no structured encounter data documented | Product stores visit records; gap in structured data |
| Problems / conditions / diagnoses | ❌ Not covered | Not mentioned; may be embedded in notes but no discrete data export documented | Product is (a)(1)–(a)(5) certified; significant gap |
| Medications / prescriptions | ❌ Not covered | Not mentioned despite product having e-prescribing (7 help docs dedicated to it) | Product stores full Rx history; significant gap |
| Allergies | ❌ Not covered | Not mentioned | Product stores allergy lists with drug interaction data; significant gap |
| Immunizations | ❌ Not covered | Not mentioned despite (f)(1) immunization registry certification | Product stores immunization records; significant gap |
| Vitals | ❌ Not covered | Not mentioned | Product stores vital signs; gap |
| Lab results | ❌ Not covered | Not mentioned despite bidirectional lab integration | Product stores lab orders and results; significant gap |
| Imaging / diagnostic reports | ❌ Not covered | Not mentioned despite imaging ordering capability | Product stores imaging orders; gap |
| Procedures | ❌ Not covered | Not mentioned | Likely stored given billing integration; gap |
| Clinical notes / documents | ⚠️ Partial | "Notes," "Text Documents," "Cover Sheet" checkboxes exist, but format/content unknown | Best-covered domain, but still no field-level documentation |
| Care plans / goals | ❌ Not covered | Not mentioned despite (a)(12) certification | Product stores care plans; gap |
| Orders / referrals | ❌ Not covered | Not mentioned despite referral management feature | Product stores referral records; gap |
| Insurance / coverage | ❌ Not covered | Not mentioned | Product stores insurance/eligibility data; significant gap |
| Claims / billing | ❌ Not covered | Not mentioned | Product has full RCM with claims, ERA/EOB, denials; **major gap** |
| Payments | ❌ Not covered | Not mentioned | Product stores payment records; significant gap |
| Consents / directives | ❌ Not covered | Not mentioned | May be stored as scanned documents; gap |
| Patient communications / portal messages | ❌ Not covered | Not mentioned | Product has patient portal with messaging; gap |
| Specialty-specific (sleep medicine) | ❌ Not covered | Not mentioned | Product targets sleep medicine practices; gap if specialty data stored |

**Summary**: Of 19 applicable domains, **0 are clearly covered**, **2 are partially/unclear** (encounters and clinical notes may be partially addressed by document export), and **17 are not covered at all**. The export documentation addresses only document-level clinical output and provides no evidence of structured data, billing, or administrative data export.

## 6. Documentation Quality

The documentation quality is among the poorest possible for a (b)(10) certified product:

- **Usability for developers**: A developer could not build an import from this documentation. The C62 format is entirely undescribed — there is no schema, no field list, no data types, no sample output, and no format specification. A third party receiving a C62 export would have no way to interpret the data without MedPointe-specific tools.
- **Usability for patients**: A patient receiving this export could not meaningfully access their data. The proprietary format requires MedPointe software to read.
- **Machine-readable artifacts**: None. No JSON schema, no XSD, no CSV headers, no sample files.
- **Prose documentation**: 2 pages of step-by-step screenshots. The content could fit on a single page — it explains which menus to click, not what data is exported.
- **What's well-documented**: The UI workflow for initiating an export (3 methods: single document, chart, batch).
- **What requires guesswork**: Everything else — what data is exported, in what format, with what structure, covering which domains.

The documentation was created on 2023-11-16, approximately 9 months after the certification date (2023-02-16). The PDF metadata title ("Microsoft Word - Exporting Documents via C62") suggests it was written in Word and printed to PDF. The Webflow-based help page (©2019) predates the documentation.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what is actually exported. The 2-page PDF describes a UI workflow for exporting documents in an undocumented proprietary format (C62), with no data dictionary, no schema, no sample data, and no specification of what data domains are covered. There is zero field-level documentation.

### Key Findings

1. **The entire EHI export documentation is a single 2-page PDF** that explains how to click the export button but provides zero information about what data comes out. There are no tables, no fields, no schema, and no format specification. (Source: `Providers - Exporting Computer Readable Documents.pdf`, 2 pages, 475 KB)

2. **The export uses a proprietary, undocumented "C62" format** that has no public specification, no schema, and no documentation anywhere. A recipient of a C62 export cannot interpret the data without MedPointe software. This fails the basic interoperability premise of (b)(10). (Source: PDF text extraction; web search for "C62 file format" yields no results)

3. **The export appears to cover only clinical documents** (notes, cover sheets, scanned documents), not structured clinical data or any non-clinical data. The export dialog checkboxes — Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents — describe document types, not data domains. There is no mention of demographics, medications, labs, allergies, vitals, billing, claims, insurance, or any structured data. (Source: PDF document type checkboxes)

4. **MedPointe is a comprehensive EHR+PM+billing platform**, making the gap between product capabilities and export documentation especially stark. The product stores clinical records, billing/RCM data, claims, insurance, patient portal messages, prescriptions, lab results, immunizations, and more — yet the export documentation addresses none of these domains. (Source: product-research.md; CHPL metadata showing 37 certified criteria)

5. **No additional documentation exists.** Verified that the help documents page (still live, HTTP 200) lists only this one PDF under "Exporting Documents." The Apache directory listing at the download server confirms only one file. No data dictionary, API documentation, or format specification was found on any of the vendor's three domains. (Source: live verification of hstspot.com, directory listing at downloads.hstcentral.com)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Proprietary "C62" (undocumented)
Model type:      Unknown (no format specification available)
Entities:        0 (no data dictionary)
Fields:          0 (no fields documented)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (batch export by patient criteria)
Domains covered: 0–1 of 19 applicable domains (clinical notes partially, nothing else)
```

### Bottom Line

MedPointe's EHI export documentation is a 2-page instruction sheet for exporting clinical documents in an undocumented proprietary format, with no data dictionary, no schema, and no coverage of structured clinical data, billing, or administrative records. For a product that is a comprehensive EHR, practice management, and billing platform with 37 ONC-certified criteria, this represents one of the most minimal possible compliance efforts. A patient or provider receiving this export would get files in a format only MedPointe can read, covering only a fraction of the data the system stores.
