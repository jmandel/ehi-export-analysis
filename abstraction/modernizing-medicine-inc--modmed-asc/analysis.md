# EHI Export Analysis: Modernizing Medicine Inc.

**Product**: ModMed ASC (version 6)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2002.mASC.06.11.0.250902

## 1. Product Context

ModMed ASC is a cloud-based EHR platform purpose-built for ambulatory surgery centers (ASCs), primarily serving ophthalmology and gastroenterology ASCs. Built on the gGastro platform, it provides:

- **Surgical documentation & charting**: Pre-op, intra-op, post-op nursing documentation; anesthesia notes; operative/procedure reports; endoscopy reports; concurrent charting for multiple roles
- **Billing & revenue cycle**: Integrated billing for professional, office, ASC, and facility charges; claims scrubbing; insurance eligibility; EDI transactions; payment processing
- **Scheduling**: Surgical case scheduling with cost estimates
- **Lab integration**: Electronic lab orders and results
- **Patient portal** (gPortal): Messaging, appointment management, document access
- **Quality reporting**: ASC Quality Reporting (ASCQR), GIQuIC for GI, OAS CAHPS
- **Specialty-specific clinical data**: GI findings/impressions/colonoscopy data, ophthalmology lens data, cardiology procedures (TTE, stress tests, nuclear perfusion)
- **E-prescribing**: Surescripts-certified prescriptions
- **Direct messaging**: Secure clinical messaging via Direct Trust
- **Telehealth**: Session management

The product stores patient demographics, medical/social history, insurance data, surgical schedules, consent forms, medications, anesthesia documentation, nursing notes, procedure reports, vital signs, imaging data, findings/diagnoses, discharge records, billing data (claims, charges, payments), quality measures, portal content, referrals, and correspondence.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `gGastro-EHI-Patient-Export-Specifications-Dec2025.pdf` (14.4 MB, 167 pp) | Primary data dictionary, version 6.5.3.20251230. Defines all CSV entities with field-level specifications. **Most informative artifact.** | ⭐⭐⭐ |
| `gGastro-Patient-Export-Specifications.pdf` (2.3 MB, 168 pp) | Earlier version of the same data dictionary, version 6.4.4.20250707, linked from the ASC certification page. Same ~442 entities. | ⭐⭐ (redundant with above) |
| `gGastro-EHI-Patient-Export-Specifications-Additional.pdf` (16.9 MB, 551 pp) | Supplementary translation/value set document. Contains extended reference data including thousands of occupation codes (SOC mapping), providing complete value sets for coded fields. | ⭐⭐ |
| `ASC-Mandatory-Disclosures.pdf` (149 KB, 5 pp) | Describes ModMed ASC capabilities, costs, contractual and technical requirements. Confirms product capabilities. | ⭐ |
| `ModMed-ASC-Certification.pdf` (331 KB, 1 p) | Drummond Group compliance certificate for ModMed ASC 6, certified 09/02/2025. | ⭐ |
| `screenshot-asc-onc-certification-fullpage.png` | Full-page screenshot of the ASC ONC Certification page. | ⭐ |

## 3. Export Mechanics

- **Format**: CSV files, one file per entity/table, with GUID-based primary and foreign keys
- **Mechanism**: The documentation describes an "EHI Patient Export" package. The ASC certification page provides the data dictionary under "EHI Export Documentation." The mandatory disclosures do not specify a separate fee for EHI export. Exact UI mechanism is not documented in the available artifacts.
- **Single-patient vs bulk**: The title "Patient Export Specifications" and the data schema rooted at "Patient" indicate a single-patient export model.
- **Access constraints**: No specific fees mentioned for EHI export. The system requires ModMed ASC EHR subscription.
- **Binary document support**: The export includes binary documents (service documents, imaging documents, portal documents, statements, letters) with documented reconstruction paths for file pointers.

## 4. Export Content: What's In It

### Data Dictionary Overview

The data dictionary (version 6.5.3.20251230, 167 pages) is organized into five sections:

1. **CSV Files Dictionary** (pp 1–87): Defines 442 CSV entities with field-level detail
2. **Data Schema** (pp 88–95): Hierarchical tree showing parent-child relationships between all tables, rooted at "Patient," with 441 unique entity names
3. **Translations** (pp ~96–162): Value set lookup tables for coded fields across ~150 unique translation table references
4. **Patient Documents** (pp ~163–166): Instructions for reconstructing file paths for 5 document types (Service Documents, Imaging Documents, Patient Portal Documents, Statements, Letters)
5. **Glossary** (p 167): Definitions of 9 data types (Alphanumeric, Boolean, Date, Date & Time, Decimal, GUID, Numeric, Time, XML)

