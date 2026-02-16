# EHI Export Analysis: Juno Health

**Product**: Juno EHR v24
**Analysis date**: 2026-02-16
**CHPL IDs**: 11497 (15.04.04.2925.Juno.23.02.1.240809)

## 1. Product Context

Juno EHR is a cloud-native EHR from Juno Health (a division of Document Storage Systems, Inc./DSS), certified in August 2024. DSS has 30+ years of VA/VistA integration experience; Juno EHR is their commercial product for non-VA markets. Ranked #1 EHR for rural hospitals by Black Book in 2025.

**Target settings**: Acute care hospitals (especially critical access/rural), behavioral health facilities, state mental health systems, and public health agencies. Notable customers include state health departments (Tennessee, Florida, Idaho, New York) and rural hospitals.

**Key modules and data domains** (relevant to export completeness):
- **Clinical documentation**: 400+ pre-built templates, Clinical Content Builder, flowsheets, assessments, AI Scribe
- **Orders & medications**: CPOE, e-prescribing (Surescripts/EPCS), medication reconciliation, pharmacy (unit dose, IV, outpatient)
- **Behavioral health**: Treatment plans with "Golden Thread" linking, group therapy notes, 150+ BH assessments, session management
- **Surgery/perioperative**: AORN-compliant perioperative nursing documentation
- **Public health**: Immunization registry, disease surveillance, outbreak response
- **Revenue cycle management**: Charge posting, claim submission (UB-04, CMS-1500), ERA processing
- **Patient portal**: Secure messaging, appointment scheduling, prescription refills (separately certified)
- **Scheduling**: Appointment scheduling integrated with clinical workflows
- **Emergency department**: JESS (Juno Emergency Services Solution, separately certified)
- **Quality reporting**: CQMsolution for clinical quality measure reporting (separately certified)
- **E-prescribing**: RxTracker (separately certified, originated as VA product)

This product stores data across clinical, behavioral health, pharmacy, billing, public health, and administrative domains. A complete EHI export should cover all of these.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `main-ehiexport-page.html` (70 KB) | Main EHI Tables Export landing page on HubSpot. Describes CSV export format, links to four component-specific data dictionaries. | Medium — provides export mechanics overview |
| `jehr-data-dictionary.html` (201 KB) | JunoEHR Export Schema index page listing 1,256 database tables with links to individual table documentation. | **High** — primary data dictionary index |
| `rtvx-data-dictionary.html` (17 KB) | RxTracker Export Schema index page listing 66 database tables for the pharmacy/prescribing module. | **High** — pharmacy data dictionary |
| `connectehr-cqmsolution-page.html` (84 KB) | ConnectEHR & CQMsolution EHI Export page describing C-CDA 2.1 and QRDA I exports. | Low — secondary export mechanism, no data dictionary |
| `patient-portal-page.html` (85 KB) | Patient Portal EHI Export page describing C-CDA export for portal data. | Low — secondary export, no data dictionary |
| 1,322 individual table pages (fetched live) | Individual HTML pages at `ehiexports.junohealth.com/jehr/*.html` and `ehiexports.junohealth.com/rtvx/*.html` documenting every column, type, description, primary keys, and foreign keys. | **High** — the core field-level documentation |
| 6 screenshots (PNG) | Screenshots of the above pages for visual reference. | Low — confirmatory |

The individual table detail pages (not included in the original downloads but fetched during analysis) are the most informative artifacts. Each page documents a single database table with: table description, primary key(s), foreign key relationships with hyperlinked references, and column-level detail (ordinal position, name, SQL data type, natural-language description).

## 3. Export Mechanics

**Primary export (Juno EHR + RxTracker):**
- **Format**: CSV files reflecting the native database schema, plus non-tabular files (images, PDFs, XML, text documents) exported alongside
- **Mechanism**: Manual, UI-driven — described as "a manual one-time export of health data for one or more patients"
- **Scope**: Single-patient or multi-patient ("one or more patients")
- **Bulk**: Yes — supports exporting multiple patients
- **Access**: Staff with appropriate permissions via EHR UI
- **Fees**: Not mentioned
- **Variability**: Content varies based on software applications in use, version, documentation practices, configuration, and materials not sourced from Juno

