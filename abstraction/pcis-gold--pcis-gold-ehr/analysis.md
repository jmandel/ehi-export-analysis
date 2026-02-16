# EHI Export Analysis: PCIS GOLD

**Product**: PCIS GOLD EHR v2.6
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2126.PCIS.26.02.1.221222

## 1. Product Context

PCIS GOLD EHR is an integrated ambulatory EHR and practice management platform developed by DHI Computing Service, Inc. (Provo, UT). The product targets independent ambulatory medical groups, particularly those with 10+ physicians, and serves as an all-in-one system covering clinical documentation, e-prescribing, lab integration, billing/claims management, patient portal, and analytics.

The product is certified for 33 ONC criteria including (b)(10) EHI export. Key data domains the product stores:

- **Clinical**: Patient demographics, charting/notes (customizable forms), vitals, allergies, medications, problem lists, immunizations, lab orders/results, procedures, imaging orders, implantable devices, family history, clinical decision support alerts
- **Specialty**: Ophthalmology/eye care (refraction, IOP, visual acuity, keratometry, contact lenses), allergy immunotherapy (antigens, skin tests, vials, mixing lab), oncology (cancer diagnoses, events, planned treatments), and screening/assessments
- **Billing/PM**: Patient scheduling, registration, insurance verification, billing, claims submission/scrubbing, accounts receivable, payments, e-statements, revenue cycle reporting
- **Patient engagement**: Patient portal, secure messaging, online scheduling, digital intake forms, appointment reminders, patient education
- **Care coordination**: Transitions of care (C-CDA), referral management, FHIR API access
- **E-prescribing**: Surescripts-certified electronic prescriptions via NewCrop

This is a small vendor (14–28 employees) serving a niche market, but the integrated nature of the platform means it stores data across all major clinical and financial domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-data-table-definitions.html` (534 KB) | Self-contained HTML data dictionary documenting 309 tables and 4,481 fields in the EHI export. Single-page document with TOC, table descriptions, and field-level definitions (name, type, description). Last updated 10/27/2023. | **Primary artifact** — contains the entire data dictionary |
| `ehi-export-page-screenshot.png` (211 KB) | Browser screenshot of the documentation page showing title, intro text, and TOC index | Low — confirms page layout only |
| `enrichment/tables.json` (628 KB) | Prior agent's JSON extraction of all 309 tables with fields | Useful for cross-validation; my independent parse matches exactly |
| `enrichment/coverage-stats.json` (11 KB) | Prior agent's parsing statistics and domain categorization | Useful for cross-validation |
| `enrichment/table-index.json` (34 KB) | Lightweight table name/description/count index | Minor — subset of tables.json |
| `enrichment/extract-tables.ts` (10 KB) | Bun TypeScript script that produced the enrichment artifacts | Code review confirms parsing approach |

The HTML data dictionary is the sole substantive artifact. There is no sample data, no machine-readable schema, no PDF, no FHIR documentation, and no additional downloadable files. The URL (`https://fhir.pcisgold.com/ehiexport/`) was verified live on 2026-02-15 returning HTTP 200 with identical content (534,594 bytes).

## 3. Export Mechanics

- **Format**: ZIP archive containing tab-delimited text files (one file per table) plus a `Files/` folder containing binary attachments (documents, images) referenced by the `T_BlobData` table
- **Mechanism**: UI-driven. Single-patient export via "EHI Export" tool from the Tools menu with patient search/selection. Population-level export via "EHI Export" button on the patient queries screen.
- **Single-patient**: Yes — explicitly described
- **Bulk/population**: Yes — explicitly described via patient queries
- **Access constraints or fees**: Not documented in the export documentation. No mention of fees, restrictions, or turnaround times.

The introductory text states:
> "The EHI Export zip file contains a file for each of the following data tables. The individual files are formatted using tab-delimited fields. The fields are defined for each of the data tables below. The EHI Export zip file also contains a folder named *Files* that contains related patient files. The files are named with an identifier that matches the Id field in the EHI_T_BlobData data table."

## 4. Export Content: What's In It

The export is a native database dump: 309 tables with 4,481 fields documented in an HTML data dictionary. This is the vendor's internal data model, not a projection into FHIR or C-CDA.

### Data dictionary statistics

