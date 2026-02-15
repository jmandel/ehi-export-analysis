# EHI Export Analysis: eHana

**Product**: eHana EHR
**Analysis date**: 2025-07-15
**CHPL ID**: 15.04.04.2594.eHan.19.00.1.191206

## 1. Product Context

eHana EHR is a cloud-based behavioral health electronic health record system designed primarily for Massachusetts nonprofit behavioral health organizations. According to product research, eHana supports:

- **Clinical documentation**: Progress notes, treatment plans, behavioral health assessments (including CANS — Child and Adolescent Needs and Strengths), group notes, e-prescribing via DrFirst integration
- **Billing and practice management**: HIPAA-compliant 837/835 claim processing, ERA posting, superbill generation, insurance verification, batch billing
- **Scheduling**: Appointment management with recurring appointments
- **Multi-program enrollment**: Tracking clients across multiple behavioral health programs with enrollment/discharge dates
- **Patient portal**: Secure messaging, document sharing
- **Specialty behavioral health**: CANS assessments, substance use tracking, behavioral health-specific workflow tools

The product reportedly generates over 600,000 clinical documents per month across its user base. This baseline establishes that a complete EHI export should cover behavioral health-specific assessments, billing/claims data, multi-program enrollment, scheduling context, and e-prescribing records — in addition to standard clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `EHI_Export.pdf` (15 pages) | The sole EHI export documentation. Image-based PDF (created via "Microsoft: Print To PDF" from Google Docs, 2023-05-10). Contains 18 C-CDA section descriptions, each with overview text, a UI screenshot ("HTML Element"), and sample C-CDA XML ("XML Element"). No extractable text (pdftotext returns empty). | **Primary artifact** — the only (b)(10)-specific documentation |
| `SmartOnFHIR-API-Doc.pdf` (68 pages) | SMART on FHIR API documentation for §170.315(g)(10). Describes FHIR R4 endpoints, OAuth2 flows, and supported USCDI resources. Separate from (b)(10). | Context only — not EHI export documentation |
| `fhir-base-urls.csv` | Four rows: test and prod FHIR server endpoints and auth server endpoints. Prod URLs listed as "available upon request." | Minimal — confirms FHIR infrastructure exists |
| `screenshot-ehana.com.png` | Screenshot of eHana website | Minimal |

**Key finding**: Only one artifact (`EHI_Export.pdf`) documents the (b)(10) EHI export. There is no data dictionary, no schema, no sample export file, and no machine-readable specification.

## 3. Export Mechanics

- **Format**: C-CDA R2 (Clinical Document Architecture Release 2) XML
- **Mechanism**: Not clearly documented. The PDF title page states compliance with §170.315(b)(10) but does not describe how a user initiates an export (UI button, API call, or vendor-assisted process).
- **Single-patient vs bulk**: Not specified. C-CDA is inherently a single-patient document format; the documentation shows single-patient examples only.
- **Access constraints or fees**: Not documented.

The PDF opens with: "Electronic Health Information (EHI) Export" and states it follows the CDA R2 format for §170.315(b)(10) compliance. Beyond this, there is no procedural documentation.

## 4. Export Content: What's In It

### Structure of the documentation

The 15-page PDF documents 18 C-CDA sections. Each section follows an identical three-part format:

1. **Overview**: A 1-2 sentence description of the section
2. **HTML Element**: A screenshot of how the data appears in the eHana UI
3. **XML Element**: A sample C-CDA XML snippet showing the structured data

There is **no data dictionary**. There are no field-level specifications, no cardinality/optionality documentation, no value set enumerations beyond what's visible in the XML snippets, and no relationship documentation.

### What a C-CDA inherently contains

A C-CDA document is a standardized clinical summary. It represents a **projection** of the EHR's native data model into a fixed set of clinical sections. By definition, C-CDA cannot represent:

- Billing/claims data (837/835 transactions)
- Insurance/coverage details beyond basic payer info
- Multi-program enrollment records
- Behavioral health-specific assessments (e.g., CANS instruments)
- Scheduling data
- Custom clinical forms or assessments
- E-prescribing transaction history
- Patient portal messages

### Vendor's own content organization

The vendor organizes the export into 18 numbered sections. All are standard C-CDA sections — no vendor extensions or custom sections are documented.