### Field Documentation Quality

For each field, the dictionary provides:
- **Column position**: ✅ Always present
- **Field name**: ✅ Always present
- **Data type**: ✅ Always present (GUID: 1362, Alphanumeric: 1298, Numeric: 642, Boolean: 486, Date & Time: 387, Decimal: 243, Date: 11, XML: 11, Time: 4)
- **Max length**: Present for applicable Alphanumeric fields
- **Format/Translation references**: Present for GUIDs (format pattern), dates (format pattern), booleans (0/1 mapping), and coded fields (translation table names)
- **Prose descriptions**: Not present. Fields are documented by name, type, and format/translation reference only. No natural-language descriptions of what fields mean.

Field names are generally self-documenting (e.g., `PatientId`, `ServiceDate`, `ColonoscopyIndication`, `ScoreRespiration`), and coded fields point to named translation tables (e.g., "Service Components Aldrete Activity Score," "Billing Claim Type").

### Vendor's Content Organization

The CSV entities, categorized by their naming patterns and domain:

| Category | Entities | Fields | Key Examples |
|---|---|---|---|
| Billing/Financial | 113 | 1,247 | BillingClaimSnapshot (95), BillingSuperbill (43), BillingPatientStatementHistory (43), BillingCharge (25), BillingPaymentAdjustmentRefund (33) |
| Procedures/Services | 56 | 480 | Intervention (115), ProcedureOverview (43), Service (36), ServiceProcedure (14), Prescription (30) |
| Patient Demographics/History | 49 | 457 | Person (36), Patient (30), PatientSocialHistory (11), PatientTobaccoHistory (14), PatientAlcoholHistory (15) |
| Documents | 30 | 220 | ImagingDocument (38), ServiceDocument (18), PatientPortalDocument (19), PatientCcdaDocument (11) |
| Scheduling | 27 | 194 | Appointment (38), AppointmentSet (6), AppointmentReminderEventLog (11) |
| Diagnoses/Problems | 21 | 172 | PatientDiagnosis (21), Condition (24), PatientDiagnosisHistory (14) |
| Lab/Results | 19 | 200 | InterfaceResult (53), InterfaceTest (23), InterfaceTestResult (19), InterfaceSpecimen (8) |
| Clinical Documentation | 17 | 129 | ChartNotes (12), QuestionnaireResponse (8), AscQualityMeasures (7) |
| Portal/Telehealth | 16 | 108 | PatientPortalMessage (23), PatientPortalAccessLog (13), PatientPortalUser (8), TelehealthService (2) |
| Medications/Prescriptions | 14 | 177 | MedicationHistory (44), Medication (41), PrescriptionInboundQueue (44), Prescription (30) |
| Nursing/ASC Operations | 14 | 114 | InfusionSession (16), LimitationComplication (14), Oxygen (12), IvFluid (11) |
| GI-Specific | 10 | 311 | Finding (155), GiquicExport (100), Impression (14), AgaService (13) |
| Cardiology | 8 | 112 | Tte (41), StressTest (19), NuclearPerfusion (14) |
| Insurance/Coverage | 7 | 92 | Insurance (35), EligibilityInsurance (22), BillingPatientAuthorization (16) |
| Orders | 7 | 83 | Order (50), OrderNotes (5), OrderAUC (6) |
| Immunizations | 4 | 51 | PatientImmunization (38), ExportImmunization (5) |
| Communications | 5 | 39 | DirectMessage (18), DirectMessageAttachment (8), DirectMessageRecipient (8) |
| Vital Signs | 5 | 80 | VitalSigns (27), VitalSignsMonitorSession (16), BloodPressure (6) |
| Tasks/Workflow | 5 | 40 | Task (15), TaskAttachment (8), TaskRecipient (8) |
| Allergies | 3 | 39 | PatientAllergy (24), PatientAllergyHistory (9), PatientAllergyReview (6) |
| Clinical Guidelines | 2 | 17 | GuidelineOverride (10), GuidelineAction (7) |
| Ophthalmology | 2 | 8 | ServiceProcedureOphthalmologyLens (7), ServiceProcedureOphthalmology (1) |
| Other | 6 | 48 | CodingAdvisor (29), Interval (39), Side (18) |
| Reporting/Export | 1 | 6 | ServiceExport (11) |
| **Total** | **442** | **4,446** | |

The full entity inventory with all fields is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is exceptionally broad, reflecting what appears to be a near-complete database dump rather than a curated subset. Key observations:

- **Billing/Financial is the largest domain** at 113 entities and 1,247 fields — this alone represents 28% of all fields. It includes deep coverage of claims, charges, payments, adjustments, EDI transactions, superbills, patient statements, collection workflows, prepayments, online payments, credit card processing, and fee schedules.
- **Procedures/Services** (56 entities, 480 fields) covers the clinical service model comprehensively: service records, procedure coding, CPT codes, procedure overviews, interventions, anesthesia (Aldrete scores, complications), surgical site documentation, and service-linked documents.
- **Patient Demographics/History** (49 entities, 457 fields) goes well beyond basic demographics into social history, tobacco/alcohol/drug/caffeine history, sexual history, exercise history, occupation history, contraceptive history, family member history, advance directives, implantable devices, and disease scoring systems (PHQ-9, AD8, HBI for IBD, Montreal classification).
- **GI-Specific data** (10 entities, 311 fields) includes the massive Finding entity (155 fields — the largest single entity) with detailed polyp/lesion characterization, the GiquicExport entity (100 fields for GI quality registry), and AGA registry data.
- **Cardiology** (8 entities, 112 fields) covers TTE (echocardiography, 41 fields), stress tests, nuclear perfusion studies, carotid ultrasound, and HeartCentrix integration.
- **Ophthalmology** is thin (2 entities, 8 fields) — just lens data and a single-field ophthalmology procedure marker. This likely reflects that the ophthalmology-specific documentation lives more in the EMA EHR than in the gGastro/ASC platform.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (30 fields), `Person` (36 fields), `EmergencyContact`, `Employment`, `UsaAddress` (22 fields), `Phone` (14 fields), `Email` (10 fields), race/ethnicity/tribal granularity entities | Thorough; includes granular race/ethnicity, gender identity, tribal affiliation |
| Encounters / visits | ✅ Covered | `Service` (36 fields), `BillingEncounter` (30 fields), `ServiceVisit`, `ServiceTimeMarker`, `Appointment` (38 fields) | Comprehensive with scheduling, visit tracking, and billing encounter linkage |
| Problems / conditions / diagnoses | ✅ Covered | `PatientDiagnosis` (21 fields), `Condition` (24 fields), `PatientDiagnosisHistory` (14 fields), `PatientDisease` with IBD-specific entities, disease scoring systems (PHQ-9, AD8, HBI) | Deep; includes disease tracking, scoring systems, and diagnosis history |
| Medications / prescriptions | ✅ Covered | `Medication` (41 fields), `MedicationHistory` (44 fields), `Prescription` (30 fields), `PrescriptionInboundQueue` (44 fields), `AdministeredMedication` (20 fields), `MedicationSnapshot`, `MedicationWarning`, `PrescriptionSig` | Very thorough; includes administered meds, warnings, formulary data, renewal requests |
| Allergies | ✅ Covered | `PatientAllergy` (24 fields), `PatientAllergyHistory` (9 fields), `PatientAllergyReview` (6 fields), `MedicationDiagnosis` | Good coverage including history and review tracking |
| Immunizations | ✅ Covered | `PatientImmunization` (38 fields), `ExportImmunization`, `CvxCodePerPatientImmunization`, `Hl7SetValuePerPatientImmunization` | Thorough with CVX coding and HL7 value sets |
| Vitals | ✅ Covered | `VitalSigns` (27 fields), `VitalSignsMonitorSession` (16 fields), `BloodPressure` (6 fields), `PhysicalMeasurement` (19 fields) | Strong; includes monitor session data for ASC vital signs monitoring |
| Lab results | ✅ Covered | `InterfaceResult` (53 fields), `InterfaceTest` (23 fields), `InterfaceTestResult` (19 fields), `InterfaceSpecimen` (8 fields), `InterfaceResultPathology` (16 fields), `InterfaceLab` (13 fields) | Comprehensive with pathology results, specimen tracking, and lab director data |
| Imaging / diagnostic reports | ✅ Covered | `ImagingDocument` (38 fields), `ImagingService` (22 fields), `ImagingDocumentPage`, `PatientDiagnosticStudy` (23 fields) | Good; includes document pages and diagnostic study tracking |
| Procedures | ✅ Covered | `ServiceProcedure` (14 fields), `ProcedureOverview` (43 fields), `Intervention` (115 fields), `Finding` (155 fields), `ProcedureCodingProcedure`, `ProcedureCodingDiagnosis` | Exceptionally deep for GI/endoscopy; includes finding-level detail |
| Clinical notes / documents | ✅ Covered | `ServiceDocument` (18 fields), `ServiceDocumentVersion` (8 fields), `Addendum` (11 fields), `ChartNotes` (12 fields), `ServiceNotes`, with binary document reconstruction | Strong; includes versioned documents and reconstruction paths |
| Care plans / goals | ⚠️ Partial | `PatientAdvancedDirectives` (5 fields), `GuidelineAction` (7 fields), `GuidelineOverride` (10 fields) | No explicit care plan entity; guidelines and directives present but limited |
| Orders / referrals | ✅ Covered | `Order` (50 fields), `OrderNotes`, `OrderAUC`, `InterfaceRequisition`, `ReferringPhysicianPerPatient`, `ServiceReferringPhysician` | Good; includes AUC (appropriate use criteria) for imaging orders |
| Insurance / coverage | ✅ Covered | `Insurance` (35 fields), `EligibilityInsurance` (22 fields), `Eligibility` (6 fields), `BillingPatientAuthorization` (16 fields), `PrescriptionInsurance`, `BillingPatientBillingInformation` (15 fields) | Very thorough including eligibility, authorizations, and prescription insurance |
| Claims / billing | ✅ Covered | 113 billing entities (1,247 fields): `BillingClaimSnapshot` (95 fields), `BillingClaim`, `BillingClaimEvent`, EDI claim payment hierarchy (12 entities), `BillingEncounter`, `BillingSuperbill` (43 fields) | **Exceptionally deep**; full claims lifecycle with EDI payment details, scrubbing results, claim snapshots |
| Payments | ✅ Covered | `BillingPaymentAdjustmentRefund` (33 fields), `BillingChargeTransaction` (16 fields), `BillingOnlinePayment` (18 fields), `BillingPatientPrepay` (21 fields), `BillingCollectionPaymentPlan` (12 fields) | Comprehensive including payment plans, adjustments, refunds, online payments |
| Consents / directives | ⚠️ Partial | `PatientAdvancedDirectives` (5 fields), `PatientDataRestrictionResponse` (5 fields) | Advance directives present but no dedicated consent form entity |
| Patient communications / portal messages | ✅ Covered | `PatientPortalMessage` (23 fields), `PatientPortalMessageAttachment`, `DirectMessage` (18 fields), `DirectMessageAttachment`, `PatientPortalUpdateRequest` (14 fields), `PatientPortalAccessLog` (13 fields) | Strong; includes portal messages, direct messages, portal access logging |
| Specialty-specific: GI | ✅ Covered | `Finding` (155 fields), `GiquicExport` (100 fields), `Impression` (14 fields), `AgaService` (13 fields), `FindingCode`, `FindingSite`, `FindingSegments` | **Exceptional depth** — the Finding entity alone captures detailed polyp/lesion characterization |
| Specialty-specific: Cardiology | ✅ Covered | `Tte` (41 fields), `StressTest` (19 fields), `NuclearPerfusion` (14 fields), `CarotidUltrasound`, `HeartCentrix` | Good specialty coverage |
| Specialty-specific: Ophthalmology | ⚠️ Partial | `ServiceProcedureOphthalmology` (1 field), `ServiceProcedureOphthalmologyLens` (7 fields) | Thin; likely most ophthalmic data resides in the EMA EHR rather than the gGastro/ASC platform |
| Anesthesia documentation | ✅ Covered | `AldreteScore` (14 fields), `AnesthesiaComplication` (8 fields), `AsaClass` (6 fields), `AdministeredMedication` (20 fields), anesthesia-related vital signs | ASC-appropriate; includes Aldrete scoring, ASA classification, complications |
| Nursing documentation | ✅ Covered | `NursingComplication`, `PainAssessment`, `Oxygen`, `IvFluid`, `IvSetup`, `IvDiscontinued`, `Npo`, `Preparation`, `DischargeInstruction`, `InfusionSession` | Good ASC nursing workflow coverage |

