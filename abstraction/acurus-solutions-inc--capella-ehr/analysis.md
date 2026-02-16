# EHI Export Analysis: Acurus Solutions, Inc.

**Product**: Capella EHR v6.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.2669.ACUR.01.01.1.220131 (CHPL ID 10807)

## 1. Product Context

Capella EHR is an integrated EHR + Practice Management system developed by Acurus Solutions, Inc. (a subsidiary of Akido Labs, Inc.). It is certified as an ambulatory EHR for multi-specialty outpatient practices including Internal Medicine and Family Medicine. Its primary deployment is within Akido Care's own clinical network of 240+ providers across ~100 clinics serving 500,000+ patients in California, Rhode Island, and New York.

Key capabilities relevant to EHI scope:

- **Clinical EHR**: Demographics, problem lists, medication lists, allergies, CPOE, clinical decision support, vitals, lab orders/results, immunizations, procedures, implantable devices, family health history, clinical notes, care plans
- **Practice Management**: Appointment scheduling, revenue cycle management (RCM), HCC coding, claims and referral management
- **E-Prescribing**: Implied by (b)(3) certification and implementation cost listings
- **Patient Engagement**: Patient portal (e)(1), secure messaging (h)(1)
- **Interoperability**: C-CDA document exchange, FHIR R4 API (US Core 3.1.1), Direct messaging
- **Public Health**: Immunization registry, syndromic surveillance, cancer case reporting
- **AI Integration**: ScopeAI clinical co-pilot (in Akido Care deployments) for documentation and diagnosis assistance

The product stores clinical, billing/PM, and patient engagement data. A complete EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `170.315(b)(10)-EHI-export-v3.pdf` (547 KB, 9 pages) | Primary (b)(10) EHI export documentation. Describes CCD-based export with data element mapping tables for 24 CCD sections. Dated September 5, 2023, version 3. | **Most informative** — the core artifact |
| `170.315-g10-API-Documentation.pdf` (346 KB, 10 pages) | FHIR R4 API documentation for §170.315(g)(10). Describes FHIR endpoint at fhir.healthtogo.me with OAuth 2.0 auth, Bulk Data export. Dated November 2024. | Contextual — shows (b)(10) and (g)(10) are separate mechanisms |
| `170.315-g7-g9-API-Documentation.pdf` (333 KB, 8 pages) | API documentation for §170.315(g)(7)/(g)(9). References EMR Direct interopengine documentation. Dated July 2024. | Minimal relevance — mostly Terms of Use |
| `certification-page-screenshot.png` (606 KB) | Screenshot of the acurussolutions.com/Certification.html page | Confirms page layout and link placement |

The (b)(10) PDF is the only artifact directly relevant to the EHI export assessment. No sample data files, no machine-readable schemas, no data dictionaries beyond the CDA mapping tables in the PDF were provided.

## 3. Export Mechanics

- **Format**: C-CDA CCD (Consolidated CDA Release 2.1 DSTU, August 2015) in XML format, also renderable as Adobe PDF
- **Standard**: §170.205(a)(4) HL7 Implementation Guide for CDA Release 2
- **Single-patient export**: UI screen ("Clinical Summary") with checkboxes for individual CCD sections. User selects sections and clicks "Generate CCD." Output in both CCD XML and PDF.
- **Bulk export**: Separate UI allowing selection of multiple patients by provider and/or date of service range. Generates CCD for all selected patients.
- **Export Scheduler**: Supports non-recurring (specific date/time) and recurring exports (configurable start date, time, frequency) with a configurable destination path.
- **Additional**: The document mentions "Ability to download the Images / Clinical notes on demand and can be printed in Adobe PDF format" — but this is described as separate from the CCD export, and no further detail is provided on format, scope, or integration with the bulk export.
- **Access constraints/fees**: Not documented; the export appears to be a built-in UI feature available to clinical users.

## 4. Export Content: What's In It

The export is a C-CDA CCD document. The PDF documentation provides a data element mapping table covering 24 CCD sections with 82 total data elements. For each element, the documentation specifies:

- **Data element name**: Yes (all 82 fields)
- **XPATH / CDA Entry template ID**: Yes for primary entries in most sections (30 of 82 fields have explicit XPATHs or template IDs)
- **Code system OID**: Yes where applicable (27 of 82 fields reference a code system)
- **Code system name**: Yes where applicable (e.g., SNOMED, ICD-10, LOINC, RxNorm, CVX, CPT-4, HCPCS, NDC, NCI Thesaurus, AdministrativeGender, Race & Ethnicity CDC)

There are no field-level descriptions, no cardinality/optionality indicators, no value set bindings (beyond naming the code system), no sample data, and no relationship documentation beyond what is implicit in the CDA structure.

### Vendor's own content organization

The vendor organizes the CCD output into the following sections (from `full-entity-inventory.json`):

