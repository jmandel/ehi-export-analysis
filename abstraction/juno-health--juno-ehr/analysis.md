# EHI Export Analysis: Juno Health

**Product**: Juno EHR v24
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2925.Juno.23.02.1.240809

## 1. Product Context

Juno Health (a division of Document Storage Systems/DSS, Inc.) offers a cloud-native EHR primarily serving acute care hospitals (especially critical access/rural), behavioral health facilities, state mental health systems, and public health agencies. DSS has 30+ years of VA/VistA heritage, and the product incorporates pharmacy (RxTracker), order management, perioperative, behavioral health, and other modules originally built for the VA ecosystem.

**Key data domains the product stores:**
- **Clinical records**: Demographics, problem lists, medication lists, allergies, vital signs, lab results, clinical notes (400+ templates), assessments, consults, admission/discharge/transfer records
- **Orders & medications**: CPOE, e-prescribing (EPCS via Surescripts), medication administration (BCMA/eMAR), pharmacy (inpatient and outpatient), prior authorization
- **Behavioral health**: Treatment plans with goals/objectives/interventions, group therapy notes, 150+ assessments, "Golden Thread" linking assessment → treatment plan → notes → outcomes → discharge
- **Surgery/perioperative**: AORN-compliant perioperative nursing documentation, surgical case records
- **Public health**: Immunization registry, disease surveillance, outbreak response
- **Revenue cycle**: Integrated billing with charge posting, claim submission (UB-04, CMS-1500), ERA processing
- **Patient engagement**: Portal with secure messaging, appointment requests, prescription refills
- **Quality reporting**: CQM (QRDA I/III) via CQMsolution module

