# EHI Export Analysis: OmniMD Inc.

**Product**: OmniMD
**Analysis date**: 2026-02-16
**CHPL IDs**: 10784 (v18.0, certified 2022-01-10), 11354 (v20, certified 2023-10-24)

## 1. Product Context

OmniMD is a cloud-based, integrated EHR and practice management platform for ambulatory practices, serving 12,000+ healthcare professionals across 600+ facilities. It is marketed to 40+ medical specialties and includes:

- **EHR/EMR**: Clinical charting, specialty templates, AI-powered ambient documentation (AI Scribe), problem lists, medication lists, allergy tracking, lab integration (Labcorp, Quest), voice recognition
- **E-Prescribing**: SureScripts-certified, EPCS-certified controlled substance prescribing, medication reconciliation
- **Practice Management**: Scheduling, patient check-in (digital kiosk), insurance eligibility verification, patient flow management
- **Billing & RCM**: Built-in medical billing, automated claim scrubbing, claims management, denial tracking, revenue analytics, outsourced billing services
- **Patient Portal**: Secure messaging, appointment scheduling, online billing/payments, health record access
- **Telehealth**: Integrated video visits with EHR documentation
- **Remote Patient Monitoring**: Chronic condition monitoring, remote vitals
- **AI Tools**: AI Front Desk, AI Medical Scribe, AI RCM, AI Clinician

This breadth is critical for assessing export completeness. OmniMD stores clinical data, billing/claims data, prescription records, patient communications, telehealth records, RPM device data, specialty-specific assessments, and practice management data. A compliant (b)(10) export should cover all patient-facing data across these domains.

## 2. Artifacts Reviewed

| # | Artifact | Size | Description | Informativeness |
|---|---|---|---|---|
| 1 | `ELECTRONIC-HEALTH-INFORMATION-EHI-EXPORT-3-1.doc` | 38 KB (211 words, 2 pages) | Primary EHI export document — Word file listing 20 C-CDA sections and referencing FHIR Bulk Data. Created 2023-07-24 by Dr. Girirajtosh Purohit, last modified 2023-09-11. | **Most informative** — defines the export scope |
| 2 | `OpenApi.pdf` | 289 KB (9 pages) | OpenAPI v1.1 documentation for the (g)(7)/(g)(9) REST API. Documents 39 API endpoints including GetPatientData with 33 toggleable C-CDA section parameters. Created 2024-05-10. | Moderately informative — reveals available C-CDA sections via API |
| 3 | `openapiui.html` | 30 KB | Interactive API documentation at `prod.omnixchange.com/openapiui`. Same content as PDF in web form. Lists 20 selectable C-CDA sections. Explicitly states it satisfies §170.315(g)(7) and (g)(9). | Confirmatory |
| 4 | `openapi-help.html` | 15 KB | ASP.NET Web API Help Page scaffold listing 39 endpoints across 7 categories (Account, User, Patient, Practice, Values, Audit, Role). Every endpoint shows "No documentation available." | Minimally informative — unpopulated default scaffold |
| 5 | `rwt-page-full.png` | 978 KB | Screenshot of the registered URL showing the EHI export button placement under the V20 RWT section | Confirmatory |
| 6 | `open-api-page-full.png` | 1.1 MB | Screenshot of the Open API page with terms and download buttons | Confirmatory |
| 7 | `openapiui-screenshot.png` | 992 KB | Screenshot of the interactive API documentation UI | Confirmatory |
| 8 | `openapi-help-screenshot.png` | 371 KB | Screenshot of the ASP.NET Help Page | Confirmatory |

**No data dictionary, no sample data, no JSON/XML schema, no field-level documentation of any kind was found.**

## 3. Export Mechanics

