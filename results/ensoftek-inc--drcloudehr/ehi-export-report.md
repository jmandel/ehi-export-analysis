# EnSoftek, Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.drcloudemr.com/wp-content/uploads/EHI_Export/docs/index.html
- CHPL IDs: 10835
- Product: DrCloudEHR (version 2025)
- Certification date: 2022-02-18

## Navigation Journal

The registered URL returned HTTP 200 directly with a 118KB HTML page. No redirects, no authentication, no anti-bot measures.

```bash
curl -sI -L "https://www.drcloudemr.com/wp-content/uploads/EHI_Export/docs/index.html" \
  -H 'User-Agent: Mozilla/5.0'
# → HTTP/1.1 200 OK, Content-Type: text/html, Content-Length: 118492
```

The page is a SchemaSpy-generated database documentation site titled "DrCloudEHR FHIR" with a custom header section explaining the EHI export format. The site has four main navigation pages:

1. **Tables** (`index.html`) — lists all 128 exported tables with comments
2. **Columns** (`columns.html`) — all 2747 columns across all tables
3. **Relationships** (`relationships.html`) — SVG diagram of foreign key relationships

Additional files linked from the index:
- `drcloudehr.FHIR.xml` — SchemaSpy XML export (machine-readable schema)
- `insertionOrder.txt` / `deletionOrder.txt` — table load/purge ordering

Each of the 128 table pages (`tables/<name>.html`) contains:
- Table description
- Column listing with: name, data type, size, nullable, auto-updated, default value, parent/child relationships, and comments
- Per-table 1-degree and 2-degree relationship SVG diagrams

All 128 table pages, the XML schema export, 254 per-table SVG diagrams, and 2 summary relationship SVGs were downloaded via curl without issues:

```bash
# Main pages
curl -sL -H 'User-Agent: Mozilla/5.0' \
  'https://www.drcloudemr.com/wp-content/uploads/EHI_Export/docs/index.html' -o index.html

# Machine-readable schema
curl -sL -H 'User-Agent: Mozilla/5.0' \
  'https://www.drcloudemr.com/wp-content/uploads/EHI_Export/docs/drcloudehr.FHIR.xml' -o drcloudehr.FHIR.xml

# Table pages (128 total, example)
curl -sL -H 'User-Agent: Mozilla/5.0' \
  'https://www.drcloudemr.com/wp-content/uploads/EHI_Export/docs/tables/patient_data.html' -o tables/patient_data.html
```

## What Was Found

### Export Format

The documentation explicitly describes the ONC §170.315(b)(10) Electronic Health Information export feature. The export produces **ZIP files** containing:

- **CSV files** — one per table, named `<table_name>.csv`, for each table where patient data exists
- **`/images/`** directory — images used in data export (e.g., visual pain map forms)
- **`/documents/<pid>/`** directory — patient documents from the document management system, organized by patient ID
- **`README`** — with links back to this documentation site

ZIP files are 1MB–4GB in size (configurable). Each ZIP contains a batch of 1 or more patients. A single-patient export contains one patient. Batch ZIPs are self-contained and importable into another EHR, with duplicate-checking needed for supporting entities.

### Data Dictionary

The documentation is a SchemaSpy database schema documentation site documenting **128 tables with 2,747 columns**. The underlying database is MariaDB 10.11.5 (MySQL-compatible), and the schema name is `openemr.openemr` — confirming this is based on/derived from OpenEMR.

The data dictionary provides for each column:
- Column name
- Data type and size
- Nullability
- Auto-update flag
- Default value
- Foreign key parent/child relationships
- Free-text comments/remarks

The XML export (`drcloudehr.FHIR.xml`, 665KB) is the primary machine-readable artifact, containing all of the above in a structured format.

### Documentation Quality Metrics (from enrichment)

- **128/128 tables** have remarks/descriptions (100%)
- **1,135 of 2,747 columns** have remarks (41.3%)
- **628 relationship references** documented (parent/child foreign keys)
- **0 parse failures** in enrichment extraction

## Export Coverage Assessment

