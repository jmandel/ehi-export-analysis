# EHI Export Analysis: OpenEMR Foundation

**Product**: OpenEMR (versions 7.0 and 8)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3115.OPEN.01.00.1.220708 (v7.0), 15.05.05.3115.OPEN.02.01.1.260130 (v8)

## 1. Product Context

OpenEMR is the most popular open-source EHR and practice management system worldwide, used at an estimated 20,000+ healthcare facilities across 184 countries. In the US, approximately 5,000+ installations serve 30+ million patients. It primarily targets small to mid-size ambulatory practices, community health centers, and clinics.

OpenEMR is a **full-featured ambulatory EHR and practice management system** — not just a clinical charting tool. Its data footprint includes:

- **Clinical**: Patient demographics, encounters, SOAP notes, problem lists, medications, allergies, immunizations, vitals, lab orders/results, procedures, clinical notes, care plans, referrals, clinical decision support rules
- **Billing & Practice Management**: CPT/HCPCS/ICD coding, CMS-1500 and UB-04 billing, electronic claims, insurance tracking, accounts receivable, ERA/835 posting, eligibility verification, payments
- **Specialty Modules**: Ophthalmology/optometry (17 dedicated form tables), behavioral health (group therapy), SDOH assessments, bronchitis/ankle injury specialty forms
- **Patient Portal**: Secure messaging, online payments, document exchange, appointment scheduling, self-registration
- **Prescriptions/Pharmacy**: e-Prescribing, in-house pharmacy dispensing, drug inventory
- **Documents**: Electronic document management with categories, e-signatures
- **Scheduling**: Appointment calendar, patient flow tracking, recalls/reminders
- **Messaging**: Internal staff messaging (pnotes), patient notifications, direct secure messaging
- **Custom Forms**: Layout-based forms (LBF) system for unlimited custom form creation
- **Telehealth**: Video conferencing integration (Comlink)

This breadth establishes the baseline: a genuine (b)(10) export should cover clinical data, billing/financial, specialty forms, documents, communications, prescriptions, and custom form data — not just the USCDI clinical subset.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `wiki-page-b10.html` (25 KB) | MediaWiki page documenting the EHI export feature — setup instructions, single-patient and population export workflows with screenshots | **High** — primary source for export mechanics |
| `openemr.openemr.xml` (1.0 MB) | SchemaSpy XML schema — machine-readable data dictionary with all 322 tables, 4,941 columns, types, relationships, remarks | **Critical** — authoritative data dictionary |
| `ehi-export-docs-v7.html` (251 KB) | SchemaSpy index page — rendered table listing (JavaScript-rendered via DataTables) | **Medium** — confirms table inventory |
| `columns.html` (1.7 MB) | SchemaSpy all-columns page | **Low** — JS-rendered, XML is more useful |
| `tables/*.html` (318 files, 9.3 MB total) | Individual SchemaSpy table documentation pages | **Medium** — one per table, JS-rendered |
| `relationships.html` (9.5 KB) | SchemaSpy relationships diagram page | **Low** — client-side rendered |
| `insertionOrder.txt` (5.5 KB) | Table dependency/load order (322 tables) | **Medium** — confirms FK dependencies |
| `deletionOrder.txt` (5.5 KB) | Reverse dependency order | **Low** — mirror of insertion order |
| `SinglePatient_EHI_Export.png` (99 KB) | Screenshot of single-patient export UI | **Medium** — confirms UI export mechanism |
| `TotalPatient_EHI_Export.png` (99 KB) | Screenshot of population export UI | **Medium** — confirms bulk export capability |
| `EHI-Export-Task-Completed.png` (47 KB) | Screenshot of completed export with download link | **Low** — confirms download/hash verification |
| `enrichment/schema.json` (2.2 MB) | Parsed JSON from XML — all tables, columns, FK relationships | **Critical** — used as primary data source for analysis |
| `enrichment/html-comments.json` (878 KB) | Column metadata extracted from HTML table pages | **Low** — contains mostly default values and index info, not semantic descriptions |

