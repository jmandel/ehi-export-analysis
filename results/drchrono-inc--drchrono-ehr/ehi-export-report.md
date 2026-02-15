# drchrono Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://support.drchrono.com/home/20260096536987-ehi-export-overview
- CHPL IDs: 10910
- Product: drchrono EHR v11.0
- Certification Date: 2022-05-31

## Navigation Journal

### Step 1: Initial probe
```bash
curl -sI -L "https://support.drchrono.com/home/20260096536987-ehi-export-overview" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Returned HTTP 200 with `Content-Type: text/html; charset=UTF-8`. No redirects. The page is a KnowledgeOwl-hosted support article.

### Step 2: Fetched and examined the overview page
```bash
curl -sL "https://support.drchrono.com/home/20260096536987-ehi-export-overview" \
  -H 'User-Agent: Mozilla/5.0' -o ehi-export-overview.html
```
The overview page describes the EHI Export product — a self-service export feature compliant with 21st Century Cures Act. It links to a rich set of sub-pages.

### Step 3: Identified documentation link structure
Searched the HTML for EHI-related links and found an extensive documentation hub organized under "EHI Bulk Data Export" in the left navigation. Key pages:

- **EHI Export: Overview** — main landing page
- **Creating a New Request: EHI Export** — user guide for initiating exports
- **EHI Export FAQ** — frequently asked questions
- **Glossary: Data Elements** — v1 through v5, field-level descriptions of all CSV files
- **DrChrono EHI Export Reference Guides** — v1 through v4, technical reference with file structure, naming conventions, security model
- **Single Patient and Bulk Export File/Folder Contents** — versioned XLSX data dictionaries (v1.0 through v1.8)
- **Understanding EHI Data Mapping in Exported Files** — v1 and v2, guides for linking data across CSV files
- **Unpacking Your DrChrono Export Files** — instructions for extracting .7z archives

### Step 4: Downloaded XLSX data dictionaries
The "Single Patient and Bulk Export File/Folder Contents" page links to 8 versioned XLSX files hosted on CloudFront CDN:
```bash
curl -sL "https://dyzz9obi78pm5.cloudfront.net/app/image/id/6973ea26e257319ba90d046a/n/drchrono-ehi-export-documentation-v18.xlsx" \
  -H 'User-Agent: Mozilla/5.0' -o drchrono-ehi-export-documentation-v18.xlsx
