# Greenway Health, LLC — Intergy EHR — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ehi.greenwayhealth.com/Intergy/IntergyEHIExport.html
- CHPL IDs: 11682 (v22, certified 2025-08-14), 11351 (v21, certified 2023-10-03)
- Developer: Greenway Health, LLC

## Navigation Journal

**Step 1 — Initial probe:**
```bash
curl -sI -L "https://ehi.greenwayhealth.com/Intergy/IntergyEHIExport.html" -H 'User-Agent: Mozilla/5.0'
```
Response: HTTP/2 200, Content-Type: text/html, 9,266 bytes. Served from S3 via CloudFront. No redirects.

**Step 2 — Fetch and examine the page:**
```bash
curl -sL "https://ehi.greenwayhealth.com/Intergy/IntergyEHIExport.html" -H 'User-Agent: Mozilla/5.0' -o IntergyEHIExport.html
```
Static HTML page (generated from Microsoft Word 15) describing the Intergy EHI export in detail. Contains:
- Description of Single Patient and Patient Population export modes
- Details about Documents, Images, and Tables folders in the export package
- A prominent "Data Tables" button linking to `./EHI/Viewer/index.html`
- MEDCIN findings cross-reference (pregnancy and smoking status mappings to SNOMED codes)
- Inline image showing TMSCatalogBlob folder structure

**Step 3 — Navigate to Data Tables viewer:**
```bash
curl -sL "https://ehi.greenwayhealth.com/Intergy/EHI/Viewer/index.html" -H 'User-Agent: Mozilla/5.0'
```
Frameset page with two iframes:
- Left pane: `Contracts/DBTOC.htm` — table of contents with searchable list
- Right pane: individual table definition pages (default: `Account.htm`)

**Step 4 — Fetch table of contents and JavaScript data source:**
```bash
curl -sL "https://ehi.greenwayhealth.com/Intergy/EHI/Viewer/Contracts/DBTOC.htm" -H 'User-Agent: Mozilla/5.0'
curl -sL "https://ehi.greenwayhealth.com/Intergy/EHI/Viewer/Contracts/include/DBDescriptions.js" -H 'User-Agent: Mozilla/5.0'
```
The DBTOC.htm page loads table names dynamically from `DBDescriptions.js`, which contains 261 table entries with names and descriptions.

**Step 5 — Download all 261 table definition pages:**
```bash
# Extract table names
grep -oP "new Table\('\K[^']*" DBDescriptions.js > table-names.txt
# Download each table page
while read TABLE; do
  curl -sL "https://ehi.greenwayhealth.com/Intergy/EHI/Viewer/Contracts/${TABLE}.htm" \
    -H 'User-Agent: Mozilla/5.0' -o "viewer/Contracts/${TABLE}.htm"
done < table-names.txt
```
All 261 pages downloaded successfully. Each is a structured HTML page with field definitions, data types, default values, null options, comments, parent tables, and child tables.

**Step 6 — Check parent home page:**
```bash
curl -sL "https://ehi.greenwayhealth.com/default.htm" -H 'User-Agent: Mozilla/5.0'
```
Parent page is Greenway's EHI export hub covering both Intergy and Prime Suite. Links to each product's EHI export page. Also mentions Greenway Insights, Patient Portal, and Electronic Case Reporting are covered by the respective EHR product's export. Links to Greenway Health Developer Platform (FHIR API) — this is separate from the EHI export.

**Step 7 — Check for additional downloadable files:**
No PDFs, ZIPs, CSVs, or other downloadable files were linked from any of the pages. The entire data dictionary is HTML-based.

**Step 8 — Screenshots taken in browser:**
- Main EHI export page (full page screenshot)
- Data Tables viewer with left-pane table list and right-pane table definition

## What Was Found

Greenway Health provides a well-structured, purpose-built EHI export documentation site for Intergy. This is a genuine (b)(10) implementation — not a repackaged FHIR API.

### Export Format
The Intergy EHI export produces a package containing three types of content:

