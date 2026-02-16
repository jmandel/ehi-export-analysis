# EHI Export Analysis: Prime Clinical Systems, Inc.

**Product**: Patient Chart Manager
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.2206.PRIC.01.03.1.220114 (CHPL listing 10791)

## 1. Product Context

Patient Chart Manager is an ambulatory EHR from Prime Clinical Systems, Inc. (founded 1983, Pasadena, CA). It is part of an integrated EHR + practice management platform that also includes billing/scheduling modules (branded historically as "OnSTAFF," "Intellect," and currently "WebSTAFF"). The product targets solo practitioners through mid-sized multi-specialty groups across 14+ specialties (allergy, cardiology, dermatology, family practice, gastroenterology, internal medicine, OB/GYN, ophthalmology, orthopedics, ENT, pediatrics, podiatry, psychiatry, surgery).

**Data the product stores (relevant to EHI scope):**
- **Clinical**: Patient charting (keyboard, stylus, voice, scanned docs), e-prescribing, lab result integration, allergy tracking, care plans, clinical decision support, DICOM-compatible medical imaging, document scanning/faxing
- **Practice management/billing**: Appointment scheduling, patient registration, insurance eligibility verification, medical billing/claims (CMS-1500), claim scrubbing, ICD-10 coding, CPT tracking, payment posting, aging reports, charge posting
- **Interoperability**: C-CDA, HL7, FHIR R4, Direct messaging
- **Public health**: Immunization registry, syndromic surveillance, cancer case reporting
- **Patient portal**: View/download/transmit health information

This is a full-featured ambulatory EHR with integrated practice management. A complete (b)(10) export should cover clinical documentation, prescriptions, labs, allergies, immunizations, vitals, problems, procedures, billing/claims, insurance, and specialty-specific data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `EHI_Export_170.315_b10.pdf` (4.3 MB, 3 pages) | The sole EHI export documentation. Titled "Export Format & Naming Conventions." Describes file structure, naming conventions, and VB6 code for reading exported ADO XML recordsets. Updated 12/23/2025 for PCM Ver. 7.1.1877. | **Primary artifact** — all export information comes from this single document. |
| `EHI_Export_page1.png` (337 KB) | Rendered page 1: General format notes, default export location, XMLDATAExport contents (5 table names visible in screenshot), CDAXMLExport description. | **Most informative** — the embedded Windows Explorer screenshot shows the only concrete list of exported tables. |
| `EHI_Export_page2.png` (387 KB) | Rendered page 2: Chart document naming conventions with color-coded field references, patient data table naming, CDASUMDATA/CDAFULSUM screenshot, CDAXMLDOC screenshot with 3 example files, beginning of Section C (data migration). | **Moderately informative** — reveals additional file structure details and a few field names from database tables. |
| `EHI_Export_page3.png` (197 KB) | Rendered page 3: VB6 code examples for saving/loading ADO XML recordsets, next steps for migration, support contact. | **Least informative** — purely technical boilerplate for reading XML files. |
| Mandatory-Disclosure.pdf (582 KB, obtained via URL in CHPL metadata) | Certification criteria listing, pricing, relied-upon software, and a one-line EHI export reference: "Single patient and patient population EHI is exported in C-CDA R2.1 format." | **Supplementary** — confirms the export exists and links to the same PDF; adds no additional detail. |

**Verification notes:**
- The prior report stated the vendor website was in maintenance mode. As of 2026-02-15, the site responds with HTTP 200 but contains minimal content (a header, footer, and no navigation or product pages). The PDF remains accessible at its registered URL.
- The prior report mentioned a companion document "Including and Excluding Data" — confirmed still unavailable (returns HTML stub page, not a PDF).
- PDF metadata: Created 2026-01-13 by PDFium, 3 pages, 4,300,225 bytes — confirmed.

## 3. Export Mechanics

