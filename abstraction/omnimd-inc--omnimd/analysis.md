# EHI Export Analysis: OmniMD Inc.

**Product**: OmniMD (v18.0, v20)
**Analysis date**: 2026-02-16
**CHPL IDs**: 10784 (v18.0, certified 2022-01-10), 11354 (v20, certified 2023-10-24)

## 1. Product Context

OmniMD is a cloud-based, integrated ambulatory EHR and practice management platform from OmniMD Inc. (Hawthorne, NY), serving 12,000+ healthcare professionals across 600+ facilities. The platform combines:

- **EHR/EMR**: Clinical charting with specialty-specific templates for 40+ specialties, problem lists, medication lists, allergy tracking, lab integration (Labcorp, Quest), vitals, immunizations, procedures, clinical notes, AI-powered ambient documentation (AI Medical Scribe), clinical decision support (AI Clinician)
- **E-Prescribing**: SureScripts-certified, EPCS-certified controlled substance prescribing, medication reconciliation
- **Practice Management**: Appointment scheduling, patient check-in, insurance eligibility verification, patient flow management
- **Billing / RCM**: Built-in medical billing, claim scrubbing, claims submission, denial management, revenue analytics, outsourced billing services
- **Patient Portal**: Secure messaging, appointment scheduling, online billing/payments, view/download/transmit health records
- **Telehealth & RPM**: Video visits, remote patient monitoring, remote vitals capture
- **AI Solutions**: AI Front Desk, AI Medical Scribe, AI RCM, AI Clinician
- **Public Health Reporting**: Immunization registries, syndromic surveillance, cancer registries