| CCD Section | Fields | With Code System | Template ID |
|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | — |
| Provider's name and office contact information | 3 | 0 | — |
| Date and Location of visit | 2 | 0 | 2.16.840.1.113883.10.20.22.2.22.1 |
| Chief Complaint and Reason for visit | 1 | 0 | 2.16.840.1.113883.10.20.22.2.13 |
| Encounters | 5 | 2 | 2.16.840.1.113883.10.20.22.2.22.1 |
| Immunizations | 9 | 3 | 2.16.840.1.113883.10.20.22.2.2.1 |
| Instructions | 1 | 1 | 2.16.840.1.113883.10.20.22.2.45 |
| Treatment Plan | 2 | 1 | 2.16.840.1.113883.10.20.22.2.10 |
| Social History | 3 | 2 | 2.16.840.1.113883.10.20.22.2.17 |
| Problems | 3 | 1 | 2.16.840.1.113883.10.20.22.2.5.1 |
| Medications | 5 | 1 | 2.16.840.1.113883.10.20.22.2.1.1 |
| Medication Allergies | 4 | 4 | 2.16.840.1.113883.10.20.22.2.6.1 |
| Laboratory Tests | 4 | 1 | — |
| Laboratory Information | 5 | 0 | — |
| Laboratory value(s)/result(s) | 5 | 1 | 2.16.840.1.113883.10.20.22.2.3.1 |
| Vitals | 2 | 1 | 2.16.840.1.113883.10.20.22.2.4.1 |
| Goal | 3 | 0 | 2.16.840.1.113883.10.20.22.2.60 |
| Procedures | 2 | 1 | 2.16.840.1.113883.10.20.22.2.7.1 |
| Care team member(s) | 3 | 0 | 2.16.840.1.113883.10.20.22.2.500 |
| Reason for Referral | 1 | 1 | 1.3.6.1.4.1.19376.1.5.3.1.3.1 |
| Medical Equipment (Implanted Devices) | 2 | 1 | 2.16.840.1.113883.10.20.22.2.23 |
| Mental Status | 4 | 1 | 2.16.840.1.113883.10.20.22.2.56 |
| Functional Status | 4 | 1 | 2.16.840.1.113883.10.20.22.2.14 |
| Health Concern | 3 | 1 | 2.16.840.1.113883.10.20.22.2.58 |
| **Totals** | **82** | **27** | |

This is a standard C-CDA CCD section inventory. There are no vendor-specific extensions or custom sections beyond what C-CDA defines.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers standard C-CDA clinical document sections. The 24 sections span:

- **Core clinical data** (strongest coverage): Demographics (6 fields), Problems (3 fields with SNOMED + ICD-10), Medications (5 fields with RxNorm + NDC), Medication Allergies (4 fields), Laboratory results (14 fields across 3 lab sections), Vitals (2 fields), Immunizations (9 fields with CVX + CPT-4)
- **Encounter documentation**: Encounters (5 fields with CPT), Chief Complaint, Date/Location, Provider info
- **Care planning**: Goals (3 fields), Treatment Plan (2 fields), Care Team (3 fields), Instructions, Reason for Referral
- **Assessment data**: Mental Status (4 fields), Functional Status (4 fields), Health Concern (3 fields), Social History (3 fields)
- **Devices**: Medical Equipment / Implanted Devices (2 fields)

The coverage is broad within the clinical domain but shallow — most sections have only 2–5 fields. The entire export is constrained to what C-CDA CCD can represent. There is nothing beyond standard CCD sections.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient Demographics/Information section: name, sex, DOB, race, ethnicity, language (6 fields) | Core demographics present; address, phone, email, emergency contacts not explicitly listed |
| Encounters / visits | ✅ Covered | Encounters section (5 fields), Date and Location of visit (2 fields) | Basic encounter data present |
| Problems / conditions / diagnoses | ✅ Covered | Problems section (3 fields), coded in SNOMED + ICD-10 | Adequate |
| Medications / prescriptions | ✅ Covered | Medications section (5 fields), coded in RxNorm + NDC | Medication list present; pharmacy/fill data absent |
| Allergies | ✅ Covered | Medication Allergies section (4 fields), coded in RxNorm + SNOMED | Adequate |
| Immunizations | ✅ Covered | Immunizations section (9 fields), coded in CVX + CPT-4 | Most detailed section in the export |
| Vitals | ✅ Covered | Vitals section (2 fields), coded in LOINC | Present but thin (only 2 fields) |
| Lab results | ✅ Covered | Three lab sections (14 fields total), coded in LOINC | Well-covered |
| Imaging / diagnostic reports | ⚠️ Partial | Treatment Plan mentions "Diagnostic tests pending"; no dedicated imaging section | No structured imaging results section; unclear if images are in the "on demand" download |
| Procedures | ✅ Covered | Procedures section (2 fields), coded in CPT-4/SNOMED/HCPCS | Present |
| Clinical notes / documents | ⚠️ Partial | Document mentions "Ability to download Images / Clinical notes on demand" separate from CCD; no notes section in CCD mapping | Product stores clinical notes; the CCD export does not have a dedicated notes section. The "on demand" mechanism is undocumented |
| Care plans / goals | ✅ Covered | Goal (3 fields), Treatment Plan (2 fields), Care Team (3 fields), Instructions (1 field) | Present |
| Orders / referrals | ⚠️ Partial | Reason for Referral section (1 field); Treatment Plan mentions "Future scheduled tests" | Referral reasons present; no structured order entries |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entities in CCD export | Product is "EHR + Practice Management" with RCM; insurance data is EHI — **significant gap** |
| Claims / billing | ❌ Not covered | No billing, claims, or charge entities in CCD export | Product has RCM module, HCC coding, claims management; billing records are EHI — **significant gap** |
| Payments | ❌ Not covered | No payment entities in CCD export | Product handles revenue cycle; payment records are EHI — **significant gap** |
| Consents / directives | ❌ Not covered | No consent or advance directive section in CCD export | Not clearly documented as stored by product; may be N/A |
| Patient communications / portal messages | ❌ Not covered | No messaging entities in CCD export | Product is certified for (e)(1) patient portal and (h)(1) Direct messaging; portal messages are EHI — **gap** |
| Family health history | ❌ Not covered | Not present in CCD sections despite (a)(12) certification | Product certified for family health history — **gap** |

