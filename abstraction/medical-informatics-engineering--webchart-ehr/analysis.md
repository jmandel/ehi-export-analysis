# EHI Export Analysis: Medical Informatics Engineering

**Product**: WebChart EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1932.WebC.84.01.0.221117

## 1. Product Context

WebChart EHR is a cloud-based ambulatory EHR developed by Medical Informatics Engineering (MIE), headquartered in Fort Wayne, Indiana. It serves small to mid-sized ambulatory practices across many specialties, with a particular strength in occupational/employee health through the related Enterprise Health product built on WebChart's core platform.

**Key capabilities relevant to export completeness:**
- **Clinical:** Full encounter documentation, problem lists, medications (with EPCS e-prescribing), allergies, vitals, lab results, orders/referrals, immunizations, clinical notes, care plans, procedures, family history
- **Documents:** Document management (scanned, PDFs, photos, forms), DICOM imaging, dictation/transcription
- **Occupational health:** Workplace injury/incident tracking (OSHA cases), work restrictions/accommodations, health surveillance panels, audiometry, PFT, respirator fit testing, medical clearances
- **Scheduling:** Appointment management with multiple views
- **Insurance:** Insurance eligibility, policy management, prior authorizations
- **Billing-adjacent:** Fee schedules, pending billing reports, EOB scanning, integration with billing/PM systems (OpenPM); revenue cycle management described on marketing site, though full claims processing may rely on external systems
- **Patient portal:** Secure messaging, health questionnaires, self check-in
- **Tasks & communications:** User-to-user task management, conversation messages

