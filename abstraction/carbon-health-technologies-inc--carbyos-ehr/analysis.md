# EHI Export Analysis: Carbon Health Technologies, Inc.

**Product**: CarbyOs EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 11590 (version 2, certified 2025-01-29), 11700 (version 3, certified 2025-09-25)

## 1. Product Context

CarbyOs EHR is a cloud-based, proprietary EHR platform built by Carbon Health Technologies, Inc. Originally developed for Carbon Health's own urgent care and primary care clinics (~93 locations), the product was later licensed to external healthcare organizations, reportedly serving 1,200+ providers across 200+ locations. In February 2026, Carbon Health filed for Chapter 11 bankruptcy.

CarbyOs is marketed as an "AI-powered operating system for care delivery" with four core modules:

1. **Care (EHR)**: Clinical documentation with AI-powered ambient charting (GPT-4), template-based charting, e-prescribing, lab ordering, imaging, referral management, care plans, clinical decision support, automated ICD-10/CPT coding suggestions.
2. **Health (Patient App)**: Scheduling, video visits, patient messaging, treatment plan and records viewing, lab results, prescription tracking, billing/payment, digital vaccine card.
3. **Operate (Operations)**: Analytics and operational insights (minimal public documentation).
4. **Billing (Intelligent RCM)**: Real-time eligibility verification, patient responsibility calculation, payment processing, coding suggestions, claims scrubbing, batch claim correction, full claims lifecycle management.

**Data domains the product stores**: Demographics, clinical notes (including AI-generated SOAP notes), problem lists, medication lists, allergies, vitals, lab results, imaging references, care plans, e-prescriptions, referrals, insurance/eligibility, claims, payments, patient messages, appointment records, immunizations, and operational analytics.

**What should a complete EHI export cover**: At minimum, all clinical documentation (notes, problems, meds, allergies, labs, vitals, procedures, immunizations, care plans), billing records (claims, charges, payments, insurance), patient communications, and any uploaded documents or images. The billing module is deeply integrated, so its data is clearly EHI.

## 2. Artifacts Reviewed

| Artifact | Description | Size | Informativeness |
|---|---|---|---|
| `certification-disclosures.html` | Certification disclosures page containing the complete EHI export documentation (~192 words of prose), plus MFA, FHIR API, and SED sections | 49,799 bytes | **Primary source** — the only EHI export documentation that exists |
| `carbonhealth-fhir-api-doc-v1_2.pdf` | 74-page SMART-on-FHIR API documentation for §170.315(g)(10). Documents 23 FHIR R4 resources mapped to US Core 6.1.0 / USCDI v3, with ~403 data elements. | 1.4 MB, 74 pages | **Supplementary** — covers (g)(10) API, not (b)(10) EHI export; provides the only reference for what clinical data elements the system can expose |
| `sed-testing.pdf` | NISTIR 7742 Safety Enhanced Design usability test report for CarbyOs EHR v3, dated August 2025 | 522 KB, 36 pages | **Not relevant** — usability testing; zero mentions of EHI export |
| `certification-disclosures-ehi-section.png` | Screenshot of the EHI Export Functionality section | 292 KB | Archival; confirms HTML text content |
| `certification-disclosures-full-page.png` | Full-page screenshot of certification disclosures | 666 KB | Archival |
| `certification-disclosures-top.png` | Screenshot of page header with vendor details | 281 KB | Archival; confirms vendor info |

**No data dictionary, schema, sample export, or import instructions exist.** The EHI export documentation consists entirely of 192 words of general prose on the certification disclosures page.

## 3. Export Mechanics

- **Format(s)**: C-CDA documents (clinical records), PDFs (billing and claims), original native formats (uploaded documents)
- **Mechanism**: UI-driven; "users can export all EHI for an individual patient at any time without requiring developer assistance." No technical details on the actual UI workflow or export process are provided.
- **Single-patient**: Supported (per documentation)
- **Bulk export**: Supported for "entire patient population" (per documentation); no technical details on format (e.g., ZIP of individual C-CDAs? single archive? API endpoint?)
- **Access constraints**: "System administrators manage the ability to perform EHI exports to maintain data security"
- **Fees**: Not mentioned
- **Exclusions**: Psychotherapy notes (per 45 CFR 164.501) and information compiled for legal proceedings