### Data Domain Coverage

This is a genuine (b)(10) export that exports the full database schema — not a FHIR or USCDI-only slice. The 128 tables cover:

**Clearly covered domains:**

| Domain | Tables | Notes |
|--------|--------|-------|
| Demographics & contacts | `patient_data` (126 cols), `patient_history`, `history_data` (91 cols) | Extensive: name, DOB, address, language, race/ethnicity, insurance, emergency contacts, employer, family history, habits |
| Clinical notes/forms | 38 `form_*` tables + `forms`, `pnotes` | SOAP notes, care plans, treatment plans, clinical notes, dictation, aftercare plans, clinical instructions, review of systems |
| Behavioral health assessments | `form_phq9`, `form_gad7`, `form_sdoh` (135 cols), `pro_assessments`, `questionnaire_response` | PHQ-9, GAD-7, SDOH screening, PROMIS patient-reported outcomes, custom questionnaires |
| Medications & prescriptions | `prescriptions` (48 cols), `drugs`, `drug_sales`, `lists_medication`, `medex_recalls` | Detailed prescription data including drug, dosage, frequency, route, refills, e-prescribing status |
| Lab/procedure orders & results | `procedure_order`, `procedure_order_code`, `procedure_report`, `procedure_result`, `procedure_type`, `procedure_answers` | Full lab/procedure lifecycle: order → report → individual results |
| Billing & claims | `billing` (30 cols), `claims`, `ar_activity`, `ar_session`, `voids`, `form_misc_billing_options` | Billing codes, claims submission tracking, accounts receivable, payment activity, voided transactions |
| Insurance | `insurance_data` (34 cols), `insurance_companies`, `insurance_type_codes`, `benefit_eligibility`, `eligibility_verification` | Patient insurance info, company details, eligibility verification |
| Immunizations | `immunizations` (30 cols), `immunization_observation` | Vaccine administration with observations |
| Documents & attachments | `documents` (33 cols), `document_templates`, plus `/documents/<pid>/` directory in ZIP | Digital documents with metadata, plus actual file export |
| Patient portal / messaging | `onsite_documents`, `onsite_mail`, `onsite_messages`, `onsite_portal_activity`, `onsite_signatures`, `patient_access_onsite` | Portal documents, secure messaging, chat, digital signatures |
| Therapy groups | `therapy_groups`, `therapy_groups_counselors`, `therapy_groups_participants`, `therapy_groups_participant_attendance` | Group therapy sessions, attendance tracking |
| Care plans & treatment plans | `form_care_plan`, `form_treatment_plan`, `clinical_plans` | Clinical care plans, treatment plans, quality measures |
| Scheduling/appointments | `openemr_postcalendar_events` (39 cols), `openemr_postcalendar_categories`, `patient_tracker`, `patient_tracker_element` | Appointment calendar data, patient flowboard events |
| Allergies, problems, conditions | `lists` (36 cols), `issue_types`, `issue_encounter` | Patient issues list covers allergies, medical problems, medications, devices, surgeries, dental issues (type-discriminated) |
| Referrals/transfers | `transactions`, `form_transfer_summary` | Patient referrals, transfer summaries |
| Eye care | 16 `form_eye_*` tables | Comprehensive ophthalmology: acuity, anterior/posterior segment, refraction, neuro, biometrics, prescriptions |
| Amendments | `amendments`, `amendments_history` | Health information amendment requests and history |
| E-signatures | `esign_signatures` | Digital signatures for encounters and chart notes |
| EHI disclosures | `extended_log` | Disclosures of EHI made to third parties |
| Dynamic/custom fields | `lbf_data`, `lbt_data`, `shared_attributes`, `layout_options`, `layout_group_properties` | Layout-Based Forms (LBF) extensibility mechanism for custom data |

**Domains with potential gaps:**

