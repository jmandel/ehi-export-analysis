# OpenEMR Foundation — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.open-emr.org/wiki/index.php/OpenEMR_7.0_B10
- CHPL IDs: 11757 (v8, certified 2026-01-30), 10938 (v7.0, certified 2022-07-08)
- Developer: OpenEMR Foundation

## Navigation Journal

### Step 1: Probe the registered URL

```bash
curl -sI -L "https://www.open-emr.org/wiki/index.php/OpenEMR_7.0_B10" -H 'User-Agent: Mozilla/5.0'
```

HTTP/2 200, Content-Type: text/html, served via Cloudflare. The URL redirects (MediaWiki internal redirect) from `OpenEMR_7.0_B10` to `OpenEMR_7.0.4_B10`.

### Step 2: Fetch and examine the wiki page

```bash
curl -sL "https://www.open-emr.org/wiki/index.php/OpenEMR_7.0_B10" -H 'User-Agent: Mozilla/5.0' -o wiki-page-b10.html
```

25,336 bytes. A MediaWiki page titled "OpenEMR 7.0.4 B10 Electronic health information (EHI) export" with four sections:
1. **Public EHI Export Format Documentation** — links to two SchemaSpy documentation sites
2. **Setup Instructions** — how to enable the EHI Export module
3. **Single Patient Export Instructions** — step-by-step with screenshots
4. **Entire Patient Population Export Instructions** — bulk export with batch/zip splitting

### Step 3: Follow the documentation links

The page provides two links to the EHI export data dictionary:
- **Primary Link**: `https://seven.openemr.io/d/openemr/Documentation/EHI_Export/docs/index.html`
- **Backup Link**: `https://one.openemr.io/b/openemr/Documentation/EHI_Export/docs/index.html`

Both return HTTP 200, 251,014 bytes each, and are identical in content (confirmed via md5sum comparison). These are SchemaSpy 6.2.4-generated database documentation sites.

```bash
curl -sL "https://seven.openemr.io/d/openemr/Documentation/EHI_Export/docs/index.html" -o ehi-export-docs-v7.html
curl -sL "https://one.openemr.io/b/openemr/Documentation/EHI_Export/docs/index.html" -o ehi-export-docs-v8.html
```

### Step 4: Download SchemaSpy artifacts

The SchemaSpy site is JavaScript-heavy (uses jQuery DataTables for rendering). Key pages and files:

