# EHI Export Analysis: OpenEMR Foundation

**Product**: OpenEMR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 10938 (v7.0, certified 2022-07-08), 11757 (v8, certified 2026-01-30)

## 1. Product Context

OpenEMR is the most widely deployed open-source EHR and practice management system globally, used at 20,000+ healthcare facilities across 184 countries. It is an ONC-certified Complete Ambulatory EHR primarily serving small to mid-size practices, community health centers, and solo practitioners. It runs on PHP/MySQL(MariaDB) and is free under the GNU GPL.

**Key data domains relevant to EHI export completeness:**

- **Clinical EHR**: Encounter documentation (SOAP notes, physical exams, review of systems), problem lists, medications, allergies, immunizations, vitals, lab orders/results, procedures, clinical decision support, care plans, clinical notes across specialties.
- **Specialty modules**: Ophthalmology/optometry (17 dedicated `form_eye_*` tables), behavioral health (GAD-7, PHQ-9, SDOH assessments), group therapy.
- **Billing & practice management**: CPT/HCPCS/ICD coding, CMS-1500 and UB-04 billing, electronic claims, insurance tracking, accounts receivable, payment processing, ERA posting.
- **Prescriptions / e-Prescribing**: Prescription tracking, drug inventory, in-house pharmacy dispensary.
- **Patient portal**: Secure messaging, appointment scheduling, document center, online payments, consents.
- **Documents**: Electronic document management with upload/generation capabilities, digital signatures.
- **Scheduling**: Appointment calendar, patient flow board, recall/reminders.
- **Forms**: Layout-based forms (LBF) for custom form creation, CAMOS notes, template-driven forms.
- **Interoperability**: C-CDA import/export, FHIR R4 API (US Core), Direct messaging.

This is a full-featured ambulatory EHR + practice management system. A genuine (b)(10) export should cover all of the above clinical and billing domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `wiki-page-b10.html` (25 KB) | MediaWiki page "OpenEMR 7.0.4 B10" — export setup/usage instructions with screenshots | High — documents export mechanics |
| `openemr.openemr.xml` (1.0 MB) | SchemaSpy XML schema — 322 tables, 4,941 columns, 892 FK relationships, machine-readable | **Primary artifact** — authoritative data dictionary |
| `ehi-export-docs-v7.html` (251 KB) | SchemaSpy index page listing all 322 tables with row/column counts | High — overview of schema |
| `tables/*.html` (318 files, 9.3 MB total) | Individual SchemaSpy table documentation pages with column-level comments | High — source of 1,805 additional column descriptions |
| `columns.html` (1.7 MB) | All columns across all tables (JS-rendered DataTables) | Medium — redundant with XML |
| `insertionOrder.txt` / `deletionOrder.txt` (5.5 KB each) | Table dependency ordering for database load/unload | Medium — shows FK dependency chain |
| `relationships.html` (9.5 KB) | Relationship diagram page (JS-rendered) | Low — requires browser |
| `enrichment/schema.json` (2.2 MB) | Pre-parsed JSON of the XML schema — all 322 tables/4,941 columns | High — machine-readable parse |
| `enrichment/html-comments.json` (878 KB) | Column comments extracted from 318 HTML table pages | High — 4,469 columns with HTML comments |
| `SinglePatient_EHI_Export.png` / `TotalPatient_EHI_Export.png` / `EHI-Export-Task-Completed.png` | Screenshots of export UI | Medium — confirms export mechanism |

The XML schema file (`openemr.openemr.xml`) is by far the most informative artifact — it is a complete, machine-readable representation of the entire database schema with types, sizes, nullability, defaults, foreign keys, and remarks. The individual table HTML pages supplement this with additional column-level descriptions not present in the XML.

## 3. Export Mechanics

- **Format**: ZIP files containing CSV files (one per database table) plus patient documents and images. Each ZIP includes a README linking to the public SchemaSpy documentation.
- **Mechanism**: Built-in module activated by administrator (Modules → Manage Modules → Electronic Health Information Exporter). Accessible via Miscellaneous → Electronic Health Information Export menu.
- **Single-patient export**: Specify patient PID; all data bundled into one ZIP.
- **Bulk/population export**: Leave PID blank; system batches patients into ZIP files of configurable size (1–4,000 MB). Batch sizing accounts for document storage + ~100KB per patient for database data.
- **Access**: Administrator role only (admin/super ACL).
- **Document inclusion**: Optional checkbox to include/exclude patient document files from storage.
- **Integrity verification**: Hash values provided for each ZIP file.
- **No fees or vendor assistance required** — self-service through the UI.

