# EHI Export Analysis: ezEMRx Inc

**Product**: ezEMRx
**Analysis date**: 2026-02-16
**CHPL IDs**: 10779 (Product Number: 15.02.05.2886.EZEM.01.01.1.220105)

## 1. Product Context

ezEMRx is a certified ambulatory EHR with integrated practice management, billing, inventory management, and patient portal, built by a small (~50 employees) Illinois-based vendor. It serves two primary markets: **public health departments** (via exclusive reseller CDP, deployed in 1,000+ locations) and **private ambulatory clinics** across multiple specialties.

Key capabilities relevant to export completeness:

- **Clinical EHR**: Patient charting, clinical documentation, problems, medications, allergies, immunizations, vitals, lab orders/results, e-prescribing, clinical decision support, treatment plans. Specialty templates for immunization clinics, family planning, behavioral health, substance abuse, TB/STD/HIV, case management, and home health.
- **Practice Management**: Scheduling, patient registration, household management.
- **Billing & Revenue Cycle**: Integrated billing with claims scrubbing, electronic claims submission, eligibility verification, sliding fee schedules, multi-payor payment posting, denial tracking, patient statements, merchant services. Optional outsourced RCM service.
- **Inventory Management**: Medication/supply inventory with barcode scanning, vaccine batch tracking and distribution (important for COVID-19 vaccination programs).
- **Patient Portal**: Patient access to health information, appointment reminders.
- **Interoperability**: FHIR APIs, C-CDA exchange, DIRECT messaging, HIE portal.
- **Public Health Reporting**: Immunization registry, syndromic surveillance, cancer case reporting.