- **index.html** — main tables listing (322 tables)
- **columns.html** — all columns across all tables (1.7 MB)
- **relationships.html** — relationship diagram page
- **openemr.openemr.xml** — complete machine-readable XML schema (1.0 MB)
- **insertionOrder.txt** — table dependency order for loading
- **deletionOrder.txt** — reverse dependency order
- **tables/*.html** — 318 individual table documentation pages

```bash
curl -sL "https://seven.openemr.io/d/openemr/Documentation/EHI_Export/docs/openemr.openemr.xml" -o openemr.openemr.xml
curl -sL "https://seven.openemr.io/d/openemr/Documentation/EHI_Export/docs/columns.html" -o columns.html
curl -sL "https://seven.openemr.io/d/openemr/Documentation/EHI_Export/docs/relationships.html" -o relationships.html
curl -sL "https://seven.openemr.io/d/openemr/Documentation/EHI_Export/docs/insertionOrder.txt" -o insertionOrder.txt
curl -sL "https://seven.openemr.io/d/openemr/Documentation/EHI_Export/docs/deletionOrder.txt" -o deletionOrder.txt
# All 318 table pages downloaded in parallel via xargs
```

### Step 5: Download wiki screenshots

Three screenshots embedded in the wiki page:
```bash
curl -sL "https://www.open-emr.org/wiki/images/7/78/SinglePatient_EHI_Export.png" -o SinglePatient_EHI_Export.png
curl -sL "https://www.open-emr.org/wiki/images/a/a1/TotalPatient_EHI_Export.png" -o TotalPatient_EHI_Export.png
curl -sL "https://www.open-emr.org/wiki/images/0/0c/EHI-Export-Task-Completed.png" -o EHI-Export-Task-Completed.png
```

All confirmed as valid PNG images.

### Step 6: Enrichment

The XML schema was parsed into queryable JSON using a Bun TypeScript script. A second script extracted column comments from the 318 HTML table pages, recovering 3,125 additional column descriptions not present in the XML file.

## What Was Found

### Export Format

OpenEMR's EHI export produces **ZIP files** containing:
- **CSV files** — one per database table with patient data (`<table_name>.csv`)
- **/documents/\<pid\>/** — patient document files from the document storage system
- **/images/** — images used in data elements (e.g., visual pain map form)
- **README** — links back to the public documentation

The export is a **direct database dump in CSV format** of the entire MariaDB schema relevant to patient data. This is not a FHIR export, not a C-CDA export — it is the raw database tables exported as CSV with the full schema documented via SchemaSpy.

### Data Dictionary

The documentation is a **SchemaSpy 6.2.4** site generated against a MariaDB 11.4.9 database. It documents:
- **322 tables** in the `openemr` schema
- **4,941 columns** with data types, sizes, nullability, and default values
- **~1,521 columns with XML-level remarks** (table-level descriptions and foreign key annotations)
- **~4,469 columns with HTML-level comments** (additional descriptions in the rendered pages)
- **892 foreign key relationships** (defined in XML, linking tables together)
- **Insertion/deletion order** for database loading dependency resolution

### Export Mechanism

From the wiki instructions:
- The export is a **module** that must be enabled by an administrator (Modules → Manage Modules → Electronic Health Information Exporter)
- Supports **single patient** export (specify patient PID) or **entire population** export
- Population export batches patients into ZIP files of configurable size (1–4,000 MB)
- Document files can optionally be included/excluded
- ZIP integrity is verified via hash values
- Only accessible to users with the Administrator role (admin/super ACL)

### Scope of Export

The export covers the complete OpenEMR database schema. Looking at the 322 tables, this encompasses:

**Clinical data**: 60+ form tables covering encounters, vitals, SOAP notes, physical exams, review of systems, clinical notes, care plans, treatment plans, transfer summaries, functional/cognitive status, GAD-7, PHQ-9, SDOH assessments, pain maps, bronchitis forms, ankle injury forms, CAMOS notes, and the extensive ophthalmology module (17 `form_eye_*` tables).

**Demographics**: `patient_data` (137 columns — one of the largest tables), patient history (`history_data`), patient access/portal data.

**Billing/Financial**: `billing`, `claims`, `ar_activity`, `ar_session`, `payments`, `insurance_data`, `insurance_companies`, `fee_sheet_options`, `x12_partners`, `x12_remote_tracker`, `payment_gateway_details`, `payment_processing_audit`.

**Medications/Rx**: `prescriptions`, `drugs`, `drug_inventory`, `drug_sales`, `drug_templates`, `immunizations`, `immunization_observation`, e-prescribing tables (`erx_*`).

**Labs/Procedures**: `procedure_order`, `procedure_report`, `procedure_result`, `procedure_type`, `procedure_answers`, `procedure_questions`, `procedure_specimen`.

**Documents**: `documents`, `document_templates`, `onsite_documents`, document categorization tables.

**Scheduling**: `openemr_postcalendar_events`, `openemr_postcalendar_categories`, `calendar_external`.

**Messaging**: `pnotes` (patient notes between staff), notification tables.

**Amendments**: `amendments`, `amendments_history` — patient-initiated amendment requests.

**Reference data**: ICD-9/10 codes, value sets, list options, code tables.

**Supporting entities**: `users`, `facility`, `insurance_companies`, `pharmacies` — included in each batch for self-contained import capability.

## Export Coverage Assessment

### Data Domain Coverage

This is one of the most thorough EHI export implementations observed. The export is a direct dump of the entire patient-facing database schema — **322 tables encompassing virtually all data domains the product stores**.

**Clearly covered domains:**
- Patient demographics (137-column `patient_data` table)
- All clinical encounters and forms (60+ form tables, including specialty modules)
- Problem lists, medications, allergies (via `lists` table)
- Lab orders, reports, and results (full procedure chain)
- Prescriptions and e-prescribing
- Immunizations
- Billing records, claims, A/R activity, payments
- Insurance data
- Patient documents and images
- Clinical notes across all specialties
- Care plans and treatment plans
- Amendments and amendment history
- Social determinants of health assessments
- Ophthalmology/optometry specialty data (17 dedicated tables)
- Group therapy data
- Questionnaire assessments (FHIR Questionnaire support)
- Vitals with calculation components

**Not covered (but correctly scoped out per EHI definition):**
- Audit logs (`log`, `log_comment_encrypt` — these are present in the export, which is actually *more* than required)
- System configuration tables are included as supporting entities, which is generous

**Potential gaps (minor):**
- The `history_data` table (patient history) appears in the schema but is not separately categorized — it is included
- Custom layout-based form data (`lbf_data`) is included
- Portal chat history may be in `onsite_documents` or separate tables

The export genuinely covers **all electronic health information** the product stores, not just the US Core/USCDI subset. This is a true (b)(10) implementation that exports the complete database, not a (g)(10) FHIR API relabeled.

### Export Format & Standards

The format is **CSV files with a complete SchemaSpy data dictionary**. This is not a standardized interchange format (FHIR, C-CDA, etc.) but rather a raw database export with full schema documentation. This is entirely appropriate for (b)(10):

- CSV is universally readable by any tool or programming language
- The XML schema provides machine-readable column definitions, data types, and relationships
- Foreign key relationships are documented, allowing reconstruction of the full data model
- The insertion order file enables proper loading into a destination database
- Each ZIP is self-contained with supporting entity data for independent import

A third party could reconstruct the patient record from this export by:
1. Loading CSV files into a relational database following the insertion order
2. Using the XML schema to understand column semantics and relationships
3. Referencing the SchemaSpy HTML documentation for column descriptions

### Documentation Quality

**Excellent.** This is among the best EHI export documentation observed:

- **Complete data dictionary**: Every table and column is documented with data types, sizes, nullability, defaults, and constraints
- **Rich annotations**: 141/322 tables have remarks describing their purpose; 4,469/4,941 columns have descriptions in the HTML documentation
- **Relationship documentation**: 892 foreign key relationships are explicitly defined, showing how tables connect
- **Clear export instructions**: Step-by-step guide with screenshots for both single-patient and population exports
- **Self-describing exports**: Each ZIP includes a README linking to the documentation
- **Dual hosting**: Primary and backup documentation URLs for redundancy
- **Machine-readable schema**: XML export enables programmatic analysis

Areas for improvement (minor):
- Not all columns have descriptions (472 columns lack remarks in HTML)
- Some tables lack table-level descriptions (181/322)
- No sample export files are provided in the documentation
- No worked example of CSV content is shown

### Structure & Completeness

**Granularity**: Field-level documentation with data types, sizes, nullability, default values, auto-increment flags, and foreign key relationships. This is as detailed as documentation gets short of providing the actual DDL.

**Value sets**: Coded fields reference `list_options` table via documented foreign keys (e.g., `list_options.list_id='amendment_from'`). The `list_options` table itself is included in the export, so value sets are self-contained.

**Relationships**: 892 explicitly defined foreign key relationships. The `insertionOrder.txt` and `deletionOrder.txt` files provide dependency ordering.

**Versioning**: The documentation is generated from the live database schema (MariaDB 11.4.9). The wiki page title references version 7.0.4, though the same documentation applies to the v8 certification.

## Access Summary
- Final URL (after redirects): https://www.open-emr.org/wiki/index.php/OpenEMR_7.0.4_B10
- Status: found
- Required browser: no (curl works for all artifacts)
- Navigation complexity: one_click (wiki page links directly to SchemaSpy site)
- Anti-bot issues: none (Cloudflare serves cached content without challenges)

## Obstacles & Dead Ends

None. The documentation was straightforward to find and download:
- The registered URL was live and correctly pointed to the EHI export documentation
- All linked resources were accessible without authentication
- The SchemaSpy site rendered via JavaScript in the browser, but all key artifacts (XML schema, HTML pages) were directly downloadable via curl
- Both the primary (seven.openemr.io) and backup (one.openemr.io) documentation hosts were operational and serving identical content
