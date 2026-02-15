# EHI Export Analysis: drchrono Inc.

**Product**: drchrono EHR v11.0
**Analysis date**: 2026-02-15
**CHPL ID**: 15.99.04.2897.DRCH.11.03.1.220531 (ID 10910)

## 1. Product Context

drchrono EHR is a cloud-based, all-in-one ambulatory EHR and practice management platform serving 4,600+ independent practices and 13,000+ providers. It targets small to mid-sized practices across 20+ medical specialties (family medicine, internal medicine, psychiatry, OB/GYN, orthopedics, etc.) and is mobile-first with native iOS apps.

The platform stores data across these key functional areas:

- **Clinical EHR**: Customizable clinical note templates, problem lists, medications, allergies, vitals, procedures, care plans, risk assessments, physical exams, implantable device tracking, family/social history, functional/mental status assessments
- **E-Prescribing**: eRx, EPCS, electronic prior authorization, pharmacy messaging
- **Lab & Imaging**: Lab ordering, results, document management; imaging orders
- **Scheduling**: Appointments, reminders, patient self-scheduling, check-in kiosk
- **Billing & RCM**: HCFA 1500 claims, fee schedules, billing profiles, eligibility checks, insurance management, ERA/EOB, line items, transactions, patient payments, denial management
- **Patient Portal (OnPatient)**: Secure messaging, intake forms, consent forms, appointment scheduling, payments, clinical summaries
- **Document Management**: Integrated eFax, uploaded documents, referral documents
- **Communications**: Internal messaging, patient messaging, direct messaging, communication logs
- **Immunizations**: Vaccine records, inventory tracking, registry integration
- **Public Health**: Immunization registry, syndromic surveillance, cancer case reporting

This establishes the baseline: a complete (b)(10) export should cover clinical data, billing/claims, insurance, medications, labs, communications, documents, and specialty-specific clinical content.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `drchrono-ehi-export-documentation-v18.xlsx` (170 KB) | **Primary data dictionary** — two sheets: "Single Patient Export" (98 entities, 1,586 fields) and "Bulk Patient Export" (107 entities, 1,786 fields). Three columns: Export Name, Field, Description. | **Most informative** — definitive source for entity/field inventory |
| `reference-guide-v4.pdf` (5 pages, 428 KB) | Technical reference: file naming conventions, directory structure, export process, security model, data element listing by exporter type | High — export mechanics and structure |
| `reference-guide-v4.html` (682 KB) | HTML version of reference guide v4 (same content as PDF) | Same as PDF |
| `glossary-data-elements-v5.pdf` (3 pages, 75 KB) | Field-level glossary organized by exporter (Doctor, Patient, Practice Group, Media, ReadMe). Updated 1/23/2026. | High — entity-level descriptions and media file types |
| `glossary-data-elements-v5.html` (662 KB) | HTML version of glossary v5 | Same as PDF |
| `creating-a-new-request.html` (661 KB) | Step-by-step user guide for initiating single-patient and bulk exports, including permissions, dashboard navigation | Medium — export mechanics |
| `ehi-export-overview.html` (653 KB) | Landing page describing self-service EHI export feature and its compliance basis | Medium — confirms self-service access |
| `ehi-export-faq.html` (652 KB) | FAQ covering processing time (up to 14 business days), export sizes (200+ GB), blank CSV explanations, batch file numbering | Medium — practical details |
| `data-mapping-v2.html` (692 KB) | Data mapping guide showing how to join CSVs via foreign keys (e.g., patient_id linking demographics to uploaded_documents) | Medium — relationship documentation |
| `unpacking-export-files.html` (649 KB) | Instructions for extracting .7z multi-part archives | Low — operational guidance |
| `folder-contents.html` (650 KB) | Hub page linking to all 8 versioned XLSX data dictionaries (v1.0–v1.8) | Low — link index |
| XLSX versions v1.0–v1.7 (7 files) | Prior versions of the data dictionary | Low — superseded by v1.8 |
| 6 screenshots (PNG) | Full-page browser captures of key support pages | Low — visual confirmation of page content |
| `reference-guide-v1.html` (679 KB) | Earlier version of reference guide | Low — superseded by v4 |

