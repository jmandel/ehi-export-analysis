# EHI Export Analysis: drchrono Inc.

**Product**: drchrono EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.99.04.2897.DRCH.11.03.1.220531

## 1. Product Context

drchrono EHR is a cloud-based, all-in-one EHR and practice management platform targeting ambulatory care physicians at small to mid-sized independent practices. Acquired by EverCommerce in 2021, it serves 4,600+ practices and 17 million+ patients. The single certified product (v11.0) integrates:

- **Clinical EHR**: Customizable note templates for 20+ specialties, problem lists, medications, allergies, procedures, vitals, care plans, implantable devices, lab ordering/results
- **E-Prescribing**: eRx, EPCS, electronic prior authorization
- **Practice Management**: Scheduling, appointment reminders, task management, patient check-in kiosk
- **Billing & RCM**: Claims submission, fee schedules, eligibility verification, ERA, denial management, patient payments, payment plans, superbills
- **Patient Portal (OnPatient)**: Secure messaging, intake/consent forms, appointment scheduling, payments, telehealth
- **Document Management**: eFax, referrals, uploaded documents
- **Interoperability**: C-CDA, FHIR R4 API, Direct messaging, open REST API

The product is certified across 35+ ONC criteria including (b)(10). Per the API documentation, it stores data across ~27 endpoint groups covering demographics, clinical data, billing, insurance, messaging, and documents. This is the baseline for what a complete (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `drchrono-ehi-export-documentation-v18.xlsx` (170 KB) | Latest XLSX data dictionary with 2 sheets: Single Patient Export (98 entities, 1,586 fields) and Bulk Patient Export (108 entities, 1,795 fields). Each field has Export Name, Field, and Description columns. | **Most informative** — primary data dictionary |
| `reference-guide-v4.html` / `.pdf` | Technical reference (eff. 10/21/2025): file naming, directory structure, export process, security model, data element listing | **Highly informative** — explains mechanics |
| `glossary-data-elements-v5.html` / `.pdf` | Glossary (eff. 1/28/2026): organized by exporter type (Doctor, Patient, Practice Group, Media, ReadMe) with entity descriptions | **Informative** — provides entity-level context |
| `creating-a-new-request.html` | UI guide for single-patient and bulk export requests, permissions, dashboard navigation | Informative — explains access mechanism |
| `ehi-export-overview.html` | Landing page describing self-service EHI export feature | Orientation only |
| `ehi-export-faq.html` | FAQ: processing time (up to 14 business days for bulk), export sizes (200+ GB), file types, blank CSVs | Useful for mechanics |
| `data-mapping-v2.html` | Instructions for tracing patient data across CSV exports using foreign key relationships | Informative — documents relationships |
| `folder-contents.html` | Hub page linking to all 8 versioned XLSX data dictionaries (v1.0–v1.8) | Index only |
| `unpacking-export-files.html` | Instructions for extracting .7z multi-part archives | Minor |
| 7 earlier XLSX versions (v1.0–v1.7) | Prior versions of data dictionary showing evolution | Useful for provenance |
| 6 screenshots | Visual captures of documentation pages | Supporting evidence |

## 3. Export Mechanics

- **Format**: CSV files compiled into a ZIP archive (or .7z multi-part for large exports)
- **Mechanism**: Self-service UI within drchrono EHR (Reports → EHI Data Export). Single-patient exports are real-time; bulk/practice-level exports are queued and may take up to 14 business days.
- **Single-patient**: Yes — initiated by provider with EHI Export permission enabled. Real-time download.
- **Bulk/practice-level**: Yes — exports all patients. Requires a request form with practice contact info, reason for export, etc. DrChrono processes internally. Exports are batched in groups of 50 patients, producing numbered CSV files (e.g., `allergies_1.csv`, `allergies_2.csv`).
- **Access constraints**: Requires EHI Export permission enabled in Account Settings. Files available for download for 30 days, then archived and permanently deleted.
- **Fees**: Bulk exports can optionally be delivered on a hard drive for an additional cost if the practice cannot meet technical requirements for download.
- **Directory structure**: Organized into `doctors/`, `patients/`, `practice_group/`, and `Media/` subfolders, plus a `README.txt`.

## 4. Export Content: What's In It

### Data Dictionary Overview

The XLSX data dictionary v1.8 provides field-level documentation for every CSV file in the export. It has two sheets:

| Sheet | Entities | Fields | Fields with Descriptions | % Described |
|---|---|---|---|---|
| Single Patient Export | 98 | 1,586 | 1,586 | 100.0% |
| Bulk Patient Export | 108 | 1,795 | 1,754 | 97.7% |

The bulk export includes 10 additional entities (practice-level reference data like `offices.csv`, `practice_group.csv`, `custom_vital_type.csv`, etc.) not present in the single-patient export.

Of the 1,795 bulk export fields, 41 lack descriptions — concentrated in just 2 entities: `doctor_message.csv` (22 fields, 0 described) and `doctor_message_log.csv` (7 fields, 0 described), plus a parsing artifact entity with 9 undescribed fields and 3 fields in `race_subcategories_1.csv`.

Each field entry provides: **Export Name** (CSV filename), **Field** (column name), and **Description** (plain-text explanation). No explicit data types, constraints, or value sets are documented, but descriptions are generally clear enough to understand the data (e.g., "The unique identifier for the patient vaccination record" or "Date the appointment was scheduled for").

### Media Files

In addition to CSV data, the export includes binary media files organized into subfolders:
- `clinical/` — clinical documents and uploaded patient documents
- `dr_message_attachment/` — doctor message file attachments
- `hipaa_forms/` — consent form templates
- `education/` — custom patient education resources
- `message_attachment/` — DIRECT secure message attachments
- `patient_import/` — imported CCDA XML files
- `inbound_faxes/` — inbound referral files
- `LabOrderDocumentFiles/` — lab order document PDFs
- `referrals/` — outbound referral files

### Vendor's Own Content Organization

The vendor organizes entities into four "exporters" documented in the Glossary v5:

**Doctor Exporter** (8 entities in bulk): Practice-level reference data.
**Practice Group Exporter** (3 entities): Lab order codes, practice group info.
**Patient Exporter** (~95 entities): Core patient data across all domains.
**Media Exporter** (9 folder types): Binary files and documents.

#### Top 20 entities by field count (Bulk Patient Export):

| Entity | Fields | Described | Category |
|---|---|---|---|
| demographics.csv | 180 | 180 | Demographics |
| clinical_decision_support_rules.csv | 117 | 117 | Clinical Decision Support |
| prescription.csv | 59 | 59 | Medications |
| patient_drug.csv | 50 | 50 | Medications |
| auto_accident_insurance.csv | 48 | 48 | Insurance |
| education_resource.csv | 44 | 44 | Education |
| patient_vaccination_record.csv | 37 | 37 | Immunizations |
| soap_note_custom_report.csv | 36 | 36 | Clinical Notes |
| primary_hospital_insurance.csv | 35 | 35 | Insurance |
| claims.csv | 31 | 31 | Claims / Billing |
| payments_insurance.csv | 29 | 29 | Claims / Billing |
| soap_note_line_item_field_type.csv | 29 | 29 | Clinical Notes |
| history_message.csv | 26 | 26 | Communications |
| consent_form_signatures.csv | 25 | 25 | Consent Forms |
| lab_result.csv | 25 | 25 | Lab Results |
| payments_patient.csv | 25 | 25 | Claims / Billing |
| problems.csv | 25 | 25 | Problems |
| system_vitals.csv | 25 | 25 | Vitals |
| uploaded_documents.csv | 25 | 25 | Clinical Notes |
| allergies.csv | 24 | 24 | Allergies |

The full entity inventory (108 entities, all fields) is saved in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized into domain categories by entity count and field depth:

| Domain | Entities | Fields | Fields Described |
|---|---|---|---|
| Demographics | 10 | 262 | 259 |
| Clinical Notes / Documents | 11 | 177 | 177 |
| Medications / Prescriptions | 5 | 149 | 149 |
| Insurance / Coverage | 5 | 137 | 137 |
| Clinical Decision Support | 2 | 128 | 128 |
| Communications / Messages | 9 | 121 | 92 |
| Lab Results | 8 | 118 | 118 |
| Claims / Billing | 4 | 109 | 109 |
| Education | 3 | 58 | 58 |
| Provider / Practice | 5 | 56 | 56 |
| Care Plans / Goals | 8 | 53 | 53 |
| Vitals | 4 | 52 | 52 |
| Devices | 3 | 49 | 49 |
| Consent Forms | 4 | 48 | 48 |
| Immunizations | 2 | 40 | 40 |
| Care Team | 4 | 37 | 37 |
| Referrals | 2 | 31 | 31 |
| Functional / Mental Status | 6 | 30 | 30 |
| Allergies | 2 | 28 | 28 |
| Encounters / Visits | 2 | 27 | 27 |
| Problems / Conditions | 1 | 25 | 25 |
| Family History | 2 | 18 | 18 |
| Imaging / Diagnostic Reports | 1 | 12 | 12 |
| Patient Flags | 1 | 12 | 12 |
| Procedures | 1 | 7 | 7 |

**Richest domains**: Demographics (180 fields for the demographics.csv alone — very deep), Medications (109 fields across prescriptions and patient drugs), Insurance (137 fields across 5 insurance-type entities), and Claims/Billing (109 fields across claims, insurance payments, patient payments, and cost estimator).

**Thinnest domains**: Procedures (7 fields in a single entity — notably sparse for a practice management system), Encounters/Visits (27 fields — appointments are present but encounter-level clinical data is captured via clinical notes), and Imaging (12 fields — single entity for imaging orders only).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `demographics.csv` (180 fields), `tribal_affiliations.csv`, `ethnicity_subcategories_1.csv`, `race_subcategories_1.csv`, `uscdi_occupation_code.csv`, `uscdi_industry_code.csv`, `additional_responsible_party.csv`, `responsible_party_address.csv` | Exceptionally thorough — 180 fields for demographics alone, plus USCDI-specific occupation/industry codes and tribal affiliations |
| Encounters / Visits | ✅ Covered | `appointments.csv` (19 fields), `case_report_encounters.csv` (8 fields) | Appointments are exported; clinical encounter data captured via clinical notes |
| Problems / Conditions | ✅ Covered | `problems.csv` (25 fields) | Solid — includes ICD codes, onset, status, SNOMED mappings |
| Medications / Prescriptions | ✅ Covered | `prescription.csv` (59 fields), `patient_drug.csv` (50 fields), `prescription_message.csv` (18 fields), `cover_my_meds_pa_request.csv` (15 fields), `pa_request_medication.csv` (7 fields) | Deep — includes prior auth requests, pharmacy messaging |
| Allergies | ✅ Covered | `allergies.csv` (24 fields), `allergy_snomed_code_mapping.csv` (4 fields) | Thorough with SNOMED mappings |
| Immunizations | ✅ Covered | `patient_vaccination_record.csv` (37 fields), `patientvaccinerecord_doses.csv` (3 fields), `iz_patient_demographic.csv` (11 fields) | Deep — includes dose-level data |
| Vitals | ✅ Covered | `system_vitals.csv` (25 fields), `custom_vital_value.csv` (7 fields), `custom_vital_type.csv` (17 fields), `system_vitals_author.csv` (3 fields) | Thorough — includes custom vitals |
| Lab Results | ✅ Covered | `lab_result.csv` (25 fields), `patient_lab_result_set.csv` (20 fields), `lab_order.csv` (19 fields), `lab_order_document.csv` (10 fields), `lab_order_icd10_codes.csv` (3 fields), `lab_result_author.csv` (3 fields) | Deep — 8 entities covering orders, results, documents, ICD10 codes |
| Imaging / Diagnostic Reports | ⚠️ Partial | `patient_imaging_order.csv` (12 fields) | Imaging orders present but only a single thin entity; no imaging results/reports entity |
| Procedures | ⚠️ Partial | `procedures.csv` (7 fields) | Present but notably sparse (7 fields) for a PM system that supports procedure documentation |
| Clinical Notes / Documents | ✅ Covered | `clinical_notes.csv` (15 fields), `clinical_observation.csv` (7 fields), `custom_clinical_note_sections.csv` (13 fields), `note_section_comments.csv` (6 fields), `soap_note_line_item_field_value.csv` (6 fields), `soap_note_line_item_field_type.csv` (29 fields), `soap_note_custom_report.csv` (36 fields), `uploaded_documents.csv` (25 fields), `clinical_list.csv` (19 fields); plus Media folder with actual document files | Very thorough — structured SOAP note data, custom sections, plus binary documents |
| Care Plans / Goals | ✅ Covered | 8 entities: `care_plans.csv`, `care_plan_goals.csv`, `care_plan_interventions.csv`, `care_plan_objectives.csv`, etc. (53 fields total) | Well-structured with goals, interventions, attached codes, authors |
| Orders / Referrals | ✅ Covered | `inbound_referrals.csv` (13 fields), `outbound_referrals.csv` (18 fields), `patient_device_orders.csv` (24 fields), `patient_imaging_order.csv` (12 fields), `lab_order.csv` (19 fields) | Good coverage across referral types and order types |
| Insurance / Coverage | ✅ Covered | `primary_hospital_insurance.csv` (35 fields), `auto_accident_insurance.csv` (48 fields), `auto_accident_insurance_accident.csv` (23 fields), `workers_comp_insurance.csv` (17 fields), `insurance_authorizations.csv` (14 fields) | Deep — multiple insurance types plus authorizations |
| Claims / Billing | ✅ Covered | `claims.csv` (31 fields), `payments_insurance.csv` (29 fields), `payments_patient.csv` (25 fields), `patient_cost_estimator.csv` (24 fields) | Genuinely goes beyond USCDI — includes claims, insurance payments, patient payments, cost estimator |
| Payments | ✅ Covered | `payments_insurance.csv` (29 fields), `payments_patient.csv` (25 fields) | Both insurance and patient payment records included |
| Consents / Directives | ✅ Covered | `consent_forms.csv` (10 fields), `consent_form_assignments.csv` (6 fields), `consent_form_signatures.csv` (25 fields), `consent_form_signature_audit_logs.csv` (7 fields); plus Media `hipaa_forms/` | Thorough — includes form definitions, assignments, signatures, and audit logs |
| Patient Communications / Portal Messages | ✅ Covered | `doctor_message.csv` (22 fields), `patient_message.csv` (12 fields), `patient_message_attachment.csv` (14 fields), `direct_message.csv` (19 fields), `direct_message_attachment.csv` (5 fields), `history_message.csv` (26 fields), `communication_log.csv` (9 fields), `outgoing_patient_message_status.csv` (7 fields) | Very thorough — 9 entities covering doctor messages, patient messages, DIRECT messages, communication logs, message attachments |
| Family History | ✅ Covered | `family_history.csv` (14 fields), `relationship.csv` (4 fields), `person.csv` (13 fields) | Includes clinical observations and person details |
| Care Team | ✅ Covered | `care_team_member.csv` (4 fields), `doctor_staff_Care_team_members.csv` (13 fields), `external_Care_team_members.csv` (13 fields), `patient_as_care_team_members.csv` (7 fields) | Multiple member types documented |
| Devices | ✅ Covered | `implantable_devices.csv` (22 fields), `implantable_device_authors.csv` (3 fields), `patient_device_orders.csv` (24 fields) | Includes devices and device orders |
| Functional / Mental / Social Status | ✅ Covered | `functional_statuses.csv` (8 fields), `mental_statuses.csv` (7 fields), `social_history.csv` (6 fields), plus author entities | Health status assessments beyond USCDI floor |

**Notable gaps relative to product capabilities**:
- **Fee schedules / billing profiles**: The drchrono API exposes `/api/fee_schedules` and `/api/billing_profiles`, but no corresponding entity appears in the export. These are reference data that affect billing decisions.
- **Eligibility checks**: The API exposes `/api/eligibility_checks` but no export entity exists for this data.
- **Tasks**: The product has a task management system (API: `/api/tasks`, `/api/task_categories`, etc.) but no task-related entity appears in the export.
- **Superbills / line items**: The API exposes `/api/line_items` and the product generates HCFA 1500 forms, but no explicit superbill or line item entity is in the export (though claims.csv and payments may partially cover this).
- **Patient portal access records**: Not explicitly exported.

These gaps are relatively minor — the export covers the major patient-facing data domains including billing, which many vendors omit entirely.

## 6. Documentation Quality

**Strengths**:
- **Comprehensive XLSX data dictionary**: 108 entities with 1,795 fields, 97.7% with plain-text descriptions. This is above average for EHI export documentation.
- **Versioned documentation**: 8 versions of the data dictionary (v1.0–v1.8) show active maintenance and evolution. The glossary is on v5 and the reference guide on v4.
- **Multiple documentation types**: Reference guide (structure + mechanics), glossary (entity descriptions), data mapping guide (foreign key relationships), FAQ (practical questions), and the XLSX data dictionary (field-level detail).
- **Export process documentation**: Clear instructions for both single-patient and bulk exports, including permissions setup, dashboard navigation, and download procedures.
- **Media file documentation**: The glossary describes what binary files are included in each Media subfolder.

**Weaknesses**:
- **No explicit data types**: The XLSX provides field names and descriptions but does not document data types (string, integer, date, boolean), constraints, or max lengths.
- **No value sets or coded values**: Fields that contain coded values (e.g., status fields, type fields) do not document the allowed values.
- **No foreign key documentation in XLSX**: While the data mapping guide v2 explains how to trace relationships, the XLSX itself doesn't document foreign keys or relationships between entities.
- **Two entities without descriptions**: `doctor_message.csv` (22 fields) and `doctor_message_log.csv` (7 fields) have zero field descriptions — a notable omission for messaging data.
- **No sample data**: No sample export files are provided in the documentation.
- **No machine-readable schema**: The XLSX is the closest thing to a machine-readable artifact, but there's no JSON schema, SQL DDL, or similar formal schema definition.

**Usability**: A developer could build an import from this documentation with moderate effort. The field names are generally self-explanatory, the descriptions add useful context, and the data mapping guide helps with relationships. The lack of data types and value sets would require some trial-and-error with actual export data.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

drchrono's EHI export demonstrably covers the breadth of data domains the product stores. With 108 entities and 1,795 fields across 25 data domains, it goes well beyond USCDI to include:
- **Billing and revenue cycle**: claims, insurance payments, patient payments, cost estimator (109 fields total)
- **Insurance**: 5 entities covering primary, auto accident, workers' comp, and authorization data (137 fields)
- **Patient communications**: 9 entities covering doctor messages, patient portal messages, DIRECT messages, and communication logs (121 fields)
- **Consent forms**: 4 entities with form definitions, assignments, signatures, and audit logs (48 fields)
- **Clinical notes at the SOAP-note structural level**: custom sections, field types, field values, line items (177 fields across 11 entities)
- **Media files**: actual document binaries including faxes, clinical documents, lab PDFs, referrals, and message attachments

The only notable gaps (fee schedules, eligibility checks, tasks, line items) are relatively minor reference or operational data — not core designated record set items. For an ambulatory EHR targeting independent practices, this export covers the relevant breadth.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged C-CDA or FHIR export:
- **Native CSV format** reflecting the product's internal data model, not a projection into FHIR or C-CDA
- **108 entities** far exceed what C-CDA sections or FHIR Bulk Data would provide
- **Billing, insurance, and payment data** are present — these are not in any standard clinical exchange format
- **Active versioning**: 8 data dictionary versions (v1.0–v1.8) and 5 glossary versions show ongoing development effort specifically for this export
- **Dedicated UI**: Self-service export functionality with its own dashboard, permissions, and audit logging
- **Media files**: Binary document export alongside structured CSV data
- **Documentation explicitly references (b)(10)**: The reference guide cites CFR § 170.315(b)(10)(i)(A) and (b)(10)(ii)

### Key Findings

1. **Genuinely comprehensive export with billing coverage**: drchrono exports claims, insurance payments, patient payments, and cost estimator data alongside clinical data — a meaningful signal that this is a real (b)(10) effort, not a clinical summary repackaged. (Source: `drchrono-ehi-export-documentation-v18.xlsx`, Bulk Patient Export sheet)

2. **Deep demographics model**: 180 fields for demographics alone, plus dedicated entities for tribal affiliations, ethnicity subcategories, race subcategories, and USCDI occupation/industry codes. This is one of the most detailed demographics exports observed. (Source: `demographics.csv` entity in XLSX)

3. **Strong documentation maturity**: 8 versions of the data dictionary, 5 versions of the glossary, and 4 versions of the reference guide demonstrate active maintenance. The latest XLSX (v1.8) has 97.7% of fields described — only 41 of 1,795 fields lack descriptions. (Source: `drchrono-ehi-export-documentation-v18.xlsx`)

4. **Procedures entity is thin**: Only 7 fields for procedures, which seems sparse for a product that supports procedure documentation and billing. This may indicate that procedure detail is captured within SOAP notes rather than in a standalone entity. (Source: `procedures.csv` entity in XLSX)

5. **No data types or value sets in documentation**: While descriptions are present, the XLSX does not document data types, constraints, or allowed coded values — a gap that would slow import development. (Source: `drchrono-ehi-export-documentation-v18.xlsx` column structure)

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (ZIP/7z archive) + binary media files
Entities:        108 (bulk), 98 (single patient)
Fields:          1,795 (bulk), 1,586 (single patient)
Descriptions:    97.7% of fields have descriptions (bulk)
Sample data:     No
Bulk export:     Yes (up to 14 business days processing)
Domains covered: 23 of 25 applicable domains (imaging and procedures partial)
```

### Bottom Line

drchrono delivers a genuinely comprehensive (b)(10) export that covers clinical, billing, insurance, communications, and document data across 108 CSV entities with 1,795 documented fields. The export is purpose-built with its own UI, versioned documentation, and active maintenance. The single biggest strength is the inclusion of billing and insurance data (4 billing entities, 5 insurance entities) alongside deep clinical data — a clear signal this is not a repackaged clinical exchange. The main gaps are the absence of data types/value sets in the documentation and a few thin entities (procedures at 7 fields), but overall this is one of the stronger (b)(10) implementations observed.
