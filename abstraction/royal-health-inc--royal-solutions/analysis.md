# EHI Export Analysis: Royal Health, Inc.

**Product**: Royal Solutions v5
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2845.Roya.05.00.1.211229

## 1. Product Context

Royal Health, Inc. is a healthcare technology company specializing in **radiology and diagnostic imaging**. Royal Solutions v5 is a cloud-native Radiology Information System (RIS) marketed under names including RoyalCare™ and Royal Enterprise Care™. It covers the full radiology lifecycle, described by the vendor as "from image ordered to cash in the bank."

The product serves outpatient imaging centers and radiology practices, with modules spanning:

- **Core RIS / Clinical Workflow**: order entry, exam scheduling, patient registration, insurance authorization/verification, mammography tracking, lung screening/tracking, protocol management, report/image distribution
- **Patient Engagement**: self-scheduling, pre-registration, kiosk check-in, patient portal (images/reports/bills), secure messaging
- **Provider Engagement (RoyalMD)**: referral order submission, status tracking, clinical decision support
- **Revenue Cycle Management (RoyalPay/Royal Cash)**: eligibility verification, prior authorization, cost estimation, claims management, billing/collections, payment processing
- **Interoperability**: C-CDA, FHIR API (g)(7)–(g)(10), Direct Mail, encrypted report distribution

The product is certified under ONC criteria including (a)(1)–(a)(5), (a)(12), (a)(14), (b)(1)–(b)(2), (b)(10), (e)(1), (e)(3), (g)(7)–(g)(10), and (h)(1). While radiology-focused, certification requires it to store demographics, problem lists, medications, allergies, clinical notes, family health history, and implantable devices.