| Metric | Value |
|---|---|
| Total tables | 309 |
| Total fields | 4,481 |
| Fields with descriptions | 4,063 (90.7%) |
| Fields without descriptions | 418 (9.3%) |
| Fields with data types | 4,480 (>99.9%) |
| Tables with all fields undescribed | 26 |
| Fully described tables | 215 (69.6%) |
| Last updated | 10/27/2023 |

The data dictionary contains two naming generations: 99 legacy tables (no `T_` prefix, 2,453 fields, 96.7% described) using abbreviated AS/400-style field names (e.g., `TDTYPE`, `ACINST`), and 210 modern tables (`T_` prefix, 2,028 fields, 83.4% described) using descriptive names (e.g., `PatientId`, `StartDate`). Every field has a SQL data type. Relationships are inferred through naming conventions (~632 fields ending in "Id") but not formally declared via foreign keys.

### Vendor's own content organization

The vendor does not organize tables into explicit categories — the data dictionary is a flat alphabetical list. I categorized tables heuristically by name prefix and content. Full inventory is in `analysis/full-entity-inventory.json`.

**Category breakdown (by field count):**

| Category | Tables | Fields |
|---|---|---|
| Visits/Encounters | 39 | 713 |
| Billing/Financial | 12 | 447 |
| Patient Administrative | 3 | 352 |
| Patient Clinical Data | 23 | 308 |
| Ophthalmology/Eye Care | 23 | 265 |
| Medications/Prescriptions | 10 | 246 |
| Accounts | 3 | 209 |
| Orders | 10 | 184 |
| System/Reference | 27 | 164 |
| Referrals | 8 | 153 |
| Allergy/Immunotherapy | 20 | 151 |
| Laboratory | 6 | 132 |
| Immunizations | 8 | 102 |
| Vitals | 21 | 96 |
| Allergies/Alerts | 11 | 88 |
| Recalls | 5 | 78 |
| Problem List | 7 | 78 |
| Information Release | 2 | 66 |
| Family History | 9 | 57 |
| Oncology/Cancer | 5 | 52 |
| Tasks | 2 | 46 |
| Screening/Assessment | 5 | 45 |
| Patient Notes | 2 | 44 |
| E-Tasking/Communication | 7 | 41 |
| Flowsheets | 4 | 41 |
| Custom/Column-Based Data | 5 | 39 |
| Demographics | 6 | 38 |
| Transitions of Care | 3 | 34 |
| Health Record Items | 7 | 33 |
| Fax | 2 | 32 |
| Patient Portal | 2 | 31 |
| Documents/Attachments | 2 | 26 |
| Addresses | 1 | 23 |
| Scribble/Drawing Notes | 2 | 18 |
| Device Integration (Midmark) | 2 | 16 |
| Panels | 2 | 14 |
| Patient Forms | 2 | 13 |
| Record Requests | 1 | 6 |
| **Total** | **309** | **4,481** |

**20 largest entities (representative examples):**

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| Visits | 393 | 393 | yes | Visits/Encounters |
| Patients | 315 | 315 | yes | Patient Administrative |
| Accounts | 156 | 153 | yes | Accounts |
| Trans | 156 | 156 | yes | Billing/Financial |
| Referrals | 80 | 76 | yes | Referrals |
| T_RenewalRequests | 79 | 72 | yes | Medications/Prescriptions |
| T_Patients | 78 | 66 | yes | Patient Clinical Data |
| T_PatientMedication | 72 | 55 | yes | Medications/Prescriptions |
| T_Visits | 71 | 66 | yes | Visits/Encounters |
| InfoRelease | 59 | 59 | yes | Information Release |
| Statements | 58 | 58 | yes | Billing/Financial |
| Orders | 56 | 56 | yes | Orders |
| Lab_CompletedTests | 50 | 44 | yes | Laboratory |
| Lab_CompletedOrders | 49 | 48 | yes | Laboratory |
| PatientRecalls | 49 | 49 | yes | Recalls |
| T_PatientImmunizations | 48 | 43 | yes | Immunizations |
| T_LabRecOrder | 41 | 0 | yes | Orders |
| PatientNotes | 40 | 40 | yes | Patient Notes |
| AcctNotes | 38 | 38 | yes | Accounts |
| TaskHeader | 38 | 38 | yes | Tasks |

