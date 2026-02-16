# Oracle Health — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.oracle.com/health/regulatory/certified-health-it/
- Final URL (after redirect): https://www.oracle.com/health/certified-health-it/
- CHPL IDs: 11670 (version 2025), 11522 (version 2024)

## Navigation Journal

### Step 1: Initial probe

```bash
curl -sI -L "https://www.oracle.com/health/regulatory/certified-health-it/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```

Result: HTTP 301 redirect to `/health/certified-health-it/`, then HTTP 200. Content-Type: text/html, 63 KB page.

### Step 2: Page examination

The page is a static HTML compliance hub. Searched for EHI-related content:

```bash
grep -oiE 'href="[^"]*"' /tmp/oracle-page.html | grep -iE 'ehi|export|data.dictionary|b.10|bulk|mysql|model'
```

Found a dedicated "Electronic Health Information (EHI) Export" section with an anchor `#ehi-export-lnk`. The section describes both single-patient and patient-population export capabilities and links to seven downloadable files.

### Step 3: Downloads

All files downloaded with `curl -sL -H "User-Agent: Mozilla/5.0 ..." -o <filename> <url>`.

**Direct PDF/ZIP downloads from the page:**

1. `cerner-corp-single-patient-ehi-export-data-overview.pdf` → Single Patient EHI Export Data Overview and User Instructions (4 pages)
2. `single-patient-ehi-export-data-format-specifications.zip` → Contains MySQL data model ZIP + Longitudinal Plan PDF
3. `cerner-corp-patient-population-ehi-export-data-overview.pdf` → Patient Population EHI Export Data Overview and User Instructions (23 pages)
4. `patient-population-ehi-export-data-format-specifications.zip` → Contains MySQL model, Oracle model, Longitudinal Plan PDF, Document Imaging schema PDF, XSD, DICOM specs, Non-DICOM column definitions
5. `health-data-intelligence-ehi-export-data-overview-user-instructions.pdf` → HDI EHI Export Overview (3 pages)
6. `health-data-intelligence-ehi-export-data-format-specifications.pdf` → HDI data format specs (8 pages, ~20K lines of entity/field definitions)
7. `certified-health-it-transparency-disclosure-information.pdf` → Transparency/cost disclosure (32 pages)

### Step 4: ZIP extraction

Both format specification ZIPs were extracted. The single-patient ZIP contains:
- `EHI MYSQL DATA MODEL 2025401.zip` (nested ZIP with 1,456 HTML files)
- `Longitudinal Plan EHI Export - Single Patient.pdf`

The patient-population ZIP additionally contains:
- `EHI ORACLE DATA MODEL 2025401.zip` (parallel Oracle DB model)
- `Oracle Health Document Imaging AxAnnotations.xsd`
- `Oracle Health Document Imaging Content Management Database Schema.pdf`
- `Oracle Health Multimedia Storage DICOM Data Structure and Definitions.pdf`
- `Oracle Health Multimedia Storage Non-DICOM Data Column Definitions.pdf`

### Step 5: Data model extraction

The MySQL data model ZIP was extracted to `mysql-model/`. It contains 1,422 HTML report pages covering 6,604 database tables across 242 subject areas (version 2025.4.01, dated January 16, 2025). An enrichment script (`enrichment/extract-mysql-model.ts`) parsed all pages into structured JSON.

## What Was Found

Oracle Health provides one of the most comprehensive EHI export documentation sets of any certified EHR vendor. The documentation covers four distinct data storage locations, with separate export mechanisms and format specifications for each.

### Export Architecture

The EHI export covers four independent storage locations:

1. **Core Millennium EHR Database** — The primary relational database containing clinical, financial, operational, and administrative data. Exported as SQL DDL + INSERT statements that can be loaded into an empty MySQL or Oracle database. For single-tenant systems, the entire database is delivered on a customer-supplied encrypted device. For multi-tenant systems, SQL files are provided.

2. **Oracle Health Multimedia Storage** — DICOM imaging data (studies, series, instances) and non-DICOM files (audio, video, photos, PDFs). Delivered in native format via a secure URL download. DICOM data is organized as tar.gz files with XML/JSON metadata per patient/study. Non-DICOM data is delivered as CSV-formatted tar.gz files.

3. **Oracle Health Document Imaging** — Scanned documents and annotations stored in a separate content management database. Uses a proprietary schema (documented in the Content Management Database Schema PDF) with an XSD for annotation structures.

