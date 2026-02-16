# EHI Export Analysis: EnSoftek, Inc

**Product**: DrCloudEHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.1434.ENST.01.01.1.220218

## 1. Product Context

DrCloudEHR is a cloud-based EHR built by EnSoftek, Inc, purpose-built for **behavioral health and human services organizations** — including CCBHCs, substance use disorder treatment programs, IDD/ABA providers, and county health departments. It is deployed across 26 states with 170+ organizations, heavily in the public/safety-net sector.

The product is a full-featured platform encompassing:

- **Clinical documentation**: intake, assessments, progress notes, treatment plans, care plans, clinical forms (including behavioral health–specific screenings like PHQ-9, GAD-7, SDOH), group therapy documentation
- **Medication management**: ePrescribing (via DrFirst), eMAR, CPOE for meds/labs/imaging
- **Practice management**: scheduling, front desk, document management, e-signatures
- **Billing/RCM**: integrated billing, claims management, clearinghouse integration (Office Ally), A/R tracking
- **Patient portal**: messaging, document access, telehealth, self-registration
- **Specialty modules**: eye/ophthalmology forms, ABA tools, IDD workflows
- **Interoperability**: FHIR APIs, DIRECT messaging, public health reporting (immunization registries, syndromic surveillance)

The underlying platform is based on **OpenEMR** (the database is named "openemr" and uses MariaDB 10.11.5), with substantial behavioral health and specialty extensions.

