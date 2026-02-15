# EHI Export Analysis: CHN Tech Solutions LLC

**Product**: Integrated Care EHR (ICE), Version 3  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.05.05.3133.CHTS.01.00.1.221213 (ID 11067)

## 1. Product Context

Integrated Care EHR (ICE) is a cloud-based EHR built on the open-source OpenEMR platform, developed by CHN Tech Solutions LLC. The primary (and possibly only) deployment is at MyCHN (Community Health Network), a Federally Qualified Health Center (FQHC) with 19 locations in the greater Houston, Texas area. The product serves an FQHC population with these clinical capabilities:

- **Primary care** across adult, pediatric, and women's health specialties
- **Behavioral health**: psychiatry, counseling, and Medication Assisted Therapy (MAT)
- **Dental services**
- **Pharmacy services**
- **Screening/assessment tools**: SDOH, substance abuse, depression, fall risk, human trafficking, lead poisoning, vision, TB, smoking, dental, Zika
- **FQHC billing**: facility billing, fee-for-service billing, patient ledgers, payor aging reports
- **E-prescribing** (via NewCrop/SureScripts, transitioned from VeraDigm)
- **Lab interfaces** with 20+ laboratories
- **Radiology connectivity**
- **Patient portal** with secure messaging and mobile apps
- **Chronic care management** tracking, reporting, and billing
- **UDS reporting** (critical for FQHC compliance)

This product stores a wide range of clinical, billing, and specialty data. An adequate (b)(10) EHI export should cover all of these domains.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `ehi-export-page.html` | 46.2 KB | Main (b)(10) EHI export page — brief prose describing C-CDA as the export format, with links to HL7/IHE standards. No data dictionary, no field-level detail. | **Low** — establishes the export is C-CDA but provides no detail |
| `ehi-export-page.png` | 209.3 KB | Screenshot of the above page | Low — confirms text content |
| `ccd-operation-in-fhir.html` | 60.1 KB | Step-by-step tutorial for generating a CCD via FHIR `$docref` operation using Swagger UI (11 numbered steps with screenshots) | **Medium** — explains *how* to generate the export |
| `ccd-operation-in-fhir-screenshot.png` | 592.5 KB | Screenshot of the tutorial page | Low — visual confirmation |
| `fhir-api-page.html` | 66.7 KB | FHIR R4/US Core 3.1 API documentation — includes CCD section listing (21 sections), Bulk FHIR export endpoints, SMART on FHIR support, scope definitions | **High** — most informative artifact; lists CCD sections and FHIR resources |
| `rest-api-page.html` | 76.1 KB | OpenEMR-based REST API documentation — scope listings revealing native data model (23 resource types), OIDC auth, client registration | **High** — reveals data domains the product stores beyond C-CDA |
| `standard-api-page.html` | 80.5 KB | Near-duplicate of rest-api-page.html with minor formatting differences | Low — redundant |
| `CCDA_Vol1_2022SEP_errata.pdf` | 962.9 KB (63 pages) | HL7 C-CDA Implementation Guide Volume 1 (Introductory Material) — **standard HL7 document, not vendor-specific** | **None for vendor assessment** — generic standard hosted on vendor's site |
| `CCDA_Vol2_2022SEP_errata.pdf` | 6.9 MB (913 pages) | HL7 C-CDA Implementation Guide Volume 2 (Templates and Supporting Material) — **standard HL7 document, not vendor-specific** | **None for vendor assessment** — generic standard hosted on vendor's site |