## 3. Export Mechanics

**Format**: CSV files organized in a hierarchical directory structure, delivered as a ZIP archive (or multi-part .7z for large practices).

**Directory structure** (from Reference Guide v4, p. 2):
```
drchrono_data_export/
├── <export_id>/
│   ├── doctors/          (doctor/provider CSVs + consent_form_files/ + doctor_message_files/)
│   ├── patients/         (patient CSVs + exported_documents/ subdirectories)
│   ├── practice_group/   (practice-level CSVs, bulk export only)
│   ├── media/            (actual binary files: PDFs, images, faxes, etc.)
│   └── README.txt
```

**Mechanism**: Self-service via the EHR UI under Reports → EHI Data Export. Users need the "EHI Export" permission enabled in account settings.

- **Single patient**: Real-time processing, initiated by provider. Select patient → click Request → download from dashboard.
- **Bulk (practice-level)**: Requires completing a request form (contact info, doctor ID, practice group ID, reason). Processed in up to 14 business days. Patients batched in groups of 50, with numerically suffixed CSV files (e.g., `allergies_1.csv`, `allergies_2.csv`).

**Access constraints**: Exports available for download for 30 days; then archived (metadata kept, files deleted). For very large exports (200+ GB), DrChrono offers ETL team delivery on a hard drive for an additional cost.

**No fees for standard export**: Self-service single-patient and bulk export are included features. Hard drive delivery is the only cost option mentioned.

## 4. Export Content: What's In It

### Data dictionary summary

The XLSX data dictionary v1.8 (effective with exports after 1/28/2026) contains:

| Sheet | Entities (CSV files) | Total Fields | Fields with Descriptions | Description % |
|---|---|---|---|---|
| Single Patient Export | 98 | 1,586 | 1,586 | 100.0% |
| Bulk Patient Export | 107 | 1,786 | 1,754 | 98.2% |

The 9 additional entities in the bulk export are practice-level data: `custom_vital_type.csv`, `education_resource.csv`, `mu_syndromic_surveillance_log.csv`, `offices.csv`, `patient_import_ccda_file.csv`, `soap_note_custom_report.csv`, `lab_quest_cd_order_code.csv`, `lab_quest_cd_order_code_aoe.csv`, and `practice_group.csv`.

The 32 fields without descriptions (1.8% of bulk export) are concentrated in two entities: `doctor_message.csv` (22 fields) and `doctor_message_log.csv` (7 fields), plus 3 fields in `race_subcategories_1.csv`. These appear to be a documentation oversight in these specific entities, not a systematic gap.

**Documentation structure**: Each row has three columns — `Export Name` (CSV filename), `Field` (column name), and `Description` (human-readable explanation). No explicit data types, value sets, or foreign key columns — though types are often implied by descriptions (e.g., "Date of Birth", "Boolean flag", "Unique ID") and foreign key relationships are documented separately in the Data Mapping Guide v2.

### Vendor's content organization

The vendor organizes entities into four "exporters" (from Glossary v5 and Reference Guide v4):

**Doctor Exporter** (8 entities in bulk, 2 in single-patient)

| Entity | Fields | Described | Notes |
|---|---|---|---|
| doctors.csv | 16 | 16 | Provider demographics, NPI, specialty |
| offices.csv | 29 | 29 | Practice locations, exam rooms |
| custom_vital_type.csv | 7 | 7 | Custom vital type definitions |
| education_resource.csv | 44 | 44 | Patient education materials |
| mu_syndromic_surveillance_log.csv | 13 | 13 | Public health surveillance logs |
| patient_import_ccda_file.csv | 18 | 18 | Imported C-CDA file records |
| soap_note_custom_report.csv | 36 | 36 | Custom SOAP note report templates |
| soap_note_line_item_field_type.csv | 29 | 29 | SOAP note structured field definitions |

**Practice Group Exporter** (3 entities, bulk only)

| Entity | Fields | Described |
|---|---|---|
| practice_group.csv | 7 | 7 |
| lab_quest_cd_order_code.csv | 25 | 25 |
| lab_quest_cd_order_code_aoe.csv | 15 | 15 |