1. **Tables** — CSV files, one per database table. The export covers 261 tables across the full Intergy database schema. Each CSV can be opened in Excel or other spreadsheet applications.

2. **Documents** — Clinical documents, patient clinical summaries, and other chart documents exported as ZIP files containing embedded RTF/PDF/DOC files. Two types:
   - `GenFile` (general files/images, keyed by GenFileSID)
   - `TMSCatalog` (transcription management system documents, keyed by CatalogSID)
   - `PracPersonSecureMsg` (secure messages, population export only)

3. **Images** — Patient images (X-rays, advance directives, diagnostic imaging/procedure reports) in TIF and video clip format, with XML annotation files (.ann, base64 encoded). In population export, images are packaged in TAR files (up to 5GB each) with an `ImageIndexFile.csv` for path lookup.

### Two Export Modes
- **Single Patient Export**: Documents, Images, and Tables folders for one patient.
- **Patient Population Export**: All patients in the organization. Documents are organized into subfolders (GenFileBlob, TMSCatalogBlob, PracPersonSecureMsgBlob) with a 10,000 document per folder limit. Images in TAR archives with index files. Includes a Bulk Export Status CSV showing success/failure per table/document/image.

### Data Dictionary
The data dictionary is the crown jewel of this documentation. For each of the 261 tables:
- **Table description** explaining its purpose
- **Field definitions** with: field name, SQL data type, default value, null option (MANDATORY/OPTIONAL), and a human-readable comment
- **Parent table relationships** with join conditions and delete cascade behavior
- **Child table relationships** with join conditions and delete cascade behavior
- **Version metadata**: Last Updated 9/24/2025, Intergy Version 22.00.00.00

Total: 261 tables, 4,529 fields, 1,052 documented relationships.

### MEDCIN Cross-Reference
The main page provides specific MEDCIN finding ID mappings:
- Pregnancy findings: MEDCIN 30596 → SNOMED 77386006 / ICD-10 Z33.1
- Smoking status: MEDCIN 100000511 with 8 ClinicalLookupCode values mapped to SNOMED codes

### Minimum Version
EHI export requires Intergy version 21.24.00.00 or later.

## Export Coverage Assessment

### Data Domain Coverage

This export is remarkably comprehensive. The 261 tables span virtually every data domain that Intergy stores about patients:

**Clearly covered (with deep table structures):**
- **Demographics/Person** (34 tables, 415 fields): Person, Entity, Address, Phone, Email, PersonRace, PersonTribalAffiliation, PersonRelationship, PersonHistory, DOBHistory, SexHistory, PersonName, Employee, Occupation — including full change history tables
- **Clinical encounters** (15 tables, 344 fields): Encounter, EncounterFinding, EncounterFindingHistory, EncounterDiagnosis, EncounterEducation, EncounterEvent, EncounterVital, EncounterVitalSet, ClinicalCase, ClinicalCustomFinding
- **Problems/Diagnoses** (8 tables, 148 fields): PatientProblem, PatientProblemHistory, PatientProblemCodeLink, Diagnosis, Ailment with diagnosis/note/procedure sub-tables
- **Medications/Prescriptions** (18 tables, 318 fields): PatientRx, PatientRxActivity, PatientRxDenial, PatientRxFill, RxChangeRequest, RxDiagnosis, RxEligibility (PBM eligibility/benefits), DURAlert, RxNote, RxRequest
- **Allergies** (5 tables across demographics): PersonAllergy, PersonAllergyHistory, PersonAllergyReaction, PersonAllergyReactionHist, Allergy
- **Lab orders/results** (17 tables, 341 fields): Full lab workflow from LabOrder through LabOrderTest, LabOrderTestResult, LabOrderTestResultNote, LabOrderTestSpecimen, with lab/provider/specimen metadata
- **Immunizations** (5 tables, 120 fields): PatientVacDose, PatientVacDoseAction, PatientVacDoseReaction, Vaccine definitions, VaccineReaction definitions
- **Vitals** (3 tables): EncounterVital, EncounterVitalSet, VitalType
- **Care plans** (12 tables, 153 fields): PatientCarePlan, goals, interventions, outcomes, health concerns — with full history tables
- **Documents/Imaging** (13 tables, 218 fields): Document, DocumentInterpretation, DocumentNote, GenFile/GenFileBlob, TMSCatalog/TMSCatalogBlob, RISStudy/RISVisit (radiology), CLWCorrespondence (clinical letter writer)
- **Billing/Claims** (43 tables, 855 fields): Account, Charge, ChargeActivity, ChargeCoverage, Claim, ClaimCharge, Payment, PaymentAssignment, PlanClaim with full remittance detail (PlanClaimChargeRemit, PlanClaimChargeRemitAdj, PlanClaimChargeRemitRmk), Adjustment, CopayActivity, AccountBill, AccountStatement
- **Insurance/Coverage** (11 tables, 218 fields): Carrier, Plan, PlanGroup, Policy, PolicyMember, Eligibility/EligibilityBenefit/EligibilityComment, PriorAuthInfo
- **OB/GYN specialty** (12 tables, 284 fields): OBPregnancy, OBInitialVisit, OBPrenatalVisit, OBPostpartumVisit, OBBirth, OBUltraSound — full obstetrics workflow
- **Cardiology** (4 tables, 54 fields): CardioOrder, CardioComponent, CardioOrderComponent
- **Orders** (8 tables, 115 fields): PatientOrderSet, PatientOMOrderLineItem with AUC (Appropriate Use Criteria) tracking
- **Referrals** (11 tables, 136 fields): Referral, ReferralDiagnosis, ReferralTreatmentPlan/Result, RefDoctor
- **Workers' Comp** (3 tables, 52 fields): WorkersComp, WorkersCompDiagnosis, WorkersCompProcedure
- **PHI/Consent** (5 tables, 67 fields): PHIAuthorization, PHIConsent, PHIDisclosure with activity tracking
- **Appointments** (5 tables, 76 fields): Appointment, ApptQuestionnaire, ApptRecall, ApptRoom, ApptStaff
- **Secure messaging** (2 tables): PracPersonSecureMessage, PracPersonSecureMsgBlob
- **Implantable devices** (2 tables): PatImplantableDevice, PatImplantableDeviceActivity
- **Advance directives** (2 tables): AdvanceDirective, AdvanceDirectiveActivity
- **Patient portal access** (1 table): PatientPortalAccess
- **Inpatient visits** (2 tables): InpatientVisit, InpatientVisitNote
- **Ryan White program** (2 tables): PatientRSRInfo, PatientRSRNote
- **Lookup/reference codes** (4 tables): LookupCode, AltLookupListCode, ExtAttributeCode, ClinicalLookupCode
- **Extended attributes** (1 table): EAObjectData — extensible data model for custom fields

**Not explicitly present but likely not EHI:**
- Audit logs (correctly excluded — operational security data)
- System configuration tables (correctly excluded — infrastructure)
- Template definitions (correctly excluded — system configuration)
- Print/fax logs (correctly excluded — operational)

**Potentially missing but borderline:**
- Telehealth session metadata — the product research mentions integrated telehealth (Greenway Telehealth), but no telehealth-specific tables appear. Telehealth encounters may be recorded as regular Encounters with a visit type flag rather than separate tables.
- Chronic Care Management (CCM) and Remote Patient Monitoring (RPM) — mentioned in product research as integrated capabilities. May be captured through existing encounter/order tables or through the ExtAttributeCode/EAObjectData extensibility framework. No dedicated CCM/RPM tables are visible.
- Practice Analytics data — product has 5,000 reportable fields, but analytics/reporting data is aggregate/operational, not per-patient EHI.

### Export Format & Standards

The export uses a **database dump approach** — CSV files corresponding to database tables, plus native document/image files. This is not FHIR, C-CDA, or any healthcare interoperability standard. It is, however, arguably the most honest and complete approach to (b)(10) compliance:

- **CSV tables** preserve the full relational database structure with all fields, including internal IDs that enable cross-table joins
- **Documents** are exported in their native formats (RTF, PDF, DOC) inside ZIP containers
- **Images** are exported in native TIF/video formats with XML annotations
- **Relationships** between tables are fully documented with join conditions

The format is appropriate for the data. A relational database export with documented schema is the most faithful way to export "all electronic health information" from a relational database system. A FHIR translation would inevitably lose data that doesn't map to FHIR resources.

A third party could reconstruct the patient record from this export given the data dictionary — the join conditions, foreign key annotations, and table descriptions provide the necessary context to navigate the relational model.

### Documentation Quality

**Strengths:**
- Every one of 261 tables has a dedicated documentation page
- Field-level documentation includes data types, nullability, and descriptive comments
- Foreign key relationships are explicitly documented with join conditions and cascade behaviors
- The data dictionary is searchable via the viewer interface
- Version and date stamps are present on every page (Last Updated: 9/24/2025, Intergy Version: 22.00.00.00)
- The main page provides clear guidance on export structure, including notes about file format quirks (e.g., ZIP files that need renaming to .RTF)

**Weaknesses:**
- Some table descriptions are empty ("No Description Available" or blank) — about 20-30 tables
- Many FK fields simply say "FK" in the comment without specifying which lookup table/type they reference (though parent table relationships section helps)
- No sample export files or worked examples are provided
- No explicit documentation of which tables are exported in Single Patient vs. Population mode
- Value sets for coded fields are often described indirectly ("defined in LookupCode table for lookup type 'X'") rather than enumerated — the LookupCode table itself is in the export, so values are available but require cross-referencing
- The MEDCIN finding cross-reference is helpful but limited to pregnancy and smoking status — other MEDCIN IDs in EncounterFinding are not mapped

### Structure & Completeness

**Field-level granularity**: Excellent. Every field has a name, SQL data type (INTEGER, CHARACTER(n), DECIMAL(n,m), DATE, etc.), default value, mandatory/optional flag, and a descriptive comment.

**Relationships**: Thoroughly documented. Parent and child table relationships include join conditions and delete cascade behavior (RESTRICT, CASCADE, SET NULL). This is essential for navigating the relational model.

**Value sets**: Partially documented. Coded fields reference lookup types in the LookupCode table but don't enumerate the actual codes inline. Some clinical codes (MEDCIN, SNOMED, ICD-10) are cross-referenced on the main page. The ClinicalLookupCode table provides mappings for clinical coded values.

**Versioning**: Each table page shows the Intergy version (22.00.00.00) and last update date (9/24/2025). No change history or diff between versions is provided.

### Overall Assessment

Greenway Health has done genuine (b)(10) work here. This is not a FHIR API repackaged as EHI export documentation. The export is a faithful database dump covering 261 tables across every major data domain in the product — demographics, clinical encounters, problems, medications, allergies, labs, immunizations, vitals, care plans, billing, claims, insurance, specialty clinical data (OB/GYN, cardiology), documents, images, referrals, workers' comp, advance directives, and more.

The documentation is one of the more thorough EHI export data dictionaries we've encountered. The combination of field-level definitions, relationship documentation, and export format descriptions provides enough information for a technically competent consumer to understand and process the export. The 4,529 documented fields across 261 tables with 1,052 explicit relationships represents substantial investment in documentation.

The main gaps are cosmetic rather than substantive: some tables lack descriptions, some FK comments are terse, and there are no sample files. But the core data dictionary is solid, and the export approach (CSV database dump + native documents/images) is well-suited to the (b)(10) requirement of exporting all electronic health information.

## Access Summary
- Final URL (after redirects): https://ehi.greenwayhealth.com/Intergy/IntergyEHIExport.html
- Status: found
- Required browser: no (all content accessible via curl; JavaScript loads table list in viewer but underlying data is in static .htm files)
- Navigation complexity: one_click (main page → Data Tables viewer → individual table pages)
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The documentation was fully accessible, well-structured, and easy to navigate. All 261 table pages downloaded without errors.