4. **Oracle Health Longitudinal Plan (One Plan)** — Care plans, health concerns, goals, activities, and strengths. Exported as JSON files with specifications referencing the HealtheIntent API documentation.

### Data Model

The Millennium data model is extraordinarily comprehensive: **6,604 tables with 129,148 columns** across 242 subject areas. Key areas include:

| Domain | Subject Area(s) | Tables |
|--------|-----------------|--------|
| Core infrastructure | bedrock | 197 |
| Microbiology | micro | 156 |
| Drug database | multum, multum_load | 271 |
| Quality measures | lh_quality_measures | 136 |
| Patient financial | pft_account_manageme, pft_billing, pft_posting_and_tran, pft_revenue_cycle_wh | 361 |
| Encounters | encounter, encounter___revenue, encounter___care_man | 148 |
| Person/demographics | person | 111 |
| Scheduling | scheduling, scheduling_build | 183 |
| Pharmacy | pharmnet, pharmnet_ambulatory | 178 |
| Surgery | surginet, surginet___anesthesi, surginet_* | ~280 |
| Lab | general_lab, pathnet_* | ~200 |
| Clinical events | clinical_events | multiple pages |
| Charting | charting | 71 |
| Radiology | radnet_* | ~100 |
| Orders | orders, orders_build | ~100 |
| Behavioral health | behavioral_health | present |
| Oncology | oncology | present |
| Women's health | womens_health___* | present |
| Blood bank | blood_bank, bb_* | ~150 |
| Supply chain | scm_* | ~130 |
| Charge services | charge_services | 55 |
| Collections | collections | 40 |

Each table report includes: table name, description, definition, table type (ACTIVITY/REFERENCE), and column-level detail (column name, data type, nullable flag, and a prose definition of each column).

### Health Data Intelligence (HDI) Export

A separate export pathway for the HDI Longitudinal Record, which is Oracle's population health/analytics platform. This uses REST APIs (Longitudinal Record Bulk Extract API + Data Syndication API) to export data as JSON. The HDI format specifications PDF is 8 pages but contains ~20,000 lines documenting Avro-style entity definitions covering the poprecord model (actors, addresses, clinical events, medications, observations, etc.).

## Export Coverage Assessment

### Data Domain Coverage

Oracle Health's EHI export documentation is **exceptionally broad**. The export explicitly covers "all data for a single patient" or "all patients" in the Millennium system, and the data model documentation substantiates this claim with 6,604 tables spanning virtually every domain the product supports:

**Clearly covered (with extensive table/column documentation):**
- Demographics and person data (111 tables)
- Clinical events, results, and observations
- Medications, pharmacy (178 tables), drug databases (271 tables)
- Laboratory (PathNet — ~200 tables across general lab, microbiology, HLA)
- Radiology and imaging (RadNet — ~100 tables + DICOM/non-DICOM multimedia specs)
- Surgery and anesthesia (280+ tables)
- Orders and CPOE
- Encounters and care management (148 tables)
- Problems, diagnoses, charting (71 tables)
- Patient financial transactions and billing (361 tables across PFT subject areas)
- Revenue cycle (collections, charge services, financial clearance)
- Supply chain management (130 tables)
- Scheduling (183 tables)
- Blood bank (150+ tables)
- Behavioral health
- Oncology
- Women's health / obstetrics
- Clinical trials (85 tables)
- Immunizations
- Care planning and longitudinal plans
- Document imaging and scanned documents
- Consent management
- Authorization
- Community health
- Health maintenance / preventive care

**Notable inclusion of non-clinical data:**
- Benefits and insurance data
- Electronic prior authorization
- Revenue cycle workflow
- Supply chain (purchasing, contracts, inventory)
- Referrals

**Domains that are present but less documented:**
- Annotations on imaging documents (XSD provided, but limited prose)
- Non-DICOM multimedia (8 columns documented for CSV export)

**No significant EHI gaps identified.** The export covers the full Millennium database, including both clinical and financial data. This is a genuine (b)(10) export — not a repackaged FHIR API or USCDI-only subset. The export delivers the actual database tables, not a curated clinical summary.

### Export Format & Standards

The export uses a **proprietary database dump** approach — the most honest and complete approach for a product of this complexity:

- **Core EHR data**: MySQL or Oracle SQL DDL + INSERT statements. The recipient recreates the Millennium database schema locally and loads the data. This preserves all relationships, data types, and referential integrity.
- **Multimedia**: Native format files (DICOM, audio, video, images, PDFs) with structured metadata for cross-referencing back to the core EHR.
- **Document Imaging**: Proprietary content management database schema with documented tables and an XSD for annotations.
- **Longitudinal Plan**: JSON files following the HealtheIntent API entity model.
- **HDI export**: JSON via REST API.

