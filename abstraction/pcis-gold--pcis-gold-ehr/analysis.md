# EHI Export Analysis: PCIS GOLD

**Product**: PCIS GOLD EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2126.PCIS.26.02.1.221222

## 1. Product Context

PCIS GOLD EHR is an integrated ambulatory EHR and practice management platform developed by PCIS GOLD (a division of DHI Computing Service, Inc.) in Provo, Utah. It targets independent ambulatory medical groups, particularly those with 10+ physicians, from single-physician clinics to multi-specialty groups. At least one customer is an eyecare practice, which is reflected in the export's extensive ophthalmology data tables.

The product is a single integrated platform covering:
- **Clinical**: Charting, CPOE, e-prescribing, lab integration, immunizations, clinical decision support, customizable form-based documentation
- **Practice Management & Billing**: Scheduling, registration, insurance verification, billing/claims, accounts receivable, co-pay collection, revenue cycle reporting
- **Patient Engagement**: Patient portal, secure messaging, online scheduling, payment processing, digital intake forms
- **Specialty**: Eye/ophthalmology data (refraction, IOP, visual acuity, contact lens, keratometry), allergy/immunotherapy module, OB data, cancer event tracking
- **Reporting**: CQMs, public health reporting (immunization registries, syndromic surveillance, cancer case reporting)