## 6. Documentation Quality

**Strengths:**
- **Complete entity and field enumeration**: Every CSV file and every field is documented with position, name, type, and max length — a developer knows exactly what to expect in each file
- **Full relational schema**: The Data Schema section provides a complete tree view of parent-child relationships with foreign key field names, enabling proper record reconstruction
- **Translation tables**: Coded fields reference named translation tables with complete value mappings, enabling developers to decode numeric codes to human-readable values
- **Binary document reconstruction**: Clear instructions for reconstructing file paths for 5 document types with examples
- **Versioning**: Documents are versioned (6.5.3.20251230) indicating active maintenance
- **Supplementary value sets**: The 551-page Additional document provides extended reference data (e.g., thousands of occupation codes mapped to SOC classifications)

**Weaknesses:**
- **No prose field descriptions**: Fields have names, types, and format references, but no natural-language descriptions explaining what they mean. A developer must infer meaning from field names alone (e.g., `PatientCondition` references "Billing Superbill Additional Patient Condition" translation table but doesn't explain what this field represents clinically)
- **No sample data**: No example CSV files or sample records are provided
- **No machine-readable schema**: The data dictionary is a PDF only — no JSON schema, SQL DDL, or other machine-parseable format
- **Field naming conventions**: Generally clear PascalCase names, but some are cryptic (e.g., `ExportSIUStatus`, `Dysplastic`, `Side`)

**Could a developer build an import from this documentation?** Yes, with significant effort. The field positions, types, lengths, and relationships are sufficient to parse the CSV files correctly. The translation tables enable decoding coded values. However, the lack of prose descriptions means a developer would need domain expertise (or access to the application) to understand the semantic meaning of many fields. The documentation is structurally complete but semantically thin.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the full breadth of data domains that ModMed ASC stores. The 442 entities and 4,446 fields span clinical documentation, billing/financial (113 entities — an extraordinary depth), medications, labs, imaging, scheduling, patient portal, specialty-specific GI/cardiology data, nursing operations, quality reporting, and more. The billing coverage alone (1,247 fields across claims, charges, payments, adjustments, EDI transactions, statements, collections) goes far beyond USCDI. The specialty GI data (Finding with 155 fields, GiquicExport with 100 fields) represents the kind of deep, product-specific clinical data that USCDI doesn't address. This is clearly a database-level export, not a clinical summary repackaged.

The only notable thinness is ophthalmology (2 entities, 8 fields), which likely reflects the platform architecture — ModMed ASC is built on gGastro, so GI data is deeply embedded while ophthalmology data may live primarily in the EMA EHR for ophthalmology practices.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built EHI export. The evidence:
- The export uses a proprietary CSV format with the vendor's native data model (not FHIR, not C-CDA)
- 442 entities vastly exceeds what any clinical exchange standard provides
- The export includes 113 billing/financial entities, which are completely absent from USCDI/(g)(10)
- The data schema shows the full relational model of the underlying database
- The export is distinct from their FHIR API (documented separately at portal.api.modmed.com)
- The data dictionary is titled "gGastro EHI Patient Export Specifications" — purpose-titled for (b)(10)
- The certification page separates "EHI Export Documentation" from the FHIR API documentation
- Binary document reconstruction instructions indicate the export includes actual document files, not just metadata

### Key Findings

1. **Exceptionally deep billing coverage**: 113 billing/financial entities with 1,247 fields represent the most thorough billing data export among typical (b)(10) implementations. Full claims lifecycle including EDI payment details, adjustment codes, collection workflows, and payment plan tracking.

2. **Deep specialty clinical data**: The GI-specific Finding entity (155 fields) captures detailed polyp/lesion characterization at a level that no standard export format addresses. GiquicExport (100 fields) provides registry-quality data. Cardiology entities cover TTE, stress testing, and nuclear perfusion.

3. **Complete relational schema**: The Data Schema section documents all parent-child relationships with explicit foreign key fields, enabling proper record reconstruction — a critical feature many vendors omit.

4. **No prose field descriptions**: While structurally complete, the data dictionary lacks natural-language descriptions of what fields mean. All 4,446 fields are documented by name, type, and format/translation reference only.

5. **Platform architecture note**: ModMed ASC and gGastro share the same underlying data model and export mechanism. The ASC certification page links to the gGastro export specification. Both versions (v6.4.4 on ASC page, v6.5.3 on gGastro page) document essentially the same ~442 entities.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (one file per entity, plus binary documents)
Entities:        442
Fields:          4,446
Descriptions:    0% prose descriptions; 100% have type+format; ~150 translation table references for coded fields
Sample data:     No
Bulk export:     Unclear (appears to be single-patient)
Domains covered: 19 of 21 applicable domains (care plans and consent forms are partial)
```

### Bottom Line

ModMed ASC provides one of the more thorough (b)(10) EHI export implementations: 442 CSV entities covering 4,446 fields across clinical, billing, scheduling, specialty, and operational domains. The 113 billing entities alone demonstrate genuine engagement with the EHI mandate beyond repackaging USCDI. The main limitation is the absence of prose field descriptions — a developer gets complete structural documentation but must infer semantic meaning from field names and translation table references.