The certified product includes six separately certified modules: Juno EHR, ConnectEHR, CQMsolution, RxTracker, JESS (Emergency Services), and Patient Portal.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/main-ehiexport-page.html` (70 KB) | Main EHI export landing page on HubSpot. Describes CSV export format, mentions non-tabular file export, links to four component-specific docs. | Medium — provides overview and export mechanism description |
| `downloads/jehr-data-dictionary.html` (201 KB) | Juno EHR Export Schema index page listing 1,256 database tables with links to individual table documentation. | **High** — primary artifact; the gateway to 1,256 individual table pages |
| `downloads/rtvx-data-dictionary.html` (17 KB) | RxTracker Export Schema index page listing 66 database tables. | **High** — covers e-prescribing/pharmacy module separately |
| `downloads/connectehr-cqmsolution-page.html` (84 KB) | ConnectEHR (C-CDA 2.1 export) and CQMsolution (QRDA I export) documentation. Explicitly states these are certified to (b)(10) under "limited ePHI USCDIv1 definition." | Medium — confirms these are USCDI-scoped supplements, not the primary export |
| `downloads/patient-portal-page.html` (85 KB) | Patient Portal EHI export documentation. C-CDA format, certified to (b)(10) under USCDIv1. | Low — thin process description, no data dictionary |
| Screenshots (×6) | Visual captures of each page | Low — confirm page content matches HTML |

**Most informative**: The JEHR and RTVX data dictionary index pages, plus the 1,322 individual table pages fetched from `ehiexports.junohealth.com` during analysis (cached in `analysis/table_pages_cache/`). Each table page contains field-level documentation with names, types, descriptions, primary keys, and foreign key relationships.

## 3. Export Mechanics

- **Format**: CSV files reflecting native database structures, plus non-tabular files (images, PDFs, XML, text documents) exported alongside the CSVs
- **Mechanism**: Manual one-time export initiated through the EHR UI; described as "EHI Export allows health systems to do a manual one-time export of health data for one or more patients"
- **Scope**: Single-patient or multi-patient ("one or more patients")
- **Bulk capability**: Yes — supports selecting multiple patients
- **Access constraints**: Requires "enhanced permissions" for staff; no mention of fees
- **Supplemental exports**: ConnectEHR provides C-CDA 2.1 export (scheduled or on-demand, single or bulk), Patient Portal provides C-CDA export (on-demand), CQMsolution provides QRDA I XML export — all three explicitly certified to (b)(10) but under the "limited ePHI USCDIv1 definition"

The primary (b)(10) export is the CSV table dump from Juno EHR and RxTracker. The C-CDA and QRDA exports are secondary, USCDI-scoped mechanisms that the vendor transparently labels as limited.

## 4. Export Content: What's In It

### Data dictionary scope

The export documentation comprises **1,322 database tables** across two modules:
- **Juno EHR (JEHR)**: 1,256 tables, 9,045 fields
- **RxTracker (RTVX)**: 66 tables, 1,190 fields
- **Combined total**: 1,322 tables, 10,235 fields

**Documentation quality metrics:**
- Fields with descriptions: **10,235 of 10,235 (100%)**
- Tables with descriptions: **1,308 of 1,322 (98.9%)**
- Tables with foreign key documentation: **826 of 1,322 (62.5%)**
- Tables with primary key documentation: **126 of 1,322 (9.5%)**
- Data types documented for every field (INT, NVARCHAR, DATETIME, BIT, DECIMAL, etc.)

### Vendor's own content organization

The data dictionary is organized alphabetically (A–V) without vendor-defined categories. The following categorization was derived from table names, descriptions, and foreign key relationships:

| Category | Tables | Fields | Representative Tables |
|---|---|---|---|
| Lookup/Reference | 546 | 2,578 | LKALLERGYCLINICALSTATUS, LKMEDROUTE, LKGENDER |
| Medications | 95 | 861 | MEDICATIONREQUEST, MEDICATIONADMINISTRATION, OUTPATIENT_MEDICATIONS |
| Pharmacy/Prescription | 60 | 986 | AU_PRESCRIPTION (113 fields), AU_PHARMACY_PATIENT_UNIT_DOSE (102), AU_PHARMACY_PATIENT_IV (71) |
| Patient Demographics | 60 | 509 | PATIENT (50 fields), RELATEDPERSON, PERSONS, ADDRESS |
| Questionnaires/Forms | 57 | 550 | QUESTIONNAIRE, QUESTIONNAIRERESPONSE, ITEM, ITEMBUNDLE |
| Encounters | 56 | 514 | ENCOUNTER (59 fields), EPISODEOFCARE, ENCOUNTERINSURANCE |
| Orders | 51 | 556 | MEDICATION_ORDERS (110), SERVICEREQUEST, ORDERS, PENDINGORDER |
| Goals/Interventions | 42 | 235 | GOAL, INTERVENTION, INTERVENTIONPROGRESS, INTERVENTIONOUTCOME |
| Billing/Financial | 41 | 845 | RCMUB04CLAIM (260 fields), RCM1500CLAIM (116), BILLINGITEM (115) |
| Conditions/Problems | 41 | 275 | CONDITION, PROBLEM, DIAGNOSES, DETECTEDISSUE |
| Documents/Notes | 38 | 287 | DOCUMENTREFERENCE, DOCUMENTS, CLINICALNOTESCONFIGURATION |
| Observations/Vitals | 32 | 248 | OBSERVATION, DRAFTOBSERVATION, PERSONS_VITAL_STATISTICS |
| Organizations/Providers | 29 | 315 | ORGANIZATION, PRACTITIONER, LOCATION, HEALTHCARESERVICE |
| Procedures/Surgery | 23 | 184 | PROCEDURE, IMPLANTABLEDEVICEINTRAOPERATIVE (59), ANESTHESIATYPE |
| Care Plans | 23 | 128 | CAREPLAN, CAREPLANACTIVITY, ENCOUNTER_CARE_PLAN |
| Scheduling | 19 | 196 | SCHEDULE, SCHEDULEACTOR, SLOT |
| Medical Devices | 16 | 187 | DEVICE, DEVICEUDICARRIER, IMPLANTABLEDEVICEINTRAOPERATIVE |
| Laboratory/Specimens | 16 | 77 | SPECIMEN, SPECIMENDEFINITION, SPECIMENCONTAINER |
| Insurance/Coverage | 13 | 172 | ENCOUNTERINSURANCE (54), COVERAGE, ENCOUNTER_PAYERS |
| Immunizations | 13 | 77 | IMMUNIZATION, IMMUNIZATIONEDUCATION, IMMUNIZATIONREACTION |
| Imaging | 12 | 69 | IMAGINGSTUDY, IMAGINGSTUDYSERIES, IMAGINGSTUDYSERIESINSTANCE |
| Behavioral Health | 11 | 94 | GROUPSESSION, LEGALSTATUS, CHARTRESTRICTION, SENSITIVEPATIENTVIEWEDBY |
| Allergies | 7 | 99 | ALLERGY (51 fields), ALLERGYREACTION, ALLERGYMANIFESTATIONCODING |
| Media/Attachments | 7 | 62 | MEDIA, MEDIACODE, FILESTORAGE |
| Care Team | 3 | 23 | CARETEAM, CARETEAMPARTICIPANT, CARETEAMORGANIZATION |
| Tasks | 3 | 25 | CLINICALTASK, CLINICALTASKDOCUMENTATION |
| Provenance | 2 | 24 | PROVENANCE, PROVENANCEAGENT |
| Referrals | 1 | 2 | REFERRAL |
| Other | 5 | 57 | BILLHOLDREASON, HEALTHCONCERNREVIEW |

**Notable billing depth**: The three largest tables in the entire export are billing tables — RCMUB04CLAIM (260 fields mapping every box on the UB-04 institutional claim form), RCM1500CLAIM (116 fields for the CMS-1500 professional claim form), and BILLINGITEM (115 fields for chargeable transactions). This is genuine revenue cycle data, not summary billing.

**Notable pharmacy depth**: The AU_ prefix tables (60 tables, 986 fields) derive from DSS's VistA pharmacy heritage. AU_PRESCRIPTION alone has 113 fields covering prescriptions, copay activity logs, CMOP events, drug allergy ingredients, refills, reject info, lot/expiration tracking, and medication routes.

**Lookup tables**: 546 tables (41% of total) are lookup/reference tables (prefixed "LK"). These provide coded value sets for clinical statuses, allergy types, medication routes, encounter classes, etc. Their inclusion means the CSV export is self-contained — the coded values used in clinical tables can be resolved against these lookup tables without external documentation.

The full inventory of all 1,322 entities and 10,235 fields is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a native database dump covering the full breadth of the EHR's data model. The richest areas:

1. **Pharmacy/Medications** (155 tables, 1,847 fields combined across Medications + Pharmacy/Prescription categories, plus RxTracker's 66 tables): Extremely deep, reflecting DSS's VA pharmacy heritage. Covers outpatient Rx, inpatient unit dose, IV, pending orders, refills, copay activity, CMOP, reject info, medication administration, reconciliation.

2. **Billing/Financial + Insurance** (54 tables, 1,017 fields): Genuinely comprehensive revenue cycle data. UB-04 claims (260 fields), CMS-1500 claims (116 fields), billing items (115 fields), accounts, charges, coverage, payers, encounter insurance, sliding scale determinations, medical coding worksheets.

3. **Encounters** (56 tables, 514 fields): Full admission/discharge/transfer workflows, episode of care, encounter locations, encounter diagnoses, encounter insurance, bed status, accommodations.

4. **Questionnaires/Forms** (57 tables, 550 fields): The Item/Questionnaire/QuestionnaireResponse tables support the product's 400+ configurable templates and behavioral health assessments.

5. **Patient Demographics** (60 tables, 509 fields): Comprehensive — patient, related persons, contacts, identifiers, addresses, races, ethnicities, medical record numbers, merged records, SSN, smoking status.

The thinnest clinical areas are Referrals (1 table, 2 fields) and Behavioral Health-specific tables (11 tables, 94 fields), though behavioral health data is also captured through the questionnaire/form tables, care plan tables, and group session tables.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | PATIENT (50 fields), RELATEDPERSON, ADDRESS, CONTACTPOINT, MEDICALRECORDNUMBER, PERSONS, PERSONS_SSN, RACES, ETHNICITIES — 60 tables, 509 fields | Thorough; multiple identity and contact tables |
| Encounters / visits | ✅ Covered | ENCOUNTER (59 fields), EPISODEOFCARE, BEDSTATUS, ACCOMMODATION, ENCOUNTERS, ENCOUNTERS_LOCATIONS — 56 tables, 514 fields | Comprehensive; includes ADT, bed management, episode of care |
| Problems / conditions | ✅ Covered | CONDITION, PROBLEM, DIAGNOSES, DETECTEDISSUE, HEALTHCONCERNREVIEW — 41 tables, 275 fields | Thorough; includes conditions, problems, detected issues, health concerns |
| Medications / prescriptions | ✅ Covered | 155 tables, 1,847 fields across Medications + Pharmacy/Prescription; AU_PRESCRIPTION (113 fields), MEDICATIONREQUEST, MEDICATIONADMINISTRATION, OUTPATIENT_MEDICATIONS (100), INPATIENT_MEDICATIONS (80) | Exceptionally deep; strongest area of the export |
| Allergies | ✅ Covered | ALLERGY (51 fields), ALLERGYREACTION, ALLERGYMANIFESTATIONCODING, PERSONS_ALLERGIES, RECONCILIATIONS_ALLERGIES — 7 tables, 99 fields | Solid coverage with reactions, manifestations, coded allergens |
| Immunizations | ✅ Covered | IMMUNIZATION, IMMUNIZATIONEDUCATION, IMMUNIZATIONPROTOCOLAPPLIED, IMMUNIZATIONREACTION — 13 tables, 77 fields | Good; includes education, protocols, and reactions |
| Vitals | ✅ Covered | OBSERVATION, DRAFTOBSERVATION, PERSONS_VITAL_STATISTICS (42 fields), REFERENCERANGE — 32 tables, 248 fields | Thorough |
| Lab results | ✅ Covered | DIAGNOSTICREPORT (18 fields) + 11 sub-tables, SPECIMEN + sub-tables, OBSERVATION — 28 tables combined | Good; diagnostic reports and specimens well-modeled |
| Imaging / diagnostic reports | ✅ Covered | IMAGINGSTUDY and 11 sub-tables (series, instances, performers, endpoints, specimens) — 12 tables, 69 fields | Modeled as DICOM-aligned imaging studies with series/instance detail |
| Procedures | ✅ Covered | PROCEDURE, IMPLANTABLEDEVICEINTRAOPERATIVE (59 fields), ANESTHESIATYPE, surgical case tables — 23 tables, 184 fields | Includes perioperative/surgical detail with implant tracking |
| Clinical notes / documents | ✅ Covered | DOCUMENTREFERENCE, DOCUMENTS, CLINICALNOTESCONFIGURATION, AMENDMENTREQUEST, RELEASEOFINFORMATION — 38 tables, 287 fields | Includes amendment requests and release of information tracking |
| Care plans / goals | ✅ Covered | CAREPLAN (23 tables, 128 fields) + GOAL/INTERVENTION (42 tables, 235 fields) = 65 tables, 363 fields | Deep; intervention tracking, progress, outcomes, performer — supports behavioral health "Golden Thread" |
| Orders / referrals | ✅ Covered | SERVICEREQUEST, MEDICATION_ORDERS (110 fields), ORDERS (45), PENDINGORDER, REFERRAL — 52 tables, 558 fields | Strong on medication and general orders; referrals table is thin (2 fields) |
| Insurance / coverage | ✅ Covered | ENCOUNTERINSURANCE (54 fields), COVERAGE, ENCOUNTER_PAYERS — 13 tables, 172 fields | Solid encounter-level insurance mapping |
| Claims / billing | ✅ Covered | RCMUB04CLAIM (260 fields), RCM1500CLAIM (116), BILLINGITEM (115), MEDICALCODING, accounts — 41 tables, 845 fields | Exceptionally deep; full UB-04 and CMS-1500 claim forms |
| Payments | ⚠️ Partial | No dedicated payment tables visible; BILLINGITEM includes payment-related fields; SLIDINGSCALEDETERMINATION for fee schedules | May be embedded in billing tables; no standalone payment/ERA tables |
| Consents / directives | ✅ Covered | CONSENT tables, RELEASEOFINFORMATION (7 tables) — consents and ROI tracked | Moderate coverage |
| Patient communications | ⚠️ Partial | CLINICALTASK, NURSEBRAINCLINICALCOMMUNICATION, DIAGNOSTICREPORTCLINICALCOMMUNICATION | No explicit portal messaging or secure messaging tables; communications appear to be clinical handoff-focused |
| Specialty: Behavioral health | ✅ Covered | GROUPSESSION (+ participant, recurrence), LEGALSTATUS, CHARTRESTRICTION, 400+ templates via QUESTIONNAIRE/ITEM system, treatment plans via GOAL/INTERVENTION | Well-modeled; group sessions, legal status, and extensive form/assessment infrastructure |
| Specialty: Emergency | ⚠️ Partial | No dedicated ED tables; JESS module is separately certified but no JESS-specific tables in this dictionary | ED data likely captured in encounters/orders/notes; JESS module may have separate data store |
| Medical devices | ✅ Covered | DEVICE (16 tables, 187 fields), IMPLANTABLEDEVICEINTRAOPERATIVE (59 fields), UDI carrier tracking | Thorough; includes UDI tracking and intraoperative implant records |
| Family history | ❌ Not covered | No FAMILYMEMBERHISTORY or family history tables found | Product is certified for (a)(12) family health history; this is a gap |
| Media / attachments | ✅ Covered | MEDIA (7 tables, 62 fields), FILESTORAGE; non-tabular files exported alongside CSVs | Good; media records plus actual file export |

**Key gaps:**
- **Family health history**: No dedicated tables despite (a)(12) certification. May be captured in observation or questionnaire tables but no explicit entity.
- **Patient portal messaging**: No portal message or secure messaging tables visible. Portal data is covered by a separate C-CDA export, but portal-specific interactions (messages, requests) may not be in the CSV export.
- **Payments/ERA**: While billing/claims are deeply modeled, standalone payment posting and ERA processing tables are not clearly identified.
- **Emergency department**: JESS module tables are not present in the JEHR data dictionary; the separately certified JESS module may maintain its own data store.

## 6. Documentation Quality

**Strengths:**
- Every field (10,235 of 10,235) has a text description — ranging from brief ("Unique identifier") to detailed multi-sentence explanations
- Data types are specified for every field using SQL Server types (INT, NVARCHAR, DATETIME, BIT, DECIMAL, FLOAT, UNIQUEIDENTIFIER, DATETIMEOFFSET, etc.)
- Foreign key relationships are documented with hyperlinked cross-references to referenced tables (826 tables have FK documentation)
- Table-level descriptions are present for 98.9% of tables, explaining what each table stores
- The data dictionary is hosted on a dedicated subdomain (`ehiexports.junohealth.com`) with consistent HTML structure across all 1,322 pages
- The 546 lookup tables make the export self-describing — coded values can be resolved without external documentation

**Weaknesses:**
- No sample export files or worked examples are provided
- No machine-readable schema (JSON Schema, SQL DDL, etc.) — the data dictionary is HTML only
- Nullable/required constraints are not documented
- Maximum string lengths are not specified (fields are typed as NVARCHAR without length)
- Value set contents for lookup tables are not enumerated inline — recipients must rely on the lookup table CSV files themselves
- No explicit cardinality documentation (one-to-many, many-to-many relationships)
- Primary keys are documented for only 126 of 1,322 tables (9.5%), though IEN/ID columns are identifiable by naming convention
- No versioning or changelog — the dictionary was last modified 2026-01-23

**Developer usability**: A developer could build an import system from this documentation. The field names, types, descriptions, and foreign key relationships provide sufficient semantic context to understand the data model. The main challenge would be reconstructing relationships for the ~500 tables without explicit FK documentation, and resolving coded values against the lookup tables.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This is one of the most thorough EHI export data dictionaries observed. With 1,322 tables and 10,235 fields, the export covers the full breadth of what Juno EHR stores: clinical records, medications/pharmacy (exceptionally deep), billing/claims (full UB-04 and CMS-1500 forms), insurance, procedures/surgery, behavioral health, questionnaires/forms, imaging, devices, care plans, goals/interventions, and documents. The coverage goes far beyond USCDI — the 41 billing tables with 845 fields alone demonstrate genuine engagement with the designated record set. The 546 lookup tables ensure the export is self-describing. Minor gaps (family history, portal messaging, ED-specific tables) are small relative to the overall breadth.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built native database dump, not a repackaged clinical exchange export. The evidence is unambiguous:
1. The export format is CSV reflecting native database structures — not C-CDA or FHIR
2. The 1,256-table JEHR data dictionary covers the product's internal data model including billing, pharmacy, scheduling, and administrative tables that would never appear in a clinical exchange export
3. The vendor explicitly distinguishes between this CSV export (the primary EHI mechanism) and the ConnectEHR/Patient Portal C-CDA exports, which are transparently labeled as certified under the "limited ePHI USCDIv1 definition"
4. The AU_ prefix tables reveal VistA-heritage pharmacy structures — these are raw database entities, not FHIR or C-CDA mappings
5. Non-tabular data (images, PDFs, XML, text) is exported alongside CSVs
6. The dedicated `ehiexports.junohealth.com` subdomain and 1,322 individual documentation pages represent significant investment in documentation

### Key Findings

1. **Exceptionally deep billing coverage**: The three largest tables in the entire export are billing tables (RCMUB04CLAIM at 260 fields, RCM1500CLAIM at 116, BILLINGITEM at 115). This is genuine revenue cycle data mapping every field on institutional and professional claim forms — a strong signal of authentic (b)(10) engagement.

2. **100% field-level documentation**: All 10,235 fields across all 1,322 tables have text descriptions, and all have data types documented. This is rare among EHI export documentation.

3. **Self-describing export via lookup tables**: 546 lookup/reference tables (41% of total) provide coded value resolution. The export doesn't require an external codebook to interpret coded fields.

4. **Transparent labeling of USCDI-scoped exports**: The vendor explicitly states that ConnectEHR and Patient Portal exports are certified under the "limited ePHI USCDIv1 definition," distinguishing them from the comprehensive CSV export.

5. **VistA heritage visible in data model**: The AU_ prefix tables (pharmacy) show direct lineage from VistA/CPRS, while newer tables (CAREPLAN, ENCOUNTER, OBSERVATION) use a modern FHIR-aligned naming convention, revealing a hybrid architecture.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (native database tables) + non-tabular files
Entities:        1,322 (1,256 JEHR + 66 RTVX)
Fields:          10,235
Descriptions:    100% of fields
Sample data:     No
Bulk export:     Yes (single or multi-patient)
Domains covered: 18 of 20 applicable domains (family history and portal messaging gaps)
```

### Bottom Line

Juno Health's EHI export is one of the strongest (b)(10) implementations reviewed. The native database dump of 1,322 tables with 10,235 fully-described fields covers clinical, billing, pharmacy, behavioral health, and administrative data — far exceeding USCDI scope. The biggest weakness is the lack of sample data files; the biggest strength is the genuine depth of billing and pharmacy data (the three largest entities are UB-04 claims, CMS-1500 claims, and billing line items), demonstrating that this is a real designated record set export, not a clinical summary repackaged.