## 4. Export Content: What's In It

### What the documentation tells us

The EHI export documentation provides **zero field-level detail**. The entire content specification is:

> "Export formats include C-CDA documents for clinical records, PDFs for billing and claims information, and original native formats for uploaded documents."

There is:
- **No data dictionary** — no listing of tables, fields, data types, or relationships
- **No C-CDA template specification** — no indication of which C-CDA document types (CCD, Discharge Summary, Progress Note, etc.) or which sections/templates are included
- **No billing data specification** — no detail on what billing/claims information appears in the PDFs
- **No schema documentation** — no XSD, JSON schema, or any machine-readable format definition
- **No sample exports** — no example files showing actual output
- **No export instructions** — no screenshots, no step-by-step guide

### FHIR API reference (g)(10) — not (b)(10)

The only structured data documentation available is the 74-page FHIR API document for §170.315(g)(10). This covers 23 FHIR R4 resources with ~403 data elements mapped to US Core 6.1.0 profiles. These resources represent the USCDI v3 clinical data subset:

| FHIR Resource | Data Elements | US Core Profile |
|---|---|---|
| Patient | 37 | US Core Patient |
| Conditions | 30 | US Core Condition |
| Allergy Intolerance | 24 | US Core AllergyIntolerance |
| Observation | 23 | US Core Observation |
| Related Person | 22 | US Core RelatedPerson |
| Location | 21 | US Core Location |
| Practitioner | 21 | US Core Practitioner |
| Encounter | 20 | US Core Encounter |
| Service Request | 20 | US Core ServiceRequest |
| Diagnostic Reports | 19 | US Core DiagnosticReport |
| Document Reference | 18 | US Core DocumentReference |
| Organization | 18 | US Core Organization |
| Medication Request | 18 | US Core MedicationRequest |
| Coverages | 17 | US Core Coverage |
| Medical Dispense | 16 | US Core MedicationDispense |
| Immunization | 14 | US Core Immunization |
| Implantable Devices | 12 | US Core Implantable Device |
| Provenance | 12 | US Core Provenance |
| Procedure | 12 | US Core Procedure |
| Care Plan | 10 | US Core CarePlan |
| Care Teams | 8 | US Core CareTeam |
| Goal | 7 | US Core Goal |
| Specimen | 4 | US Core Specimen |

This FHIR API covers standard USCDI v3 clinical data classes only. It does **not** cover billing, claims, payments, patient messages, AI-generated charting metadata, or any vendor-specific data. If the (b)(10) C-CDA export draws from the same data source as the (g)(10) API, then the clinical portion of the export is limited to a USCDI summary — not the full clinical record.

### Vendor's own content organization

The vendor does not organize the EHI export into categories, tables, or entities. The only categorization provided is:

| Category (vendor's) | Format | Detail Provided | Entities | Fields |
|---|---|---|---|---|
| Clinical records | C-CDA | None — no templates, sections, or fields specified | 0 | 0 |
| Billing and claims information | PDF | None — no specification of what billing data is included | 0 | 0 |
| Uploaded documents | Original native formats | None — no detail on document types | 0 | 0 |

**Total entities documented for (b)(10) export: 0. Total fields documented: 0.**

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation makes three high-level claims:

1. **Clinical records via C-CDA**: This could range from a minimal CCD (essentially USCDI summary data — demographics, problems, meds, allergies, vitals, immunizations) to a comprehensive multi-document export with full clinical notes, lab results with panels, imaging reports, and referral packages. **Without C-CDA template documentation, the actual scope is unknowable.** The FHIR API documentation suggests the system stores USCDI v3 data classes, but whether the C-CDA export includes more or less than the FHIR API exposes is not documented.

2. **Billing/claims via PDF**: The vendor acknowledges billing data exists and exports it, but in PDF format. PDFs are not computable — a downstream system receiving billing PDFs would need OCR or manual data entry to use the information. This is a significant weakness for (b)(10) compliance, which requires data in an "electronic and computable" format. Furthermore, no detail is provided on what billing data the PDFs contain (claims, payments, eligibility, all of these?).

3. **Uploaded documents in native formats**: This is a reasonable approach for documents uploaded to the patient record (e.g., scanned forms, external reports). No detail on what types of documents are included.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implied via "C-CDA documents for clinical records"; FHIR API documents Patient resource (37 elements) | C-CDA typically includes demographics, but no confirmation of scope |
| Encounters / visits | ⚠️ Partial | Implied via C-CDA; FHIR API documents Encounter resource (20 elements) | No detail on what encounter data is in the C-CDA |
| Problems / conditions / diagnoses | ⚠️ Partial | Implied via C-CDA; FHIR API documents Condition resource (30 elements) | Standard C-CDA section; likely present but unconfirmed |
| Medications / prescriptions | ⚠️ Partial | Implied via C-CDA; FHIR API documents MedicationRequest (18) and MedicationDispense (16) | Product has e-prescribing; C-CDA likely includes medication list but scope unknown |
| Allergies | ⚠️ Partial | Implied via C-CDA; FHIR API documents AllergyIntolerance (24 elements) | Standard C-CDA section; likely present but unconfirmed |
| Immunizations | ⚠️ Partial | Implied via C-CDA; FHIR API documents Immunization (14 elements); product certified for (h)(1) immunization registry | Likely present in C-CDA but unconfirmed |
| Vitals | ⚠️ Partial | Implied via C-CDA; FHIR API documents Observation resource | Standard C-CDA section; likely present but unconfirmed |
| Lab results | ⚠️ Partial | Implied via C-CDA; FHIR API documents DiagnosticReport (19 elements) and Observation | Product has lab ordering; likely in C-CDA but scope unknown |
| Imaging / diagnostic reports | ⚠️ Partial | Implied via C-CDA; FHIR API documents DiagnosticReport | Product has imaging ordering; unclear if imaging data is in C-CDA |
| Procedures | ⚠️ Partial | Implied via C-CDA; FHIR API documents Procedure (12 elements) | Likely present but unconfirmed |
| Clinical notes / documents | ⚠️ Partial | Implied via C-CDA; FHIR API documents DocumentReference (18 elements) | Product's flagship feature is AI-generated SOAP notes; unclear if full note text is in C-CDA or only structured summaries |
| Care plans / goals | ⚠️ Partial | Implied via C-CDA; FHIR API documents CarePlan (10) and Goal (7) | Likely present but unconfirmed |
| Orders / referrals | ⚠️ Partial | Implied via C-CDA; FHIR API documents ServiceRequest (20 elements) | Product has referral management; unclear if referral data is exported |
| Insurance / coverage | ⚠️ Partial | Possibly in billing PDFs; FHIR API documents Coverage (17 elements) | Product has real-time eligibility verification; billing PDFs may include some coverage info |
| Claims / billing | ⚠️ Partial | Vendor says "PDFs for billing and claims information" | Product has deep RCM module (claims, scrubbing, coding); PDF format is not computable; no detail on content |
| Payments | ⚠️ Partial | Possibly in billing PDFs | Product processes credit card payments; unclear if payment records are in PDFs |
| Consents / directives | ❌ Not covered | No evidence | Not mentioned; unclear if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No evidence | Product has patient messaging (live chat, video visits); these are not mentioned in export |
| Specialty-specific (urgent care / primary care) | ❌ Not covered | No evidence | Product's AI charting generates urgent care-specific SOAP notes, triage workflows, check-in data; none specifically mentioned |

**Summary**: Every clinical domain is rated "⚠️ Partial" because the vendor claims C-CDA covers "clinical records" but provides zero detail on which C-CDA sections, templates, or data elements are included. Without this detail, we can only infer likely coverage from standard C-CDA conventions. Billing is also "⚠️ Partial" because it's acknowledged but exported as non-computable PDFs with no content specification. Patient communications and specialty data have no evidence of coverage.

## 6. Documentation Quality

**Extremely poor.** The EHI export documentation consists of 192 words of marketing-quality prose that could apply to virtually any EHR claiming (b)(10) compliance. It provides:

- **No technical specification** of any kind
- **No data dictionary** — zero entities, zero fields documented
- **No C-CDA template or section listing** — impossible to know what clinical data is exported
- **No billing data specification** — impossible to know what's in the billing PDFs
- **No sample exports** — no example files
- **No export instructions** — no UI walkthrough or API documentation
- **No schema or format documentation** — "C-CDA" and "PDF" is the entire format specification
- **No value sets or code system documentation**
- **No relationship documentation**

A developer tasked with importing data from this export would have essentially nothing to work with beyond "expect some C-CDA files and some PDFs." They would not know what data elements to expect, what coding systems are used, how clinical and billing data relate, or how to parse the billing PDFs.

The only substantive technical documentation is the 74-page FHIR API PDF, but this covers §170.315(g)(10) — the standardized API — not the (b)(10) EHI export. It documents 23 FHIR R4 resources with 403 data elements mapped to US Core 6.1.0 profiles. While this provides insight into what clinical data the system can expose, it explicitly covers only the USCDI v3 subset and says nothing about billing, patient communications, or vendor-specific data.

**Could a developer build an import from this documentation?** No. The documentation is insufficient to understand what the export contains, let alone build a parser for it.

## 7. Overall Assessment

### Classification

**Minimal/stub**: Documentation is too thin to assess actual export content. The 192-word description on the certification disclosures page asserts (b)(10) compliance but provides no technical substance. There is no data dictionary, no schema, no sample data, and no specification of what clinical or billing data is actually exported. The use of PDF for billing data raises computability concerns.

### Key Findings

1. **No data dictionary or technical documentation exists for the (b)(10) export.** The entire EHI export specification is 192 words of general prose claiming C-CDA for clinical data and PDF for billing data. This is among the thinnest (b)(10) documentation possible. (Source: `certification-disclosures.html`)

2. **Billing data is exported as PDF — not a computable format.** The vendor's RCM module stores structured claims, charges, payments, and eligibility data, but the export renders this as PDF. This likely fails the "electronic and computable" requirement of (b)(10). (Source: `certification-disclosures.html`, EHI Export section)

3. **No distinction between (b)(10) and (g)(10) coverage is evident.** The only available technical documentation for the product's data model is the FHIR API PDF covering USCDI v3 / US Core 6.1.0 — the same standard clinical summary available through the (g)(10) API. If the C-CDA export draws from the same data source, the (b)(10) export adds only billing PDFs and uploaded documents beyond what's already available via FHIR. (Source: `carbonhealth-fhir-api-doc-v1_2.pdf`)

4. **Patient communications and AI-generated charting data are not mentioned.** CarbyOs's flagship feature is AI-powered ambient charting that generates SOAP notes from doctor-patient conversations. The product also has patient messaging and video visit capabilities. Neither is mentioned in the EHI export documentation. (Source: `product-research.md` vs `certification-disclosures.html`)

5. **The live certification disclosures site (ehr-support.carbyos.com) is accessible and unchanged.** Verified 2026-02-16 — HTTP 200, same 49,799-byte page, hosted on Vercel. No additional EHI export documentation has been added since collection. (Source: live verification)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   C-CDA (clinical), PDF (billing), native (uploads)
Model type:      Standard projection (C-CDA) + non-computable PDFs
Entities:        0 (no data dictionary)
Fields:          0 (no data dictionary)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (claimed, no technical detail)
Domains covered: 0 of 16 confirmed; up to 13 of 16 implied but unverifiable
```

### Bottom Line

Carbon Health's EHI export documentation is a compliance stub — 192 words asserting (b)(10) compliance with no supporting technical detail. A patient or provider requesting their data would receive C-CDA files and billing PDFs, but there is no way to know from the documentation what data elements are included, whether the clinical export goes beyond a standard USCDI summary, or what billing information appears in the non-computable PDFs. The single biggest gap is the complete absence of a data dictionary or any field-level documentation, making it impossible to assess whether this is a genuine "all EHI" export or a clinical summary repackaged with billing PDFs.
