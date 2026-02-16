# EHI Export Analysis: EnSoftek, Inc

**Product**: DrCloudEHR (version 2025)
**Analysis date**: 2026-02-16
**CHPL IDs**: 10835 (15.02.05.1434.ENST.01.01.1.220218)

## 1. Product Context

DrCloudEHR is a cloud-based EHR purpose-built for **behavioral health and human services organizations**, developed by EnSoftek, Inc (Beaverton, Oregon). The product is deeply specialized for mental health clinics, substance use disorder (SUD) treatment programs, Certified Community Behavioral Health Clinics (CCBHCs), IDD/ABA service providers, and county health/human services agencies. It is in use across 26 states with a heavily public-sector customer base.

The product is a comprehensive integrated platform encompassing:

- **Clinical documentation**: Intake, assessments, progress notes, treatment plans, care plans, form builder, behavioral health instruments (PHQ-9, GAD-7, SDOH screening)
- **Medication management**: ePrescribing (via DrFirst), eMAR, CPOE, drug interaction checking
- **Practice management**: Scheduling, front desk, document management, electronic signatures
- **Billing / RCM**: Full-spectrum revenue cycle management, claims submission, clearinghouse integration (Office Ally), Medicaid billing
- **Patient engagement**: Patient portal, telehealth, secure messaging
- **Specialty features**: CCBHC nine required service areas, IDD/ABA tools, AI Group Scribing, clinical dictation
- **Reporting**: Standard and custom reports, BI dashboards, CCBHC compliance measures
- **Interoperability**: C-CDA transitions of care, FHIR APIs, immunization/syndromic surveillance reporting

The product is built on/derived from **OpenEMR** (the schema name is `openemr.openemr`, database is MariaDB 10.11.5). This means the export covers OpenEMR's broad data model plus EnSoftek's behavioral health extensions.

For the EHI export to be complete, it should cover: patient demographics, clinical notes/assessments, behavioral health instruments, medications, lab/procedure orders and results, billing and claims, insurance, scheduling, patient portal communications, documents, immunizations, therapy group data, and care/treatment plans.

## 2. Artifacts Reviewed

| Artifact | Size/Scope | Description | Informativeness |
|---|---|---|---|
| `downloads/drcloudehr.FHIR.xml` | 665 KB | SchemaSpy XML schema export — machine-readable schema for all 128 tables, 2,747 columns, types, remarks, and 314 foreign key relationships | **Most informative** — primary computable artifact |
| `downloads/index.html` | 118 KB | Main SchemaSpy page with export format description and table overview. Includes the ONC §170.315(b)(10) export description | **Most informative** — defines ZIP structure, CSV format, and export mechanics |
| `downloads/columns.html` | 1.1 MB | Complete column listing with embedded JSON (`tableData` array) for all 2,747 columns | High — used for cross-validation |
| `downloads/tables/*.html` | 128 files | Per-table documentation pages with column definitions, types, remarks, relationship diagrams | High — detailed per-table docs |
| `downloads/enrichment/schema.json` | ~500 KB | Pre-parsed JSON extraction from XML (128 tables, 2,747 columns) | High — used as cross-check |
| `downloads/enrichment/coverage-report.json` | 0.5 KB | Summary statistics from enrichment extraction | Medium — summary stats |
| `downloads/insertionOrder.txt` | 2 KB | Table insertion order (128 tables) for respecting FK constraints | Medium — confirms export is designed for reimport |
| `downloads/deletionOrder.txt` | 2 KB | Table deletion order (128 tables) | Medium |
| `downloads/relationships.html` | 9 KB | Relationship diagram page (links to SVGs) | Low — visual only |
| `downloads/diagrams/` | SVG files in summary/ and tables/ subdirs | Relationship diagrams (compact and large for summary; per-table) | Low — visual supplements |
| `downloads/anomalies.html` | 21 KB | SchemaSpy anomalies: 4 tables without indexes, tables with incrementing column names (denormalization signals) | Low |
| `downloads/constraints.html` | 11 KB | Database constraints listing | Low |
| `downloads/orphans.html` | 8 KB | Orphan tables page (no orphans listed) | Low |
| `downloads/routines.html` | 9 KB | Database routines (none) | Low |

## 3. Export Mechanics

**Format**: CSV files (one per table) packaged in ZIP files. Each ZIP file is structured as:
```
ehi-export-<UNIQUEID>.zip
  /images/             — Images used in data export (e.g., visual pain map forms)
  /documents/<pid>/    — Patient documents from the document management system
  README               — Links to the documentation site
  <table_name>.csv     — One CSV file per table with patient data
```

