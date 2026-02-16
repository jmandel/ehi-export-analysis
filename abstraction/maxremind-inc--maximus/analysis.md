# EHI Export Analysis: MaxRemind Inc

**Product**: Maximus 1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3173.MAXR.01.00.1.231031 (ID 11360)

## 1. Product Context

Maximus EHR is a cloud-based, ONC-certified electronic health record system by MaxRemind Inc, a small Richardson/Carrollton, Texas–based company whose core business is medical billing and revenue cycle management (RCM). The product is marketed as an "all-in-one" platform for clinical documentation, practice management, and billing, supporting 75+ medical specialties. It was certified in October 2023 with 35+ ONC criteria.

**Data domains the product stores (baseline for completeness assessment):**

- **Clinical documentation**: Problem lists, medications, allergies, vitals, labs, immunizations, procedures, clinical notes, care plans, family history, implantable devices, social/behavioral data
- **Orders & prescriptions**: CPOE for medications, labs, diagnostic imaging; e-prescribing
- **Billing & RCM**: Claims, billing records, charges, payments, ICD/CPT codes, eligibility verification — this is MaxRemind's core competency
- **Scheduling**: Appointments, follow-ups, reminders
- **Patient engagement**: Patient portal with secure messaging, appointment self-scheduling
- **Care coordination**: Transitions of care (C-CDA), Direct messaging, referrals
- **Documents**: Progress notes, lab results, radiology reports, scanned/uploaded documents
- **Remote patient monitoring**: Via MaxRPM companion product (vitals: BP, weight, pulse, glucose)
- **Public health reporting**: Immunization registries, syndromic surveillance, electronic case reporting

The critical question for this analysis: does the export cover the billing/RCM data that is central to MaxRemind's business, and does it go beyond standard clinical summaries?

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `B10-Electronic-Health-information-Export.pdf` (254 KB, 4 pages) | The sole EHI export documentation. Describes 6 export components: C-CDA, FHIR Bulk Data, Demographics/Insurance Excel, Appointments Excel, and document files. Created 2023-10-03 by Nouman Zafar in Microsoft Word. | **Primary artifact** — but extremely thin. No data dictionary, no field definitions, no schemas, no sample data. |
| `screenshot-certification-page-full.png` (1.1 MB) | Full-page screenshot of the ONC certification page at maxremind.com/maximusehr-certification/. Shows all certification criteria, documentation links, additional software (NewCrop 2.0, MaxMD 3.0), and costs section. | Moderately informative — confirms page structure, third-party integrations. |
| `screenshot-certification-page.png` (473 KB) | Partial screenshot of the same page, focused on the documentation links section. | Low — subset of the full screenshot. |
| `screenshot-fhir-docs-portal.png` (260 KB) | Screenshot of the FHIR documentation portal at documents.maximus.care. Shows client registration, OAuth2 flow, authorization server info, and API endpoints. | Moderately informative — confirms this is strictly (g)(10) FHIR API documentation with no (b)(10)-specific content. |
| `documents.maximus.care` JS bundle (live, verified 2026-02-16) | React SPA serving FHIR API docs. Parsed to extract 18 US Core STU 3.1.1 resource types documented. | Confirms standard US Core only — no custom profiles or vendor extensions. |

**Verification notes:**
- Certification page (maxremind.com/maximusehr-certification/) returns HTTP 200 as of 2026-02-16 — confirmed accessible.
- FHIR docs portal (documents.maximus.care) returns HTTP 200 — confirmed accessible.
- FHIR API metadata endpoint (fhir.maximus.care/api/metadata) returns HTTP 404 — confirmed not publicly accessible.
- The B10 PDF is indeed 4 pages and 254,534 bytes as reported. No additional EHI-specific documentation was found beyond this PDF.

## 3. Export Mechanics

**Format(s):** Hybrid multi-format:
- C-CDA XML (R2.1) for structured clinical data
- FHIR R4 / US Core STU 3.1.1 via Bulk Data API
- Excel (.xlsx) for demographics/insurance and appointments
- Native file formats (PDF, JPG, PNG) for clinical documents

