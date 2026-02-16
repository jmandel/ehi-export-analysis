# EHI Export Analysis: Modernizing Medicine Gastroenterology, LLC

**Product**: gGastro  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3031.gGas.GA.10.1.221207

## 1. Product Context

gGastro is a **specialty-specific EHR platform for gastroenterology** by Modernizing Medicine (ModMed), originating from gMed, Inc. (acquired 2015). It is the dominant GI-specialty EHR in the US, ranking #1 in Black Book surveys for 15+ consecutive years. It is architecturally distinct from ModMed's EMA platform used for other specialties.

The product suite includes:

- **gGastro EHR**: Cloud-based GI-specific clinical documentation, problem lists, medications, allergies, immunizations, labs, CPOE, e-prescribing, quality measures, and AI-powered ambient scribe.
- **gGastro ERW (Endoscopy Report Writer)**: The hallmark differentiator — dedicated module for endoscopy/colonoscopy procedure documentation including pre-op, intra-procedure, post-procedure notes, anesthesia, nursing notes, recovery, and time-stamped workflow tracking.
- **gPM (Practice Management)**: Scheduling, billing, claims submission, claim scrubbing, financial dashboards, eligibility verification, document management.
- **Patient Engagement**: Patient portal (gPortal), intake kiosk (gKiosk), reminders (gReminder), surveys (gSurvey), cost estimation (gEstimator).
- **Analytics**: gInsights, gAdvisor.
- **Revenue Cycle Management**: Integrated billing services.
- **Interoperability**: ModMed Records Exchange, lab integrations (150+ labs), FHIR R4 API, Direct messaging, C-CDA.

For EHI assessment, the relevant data domains include: patient demographics, clinical encounters, endoscopy/procedure documentation, medications, labs/pathology, allergies, immunizations, vitals, problems/diagnoses, orders/referrals, clinical notes/documents, insurance/coverage, billing/claims/superbills/payments, scheduling, patient communications (tasks/portal), imaging documents, GI-specific registry data (AGA/GIQuIC), and care plans.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `gGastro-EHI-Patient-Export-Specifications.pdf` (14.4 MB, 167 pages) | Main EHI Patient Export Specifications document. Contains CSV Files Dictionary (441 tables, 4,453 fields), Data Schema (574 relationships), Translations (1,166 value sets), Patient Documents instructions, and Glossary. Version 6.5.3.20251230, dated 2025-12-30. | **Primary source** — most informative |
| `gGastro-EHI-Patient-Export-Specifications-Additional.pdf` (16.9 MB, 551 pages) | Additional translation tables (Occupation and Occupation Industry) too large for main document. GUID-to-value lookup tables for patient occupation tracking. | Supplementary |
| `onc-certification-gi-page.png` (789 KB) | Screenshot of the ONC Certification page at modmed.com/onc-certification-gi/ showing EHI export documentation links. | Context/verification |

The main 167-page PDF is the definitive artifact. It is a genuine, purpose-built data dictionary for the EHI export — not a FHIR or C-CDA spec reference. It documents every CSV file in the export, every field, data types, maximum lengths, relationships between tables, and value set translations.

## 3. Export Mechanics

- **Format**: CSV files (comma-separated values) — one CSV per entity/table, plus document files organized in a folder structure.
- **Mechanism**: The export is described as a "package" containing CSV files and patient documents. The ONC certification page links to the specifications document. The exact UI mechanism (button, request process) is not described in the documentation, but the export is clearly per-patient (the Data Schema is rooted at `Patient`).
- **Single-patient vs bulk**: The Data Schema shows a single-patient tree rooted at `Patient`, indicating this is a single-patient export. Bulk export capability is not described.
- **Access constraints or fees**: Not described in the documentation.
- **Document export**: In addition to structured CSV data, the export includes patient documents (service documents/encounter notes, imaging documents/scanned files, patient portal documents, and letters) with explicit path construction instructions.

## 4. Export Content: What's In It

### Data Dictionary Overview

The main PDF documents **441 CSV tables** containing **4,453 fields** total.

