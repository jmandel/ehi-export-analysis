# EHI Export Analysis: Meridian Medical Management

**Product**: VertexDr v9.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2112.Vert.09.01.1.221024 (CHPL #11002)

## 1. Product Context

VertexDr is a fully integrated EMR and Practice Management (PM) system developed by Meridian Medical Management (now a CareCloud company). It was built from the ground up as a unified clinical and billing platform — the former SSIMED (PM) and EMRge (EMR) products rebranded in 2016. The product targets ambulatory physician practices, particularly large multi-specialty groups and academic faculty practice plans (200–600 providers).

**Key data domains the product stores:**
- **Clinical**: Patient demographics, problem lists, medications, allergies, immunizations, vitals, lab results, clinical notes (customizable templates), e-prescribing (including EPCS), procedures, care plans, referrals, family health history, medical devices, mental/functional status assessments
- **Billing/PM**: Appointment scheduling, claims management, billing records, insurance information, payment processing, revenue cycle data, claims editing
- **Patient engagement**: Patient portal (via MedFusion), secure messaging, SMS reminders
- **Documents**: Progress notes, lab results, radiology reports, scanned/uploaded documents
- **Reporting/Analytics**: Embedded PrecisionBI analytics, clinical quality measures

This is a product with genuine billing/PM capabilities integrated into the same platform as the clinical EHR — a (b)(10) export should cover both clinical and billing domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `VertexDr-b10-EHI-Export-Documentation.pdf` (716 KB, 11 pages) | The sole (b)(10) documentation. Pages 1–5: overview and export instructions with screenshots. Pages 6–10: C-CDA data element mapping table with XPATHs and code system OIDs for ~24 clinical sections. Page 11: one-sentence descriptions of 6 PDF export categories plus a single sentence about FHIR. | **Primary artifact** — contains everything available |
| `VertexDr-Mandatory-Disclosures.pdf` (135 KB, 1 page) | Costs and limitations for MedFusion patient portal and DataMotion secure messaging. Not EHI export-related. | Low |
| `vertexdr-homepage-full.png` (1.2 MB) | Full-page screenshot of vertexdr.com showing the EHI export section. | Low — confirms PDF is the only linked artifact |
| `vertexdr-ehi-section-screenshot.png` (6 KB) | Cropped screenshot of the "Electronic Health Information Export" heading. | Low |

The entire (b)(10) documentation is a single 11-page PDF. No data dictionary, no sample data, no API documentation, no machine-readable schemas.

## 3. Export Mechanics

- **Format**: Dual-format approach:
  - C-CDA XML for structured clinical data (conforming to HL7 CDA R2, Consolidated CDA Templates DSTU R2.1, August 2015)
  - PDF for non-clinical data (demographics/insurance, advance directives, appointments, messages, billing, documents)
  - FHIR mentioned but undocumented
- **Mechanism**: UI-driven export within the VertexDr application
  - Single patient: File → Export CCD from patient chart
  - Bulk patient: File → Export CCD(s) for Patients → generates ZIP of C-CDA XML files
  - PDF exports: via application's 'Reports' section
- **Single-patient vs bulk**: Both supported for C-CDA; PDF exports appear to be per-patient via reports
- **Access constraints/fees**: No specific fees mentioned for (b)(10) export. MedFusion patient portal and DataMotion secure messaging have separate fees (per mandatory disclosures), but these are not directly the EHI export mechanism.

## 4. Export Content: What's In It

### C-CDA Clinical Data (pages 6–10)

The documentation provides a mapping table with 24 C-CDA sections containing 82 data elements total. Each element lists:
- Element name
- XPATH / entry path (provided for 30 of 82 fields, 36.6%)
- Code system OID (provided for 27 of 82 fields, 32.9%)
- Code system name (provided for 27 of 82 fields)

**No fields have prose descriptions** — only field names and technical identifiers. No data types, no cardinality, no value sets, no relationships.

### PDF Export Categories (page 11)

Six categories of non-clinical data are described in single-sentence boilerplate. Each sentence follows the identical template: "This file offers a comprehensive view of [category], structured for clarity and ease of access." No field-level detail is provided for any PDF export.

### FHIR Export (page 11)

A single sentence: "VertexDr FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)." No endpoint URLs, no resource types, no authentication details, no sample payloads.

### Vendor's own content organization

| Entity/Section | Fields | Has Code System | Has XPATH | Format | Source |
|---|---|---|---|---|---|
| Patient Demographics/Information | 6 | 2 | 5 | XML (C-CDA) | C-CDA Export |
| Provider's name and office contact info | 3 | 0 | 3 | XML (C-CDA) | C-CDA Export |
| Date and Location of visit | 2 | 0 | 2 | XML (C-CDA) | C-CDA Export |
| Chief Complaint and Reason for visit | 1 | 0 | 0 | XML (C-CDA) | C-CDA Export |
| Encounters | 5 | 2 | 1 | XML (C-CDA) | C-CDA Export |
| Immunizations | 9 | 3 | 1 | XML (C-CDA) | C-CDA Export |
| Instructions | 1 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Treatment Plan | 2 | 1 | 2 | XML (C-CDA) | C-CDA Export |
| Social History | 3 | 2 | 1 | XML (C-CDA) | C-CDA Export |
| Problems | 3 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Medications | 5 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Medication Allergies | 4 | 4 | 1 | XML (C-CDA) | C-CDA Export |
| Laboratory Tests | 4 | 1 | 0 | XML (C-CDA) | C-CDA Export |
| Laboratory Information | 5 | 0 | 0 | XML (C-CDA) | C-CDA Export |
| Laboratory value(s)/result(s) | 5 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Vitals | 2 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Goal | 3 | 0 | 1 | XML (C-CDA) | C-CDA Export |
| Procedures | 2 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Care team member(s) | 3 | 0 | 1 | XML (C-CDA) | C-CDA Export |
| Reason for Referral | 1 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Medical Equipment | 2 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Mental Status | 4 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Functional Status | 4 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Health Concern | 3 | 1 | 1 | XML (C-CDA) | C-CDA Export |
| Patient Demographic/Insurance | 2 | 0 | 0 | PDF | PDF Export |
| Advance Directive | 1 | 0 | 0 | PDF | PDF Export |
| Appointments | 1 | 0 | 0 | PDF | PDF Export |
| Provider-to-Patient Messages | 1 | 0 | 0 | PDF | PDF Export |
| Billing Data (Claim) | 3 | 0 | 0 | PDF | PDF Export |
| Documents | 4 | 0 | 0 | PDF | PDF Export |
| FHIR Data Export | 0 | — | — | FHIR | Undocumented |

**Summary**: 31 entities, 94 fields total. 82 fields from C-CDA sections; 12 from PDF export categories (category-level only, no true field definitions). Zero fields have prose descriptions. The C-CDA mapping table provides code system OIDs for 27 fields and XPATHs for 30 fields.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three tiers:

1. **C-CDA clinical data** (24 sections, 82 fields): This is the richest part of the documentation. The sections map directly to standard C-CDA template sections — demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, goals, care team, referrals, medical equipment, mental/functional status, health concerns, social history, treatment plan, and instructions. This is exactly what a standard Consolidated CDA document contains — no more, no less.

2. **PDF exports** (6 categories, category-level only): Demographics/insurance, advance directives, appointments, messages, billing (claims with CPT/ICD/modifier), and documents (progress notes, lab results, radiology reports, scanned documents). These are described in boilerplate sentences with zero field-level detail. The billing category is the most notable — it mentions CPT, ICD, and modifier codes but provides no detail on claim structure, amounts, dates of service, payers, or other billing fields.

3. **FHIR export** (1 sentence, undocumented): Mentions FHIR DocumentReference and Bulk Data but provides no technical detail whatsoever.

The C-CDA sections are the standard USCDI/US Core clinical data set. The PDF exports attempt to address non-USCDI domains (billing, appointments, messages) but the PDF format makes this data non-computable, and the documentation provides no field-level detail.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 fields (name, sex, DOB, race, ethnicity, language). PDF: "demographics" (unspecified). | C-CDA covers USCDI demographics. PDF may add address, phone, etc. but no detail provided. Product stores registration data — likely deeper than documented. |
| Encounters / visits | ✅ Covered | C-CDA Encounters section: code, performer, diagnosis, location, date (5 fields) | Standard C-CDA encounter representation. |
| Problems / conditions | ✅ Covered | C-CDA Problems: problem (SNOMED+ICD10), status, active date (3 fields) | Standard C-CDA problem list. |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medications: medication (RxNorm+NDC), directions, start/end date, status (5 fields) | Covers active medication list. Product supports EPCS — detailed e-prescribing transaction history (pharmacy transmissions, controlled substance records) not documented. |
| Allergies | ✅ Covered | C-CDA Medication Allergies: substance, reaction, severity, status (4 fields) | Standard C-CDA allergy representation. |
| Immunizations | ✅ Covered | C-CDA Immunizations: vaccine, date, status, route, site, manufacturer, dose, lot, notes (9 fields) | Reasonably detailed for an immunization record. |
| Vitals | ✅ Covered | C-CDA Vitals: observation (LOINC-coded), date/time (2 fields) | Standard C-CDA vitals. |
| Lab results | ✅ Covered | C-CDA Laboratory sections: tests (4 fields), lab info (5 fields), results (5 fields) — 14 fields total | Three related sections cover orders, lab identification, and results. |
| Imaging / diagnostic reports | ⚠️ Partial | PDF Documents export mentions "radiology reports." No structured imaging data in C-CDA. | Radiology reports exported as PDF documents only — not structured/computable. Product capabilities around imaging are unclear. |
| Procedures | ✅ Covered | C-CDA Procedures: procedure (CPT-4/SNOMED/HCPCS), date (2 fields) | Standard C-CDA procedure list. |
| Clinical notes / documents | ✅ Covered | PDF Documents export: signed progress notes, lab results, radiology reports, scanned documents | Documents exported as PDFs. No structured note content beyond what's in C-CDA. |
| Care plans / goals | ✅ Covered | C-CDA Treatment Plan (2 fields) and Goal (3 fields) | Standard C-CDA care plan/goal sections. |
| Orders / referrals | ⚠️ Partial | C-CDA Reason for Referral: 1 field. Treatment Plan mentions "future appointments, referrals." | Referral reason captured but no order detail (order sets, linked results, order status). |
| Insurance / coverage | ⚠️ Partial | PDF "Patient Demographic/Insurance" — no field detail. | Product stores insurance as part of PM module. PDF export mentioned but zero documentation of what insurance fields are included. |
| Claims / billing | ⚠️ Partial | PDF "Billing Data (Claim)" — mentions CPT, ICD, Modifier. No field-level detail. | Product has full claims management/billing. Export mentions billing but only in PDF format with no field detail. Major gap: no structured billing data, no claim amounts, no payer info, no payment records documented. |
| Payments | ❌ Not covered | No mention of payment data in export documentation. | Product handles revenue cycle and payment processing. No payment data in documented export. |
| Consents / directives | ✅ Covered | PDF "Advance Directive" export. C-CDA Health Concern and Instructions sections. | Advance directives addressed via PDF export. |
| Patient communications | ⚠️ Partial | PDF "Provider-to-Patient Messages" — no field detail. | Product has patient portal messaging and SMS. Messages exported as PDF — no structured content. |
| Specialty-specific data | N/A | No specialty-specific data documented. | Product serves multi-specialty groups but no specialty-specific clinical modules identified beyond standard ambulatory EMR. |

## 6. Documentation Quality

**Overall quality: Poor to minimal.**

- **No data dictionary exists.** The C-CDA mapping table (pages 6–10) is the closest thing — it lists field names, XPATHs, and code system OIDs. But it provides no prose descriptions, no data types, no cardinality, no value set bindings, no examples.
- **PDF export sections are boilerplate.** Six categories described in identical one-sentence templates with zero field-level detail. A developer could not build an import from "a comprehensive view of billing data (CPT, ICD, Modifier)."
- **FHIR export is undocumented.** A single sentence claiming FHIR Bulk Data support with no technical specification — endpoint, authentication, resource types, response format, or sample payloads.
- **No sample data or machine-readable schemas.** The only parseable artifact is the C-CDA mapping table, which itself is embedded in a PDF rather than provided as a machine-readable file.
- **No relationship documentation.** How entities relate to each other is not described.
- **Could a developer build an import?** For the C-CDA clinical data: yes, if they already understand the C-CDA standard (the vendor's table adds little beyond the standard spec). For anything else: no. The PDF exports and FHIR export are essentially black boxes.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The vendor correctly identified that (b)(10) requires more than clinical data alone and added PDF exports for billing, insurance, appointments, messages, and documents. This demonstrates awareness of the broader scope. However:
- The C-CDA portion maps exactly to standard Consolidated CDA sections — this is the USCDI/US Core clinical data set with no product-specific additions.
- The PDF exports for billing and insurance are non-computable and have zero field-level documentation, making their actual coverage unverifiable.
- Payment data, detailed claims structure, insurance coverage details, and e-prescribing transaction history appear to be missing entirely.
- The product has genuine billing/PM capabilities (claims management, revenue cycle, payment processing) that are at best superficially addressed by a PDF "comprehensive view of billing data (CPT, ICD, Modifier)."

**Axis 2 — Export approach: Repackaged existing export with PDF supplements**

The clinical data export is a standard C-CDA — the same format used for (b)(1)–(b)(3) transitions of care. The sections documented are exactly the standard Consolidated CDA sections with no product-specific extensions. The PDF exports represent a minimal effort to address non-clinical domains, but they are not machine-readable, not documented at field level, and appear to be printouts from existing reports rather than a purpose-built EHI export. The FHIR mention appears to be a reference to the existing (g)(10) FHIR API capability rather than a separate (b)(10) mechanism. The overall pattern is: existing C-CDA export + existing report printouts + existing FHIR API reference = "(b)(10)."

### Key Findings

1. **C-CDA clinical export is standard, not product-specific.** The 24 documented C-CDA sections with 82 data elements map directly to the Consolidated CDA standard. No product-specific extensions, custom sections, or data beyond standard C-CDA templates are documented. This is the same clinical data surface as transitions of care.

2. **Billing data is exported as PDF only.** Despite VertexDr being a fully integrated EMR+PM system with claims management and revenue cycle capabilities, billing data is exported as non-computable PDF documents. The documentation provides only "CPT, ICD, Modifier" as the billing data description — no claim amounts, dates of service, payer information, payment records, or claim status.

3. **PDF exports have zero field-level documentation.** All six PDF export categories use identical boilerplate language. A developer cannot determine what fields, structure, or completeness to expect from any PDF export.

4. **FHIR export is an unsubstantiated claim.** A single sentence mentions FHIR Bulk Data support with no technical documentation whatsoever. No FHIR documentation exists anywhere on the vendor's website (confirmed by the collection agent's search of the entire 11-page WordPress site).

5. **No sample data, no schemas, no machine-readable artifacts.** The entire (b)(10) documentation is a single 11-page PDF with no supplementary materials.

### Summary Stats

    Coverage:        Partial
    Approach:        Repackaged existing export (C-CDA + PDF report printouts)
    Export format:   C-CDA XML + PDF + FHIR (claimed, undocumented)
    Entities:        31 (24 C-CDA sections + 6 PDF categories + 1 FHIR stub)
    Fields:          94 (82 C-CDA + 12 PDF category-level; PDF fields are category-level only, not true field definitions)
    Descriptions:    0% of C-CDA fields have descriptions; PDF fields have boilerplate only
    Sample data:     No
    Bulk export:     Yes (C-CDA bulk via ZIP; FHIR bulk claimed but undocumented)
    Domains covered: 10 of 17 applicable domains (most only partially)

### Bottom Line

VertexDr's (b)(10) export is a standard C-CDA clinical summary supplemented by PDF printouts for non-clinical data. The vendor shows awareness that billing and administrative data should be included, but the execution — non-computable PDF format, zero field-level documentation, and an undocumented FHIR claim — falls short of a genuine EHI export. The biggest gap is that a fully integrated EMR+PM system's billing and revenue cycle data is reduced to an undocumented PDF printout, making the structured billing data effectively inaccessible for data portability.
