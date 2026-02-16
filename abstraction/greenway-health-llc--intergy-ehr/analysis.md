# EHI Export Analysis: Greenway Health, LLC

**Product**: Intergy EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2913.Inte.21.05.0.231003 (v21), 15.04.04.2913.Inte.22.06.0.250814 (v22)

## 1. Product Context

Intergy EHR is a cloud-based (AWS-hosted) integrated Electronic Health Record and Practice Management platform by Greenway Health, LLC, serving 10,000+ organizations and 55,000+ providers across 40+ medical specialties. It focuses on ambulatory healthcare — solo practices through large multi-specialty groups, with strength in primary care, OB-GYN, orthopedics, pediatrics, FQHCs, and tribal health.

**Key data domains the product stores** (per vendor materials):
- **Clinical**: charting with 500+ templates, problem lists, medications (e-Rx, EPCS, PDMP), allergies, vitals, lab orders/results, imaging orders, immunizations, clinical decision support, encounter findings (MEDCIN-based), care plans, advance directives, clinical documents, implantable devices
- **Billing/Revenue Cycle**: comprehensive claims management, charge posting, claim scrubbing, accounts receivable, adjustments, payments, clearinghouse integration, superbills/statements
- **Insurance**: eligibility verification, coverage, prior authorizations, remittance/EOBs
- **Practice Management**: scheduling, appointments, multi-location support, resource management
- **Patient Engagement**: patient portal (messages, refill requests, bill pay), secure messaging
- **Specialty**: OB/GYN (prenatal, labor/delivery, birth records), cardiology device orders/results, radiology (RIS studies), workers' compensation
- **Referrals**: referral workflows with treatment plans and results
- **Documents**: scanning, indexing (Document Manager), transcription management (TMSCatalog)
- **Interoperability**: C-CDA exchange, FHIR API, CommonWell, Direct messaging