**Mechanism**: The export is generated from the EHR UI. The documentation on the index page describes it as a feature of DrCloudEHR itself.

**Single-patient vs bulk**: Both supported. A single-patient export produces a ZIP with one patient. Batch exports produce ZIPs with multiple patients. ZIP sizes are configurable, approximately 1 MB–4 GB.

**Self-contained**: Each ZIP is described as self-contained and importable into another EHR, with insertion/deletion ordering provided for database loading. Duplicate checking is needed for supporting entities (e.g., `insurance_companies`, `list_options`, `users`) when importing a full patient population.

**Access constraints/fees**: Not documented in the artifacts.

## 4. Export Content: What's In It

The export is a **native database model dump** of 128 MariaDB tables as CSV files. This is not a FHIR or C-CDA projection — it is the vendor's actual relational database schema, exported table-by-table.

### Data Dictionary Statistics

| Metric | Value |
|---|---|
| Tables | 128 |
| Total columns | 2,747 |
| Columns with descriptions | 1,134 (41.3%) |
| Columns without descriptions | 1,613 (58.7%) |
| Tables with table-level descriptions | 127 of 128 (99.2%) |
| Tables with 100% column descriptions | 37 |
| Tables with 0 column descriptions | 7 |
| Foreign key relationships | 314 (parent) + 314 (child) = 628 total |
| Data types documented | Yes, for all columns |
| Nullability documented | Yes, for all columns |
| Default values documented | Yes, for all columns |
| Value sets/code lists documented | No — coded fields reference `list_options` but actual values not enumerated |
| Sample data files | No |
| Machine-readable schema | Yes — `drcloudehr.FHIR.xml` (SchemaSpy XML) |

The one table without a table-level description is `form_track_anything_results` (7 columns).

### Vendor's own content organization

The vendor organizes content as database tables within a single schema. The tables group naturally by prefix and function. Below are the 20 largest tables (of 128 total):

| Entity/Table | Fields | Described | Types | Category |
|---|---|---|---|---|
| form_ros | 142 | 1 | yes | Review of Systems |
| form_sdoh | 135 | 4 | yes | Behavioral Health (SDOH) |
| patient_data | 126 | 92 | yes | Demographics |
| form_reviewofs | 115 | 1 | yes | Clinical Forms |
| history_data | 91 | 2 | yes | Demographics / History |
| form_bronchitis | 89 | 89 | yes | Clinical Forms |
| form_eye_neuro | 81 | 2 | yes | Eye Care |
| form_eye_refraction | 65 | 2 | yes | Eye Care |
| users | 62 | 62 | yes | Users / Providers |
| form_eye_mag_dispense | 55 | 1 | yes | Eye Care |
| prescriptions | 48 | 17 | yes | Medications |
| form_eye_mag_wearing | 41 | 1 | yes | Eye Care |
| form_eye_antseg | 39 | 1 | yes | Eye Care |
| openemr_postcalendar_events | 39 | 39 | yes | Scheduling |
| facility | 37 | 37 | yes | Facility |
| lists | 36 | 36 | yes | Problems/Allergies |
| form_eye_hpi | 35 | 2 | yes | Eye Care |
| insurance_data | 34 | 3 | yes | Insurance |
| documents | 33 | 33 | yes | Documents |
| form_encounter | 33 | 9 | yes | Encounters |

The complete inventory of all 128 tables is in `analysis/full-entity-inventory.json`.

### Category Breakdown

