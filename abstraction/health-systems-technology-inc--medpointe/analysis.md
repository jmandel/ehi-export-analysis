# EHI Export Analysis: Health Systems Technology, Inc.

**Product**: MedPointe v13
**Analysis date**: 2026-02-16
**CHPL IDs**: 11238 (15.04.04.1597.MedP.13.01.1.230216)

## 1. Product Context

MedPointe is a cloud-based, all-in-one ambulatory EHR and practice management suite developed by Health Systems Technology, Inc. (HST), a small vendor based in Rochester, NY. The product targets small to mid-sized ambulatory practices in family medicine, internal medicine, pediatrics, urgent care, and sleep medicine.

MedPointe is a comprehensive system integrating:

- **Clinical/EHR**: Full clinical documentation with an "Intelligent Text Generation" engine, problem lists, medication lists, allergy lists, drug interaction checking, e-prescribing, lab ordering/results (bidirectional), imaging ordering, referral management, immunization records, preventive care tracking, document management, and picture archiving.
- **Practice Management**: Patient scheduling with automated reminders, demographics management, real-time insurance eligibility verification, analytics and reporting.
- **Billing/RCM**: Integrated medical billing and revenue cycle management — claims generation/submission, ERA/EOB processing, payment posting, denial management, and an integrated clearinghouse.
- **Patient Engagement**: Patient portal with scheduling, messaging, records access, online intake forms, and multi-channel notifications (text, email, voice).
- **Telemedicine**: Built-in virtual visits via ZoomVisit integration.
- **Health Information Exchange**: Direct messaging, C-CDA transitions of care.
- **Public Health Reporting**: Immunization registry and cancer case reporting.

The product holds 37 certified criteria including (b)(10) for EHI export, certified 2023-02-16. This is a full-featured ambulatory EHR storing clinical records, billing/RCM data, scheduling, patient portal communications, scanned documents, lab results, prescriptions, and more. A genuine (b)(10) export should cover all of these domains.

## 2. Artifacts Reviewed

| # | Artifact | Description | Informativeness |
|---|----------|-------------|-----------------|
| 1 | `Providers - Exporting Computer Readable Documents.pdf` (474,907 bytes, 2 pages) | The sole EHI export documentation. Describes how to export clinical documents in a proprietary "C62" format. Contains two screenshots: a right-click context menu showing 9 export options, and an Export Chart dialog with document type checkboxes and output options. Author: Tim Schmidt. Created: 2023-11-16. | **Primary artifact** — but extremely thin. No data dictionary, no schema, no format spec. |
| 2 | `help-documents-page.png` (563,801 bytes) | Screenshot of `hstspot.com/help-documents.php`, the registered EHI documentation URL. Shows three categories of help documents: Exporting Documents (1 PDF), Tutorials (12 MP4 videos), and e-Prescribing (7 PDFs). Page built with Webflow, last published 2020-03-27. | **Contextual** — confirms only one export document exists on the vendor's help site. |

**Verification of help page**: I fetched the live page at `https://hstspot.com/help-documents.php` and confirmed it is still accessible (HTTP 200), still structured identically to the screenshot, and still links to the same single PDF under "Exporting Documents." No additional export documentation has been added since the original collection.

**Verification of PDF**: I extracted text with `pdftotext` and rendered both pages with `pdftoppm`. The text extraction matches the prior report's description. The rendered pages revealed important additional detail in the screenshots that text extraction missed — specifically, a right-click context menu showing 9 export-related options (see Section 3).

## 3. Export Mechanics

**Format**: Proprietary "C62" file format. No public documentation, schema, or specification exists for this format. Web searches for "C62 file format" in healthcare contexts return zero results. The format appears entirely vendor-proprietary.

**Mechanism**: UI-based export from within MedPointe's clinical window, via three methods:

1. **Single Document**: Right-click a document in the patient's TOC → "Export via C62"
2. **Chart Export (multiple documents)**: From patient Overview Page → right-click → Export → Export Chart. Opens a dialog with:
   - Date range selection (From/thru fields)
   - Document type checkboxes: Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents, Include Restricted Documents
   - Output options: Print, Export to Folder, **Export to C62 file**
   - Select Recipient and Queue/Fax Record buttons
3. **Batch Export**: Main Menu → Tools → Clinical → Export. Allows filtering by last name range, date of birth, patient classification, provider, etc.

**Single-patient vs bulk**: Both supported. Single-patient via chart export, multi-patient via batch export.