## 4. Export Content: What's In It

The export is a **direct dump of the OpenEMR MariaDB database** in CSV format, accompanied by a complete SchemaSpy-generated data dictionary.

### Scale

- **322 tables** in the `openemr` schema
- **4,941 columns** across all tables
- **2,782 columns (56.3%) have descriptions** (from XML remarks, HTML comments, or both)
- **141 tables (43.8%) have table-level remarks** describing their purpose
- **446 foreign key relationships** documented (892 FK references in the XML including child references)
- **1 table** (`address`) has 0 columns (empty placeholder)
- **5 tables** have columns but zero descriptions

### Description sources

Column descriptions come from two complementary sources:
- **1,521 columns** have remarks in the XML schema
- **1,805 columns** have comments in the HTML table pages
- **544 columns** have descriptions from both sources
- **977 columns** have XML-only descriptions; **1,261 columns** have HTML-only descriptions
- **2,159 columns (43.7%)** have no description from either source

### Vendor's own content organization

The SchemaSpy documentation doesn't impose its own categories — each of the 322 tables is documented individually. The table-level remarks and naming conventions allow categorization. Based on table names, remarks, and the product's module structure, the tables fall into these groups:

| Category | Tables | Columns | Described | Desc % |
|---|---|---|---|---|
| Clinical Forms (encounters, vitals, SOAP, physical exams, etc.) | 53 | 995 | 455 | 45.7% |
| Ophthalmology/Eye Care (17 `form_eye_*` tables) | 17 | 566 | 106 | 18.7% |
| System & Configuration | 45 | 446 | 299 | 67.0% |
| Users & Access Control | 42 | 386 | 297 | 76.9% |
| Demographics & Patient | 14 | 379 | 186 | 49.1% |
| Reference Data & Code Sets | 32 | 329 | 198 | 60.2% |
| Billing & Financial | 15 | 245 | 168 | 68.6% |
| Labs & Procedures | 12 | 235 | 184 | 78.3% |
| Medications & Prescriptions | 12 | 231 | 128 | 55.4% |
| Documents | 13 | 200 | 148 | 74.0% |
| Clinical Lists & Issues | 12 | 182 | 117 | 64.3% |
| Facility & Reference Entities | 11 | 158 | 110 | 69.6% |
| Scheduling | 9 | 148 | 119 | 80.4% |
| Messaging & Notifications | 11 | 130 | 95 | 73.1% |
| Audit & Logging | 8 | 87 | 56 | 64.4% |
| Insurance | 4 | 69 | 19 | 27.5% |
| Questionnaires | 2 | 48 | 35 | 72.9% |
| Interoperability (CCDA) | 5 | 47 | 20 | 42.6% |
| Care Plans & Teams | 3 | 42 | 25 | 59.5% |
| Amendments | 2 | 18 | 17 | 94.4% |
| **TOTAL** | **322** | **4,941** | **2,782** | **56.3%** |

The full entity inventory with all 322 tables and 4,941 columns is in `analysis/full-entity-inventory.json`.

### Top 20 largest tables

| Table | Columns | Described | Category | Remarks |
|---|---|---|---|---|
| `patient_data` | 137 | 100 | Demographics & Patient | Main patient record with demographic information |
| `history_data` | 94 | 5 | Demographics & Patient | Patient eating, sleeping, drinking, drug habits and other history |
| `form_eye_neuro` | 84 | 13 | Ophthalmology/Eye Care | (none) |
| `form_eye_refraction` | 68 | 5 | Ophthalmology/Eye Care | (none) |
| `form_eye_mag_dispense` | 59 | 5 | Ophthalmology/Eye Care | (none) |
| `prescriptions` | 52 | 22 | Medications & Prescriptions | Internal and external prescription information |
| `openemr_postcalendar_events` | 49 | 47 | Scheduling | (none) |
| `form_eye_mag_wearing` | 46 | 8 | Ophthalmology/Eye Care | (none) |
| `procedure_order` | 45 | 40 | Labs & Procedures | (none) |
| `form_eye_antseg` | 42 | 4 | Ophthalmology/Eye Care | (none) |
| `documents` | 41 | 36 | Documents | Digital documents connected to a patient |
| `form_encounter` | 40 | 17 | Clinical Forms | Patient's visit to a healthcare provider |
| `lists` | 40 | 38 | Clinical Lists & Issues | Patient issues: allergies, medications, medical problems, surgeries |
| `insurance_data` | 39 | 7 | Insurance | Patient insurance information |
| `form_eye_hpi` | 38 | 4 | Ophthalmology/Eye Care | (none) |
| `immunizations` | 34 | 22 | Medications & Prescriptions | Patient immunizations |
| `form_eye_acuity` | 33 | 6 | Ophthalmology/Eye Care | (none) |
| `form_eye_external` | 33 | 4 | Ophthalmology/Eye Care | (none) |
| `billing` | 32 | 31 | Billing & Financial | Patient billing records for billing codes |
| `form_vitals` | 32 | 14 | Clinical Forms | Records of patient vital sign assessment |

