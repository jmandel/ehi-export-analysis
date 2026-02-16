# EHI Export Analysis: Carbon Health Technologies, Inc.

**Product**: CarbyOs EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.3216.Carb.02.00.0.250129 (v2), 15.04.04.3216.Carb.02.01.1.250925 (v3)

## 1. Product Context

CarbyOs EHR is a cloud-based, proprietary EHR platform built by Carbon Health Technologies, Inc. — a combined healthcare provider and technology company operating ~93 urgent care and primary care clinics. CarbyOs was originally built for internal use and is now also licensed externally, claiming 1,200+ providers and 200+ locations.

The product has four core modules relevant to EHI completeness:

- **Care (EHR)**: AI-powered clinical documentation with ambient charting (GPT-4), SOAP notes, problem lists, medication lists, allergy lists, vitals, lab orders/results, imaging, referral management, care plans, e-prescribing, and ICD-10/CPT coding suggestions.
- **Health (Patient App)**: Scheduling, virtual visits, patient messaging, lab results, prescription tracking, online billing/payment.
- **Operate (Operations)**: Practice analytics and operational insights.
- **Billing (Intelligent RCM)**: Real-time eligibility, claims scrubbing, batch claim correction, payment processing, full claims lifecycle management.

The product stores clinical data, billing/RCM data, patient engagement data (messages, scheduling), and operational data. A genuine (b)(10) export should cover clinical records, billing/claims, patient communications, and insurance data at minimum.

**Bankruptcy context**: Carbon Health filed for Chapter 11 bankruptcy in February 2026 with liabilities exceeding $100 million. Operations reportedly continue.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `certification-disclosures.html` (49,799 bytes) | Certification disclosures page with the EHI Export Functionality section (~157 words of prose). Hosted on Vercel/Nextra. | **Primary (b)(10) source** — but contains no technical detail |
| `carbonhealth-fhir-api-doc-v1_2.pdf` (74 pages, 1.4 MB) | SMART-on-FHIR API documentation for (g)(10). Covers 23 FHIR R4 resources mapped to USCDI v3 with 441 data elements. | **Most informative** — but documents the (g)(10) API, not (b)(10) |
| `sed-testing.pdf` (36 pages, 522 KB) | NISTIR 7742 usability test report for CarbyOs EHR v3, August 2025. | **Not relevant** to EHI export content |
| `certification-disclosures-ehi-section.png` (292 KB) | Screenshot of the EHI Export Functionality section. | Confirms HTML extraction is accurate |
| `certification-disclosures-top.png` (281 KB) | Screenshot of certification info header. | Minor — confirms vendor details |
| `certification-disclosures-full-page.png` (666 KB) | Full-page screenshot for archival. | Minor — confirms no hidden sections |

**No data dictionary, schema, sample export, or field-level documentation exists for the (b)(10) export.** The FHIR API PDF is the only structured technical document, and it explicitly covers (g)(10), not (b)(10).

## 3. Export Mechanics

- **Format(s)**: C-CDA documents for clinical records; PDFs for billing and claims information; original native formats for uploaded documents.
- **Mechanism**: UI-based ("Users can export all EHI for an individual patient at any time without requiring developer assistance"). No API endpoint documented for export.
- **Single-patient**: Yes — explicitly stated.
- **Bulk/population**: Yes — "Users can export all EHI for their entire patient population in bulk."
- **Access constraints**: System administrators manage the ability to perform EHI exports.
- **Fees**: Not mentioned.
- **Exclusions**: Psychotherapy notes (45 CFR 164.501) and information compiled for legal proceedings.

**No instructions, screenshots, or step-by-step guides** are provided for how to actually perform the export.

## 4. Export Content: What's In It

### The (b)(10) documentation problem

The entire (b)(10) EHI export documentation consists of **~157 words of prose** on the certification disclosures page. Verbatim substantive content:

> *"Export formats include C-CDA documents for clinical records, PDFs for billing and claims information, and original native formats for uploaded documents."*

That single sentence is the **complete technical specification** of what the export contains. There is:
- **No data dictionary** — zero tables, fields, types, or relationships documented
- **No C-CDA template specification** — no indication of which CDA document types or sections are used
- **No billing PDF content description** — no indication of what billing data is rendered in PDF
- **No sample exports**
- **No machine-readable schemas**

### The (g)(10) FHIR API (for context only)

The only structured documentation available is the 74-page FHIR API document covering the (g)(10) Standardized API. This documents 23 FHIR R4 resources with 441 data elements mapped to USCDI v3:

| FHIR Resource | Fields | US Core Profile |
|---|---|---|
| Patient | 40 | US Core Patient |
| Allergy Intolerance | 26 | US Core AllergyIntolerance |
| Care Plan | 11 | US Core CarePlan |
| Care Teams | 9 | US Core CareTeam |
| Conditions | 32 | US Core Condition |
| Coverages | 19 | US Core Coverage |
| Implantable Devices | 13 | US Core ImplantableDevice |
| Diagnostic Reports | 21 | US Core DiagnosticReport |
| Document Reference | 20 | US Core DocumentReference |
| Encounter | 22 | US Core Encounter |
| Goal | 8 | US Core Goal |
| Immunization | 15 | US Core Immunization |
| Location | 23 | US Core Location |
| Medical Dispense | 17 | US Core MedicationDispense |
| Medication Request | 20 | US Core MedicationRequest |
| Observation | 25 | US Core Observation |
| Procedure | 13 | US Core Procedure |
| Service Request | 22 | US Core ServiceRequest |
| Organization | 20 | US Core Organization |
| Practitioner | 23 | US Core Practitioner |
| Provenance | 13 | US Core Provenance |
| Related Person | 24 | US Core RelatedPerson |
| Specimen | 5 | US Core Specimen |

These 23 resources map to USCDI v3 data classes and represent the standard clinical exchange surface. **This is the (g)(10) API, not the (b)(10) export**, but it is the only structured data documentation available from this vendor.

### Vendor's own content organization

The vendor organizes (b)(10) content into three format categories with no further detail:

| Category (vendor's) | Format | Fields | Detail Level |
|---|---|---|---|
| Clinical records | C-CDA | Unknown | None — no templates, sections, or fields specified |
| Billing and claims information | PDF | Unknown | None — no content description |
| Uploaded documents | Native formats | N/A | None — passthrough of original files |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) documentation describes three export categories:

1. **"C-CDA documents for clinical records"**: This could range from a minimal CCD (essentially a USCDI summary — the same data available via the (g)(10) FHIR API) to a comprehensive C-CDA with vendor-specific sections. Without template documentation, it's impossible to determine the scope. Given the 23 FHIR resources documented for (g)(10) cover standard USCDI v3 clinical data, the C-CDA likely covers approximately the same clinical domain.

2. **"PDFs for billing and claims information"**: The vendor acknowledges billing data exists and includes it in the export — but in PDF format. This is technically "electronic" but not meaningfully "computable." A developer receiving billing PDFs would need OCR or manual data entry to use the information. This is a notable choice for a product with a full RCM module that stores structured claims, eligibility, and payment data internally.

3. **"Original native formats for uploaded documents"**: Reasonable approach for documents uploaded into the system (scans, images, external PDFs). This is passthrough, not transformation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Claimed via "C-CDA" (likely included); no field detail | C-CDA typically includes demographics, but depth unknown |
| Encounters / visits | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has Encounter resource | C-CDA typically includes encounters, but depth unknown |
| Problems / conditions | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has Condition resource | Likely USCDI-level coverage only |
| Medications / prescriptions | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has MedicationRequest, MedicationDispense | Likely USCDI-level; product has e-prescribing |
| Allergies | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has AllergyIntolerance | Likely USCDI-level |
| Immunizations | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has Immunization | Likely USCDI-level |
| Vitals | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has Observation | Likely USCDI-level |
| Lab results | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has Observation, DiagnosticReport | Likely USCDI-level |
| Imaging / diagnostic reports | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has DiagnosticReport | Likely USCDI-level |
| Procedures | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has Procedure | Likely USCDI-level |
| Clinical notes / documents | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has DocumentReference | AI-generated SOAP notes are a core feature; unclear if full note content is in C-CDA |
| Care plans / goals | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has CarePlan, Goal | Likely USCDI-level |
| Orders / referrals | ⚠️ Partial | Claimed via "C-CDA"; (g)(10) has ServiceRequest | Product has referral management; depth unknown |
| Insurance / coverage | ⚠️ Partial | Possibly in billing PDFs; (g)(10) has Coverage resource | Product has RTE and eligibility; PDF format limits usability |
| Claims / billing | ⚠️ Partial | Claimed via "PDFs for billing and claims" | Product has full RCM module; PDF format is not computable |
| Payments | ❌ Not covered | No evidence of payment data in export | Product processes credit card payments; not mentioned in export |
| Consents / directives | ❌ Not covered | No mention in documentation | Unknown if product stores structured consents |
| Patient communications | ❌ Not covered | No mention of messages, chat, or portal communications | Product has patient messaging and live chat; significant gap |
| Specialty-specific (urgent care) | ❌ Not covered | No mention of triage workflows, check-in data, or urgent care-specific data | Product has one-touch check-in and triage; not in export docs |