**For export completeness assessment**, the key question is: does the export cover not just the standard clinical data fields required by certification, but also the radiology-specific operational data (exams, orders, reports, images), financial/billing data (claims, payments, insurance), and patient engagement data (portal messages, forms) that constitute the product's core value?

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/DocumentationB10FormatExport.pdf` | 10-page PDF data dictionary documenting 12 CSV files with 263 fields. Created 2023-11-09 by Karol Guzman via Microsoft Word. This is the **sole artifact** — the entire (b)(10) export documentation. | **Primary source** — contains the complete data dictionary |

Only one artifact was collected. No sample data files, no JSON/XML schemas, no additional documentation pages were found. The vendor's certifications page (royalsolutionsgroup.com/certifications) links only to Real World Testing PDFs, not additional EHI export documentation.

## 3. Export Mechanics

- **Format**: ZIP archive containing multiple CSV files (comma-delimited) plus nested ZIP files containing patient images/documents
- **Mechanism**: Not explicitly described in the documentation. The document states the export "contains the electronic health information available for the patients' records" but does not describe the UI workflow, API endpoint, or process for triggering the export
- **Single-patient vs bulk**: Not specified. The document implies per-patient exports (images/documents are "for each patient") but does not clarify whether bulk export of multiple patients is supported
- **Access constraints or fees**: Not documented

## 4. Export Content: What's In It

The export is documented as a **ZIP archive of 12 CSV files** plus additional ZIP files for patient images/documents. The data dictionary provides field names and text descriptions for every field (262 of 263 fields have descriptions; only `Insurance_NameTertiary` in Appointments.csv lacks one).

**No data types** are specified for any field — there is no indication of date formats, string lengths, numeric precision, or boolean representations. **No value sets** are formally defined, though some field descriptions mention example values inline (e.g., `ExamResultsStatus`: "Final, Addendum, Dictated, Prelim"; `State` in Transactions: "1=Created; 2=Declined; 3=Approved; 4=Voided; 5=Refunded"). **No sample data** or example files are provided. **No schema for the images/documents sub-ZIPs** is documented.

Standard terminologies are referenced where applicable: RxNorm for medications and allergies, SNOMED for problems/procedures/reactions, CVX for immunizations, UDI identifiers for devices.

Records are linked via `PatientMRN` (present in all CSV files) and `AccessionNumber` (linking Appointments to Transactions and Orders).

### Vendor's own content organization

The vendor does not explicitly organize the CSV files into named categories. The categorization below is based on the content of each file:

| Entity/Table | Fields | Described | Types | Domain |
|---|---|---|---|---|
| Patients.csv | 49 | 49 | No | Demographics, contacts, guarantor, employer, mammography tracking |
| Appointments.csv | 88 | 87 | No | Radiology exams, scheduling, insurance (3 tiers), authorization, CPT codes, BI-RADS |
| Transactions.csv | 18 | 18 | No | Payment transactions, amounts, states, facility |
| Orders.csv | 30 | 30 | No | Referral orders, referring provider, form submissions |
| Demographics2.csv | 14 | 14 | No | Previous names/addresses, granular race/ethnicity, PCP |
| Allergies.csv | 8 | 8 | No | RxNorm-coded allergies, reactions, severity |
| Devices.csv | 12 | 12 | No | Implantable devices, UDI, manufacturing details |
| Immunizations.csv | 8 | 8 | No | CVX-coded vaccines, lot numbers |
| Medications.csv | 8 | 8 | No | RxNorm-coded medications, dosing |
| Problems.csv | 6 | 6 | No | SNOMED-coded problem list |
| Procedures.csv | 7 | 7 | No | SNOMED-coded procedures |
| Vitals.csv | 15 | 15 | No | Vital signs including percentiles |
| **TOTAL** | **263** | **262** | — | — |

**Category breakdown** (by field count):

| Category | CSV Files | Total Fields |
|---|---|---|
| Radiology Operations / Insurance | 1 (Appointments) | 88 |
| Demographics | 2 (Patients, Demographics2) | 63 |
| Clinical | 7 (Allergies, Devices, Immunizations, Medications, Problems, Procedures, Vitals) | 64 |
| Orders / Referrals | 1 (Orders) | 30 |
| Billing / Payments | 1 (Transactions) | 18 |

The **Appointments.csv** is by far the richest entity at 88 fields, serving as a denormalized record combining exam details, scheduling, insurance coverage (primary/secondary/tertiary), authorization details, insured party demographics, CPT codes, and clinical indicators (BI-RADS). This reflects the product's core RIS function.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers five main data areas:

1. **Patient Demographics** (63 fields across 2 files): Comprehensive — includes name, SSN, DOB, contact info, guarantor details, employer, emergency contacts, smoking status, race/ethnicity (including granular codes), language, marital status, previous names/addresses, and mammography/DEXA tracking dates. This is thorough.

2. **Radiology Appointments/Exams** (88 fields): The deepest section, reflecting the product's core function. Covers accession numbers, exam codes, modality types, exam status, BI-RADS codes, referring providers, visit notes, scheduling notes, CPT codes, exam priority, resources/equipment, e-signature/kiosk registration, and three tiers of insurance with authorization details. This captures the operational data of a radiology practice.

3. **Clinical Data** (64 fields across 7 files): Standard USCDI-aligned clinical data — allergies, medications, problems, procedures, immunizations, vital signs, and implantable devices. All use appropriate terminologies (RxNorm, SNOMED, CVX). These are relatively thin (6–15 fields each) but cover the expected domains.

4. **Orders/Referrals** (30 fields): Referral orders with provider info, order source (Hub, Fax, RoyalMD, Print, Migrated, Manual), form submission details, and scheduling source.

5. **Financial Transactions** (18 fields): Payment records with amounts (requested/authorized/captured), payment types, transaction states, and facility linkage. This covers point-of-service collections but not claims lifecycle.

**Images/Documents**: The documentation states the ZIP includes "other zip files that contain the images/documents for each patient" but provides no schema for these sub-archives. Radiology reports and clinical documents may be included here, but their structure and content are undocumented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patients.csv` (49 fields), `Demographics2.csv` (14 fields) — name, SSN, DOB, contacts, guarantor, employer, race/ethnicity, language, marital status, previous names/addresses | Thorough |
| Encounters / visits | ✅ Covered | `Appointments.csv` (88 fields) — each radiology appointment/exam constitutes an encounter, with dates, status, providers, location, notes | Covered via radiology encounters; no separate encounter entity |
| Problems / conditions | ✅ Covered | `Problems.csv` (6 fields) — SNOMED-coded with dates and status | Adequate |
| Medications / prescriptions | ✅ Covered | `Medications.csv` (8 fields) — RxNorm-coded with dates, frequency, route, dose | Adequate for a radiology product (e-prescribing not in scope) |
| Allergies | ✅ Covered | `Allergies.csv` (8 fields) — RxNorm-coded with SNOMED reaction codes, severity | Good |
| Immunizations | ✅ Covered | `Immunizations.csv` (8 fields) — CVX-coded with lot, manufacturer, status | Adequate |
| Vitals | ✅ Covered | `Vitals.csv` (15 fields) — standard vital signs plus percentiles | Good |
| Lab results | N/A | No lab results entity | Product is radiology-focused; lab results are not a core function |
| Imaging / diagnostic reports | ⚠️ Partial | `Appointments.csv` has exam metadata (status, BI-RADS, finalized date) and CPT codes, but **no report text field**. Documents ZIP may contain reports but is undocumented | **Significant gap** — radiology report text is the single most important clinical output of a RIS. Its absence from the documented export is notable. May be in the undocumented images/documents ZIP |
| Procedures | ✅ Covered | `Procedures.csv` (7 fields) — SNOMED-coded with dates and notes | Adequate |
| Clinical notes / documents | ⚠️ Partial | Various note fields in Appointments.csv (`VisitNotes`, `Notes`, `ScheduleNotes`, `RefPhysNotes`, `ReferringPhysicianNotes`). Undocumented documents ZIP may contain additional notes | Notes are embedded as appointment-level fields; no standalone clinical notes entity |
| Care plans / goals | N/A | Not present | Not a core function of a radiology RIS |
| Orders / referrals | ✅ Covered | `Orders.csv` (30 fields) — referral orders with provider info and form details | Good for radiology referral workflow |
| Insurance / coverage | ✅ Covered | `Appointments.csv` includes primary/secondary/tertiary insurance plan, subscriber, group, carrier, payer type, insured demographics. `Patients.csv` has guarantor info | Thorough — three tiers of insurance per appointment |
| Claims / billing | ⚠️ Partial | `Transactions.csv` (18 fields) covers payment transactions. `Appointments.csv` includes CPT codes and `PatientDue`. No dedicated claims entity with line-item charges, adjustments, or denial tracking | Product has full billing/claims module (RoyalPay); export captures payments but not claims lifecycle detail |
| Payments | ✅ Covered | `Transactions.csv` with amounts, payment types, and 5 transaction states (Created/Declined/Approved/Voided/Refunded) | Covers point-of-service and card transactions |
| Consents / directives | ❌ Not covered | No consent or directive entities | Product captures e-signatures at kiosk (documented in `IsESigned`, `ESignedDate` fields) but no consent document export |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal communication entities | Product has secure messaging and patient portal; this is a gap |
| Family health history | ❌ Not covered | No family history entity | Product is certified for (a)(12) family health history; absence from export is a gap |
| Specialty-specific (Radiology) | ⚠️ Partial | Exam metadata well-covered (88 fields). BI-RADS codes present. Mammography/DEXA tracking dates in Patients.csv. But no dedicated mammography tracking, lung screening, or radiology report entities | Core radiology exam workflow is well-covered; specialty tracking modules (mammography recall, lung screening) are not separately exported |