- **Format**: Two formats in parallel:
  1. **Microsoft ADO XML Recordsets** (VB6 `adPersistXML`) — database table dumps in a proprietary XML serialization format from the Visual Basic 6.0 era
  2. **C-CDA R2.1** — clinical document architecture documents, including chart documents with embedded PDFs
- **Mechanism**: UI-driven export within Patient Chart Manager. The export is controlled by checkboxes; with none selected, only "Patient Data" is exported. The specific UI is not shown in the documentation.
- **Single-patient vs bulk**: Both. The mandatory disclosure states "Single patient and patient population" export. The PDF references "Bulk CCDA Export" as an option.
- **Output location**: Network share at `\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports_#` (session-based directories)
- **Access constraints/fees**: No fees mentioned in documentation. The mandatory disclosure lists no separate charge for (b)(10) export.

## 4. Export Content: What's In It

### What the documentation actually shows

The documentation provides **zero field-level detail**. There is no data dictionary, no schema, no field list, no type definitions, no value sets. The only concrete information about export content comes from:

1. **Five table names** visible in a Windows Explorer screenshot of `XMLDATAExport_#.zip` (PDF page 1)
2. **Six field names** mentioned incidentally in naming convention descriptions (PDF page 2)
3. **One C-CDA summary file** name visible in a screenshot (PDF page 2)

### Export components

The export produces three ZIP files:

**Component 1: XMLDATAExport_#.zip** — Core data tables as ADO XML

| Table Name | Description (from PDF) | Compressed/Full Size |
|---|---|---|
| CHART_DOCS;DataTable.xml | Chart document details for exported date/MR range | 2 KB / 10 KB |
| CHART_STORE;DataTable.xml | Chart storage details for exported date/MR range | 1 KB / 7 KB |
| PATIENT;DataTable.xml | Patient data table details ("all patient data tables included, except those hidden via HIDE option") | 4 KB / 39 KB |
| PT_ALLERGIES;DataTable.xml | Patient allergies | 2 KB / 11 KB |
| PT_COMPLAINTS;DataTable.xml | Patient complaints/problems | 1 KB / 6 KB |

These are the **only data tables visible** in the documentation. The PDF states "All patient data tables included" under PATIENT;DataTable.xml, but provides no enumeration of what those tables are.

**Component 2: CDAXMLExport_#.zip** — C-CDA clinical summaries

- Contains C-CDA files; included only with "Bulk CCDA Export" option
- A `CDASUMDATA.Zip` sub-archive is visible in a page 2 screenshot containing `CDAFULSUM.xml` (6 KB compressed)

**Component 3: CDAXMLDOC.Zip** — Chart documents as embedded PDFs in C-CDA

- Per-patient chart document XML files with embedded PDF content
- File naming encodes: MRN, PCM logon clinic, patient-clinic, patient-account, chart doc ID
- Three example files visible in screenshot: sizes 16 KB, 185 KB, 107 KB

### Field names mentioned (incidentally, in naming conventions)

Only 6 field names appear anywhere in the documentation, all in the context of explaining file naming conventions — not as a data dictionary:

- `pa_clinic`, `pa_account` — from the Patient table
- `cs_mr_num`, `cs_cl_key` — from the chart_store table
- `cdview_cddocid`, `CD_DOC_ID` — from the pt_chart_docs table

### Vendor's own content organization

The vendor provides no content organization, categories, or taxonomy. There is no data dictionary to tabulate. The five table names above constitute the entirety of documented export content.

### What's notably absent from documentation

Given the product's capabilities (Section 1), the following data domains have **zero representation** in the export documentation:

- Medications / prescriptions (product has e-prescribing)
- Lab results (product integrates lab results)
- Immunizations (product reports to immunization registries)
- Vital signs
- Procedures
- Insurance / coverage (product does eligibility verification)
- Billing / claims / charges / payments (product does full billing with CMS-1500)
- Care plans (listed as a product feature)
- Imaging data (DICOM-compatible)
- Clinical notes content (only document metadata tables visible, not note content tables)