**Key finding**: Every clinical domain is marked "⚠️ Partial" rather than "✅ Covered" because the documentation provides zero detail about what's actually in the C-CDA. We know a C-CDA is generated; we don't know what's in it. The billing domain is also partial because while billing data is acknowledged, it's exported as non-computable PDFs.

## 6. Documentation Quality

The (b)(10) export documentation is **among the thinnest possible** while still technically existing:

- **No data dictionary**: A developer cannot determine what data is in the export.
- **No C-CDA template documentation**: No indication of which CDA document types (CCD, Discharge Summary, Continuity of Care Record, etc.) or which sections are included.
- **No sample data**: No way to inspect export output without access to a live system.
- **No machine-readable artifacts**: No schemas, no XSDs, no JSON definitions.
- **No export instructions**: No screenshots or step-by-step procedures.
- **No relationship documentation**: No indication of how C-CDA documents relate to billing PDFs.

The (g)(10) FHIR API documentation (74 pages, 23 resources, 441 fields) is reasonably detailed but covers only the standardized API, not the (b)(10) export. A developer receiving a CarbyOs EHI export would know to expect "some C-CDA files and some PDFs" — and nothing more.

**Could a developer build an import from this documentation?** No. The documentation does not specify what data elements are present, what coding systems are used, how billing data is structured in the PDFs, or how to programmatically process the output.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to assess actual coverage. The vendor *claims* to export "all EHI" including clinical records (C-CDA) and billing/claims (PDF), which would theoretically cover two major domains. However:
- There is no data dictionary to verify what "clinical records" means in C-CDA terms
- Billing data exported as PDF is not meaningfully computable
- Patient communications (messaging, chat), payment records, triage workflows, and AI-generated charting metadata are not mentioned
- The (b)(10) documentation is ~157 words — a compliance statement, not technical documentation

Without a data dictionary, sample exports, or any field-level detail, it is impossible to determine whether this export goes beyond a standard CCD (which would be USCDI-equivalent, i.e., the same as the (g)(10) API in document form).

**Axis 2 — Export approach: Unclear/undetermined**

There are signals in both directions:
- **Possible purpose-built signals**: The vendor explicitly mentions billing/claims PDFs as a separate export format alongside C-CDA, suggesting they built something beyond a generic C-CDA generator. This at least acknowledges billing data as part of EHI.
- **Possible repackaged signals**: C-CDA is the standard clinical exchange format and could easily be the same CCD generated for transitions of care (b)(1). The (g)(10) FHIR API covers the same USCDI v3 data classes. No vendor-specific data dictionary or schema exists, which is a hallmark of repackaged exports.
- **Why unclear**: Without seeing the actual C-CDA templates or billing PDF content, we cannot determine if the C-CDA contains vendor-specific sections beyond a standard CCD, or if the billing PDFs contain structured claim data or just summary statements.

### Key Findings

1. **No data dictionary exists for (b)(10).** The entire export documentation is ~157 words of prose on the certification disclosures page — no tables, fields, types, schemas, or samples. This is the most fundamental gap possible.

2. **Billing data exported as PDF is a computability concern.** The product has a full RCM module with structured claims, eligibility, and payment data. Exporting this as PDF — rather than CSV, JSON, or 837 format — undermines the "electronic and computable" requirement.

3. **The only structured documentation is for (g)(10), not (b)(10).** The 74-page FHIR API document covers 23 FHIR resources mapped to USCDI v3 — the standard clinical exchange floor. No separate (b)(10) technical documentation exists.

4. **Core product differentiators are undocumented in the export.** AI-generated SOAP notes (the product's flagship feature), patient messaging/chat, triage workflows, and payment processing are not mentioned in the export documentation.

5. **Both single-patient and bulk export are claimed.** The documentation does confirm both export modes, which is a positive signal — but without technical detail, the claim cannot be verified.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Unclear/undetermined
Export format:   C-CDA (clinical), PDF (billing), native (uploads)
Entities:        N/A (no data dictionary)
Fields:          N/A (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (claimed)
Domains covered: 0 of 15 confirmed; ~12 claimed via "C-CDA" and "PDF" but unverifiable
```

### Bottom Line

Carbon Health's (b)(10) export documentation is a compliance checkbox: ~157 words of prose asserting the export exists, with zero technical substance. A patient or provider receiving this export would get C-CDA files and billing PDFs with no documentation to interpret them. The single biggest gap is the complete absence of a data dictionary — without it, there is no way to assess whether this export delivers "all EHI" or just a standard clinical summary repackaged with billing PDFs stapled on.
