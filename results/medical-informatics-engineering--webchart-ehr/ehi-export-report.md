# Medical Informatics Engineering — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-technical-details/
- CHPL IDs: 11022
- CHPL Product Number: 15.04.04.1932.WebC.84.01.0.221117
- Product: WebChart EHR, Version 8.4
- Certification Date: 2022-11-17

## Navigation Journal

1. **Initial probe** — HTTP HEAD on the registered URL returned `200 OK` with `content-type: text/html; charset=utf-8`. The URL is live and served by Cloudflare. No redirects.

```bash
curl -sI -L "https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-technical-details/" -H 'User-Agent: Mozilla/5.0'
```

2. **Fetched the main technical details page** (984KB HTML). The page is a static documentation site built with Hugo, served from Cloudflare. No JavaScript rendering required — full content is in the HTML source.

```bash
curl -sL "https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-technical-details/" -H 'User-Agent: Mozilla/5.0' -o ehi-export-technical-details.html
```

3. **Navigated to the parent section** at `/resources/system-specifications/electronic-health-information-ehi-export/` which lists two sub-pages:
   - "Export for End Users" — user-facing instructions with screenshots
   - "Technical Details" — the registered URL with data dictionary and sample export

4. **Fetched the end-users page** (396KB HTML) which contains screenshots of the EHI Export interface:

```bash
curl -sL "https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-for-end-users/" -H 'User-Agent: Mozilla/5.0' -o ehi-export-for-end-users.html
```

5. **Downloaded screenshots** embedded in the end-users page:
   - Admin/SuperUser export interface showing Patient, System ("Export All"), and Provider export options
   - Clinical user export interface showing single-patient export only

```bash
curl -sL "https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-for-end-users.assets/5d50c74dda022b94cfb22a0732f2f721.png" -o screenshot-admin-export.png
curl -sL "https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-for-end-users.assets/525081618ca33295b2ef8cd9c4533db3.png" -o screenshot-clinical-export.png
```

6. **Found the GitHub source repository** (mieweb/docs) linked from the page footer. Downloaded the raw markdown source files, which are cleaner than the rendered HTML and include YAML frontmatter metadata:

```bash
curl -sL "https://raw.githubusercontent.com/mieweb/docs/master/content/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-technical-details.md" -o ehi-export-technical-details.md
curl -sL "https://raw.githubusercontent.com/mieweb/docs/master/content/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-for-end-users.md" -o ehi-export-for-end-users.md
```

7. **Extracted the sample JSON export** embedded in the technical details page — a complete single-patient export (482KB) with actual field-level data for patient "William S. Hart".

8. **Checked Google Drive source documents** (linked via "Edit in Google Drive" buttons). Both require Google authentication — not publicly accessible. The published HTML/markdown versions contain the complete content.

9. **Built enrichment scripts** to extract queryable JSON from the documentation: a data dictionary (99 DRS objects) and a field-level schema inferred from the sample export.

## What Was Found

### Export Format

The WebChart EHI export produces data in **JSON format** — a custom, proprietary JSON structure that maps directly to the product's internal MySQL database schema. This is a genuine (b)(10) export, not a FHIR wrapper.

Key structural elements:
- **Top-level envelope**: `{ "request", "documentation", "db", "meta" }`
- **Request pattern**: `db/patients/{pat_id}/drs` — retrieves the Designated Record Set for a patient
- **Patient data**: The `db` array contains one object per patient, with:
  - 61+ scalar fields for demographics, contact info, identifiers (SSN, MRN), insurance, and dates
  - 33+ nested arrays keyed as `{table_name}.{foreign_key}` (e.g., `accommodations.pat_id`, `documents.pat_id`, `encounters.pat_id`)
  - Foreign key references to `users` and other lookup tables are resolved inline (the full user record is embedded wherever a user_id reference occurs)
- **Multi-patient exports**: Generate one JSON file per patient, then compress all into a ZIP archive
- **Binary content**: Documents and DICOM images are provided as Base64-encoded strings within the JSON

### Data Dictionary (Designated Record Set Content)

The documentation enumerates **99 database objects** included in the DRS export:

| Category | Objects | Examples |
|----------|---------|----------|
| Patient demographics | 7 | patients, patient_mrns, patient_extended_values, patient_additional_info, patient_partitions, pat_pat_relations, pat_pat_relflat |
| Clinical encounters | 8 | encounters, encounter_orders, encounter_documents, encounter_dictation, encounter_extended_values, encounter_extended_index, encounter_order_status, encounters_link |
| Medications & prescriptions | 12 | rxlist, rxlist_allergylist, rxlist_refills, rxlist_sign, escript_newrx, escript_refreq, escript_refres_sign, escript_cancelrx, escript_changereq, escript_error, escript_message, escript_rxfill |
| Documents & imaging | 10 | documents, documents_txt, documents_link, document_attachments, document_sign, document_types, dicom_studies, dicom_series, dicom_images, dictation |
| Orders & labs | 10 | order_requests, order_items, order_list, order_questions, order_question_answers, order_request_icd9cm, lab_requests, lab_requests_txt, observations, observation_codes |
| Conditions & procedures | 4 | patient_conditions, patient_conditions_family, patient_procedures, coding_link |
| Occupational health | 15 | incidents, incident_bls, incident_nibp, incident_links, incident_condition_link, incident_extended_fields, incident_users, accommodations, patient_clinical_restriction, audio, audio_baseline, pft, pft_maneuver, panel, panel_membership |
| Insurance & billing | 4 | insurance_policy, insurance_plans, insurance_pre_cert |
| Appointments | 4 | appointments, apt_types, multi_referrer_apt, multi_resource_apt, multi_type_apt |
| Tasks & messaging | 4 | tasks, tasklist_extended_values, conversation_messages, extended_value_names |
| Injections/immunizations | 1 | injections |
| Reference/lookup tables | 10+ | accommodation_types, body_part_types, clinical_restriction_types, encounter_visit_types, document_types, nature_of_injury_types, observation_codes, storage_types, relation_types, users, locations |

Of these 99 objects, 81 have descriptions; 18 (mostly escript_* and incident_* tables) have names only.

### Export Interface

The export is initiated from **Control Panel → Interfaces → EHI Export** within WebChart:
- **Administrators/SuperUsers** can export: a single patient, all patients for a provider, or all patients in the system
- **Clinical users** can export: a single patient only
- System requirements: 8GB RAM, ~100MB disk per patient exported
- MIE offers assistance for customers lacking hardware capacity

### Sample Export

The documentation includes a complete single-patient sample export (482KB JSON) for a test patient "William S. Hart" (pat_id 18, DOB 1954-11-30). The sample demonstrates:
- Full demographic fields including SSN, insurance, emergency contacts
- 2 appointments, 9 documents, 2 encounter orders, 1 encounter
- 1 incident (workplace injury), 2 insurance policies
- 3 patient conditions, 2 family conditions, 1 procedure
- 2 medications, 2 allergies, 1 accommodation, 1 clinical restriction
- Documents with Base64-encoded content
- User references resolved inline with full user records

## Export Coverage Assessment

### Data Domain Coverage

This is one of the more thorough (b)(10) implementations encountered. The export explicitly addresses the **designated record set** by name and maps to internal database tables rather than to a standardized clinical model. This means it naturally captures data that a FHIR-only approach would miss.

**Clearly covered domains:**
- Demographics and identifiers (patients, patient_mrns, patient_extended_values)
- Clinical encounters with full encounter data (encounters + extended values + orders + documents)
- Medications and prescriptions, including full e-prescribing history (rxlist, escript_* tables)
- Allergies (rxlist_allergylist)
- Conditions, diagnoses, and problems (patient_conditions, patient_conditions_family)
- Procedures (patient_procedures)
- Lab results and observations (observations, lab_requests, observation_codes)
- Orders (order_requests, order_items)
- Documents with binary content in Base64 (documents, documents_txt, document_attachments)
- DICOM imaging data (dicom_studies, dicom_series, dicom_images)
- Insurance policies (insurance_policy, insurance_plans, insurance_pre_cert)
- Appointments (appointments, apt_types)
- Injections/immunizations (injections)
- Dictation and transcription (dictation, dictation_documents, encounter_dictation)
- Patient-provider messaging (conversation_messages)
- Tasks and care coordination (tasks, tasklist_extended_values)
- E-signatures (document_sign)
- Patient relationships (pat_pat_relations, user_patients)

**Strong occupational health coverage:**
- Workplace incidents with full detail (incidents, incident_bls, incident_nibp, incident_links, incident_condition_link, incident_extended_fields)
- Work accommodations and restrictions (accommodations, patient_clinical_restriction, accommodation_types, clinical_restriction_types)
- Health surveillance panels (panel, panel_membership, panel_decert, patient_panel_status)
- Audiometric data (audio, audio_baseline)
- Pulmonary function tests (pft, pft_maneuver)
- Respirator fit data (patient_respiratordetails)