**Secondary exports:**
- **ConnectEHR**: C-CDA 2.1 XML, single-patient or bulk, scheduled or on-demand. Certified to (b)(10) under "limited ePHI USCDIv1 definition." Also supports FHIR API (DocumentReference, Bulk Data Export). Path: Administration > Data Export > Data Export.
- **CQMsolution**: QRDA I XML patient-level quality measure data. Claims "contains all EHI stored in Juno CQMsolution for each patient."
- **Patient Portal**: C-CDA format, single-patient or population export. Path: Organization > Reports > Regulatory Reports > Electronic Health Information Request.

The ConnectEHR and Patient Portal exports are explicitly described as limited to USCDIv1 scope. The primary CSV export is the comprehensive (b)(10) mechanism.

## 4. Export Content: What's In It

### Summary Statistics

All figures derived from parsing 1,322 individual table documentation pages (see `analysis/full-entity-inventory.json`):

| Metric | JunoEHR | RxTracker | Combined |
|---|---|---|---|
| Tables | 1,256 | 66 | 1,322 |
| Total columns | 9,045 | 1,190 | 10,235 |
| Columns with descriptions | 9,045 (100%) | 1,190 (100%) | 10,235 (100%) |
| Foreign key relationships | 2,093 | 152 | 2,245 |
| Tables with table-level descriptions | 1,242 (98.9%) | 66 (100%) | 1,308 (98.9%) |
| Tables with foreign keys | — | — | 826 (62.5%) |

**Column count distribution:**

| Range | Count |
|---|---|
| 0-1 columns | 9 (including 2 trace tables with 0) |
| 2-5 columns | 796 |
| 6-10 columns | 324 |
| 11-20 columns | 115 |
| 21-50 columns | 64 |
| 51-100 columns | 9 |
| 100+ columns | 7 |

Of the 1,322 tables, 546 are lookup/reference tables (LK prefix) with 2,578 columns, and 776 are data tables with 7,657 columns. The lookup tables provide coded value definitions that make the CSV export self-contained.

### Documentation quality per field