This is a full-featured ambulatory EHR with significant billing/RCM and practice management capabilities. A genuine (b)(10) export should cover clinical data, billing/claims, prescribing details, patient portal communications, specialty-specific data, and documents — not just clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc` (38.6 KB) | Primary EHI export documentation. Word document listing 20 C-CDA sections and a reference to FHIR Bulk Data via g(10). Single-page, no data dictionary. | **Most informative** — defines the export scope |
| `OpenApi.pdf` (295 KB, 9 pages) | OpenAPI v1.1 documentation for OmniMD REST API. Documents `GetPatientData` endpoint with 33 boolean C-CDA section toggles. Created 2024-05-10. Explicitly serves g(7)/g(9), not b(10). | Moderately informative — reveals API structure and C-CDA section toggles |
| `openapiui.html` (29.7 KB) | Interactive API documentation UI at prod.omnixchange.com. Same content as PDF in web form. Explicitly states it satisfies g(7)/g(8)/g(9). | Low — duplicates PDF |
| `openapi-help.html` (14.4 KB) | ASP.NET Web API Help page listing 39 API endpoints. All descriptions say "No documentation available." | Low — unpopulated scaffold |
| `rwt-page-full.png` (1 MB) | Screenshot of the RWT page showing the EHI Export button placement | Low — confirms navigation path |
| `open-api-page-full.png` (1.1 MB) | Screenshot of the Open API page | Low — confirms page exists |
| `openapiui-screenshot.png` (1 MB) | Screenshot of interactive API UI | Low |
| `openapi-help-screenshot.png` (379 KB) | Screenshot of ASP.NET help page | Low |

## 3. Export Mechanics

- **Format**: C-CDA XML (CDA version 2.1), compliant with USCDI v1. Also references FHIR R4 Bulk Data but only by deferral to g(10).
- **Mechanism**: The Word document states the export supports both single-patient and patient-population ("bulk") export. The `GetPatientData` API endpoint returns CDA XML with selectable sections via boolean parameters. A separate `DownloadCDAPatient` endpoint also exists.
- **Single-patient vs bulk**: Both claimed ("export of electronic health information (EHI) for a single patient as well as for the patient population").
- **Access constraints**: API requires authentication (token-based, bearer token with 24-hour expiry). Registration requires vendor name, email, phone, and address. No fees mentioned in documentation.
- **Access path**: The EHI export documentation is a single button buried at the bottom of the Real World Testing page (omnimd.com/rwt/), under the V20 section.

## 4. Export Content: What's In It

### What the documentation provides

The EHI export documentation is a **single-page Word document** that lists 20 C-CDA section names with zero field-level detail. There is:

- **No data dictionary**: No field names, types, descriptions, cardinalities, or constraints
- **No schema**: No machine-readable definition of the export structure
- **No sample data**: No example C-CDA output or sample files
- **No value sets**: No code systems or coded value documentation
- **No relationships**: No documentation of how entities relate to each other
- **No vendor-specific mapping**: The document simply points to the HL7 C-CDA specification for format details

The OpenAPI PDF provides slightly more information via the `GetPatientData` endpoint, which reveals 33 boolean toggle parameters — 32 distinct C-CDA section selectors plus a `PatientAll` master toggle. This shows the API supports additional sections beyond the 20 listed in the EHI export document (e.g., `Pregnancy`, `ReasonForReferral`, `CarePlan`, `CareTeam`, `ClinicInformation`, `PatientContact`, `PlannedMedication`, `PlannedAppointments`, `PlannedProcedure`).

### Vendor's own content organization

The vendor organizes the export as C-CDA sections. Since no field-level documentation exists, the table below reflects only section names:

| C-CDA Section | Fields | Described | Types | Category |
|---|---|---|---|---|
| ADVANCE DIRECTIVES | 0 (undocumented) | N/A | N/A | Clinical |
| ALLERGIES, ADVERSE REACTIONS, ALERTS | 0 (undocumented) | N/A | N/A | Clinical |
| ASSESSMENTS | 0 (undocumented) | N/A | N/A | Clinical |
| ENCOUNTERS | 0 (undocumented) | N/A | N/A | Clinical |
| FAMILY HISTORY | 0 (undocumented) | N/A | N/A | Clinical |
| FUNCTIONAL STATUS | 0 (undocumented) | N/A | N/A | Clinical |
| IMMUNIZATIONS | 0 (undocumented) | N/A | N/A | Clinical |
| INSTRUCTIONS | 0 (undocumented) | N/A | N/A | Clinical |
| MEDICAL EQUIPMENT | 0 (undocumented) | N/A | N/A | Clinical |
| HISTORY OF MEDICATION | 0 (undocumented) | N/A | N/A | Clinical |
| MEDICATION ADMINISTERED | 0 (undocumented) | N/A | N/A | Clinical |
| INSURANCE PROVIDERS | 0 (undocumented) | N/A | N/A | Insurance |
| TREATMENT PLAN | 0 (undocumented) | N/A | N/A | Clinical |
| PROBLEM LIST | 0 (undocumented) | N/A | N/A | Clinical |
| PROCEDURES | 0 (undocumented) | N/A | N/A | Clinical |
| PROGRESS NOTE | 0 (undocumented) | N/A | N/A | Clinical |
| CHIEF COMPLAINT AND REASON FOR VISIT | 0 (undocumented) | N/A | N/A | Clinical |
| LAB RESULTS | 0 (undocumented) | N/A | N/A | Clinical |
| SOCIAL HISTORY | 0 (undocumented) | N/A | N/A | Clinical |
| VITAL SIGNS | 0 (undocumented) | N/A | N/A | Clinical |

**Additional sections visible in the API but not listed in EHI export doc**: Pregnancy, ReasonForReferral, CarePlan, CareTeam, EncompassingEncounter, ClinicInformation, PlannedMedication, PatientContact, PlannedAppointments, PlannedProcedure, FunctionalStatus (appears redundant with FunctionalStatus listed in the EHI doc as "FUNCTIONAL STATUS").

Total entities in the full inventory JSON: 20 C-CDA sections (from the EHI doc), 0 fields documented.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes their EHI export as 20 C-CDA sections, which map directly to standard clinical summary categories: allergies, problems, medications, vitals, labs, immunizations, procedures, encounters, notes, care plans, social history, family history, advance directives, functional status, medical equipment, and insurance payers. The vendor explicitly states the export complies with "USCDI, Version 1 requirements."

This is a clinical summary export. It has no depth — zero field-level documentation, zero description of what OmniMD-specific data each section contains, zero indication that the export goes beyond what a standard C-CDA template would contain. There is no evidence of any billing, specialty, portal, telehealth, prescribing detail, or custom form data in the export.

The FHIR alternative is explicitly described as the g(10) specification — not an independent EHI export but a direct reference to the existing FHIR API.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implicit in C-CDA patient header; no dedicated entity | C-CDA includes basic demographics but no indication of extended demographic fields OmniMD stores |
| Encounters / visits | ⚠️ Partial | ENCOUNTERS section listed | Section name only; no field detail. Product stores encounter data with scheduling, check-in, telehealth — likely only clinical encounter summary exported |
| Problems / conditions | ⚠️ Partial | PROBLEM LIST section listed | Section name only; standard C-CDA problem list. No indication of OmniMD-specific problem fields |
| Medications / prescriptions | ⚠️ Partial | HISTORY OF MEDICATION, MEDICATION ADMINISTERED sections | Covers medication history but likely not detailed e-prescribing records (Rx transactions, pharmacy interactions, EPCS records) |
| Allergies | ⚠️ Partial | ALLERGIES, ADVERSE REACTIONS, ALERTS section | Standard C-CDA allergy section |
| Immunizations | ⚠️ Partial | IMMUNIZATIONS section | Standard C-CDA immunization section |
| Vitals | ⚠️ Partial | VITAL SIGNS section | Standard section; unclear if RPM-captured vitals are included |
| Lab results | ⚠️ Partial | LAB RESULTS section | Standard section; no detail on how Labcorp/Quest integration data is represented |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in export | Product has LIS/RIS integration; imaging reports absent |
| Procedures | ⚠️ Partial | PROCEDURES section | Standard C-CDA procedure section |
| Clinical notes / documents | ⚠️ Partial | PROGRESS NOTE, ASSESSMENTS, CHIEF COMPLAINT sections | Clinical notes present but no indication of AI Scribe outputs, specialty templates, or attached documents |
| Care plans / goals | ⚠️ Partial | TREATMENT PLAN section (+ CarePlan, CareTeam in API) | Standard C-CDA plan of care |
| Orders / referrals | ⚠️ Partial | ReasonForReferral toggle in API (not in EHI doc) | API has a referral parameter but not listed in the EHI export doc |
| Insurance / coverage | ⚠️ Partial | INSURANCE PROVIDERS section | Payer identity only via C-CDA Payers section; not detailed coverage/eligibility data |
| Claims / billing | ❌ Not covered | No billing entities in export | **Significant gap.** Product has full billing/RCM: claims, charge capture, denial management, revenue analytics. None exported. |
| Payments | ❌ Not covered | No payment entities in export | **Significant gap.** Product supports patient payments via portal. None exported. |
| Consents / directives | ⚠️ Partial | ADVANCE DIRECTIVES section | Standard C-CDA section; likely limited to advance directive documents, not consent forms |
| Patient communications | ❌ Not covered | No portal message or communication entities | **Gap.** Product has patient portal with secure messaging. None exported. |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities | **Gap.** Product claims 40+ specialty templates. None represented in export. |

## 6. Documentation Quality

The documentation quality is extremely poor:

- **Usability for a developer**: A developer could not build an import from this documentation. The EHI export document lists 20 section names and points to the HL7 C-CDA specification. No OmniMD-specific mapping, field definitions, or structural guidance is provided.
- **Field-level documentation**: None. Zero fields documented. Zero descriptions. Zero types.
- **Machine-readable artifacts**: None. No schema, no JSON/XML structure definition, no sample data files.
- **Worked examples**: None. The OpenAPI PDF shows authentication examples but no C-CDA output examples.
- **Completeness**: The documentation is a single page. The entire EHI export section of the Word document could fit in a single paragraph.

The only additional technical detail comes from the OpenAPI PDF (which documents the g(7)/g(9) API, not the b(10) export specifically), which reveals 33 boolean parameters for the `GetPatientData` endpoint — showing which C-CDA sections can be toggled on/off. This is the closest thing to a "data dictionary" and it provides only parameter names and brief descriptions.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export is described only as 20 C-CDA section names with zero field-level detail. Even taking the sections at face value, they cover only standard clinical summary data — the same USCDI v1 scope that a C-CDA transitions-of-care document would contain. The product stores extensive billing/RCM data (claims, charges, payments, denials), patient portal communications, prescribing transaction records, specialty-specific clinical templates for 40+ specialties, telehealth records, and RPM data — none of which appear in the export. The documentation is too thin to assess whether the actual C-CDA output includes any vendor-specific extensions, but the documentation gives no indication of any. The export description explicitly states USCDI v1 compliance as its target, not all-EHI scope.

**Axis 2 — Export approach: Repackaged existing export**

Multiple lines of evidence confirm this is a repackaged C-CDA clinical exchange export, not a purpose-built EHI export:

1. The EHI export document explicitly says the C-CDA complies with "USCDI, Version 1 requirements" — framing the export as a clinical exchange deliverable, not an all-EHI export.
2. The `GetPatientData` API endpoint is documented in the OpenAPI PDF as satisfying "§ 170.315(g)(7) and § 170.315(g)(9)" — the same API that serves the existing clinical exchange use case.
3. The FHIR alternative is described as "Please refer 170.315(g)(10) for the Standardized API" — an explicit deferral to the g(10) specification rather than an independent EHI export.
4. The 20 C-CDA sections map directly to standard C-CDA templates. No vendor-specific sections, extensions, or non-clinical data types are present.
5. No data dictionary, schema, or field-level mapping exists — the vendor did not build any product-specific export documentation, just pointed to the C-CDA standard.

### Key Findings

1. **The EHI export is a single-page Word document listing 20 C-CDA section names** — the thinnest documentation observed. No data dictionary, no field definitions, no sample data, no schema. (Source: `ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc`)

2. **Billing and RCM data — a major product capability — is entirely absent from the export.** OmniMD has built-in claims management, charge capture, denial management, and revenue analytics. None of this patient-specific billing data is exported. (Source: comparison of product-research.md capabilities vs. export sections)

3. **The export is explicitly framed as USCDI v1 compliance**, not all-EHI. The document states the C-CDA "comply with United States Core Data for Interoperability (USCDI), Version 1 requirements." (Source: `ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc`)

4. **The FHIR option is not an independent export** — it's a direct reference to the g(10) specification ("Please refer 170.315(g)(10)"). (Source: `ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc`)

5. **Specialty-specific data for 40+ specialties is unaccounted for.** OmniMD markets specialty-specific templates and workflows, but the export contains only generic C-CDA sections with no specialty content. (Source: product-research.md vs. export sections)

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML (CDA 2.1) + FHIR R4 (by reference to g(10))
Entities:        20 C-CDA sections (no field-level decomposition)
Fields:          N/A (zero field-level documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (claimed for single-patient and population)
Domains covered: ~8 of 18 applicable domains (all partial/USCDI-level only)
```

### Bottom Line

OmniMD's (b)(10) export is a compliance stub: a single-page document listing 20 standard C-CDA section names with no data dictionary, no field documentation, and no sample data. The export is a repackaged C-CDA clinical exchange covering only USCDI v1 scope, while the product stores extensive billing/RCM, specialty-specific clinical, patient communication, and prescribing data that is entirely absent from the export. A patient requesting their complete record through this export would receive a clinical summary but not their billing history, portal messages, specialty assessments, or detailed prescribing records.
