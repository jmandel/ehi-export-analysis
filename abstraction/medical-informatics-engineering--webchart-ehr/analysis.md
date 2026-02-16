# EHI Export Analysis: Medical Informatics Engineering

**Product**: WebChart EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1932.WebC.84.01.0.221117 (CHPL ID 11022)

## 1. Product Context

WebChart EHR by Medical Informatics Engineering (MIE) is a cloud-based, web-native ambulatory EHR system founded in 1995. It serves a broad range of ambulatory settings — from solo practices to multispecialty groups — with particular strength in occupational and employee health through its Enterprise Health platform, which is built on WebChart's core.

The product is a comprehensive clinical system covering:
- **Clinical documentation**: Encounters, notes, HPI, ROS, exams, vitals, diagnoses, chief complaints
- **Medications & e-prescribing**: Full EPCS support, SureScripts integration, refill management
- **Orders & results**: CPOE, lab interfaces, observation flowsheets
- **Document management**: Scanned documents, PDFs, photos, DICOM imaging, dictation/transcription
- **Scheduling**: Appointments, waiting lists, check-in
- **Patient portal**: Secure messaging, questionnaires, self-check-in
- **Immunizations**: Injection tracking, vial management, immunization registry interfaces
- **Occupational health** (major differentiator): Workplace incidents (OSHA/workers' comp), work restrictions/accommodations, health surveillance panels, audiometry, PFT, respirator fit testing, DOT exams
- **Billing-adjacent**: Insurance eligibility, fee schedules, EOB scanning, prior authorizations — but full claims/billing may be handled by external PM systems (OpenPM integration documented)

This establishes a broad baseline: the export should cover clinical, occupational health, document, medication, order, insurance, and messaging data. Full claims/billing data may not be stored natively.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-technical-details.md` (493 KB) | Raw markdown source of the main documentation page; contains DRS table (99 objects) and embedded sample JSON export | **Primary source** — most informative |
| `ehi-export-technical-details.html` (984 KB) | Rendered HTML of the same page | Redundant with markdown; used for verification |
| `sample-single-patient-export.json` (482 KB) | Complete single-patient export for test patient William S. Hart (pat_id 18) extracted from the documentation | **Primary source** — provides field-level detail |
| `ehi-export-for-end-users.md` (2.3 KB) | User-facing export instructions | Useful for understanding export mechanics |
| `ehi-export-parent.html` (389 KB) | Parent section index page | Minimal value (just links to sub-pages) |
| `screenshot-admin-export.png` (29 KB) | Admin export interface showing Patient, System (Export All), and Provider export options | Confirms export mechanics |
| `screenshot-clinical-export.png` (26 KB) | Clinical user export interface showing single-patient export only | Confirms role-based access |
| `enrichment/drs-data-dictionary.json` (11 KB) | Pre-extracted JSON of 99 DRS objects with descriptions | Useful reference; verified against source |
| `enrichment/export-schema.json` (272 KB) | Field-level schema inferred from sample export | Useful cross-reference; verified |
| `enrichment/extraction-report.json` (4 KB) | Coverage/accounting report | Verified; found minor discrepancies corrected in my analysis |

## 3. Export Mechanics

- **Format**: Custom JSON mapping directly to the product's internal MySQL database schema. Not FHIR, C-CDA, or any external standard.
- **Mechanism**: UI-driven via Control Panel → Interfaces → EHI Export
- **Single-patient**: Available to all clinical users via patient autocomplete + "Single Export" button
- **Bulk export**: Administrators/SuperUsers can export all patients system-wide ("Export All") or all patients for a specific provider ("Provider Export")
- **Output**: Single-patient export produces one JSON file; multi-patient exports produce individual JSON files per patient, compressed into a ZIP archive
- **Binary content**: Documents and DICOM images are Base64-encoded inline within the JSON
- **System requirements**: 8 GB RAM, ~100 MB disk per patient exported
- **Vendor assistance**: MIE offers help for customers lacking hardware capacity
- **Access constraints/fees**: No fees or access barriers documented beyond role-based permissions

The JSON structure uses a top-level envelope `{"request", "documentation", "db", "meta"}` where `db` is an array of patient objects. Each patient has scalar demographic fields plus nested arrays keyed as `{table_name}.{foreign_key}` (e.g., `encounters.pat_id`, `documents.pat_id`). Foreign key references to users are resolved inline — the full user record is embedded wherever a `user_id` field appears.

## 4. Export Content: What's In It

### Data dictionary scope

The vendor's documentation enumerates **99 database objects** (tables) in the Designated Record Set, presented in an HTML table with two columns: Object and Description. Of these:
- **81 objects** have one-line natural-language descriptions
- **18 objects** have names only with no description (mostly `escript_*` and `incident_*` tables)

**There is no field-level documentation.** The vendor documents table names and one-line descriptions but provides zero documentation of individual fields — no field names, no types, no descriptions, no value sets, no foreign key definitions.

### Sample export analysis

The sample export (482 KB JSON, test patient William S. Hart, pat_id 18) provides field-level visibility. Analysis reveals:
- **62 scalar fields** at the patient level (demographics, contacts, identifiers)
- **33 nested array slots** at the top level, representing different entities linked to the patient
- **17 entities with populated data** in the sample, containing a total of **510 observable fields**
- **3 entities appear in the sample but not in the DRS table**: `audit_log_chart`, `patient_warnings`, `patient_warning_dismiss` — suggesting the actual export includes slightly more than the 99 documented objects
- **60 DRS-listed entities have no representation in the sample** — because the test patient simply doesn't have data for those entities (e.g., no lab results, no observations, no injections, no DICOM images)

The `documents` entity is notable for nesting 16 sub-entity arrays within each document record (e.g., `audio.doc_id`, `dicom_studies.doc_id`, `dictation_documents.doc_id`, `pft.doc_id`), demonstrating that related data is linked hierarchically rather than at a flat top level.

### Vendor's own content organization

The DRS table lists entities alphabetically with no explicit category groupings. Based on the entity names and descriptions, I assigned categories and computed the following breakdown. The full inventory is in `analysis/full-entity-inventory.json`.

| Category | Entities | Fields Observed | Entities with Descriptions |
|---|---|---|---|
| Occupational Health | 20 | 175 | 15 |
| Demographics & Patient | 8 | 78 | 7 |
| Conditions & Procedures | 3 | 67 | 3 |
| Encounters | 9 | 60 | 9 |
| Medications & Prescriptions | 12 | 47 | 3 |
| Insurance | 3 | 34 | 3 |
| Appointments | 5 | 31 | 5 |
| Documents & Imaging | 13 | 18 | 13 |
| Observations & Results | 5 | 0 | 3 |
| Orders & Labs | 8 | 0 | 8 |
| Tasks & Messaging | 4 | 0 | 4 |
| Health Surveillance | 3 | 0 | 3 |
| Reference & Lookup | 5 | 0 | 4 |
| Immunizations | 1 | 0 | 1 |
| Clinical Alerts | 2 | 0 | 0 |
| Audit | 1 | 0 | 0 |

**Note**: "Fields Observed" is 0 for many categories because the test patient had no data for those entities. The entities exist in the DRS definition but cannot be inspected for field content without populated data.

### Top entities by field count (from sample data)

| Entity | Fields | Records in Sample | Category |
|---|---|---|---|
| `incidents` | 125 | 1 | Occupational Health |
| `patients` | 62 | 1 | Demographics & Patient |
| `encounters` | 35 | 1 | Encounters |
| `insurance_policy` | 34 | 2 | Insurance |
| `appointments` | 31 | 2 | Appointments |
| `patient_conditions` | 30 | 3 | Conditions & Procedures |
| `rxlist` | 27 | 2 | Medications & Prescriptions |
| `patient_clinical_restriction` | 26 | 1 | Occupational Health |
| `encounter_orders` | 25 | 2 | Encounters |
| `patient_conditions_family` | 21 | 2 | Conditions & Procedures |
| `rxlist_allergylist` | 20 | 2 | Medications & Prescriptions |
| `documents` | 18 | 9 | Documents & Imaging |
| `patient_procedures` | 16 | 1 | Conditions & Procedures |
| `accommodations` | 14 | 1 | Occupational Health |
| `pat_pat_relations` | 11 | 1 | Demographics & Patient |

### Entities without descriptions (18 of 99)

All 8 `escript_*` tables (e-prescribing transaction types: `escript_cancelrx`, `escript_changereq`, `escript_error`, `escript_message`, `escript_newrx`, `escript_refreq`, `escript_refres_sign`, `escript_rxfill`), 3 `incident_*` tables (`incident_bls`, `incident_condition_link`, `incident_users`), plus `nature_of_injury_types`, `observation_flags`, `observation_keys`, `patient_additional_info`, `patient_targets`, `relation_types`, `rxlist_sign`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized as a direct dump of the product's internal MySQL database tables — 99 named objects covering the patient's Designated Record Set. This is genuinely a native data model export, not a clinical summary projection.

**Strongest coverage**: Occupational Health (20 entities, 175 observable fields) — reflecting WebChart's strength in this area. The `incidents` table alone has 125 fields covering workplace injuries, OSHA classification, workers' comp details, hospitalization info, and return-to-work tracking. Supporting entities cover accommodations, clinical restrictions, audiometry, PFT, respirator details, health surveillance panels, and occupational injury codes.

**Clinical core**: Demographics (8 entities), encounters (9 entities), conditions/procedures (3 entities), medications (12 entities including 8 e-prescribing transaction tables), and documents/imaging (13 entities including DICOM support). These are well-represented as entity names in the DRS table.

**Thinner areas**: Observations/results (5 entities but 0 fields observable in sample), orders/labs (8 entities, 0 fields observable), immunizations (1 entity, 0 fields observable), tasks/messaging (4 entities, 0 fields observable). These entities exist but their field structure cannot be verified from the sample since the test patient has no data for them.

**Insurance**: Present but limited to 3 entities (`insurance_policy`, `insurance_plans`, `insurance_pre_cert`). No claims, charges, payments, or billing transaction tables are listed.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients` (62 fields), `patient_mrns`, `patient_extended_values`, `patient_additional_info`, `patient_partitions`, `pat_pat_relations`, `pat_pat_relflat` | Thorough — includes SSN, contacts, emergency contact, employment status, marital status |
| Encounters / visits | ✅ Covered | `encounters` (35 fields), `encounter_orders`, `encounter_documents`, `encounter_dictation`, `encounter_extended_values`, `encounter_extended_index`, `encounter_order_status`, `encounters_link`, `encounter_visit_types` | 9 entities covering encounter core plus extended data, orders, documents, and dictation |
| Problems / conditions / diagnoses | ✅ Covered | `patient_conditions` (30 fields incl. ICD-9, ICD-10, SNOMED, clinical_status, verification_status), `patient_conditions_family` (21 fields), `coding_link` | Includes coded diagnoses, family history, onset/conclusion dates |
| Medications / prescriptions | ✅ Covered | `rxlist` (27 fields), `rxlist_allergylist` (20 fields), `rxlist_refills`, `rxlist_sign`, plus 8 `escript_*` tables for e-prescribing transactions | Deep — covers full prescription lifecycle including e-prescribing messages |
| Allergies | ✅ Covered | `rxlist_allergylist` (20 fields) — stored alongside medications | Includes drug allergies with coded data |
| Immunizations | ✅ Covered | `injections` — listed in DRS table ("Vaccinations and injectable medications") | Entity exists; no field detail observable from sample |
| Vitals | ✅ Covered | Stored in `observations` table ("Discrete repeatable information regarding a patient (lab results, vitals, measurements, etc)") | Vitals are a subset of the generic observations entity |
| Lab results | ✅ Covered | `observations`, `observation_codes`, `lab_requests`, `lab_requests_txt` | 4 entities covering lab results and observation codes with LOINC mappings |
| Imaging / diagnostic reports | ✅ Covered | `dicom_studies`, `dicom_series`, `dicom_images` (with Base64 content), `documents` | DICOM data exported at study/series/image level |
| Procedures | ✅ Covered | `patient_procedures` (16 fields) | Includes procedure records for patients |
| Clinical notes / documents | ✅ Covered | `documents` (18 scalar fields + 16 nested sub-entity arrays), `documents_txt`, `document_attachments`, `documents_link`, `document_sign`, `document_types` | Extensive — includes document content (Base64), text content, attachments, signatures, and linked entities |
| Care plans / goals | ⚠️ Partial | No dedicated care plan entity; may be captured as documents or encounter extended values | Product likely stores care plans as documents; no named entity for structured care plans |
| Orders / referrals | ✅ Covered | `order_requests`, `order_items`, `order_list`, `order_questions`, `order_question_answers`, `order_request_icd9cm` | 6+ entities covering order lifecycle |
| Insurance / coverage | ✅ Covered | `insurance_policy` (34 fields), `insurance_plans`, `insurance_pre_cert` | Includes policy details, plan information, and prior authorizations |
| Claims / billing | ❌ Not covered | No claims, charges, payments, or billing transaction entities in the DRS | Product has billing-adjacent features (fee schedules, EOBs, revenue cycle management) but may rely on external PM systems (OpenPM) for full billing. This may be a product boundary rather than an export gap. |
| Payments | ❌ Not covered | No payment entities in the DRS | See claims/billing above |
| Consents / directives | ⚠️ Partial | No dedicated consent entity; `document_sign` covers e-signatures; advance directives likely stored as documents | Product documents e-signatures but no structured consent entity |
| Patient communications / portal messages | ✅ Covered | `conversation_messages` ("Messages between a patient or representative and their care team"), `tasks` | Messaging and task-based communication included |
| Specialty-specific (Occupational Health) | ✅ Covered | 20 entities: `incidents` (125 fields), `accommodations`, `patient_clinical_restriction`, `audio`, `audio_baseline`, `pft`, `pft_maneuver`, `panel`, `panel_membership`, `panel_decert`, `patient_panel_status`, `patient_respiratordetails`, `incident_bls/nibp/links/condition_link/extended_fields/users`, `accommodation_types`, `clinical_restriction_types`, `body_part_types`, `nature_of_injury_types` | Exceptionally thorough — this is one of the most detailed specialty data exports observed |

## 6. Documentation Quality

**Strengths:**
- Clear, well-structured documentation on a modern Hugo-based documentation site (docs.webchartnow.com)
- Source markdown available on GitHub (mieweb/docs repository), enabling machine parsing
- Explicit regulatory references to 45 CFR 164.501 and §170.315(b)(10) — the vendor understands the requirement
- Complete sample export (482 KB JSON) for a test patient with realistic data across multiple entity types
- 99 database objects enumerated with one-line descriptions for 81 of them
- Export instructions with screenshots for both admin and clinical user roles
- System requirements documented (8 GB RAM, ~100 MB/patient)
- Multi-patient export behavior documented (ZIP of individual JSON files)

**Weaknesses:**
- **No field-level documentation whatsoever**: The data dictionary is table-level only. Of the 510+ fields observable in the sample, zero have vendor-provided descriptions. A developer must infer field meanings from names alone (e.g., `onset_date_fuzzy`, `header_item`, `pmh`, `is_tmp`).
- **No data types specified**: All values in the JSON are serialized as strings (even IDs and dates), with no schema defining intended types.
- **No value sets or code definitions**: Coded fields like `status`, `confirmed`, `canceled`, `osha_classification`, `case_type` use numeric or short-text codes without documenting possible values.
- **No relationship/ERD documentation**: Foreign key relationships are implied by the `{table}.{fk}` naming convention but not formally documented.
- **18 of 99 entities have no description at all** — just names. All 8 `escript_*` tables and several incident-related tables lack even a one-line description.
- **Single test patient**: Only one sample patient is provided, and many entity types are empty for that patient (observations, labs, injections, orders, DICOM, etc.)
- **Date conventions undocumented**: Sentinel values like `0000-00-00 00:00:00` appear without explanation.

**Developer usability**: A developer could reconstruct the basic record structure from the sample export, but would need significant reverse-engineering for coded fields, status values, date handling, and the meaning of fields with non-obvious names. The documentation is adequate for understanding *what data is included* but insufficient for building a reliable import without access to the source system.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native database model export covering the product's internal MySQL tables. It is not a FHIR or C-CDA projection — it exports the vendor's own data structures, which naturally captures data (especially occupational health detail) that no standard clinical data model would represent. With 99 documented entities spanning demographics, encounters, medications, documents, orders, occupational health, insurance, messaging, and more, this export covers most of what the product stores about patients.

### Key Findings

1. **Genuine native data model export**: The JSON output maps directly to WebChart's MySQL tables, covering 99 DRS objects across clinical, occupational health, document management, and administrative domains. This is exactly what §170.315(b)(10) intends — not a clinical summary repackaging. (Source: `ehi-export-technical-details.md`, DRS table)

2. **Exceptionally strong occupational health coverage**: 20 entities and 175+ observable fields dedicated to workplace incidents, accommodations, clinical restrictions, audiometry, PFT, health surveillance panels, and workers' compensation. The `incidents` table alone has 125 fields. This is the most detailed specialty-specific export coverage in the analysis set. (Source: `sample-single-patient-export.json`, incidents record)

3. **Documentation is table-level only — zero field-level documentation**: Despite exporting 500+ fields, the vendor provides no field names, types, descriptions, value sets, or relationship definitions beyond the table-level DRS listing. This is a significant documentation gap. (Source: `ehi-export-technical-details.md`, entire DRS section)

4. **Billing/claims data absent**: No entities for charges, claims, payments, EOBs, or billing transactions appear in the export. The product has billing-adjacent features (insurance eligibility, fee schedules, prior authorizations) and markets revenue cycle management, but detailed billing may reside in external PM systems. (Source: DRS table — no billing entities present)

5. **Broad domain coverage with bulk export support**: Single-patient, per-provider, and system-wide export available through the UI. Supports 15+ EHI domains. Binary content (documents, DICOM images) included inline as Base64. (Source: `ehi-export-for-end-users.md`, screenshots)

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   JSON (proprietary schema mapping to MySQL tables)
Model type:      Native database
Entities:        99 (documented) / 102 (observed in sample)
Fields:          510+ observed (from 17 populated entities in sample)
Descriptions:    81/99 DRS entities (82%) have table-level descriptions; 0% field-level descriptions
Sample data:     Yes (1 test patient, 482 KB)
Bulk export:     Yes (system-wide and per-provider via admin UI)
Domains covered: 14 of 17 applicable domains
```

### Bottom Line

WebChart EHR provides one of the better (b)(10) exports — a genuine native database dump covering 99 tables across clinical, occupational health, document, medication, and administrative domains, with both single-patient and bulk export capabilities. The single biggest weakness is the complete absence of field-level documentation: a developer receives 500+ fields with no descriptions, no types, no value sets, and must reverse-engineer meaning from field names and sample values alone. The export itself is broad and structurally sound; the documentation needs substantial improvement to make the exported data independently usable.
