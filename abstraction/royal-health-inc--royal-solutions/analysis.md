# EHI Export Analysis: Royal Health, Inc.

**Product**: Royal Solutions v5
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2845.Roya.05.00.1.211229 (CHPL #10770)

## 1. Product Context

Royal Solutions v5 is a **cloud-native Radiology Information System (RIS)** built by Royal Health, Inc. for outpatient imaging centers and radiology practices. It is not a general-purpose EHR — it is purpose-built for the radiology lifecycle "from image ordered to cash in the bank."

The product stores and manages data across these key domains:

- **Clinical data**: Demographics, problem lists, medication lists, allergies, immunizations, vitals, implantable devices, clinical notes (certified under ONC criteria (a)(1)–(a)(5), (a)(12), (a)(14))
- **Radiology operations**: Imaging orders/referrals, exam scheduling, patient registration, clinical workflow tracking, radiology reports, DICOM image integration, mammography and lung screening tracking, BI-RADS codes, exam protocols
- **Revenue cycle / billing**: Insurance eligibility, prior authorizations, cost estimates, payment processing, claims management, billing and collections (RoyalPay/Royal Cash modules)
- **Patient engagement**: Self-scheduling, pre-registration, patient portal (reports/images), secure messaging, bill payment
- **Provider engagement**: Referring provider portal (RoyalMD), electronic order submission, order tracking, status updates

For assessing (b)(10) completeness, the export should cover: clinical data, radiology-specific operational data (appointments, orders, reports, imaging workflow), financial/billing data, and patient-facing records. The product does NOT do e-prescribing, lab management, or general inpatient workflows — those are N/A for this assessment.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/DocumentationB10FormatExport.pdf` | 10-page PDF data dictionary documenting 12 CSV files with 263 total fields. Created 2023-11-09 by Karol Guzman using Microsoft Word. | **Primary source** — the sole artifact and most informative |
| `product-research.md` | Prior research on vendor capabilities and product modules | Useful for establishing baseline expectations |
| `ehi-export-report.md` | Prior agent's analysis of the export documentation | Orientation; verified independently |
| `chpl-metadata.json` | CHPL certification details | Confirmed (b)(10) certification and criteria list |
| `files.json` | Manifest of downloaded files | Confirmed single PDF artifact |

Only one artifact was available: the PDF data dictionary. No sample data, no machine-readable schema, no additional documentation was found.

## 3. Export Mechanics

- **Format**: ZIP archive containing multiple CSV (comma-delimited) files plus separate ZIP files containing images/documents per patient
- **Mechanism**: Not specified in the documentation. The PDF describes the format but not how to initiate the export (UI button, API, vendor-assisted, etc.)
- **Single-patient vs bulk**: Not specified. The document describes the export as containing "the electronic health information available for the patients' records" (plural), suggesting it can cover multiple patients
- **Access constraints or fees**: Not documented
- **Character encoding, date formats, quoting conventions**: Not specified

## 4. Export Content: What's In It

The export is documented as a **vendor-specific CSV format** — 12 CSV files in a ZIP archive, plus per-patient ZIP files for images/documents. The data dictionary provides field names and text descriptions for 263 fields across 12 entities. Data types, value set enumerations, cardinality, and constraints are not documented. Standard terminologies are referenced (RxNorm, SNOMED, CVX) but not formally bound.

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patients.csv | 49 | 49 | No | Demographics |
| Demographics2.csv | 14 | 14 | No | Demographics |
| Appointments.csv | 88 | 87 | No | Radiology Operations / Scheduling / Insurance |
| Transactions.csv | 18 | 18 | No | Billing / Payments |
| Orders.csv | 30 | 30 | No | Orders / Referrals |
| Allergies.csv | 8 | 8 | No | Clinical |
| Devices.csv | 12 | 12 | No | Clinical |
| Immunizations.csv | 8 | 8 | No | Clinical |
| Medications.csv | 8 | 8 | No | Clinical |
| Problems.csv | 6 | 6 | No | Clinical |
| Procedures.csv | 7 | 7 | No | Clinical |
| Vitals.csv | 15 | 15 | No | Clinical |
| **TOTAL** | **263** | **262** | — | — |

**Key observations:**

- **Appointments.csv** is by far the largest entity (88 fields, 33% of all fields). It serves as the central hub of the radiology workflow, combining exam scheduling, insurance details for up to three tiers (primary/secondary/tertiary), authorization data, CPT codes, BI-RADS, modality, and clinical status. This is genuinely radiology-specific operational data.
- **Patients.csv** (49 fields) includes standard demographics plus guarantor info, employer data, emergency contacts, and mammography/DEXA tracking dates — domain-specific extensions beyond USCDI.
- **Transactions.csv** (18 fields) covers payment transactions with amounts requested/authorized/captured, payment types, and state codes (Created/Declined/Approved/Voided/Refunded).
- **Clinical CSVs** (Allergies, Devices, Immunizations, Medications, Problems, Procedures, Vitals) use standard terminologies and have 6–15 fields each — adequate for a RIS product.
- **Images/documents ZIP**: Mentioned in the introduction but completely undocumented. No schema, no file naming conventions, no format specifications.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes data into five implicit categories:

1. **Demographics** (2 entities, 63 fields): Comprehensive patient demographics with guarantor, employer, emergency contacts, previous names/addresses, granular race/ethnicity, PCP. This exceeds USCDI demographic requirements.

2. **Radiology Operations / Scheduling / Insurance** (1 entity, 88 fields): The Appointments.csv is the crown jewel — deeply detailed radiology workflow data including accession numbers, exam codes, modality, BI-RADS, exam status, three tiers of insurance with full subscriber demographics, authorization tracking with ICD/CPT codes, e-signature/kiosk data, referring provider details, and various notes fields. This is genuine EHR-specific operational data that would never appear in a USCDI export.

3. **Billing / Payments** (1 entity, 18 fields): Payment transactions with amounts, card authorization data, facility info, and transaction states. This covers time-of-service collections but is relatively thin — no claims line items, no charge amounts per CPT, no adjustments, no denials, no EOBs.

4. **Orders / Referrals** (1 entity, 30 fields): Referral orders with provider details, order source tracking, form submission data, exam details. Covers the inbound referral workflow.

5. **Clinical** (7 entities, 64 fields): Standard USCDI-scope clinical data (allergies, devices, immunizations, medications, problems, procedures, vitals) using standard terminologies. Adequate but not deep.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patients.csv` (49 fields), `Demographics2.csv` (14 fields) — includes guarantor, employer, emergency contacts, race/ethnicity detail | Thorough; exceeds USCDI |
| Encounters / visits | ✅ Covered | `Appointments.csv` (88 fields) — radiology appointments with full workflow status, dates, providers, locations | Comprehensive for radiology encounters |
| Problems / conditions | ✅ Covered | `Problems.csv` (6 fields) — SNOMED-coded with dates and status | Adequate; minimal depth |
| Medications | ✅ Covered | `Medications.csv` (8 fields) — RxNorm-coded with dates, frequency, route, dose | Adequate |
| Allergies | ✅ Covered | `Allergies.csv` (8 fields) — RxNorm-coded with SNOMED reactions, severity | Good |
| Immunizations | ✅ Covered | `Immunizations.csv` (8 fields) — CVX-coded with lot, manufacturer | Adequate |
| Vitals | ✅ Covered | `Vitals.csv` (15 fields) — standard vital signs including BP, HR, temp, SpO2, respiratory rate, BMI/weight/head percentiles | Good |
| Imaging / diagnostic reports | ⚠️ Partial | `Appointments.csv` has exam metadata (ExamResultsStatus, ExamFinalizedDate, BiradCode, ModalityType, ExamCode). Report text not in CSVs. May be in undocumented images/documents ZIP. | **Significant gap if radiology report text is not in the documents ZIP.** For a RIS, the diagnostic report is the core clinical output. |
| Procedures | ✅ Covered | `Procedures.csv` (7 fields) — SNOMED-coded | Adequate |
| Clinical notes / documents | ⚠️ Partial | Various notes fields across entities (VisitNotes, ScheduleNotes, PatientsNotes, RefPhysNotes). Documents referenced as being in per-patient ZIP files, but undocumented. | Unclear how much narrative documentation is captured |
| Orders / referrals | ✅ Covered | `Orders.csv` (30 fields) — referral source, provider, form submissions, scheduling | Good for inbound referral workflow |
| Insurance / coverage | ✅ Covered | `Appointments.csv` has primary/secondary/tertiary insurance plans, subscriber numbers, group numbers, carrier names, payer types, insured demographics, relationships | Comprehensive insurance data — 40+ insurance-related fields |
| Claims / billing | ⚠️ Partial | `Transactions.csv` (18 fields) covers payment transactions. CPT codes in Appointments.csv. No dedicated claims entity with line items, charges, adjustments, denials. | Product has full RCM (RoyalPay); export captures payments but not the full claims lifecycle |
| Payments | ✅ Covered | `Transactions.csv` — amounts requested/authorized/captured, payment types, states | Covers time-of-service payments |
| Implantable devices | ✅ Covered | `Devices.csv` (12 fields) — UDI, device codes, dates, lot/serial numbers | Good |
| Care plans / goals | ❌ Not covered | No care plan or goal entities | N/A — likely minimal in a radiology-focused product |
| Consents / directives | ❌ Not covered | E-signature data exists (IsESigned, ESignedDate) but no consent forms exported | Minor gap; consent forms may be in documents ZIP |
| Patient communications | ❌ Not covered | No secure messaging or portal message entities | Product has patient portal with secure messaging; potential gap |
| Family health history | ❌ Not covered | No family history entity despite (a)(12) certification | Minor gap for radiology context |
| Specialty-specific (radiology) | ✅ Covered | Mammography tracking (LastMammoDate, LastCompletedMammoDate, BiradCode), DEXA tracking, modality types, accession numbers, exam codes, exam resources, BI-RADS | Core radiology workflow data well represented in Appointments.csv |
| Prior authorizations | ✅ Covered | `Appointments.csv` — AuthorizationStatus, AuthorizationICDCode, AuthorizationDiagnosis, AuthorizationRequestDate, AuthorizationCaseNumber, AuthCPTCodes, ReferenceNumbers | Good |

## 6. Documentation Quality

**Strengths:**
- Every field has a text description (262 of 263 fields, 99.6%) that explains the business meaning, not just the field name
- Descriptions are substantive — e.g., explaining when subscriber numbers will be null, how ExamCode is derived, what BI-RADS codes represent
- The document clearly states the export format (ZIP of CSVs + per-patient document ZIPs)
- Standard terminologies identified (RxNorm, SNOMED, CVX)

**Weaknesses:**
- **No data types specified** — no indication whether fields are strings, dates, integers, or booleans; date formats unknown
- **No value sets enumerated** — coded fields mention example values inline (e.g., ExamResultsStatus: "Final, Addendum, Dictated, Prelim") but don't provide exhaustive lists. Only Transactions.State has formal value coding (1–5).
- **No sample data** — no example CSVs or worked records
- **No machine-readable schema** — PDF only; no JSON schema, CSV template, or formal specification
- **Images/documents ZIP completely undocumented** — the introduction mentions per-patient ZIP files for images/documents but provides no schema, naming conventions, or format details
- **No encoding specification** — character encoding, quoting, and line ending conventions not stated
- **No relationship documentation** — PatientMRN and AccessionNumber linkages are implicit but not formally documented as foreign keys
- **No export procedure documented** — how to initiate the export is not described

A developer could understand what data to expect but would need trial-and-error to build a reliable import parser, especially for date parsing, encoding, and the documents archive.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data, scheduling/appointment data with deep radiology-specific detail, insurance information, payment transactions, and referral orders. This goes meaningfully beyond USCDI — the 88-field Appointments.csv with BI-RADS codes, modality types, accession numbers, and three tiers of insurance data is clearly product-specific operational data that would never appear in a (g)(10) FHIR API or C-CDA export.

However, there are notable gaps relative to what the product stores:
- **Radiology report text**: The most significant gap. The product's primary clinical output — dictated/finalized radiology reports — has no dedicated CSV. Report metadata exists (ExamResultsStatus, ExamFinalizedDate) but the actual report content is missing from the documented export. It may be in the undocumented images/documents ZIP, but this is unverified.
- **Claims lifecycle**: The product has full RCM capabilities (RoyalPay/Royal Cash), but the export only captures payment transactions (18 fields), not claims line items, charges, adjustments, or denials.
- **Mammography/lung screening tracking**: Only tracking dates appear in Patients.csv; the dedicated tracking modules' follow-up recommendations, recall status, and screening histories are not exported.
- **Patient portal data**: Secure messages, pre-registration forms, and portal activity are not represented.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export, not a repackaged clinical exchange:
- The format is vendor-specific CSV, not FHIR or C-CDA
- The export includes radiology-specific operational data (accession numbers, modality types, BI-RADS, exam workflow status, resources/equipment) that is absent from any standard clinical exchange format
- Insurance data with three tiers of coverage, authorization tracking, and carrier details goes well beyond USCDI
- Payment transaction data is included
- The data dictionary maps to the vendor's internal data model, not to USCDI profiles

### Key Findings

1. **Genuine purpose-built export with meaningful radiology-specific content.** The 88-field Appointments.csv is the standout — it captures the full radiology workflow including exam scheduling, insurance authorization, BI-RADS codes, modality types, and CPT codes. This is clearly native operational data, not a USCDI repackaging.

2. **Possible gap in radiology report text.** For a RIS, the diagnostic report is the single most important clinical document. No CSV captures report content. It may be in the undocumented per-patient documents ZIP, but the documentation provides no assurance.

3. **Billing coverage is thin relative to product capabilities.** The product advertises full revenue cycle management, but the export's Transactions.csv (18 fields) captures only payment transactions — not claims, charges, adjustments, or collections. The insurance data in Appointments.csv is extensive but appointment-level, not claims-level.

4. **Documentation is functional but incomplete.** Field descriptions are substantive (99.6% coverage), but the absence of data types, formal value sets, sample data, and the completely undocumented images/documents archive limits usability for import implementation.

5. **Small but well-scoped for its domain.** At 12 entities and 263 fields, this is a modest export, but the product is a focused RIS — not a full hospital EHR. The scope is reasonable for the product's footprint, with the caveats above about reports and billing depth.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   CSV (comma-delimited) in ZIP archive
    Entities:        12
    Fields:          263
    Descriptions:    99.6% (262 of 263 fields)
    Sample data:     No
    Bulk export:     Unclear
    Domains covered: 12 of 16 applicable domains (with 3 partial)

### Bottom Line

Royal Solutions v5 has built a genuine (b)(10) export that goes meaningfully beyond USCDI, especially in radiology-specific workflow and insurance data. However, the export has a potentially critical gap: radiology report text — the product's core clinical output — is not present in the documented CSV structure and may only exist in an undocumented images/documents archive. The billing export is also thinner than expected given the product's full RCM capabilities. A patient would get a reasonably complete copy of their demographic, clinical, and scheduling data, but may not get their actual radiology reports in a structured, documented format.
