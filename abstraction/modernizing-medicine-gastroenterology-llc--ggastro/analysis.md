# EHI Export Analysis: Modernizing Medicine Gastroenterology, LLC

**Product**: gGastro
**Analysis date**: 2026-02-15
**CHPL IDs**: 11054 (`15.04.04.3031.gGas.GA.10.1.221207`)

## 1. Product Context

gGastro is a specialty-specific EHR platform for gastroenterology, developed by Modernizing Medicine Gastroenterology, LLC (formerly gMed, Inc., acquired by ModMed in 2015). It is the dominant GI-specialty EHR in the United States, ranking #1 in Black Book's gastroenterology category for 15+ consecutive years. gGastro is architecturally distinct from ModMed's other EHR platform (EMA) — it has its own codebase and database model.

The product is a comprehensive suite covering:

- **gGastro EHR**: Core clinical documentation with GI-specific templates, problem lists, medications, allergies, immunizations, CPOE, clinical decision support, e-prescribing, and AI-assisted note generation (ModMed Scribe)
- **gGastro ERW (Endoscopy Report Writer)**: Dedicated endoscopy/colonoscopy procedure documentation including pre-op, intra-procedure, and post-procedure notes; anesthesia and recovery documentation; time-stamped workflow tracking; nursing notes
- **gPM (Practice Management)**: Scheduling, billing, claims submission, clearinghouse integration, eligibility verification, financial dashboards
- **Patient Engagement**: Patient portal (gPortal), intake kiosk (gKiosk), appointment reminders (gReminder), surveys (gSurvey), cost estimation (gEstimator)
- **Lab Integrations**: Interfaces with 150+ labs including Labcorp and Quest
- **Revenue Cycle Management**: Integrated billing services
- **Telehealth**: Virtual visit capabilities
- **Analytics**: gInsights, gAdvisor

For a complete (b)(10) export, we should expect coverage of clinical data (demographics, encounters, diagnoses, medications, allergies, immunizations, labs, vitals, procedures, clinical notes), GI-specialty data (endoscopy findings, interventions, disease-specific assessments), billing data (charges, claims, superbills, payments, insurance, statements), and patient engagement data (portal messages, kiosk data, recalls).

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informational Value |
|---|---|---|---|
| `gGastro-EHI-Patient-Export-Specifications.pdf` | 14.4 MB, 167 pages | Main EHI Patient Export Specifications v6.5.3.20251230 (dated 2025-12-30). Contains CSV Files Dictionary, Data Schema, Translations, Patient Documents section, and Glossary. Author: Isaac Tobelem. | **Primary source** — contains the complete data dictionary |
| `gGastro-EHI-Patient-Export-Specifications-Additional.pdf` | 16.9 MB, 551 pages | Additional specifications containing two large translation tables (Occupation and Occupation Industry) that were too large for the main document. | **Supplementary** — occupation/industry lookup tables only |
| `onc-certification-gi-page.png` | 789 KB | Screenshot of the ONC Certification page at modmed.com/onc-certification-gi/ showing the "EHI Export Documentation" section with links to both PDFs. | **Contextual** — confirms the export documentation is publicly accessible |
| `enrichment/data-dictionary.json` | 1.5 MB | Structured JSON extraction from the main PDF, produced by the enrichment script. Contains 441 tables, 4,453 fields, 574 relationships, 1,157 translation tables with 5,757 entries, and 23 glossary terms. | **Highly valuable** — machine-queryable version of the PDF content |
| `enrichment/main-pdf-layout.txt` | 681 KB | Text extracted from main PDF via `pdftotext -layout`. | **Source material** for verification |
| `enrichment/additional-pdf-layout.txt` | 10.7 MB | Text extracted from additional PDF via `pdftotext -layout`. | **Supplementary** — raw occupation/industry tables |
| `enrichment/extract-data-dictionary.ts` | 11 KB | Bun TypeScript script used to parse the PDF text into structured JSON. | **Reproducibility** — enables re-extraction |
| `enrichment/README.md` | 2.4 KB | Documentation for enrichment scripts with known parsing limitations. | **Metadata** |

The main PDF and its structured JSON extraction are the definitive artifacts. No sample export data was provided — only the specification/data dictionary.