This is a full-featured ambulatory EHR+PM platform, so a (b)(10) export should cover clinical, billing, insurance, specialty, and administrative patient data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/IntergyEHIExport.html` (9 KB) | Main EHI export documentation page describing Single Patient and Patient Population export modes, export package structure (Documents, Images, Tables folders), MEDCIN-to-SNOMED mappings | **High** — establishes export mechanics |
| `downloads/viewer/Contracts/*.htm` (261 files, ~1.9 MB total) | Individual HTML table definition pages — one per database table, each with field names, data types, defaults, null options, comments, parent/child relationships | **Very high** — this IS the data dictionary |
| `downloads/viewer/Contracts/include/DBDescriptions.js` (28 KB) | JavaScript file containing 261 table names and descriptions | **High** — table-level metadata |
| `downloads/viewer/index.html` (1.2 KB) | Data Tables viewer frameset | Low — navigation only |
| `downloads/viewer/Contracts/DBTOC.htm` (1.2 KB) | Table of contents page for viewer | Low — navigation only |
| `downloads/home-default.htm` (3.5 KB) | Greenway EHI hub page linking Intergy and PrimeSuite | Low — context only |
| `downloads/screenshot-main-page.png` (936 KB) | Screenshot of main documentation page | Low — visual confirmation |
| `downloads/screenshot-data-tables-viewer.png` (236 KB) | Screenshot of data tables viewer | Low — visual confirmation |
| `downloads/assets/tmscatalogblob.jpg` (186 KB) | Screenshot showing TMSCatalogBlob folder structure | Medium — explains document export structure |
| `downloads/assets/ehistyle.css` (14 KB) | Stylesheet | None |
| `downloads/enrichment/tables.json` (1.4 MB) | Prior agent's structured parse of data dictionary | Used for reference/cross-check only |

## 3. Export Mechanics

**Format**: CSV files for tabular data, with documents (RTF/PDF/DOC as ZIP files) and images (TIF, video clips, with XML annotation files) in separate folders.

**Mechanism**: Built-in export feature within Intergy, minimum version 21.24.00.00. The export is initiated from within the application (UI-driven). Documentation describes the export package structure clearly.

**Two modes**:
1. **Single Patient Export**: Exports one patient's data with three folders:
   - `Documents/` — clinical documents (GenFile JPEGs, TMSCatalog ZIPs containing RTF/PDF/DOC)
   - `Images/` — patient images (X-rays, scanned documents, diagnostic imaging) in TIF and video formats, with XML annotation files (.ann, base64-encoded)
   - `Tables/` — CSV files for each database table
2. **Patient Population Export**: Bulk export of all patients with:
   - `Documents/` — all documents including GenFileBlob, TMSCatalogBlob, PracPersonSecureMsgBlob folders (capped at 10,000 docs per folder)
   - `Images/` — all images in TAR format (5GB per tar), with ImageIndexFile.csv for path lookup
   - `Tables/` — all CSV tables
   - `Bulk Export Status` — CSV showing success/failure per table/document/image

**Access constraints**: No fees mentioned. Requires Intergy v21.24+. Both single-patient and bulk population export are supported.

## 4. Export Content: What's In It

### Data Dictionary Overview

The export is documented with a comprehensive, interactive HTML data dictionary covering **261 database tables** with **4,529 fields** total. The data dictionary includes:

- **Field names**: all 4,529 fields named ✅
- **Data types**: all fields have types (INTEGER, CHARACTER(n), DECIMAL(n,n), DATE, etc.) ✅
- **Null options**: all fields marked MANDATORY or OPTIONAL ✅
- **Default values**: documented where applicable ✅
- **Field descriptions/comments**: 4,053 of 4,529 fields (89%) have meaningful descriptions beyond just a name ✅
- **Relationships**: 1,052 parent/child table relationships with join conditions and cascade/restrict behavior ✅
- **Table descriptions**: 232 of 261 tables (89%) have descriptions ✅
- **Value sets**: many fields document valid values inline (e.g., Charge.CurrentStatus documents codes G, GT, GA, I, IU, IT, IF; Charge.RecordStatus documents O, S, V, P) ✅
- **Version info**: all tables stamped "Intergy Version: 22.00.00.00", last updated 9/24/2025

This is a native database schema export — the CSV files mirror Intergy's internal database tables directly.

### Vendor's Own Content Organization

The data dictionary doesn't use vendor-defined categories; tables are presented as a flat alphabetical list. I've categorized them based on table names and descriptions. The full inventory is in `analysis/entity-inventory-full.json` (261 tables, 4,529 fields). Below is a breakdown by domain:

| Category | Tables | Fields | Representative Tables |
|---|---|---|---|
| Insurance Claims | 15 | 360 | PlanClaimData (110), PlanClaimLineItemData (41), PlanClaimCharge (31), PlanClaimChargeRemit (30) |
| Demographics/Person | 23 | 359 | Patient (80), Person (45), PersonHistory (23), PersonAllergyHistory (20) |
| Laboratory | 17 | 341 | LabOrder (70), LabOrderTest (43), Lab (43), LabOrderTestResult (22) |
| Medications/Prescriptions | 19 | 325 | PatientRx (66), RxEligRequest (24), RxEligPBMRespEB (23), DURAlert (22) |
| OB/GYN | 12 | 284 | OBPregnancy (48), OBUltraSound (44), OBBirth (37), OBInitialVisit (36) |
| Insurance/Coverage | 12 | 253 | Eligibility (45), EligibilityBenefit (42), Policy (38), PolicyMember (28) |
| Accounts/Financial | 8 | 228 | AccountStatement (61), AccountStatementItem (40), Account (28), AccountBill (25) |
| Encounters/Clinical | 9 | 220 | Encounter (61), EncounterFinding (51), EncounterFindingHistory (48) |
| Organization/Staff | 12 | 188 | Staff (33), Provider (33), Entity (28), MMUser (22) |
| Billing/Charges | 13 | 178 | Charge (45), ChargeActivity (25), ChargeCoverage (16) |
| Care Plans | 12 | 153 | PatientCPGoalIntervention (20), PatientCPGoal (19), PatientCPHealthConcern (18) |
| Referrals | 12 | 148 | Referral (32), ReferralTreatmentResult (21), ReferralTreatmentPlan (14) |
| Documents | 9 | 142 | TMSCatalog (54), Document (22), GenFile (17) |
| Problems/Conditions | 7 | 133 | Ailment (34), PatientProblem (31), AilmentDiagnosis (17) |
| Clinical Findings | 6 | 124 | ClinicalCustomFinding (31), MedcinFinding (30), ImportEncFinding (26) |
| Immunizations | 5 | 120 | PatientVacDose (38), Vaccine (30), PatientVacDoseAction (24) |
| Orders | 8 | 115 | PatientOMOrderLineItem (28), PatientOrderSet (22), PatientOMOrderSet (12) |
| Appointments/Scheduling | 6 | 95 | Appointment (35), ApptRecall (16), RecallNotice (14) |
| Payments | 7 | 95 | Payment (26), PaymentAssignment (18), PaymentReversal (14) |
| Procedures/Diagnosis | 4 | 87 | ProcedureEvent (28), Procedure (26), Diagnosis (22) |
| Allergies | 5 | 77 | PersonAllergy (22), Allergy (17), PersonAllergyReaction (14) |
| Imaging/Radiology | 4 | 76 | RISStudy (45), RISVisit (16) |
| Consent/PHI | 5 | 67 | PHIAuthorization (20), PHIDisclosure (15), PHIConsent (13) |
| Reference/Lookup | 5 | 61 | ExtAttributeCode (16), EAObjectData (15), LookupCode (12) |
| Cardiology | 4 | 54 | CardioOrder (20), CardioOrderComponent (14), CardioComponent (11) |
| Communications/Contact | 4 | 39 | Email (12), Phone (12) |
| Vitals | 3 | 38 | EncounterVitalSet (15), EncounterVital (14), VitalType (9) |
| Implantable Devices | 2 | 36 | PatImplantableDevice (22), PatImplantableDeviceActivity (14) |
| Patient Programs | 3 | 35 | PatientRSRInfo (17) — Ryan White/FQHC specific |
| Advance Directives | 2 | 27 | AdvanceDirective (16), AdvanceDirectiveActivity (11) |
| Universal Billing Codes | 3 | 24 | UBConditionCode, UBOccurrenceCode, UBSpanCode |
| Prior Authorization | 2 | 17 | PriorAuthInfo (11), PriorAuthInfoResponse (6) |
| Care Team | 1 | 11 | CareTeamMember |
| Questionnaires | 1 | 11 | Questionnaire |
| Patient Portal | 1 | 8 | PatientPortalAccess |

### Notable Details

- **PlanClaimData** is the largest table at 110 fields — a deeply detailed claims data structure covering rendering provider, facility, billing codes, authorization info, ambulance details, and more
- **Patient** table has 80 fields including demographics, clinical preferences, consent flags, and program enrollment
- **EncounterFinding** (51 fields) captures clinical findings using the MEDCIN system with detailed attributes (severity, duration, onset, character, location, modifiers)
- **OB/GYN** module is extensive (12 tables, 284 fields) — covers pregnancy, prenatal visits, ultrasounds, birth records, postpartum
- **Secure messaging** is included: `PracPersonSecureMessage` and `PracPersonSecureMsgBlob` tables
- **Workers' Compensation**: 3 dedicated tables (WorkersComp, WorkersCompDiagnosis, WorkersCompProcedure)
- **MEDCIN-to-SNOMED mapping** for smoking status and pregnancy findings is documented on the main page with explicit code crosswalks

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export presents a native database dump of Intergy's relational schema. The coverage is remarkably broad:

**Richest domains** (most tables and fields):
- **Insurance Claims** (15 tables, 360 fields): Deep claims lifecycle — PlanClaimData alone has 110 fields covering every aspect of claim submission, status, and remittance
- **Demographics** (23 tables, 359 fields): Patient, Person, PersonHistory, addresses, contact methods, race, tribal affiliation, occupation, name history, DOB history, sex history
- **Laboratory** (17 tables, 341 fields): Full lab order lifecycle — ordering, specimens, tests, results, result notes, performing lab, LOINC crossref
- **Medications** (19 tables, 325 fields): Prescriptions, Rx activity history, fill status from pharmacies, DUR alerts, change requests, eligibility/PBM data, Rx notes, drug ineffectiveness
- **OB/GYN** (12 tables, 284 fields): A genuine specialty module — pregnancy, prenatal visits, initial visits with findings, ultrasounds (with fetal data), birth records (with race), postpartum visits

**Moderately deep**:
- **Billing/Charges** (13 tables, 178 fields): Charges, charge activities, claim notes, coverage, copay activity, auxiliary data
- **Care Plans** (12 tables, 153 fields): Goals, interventions, outcomes, health concerns — with history tables for tracking changes
- **Referrals** (12 tables, 148 fields): Full referral workflow with treatment plans, results, modifiers, diagnoses
- **Documents** (9 tables, 142 fields): TMSCatalog (54 fields) for transcription/documents, GenFile for general files, blob storage

**Also present**: Appointments, payments (including reversals and voids), consent/PHI authorization, advance directives, clinical findings, questionnaires, prior authorization, implantable devices, care team, patient portal access, cardiology device orders, radiology studies, workers' comp, universal billing codes, and Ryan White program (FQHC) data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (80 fields), `Person` (45), `PersonHistory`, `PersonRace`, `PersonTribalAffiliation`, `PersonOccupation`, `Address/AddressHistory`, `Phone/PhoneHistory`, `Email/EmailHistory`, `DOBHistory`, `SexHistory`, `PersonName`, `PersonContactMethod`, `PersonRelationship` | Thorough — includes history tracking, tribal affiliation, occupation |
| Encounters / visits | ✅ Covered | `Encounter` (61 fields), `EncounterEvent`, `EncounterDiagnosis`, `EncounterEducation`, `InpatientVisit`, `InpatientVisitNote` | Thorough |
| Problems / conditions | ✅ Covered | `PatientProblem` (31), `PatientProblemHistory`, `PatientProblemCodeLink`, `Ailment` (34), `AilmentDiagnosis`, `AilmentNote`, `AilmentProcedure` | Thorough — includes linked diagnoses and history |
| Medications / prescriptions | ✅ Covered | `PatientRx` (66), `PatientRxActivity`, `PatientRxDenial`, `PatientRxFill`, `PatientRxFillAttribute`, `RxDiagnosis`, `RxNote`, `RxRequest`, `RxChangeRequest`, `DURAlert`, `PersonDrugIneffective` | Very thorough — fills, denials, change requests, DUR alerts |
| Allergies | ✅ Covered | `PersonAllergy` (22), `PersonAllergyHistory`, `PersonAllergyReaction`, `PersonAllergyReactionHist`, `Allergy` | Thorough — includes reaction history |
| Immunizations | ✅ Covered | `PatientVacDose` (38), `PatientVacDoseAction` (24), `PatientVacDoseReaction`, `Vaccine` (30), `VaccineReaction` | Thorough — ordering, administering, refusing, voiding, reactions |
| Vitals | ✅ Covered | `EncounterVital` (14), `EncounterVitalSet` (15), `VitalType` (9) | Adequate |
| Lab results | ✅ Covered | `LabOrder` (70), `LabOrderTest` (43), `LabOrderTestResult` (22), `LabOrderTestResultNote`, `LabOrderTestSpecimen`, `LabPerformingLab`, `LabComponentXref`, `Lab` (43) | Very thorough — 17 tables covering full lifecycle |
| Imaging / diagnostic reports | ✅ Covered | `RISStudy` (45), `RISVisit` (16), `RISStudyNote`, `DocumentInterpretation` | Thorough for radiology; images exported as TIF/video |
| Procedures | ✅ Covered | `ProcedureEvent` (28), `ProcedureEventDiag`, `Procedure` (26) | Adequate |
| Clinical notes / documents | ✅ Covered | `TMSCatalog` (54), `TMSCatalogBlob`, `TMSActivity`, `Document` (22), `DocumentNote`, `DocumentAttributeValue`, `CLWCorrespondence`, `GenFile` (17), `GenFileBlob` | Thorough — transcriptions, documents, general files with blob data |
| Care plans / goals | ✅ Covered | 12 tables: `PatientCarePlan`, `PatientCPGoal`, `PatientCPGoalIntervention`, `PatientCPGoalOutcome`, `PatientCPHealthConcern`, plus history tables | Thorough |
| Orders / referrals | ✅ Covered | Orders: `PatientOMOrderLineItem` (28), `PatientOrderSet` (22), `PatientOMOrderSet`; Referrals: `Referral` (32), `ReferralActivity`, `ReferralDiagnosis`, treatment plans/results (12 referral tables total) | Thorough |
| Insurance / coverage | ✅ Covered | `Policy` (38), `PolicyMember` (28), `Plan` (22), `PlanGroup`, `PlanAltID`, `Carrier`, `Eligibility` (45), `EligibilityBenefit` (42), `EligibilityComment` | Very thorough — includes eligibility verification details |
| Claims / billing | ✅ Covered | `PlanClaimData` (110!), `PlanClaim`, `PlanClaimCharge`, `PlanClaimDiag`, `PlanClaimLineItem`, `PlanClaimLineItemData`, `PlanClaimStatus`, `PlanClaimActivity`, `PlanClaimRemit`, remittance adjustments, remark codes | Exceptionally thorough — 15 claim tables, 360 fields |
| Payments | ✅ Covered | `Payment` (26), `PaymentAssignment` (18), `PaymentNote`, `PaymentReversal`, `PaymentVoid`, `PaymentVoidNote`, `PatientRemitPayment` | Thorough — includes reversals, voids, assignment details |
| Charges | ✅ Covered | `Charge` (45), `ChargeActivity` (25), `ChargeNote`, `ChargeCoverage`, `ChargeAuxData`, `ChargeClaimNote`, `CopayActivity` | Thorough |
| Consents / directives | ✅ Covered | `PHIAuthorization` (20), `PHIConsent` (13), `PHIConsentActivity`, `PHIDisclosure` (15), `PHIDiscActivity`, `AdvanceDirective` (16), `AdvanceDirectiveActivity` | Thorough |
| Patient communications | ✅ Covered | `PracPersonSecureMessage`, `PracPersonSecureMsgBlob` (message content) | Adequate — secure messaging included |
| Specialty: OB/GYN | ✅ Covered | 12 tables: `OBPregnancy` (48), `OBUltraSound` (44), `OBBirth` (37), `OBInitialVisit` (36), `OBPrenatalVisit`, `OBPostpartumVisit`, `OBEncounter`, `OBPatient`, fetus data, birth race | Very thorough |
| Specialty: Cardiology | ✅ Covered | `CardioOrder` (20), `CardioOrderActivity`, `CardioOrderComponent`, `CardioComponent` | Adequate — order/result tracking for cardiology devices |
| Specialty: Workers' Comp | ✅ Covered | `WorkersComp`, `WorkersCompDiagnosis`, `WorkersCompProcedure` | Adequate |
| Questionnaires | ✅ Covered | `Questionnaire` (11), `ApptQuestionnaire` | Present but thin |
| Implantable Devices | ✅ Covered | `PatImplantableDevice` (22), `PatImplantableDeviceActivity` (14) | Adequate |
| Care Team | ✅ Covered | `CareTeamMember` (11) | Present |

**Domains NOT applicable**: Dental, behavioral health (no dedicated module evident), oncology — not part of Intergy's feature set based on the schema.

## 6. Documentation Quality

**Strengths**:
- The data dictionary is **machine-readable and interactive** — 261 individual HTML pages with consistent structure, parseable by scripts
- **89% of fields** (4,053 of 4,529) have meaningful descriptions/comments
- **All fields** have data types, null options, and default values documented
- **1,052 relationships** are documented with explicit join conditions and cascade behavior — this is excellent relational documentation
- **Value sets** are documented inline for many coded fields (e.g., charge status codes, record status codes, responsibility types)
- The main documentation page includes **MEDCIN-to-SNOMED code crosswalks** for smoking status and pregnancy findings
- Export structure is clearly described with practical guidance on file handling

**Weaknesses**:
- No **sample data** is provided
- Some fields have minimal descriptions like "FK" (foreign key) with no context — but these are relatively few and usually obvious from the table name
- 29 tables (11%) have no table-level description, though their fields are still documented
- No formal **ERD diagram** — relationships must be inferred from parent/child tables
- Value sets referenced as "defined in LookupCode table" are not enumerated in the documentation itself; the LookupCode table would need to be consulted at runtime

**Could a developer build an import?** Yes. The combination of field definitions, data types, relationships, and descriptions provides enough information to understand the data model and build an import pipeline. The CSV format is straightforward. The main gap is lack of sample data and some coded value sets being referenced rather than enumerated.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the full breadth of what Intergy stores as a patient's designated record set. It goes far beyond USCDI clinical summaries to include:
- **Deep billing/revenue cycle data**: 15 insurance claim tables (360 fields), 13 billing/charge tables (178 fields), 7 payment tables (95 fields), plus accounts/financial (228 fields) — this is a genuine billing system export, not a stub
- **Specialty clinical data**: 12 OB/GYN tables (284 fields) representing a real specialty module with pregnancy tracking, ultrasound data, birth records; plus 4 cardiology tables and 3 workers' comp tables
- **Insurance/eligibility**: 12 tables (253 fields) with eligibility verification, PBM responses, coverage details far beyond basic membership
- **Referral workflows**: 12 tables (148 fields) with treatment plans, results, diagnoses, modifiers
- **Patient communications**: Secure messaging with blob content
- **Administrative**: PHI authorizations, consents, advance directives, prior authorizations
- **Clinical depth within USCDI domains**: The Encounter table has 61 fields, PatientRx has 66, LabOrder has 70 — these go well beyond the handful of Must Support elements in US Core profiles

The only minor gaps are operational data outside EHI scope (scheduling is thin with 6 tables, but appointment data is administrative) and questionnaire content (only 1 table). Given Intergy's ambulatory focus, this export covers essentially all applicable patient data domains.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. The evidence:
1. **Native database schema**: The export uses Intergy's internal relational model (261 CSV tables), not C-CDA, FHIR, or any standard exchange format
2. **Billing data**: The presence of 15 insurance claim tables, 13 charge tables, and 7 payment tables — none of which would appear in a C-CDA or FHIR Bulk Data export — proves this was purpose-built
3. **OB/GYN specialty module**: 12 dedicated tables with pregnancy, ultrasound, and birth data that would never appear in standard clinical exchange
4. **Document/image handling**: Custom export structure with blob data (TMSCatalogBlob, GenFileBlob, PracPersonSecureMsgBlob), TAR files for images, and annotation XML — this is operational export infrastructure
5. **Minimum version requirement**: "Intergy version 21.24.00.00" suggests this feature was specifically developed for (b)(10)
6. **Two export modes**: Both single-patient and bulk population export with status tracking — this is a built-out feature, not a quick wrapper

### Key Findings

1. **Exceptionally deep billing coverage**: 15 insurance claim tables with 360 fields (PlanClaimData alone has 110 fields), plus 13 charge tables and 7 payment tables. This is one of the most detailed billing data exports observed, demonstrating genuine engagement with the "all EHI" requirement.

2. **Comprehensive native database export**: 261 tables, 4,529 fields with 89% having meaningful descriptions and 1,052 documented relationships. The export presents Intergy's actual internal data model rather than a projection into a standard format.

3. **Genuine specialty coverage**: The OB/GYN module (12 tables, 284 fields covering pregnancy through postpartum) and cardiology device tracking demonstrate that the export captures specialty-specific clinical data beyond general clinical exchange.

4. **Strong documentation quality**: Interactive HTML data dictionary with field types, descriptions, nullability, default values, value set documentation, and relationship diagrams — sufficient for a developer to build an import pipeline.

5. **Both single-patient and bulk export**: Documentation covers both individual patient and full population export modes with clear file structure descriptions, status tracking, and practical guidance on handling document/image formats.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (tables), ZIP (documents), TIF/video (images)
Entities:        261 tables
Fields:          4,529
Descriptions:    89% of fields have descriptions
Sample data:     No
Bulk export:     Yes (Patient Population Export mode)
Domains covered: 22 of 22 applicable domains
```

### Bottom Line

Intergy EHR's (b)(10) export is a strong example of a purpose-built EHI export. With 261 native database tables covering 4,529 fields across clinical, billing, insurance, specialty (OB/GYN, cardiology), and administrative domains — all documented with types, descriptions, and relationships — a patient or provider would receive a genuinely complete copy of their data. The single biggest strength is the exceptionally deep billing/claims coverage (360 fields across 15 claim tables), which unambiguously distinguishes this from a repackaged clinical exchange export.