| Category | Tables | Columns | Described | Coverage % |
|---|---|---|---|---|
| Clinical Forms | 23 | 436 | 191 | 43.8% |
| Eye Care / Ophthalmology | 16 | 498 | 27 | 5.4% |
| Lab / Procedure Orders & Results | 8 | 134 | 122 | 91.0% |
| Billing / Revenue Cycle | 6 | 127 | 92 | 72.4% |
| Medications / Prescriptions | 6 | 111 | 50 | 45.0% |
| Reference / Configuration Data | 6 | 68 | 16 | 23.5% |
| Insurance / Coverage | 5 | 76 | 31 | 40.8% |
| Therapy Groups | 5 | 25 | 17 | 68.0% |
| Patient Portal / Messaging | 5 | 67 | 41 | 61.2% |
| Care Plans / Treatment Plans | 4 | 63 | 32 | 50.8% |
| Patient-Reported Outcomes | 4 | 65 | 46 | 70.8% |
| Demographics / Patient Data | 4 | 238 | 102 | 42.9% |
| Scheduling / Appointments | 4 | 75 | 75 | 100.0% |
| Documents / Attachments | 3 | 56 | 37 | 66.1% |
| Behavioral Health Assessments | 3 | 166 | 12 | 7.2% |
| Clinical Forms — Vitals/SOAP | 3 | 43 | 3 | 7.0% |
| Problems / Allergies / Conditions | 3 | 50 | 40 | 80.0% |
| Amendments | 2 | 15 | 15 | 100.0% |
| External / Imported Data | 2 | 16 | 3 | 18.8% |
| Encounters | 2 | 47 | 23 | 48.9% |
| Referrals / Transfers | 2 | 22 | 3 | 13.6% |
| Immunizations | 2 | 42 | 20 | 47.6% |
| Clinical Notes | 2 | 22 | 10 | 45.5% |
| E-Signatures | 1 | 9 | 9 | 100.0% |
| Facility | 1 | 37 | 37 | 100.0% |
| Clinical Forms — Dictation | 1 | 9 | 1 | 11.1% |
| Clinical Forms — Review of Systems | 1 | 142 | 1 | 0.7% |
| Patient Communications | 1 | 14 | 10 | 71.4% |
| Clinical Decision Support | 1 | 5 | 5 | 100.0% |
| Users / Providers | 1 | 62 | 62 | 100.0% |
| Logging / Audit | 1 | 7 | 1 | 14.3% |

### Notable patterns

**Well-documented categories**: Lab/Procedure (91.0%), Scheduling (100%), Billing (72.4%), Problems/Allergies (80.0%), and several small categories (Amendments, E-Signatures, Facility, Users) are fully documented with descriptions on all columns.

**Poorly-documented categories**: Eye Care (5.4% — 16 tables, 498 columns, only 27 with descriptions), Behavioral Health Assessments (7.2% — including the large `form_sdoh` with 135 columns but only 4 described), Clinical Forms — Vitals/SOAP (7.0%), and Review of Systems (0.7% — 142 columns, only 1 described). These are large tables where column names are semi-self-documenting (e.g., `weight_change`, `fever`, `night_sweats`) but lack formal descriptions.

**The `list_options` table** (15 columns, 5,636 rows, 0 descriptions) is a critical reference table used by many coded fields across the schema. Multiple columns in other tables reference `list_options.option_id` via foreign keys, but the actual option values are not enumerated anywhere in the documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers a broad swath of the DrCloudEHR data model, organized into these functional areas:

**Demographics & Patient History** (4 tables, 238 columns): The `patient_data` table alone has 126 columns covering name, DOB, address, language, race/ethnicity, insurance, emergency contacts, employer data, and more. `history_data` adds 91 columns of family/social/behavioral history. `patient_history` tracks changes.

**Clinical Forms** (23+ tables, 436+ columns): Includes SOAP notes (`form_soap`), clinical notes (`form_clinical_notes`, `form_clinic_note`), aftercare plans (`form_aftercare_plan`), review of systems (`form_ros` — 142 columns, `form_reviewofs` — 115 columns), physical exam, pain map, ankle injury, bronchitis, and various specialty forms. The CAMOS (Computer Assisted Medical Ordering System) module has 4 tables for categorized clinical content.

**Behavioral Health** (3 tables, 166 columns): PHQ-9 (`form_phq9`), GAD-7 (`form_gad7`), and SDOH screening (`form_sdoh` — 135 columns). These are the product's core behavioral health instruments. The GAD-7 and PHQ-9 tables exist but `form_gad7` has 0 sample rows.

**Patient-Reported Outcomes** (4 tables, 65 columns): `questionnaire_response`, `questionnaire_repository`, `pro_assessments`, `form_questionnaire_assessments` — supporting PROMIS and custom questionnaires.

**Medications & Prescriptions** (6 tables, 111 columns): `prescriptions` (48 columns with drug, dosage, frequency, route, refills, e-prescribing status), `drugs`, `drug_sales`, `lists_medication`, `medex_recalls`, `pharmacies`.

**Lab / Procedure Orders & Results** (8 tables, 134 columns — 91% described): Full lifecycle coverage: `procedure_order` → `procedure_order_code` → `procedure_report` → `procedure_result`. Plus `procedure_type`, `procedure_providers`, `procedure_questions`, `procedure_answers`. This is one of the best-documented categories.