- **AI-generated content**: The product research describes AI Group Scribing (speaker diarization, sentiment analysis, per-speaker summaries), DrCloudDictate, and DrCloudIQ. There's a `form_dictation` table, but no tables visible for AI group scribing output, sentiment analysis, or speaker diarization data. These may be stored in external systems, in the `documents` table as attachments, or via the LBF extensibility mechanism — but they're not explicitly documented in the schema.
- **Telehealth session data**: The product has integrated telehealth, but no dedicated telehealth tables appear. Session data may be captured in encounter forms or external systems.
- **eMAR (electronic Medication Administration Records)**: The product advertises eMAR functionality for residential settings, but no explicit eMAR table exists. Medication administration may be captured in `drug_sales` or through the forms mechanism.
- **Scanned documents**: The `documents` table and `/documents/<pid>/` directory structure support document export, but it's not clear whether all scanned/uploaded files are included or only certain categories.

**Not expected (correctly absent from EHI export):**

- Audit logs (operational, not DRS)
- System configuration
- User credentials (except portal access metadata)
- Aggregate quality metrics

### Export Format & Standards

The export uses **CSV files** — one per database table — packaged in ZIP files. This is a straightforward database dump approach rather than a standards-based format like FHIR or C-CDA. This is appropriate for a (b)(10) export because:

1. It captures the full breadth of data (128 tables, 2,747 columns) rather than mapping to a subset of FHIR resources
2. It preserves the relational structure via documented foreign keys
3. CSV is universally parseable

The documentation includes `insertionOrder.txt` and `deletionOrder.txt` which specify the order tables should be loaded/deleted to respect foreign key constraints — a practical detail that shows this export was designed for actual data portability.

The format is **not** FHIR-based despite the XML file being named `drcloudehr.FHIR.xml` — that filename is misleading. The XML is a SchemaSpy schema export, not a FHIR resource.

### Documentation Quality

**Strengths:**
- The SchemaSpy site is well-organized and navigable
- Every table has a description explaining its purpose
- Column data types, sizes, and nullability are documented
- Foreign key relationships are documented both in the XML and visually in SVG diagrams
- The index page has a clear, well-written explanation of the export ZIP structure
- The export is described as self-contained and importable

**Weaknesses:**
- Only 41.3% of columns have remarks/descriptions. The remaining 58.7% have column name and data type only, which requires inference. For example, `form_ros` has 142 columns but many are boolean fields with abbreviated names (e.g., `weight_change`, `fever`, `night_sweats`) that are guessable but not formally documented.
- No sample export files or worked examples are provided
- No explicit data type encoding guide (e.g., how dates are formatted in CSV, how binary fields like UUIDs are represented, how null values appear)
- No documentation of value sets — coded fields reference `list_options` but the actual option values are not enumerated
- The `list_options` table is a key-value store (list_id → option_id) referenced by many columns, but the documentation doesn't enumerate what values exist for each list_id

### Structure & Completeness

- **Table-level documentation**: Complete — all 128 tables have descriptions
- **Column-level documentation**: Partial — types and constraints are complete, but only 41.3% have free-text remarks
- **Relationship documentation**: Good — 628 foreign key relationships documented with parent/child references
- **Value set documentation**: Absent — coded fields point to `list_options` but actual code values are not documented
- **Sample data**: Absent — no example CSVs or sample ZIPs
- **Versioning/changelog**: Absent — the page was last modified 2024-06-25 (per HTTP Last-Modified header) but no version history is provided

This is a solid, genuine (b)(10) export. The vendor clearly built a real database-dump export that covers the full breadth of their data model, including billing, behavioral health assessments (PHQ-9, GAD-7, SDOH), therapy groups, and specialty clinical forms. The documentation is above average for the industry — using SchemaSpy to generate navigable, structured documentation with relationship diagrams and an XML schema export. The main gaps are in column-level descriptions and value set enumeration.

## Access Summary
- Final URL (after redirects): https://www.drcloudemr.com/wp-content/uploads/EHI_Export/docs/index.html
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The documentation was fully accessible via simple HTTP GET requests with a standard User-Agent header. No JavaScript rendering required — the SchemaSpy site is static HTML. All 401 files (128 table pages, 256 SVG diagrams, 13 supporting files, 4 enrichment outputs) downloaded without errors.