The product is broadly certified with 40+ ONC criteria including (b)(10) EHI Export.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-technical-details.md` (493 KB, 5,701 lines) | Raw markdown source of the EHI Export Technical Details page. Contains: DRS content table (99 objects with descriptions), full sample JSON export for a test patient, system requirements. **Primary artifact.** | ★★★ High |
| `downloads/ehi-export-technical-details.html` (984 KB) | Rendered HTML version of the same page. | ★★ (redundant with .md) |
| `downloads/sample-single-patient-export.json` (482 KB) | Complete sample single-patient EHI export in JSON for test patient William S. Hart (pat_id 18). Contains 61 patient scalar fields + 33 nested object types. | ★★★ High |
| `downloads/ehi-export-for-end-users.md` (2.3 KB) | End-user instructions for performing exports. Documents single-patient, provider-based, and system-wide export capabilities. | ★★ Medium |
| `downloads/ehi-export-for-end-users.html` (396 KB) | Rendered HTML version of end-user page. | ★ (redundant) |
| `downloads/ehi-export-parent.html` (389 KB) | Parent index page linking to sub-pages. | ★ Low |
| `downloads/screenshot-admin-export.png` (29 KB) | Screenshot showing admin export interface with Patient, System (Export All), and Provider export options. | ★★ Medium |
| `downloads/screenshot-clinical-export.png` (26 KB) | Screenshot showing clinical user single-patient export interface. | ★ Low |
| `downloads/enrichment/drs-data-dictionary.json` (11 KB) | Previously extracted JSON of 99 DRS objects from the table. | ★★ (reference) |
| `downloads/enrichment/export-schema.json` (272 KB) | Previously inferred field-level schema from sample export. | ★★ (reference) |
| `downloads/enrichment/extraction-report.json` (3.9 KB) | Coverage report noting gaps between DRS table and sample. | ★★ (reference) |

## 3. Export Mechanics

- **Format:** JSON (ECMA-404). Each patient's DRS is exported as a single JSON file. Multi-patient exports are compressed into a ZIP file containing one JSON file per patient.
- **Mechanism:** UI-based. Accessed via Control Panel → Interfaces → EHI Export.
- **Single-patient:** Yes — any clinical user can export a single patient via autocomplete selection.
- **Bulk capability:** Yes — administrators/superusers can:
  - Export all patients for a single provider (Provider Export)
  - Export all patients in the system (Export All / System Export)
- **Access constraints:** Clinical users can only export patients they have access to. System-wide export requires admin/superuser permissions.
- **System requirements:** 8 GB RAM, 100 MB available disk per patient. MIE offers assistance if the customer lacks adequate hardware.
- **Fees:** Not mentioned in documentation.
- **Documentation link:** Export includes a `documentation` field pointing to `https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/technical-details`

## 4. Export Content: What's In It

### Data Dictionary Overview

The DRS content table in the Technical Details documentation lists **99 named objects** (database entities/tables) with brief descriptions. Of these:
- **81 objects** (82%) have descriptions
- **18 objects** (18%) have empty descriptions (primarily `escript_*` e-prescribing objects, some incident/occupational objects, and a few miscellaneous ones)

The sample export reveals **3 additional objects** not in the DRS table: `audit_log_chart`, `patient_warning_dismiss`, and `patient_warnings`, bringing the total to **102 unique objects** (excluding `revised_by` which is an inline user reference, not a standalone entity).

### Field-Level Detail

The documentation provides **no per-field data dictionary**. There are no field names, types, descriptions, value sets, foreign key relationships, or constraints documented anywhere. The only field-level information comes from the sample JSON export, which provides field names and sample values for 18 of the 99 DRS objects (those where the test patient had data).

From the sample export, we can observe **581 distinct fields** across the 18 populated objects. The remaining 81 objects have no field-level visibility. Types must be inferred from sample values; no formal schema exists.

### Vendor's own content organization

The vendor organizes the DRS objects in a flat table (no explicit categories). Based on naming conventions and descriptions, I've grouped them into functional categories:

| Category | Entities | Fields (from sample) | Key Objects |
|---|---|---|---|
| Occupational Health | 22 | 165 | `incidents` (125 fields), `accommodations`, `patient_clinical_restriction`, `audio`, `audio_baseline`, `pft`, `pft_maneuver`, `panel`, `panel_membership`, `patient_respiratordetails` |
| Demographics & Administration | 12 | 87 | `patients` (61 fields), `patient_mrns`, `patient_extended_values`, `pat_pat_relations`, `users`, `locations` |
| Medications & Prescriptions | 12 | 47 | `rxlist` (27 fields), `rxlist_allergylist` (20 fields), `rxlist_refills`, 8 `escript_*` e-prescribing objects |
| Documents & Dictation | 10 | 34 | `documents` (34 fields), `document_attachments`, `dictation`, `documents_txt`, `document_sign` |
| Encounters | 9 | 60 | `encounters` (35 fields), `encounter_orders` (25 fields), `encounter_extended_values`, `encounters_link` |
| Orders & Lab Results | 8 | 0 | `order_requests`, `order_items`, `lab_requests`, `order_questions`, `order_question_answers` |
| Scheduling | 5 | 31 | `appointments` (31 fields), `apt_types`, `multi_referrer_apt`, `multi_resource_apt` |
| Observations & Results | 5 | 0 | `observations`, `observation_codes`, `observation_flags`, `observation_keys`, `observations_snomed` |
| Conditions & Procedures | 3 | 67 | `patient_conditions` (30 fields), `patient_conditions_family` (21 fields), `patient_procedures` (16 fields) |
| Insurance & Coverage | 3 | 34 | `insurance_policy` (34 fields), `insurance_plans`, `insurance_pre_cert` |
| Communications & Tasks | 3 | 0 | `conversation_messages`, `tasks`, `tasklist_extended_values` |
| Imaging (DICOM) | 3 | 0 | `dicom_images`, `dicom_series`, `dicom_studies` |
| Immunizations | 1 | 0 | `injections` |
| Coding & Terminology | 1 | 0 | `coding_link` |
| Clinical Alerts | 2 | 0 | `patient_warnings`, `patient_warning_dismiss` |
| Audit | 1 | 0 | `audit_log_chart` |

**Representative entities from the sample export** (showing field-level detail available):

| Entity | Fields | Sample Records | Notable Fields |
|---|---|---|---|
| `incidents` | 125 | 1 | `case_number`, `case_related_to_employment`, `employer_notified_date`, `osha_*` fields, `disability_*`, `lost_time_*`, etc. |
| `patients` | 61 | 1 | `first_name`, `last_name`, `birth_date`, `death_date`, `ssn`, `marital_status`, `race`, `sex`, `email`, `cell_phone`, etc. |
| `encounters` | 35 | 1 | `chief_complaint`, `accident_code`, `closed`, `create_date`, `discharge_date`, `location_id`, etc. |
| `insurance_policy` | 34 | 2 | `group_number`, `holder_*` fields, `start_datetime`, `end_datetime`, `policy_number`, etc. |
| `documents` | 34 | 9 | `doc_id`, `doc_type`, `enter_date`, `origin_id`, `service_date`, `subject`, content is Base64-encoded |
| `appointments` | 31 | 2 | `cancel_code`, `confirmed`, `contact`, `duration`, `resource_id`, `starttime`, `visit_type`, etc. |
| `patient_conditions` | 30 | 3 | `code`, `clinical_status`, `description`, `onset_date`, `conclusion_date`, `verification_status` |
| `rxlist` | 27 | 2 | `drug_name`, `drug_id`, `start_date`, `end_date`, `sig`, `indication`, `refills` |
| `patient_clinical_restriction` | 26 | 1 | `restriction_type`, `start_date`, `end_date`, `allowed_weight`, `disability`, `email_notification` |
| `encounter_orders` | 25 | 2 | `concept_id`, `completed_dt`, `due_date`, `ordering_user`, `status` |
| `patient_conditions_family` | 21 | 2 | `code`, `description`, `onset_date`, family member info |
| `rxlist_allergylist` | 20 | 2 | `allergy_name`, `reaction`, `severity`, `intolerance`, `onset_date` |

The full entity inventory with all fields is available in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is MIE's **native database model** exposed as JSON — these are the actual internal table structures, not a projection into any standard format. This is evident from:
- Object names match internal database table naming conventions (e.g., `rxlist`, `pat_pat_relflat`, `escript_newrx`)
- Fields include internal IDs (`pat_id`, `doc_id`, `enc_id`), interface metadata (`interface`, `ext_id`), and audit fields (`create_date`, `edit_date`, `revised_by`)
- Foreign key relationships are embedded (e.g., `insurance_policy` linked via `pat_id` and `holder_pat_id`)

**Strongest areas:**
- **Occupational health** is exceptionally deep: 22 entities covering incidents (125 fields including full OSHA case detail), work restrictions, accommodations, audiometry, PFT, panel surveillance, respirator details, and medical decertification. This reflects the product's core strength.
- **Demographics** has 61 patient fields including emergency contacts, employment, SSN, multiple identifiers.
- **Insurance** includes policy details, pre-certifications, and plan information.
- **Encounters** have extended value support for capturing arbitrary additional data.

**Notable breadth:**
- E-prescribing has 8 dedicated objects (`escript_*`) covering the full lifecycle: new Rx, refill requests/responses, cancellations, change requests, fill notifications, and errors.
- Documents include content in Base64, with attachments, e-signature tracking, and linking.
- DICOM imaging has dedicated objects for studies, series, and image data.
- Conversation messages, tasks, and patient warnings are included.

**Thinner areas:**
- **Observations** (vitals, lab results, measurements) are listed in the DRS table but have no field-level detail from the sample. The `observations` entity description ("Discrete repeatable information regarding a patient (lab results, vitals, measurements, etc)") suggests it's a generic EAV-style (entity-attribute-value) table that captures diverse clinical data.
- **Orders and lab results** have 8 entities listed but no sample data to confirm field detail.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients` (61 fields), `patient_mrns`, `patient_extended_values`, `pat_pat_relations` | Thorough — includes name, DOB, SSN, address, race, sex, marital status, emergency contacts, employment status, death date/indicator |
| Encounters / visits | ✅ Covered | `encounters` (35 fields), `encounter_extended_values`, `encounter_visit_types`, `encounters_link` | Solid — includes chief complaint, visit type, dates, linked data |
| Problems / conditions | ✅ Covered | `patient_conditions` (30 fields), `patient_conditions_family` (21 fields) | Good — includes ICD codes, onset/conclusion dates, clinical status, verification status, family history |
| Medications / prescriptions | ✅ Covered | `rxlist` (27 fields), `rxlist_refills`, `rxlist_sign`, 8 `escript_*` e-prescribing objects | Deep — full e-prescribing lifecycle with SureScripts integration data |
| Allergies | ✅ Covered | `rxlist_allergylist` (20 fields) | Good — includes allergy name, reaction, severity, intolerance flag, onset date |
| Immunizations | ✅ Covered | `injections` entity listed in DRS | Present as entity; no field detail visible from sample |
| Vitals | ✅ Covered | `observations` entity (described as "lab results, vitals, measurements, etc") | Covered via generic observations table; no sample data to confirm field structure |
| Lab results | ✅ Covered | `observations`, `lab_requests`, `lab_requests_txt`, `observation_codes` | Multiple entities; observations is the main store, lab_requests for grouping |
| Imaging / diagnostic reports | ✅ Covered | `dicom_images`, `dicom_series`, `dicom_studies` — images in Base64 | DICOM data included at study/series/image level |
| Procedures | ✅ Covered | `patient_procedures` (16 fields) | Includes CPT, ICD10, description, dates |
| Clinical notes / documents | ✅ Covered | `documents` (34 fields), `documents_txt`, `document_attachments`, `document_sign` | Deep — document content in Base64, text content, attachments, e-signatures |
| Care plans / goals | ⚠️ Partial | `patient_targets` (10 fields) appears related to care targets/goals | Thin — only `patient_targets` with minimal field detail; no dedicated care plan entity |
| Orders / referrals | ✅ Covered | `encounter_orders` (25 fields), `order_requests`, `order_items`, `order_list`, `order_questions`, `order_question_answers` | Comprehensive entity structure for orders |
| Insurance / coverage | ✅ Covered | `insurance_policy` (34 fields), `insurance_plans`, `insurance_pre_cert` | Good — policy details, pre-certifications, plan info |
| Claims / billing | ❌ Not covered | No billing/claims entities in DRS table | Product has billing-adjacent features (fee schedules, pending billing, RCM); may rely on external PM system (OpenPM). No claims/charge data in export. This is a gap if the product handles billing internally, or N/A if billing is handled externally. |
| Payments | ❌ Not covered | No payment entities in DRS table | Same uncertainty as claims/billing — depends on deployment model |
| Consents / directives | ⚠️ Partial | `document_sign` for e-signatures; no dedicated consent entity | E-signatures tracked, but no explicit consent/directive objects |
| Patient communications | ✅ Covered | `conversation_messages` — "Messages between a patient or representative and their care team" | Present as entity; no field detail from sample |
| Specialty: Occupational health | ✅ Covered | 22 entities spanning incidents, restrictions, accommodations, audiometry, PFT, surveillance panels, respirator details | Exceptionally deep — this is the product's core specialty |