Key metrics:
- **Fields with types**: 4,448 / 4,453 (99.9%) — virtually all fields have documented types
- **Field types**: GUID (1,362), Alphanumeric (1,291), Numeric (629), Boolean (488), Date & Time (281), Decimal (242), Date (120), Score (12), Time (12), XML (11)
- **Fields with lengths**: 1,516 / 4,453 (34.0%) — applicable primarily to Alphanumeric fields
- **Fields with format/translation/comments**: 2,442 / 4,453 (54.8%)
- **Fields referencing translation tables**: 172 — Numeric fields that map to named value sets
- **Relationships**: 574 parent-child relationships documented in a tree-style Data Schema
- **Translation tables**: 1,166 value sets with 5,783 total entries
- **Glossary**: 23 terms defined

Field names are descriptive and self-documenting (e.g., `BillingClaimSnapshot.PayerResponsibilitySequence`, `Finding.PolypectomyDevice`, `ServiceProcedure.WithdrawalTimeSeconds`). The documentation does not include per-field narrative descriptions, but the combination of descriptive names, data types, lengths, and translation table references provides sufficient context for interpretation.

Relationships are documented as a hierarchical tree rooted at `Patient`, showing which tables reference which others via foreign key fields. This enables full reconstruction of the patient record from the CSV files.

### Vendor's own content organization

The vendor organizes data as a flat list of 441 CSV tables alphabetically. They don't use explicit categories. Below is a heuristic categorization based on table name patterns, with representative examples from each domain:

| Category | Tables | Fields | Notable Tables |
|---|---|---|---|
| Billing & Financial | 115 | 1,164 | BillingClaimSnapshot (95), BillingSuperbill (43), BillingPaymentAdjustmentRefund (33), BillingCharge (28), BillingEdiClaimPayment (22), BillingCollection (17) |
| Patient Demographics | 79 | 740 | PatientImmunization (38), Person (36), Patient (30), PatientMedication (28), PatientProblem (24), PatientDocument (21) |
| Procedures & Endoscopy | 41 | 421 | Finding (155), ProcedureOverview (43), ServiceProcedure (25), ServiceProcedureFinding (19), ServicePhase (12) |
| Medications | 17 | 275 | MedicationHistory (44), PrescriptionInboundQueue (44), Medication (41), PrescriptionDispenseHistory (22) |
| Encounters & Services | 32 | 179 | Service (36), ServiceVital (23), ServiceDiagnosis (8), ServiceMedication (6) |
| Labs & Results | 15 | 151 | InterfaceResult (53), InterfaceResultComment (7), InterfaceResultNote (4) |
| Scheduling & Appointments | 17 | 134 | Appointment (38), AppointmentKioskSnapshot (15), AppointmentStatusHistory (8) |
| Clinical Notes & Documents | 16 | 125 | ImagingDocument (38), ServiceDocument (17), ServiceDocumentVersion (8) |
| Tasks & Communications | 10 | 96 | Task (23), TaskAttachment (5), RecallEvent (9) |
| Orders & Referrals | 8 | 95 | Order (50), OrderResult (10) |
| Insurance | 3 | 44 | Insurance (35), InsuranceEligibility (5) |
| Vital Signs | 2 | 43 | ServiceVital (23), VitalSign (20) |
| GI Registry & Quality | 5 | 37 | GiquicExport (149 — this one is mis-categorized but contains quality reporting), AgaService (12), AgaExport (6) |
| Other | 68 | 858 | Intervention (115), Tte (41), BloodPressure (17), Relative (21), QuestionnaireResponse (10) |

The full inventory is in `analysis/entity-inventory-full.json` (441 tables, all fields).

### Billing & Financial depth

The 115 billing tables (1,164 fields) represent remarkably deep billing coverage:
- **Claims/EDI**: 36 tables, 370 fields — complete claim lifecycle including snapshots, charges, diagnoses, payments, adjustments, payer information, and EDI remittance
- **Superbills**: 14 tables, 157 fields — encounter billing forms with procedures, diagnoses, modifiers
- **Payments/Refunds**: 9 tables, 112 fields — payment posting, adjustments, refunds
- **Charges**: 12 tables, 95 fields — charge capture, modifiers, fee schedules
- **Eligibility**: 7 tables, 83 fields — insurance eligibility checking
- **Statements**: 3 tables, 47 fields — patient billing statements
- **Collections**: 2 tables, 25 fields — collections tracking
- **Authorizations**: 1 table, 16 fields — prior authorization tracking

### Endoscopy & Procedure depth