For (b)(10) completeness, the export should cover: demographics, clinical encounters, notes, assessments (especially behavioral health), medications, labs/imaging orders & results, billing/claims, insurance, patient portal communications, documents, therapy group records, and specialty clinical forms.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/drcloudehr.FHIR.xml` (665 KB) | **PRIMARY artifact.** SchemaSpy XML export containing complete machine-readable schema: 128 tables, 2,747 columns, with types, remarks, and foreign key relationships. | ⭐⭐⭐ Most informative |
| `downloads/index.html` (118 KB) | Main SchemaSpy documentation page with export format description, table listing, and overview. Documents that the export is CSV-in-ZIP format. | ⭐⭐⭐ Key for export mechanics |
| `downloads/columns.html` (1.1 MB) | Complete HTML listing of all 2,747 columns across 128 tables with types and comments. Redundant with XML. | ⭐⭐ Supplementary |
| `downloads/relationships.html` (9 KB) | Foreign key relationship diagram page. | ⭐ Supporting |
| `downloads/anomalies.html` (21 KB) | SchemaSpy-detected database anomalies. | ⭐ Supporting |
| `downloads/constraints.html` (11 KB) | Database constraints listing. | ⭐ Supporting |
| `downloads/routines.html` (9 KB) | Stored procedures and functions. | ⭐ Supporting |
| `downloads/orphans.html` (8 KB) | Orphan tables (no FK relationships). | ⭐ Supporting |
| `downloads/insertionOrder.txt` / `deletionOrder.txt` (2 KB each) | Table load/delete ordering for database operations. | ⭐ Supporting |
| `downloads/diagrams/summary/*.svg` | Relationship diagrams (compact and large). | ⭐ Visual reference |
| `downloads/diagrams/tables/*.svg` | Per-table relationship diagrams (1-degree and 2-degree). | ⭐ Visual reference |
| `downloads/tables/*.html` (128 files) | Per-table HTML documentation pages with column details. | ⭐⭐ Supplementary |
| `downloads/enrichment/schema.json` (945 KB) | Prior agent's JSON extraction of the XML schema. | Used for reference only; built own parse |

## 3. Export Mechanics

- **Format**: CSV files packaged in ZIP archives. Each table in the database schema maps to a `<table_name>.csv` file in the ZIP.
- **Structure**: Each ZIP contains:
  - CSV files for each table with patient data
  - `/documents/<pid>/` — patient documents from the document storage system
  - `/images/` — images used in clinical forms (e.g., pain maps)
  - `README` — links to the online documentation
- **Batch size**: Configurable, ZIP files range from ~1 MB to 4 GB
- **Scope**: Single-patient or multi-patient batch export
- **Mechanism**: UI-driven export from within DrCloudEHR (details from index.html documentation)
- **Bulk capability**: Yes — supports batch export of multiple patients in a single ZIP
- **Access constraints**: Not documented; no mention of fees

The documentation explicitly states: *"Every batch zip file is self-contained and can be used to import that batch of patients into another EHR."* This indicates a purpose-built export designed for data portability.

## 4. Export Content: What's In It

The export is a **native database dump** of the DrCloudEHR/OpenEMR data model, documented via SchemaSpy. The schema contains:

- **128 tables** (all documented with table-level remarks except 1)
- **2,747 columns** total
- **1,134 columns (41.3%)** have descriptive remarks/comments
- **All columns** have type information (though some in `amendments_history` show "Unknown")
- **314 columns** have documented foreign key relationships
- **127 of 128 tables** have table-level descriptions

### Documentation Quality by Category

The remark coverage is uneven. Some categories are very well documented (100% remarks on Amendments, Documents, Facility/Users, Scheduling) while others are nearly bare — Review of Systems forms (257 columns, 2 remarks), Eye/Ophthalmology forms (471 columns, 25 remarks), Patient History (91 columns, 2 remarks), and Vitals (59 columns, 4 remarks). The best-documented areas tend to be the structural tables; the clinical form tables that hold actual patient observations are often documented only by their column names.

### Vendor's own content organization

The vendor organizes this as a flat database schema (no explicit categories in the SchemaSpy output). I have grouped tables by functional domain based on naming conventions and table descriptions. The 20 largest tables:

| Table | Fields | w/ Remarks | Type | Domain |
|---|---|---|---|---|
| form_ros | 142 | 1 | Clinical Form | Review of Systems |
| form_sdoh | 135 | 4 | Clinical Form | SDOH Assessment |
| patient_data | 126 | 92 | Core Table | Demographics |
| form_reviewofs | 115 | 1 | Clinical Form | Review of Systems |
| history_data | 91 | 2 | Core Table | Patient History |
| form_bronchitis | 89 | 64 | Clinical Form | Specialty |
| form_eye_neuro | 81 | 2 | Clinical Form | Ophthalmology |
| form_eye_refraction | 65 | 2 | Clinical Form | Ophthalmology |
| users | 62 | 62 | Reference Table | Facility/Users |
| form_eye_mag_dispense | 55 | 1 | Clinical Form | Ophthalmology |
| prescriptions | 48 | 17 | Core Table | Medications |
| form_eye_mag_wearing | 41 | 1 | Clinical Form | Ophthalmology |
| form_eye_antseg | 39 | 1 | Clinical Form | Ophthalmology |
| openemr_postcalendar_events | 39 | 39 | Core Table | Scheduling |
| facility | 37 | 37 | Reference Table | Facility |
| lists | 36 | 36 | Core Table | Problems/Allergies |
| form_eye_hpi | 35 | 2 | Clinical Form | Ophthalmology |
| insurance_data | 34 | 3 | Core Table | Insurance |
| form_encounter | 33 | 32 | Core Table | Encounters |
| documents | 33 | 33 | Core Table | Documents |

The complete inventory is in `analysis/entity-inventory-full.json`.

### Category breakdown (all 128 tables)

| Category | Tables | Columns | % Remarked |
|---|---|---|---|
| Eye/Ophthalmology Forms | 15 | 471 | 5% |
| Review of Systems | 2 | 257 | 1% |
| Other Clinical Forms | 18 | 252 | 61% |
| Assessments & Questionnaires | 7 | 231 | 25% |
| Patient Demographics & Tracking | 6 | 179 | 72% |
| Orders & Results (Lab/Imaging) | 9 | 143 | 87% |
| Billing & Claims | 6 | 127 | 72% |
| Facility & Users | 3 | 102 | 100% |
| Care Plans & Clinical Notes | 6 | 95 | 34% |
| Patient History | 1 | 91 | 2% |
| Medications | 3 | 89 | 39% |
| Patient Portal | 5 | 80 | 48% |
| Insurance & Eligibility | 5 | 76 | 41% |
| Configuration & Layout | 6 | 68 | 24% |
| Encounters | 3 | 64 | 52% |
| Vitals | 3 | 59 | 7% |
| Scheduling | 2 | 58 | 100% |
| Problems/Allergies/Issues | 4 | 58 | 81% |
| Documents & Signatures | 4 | 50 | 100% |
| Immunizations | 2 | 42 | 48% |
| Therapy Groups | 5 | 30 | 70% |
| Clinical Decision Support | 4 | 27 | 89% |
| Communications & Logging | 2 | 23 | 22% |
| Amendments | 2 | 15 | 100% |
| Form Registry | 1 | 14 | 100% |
| Prior Authorization | 1 | 8 | 25% |
| Referrals/Transactions | 1 | 7 | 14% |
| Pharmacies | 1 | 6 | 0% |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a **direct dump of the full OpenEMR/DrCloudEHR database schema**, covering 128 tables and 2,747 columns. This is not a filtered clinical summary — it includes the product's internal data model spanning clinical, billing, administrative, and portal domains.

**Richest areas:**
- **Patient Demographics** (126 columns on `patient_data` alone) — comprehensive including race, ethnicity, language, contacts, employment, multiple name fields
- **Clinical Forms** (54 `form_*` tables, 1,447 columns) — extensive specialty forms including ophthalmology (15 tables), behavioral health assessments (PHQ-9, GAD-7, SDOH), review of systems, vitals, SOAP notes, care plans, treatment plans
- **Billing & Claims** (6 tables, 127 columns) — `billing`, `claims`, `ar_activity`, `ar_session`, `voids`, `form_misc_billing_options` — genuine billing depth
- **Orders & Results** (9 tables, 143 columns) — procedure orders, results, reports, providers, questions/answers — well-structured lab/imaging workflow
- **Patient Portal** (5 tables, 80 columns) — portal messages, mail, documents, signatures, activity tracking

**Thinnest areas:**
- **Referrals/Transactions** — only 1 table (`transactions`) with 7 columns and 1 remark
- **Prior Authorization** — only 1 table (`form_prior_auth`) with 8 columns
- **Patient History** — `history_data` has 91 columns but only 2 have remarks (column names are self-descriptive, e.g., `coffee`, `tobacco`, `alcohol`, `history_mother`, but lack formal documentation)

**Notable strengths:**
- Includes **therapy group** tables (5 tables) — directly relevant to the behavioral health focus
- Includes **patient portal communications** (`onsite_mail`, `onsite_messages`) — secure messaging between patients and staff
- Includes **document storage** with actual files exported in the ZIP (`/documents/<pid>/`)
- Includes **e-signature records** (`esign_signatures`)
- Includes **patient-reported outcomes** (`pro_assessments`)
- Includes **SDOH screening** (`form_sdoh` with 135 columns)
- Includes **eligibility verification** and **benefit eligibility** tables

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient_data` (126 fields), `patient_history` (14 fields), `history_data` (91 fields) | Thorough — 126 demographic columns |
| Encounters / visits | ✅ Covered | `form_encounter` (33 fields), `form_groups_encounter` (24 fields), `external_encounters` (7 fields) | Good — includes group encounters |
| Problems / conditions / diagnoses | ✅ Covered | `lists` (36 fields), `lists_medication` (8 fields), `issue_encounter` (4 fields), `issue_types` (10 fields) | Good — unified issues model |
| Medications / prescriptions | ✅ Covered | `prescriptions` (48 fields), `drugs` (22 fields), `drug_sales` (19 fields), `lists_medication` (8 fields) | Good — includes dispensing data |
| Allergies | ✅ Covered | Allergies stored in `lists` table (type-based issue model) | Adequate — part of unified issues model |
| Immunizations | ✅ Covered | `immunizations` (30 fields), `immunization_observation` (12 fields) | Good |
| Vitals | ✅ Covered | `form_vitals` (28 fields), `form_vital_details` (4 fields), `form_eye_vitals` (27 fields) | Good — includes eye-specific vitals |
| Lab results | ✅ Covered | `procedure_result` (16 fields), `procedure_report` (13 fields), `procedure_order` (31 fields) | Good — well-structured order/result model |
| Imaging / diagnostic reports | ✅ Covered | Same procedure tables handle imaging orders and results | Adequate |
| Procedures | ✅ Covered | `procedure_order_code` (16 fields), `external_procedures` (9 fields), plus procedure tables | Good |
| Clinical notes / documents | ✅ Covered | `form_clinical_notes` (17 fields), `form_soap` (11 fields), `form_dictation` (9 fields), `form_CAMOS` (11 fields), `documents` (33 fields) with actual files exported | Thorough — multiple note types plus document files |
| Care plans / goals | ✅ Covered | `form_care_plan` (20 fields), `form_treatment_plan` (18 fields), `form_aftercare_plan` (18 fields) | Good — three separate plan types |
| Orders / referrals | ✅ Covered | `procedure_order` (31 fields), `transactions` (7 fields — referrals), `form_transfer_summary` (15 fields) | Adequate |
| Insurance / coverage | ✅ Covered | `insurance_data` (34 fields), `insurance_companies` (13 fields), `benefit_eligibility` (18 fields), `eligibility_verification` (8 fields), `insurance_type_codes` (3 fields) | Good — includes eligibility data |
| Claims / billing | ✅ Covered | `billing` (30 fields), `claims` (13 fields), `ar_activity` (22 fields), `ar_session` (17 fields), `form_misc_billing_options` (33 fields), `voids` (12 fields) | **Strong** — 6 tables, 127 columns covering claims, A/R, billing codes, voids |
| Payments | ✅ Covered | `ar_activity` and `ar_session` tables cover payment posting and sessions | Adequate — part of A/R model |
| Consents / directives | ⚠️ Partial | `onsite_documents` and `onsite_signatures` handle some consent workflows; `document_templates` for form templates | No dedicated consent table; relies on document system |
| Patient communications / portal messages | ✅ Covered | `onsite_mail` (22 fields), `onsite_messages` (7 fields), `pnotes` (16 fields — patient notes/messages) | Good — both async mail and real-time chat |
| Specialty: Behavioral health | ✅ Covered | `form_phq9` (27 fields), `form_gad7` (4 fields), `form_sdoh` (135 fields), `form_aftercare_plan` (18 fields — includes acute intoxication/withdrawal), therapy group tables (5 tables) | Good — core to product's focus |
| Specialty: Ophthalmology | ✅ Covered | 15 `form_eye_*` tables (471 columns) covering neuro, refraction, acuity, anterior/posterior segment, HPI, biometrics, ROS, dispensing, orders | Extensive — inherited from OpenEMR eye module |
| Prior authorization | ⚠️ Partial | `form_prior_auth` (8 fields) | Minimal — only 8 fields |
| Patient-reported outcomes | ✅ Covered | `pro_assessments` (12 fields), `questionnaire_response` (20 fields), `form_questionnaire_assessments` (16 fields) | Good |
| Amendments | ✅ Covered | `amendments` (10 fields), `amendments_history` (5 fields) | Complete |

**Gap Analysis Summary**: The export covers **19 of 19 applicable domains** with at least partial coverage. There are no major domain-level gaps. The product stores billing data and the export includes billing data. The product stores behavioral health assessments and the export includes them. Patient portal communications are exported. The only thin areas are prior authorization (8 fields) and consents (handled through the generic document system rather than a dedicated table).

## 6. Documentation Quality

**Strengths:**
- **Machine-readable schema** (SchemaSpy XML) with complete type information, foreign keys, and indexes — a developer can parse this programmatically
- **127 of 128 tables** have table-level descriptions explaining what each table stores
- **Relationship documentation** with FK diagrams (SVG) and insertion/deletion ordering
- **Export format clearly documented**: the index.html explains the ZIP structure, CSV format, document storage layout, and how to interpret the data
- **Self-contained export**: documentation explicitly states exports are importable

**Weaknesses:**
- **Only 41.3% of columns have descriptive remarks** — many columns are documented only by their names
- **Worst areas**: Review of Systems (1% remarked), Eye forms (5%), Patient History (2%), Vitals (7%) — these are clinically important tables with hundreds of columns that have no descriptions beyond their column names
- **No value sets documented**: although many columns reference `list_options` via foreign keys (e.g., `amendment_status` references `list_options.list_id='amendment_status'`), the actual coded values are not enumerated in the documentation
- **No sample data files** provided with the documentation
- **Column names are generally self-descriptive** (e.g., `last_mammogram`, `sleep_patterns`, `seatbelt_use` in `history_data`), which partially compensates for missing remarks

**Overall**: A developer could build an import from this documentation, especially for the well-documented tables (billing, demographics, procedures). For the sparsely documented clinical forms, column names are descriptive enough to infer meaning in most cases, but formal descriptions would improve confidence. The value set gap (no enumeration of coded values) would require access to a running system or the `list_options` table data to fully interpret coded fields.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains DrCloudEHR stores. It includes 128 tables spanning demographics (126 fields), clinical encounters, multiple clinical form types (54 form tables), billing and claims (6 tables, 127 fields), insurance and eligibility (5 tables), medications, labs/imaging, patient portal communications, documents (with actual file export), therapy groups, behavioral health assessments (PHQ-9, GAD-7, SDOH), patient-reported outcomes, and specialty ophthalmology forms. The export goes well beyond USCDI — it includes billing/A/R tables, prior authorizations, patient portal messages, e-signatures, therapy group attendance, voids, and dozens of specialty clinical forms that have no USCDI or US Core equivalent.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged clinical exchange. The evidence:
1. The export is a **native database dump** (CSV per table) of the OpenEMR/DrCloudEHR schema — not C-CDA or FHIR bulk data
2. The documentation site is explicitly labeled as *"ONC §170.315(b)(10) Electronic Health Information export"*
3. The export includes **billing**, **A/R**, **claims**, **patient portal messages**, **therapy groups**, and other non-USCDI data that would never appear in a (g)(10) FHIR API or C-CDA export
4. The vendor built a **SchemaSpy-based documentation site** specifically for this export, with per-table documentation, relationship diagrams, and a machine-readable XML schema
5. The export includes **patient documents** (actual files) alongside structured data
6. The ZIP format with CSV files, document folders, and README is clearly designed for (b)(10) portability

### Key Findings

1. **Genuinely comprehensive database export**: 128 tables / 2,747 columns covering clinical, billing, administrative, and portal data — this is the full database schema, not a filtered subset. The underlying OpenEMR platform provides a solid data model.

2. **Strong billing coverage**: 6 dedicated billing/claims/A/R tables with 127 columns, including claims tracking, A/R payment sessions, billing codes, and voided transactions. This is a clear signal of genuine (b)(10) effort — billing data is the litmus test most repackaged exports fail.

3. **Behavioral health depth**: The export includes behavioral health–specific tables (PHQ-9, GAD-7, SDOH screening with 135 columns, therapy group tables, aftercare plans referencing substance use treatment) that reflect the product's clinical focus.

4. **Documentation is mixed**: 100% of tables and 41.3% of columns have descriptions. Well-documented areas (billing, demographics, procedures) alternate with sparsely documented areas (eye forms at 5%, review of systems at 1%, vitals at 7%). The machine-readable XML schema and SchemaSpy site are excellent structural documentation, but column-level descriptions are inconsistent.

5. **Document export includes actual files**: The export ZIP includes a `/documents/<pid>/` directory with the patient's stored documents, not just metadata — a strong feature for completeness.

### Summary Stats

    Coverage:        Comprehensive
    Approach:        Purpose-built EHI export
    Export format:   CSV (in ZIP archives, with document files)
    Entities:        128 tables
    Fields:          2,747 columns
    Descriptions:    41.3% of columns have remarks (127/128 tables have table-level descriptions)
    Sample data:     No
    Bulk export:     Yes (configurable batch sizes)
    Domains covered: 19 of 19 applicable domains (2 partial)

### Bottom Line

DrCloudEHR provides one of the stronger (b)(10) implementations: a genuine native database export with 128 tables covering clinical, billing, insurance, patient portal, and specialty behavioral health data, backed by machine-readable SchemaSpy documentation. A patient or provider would get a meaningfully complete copy of their data. The biggest weakness is uneven column-level documentation — while table structures and types are fully documented, only 41% of individual columns have descriptive remarks, with clinical observation forms being the least documented.