**Domains covered:** 15 of 17 applicable (plus 1 N/A specialty coverage)
**Key gap:** Claims/billing data is absent. Whether this is a true gap or reflects the product's architecture (billing handled by external PM system) is uncertain from the documentation.

## 6. Documentation Quality

**Strengths:**
- The DRS content table provides a clear catalog of all 99 objects with brief descriptions
- A complete sample JSON export is provided, allowing developers to understand the structure
- The export format (JSON) is a well-known standard with a documentation link
- User-facing documentation with screenshots explains how to perform exports
- The markdown source is publicly available on GitHub (mieweb/docs repo), enabling programmatic parsing

**Weaknesses:**
- **No per-field data dictionary.** There are no field names, types, descriptions, value sets, or constraints documented. The only way to discover fields is by examining the sample export.
- **No schema definition.** No JSON Schema, no OpenAPI spec, no formal contract for what fields exist or what they mean.
- **No foreign key / relationship documentation.** Relationships between objects must be inferred from field names (e.g., `pat_id`, `doc_id`, `enc_id`).
- **No value sets or code systems.** Fields like `marital_status`, `race`, `sex`, `clinical_status`, `verification_status` have no documented valid values.
- **18 objects lack descriptions** in the DRS table (mostly `escript_*` objects and some occupational health tables).
- **Sample covers only 18 of 99 objects.** The test patient (William S. Hart) only has data in 18 entities, leaving 81 entities with zero field-level visibility.
- **No bulk export sample.** Only a single-patient example is provided.