**Patient Exporter** (87–90 entities) — see breakdown by domain below.

**Media Exporter** — binary files organized in subfolders:
- `clinical/` — Clinical documents and uploaded patient documents
- `dr_message_attachment/` — Doctor message file attachments
- `hipaa_forms/` — Practice consent form templates
- `education/` — Custom patient education resource files
- `message_attachment/` — DIRECT secure message attachments
- `patient_import/` — Imported patient C-CDA XML files
- `inbound_faxes/` — Inbound referral files
- `LabOrderDocumentFiles/` — Lab order document PDFs
- `referrals/` — Outbound referral files

### Category breakdown (Bulk Patient Export)

| Category | Entities | Fields | Described | Desc % |
|---|---|---|---|---|
| Demographics | 8 | 238 | 235 | 99% |
| Clinical Notes | 4 | 40 | 40 | 100% |
| Problems / Diagnoses | 1 | 25 | 25 | 100% |
| Medications / Prescriptions | 4 | 131 | 131 | 100% |
| Allergies | 2 | 28 | 28 | 100% |
| Immunizations | 3 | 51 | 51 | 100% |
| Vitals | 3 | 35 | 35 | 100% |
| Lab Orders & Results | 6 | 80 | 80 | 100% |
| Imaging Orders | 1 | 12 | 12 | 100% |
| Procedures | 1 | 7 | 7 | 100% |
| Care Plans / Goals | 9 | 54 | 54 | 100% |
| Care Team | 4 | 37 | 37 | 100% |
| Family History | 5 | 47 | 47 | 100% |
| Social History | 2 | 9 | 9 | 100% |
| Functional & Mental Status | 4 | 21 | 21 | 100% |
| Insurance / Coverage | 5 | 137 | 137 | 100% |
| Claims / Billing | 4 | 109 | 109 | 100% |
| Consent Forms | 4 | 48 | 48 | 100% |
| Communications / Messages | 10 | 139 | 110 | 79% |
| Documents | 2 | 37 | 37 | 100% |
| Referrals | 2 | 31 | 31 | 100% |
| Devices | 3 | 49 | 49 | 100% |
| Clinical Decision Support | 2 | 128 | 128 | 100% |
| Encounters / Visits | 1 | 19 | 19 | 100% |
| Patient Education | 2 | 14 | 14 | 100% |
| Patient Flags | 1 | 12 | 12 | 100% |
| Case Reporting | 1 | 8 | 8 | 100% |
| Imported CCDA Data | 1 | 19 | 19 | 100% |
| Doctor / Provider Info | 8 | 173 | 173 | 100% |
| Practice Group | 3 | 47 | 47 | 100% |

Full entity inventory with all fields: `analysis/full-entity-inventory.json`

### Top entities by field count

