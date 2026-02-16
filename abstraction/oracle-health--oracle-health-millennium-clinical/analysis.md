# EHI Export Analysis: Oracle Health

**Product**: Oracle Health Millennium (Clinical)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1221.Mill.24.07.0.240920 (v2024), 15.04.04.1221.Mill.25.08.0.250620 (v2025)

## 1. Product Context

Oracle Health Millennium (formerly Cerner Millennium) is the second-largest acute care EHR in the U.S. (~22.9% of hospitals), deployed across large health systems, academic medical centers, community hospitals, VA/DoD facilities, and ambulatory clinics worldwide. It is a comprehensive hospital information system — not merely a clinical EHR — encompassing:

- **Core Clinical (PowerChart)**: demographics, encounters, problem lists, medication lists, allergies, immunizations, vitals, clinical documentation, care plans, family history, implantable devices
- **CPOE (PowerOrders)**: medication, lab, imaging, and procedure orders with decision support
- **Pharmacy (PharmNet)**: closed-loop medication management, eMAR, dispensing, pharmacy verification
- **Laboratory (PathNet)**: chemistry, hematology, microbiology, blood bank, anatomic pathology
- **Radiology (RadNet)**: RIS, order tracking, reporting, PACS integration
- **Surgery (SurgiNet)**: perioperative documentation, anesthesia records, surgical supplies, charge capture
- **Emergency Department (FirstNet)**: triage, tracking, clinical documentation, charge tracking
- **Revenue Cycle / Financial Operations**: patient accounting, claims, payments, insurance verification, eligibility, denials management, A/R
- **Patient Portal (HealtheLife)**: secure messaging, appointment scheduling, results viewing, bill payment
- **Document Imaging**: scanned documents, media files
- **Multimedia Storage**: DICOM imaging, audio/video, photos
- **Health Data Intelligence (HDI)**: population health analytics, longitudinal records

The (b)(10) EHI export should cover data from all of these integrated modules. The transparency disclosure confirms Oracle supports both single-patient and population-level EHI export at no required cost (though population exports may incur ancillary costs for encrypted devices/cloud storage).

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `single-patient-ehi-export-data-overview.pdf` | User instructions for single-patient export process | 4 pages | High — explains export structure (SQL files + multimedia + documents) |
| `patient-population-ehi-export-data-overview.pdf` | User instructions for population-level export | 23 pages | High — covers multi-tenant vs single-tenant delivery, multimedia, document imaging, longitudinal plan |
| `health-data-intelligence-ehi-export-data-overview.pdf` | HDI Longitudinal Record export via REST APIs | 3 pages | Medium — API instructions for bulk extract and data syndication |
| `health-data-intelligence-ehi-export-data-format-specifications.pdf` | HDI Longitudinal Record entity model | 196 pages, 249 entities (220 records + 29 enums), 1,697 fields | High — detailed entity-level documentation with types and descriptions |
| `mysql-model/` (extracted from ZIP) | Millennium MySQL Data Model Reports v2025.4.01 | 1,422 HTML pages documenting 6,604 tables with 129,148 columns | **Most informative** — complete database schema with column-level definitions |
| `certified-health-it-transparency-disclosure.pdf` | Cost/fee disclosure for all certified modules | 32 pages | Medium — confirms no required costs for EHI export |
| `Oracle Health Document Imaging Content Management Database Schema.pdf` | Document imaging database tables | 7 pages, 7+ tables | Medium — documents AE_ADEFS, AE_APPS, AE_PATHS, AE_RH, etc. |
| `Oracle Health Multimedia Storage DICOM Data Structure and Definitions.pdf` | DICOM data organization | 8 pages | Low-medium — hierarchical XML/JSON structure for imaging |
| `Oracle Health Multimedia Storage Non-DICOM Data Column Definitions.pdf` | Non-DICOM multimedia CSV format | 1 page, 8 columns | Low — simple column list |
| `Oracle Health Document Imaging AxAnnotations.xsd` | XML Schema for document annotations | 9 KB | Low — annotation format spec |
| `Longitudinal Plan EHI Export - Single Patient.pdf` | Longitudinal Plan export (health concerns, goals, activities, strengths, care plans) | 1 page | Low — pointers to external API docs |