The XML schema (`openemr.openemr.xml`) and its parsed JSON representation (`enrichment/schema.json`) are the most informative artifacts. The wiki page provides essential context on export mechanics.

## 3. Export Mechanics

- **Format**: ZIP files containing CSV files (one per database table) plus patient documents and images
- **Mechanism**: Purpose-built admin module (Modules → Manage Modules → Electronic Health Information Exporter). Accessed via Miscellaneous → Electronic Health Information Export menu.
- **Single-patient**: Enter patient PID, export generates one ZIP file
- **Bulk/population**: Leave PID blank, configure ZIP file size limit (1–4,000 MB), system batches patients across multiple ZIP files based on document storage size + ~100KB per patient for database data
- **Access constraints**: Administrator role only (admin/super ACL required)
- **Fees**: None (open-source; export is a built-in module)
- **Document inclusion**: Optional checkbox to include/exclude patient document files from storage
- **Integrity verification**: Hash value provided for each ZIP file
- **Self-contained**: Each ZIP includes supporting entity data (users, facilities, insurance companies, pharmacies) for independent import capability
- **README**: Each ZIP includes a README linking back to the public SchemaSpy documentation

## 4. Export Content: What's In It

### Data Dictionary Overview

The export is documented via a **SchemaSpy 6.2.4** site generated against a MariaDB 11.4.9 database. The authoritative machine-readable artifact is the XML schema file (`openemr.openemr.xml`).