## 6. Documentation Quality

**Strengths:**
- Clean, structured PDF with consistent field-name / description table format
- 262 of 263 fields (99.6%) have substantive descriptions — not just restating field names but explaining business context (e.g., clarifying when fields will be null, how exam codes are derived, what insurance authorization fields represent)
- Standard terminology codes are identified (RxNorm, SNOMED, CVX, UDI)
- Cross-references between entities via PatientMRN and AccessionNumber are evident

**Weaknesses:**
- **No data types** for any field — date formats, string lengths, numeric types are all unspecified
- **No formal value sets** — coded fields mention example values inline but don't provide exhaustive enumerations
- **No sample data** — no example CSV files or records
- **No machine-readable schema** — documentation exists only as a PDF; no JSON schema, CSV header template, or other parseable format
- **Images/documents ZIP structure is completely undocumented** — this is a significant gap since this is where radiology reports and clinical documents likely reside
- **No encoding specification** — character encoding, quoting, line endings are unspecified
- **No export process documentation** — no description of how to initiate, configure, or receive an export

A developer could understand the *structure* of the CSV export from this documentation but would face significant trial-and-error to build a reliable parser, particularly around date formats, null handling, and the images/documents archive.

## 7. Overall Assessment

### Classification

**Partial native export**

This is a genuine (b)(10) export using the vendor's native data model (not a C-CDA or FHIR projection). The 12 CSV files with 263 fields cover demographics, radiology encounters, insurance, payments, orders, and standard clinical data using appropriate terminology codes. However, it has significant coverage gaps: no radiology report text in the documented export, no family health history (despite (a)(12) certification), no patient portal communications, thin claims detail relative to the product's billing capabilities, and an undocumented images/documents archive that may contain critical data (reports, clinical documents) whose structure cannot be assessed.