### Critical ambiguity

The PDF states "All patient data tables included (except those hidden via HIDE option)" under the PATIENT;DataTable.xml entry. This *could* mean the actual export contains many more tables than the 5 visible in the screenshot — the XML files are self-describing (ADO XML embeds schema), so additional tables might exist in a real export. However, **the documentation provides no evidence of this**. Without a table listing, sample export, or data dictionary, it is impossible to verify what "all patient data tables" actually includes.

The companion document "Including and Excluding Data" — which would clarify the HIDE feature and presumably list available tables — is not publicly available.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categories or organized content structure. The export documentation is purely technical — file naming and directory structure — with no description of data domains or content areas.

The 5 visible table names suggest coverage of:
- **Patient demographics** (PATIENT table — but fields unknown)
- **Allergies** (PT_ALLERGIES table — but fields unknown)
- **Problems/complaints** (PT_COMPLAINTS table — but fields unknown)
- **Chart document metadata** (CHART_DOCS, CHART_STORE — document management, not clinical content)
- **Clinical documents** (via C-CDA export and embedded PDFs — clinical summaries and scanned documents)

The thinnest aspect is that even for these 5 tables, there is zero field-level documentation. The richest content is arguably the C-CDA export, which by standard would include demographics, problems, medications, allergies, and other USCDI data — but the vendor provides no detail about which C-CDA sections are populated.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `PATIENT;DataTable.xml` exists (39 KB uncompressed), but zero fields documented | Table exists; content unknown |
| Encounters / visits | ❌ Not covered | No encounter/visit table in documentation | Product stores visit history; gap |
| Problems / conditions / diagnoses | ⚠️ Partial | `PT_COMPLAINTS;DataTable.xml` exists, but zero fields documented; C-CDA may include problem list | Table exists; content unknown |
| Medications / prescriptions | ❌ Not covered | No medication or prescription table mentioned; C-CDA may include medications section | Product has e-prescribing; significant gap in native export |
| Allergies | ⚠️ Partial | `PT_ALLERGIES;DataTable.xml` exists, but zero fields documented | Table exists; content unknown |
| Immunizations | ❌ Not covered | No immunization table mentioned | Product reports to immunization registries; gap |
| Vitals | ❌ Not covered | No vitals table mentioned | Standard EHR data; gap |
| Lab results | ❌ Not covered | No lab table mentioned | Product integrates lab results; significant gap |
| Imaging / diagnostic reports | ❌ Not covered | No imaging table mentioned | Product is DICOM-compatible; gap |
| Procedures | ❌ Not covered | No procedure table mentioned | Standard EHR data; gap |
| Clinical notes / documents | ⚠️ Partial | `CHART_DOCS` and `CHART_STORE` tables provide document metadata; `CDAXMLDOC.Zip` exports chart documents as embedded PDFs in C-CDA; content/completeness unknown | Document containers exist but clinical note content coverage unclear |
| Care plans / goals | ❌ Not covered | No care plan table mentioned | Product advertises care planning; gap |
| Orders / referrals | ❌ Not covered | No order or referral table mentioned | Standard EHR data; gap |
| Insurance / coverage | ❌ Not covered | No insurance table mentioned | Product does eligibility verification; gap |
| Claims / billing | ❌ Not covered | No billing, claims, or charge table mentioned | Product has full PM with CMS-1500, claims processing, charge posting; **major gap** |
| Payments | ❌ Not covered | No payment table mentioned | Product has payment posting and aging reports; gap |
| Consents / directives | ❌ Not covered | No consent table mentioned | N/A — unclear if product stores this |
| Patient communications / portal messages | ❌ Not covered | No portal or communication table mentioned | Product has patient portal; gap |

**Summary**: Of 17 standard EHI domains applicable to this product, **0 are definitively covered** (we can see tables exist for 3–4 domains, but with zero field documentation, actual coverage cannot be confirmed), **4 have partial evidence** (table name exists but content unknown), and **13 have no evidence at all**.

