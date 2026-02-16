# EHI Export Analysis: NextGen Healthcare

**Product**: NextGen Enterprise EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2054.Next.60.10.1.220318 (v6.2021.1 Cures), 15.04.04.2054.Next.80.12.1.250602 (Enterprise 8)

## 1. Product Context

NextGen Enterprise EHR is a comprehensive ambulatory EHR and practice management platform targeting mid-size to enterprise-level healthcare organizations — multi-specialty groups, FQHCs, community health centers, and large single-specialty practices. It serves over 100,000 providers managing 65+ million patients. The company was taken private by Thoma Bravo in 2023 for $1.8 billion.

The product is a full-suite platform encompassing:

- **Clinical Documentation (EHR)**: Specialty-specific templates for 26+ specialties including cardiology, ophthalmology, behavioral health, OB/GYN, pediatrics, orthopedics, rheumatology, dermatology, gastroenterology, oncology, ENT, urology, and more. Supports CPOE, drug interaction checking, CQMs, e-prescribing (EPCS), family health history, social determinants, and implantable device tracking.
- **Practice Management (PM)**: Patient registration, scheduling, eligibility verification, multi-location support, master patient index.
- **Revenue Cycle Management (RCM) & Billing**: Automated claim scrubbing, charge review, claims processing, EDI/clearinghouse, A/R management, denial management, ICD-10 coding, financial reporting.
- **Patient Engagement / Portal**: Secure messaging, self-scheduling, online payments, intake forms, telehealth, remote patient monitoring.
- **Behavioral Health**: Integrated outpatient mental health, substance use disorder, crisis intervention, residential treatment, I/DD services (KLAS award winner).
- **Dental Integration**: Unified dental-medical-behavioral health records for FQHCs.
- **AI**: Ambient Assist (AI SOAP notes), Intelligent Agent (voice command).
- **Interoperability**: C-CDA, FHIR API (g)(10), Direct messaging, Mirth Connect integration engine, HIE connectivity.