**Could a developer build an import?** Partially. A developer could parse the JSON structure and identify the main entities/fields from the sample, but would need to reverse-engineer field meanings, data types, and relationships for many objects. The 81 entities without sample data would require additional investigation. Overall, the documentation is functional but significantly below what would be needed for reliable interoperability.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

The export covers 99 DRS objects spanning the full breadth of what WebChart EHR stores: demographics, encounters, medications (with full e-prescribing lifecycle), conditions, procedures, allergies, observations (vitals/labs), documents (with Base64 content), DICOM imaging, orders, insurance policies, immunizations, patient communications, tasks, and — most notably — 22 occupational health entities covering incidents, restrictions, accommodations, audiometry, PFT, surveillance panels, and respirator details. This goes well beyond USCDI/US Core clinical exchange and reflects the product's actual internal data model.

The notable absence is claims/billing data, but this likely reflects WebChart's architecture: the product appears to handle billing-adjacent functions (insurance eligibility, fee schedules, pending billing reports) while relying on external systems like OpenPM for full claims processing. If the billing data lives in an external PM system, it would not be part of WebChart's designated record set.

The export is comprehensive relative to what WebChart itself stores.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange:
- The format is the vendor's **native database model** exported as JSON — not C-CDA, not FHIR, not any standard clinical exchange format
- It includes internal table structures with database field names, internal IDs, and audit metadata
- It covers data domains (occupational health incidents, e-prescribing message lifecycle, DICOM images, work restrictions, health surveillance panels) that would never appear in a (g)(10) FHIR API or C-CDA exchange
- The export has its own dedicated UI with patient, provider, and system-wide export options
- Documentation references 45 CFR 164.501 (designated record set) explicitly
- The export is designed to output the entire patient record, not a clinical summary

