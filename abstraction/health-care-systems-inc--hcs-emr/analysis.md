# EHI Export Analysis: Health Care Systems, Inc.

**Product**: HCS eMR v10
**Analysis date**: 2026-02-15
**CHPL ID**: 15.99.04.1582.HC01.10.02.1.231220 (CHPL #11416)

## 1. Product Context

Health Care Systems, Inc. (HCS) is a behavioral health EHR vendor founded in 1983, headquartered in Montgomery, Alabama. HCS eMR is a **comprehensive behavioral health electronic medical record** designed for inpatient psychiatric hospitals, residential treatment centers, substance use disorder programs, and correctional healthcare facilities. Major customers include UHS, Acadia Healthcare, HCA Healthcare, LifePoint Behavioral Health, and other large behavioral health chains.

The product is a fully integrated suite comprising seven modules:

1. **Behavioral Record** (core clinical EMR) — intake, assessments (50+ standardized tools including ASAM, PHQ-9, C-SSRS), treatment planning, group therapy notes, patient safety rounds, patient portal
2. **Call Center CRM** — pre-admission screening, referral management, patient engagement
3. **Revenue Cycle Management** — eligibility verification, charge capture, claims, denials, payments, ERA processing
4. **Order Management (CPOE)** — medication, lab, radiology, and task orders
5. **Medication Management** — eMAR with barcode scanning, ePrescribing (EPCS), pharmacy information system, MAT
6. **Patient Safety** — electronic observation rounding (patented), proximity beacons, clinical decision support
7. **Compliance Toolkit** — IPFQR quality reporting, credentialing, chart review, regulatory monitoring

Certified for 40+ ONC criteria including (b)(10) EHI export. For a complete EHI export, one would expect coverage of: demographics, encounters, diagnoses/problems, medications, medication administration, allergies, observations/vitals/assessments (especially the 50+ behavioral health instruments), treatment plans, clinical notes, billing/charges/claims, insurance, payments, consent, immunizations, devices, and documents.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `HCSDataDictionary.csv` (254 KB, 4,557 lines) | CSV data dictionary documenting 339 database tables and 3,878 columns with table name, column name, SQL data type, size, and description | **Most informative** — the core artifact for assessing export completeness |
| `EHIExportInstructionsHCSeMRv10.pdf` (609 KB, 2 pages, scanned) | Scanned instructions document covering export overview, user access, step-by-step instructions, UI screenshot, and attestation signed by Reubin Felkey (12/19/2023) | **Highly informative** — confirms export mechanics, scope statement, and attestation |
| `meaningful-use-page.png` (438 KB) | Screenshot of https://www.hcsinc.net/meaningful-use/ showing EHI Export section with download links and mandatory disclosures | **Moderately informative** — confirms public availability and attestation text |
| `hcsinc-403-page.png` (169 KB) | Screenshot of 403 error page returned by anti-bot protection | Not informative for export analysis |

**Note**: The vendor's website (hcsinc.net) blocks programmatic access with HTTP 403 for curl/non-browser clients (confirmed still returning 403 as of 2026-02-15). The artifacts were originally downloaded via browser-based access.

## 3. Export Mechanics

- **Format**: ZIP file containing one CSV file per database table, plus a readme file with a hyperlink to the current data dictionary
- **Mechanism**: Built-in UI function at System → EHI Export. Uses the product's standard Patient Selection interface with 20+ filter options (by date range, patient set, admit/discharge date, class, staff assignment, etc.)
- **Single-patient vs bulk**: Both — users can select a single patient by Visit Identifier or groups of patients using various filter criteria (date ranges, patient sets, active patients, discharge ranges, etc.)
- **Access**: Available to "Corporate Users" (typically administrators and analysts); configurable via Active Directory; defaults to on
- **Cost**: No additional charge — built into HCS eMR
- **Vendor assistance**: Not required — users can export autonomously without contacting HCS Support or Developers
- **Real-time**: Exports occur in real time
- **Key attestation statement** (from PDF page 2): *"The files exported as part of the HCS EHI Export contain all necessary data, including that which is not strictly personal health information, to allow the creation of a complete and fully usable HCS database with only the patient(s) that the users chose to export."*

## 4. Export Content: What's In It

### Data dictionary structure

The data dictionary (`HCSDataDictionary.csv`) documents **339 tables** with **3,878 fields**. Every field has:

- **Table name**: ✅ Present for all 3,878 fields
- **Column name**: ✅ Present for all 3,878 fields
- **SQL data type**: ✅ Present for all 3,878 fields (14 distinct types: varchar, bigint, int, bool, datetime, decimal, bit, varbinary, char, numeric, time, nvarchar, geography, tinyint)
- **Size constraints**: ✅ Present where applicable (e.g., `varchar(1000)`, `decimal(15,5)`)
- **Descriptions**: ✅ Present for all 3,878 fields (100%), but quality is limited — see below

**Description quality breakdown** (from scripted analysis):

| Description Type | Count | % |
|---|---|---|
| Trivial (column name re-spaced, e.g., `RowVersionNumber` → "Row Version Number") | 2,760 | 71.2% |
| FK reference (e.g., "Reference to PatientVisit") | 730 | 18.8% |
| ID field (e.g., "ID for Patient") | 290 | 7.5% |
| Other/meaningful | 98 | 2.5% |

Every field has a description, but **71% are trivial** — just the CamelCase column name with spaces inserted. The FK references (19%) are structurally useful for reconstructing relationships but don't explain semantics. Only ~2.5% of descriptions add information beyond what the column name already conveys.

**Foreign key relationships**: 730 FK references documented across 298 distinct target tables. Relationships are expressed as text ("Reference to [TableName]") in the description column rather than as machine-parseable constraints.

### Data type distribution

| Type | Count | % |
|---|---|---|
| varchar | 1,374 | 35.4% |
| bigint | 1,040 | 26.8% |
| int | 590 | 15.2% |
| bool | 352 | 9.1% |
| datetime | 318 | 8.2% |
| decimal | 127 | 3.3% |
| varbinary | 23 | 0.6% |
| Other (bit, char, numeric, time, nvarchar, geography, tinyint) | 54 | 1.4% |

### Vendor's own content organization

The data dictionary uses table names as its organizational structure (no explicit category groupings from the vendor). Based on systematic analysis of all 339 table names and their contents, here is the domain breakdown:

| Domain | Tables | Fields | Representative Tables |
|---|---|---|---|
| Pharmacy / Drug Products | 61 | 516 | DispensableProduct, RoutedProduct, PackagedProduct, NamedProduct, ProductSubstitution, ProductInteraction |
| Orders / Medications | 30 | 438 | PatientOrder (143 cols), OrderItem (30), HCS_MedList (27), MedRecItem (29), OrderSet (13) |
| Observations / Vitals / Labs / Assessments | 14 | 413 | Observation (88 cols), ObservationGroup (62), ObservationGroupItem (71), VisitObservation (46), VisitObservationSet (58) |
| Staff / Providers | 21 | 201 | Staff (80 cols), StaffAddress, StaffFacility, StaffSpecialty, StaffPractitionerID |
| Work Queues / Tasks | 21 | 187 | T_WORKQUEUE (19), T_WQ_ITEM (22), WorkTask (19), V_WQ_ITEM (30) |
| Facilities / Locations / Config | 14 | 157 | Facility (29), FacilityLocation, FacilityPCU, Unit, UnitBed, Location |
| Billing / Charges / Claims | 8 | 147 | VisitCharge (60 cols), ChargeClaim (40), PatientClaimResponse (12), VisitDispense (12) |
| PBM / Formulary | 12 | 139 | PBMFormularyAlternative, PBMCoveragePlan, CoverageProduct, CoverageProductStep, EligibilityPBMResponse (36) |
| Reporting / Metrics | 13 | 137 | Metric (18), MetricValue (10), Measure (10), ReportSet (13), PerformanceMetricValue (13) |
| Patient Demographics & Identity | 13 | 121 | Patient (37 cols), PatientAddress, PatientContact, PatientIdentifier, PatientRace, PatientAlias, PatientRelation |
| Patient Lists / Sets | 10 | 119 | PatientListCriteria (51), PatientSet (13), PatientSetVisit (10) |
| Encounters / Visits | 11 | 114 | PatientVisit (48 cols), VisitTransfer (11), VisitStaff (9), VisitIdentifier (6) |
| Diagnoses / Problems / Conditions | 7 | 108 | Condition (31), VisitDiagnosis (13), VisitProblem (19), VisitCondition (13) |
| Insurance / Coverage | 8 | 106 | PatientInsuranceCoverage (27), InsuranceCompany (24), VisitInsuranceAuthorization, VisitEligibilityQuery |
| Medication Administration (MAR) | 6 | 83 | TherapyAdmin (45 cols), AdminProduct (18), AdminVolume (8), AdminComponent, AdminField |
| System Configuration | 10 | 76 | UserDefinedField (16), DisplaySection (11), MenuItem (19), SQLModifier (7) |
| HL7 / Interface Config | 6 | 77 | HL7Table (13), HL7TableValue (16), ExternalInterface (15), FileToProcess (26) |
| Rules Engine | 5 | 77 | RuleInfo (29), RuleAction (29), RuleTrigger (9) |
| Scheduling / Events | 11 | 75 | Event, EventOccurrence, EventItem, CalendarDay, EventLocation, EventStaff, EventVisit |
| Safety / Clinical Alerts | 5 | 69 | ClinicalAlert (21), ClinicalRelationship (24), VisitPhysicalLocation (8), NearMiss (11) |
| Care Plans / Treatment Planning | 6 | 68 | VisitIntervention (33), InterventionStatus (12), InterventionActivity (6), VisitCarePlan (4), VisitConcern (8) |
| Clinical Notes / Documents | 7 | 57 | PatientDocument (16), VisitDocument (19), VisitNote (7), ConsentDocument (4), DocumentPendingSignature |
| Consent | 2 | 46 | PatientConsent (23), VisitConsent (23) |
| Messaging / Communications | 6 | 39 | Chat, ChatMessage, ChatStaff, MailMessage (13), MessageAttachment |
| Discharge / Instructions | 4 | 39 | VisitInstruction (14), Instruction (16), InstructionSet (5) |
| Transaction Logging | 3 | 39 | TransactionLogAction (29), LogLine (7), TextLog (3) |
| Frequency Definitions | 5 | 38 | Frequency (17), FrequencyAdminTime (7), FrequencySet |
| Authorization / Roles | 4 | 21 | AuthorizationRole, AuthorizationAction, RoleAuthorizationArea |
| Allergies | 1 | 20 | PatientAllergy (20 cols) |
| Immunizations | 3 | 19 | VisitImmunizationQuery (11), ImmunizationQueryForecast, ImmunizationQueryHistory |
| Patient Devices | 2 | 19 | PatientDevice (13), DeviceIdentifier (6) |
| Procedures | 1 | 18 | VisitProcedure (18 cols) |
| Public Health Reporting | 2 | 14 | AUBatch, AUBatchReport |
| Payments | 1 | 12 | Payment (12 cols) |
| Family History | 1 | 9 | PatientFamilyHistoryItem (9 cols) |
| Images | 1 | 11 | NamedImage |

The full entity inventory (all 339 tables with all columns) is saved to `analysis/full-entity-inventory.json`.

### Notable tables: the largest and most detailed

| Table | Cols | Description |
|---|---|---|
| PatientOrder | 143 | Comprehensive order record — medications, labs, radiology, tasks. Includes dosing, frequency, route, prescriber, status, refills, DAW codes, controlled substance info, ePrescribe data |
| Observation | 88 | Observation definition table — value types, ranges, formulas, validation, image markup, multi-select configs. This is the template for all clinical observations including behavioral health assessments |
| Staff | 80 | Provider/staff record — credentials, NPI, DEA, specialties, contact info, facility assignments |
| ObservationGroupItem | 71 | Individual items within observation groups (assessment tool questions/items) |
| ObservationGroup | 62 | Observation group definitions (assessment instruments, panel definitions) |
| VisitCharge | 60 | Charge records with CPT/HCPCS codes, revenue codes, NDC, amounts, modifiers, diagnosis pointers |
| VisitObservationSet | 58 | Observation sets with specimen collection, result timing, status |
| PatientVisit | 48 | Visit/encounter record — admission, discharge, class, bed, attending, diagnosis references |
| VisitObservation | 46 | Patient-specific observation values — the actual recorded clinical data |
| TherapyAdmin | 45 | Medication administration record — dose given, time, route, site, verification |

### Binary data handling

The data dictionary includes 23 `varbinary` columns across tables like `PatientDocument.DocumentData`, `VisitDocument.DocumentData`, `VisitObservation.ObservationValue_ImageBytes`, `NamedImage.ImageBytes`, and `VisitIntervention.AttachmentData`. Since the export format is CSV, it is unclear how binary data (scanned documents, images, signatures) is represented. The CSV format inherently cannot represent binary blobs without encoding (e.g., Base64), and no documentation addresses this.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is genuinely broad. The 339 tables span:

- **Deep pharmacy/medication coverage** (61 pharmacy tables, 30 order tables, 6 MAR tables = 97 tables, 1,037 fields) — by far the largest domain. This reflects HCS's roots as a pharmacy-focused system and includes the full drug product hierarchy, formulary management, PBM integration, dispensing, and administration.

- **Rich clinical observation model** (14 tables, 413 fields) — the Observation/ObservationGroup/ObservationGroupItem hierarchy is how HCS stores its 50+ behavioral health assessment tools. The Observation table alone (88 cols) defines value types, validation rules, reference ranges, and formulas. VisitObservation (46 cols) stores actual patient values. This generic model exports all assessment data regardless of instrument type.

- **Solid billing/financial data** (8+12+1 = 21 billing/PBM/payment tables, 298 fields) — VisitCharge (60 cols) with CPT/HCPCS, NDC, amounts, modifiers; ChargeClaim (40 cols) for claims; Payment; PBM coverage and formulary data.

- **Complete encounter and demographic data** (13+11 = 24 tables, 235 fields) — Patient demographics, visit records, transfers, staff assignments.

- **Treatment planning** (6 tables, 68 fields) — VisitIntervention with goals, objectives, outcomes; VisitCarePlan; VisitConcern. Critical for behavioral health.

- **Consent tracking** (2 tables, 46 fields) — detailed consent records with giver, requester, type, expiration, revocation.

- **Safety data** (5 tables, 69 fields) — physical location tracking (proximity beacons), near-miss events, clinical alerts.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (37 fields), `PatientAddress`, `PatientContact`, `PatientIdentifier`, `PatientRace`, `PatientAlias` — 13 tables, 121 fields | Thorough — includes name, DOB, sex, birth sex, ethnicity, language, religion, marital status, smoking status, death info |
| Encounters / visits | ✅ Covered | `PatientVisit` (48 fields), `VisitTransfer`, `VisitStaff`, `VisitIdentifier`, `VisitEncounterType` — 11 tables, 114 fields | Thorough — admission/discharge, bed assignment, attending, visit class, transfers |
| Problems / conditions / diagnoses | ✅ Covered | `VisitDiagnosis` (13), `VisitProblem` (19), `Condition` (31), `VisitCondition` (13) — 7 tables, 108 fields | Thorough — includes coding, status, classification, evidence |
| Medications / prescriptions | ✅ Covered | `PatientOrder` (143 fields), `HCS_MedList` (27), `MedRecItem` (29), `OrderItem` (30) — 30 tables, 438 fields | Exceptionally detailed — dosing, frequency, route, DAW codes, controlled substance info, ePrescribe status |
| Allergies | ✅ Covered | `PatientAllergy` (20 fields) — severity, reaction, source, product info | Adequate |
| Immunizations | ✅ Covered | `VisitImmunizationQuery` (11), `ImmunizationQueryForecast`, `ImmunizationQueryHistory` — 3 tables, 19 fields | Present — query-based model reflecting registry integration |
| Vitals | ✅ Covered | Stored via `VisitObservation`/`VisitObservationSet` observation model — 14 tables, 413 fields | Covered within the generic observation framework |
| Lab results | ✅ Covered | Stored via `VisitObservation`/`VisitObservationSet` — includes specimen info, result values, reference ranges | Covered within observation framework |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated radiology/imaging tables. Results likely flow through `VisitObservation`; report documents through `VisitDocument` | No explicit imaging tables, but this is an inpatient behavioral health system — limited imaging is expected |
| Procedures | ✅ Covered | `VisitProcedure` (18 fields) | Present |
| Clinical notes / documents | ✅ Covered | `VisitNote` (7 fields with `NoteText` varchar 400), `VisitDocument` (19 fields with `DocumentData` varbinary), `PatientDocument` (16 fields) — 7 tables | Present, but `VisitNote.NoteText` is limited to 400 chars; longer clinical narratives likely stored as documents in `VisitDocument.DocumentData` (varbinary — unclear how exported in CSV) |
| Care plans / goals | ✅ Covered | `VisitIntervention` (33 fields), `VisitCarePlan` (4), `VisitConcern` (8), `ConcernItem` (5) — 6 tables, 68 fields | Good — treatment plans with goals, objectives, outcomes, intervention activities |
| Orders / referrals | ✅ Covered | `PatientOrder` (143 fields) covers all order types; `OrderSet`, `OrderType`, `OrderClarification` | Exceptionally detailed |
| Insurance / coverage | ✅ Covered | `PatientInsuranceCoverage` (27), `InsuranceCompany` (24), `InsuranceContract` (9), `VisitInsuranceAuthorization`, `VisitEligibilityQuery` — 8 tables, 106 fields | Thorough — coverage, authorization, eligibility |
| Claims / billing | ✅ Covered | `VisitCharge` (60 fields), `ChargeClaim` (40), `PatientClaimResponse` (12) — 8 tables, 147 fields | Genuinely detailed — CPT/HCPCS codes, amounts, modifiers, NDC, diagnosis pointers, AR status |
| Payments | ✅ Covered | `Payment` (12 fields), `CopayProduct`, `CopaySummary` | Present |
| Consents / directives | ✅ Covered | `PatientConsent` (23 fields), `VisitConsent` (23), `ConsentDocument` (4), `PatientDirective` (4) | Detailed — giver, requester, type, expiration, revocation |
| Patient communications / portal | ⚠️ Partial | `Chat`/`ChatMessage`/`ChatStaff` (messaging), `MailMessage`, Patient portal fields in `Patient` table | Portal messaging exists; unclear if comprehensive patient-facing communication history is captured |
| Specialty-specific (behavioral health) | ✅ Covered | Behavioral health assessments stored via `Observation`/`ObservationGroup`/`ObservationGroupItem` hierarchy (413 fields); `VisitIntervention` for treatment planning; `VisitPhysicalLocation` for safety rounds | Core behavioral health workflows well-represented through generic observation model |

**Summary**: 15 of 17 applicable domains are fully covered, 2 are partially covered. No applicable domains are entirely missing.

## 6. Documentation Quality

**Strengths:**
- The data dictionary is **machine-readable CSV** — far superior to a PDF for downstream processing
- **100% of fields** have a name, type, size constraint, and description
- **730 foreign key relationships** are documented, enabling reconstruction of the relational model
- The data dictionary is described as updated with each new software version
- Export instructions are clear, actionable, and include a UI screenshot
- The attestation explicitly claims the export creates "a complete and fully usable HCS database"

**Weaknesses:**
- **Description quality is poor**: 71% of descriptions are trivial re-spacings of the column name (e.g., `RowVersionNumber` → "Row Version Number"). Only ~2.5% (98 fields) provide information not already apparent from the column name.
- **No value set documentation**: Coded fields (e.g., `ConsentType`, `ChargeType`, `ProblemStatus`, `OrderStatus`, `DocumentType`) list no valid values. A developer would have to reverse-engineer valid codes from sample data.
- **No sample export data** is provided
- **No ER diagram** or visual representation of table relationships
- **No documentation mapping tables to clinical workflows** (e.g., which tables correspond to "treatment planning" vs "medication administration")
- **The PDF instructions are a scan** of a paper document — not searchable, not accessible, not machine-readable
- **Binary data handling is undocumented**: 23 varbinary columns (including clinical documents and images) with no explanation of how they appear in CSV output

**Could a developer build an import?** Partially. The schema (types, sizes, FK references) is sufficient to reconstruct the database structure. However, interpreting the data would require significant reverse-engineering due to the lack of value set documentation and meaningful field descriptions. A developer could load the data but would struggle to understand what many coded values mean.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

HCS exports its full native relational database model as CSV files — 339 tables covering clinical, billing, pharmacy, administrative, and behavioral health-specific domains. This is a genuine "(b)(10) export" of all EHI, not a repackaged C-CDA or FHIR projection. The vendor's explicit statement that the export enables "creation of a complete and fully usable HCS database" demonstrates correct understanding of the requirement, and the table inventory substantiates this claim.

### Key Findings

1. **Genuine full-database export with 339 tables and 3,878 fields.** This is one of the more thorough EHI exports — the vendor exports their entire native data model as one CSV per table, covering clinical, financial, pharmacy, and operational domains. The attestation and table inventory are consistent with a real "all EHI" export (`EHIExportInstructionsHCSeMRv10.pdf`, `HCSDataDictionary.csv`).

2. **Behavioral health assessment data is well-covered through a generic observation model.** The 50+ standardized assessment tools (PHQ-9, C-SSRS, ASAM, etc.) are stored via the Observation/ObservationGroup/ObservationGroupItem hierarchy (14 tables, 413 fields). This is a sound architectural approach that exports all assessment data without hard-coding instrument names into the schema.

3. **Billing and financial coverage is genuine.** With `VisitCharge` (60 fields including CPT/HCPCS, NDC, amounts, modifiers), `ChargeClaim` (40 fields), `Payment`, and extensive PBM/formulary tables — this is not a clinical-only export.

4. **Description quality significantly undermines the data dictionary's utility.** While 100% of fields have descriptions, 71% are trivial re-spacings of the column name. No value sets are documented for coded fields. A developer receiving this export would face substantial reverse-engineering work to interpret the data semantically.

5. **Binary data (documents, images) handling is an open question.** The 23 varbinary columns include clinically important data (scanned documents, clinical images, observation images), and there is no documentation on how these are represented in CSV format. This could mean loss of document content in the export.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (one file per table, in ZIP archive)
Model type:      Native database
Entities:        339 tables
Fields:          3,878
Descriptions:    100% present, but 71% trivial (name re-spaced)
Sample data:     No
Bulk export:     Yes (multi-patient selection with 20+ filter options)
Domains covered: 15 of 17 applicable domains (2 partial)
```

### Bottom Line

HCS eMR delivers one of the stronger EHI exports seen — a genuine full-database export of 339 tables across clinical, billing, pharmacy, and behavioral health domains, available self-service at no charge. The single biggest weakness is documentation quality: while every field has a description, the vast majority are trivial re-spacings of the column name, and no value sets are provided for coded fields. A patient or provider would get a structurally complete copy of their data, but interpreting it would require significant domain expertise and reverse-engineering of coded values.