### Notable observations

- **`history_data` (94 columns, only 5 described)**: One of the largest tables but poorly described. Contains patient social/behavioral history — significant EHI but with minimal column-level documentation.
- **Ophthalmology tables (566 columns, only 18.7% described)**: The 17 `form_eye_*` tables are the second-largest category by column count but have the lowest description rate. Many columns are clinical measurement fields whose meaning may be obvious to ophthalmologists but opaque to general developers.
- **`insurance_data` (39 columns, only 7 described)**: Key EHI table with poor documentation coverage.
- **`lbf_data` (5 columns)**: Layout-based form data — the dynamic form system. All custom form data flows through this table with form_id/field_id/field_value columns. This is an elegant but opaque design: the actual field semantics are determined by the layout definition, not the schema.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is a **complete database dump** — all 322 tables in the OpenEMR MariaDB schema are exported as CSV files. This is not a curated subset; it is literally every table in the database.

**Richest categories by column count:**
1. **Clinical Forms** (53 tables, 995 columns): Comprehensive encounter documentation including SOAP notes, vitals, physical exams, review of systems, care plans, transfer summaries, functional/cognitive status, GAD-7, PHQ-9, SDOH assessments, pain maps, and numerous specialty forms. The `form_encounter` table (40 columns) anchors all encounters, with the `forms` table linking form instances to encounters.
2. **Ophthalmology/Eye Care** (17 tables, 566 columns): Deep specialty module covering acuity, refraction, biometrics, anterior/posterior segment, neuro, HPI, external exam, dispensing, and wearing records. This level of specialty detail is unusual.
3. **Demographics & Patient** (14 tables, 379 columns): The `patient_data` table alone has 137 columns. Combined with `history_data` (94 columns), patient access/portal data, and person records, this is exhaustive.
4. **Billing & Financial** (15 tables, 245 columns): Full billing chain: `billing` (32 cols), `claims` (16 cols), `ar_activity` (26 cols), `ar_session`, `payments`, `fee_schedule`, `voids`, and payment processing tables.
5. **Labs & Procedures** (12 tables, 235 columns): Complete procedure workflow: `procedure_type`, `procedure_order` (45 cols), `procedure_report`, `procedure_result`, `procedure_answers`, `procedure_questions`, `procedure_specimen`.