**Billing & Revenue Cycle** (6 tables, 127 columns — 72.4% described): `billing` (30 columns — all described), `claims` (13 columns), `ar_activity` (22 columns — accounts receivable), `ar_session` (17 columns), `voids`, `form_misc_billing_options`. Genuine billing data, not just clinical summaries.

**Insurance / Coverage** (5 tables, 76 columns): `insurance_data` (34 columns), `insurance_companies`, `insurance_type_codes`, `benefit_eligibility` (18 columns — fully described), `eligibility_verification`.

**Documents & Attachments** (3 tables, 56 columns): `documents` (33 columns — all described) plus actual patient documents exported to `/documents/<pid>/` directories in the ZIP. `document_templates` is a supporting table.

**Patient Portal / Messaging** (5 tables, 67 columns): `onsite_documents`, `onsite_mail` (22 columns — fully described), `onsite_messages`, `onsite_portal_activity`, `onsite_signatures`.

**Therapy Groups** (5 tables, 25 columns): `therapy_groups`, `therapy_groups_counselors`, `therapy_groups_participants`, `therapy_groups_participant_attendance`, `groups`. Supports group therapy session tracking relevant to behavioral health.

**Scheduling / Appointments** (4 tables, 75 columns — 100% described): `openemr_postcalendar_events` (39 columns), `openemr_postcalendar_categories`, `patient_tracker`, `patient_tracker_element`.

**Eye Care / Ophthalmology** (16 tables, 498 columns): Comprehensive ophthalmology coverage inherited from OpenEMR: acuity, anterior/posterior segment, refraction, neuro, biometrics, HPI, vitals, prescriptions, orders, dispensing. Very thin on descriptions (5.4%).

**Problems / Allergies / Conditions** (3 tables, 50 columns — 80% described): The `lists` table (36 columns, all described) is a type-discriminated table handling allergies, medical problems, medications, medical devices, surgeries, and dental issues.

**Care Plans / Treatment Plans** (4 tables, 63 columns): `form_care_plan`, `form_treatment_plan`, `clinical_plans`, `form_aftercare_plan` (18 columns — all described).