The GI-specialty differentiation shows clearly:
- **Finding** (155 fields): Comprehensive endoscopic finding documentation including polyp characteristics (size, morphology, location, removal method, pathology), biopsy details, and GI-specific classifications
- **ProcedureOverview** (43 fields): Procedure setup, equipment, indications
- **ServiceProcedure** (25 fields): Procedure timing, scope details, withdrawal time
- **AldreteScore** (14 fields): Post-anesthesia recovery scoring
- **AnesthesiaComplication** (8 fields): Complication tracking
- Multiple tables for sedation, nursing notes, recovery phases, instrument tracking

### Document Export

The Patient Documents section describes how to locate physical document files accompanying the CSV data:
- **Service Documents**: Encounter notes in `.mht` format, linked via ServiceDocument/ServiceDocumentVersion tables
- **Imaging Documents**: Scanned documents, faxes, imported documents, lab results with external files (`.jpg`, `.pdf`, etc.)
- **Patient Portal Documents**: Documents published to the patient portal
- **Letters**: Business correspondence, recall letters

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized as 441 CSV tables representing the gGastro database schema. The coverage is strikingly comprehensive:

**Richest domains:**
- **Billing & Financial** (115 tables, 1,164 fields): The deepest single domain, covering the full revenue cycle from charge capture through claims submission, EDI remittance processing, payment posting, adjustments, refunds, collections, and patient statements. This alone signals a purpose-built EHI export — no repackaged clinical exchange would include this depth of billing data.
- **Patient Demographics** (79 tables, 740 fields): Extends well beyond USCDI demographics to include detailed address history, phone numbers, emergency contacts, employment, guarantors, relatives, patient preferences, consent forms, portal access, and kiosk intake snapshots.
- **Procedures & Endoscopy** (41 tables, 421 fields): The GI specialty strength. The 155-field `Finding` table captures granular polyp/lesion characteristics, biopsy details, pathology tracking, and GI-specific morphology — far beyond what any standard clinical exchange format would convey.
- **Medications** (17 tables, 275 fields): Full medication lifecycle including active medications, prescription history, e-prescribing inbound queues, dispense history, administered medications (during procedures), and NDC tracking.

**Moderate domains:**
- **Encounters & Services** (32 tables, 179 fields): Encounters with linked clinical data.
- **Labs & Results** (15 tables, 151 fields): Interface results from external labs.
- **Scheduling** (17 tables, 134 fields): Appointments, holds, wait lists, kiosk snapshots, status history.
- **Clinical Notes & Documents** (16 tables, 125 fields): Service documents, imaging documents, document versions.
- **Tasks & Communications** (10 tables, 96 fields): Internal task workflows, recall events, reminders.
- **Orders & Referrals** (8 tables, 95 fields): Provider orders with 50 fields.