This is **not a standardized format** — it's a raw database export. This is appropriate for a product of Millennium's complexity. A FHIR-based export would inevitably lose data. The SQL dump approach preserves everything and enables SQL-based querying and transformation.

The documentation explicitly notes that recipients can "map or translate the proprietary data format to other proprietary formats, such as for a third-party destination system."

### Documentation Quality

**Strengths:**
- The data model is exhaustive: 6,604 tables, 129,148 columns, each with a prose definition
- Every column has a data type, nullability flag, and description
- Table types are classified (ACTIVITY vs REFERENCE) to help distinguish patient-specific data from lookup tables
- Subject areas provide logical grouping of tables by functional domain
- Four separate storage systems are individually documented with format specs
- User instructions explain the end-to-end export process clearly
- DICOM data structure includes sample XML with entity definitions
- The Document Imaging schema includes table-level documentation with column definitions

**Weaknesses:**
- Column definitions often reference internal identifiers (e.g., "Foreign key to code_value table, code set 48") without providing the code set values themselves
- Relationships between tables are implied via column definitions rather than documented as a formal ERD or relationship graph
- The Longitudinal Plan documentation references external HealtheIntent API docs (docs.healtheintent.com) for entity definitions rather than being self-contained
- No sample export files are provided
- No worked examples showing how to query the exported data for common use cases
- The transparency disclosure PDF focuses on costs and licensing, not technical details

### Structure & Completeness

**Granularity:** Field-level documentation with data types, nullability, and definitions for all 129,148 columns. This is exceptional granularity.

**Coded fields:** Column definitions frequently reference "code set" numbers (e.g., "code set 48") which are lookup tables in the CODE_VALUE table. The code sets themselves are part of the export (as reference data), so the coded values are available but require loading the database to resolve.

**Relationships:** Foreign key relationships are described in column definitions (e.g., "Foreign key to ORDER_CATALOG table") but not extracted as a separate relationship graph. The DDL files include foreign key constraints.

**Versioning:** The data model is versioned (2025.4.01, dated January 16, 2025). The PDFs show copyright dates of 2023, suggesting the user instructions haven't been updated since initial publication but the data model itself is current.

## Narrative Assessment

Oracle Health (formerly Cerner) has done genuine (b)(10) work. This is not a FHIR API repackaged as an EHI export — it's a complete database dump of the Millennium system with comprehensive field-level documentation. The approach is pragmatic: rather than trying to map their enormous proprietary data model into a standard format, they export the raw database and provide the documentation needed to interpret it.

The documentation corpus is massive. The MySQL data model alone is 1,422 HTML pages documenting 6,604 tables. When you add the Oracle model, multimedia specs, document imaging schema, and HDI specs, this is among the most thoroughly documented EHI exports in the certified EHR market.

The export covers four independent data storage locations (core EHR, multimedia, document imaging, and longitudinal plans), which reflects the actual architecture of the Millennium platform. This is honest documentation that acknowledges the complexity rather than hiding it behind a simplified API.

The main weakness is that the documentation is a reference, not a guide. A developer receiving a Millennium export would have the schema and definitions to understand every field, but would lack guidance on common query patterns, how to reconstruct clinical documents from the normalized tables, or how to handle the code set lookups that permeate the data model. The export is complete but not easy.

Overall, Oracle Health's EHI export represents the gold standard for (b)(10) compliance: a genuine full-database export with field-level documentation, covering clinical, financial, operational, and specialty-specific data across the entire Millennium platform.

## Access Summary
- Final URL (after redirects): https://www.oracle.com/health/certified-health-it/
- Status: found
- Required browser: no
- Navigation complexity: accordion (EHI Export section on compliance page)
- Anti-bot issues: none (User-Agent header sufficient)

## Obstacles & Dead Ends
- None. All files were directly downloadable via curl with a standard User-Agent header.
- The registered URL (`/health/regulatory/certified-health-it/`) 301-redirects to `/health/certified-health-it/` — a minor URL change but the content is present.
- The Longitudinal Plan PDF references external docs at `docs.healtheintent.com` for entity definitions. These are Oracle's own HealtheIntent API docs and were confirmed accessible (HTTP 200) but not downloaded since they document the API specification format rather than the EHI export content itself.