**Notable**: No data dictionary, no sample export files, no schema documentation, no vendor-specific field mappings exist among the artifacts. The two PDFs (976 pages total) are standard HL7 publications, not vendor documentation.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated Clinical Document Architecture) XML document — a single CCD (Continuity of Care Document) per patient, generated on demand.
- **Mechanism**: API-based. The export is performed via the FHIR `$docref` operation using the system's Swagger UI or programmatic API calls. The 11-step tutorial involves: registering an API client, configuring OAuth2 scopes, authenticating, selecting a patient, calling the `$docref` endpoint, and downloading the resulting C-CDA file via the Binary endpoint. There is no documented in-product UI button or menu for direct patient/provider-initiated export.
- **Single-patient vs bulk**: The documented (b)(10) mechanism is **single-patient only** (one CCD per `$docref` call). The system also supports Bulk FHIR Export (system, group, and patient-level `$export`), but this is documented as the (g)(10) mechanism and exports FHIR resources, not C-CDA.
- **Date filtering**: CCD generation supports optional start/end date parameters that filter encounter-related sections. If no dates are specified, full history is returned for all sections.
- **Access constraints**: Requires OAuth2 authentication and specific scopes (`DocumentReference.$docref`, `DocumentReference.read`, `Binary.read`). The testing API endpoint (`chntech.from-tx.com`) is not DNS-resolvable (verified 2026-02-15; curl exit code 6). No production FHIR endpoint is published — the site states it "will be added when available."
- **Fees**: Not documented.

## 4. Export Content: What's In It

The export produces a standard C-CDA CCD document. There is **no vendor-specific data dictionary** — the vendor provides only CCD section names and defers entirely to the HL7 C-CDA Implementation Guide (913-page Vol. 2) for field-level detail.

### CCD sections documented

The FHIR API page (`fhir-api-page.html`) lists 21 CCD sections in two categories:

**Date-filtered sections (13)** — only include encounters within specified date range:
1. History of Procedures
2. Relevant DX Tests / LAB Data
3. Functional Status
4. Progress Notes
5. Procedure Notes
6. Laboratory Report Narrative
7. Encounters
8. Assessments
9. Treatment Plan
10. Goals
11. Health Concerns
12. Document Reason for Referral
13. Mental Status

**Full medical record sections (8)** — always include complete history:
1. Demographics
2. Allergies, Adverse Reactions, Alerts
3. History of Medication Use
4. Problem List
5. Immunizations
6. Social History
7. Medical Equipment
8. Vital Signs (latest recorded only)

### What the CCD does NOT contain

C-CDA is a clinical summary format. By design, it excludes:
- Billing/claims data
- Insurance/coverage information
- Scheduling/appointment data
- Patient portal messages
- Prescription routing/transmission records
- Dental records
- Screening instrument responses (as structured data)
- Custom form data
- Documents/attachments beyond the generated summary

### OpenEMR native REST API: reveals additional data domains

The REST API documentation (`rest-api-page.html`) exposes 23 native resource types through OpenEMR-specific API scopes, revealing data the system stores but does NOT export via the (b)(10) C-CDA mechanism:

| OpenEMR API Resource | In CCD Export? | Notes |
|---|---|---|
| allergy | ✅ Yes | Mapped to CCD Allergies section |
| appointment | ❌ No | Scheduling data, not in CCD |
| dental_issue | ❌ No | Dental-specific data, no CCD mapping |
| document | ❌ No | Stored documents/attachments |
| drug | Partial | Drug reference data; medications are in CCD |
| encounter | ✅ Yes | Mapped to CCD Encounters section |
| facility | N/A | Administrative/organizational data |
| immunization | ✅ Yes | Mapped to CCD Immunizations section |
| insurance | ❌ No | Patient insurance/coverage data |
| insurance_company | N/A | Reference data |
| insurance_type | N/A | Reference data |
| list | Varies | Lists may map to various CCD sections |
| medical_problem | ✅ Yes | Mapped to CCD Problem List |
| medication | ✅ Yes | Mapped to CCD Medications section |
| message | ❌ No | Patient/provider communications |
| patient | ✅ Yes | Demographics in CCD |
| practitioner | N/A | Provider reference data |
| prescription | Partial | Rx list in CCD, but not routing/transmission detail |
| procedure | ✅ Yes | Mapped to CCD Procedures section |
| soap_note | Partial | May map to Progress Notes, but CCD doesn't carry full SOAP structure |
| surgery | ❌ No | Surgical records — separate from generic procedures |
| transaction | ❌ No | Financial transactions |
| vital | ✅ Yes | Mapped to CCD Vital Signs (latest only) |

### FHIR API resources (25 types)

The FHIR API exposes standard US Core 3.1 resources: AllergyIntolerance, Appointment, Binary, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Group, Immunization, Location, Medication, MedicationRequest, Observation, Organization, Patient, Person, Practitioner, PractitionerRole, Procedure, Provenance.