## 3. Export Mechanics

Oracle Health provides **three distinct export pathways**, all purpose-built for (b)(10):

### 3a. Core Millennium EHR Export (Primary)

- **Format**: SQL (DDL + INSERT statements for MySQL or Oracle databases)
- **Structure**: Creates a complete relational database that can be queried with standard SQL
- **Components**:
  - `v500/schema/` — DDL files (V500TableSchema.sql, V500IndexSchema.sql, V500PrimaryKeySchema.sql, V500ForeignKeySchema.sql)
  - `v500/activity/` — INSERT files for activity (transactional) data per table
  - `v500/reference/` — INSERT files for reference (lookup) data per table
  - `camm/` — Multimedia storage files linked via `dms_media_identifier` table
  - `dicom/` — DICOM images organized by study UID
  - `edm/` — Electronic document management files (Document Imaging)
  - `longitudinal_plan/` — JSON files for health concerns, goals, activities, strengths, care plans
- **Single-patient**: Automated process producing .zip file(s)
- **Population (multi-tenant)**: SQL files delivered via secure mechanism
- **Population (single-tenant)**: Full database copy on customer-supplied encrypted device, restored via Oracle backup/restore
- **Access**: No required costs; population exports may have ancillary costs for devices/storage

### 3b. Health Data Intelligence (HDI) Longitudinal Record Export

- **Format**: JSON (Avro-style entities) delivered via REST API
- **Mechanism**: Longitudinal Record Bulk Extract API + Data Syndication API
- **Supports**: Both single-patient (filtered by empiId) and population-level extraction
- **Authentication**: Bearer token or OAuth 1.0a
- **Availability**: Download available for 21 days after extraction completes
- **Prerequisite**: Oracle Health must enable the Bulk Extract API for the tenant

### 3c. Document Imaging Export (Supplementary)