For EHI export assessment, the critical question is whether the export covers not just clinical data but also billing/RCM, specialty-specific forms, patient communications, and the deep specialty clinical content across 26+ specialties.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/DD_Complete_EHI_20250627.pdf` | 10,875-page PDF, SQL Server schema dump for the EHI export. 5,290 tables, 283,279 columns. Dated June 27, 2025. Created with Adobe Acrobat. 29.2 MB. | **Primary artifact** — this IS the data dictionary |
| `downloads/ehi-landing-page.html` | HTML source of the EHI documentation landing page at the registered URL. Contains explanatory text about the export format, links to dictionaries for all NextGen products. | **Key context** — explains export format and mechanism |
| `downloads/ehi-landing-page-screenshot.png` | Full-page screenshot of the landing page. | Archival/visual reference |
| `downloads/enrichment/data-dictionary.json` | Machine-parsed extraction of the PDF: 5,290 table objects with column arrays (name, dataType, default, notNull). 37.3 MB JSON. | **Key reference** — used as basis for quantitative analysis |
| `downloads/enrichment/summary.json` | Extraction statistics from enrichment. | Supporting stats |
| `downloads/enrichment/dd-raw.txt` | Raw pdftotext output of the PDF. 7.6 MB. | Intermediate artifact |
| `downloads/enrichment/extract-data-dictionary.ts` | Bun TypeScript script used to parse the PDF. | Methodology reference |

## 3. Export Mechanics

**Format**: SQL Server database extract in machine-readable format. The data dictionary documents SQL Server table/column schemas with data types including `char`, `varchar`, `nvarchar`, `int`, `datetime`, `uniqueidentifier`, `bit`, `float`, `money`, `image`, `xml`, and others. Binary content (images, documents, reports, audio files) is exported as separate files in accompanying folders.

**Mechanism**: The landing page states the export is available in "v6.2021.1 Cures and higher." No specific UI workflow or API documentation is provided for initiating the export. The landing page directs users to "request a CCDA from their provider" as an alternative for human-readable format, implying the EHI export requires a provider/admin action. The mandatory disclosures mention a "Bulk C-CDA Export Utility" requiring billable setup hours, suggesting the machine-readable EHI export may also require vendor-assisted setup.

**Single-patient vs bulk**: Not explicitly documented. The database-level export structure (with `enterprise_id`, `practice_id`, `person_id` as key columns across all tables) implies per-patient extraction is possible, but whether the system exports one patient at a time or in bulk is unclear.

**Access constraints**: The landing page mentions no fees for the EHI export itself, but the mandatory disclosures note that interface implementation requires separate licensing and professional services fees. The export documentation URL is publicly accessible with no authentication.

## 4. Export Content: What's In It

### Data dictionary structure

The export documentation is a single massive PDF (10,875 pages) containing a SQL Server database schema dump. For each table, it lists:
- **Table Name**: The SQL Server table name (tables conventionally end with `_`)
- **Column Name**: Each column in the table
- **Data Type**: SQL Server data type
- **Default**: Default value (when present)
- **Not Null**: Constraint indicator (unreliably captured in PDF extraction)

There are **no field descriptions** — column names are the only semantic information. There are **no value set enumerations**, **no relationship/FK documentation**, **no table-level descriptions**, and **no sample data**. The schema is entirely self-documenting via naming conventions.

### Key statistics

- **Total tables**: 5,290
- **Total fields**: 283,279
- **Fields with data types**: 281,893 (99.5%)
- **Fields with descriptions**: 0 (0%)
- **Fields with defaults**: 6,400 (2.3%)
- **Average fields per table**: 53.5
- **Thin tables (<5 fields)**: 1
- **Data types**: 20+ SQL Server types used; most common are `varchar`, `char`, `int`, `datetime`, `uniqueidentifier`, `bit`

### Vendor's own content organization

The vendor does not organize the data dictionary into categories — tables are listed alphabetically. However, the table naming conventions reveal a clear organizational structure. Based on automated categorization of all 5,290 tables by name prefix patterns (see `analysis/analyze_dictionary.py`), the export covers these domains:

**High-level domain aggregation** (from `analysis/entity-inventory-summary.json`):

| Domain Group | Tables | Fields | Notes |
|---|---|---|---|
| Clinical Documentation (HPI, PE, ROS, notes, forms) | 1,615 | 82,675 | Largest domain — extensive specialty templates |
| Specialty Clinical (26+ specialties) | 1,329 | 75,531 | Cardiology alone: 389 tables, 21,803 fields |
| Surgical / Procedural (IORTS) | 752 | 62,380 | Very deep surgical/procedural documentation |
| Demographics / Patient | 148 | 5,333 | Patient identity, contacts, demographics |
| Assessments / Screening | 117 | 3,985 | ACEs, SDOH, barriers to care, family history |
| Orders / Referrals | 91 | 7,332 | 68 order tables, 23 referral tables |
| Medications / Allergies | 74 | 3,817 | Prescriptions, allergy tracking |
| Billing / Financial / Insurance | 66 | 2,862 | Claims (311 cols), charges (176 cols), payers, insurance |
| Laboratory | 65 | 3,696 | Lab orders, results, master tables |
| Care Plans / Goals | 52 | 1,855 | 47 goal/care plan tables across specialties |
| Documents / Media | 42 | 757 | Attachments, images, document library |
| Communications | 42 | 1,701 | Telephone calls, portal, patient messages |
| Encounters | 39 | 1,226 | Encounter records, scheduling |
| Vitals | 32 | 763 | Adult, pediatric, device-captured vitals |
| Immunizations | 26 | 1,101 | Forecasts, titers, reactions, contraindications |
| Diagnoses / Problems | 25 | 708 | Problem lists, chronic conditions |
| Consents | 11 | 243 | Advance directives, consent forms |
| Other / Uncategorized | 764 | 27,314 | Mix of specialty forms, system, reference data |

**Top 20 largest tables** (representative examples):

| Table | Fields | Category |
|---|---|---|
| `symptom_master_` | 699 | Symptom Reference |
| `symptom_master2_` | 645 | Symptom Reference |
| `RHE_Conn_Tissue_` | 586 | Rheumatology |
| `IORTSproc_jt_inj_foot_` | 576 | Surgical / Procedural |
| `IORTSsymptom_master_` | 546 | Surgical / Procedural |
| `Lab_Master_` | 536 | Laboratory |
| `IORTSproc_jt_px_codes2_` | 493 | Surgical / Procedural |
| `IORTSsurg_sched_v2_` | 493 | Surgical / Procedural |
| `IORTSsymptom_master2_` | 481 | Surgical / Procedural |
| `activity_detail_snapshot` | 477 | Activity Tracking |
| `IORTSproc_jt_inj_hand_` | 467 | Surgical / Procedural |
| `IORTSnum_pe_adult_ext1_` | 459 | Surgical / Procedural |
| `IORTSnum_pe_adult_ext2_` | 459 | Surgical / Procedural |
| `PEDS_PE_NEWBORN_` | 437 | Pediatrics |
| `IORTSproc_jt_inj_wrist_` | 406 | Surgical / Procedural |
| `IORTSproc_jt_px_codes_` | 399 | Surgical / Procedural |
| `IORTSnb_PE_` | 396 | Surgical / Procedural |
| `pe_adult_` | 395 | Physical Exam |
| `AINF_PT_LTC_MDS_` | 384 | Clinical Forms (AINF) |
| `claims` | 311 | Billing / Financial |

**Notable billing/financial tables** (verifying actual export of RCM data):

| Table | Fields | Content Indicators |
|---|---|---|
| `claims` | 311 | `claim_id`, `status`, `payer_id`, `rendering_provider_id`, `total_charge`, `submission_date` |
| `claim_payers` | 192 | `claim_filing_ind`, `source_of_pay`, `ins_type_code`, `payer_claim_office_nbr` |
| `charges` | 176 | `charge_id`, `person_id`, `source_type`, `service_item_lib_id`, `location_id` |
| `card_device_charges_` | ~50+ | Cardiology device billing |
| `card_submit_superbill_` | ~30+ | Superbill submission |
| `claim_based_reporting_` | — | Claim analytics |
| `CPTII_codes_holding_` | — | CPT II quality codes |

The full inventory of all 5,290 tables with all 283,279 fields is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The NextGen Enterprise EHR EHI export is a **full SQL Server database schema dump** covering the entire product's data model. The export is organized around the product's internal table structure, with tables named by specialty prefix (e.g., `CARD_` for cardiology, `bh_` for behavioral health, `IORTS` for surgical/procedural) and functional area (e.g., `hpi_` for history of present illness, `pe_` for physical exam).

**Strongest coverage areas:**
- **Clinical documentation** (1,615 tables, 82,675 fields): Massive depth across HPI, physical exam, review of systems, clinical notes, and hundreds of specialty-specific documentation forms
- **Specialty clinical** (1,329 tables, 75,531 fields): 24+ medical specialties represented with dedicated table sets, led by cardiology (389 tables) and ophthalmology (176 tables)
- **Surgical/procedural** (752 tables, 62,380 fields): Extremely deep IORTS framework covering surgical scheduling, documentation, billing, and outcomes
- **Orders and referrals** (91 tables, 7,332 fields): Comprehensive ordering system with 33 referral-related tables

**Moderate coverage:**
- **Billing/financial/insurance** (66 tables, 2,862 fields): The `claims` table alone has 311 columns — this is genuine billing data, not a placeholder. Includes claim payers, charges, encounter payers, insurance forms, preauthorization, and eligibility
- **Assessments/screening** (117 tables, 3,985 fields): ACEs screening, barriers to care, social determinants, family history, medical history
- **Care plans and goals** (52 tables, 1,855 fields): Dedicated care plan framework plus specialty-specific goal tracking

**Thinner but present:**
- **Communications** (42 tables, 1,701 fields): Telephone calls, patient portal data, communication summaries — present but relatively thin for a product with a full patient portal
- **Documents/media** (42 tables, 757 fields): Document library, attachments, image capture — with binary files exported separately per the landing page

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | 148 tables, 5,333 fields. `CARD_patient_`, `ainf_patient_enc_info_`, `DCE_CCM_Demographic_Fields_` and 145 more | Thorough; patient identity data across specialties |
| Encounters / visits | ✅ Covered | `patient_encounter`, `encounter_diags`, `encounter_notes`, `encounter_payer`, scheduling tables (14) | Solid encounter model with diagnoses, notes, payers linked |
| Problems / conditions | ✅ Covered | `diagnos*` tables, `chronic_condition_status_`, `encounter_diags`, specialty-specific diagnosis tables | Present across many specialty contexts |
| Medications / prescriptions | ✅ Covered | 38 tables, 1,094 fields. `allergy_prescribe_`, `Associate_Medications_`, `bh_medication_data_`, `erx_message_history` | E-prescribing and medication management covered |
| Allergies | ✅ Covered | 36 tables, 2,723 fields. `allergy_prescribe_` and allergy-related tables | Extensive allergy documentation |
| Immunizations | ✅ Covered | 26 tables, 1,101 fields. `immunization_ord_`, `Immunization_Rec_`, `immunization_forecasts`, `imported_immunizations`, `Vaccine_Lot_`, `imm_vaccine_reaction`, `vaers_form_` | Comprehensive — includes forecasts, titers, reactions, contraindications, VAERS reporting |
| Vitals | ✅ Covered | 32 tables, 763 fields. `VS_Adult_`, `vs_charts_adult_`, `vs_charts_peds_`, `WelchAllynVitals_` | Adult and pediatric vitals with device integration |
| Lab results | ✅ Covered | 65 tables, 3,696 fields. `Lab_Master_` (536 cols), `ainf_ord_labs_*`, `CBC_Manual_` | Deep lab data model |
| Imaging / diagnostic reports | ✅ Covered | `viewAllDiagStudy_`, `diagnostics_all_orders_`, imaging-specific tables across specialties | Present but spread across specialty tables |
| Procedures | ✅ Covered | 752 tables (IORTS framework), 62,380 fields. Surgical scheduling, consent, pre/post-op, billing | Exceptionally deep — this is a standout area |
| Clinical notes / documents | ✅ Covered | 12 clinical notes tables + 42 document tables + binary files exported separately. `ChartNotesExtPop_`, `encounter_notes`, `Document_Library_` | Notes in tables; binary content in file folders |
| Care plans / goals | ✅ Covered | 52 tables, 1,855 fields. `care_plan_*` framework, `pt_goals_*`, `bh_iap_goals_*`, specialty-specific goals | Multi-specialty care plan support |
| Orders / referrals | ✅ Covered | 91 tables, 7,332 fields. `ainf_orders_*`, `ord_*`, `patient_referral`, `referral_management_`, 33 referral tables total | Comprehensive ordering and referral workflows |
| Insurance / coverage | ✅ Covered | 21 tables, 729 fields. `patient_eligibility` (60 cols), `encounter_payer` (37 cols), `claim_payers` (192 cols), preauthorization tables | Eligibility, encounter-level payer, claim payers |
| Claims / billing | ✅ Covered | `claims` (311 cols), `charges` (176 cols), `card_submit_superbill_`, `CPTII_codes_holding_`, `claim_based_reporting_` | Genuine billing data — claims table with 311 columns is substantial |
| Payments | ⚠️ Partial | No dedicated payment/remittance tables identified by name; payment data may be embedded in `claims` (311 cols) or `charges` (176 cols) | Product has full RCM; dedicated payment/remittance tables may exist under uncategorized names |
| Consents / directives | ✅ Covered | 11 tables, 243 fields. `advance_directives_`, `configurable_consent_`, `proc_consent_`, specialty-specific consent forms | Present across clinical contexts |
| Patient communications / portal | ⚠️ Partial | 42 tables, 1,701 fields. `ngweb_communications`, telephone call tables, `patient_recall_message_result`, `epcs_erx_message_history` | Portal/web tables present but relatively thin for a product with full portal messaging, self-scheduling, and online payments |
| Behavioral health | ✅ Covered | 204 tables, 10,522 fields. `bh_aims_`, `bh_ansa_`, `bh_asam_`, `bh_crisis_contact_note_`, `bh_psychopharm_`, `ADHD_*`, `ACEs_*`, `depression_*` | Exceptionally deep — KLAS award-winning module well-represented |
| Cardiology | ✅ Covered | 389 tables, 21,803 fields. Comprehensive cardiac documentation, testing, devices, procedures | Outstanding specialty depth |
| Ophthalmology | ✅ Covered | 176 tables, 10,770 fields. Eye exams, contacts, ASC, consent, billing | Deep specialty coverage |
| OB/GYN | ✅ Covered | 113 tables, 4,835 fields. Prenatal, labor/delivery, birth records, well-woman | Full reproductive health workflow |
| Pediatrics | ✅ Covered | 106 tables, 7,182 fields. `PEDS_PE_NEWBORN_` (437 cols), well-child, immunizations | Deep pediatric documentation |
| Oncology | ✅ Covered | 28 tables, 1,766 fields. `Cancer_staging_grid_`, `Cancer_type_grid_`, `onc_*` tables | Present with staging and treatment data |
| Dental | ⚠️ Partial | 1 table, 87 fields. `dental_summary_` | Product integrates dental (especially FQHCs) but only 1 export table — possible gap |
| Social determinants / SDOH | ✅ Covered | 39 tables, 1,245 fields. `SHx_*`, `social_*`, `barriers_to_care_` | Solid SDOH and social history coverage |

## 6. Documentation Quality

**Strengths:**
- **Massive scope**: 5,290 tables with 283,279 columns — this is clearly a complete database schema, not a curated subset
- **Data types documented**: 99.5% of fields have SQL Server data types specified
- **Clear landing page**: The EHI documentation page clearly explains the export format, distinguishes machine-readable from human-readable exports, and properly directs users
- **Actively maintained**: Updated June 27, 2025 — current
- **Binary content acknowledged**: Landing page explicitly states that images, documents, reports, and audio files are in accompanying file folders

**Weaknesses:**
- **Zero field descriptions**: Not a single column has a description beyond its name. `chk_pt_edu_session` vs `chk_pt_multi_gest` requires domain knowledge to interpret
- **No value sets**: Coded fields (varchar, int values representing categories) have no enumeration of valid values
- **No relationship/FK documentation**: How tables join is not documented. `person_id` and `enc_id` serve as implicit FKs but there's no ERD or relationship diagram
- **No table descriptions**: What each table represents must be inferred from naming conventions
- **No sample data**: No example exports or worked examples
- **PDF-only format**: A 10,875-page PDF is essentially unusable without automated parsing. No structured alternative (CSV, JSON, SQL DDL) is provided by the vendor
- **No export procedure documentation**: No user guide for how to request, configure, or execute the export

**Usability assessment**: A developer attempting to import this data into another system would face significant reverse-engineering effort. The column names are often self-evident (e.g., `person_id`, `enc_id`, `create_timestamp`), but specialty-specific columns (e.g., `chk_topo_agt_5fu`, `cm_iol_model`) require clinical domain expertise. The lack of FK documentation means reconstructing table relationships requires inspecting common key columns across thousands of tables. The vendor essentially exported their internal database schema documentation — valuable for completeness, but minimal for usability.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

NextGen has exported their entire SQL Server database schema — 5,290 tables with 283,279 columns. This is not a curated clinical summary; it is the actual internal data model of the product. The export covers:
- All 26+ clinical specialties the product supports, with dedicated table sets per specialty
- Core clinical data (demographics, encounters, diagnoses, medications, labs, vitals, immunizations, notes)
- Billing and financial data (claims with 311 columns, charges with 176 columns, claim payers with 192 columns)
- Insurance and authorization (eligibility, encounter payers, preauthorization)
- Behavioral health (204 tables — reflecting their KLAS-awarded module)
- Surgical/procedural documentation (752 tables — the deepest single domain)
- Patient communications, portal data, referrals, care plans, consents
- Binary content (images, documents, audio) exported as separate files

The coverage clearly goes far beyond USCDI. The `claims` table alone (311 columns) contains more fields than many vendors' entire EHI exports. Minor gaps exist (dental is thin at 1 table for a product with dental integration; dedicated payment tables are not clearly identifiable), but these are marginal relative to the extraordinary breadth of coverage.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. The vendor built a mechanism to export their internal SQL Server database tables directly, complete with specialty-specific clinical forms, billing data, surgical records, and behavioral health documentation. This is not a repackaged FHIR API or C-CDA export — the 5,290 SQL Server tables with internal naming conventions (`IORTSsurg_sched_v2_`, `bh_psychopharm_`, `card_device_charges_`) make it clear this is the product's native data model. The landing page explicitly distinguishes between this machine-readable EHI export and the human-readable C-CDA alternative.

### Key Findings

1. **Massive, genuine database export**: 5,290 tables with 283,279 columns exported in SQL Server native format. This is one of the largest EHI data dictionaries in the industry, reflecting a product with deep specialty clinical content across 26+ medical specialties.

2. **Billing data is real**: The `claims` table (311 columns), `charges` (176 columns), and `claim_payers` (192 columns) confirm this export includes genuine RCM data — not just clinical summaries. This alone distinguishes it from vendors who repackage C-CDA or FHIR exports.

3. **Zero documentation beyond schema**: Despite the impressive breadth, not a single field has a description. No value sets, no relationships, no sample data. The 10,875-page PDF is a raw schema dump with no interpretive guidance. A developer would face enormous reverse-engineering effort.

4. **Specialty depth is exceptional**: Cardiology (389 tables), behavioral health (204 tables), ophthalmology (176 tables), OB/GYN (113 tables), and pediatrics (106 tables) each have dedicated table frameworks with hundreds to thousands of specialty-specific fields. This reflects genuine clinical depth, not placeholder tables.

5. **Export procedure is undocumented**: There is no user-facing guide for how to initiate, configure, or receive the EHI export. The landing page describes what the export contains but not how to get it.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   SQL Server database extract (native tables) + binary file folders
    Entities:        5,290 tables
    Fields:          283,279
    Descriptions:    0% (no field descriptions)
    Sample data:     No
    Bulk export:     Unclear
    Domains covered: 17 of 19 applicable domains (payments and dental are partial/thin)

### Bottom Line

NextGen Healthcare has built one of the most comprehensive EHI exports available — a full database dump of 5,290 SQL Server tables covering clinical, billing, specialty, and administrative data across 26+ medical specialties. A patient or provider would receive genuinely complete data. The single biggest weakness is documentation quality: zero field descriptions, no value sets, no relationship documentation, and no export procedure guide mean that while the data is all there, making practical use of it requires significant reverse-engineering. The breadth is outstanding; the interpretability is poor.