Every single column (10,235 of 10,235) has a natural-language description. Descriptions range from brief ("Unique identifier for the table") to detailed multi-sentence explanations of business logic (e.g., AU_PRESCRIPTION's description: "Contains all outpatient RX data used by the outpatient pharmacy package… Deletion of an entry in this file must be handled VERY carefully and is not allowed if refills have been issued").

All columns have SQL data types specified (INT, NVARCHAR, DATETIME, BIT, DECIMAL, FLOAT, etc.). Foreign key relationships are documented with hyperlinked cross-references to the referenced table. Primary keys are identified for each table.

### Vendor's own content organization

The data dictionary is organized alphabetically by table name, not by clinical domain. Tables use naming conventions reflecting their data lineage:

- **AU_ prefix** (60 tables): VA/VistA-heritage pharmacy tables (Automated Unit dose)
- **LK prefix** (546 tables): Lookup/reference tables providing coded values
- **RCM prefix** (billing): Revenue Cycle Management tables
- **No prefix** (remainder): Modern FHIR-aligned naming (ENCOUNTER, PATIENT, CONDITION, OBSERVATION, etc.)

### 20 Largest Tables (representative examples)

| Table | Columns | Schema | Domain |
|---|---|---|---|
| RCMUB04CLAIM | 260 | jehr | Billing — UB-04 institutional claim form |
| RCM1500CLAIM | 116 | jehr | Billing — CMS-1500 professional claim form |
| BILLINGITEM | 115 | jehr | Billing — chargeable transactions |
| AU_PRESCRIPTION | 113 | jehr | Pharmacy — outpatient prescriptions |
| MEDICATION_ORDERS | 110 | rtvx | Pharmacy — medication orders |
| AU_NON-VERIFIED_ORDERS | 103 | jehr | Pharmacy — unit dose orders pending verification |
| AU_PHARMACY_PATIENT_UNIT_DOSE | 102 | jehr | Pharmacy — active unit dose orders per patient |
| OUTPATIENT_MEDICATIONS | 100 | rtvx | Pharmacy — outpatient medication list |
| INPATIENT_MEDICATIONS | 80 | rtvx | Pharmacy — inpatient medications |
| AU_PHARMACY_PATIENT_IV | 71 | jehr | Pharmacy — IV orders per patient |
| LKREGADTCONTROL | 67 | jehr | Registration — ADT control table |
| ENCOUNTER | 59 | jehr | Encounters — patient-provider interactions |
| IMPLANTABLEDEVICEINTRAOPERATIVE | 59 | jehr | Devices — intraoperative implantable devices |
| AU_PENDING_OUTPATIENT_ORDERS | 55 | jehr | Pharmacy — pending OE/RR orders |
| ENCOUNTERINSURANCE | 54 | jehr | Encounters — insurance mapping |
| ALLERGY | 51 | jehr | Allergies — clinical allergy assessments |
| PATIENT | 50 | jehr | Demographics — core patient record |
| AU_PHARMACY_PATIENT | 45 | jehr | Pharmacy — patient-level pharmacy info |
| HOSPITAL_MEDICATIONS | 45 | rtvx | Pharmacy — hospital medication records |
| ORDERS | 45 | rtvx | Orders — clinical orders |

The complete inventory of all 1,322 tables with all 10,235 fields is in `analysis/full-entity-inventory.json`.

### Domain breakdown by column count

| Domain | Tables | Columns | % of Total |
|---|---|---|---|
| Pharmacy/Prescriptions (VA legacy) | 60 | 986 | 9.6% |
| Billing/Revenue Cycle | 71 | 955 | 9.3% |
| Medications | 98 | 916 | 8.9% |
| Encounters/Visits | 83 | 697 | 6.8% |
| Patient/Demographics | 70 | 628 | 6.1% |
| Questionnaires/Assessments | 67 | 578 | 5.6% |
| Observations/Vitals/Labs/Imaging | 89 | 503 | 4.9% |
| Orders | 62 | 434 | 4.2% |
| Scheduling | 70 | 429 | 4.2% |
| Reference/Configuration | 89 | 339 | 3.3% |
| Registration/Admin | 32 | 295 | 2.9% |
| Goals/Interventions | 45 | 255 | 2.5% |
| Devices/Implants | 26 | 229 | 2.2% |
| Conditions/Problems | 32 | 221 | 2.2% |
| Procedures/Surgery | 38 | 209 | 2.0% |
| Documents/Notes | 27 | 196 | 1.9% |
| Care Plans/Treatment Plans | 37 | 185 | 1.8% |
| Allergies/Adverse Events | 20 | 161 | 1.6% |
| Immunizations | 33 | 158 | 1.5% |
| Nutrition | 27 | 144 | 1.4% |
| Referrals/Service Requests | 19 | 90 | 0.9% |
| Other/Uncategorized | 101 | 991 | 9.7% |
| Lookup Tables (uncategorized) | 84 | 370 | 3.6% |

Note: "Other/Uncategorized" (101 tables, 991 columns) includes tables like ACCOMMODATION, ADDRESS, ADMITTINGCRIMINALSTATUS, CLINICALTASK, CONSENT (if present via other naming), and various supporting entities that span multiple domains.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized as a complete native database dump across two schemas:

**JunoEHR schema (1,256 tables, 9,045 columns)** — the core EHR covering:
- Patient demographics and identification (PATIENT with 50 fields, plus HUMANNAME, CONTACTPOINT, ADDRESS, IDENTIFIER, and numerous related tables)
- Encounters/admissions/discharges/transfers (ENCOUNTER with 59 fields, ENCOUNTERINSURANCE with 54, plus admission waitlists, bed status, census tracking)
- Conditions/problems (CONDITION, CONDITIONCODING, CONDITIONBODYSITE, CONDITIONEVIDENCE — 32 tables)
- Observations/vitals/labs/imaging (OBSERVATION, OBSERVATIONVALUE, DRAFTOBSERVATION, IMAGINGSTUDY, SPECIMEN, DIAGNOSTICREPORT — 89 tables)
- Medications and pharmacy (AU_PRESCRIPTION with 113 fields, plus 98 MEDICATION-prefix tables, DRUGORDER and related)
- Allergies (ALLERGY with 51 fields, ALLERGYREACTION, PATIENTALLERGY — 20 tables)
- Immunizations (IMMUNIZATION, IMMUNIZATIONFORECAST, IMMUNIZATIONEDUCATION — 33 tables)
- Procedures/surgery (PROCEDURE, SURGERYINTRAOPERATIVE, ANESTHESIATYPE, IMPLANTABLEDEVICE — 38+ tables)
- Care plans/treatment plans (CAREPLAN with 37 related tables — critical for behavioral health "Golden Thread")
- Billing/RCM (RCMUB04CLAIM with 260 fields, RCM1500CLAIM with 116, BILLINGITEM with 115, COVERAGE, ACCOUNT — 71 tables)
- Documents/notes (DOCUMENTREFERENCE, AMENDMENTREQUEST, COMPOSITION — 27 tables)
- Questionnaires/assessments (QUESTIONNAIRE, QUESTIONNAIREITEM, QUESTIONNAIRERESPONSE — 67 tables; supports the 400+ configurable templates)
- Orders (ORDER, ORDERABLE, ORDERACTION — 62 tables)
- Scheduling (SCHEDULE, APPOINTMENT, SLOT — 70 tables)
- Goals/interventions (GOAL, INTERVENTION, CAREPLANACTIVITY — 45 tables)
- Behavioral health (GROUPSESSION, GROUPSESSIONPARTICIPANT, BEHAVIORALHEALTHPATIENTPRACTITIONERCONFLICT — 4 explicit tables, though BH data is also in care plans, questionnaires, and notes)
- Communications/messages (11 tables)
- Nutrition (NUTRITIONORDER, NUTRITIONPRODUCT — 27 tables)
- Devices/implants (IMPLANTABLEDEVICE, DEVICE — 26 tables)
- Referrals/service requests (SERVICEREQUEST, REFERRAL — 19 tables)

**RxTracker schema (66 tables, 1,190 columns)** — the e-prescribing/pharmacy module:
- Patient records (PATIENTS, PERSONS, PERSONS_ALLERGIES, PERSONS_PROBLEMS)
- Prescriptions (PRESCRIPTIONS, MEDICATION_ORDERS with 110 fields, OUTPATIENT_MEDICATIONS with 100, INPATIENT_MEDICATIONS with 80)
- Encounters and visits (ENCOUNTERS, VISITS, ENCOUNTERS_DIAGNOSES)
- Orders and reconciliations (ORDERS, RECONCILIATIONS and related tables)
- Documents and notes (DOCUMENTS, VISITS_NOTES)

The richest domains by column count are pharmacy (986 + 916 = 1,902 columns across AU_ and medication tables), billing (955 columns), and encounters (697 columns). The pharmacy depth reflects DSS's 30+ year VA pharmacy heritage.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PATIENT (50 fields), HUMANNAME, CONTACTPOINT, ADDRESS, RELATEDPERSON, IDENTIFIER + 70 total tables | Thorough — includes race, ethnicity, language, guardian, identifiers |
| Encounters / visits | ✅ Covered | ENCOUNTER (59 fields), ENCOUNTERINSURANCE (54), ADMISSIONWAITLIST, BEDSTATUS, CENSUS — 83 tables | Deep — includes admission, discharge, transfer, bed tracking |
| Problems / conditions | ✅ Covered | CONDITION, CONDITIONCODING, CONDITIONBODYSITE, CONDITIONEVIDENCE, PROBLEMDEFINITION — 32 tables | Thorough — coded diagnoses with body site and evidence |
| Medications / prescriptions | ✅ Covered | AU_PRESCRIPTION (113 fields), DRUGORDER, MEDICATIONREQUEST, MEDICATIONADMINISTRATION, MEDICATIONSTATEMENT + RxTracker's 66 tables — 158 combined tables | Exceptionally deep — VA-heritage pharmacy + modern medication management |
| Allergies | ✅ Covered | ALLERGY (51 fields), ALLERGYREACTION, PATIENTALLERGY — 20 tables | Thorough — reactions, manifestations, clinical status, coding |
| Immunizations | ✅ Covered | IMMUNIZATION, IMMUNIZATIONFORECAST, IMMUNIZATIONEDUCATION, IMMUNIZATIONELIGIBILITY — 33 tables | Deep — includes forecasting, lot tracking, vaccine education |
| Vitals | ✅ Covered | OBSERVATION, OBSERVATIONVALUE, DRAFTOBSERVATION tables within Observations domain | Covered as part of observation framework |
| Lab results | ✅ Covered | OBSERVATION tables, SPECIMEN, DIAGNOSTICREPORT, IMAGINGSTUDYSERIES — 89 tables in combined Observations/Labs domain | Covered through observation and diagnostic report tables |
| Imaging / diagnostic reports | ✅ Covered | IMAGINGSTUDY, IMAGINGSTUDYSERIES, DIAGNOSTICREPORT, DIAGNOSTICREPORTCLINICALCOMMUNICATION | Covered — study and series level, though imaging files themselves may reference external PACS |
| Procedures | ✅ Covered | PROCEDURE, SURGERYINTRAOPERATIVE, ANESTHESIATYPE, IMPLANTABLEDEVICE — 38 tables | Deep — includes perioperative documentation and implantable devices |
| Clinical notes / documents | ✅ Covered | DOCUMENTREFERENCE, COMPOSITION, NARRATIVE, AMENDMENTREQUEST — 27 tables; non-tabular files (PDFs, images) exported alongside CSVs | Thorough — structured references plus actual document files |
| Care plans / goals | ✅ Covered | CAREPLAN (37 related tables), GOAL, INTERVENTION — 82 combined tables | Deep — critical for BH treatment planning with "Golden Thread" |
| Orders / referrals | ✅ Covered | ORDER, ORDERABLE, ORDERACTION, SERVICEREQUEST — 62+ tables | Thorough — CPOE-level detail |
| Insurance / coverage | ✅ Covered | COVERAGE (24 fields), COVERAGEINSURANCEPLAN, ENCOUNTERINSURANCE, LKINSURANCECOMPANY, LKINSURANCEPLAN — part of 71 billing tables | Thorough — plan, payer, and coverage details |
| Claims / billing | ✅ Covered | RCMUB04CLAIM (260 fields), RCM1500CLAIM (116 fields), BILLINGITEM (115 fields), CHARGEITEMDEFINITION — 71 tables, 955 columns | Exceptionally deep — institutional (UB-04) and professional (CMS-1500) claim forms with full field detail |
| Payments | ✅ Covered | TRANSACTIONCODE, RCM-related payment tables | Present but less detail than claims |
| Consents / directives | ❌ Not covered | No CONSENT or ADVANCEDIRECTIVE tables found in the data dictionary | Unclear gap — product likely captures consents but no dedicated export tables identified |
| Patient communications / portal | ⚠️ Partial | 11 communication/message lookup tables in JEHR; Patient Portal has separate C-CDA export (USCDIv1 only) | Portal messages may not be in the native CSV export; portal has its own limited C-CDA export |
| Behavioral health (specialty) | ✅ Covered | GROUPSESSION (4 explicit tables), plus CAREPLAN (37 tables), QUESTIONNAIRE (67 tables) for BH assessments and treatment plans | Covered — BH-specific group sessions, plus shared frameworks for treatment planning and assessments. The 150+ BH assessments are captured through the questionnaire framework |
| Public health (specialty) | ✅ Covered | IMMUNIZATION (33 tables), CONDITION (for disease surveillance), OBSERVATION (for monitoring) | Covered through standard clinical tables — no dedicated public health surveillance tables visible, but immunization registry data is comprehensive |

### Key coverage observations

1. **Billing is genuinely deep**: The RCMUB04CLAIM table alone has 260 fields capturing the complete UB-04 institutional claim form. Combined with RCM1500CLAIM (116 fields) and BILLINGITEM (115 fields), this is one of the most detailed billing exports observed.

2. **Pharmacy coverage is exceptional**: Combining the 60 AU_PRESCRIPTION tables (VA heritage) with 98 modern medication tables in JEHR plus 66 RxTracker tables yields approximately 158 pharmacy/medication tables with nearly 2,000 columns.

3. **Questionnaire framework is large**: 67 tables with 578 columns support the vendor's configurable assessment and template system — important for behavioral health's 400+ templates.

4. **Missing consent tables**: No dedicated consent or advance directive tables were found. This is a minor gap — consents are part of the designated record set, though the product may capture them through the document framework.

## 6. Documentation Quality

**Exceptional for field-level detail.** Every column in all 1,322 tables has:
- Column name
- SQL data type (INT, NVARCHAR, DATETIME, BIT, DECIMAL, FLOAT, etc.)
- Ordinal position
- Natural-language description (100% coverage — 10,235 of 10,235 columns described)

**Strong for relationships.** 2,245 foreign key relationships are documented with hyperlinked cross-references between tables. 826 of 1,322 tables (62.5%) have at least one documented foreign key. Primary keys are identified for every table.

**Good table-level descriptions.** 1,308 of 1,322 tables (98.9%) have a table-level narrative description explaining what the table stores. Only 14 tables lack descriptions (including AMENDMENTREQUEST, BILLTYPE, CARETEAM, GROUP, LOCATION, VALUE, and 2 trace tables).

**Hosted on a dedicated subdomain.** The data dictionary is served as static HTML from Azure blob storage at `ehiexports.junohealth.com`, suggesting deliberate investment in documentation infrastructure. Last modified 2026-01-23.

**What's missing:**
- **No sample data or worked examples** — a developer cannot see what an actual export looks like
- **No value set documentation** — coded fields reference lookup (LK) tables, but the allowed values aren't enumerated inline. However, the 546 LK tables themselves would be exported as CSVs alongside the data, making the export self-documenting for coded values
- **No explicit nullability or max-length constraints** — column definitions include type but not constraints
- **No versioning or changelog** for the data dictionary
- **No machine-readable schema** (e.g., JSON Schema, SQL DDL) — only HTML documentation

**Could a developer build an import?** Yes, with significant effort. The documentation provides enough information to understand the structure: table relationships, column types, and descriptions. The main challenge would be the proprietary schema — there's no mapping to FHIR or other standards, so a developer would need to understand Juno's domain model. The lookup tables would need to be cross-referenced for coded values. A machine-readable schema would significantly reduce implementation effort.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

Juno Health's EHI export is a genuine native database dump with field-level documentation across 1,322 tables and 10,235 columns. It covers clinical, pharmacy, billing, behavioral health, immunization, surgery, and administrative domains — essentially the full breadth of what the product stores. The 100% field description rate and extensive foreign key documentation make this one of the most thoroughly documented EHI exports observed.

### Key Findings

1. **Exceptionally large and well-documented data dictionary.** 1,322 tables with 10,235 columns, all with descriptions, types, and relationship documentation. This is among the most comprehensive EHI export schemas available, reflecting the depth of a product with 30+ years of VA clinical software heritage.

2. **Genuine billing/RCM coverage.** Unlike many vendors that omit billing data, Juno exports complete UB-04 claims (260 fields), CMS-1500 claims (116 fields), billing items, insurance, and coverage data — 71 tables with 955 columns dedicated to revenue cycle.

3. **Deep pharmacy coverage spanning two eras.** The VA-heritage AU_PRESCRIPTION tables (60 tables) and modern FHIR-aligned medication tables (98 tables) plus RxTracker's separate 66-table schema provide extraordinary pharmacy/medication detail.

4. **Multi-component export architecture.** The vendor documents four separate certified components (Juno EHR CSV, RxTracker CSV, ConnectEHR C-CDA, Patient Portal C-CDA), with the CSV exports being the comprehensive (b)(10) mechanism and the C-CDA exports being limited USCDIv1 projections. The vendor is transparent about this distinction.

5. **No sample data provided.** Despite excellent schema documentation, there are no sample export files, worked examples, or demonstration datasets. This is the primary gap in the documentation.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (native database tables) + non-tabular files (images, PDFs, XML, text)
Model type:      Native database
Entities:        1,322 (1,256 JunoEHR + 66 RxTracker)
Fields:          10,235 (9,045 JunoEHR + 1,190 RxTracker)
Descriptions:    100% (10,235 of 10,235 fields described)
Sample data:     No
Bulk export:     Yes (single-patient or multi-patient)
Domains covered: 17 of 18 applicable domains (missing: consents/directives)
```

### Bottom Line

Juno Health's EHI export is one of the strongest (b)(10) implementations reviewed. With 1,322 native database tables, 10,235 fully-described columns, deep billing/RCM coverage (71 tables), and comprehensive pharmacy data (158+ tables across three schemas), this is a genuine "all EHI" export — not a clinical summary repackaged. The only notable gaps are the absence of dedicated consent/directive tables and the lack of sample data to validate what the export actually produces.