**Thinner but present:**
- **Insurance** (3 tables, 44 fields): Insurance plans with 35 fields, eligibility tracking.
- **Vital Signs** (2 tables, 43 fields): Vitals per encounter.
- **GI Registry** (5 tables, 37 fields): AGA and GIQuIC quality registry data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (30 fields), `Person` (36 fields), `PatientRace`, `PatientEthnicity`, `PatientLanguage`, `EmergencyContact`, `Employment`, `UsaAddress`, `Phone`, `Email` | Thorough — includes name, DOB, SSN, race, ethnicity, language, addresses, phones, employment, emergency contacts, guarantor |
| Encounters / visits | ✅ Covered | `Service` (36 fields), `ServiceDiagnosis`, `ServiceMedication`, `ServiceVital`, `ServicePhase` | Comprehensive encounter model with linked diagnoses, medications, vitals, and phases |
| Problems / diagnoses | ✅ Covered | `PatientProblem` (24 fields), `PatientProblemHistory`, `ServiceDiagnosis`, `BillingSuperbillDiagnosis` | Active problem list + encounter-level diagnoses + billing diagnoses |
| Medications | ✅ Covered | `PatientMedication` (28 fields), `Medication` (41), `MedicationHistory` (44), `PrescriptionDispenseHistory` (22), `AdministeredMedication` (20) | Full lifecycle: active meds, history, prescriptions, dispense, administration during procedures |
| Allergies | ✅ Covered | `PatientAllergy` (14 fields), `PatientAllergyReaction` | Allergies with reaction tracking |
| Immunizations | ✅ Covered | `PatientImmunization` (38 fields), `PatientImmunizationHistory`, `PatientImmunizationRegistryStatus` | Detailed immunization records with registry status |
| Vitals | ✅ Covered | `ServiceVital` (23 fields), `VitalSign` (20 fields) | Per-encounter vitals |
| Lab results | ✅ Covered | `InterfaceResult` (53 fields), `InterfaceResultComment`, `InterfaceResultNote`, `InterfaceRequisition`, `InterfaceTest` | Lab results with comments, notes, requisitions, and test definitions |
| Imaging / diagnostic reports | ✅ Covered | `ImagingDocument` (38 fields), `ImagingDocumentPage` | Imaging documents with pages; physical files included in export |
| Procedures | ✅ Covered | `ServiceProcedure` (25 fields), `ProcedureOverview` (43), `Finding` (155), `Biopsy`, `AldreteScore`, anesthesia tables | Exceptionally deep — GI specialty strength with 41 tables |
| Clinical notes / documents | ✅ Covered | `ServiceDocument` (17 fields), `ServiceDocumentVersion`, `Addendum`, `PatientPortalDocument` | Service documents + versioning + addenda + portal docs; physical files included |
| Care plans / goals | ⚠️ Partial | `PatientCarePlan`, `PatientGoal` appear in relationships; `Order` (50 fields) covers care instructions | Present but thin — care plan and goal tables exist in the schema tree |
| Orders / referrals | ✅ Covered | `Order` (50 fields), `OrderResult` (10 fields), `ReferringPhysicianPerPatient` | Comprehensive order model including results |
| Insurance / coverage | ✅ Covered | `Insurance` (35 fields), `InsuranceEligibility`, `BillingPatientAuthorization` (16 fields) | Policy details, eligibility, authorizations |
| Claims / billing | ✅ Covered | 115 billing tables with 1,164 fields: `BillingClaimSnapshot` (95), `BillingSuperbill` (43), `BillingCharge` (28), 36 EDI tables | Exceptionally deep — full revenue cycle |
| Payments | ✅ Covered | `BillingPaymentAdjustmentRefund` (33 fields), `BillingChargeTransaction`, `BillingEdiClaimPaymentClaimService` | Payments, adjustments, refunds, EOB processing |
| Consents / directives | ⚠️ Partial | `PatientAdvancedDirective`, `PatientConsent` appear in relationship tree | Tables exist but field count is thin |
| Patient communications | ✅ Covered | `Task` (23 fields), `TaskAttachment`, `RecallEvent`, `RecallEventLog`, `LetterQueue`, `PatientPortalDocument` | Tasks, recalls, letters, portal documents |
| Specialty-specific (GI) | ✅ Covered | `Finding` (155 fields), `AgaService`, `AgaExport`, `GiquicExport` (149 fields), `Biopsy`, `Colonoscopy`-related tables, `ExtraIntestinalManifestations` | Deeply GI-specific: polyp characteristics, colonoscopy indicators, AGA/GIQuIC registry data, biopsy tracking |

**Domains covered**: 17 of 19 applicable domains fully covered; 2 partial. No applicable domains are absent.

## 6. Documentation Quality

**Strengths:**
- **Complete field inventory**: Every CSV table and every field is listed with index, name, and data type. This is exhaustive — 441 tables, 4,453 fields, no gaps.
- **Data types documented**: 99.9% of fields have explicit types (GUID, Alphanumeric, Numeric, Boolean, Date & Time, Decimal, Date, Time, Score, XML).
- **Relationships documented**: The Data Schema section provides a complete hierarchical tree showing parent-child relationships between all 441 tables via foreign key fields. A developer can reconstruct the full patient record from this tree.
- **Value sets documented**: 1,166 translation tables with 5,783 entries map coded values to human-readable labels. Fields reference their translation tables by name.
- **Document path construction**: Explicit instructions for locating physical document files (service documents, imaging, portal docs, letters) with example paths.
- **Format specifications**: Date/time formats, GUID formats, and boolean conventions are consistently documented.
- **Glossary**: 23 key terms defined (AGA, GIQuIC, Service, Task, etc.).