**Additional export options visible but undocumented**: The PDF's page 1 screenshot shows a right-click Export submenu with 9 options:
- Patient Portal: Update Chart
- Patient Portal: Password Reset
- Export Continuity of Care
- **Export Chart** (the one documented in the PDF)
- Export Continuity of Care - Referral
- Export Continuity of Care - Batch
- Export Immunization Data
- Export Syndromic Data
- Export Medical Records

Only "Export Chart" (the C62 export) is documented. The other 8 options — including "Export Medical Records" and "Export Continuity of Care" — are undocumented. It is unknown whether "Export Medical Records" produces a different, more comprehensive export than "Export Chart."

**Access constraints/fees**: Not documented. The export appears to be a standard UI function accessible to providers.

## 4. Export Content: What's In It

### No data dictionary exists

There is **no data dictionary, no schema, no field definitions, no sample data, and no format specification** for the C62 export or any other export format. The entire EHI export documentation is 2 pages of step-by-step UI instructions for clicking through menus.

### What is known about export content

The only evidence of export content comes from the Export Chart dialog screenshot, which shows 5 document type checkboxes:

| Document Type | Description |
|---|---|
| Cover Sheet | Presumably a patient demographics/summary cover page |
| Notes | Clinical encounter notes |
| Text Documents | Other text-based documents in the chart |
| Scanned/Faxed Documents | Scanned paper documents and faxes |
| Include Restricted Documents | Option to include restricted/sensitive documents |

These are **document categories**, not structured data entities. The export appears to be a document-level export — it exports clinical documents as files in a proprietary format, not the underlying structured data (coded diagnoses, discrete lab values, medication records, billing data, etc.) that lives in the EHR's database.

### What is NOT documented

- No structured clinical data: problems, medications, allergies, immunizations, vitals, lab results
- No billing or financial data: claims, charges, payments, ERA/EOB
- No administrative data: insurance/coverage, demographics fields
- No patient portal data: messages, intake forms
- No relationships between records
- No field names, types, value sets, or constraints
- No explanation of what the C62 format contains or how to parse it

### Vendor's own content organization

The vendor provides no data dictionary or entity-level organization. The only categorization is the 5 document type checkboxes in the export dialog. There are no entities, no tables, no fields to inventory.