## 6. Documentation Quality

**Overall quality: Extremely poor.** This is among the thinnest EHI export documentation possible.

- **Data dictionary**: None. Zero field definitions in the entire 3-page document.
- **Schema documentation**: None. The ADO XML format is self-describing (embeds schema in each file), but no external documentation of the schema is provided.
- **Field types**: Not documented.
- **Relationships/foreign keys**: Not documented (6 field names are mentioned incidentally in naming conventions, hinting at cross-table relationships, but no relationship model is provided).
- **Value sets/code systems**: Not documented.
- **Sample data**: None.
- **Machine-readable artifacts**: None (no JSON schema, no XSD, no sample XML).

**Can a developer build an import from this documentation?** No. A developer would need to:
1. Obtain an actual export to discover the schema (embedded in ADO XML files)
2. Reverse-engineer table relationships from field naming patterns
3. Understand ADO XML format (a legacy VB6 technology)
4. Have no documentation for coded values, value sets, or business rules

The VB6 code examples for reading ADO XML are functional but trivial — they show how to open and save files, not how to interpret the data.

The documentation is exclusively focused on **file mechanics** (where files are, what they're named, how to open them) with zero attention to **data semantics** (what the data means, what fields exist, what values are valid).

## 7. Overall Assessment

### Classification

**Minimal/stub**: The documentation is too thin to assess export completeness. The export may contain more data than documented — the claim "all patient data tables included" suggests broader coverage — but the documentation provides no evidence for this. What is documented covers only file structure and naming conventions for 5 named tables with zero field definitions.

### Key Findings

1. **The entire EHI export documentation is 3 pages with zero field-level detail.** The PDF (`EHI_Export_170.315_b10.pdf`, 4.3 MB due to embedded screenshots) describes only file naming conventions and directory structure. There is no data dictionary, no schema documentation, no sample data, and no field definitions.

2. **Only 5 database table names are visible** — CHART_DOCS, CHART_STORE, PATIENT, PT_ALLERGIES, PT_COMPLAINTS — with no documentation of what fields they contain. The claim "all patient data tables included" is unverifiable.

3. **Billing and practice management data are entirely unaddressed.** Despite the product offering full practice management (CMS-1500 claims, charge posting, payment posting, insurance verification, aging reports), zero billing-related tables appear in the export documentation. This is the most significant gap for a combined EHR+PM system.

4. **The export format — Microsoft ADO XML Recordsets — is legitimate but dated.** This is a native database dump format from the VB6 era (~1998), which preserves table structure and is self-describing. It is not a standard-based projection. However, it requires ADO-aware tooling to parse and is unfamiliar to most modern developers.

5. **The mandatory disclosure characterizes the export misleadingly** as "exported in C-CDA R2.1 format," when the actual export also (primarily) consists of ADO XML recordsets. The C-CDA component appears to be supplementary.

### Summary Stats

```
Classification:  Minimal/stub
Export format:   ADO XML Recordsets (VB6) + C-CDA R2.1
Model type:      Native database (ADO XML), supplemented by C-CDA
Entities:        5 named tables visible (actual count unknown)
Fields:          0 documented (6 field names mentioned incidentally)
Descriptions:    N/A (no field documentation exists)
Sample data:     No
Bulk export:     Yes (single-patient and population)
Domains covered: 0 confirmed of 15+ applicable domains (4 have table names but no field detail)
```

### Bottom Line

This export documentation is a bare-minimum compliance artifact. A patient or provider would receive exported files but have no way to understand their contents without reverse-engineering the ADO XML schema. The single biggest gap is the complete absence of documentation — not just for billing (which is a major content gap for a product with full PM capabilities), but for *everything*. Zero fields are defined across the entire export. The phrase "all patient data tables included" is the only assurance of completeness, and it is unverifiable from the provided documentation.