**Extensibility** (via Reference/Configuration): `lbf_data`, `lbt_data`, `layout_options`, `layout_group_properties`, `shared_attributes` — the Layout-Based Forms (LBF) mechanism allows custom data fields, and their values are included in the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient_data` (126 fields), `patient_history`, `history_data` (91 fields) — name, DOB, address, language, race/ethnicity, contacts, employer | Thorough — 238 total columns |
| Encounters / visits | ✅ Covered | `form_encounter` (33 fields), `forms` (14 fields — form registry linking encounters to form types) | Solid encounter tracking |
| Problems / conditions / diagnoses | ✅ Covered | `lists` (36 fields, type-discriminated for problems, diagnoses), `issue_types`, `issue_encounter` | Well-documented |
| Medications / prescriptions | ✅ Covered | `prescriptions` (48 fields), `drugs` (22 fields), `drug_sales`, `lists_medication`, `medex_recalls`, `pharmacies` | Full medication lifecycle |
| Allergies | ✅ Covered | `lists` table with `type='allergy'` discrimination | Documented via `lists` |
| Immunizations | ✅ Covered | `immunizations` (30 fields, 13,694 sample rows), `immunization_observation` | Good — includes observations |
| Vitals | ✅ Covered | `form_vitals` (28 fields, 906 sample rows), `form_vital_details`, `form_eye_vitals` | Present |
| Lab results | ✅ Covered | `procedure_order` (31 fields), `procedure_order_code`, `procedure_report`, `procedure_result` (261,850 sample rows) | Excellent — full lifecycle, 91% column descriptions |
| Imaging / diagnostic reports | ⚠️ Partial | Labs and procedures are in the same `procedure_*` tables; no separate imaging-specific entities | Procedure framework covers imaging orders but product doesn't emphasize imaging storage |
| Procedures | ✅ Covered | `procedure_type` (20 fields), `procedure_order`, `procedure_result`, `external_procedures` (88,896 sample rows) | Thorough |
| Clinical notes / documents | ✅ Covered | `pnotes` (16 fields), `notes`, `form_clinical_notes`, `form_clinic_note`, `form_dictation`, `form_soap`, plus `documents` table and `/documents/<pid>/` file export | Multiple note types plus document files |
| Care plans / goals | ✅ Covered | `form_care_plan`, `form_treatment_plan`, `clinical_plans`, `form_aftercare_plan` (18 fields, fully described) | 4 tables, 63 columns |
| Orders / referrals | ✅ Covered | `procedure_order` (31 fields), `transactions` (referrals), `form_prior_auth`, `form_transfer_summary` | Orders and referral tracking |
| Insurance / coverage | ✅ Covered | `insurance_data` (34 fields), `insurance_companies`, `benefit_eligibility` (18 fields), `eligibility_verification` | 5 tables, 76 columns |
| Claims / billing | ✅ Covered | `billing` (30 fields, all described), `claims` (13 fields), `ar_activity` (22 fields), `ar_session`, `voids`, `form_misc_billing_options` | Genuine billing data — 6 tables, 127 columns |
| Payments | ✅ Covered | `ar_activity` tracks payment activity, `ar_session` tracks payment sessions | Part of billing/AR tables |
| Consents / directives | ⚠️ Partial | `onsite_signatures` captures e-signatures; `form_care_plan` may include advance directives. No dedicated consent table | Consent data may be in documents or forms |
| Patient communications / portal messages | ✅ Covered | `onsite_mail` (22 fields), `onsite_messages` (7 fields), `onsite_portal_activity`, `patient_reminders` | Portal messaging well-covered |
| Specialty — Behavioral health assessments | ✅ Covered | `form_phq9`, `form_gad7`, `form_sdoh` (135 fields), `pro_assessments`, `questionnaire_response` | Core specialty instruments present |
| Specialty — Therapy groups | ✅ Covered | `therapy_groups`, `therapy_groups_participants`, `therapy_groups_participant_attendance`, `therapy_groups_counselors` | Group therapy tracking included |
| Specialty — Eye care | ✅ Covered | 16 `form_eye_*` tables (498 columns) | Comprehensive ophthalmology (from OpenEMR) |
| Specialty — Custom/extensible data | ✅ Covered | `lbf_data`, `lbt_data`, `layout_options` — Layout-Based Forms extensibility | Custom form data included |

**Gap Analysis Summary**: The export covers **19 of 19 applicable standard domains** (counting 2 as partial). The only partial areas are: (1) imaging/diagnostic reports — handled through the generic procedure framework rather than dedicated imaging tables, which is appropriate given the product's behavioral health focus; (2) consents/directives — no dedicated consent entity, though e-signatures and documents may contain this data.

**Notable absence**: The product advertises AI Group Scribing (speaker diarization, sentiment analysis, per-speaker summaries) and eMAR functionality. Neither has a dedicated table in the export. AI-generated content may be stored in the `documents` table or via the LBF extensibility mechanism, and eMAR data may be captured through `drug_sales` or forms. However, these cannot be confirmed from the documentation alone.

## 6. Documentation Quality

### Strengths

- **Machine-readable schema**: The `drcloudehr.FHIR.xml` (SchemaSpy XML) is a complete, parseable artifact containing all 128 tables, all 2,747 columns, data types, nullability, defaults, and 314 foreign key relationships. This is rare and valuable.
- **100% table-level documentation**: 127 of 128 tables have descriptions explaining their purpose. The descriptions explicitly state the CSV filename pattern: "the file for this export will be found in the extracted zip folder location under the filename of `<table_name>.csv`."
- **Navigable web documentation**: The SchemaSpy-generated site has table-by-table pages, column listings, and SVG relationship diagrams. Per-table pages show parent/child relationships visually.
- **Insertion/deletion ordering**: `insertionOrder.txt` and `deletionOrder.txt` specify the order for loading/purging data respecting FK constraints — practical detail showing the export is designed for reimport.
- **Well-described core tables**: 37 tables have 100% column descriptions, including critical tables like `billing`, `lists`, `documents`, `users`, `facility`, and `openemr_postcalendar_events`.

### Weaknesses

- **58.7% of columns lack descriptions**: 1,613 of 2,747 columns have no remarks beyond their name and type. The largest underdocumented tables are `form_ros` (142 columns, 1 described), `form_sdoh` (135 columns, 4 described), `form_reviewofs` (115 columns, 1 described), and `history_data` (91 columns, 2 described).
- **No value set documentation**: Coded fields reference `list_options.list_id` values (e.g., `amendment_from`, `amendment_status`, `issue_subtypes`) but the actual option values are not enumerated anywhere. The `list_options` table itself has 5,636 rows and 0 column descriptions.
- **No sample data**: No example CSV files or sample ZIP exports are provided. A developer would need to request an actual export to understand data encoding (date formats, null representation, boolean encoding, etc.).
- **No data encoding guide**: The documentation doesn't specify how dates are formatted in CSV, how binary fields (UUIDs stored as BINARY(16)) are represented, how null values appear, or how multi-line text fields are escaped.
- **Eye Care documentation is very thin**: 16 tables with 498 columns but only 27 descriptions (5.4%). Column names like `ODSPH`, `ODCYL`, `ODAXIS` are domain-specific abbreviations that require ophthalmology knowledge to interpret.

### Could a developer build an import?

**Partially.** The schema structure, data types, and foreign key relationships are well-documented enough to build a database schema and load CSV files. However:
- A developer would struggle with undescribed columns (59% of all columns)
- Coded values from `list_options` would be opaque without the actual reference data (though the export includes the `list_options` table itself in the ZIP, so importers would have the values)
- Data encoding conventions for CSV files are unspecified
- Many behavioral health-specific fields (especially in `form_sdoh` and `form_ros`) require clinical domain knowledge to interpret

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native database model export covering 128 tables and 2,747 columns across clinical, billing, insurance, scheduling, portal, and specialty behavioral health domains. It is not a C-CDA or FHIR projection — it exports the vendor's actual MariaDB/OpenEMR-derived relational schema as CSV files in self-contained ZIP archives. The breadth of coverage (19 of 19 applicable domains) and the inclusion of billing, insurance, therapy groups, and extensible custom form data demonstrate this is a real EHI export, not a compliance stub.

### Key Findings

1. **Genuine full-database export**: 128 tables exported as CSV in ZIP files, covering the complete OpenEMR-derived data model. Billing, insurance, claims, and AR data are included with dedicated tables — this is not just clinical summaries repackaged. (`billing`, `claims`, `ar_activity`, `ar_session`, `voids` — 127 columns total for billing/RCM)

2. **Machine-readable schema is a standout**: The `drcloudehr.FHIR.xml` SchemaSpy export provides a complete, parseable schema with types, relationships, and remarks — a level of machine-readability rare among EHI export documentation. (`drcloudehr.FHIR.xml`, 665 KB, 128 tables, 2,747 columns, 314 FK relationships)

3. **Column-level descriptions cover only 41.3%**: While every table has a description, only 1,134 of 2,747 columns have remarks. The largest undocumented tables — `form_ros` (142 cols, 1 described), `form_sdoh` (135 cols, 4 described), `history_data` (91 cols, 2 described) — are clinically important. Column names are often semi-self-documenting but this is a real documentation gap.

4. **Behavioral health specialty data is present but thinly documented**: The product's core differentiator — behavioral health instruments (PHQ-9, GAD-7, SDOH) — has dedicated tables but very low description coverage (7.2% for behavioral health assessments). The `form_sdoh` table has 135 columns (one of the largest tables) with only 4 described.

5. **Value sets are undocumented**: The `list_options` reference table (5,636 rows) is used by coded fields throughout the schema but has 0 column descriptions, and the actual option values/labels are not enumerated in the documentation. However, the `list_options` table data is included in the export itself, which partially mitigates this gap.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV files in ZIP archives
Model type:      Native database (MariaDB/OpenEMR-derived)
Entities:        128 tables
Fields:          2,747 columns
Descriptions:    41.3% of fields (1,134/2,747)
Sample data:     No (row counts in schema suggest production data: 888 patients, 261K procedure results)
Bulk export:     Yes (configurable batch sizes, 1 MB–4 GB ZIPs)
Domains covered: 19 of 19 applicable domains (2 partial)
```

### Bottom Line

DrCloudEHR's EHI export is a **genuinely comprehensive native database dump** that covers all major data domains a patient or provider would need, including behavioral health assessments, billing, insurance, therapy groups, and patient portal data. The machine-readable SchemaSpy documentation with foreign key relationships and insertion ordering is above-average for the industry. The main weakness is that 59% of columns lack descriptions — particularly in the large clinical forms and behavioral health assessment tables that are the product's specialty — and value sets are not enumerated in the documentation (though they are included in the export data itself). A patient would get a usable, complete copy of their data; a developer importing it would have solid structural documentation but would need domain expertise to interpret many undescribed fields.