**Mechanism:** The PDF states the system "allows a user to export electronic health information (EHI) for a single patient at any time without developer assistance." No step-by-step procedure, screenshots, or UI description is provided. The FHIR component references the (g)(10) API, implying programmatic access via OAuth2.

**Single-patient vs bulk:** Both are explicitly supported. Single-patient export is available "at any time without developer assistance." Multi-patient export is described as exporting "all the data for a patient population."

**Access constraints or fees:** The certification page includes a "Costs" section describing a subscription-based model for access to EHR features including data management. No specific export fees are mentioned, but the cost model is not granular enough to determine if export functionality incurs additional charges.

**Additional software noted on certification page:** NewCrop 2.0 (prescribing) and MaxMD 3.0 (Direct messaging). These are third-party integrations whose data may or may not be included in the export.

## 4. Export Content: What's In It

### Overview

The export documentation contains **zero field-level definitions**. There is no data dictionary, no schema, no sample data, and no machine-readable artifact describing the structure of any export component. The entire export is described in approximately 400 words of prose across 4 PDF pages, most of which is boilerplate (title page, table of contents, copyright notices).

### Vendor's own content organization

The B10 PDF organizes export content into the following components:

| Component | Format | Documentation Detail | Fields Documented |
|---|---|---|---|
| CCD/C-CDA Documents | HL7 C-CDA XML R2.1 | References HL7 specifications; no vendor-specific detail | 0 (inherits C-CDA standard) |
| FHIR Bulk Data Access | FHIR R4 / US Core 3.1.1 | References documents.maximus.care; standard US Core only | 0 (inherits US Core standard) |
| Patient Demographics & Insurance | Excel | One sentence: "comprehensive view of demographics and insurance details" | 0 |
| Appointments | Excel | One sentence: "comprehensive view of all future appointment details" | 0 |
| Documents | PDF, JPG, PNG | One paragraph describing folder organization by patient chart number and category | 0 |

**Total vendor-documented fields: 0.** No column names, no data types, no descriptions, no value sets, no relationships.

### FHIR component detail

The FHIR documentation portal documents 18 US Core STU 3.1.1 resource types:

AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationRequest, Observation, Organization, Patient, Practitioner, Procedure, Provenance

These are standard US Core resources with no custom profiles, no vendor extensions, and no vendor-specific search parameters. Two US Core resources are absent from the documentation: Medication and PractitionerRole (minor gaps).

This component is the (g)(10) FHIR API repackaged as a (b)(10) export component.

### C-CDA component detail

The PDF references three HL7 C-CDA specifications (R2.1 era) and states compliance with USCDI v1. No vendor-specific C-CDA template customizations, no section list, no sample document. The clinical content would be whatever standard C-CDA sections the product populates — likely covering problems, medications, allergies, vitals, labs, immunizations, procedures, and results, but this cannot be verified from the documentation alone.

### Proprietary components (beyond standards)

Only three components go beyond C-CDA/FHIR:

1. **Demographics & Insurance Excel**: No column definitions. "Comprehensive view" is the only description.
2. **Appointments Excel**: No column definitions. Explicitly limited to "future" appointments — historical appointment/visit data is not mentioned.
3. **Document files**: Physical files (PDF, JPG, PNG) organized in folders by patient chart number with category subfolders. No metadata file or manifest is described.

These three components are the only (b)(10)-specific additions. They are undocumented at the field level.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes five content areas:

1. **Standard clinical data via C-CDA/FHIR** — The broadest component, covering standard USCDI v1 clinical data through two standard interchange formats. This is purely the (g)(10) API and C-CDA export rebranded. It covers problems, medications, allergies, immunizations, vitals, labs, procedures, encounters, care plans, goals, devices, and provenance — but only what the standard specifications define, not what the EHR actually stores.

2. **Demographics & Insurance** — A single undocumented Excel file. Potentially valuable as it may include insurance coverage data not in C-CDA/FHIR, but with zero documentation, this is unknowable.