### Key Findings

1. **Genuine native export, not a FHIR/C-CDA repackaging**: The export uses vendor-specific CSV format with 263 fields across 12 entities, including radiology-specific operational data (BI-RADS codes, modality types, exam protocols) and insurance/billing data that would never appear in a standards-based clinical summary. This is real (b)(10) work.

2. **Radiology report text is absent from documented export**: For a Radiology Information System, the dictated/finalized diagnostic report is the most important clinical output. No field in any CSV file contains report text. The `ExamResultsStatus` and `ExamFinalizedDate` fields confirm reports exist but only capture metadata. Reports may exist in the undocumented images/documents ZIP, but this cannot be verified from the documentation alone.

3. **Insurance coverage is unusually thorough**: The Appointments.csv includes three full tiers of insurance (primary/secondary/tertiary) with subscriber details, group numbers, carrier names, payer types, authorization details, and insured party demographics — 40+ insurance-related fields. This reflects genuine radiology practice data needs.

4. **Family health history is certified but not exported**: The product holds (a)(12) certification for family health history, but no family history entity exists in the export. This is a documented certification-to-export gap.

5. **Single-artifact documentation with no sample data**: The entire (b)(10) documentation is a single 10-page PDF. There are no sample export files, no machine-readable schemas, and no process documentation for how to obtain an export.

### Summary Stats

```
Classification:  Partial native export
Export format:   CSV (comma-delimited) in ZIP, plus nested ZIPs for images/documents
Model type:      Native database
Entities:        12 CSV files
Fields:          263
Descriptions:    99.6% (262 of 263 fields)
Sample data:     No
Bulk export:     Unclear
Domains covered: 10 of 16 applicable domains (✅ covered); 4 partial (⚠️); 2 not covered (❌)
```

### Bottom Line

Royal Solutions provides a genuine native-model (b)(10) export that goes meaningfully beyond FHIR/C-CDA, with strong coverage of demographics, radiology encounters, insurance, and standard clinical data. However, the most critical gap is the apparent absence of radiology report text from the documented export — for a RIS, this is the single most important clinical record. The undocumented images/documents ZIP archive may contain reports and other critical data, but without documentation or sample files, this cannot be confirmed. A patient or provider would get a usable but potentially incomplete copy of their data, with the completeness depending on what the undocumented archive actually contains.