**Thinnest categories:**
- **Amendments** (2 tables, 18 columns) — but fully described (94.4%), and the domain is small.
- **Insurance** (4 tables, 69 columns) — functional but poorly described (27.5%).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient_data` (137 cols), `history_data` (94 cols), `person` (33 cols), portal data tables | Exhaustive. 137-column patient record is among the most detailed seen. |
| Encounters / visits | ✅ Covered | `form_encounter` (40 cols), `forms` (index table), 45+ form tables | Comprehensive — every encounter form type has its own table. |
| Problems / conditions / diagnoses | ✅ Covered | `lists` (40 cols, type='medical_problem'), `issue_encounter`, `issue_types` | Well-covered via unified `lists` table with type discriminator. |
| Medications / prescriptions | ✅ Covered | `prescriptions` (52 cols), `drugs` (47 cols), `drug_inventory`, `drug_sales`, `drug_templates`, `erx_*` tables | Includes e-prescribing chain and pharmacy dispensing. |
| Allergies | ✅ Covered | `lists` (type='allergy') | Stored in unified `lists` table. |
| Immunizations | ✅ Covered | `immunizations` (34 cols), `immunization_observation` | Dedicated tables with observation data. |
| Vitals | ✅ Covered | `form_vitals` (32 cols), `form_eye_vitals` (30 cols for eye-specific) | Includes BMI, head circumference, growth chart support. |
| Lab results | ✅ Covered | `procedure_order` (45 cols), `procedure_report`, `procedure_result` (19 cols), `procedure_type`, `external_procedures` | Full order-report-result chain plus external procedure tracking. |
| Imaging / diagnostic reports | ⚠️ Partial | `documents` table stores images; DICOM viewer mentioned in product features but no dedicated imaging tables | Images stored as documents; no structured radiology report table. |
| Procedures | ✅ Covered | `procedure_order`, `procedure_type`, `procedure_report`, `procedure_result` | Full procedure workflow. |
| Clinical notes / documents | ✅ Covered | `form_soap` (12 cols), `form_clinical_notes`, `form_clinical_instructions`, `pnotes`, `documents` (41 cols), CAMOS notes | Multiple note types plus full document management. |
| Care plans / goals | ✅ Covered | `form_care_plan`, `care_team`, `care_team_member`, `care_teams`, `patient_care_experience_preferences`, `patient_treatment_intervention_preferences` | Dedicated form tables and care team tracking. |
| Orders / referrals | ✅ Covered | `procedure_order` (45 cols), `transactions` (for referrals), `form_eye_mag_orders` | Orders are well-structured; referrals via `transactions` table. |
| Insurance / coverage | ✅ Covered | `insurance_data` (39 cols), `insurance_companies` (32 cols), `insurance_numbers`, `insurance_type_codes` | Multiple insurance plans per patient supported. |
| Claims / billing | ✅ Covered | `billing` (32 cols), `claims` (16 cols), `ar_activity` (26 cols), `ar_session`, `x12_partners`, `x12_remote_tracker` | Full claims lifecycle: creation, submission, tracking, AR. |
| Payments | ✅ Covered | `payments`, `ar_activity`, `ar_session`, `payment_gateway_details`, `payment_processing_audit`, `voids` | Payment processing with void tracking. |
| Consents / directives | ✅ Covered | `onsite_documents` (patient portal consents/forms), `onsite_signatures` (digital signatures) | Portal document submission and digital signature capture. |
| Patient communications / portal messages | ✅ Covered | `pnotes` (18 cols), `onsite_mail` (24 cols), `onsite_messages` (8 cols), `onsite_portal_activity` | Both async messages and real-time chat. |
| Specialty: Ophthalmology | ✅ Covered | 17 `form_eye_*` tables (566 cols total) | Exceptionally deep: acuity, refraction, biometrics, neuro, dispensing. |
| Specialty: Behavioral health | ✅ Covered | `form_gad7`, `form_phq9`, `form_sdoh` (SDOH assessments) | Standardized screening instruments. |
| Specialty: Group therapy | ✅ Covered | `therapy_groups`, `therapy_groups_participants`, `therapy_groups_counselors`, `therapy_groups_participant_attendance` | Dedicated group therapy tracking. |
| Custom forms | ✅ Covered | `lbf_data` (layout-based form data), `lbt_data`, `layout_group_properties`, `layout_options` | Dynamic form system — all custom form responses exported. |
| Amendments | ✅ Covered | `amendments` (12 cols), `amendments_history` (6 cols) | Patient-initiated amendment requests with audit trail. |
| Questionnaires / PROs | ✅ Covered | `questionnaire_repository` (23 cols), `questionnaire_response` (25 cols), `pro_assessments` (13 cols) | FHIR-based questionnaire support plus PRO assessments. |

**Domains covered: 22 of 22 applicable** (imaging is partial — stored as documents but no structured radiology reports).

**Gap analysis**: The product covers all identified EHI domains. The export includes the complete database, so there are no structural gaps. The only domain marked partial (imaging) reflects a product design choice (images stored as documents) rather than an export gap. The export actually goes beyond EHI requirements by including audit logs, system configuration, reference data, and user/access control tables.

## 6. Documentation Quality

### Strengths

- **Machine-readable schema**: The `openemr.openemr.xml` file is a complete, parseable representation of the entire database schema. A developer can programmatically discover every table, column, type, constraint, and relationship.
- **SchemaSpy documentation site**: Generated from the live database schema (MariaDB 11.4.9 via SchemaSpy 6.2.4). Provides a browsable, searchable interface with DataTables. 318 individual table pages with column details.
- **Foreign key documentation**: 446 foreign key relationships explicitly defined, showing how tables connect. Insertion/deletion order files enable proper database loading.
- **Data types and constraints**: Every column has type, size, nullability, and default value documented.
- **Clear export instructions**: Step-by-step wiki guide with screenshots for both single-patient and population exports.
- **Dual hosting**: Primary and backup documentation URLs for redundancy.
- **Self-describing exports**: Each ZIP includes a README linking to documentation.

### Weaknesses

- **43.7% of columns lack any description** (2,159 of 4,941). While types and names are always present, many columns have no textual explanation of their purpose.
- **Ophthalmology module is poorly described**: 17 tables, 566 columns, but only 18.7% described. These are highly specialized clinical fields.
- **`history_data` is poorly described**: 94 columns but only 5 with descriptions. This is one of the most important EHI tables.
- **`insurance_data` is poorly described**: 39 columns but only 7 described (27.5%).
- **No sample data provided**: No example CSV files showing what the export output looks like. A developer would need to set up OpenEMR and perform an export to see actual data.
- **No value set documentation beyond the schema**: Coded fields reference `list_options` but the actual option values aren't documented in the schema (they're in the exported `list_options.csv` itself).
- **Table-level remarks missing for 56.2% of tables** (181 of 322).

### Developer usability

A developer could reconstruct the complete OpenEMR data model from this documentation. The XML schema provides enough information to create a receiving database, load the CSV files in the correct order, and establish foreign key relationships. However, understanding the *meaning* of many columns would require either domain expertise or access to the OpenEMR source code (which is open-source, mitigating this concern). The lack of sample data makes it harder to understand encoded values, delimiters in multi-value fields, and date formats without performing an actual export.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a direct export of the complete MariaDB database schema — 322 tables, 4,941 columns — covering every data domain the product stores. It is not a FHIR projection, not a C-CDA repackaging, and not a clinical summary. It is the full native data model exported as CSV with complete schema documentation via SchemaSpy.

### Key Findings

1. **Genuinely complete export**: All 322 database tables are exported as CSV files. This includes clinical, billing, scheduling, medications, labs, documents, messaging, specialty modules, and more. No EHI domains are structurally missing.

2. **Machine-readable schema with 4,941 columns**: The SchemaSpy XML provides a complete, parseable data dictionary with types, sizes, nullability, defaults, and 446 foreign key relationships. This is among the most detailed EHI export documentation reviewed.

3. **56.3% of columns have descriptions**: While far from perfect, 2,782 of 4,941 columns have textual descriptions from the XML schema and/or HTML table pages. Key tables like `patient_data` (73% described), `billing` (97% described), and `lists` (95% described) are well-documented. Weaker areas include `history_data` (5.3% described) and the ophthalmology module (18.7% described).

4. **Exceptional specialty depth**: The 17 ophthalmology tables with 566 columns represent a level of specialty clinical data rarely seen in EHI exports. The behavioral health screening forms (GAD-7, PHQ-9, SDOH) and group therapy tracking further distinguish this export.

5. **Self-service, no vendor assistance needed**: The export is a built-in module with clear documentation, supporting both single-patient and population-level export. No fees, no vendor involvement required.

### Summary Stats

    Classification:  Comprehensive native export
    Export format:   CSV (in ZIP files with patient documents)
    Model type:      Native database (MariaDB)
    Entities:        322 tables
    Fields:          4,941 columns
    Descriptions:    56.3% of fields (2,782 of 4,941)
    Sample data:     No
    Bulk export:     Yes (configurable batch sizes up to 4 GB per ZIP)
    Domains covered: 22 of 22 applicable (imaging partial)

### Bottom Line

OpenEMR's EHI export is one of the strongest (b)(10) implementations reviewed. The complete database dump as CSV, combined with a machine-readable SchemaSpy data dictionary covering 322 tables and 4,941 columns, provides genuine "all EHI" export — not a clinical summary repackaged. The main weakness is that 43.7% of columns lack descriptions, with the ophthalmology module and patient history table particularly under-documented. However, the open-source nature of the codebase partially compensates, since a developer can inspect the source code to understand any column. A patient or provider requesting their data would receive a complete, usable copy of everything OpenEMR stores about them.
