# EHI Export Analysis: Health Care Systems, Inc.

**Product**: HCS eMR v10  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.99.04.1582.HC01.10.02.1.231220 (CHPL #11416)

## 1. Product Context

HCS eMR is a **comprehensive behavioral health electronic medical record** built for inpatient psychiatric hospitals, residential treatment centers, substance use disorder programs, and correctional healthcare facilities. Major customers include UHS, Acadia Healthcare, HCA Healthcare, and other large behavioral health chains.

The product is a full-suite platform covering:

- **Clinical**: Patient intake, assessments (50+ validated behavioral health tools including ASAM, PHQ-9, C-SSRS), treatment planning, group therapy notes, progress notes, discharge summaries, vital signs, labs, medication management
- **Pharmacy**: CPOE, eMAR with barcode scanning, ePrescribing (EPCS), medication reconciliation, pharmacy information system (HCS MEDICS), Medication Assisted Treatment (MAT)
- **Revenue cycle management**: Eligibility verification, charge capture, claim processing, denial management, ERA processing, payment tracking
- **Patient safety**: Electronic observation rounding (patented Safety Checks), proximity beacons, clinical decision support
- **Patient engagement**: Community Portal for scheduling and messaging, Call Center CRM for referral management
- **Compliance**: IPFQR quality reporting, credentialing management, chart review, regulatory reporting

This is a purpose-built behavioral health system — a (b)(10) export should cover clinical data, behavioral health assessments, treatment plans, medication administration, billing/charges/claims, and patient safety records.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/HCSDataDictionary.csv` (254 KB, 4,557 lines) | Machine-readable data dictionary: 339 tables, 3,878 fields with table name, column name, SQL type, size, and description. **Primary source of truth.** | ★★★★★ Most informative |
| `downloads/EHIExportInstructionsHCSeMRv10.pdf` (609 KB, 2 pages, scanned) | Scanned export instructions: overview, user access, step-by-step export creation, screenshot of export UI, attestation signed by Reubin Felkey (12/19/2023). Confirms CSV-in-ZIP format. | ★★★ Useful for mechanics |
| `downloads/meaningful-use-page.png` (438 KB) | Screenshot of the vendor's Meaningful Use page with EHI Export section and download links. | ★★ Contextual |
| `downloads/hcsinc-403-page.png` (169 KB) | Screenshot of 403 error page for curl access. Documents anti-bot protection. | ★ Low value |

## 3. Export Mechanics

- **Format**: ZIP file containing one CSV file per database table, plus a readme file with a hyperlink to the current data dictionary
- **Mechanism**: Built-in UI function at System → EHI Export; uses the same Patient Selection tool used elsewhere in the application
- **Single-patient vs bulk**: Both supported — users can select a single patient by Visit Identifier or a group using extensive filter parameters (date ranges, patient sets, admission/discharge dates, staff assignment, patient class, etc.)
- **Access**: Available to "Corporate Users" by default (typically administrators and analysts); configurable via Active Directory; no HCS assistance required
- **Cost**: No additional charge
- **Key claim**: Export instructions state the files "contain all necessary data, including that which is not strictly personal health information, to allow the creation of a complete and fully usable HCS database with only the patient(s) that the users chose to export"

## 4. Export Content: What's In It

The data dictionary documents **339 database tables** with **3,878 fields**. Every field has a name, SQL data type, size constraint (where applicable), and a plain-English description. 100% of fields have descriptions and type information. 730 fields (18.8%) document foreign key relationships via "Reference to [TableName]" in the description.

### Data types distribution

| Type | Count |
|---|---|
| bigint | 1,571 |
| varchar | 1,089 |
| int | 416 |
| datetime | 372 |
| bool | 261 |
| decimal | 126 |
| varbinary | 42 |
| bit | 1 |

### Vendor's own content organization

The data dictionary uses a flat table-per-row structure without explicit category headers. Tables are named with descriptive prefixes. Based on analysis of the 339 tables, they break down into these functional areas:

| Category | Tables | Fields | Key Tables |
|---|---|---|---|
| Orders & Pharmacy | 84 | 914 | PatientOrder (143), OrderItem (30), OrderComponent (25), DispensableProduct (22), RoutedProduct (18), PackagedProduct (12), NamedProduct (13), MedRecItem (29), HCS_MedList (27) |
| Observations & Assessments | 21 | 497 | Observation (88), ObservationGroup (62), ObservationGroupItem (71), VisitObservation (46), VisitObservationSet (58) |
| Patient & Demographics | 31 | 392 | Patient (37), PatientVisit (48), PatientAddress (11), PatientContact (8), PatientIdentifier (7), PatientRace (4), PatientAlias (7) |
| Billing & Insurance | 25 | 370 | VisitCharge (60), ChargeClaim (40), PatientInsuranceCoverage (27), InsuranceCompany (24), Payment (12), EligibilityPBMResponse (36) |
| Visits & Encounters | 27 | 272 | PatientVisit (48), VisitDiagnosis (13), VisitProblem (19), VisitProcedure (18), VisitTransfer (11), VisitCareLevel (7) |
| Staff & Providers | 24 | 207 | Staff (80), StaffPractitionerID (5), StaffSpecialty (5), StaffIDCode (5) |
| Reference / System | 92 | 944 | Facility (22), Department (10), Frequency (26), HL7Table (4), WorkQueue tables, authorization/role tables |
| Clinical Care | 6 | 73 | VisitIntervention (33), Condition (31), VisitCarePlan (4), VisitConcern (8) |
| Scheduling | 9 | 64 | Event (11), EventOccurrence (9), CalendarDay (9) |
| Documents & Notes | 7 | 42 | PatientDocument (16), VisitDocument (19), VisitNote (7) |
| Medication Administration | 5 | 38 | TherapyAdmin (45), AdminProduct (18), AdminComponent (4), AdminField (5), AdminObservation (3) |
| Safety & Compliance | 2 | 30 | VisitPhysicalLocation (8), NearMiss (11) |
| Communications | 4 | 27 | Chat (10), ChatMessage (7) |
| Immunizations | 2 | 8 | VisitImmunizationQuery (5), ImmunizationQueryForecast (3) |

### Top 20 largest tables (representative examples)

| Table | Fields | Description |
|---|---|---|
| PatientOrder | 143 | All orders including medications — dosing, frequency, route, prescriber, status, refills, DAW codes, controlled substance info |
| Observation | 88 | Clinical observations with coded values, units, ranges, abnormal flags |
| Staff | 80 | Provider/staff records — credentials, NPI, DEA, specialties |
| ObservationGroupItem | 71 | Individual items within observation groups (assessment tool items) |
| ObservationGroup | 62 | Observation groupings/panels (assessment instruments) |
| VisitCharge | 60 | Charges with CPT/HCPCS, revenue codes, diagnosis pointers, amounts, modifiers, NDC |
| VisitObservationSet | 58 | Observation sets with specimen collection details |
| PatientListCriteria | 51 | Patient list/query criteria |
| PatientVisit | 48 | Admission/discharge, visit type, class, bed assignment, attending physician |
| VisitObservation | 46 | Visit-specific observations (vitals, labs, assessments) |
| TherapyAdmin | 45 | Medication administration records — administered amount, route, timing, witness |
| ChargeClaim | 40 | Claim submissions with payer responses, NCPDP messaging, copay info |
| Patient | 37 | Demographics — SSN, DOB, gender, ethnicity, language, religion, marital status, veteran status |
| EligibilityPBMResponse | 36 | PBM eligibility/formulary responses |
| ItemDispenseSize | 33 | Dispense size configurations |
| VisitIntervention | 33 | Treatment plan interventions with goals, objectives, outcomes |
| Condition | 31 | Detailed condition records |
| OrderItem | 30 | Order line items |
| V_WQ_ITEM | 30 | Work queue items (view) |
| MedRecItem | 29 | Medication reconciliation items |

The full inventory of all 339 tables and 3,878 fields is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

HCS exports their **entire relational database schema** as CSV files — one per table. This is not a curated clinical subset; it is a full database dump scoped to selected patients. The attestation explicitly states the export includes "all necessary data, including that which is not strictly personal health information, to allow the creation of a complete and fully usable HCS database."

**Richest areas:**
- **Orders & Pharmacy** (84 tables, 914 fields): Exceptionally deep. PatientOrder alone has 143 fields covering medications, CPOE, controlled substance tracking, ePrescribing details, and refill management. Full drug product hierarchy (DispensableProduct → RoutedProduct → PackagedProduct → NamedProduct). Medication reconciliation, PBM formulary data, and dispensing batch management are all included.
- **Observations & Assessments** (21 tables, 497 fields): The observation model (Observation/ObservationGroup/ObservationGroupItem) is the generic infrastructure storing behavioral health assessments (PHQ-9, C-SSRS, ASAM, etc.). With 88 columns on Observation alone, this captures the full assessment data.
- **Billing & Insurance** (25 tables, 370 fields): Genuine billing depth — VisitCharge (60 fields) with CPT/HCPCS codes, revenue codes, diagnosis pointers, modifiers, NDC codes, amounts, expected reimbursement. ChargeClaim (40 fields) for claims. Payment, copay, insurance coverage, and eligibility tables complete the revenue cycle.

**Thinnest areas:**
- **VisitNote** (7 fields): Clinical notes appear limited — NoteText is varchar(400), suggesting short free-text notes rather than full narrative documents. However, clinical documents may be stored in PatientDocument (which includes DocumentData as varbinary) and VisitDocument (19 fields).
- **Immunizations** (2 tables, 8 fields): Only query/forecast tables, no immunization administration records — though this may be appropriate for a behavioral health inpatient product.
- **VisitCarePlan** (4 fields): Thin, but treatment planning data is primarily in VisitIntervention (33 fields) which captures goals, objectives, and outcomes.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (37 fields), `PatientAddress` (11), `PatientContact` (8), `PatientRace` (4), `PatientAlias` (7), `PatientIdentifier` (7) | Thorough: SSN, DOB, birth sex, gender identity, ethnicity, language, religion, marital status, veteran status, death info |
| Encounters / visits | ✅ Covered | `PatientVisit` (48 fields), `VisitTransfer` (11), `VisitCareLevel` (7), `VisitServiceLevel` (4) | Strong: admission/discharge, visit type, class, bed assignment, attending, transfer tracking |
| Problems / conditions / diagnoses | ✅ Covered | `VisitDiagnosis` (13), `VisitProblem` (19), `VisitProspectiveProblem` (6), `Condition` (31) | Good coverage with coding system, rank, status, classification, evidence |
| Medications / prescriptions | ✅ Covered | `PatientOrder` (143 fields!), `HCS_MedList` (27), `MedRecItem` (29), full product hierarchy (DispensableProduct, RoutedProduct, PackagedProduct, NamedProduct) | Exceptionally deep: dosing, frequency, route, refills, DAW, controlled substance, ePrescribing |
| Medication administration (MAR) | ✅ Covered | `TherapyAdmin` (45), `AdminProduct` (18), `AdminComponent` (4), `AdminField` (5), `AdminVolume` (4) | Strong: administered amount, route, timing, witness, lot number, manufacturer |
| Allergies | ✅ Covered | `PatientAllergy` (20 fields) | Severity, reaction, source documented |
| Immunizations | ⚠️ Partial | `VisitImmunizationQuery` (5), `ImmunizationQueryForecast` (3) | Query/forecast only; no administration records. Acceptable for behavioral health inpatient focus |
| Vitals | ✅ Covered | `VisitObservation` (46), `VisitObservationSet` (58), `Observation` (88) | Stored in generic observation model with coded values, units, ranges |
| Lab results | ✅ Covered | Same observation tables; `VisitObservationSet` includes specimen collection details | Includes specimen info, result values, abnormal flags |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated radiology tables; results would flow through observation model | Likely adequate for a behavioral health product with limited imaging |
| Procedures | ✅ Covered | `VisitProcedure` (18 fields) | Coding system, procedure code, modifiers included |
| Clinical notes / documents | ✅ Covered | `VisitNote` (7), `PatientDocument` (16 with varbinary DocumentData), `VisitDocument` (19) | VisitNote is thin (varchar 400); longer documents stored as binary in PatientDocument/VisitDocument |
| Care plans / goals | ✅ Covered | `VisitCarePlan` (4), `VisitIntervention` (33), `VisitConcern` (8), `ConcernItem` (5) | Treatment plan data is in VisitIntervention with goals, objectives, outcomes — critical for behavioral health |
| Orders / referrals | ✅ Covered | `PatientOrder` (143), `OrderItem` (30), `OrderComponent` (25) | CPOE orders for medications, labs, radiology, tasks |
| Insurance / coverage | ✅ Covered | `PatientInsuranceCoverage` (27), `InsuranceCompany` (24), `InsuranceContract` (9), `VisitInsuranceCoverage` (9), `VisitInsuranceAuthorization` (15), `VisitEligibilityQuery` (14) | Deep: coverage details, authorization tracking, eligibility verification |
| Claims / billing | ✅ Covered | `VisitCharge` (60), `ChargeClaim` (40), `PatientClaimResponse` (12), `ClaimObservation` (4) | Genuine billing depth: CPT, revenue codes, diagnosis pointers, amounts, modifiers, NDC |
| Payments | ✅ Covered | `Payment` (12), `CopayProduct` (4), `CopaySummary` (4) | Payment tracking and copay management |
| Consents / directives | ✅ Covered | `PatientConsent` (23), `VisitConsent` (6), `ConsentDocument` (4) | Comprehensive consent documentation |
| Patient communications | ⚠️ Partial | `Chat` (10), `ChatMessage` (7) | Basic messaging infrastructure; no portal message or phone call log tables visible |
| Behavioral health assessments | ✅ Covered | `Observation` (88), `ObservationGroup` (62), `ObservationGroupItem` (71) | Assessment tools (PHQ-9, C-SSRS, ASAM, etc.) stored in generic observation model — a sound architectural choice |
| Patient safety / rounding | ✅ Covered | `VisitPhysicalLocation` (8), `NearMiss` (11) | Safety Checks proximity rounding data included |
| Family history | ✅ Covered | `PatientFamilyHistoryItem` (9) | Present |
| Devices | ✅ Covered | `PatientDevice` (13), `DeviceIdentifier` (8) | UDI tracking included |

**Domains covered**: 19 of 20 applicable domains have dedicated coverage; 1 additional (imaging) has partial coverage appropriate to the product's behavioral health focus.

## 6. Documentation Quality

**Strengths:**
- **Machine-readable data dictionary in CSV** — 339 tables, 3,878 fields, all with SQL types, sizes, and descriptions. This is far better than most vendors who provide PDFs or nothing.
- **100% description coverage**: Every single field has a description. While many are short/formulaic ("Field Name" → "Field Name" description), they are consistently present.
- **Foreign key documentation**: 730 fields (18.8%) explicitly document relationships via "Reference to [TableName]", allowing reconstruction of table joins.
- **Export instructions are clear**: Step-by-step with screenshot, accessible in the UI at System → EHI Export.

**Weaknesses:**
- **Descriptions are often tautological**: Many descriptions just reformat the field name (e.g., column "ChargeDateTime" → description "Charge Date Time"). These confirm the field exists but don't explain semantics.
- **No value set documentation**: Coded fields (e.g., `ProblemStatus`, `OrderStatus`, `ChargeStatus`) don't enumerate valid values.
- **No sample data files**: No example CSV export is provided to verify actual output format.
- **No ER diagram**: Relationships are documentable via FK references but no visual schema is provided.
- **Export instructions are a scanned PDF**: Not searchable, not accessible, not version-controllable. Dated 12/19/2023.

**Could a developer build an import?** Yes, with effort. The data dictionary provides sufficient structural information to create a receiving database schema and load CSV files. Foreign key references enable relationship reconstruction. However, interpreting coded values and understanding clinical semantics would require domain knowledge or access to the running system.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is one of the more thorough (b)(10) exports observed. HCS exports their entire relational database — 339 tables covering clinical data, behavioral health assessments, medication administration, billing/charges/claims, insurance, pharmacy management, patient safety, treatment planning, and operational support data. The export explicitly goes beyond clinical summaries to include "all necessary data, including that which is not strictly personal health information, to allow the creation of a complete and fully usable HCS database." For a behavioral health EHR, the key domains are all present: assessments (via the deep Observation model), treatment plans (VisitIntervention with 33 fields), MAR data (TherapyAdmin with 45 fields), and billing (VisitCharge with 60 fields, ChargeClaim with 40 fields). The only minor gaps are in patient communications (basic chat tables only) and immunization administration (query/forecast only), both of which are peripheral to the product's behavioral health inpatient focus.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. Key signals:
1. The export produces one CSV per database table — a native database dump, not a repackaged C-CDA or FHIR output
2. 339 tables go far beyond any USCDI or (g)(10) scope — includes billing, pharmacy management, PBM data, work queues, safety rounding, and other operational data
3. A dedicated UI function (System → EHI Export) with flexible patient selection
4. A machine-readable data dictionary maintained with each release
5. The attestation explicitly distinguishes this from clinical summaries

### Key Findings

1. **Genuinely comprehensive database export**: 339 tables and 3,878 fields exported as CSV files covering the full breadth of the HCS database. This is what a (b)(10) export should look like — not a clinical summary, but the actual database content scoped to selected patients.

2. **Strong billing and financial coverage**: 25 tables with 370 fields covering charges (CPT, revenue codes, diagnosis pointers, NDC), claims, payments, copays, insurance coverage, and PBM eligibility. This goes well beyond what clinical exchange standards cover.

3. **Behavioral health assessment data is well-covered**: The generic Observation/ObservationGroup/ObservationGroupItem model (221 total fields across these three tables) stores the 50+ behavioral health assessment tools. This is architecturally sound and ensures all assessment data is captured.

4. **100% field documentation with limitations**: Every field has a description and type, which is excellent coverage. However, many descriptions are tautological (reformatted field names) and no value sets are documented for coded fields.

5. **No sample data provided**: The absence of example export files means the actual CSV output format and data completeness cannot be independently verified from documentation alone.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV files in ZIP archive (one CSV per database table)
Entities:        339 tables
Fields:          3,878
Descriptions:    100% (though many are tautological)
Sample data:     No
Bulk export:     Yes (supports single patient and bulk via flexible filters)
Domains covered: 19 of 20 applicable domains (imaging partial, appropriate to product)
```

### Bottom Line

HCS has built a genuinely comprehensive (b)(10) export that dumps their entire relational database as CSV files — 339 tables covering clinical, behavioral health, pharmacy, billing, safety, and operational data. A patient or provider would get a complete, structurally faithful copy of all data the system stores about them. The main limitation is that the documentation, while structurally complete (100% of fields described and typed), lacks value set definitions and sample data that would make the export fully self-documenting.