| # | Section Name | Key Data Elements | LOINC Code | Code Systems | Pages |
|---|---|---|---|---|---|
| 1 | Electronic Chart / Patient Data | Name, DOB, gender, race, ethnicity, language, telecom, address | N/A | HL7 AdminGender, CDC Race/Ethnicity | 2–3 |
| 2 | Vital Signs | Vital type, value+units, time | 8716-3 | LOINC | 3–4 |
| 3 | Immunization | Vaccine (CVX), manufacturer, lot#, date | 11369-6 | CVX | 4 |
| 4 | Allergies, Adverse Reactions, Alerts | Allergen (RxNorm/SNOMED), reaction, severity, status | 48765-2 | SNOMED-CT, RxNorm | 5 |
| 5 | History of Medication Use | Medication (RxNorm/NDC), start/end date, frequency, instructions, status | 10160-0 | RxNorm, NDC | 6 |
| 6 | Instructions | Instruction text, date | 69730-0 | LOINC | 7 |
| 7 | Functional and Cognitive Status | Assessment type, status, date | 47420-5 | SNOMED-CT, LOINC | 7–8 |
| 8 | Chief Complaint / Reason For Visit | Complaint text, date | 46239-0 | — | 8 |
| 9 | Problem List | Diagnosis (SNOMED), status, onset/resolution | 11450-4 | SNOMED-CT | 9 |
| 10 | Social History | Smoking status (SNOMED), birth sex | 29762-2 | SNOMED-CT | 10 |
| 11 | Encounters | Type, date/time, provider, diagnoses, location | 46240-8 | CPT | 10 |
| 12 | Results | Result type (LOINC), value+units, range, interpretation | 30954-2 | LOINC | 10 |
| 13 | Procedures | Procedure (SNOMED), date, status, provider | 47519-4 | SNOMED-CT | 11 |
| 14 | Reason for Referral | Referral reason text, date, status | 42349-1 | SNOMED-CT | 11 |
| 15 | Implantable Devices | Device UDI, name, assigning authority | N/A | SNOMED-CT | 12 |
| 16 | Health Concerns | Concern text, date | 75310-3 | LOINC | 13 |
| 17 | Assessment and Plan | Assessment narrative, plan items, date | 51847-2 | LOINC | 14 |
| 18 | Goals | Goal text, date | 61146-7 | LOINC | 15 |

**Total**: 18 sections, ~77 distinct data elements visible across all XML examples, 8 standard code systems referenced (SNOMED-CT, LOINC, RxNorm, NDC, CVX, CPT, HL7 AdministrativeGender, CDC Race/Ethnicity).

All 18 sections are standard C-CDA sections using standard template OIDs (e.g., `2.16.840.1.113883.10.20.22.2.5.1` for Problem List). No vendor-specific extensions, custom sections, or behavioral health-specific templates are present.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly what a standard C-CDA R2.1 clinical summary contains — no more, no less. The 18 sections map to standard USCDI v1 data classes:

- **Demographics**: Standard patient header (name, DOB, gender, race, ethnicity, address, phone)
- **Clinical observations**: Vitals, allergies, medications, problems, results, procedures, immunizations, social history, functional status
- **Care narrative**: Chief complaint, assessment & plan, instructions, health concerns, goals
- **Referrals**: Reason for referral
- **Device tracking**: Implantable devices
- **Encounters**: Basic encounter records

This is the standard C-CDA content set. It is essentially the same data available through the product's FHIR API (documented in the separate 68-page SmartOnFHIR-API-Doc.pdf). The (b)(10) export adds nothing beyond what (g)(10) already provides.

**What is entirely absent** — and this is the critical gap — is everything that makes eHana a *behavioral health* EHR:

- No billing/claims data (837/835 transactions, superbills, charge records)
- No insurance/coverage details
- No multi-program enrollment records
- No behavioral health assessments (CANS, substance use screenings)
- No custom clinical forms or behavioral health-specific documentation templates
- No e-prescribing transaction history (only current medication list)
- No patient portal messages
- No clinical document content beyond what fits in C-CDA sections (progress notes, treatment plans as structured documents)
- No payment records

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Section 1: name, DOB, gender, race, ethnicity, language, telecom, address | Standard C-CDA header; adequate for basic demographics |
| Encounters / visits | ⚠️ Partial | Section 11: encounter type, date, provider, diagnoses | Basic encounter records only; no encounter-level notes or detailed visit documentation |
| Problems / conditions | ✅ Covered | Section 9: SNOMED-coded diagnoses with status, onset/resolution | Standard problem list |
| Medications / prescriptions | ⚠️ Partial | Section 5: medication list with RxNorm/NDC codes, dates, frequency | Medication list only; no e-prescribing transaction history or prescription details |
| Allergies | ✅ Covered | Section 4: allergen, reaction, severity, status | Standard allergy section |
| Immunizations | ✅ Covered | Section 3: CVX-coded vaccines, manufacturer, lot# | Standard immunization section |
| Vitals | ✅ Covered | Section 2: LOINC-coded vitals with values and units | Standard vital signs |
| Lab results | ✅ Covered | Section 12: LOINC-coded results with values, ranges, interpretation | Standard results section |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in C-CDA export | If product stores imaging orders/reports, this is a gap |
| Procedures | ✅ Covered | Section 13: SNOMED-coded procedures with dates and status | Standard procedures section |
| Clinical notes / documents | ⚠️ Partial | Section 17 (Assessment and Plan) contains narrative text; no dedicated notes section | eHana generates 600K+ docs/month — progress notes, treatment plans, group notes are core product features but not exported as documents |
| Care plans / goals | ⚠️ Partial | Section 18 (Goals) and Section 16 (Health Concerns) | Basic goals and concerns; no structured treatment/care plans |
| Orders / referrals | ⚠️ Partial | Section 14 (Reason for Referral) | Referral reason text only; no structured orders |
| Insurance / coverage | ❌ Not covered | No insurance entities in export | Product handles insurance verification and billing — significant gap |
| Claims / billing | ❌ Not covered | No billing entities in export | Product processes 837/835 claims, generates superbills — **major gap** |
| Payments | ❌ Not covered | No payment records in export | Product processes ERA/835 payments — significant gap |
| Consents / directives | ❌ Not covered | No consent section in export | Unknown if product stores structured consents |
| Patient communications / portal messages | ❌ Not covered | No communications in export | Product has patient portal — gap if messages are stored |
| Specialty-specific (behavioral health) | ❌ Not covered | No behavioral health assessments (CANS, substance use screenings), no program enrollment, no behavioral health-specific forms | **Critical gap** — this is the product's core differentiator |