- **Format**: HL7 C-CDA XML (CDA version 2.1), compliant with USCDI Version 1. FHIR R4 Bulk Data is mentioned as a secondary mechanism but refers entirely to the g(10) specification with no additional documentation.
- **Mechanism**: The EHI export document states support for both single-patient and patient population (bulk) export. The OpenAPI (g(7)/g(9)) provides a `POST api/Patient/GetPatientData` endpoint and a `POST api/Patient/DownloadCDAPatient` endpoint that return C-CDA XML. The EHI doc does not specify whether the (b)(10) export uses a different mechanism or the same API. No separate UI-based export workflow is documented.
- **Single-patient vs bulk**: Document claims both single-patient and bulk ("patient population") export capability.
- **Access constraints**: The API requires bearer token authentication via OAuth2 password grant. Registration requires a vendor account. No information about fees.

## 4. Export Content: What's In It

The export is defined entirely as a set of C-CDA sections. There is **no data dictionary** — no field-level documentation, no entity definitions, no types, no value sets, no relationships, no sample data. The only documentation is a bulleted list of 20 C-CDA section names in a 211-word Word document.

### Vendor's own content organization

The EHI export document lists 20 C-CDA sections as the exported content. The vendor provides no other categorization. Below is the complete list with domain classification:

| C-CDA Section (vendor's name) | API Parameter | Domain | Documentation Level |
|---|---|---|---|
| ADVANCE DIRECTIVES | AdvanceDirective | Consents/Directives | Section name only |
| ALLERGIES, ADVERSE REACTIONS, ALERTS | Allergy | Allergies | Section name only |
| ASSESSMENTS | Assessment | Clinical Notes | Section name only |
| ENCOUNTERS | Encounter | Encounters | Section name only |
| FAMILY HISTORY | FamilyHistory | Family History | Section name only |
| FUNCTIONAL STATUS | FunctionalStatus | Functional Status | Section name only |
| IMMUNIZATIONS | Immunization | Immunizations | Section name only |
| INSTRUCTIONS | Instruction | Patient Education | Section name only |
| MEDICAL EQUIPMENT | MedicalEquipment | Medical Equipment | Section name only |
| HISTORY OF MEDICATION | Medication | Medications | Section name only |
| MEDICATION ADMINISTERED | MedicationsAdministered | Medications | Section name only |
| INSURANCE PROVIDERS | Payer | Insurance/Coverage | Section name only |
| TREATMENT PLAN | PlanOfCare | Care Plans | Section name only |
| PROBLEM LIST | Problems | Problems/Conditions | Section name only |
| PROCEDURES | Procedure | Procedures | Section name only |
| PROGRESS NOTE | ProgressNote | Clinical Notes | Section name only |
| CHIEF COMPLAINT AND REASON FOR VISIT | ReasonForVisit | Clinical Notes | Section name only |
| LAB RESULTS | Results | Lab Results | Section name only |
| SOCIAL HISTORY | SocialHistory | Social History | Section name only |
| VITAL SIGNS | Vital | Vitals | Section name only |

The OpenAPI PDF's `GetPatientData` endpoint exposes 13 additional toggleable sections beyond the core 20 (including PatientContact, Pregnancy, CareTeam, CarePlan, ReasonForReferral, PlannedMedication, PlannedAppointments, PlannedProcedure, EncompassingEncounter, ClinicInformation, FunctionStatus, FunctionalStatus, PatientAll). These are not mentioned in the EHI export document and appear to be API features for g(7)/g(9) use rather than documented (b)(10) export content.

**Key statistics:**
- Total entities: 20 C-CDA sections (the only documented export content)
- Total fields: 0 documented (no field-level detail exists)
- Fields with descriptions: 0
- Data types documented: No
- Value sets documented: No
- Relationships documented: No
- Sample data: None

The complete entity inventory is in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor defines the export exclusively as 20 C-CDA sections. These map to standard clinical data classes in USCDI v1 — demographics (implicit in CDA header), problems, medications, allergies, immunizations, vitals, lab results, procedures, encounters, notes, and a few additional clinical categories. The "Insurance Providers" (Payer) section captures payer identity but not billing transactions.

The vendor provides no categorization or grouping of these sections. They are presented as a flat list. There is no differentiation between "deep" and "thin" coverage areas because there is no field-level detail for any section.

The export scope is essentially identical to what a g(10) Standardized FHIR API would provide — USCDI clinical data classes. The EHI document even explicitly references g(10) as the FHIR alternative, reinforcing that the (b)(10) export is scoped to the same USCDI data as the interoperability APIs.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Implicit in C-CDA patient header; no dedicated section. OpenAPI PDF has `PatientContact` toggle but not in EHI doc. | C-CDA header carries basic demographics but OmniMD stores richer patient data (insurance eligibility, portal accounts, digital check-in data) |
| Encounters / visits | ✅ Covered | ENCOUNTERS section | Section name only; no detail on encounter types or depth |
| Problems / conditions | ✅ Covered | PROBLEM LIST section | Section name only |
| Medications / prescriptions | ⚠️ Partial | HISTORY OF MEDICATION and MEDICATION ADMINISTERED sections | Covers medication history but likely misses EPCS prescribing records, pharmacy transaction logs, medication reconciliation details. OmniMD is SureScripts/EPCS-certified. |
| Allergies | ✅ Covered | ALLERGIES, ADVERSE REACTIONS, ALERTS section | Section name only |
| Immunizations | ✅ Covered | IMMUNIZATIONS section | Section name only |
| Vitals | ✅ Covered | VITAL SIGNS section | Section name only |
| Lab results | ✅ Covered | LAB RESULTS section | Section name only; unclear if full structured lab data or summary |
| Imaging / diagnostic reports | ❌ Not covered | No radiology/imaging section in export | OmniMD integrates with RIS; imaging reports and orders not addressed |
| Procedures | ✅ Covered | PROCEDURES section | Section name only |
| Clinical notes / documents | ⚠️ Partial | PROGRESS NOTE, ASSESSMENTS, CHIEF COMPLAINT AND REASON FOR VISIT sections | Standard C-CDA note sections included, but specialty-specific templates (40+ specialties), custom forms, AI-generated documentation (AI Scribe, AI Clinician) likely not captured in standard C-CDA |
| Care plans / goals | ✅ Covered | TREATMENT PLAN section | Section name only |
| Orders / referrals | ❌ Not covered | No order or referral section in EHI doc. OpenAPI PDF has `ReasonForReferral` toggle but not in EHI export scope. | OmniMD supports referral tracking; this is a gap |
| Insurance / coverage | ⚠️ Partial | INSURANCE PROVIDERS section (Payer) | Captures payer identity only; does not include eligibility verification results, insurance plan details, or enrollment data |
| Claims / billing | ❌ Not covered | No billing/claims entities in export | **Significant gap.** OmniMD has built-in billing, RCM, claim scrubbing, denial management, revenue analytics. None of this data is in the export. |
| Payments | ❌ Not covered | No payment entities in export | OmniMD processes payments through portal and billing; not exported |
| Consents / directives | ✅ Covered | ADVANCE DIRECTIVES section | Section name only |
| Patient communications / portal messages | ❌ Not covered | No messaging/communication entities | OmniMD has patient portal with secure messaging; not exported |
| Telehealth records | ❌ Not covered | No telehealth entities | OmniMD offers integrated telehealth with video visits; not exported |
| Remote patient monitoring | ❌ Not covered | No RPM entities | OmniMD offers RPM for chronic conditions; not exported |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities | OmniMD claims 40+ specialty templates; none of this specialty-specific assessment or clinical data is distinctly addressed in the C-CDA export |

**Coverage summary**: 8 of 20 applicable domains are covered, 4 are partially covered, 8 are not covered at all. The covered domains are exclusively standard clinical data classes that map to USCDI/C-CDA — the exact same data that would be available through the g(10) FHIR API.

## 6. Documentation Quality

The EHI export documentation is among the thinnest possible. Key deficiencies:

- **No data dictionary**: The entire export documentation is a 211-word, 2-page Word document listing 20 C-CDA section names. There is zero field-level documentation.
- **No schema or structure definition**: The document defers to the HL7 C-CDA specification for format details. A developer would need to independently reference the C-CDA standard to understand what fields might appear in each section.
- **No sample data**: No example C-CDA documents, no example API responses with clinical content, no sample exports.
- **No vendor-specific documentation**: No description of how OmniMD populates each section, what coded values it uses, what OmniMD-specific data might appear in vendor extensions, or how data from OmniMD's 40+ specialty templates maps to C-CDA sections.
- **No machine-readable artifacts**: No JSON schema, no XML schema beyond the C-CDA standard reference, no data dictionary in any parseable format.
- **Could a developer build an import?**: No. A developer would know the export is C-CDA XML, but would have no OmniMD-specific guidance on what to expect in each section, what coding systems are used, or how to handle vendor-specific content.

The OpenAPI PDF (9 pages, for g(7)/g(9)) provides more detail than the EHI export document — it documents API parameters, authentication, and the toggleable C-CDA sections — but it explicitly serves a different certification criterion and does not describe the (b)(10) export.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The export is entirely a C-CDA patient summary (with a reference to FHIR Bulk Data via g(10)). It covers USCDI v1 clinical data classes but does not export OmniMD's native data model. Billing, claims, specialty-specific assessments, patient portal data, telehealth records, RPM data, and AI-generated documentation are all absent. The export scope is indistinguishable from what the g(10) API provides.

### Key Findings

1. **The (b)(10) export is functionally identical to the g(10) FHIR/C-CDA API output.** The EHI export document lists 20 C-CDA sections that map precisely to USCDI v1 data classes, and explicitly references g(10) for the FHIR alternative. This is a textbook case of repackaging existing interoperability capabilities as "(b)(10)" — the exact failure mode the regulation was designed to prevent.

2. **Billing and RCM data is entirely absent despite being a core product capability.** OmniMD offers built-in medical billing, claim scrubbing, denial management, and revenue analytics. No billing, claims, payment, or RCM data appears in the export. This is the single largest gap given that billing records are explicitly part of the HIPAA designated record set.

3. **No data dictionary exists.** The EHI export documentation is a 211-word Word document listing 20 section names with no field-level detail, no types, no value sets, no relationships, and no sample data. The document was authored by the developer's contact person (Dr. Purohit), revised 5 times over ~7 weeks (2023-07-24 to 2023-09-11), and totals 44 minutes of editing time per Word metadata.

4. **Specialty-specific data for 40+ specialties is not addressed.** OmniMD's marketing emphasizes specialty-specific templates and workflows across 40+ medical specialties. Standard C-CDA sections cannot capture this specialty-specific structured data. None of it is mentioned in the export.

5. **Patient-facing digital health data (portal, telehealth, RPM) is absent.** OmniMD offers patient portal messaging, telehealth video visits, and remote patient monitoring — all generating patient-specific health data. None appear in the export.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML (CDA 2.1), FHIR R4 (by reference to g(10))
Model type:      Standard projection (C-CDA/USCDI v1)
Entities:        20 C-CDA sections (no native tables)
Fields:          N/A (no field-level documentation)
Descriptions:    N/A (section names only)
Sample data:     No
Bulk export:     Yes (claimed for both C-CDA and FHIR)
Domains covered: 8 of 20 applicable domains (4 partial)
```

### Bottom Line

The OmniMD EHI export is a C-CDA clinical summary repackaged as a (b)(10) export, covering only the USCDI clinical data that was already available through g(10). A patient or provider would not receive a complete copy of their data — billing records, specialty assessments, portal communications, telehealth records, and RPM data would all be missing. The documentation is among the thinnest possible: 20 section names in a 211-word document with no data dictionary, no schema, and no sample data.