3. **Appointments** — A single undocumented Excel file limited to *future* appointments only.

4. **Clinical documents** — Physical files in native formats. Could potentially be rich (scanned records, progress notes, lab reports, radiology), but the absence of a metadata index means there's no structured way to link these to patients, encounters, or dates beyond folder naming.

**What's missing is stark.** For a vendor whose core business is medical billing/RCM, the export documentation makes absolutely no mention of billing data, claims, charges, payments, superbills, coding data, or any financial records. Similarly absent: e-prescribing history, referrals, care coordination records, remote patient monitoring data (MaxRPM), patient portal messages, and specialty-specific clinical assessments.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | "Demographics & Insurance" Excel (undocumented); FHIR Patient resource | Excel file likely covers this but zero field documentation prevents verification |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource; C-CDA headers | Standard encounter data only; no visit-level detail beyond what C-CDA/FHIR provides |
| Problems / conditions | ⚠️ Partial | FHIR Condition; C-CDA Problem section | Standard only — no vendor-specific problem list extensions |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest; C-CDA Medications section | MedicationRequest only (no MAR, no e-prescribing transaction history); product uses NewCrop for prescribing — unclear if that data is included |
| Allergies | ⚠️ Partial | FHIR AllergyIntolerance; C-CDA Allergies section | Standard only |
| Immunizations | ⚠️ Partial | FHIR Immunization; C-CDA Immunizations section | Standard only |
| Vitals | ⚠️ Partial | FHIR Observation (vitals); C-CDA Vital Signs section | Standard only |
| Lab results | ⚠️ Partial | FHIR DiagnosticReport, Observation (labs); C-CDA Results section; document files (lab reports) | Standard structured results plus physical lab report files |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport; document files (radiology) | Standard structured reports plus physical radiology report files |
| Procedures | ⚠️ Partial | FHIR Procedure; C-CDA Procedures section | Standard only |
| Clinical notes / documents | ✅ Covered | Document file export (signed progress notes, lab results, radiology reports, scanned/uploaded documents in PDF/JPG/PNG) | This is the strongest proprietary component — exports actual document files organized by patient |
| Care plans / goals | ⚠️ Partial | FHIR CarePlan, Goal; C-CDA | Standard only |
| Orders / referrals | ❌ Not covered | No export component addresses orders or referrals | Product supports CPOE and referral management; gap |
| Insurance / coverage | ⚠️ Partial | "Demographics & Insurance" Excel (undocumented) | Excel file title suggests insurance data is present, but no documentation to confirm scope |
| Claims / billing | ❌ Not covered | No billing data in any export component | **Critical gap.** MaxRemind's core business is medical billing/RCM. Product stores claims, charges, payments, billing records. None are mentioned in the export. |
| Payments | ❌ Not covered | No payment data mentioned | Product handles payment processing; gap |
| Consents / directives | ❌ Not covered | No consent data mentioned | Unclear if product stores advance directives; possible gap |
| Patient communications / portal messages | ❌ Not covered | No portal message data mentioned | Product has patient portal with secure messaging; gap |
| Specialty-specific data | ❌ Not covered | No specialty data mentioned | Product claims 75+ specialties (wound care case study highlighted); no specialty-specific assessments in export |

**Summary:** 0 domains fully and verifiably covered with field-level documentation. 11 domains partially covered via standard C-CDA/FHIR (but with no vendor-specific detail). 1 domain (clinical documents) covered through file export. 5+ domains completely absent from the export, including billing — the vendor's core competency.

## 6. Documentation Quality

**Rating: Very poor.**

The EHI export documentation fails on every dimension a developer would need:

- **Data dictionary**: None. Zero fields documented across all export components.
- **Schemas**: None. No XSD, JSON Schema, Excel column definitions, or any machine-readable format description.
- **Sample data**: None. No example C-CDA documents, no sample Excel files, no example FHIR resources with vendor-specific context.
- **Relationships**: Not documented. How demographics Excel relates to C-CDA patient records or FHIR Patient resources is unexplained.
- **Value sets**: Not documented for proprietary components. C-CDA/FHIR inherit standard value sets.
- **Export procedure**: Not documented. No screenshots, no step-by-step instructions, no UI descriptions.
- **Completeness statement**: No enumeration of what data is or isn't included in the export.

A developer receiving this export would be able to parse the C-CDA and FHIR components using standard tooling but would have no idea what columns the Excel files contain, no way to link document files to structured records, and no understanding of what data is missing versus what the EHR actually stores.

The FHIR documentation portal (documents.maximus.care) is the only substantive technical documentation, but it is purely (g)(10) API documentation — OAuth2 flows, FHIR endpoints, and standard US Core resource descriptions. It adds nothing specific to the (b)(10) EHI export requirement.

The entire (b)(10)-specific documentation is approximately 150 words of prose across the bottom half of one PDF page.

## 7. Overall Assessment

### Classification

**Minimal/stub.** The export documentation is too thin to assess actual export completeness. What documentation exists reveals that the "export" is primarily the C-CDA and FHIR (g)(10) API repackaged as a (b)(10) component, supplemented by three undocumented proprietary components (two Excel files and a document folder). There is no data dictionary, no field-level documentation, no sample data, and critical data domains (billing, specialty clinical data) are entirely absent.

### Key Findings

1. **The (b)(10) export is primarily the (g)(10) FHIR API and C-CDA export relabeled.** The PDF explicitly references the "(g)(10) SmartOnFHIR API Documentation" and the FHIR docs portal. The C-CDA and FHIR components cover only standard USCDI v1 clinical data — a subset of what the product stores. (`B10-Electronic-Health-information-Export.pdf`, page 3)

2. **Zero field-level documentation exists for any export component.** The entire EHI export is described in ~150 words of new prose (beyond boilerplate). The three proprietary components (demographics/insurance Excel, appointments Excel, document files) have one-sentence descriptions each with no column names, types, or value sets. (`B10-Electronic-Health-information-Export.pdf`, page 4)

3. **Billing and RCM data — MaxRemind's core competency — is completely absent from the export.** The product stores claims, charges, payments, and billing records (the company's primary business is medical billing services), yet the export documentation makes no mention of any financial data whatsoever. This is the single largest coverage gap. (`product-research.md`; `B10-Electronic-Health-information-Export.pdf`)

4. **Appointments export is limited to "future" appointments only.** The PDF explicitly states "future appointment details" — historical visit data, which is part of the designated record set, appears to be excluded. (`B10-Electronic-Health-information-Export.pdf`, page 4)

5. **No sample data, schemas, or machine-readable documentation exist.** A developer receiving this export would have no way to understand the proprietary Excel components without inspecting actual exported files. The FHIR documentation is purely standard US Core with no vendor customizations. (`files.json`; verified by artifact inspection)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   Mixed (C-CDA XML, FHIR R4 JSON, Excel, PDF/JPG/PNG)
Model type:      Standard projection (C-CDA + FHIR) with minimal proprietary additions
Entities:        0 documented (C-CDA/FHIR inherit standard; Excel files undocumented)
Fields:          0 documented
Descriptions:    N/A (no fields documented)
Sample data:     No
Bulk export:     Yes (stated for both single-patient and multi-patient)
Domains covered: 1 of 15 applicable domains fully covered; 11 partially via standards only
```

### Bottom Line

MaxRemind's EHI export is a compliance checkbox, not a genuine effort to export all electronic health information. The documentation consists of a 4-page PDF that primarily points to the existing (g)(10) FHIR API and C-CDA exports, with three undocumented proprietary Excel/file additions. The most significant gap is the complete absence of billing and RCM data — ironic given that medical billing is MaxRemind's core business. A patient or provider would receive standard clinical summary data via C-CDA/FHIR plus some document files, but would miss billing records, specialty assessments, portal communications, and any vendor-specific structured data the system maintains.