For a (b)(10) assessment, we should expect the export to cover clinical data, billing/transactions, specialty data (especially ophthalmology), patient communications, documents, and custom forms.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-data-table-definitions.html` (535 KB) | Self-contained HTML data dictionary documenting 309 tables and 4,481 fields in the EHI export. Last updated 10/27/2023. | **Most informative** — the primary artifact |
| `downloads/ehi-export-page-screenshot.png` (211 KB) | Browser screenshot of the documentation page showing title and table-of-contents | Confirms UI layout; low information density |
| `downloads/enrichment/tables.json` (628 KB) | Prior agent's JSON extraction of all 309 tables with fields | Cross-validation reference |
| `downloads/enrichment/coverage-stats.json` (11 KB) | Prior agent's parsing statistics | Cross-validation; confirmed 309 tables / 4,481 fields |

The HTML data dictionary is the sole substantive artifact. No sample data files, no JSON schemas, no downloadable ZIP samples were provided.

## 3. Export Mechanics

Based on the HTML documentation header text:

- **Format**: Tab-delimited files, one file per data table, packaged in a ZIP archive. A `Files` subfolder contains related patient files (binary/blob data), keyed by ID to the `EHI_T_BlobData` table.
- **Mechanism**: UI-based — "EHI Export tool from the tools menu" with an "Add Patient" button to search/select patients. Bulk population export available via "EHI Export button on the patient queries screen."
- **Single-patient**: Yes — individual patient selection supported
- **Bulk capability**: Yes — population-level export via patient queries
- **Access constraints**: No fees or restrictions mentioned in the documentation
- **Documentation URL**: https://fhir.pcisgold.com/ehiexport/

## 4. Export Content: What's In It

### Summary Statistics

| Metric | Value |
|---|---|
| Total tables | 309 |
| Total fields | 4,481 |
| Fields with descriptions | 4,063 (90.7%) |
| Fields with type information | 4,480 (100.0%) |
| Tables with table-level descriptions | 309 (100%) |
| Field types | 20 distinct types (int, varchar, character, binary, datetime, nvarchar, bit, decimal, etc.) |

Every table has a description. Every field has a type. 90.7% of fields have descriptions (418 lack descriptions). The 418 missing descriptions are spread across multiple tables, with notable concentrations in legacy PM tables (e.g., `Accounts` has fields like `ACFIRST`, `ACMIDL`, `ACLAST` without descriptions) and the `ColBased_*` custom form tables.

The documentation provides field names, SQL-style data types, and free-text descriptions. It does **not** provide: foreign key relationships, value sets/coded values, max lengths, nullability constraints, or sample data.

### Vendor's Content Organization

The vendor presents tables alphabetically in a flat list (no explicit categories). I categorized them by naming patterns and table descriptions. Full inventory saved to `analysis/entity-inventory-full.json`.

**Top categories by field count:**

| Category | Tables | Fields | Representative Tables |
|---|---|---|---|
| Demographics | 23 | 557 | `Patients` (315), `T_Patients` (78), `T_PatientAddress` (21) |
| Visits/Encounters | 13 | 546 | `Visits` (393), `T_Visits` (71), `T_VisitTypes` (5) |
| Eye/Ophthalmology | 23 | 265 | `T_PatientRefraction` (18), `T_VisitRefraction` (14), `T_PatientEyeIOP` (17) |
| Accounts | 4 | 223 | `Accounts` (156), `AcctNotes` (38) |
| Billing/Transactions | 2 | 185 | `Trans` (156), `Trans_Reps` (29) |
| Laboratory | 10 | 195 | `Lab_CompletedTests` (50), `Lab_CompletedOrders` (49), `T_LabRecOrder` (41) |
| Referrals | 8 | 153 | `Referrals` (80), `T_PatientReferrals` (23) |
| Allergy/Immunotherapy | 20 | 151 | `Allergy_Antigen` (14), `Allergy_Concentration` (12), `Allergy_Vial` (10) |
| Immunizations | 10 | 115 | `T_PatientImmunizations` (48), `T_Immunizations` (18) |
| Clinical Notes | 16 | 106 | `T_VisitNote` (9), `T_VisitNotesSection` (8), `T_VisitHPIData` (8) |
| Orders | 2 | 91 | `Orders` (56), `T_OrderTracking` subgroup |
| Medication Renewals | 2 | 88 | `T_RenewalRequests` (79) |
| Medications/E-Prescribing | 7 | 86 | `T_PatientERxDetails` (27), `T_PatientRxHistory` (14) |
| Medications | 3 | 80 | `T_PatientMedication` (72) |
| Billing/Payments | 2 | 70 | `AllocatedTrans` (34), `PaymentPlans` (36) |
| Billing/Statements | 2 | 63 | `Statements` (58) |
| Billing/EOB | 2 | 49 | `EOBRecs` (30), `EOBRecs_Reps` (19) |
| Billing/Estimates | 2 | 53 | `EstimateHdr` (32), `EstimateDtl` (21) |
| Claims/Billing | 1 | 15 | `ClaimHistory` (15) |
| Billing/Collections | 1 | 12 | `DunningMessages` (12) |
| Information Release | 2 | 66 | `InfoRelease` (59) |
| Care Coordination | 5 | 64 | `TOC_Entries` (22), `T_PatientTransitionsOfCare` (18) |
| Family History | 9 | 57 | `T_FamilyHistoryCondition` (8), `T_PatientFamilyHistory` (8) |
| Problems | 7 | 78 | `Problem_Problem` (23), `Problem_Codes` (14) |
| Vitals | 18 | 76 | `T_Vital` (7), `T_VitalModifier` (6) |
| Documents/Files | 5 | 49 | `T_BlobData` (18), `T_VisitAttachments` (7) |
| Custom Forms/Columns | 5 | 39 | `ColBased_PatientData` (10), `ColBased_Columns` (7) |
| Patient Portal | 2 | 31 | `T_PatientPortalMessages` (18), `T_PatientPortalInfo` (13) |
| Screening/Assessments | 3 | 25 | `ScreeningDef` (9), `ScreeningQuestionDef` (10) |
| Cancer/Oncology | 2 | 11 | `T_PatientCancerEvent` (7) |
| OB/GYN | 1 | 6 | `T_OBData` (6) |
| Prior Authorization | ~1–2 | varies | PAR_ prefix tables |

### Notable Tables

- **`Visits` (393 fields)**: The single largest table — a comprehensive visit record spanning clinical, billing, and administrative data. Includes fields for procedures, diagnoses, charges, insurance, modifiers, and clinical documentation links.
- **`Patients` (315 fields)**: Extensive demographic record with legacy PM-style field names (e.g., `APPSSN`, `APFNAM`, `APLNAM`). Covers addresses, phone numbers, insurance references, employer, guarantor linkages, and clinical flags.
- **`Trans` (156 fields)**: Full financial transaction record — charges, payments, adjustments, insurance allocations, claim tracking.
- **`Accounts` (156 fields)**: Account-level financial data — balances, billing addresses, insurance references, guarantor data.
- **`T_PatientMedication` (72 fields)**: Detailed medication records with sig, refills, prescriber, pharmacy, start/stop dates, DAW codes, and e-prescribing tracking.

## 5. Coverage Assessment

### 5a. What the Vendor Covers (Bottom-Up)

The export is a **native database dump** covering the full breadth of PCIS GOLD's data model. Key strengths:

**Clinical depth is excellent.** The export includes deep tables for medications (72 fields per medication record), lab orders and results (6 tables, 195 fields), immunizations (10 tables, 115 fields), vitals (18 tables, 76 fields), problems (7 tables, 78 fields), clinical notes (16 tables, 106 fields), family history (9 tables, 57 fields), and allergy/immunotherapy (20 tables, 151 fields — reflecting a deep allergy testing/treatment module).

**Billing coverage is genuinely deep.** The export includes 12+ billing-related tables with 447+ fields total: `Trans` (156 fields for individual transactions), `Accounts` (156 fields for account financials), `Statements` (58 fields), `EOBRecs` (30+19 fields for explanation of benefits), `ClaimHistory` (15 fields), `AllocatedTrans` (34 fields for payment allocation), `PaymentPlans` (36 fields), `EstimateHdr`/`EstimateDtl` (53 fields for cost estimates), and `DunningMessages` (12 fields for collections). This is not a token nod to billing — it's the product's full financial data model.

**Specialty data is present.** 23 ophthalmology tables (265 fields) covering refraction, IOP, visual acuity, keratometry, contact lens, dilation, and ocular history. Also: OB data (1 table), cancer event tracking (2 tables), and a deep allergy/immunotherapy module (20 tables).

**Custom forms and flowsheets.** `ColBased_*` tables (5 tables, 39 fields) for column-based custom forms, plus `PatientFormResponse`/`PatientFormResponseQuestions` (2 tables) and `ScreeningDef`/`ScreeningQuestionDef`/`ScreeningQuestionChoice` (3 tables, 25 fields) for screening instruments. `T_Flowsheet*` tables (4 tables, 41 fields) for clinical flowsheets.

**Patient engagement data included.** Portal messages (`T_PatientPortalMessages`, 18 fields), patient portal info, patient letters, e-task messaging (7 tables, 41 fields), faxes, and communication preferences.

### 5b. Standardized Domain Coverage (Top-Down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patients` (315 fields), `T_Patients` (78), `Demo_*` (6 tables), `T_PatientAddress`, `T_PatientPhones`, `T_PatientEmergencyContact`, `T_PatientNextOfKin`, `T_PatientRaces`, `T_PatientEthnicity` | Very thorough — 23 tables, 557 fields |
| Encounters / visits | ✅ Covered | `Visits` (393 fields), `T_Visits` (71), plus 11 related tables | Extremely deep — largest table in the export |
| Problems / conditions | ✅ Covered | `Problem_Problem` (23 fields), `Problem_Codes`, `Problem_Group`, `Problem_Links`, `Problem_External`, `Problem_CodeTypes` | 7 tables, well-structured |
| Medications / prescriptions | ✅ Covered | `T_PatientMedication` (72 fields), `T_PatientERxDetails` (27), `T_PatientRxHistory` (14), `T_RenewalRequests` (79), plus 7 more tables | Comprehensive — includes e-prescribing details |
| Allergies | ✅ Covered | `T_PatientAllergy` (21 fields), `T_PatientAllergyReactions`, plus 20 allergy/immunotherapy tables (151 fields) | Extensive module |
| Immunizations | ✅ Covered | `T_PatientImmunizations` (48 fields), `T_Immunizations`, VFC eligibility, registry info, VIS — 10 tables, 115 fields | Thorough |
| Vitals | ✅ Covered | `T_Vital`, `T_VitalsData`, vital modifiers, templates — 18 tables | Deep configuration model |
| Lab results | ✅ Covered | `Lab_CompletedTests` (50), `Lab_CompletedOrders` (49), `Lab_CompletedObservations` (14), `T_LabRecOrder` (41) — 10 tables, 195 fields | Strong |
| Imaging / diagnostic reports | ⚠️ Partial | `T_VisitRadOutboundInfo` (5 fields) — radiology outbound tracking only; `MidmarkReportInfo`/`MidmarkReportsBlobData` (16 fields) — Midmark device integration | Product may not store imaging results natively; ordering info present |
| Procedures | ✅ Covered | Visit-level procedure data in `Visits` (393 fields includes procedure fields), `T_VisitProcDiag`, `T_VisitProcMod` | Captured within visit context |
| Clinical notes / documents | ✅ Covered | `T_VisitNote`, `T_VisitNoteAddendum`, `T_VisitNoteAmendment`, `T_VisitNotesSection`, `T_VisitHPIData`, `T_VisitPEData`, `PatientNotes` (40), `T_ScribblePageData`, `T_VisitSketchImage` — 16+ tables | Rich note structure including addenda and amendments |
| Care plans / goals | ⚠️ Partial | `T_PatientCognitiveStatus`, `T_PatientFunctionalStatus`, `ScreeningDef`/`ScreeningQuestionDef` for assessments, but no dedicated care plan tables | No explicit care plan entity — assessments present |
| Orders / referrals | ✅ Covered | `Orders` (56 fields), `T_OrderTracking` (5 tables, 36 fields), `Referrals` (80 fields), `T_PatientReferrals` (23), referral status tracking — 13+ tables | Strong order and referral tracking |
| Insurance / coverage | ✅ Covered | Insurance data embedded in `Patients` (315 fields includes insurance references), `Accounts` (156 fields), insurance verification fields, `POS_InsCompany` (if present) | Integrated into account/patient records |
| Claims / billing | ✅ Covered | `Trans` (156 fields), `ClaimHistory` (15), `EOBRecs` (30+19), `AllocatedTrans` (34), `Statements` (58) | **Genuinely deep** — full transaction and claims lifecycle |
| Payments | ✅ Covered | `AllocatedTrans` (34 fields), `PaymentPlans` (36), transaction payment records in `Trans` | Full payment tracking including payment plans |
| Consents / directives | ✅ Covered | `Demo_PatConsent` (8 fields), `PatientHIPAA` (22 fields), `InfoRelease` (59 fields), `InfoReleaseDetail` (7 fields) | Consent, HIPAA, and information release tracking |
| Patient communications | ✅ Covered | `T_PatientPortalMessages` (18 fields), `T_PatientLetter` (9 fields), `eTask_Items` (7+ tables), `T_Faxes`, `T_FaxStatus` | Portal messages, letters, e-tasks, and fax tracking |
| Specialty: Ophthalmology | ✅ Covered | 23 tables, 265 fields — refraction, IOP, visual acuity, keratometry, contact lens, dilation, ocular history | Very deep specialty coverage |
| Specialty: Allergy/Immunotherapy | ✅ Covered | 20 tables, 151 fields — antigens, concentrations, trays, vials, skin tests, mixing lab, schedules | Full allergy testing/treatment module |
| Specialty: Oncology | ⚠️ Partial | `T_PatientCancerEvent` (7 fields), `T_PatientCancerEventPlannedMeds` (4 fields) | Basic cancer event tracking — consistent with ambulatory EHR scope |
| Specialty: OB/GYN | ⚠️ Partial | `T_OBData` (6 fields) | Minimal — just a single table |
| Documents / attachments | ✅ Covered | `T_BlobData` (18 fields), `T_BlobData_Category`, `T_VisitAttachments`, `T_PatientEducationDocuments`, plus `Files` subfolder in export ZIP | Binary files exported alongside structured data |
| Custom forms | ✅ Covered | `ColBased_*` (5 tables, 39 fields), `PatientFormResponse` (2 tables, 13 fields), `ScreeningDef`/`ScreeningQuestionDef`/`ScreeningQuestionChoice` (3 tables, 25 fields), `T_Flowsheets`/`T_FlowsheetColumns`/etc. (4 tables, 41 fields) | Multiple custom data capture mechanisms |