**Notable outliers:**
- `T_LabRecOrder` (41 fields) has zero field descriptions — entirely undescribed
- `T_PatientEyeVisualAcuity` (18 fields) — completely undescribed
- `T_OrderTrackingStatusDefs` (16 fields) — completely undescribed
- All 5 `ColBased_*` tables (39 fields total) — completely undescribed
- 3 of 5 oncology/cancer tables (`PlannedEncounters`, `PlannedMeds`, `PlannedProcedures`) — completely undescribed

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers an impressive breadth of the product's data model:

**Deepest coverage (most tables and fields):**
- **Visits/Encounters** (39 tables, 713 fields): Extremely thorough — covers visit data, notes, addenda, amendments, sections, diagnoses, procedures, HPI, physical exam, vital modifiers, checkout workflows, ink/sketch data, attachments, and specialty visit data (ophthalmology, radiology). The legacy `Visits` table alone has 393 fields.
- **Billing/Financial** (12 tables, 447 fields): Genuine billing depth — `Trans` (156 fields) for transactions, `AllocatedTrans` for payment allocation, `ClaimHistory` for claims, `EOBRecs` for explanation of benefits, `Statements`, `PaymentPlans`, `EstimateHdr`/`EstimateDtl`, and `DunningMessages`.
- **Patient Administrative** (3 tables, 352 fields): Legacy `Patients` table with 315 fields covering extensive demographic and administrative data, plus `Patients_Reps` (additional fields) and `PatientHIPAA`.
- **Patient Clinical Data** (23 tables, 308 fields): Modern `T_Patients` (78 fields), addresses, phones, emergency contacts, next of kin, ethnicity, races, education documents, cognitive/functional status, implantable devices, CCDA records, section notes, history, and transitions of care.

**Specialty coverage (distinctive):**
- **Ophthalmology/Eye Care** (23 tables, 265 fields): Unusually deep — IOP, refraction, keratometry, visual acuity, contact lenses, dilation, current Rx, ocular history, plus visit-level eye data. Reflects the vendor's eye care customer base.
- **Allergy/Immunotherapy** (20 tables, 151 fields): Full immunotherapy workflow — antigens, concentrations, vials, skin tests, mixing lab, schedules, tray configurations. Goes well beyond basic allergy lists.
- **Oncology/Cancer** (5 tables, 52 fields): Cancer diagnoses, events, planned encounters, medications, and procedures. 3 of 5 tables lack descriptions.