The product has broad ONC certification (40+ criteria) including (b)(10) EHI export. This is a full-featured ambulatory EHR — the export should cover clinical data, billing, and the specialty/public-health data the product is known for.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-data-dictionary.pdf` | 9-page PDF, Document Control 01US03P98C001, v2.0 (footer) / v1.0 (cover), dated April 25, 2024. The sole (b)(10) export documentation. Contains file naming conventions, 2 CSV column definition tables, and references to C-CDA R2.1 for clinical/scanned data. Created with Acrobat PDFMaker 20 for Word. 189 KB. | **Primary source** — all export content analysis derives from this document. |
| `downloads/ehi-export-data-dictionary.txt` | Plain text extraction of the PDF via pdftotext. 17 KB. | Used for automated parsing. Table structure is partially garbled without `-layout` flag. |
| `downloads/ehi-export-page-full.png` | Full-page screenshot of the Wix-hosted EHI Export Specifications page at `ezemrx.com/ehi-export`. 821 KB. | Confirms page structure: header with EHI definition, compliance bullet points, a large blank area (PDF Viewer Pro widget where the PDF should render), and a text section promising documentation. |
| `downloads/ehi-export-page-blank-area.png` | Cropped screenshot of the blank PDF Viewer Pro widget area. 90 KB. | Shows the widget area appeared empty during screenshot capture (the PDF requires full browser JS rendering to load via Firebase). |
| `downloads/ehi-export-page-text.txt` | Extracted text from the rendered Wix page. 2 KB. | Contains compliance claims paraphrased from ONC regulation and a promise of documentation. No technical content. |
| `downloads/enrichment/data-dictionary.json` | Prior enrichment extraction of the PDF. 6 KB. | Useful for cross-checking; matched my independent parse except for the column count discrepancy (prior enrichment listed 17 billing columns with corrected sequential numbering, which I verified is correct — 17 distinct column names despite the PDF numbering them 1-16 with a duplicate #3). |
| `downloads/enrichment/extract-data-dictionary.ts` | Enrichment script (Bun/TypeScript). 7 KB. | Hard-coded values from manual reading of the PDF rather than automated parsing. |

## 3. Export Mechanics

- **Format**: Hybrid — HL7 C-CDA R2.1 (XML + HTML) for clinical/demographic data and scanned records; CSV for billing claims and patient notes.
- **Container**: ZIP file(s), one or more per export.
- **File naming**: `PID_INTERNALNUMBERING[_TYPE].EXT` where TYPE is `ClaimData`, `patNotes`, or `Echart` (absent for demographics/clinical C-CDA files).
- **Mechanism**: Self-service from within the ezEMRx application (UI-based). Vendor-assisted export also available.
- **Single-patient**: Yes, explicitly documented.
- **Bulk/population**: Yes, explicitly documented ("one patient, or a full collection of patients").
- **Fees**: No fees for self-service export. Potential fees if vendor performs the export ("based on time and effort").
- **Access constraints**: Requires valid user subscription. System can limit which users perform exports.
- **Support**: support@ezemrx.com for developer-related questions about the export format.

## 4. Export Content: What's In It

The export consists of 4 file categories. Only 2 have field-level documentation (the CSV schemas). The other 2 (C-CDA) defer entirely to the HL7 standard with no vendor-specific documentation.

**Total documented entities**: 4
**Total fields with column definitions**: 24 (17 billing + 7 notes)
**All 24 fields have descriptions**: 100% description coverage (for CSV schemas only)
**C-CDA fields**: 0 documented (vendor provides no field-level docs for C-CDA content)

### Vendor's own content organization

| Entity/Table | Fields | Described | Types Documented | Format | File Type Indicator |
|---|---|---|---|---|---|
| Patient Demographics and Clinical Data | 0 (defers to C-CDA spec) | 0 | No | HL7 C-CDA R2.1 (XML+HTML) | _(none)_ |
| Patient Billing and Claims Data | 17 | 17 | No | CSV | `ClaimData` |
| Adhoc Patient Notes | 7 | 7 | No | CSV | `patNotes` |
| Scanned Records | 0 (defers to C-CDA spec) | 0 | No | HL7 C-CDA R2.1 (XML) | `Echart` |

#### Patient Billing and Claims Data — 17 columns

This is the most detailed section. Each row is a claim line item:

| # | Column Name | Description |
|---|---|---|
| 1 | PID | Patient ID (unique) |
| 2 | DOS | Date of service being billed |
| 3 | Payor | Insurance payor for the date of service |
| 4 | Provider | Rendering provider who performed the service |
| 5 | CPT | CPT code billed |
| 6 | ICD | ICD code associated with the CPT code billed |
| 7 | NDC | NDC code for drugs billed that have been administered or rendered |
| 8 | Modifier | Modifier code associated with the CPT code billed |
| 9 | Charge | Amount billed |
| 10 | Pri Payment | Payment received from primary insurance plan/payor |
| 11 | Sec Payment | Payment received from secondary insurance plan/payor |
| 12 | TerPayment | Payment received from tertiary insurance plan/payor |
| 13 | Oth Payment | Payment received from other sources |
| 14 | Pat Payment | Payment received from the patient |
| 15 | Patient Resp | Patient outstanding balances |
| 16 | Wri-Off/Adj | Balances adjusted or written off |
| 17 | Balance | Patient account balances including pending claims |

**Note**: The PDF's column numbering has an error — both Payor and Provider are listed as column 3, making all subsequent numbers off by one. The table has 17 distinct rows/columns despite numbering only reaching 16.

#### Adhoc Patient Notes — 7 columns

| # | Column Name | Description |
|---|---|---|
| 1 | PID | Patient ID (unique) |
| 2 | Patient Notes ID | Patient note ID (unique) |
| 3 | User Name | User who documented the note |
| 4 | Subject | Subject of the note (may be blank) |
| 5 | Patient Notes Category | Category (user-defined pick list) |
| 6 | Patient Notes Date | Date the note was created |
| 7 | Patient Notes | Documented details of the patient note |

**Note**: Same numbering error — User Name and Subject both listed as column 3.

#### Patient Demographics and Clinical Data — C-CDA R2.1

No field-level documentation. The vendor states only that the files "follow the specification as set for HL7 C-CDA R2.1 specifications" and provides two external links (to HL7 and an NLM article). The C-CDA standard can include sections for demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, encounters, care plans, goals, social history, advance directives, and more — but the vendor does not specify which sections are populated, what coded values are used, or whether any vendor-specific extensions exist.

#### Scanned Records — C-CDA R2.1 with Base64

Also no field-level documentation. Documents are Base64-encoded within a CDA XML wrapper. The vendor notes these files "could be large in size depending on the amount of scanned data."

### Documentation quality issues

- **No data types specified** for CSV columns (no date formats, no numeric precision, no string length constraints, no nullability)
- **No value sets** (what do Payor codes look like? What Patient Notes Categories exist?)
- **No foreign key documentation** beyond shared PID
- **No sample data** or worked examples
- **Version discrepancy**: Cover page says "Version: 1.0" while the footer on all subsequent pages says "v2.0 | April 25, 2024"

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into 4 categories:

1. **Patient Demographics and Clinical Data** (C-CDA): Potentially the broadest category, but entirely opaque. C-CDA R2.1 *can* carry demographics, problems, medications, allergies, immunizations, vitals, labs, procedures, encounters, and more — but without vendor-specific documentation or sample data, we cannot confirm what sections ezEMRx actually populates. The vendor provides zero field-level detail.

2. **Patient Billing and Claims Data** (CSV, 17 columns): The most concrete section. Covers the full claim lifecycle at the line-item level: CPT/ICD/NDC codes, charges, payments from up to 4 payors (primary/secondary/tertiary/other), patient payments, patient responsibility, write-offs/adjustments, and balances. This is genuine billing data that goes beyond USCDI.

3. **Adhoc Patient Notes** (CSV, 7 columns): Telephone calls and ad-hoc notes with category, subject, author, date, and text. A real but narrow slice of the communication/documentation record.

4. **Scanned Records** (C-CDA with Base64): All scanned and uploaded documents. Good coverage of document imaging, though no metadata about document types or categories is documented.

The billing CSV is the strongest signal that this is a genuine (b)(10) effort — billing data at this level of detail would not be available through a (g)(10) FHIR API or standard C-CDA exchange.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA (no field-level docs) | Likely present in C-CDA but completely undocumented. Cannot confirm depth or completeness. |
| Encounters / visits | ⚠️ Partial | C-CDA (no field-level docs); DOS in billing CSV | Date of service in billing implies encounter data. C-CDA may have encounter sections. Undocumented. |
| Problems / conditions | ⚠️ Partial | C-CDA (no field-level docs) | Standard C-CDA section; likely populated but unconfirmed. |
| Medications / prescriptions | ⚠️ Partial | C-CDA (no field-level docs); NDC in billing CSV | NDC codes appear in billing. C-CDA likely has medication list. No MAR detail documented. |
| Allergies | ⚠️ Partial | C-CDA (no field-level docs) | Standard C-CDA section; likely populated but unconfirmed. |
| Immunizations | ⚠️ Partial | C-CDA (no field-level docs) | Standard C-CDA section. Critical for a public-health-focused product. Likely present but undocumented. |
| Vitals | ⚠️ Partial | C-CDA (no field-level docs) | Standard C-CDA section; likely populated but unconfirmed. |
| Lab results | ⚠️ Partial | C-CDA (no field-level docs) | Standard C-CDA section; likely populated but unconfirmed. |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA (no field-level docs) | May be in C-CDA if the product generates diagnostic reports. Unconfirmed. |
| Procedures | ⚠️ Partial | C-CDA (no field-level docs); CPT in billing CSV | CPT codes in billing. C-CDA likely has procedures section. |
| Clinical notes / documents | ✅ Covered | Adhoc Patient Notes CSV (7 fields); Scanned Records (Base64 CDA) | Ad-hoc notes exported with full text. Scanned documents exported as Base64. However, structured clinical notes (progress notes, H&P) are undocumented — may be in C-CDA. |
| Care plans / goals | ⚠️ Partial | C-CDA (no field-level docs) | May be in C-CDA. ezEMRx documents treatment plans as a feature. Unconfirmed. |
| Orders / referrals | ❌ Not covered | No evidence in export | Product likely manages orders (certified for CPOE). No specific export documentation. May be partially in C-CDA. |
| Insurance / coverage | ⚠️ Partial | Payor name in billing CSV | Only the payor name appears. No insurance plan details, subscriber info, eligibility records, coverage dates, or sliding fee schedule data. Product has deep insurance/eligibility features. Significant gap. |
| Claims / billing | ✅ Covered | Billing CSV (17 fields) | Line-item claims with codes, charges, multi-payor payments, adjustments, balances. Good coverage. |
| Payments | ✅ Covered | 5 payment columns + write-offs in billing CSV | Primary, secondary, tertiary, other, and patient payments plus write-offs/adjustments. |
| Consents / directives | ❌ Not covered | No evidence | No consent forms or advance directives mentioned. May be in C-CDA advance directives section. Unconfirmed. |
| Patient communications / portal messages | ⚠️ Partial | Adhoc Patient Notes CSV | Only ad-hoc notes (telephone calls etc.). No portal messages, appointment reminders, or secure messaging. |
| Specialty-specific (behavioral health, substance abuse, family planning, TB/STD/HIV, case management, home health) | ❌ Not covered | No evidence | This is a critical gap. ezEMRx markets specialty templates for behavioral health, substance abuse, family planning, TB/STD/HIV, case management, and home health. None of these specialty-specific data elements are mentioned in the export documentation. Some may be captured in C-CDA but this is speculative. |
| Inventory / vaccine management | N/A | Not in export | Inventory tracking and vaccine batch management are operational data, not part of the designated record set. However, patient-specific vaccine administration records (which doses a patient received) *are* EHI and should be in the immunization section. |

**Domain summary**: Of 17 applicable domains, 3 are clearly covered (billing, payments, clinical notes/documents), 9 are partially covered (likely present in C-CDA but completely undocumented), 3 are not covered (orders/referrals, consents, specialty-specific data), and 2 are ambiguous.

## 6. Documentation Quality

The documentation is a **minimal 9-page PDF** — 4 pages of boilerplate (cover, copyright, table of contents, introduction/executive summary), 3 pages of actual export documentation (pages 6-8), and 1 page of fees/legal/contact (page 9).

**Strengths**:
- Clear file naming convention with component-by-component explanation
- Complete column definitions for both CSV schemas (24 total fields, all with descriptions)
- Explicit about export container format (ZIP), single-patient and population support, and fee structure
- The billing CSV schema is genuinely useful — a developer could parse claim line items from this

**Weaknesses**:
- Zero field-level documentation for C-CDA content (2 of 4 categories). A developer would need to inspect actual export files to understand what clinical data is included.
- No data types for CSV columns (date formats, numeric precision, string encoding)
- No value sets or code system documentation (what Payor values look like, what Note Category options exist)
- No sample data or worked examples
- No relationship documentation beyond shared PID
- No documentation of which C-CDA sections are populated, which is critical for understanding clinical data coverage
- Column numbering errors in both CSV tables (column 3 listed twice)
- Version number discrepancy between cover page (1.0) and footer (v2.0)

**Could a developer build an import?** For billing CSV: yes, with some guesswork on data types and value formats. For clinical data: no — they would need to reverse-engineer the C-CDA output from actual export files. For scanned records: they could extract Base64 documents from CDA XML, but with no metadata about document types or naming.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers billing at genuine depth (17 columns of line-item claim data with multi-payor payments) and includes ad-hoc notes and scanned documents — these go beyond what a USCDI-only export would provide. However, relative to what ezEMRx stores, there are significant gaps:

- **Specialty clinical data** is the biggest gap. ezEMRx's core value proposition for its primary market (public health departments) is specialty-specific templates for behavioral health, substance abuse, family planning, TB/STD/HIV, case management, and home health. None of these appear in the export documentation. The C-CDA might capture some structured data from these templates, but the vendor provides no evidence of this.
- **Insurance detail** beyond the payor name is absent. The product has deep eligibility verification, sliding fee schedules, and multi-payor management, but the export captures only the payor name per claim line.
- **Clinical data completeness is unknowable** from the documentation alone. The C-CDA may be rich or thin — without sample data or section-level documentation, we cannot assess.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged (g)(10) or C-CDA exchange:
- The export is file-based (ZIP of CSV + XML), not API-based
- The billing CSV with 17 columns of claim-level financial data is net-new content that would not exist in a standard C-CDA or FHIR (g)(10) exchange
- The adhoc patient notes CSV is vendor-specific content beyond standard clinical summaries
- The scanned records export (Base64 CDA) packages all patient documents, not just clinical exchange documents
- The documentation does not reference USCDI, US Core, or the FHIR API — it describes a distinct, vendor-specific export format

The vendor built something genuinely new for (b)(10). The question is whether it's complete enough given the product's breadth — and the documentation is too thin to answer that definitively, especially for clinical data.

### Key Findings

1. **Genuine (b)(10) effort with billing data**: The billing CSV with line-item claims, CPT/ICD/NDC codes, multi-payor payments, adjustments, and balances is the strongest signal. This goes meaningfully beyond USCDI and demonstrates the vendor understands (b)(10) requires financial data. (Source: `ehi-export-data-dictionary.pdf`, pages 7)

2. **C-CDA clinical data is a black box**: The vendor provides zero field-level documentation for C-CDA content, which represents 2 of the 4 export categories and likely contains the majority of clinical data. Whether this C-CDA output includes behavioral health assessments, substance abuse treatment records, immunization details, or just standard clinical summary sections is impossible to determine from the documentation alone. (Source: `ehi-export-data-dictionary.pdf`, pages 6, 8)

3. **Specialty data is the biggest likely gap**: ezEMRx's public health specialty templates (behavioral health, substance abuse, family planning, TB/STD/HIV, case management) are its core differentiator, and none appear explicitly in the export documentation. If these are captured only in free-text C-CDA sections, structured specialty-specific data elements may be lost. (Source: `product-research.md`, specialty list; `ehi-export-data-dictionary.pdf`, no mention)

4. **Documentation has quality issues**: Column numbering errors in both CSV tables, version number discrepancy between cover page and footer, and no data types, value sets, or sample data. The 9-page PDF is 55% boilerplate. (Source: `ehi-export-data-dictionary.pdf`, pages 1-5 boilerplate, pages 7-8 numbering errors)

5. **Export mechanics are well-designed**: Self-service single-patient and population export, no fees for self-service, clear file naming convention, pragmatic hybrid format (C-CDA for clinical, CSV for tabular billing data). The format choices are reasonable for the content types. (Source: `ehi-export-data-dictionary.pdf`, pages 6, 9)

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   C-CDA R2.1 (XML+HTML) + CSV (hybrid)
Entities:        4
Fields:          24 (17 billing CSV + 7 notes CSV; 0 for C-CDA entities)
Descriptions:    100% of CSV fields; 0% of C-CDA content
Sample data:     No
Bulk export:     Yes
Domains covered: 3 of 17 clearly; 9 partially (undocumented C-CDA); 3 not covered; 2 N/A
```

### Bottom Line

ezEMRx built a genuine (b)(10) export that includes real billing data alongside clinical C-CDA documents — a meaningful effort from a small vendor. However, the clinical data half is a documentation black box (the C-CDA content is completely undocumented), and the product's core specialty-specific capabilities (behavioral health, substance abuse, family planning, public health program templates) are not visibly represented in the export. A patient would get their billing records in clear detail and their clinical records in some form, but whether the specialty-specific assessments and treatment data that make ezEMRx distinctive are captured is impossible to determine from the documentation alone.