## 6. Documentation Quality

The documentation is **minimal but functional for its format**:

**Strengths:**
- Data element mapping with CDA template IDs, XPATHs, and code system OIDs provides enough structure for a developer familiar with C-CDA to understand the output
- Standard code systems are clearly identified (SNOMED, LOINC, RxNorm, CVX, CPT, etc.)
- Screenshots of the export interface clarify the user workflow
- Both single-patient and bulk export are documented with a scheduling capability

**Weaknesses:**
- No field-level descriptions — just field names
- No cardinality or optionality documented (which fields are required vs. optional)
- No value set bindings beyond naming the code system
- No sample data or sample CCD output
- No machine-readable schema beyond the PDF tables
- No documentation of the "Images / Clinical notes on demand" capability beyond one sentence
- No documentation of what data is NOT included or how non-CDA data is handled
- A developer without C-CDA expertise would need to extensively reference the HL7 Implementation Guide

A developer could reconstruct a C-CDA parser from this documentation, but only because C-CDA is a well-known standard. The vendor's documentation adds only the mapping of their sections to CDA templates — it does not provide enough information to understand the full scope of what's exported or how to access data outside the CCD.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is a C-CDA CCD document — a standard clinical summary format designed for transitions of care, not for comprehensive data export. While the vendor has separate (b)(10) and (g)(10) mechanisms (the CCD is not simply the FHIR API repackaged), the CCD format inherently constrains the export to clinical data that fits within C-CDA's section structure. Billing, practice management, patient communications, and other vendor-specific data are absent.

### Key Findings

1. **The export is a C-CDA CCD, covering 24 standard clinical sections with 82 data elements.** This is a legitimate clinical document but not a native data model export. It captures what C-CDA can represent and nothing more. (Source: `170.315(b)(10)-EHI-export-v3.pdf`, pages 4–8)

2. **Billing and practice management data are entirely absent despite the product being an "EHR + PM" system.** Capella EHR has RCM, HCC coding, and claims management capabilities, but the CCD export has no billing, insurance, claims, or payment data. These are part of the HIPAA designated record set. (Source: product-research.md; no billing sections in PDF)

3. **Clinical notes are handled separately and are poorly documented.** The document mentions "Ability to download the Images / Clinical notes on demand" but this is a single sentence with no detail on format, scope, or integration with the bulk export. (Source: `170.315(b)(10)-EHI-export-v3.pdf`, page 2)

4. **The vendor does provide a bulk export with scheduling capability.** The Export Scheduler with recurring/non-recurring modes and configurable destination paths is a meaningful operational feature. (Source: `170.315(b)(10)-EHI-export-v3.pdf`, page 3)

5. **Family health history is missing despite (a)(12) certification.** This is a gap within the clinical domain itself — the product is certified for family health history but it doesn't appear in the CCD section inventory. (Source: comparison of CCD sections vs. certified criteria in metadata.json)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA CCD XML (+ PDF rendering)
Model type:      Standard projection (C-CDA)
Entities:        24 CCD sections
Fields:          82 data elements
Descriptions:    0% (field names only, no descriptions)
Sample data:     No
Bulk export:     Yes (with scheduling)
Domains covered: 9 of 16 applicable domains (with 3 partial)
```

### Bottom Line

Capella EHR's (b)(10) export is a standard C-CDA CCD that covers core clinical data but misses the broader EHI scope. A patient would get a reasonable clinical summary but would not receive their billing records, insurance information, clinical notes (unless obtained through the undocumented "on demand" mechanism), or patient portal communications. The most significant gap is the complete absence of billing and practice management data from a product explicitly marketed as an integrated EHR + PM system.