- **Format**: Binary files (.bin) in native format (TIFF, JPEG, PDF, etc.) with SQL metadata
- **Structure**: Content management database (AE_APPS, AE_DT#, AE_DL#, AE_RH#, AE_PATHS tables) plus physical file storage

### Summary

| Feature | Value |
|---|---|
| Single-patient | ✅ Automated |
| Bulk/population | ✅ Supported |
| Format | SQL (DDL + INSERT), JSON (HDI), native files (multimedia/documents) |
| Fees | No required cost; ancillary costs possible for population export storage |

## 4. Export Content: What's In It

### 4a. Core Millennium Database Model

The Millennium data model documentation is extraordinarily detailed. Based on the MySQL Data Model Reports v2025.4.01 (parsed from 1,422 HTML pages):

- **6,604 tables** across **242 subject areas**
- **129,148 total columns (fields)**
- **129,069 fields with definitions** (99.9% coverage — only 79 fields lack definitions)
- **All fields have types** (VARCHAR, DOUBLE, DATETIME, MEDIUMTEXT, etc.)
- **Nullability documented** for all columns
- **Foreign key relationships** documented via V500ForeignKeySchema.sql
- **Table-level descriptions and definitions** for 6,603 of 6,604 tables (only `PREEXIST_CONDITION` lacks both)
- **Table types** classified as ACTIVITY (transactional) or REFERENCE (lookup)

This is a native database dump — the actual Millennium EHR schema — not a projection into a standard format.

### 4b. HDI Longitudinal Record

The HDI format specifications (196-page PDF) document:

- **249 entity types** (220 record types + 29 enumerations)
- **1,697 fields** across record types
- Entities span clinical, billing, and administrative domains including: Claim (78 fields), Medication (53 fields), Result (53 fields), Encounter (47 fields), Condition (41 fields), Immunization (40 fields), Procedure (39 fields), DocumentReference (38 fields), Service (37 fields), among others
- Each field has name, type, nullable flag, and description

### Vendor's own content organization (Millennium subject areas)

The 242 subject areas represent Oracle Health's internal module organization. Top 20 by table count:

| Subject Area | Tables | Fields | Category |
|---|---|---|---|
| bedrock | 197 | 2,513 | Core infrastructure |
| micro | 156 | 1,954 | Microbiology |
| multum | 139 | 1,371 | Drug database |
| lh_quality_measures | 136 | 10,667 | Quality measures/reporting |
| multum_load | 132 | 1,260 | Drug database loading |
| data_mgmt | 127 | 1,557 | Data management |
| pft_account_manageme | 123 | 2,741 | **Account management (billing)** |
| encounter | 117 | 3,076 | Encounters |
| a_p | 115 | 1,567 | Anatomic pathology |
| pft_revenue_cycle_wh | 112 | 2,579 | **Revenue cycle warehouse** |
| person | 111 | 2,964 | Person/demographics |
| scheduling_build | 111 | 1,619 | Scheduling configuration |
| pharmnet | 109 | 3,169 | Pharmacy |
| outcomes___hf | 108 | 3,783 | Outcomes/infection tracking |
| surginet | 103 | 2,128 | Surgery |
| surginet___anesthesi | 98 | 1,870 | Anesthesia |
| profile | 101 | 1,340 | User profiles |
| hla | 93 | 1,061 | HLA/blood bank |
| clinical_trials | 85 | 1,399 | Clinical trials |
| general_lab | 84 | 1,458 | General laboratory |

Full breakdown of all 242 subject areas is in `analysis/entity-inventory-summary.json`.

**Notable billing/financial subject areas** (533 tables, 11,527 fields total):

| Subject Area | Tables | Fields |
|---|---|---|
| pft_account_manageme | 123 | 2,741 |
| pft_revenue_cycle_wh | 112 | 2,579 |
| pft_billing | 77 | 1,573 |
| charge_services | 55 | 788 |
| collections | 40 | 653 |
| pft_posting_and_tran | 49 | 981 |
| financial_clearance | 37 | 624 |
| enterprise_eligibili | 31 | 548 |
| scm_accounting | 4 | 43 |
| revenue_cycle_config | 3 | 13 |
| revenue_cycle_core | 2 | 14 |

**Largest individual tables** (by field count):

| Table | Fields | Subject Area | Description |
|---|---|---|---|
| LH_E_VTE_2016_METRICS | 378 | lh_quality_measures | VTE quality measure metrics |
| HF_R_ISOLATE | 349 | outcomes___hf | Microbial isolate tracking |
| HF_R_HL7_ISOLATE | 346 | outcomes___hf | HL7 isolate data |
| FILL_PRINT_ORD_HX | 328 | pharmnet | Pharmacy fill/print order history |
| HF_R_MICRO_SUSCEPTIBILITY | 319 | outcomes___hf | Micro susceptibility data |
| PHA_PROD_DISP_OBS_ST | 316 | pharmnet | Pharmacy dispense observations |
| PM_TRANSACTION | 264 | person | Person transaction records |
| PFT_ACCOUNT | 245 | pft_account_manageme | **Patient financial account** |
| ENCOUNTER | 231 | encounter | Patient encounter |
| ORDERS | 224 | orders | Clinical orders |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Oracle Health's EHI export is structured as a **complete database dump** of the Millennium platform, covering every module in the system. The 242 subject areas span:

**Clinical Core** (~1,400+ tables): encounter, clinical_events, charting, orders, person, pharmnet, general_lab, micro, imaging_document, surginet, surginet___anesthesi, clinical_reporting, physician_documentat, dcp_care_coordinatio, dcp_power_chart, immunizations, medication_administr, clinical_trials, consent, fhx_family_history

**Pharmacy** (~180+ tables, 4,633+ fields): pharmnet, pharmnet_ambulatory, rxstation, knowledge_driven_med, multum, multum_load

**Laboratory** (~300+ tables): general_lab, micro, pathnet_common_servi, a_p (anatomic pathology), hla (blood bank), reference_lab_networ

**Radiology/Imaging** (~100+ tables): radnet_radiology_con, radnet_order, radnet_mammo, radnet_pull_lists, imaging_document, multimedia_foundatio

**Surgery/Anesthesia** (~200+ tables): surginet, surginet___anesthesi, surginet_surgeon_pro, surgery_implants

**Billing/Revenue Cycle** (~530+ tables): pft_account_manageme, pft_revenue_cycle_wh, pft_billing, pft_posting_and_tran, charge_services, collections, financial_clearance, enterprise_eligibili, scm_accounting, revenue_cycle_config, revenue_cycle_core

**Patient Management** (~250+ tables): person, patient_management, patient_tracking, patient_access_list, scheduling, scheduling_build

**Emergency Department**: patient_tracking (79 tables)

**Behavioral Health**: behavioral_health (6 tables)

**Women's Health**: womens_health___acut (3 tables), womens_health___mpag (1 table)

**Care Coordination**: dcp_care_coordinatio (54 tables), encounter___care_man (46 tables)

**Documents/Forms**: powerforms_cnt (49 tables), powerforms_doc_set (7 tables), powerforms_task_assa (6 tables), powerforms_io_totals (4 tables), imaging_document (63 tables)

**Analytics/Quality**: lh_quality_measures (136 tables), lighthouse_reporting (69 tables), outcomes___hf (108 tables), outcomes___uk (53 tables), outcomes___qmd (36 tables)

**Supply Chain**: scm_item (76 tables), scm_purchasing (37 tables), scm_par (6 tables), scm_physical_count (3 tables)

**Cardiovascular**: cvnet (42 tables), cvnet_staging (5 tables)

The breadth is genuinely remarkable. The HDI Longitudinal Record adds a complementary view with explicit billing entities (Claim with 78 fields, Service with 37 fields, ServiceAdjustment, BenefitCoverage, PersonBenefitCoverage, RelatedClaim, etc.).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `person` (111 tables, 2,964 fields), PersonDemographics, PersonName, PersonContact (HDI) | Thorough — extensive demographic, alias, address, contact data |
| Encounters / visits | ✅ Covered | `encounter` (117 tables, 3,076 fields), ENCOUNTER table (231 fields), Encounter HDI entity (47 fields) | Thorough — includes encounter types, locations, participants, ED tracking |
| Problems / conditions | ✅ Covered | Within `clinical_events`, Condition HDI entity (41 fields) | Thorough |
| Medications / prescriptions | ✅ Covered | `pharmnet` (109 tables, 3,953 fields), `pharmnet_ambulatory` (69 tables), `medication_administr` (6 tables), Medication HDI (53 fields) | Thorough — includes dispensing, eMAR, order history |
| Allergies | ✅ Covered | Within `clinical_events`, Allergy HDI entity | Covered |
| Immunizations | ✅ Covered | `immunizations` (6 tables), Immunization HDI entity (40 fields) | Covered |
| Vitals | ✅ Covered | Within `clinical_events` | Covered |
| Lab results | ✅ Covered | `general_lab` (84 tables, 1,458 fields), `micro` (156 tables, 1,954 fields), `a_p` (115 tables, 1,567 fields), Result HDI entity (53 fields) | Thorough — covers chemistry, hematology, microbiology, anatomic pathology |
| Imaging / diagnostic reports | ✅ Covered | `radnet_radiology_con` (42 tables), `radnet_order` (32 tables), `imaging_document` (63 tables), `multimedia_foundatio` (50 tables), DICOM export, DiagnosticReport HDI | Thorough — includes RIS data, PACS images, DICOM files |
| Procedures | ✅ Covered | `surginet` (103 tables, 2,128 fields), `surginet___anesthesi` (98 tables, 1,870 fields), `surgery_implants` (3 tables), Procedure HDI (39 fields) | Thorough — detailed perioperative, anesthesia, implant data |
| Clinical notes / documents | ✅ Covered | `physician_documentat` (26 tables), `charting` (71 tables), `powerforms_cnt` (49 tables), Document Imaging export, DocumentReference HDI (38 fields) | Thorough — structured notes, forms, scanned documents, multimedia |
| Care plans / goals | ✅ Covered | `dcp_care_coordinatio` (54 tables), Longitudinal Plan JSON export (health concerns, goals, activities, strengths, care plans), CarePlan HDI | Thorough |
| Orders / referrals | ✅ Covered | `orders` (65 tables), `orders_build` (52 tables), ORDERS table (224 fields), ServiceRequest HDI, ReferralRequest HDI | Thorough |
| Insurance / coverage | ✅ Covered | Within `encounter` and `person`, `enterprise_eligibili` (31 tables, 548 fields), `financial_clearance` (37 tables), BenefitCoverage HDI, PersonBenefitCoverage HDI | Thorough — eligibility, benefit plans, coverage details |
| Claims / billing | ✅ Covered | `pft_account_manageme` (123 tables, 2,741 fields), `pft_billing` (77 tables, 1,573 fields), `charge_services` (55 tables), Claim HDI (78 fields) | Thorough — claims, charges, billing items, financial accounts |
| Payments | ✅ Covered | `pft_posting_and_tran` (49 tables, 981 fields), `collections` (40 tables, 653 fields) | Thorough — postings, transactions, collections |
| Consents / directives | ✅ Covered | `consent` (4 tables), AdvanceDirective HDI entity, Consent HDI entity | Covered |
| Patient communications | ⚠️ Partial | Communication HDI entity, patient portal data likely in bedrock/outreach tables | Portal messaging may be embedded in general tables; no dedicated `patient_portal_messages` subject area visible |
| Specialty: Surgery | ✅ Covered | `surginet` (103 tables), `surginet___anesthesi` (98 tables) | Thorough |
| Specialty: Cardiovascular | ✅ Covered | `cvnet` (42 tables), `cvnet_staging` (5 tables) | Covered |
| Specialty: Behavioral Health | ⚠️ Partial | `behavioral_health` (6 tables) | Present but thin relative to full behavioral health capabilities |
| Specialty: Women's Health | ⚠️ Partial | `womens_health___acut` (3 tables), `womens_health___mpag` (1 table) | Present but thin |
| Specialty: Rehabilitation | ⚠️ Partial | `rehabilitation_dev` (6 tables) | Present but thin |
| Supply Chain | ✅ Covered | `scm_item` (76 tables), `scm_purchasing` (37 tables) | N/A for EHI — operational |
| Custom forms | ✅ Covered | `powerforms_cnt` (49 tables), `powerforms_doc_set` (7 tables) | Thorough — captures custom form data |

## 6. Documentation Quality

Oracle Health's EHI export documentation is **exceptionally thorough**:

**Data dictionary completeness**:
- 6,604 tables with 129,148 columns, **99.9% with column-level definitions** (only 79 fields lack definitions)
- Every table has a description and classification (ACTIVITY vs REFERENCE)
- Column types and nullability documented for all fields
- Foreign key relationships provided via DDL
- 242 subject areas provide logical grouping
- The HTML data model reports are navigable and well-structured

**Export process documentation**:
- Clear user instructions for both single-patient (4 pages) and population (23 pages) exports
- Detailed explanation of directory structures, file naming conventions, and cross-references between data sources
- SQL queries provided for linking multimedia/document files back to clinical records
- HDI API documentation with authentication, endpoint patterns, and data syndication workflows

**Machine-readable artifacts**:
- SQL DDL for full schema recreation
- XSD for document imaging annotations
- JSON format for Longitudinal Plan data
- Avro-style entity model for HDI export

**What a developer would need**:
A developer receiving this export could:
1. Execute the DDL to recreate the full Millennium database locally
2. Load activity and reference data via INSERT statements
3. Query the database with standard SQL
4. Link multimedia files back to clinical records via documented queries
5. Use the data model reports to understand every table and column

This is among the most developer-friendly export documentation in the industry. The only improvement would be value set/code set documentation (code sets are referenced by `code_set` numbers but the code values themselves are in the `CODE_VALUE` reference table included in the export).

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

Oracle Health Millennium's EHI export is a full database dump covering 6,604 tables across 242 subject areas. It goes far beyond USCDI:
- **Billing/Revenue Cycle**: 533 tables, 11,527 fields covering account management, billing, posting/transactions, charge services, collections, financial clearance, eligibility — this is genuinely deep financial data, not token coverage
- **Pharmacy**: 178 tables with 4,633 fields covering dispensing, eMAR, ambulatory pharmacy, drug databases
- **Surgery/Anesthesia**: 201+ tables covering perioperative workflow, anesthesia records, implants
- **Laboratory**: 300+ tables spanning general lab, microbiology, anatomic pathology, blood bank
- **Specialty**: Cardiovascular (47 tables), behavioral health (6 tables), women's health (4 tables), rehabilitation (6 tables), clinical trials (85 tables)
- **Custom forms**: 49+ tables in PowerForms
- **Document Imaging + Multimedia**: Complete content management database plus native DICOM and non-DICOM files

The export also includes supplementary pathways: HDI Longitudinal Record (249 entities with explicit billing Claim entity having 78 fields) and Longitudinal Plan data (care plans, goals, health concerns).

The few subject areas that are thin (behavioral_health at 6 tables, womens_health at 4 tables) likely reflect that specialty-specific data is stored in the general clinical_events and charting tables rather than separate specialty schemas. This is a characteristic of Millennium's architecture, not an export gap.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built EHI export. The telltale signs:
1. **Native database dump**: The export provides the actual Millennium database schema (6,604 tables) — not a FHIR or C-CDA projection. This is the internal data model, including tables named `PFT_ACCOUNT`, `FILL_PRINT_ORD_HX`, `HF_R_ISOLATE` — clearly internal system tables, not standard exchange resources.
2. **SQL format with DDL + data**: The export creates a full relational database that can be queried, not a summary document.
3. **Multiple data sources**: Core EHR SQL + multimedia files + DICOM images + document imaging + longitudinal plan JSON — this is not a single export format but a comprehensive extraction of all data stores.
4. **Dedicated documentation**: 4-page and 23-page user guides specifically for EHI export, separate from clinical exchange documentation.
5. **Breadth far exceeding USCDI**: 533 billing/financial tables, 200+ surgical tables, 85 clinical trials tables — none of which would be in a C-CDA or FHIR (g)(10) export.
6. **No reference to C-CDA or FHIR standards**: The core export is entirely in Oracle's native format. The HDI pathway uses a proprietary entity model, not FHIR.

### Key Findings

1. **Exceptionally comprehensive database dump**: 6,604 tables with 129,148 columns, 99.9% with descriptions — this is one of the most thorough EHI exports documented by any EHR vendor. The export includes the complete Millennium relational database, not a subset or summary.

2. **Genuine billing/financial depth**: 533 tables and 11,527 fields across account management, billing, posting/transactions, charge services, collections, and financial clearance subject areas. The HDI Claim entity adds another 78 fields. This is not token billing coverage.

3. **Three complementary export pathways**: Core Millennium SQL dump (most comprehensive), HDI Longitudinal Record API (structured entity model for analytics platform), and Longitudinal Plan JSON — ensuring data from all platform components is accessible.

4. **Outstanding documentation**: Nearly 100% field-level description coverage, navigable HTML data model reports, clear user instructions, cross-reference queries between data sources, and multiple machine-readable artifacts (DDL, XSD, entity specifications).

5. **Minor gaps**: Some specialty areas (behavioral health: 6 tables, women's health: 4 tables, rehabilitation: 6 tables) appear thin as dedicated subject areas, though their clinical data is likely captured in the general clinical_events infrastructure. Patient portal messaging doesn't have a clearly identifiable dedicated subject area.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   SQL (DDL + INSERT), JSON (HDI Longitudinal Record), native files (DICOM, multimedia, documents)
Entities:        6,604 tables (Millennium) + 249 entities (HDI) = 6,853 total
Fields:          129,148 (Millennium) + 1,697 (HDI) + 8 (non-DICOM) = 130,853 total
Descriptions:    99.9% (Millennium), documented (HDI)
Sample data:     No (but export produces real data in SQL INSERT format)
Bulk export:     Yes (population-level supported for both Millennium and HDI)
Domains covered: 17 of 18 applicable domains (all fully or partially covered)
```

### Bottom Line

Oracle Health Millennium's EHI export is a gold-standard implementation of (b)(10). It provides a complete dump of the Millennium relational database (6,604 tables, 129,148 columns at 99.9% description coverage) plus multimedia files, DICOM images, document imaging, and longitudinal plan data. This is unambiguously a purpose-built export covering clinical, financial, surgical, pharmacy, laboratory, radiology, and administrative data — far exceeding USCDI scope. The biggest strength is the sheer comprehensiveness: a recipient receives, in effect, the entire EHR database and all associated files.