**Key statistics** (verified from `entity-inventory-full.json`):
- **322 tables** in the `openemr` database schema
- **4,941 columns** total across all tables
- **4,001 columns (81.0%) have explicit data types** (VARCHAR, INT, BIGINT, TEXT, DATETIME, etc.)
- **1,521 columns (30.8%) have semantic descriptions** (XML remarks explaining the column's purpose)
- **141 tables (43.8%) have table-level descriptions** explaining what the table stores
- **446 foreign key relationships** explicitly defined, linking tables together
- **Types distribution**: VARCHAR (1,779), INT (442), BIGINT (393), TEXT (372), DATETIME (238), BOOLEAN (152), TINYINT (126), DATE (84), LONGTEXT (75), plus others

### Vendor's Own Content Organization

The data dictionary presents the raw database schema without vendor-imposed categories. Tables are named descriptively (e.g., `billing`, `patient_data`, `form_vitals`). I categorized them by name patterns and domain alignment. Full inventory is in `analysis/entity-inventory-full.json`.

**Category breakdown** (27 categories, 322 tables, 4,941 fields):

| Category | Tables | Fields | % Described | Key Tables |
|---|---|---|---|---|
| Clinical Forms | 44 | 931 | 34.9% | `forms`, `form_vitals`, `form_soap`, `form_ros` (143 fields), `form_reviewofs` (116 fields), `form_bronchitis` (89 fields), `form_history_sdoh` (56 fields) |
| Ophthalmology (Specialty) | 17 | 566 | 4.8% | `form_eye_neuro` (84), `form_eye_refraction` (68), `form_eye_mag_dispense` (59), `form_eye_vitals` (52), `form_eye_base` (50) |
| Patient Demographics & Contacts | 23 | 491 | 38.3% | `patient_data` (137), `history_data` (94), `employer_data`, `addresses`, `contact`, `phone_numbers` |
| System & Configuration | 50 | 455 | 14.9% | `globals`, `registry`, `background_services`, `modules`, `uuid_registry` |
| Billing & Insurance | 23 | 368 | 37.5% | `billing`, `claims`, `ar_activity`, `ar_session`, `insurance_data`, `insurance_companies`, `codes`, `fee_sheet_options`, `x12_partners` |
| Reference & Terminology | 24 | 233 | 8.6% | `icd10_dx_order_code`, `sct2_concept`, `sct2_description`, `valueset`, `code_types` |
| Procedures & Labs | 11 | 224 | 67.4% | `procedure_order`, `procedure_report`, `procedure_result`, `procedure_type`, `procedure_questions` |
| Documents & Signatures | 13 | 202 | 32.7% | `documents`, `document_templates`, `onsite_documents`, `esign_signatures`, `categories` |
| Medications & Pharmacy | 11 | 202 | 28.2% | `prescriptions`, `drugs`, `drug_inventory`, `drug_sales`, `drug_templates`, `erx_drug_paid` |
| Users & Facilities | 10 | 184 | 58.7% | `users` (70 fields), `facility`, `users_facility`, `pharmacies` |
| Messaging & Communications | 13 | 162 | 26.5% | `pnotes`, `onsite_mail`, `onsite_messages`, `notifications`, `dated_reminders`, `direct_message_log` |
| Access Control | 24 | 142 | 0.0% | `gacl_acl`, `gacl_aco`, `gacl_aro`, `gacl_axo` (24 phpGACL tables) |
| Clinical Decision Support | 10 | 105 | 68.6% | `clinical_rules`, `clinical_plans`, `rule_action`, `rule_filter`, `rule_target` |
| Clinical Lists & Issues | 5 | 90 | 50.0% | `lists` (problems/allergies/medications), `list_options`, `issue_encounter`, `issue_types` |
| Scheduling | 4 | 90 | 64.4% | `openemr_postcalendar_events`, `openemr_postcalendar_categories`, `calendar_external` |
| FHIR & Questionnaires | 5 | 80 | 43.8% | `questionnaire_repository`, `questionnaire_response`, `api_token`, `fhir_value_set_system` |
| Patient Preferences & PROs | 4 | 61 | 21.3% | `pro_assessments`, `patient_care_experience_preferences`, `preference_value_sets` |
| Layout-Based Forms | 4 | 56 | 19.6% | `lbf_data`, `lbt_data`, `layout_options`, `layout_group_properties` |
| Audit & Logging | 5 | 53 | 20.8% | `log`, `audit_master`, `audit_details`, `extended_log` |
| C-CDA & Interoperability | 5 | 47 | 6.4% | `ccda`, `ccda_components`, `ccda_sections`, `ccda_field_mapping` |
| Immunizations | 2 | 47 | 44.7% | `immunizations`, `immunization_observation` |
| EHI Export Infrastructure | 5 | 46 | 17.4% | `ehi_export_job`, `ehi_export_job_tasks`, `ehi_export_job_patients` |
| Care Teams | 3 | 42 | 28.6% | `care_team`, `care_team_member`, `care_teams` |
| Telehealth | 3 | 31 | 80.6% | `comlink_telehealth_appointment_session`, `comlink_telehealth_auth` |
| Amendments | 2 | 18 | 83.3% | `amendments`, `amendments_history` |
| Transactions & Referrals | 1 | 9 | 11.1% | `transactions` |
| Public Health Reporting | 1 | 6 | 0.0% | `syndromic_surveillance` |

### Notable Large Tables

| Table | Fields | Category | Description |
|---|---|---|---|
| `form_ros` | 143 | Clinical Forms | Review of systems — comprehensive system-by-system clinical review |
| `patient_data` | 137 | Demographics | Core patient record — demographics, contact info, insurance references, preferences |
| `form_reviewofs` | 116 | Clinical Forms | Review of systems (alternate format) |
| `history_data` | 94 | Demographics | Patient medical/social/family history, SDOH data |
| `form_bronchitis` | 89 | Clinical Forms | Specialty bronchitis assessment form |
| `form_eye_neuro` | 84 | Ophthalmology | Neuro-ophthalmic exam findings |
| `users` | 70 | Users & Facilities | Provider/staff records — credentials, roles, NPI, DEA numbers |
| `form_eye_refraction` | 68 | Ophthalmology | Refraction measurements and prescriptions |
| `form_eye_mag_dispense` | 59 | Ophthalmology | Optical dispensing records |
| `form_history_sdoh` | 56 | Clinical Forms | Social determinants of health assessment |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

OpenEMR's export is a **complete database dump** — it exports all 322 tables from the entire MariaDB schema, not a curated subset. This means:

**Richest areas** (by table count and field depth):
- **Clinical Forms** (44 tables, 931 fields): The product's extensive clinical documentation system, including SOAP notes, review of systems (143 fields), vitals, care plans, treatment plans, transfer summaries, functional/cognitive status assessments, GAD-7, PHQ-9, SDOH assessments, pain maps, and more.
- **Ophthalmology Specialty** (17 tables, 566 fields): A genuinely deep specialty module — neuro exam (84 fields), refraction (68 fields), dispensing (59 fields), vitals (52 fields), external exam (50 fields). This is rare to see in EHI exports.
- **Patient Demographics** (23 tables, 491 fields): Comprehensive patient record including the massive `patient_data` table (137 fields) and `history_data` (94 fields), plus addresses, contacts, employer data.
- **Billing & Insurance** (23 tables, 368 fields): Full billing chain — billing codes, claims, A/R activity, A/R sessions, insurance data, insurance companies, eligibility verification, fee schedules, payment processing, X12 partner configuration.

**Genuinely notable inclusions** (often missing from other vendors):
- `amendments` and `amendments_history` — patient-initiated amendment requests with full history
- `pnotes`, `onsite_mail`, `onsite_messages` — internal messaging and portal communications
- `pro_assessments` — patient-reported outcome assessments
- `lbf_data` and `lbt_data` — custom layout-based form data (captures any custom forms created by the practice)
- `drug_inventory`, `drug_sales` — in-house pharmacy dispensing records
- `comlink_telehealth_*` — telehealth session records
- `syndromic_surveillance` — public health reporting data
- `esign_signatures`, `onsite_signatures` — electronic signature records

**Thinnest areas**:
- `transactions` (1 table, 9 fields) — referrals/transactions are structurally thin
- Ophthalmology tables have only 4.8% description coverage despite being field-rich
- Access control tables (24 phpGACL tables) are included but not clinically relevant

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient_data` (137 fields), `history_data` (94 fields), `employer_data`, `addresses`, `contact`, `phone_numbers` — 23 tables, 491 fields total | Exceptionally thorough — 137 fields in the core patient table alone |
| Encounters / visits | ✅ Covered | `form_encounter`, `forms` (form registry), 44 clinical form tables, `enc_category_map` | Deep — encounters link to 44+ form types |
| Problems / conditions / diagnoses | ✅ Covered | `lists` table (used for problems, allergies, medications), `issue_encounter`, `issue_types`, `codes`, ICD-10 reference tables | Well-covered via the multi-purpose `lists` table |
| Medications / prescriptions | ✅ Covered | `prescriptions`, `drugs`, `drug_inventory`, `drug_sales`, `drug_templates`, `erx_*` (5 e-prescribing tables), `lists_medication` — 11 tables, 202 fields | Includes both prescribing and in-house pharmacy dispensing |
| Allergies | ✅ Covered | `lists` table (type='allergy'), `list_options` for coded values | Stored alongside problems in the `lists` table |
| Immunizations | ✅ Covered | `immunizations`, `immunization_observation` — 2 tables, 47 fields | Includes observations/component data |
| Vitals | ✅ Covered | `form_vitals` — vital sign measurements per encounter | Standard form table |
| Lab results | ✅ Covered | `procedure_order`, `procedure_report`, `procedure_result`, `procedure_type`, `procedure_questions`, `procedure_answers`, `procedure_specimen` — 11 tables, 224 fields | Full order-report-result chain with 67.4% description coverage |
| Imaging / diagnostic reports | ⚠️ Partial | `procedure_*` tables cover all ordered tests; DICOM viewer integration exists but image storage details unclear from schema alone | Product has DICOM viewer; procedure tables cover orders/reports but DICOM image blobs may be external |
| Procedures | ✅ Covered | `procedure_order`, `procedure_type`, `billing` (procedure codes) | Covered across procedure and billing tables |
| Clinical notes / documents | ✅ Covered | `documents`, `document_templates`, `onsite_documents`, `form_CAMOS`, `form_soap`, plus 40+ clinical form tables | Extensive — both structured forms and unstructured documents |
| Care plans / goals | ✅ Covered | `form_care_plan`, `form_treatment_plan`, `form_aftercare_plan`, clinical rules/plans tables | Multiple plan types supported |
| Orders / referrals | ✅ Covered | `procedure_order`, `transactions` (referrals), `form_misc_billing_options` | Orders well-covered; referrals are thin (9 fields) |
| Insurance / coverage | ✅ Covered | `insurance_data`, `insurance_companies`, `insurance_numbers`, `benefit_eligibility` — part of 23 billing tables | Multiple insurance plans per patient supported |
| Claims / billing | ✅ Covered | `billing`, `claims`, `ar_activity`, `ar_session`, `codes`, `fee_sheet_options`, `fee_schedule`, `edi_sequences`, `x12_partners` | Full billing chain from charge capture to claims submission to A/R |
| Payments | ✅ Covered | `payments`, `payment_gateway_details`, `payment_processing_audit`, `ar_session` | Includes payment processing audit trail |
| Consents / directives | ⚠️ Partial | `onsite_documents` (patient portal document signing), `esign_signatures`, `onsite_signatures` | E-signatures and portal documents are included; no dedicated consent/advance directive table but may be captured as documents |
| Patient communications / portal messages | ✅ Covered | `pnotes` (staff-to-staff notes about patients), `onsite_mail`, `onsite_messages`, `onsite_portal_activity`, `direct_message_log`, `notifications` — 13 tables | Comprehensive — covers portal messaging, internal notes, direct messaging, notifications |
| Specialty-specific (Ophthalmology) | ✅ Covered | 17 `form_eye_*` tables with 566 fields covering neuro exam, refraction, vitals, external exam, biometrics, dispensing | Exceptionally deep specialty coverage — rare among EHI exports |
| Specialty-specific (Behavioral Health) | ✅ Covered | `form_gad7`, `form_phq9`, `therapy_groups`, `therapy_groups_counselors`, `therapy_groups_participants`, `therapy_groups_participant_attendance` | GAD-7, PHQ-9 assessments plus group therapy tracking |
| Specialty-specific (SDOH) | ✅ Covered | `form_history_sdoh` (56 fields) | Dedicated SDOH assessment form |

**Gap Analysis Summary**: Of 19 applicable domains, **17 are fully covered**, **2 are partially covered** (imaging and consents). No domains are absent. The partial gaps are minor:
- **Imaging**: The product has a DICOM viewer, but DICOM image files may be stored externally to the database. The procedure tables cover imaging orders and reports.
- **Consents**: Consent documents likely exist as uploaded documents in the `documents` table or portal-signed documents in `onsite_documents`, but there's no dedicated consent tracking table.

## 6. Documentation Quality

**Overall: Very Good**

**Strengths**:
- **Machine-readable schema**: The SchemaSpy XML file is the gold standard for computable data dictionaries — every table, column, type, nullability, default value, and foreign key relationship is machine-parseable
- **Table-level descriptions**: 141 of 322 tables (43.8%) have remarks explaining their purpose (e.g., `billing`: "Patient billing records for billing codes - Used for Claims Processing")
- **Column-level descriptions**: 1,521 of 4,941 columns (30.8%) have semantic descriptions explaining what the field means (e.g., `amendments.amendment_by`: "Comes from the list_options.list_id='amendment_from' and represents who is requesting the amendment")
- **Relationship documentation**: 446 foreign key relationships are explicitly defined, enabling reconstruction of the data model
- **Clear export instructions**: Step-by-step guide with screenshots for both single-patient and population exports
- **Redundant hosting**: Primary and backup documentation URLs
- **Self-describing exports**: Each ZIP includes a README linking to the documentation

**Weaknesses**:
- **69.2% of columns lack descriptions**: While types and relationships are complete, most columns rely on naming conventions for semantics (e.g., `pid`, `encounter`, `authorized`)
- **Ophthalmology tables are poorly described**: Only 4.8% of the 566 ophthalmology fields have descriptions — the most field-rich specialty module has the least documentation
- **No value sets documented**: While some column remarks reference `list_options` entries, the actual coded value sets are not enumerated in the documentation
- **No sample data provided**: The documentation is schema-only — no example CSV files showing what exported data looks like
- **HTML pages are JavaScript-rendered**: The individual table HTML pages require a browser to render, limiting offline usability (the XML compensates for this)

**Could a developer build an import?** Yes — the combination of CSV format, SchemaSpy XML schema (types, relationships, foreign keys), and insertion order file provides sufficient information to load the data into a relational database and reconstruct the data model. The main challenge would be understanding the semantics of undescribed columns, which are generally self-explanatory from naming conventions (e.g., `date`, `pid`, `encounter`, `provider_id`).

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

OpenEMR's EHI export covers the **full database schema** — all 322 tables, including clinical forms (44 tables), billing and insurance (23 tables), specialty ophthalmology data (17 tables), medications and pharmacy (11 tables), patient communications (13 tables), documents (13 tables), and more. This goes far beyond USCDI: it includes billing records, claims, A/R activity, payment processing, in-house pharmacy dispensing, custom layout-based forms, telehealth sessions, patient-reported outcomes, amendments, and electronic signatures. For an ambulatory EHR/practice management system, this export demonstrably covers every data domain the product stores. The only potential gaps (DICOM images, advance directives) are minor and likely covered by the document storage export.

**Axis 2 — Export approach: Purpose-built EHI export**

This is unambiguously a purpose-built (b)(10) export. OpenEMR built a dedicated export module (`Electronic Health Information Exporter`) that dumps the entire patient-facing database as CSV files with a complete SchemaSpy data dictionary. This is **not** a C-CDA repackaging and **not** a FHIR (g)(10) relabeling. The telltale signs of a genuine export are all present: native database format (CSV of MariaDB tables), product-specific data dictionary (SchemaSpy XML with 322 tables and 4,941 columns), coverage of billing and operational data beyond USCDI, inclusion of specialty-specific tables (ophthalmology, behavioral health), and a purpose-built UI for single-patient and population export with batch processing. The export infrastructure itself has 5 dedicated tables (`ehi_export_job*`) managing export jobs and tasks.

### Key Findings

1. **Most thorough EHI export observed**: 322 tables, 4,941 columns exported as CSV with full schema documentation. This is a direct database dump covering every data domain — clinical, billing, specialty, communications, documents, and custom forms.

2. **Genuine billing and financial coverage**: 23 billing/insurance tables with 368 fields covering the full billing chain from charge capture (`billing`) through claims submission (`claims`) to accounts receivable (`ar_activity`, `ar_session`) and payment processing (`payments`, `payment_gateway_details`).

3. **Exceptional specialty data depth**: The ophthalmology module alone has 17 tables and 566 fields — more specialty data than many vendors export in their entire (b)(10) implementation. Behavioral health (GAD-7, PHQ-9, group therapy) and SDOH assessments are also included.

4. **Description coverage is uneven**: While 43.8% of tables have descriptions, only 30.8% of columns do. The most field-rich specialty module (ophthalmology, 566 fields) has only 4.8% description coverage. Column semantics are generally inferrable from naming conventions, but formal documentation would strengthen the data dictionary.

5. **Both single-patient and bulk export supported**: The export module handles individual patient export (by PID) and full population export with configurable batch sizes and ZIP splitting — a practical implementation for both patient access requests and organizational data portability.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (ZIP archive with per-table CSV files + patient documents)
Entities:        322
Fields:          4,941
Descriptions:    30.8% of fields (1,521 of 4,941); 43.8% of tables (141 of 322)
Sample data:     No
Bulk export:     Yes (population export with batch processing)
Domains covered: 17 of 19 fully covered, 2 of 19 partially covered
```

### Bottom Line

OpenEMR's EHI export is one of the strongest (b)(10) implementations available. A patient or provider would receive a complete copy of their data — every clinical form, billing record, prescription, lab result, document, and specialty assessment the system stores — in a universally readable CSV format with a machine-parseable schema. The single biggest strength is the export's comprehensiveness: by dumping the entire database schema rather than curating a subset, OpenEMR avoids the selective omissions that plague most vendor implementations. The main improvement opportunity is increasing column-level description coverage from 30.8% to provide richer documentation for data consumers.