```
All 8 files verified as genuine Microsoft Excel 2007+ files via `file` command.

### Step 5: Downloaded HTML pages and PDFs
Fetched all key support articles as HTML. Also downloaded PDF exports of the Reference Guide v4 and Glossary v5 via KnowledgeOwl's `/home/pdfexport/id/` endpoint.

### Step 6: Took browser screenshots
Navigated to key pages in Chrome and captured full-page screenshots of: overview page, folder contents page, glossary v5, reference guide v4, and data mapping v2.

### Step 7: Checked additional pages
- `b10-exporter-media-file-mapping` — returned 404 ("Article Not Found"). This URL appears to have been retired.
- `single-patient-and-bulk-exports` — a category/section page, not an article (no article body, just navigation links).

## What Was Found

drchrono has built a dedicated, self-service EHI export system with comprehensive public documentation. This is one of the more thorough (b)(10) implementations encountered.

### Export Format

The export produces a **ZIP archive containing CSV files** organized in a hierarchical folder structure:

```
drchrono_data_export/
├── <export_id>/
│   ├── doctors/          (doctor/provider-related CSVs)
│   ├── patients/         (patient-related CSVs)
│   ├── practice_group/   (practice-level CSVs)
│   ├── media/            (actual files: PDFs, images, faxes, etc.)
│   └── README.txt
```

For practice-level (bulk) exports, data is batched in groups of 50 patients, with numerically suffixed CSV files (e.g., `allergies_1.csv`, `allergies_2.csv`). Exports can reach 200+ GB for large practices. They're delivered as .7z multi-part archives for large exports.

### Export Scope

**Single patient export**: 98 CSV file types covering patient-specific data plus a doctors.csv file.

**Bulk (practice-level) export**: 107 CSV file types, adding practice-wide data like office configurations, practice group info, custom vital types, syndromic surveillance logs, education resources, CCDA import files, and SOAP note custom reports.

Both export types also include a **Media folder** with actual files:
- Clinical documents and uploaded patient documents
- Doctor message attachments
- HIPAA consent form files
- Patient education resource files
- DIRECT secure message attachments
- Imported patient CCDA XML files
- Inbound fax/referral files
- Lab order document PDFs
- Outbound referral files

### Data Dictionary

The primary computable artifact is the **XLSX data dictionary** (latest: v1.8), which contains two sheets — "Single Patient Export" and "Bulk Patient Export". Each sheet has three columns: `Export Name` (CSV filename), `Field` (column name), and `Description` (human-readable explanation of the field).

The latest version (v1.8) documents:
- **1,586 field definitions** for single patient export across 98 CSV files
- **1,795 field definitions** for bulk patient export across 107 CSV files

The data dictionary has been actively maintained and expanded — from v1.0 (1,413/1,586 rows) through v1.8 (1,587/1,796 rows), with consistent growth across 8 versions.

### Documentation Pages

In addition to the XLSX data dictionary, drchrono provides:

1. **Reference Guides** (v1-v4): Technical documentation covering file naming conventions, directory structure, processing times, delivery options, security/access controls, and a complete listing of all data categories with brief descriptions.

2. **Glossary: Data Elements** (v1-v5): Web-based field-level glossary organized by exporter (Doctor, Patient, Practice Group, Media). The latest version (v5, effective 1/28/2026) added race/ethnicity subcategory files.

3. **Data Mapping Guides** (v1-v2): Instructions for joining data across CSV files using foreign key relationships (e.g., linking `uploaded_documents.csv` to `demographics.csv` via `patient_id`).

4. **FAQ**: Practical guidance on export size expectations, technical requirements, handling blank CSVs, and interpretation of specific fields.

5. **Creating a New Request**: Step-by-step user guide with screenshots for initiating single-patient and bulk exports via the EHR UI.

## Export Coverage Assessment

### Data Domain Coverage

This is a genuinely comprehensive (b)(10) export. Comparing against the product research, the export covers:

**Clearly covered:**
- **Patient demographics** — `demographics.csv` plus `patient_occupation.csv`, `tribal_affiliations.csv`, `ethnicity_subcategories.csv`, `race_subcategories.csv`, `uscdi_occupation_code.csv`, `uscdi_industry_code.csv`
- **Clinical notes** — `clinical_notes.csv`, `clinical_note_archives.csv` (prior versions!), `custom_clinical_note_sections.csv`, `note_section_comments.csv`, `soap_note_line_item_field_value.csv`, `soap_note_line_item_field_type.csv`, `soap_note_custom_report.csv`
- **Problems/diagnoses** — `problems.csv`
- **Medications** — `patient_drug.csv`, `prescription.csv`, `prescription_message.csv`, `cover_my_meds_pa_request.csv`, `pa_request_medication.csv`
- **Allergies** — `allergies.csv`, `allergy_snomed_code_mapping.csv`
- **Lab orders and results** — `lab_order.csv`, `lab_order_document.csv`, `lab_order_icd10_codes.csv`, `lab_result.csv`, `lab_result_author.csv`, `patient_lab_result_set.csv`
- **Immunizations** — `patient_vaccination_record.csv`, `patientvaccinerecord_doses.csv`, `iz_patient_demographic.csv`
- **Vitals** — `system_vitals.csv`, `system_vitals_author.csv`, `custom_vital_value.csv`, `custom_vital_type.csv`
- **Care plans** — 8 related CSV files covering plans, goals, interventions, objectives, authors, and attached codes
- **Care team** — `care_team_member.csv`, `doctor_staff_care_team_members.csv`, `external_care_team_members.csv`, `patient_as_care_team_members.csv`
- **Appointments** — `appointments.csv`
- **Insurance/billing** — `claims.csv`, `payments_insurance.csv`, `payments_patient.csv`, `auto_accident_insurance.csv`, `auto_accident_insurance_accident.csv`, `primary_hospital_insurance.csv`, `workers_comp_insurance.csv`, `insurance_authorizations.csv`, `patient_cost_estimator.csv`
- **Consent forms** — `consent_forms.csv`, `consent_form_assignments.csv`, `consent_form_signatures.csv`, `consent_form_signature_audit_logs.csv`
- **Messages** — `patient_message.csv`, `patient_message_attachment.csv`, `doctor_message.csv`, `doctor_message_log.csv`, `direct_message.csv`, `direct_message_attachment.csv`, `history_message.csv`, `outgoing_patient_message_status.csv`, `prescription_message.csv`, `communication_log.csv`
- **Documents** — `uploaded_documents.csv`, plus actual media files in clinical/, inbound_faxes/, referrals/ folders
- **Referrals** — `inbound_referrals.csv`, `outbound_referrals.csv`
- **Imaging orders** — `patient_imaging_order.csv`
- **Device orders** — `patient_device_orders.csv`, `implantable_devices.csv`, `implantable_device_authors.csv`
- **Family history** — `family_history.csv`, `clinical_observation.csv`, `clinical_observation_snomed_details.csv`, `person.csv`, `relationship.csv`
- **Social history** — `social_history.csv`, `social_history_author.csv`
- **Functional/mental status** — `functional_statuses.csv`, `functional_status_authors.csv`, `mental_statuses.csv`, `mental_status_authors.csv`
- **Clinical decision support** — `clinical_decision_support_rules.csv`, `patient_specific_actions.csv`
- **Patient education** — `education_resource.csv`, `education_resource_recommendation.csv`, `mu_patient_education_log.csv`
- **Case reporting** — `case_report_encounters.csv`
- **Syndromic surveillance** — `mu_syndromic_surveillance_log.csv`
- **Patient flags** — `patient_flags.csv`
- **Practice/office configuration** — `offices.csv`, `practice_group.csv`, `doctors.csv`
- **CCDA imports** — `patient_import_ccda_file.csv`, `clinical_list.csv`
- **Lab reference data** — `lab_quest_cd_order_code.csv`, `lab_quest_cd_order_code_aoe.csv`

**Potentially missing or unclear:**
- **Audit logs** — The product has an audit log feature (there's a separate support article for "Exporting your audit logs"), but no audit log CSV appears in the EHI export data dictionary. This is notable because audit logs are part of the EHI and are separately exportable.
- **Task management** — The product has tasks with categories, notes, statuses, and templates (visible in the API), but no task-related CSVs appear in the export.
- **Fee schedules and billing profiles** — While `claims.csv` and payment files are present, the API exposes /api/fee_schedules and /api/billing_profiles that don't appear as separate CSV files.
- **Eligibility checks** — The API has /api/eligibility_checks but no corresponding CSV.
- **Reminder profiles** — Appointment reminder configurations from the API aren't represented.
- **Custom demographics** — The API has /api/custom_demographics but no dedicated CSV (may be embedded in demographics.csv).
- **User/staff accounts and permissions** — The API has /api/users and /api/user_groups, but these aren't in the export.
- **Yellow notepad** — Quick notes from the API (/api/yellow_notepad) don't appear as a CSV.
- **Vaccine inventory** — Product tracks vaccine inventory, but only patient vaccination records are exported, not inventory management data.

Overall, the export covers the vast majority of patient-facing clinical and administrative data. The gaps are mostly in administrative/configuration data (tasks, fee schedules, user management) and audit logs.

### Export Format & Standards

- **Format**: CSV files in a ZIP archive. This is an appropriate choice for a (b)(10) export — it's universally readable, requires no special tooling, and maps naturally to the relational data model of the underlying system.
- **Not FHIR-based**: This is a genuine (b)(10) implementation, not a repackaged (g)(10) FHIR API. The CSV structure directly reflects the product's internal data model with many tables that have no FHIR equivalent (claims, consent form audit logs, SOAP note field values, clinical decision support rules, etc.).
- **Relationships**: Foreign key relationships exist between CSV files (e.g., `patient_id` linking patient CSVs to `demographics.csv`). The data mapping guide explains how to join files.
- **Media files**: Actual binary files (PDFs, images, faxes) are included alongside the CSV data, organized by type in the media/ folder.
- **A third party could reconstruct the patient record**: The export includes both structured data (CSVs) and unstructured documents (media files), with documented relationships between them. The data mapping guides specifically address how to trace data across files.

### Documentation Quality

This is **excellent** documentation for an EHI export:

- **Clear data dictionary**: The XLSX provides field-level definitions with `Export Name`, `Field`, and `Description` columns for every field in every CSV file. With ~1,796 field definitions across 107 CSV files (bulk export), this is genuinely granular.
- **Versioned and maintained**: 8 XLSX versions (v1.0–v1.8), 4 reference guide versions, and 5 glossary versions. The documentation has changelog notes (e.g., v5 added ethnicity/race subcategory files).
- **Multiple documentation formats**: XLSX data dictionary (computable), HTML web pages (browsable), PDF exports (archivable).
- **Practical guidance**: The data mapping guides show specific examples of how to join CSV files. The FAQ addresses real-world concerns (export size, blank files, processing time). The unpacking guide covers .7z extraction.
- **File structure documented**: The reference guide includes a directory tree showing the export hierarchy.
- **Actively evolving**: Documentation dates range from mid-2024 through January 2026, with regular updates adding new data elements and improving structure.

A developer could implement an import of this data based on the documentation. The XLSX data dictionary provides the schema, the reference guide explains the structure, and the data mapping guide shows how to join tables.

### Structure & Completeness

- **Granularity**: Field-level documentation for every column in every CSV, with human-readable descriptions. This is more granular than most vendors provide.
- **Data types**: Not explicitly stated in the XLSX (no "data type" column), though descriptions often imply the type (e.g., "date of birth", "boolean flag", "unique ID"). The lack of explicit data types (varchar, integer, date, etc.) is a minor gap.
- **Value sets**: Coded fields are not documented with their possible values. For example, `phone_use` is described as "type of the phone number (e.g., mobile, home)" but the complete value set isn't provided.
- **Relationships**: Foreign key relationships are not documented in the XLSX itself but are explained in the separate data mapping guide. The XLSX would benefit from a "references" column.
- **Versioning**: Clear versioning with dates indicating which export version each document applies to (e.g., "Relevant to exports completed AFTER 2/19/2025").

## Access Summary
- Final URL: https://support.drchrono.com/home/20260096536987-ehi-export-overview (no redirects)
- Status: found
- Required browser: no (all content accessible via curl, though browser needed for screenshots)
- Navigation complexity: multi_page (hub with ~10 interconnected articles)
- Anti-bot issues: none (no Cloudflare, no special headers required beyond User-Agent)

## Obstacles & Dead Ends
- The `b10-exporter-media-file-mapping` page returns 404 — appears to have been retired/moved.
- The `single-patient-and-bulk-exports` URL is a category page without article content.
- The `ehi-export` URL is also a category landing page.
- `openpyxl` Python module not available on system; XLSX analysis done via raw XML parsing of the ZIP contents.
- Reference guide v4 page content was not fully extractable via simple HTML regex — KnowledgeOwl uses complex HTML structure. Full content obtained via browser snapshot and PDF download.
