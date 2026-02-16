# Greenway Health, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ehi.greenwayhealth.com/Intergy/IntergyEHIExport.html
- CHPL IDs: 11682 (v22, certified 2025-08-14), 11351 (v21, certified 2023-10-03)
- Developer: Greenway Health, LLC

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://ehi.greenwayhealth.com/Intergy/IntergyEHIExport.html"` returned HTTP 200 with `Content-Type: text/html`, 9266 bytes. Hosted on Amazon S3 behind CloudFront. No redirects, no auth required.

2. **Main page** — Static HTML describing the Intergy EHI Export. Two modes documented: Single Patient Export and Patient Population Export. The page describes three export components: Documents folder, Images folder, and Tables folder (CSV format). A prominent "Data Tables" link points to `./EHI/Viewer/index.html`.

3. **Parent page** (`https://ehi.greenwayhealth.com/default.htm`) — Greenway's EHI Export landing page linking to both Intergy and Prime Suite documentation. Also links to the Greenway Health Developer Platform (API docs at developers.greenwayhealth.com — not relevant to b(10) export).

4. **Data Tables Viewer** (`https://ehi.greenwayhealth.com/Intergy/EHI/Viewer/index.html`) — An iframe-based interface with a searchable table-of-contents on the left and table definition pages on the right. The TOC is JavaScript-generated from `Contracts/include/DBDescriptions.js`.

5. **Table definitions** — Each table has its own `.htm` page at `Contracts/{TableName}.htm` with:
   - Table description
   - Field definitions (name, datatype, default, null option, comment)
   - Parent table relationships (foreign keys referenced)
   - Child table relationships (tables that reference this table)

6. **Downloaded all 261 table definition pages** plus supporting CSS, JS, and assets. Built a Bun TypeScript enrichment script to parse all HTML into structured JSON.

No downloadable files (PDF, ZIP, CSV, etc.) were found — the entire documentation is served as HTML pages. No login wall, no anti-bot measures.

## What Was Found

### Export Format

Intergy's EHI Export produces a package containing three types of content:

1. **Documents folder** — Clinical documents, images, and clinical summaries stored in the patient chart. Files include GenFile (JPEG) and TMSCatalog (ZIP containing RTF/PDF/DOC). For population export, blob data is organized into folders (GenFileBlob, TMSCatalogBlob, PracPersonSecureMsgBlob) with a 10,000-document limit per folder.

2. **Images folder** — Patient images (X-rays, etc.) with annotations, advance directives, diagnostic imaging reports in TIF and video clip format. Annotations exported as separate XML files (.ann) with base64-encoded content. For population export, images are in TAR format (5GB limit per tar) with an ImageIndexFile.csv index.

3. **Tables folder** — Database tables exported as CSV files. This is the core data export, covering 261 tables across all data domains.

The export is a **direct database dump in CSV format** — not FHIR, not C-CDA, not any standard format. This is a genuine (b)(10) approach: export everything the system stores about patients in its native database structure.

### Data Dictionary

The data dictionary is comprehensive:
- **261 tables** with **4,529 fields** documented
- Each field has: name, datatype (e.g., INTEGER, CHARACTER(10), DECIMAL(10,2), DATE, LOGICAL), default value, null/mandatory constraint, and a comment
- **526 parent-child relationships** documented via foreign key annotations
- Table descriptions explain the purpose of each table
- Last updated: 9/24/2025, Intergy Version: 22.00.00.00

### Additional Export Notes

The documentation includes specific notes about:
- MEDCIN clinical findings mapping (pregnancy findings → SNOMED 77386006, smoking status → SNOMED codes with a clinical lookup table)
- Instructions for handling files that need extension renaming
- Population export bulk status file (CSV showing success/failure per table/document/image)

## Export Coverage Assessment

### Data Domain Coverage

This is an exceptionally thorough EHI export. The 261 exported tables cover virtually every data domain identified in the product research:

**Clinical Data — Fully Covered:**
- Patient demographics (Patient, Person, PersonName, PersonHistory, PersonRace, PersonTribalAffiliation, SexHistory, DOBHistory)
- Problems/diagnoses (PatientProblem, PatientProblemHistory, PatientProblemCodeLink, Diagnosis, EncounterDiagnosis)
- Medications/prescriptions (PatientRx, PatientRxActivity, PatientRxFill, PatientRxDenial, RxRequest, RxChangeRequest, RxNote, RxDiagnosis, RxEligRequest — extensive e-prescribing data)
- Allergies (PersonAllergy, PersonAllergyHistory, PersonAllergyReaction, PersonAllergyReactionHist, DURAlert)
- Lab orders/results (Lab, LabOrder, LabOrderTest, LabOrderTestResult, LabOrderTestSpecimen, LabOrderTask — 17 lab-related tables)
- Clinical encounters (Encounter, EncounterFinding, EncounterFindingHistory, EncounterVital, EncounterVitalSet, EncounterEducation, EncounterEvent, EncounterNotingActivity — 9 encounter tables)
- Vital signs (VitalType, EncounterVital, EncounterVitalSet)
- Immunizations (Vaccine, VaccineReaction, PatientVacDose, PatientVacDoseAction, PatientVacDoseReaction)
- Advance directives (AdvanceDirective, AdvanceDirectiveActivity)
- Clinical notes/documents (TMSCatalog, TMSCatalogBlob, TMSActivity, CLWCorrespondence, Document, DocumentNote, DocumentInterpretation, DocumentAttributeValue)
- Care plans (PatientCarePlan, PatientCareProgram, PatientCareProgramHistory, PatientCPGoal, PatientCPGoalHistory, PatientCPGoalIntervention, PatientCPGoalOutcome, PatientCPHealthConcern — 14 care plan tables)
- Implantable devices (PatImplantableDevice, PatImplantableDeviceActivity)
- Clinical decision support findings (ClinicalCustomFinding, ClinicalLookupCode, MedcinFinding, EncounterFinding)

**Billing & Financial — Fully Covered:**
- Accounts (Account, AccountAlert, AccountBill, AccountBillItem, AccountNote, AccountStatement, AccountStatementItem, AccountStatus)
- Charges (Charge, ChargeActivity, ChargeActivityNote, ChargeAuxData, ChargeCoverage, ChargeNote, ChargeClaimNote)
- Claims (Claim, ClaimCharge, ClaimNote)
- Insurance claims (PlanClaim and 15+ PlanClaim* tables for claim data, remittance, adjudication, status, line items)
- Payments (Payment, PaymentAssignment, PaymentNote, PaymentReversal, PaymentVoid, PaymentVoidNote)
- Adjustments (Adjustment, CopayActivity)
- Insurance plans/policies (Plan, PlanGroup, PlanAltID, Policy, PolicyMember)
- Eligibility (Eligibility, EligibilityBenefit, EligibilityComment)
- Workers' compensation (WorkersComp, WorkersCompDiagnosis, WorkersCompProcedure)
- Prior authorization (PriorAuthInfo, PriorAuthInfoResponse)
- Responsibility transfer (ResponsibilityTransfer)

**Practice Management — Covered:**
- Appointments (Appointment, ApptQuestionnaire, ApptRecall, ApptRoom, ApptStaff)
- Referrals (Referral, ReferralActivity, ReferralDiagnosis, ReferralNote, ReferralTreatmentPlan, ReferralTreatmentResult — 10 referral tables)
- Recall notices (RecallNotice)
- Providers/staff (Provider, Staff, RefDoctor, RefDocRole, Position, Specialty, Department)
- Practice/organization (Practice, ServiceCenter, FinanceCenter, Company, Carrier)

**Specialty Clinical Data — Covered:**
- OB/GYN (OBPatient, OBPregnancy, OBEncounter, OBInitialVisit, OBPrenatalVisit, OBPostpartumVisit, OBBirth, OBUltraSound, OBUltrasoundFetus — 13 OB-specific tables)
- Cardiology (CardioOrder, CardioOrderActivity, CardioOrderComponent, CardioComponent)
- Radiology/imaging (RISStudy, RISStudyNote, RISVisit, Document, GenFile, GenFileBlob, Images)
- Inpatient visits (InpatientVisit, InpatientVisitNote)