### Key Findings

1. **Purpose-built native database export with 99 DRS objects.** MIE built a genuine EHI export that dumps the patient's designated record set from their internal database tables as JSON. The 99 objects cover clinical, administrative, occupational health, imaging, e-prescribing, and insurance domains — well beyond any clinical exchange standard. (`ehi-export-technical-details.md`, DRS Content table)

2. **Exceptionally deep occupational health coverage.** With 22 entities and 165+ fields dedicated to occupational health (incidents with 125 fields, work restrictions, accommodations, audiometry, PFT, surveillance panels, respirator details), the export reflects WebChart's core strength and the Enterprise Health product's capabilities. (`sample-single-patient-export.json`, `incidents` object)

3. **No per-field data dictionary.** Despite having 99 entities, the documentation provides only entity-level descriptions — no field names, types, descriptions, value sets, or relationships. Field structure can only be discovered from the sample export, which covers only 18 of 99 entities. This is the export's biggest documentation weakness. (`ehi-export-technical-details.md`)

4. **Complete sample export provided.** The sample JSON for test patient William S. Hart (482 KB) contains actual data including Base64-encoded documents and DICOM images, demonstrating the export produces real, usable patient data. (`sample-single-patient-export.json`)

5. **Billing/claims data absent.** No claims, charges, payments, or superbill entities appear in the DRS. This likely reflects the product's architecture (billing via external PM system) rather than an intentional omission, but creates uncertainty about completeness for deployments where WebChart handles billing internally.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   JSON (native database model)
Entities:        99 (DRS table) + 3 additional in sample = 102
Fields:          581 observed across 18 entities with sample data; unknown for remaining 81 entities
Descriptions:    82% of entities have descriptions; 0% of fields have descriptions
Sample data:     Yes (single-patient, 482 KB)
Bulk export:     Yes (provider-level and system-wide via admin UI)
Domains covered: 15 of 17 applicable domains
```

### Bottom Line

WebChart EHR provides a genuine, purpose-built EHI export that dumps 99 internal database objects as JSON, covering clinical, occupational health, imaging, insurance, e-prescribing, and administrative data — well beyond any clinical exchange standard. The export's primary weakness is documentation: there is no field-level data dictionary, meaning developers must reverse-engineer field meanings from the sample export. The single biggest strength is the depth of occupational health data (22 entities, 125+ fields for incidents alone), reflecting the product's core domain expertise.