| Entity | Fields | Category |
|---|---|---|
| demographics.csv | 180 | Demographics |
| clinical_decision_support_rules.csv | 117 | Clinical Decision Support |
| prescription.csv | 59 | Medications / Prescriptions |
| patient_drug.csv | 50 | Medications / Prescriptions |
| auto_accident_insurance.csv | 48 | Insurance / Coverage |
| education_resource.csv | 44 | Doctor / Provider Info |
| patient_vaccination_record.csv | 37 | Immunizations |
| soap_note_custom_report.csv | 36 | Doctor / Provider Info |
| primary_hospital_insurance.csv | 35 | Insurance / Coverage |
| claims.csv | 31 | Claims / Billing |
| payments_insurance.csv | 29 | Claims / Billing |
| soap_note_line_item_field_type.csv | 29 | Doctor / Provider Info |
| history_message.csv | 26 | Communications / Messages |
| consent_form_signatures.csv | 25 | Consent Forms |
| lab_result.csv | 25 | Lab Orders & Results |
| payments_patient.csv | 25 | Claims / Billing |
| problems.csv | 25 | Problems / Diagnoses |
| system_vitals.csv | 25 | Vitals |
| uploaded_documents.csv | 25 | Documents |
| allergies.csv | 24 | Allergies |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export spans 30 distinct data categories (using the vendor's exporter/entity organization), covering substantially all clinical and administrative data the product stores about patients.

**Deepest coverage** (most entities and fields):
- **Demographics** (8 entities, 238 fields): Exceptionally detailed — includes occupation codes, tribal affiliations, race/ethnicity subcategories (separated into dedicated files in v5), responsible party information, and USCDI occupation/industry codes.
- **Medications / Prescriptions** (4 entities, 131 fields): Full medication history (`patient_drug.csv` with 50 fields), prescriptions (59 fields), prior authorization requests, and prescription messaging.
- **Insurance / Coverage** (5 entities, 137 fields): Auto accident insurance (48 fields), primary hospital insurance (35 fields), workers' comp, and insurance authorizations.
- **Claims / Billing** (4 entities, 109 fields): Claims data (31 fields), insurance payments (29 fields), patient payments (25 fields), and Good Faith Estimates/patient cost estimator (24 fields).
- **Communications** (10 entities, 139 fields): Comprehensive coverage of patient messages, doctor messages, direct (secure) messages, prescription messages, history messages, communication logs, and outgoing message statuses — with attachment references linking to media files.

**Moderate coverage**:
- **Lab Orders & Results** (6 entities, 80 fields): Lab orders, documents, ICD-10 codes, results, result authors, and result sets.
- **Care Plans / Goals** (9 entities, 54 fields): Granular decomposition into plans, goals, objectives, interventions, attached codes, and authors.
- **Clinical Notes** (4 entities, 40 fields): Notes, archives (prior versions), custom sections, section comments, and SOAP note field values.

**Thinner but present**:
- **Procedures** (1 entity, 7 fields): Relatively thin — only 7 fields.
- **Social History** (2 entities, 9 fields): Minimal field count.
- **Imaging Orders** (1 entity, 12 fields): Order records but no imaging files in the documented media structure.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `demographics.csv` (180 fields), `patient_occupation.csv`, `tribal_affiliations.csv`, `ethnicity_subcategories.csv`, `race_subcategories.csv`, `uscdi_occupation_code.csv`, `uscdi_industry_code.csv`, `additional_responsible_party.csv`, `responsible_party_address.csv` — 8 entities, 238 fields | Exceptionally thorough; includes USCDI v3 elements |
| Encounters / visits | ✅ Covered | `appointments.csv` (19–41 fields depending on export type) | Appointment records present; visit-level encounter data may be embedded in clinical notes |
| Problems / conditions / diagnoses | ✅ Covered | `problems.csv` (25 fields) | Covers problem list data including SNOMED/ICD coding |
| Medications / prescriptions | ✅ Covered | `patient_drug.csv` (50 fields), `prescription.csv` (59 fields), `cover_my_meds_pa_request.csv`, `pa_request_medication.csv`, `prescription_message.csv` — 4 entities, 131 fields | Comprehensive; includes prior authorization and pharmacy messaging |
| Allergies | ✅ Covered | `allergies.csv` (24 fields), `allergy_snomed_code_mapping.csv` (4 fields) | Full allergy records with SNOMED mapping |
| Immunizations | ✅ Covered | `patient_vaccination_record.csv` (37 fields), `patientvaccinerecord_doses.csv`, `iz_patient_demographic.csv` — 3 entities, 51 fields | Thorough including dose details and immunization demographics |
| Vitals | ✅ Covered | `system_vitals.csv` (25 fields), `system_vitals_author.csv`, `custom_vital_value.csv`, `custom_vital_type.csv` | Includes both standard and custom vitals |
| Lab results | ✅ Covered | `lab_result.csv` (25 fields), `lab_result_author.csv`, `patient_lab_result_set.csv`, `lab_order.csv`, `lab_order_document.csv`, `lab_order_icd10_codes.csv` — 6 entities, 80 fields | Full lab workflow from order to result |
| Imaging / diagnostic reports | ⚠️ Partial | `patient_imaging_order.csv` (12 fields) — orders only; no imaging report content or image files in documented media structure | Product supports imaging orders; results/images may be in `uploaded_documents.csv` or media but not clearly documented |
| Procedures | ✅ Covered | `procedures.csv` (7 fields) | Present but relatively thin at 7 fields |
| Clinical notes / documents | ✅ Covered | `clinical_notes.csv`, `clinical_note_archives.csv`, `custom_clinical_note_sections.csv`, `note_section_comments.csv`, `soap_note_line_item_field_value.csv` — 4 entities, 40 fields; plus media/clinical/ for actual document files | Includes note versioning (archives) and structured SOAP note data |
| Care plans / goals | ✅ Covered | 9 entities, 54 fields: care plans, goals, objectives, interventions, attached codes, authors | Deeply decomposed and well-structured |
| Orders / referrals | ✅ Covered | `inbound_referrals.csv`, `outbound_referrals.csv` (31 fields), `patient_device_orders.csv` (24 fields), `patient_imaging_order.csv` (12 fields) | Referrals and device/imaging orders present |
| Insurance / coverage | ✅ Covered | 5 entities, 137 fields: auto accident, primary hospital, workers' comp insurance; insurance authorizations | Comprehensive coverage of multiple insurance types |
| Claims / billing | ✅ Covered | `claims.csv` (31 fields), `payments_insurance.csv` (29 fields), `payments_patient.csv` (25 fields), `patient_cost_estimator.csv` (24 fields) — 4 entities, 109 fields | Genuine billing data export including claims, insurance payments, patient payments, and Good Faith Estimates |
| Payments | ✅ Covered | `payments_insurance.csv` (29 fields), `payments_patient.csv` (25 fields) | Both insurance and patient payment records |
| Consents / directives | ✅ Covered | `consent_forms.csv`, `consent_form_assignments.csv`, `consent_form_signatures.csv`, `consent_form_signature_audit_logs.csv` — 4 entities, 48 fields; plus media/hipaa_forms/ for actual consent documents | Full consent workflow including signature audit |
| Patient communications / portal messages | ✅ Covered | `patient_message.csv`, `patient_message_attachment.csv`, `doctor_message.csv`, `direct_message.csv`, `direct_message_attachment.csv`, `communication_log.csv`, `history_message.csv`, `outgoing_patient_message_status.csv`, `prescription_message.csv` — 10 entities, 139 fields | Exceptionally comprehensive messaging coverage |
| Family history | ✅ Covered | `family_history.csv`, `clinical_observation.csv`, `clinical_observation_snomed_details.csv`, `person.csv`, `relationship.csv` — 5 entities, 47 fields | Structured family history with clinical observations |
| Social history | ✅ Covered | `social_history.csv`, `social_history_author.csv` — 2 entities, 9 fields | Present but thin |
| Functional / mental status | ✅ Covered | `functional_statuses.csv`, `functional_status_authors.csv`, `mental_statuses.csv`, `mental_status_authors.csv` — 4 entities, 21 fields | Separate functional and mental status assessments |
| Implantable devices | ✅ Covered | `implantable_devices.csv` (22 fields), `implantable_device_authors.csv`, `patient_device_orders.csv` (24 fields) — 3 entities, 49 fields | Device tracking with UDI support |

**Notable gaps relative to product capabilities:**

| Gap | Significance |
|---|---|
| **Line items / superbills** | The product API exposes `/api/line_items` (individual billable service entries) and billing profiles, but no dedicated `line_items.csv` appears. Line item data may be embedded in `claims.csv` but this is not clear from documentation. Minor gap. |
| **Fee schedules / billing profiles** | API exposes `/api/fee_schedules` and `/api/billing_profiles` — these are practice configuration data, not patient-specific EHI. Not a true gap. |
| **Eligibility checks** | API has `/api/eligibility_checks` — administrative/operational, not patient decision-making data. Not a true gap. |
| **Tasks** | API has `/api/tasks` — these are workflow/operational records, not clinical EHI. Not a true gap. |

## 6. Documentation Quality

**Strengths:**

- **Complete field-level data dictionary**: The XLSX v1.8 provides descriptions for 100% of single-patient fields (1,586/1,586) and 98.2% of bulk export fields (1,754/1,786). This is among the highest description rates seen in (b)(10) documentation.
- **Actively versioned**: 8 XLSX versions (v1.0–v1.8), 4 reference guide versions (v1–v4), 5 glossary versions (v1–v5), and 2 data mapping guide versions — showing sustained investment in documentation over 2+ years.
- **Relationship documentation**: The Data Mapping Guide v2 explicitly explains how to join CSV files via foreign keys (e.g., `patient_id` in `uploaded_documents.csv` links to `id` in `demographics.csv`).
- **Practical guidance**: FAQ addresses real-world concerns (blank CSVs explained, batch numbering, export sizes, technical requirements).
- **Multiple formats**: XLSX (machine-parseable), HTML (browsable), PDF (archivable).

**Weaknesses:**

- **No explicit data types**: The XLSX has no "Type" column — a developer must infer whether a field is a date, integer, string, or boolean from the description text.
- **No value set documentation**: Coded/enumerated fields (e.g., status fields, message types) don't document their valid values.
- **Foreign keys not in XLSX**: Relationships are documented in a separate mapping guide rather than embedded in the data dictionary as a "References" column.
- **32 undescribed fields in bulk export**: All concentrated in `doctor_message.csv` and `doctor_message_log.csv` — appears to be an oversight rather than systematic.
- **No sample data**: No sample CSV files, synthetic data, or example records are provided. A developer would need access to an actual export to understand data shapes.

**Developer usability**: A competent developer could build an import from this documentation. The XLSX schema is machine-parseable, field descriptions are meaningful, and the mapping guide explains joins. The main friction points would be inferring data types and discovering valid values for coded fields — both solvable with a sample export.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine (b)(10) implementation exporting the vendor's native data model as CSV files. It is not a repackaged C-CDA or FHIR API. The 107 CSV entities (bulk) directly reflect internal database tables with many entities that have no FHIR equivalent (e.g., `cover_my_meds_pa_request.csv`, `soap_note_line_item_field_value.csv`, `consent_form_signature_audit_logs.csv`, `clinical_decision_support_rules.csv`). The export includes binary media files (documents, faxes, images) alongside structured data. Documentation is thorough, versioned, and actively maintained.

### Key Findings

1. **Genuinely comprehensive data model export**: 107 entities (bulk) / 98 entities (single-patient) with 1,786 / 1,586 fields covering clinical, billing, insurance, communications, documents, and specialty data — not a clinical summary repackaged as (b)(10).

2. **Near-complete field descriptions**: 100% of single-patient fields and 98.2% of bulk export fields have human-readable descriptions in the XLSX data dictionary, making this one of the most thoroughly documented (b)(10) exports.

3. **Real billing/claims coverage**: `claims.csv` (31 fields), `payments_insurance.csv` (29 fields), `payments_patient.csv` (25 fields), and `patient_cost_estimator.csv` (24 fields) — 109 total billing/claims fields. This is not just clinical data masquerading as a complete export.

4. **Active documentation maintenance**: 8 XLSX versions over ~2 years, with the latest (v1.8, effective 1/28/2026) adding race/ethnicity subcategory files. Version 5 of the glossary was published less than a month before this analysis.

5. **Self-service access**: Both single-patient and bulk exports are initiated through the EHR UI by authorized users — no vendor ticket or manual intervention required for standard exports.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV files in ZIP/7z archive, plus binary media files
Model type:      Native database model
Entities:        107 (bulk) / 98 (single-patient)
Fields:          1,786 (bulk) / 1,586 (single-patient)
Descriptions:    98.2% (bulk) / 100% (single-patient)
Sample data:     No
Bulk export:     Yes (practice-level export of all patients)
Domains covered: 21 of 21 applicable domains (imaging partial)
```

### Bottom Line

drchrono provides one of the stronger (b)(10) implementations: a true native database export with 107 CSV entities, 1,786 documented fields, near-complete descriptions, binary media file inclusion, and coverage across virtually all clinical and billing domains the product supports. The documentation is actively maintained and a developer could realistically build an import from it. The only notable gaps are the absence of sample data, lack of explicit data types/value sets, and 32 undescribed fields in two messaging entities.