| Category (vendor's) | Entities | Fields | Described | Types |
|---|---|---|---|---|
| (none) | 0 | 0 | 0 | N/A |

**Total**: 0 entities, 0 fields documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation covers only **document-level clinical export** — the ability to export clinical documents (notes, cover sheets, text documents, scanned items) in a proprietary format. There is no evidence that structured data, billing data, or any data beyond clinical documents is included.

The documentation does not describe categories, modules, or data domains. It describes a single workflow: select documents, pick a format (C62), click export. The "depth" of coverage cannot be assessed because the C62 format is undocumented — we don't know what fields or data elements are inside the exported files.

The Export submenu screenshot shows 8 additional export options (Export Medical Records, Export Continuity of Care, Export Immunization Data, Export Syndromic Data, etc.) but none are documented. It's possible these provide broader coverage, but there is no way to verify from the available documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ❌ Not covered | No demographics entity/fields in export docs; "Cover Sheet" checkbox may contain some demographic info but this is undocumented | Product stores demographics (Section 1); significant gap |
| Encounters / visits | ⚠️ Partial | "Notes" checkbox suggests encounter notes are exported as documents, but no structured encounter data | Product stores encounter data; gap in structured data |
| Problems / conditions / diagnoses | ❌ Not covered | No structured problem list data documented | Product is certified for (a)(1) problem lists; significant gap |
| Medications / prescriptions | ❌ Not covered | No medication data in export docs; e-prescribing is a major feature | Product has full e-prescribing; significant gap |
| Allergies | ❌ Not covered | No allergy data documented | Product stores allergies; gap |
| Immunizations | ❌ Not covered | "Export Immunization Data" visible in menu but undocumented in EHI export | Product is certified for (f)(1) immunization reporting; gap |
| Vitals | ❌ Not covered | No vitals data documented | Product stores vitals; gap |
| Lab results | ❌ Not covered | No lab data documented | Product has bidirectional lab integration; significant gap |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data documented | Product has imaging ordering; gap |
| Procedures | ❌ Not covered | No procedure data documented | Gap |
| Clinical notes / documents | ⚠️ Partial | "Notes", "Text Documents", "Scanned/Faxed Documents" checkboxes — but in undocumented proprietary format (C62) | Likely covers document content, but format is opaque |
| Care plans / goals | ❌ Not covered | No care plan data; "Treatment Goals" visible in menu but not in export | Product is certified for (a)(12) care plans; gap |
| Orders / referrals | ❌ Not covered | No order/referral data in export | Product manages referrals; gap |
| Insurance / coverage | ❌ Not covered | No insurance data documented | Product does real-time eligibility verification; significant gap |
| Claims / billing | ❌ Not covered | No billing data of any kind | Product has full RCM/billing; **major gap** |
| Payments | ❌ Not covered | No payment data documented | Product posts payments; significant gap |
| Consents / directives | ❌ Not covered | No consent data documented | Gap if product stores these |
| Patient communications / portal messages | ❌ Not covered | No portal messages documented | Product has patient portal with messaging; gap |
| Specialty-specific (sleep medicine) | ❌ Not covered | No specialty data documented | Product targets sleep medicine practices; potential gap |

**Summary**: Of 19 standard EHI domains assessed, **0 are fully covered**, **2 are partially covered** (encounters as document exports, clinical notes as document exports), and **17 are not covered** at all in the documentation. The two "partial" ratings are generous — the exported documents are in an undocumented proprietary format (C62), making even the covered domains effectively inaccessible without vendor tooling.

## 6. Documentation Quality

The export documentation quality is **extremely poor** — among the worst possible while still technically existing:

- **2 pages total**: Entirely UI walkthrough instructions. No technical content.
- **No data dictionary**: Zero entities, zero fields defined. Not even a table-of-contents-level list of what data the export contains.
- **No format specification**: The C62 format is named but never described. A developer receiving a C62 file would have no way to parse it. There is no schema, no structure description, no encoding documentation.
- **No sample data**: No example output files, no sample records, no illustrative content.
- **No machine-readable artifacts**: No JSON schema, no XSD, no CSV template, no FHIR StructureDefinition. Nothing machine-readable.
- **No value sets or code systems**: No documentation of coded values used in the export.
- **No relationship documentation**: No description of how records relate to each other.

**Could a developer build an import from this documentation?** No. A developer would know how to click through the UI to produce a C62 file, but would have no ability to parse, interpret, or import the resulting data. The documentation is a user guide for exporting, not a technical specification for the export format.

**What's well-documented**: The three export methods (single document, chart, batch) and the UI steps to perform them are clearly explained with screenshots.

**What requires guesswork**: Everything else — what data is in the export, how it's structured, what format C62 is, how to read the output, and which data domains are covered.

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess what the export actually covers. The export may produce files, but the proprietary C62 format is completely undocumented, there is no data dictionary, and the documentation consists solely of 2 pages of UI screenshots. The export dialog suggests only clinical document types (notes, cover sheets, scanned documents) — not structured clinical data or billing data. This is a compliance checkbox, not a genuine effort at data portability.

### Key Findings

1. **The entire EHI export documentation is a single 2-page PDF** describing how to click through menus to export clinical documents in a proprietary, undocumented "C62" format. There is no data dictionary, no schema, no format specification, no sample data (`Providers - Exporting Computer Readable Documents.pdf`, 474,907 bytes).

2. **The C62 format is completely undocumented and proprietary.** No public specification, schema, or description exists. A recipient of a C62 file would have no way to interpret or import the data without MedPointe-specific tooling. This fundamentally undermines the purpose of EHI export.

3. **The export appears limited to clinical documents only.** The Export Chart dialog shows only document-type categories (Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents). There is no indication that structured clinical data (problems, meds, labs, vitals), billing/RCM data, or administrative data is included — despite MedPointe being a full-featured ambulatory EHR with integrated billing.

4. **The PDF screenshots reveal 8 additional undocumented export options** in the Export submenu (including "Export Medical Records," "Export Continuity of Care," and "Export Immunization Data"). These could potentially provide broader coverage, but none are documented in the EHI export materials.

5. **Zero entities and zero fields are documented.** This makes MedPointe's EHI export documentation among the thinnest in the certified EHR ecosystem. There is literally nothing for a developer or patient to work with beyond the ability to produce an opaque proprietary file.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C62 (proprietary, undocumented)
Model type:      Unknown — proprietary format, no documentation
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (batch export supported via UI)
Domains covered: 0 of 17 applicable domains (2 partial at best)
```

### Bottom Line

A patient or provider receiving a MedPointe EHI export would get an opaque file in a proprietary "C62" format with no documentation on how to read, parse, or interpret it. The export appears to cover only clinical documents (notes, cover sheets, scanned items), omitting structured clinical data, billing/RCM data, and all other domains that MedPointe stores. This is a compliance checkbox rather than a meaningful data export — the single biggest gap is the complete absence of any format documentation, which renders even the exported data effectively unusable without vendor assistance.