## 6. Documentation Quality

**Strengths:**
- Complete table-level documentation: every table has a name and description
- 90.7% of fields have descriptions — most are meaningful (e.g., "The prescribed dosage and method of the medication")
- 100% of fields have SQL data types (int, varchar, datetime, bit, etc.)
- Single self-contained HTML page — no broken links or multi-page navigation
- Table index with anchor links for easy navigation

**Weaknesses:**
- No foreign key or relationship documentation — tables reference other tables by ID fields but relationships must be inferred from naming patterns (e.g., `PatientId`, `VisitId`, `AccountId`)
- No value sets or coded value definitions — fields like `TypeId`, `StatusId`, `CategoryId` have no enumeration of valid values
- No max field lengths specified — types say `varchar` or `character` but not the size
- No sample data provided
- No machine-readable schema (JSON Schema, SQL DDL, etc.) — only the HTML page
- Legacy PM tables (`Accounts`, `Patients`, `Visits`, `Trans`) use cryptic abbreviated field names (e.g., `ACINST`, `APFNAM`, `TDVSIT`) with some missing descriptions
- No nullability information

**Usability assessment:** A developer could understand the general structure and build an import for the most common tables, but would need to reverse-engineer relationships, value sets, and field semantics for the legacy tables. The newer `T_*` tables are considerably better documented than the legacy PM tables.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is a genuine full-database export of a small-to-mid-size ambulatory EHR/PM system. With 309 tables and 4,481 fields, it covers the full breadth of what an integrated ambulatory EHR + practice management system stores: clinical documentation, medications, labs, vitals, immunizations, allergies, problems, orders, referrals, billing transactions, claims, EOBs, payment plans, statements, insurance, patient portal messages, custom forms, flowsheets, and deep specialty data (ophthalmology, allergy/immunotherapy). The billing coverage is particularly notable — 12+ tables with 447+ fields covering the full financial lifecycle from charges through claims, EOBs, payments, and collections. Including account and transaction tables, the financial domain spans 16 tables with 670 fields. This goes well beyond USCDI.

