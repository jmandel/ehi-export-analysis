# EHI Export Analysis: VisionWeb

**Product**: Uprise 3.1
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2514.Upri.31.01.1.221213 (CHPL ID 11069)

## 1. Product Context

Uprise is a **cloud-based, all-in-one practice management and EHR system** built specifically for **optometry/eye care practices**, developed by VisionWeb (now part of EssilorLuxottica's HELIX division). It targets independent optometry practices from solo ODs to multi-location groups. The product is described as "Ambulatory (Optometry)" in its CHPL listing.

Uprise stores data across these domains relevant to EHI completeness:

- **Clinical/EHR**: Eye exams with SmartTouch charting, annotations, diagnoses (ICD-10), clinical decision support, pre-testing device integration, contact lens fitting, review of systems, physical exam, vital signs, allergies, immunizations, medications, care plans, goals, clinical notes, patient education
- **Optometry-specific clinical**: Refractions (manifest, cycloplegic, autorefraction, retinoscopy, wavefront), spectacle and contact lens prescriptions with sphere/cylinder/axis/prism/base curve/diameter, keratometry, intraocular pressures, binocular vision, dilation procedures
- **E-prescribing**: Medication prescriptions via NewCrop/Surescripts
- **Practice management**: Scheduling, patient demographics, intake forms, patient portal (digital questionnaires, messaging)
- **Optical dispensing & ordering**: Frame catalogs, lens ordering to 400+ labs/suppliers, inventory management, order tracking
- **Billing & claims**: Claims management (CMS-1500), insurance processing (vision and medical), CodeSAFE code verification, invoicing, payments
- **Insurance**: Policy management, benefits, electronic eligibility verification
- **Patient portal**: Secure messaging, intake forms, exam history, online scheduling

This is the baseline for "what should the export cover."

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Data_Export.pdf` | 58-page data dictionary PDF (879,710 bytes). Created 2024-02-20 by Philip Lu via Microsoft Word for Microsoft 365. Documents 81 CSV files with field names and descriptions for each. | **Primary artifact** — contains the entire data dictionary |
| `downloads/data-export-page.html` | HTML source of the ScreenSteps documentation page (35,826 bytes). Contains a brief paragraph about ONC §170.315(b)(10) and a download link for the PDF. | **Low** — just a wrapper for the PDF download |
| `downloads/screenshot-data-export-page.png` | Browser screenshot (155,411 bytes) of the live page confirming layout: breadcrumb (Uprise Support > MIPS Guide > Electronic Health Information (EHI) Export > Data Export), introductory paragraph, PDF download link. Page last updated Apr 09, 2024. | **Confirmatory** — verifies the page is publicly accessible and correctly structured |

The PDF is the sole substantive artifact. There are no sample data files, no machine-readable schemas, no FHIR/C-CDA resources, and no additional documentation pages.

## 3. Export Mechanics

- **Format**: CSV files bundled in a .zip archive. Additionally includes images and .xml data files referenced by the CSVs.
- **Mechanism**: Accessed via the **"Patient Export" section in Practice Management** (per the PDF's introductory text). This is a UI-based export.
- **Single-patient vs bulk**: The documentation page references both "single and patient population EHI" export, consistent with (b)(10) requirements.
- **Access constraints**: The mandatory disclosures page states "there are no technical or contractual considerations to use our certified product (Uprise 3.1)" and "no additional one-time or ongoing costs."

## 4. Export Content: What's In It

The export is documented through a 58-page PDF data dictionary covering **81 CSV files** with a total of **2,079 fields**. Virtually all fields (2,077 of 2,079, or 99.9%) have descriptions, though many descriptions are simple CamelCase expansions of the field name (e.g., `ClinicalStatus` → "Clinical status"). Approximately 57% of descriptions add semantic content beyond the field name; the remaining 43% are mechanical expansions.

The PDF provides field names and brief descriptions in a two-column format (Data | Notes) for each CSV. It does **not** provide:
- Data types (string, number, date, boolean)
- Date/time format specifications
- Value set enumerations for coded fields
- Cardinality (required vs optional)
- Formal relationships between CSV files (no ERD, no foreign key documentation)
- Sample data or example export files
- Machine-readable schema (JSON Schema, XSD, etc.)

Each entity includes audit trail fields (CreatedDate, CreatedBy, ModifiedDate, ModifiedBy) — 254 audit fields total across all 81 entities. Cross-references use identifiers (Patient chart number, EncounterID, ClaimID, InvoiceID, PolicyID, PrescriptionID) that appear across CSV files, making the relational structure inferable but not formally documented.

### Vendor's own content organization

The PDF does not organize entities into named categories — it lists all 81 CSV files alphabetically. The categorization below is mine, based on entity naming patterns. The full inventory is in `analysis/full-entity-inventory.json`.

**Category breakdown:**

| Category | Entities | Fields | Notes |
|---|---|---|---|
| Optometry-Specific | 11 | 749 | Largest category; includes refraction types, prescriptions, and optical orders |
| Clinical | 23 | 422 | General clinical data: allergies, conditions, procedures, medications, imaging |
| Billing & Financial | 12 | 326 | Claims (CMS-1500), invoices, payments, adjustments |
| Patient Demographics & Admin | 15 | 208 | Patient profiles, contacts, preferences, questionnaires |
| Insurance & Benefits | 5 | 111 | Policies, benefits, electronic/manual coverage |
| Observations | 8 | 95 | Vitals, lab results, physical exam, review of systems, lifestyle, PFSH |
| Scheduling & Encounters | 4 | 85 | Appointments, encounters, recall |
| Reference / Administrative | 3 | 83 | Locations, providers, products |

**Top 15 largest entities (representative examples):**

| Entity | Fields | Category |
|---|---|---|
| RxOrder.csv | 176 | Optometry-Specific |
| Prescription.csv | 151 | Optometry-Specific |
| RefractionContactLensRx.csv | 142 | Optometry-Specific |
| Claim.csv | 136 | Billing & Financial |
| RefractionSpectacleRx.csv | 58 | Optometry-Specific |
| Product.csv | 43 | Reference / Administrative |
| RefractionManifest.csv | 42 | Optometry-Specific |
| BenefitCoverageManual.csv | 40 | Insurance & Benefits |
| InvoiceLine.csv | 40 | Billing & Financial |
| RefractionAutorefraction.csv | 40 | Optometry-Specific |
| RefractionCyclopegic.csv | 40 | Optometry-Specific |
| RefractionRetinoscopy.csv | 40 | Optometry-Specific |
| RefractionWavefront.csv | 40 | Optometry-Specific |
| Patient.csv | 39 | Patient Demographics & Admin |
| ConditionChiefComplaint.csv | 31 | Clinical |

**Notable observations:**
- The optometry-specific entities dominate the export: 11 entities with 749 fields (36% of all fields). RxOrder alone has 176 fields covering frame specs, lens measurements, trace data, keratometry, contact lens parameters, pricing, and shipping.
- Claim.csv has 136 fields mapping to CMS-1500 form fields (billing provider, referring provider, accident info, disability dates, prior auth, etc.) — this is genuine billing depth, not a summary.
- Seven distinct refraction types are documented (autorefraction, contact lens Rx, cycloplegic, manifest, retinoscopy, spectacle Rx, wavefront), each with 40+ fields — comprehensive optometric exam capture.
- Two entity names contain typos in the PDF: `InvoiceLIneAdjustment.csv` and `InvoiceLIneDiagnosis.csv` (capital I in "LIne") — these are billing entities covering adjustments/write-offs and invoice-level diagnosis codes.
- No entities have zero field descriptions; all 81 entities have at least brief descriptions for every field.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers the following data domains, organized by richness:

**Deepest coverage — Optometry-specific clinical data (749 fields):**
The standout strength. Seven refraction types (autorefraction, contact lens Rx, cycloplegic, manifest, retinoscopy, spectacle Rx, wavefront), comprehensive optical prescriptions with sphere/cylinder/axis/prism/base curve/diameter for each eye, keratometry, intraocular pressures, binocular vision, dilation procedures with medications. The RxOrder entity (176 fields) captures the full optical ordering lifecycle: frame specs, lens measurements, trace data, contact lens parameters, pricing, lab instructions, and shipping. This is specialty clinical data that would be lost in a FHIR/C-CDA projection.

**Strong coverage — Billing & Financial (326 fields):**
Twelve entities covering claims (with CMS-1500 box-level detail), claim lines, claim diagnosis codes, claim status tracking, invoices, invoice line items, adjustments/write-offs, payments, and payment application details. The Claim entity alone has 136 fields including billing/rendering/referring provider details, NPI numbers, insurance policy references, accident and disability information, prior authorization, and submission tracking.

**Strong coverage — General Clinical (422 fields):**
Twenty-three entities covering allergies (with reaction substances, severity, manifestations), conditions/diagnoses (ICD codes, body sites, chief complaints, concerns, functional/cognitive status), medications, immunizations (with lot numbers, routes, VFC categories), procedures (with optometry-specific variants for dilation, IOPs, screening), clinical impressions, care plans, goals, images, documents, devices (UDI), service requests (with LOINC codes), and tasks.

**Adequate coverage — Patient Demographics (208 fields):**
Fifteen entities covering patient profiles (demographics, SOGI data, race/ethnicity, employment), addresses, phone numbers, emails, alerts, notes, document references, preferences, linked accounts, payment cards, contacts, and questionnaire responses.

**Adequate coverage — Insurance & Benefits (111 fields):**
Five entities covering policies (with member IDs, payer plans), benefits (with classifications), electronic eligibility/coverage responses (~30 fields), manual benefit coverage entries (with enhancements, frequency, allowances), and policy notes.

**Adequate coverage — Observations (95 fields):**
Eight entities covering vitals, lab results (with codes, values, units, reference ranges), physical exam, review of systems, lifestyle observations, past/family/social history (PFSH), keratometry, and binocular vision.

**Basic coverage — Scheduling & Encounters (85 fields):**
Four entities covering appointments, encounters (with class, service type, participants, recall info), encounter-level procedures with diagnoses, and patient recall.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient.csv` (39 fields), `PatientAddress.csv` (12), `PatientPhoneNumber.csv` (12), `PatientEmail.csv` (8), `Contact.csv` (25), plus 8 more patient entities | Thorough — includes SOGI, race/ethnicity, employment, preferences, emergency contacts |
| Encounters / visits | ✅ Covered | `Encounter.csv` (28 fields), `EncounterProceduresDiagnosis.csv` (26) | Good depth with service type, participants, recall info |
| Problems / conditions | ✅ Covered | `Condition.csv` (26), `ConditionChiefComplaint.csv` (31), `ConditionConcern.csv` (13), `ConditionFunctionalCognitive.csv` (16) | Thorough — ICD codes, body sites, severity, multiple condition subtypes |
| Medications / prescriptions | ✅ Covered | `MedicationRequest.csv` (21 fields) for pharmaceutical Rx; `Prescription.csv` (151) for optical Rx | Pharmaceutical Rx adequate; optical Rx extraordinarily detailed |
| Allergies | ✅ Covered | `AllergyIntolerance.csv` (24 fields) | Includes reaction substances, manifestations, severity, code systems |
| Immunizations | ✅ Covered | `Immunizations.csv` (30 fields) | Includes lot numbers, routes, sites, manufacturers, VFC category |
| Vitals | ✅ Covered | `ObservationVitals.csv` (10 fields) | Basic — code, value, unit, date |
| Lab results | ✅ Covered | `ObservationLabResults.csv` (23 fields) | Includes codes, values, units, reference ranges, interpretation |
| Imaging / diagnostic reports | ✅ Covered | `Images.csv` (28 fields), `PatientDocumentReference.csv` (9), `DocumentReference.csv` (5) | Images referenced with body sites, OD/OS laterality; actual image files included in ZIP |
| Procedures | ✅ Covered | `Procedure.csv` (30), `ProcedureDilation.csv` (29), `ProcedureIOPs.csv` (13), `ProcedureIOPsTargets.csv` (13), `ProcedureOther.csv` (18), `ProcedureScreening.csv` (18) | Thorough — includes optometry-specific procedures (dilation with medications, IOPs) |
| Clinical notes / documents | ✅ Covered | `ClinicalImpression.csv` (10 fields — assessment, general, medication notes), `PatientNote.csv` (7) | Present but somewhat thin — only 10 fields for clinical impressions |
| Care plans / goals | ✅ Covered | `CarePlan.csv` (11), `Goal.csv` (14) | Adequate |
| Orders / referrals | ✅ Covered | `RxOrder.csv` (176), `ServiceRequest.csv` (20) | Optical orders are extraordinarily detailed; service requests include LOINC codes. No dedicated referral entity, but ServiceRequest may cover this |
| Insurance / coverage | ✅ Covered | `Policy.csv` (20), `Benefit.csv` (13), `BenefitCoverageElectronic.csv` (29), `BenefitCoverageManual.csv` (40), `PolicyNote.csv` (9) | Thorough — both electronic eligibility and manual benefit entries |
| Claims / billing | ✅ Covered | `Claim.csv` (136), `ClaimLine.csv` (31), `ClaimDiagnosis.csv` (4), `ClaimLineCodes.csv` (23), `ClaimNote.csv` (7), `ClaimStatus.csv` (15) | Thorough — CMS-1500 box-level granularity |
| Payments | ✅ Covered | `Payment.csv` (17), `PaymentItem.csv` (13), `Invoice.csv` (13), `InvoiceLine.csv` (40), `InvoiceLIneAdjustment.csv` (21) | Good — covers payments, invoices, adjustments/write-offs |
| Patient communications / portal messages | ⚠️ Partial | `CommunicationEducation.csv` (13) covers patient education records; `PatientNote.csv` (7) may capture some messaging | No dedicated entity for patient-provider secure messaging or portal communications. Product has a patient portal with messaging; this appears to be a gap |
| Specialty-specific (Optometry) | ✅ Covered | 11 entities with 749 fields: 7 refraction types, prescriptions (spectacle + contact lens), RxOrder, prescription add-ons | Exceptionally thorough — this is the export's greatest strength |
| Consents / directives | ⚠️ Partial | `Patient.csv` includes `HipaaSignedDate` and `FinancialResponsibilitySignedDate` | Only consent dates, not full consent/directive documents |
| Patient education | ✅ Covered | `CommunicationEducation.csv` (13 fields) | Adequate |

**Gap summary**: 16 of 18 applicable domains are covered or substantially covered. The two partial areas (patient portal messaging and consents) are minor gaps. There is no evidence of any major data domain being entirely absent from the export. The product's core optometry, clinical, billing, and insurance data are all present with significant depth.

## 6. Documentation Quality

**Strengths:**
- Every field in every CSV has a description (2,077 of 2,079, 99.9%)
- The 58-page PDF is well-structured with consistent formatting per entity
- The documentation is publicly accessible without authentication
- Field naming conventions are descriptive and consistent (e.g., the Code/CodeDisplay/CodeSystem pattern for coded fields; the L/R suffix convention for lateralized optometry data)

**Weaknesses:**
- ~43% of field descriptions are mechanical CamelCase expansions that add no information beyond the field name itself (e.g., `RecordedDate` → "Recorded date")
- No data types specified anywhere — developers must guess whether a field is a string, number, date, or boolean
- No date/time format specification (ISO 8601? MM/DD/YYYY?)
- No value set documentation for coded fields (e.g., what are the valid values for "Status", "Classification", "Category"?)
- No cardinality information (required vs optional fields)
- No formal relationship documentation — cross-entity references use shared identifiers (Patient chart number, EncounterID, ClaimID) but there is no ERD or foreign key specification
- No sample data or example export files
- No machine-readable schema (JSON Schema, XSD, CSV-W, etc.)

**Developer usability**: A developer could understand the general structure and build a basic import, but would need actual export files to determine data types, date formats, coded value sets, cardinality, and relationship semantics. The documentation is sufficient for orientation but insufficient for building a robust import without access to sample data.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native data model export covering 81 CSV entities with 2,079 fields across clinical, optometry-specific, billing, insurance, scheduling, and administrative domains. It is not a C-CDA or FHIR projection — the entity naming shows FHIR-influenced conventions (AllergyIntolerance, MedicationRequest, Condition) but the content is the vendor's own database model with extensive optometry-specific structures (7 refraction types, 176-field optical orders) that no standard format could represent.

### Key Findings

1. **Exceptionally deep optometry-specific clinical data**: 11 entities with 749 fields covering 7 refraction types, optical prescriptions (spectacle and contact lens with per-eye sphere/cylinder/axis/prism/base curve/diameter), keratometry, IOPs, dilation procedures, and optical orders (176 fields each). This is exactly the specialty data that distinguishes a real (b)(10) export from a repackaged clinical summary.

2. **Genuine billing depth**: Claim.csv alone has 136 fields mapping to CMS-1500 form elements (billing/rendering/referring provider, NPI, accident info, disability dates, prior auth). Combined with 11 additional billing/invoice/payment entities totaling 326 fields, this is not a billing stub.

3. **81 entities, not 76**: The prior report counted 76 CSV files; verified count from the PDF text is 81 distinct CSV files with 2,079 total fields. All entities have field descriptions.

4. **Documentation quality is functional but not developer-ready**: While 99.9% of fields have descriptions, ~43% are mere CamelCase expansions. No data types, value sets, cardinality, relationships, or sample data are provided. A developer could orient themselves but not build a reliable import from documentation alone.

5. **Minor gap in patient communications**: Despite the product offering a patient portal with messaging, there is no dedicated CSV for patient-provider messages. This is the only notable domain gap.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV files in ZIP archive (with images and XML)
Model type:      Native database (FHIR-influenced naming)
Entities:        81
Fields:          2,079
Descriptions:    99.9% of fields have descriptions (~57% add semantic content beyond field name)
Sample data:     No
Bulk export:     Yes (single-patient and population)
Domains covered: 16 of 18 applicable domains (2 partial)
```

### Bottom Line

Uprise provides one of the more thorough (b)(10) implementations. A patient or provider would get a comprehensive, usable copy of their data covering clinical exams, optometry-specific measurements, billing/claims, insurance, and more across 81 CSV files. The single biggest strength is the extraordinary depth of optometry-specific clinical data (749 fields across 11 entities) that would be lost in any standard-format projection. The biggest weakness is the lack of sample data and formal schema documentation, which would make programmatic consumption require significant trial-and-error effort.