**Adequate coverage:**
- **Medications** (10 tables, 246 fields): Comprehensive — includes medication details, e-prescribing data (ERx details, changes, cancels), sig changes, Rx history, print details, and renewal requests.
- **Laboratory** (6 tables, 132 fields): Completed orders, tests, observations, test comments, and views.
- **Immunizations** (8 tables, 102 fields): Immunization records, evaluation/forecast, VIS records, registry info.
- **Problem List** (7 tables, 78 fields): Problems, codes, code types, groups, links, external references, severity.
- **Family History** (9 tables, 57 fields): Conditions, persons, relationships, and patient-specific family history.
- **Screening/Assessment** (5 tables, 45 fields): Screening definitions, questions, choices, patient responses, and answers.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `T_Patients` (78 fields), `Patients` (315 fields), `T_PatientAddress`, `T_PatientPhones`, `T_PatientEmergencyContact`, `T_PatientNextOfKin`, `Demo_Ethnicity`, `Demo_Races`, `Demo_GenderIdentity`, `Demo_SexualOrientation`, `Demo_Language` — 11+ tables | Thorough; includes modern demographic elements |
| Encounters / visits | ✅ Covered | `T_Visits` (71 fields), `Visits` (393 fields), `T_VisitNote`, `T_VisitDiags`, `T_VisitProcedures`, plus 34 more visit tables — 39 tables, 713 fields total | Extremely deep |
| Problems / conditions / diagnoses | ✅ Covered | 7 `Problem_*` tables (78 fields), `T_VisitDiags`, `T_DiagnosisCodes` | Well-structured |
| Medications / prescriptions | ✅ Covered | `T_PatientMedication` (72 fields), `T_PatientERxDetails`, `T_PatientErxChange`, `T_PatientErxCancelDetails`, `T_PatientRxHistory`, `T_RenewalRequests` (79 fields) — 10 tables, 246 fields | Comprehensive including e-prescribing |
| Allergies | ✅ Covered | `T_PatientAllergy` (21 fields), `T_PatientAllergyReactions`, `T_PatientAlertAllergies`, plus 20 allergy immunotherapy tables — 31 tables total | Goes far beyond basic allergy lists |
| Immunizations | ✅ Covered | `T_PatientImmunizations` (48 fields), evaluation/forecast, VIS records, registry info — 8 tables, 102 fields | Thorough |
| Vitals | ✅ Covered | `T_VitalsData`, `T_Vital`, `T_VitalModifier`, plus 18 supporting tables — 21 tables, 96 fields | Comprehensive including templates and conditions |
| Lab results | ✅ Covered | `Lab_CompletedOrders` (49 fields), `Lab_CompletedTests` (50 fields), `Lab_CompletedObservations`, `Lab_TestComments` — 6 tables, 132 fields | Solid |
| Imaging / diagnostic reports | ⚠️ Partial | `T_VisitRadOutboundInfo` (5 fields, undescribed) for radiology ordering info. Imaging results may be stored as blob attachments in `T_BlobData`. No dedicated imaging results table. | Product may not store imaging results natively (only ordering); radiology results likely received as documents |
| Procedures | ✅ Covered | `T_VisitProcedures` (27 fields) with CPT codes, modifiers, diagnosis links, standing orders | Adequate |
| Clinical notes / documents | ✅ Covered | `T_VisitNote`, `T_VisitNoteAddendum`, `T_VisitNoteAmendment`, `T_VisitNotesSection`, `T_VisitDataSectionText`, `T_PatientSectionNotes`, `PatientNotes` (40 fields), `T_ScribbleAddenda`, `T_ScribblePageData` | Thorough — includes structured notes, addenda, amendments, scribble/ink |
| Care plans / goals | ⚠️ Partial | No dedicated care plan table. `T_PatientCognitiveStatus`, `T_PatientFunctionalStatus` capture some assessment data. `Flowsheets` (4 tables) track ongoing data. | No explicit care plan entities, but clinical assessment and flowsheet data present |
| Orders / referrals | ✅ Covered | `Orders` (56 fields), `T_OrderTracking` (22 fields), plus 5 order tracking tables. `T_PatientReferrals`, `Referrals` (80 fields) — 8 referral tables, 153 fields | Deep |
| Insurance / coverage | ✅ Covered | Insurance fields within `Accounts` (156 fields) and `Patients` (315 fields), `T_Insurance` reference table, insurance verification fields | Covered within account/patient records |
| Claims / billing | ✅ Covered | `Trans` (156 fields), `AllocatedTrans`, `ClaimHistory`, `EOBRecs`, `Statements` (58 fields), `PaymentPlans`, `EstimateHdr`/`EstimateDtl`, `DunningMessages` — 12 tables, 447 fields | Genuinely deep billing coverage |
| Payments | ✅ Covered | `AllocatedTrans` for payment allocation, `PaymentPlans`, payment fields in `Trans` | Covered within billing tables |
| Consents / directives | ✅ Covered | `Demo_PatConsent`, `PatientHIPAA`, `InfoRelease` (59 fields), `InfoReleaseDetail` | Includes consent, HIPAA acknowledgment, and information release records |
| Patient communications / portal messages | ✅ Covered | `T_PatientPortalMessages`, `T_PatientPortalInfo`, `T_CommunicationPreferences`, `eTask_Items` and 6 related e-tasking tables | Portal messages and internal tasking both included |
| Specialty: Ophthalmology | ✅ Covered | 23 tables, 265 fields covering IOP, refraction, keratometry, visual acuity, contact lenses, dilation, current Rx, ocular history | Unusually deep specialty coverage |
| Specialty: Allergy/Immunotherapy | ✅ Covered | 20 tables, 151 fields covering full immunotherapy workflow | Complete immunotherapy module export |
| Specialty: Oncology | ✅ Covered | 5 tables, 52 fields — cancer diagnoses, events, planned encounters/meds/procedures | Present but 3 of 5 tables lack field descriptions |

## 6. Documentation Quality