**Potentially missing or unclear:**
- **Billing/claims detail**: While `insurance_policy` and `insurance_pre_cert` cover insurance and prior authorizations, there are no tables for charges, claims, payments, EOBs, or fee schedules. Given that WebChart integrates with external billing systems (OpenPM), detailed billing records may live outside the EHR. This is likely a genuine boundary of what WebChart stores rather than an export omission.
- **Vitals as a distinct entity**: Vital signs appear to be stored in the generic `observations` table rather than as a separate entity, which is appropriate.
- **Care plans and goals**: Not present as named entities, though they may be captured as encounter data or documents.
- **Referrals**: No explicit referral table, though referral information may be captured in orders or documents.
- **Patient portal data beyond messaging**: Portal questionnaire responses, self-check-in data — not clearly represented. May be captured as documents or observations.

### Export Format & Standards

- **Format**: Custom JSON mapping directly to MySQL database tables
- **Standard**: Proprietary — not FHIR, C-CDA, or any external standard
- **Appropriateness**: Highly appropriate for the data. A database-native export captures the full breadth of the product's data model, including occupational health data, incident details, and extended values that would be impossible to represent in FHIR US Core. This is exactly what (b)(10) should look like.
- **Relationships**: Foreign keys are expressed through the nested array naming convention (`table.foreign_key`) and through inline resolution of referenced records (e.g., user records are embedded at every user_id reference). This is verbose but self-contained.
- **Binary data**: Documents and images are Base64-encoded inline in the JSON. For large patient records with many documents, this could produce very large files (the docs suggest ~100MB per patient).
- **Reconstructability**: A third party could reconstruct the patient record with reasonable effort. The JSON structure is self-documenting through field names, and the data dictionary provides table-level descriptions. However, **field-level descriptions are absent** — you get field names and sample values but must infer meaning from names alone.

### Documentation Quality

**Strengths:**
- Clear, well-structured documentation on a modern documentation site
- Explicit reference to 45 CFR 164.501 and §170.315(b)(10) — the vendor understands the regulatory requirement
- Complete sample export with realistic data for a test patient
- 99 database objects enumerated with descriptions
- Export instructions with screenshots for both admin and clinical users
- System requirements documented
- Multi-patient export behavior documented (ZIP of individual JSON files)

**Weaknesses:**
- **No field-level documentation**: The data dictionary lists 99 objects with one-line descriptions, but there is no documentation of individual fields within those objects. A developer must infer field meanings from names and sample values.
- **18 objects have no descriptions at all** — just names (e.g., escript_cancelrx, incident_bls, observation_flags)
- **No data types specified**: All values in the JSON are strings (even numeric values like IDs), so there's no schema for intended types
- **No value sets documented**: Coded fields (status codes, type codes) are not documented with their possible values
- **No relationship/ERD documentation**: The foreign key relationships between tables are implied by the naming convention but not formally documented
- **Single sample only**: Only one test patient is shown; no examples of complex multi-encounter, multi-document patients
- **Date format**: Dates use MySQL's `YYYY-MM-DD HH:MM:SS` format; sentinel values like `0000-00-00 00:00:00` appear without explanation

### Structure & Completeness

- **Granularity**: Table-level names and descriptions ✓; Field-level names ✓ (in sample); Field-level descriptions ✗; Data types ✗; Value sets ✗; Cardinality ✗
- **Coded field documentation**: Not present. Fields like `status`, `confirmed`, `canceled` use numeric codes without documented meanings.
- **Relationship documentation**: Implicit through naming convention only. No entity-relationship diagram.
- **Versioning**: The markdown frontmatter shows `date: 2023-11-16`, consistent with the published date. No change history.

Overall, the data dictionary is **table-level only**, not field-level. The sample export fills the gap somewhat by showing actual field names and values, but a developer implementing an import would need significant reverse-engineering effort for coded fields, status values, and date conventions.

## Access Summary
- Final URL (after redirects): https://docs.webchartnow.com/resources/system-specifications/electronic-health-information-ehi-export/ehi-export-technical-details/
- Status: found
- Required browser: no (static HTML, no JavaScript required for content)
- Navigation complexity: direct_link (registered URL contains all technical documentation)
- Anti-bot issues: none (Cloudflare CDN but no challenge)

## Obstacles & Dead Ends

- **Google Drive source documents** (linked via "Edit in Google Drive" buttons on both pages) require Google authentication and are not publicly accessible. The published HTML/markdown versions contain the complete content, so this is not a barrier.
- **No downloadable files**: The documentation is entirely web-based — no PDFs, ZIPs, CSVs, or schema files are available for download. The sample JSON is embedded in the HTML page itself.
- **GitHub repository** (mieweb/docs) provided raw markdown source which was cleaner than the rendered HTML for extraction purposes.
