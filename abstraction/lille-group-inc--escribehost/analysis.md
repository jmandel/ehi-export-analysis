# EHI Export Analysis: Lille Group, Inc.

**Product**: escribeHOST  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.3058.LILG.01.01.1.220214 (CHPL #10830)

## 1. Product Context

escribeHOST is a cloud-based, ONC-certified EHR built by Lille Group, Inc. (Albany, NY; 11–50 employees) for **cardiology practices**, with a particular focus on electrophysiology and cardiac device management. The product serves a very small market — Capital Cardiology Associates in Albany, NY is the most prominently referenced customer.

The product covers:
- **Clinical documentation**: office visits, cardiac procedure notes, diagnostic test summaries
- **Medications & e-prescribing**: full Surescripts integration, prior authorizations, drug-drug/drug-allergy checking
- **Lab results**: LOINC-coded results, panels, reports
- **Vitals**: provider-recorded and patient-reported
- **Imaging**: diagnostic imaging reports
- **Cardiac device management**: remote monitoring transmissions, device recall tracking, alerts
- **Patient portal**: secure messaging, document access, education materials
- **Scheduling & appointments**: provider templates, reminders, appointment management
- **Orders & referrals**: clinical orders with CPT, SNOMED, ICD-10, LOINC coding
- **Surveys/custom forms**: patient intake forms, assessments
- **Research study tracking**: study enrollment, sites, descriptions
- **Insurance & eligibility**: patient insurance plans, eligibility verification, coverage

**Billing**: The vendor website says escribeHOST integrates with "various billing" systems, but it is unclear whether the product has a built-in billing/claims module or relies on external billing systems. The cardiac device module tracks "Billing Status," and CPT codes are stored in several tables, but no dedicated billing/claims/charge tables exist in the export.

## 2. Artifacts Reviewed

| Artifact | Description | Usefulness |
|---|---|---|
| `downloads/ehi-export-doc.html` (478 KB) | Single-page HTML data dictionary documenting 80 database tables with 1,246 columns for CSV export format. Version 7.85, dated 02/09/2026. | **Primary artifact** — comprehensive, well-structured data dictionary |
| `downloads/enrichment/ehi-tables.json` (399 KB) | Prior agent's structured JSON extraction of the data dictionary | Reference only — I built my own parser from raw HTML |
| `downloads/enrichment/extract-tables.ts` (7 KB) | Prior agent's Bun TypeScript parsing script | Informed my parsing approach |
| `downloads/enrichment/ehi-tables-summary.json` (23 KB) | Prior agent's table-level summary | Cross-referenced for validation |
| `downloads/enrichment/extraction-report.json` | Parsing coverage report: 80 tables, 1,246 columns, 0 failures | Confirmed my own parse matches |

The HTML data dictionary is the sole artifact and is highly informative — it is a complete, well-structured data dictionary with field names, types, descriptions, constraints, and primary keys for every table in the export.

## 3. Export Mechanics

- **Format**: CSV files mirroring internal database tables, plus binary files (PDFs, images)
- **Structure**: The documentation states: "The escribeHOST EHI Table Exports comprise electronic health information (EHI) from a patient's Electronic Health Record (EHR) in a machine-readable, comma-separated value (CSV) file format specific to escribeHOST, reflecting the internal tables structure."
- **Binary files included**: Encounter PDFs, Scanned Cards, PHR Sent Messages, PHR Received Messages, PHR Documents, CCDS Imported Documents, Patient Photos
- **Mechanism**: Not explicitly stated in the documentation. The URL path (`/ehr/api/ehi-export/doc`) suggests an API-driven export, but no API documentation, access instructions, or UI screenshots are provided.
- **Single-patient vs bulk**: Not explicitly stated, but the documentation describes "a patient's Electronic Health Record" (singular) and the table structures reference PATIENT_ID foreign keys throughout, suggesting a per-patient export.
- **Access constraints or fees**: Not documented.

## 4. Export Content: What's In It

### Data Dictionary Overview

The data dictionary documents **80 tables** with **1,246 total fields**:
- **1,139 fields (91.4%)** have text descriptions
- **1,246 fields (100%)** have data types (Oracle types: VARCHAR2, NUMBER, DATE, TIMESTAMP(6), CLOB)
- **611 fields (49.0%)** have CHECK or NOT NULL constraints documented
- **116 primary keys** across all tables
- Foreign key relationships are implicit through `_ID` column naming conventions (not formally declared)
- No value sets or coded value enumerations are provided (CHECK constraints document some allowed values)

### Vendor's own content organization

The vendor does not explicitly organize tables into categories, but the table naming conventions create natural groupings. The following table shows all 80 entities organized by functional domain:

| Entity | Fields | Described | Types | Category |
|---|---|---|---|---|
| PATIENTS | 112 | 100 | yes | Patient Demographics & History |
| PATIENT_ADDRESSES | 13 | 13 | yes | Patient Demographics & History |
| PATIENT_ETHNICITY | 4 | 4 | yes | Patient Demographics & History |
| PATIENT_RACE | 4 | 4 | yes | Patient Demographics & History |
| PATIENT_PREVIOUS_NAMES | 11 | 11 | yes | Patient Demographics & History |
| PATIENT_RELATIVES | 16 | 16 | yes | Patient Demographics & History |
| PATIENT_RELATIVE_DISEASES | 4 | 4 | yes | Patient Demographics & History |
| PATIENT_PHARMACIES | 4 | 4 | yes | Patient Demographics & History |
| PATIENT_TRANSFERS | 5 | 5 | yes | Patient Demographics & History |
| PATIENT_EDUCATION_RECIPIENTS | 2 | 2 | yes | Patient Demographics & History |
| PATIENT_EDUCATION_RESOURCES | 16 | 16 | yes | Patient Demographics & History |
| PATIENT_EDUCATION_TRACKING | 3 | 3 | yes | Patient Demographics & History |
| PATIENT_PROCEDURES | 17 | 12 | yes | Patient Demographics & History |
| PATIENT_IMMUNIZATIONS | 18 | 18 | yes | Patient Demographics & History |
| PATIENT_PROGRAM_ENROLLMENTS | 3 | 3 | yes | Patient Demographics & History |
| PATIENT_PROGRAM_SPECS | 6 | 6 | yes | Patient Demographics & History |
| PATIENT_REPORTED_VITALS | 10 | 10 | yes | Patient Demographics & History |
| PE_PATIENT_ENCOUNTER | 56 | 51 | yes | Encounters |
| PROBLEMS | 18 | 15 | yes | Problems / Diagnoses |
| PROBLEMS_DOCUMENTED | 7 | 7 | yes | Problems / Diagnoses |
| MEDS | 17 | 17 | yes | Medications & Allergies |
| MEDS_DOCUMENTED | 7 | 7 | yes | Medications & Allergies |
| MEDS_NOT_DOCUMENTED | 8 | 8 | yes | Medications & Allergies |
| MEDS_NOT_ORDERED | 17 | 8 | yes | Medications & Allergies |
| MEDS_NO_KNOWN | 1 | 1 | yes | Medications & Allergies |
| MED_CONCERNS | 22 | 21 | yes | Medications & Allergies |
| MED_CONCERNS_DOCUMENTED | 7 | 7 | yes | Medications & Allergies |
| MED_CONCERNS_NKA_STATUS | 5 | 5 | yes | Medications & Allergies |
| MED_RXS | 38 | 33 | yes | Medications & Allergies |
| MED_THERAPIES | 33 | 29 | yes | Medications & Allergies |
| DRUG_HISTORY_REQUESTS | 4 | 4 | yes | Medications & Allergies |
| DRUG_HISTORY_REQUEST_MESSAGES | 4 | 4 | yes | Medications & Allergies |
| RXHUB_DRUG_HISTORY | 89 | 89 | yes | Medications & Allergies |
| RXHUB_DRUG_HISTORY_EVAL | 8 | 8 | yes | Medications & Allergies |
| LABORATORY_TESTS | 5 | 5 | yes | Laboratory |
| LAB_ORGANIZATION | 18 | 18 | yes | Laboratory |
| LAB_PANELS | 39 | 34 | yes | Laboratory |
| LAB_REPORTS | 17 | 17 | yes | Laboratory |
| LAB_REPORT_LOCATIONS | 17 | 17 | yes | Laboratory |
| LAB_TEST_RESULTS | 32 | 32 | yes | Laboratory |
| VITALS | 56 | 50 | yes | Vitals |
| ORDERS | 44 | 37 | yes | Orders |
| ORDERS_ACTIONS | 8 | 8 | yes | Orders |
| INTERVENTIONS | 14 | 12 | yes | Interventions / Procedures |
| INTERVENTIONS_NOT_DONE | 12 | 9 | yes | Interventions / Procedures |
| PATIENT_INSURANCE | 12 | 10 | yes | Insurance & Eligibility |
| PATIENT_ELIGIBILITY_COVERAGE | 6 | 6 | yes | Insurance & Eligibility |
| PATIENT_ELIGIBILITY_INFO | 28 | 27 | yes | Insurance & Eligibility |
| DIAGNOSTIC_IMAGING_REPORTS | 6 | 6 | yes | Imaging |
| MISC_DEVICES | 22 | 22 | yes | Medical Devices |
| SOCIAL_HISTORY_ENTRIES | 14 | 14 | yes | Social History |
| SCANNED_CARDS | 8 | 8 | yes | Scanned Documents |
| AMENDMENT_REQUESTS | 8 | 8 | yes | Amendment Requests |
| RECONCILIATION_HISTORY | 7 | 7 | yes | Reconciliation |
| ETHNICITIES | 5 | 5 | yes | Reference Data |
| PHR_ACTIVITY_LOG | 8 | 8 | yes | Patient Portal / Communications |
| PHR_DOCUMENTS | 10 | 10 | yes | Patient Portal / Communications |
| PHR_PATIENT_COMMUNICATIONS | 7 | 7 | yes | Patient Portal / Communications |
| PHR_RECEIVED_MESSAGES | 11 | 9 | yes | Patient Portal / Communications |
| PHR_SENT_MESSAGES | 10 | 9 | yes | Patient Portal / Communications |
| SURVEYS | 9 | 7 | yes | Surveys / Custom Forms |
| SURVEY_FIELD_VALUES | 8 | 4 | yes | Surveys / Custom Forms |
| SURVEY_FORM_TYPES | 11 | 5 | yes | Surveys / Custom Forms |
| SURVEY_FORM_TYPE_BLOCKS | 4 | 0 | yes | Surveys / Custom Forms |
| SURVEY_FORM_TYPE_FIELDS | 9 | 7 | yes | Surveys / Custom Forms |
| SURVEY_FORM_TYPE_TEXT_BLOCKS | 3 | 0 | yes | Surveys / Custom Forms |
| CCDS_IMPORTED_DOCUMENTS | 10 | 10 | yes | Documents & Transitions of Care |
| DOCUMENT_SNAPSHOTS | 5 | 5 | yes | Documents & Transitions of Care |
| TOC_REQUESTS | 11 | 11 | yes | Documents & Transitions of Care |
| TRANSITION_OF_CARE_HISTORY_LOG | 8 | 8 | yes | Documents & Transitions of Care |
| RS_RESEARCH_STUDY_DESC | 6 | 6 | yes | Research Studies |
| RS_STUDY_MEMBER | 13 | 9 | yes | Research Studies |
| RS_STUDY_SITE | 4 | 4 | yes | Research Studies |
| HEALTH_CARE_TEAM_OTH_CONTACTS | 4 | 4 | yes | Care Team & Contacts |
| HEALTH_CARE_TEAM_PROVIDERS | 7 | 7 | yes | Care Team & Contacts |
| OTHER_CONTACTS | 15 | 15 | yes | Care Team & Contacts |
| PC_PATIENT_CONTACTS | 12 | 12 | yes | Care Team & Contacts |
| PROVIDERS | 44 | 41 | yes | Providers & System |
| USERS | 33 | 29 | yes | Providers & System |
| LOCATIONS | 17 | 15 | yes | Providers & System |

### Category Summary

| Category | Tables | Fields | Notes |
|---|---|---|---|
| Patient Demographics & History | 17 | 248 | PATIENTS alone has 112 fields; includes family history, procedures, immunizations, education |
| Medications & Allergies | 14 | 260 | Deep coverage: prescriptions (38 fields), therapies (33), drug history from PDMP (89), allergy concerns (22) |
| Laboratory | 6 | 128 | Full lab workflow: tests, panels, reports, results (32 fields), organizations, locations |
| Providers & System | 3 | 94 | Provider details (44 fields), users (33), locations (17) |
| Encounters | 1 | 56 | Single large table with encounter types, coding, signing workflow, dates |
| Vitals | 1 | 56 | Extensive vital signs: BP, HR, weight, height, BMI, SpO2, temp, plus cardiology-specific fields |
| Orders | 2 | 52 | Orders (44 fields) with CPT/SNOMED/ICD-10 coding, plus actions |
| Insurance & Eligibility | 3 | 46 | Insurance plans, eligibility verification, coverage details |
| Patient Portal / Communications | 5 | 46 | Sent/received messages, documents, activity log, communications |
| Surveys / Custom Forms | 6 | 44 | Form definitions, field definitions, and patient responses |
| Care Team & Contacts | 4 | 38 | Healthcare team members, other contacts, patient contacts |
| Documents & Transitions of Care | 4 | 34 | Imported CCDs, document snapshots, ToC requests and history |
| Interventions / Procedures | 2 | 26 | Procedures done and not done, with negation rationale |
| Problems / Diagnoses | 2 | 25 | Problem list with ICD-10/SNOMED coding, documentation status |
| Research Studies | 3 | 23 | Study descriptions, enrollment, sites |
| Medical Devices | 1 | 22 | Implantable/misc devices with UDI tracking |
| Social History | 1 | 14 | Social history entries |
| Scanned Documents | 1 | 8 | Scanned card images |
| Amendment Requests | 1 | 8 | Record amendment tracking |
| Reconciliation | 1 | 7 | Medication reconciliation history |
| Imaging | 1 | 6 | Diagnostic imaging reports |
| Reference Data | 1 | 5 | Ethnicity dictionary |

The full inventory is available in `analysis/entity-inventory-full.json` (80 entities, 1,246 fields).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a **native database dump** in CSV format, reflecting the internal table structure of escribeHOST. This is a genuinely deep export:

**Strongest areas:**
- **Medications** (14 tables, 260 fields): Exceptionally thorough — covers active meds, documented/not-documented status, prescriptions (MED_RXS with 38 fields), therapies (33 fields), allergy concerns (MED_CONCERNS with 22 fields), NKA status, and a detailed RXHUB_DRUG_HISTORY table (89 fields) capturing PDMP/pharmacy benefit history with extensive detail (drug names, NDC codes, quantities, DAW codes, pharmacy info, prescriber info).
- **Patient demographics** (112 fields in PATIENTS alone): Covers name, DOB, birth sex, gender identity, sexual orientation, pronouns, race, ethnicity, language, contact info (4 phone types with text capability flags), SSN, functional/cognitive status, advance directives, family health comments, and numerous workflow flags.
- **Laboratory** (6 tables, 128 fields): Full workflow from test ordering through results with detailed LAB_TEST_RESULTS (32 fields including reference ranges, abnormal flags, units) and LAB_PANELS (39 fields).
- **Vitals** (56 fields): Comprehensive including BP (systolic/diastolic/position), HR, weight, height, BMI, SpO2, temperature, respiration rate, plus cardiology-specific measurements.
- **Encounters** (56 fields): Includes type, location, examiner, diagnosis codes (6 chief complaint fields), signing workflow, date of service, and source tracking.

**Notable coverage:**
- **Insurance & eligibility** (3 tables, 46 fields): Goes beyond basic coverage to include detailed eligibility information (28 fields in PATIENT_ELIGIBILITY_INFO) with copay tracking.
- **Patient portal** (5 tables, 46 fields): Captures bidirectional messaging, documents, and activity logs.
- **Surveys/custom forms** (6 tables, 44 fields): Includes form definitions (types, blocks, fields) and patient responses (SURVEY_FIELD_VALUES) — captures custom data collection.
- **Medical devices** (22 fields): UDI-tracking with SNOMED coding, consistent with cardiology focus.
- **Research studies** (3 tables, 23 fields): Unusual inclusion — tracks study enrollment, sites, and descriptions.

**Thinnest areas:**
- **Imaging** (1 table, 6 fields): Only basic report metadata, though encounter PDFs may contain imaging details.
- **Amendment requests** (1 table, 8 fields): Minimal — tracks requests but limited detail.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `PATIENTS` (112 fields), `PATIENT_ADDRESSES` (13), `PATIENT_PREVIOUS_NAMES` (11), `PATIENT_RACE` (4), `PATIENT_ETHNICITY` (4) | Exceptionally thorough — 144 total fields covering demographics, contacts, preferences, advance directives |
| Encounters / visits | ✅ Covered | `PE_PATIENT_ENCOUNTER` (56 fields) | Comprehensive single table with encounter types, coding, signing workflow |
| Problems / conditions | ✅ Covered | `PROBLEMS` (18 fields), `PROBLEMS_DOCUMENTED` (7) | ICD-10 and SNOMED-coded problem list with documentation status |
| Medications / prescriptions | ✅ Covered | 14 tables, 260 fields total | Deep: prescriptions, therapies, documented/not-documented, reconciliation, PDMP history |
| Allergies | ✅ Covered | `MED_CONCERNS` (22), `MED_CONCERNS_DOCUMENTED` (7), `MED_CONCERNS_NKA_STATUS` (5) | Thorough allergy tracking with NKA status |
| Immunizations | ✅ Covered | `PATIENT_IMMUNIZATIONS` (18 fields) | Full immunization records with administration details |
| Vitals | ✅ Covered | `VITALS` (56 fields), `PATIENT_REPORTED_VITALS` (10) | Deep — 66 total fields including patient-reported vitals |
| Lab results | ✅ Covered | 6 tables, 128 fields | Complete workflow: ordering, panels, results, reference ranges |
| Imaging / diagnostic reports | ⚠️ Partial | `DIAGNOSTIC_IMAGING_REPORTS` (6 fields) | Basic metadata only; encounter PDFs may supplement |
| Procedures | ✅ Covered | `PATIENT_PROCEDURES` (17), `INTERVENTIONS` (14), `INTERVENTIONS_NOT_DONE` (12) | Includes CPT/SNOMED coding and negation rationale |
| Clinical notes / documents | ✅ Covered | `DOCUMENT_SNAPSHOTS` (5), `PE_PATIENT_ENCOUNTER` (56), binary PDFs included | Encounter PDFs explicitly listed as part of export package |
| Care plans / goals | ⚠️ Partial | `PATIENT_PROGRAM_ENROLLMENTS` (3), `PATIENT_PROGRAM_SPECS` (6) | Program enrollment tracked but no explicit care plan entity |
| Orders / referrals | ✅ Covered | `ORDERS` (44 fields), `ORDERS_ACTIONS` (8) | Detailed order tracking with CPT/SNOMED/ICD-10/LOINC coding |
| Insurance / coverage | ✅ Covered | `PATIENT_INSURANCE` (12), `PATIENT_ELIGIBILITY_INFO` (28), `PATIENT_ELIGIBILITY_COVERAGE` (6) | Thorough — 46 total fields including eligibility verification |
| Claims / billing | ❌ Not covered | No billing/claims/charge tables | CPT codes appear in procedures and orders, but no dedicated billing tables. Product may rely on external billing system — unclear if this is a gap or N/A. |
| Payments | ❌ Not covered | No payment or financial transaction tables | Same as above — likely N/A if billing is external |
| Consents / directives | ⚠️ Partial | Flags in `PATIENTS` (DRUG_HISTORY_CONSENT, TEXT_MESSAGE_CONSENT, ADVANCED_DIRECTIVE, LIVING_WILL, DNR, POWER_OF_ATTORNEY) | Consent tracked as boolean flags on patient record; no dedicated consent documents |
| Patient communications | ✅ Covered | `PHR_SENT_MESSAGES` (10), `PHR_RECEIVED_MESSAGES` (11), `PHR_PATIENT_COMMUNICATIONS` (7), `PHR_DOCUMENTS` (10) | Full bidirectional portal messaging |
| Social history | ✅ Covered | `SOCIAL_HISTORY_ENTRIES` (14 fields) | Dedicated table with social history tracking |
| Family health history | ✅ Covered | `PATIENT_RELATIVES` (16), `PATIENT_RELATIVE_DISEASES` (4) | Structured family member tracking with disease associations |
| Medical devices | ✅ Covered | `MISC_DEVICES` (22 fields) | UDI tracking with SNOMED coding — appropriate for cardiology focus |
| Care team | ✅ Covered | `HEALTH_CARE_TEAM_PROVIDERS` (7), `HEALTH_CARE_TEAM_OTH_CONTACTS` (4) | Provider and non-provider team members |
| Patient education | ✅ Covered | `PATIENT_EDUCATION_RESOURCES` (16), `PATIENT_EDUCATION_RECIPIENTS` (2), `PATIENT_EDUCATION_TRACKING` (3) | Education materials and delivery tracking |
| Custom forms / surveys | ✅ Covered | 6 survey tables (44 fields total) | Form definitions and patient responses — captures specialty assessments |
| Specialty (cardiology) | ⚠️ Partial | `MISC_DEVICES` has cardiac device fields (HAS_SORIN_DEVICE flag in PATIENTS); cardiac-specific vital signs in VITALS | Device data present but no dedicated cardiac monitoring/transmission tables despite product having cardiac device management module |

## 6. Documentation Quality

**Strengths:**
- **Comprehensive data dictionary**: 80 tables, 1,246 fields, all with data types, 91.4% with text descriptions
- **Well-structured HTML**: Clean, parseable format with consistent layout (column name, type, description, constraints per field)
- **Complete constraint documentation**: CHECK constraints provide value set hints (e.g., allowed values for coded fields); NOT NULL constraints documented
- **Primary key identification**: All PKs explicitly marked
- **Current**: Dated 02/09/2026, version 7.85 — demonstrably maintained
- **Binary file list**: Export explicitly documents inclusion of PDFs, images, scanned cards, and portal messages beyond the CSV data

**Weaknesses:**
- **107 fields (8.6%) lack descriptions**: Concentrated in newer/less common fields at the end of tables (e.g., BIRTH_TIME, PRONOUNS, VIRTUAL, HOSPITAL in recent table additions)
- **No sample data**: No example CSV files or sample export packages provided
- **No formal foreign key documentation**: Relationships must be inferred from `_ID` naming conventions
- **No explicit value sets**: While CHECK constraints hint at allowed values for some fields, there are no formal code system references or enumerated value lists
- **No export access instructions**: The documentation describes what's in the export but not how to obtain it (UI steps, API calls, turnaround time, fees)
- **No ERD or relationship diagram**: Table relationships must be inferred from column names

**Could a developer build an import?** Mostly yes. The field names, types, and descriptions are sufficient to understand the data model for most tables. The lack of formal foreign key documentation and value sets would require some reverse engineering, but the naming conventions are consistent and intuitive.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export covers the breadth of what escribeHOST stores as a cardiology-focused EHR. With 80 tables and 1,246 fields spanning demographics, encounters, medications (14 tables), labs (6 tables), vitals, orders, procedures, problems, immunizations, insurance/eligibility, patient portal messaging, surveys/custom forms, medical devices, social history, family history, care team, documents, and research studies — this is not a clinical summary repackaged. The export goes well beyond USCDI: it includes insurance/eligibility (46 fields), patient portal messaging (46 fields), custom survey forms and responses (44 fields), research study tracking (23 fields), patient education tracking (21 fields), and medication reconciliation history.

The only notable domain question is **billing**: the product may not have a built-in billing module (it integrates with external billing systems per the vendor website), making the absence of billing/claims tables potentially N/A rather than a gap. CPT codes appear in encounters, procedures, and orders, which is consistent with a product that captures procedure codes for clinical documentation but sends them to an external billing system.

The cardiac device management module (Cardiac Signals) appears to be a separate platform, which may explain why there are no dedicated cardiac monitoring/transmission tables — that data likely lives in a separate system.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. The vendor exports CSV files that mirror the internal Oracle database table structure — this is a native database dump, not a repackaged C-CDA or FHIR Bulk Data export. Key evidence:
1. The documentation URL path (`/ehr/api/ehi-export/doc`) indicates a dedicated EHI export endpoint
2. The documentation explicitly states the CSVs reflect "the internal tables structure"
3. Oracle data types (VARCHAR2, NUMBER, TIMESTAMP(6), CLOB) confirm these are native database columns
4. The export includes binary files (encounter PDFs, scanned cards, patient photos) beyond structured data
5. Tables include internal workflow fields (signing status, modification tracking, version numbers) that would never appear in a clinical exchange export
6. No references to C-CDA, FHIR, USCDI, or US Core anywhere in the documentation

### Key Findings

1. **Genuinely deep native export**: 80 internal database tables with 1,246 fields exported as CSV — this is the vendor's actual database schema, not a clinical exchange projection. The PATIENTS table alone has 112 fields, far exceeding any standard clinical summary.

2. **Outstanding medication coverage**: 14 medication-related tables with 260 fields, including a remarkably detailed RXHUB_DRUG_HISTORY table (89 fields) capturing prescription drug monitoring program data with NDC codes, quantities, DAW codes, pharmacy details, and prescriber information.

3. **Includes non-clinical patient data**: Patient portal messaging (bidirectional), custom survey responses, research study enrollment, patient education tracking, amendment requests, and document snapshots — these go meaningfully beyond USCDI clinical domains.

4. **Well-documented and current**: The data dictionary is dated 02/09/2026 (v7.85), covers 91.4% of fields with descriptions, includes data types and constraints, and is presented in clean, parseable HTML. This is active documentation, not a compliance afterthought.

5. **Minor gaps are understandable**: The absence of billing/claims tables likely reflects product architecture (external billing integration), not an oversight. The thinnest areas (imaging at 6 fields, care plans as program enrollments) reflect the product's cardiology focus rather than incomplete export design.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (native database tables) + binary files (PDFs, images)
Entities:        80
Fields:          1,246
Descriptions:    91.4% (1,139 of 1,246)
Sample data:     No
Bulk export:     Unclear (likely single-patient)
Domains covered: 18 of 20 applicable domains (billing and payments likely N/A)
```

### Bottom Line

escribeHOST's EHI export is one of the stronger (b)(10) implementations: a purpose-built native database dump covering 80 internal tables with 1,246 well-documented fields, plus binary files. A patient or provider would get a comprehensive copy of their clinical, medication, lab, insurance, portal messaging, and specialty device data. The only question mark is billing data, which the product likely delegates to external systems, making its absence reasonable rather than problematic.