**Strengths:**
- **Comprehensive scope**: 309 tables and 4,481 fields across all major data domains. This is among the most extensive EHI data dictionaries reviewed.
- **Field-level detail**: Every field has a name and SQL data type. 90.7% of fields have human-readable descriptions.
- **Clean HTML structure**: Well-organized single-page document with anchor-linked TOC. Easy to navigate and parse programmatically.
- **Clear export instructions**: The introductory text explains the format (tab-delimited), structure (one file per table, companion `Files/` folder for binaries), and how to initiate the export (single-patient and population-level).
- **Post-certification updates**: Last updated 10/27/2023, roughly 10 months after the December 2022 certification date.

**Weaknesses:**
- **No machine-readable schema**: No JSON Schema, SQL DDL, XSD, or ERD. A developer must parse the HTML to build tooling. (However, the HTML is cleanly structured and straightforward to parse.)
- **No sample data**: No example export files, sample records, or worked examples.
- **418 fields (9.3%) lack descriptions**: 26 tables have zero field descriptions, including the 41-field `T_LabRecOrder`, all 5 `ColBased_*` tables (custom data extensibility mechanism), and 3 of 5 oncology tables.
- **Abbreviated legacy field names**: Legacy tables use 4–6 character abbreviations (e.g., `TDTYPE` = "TRANSACTION TYPE (C,P,A, T)", `ACINST` = "KEY-INSTITUTION"). While descriptions are provided, the abbreviations make the data harder to work with.
- **Missing value sets**: Coded fields list types but not allowed values. For example, `TDTYPE` is described as "TRANSACTION TYPE (C,P,A, T)" without explaining what each code means. Many `bit` fields don't document what 0 vs 1 means.
- **No formal relationship documentation**: Foreign keys are inferred from naming conventions (`PatientId`, `VisitId`, `AccountId`) and field descriptions, not formally declared. ~632 fields end in "Id" suggesting foreign key relationships, but these must be manually mapped.

**Developer usability**: A competent developer with SQL experience could build an import from this documentation, but it would require significant effort to decode legacy field names, infer relationships, and handle coded values. The modern `T_` tables would be substantially easier to work with than the legacy tables.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

PCIS GOLD exports its internal database model — 309 tables across clinical, billing, specialty, and administrative domains — with field-level documentation for all 4,481 fields. This is not a C-CDA or FHIR projection. It is a genuine (b)(10) export of the vendor's native data, covering virtually every data domain the product stores.

### Key Findings

1. **Genuine native database export**: 309 tables with 4,481 fields exported as tab-delimited files in a ZIP archive. This is the vendor's actual database structure, not a clinical summary or standards-based projection. The format includes binary attachments in a companion `Files/` folder.

2. **Exceptional domain coverage**: The export covers demographics, encounters, medications, allergies, labs, vitals, immunizations, problems, procedures, clinical notes, billing/claims (447 fields across 12 tables), insurance, referrals, family history, portal messages, screenings, and three specialty modules (ophthalmology, allergy immunotherapy, oncology). Very few domains are absent.

3. **Strong documentation quality with notable gaps**: 90.7% of fields have descriptions, and all fields have SQL data types. However, 26 tables (including the 41-field `T_LabRecOrder` and all custom data tables) lack any field descriptions. No value sets, sample data, or formal schema are provided.

4. **Dual-era data model**: The export reflects two generations of the product — legacy AS/400-style tables with terse abbreviated field names (e.g., `Visits` with 393 fields) and modern SQL Server tables with descriptive names (e.g., `T_Visits` with 71 fields). Both are exported.

5. **Notable for a small vendor**: For a company with 14–28 employees serving a niche market, this is a remarkably thorough (b)(10) implementation that exceeds many larger vendors' efforts.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   Tab-delimited text files in ZIP archive (with binary attachments)
Model type:      Native database
Entities:        309
Fields:          4,481
Descriptions:    90.7% of fields
Sample data:     No
Bulk export:     Yes (patient population via patient queries)
Domains covered: 19 of 21 assessed domains fully covered; 2 partial (imaging, care plans)
```

### Bottom Line

A patient or provider would get a substantially complete copy of their data from this export. The 309-table native database dump covers clinical, billing, specialty (ophthalmology, immunotherapy, oncology), and administrative data with field-level documentation. The single biggest weakness is not scope — it's documentation completeness: the lack of value set definitions, formal relationships, and the 26 fully undescribed tables would make automated data import challenging without vendor support.