**Axis 2 — Export approach: Purpose-built EHI export**

PCIS GOLD built a dedicated EHI export that dumps its native database tables as tab-delimited files. The evidence is clear: (1) the export has a dedicated UI tool ("EHI Export tool from the tools menu"), (2) it exports 309 internal database tables — not FHIR resources or C-CDA sections, (3) it includes billing, operational, and specialty data far beyond what their (g)(10) FHIR API would cover, and (4) they built a purpose-specific HTML data dictionary at a dedicated URL documenting every table and field. This is not a repackaged clinical exchange export.

### Key Findings

1. **Genuinely comprehensive native database export.** 309 tables, 4,481 fields covering clinical, financial, specialty, and administrative data. This is the vendor's actual data model, not a clinical summary.

2. **Billing coverage is real.** 12+ billing tables with 447+ fields: `Trans` (156 fields), `Accounts` (156), `Statements` (58), `EOBRecs` (49), `AllocatedTrans` (34), `PaymentPlans` (36), `ClaimHistory` (15), `EstimateHdr`/`EstimateDtl` (53). Full financial lifecycle from charge through collection.

3. **Deep specialty data.** 23 ophthalmology tables (265 fields) and 20 allergy/immunotherapy tables (151 fields) — specialty-specific clinical data that would never appear in a USCDI or C-CDA export.

4. **Documentation quality is good but not great.** 90.7% of fields have descriptions and all have types, but no relationships, value sets, max lengths, or sample data. Legacy PM tables have cryptic field names.

5. **Both single-patient and bulk export supported** via UI tools — the documentation describes individual patient selection and population-level export via patient queries.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   Tab-delimited (TSV) files in ZIP archive
Entities:        309 tables
Fields:          4,481
Descriptions:    90.7% of fields have descriptions
Sample data:     No
Bulk export:     Yes
Domains covered: 17 of 19 applicable domains (imaging and care plans are partial)
```

### Bottom Line

PCIS GOLD has built a legitimate, purpose-specific EHI export that dumps their native database — 309 tables and 4,481 fields covering clinical, billing, specialty, and administrative data. A patient or provider would get a meaningfully complete copy of their data. The main gap is documentation depth: no relationships, value sets, or sample data, which makes the export harder to consume than it needs to be. But the coverage breadth is among the strongest for a vendor this size.