**Summary**: 7 of 19 applicable domains are adequately covered, 5 are partially covered, and 7 are not covered at all. The uncovered domains include the product's core behavioral health functionality and its entire billing/claims processing capability.

## 6. Documentation Quality

The documentation is **minimal**:

- **No data dictionary**: There is no field-level specification document. The only field information comes from eyeballing sample XML snippets in the PDF.
- **No machine-readable artifacts**: No schema (XSD, JSON Schema), no sample export file, no API specification. The PDF itself is image-based with no extractable text.
- **No export procedure documentation**: How to initiate an export, what parameters are available, and how the output is delivered are all undocumented.
- **No relationship documentation**: No foreign keys, no data model diagrams.
- **No value set documentation**: Code systems are visible in XML snippets (SNOMED, LOINC, RxNorm, etc.) but no value set bindings are specified.
- **No completeness specification**: No documentation of which fields are always present vs. optional, or what happens when data is missing.

The 15-page PDF is essentially a C-CDA template walkthrough with screenshots. A developer could not build an import pipeline from this documentation alone — they would need to rely on the C-CDA R2.1 standard specification and guess at eHana-specific behaviors.

**Could a developer use this?** Only if they already know C-CDA. The documentation adds almost nothing beyond what the C-CDA standard itself specifies. The XML snippets use standard template OIDs, standard code systems, and standard structures.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The (b)(10) EHI export is a C-CDA R2 clinical summary. It covers the same USCDI data classes available through the product's FHIR API and contains no vendor-specific extensions, no native database tables, and no data beyond what C-CDA supports. This is a textbook example of C-CDA/FHIR repackaging being labeled as "(b)(10)."

### Key Findings

1. **The export is a standard C-CDA document, not a native data export.** All 18 sections use standard C-CDA R2.1 template OIDs with no vendor extensions. This is functionally identical to a patient summary and covers perhaps 20-30% of the data eHana stores about patients. (Source: `EHI_Export.pdf`, all 15 pages)

2. **The product's core behavioral health features are entirely absent from the export.** CANS assessments, behavioral health-specific documentation templates, multi-program enrollment, substance use screenings, and other specialty features that differentiate eHana are not represented in any of the 18 C-CDA sections. (Source: product-research.md for capabilities; `EHI_Export.pdf` for absence)

3. **All billing and claims data is missing.** eHana processes HIPAA 837/835 claims, generates superbills, manages ERA posting, and handles insurance verification. None of this appears in the export — C-CDA has no billing sections. (Source: product-research.md for billing capabilities; `EHI_Export.pdf` sections 1-18 for absence)

4. **Documentation is minimal and not developer-usable.** The sole artifact is a 15-page image-based PDF with screenshots and XML snippets. No data dictionary, no schema, no sample files, no export procedure documentation. (Source: `EHI_Export.pdf`, `files.json` confirming no other EHI-specific artifacts)

5. **The (b)(10) export adds nothing beyond (g)(10) FHIR API.** The 18 C-CDA sections map directly to USCDI v1 data classes, which are the same data available through the product's SMART on FHIR API documented in `SmartOnFHIR-API-Doc.pdf`. The (b)(10) requirement exists precisely because FHIR/C-CDA clinical summaries are insufficient — yet that is exactly what this export provides.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA R2 (CDA R2 XML)
Model type:      Standard projection (C-CDA)
Entities:        18 C-CDA sections (standard, no extensions)
Fields:          ~77 data elements visible across XML examples (no formal field specification)
Descriptions:    N/A (no data dictionary; only overview sentences per section)
Sample data:     No (XML snippets in PDF only, no downloadable sample)
Bulk export:     Unclear (not documented)
Domains covered: 7 of 19 applicable domains fully covered; 5 partial
```

### Bottom Line

eHana's (b)(10) EHI export is a standard C-CDA clinical summary relabeled as an "EHI Export." It covers basic clinical data (demographics, vitals, medications, problems, allergies, labs) but entirely omits the product's core behavioral health features (CANS assessments, program enrollment, behavioral health forms), all billing/claims data, and patient portal communications. A patient or provider requesting their complete health information through this export would receive a clinical summary missing the majority of data eHana stores — particularly the behavioral health-specific information that is the product's primary purpose.