**Patient Engagement — Partially Covered:**
- Patient portal access (PatientPortalAccess)
- Secure messaging (PracPersonSecureMessage, PracPersonSecureMsgBlob)
- Clinical summaries (PatientClinicalSummary)
- Email (Email, EmailHistory)
- PHI authorizations/consent/disclosure (PHIAuthorization, PHIConsent, PHIConsentActivity, PHIDisclosure, PHIDiscActivity)

**Potentially Missing/Unclear:**
- Patient feedback/reviews (Patient Connect feature) — not visible in the table list. This may live in a separate system.
- Online scheduling data — unclear if captured beyond Appointment table
- AI-generated documentation (Clinical Assist) — unclear if stored separately or within EncounterFinding/TMSCatalog
- Telehealth session data — not explicitly represented
- Questionnaire responses beyond ApptQuestionnaire — the Questionnaire table exists but may be limited

These gaps are minor and mostly involve newer add-on modules (Patient Connect, Clinical Assist) that may store data in separate systems outside the core Intergy database.

### Export Format & Standards

- **Format**: Native database dump as CSV files, plus document blobs (ZIP, TIF, TAR, JPEG)
- **Not a FHIR or C-CDA export** — this is a raw database extract, which is the appropriate approach for (b)(10)
- **Relationships**: Foreign keys are documented in the data dictionary with parent/child table references
- **Table structure**: Preserves the actual database schema with original field names and types
- **Reconstruction feasibility**: A third party with the data dictionary could reconstruct the complete patient record, though it requires understanding the relational model (261 tables with 526 documented relationships)

This is one of the better approaches to (b)(10) compliance — export the actual database tables rather than trying to map everything into a clinical standard that can't represent billing, claims, or specialty data.

### Documentation Quality

**Strengths:**
- Complete data dictionary covering all 261 exported tables
- Field-level documentation with datatypes, nullability, and descriptions
- Foreign key relationships documented (parent and child tables)
- Clear export format documentation (what folders contain, file naming conventions)
- Practical notes about file handling (extension renaming, ZIP extraction)
- MEDCIN/SNOMED mapping for coded clinical findings
- Version-stamped (Intergy v22.00.00.00, last updated 9/24/2025)

**Weaknesses:**
- Many field comments are just "FK" without specifying which parent table/field — though the Parent Tables section usually clarifies this
- No sample export files or example records provided
- No formal schema file (XSD, JSON Schema, DDL) — the data dictionary is HTML only
- Some tables have empty descriptions (e.g., AddressHistory, AdvanceDirectiveActivity, ClinicalCase)
- No explicit value set documentation for coded fields (e.g., what values AccountStatus can take) beyond the smoking status table
- No versioning/change history between exports

**Overall**: A developer could implement an import of this data based on the documentation, though coded field interpretation would require some reverse engineering. The documentation is clearly maintained (updated July 2025) and covers the full database schema.

### Structure & Completeness

- **Granularity**: Field-level documentation with data types and comments
- **Coded fields**: Smoking status SNOMED mappings documented; other coded fields reference LookupCode table but specific value sets are not enumerated
- **Relationships**: 526 parent/child relationships documented across 261 tables
- **Entity model**: The relational model is well-documented through the foreign key structure — Patient → Account → Charge → Claim chains are traceable
- **No versioning**: The data dictionary shows a single version (22.00.00.00) with no change history

## Access Summary
- Final URL (after redirects): https://ehi.greenwayhealth.com/Intergy/IntergyEHIExport.html
- Status: found
- Required browser: no (all content accessible via curl; JS used only for table-of-contents search/filter in the viewer)
- Navigation complexity: one_click (main page → Data Tables link)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The documentation was fully accessible, well-structured, and easy to navigate. The only minor challenge was that the table-of-contents is JavaScript-generated, requiring extraction of the table names from `DBDescriptions.js` to programmatically download all 261 table pages.