**Limitations:**
- **No per-field descriptions**: Fields have names and types but no narrative descriptions explaining what each field means. Names are descriptive (e.g., `WithdrawalTimeSeconds`, `PolypectomyDevice`) but some require domain knowledge to interpret.
- **No sample data**: The documentation doesn't include sample CSV files or example records.
- **No ERD/visual schema**: Relationships are shown as an indented tree, not a formal ERD diagram. Effective but not standard.
- **PDF format only**: The data dictionary is in a PDF, not a machine-readable format like JSON schema or SQL DDL. (However, the tabular layout is parseable with pdftotext.)

**Overall**: A developer with GI domain knowledge could build an import from this documentation. The lack of per-field descriptions is the main weakness, but descriptive field names and translation tables substantially compensate. The documentation is far above average for EHI exports — most vendors provide nothing close to this level of detail.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains that gGastro stores. The 441 CSV tables with 4,453 fields span demographics, encounters, problems, medications, allergies, immunizations, vitals, labs, procedures (deeply GI-specific with 155 fields for endoscopic findings), clinical notes, orders, insurance, and — critically — a massive billing/financial domain with 115 tables and 1,164 fields. This goes far beyond USCDI. The billing depth alone (claims, superbills, EDI remittances, charges, payments, adjustments, collections, statements, eligibility, authorizations) represents data that no clinical exchange standard covers. The GI-specialty data (AGA registry, GIQuIC quality reporting, endoscopy findings with polyp morphology, biopsy tracking, anesthesia/recovery scoring) is product-specific clinical content that only a purpose-built export would include. Patient documents (encounter notes, scanned images, portal documents, letters) are exported as physical files with documented path construction — not just metadata.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built EHI export. The evidence is overwhelming:
1. **Native database model**: The export uses CSV files representing the product's internal data tables — not a projection into FHIR, C-CDA, or any standard exchange format.
2. **441 tables vs ~26 FHIR resource types**: The export surface is an order of magnitude larger than what a FHIR or C-CDA-based export could represent.
3. **Billing data**: 115 billing tables with 1,164 fields — billing data is not in USCDI or any clinical exchange standard.
4. **GI-specialty data**: Endoscopy findings (155 fields), AGA/GIQuIC registry data, procedure phases — none of this maps to standard FHIR resources.
5. **Dedicated specification document**: 167 pages of product-specific documentation with no reference to USCDI, US Core, C-CDA, or FHIR. This is clearly a separate effort from the product's (g)(10) FHIR API.
6. **Relationship tree**: A full hierarchical data schema rooted at `Patient` showing how to reconstruct the complete record — this is database-level documentation, not clinical exchange documentation.

### Key Findings

1. **Exceptionally deep billing coverage** — 115 tables and 1,164 fields (26% of all tables, 26% of all fields) cover the full revenue cycle from charges through claims, EDI remittances, payments, adjustments, collections, and patient statements. This is the strongest signal that this is a genuine EHI export, not a repackaged clinical exchange.

2. **GI-specialty clinical data is fully represented** — The 155-field `Finding` table captures granular endoscopic findings (polyp size, morphology, location, removal method, pathology correlation) that are core to the product's value proposition. The 149-field `GiquicExport` table and AGA registry tables represent quality reporting data unique to gastroenterology.

3. **Complete structural documentation** — 441 tables with 4,453 fields, 574 documented relationships, 1,166 translation tables with 5,783 value set entries, and explicit document path construction instructions. A developer could build a complete import from this specification.

4. **Document export included** — Physical document files (encounter notes, scanned images, portal documents, letters) are included alongside structured CSV data, with documented path construction rules.

5. **No sample data provided** — While the specification is thorough, no sample CSV files or example records are included, which would help validate the documentation.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV (one file per entity) + document files
    Entities:        441 tables
    Fields:          4,453
    Descriptions:    0% (no per-field descriptions, but 99.9% have types and descriptive names)
    Sample data:     No
    Bulk export:     Unclear (schema is per-patient)
    Domains covered: 17 of 19 applicable domains (2 partial)

### Bottom Line

gGastro provides one of the strongest (b)(10) EHI exports encountered. The 441-table CSV export with 4,453 fields, 574 documented relationships, 1,166 value sets, and a 167-page specification document represents a genuine, purpose-built effort to export the designated record set — including 115 billing tables and deeply GI-specific clinical data that no standard clinical exchange format would cover. The main gap is the absence of per-field narrative descriptions and sample data, but the overall completeness and depth of coverage far exceeds what most vendors provide.