These FHIR resources overlap significantly with the CCD content but are not documented as the (b)(10) export mechanism.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export is a single C-CDA CCD document per patient, containing 21 standard clinical summary sections. The vendor provides **no categorization of their own** — they simply list CCD section names and reference the HL7 standard.

The export covers the standard clinical summary data that C-CDA is designed to carry: demographics, allergies, medications, problems, immunizations, vitals, procedures, encounters, lab results, progress notes, assessments, care plans, goals, and referrals. This is the same data that would be exchanged during a transition of care — it is essentially the vendor's (b)(1) Transitions of Care capability repackaged as (b)(10).

The REST API scope listing reveals the system stores significantly more data than the CCD exports: dental issues, insurance information, surgical records, financial transactions, stored documents, appointments, SOAP notes, and patient messages are all accessible through the native API but excluded from the EHI export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | CCD Demographics section (full record) | Standard C-CDA demographics |
| Encounters / visits | ✅ Covered | CCD Encounters section (date-filterable) | Encounter data present |
| Problems / conditions / diagnoses | ✅ Covered | CCD Problem List (full record) | Standard problem list |
| Medications / prescriptions | ⚠️ Partial | CCD History of Medication Use (full record) | Medication list present but prescription routing/transmission details (NewCrop/SureScripts) not included |
| Allergies | ✅ Covered | CCD Allergies, Adverse Reactions, Alerts (full record) | Standard allergy list |
| Immunizations | ✅ Covered | CCD Immunizations section (full record) | Standard immunization list |
| Vitals | ⚠️ Partial | CCD Vital Signs — **latest recorded only** | Only most recent vitals; historical vitals not exported. Significant limitation. |
| Lab results | ✅ Covered | CCD Relevant DX Tests / LAB Data, Laboratory Report Narrative (date-filterable) | Present, though unclear if all results from 20+ interfaced labs are fully represented |
| Imaging / diagnostic reports | ⚠️ Partial | May be captured in CCD procedure/lab sections | No dedicated imaging section; unclear coverage of radiology interface results |
| Procedures | ✅ Covered | CCD History of Procedures, Procedure Notes (date-filterable) | Present |
| Clinical notes / documents | ⚠️ Partial | CCD Progress Notes (date-filterable) | Progress notes present but not the full richness of specialty SOAP notes (psychiatry, therapy, MAT, women's health). Stored documents/attachments not included. |
| Care plans / goals | ✅ Covered | CCD Treatment Plan, Goals, Health Concerns (date-filterable) | Present |
| Orders / referrals | ⚠️ Partial | CCD Document Reason for Referral (date-filterable) | Referral reasons present; order details unclear |
| Insurance / coverage | ❌ Not covered | No insurance data in CCD; `insurance` scope exists in REST API | Product stores insurance data (FQHC billing requires it); **significant gap** |
| Claims / billing | ❌ Not covered | No billing data in CCD; `transaction` scope in REST API | Product does FQHC facility billing and fee-for-service billing; **significant gap** |
| Payments | ❌ Not covered | No payment data in CCD | Product tracks payments, patient ledgers, payor aging; **significant gap** |
| Consents / directives | ❌ Not covered | No consent/directive section in CCD | Unknown if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No messaging in CCD; `message` scope in REST API | Product has patient portal with secure messaging; **gap** |
| Specialty: Behavioral health (psychiatry, therapy, MAT) | ⚠️ Partial | May be captured in Progress Notes/Assessments sections | Product has dedicated psychiatry, therapy, and MAT modules; CCD likely loses specialty-specific structured data (screening instruments, assessment tools) |
| Specialty: Dental | ❌ Not covered | No dental sections in CCD; `dental_issue` scope in REST API | MyCHN provides dental services; product has dental data; **gap** |
| Specialty: Women's health / OBGYN | ⚠️ Partial | May be captured in generic clinical sections | Product has women's health module; CCD may not capture specialty-specific data |
| Specialty: Screening assessments (SDOH, substance abuse, depression, etc.) | ⚠️ Partial | CCD Assessments and Social History sections | Product has 12+ screening tools; structured screening responses likely not fully represented in CCD template format |

**Summary**: Of ~21 applicable domains, 6 are covered, 8 are partially covered, and 7 are not covered at all. The most significant gaps are billing/claims/payments, insurance/coverage, dental records, patient communications, and specialty screening data — all of which the product demonstrably stores (evidenced by REST API scopes and product feature documentation).

## 6. Documentation Quality

- **Data dictionary**: **None.** No field-level documentation exists. No mapping between EHR data fields and CCD elements. No description of how vendor-specific data is represented in the C-CDA output.
- **Schema/format specification**: The vendor defers entirely to the HL7 C-CDA Implementation Guide (two PDFs totaling 976 pages) hosted on their site. These are standard documents, not vendor-customized.
- **Sample data**: **None.** No sample CCD files, no example exports, no test data.
- **Procedural documentation**: The 11-step Swagger tutorial for generating a CCD via `$docref` is clear and includes screenshots. A developer could follow it — if the API endpoint were accessible (it is not; DNS resolution fails for the test endpoint).
- **Machine-readable artifacts**: None. No JSON schemas, no OpenAPI/Swagger definitions (the Swagger endpoint is unreachable), no FHIR CapabilityStatement or StructureDefinitions.
- **Developer usability**: A developer would know the export produces a C-CDA CCD and would have a general tutorial on how to request one. They would have no vendor-specific information about the content, structure, or completeness of the resulting document. They would need to reverse-engineer any export they receive by reading the generic 913-page HL7 specification.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The (b)(10) EHI export is a C-CDA CCD document generated via the FHIR `$docref` operation. This is the vendor's existing Transitions of Care / FHIR clinical summary capability relabeled as the EHI export. It covers standard clinical summary domains but excludes billing, insurance, dental, messaging, and specialty-specific data that the product stores.

### Key Findings

1. **The EHI export is a C-CDA CCD — a clinical summary format, not a comprehensive data export.** The 21 CCD sections cover standard clinical domains but structurally cannot carry billing, insurance, scheduling, dental, or messaging data. This is a textbook case of repackaging the (b)(1)/(g)(10) capability as (b)(10). (Source: `fhir-api-page.html`, `ehi-export-page.html`)

2. **The REST API scope listing reveals significant data the product stores but does not export.** The OpenEMR native API exposes 23 resource types including `dental_issue`, `insurance`, `transaction`, `surgery`, `soap_note`, and `message` — none of which are represented in the C-CDA export. (Source: `rest-api-page.html`)

3. **There is no data dictionary, no sample data, and no vendor-specific documentation.** The vendor provides only CCD section names and links to generic HL7 standards. A developer cannot determine from these artifacts what specific data elements would appear in an export. (Source: all artifacts reviewed)

4. **The documented API endpoint is unreachable.** The test endpoint at `chntech.from-tx.com` fails DNS resolution (verified 2026-02-15). No production endpoint is published. This means the export mechanism cannot currently be tested or used by third parties. (Source: curl verification)

5. **Vital signs export is limited to the most recent values only.** Historical vital signs are not included in the CCD, which is an unusual limitation even within the C-CDA format. (Source: `fhir-api-page.html` — "Vital Signs (shows the latest vitals recorded for the patient)")

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML (CCD document)
Model type:      Standard projection (C-CDA R2.1)
Entities:        21 CCD sections (not database entities)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (defers to HL7 C-CDA standard)
Sample data:     No
Bulk export:     No (single-patient CCD; Bulk FHIR exists but is (g)(10), not (b)(10))
Domains covered: 6 of 21 applicable domains fully covered; 8 partial; 7 not covered
```

### Bottom Line

A patient requesting their complete EHI from Integrated Care EHR would receive a single C-CDA clinical summary document — effectively the same transition-of-care document their new provider would get. Their billing records, insurance information, dental records, screening assessment responses, patient portal messages, and specialty clinical documentation (behavioral health, MAT, women's health) would be absent. The single biggest gap is the complete absence of billing and financial data from a product that is specifically designed for FQHC billing — data that is squarely within the HIPAA designated record set.