## 3. Export Mechanics

- **Format**: CSV (one file per table/entity), plus associated document files (MHT, PDF, JPG, etc.) in a `Documents\` folder structure
- **Mechanism**: The documentation describes the output as a "package" but does not specify the UI or API mechanism for initiating the export. Based on the document title ("EHI Patient Export"), this is a single-patient export. The ONC certification page does not provide additional detail on the export process itself.
- **Single-patient vs bulk**: Single-patient export (the entire data schema tree is rooted at the `Patient` table). No evidence of bulk/multi-patient export capability in the documentation.
- **Access constraints or fees**: Not documented in the artifacts reviewed. The ONC certification page is publicly accessible at `https://www.modmed.com/onc-certification-gi/`.

The export package contains:
1. **441 CSV files** — one per entity/table, with GUID-based primary and foreign keys
2. **Document files** — service documents (MHT), imaging documents (JPG, PDF), portal documents (PDF), and letters (MHT), organized in a `Documents\YYYY\Type\YYYYMMDD\` folder structure
3. **Translation tables** — 1,157 value set mappings for coded fields (documented in the PDF; not clear if shipped as separate files or embedded in the PDF only)

## 4. Export Content: What's In It

### Data Dictionary Summary

The export specification defines **441 CSV tables** containing **4,453 fields** total. The data dictionary documents each field with:

- **Column index**: ✅ All 4,453 fields (100%)
- **Field name**: ✅ All 4,453 fields (100%)
- **Data type**: ✅ 4,420 fields (99.3%) — 33 fields have empty types, likely parsing artifacts
- **Maximum length**: ⚠️ 1,034 fields (23.2%) — only applicable to Alphanumeric fields
- **Format/Translation reference**: ⚠️ 2,416 fields (54.3%) — GUID formats, date formats, boolean formats, or translation table references
- **Descriptions**: ❌ 0 fields (0%) — no natural-language descriptions of what any field means
- **Relationships/foreign keys**: ✅ 574 documented relationships in the Data Schema section
- **Value sets**: ✅ 1,157 translation tables with 5,757 coded entries
- **Sample data**: ❌ Not provided

**Field type distribution** (across 4,420 typed fields):

| Type | Count | % |
|---|---|---|
| GUID | 1,362 | 30.6% |
| Alphanumeric | 1,297 | 29.1% |
| Numeric | 632 | 14.2% |
| Boolean | 488 | 11.0% |
| Date & Time | 387 | 8.7% |
| Decimal | 242 | 5.4% |
| Score | 12 | 0.3% |
| (empty) | 33 | 0.7% |

### Vendor's own content organization

The export does not use vendor-defined categories. Tables are listed alphabetically in the CSV Files Dictionary. The Data Schema section presents them as a hierarchical tree rooted at `Patient` with 146 direct child relationships. I have classified tables into domains based on naming conventions.

**Domain breakdown** (from `analysis/summary-stats.json`):

| Domain | Tables | Fields | Key Tables |
|---|---|---|---|
| Billing & Claims | 111 | 1,209 | `BillingClaimSnapshot` (95), `BillingSuperbill` (43), `BillingPatientStatementHistory` (43), `Insurance` (35), `BillingPaymentAdjustmentRefund` (33), `BillingEncounter` (30), `BillingCharge` (25), `BillingEdiClaimPayment` (22) |
| Endoscopy / Procedures | 53 | 861 | `Finding` (155), `GiquicExport` (149), `Intervention` (115), `ProcedureOverview` (43), `Tte` (41), `StressTest` (19), `CarotidUltrasoundMeasurement` (20), `AldreteScore` (15) |
| Patient / Demographics | 93 | 847 | `PatientImmunization` (38), `Person` (36), `Patient` (30), `PatientImplantableDevice` (25), `MedicalHistoryReview` (25), `PatientAllergy` (24), `UsaAddress` (24), `PatientDiagnosis` (21) |
| Encounters / Services | 49 | 279 | `Service` (36), `ServiceDocument` (18), `ServiceProcedure` (14) |
| Medications | 16 | 253 | `MedicationHistory` (44), `PrescriptionInboundQueue` (44), `Medication` (41), `Prescription` (30) |
| Scheduling | 28 | 209 | `Appointment` (38), `RoundingList` (17), `InboundAppointmentReservation` (13), `Recall` (11) |
| Lab Interfaces | 18 | 198 | `InterfaceResult` (53), `InterfaceTest` (23), `InterfaceTestResult` (19), `InterfaceRequisition` (17) |
| Imaging / Documents | 18 | 142 | `ImagingDocument` (38), `DocRetrieveImportDocument` (12) |
| Messaging / Communications | 16 | 124 | `DirectMessage` (18), `FaxOutboundQueue` (18), `Task` (15), `Phone` (14) |
| Clinical Assessments | 8 | 88 | `MedicalHistoryReview` (25), `NuclearPerfusion` (14), `Impression` (14), `ExtraIntestinalManifestations` (11) |
| Orders / Referrals | 8 | 80 | `Order` (50) |
| Vitals | 3 | 62 | `VitalSigns` (27), `VitalSignsMonitorSession` (16) |
| Administrative | 8 | 36 | `ExportImmunization` (5), `SyndromicSurveillance` (6) |
| Quality Reporting | 3 | 24 | `CodingAdvisor2021` (7), `MipsReportExecutionAciDetail` (9) |
| Other | 4 | 15 | `CodingAdvisorMDMTimeMode` (3) |
| Telehealth | 3 | 12 | `TelehealthPatient`, `TelehealthRoomInvite`, `TelehealthService` |
| Patient Portal | 1 | 8 | `PatientPortalAccessLog` (note: most portal tables are classified under Patient/Demographics) |
| Immunizations | 1 | 6 | `CvxCodePerPatientImmunization` |

**Top 20 largest tables** (by field count):

| Rank | Table | Fields | Domain |
|---|---|---|---|
| 1 | Finding | 155 | Endoscopy / Procedures |
| 2 | GiquicExport | 149 | Endoscopy / Procedures |
| 3 | Intervention | 115 | Endoscopy / Procedures |
| 4 | BillingClaimSnapshot | 95 | Billing & Claims |
| 5 | InterfaceResult | 53 | Lab Interfaces |
| 6 | Order | 50 | Orders / Referrals |
| 7 | MedicationHistory | 44 | Medications |
| 8 | PrescriptionInboundQueue | 44 | Medications |
| 9 | BillingPatientStatementHistory | 43 | Billing & Claims |
| 10 | BillingSuperbill | 43 | Billing & Claims |
| 11 | ProcedureOverview | 43 | Endoscopy / Procedures |
| 12 | Medication | 41 | Medications |
| 13 | Tte | 41 | Endoscopy / Procedures |
| 14 | Appointment | 38 | Scheduling |
| 15 | ImagingDocument | 38 | Imaging / Documents |
| 16 | PatientImmunization | 38 | Patient / Demographics |
| 17 | Person | 36 | Patient / Demographics |
| 18 | Service | 36 | Encounters / Services |
| 19 | Insurance | 35 | Billing & Claims |
| 20 | BillingPaymentAdjustmentRefund | 33 | Billing & Claims |

The complete inventory of all 441 tables and 4,453 fields is in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a native database dump covering virtually all patient-facing data domains in the gGastro application. The three deepest areas are:

**Billing & Claims (111 tables, 1,209 fields)**: Exceptionally deep. Covers the full billing lifecycle: charges, claims, superbills, claim snapshots, EDI claim payments and remittances (with 15+ sub-tables for adjudication detail), encounters, diagnoses per charge, modifiers, insurance, eligibility, authorizations, patient balances, statements, collections, payment plans, prepayments, online payments, cost estimations, ledger entries, and credit card processing. This is genuinely comprehensive billing data — not a summary but the full transactional model.

**Endoscopy / Procedures (53 tables, 861 fields)**: The core differentiator. The `Finding` table (155 fields) is the single largest entity in the export, reflecting the richness of endoscopic finding documentation. `Intervention` (115 fields) is the second largest. Additional tables cover procedure overviews, landmarks, sites reached/poorly visualized, instruments, anesthesia/sedation (administered medications, ASA class, Aldrete scores), nursing (complications, pain assessment, oxygen, IV setup/discontinuation, infusion sessions, NPO status, preparation), discharge instructions, and time markers. GI-specific disease tracking includes IBD classification (Montreal classification), disease scoring systems (AD8, HBI, MSI, PHQ9), and extra-intestinal manifestations. Quality registry exports (AGA, GIQuIC with 149 fields) are also included. Non-GI procedures (cardiology procedures, carotid ultrasound, nuclear perfusion, stress tests, transthoracic echo) are also present, suggesting the system is used for broader ambulatory procedural work.

**Patient / Demographics (93 tables, 847 fields)**: Comprehensive patient record including core demographics (`Patient` 30 fields, `Person` 36 fields), addresses, phone numbers, email, emergency contacts, employment, support persons, relatives, family history (members and diagnoses), social history (smoking, tobacco, alcohol, caffeine, drug, exercise, sexual, occupation), allergies (with history and review tracking), diagnoses (with history, review, and diagnostic study tracking), immunizations (with CVX codes), implantable devices, advance directives, functional/cognitive status, disease management, identifications, chart bookmarks/captures/notes, portal access, and SDOH-aware granular demographics (race, ethnicity, gender identity, tribal affiliation, self-disclosed disability).

**Medications (16 tables, 253 fields)**: Covers current medications, medication history, medication snapshots, medication warnings, medication diagnoses, prescriptions, prescription warnings, formulary warnings, prescription insurance, prescription samples, prescription signatures, prescription queue, inbound prescription queue, and renewal requests. This spans the full e-prescribing workflow.

**Encounters / Services (49 tables, 279 fields)**: Service records, service documents (with version tracking and signatures), clinical document sections, procedure components, referrals, staff assignments, CDA versions, and links between services.

**Other well-covered areas**: Lab interfaces (18 tables including requisitions, results, tests, test results, specimens), imaging/documents (18 tables), messaging/communications (direct messages, faxes, tasks, letters), scheduling (appointments, rounding lists, recalls), quality reporting (MIPS detail, coding advisors), telehealth, and patient portal interactions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (30 fields), `Person` (36 fields), `UsaAddress` (24), `Phone` (14), `Email` (10), `EmergencyContact`, `Employment`, `SupportPerson`, `Relative`, granular race/ethnicity/gender identity/tribal affiliation/disability tables | Thorough — includes USCDI v3 demographics plus social determinants |
| Encounters / visits | ✅ Covered | `Service` (36 fields), `ServiceDocument` (18), `ServiceDocumentVersion`, `ServiceDocumentSection`, `ServiceTimeMarker`, `ServiceStaff`, `Appointment` (38), `AppointmentSet` | Comprehensive encounter model with document versioning |
| Problems / conditions / diagnoses | ✅ Covered | `PatientDiagnosis` (21), `PatientDiagnosisHistory` (14), `PatientDiagnosisReview`, `PatientIllness` (18), `PatientIllnessHistory`, `PatientDisease`, `PatientDiseaseIBD` (14), `PatientMontrealClassification`, disease scoring systems | Deep — includes GI-specific disease tracking (IBD, Montreal classification) |
| Medications / prescriptions | ✅ Covered | `Medication` (41), `MedicationHistory` (44), `MedicationSnapshot`, `Prescription` (30), `PrescriptionInboundQueue` (44), `AdministeredMedication` (20), `RenewalRequest` (12), formulary/insurance/warning/sample tables | Full e-prescribing lifecycle including inbound Rx queues |
| Allergies | ✅ Covered | `PatientAllergy` (24), `PatientAllergyHistory`, `PatientAllergyReview` | Includes history and review tracking |
| Immunizations | ✅ Covered | `PatientImmunization` (38), `ExportImmunization`, `CvxCodePerPatientImmunization`, `Hl7SetValuePerPatientImmunization` | Thorough with CVX coding |
| Vitals | ✅ Covered | `VitalSigns` (27), `BloodPressure` (6), `VitalSignsMonitorSession` (16), `PhysicalMeasurement` (19) | Includes continuous monitoring data |
| Lab results | ✅ Covered | `InterfaceResult` (53), `InterfaceTest` (23), `InterfaceTestResult` (19), `InterfaceSpecimen`, `InterfaceRequisition` (17), plus 13 additional interface tables | Deep lab interface model covering requisitions through results |
| Imaging / diagnostic reports | ✅ Covered | `ImagingDocument` (38), `ImagingDocumentPage`, `ImagingDocumentNotes`, `ImagingDocumentSignature`, `PatientDiagnosticStudy`, `FindingImageService` | Includes documents, metadata, and signatures |
| Procedures | ✅ Covered | `Finding` (155), `Intervention` (115), `ProcedureOverview` (43), `ServiceProcedure` (14), `PatientProcedure`, `Instrument`, plus 40+ procedure-related tables | Exceptionally deep — the core strength of the product |
| Clinical notes / documents | ✅ Covered | `ServiceDocument` (18), `ServiceDocumentVersion`, `ServiceDocumentSection`, `ServiceDocumentSignature`, `Addendum` (11), `ChartNotes` (12), actual document files (MHT, PDF) | Includes structured data plus rendered documents |
| Care plans / goals | ⚠️ Partial | `Impression` (14), `GuidelineAction` (7), `GuidelineOverride` (10), `DischargeInstruction` (5) | No dedicated care plan entity; clinical decision support and discharge instructions present but no explicit CarePlan table |
| Orders / referrals | ✅ Covered | `Order` (50), `OrderNotes`, `OrderAUC`, `OrderPerImagingDocument`, `OrderPerInterfaceResult`, `ReferringPhysicianPerPatient`, `PhysicianStandingOrder` | Comprehensive including Appropriate Use Criteria |
| Insurance / coverage | ✅ Covered | `Insurance` (35), `BillingEligibility`, `BillingEligibilityEvent`, `Eligibility` (6), `EligibilityInsurance` (22), `EligibilityInsurancePatient` (13), `BillingPatientAuthorization`, `EligibilityFormulary` | Full insurance model with eligibility checking |
| Claims / billing | ✅ Covered | 111 billing tables, 1,209 fields total — `BillingClaimSnapshot` (95), `BillingSuperbill` (43), `BillingClaim` (16), `BillingCharge` (25), `BillingEncounter` (30), `BillingEdiClaimPayment` (22), plus sub-tables for modifiers, diagnoses, payments, adjustments | Exceptionally deep billing model — full claim lifecycle |
| Payments | ✅ Covered | `BillingPaymentAdjustmentRefund` (33), `BillingChargeTransaction`, `BillingOnlinePayment` (22), `BillingPatientPrepay` (21), `BillingCollectionPaymentPlan`, `BillingPatientLedger`, `CreditCardNotificationEvents` | Full payment/refund/collection model |
| Consents / directives | ✅ Covered | `PatientAdvancedDirectives`, `PatientDataRestrictionResponse` | Basic but present |
| Patient communications / portal messages | ✅ Covered | `PatientPortalMessage`, `PatientPortalMessageAttachment`, `PatientPortalDocument`, `PatientPortalUser`, `PatientPortalRegistration`, `PatientPortalAccessLog`, `PatientPortalRos`, `PatientPortalUpdateRequest`, `PatientPortalAlternateUser`, `PatientPortalChallenge`, 13+ portal tables total | Comprehensive portal model |
| Specialty-specific (GI) | ✅ Covered | `Finding` (155), `Intervention` (115), `GiquicExport` (149), `AgaService` (12), `PatientDiseaseIBD` (14), `PatientMontrealClassification`, disease scoring systems, endoscopy-specific nursing/anesthesia/procedure tables | The strongest area — this is a genuine GI-specialty export |

**Domains covered**: 18 of 18 applicable (with Care plans/goals rated partial)

## 6. Documentation Quality

**Strengths:**

- **Comprehensive scope**: 441 tables with 4,453 fields documented. This is one of the largest EHI data dictionaries by entity count.
- **Relationship documentation**: The Data Schema section provides a complete hierarchical tree of all table relationships with joining fields. This is critical for reconstructing the patient record from flat CSV files and is a feature many vendors omit.
- **Value sets**: 1,157 translation tables with 5,757 coded entries provide human-readable values for all coded fields. The additional 551-page PDF covers occupation/industry codes.
- **Document reconstruction**: Clear instructions with path templates and examples for reconstructing file paths to service documents, imaging documents, portal documents, and letters.
- **Versioning**: The specification is versioned (v6.5.3.20251230) and recently updated (December 2025), suggesting active maintenance.
- **Professional formatting**: Well-organized PDF with clear section divisions.

**Weaknesses:**

- **No field descriptions**: Zero of 4,453 fields have natural-language descriptions explaining what they mean. Field names are generally self-explanatory (e.g., `PatientId`, `DateOfOnset`, `IcdCode`) but some are opaque (e.g., `SystemClassName`, `ColumnNumber`, `ExportSIUStatus`, `AgentType`). A developer would need domain knowledge to interpret many fields.
- **No sample data**: No example export package is provided. A developer cannot see what actual exported data looks like.
- **No machine-readable schema**: The data dictionary is only available as a PDF. There is no JSON schema, XML schema, or other machine-readable format published by the vendor (the JSON extraction in the enrichment folder was created by the collection agent, not the vendor).
- **Limited type specificity**: Types are broad categories (GUID, Alphanumeric, Numeric, Boolean, Date & Time, Decimal, Score) rather than precise database types. Length is documented for only 23% of fields.
- **Export mechanism unclear**: The documentation describes the export package format but not how to initiate an export — there are no screenshots, API endpoints, or user instructions.

**Could a developer build an import?** Partially. The table structures, relationships, and value sets provide enough information to parse the CSV files and reconstruct the relational model. However, the absence of field descriptions means a developer would need to guess the semantics of ambiguous fields. The document file path reconstruction instructions are clear and actionable. Overall, a competent developer with healthcare domain knowledge could build a working import, but it would require significant effort to interpret field meanings.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native database model export — not a C-CDA or FHIR repackaging. The 441 CSV tables map directly to the application's internal data model, covering clinical, billing, procedural, and patient engagement domains in depth. The export includes data that would never appear in a FHIR or C-CDA representation (e.g., claim snapshot details, EDI payment adjudication, kiosk snapshots, coding advisor data, fax queues). The documentation, while lacking field descriptions, is structurally complete with relationships and value sets.

### Key Findings

1. **Exceptionally deep endoscopy/procedure data**: The `Finding` table (155 fields) and `Intervention` table (115 fields) are the two largest entities in the export, reflecting gGastro's core strength. The `GiquicExport` table (149 fields) for GI quality registry data is similarly detailed. This level of specialty-specific clinical data depth is rare among EHI exports.

2. **Genuinely comprehensive billing model**: With 111 billing-related tables and 1,209 fields (27% of all fields), billing is the largest single domain. The model covers the full billing lifecycle from superbill creation through claim submission, EDI remittance processing, payment posting, collections, and patient statements. This is not a billing summary — it's the complete transactional model.

3. **Strong relational documentation**: The 574-relationship Data Schema tree, rooted at `Patient` with 146 direct children, provides explicit foreign key documentation that enables full record reconstruction. Many vendors export flat files with no relationship documentation.

4. **No field-level descriptions**: Despite 4,453 fields across 441 tables, not a single field has a natural-language description. Field names are the only semantic cue. This is a meaningful documentation gap for a data dictionary of this size.

5. **No sample data or machine-readable schema**: The absence of sample export files and machine-readable schemas (JSON/XML) means developers must work entirely from the PDF specification with no way to validate their parsing against expected output.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (one file per table) + document files (MHT, PDF, JPG)
Model type:      Native database
Entities:        441
Fields:          4,453
Descriptions:    0% (no field descriptions)
Sample data:     No
Bulk export:     No (single-patient)
Domains covered: 17.5 of 18 applicable (care plans partially covered)
```

### Bottom Line

gGastro's EHI export is one of the most comprehensive native database exports encountered. With 441 tables, 4,453 fields, 574 documented relationships, and 1,157 value sets spanning clinical, billing, and specialty GI domains, a patient or provider would receive a genuinely complete copy of their data. The single biggest weakness is the complete absence of field-level descriptions — the data dictionary tells you *what* is exported (field names, types, relationships) but never explains *what it means*. Despite this documentation gap, the structural completeness, relationship documentation, and deep coverage of billing and GI-specialty data make this a strong (b)(10) implementation.
