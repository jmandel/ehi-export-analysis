# NextGen Healthcare — NextGen Office — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.nextgen.com/sldkjljieo0935jljsrnfkl
- CHPL ID: 9372
- CHPL Product Number: 15.04.04.2054.Medi.05.00.1.180220
- Certification Date: 2018-02-20

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://www.nextgen.com/sldkjljieo0935jljsrnfkl"` returned HTTP 200 with `Content-Type: text/html; charset=utf-8` and `Content-Length: 175648`. The URL resolves successfully without redirects.

2. **Page content** — The page title is "ELECTRONIC HEALTH INFORMATION DATA DICTIONARY HYPERLINKS". It is a Sitecore CMS page on nextgen.com that serves as the shared EHI export documentation landing page for all NextGen Healthcare certified products: NextGen Enterprise EHR, NextGen Office, NextGen Direct Messaging, and Mirth Connect.

3. **Page structure** — The page has:
   - An intro section titled "EHI Data Export" explaining NextGen's commitment to EHI access
   - A "Key Information About the Exported Data" section describing the machine-readable format
   - A "Database Dictionaries" section with subsections for each product

4. **NextGen Enterprise EHR section** — Contains descriptive text explaining the data dictionary covers v6.2021.1 Cures and higher, dated June 27, 2025. Provides a hyperlink to download:
   - `https://www.nextgen.com/-/media/files/legal/2025/DD_Complete_EHI_20250627` — a 29MB PDF, 10,875 pages, ~2,097 database tables. Confirmed via `pdftotext` to be titled "Electronic Health Information (EHI) Data Dictionary Tables for NextGen Enterprise". This is a SQL Server database schema dump with table names, column names, data types, defaults, and not-null constraints.

5. **NextGen Office section** — Contains only a brief prose description:
   > "NextGen Office provides EHI exports for patients as a ZIP archive containing various files."

   File types listed:
   - CCDA Format (XML following C-CDA specification)
   - CSV (comma-separated variable, one or more fields per record)
   - Binary files (images, PDFs)
   - HTML files

   **No data dictionary link is provided.** No schema file, no field definitions, no downloadable documentation of any kind.

6. **NextGen Direct Messaging section** — ZIP archive with CDA XML and binary files. No dictionary link.

7. **Mirth Connect section** — XML export with base64-encoded attachments. No dictionary link.

8. **Additional investigation** — Checked `https://www.nextgen.com/certifications-and-cost-disclosures` for Office-specific EHI documentation. Found only real-world testing plans and results. No EHI data dictionaries.

9. **API regulatory page** — Checked `https://www.nextgen.com/api/regulatory-ngo` (NextGen Office regulatory information). This page documents the FHIR R4 API (g)(10) certification — Patient Access API, Smart App Launch API, and Bulk FHIR API. These are explicitly scoped to USCDIv1 data only. No reference to a (b)(10) EHI export mechanism or data dictionary.

10. **Downloaded the Enterprise data dictionary** anyway — while it is not for NextGen Office, it is the only substantive artifact linked from the registered URL and provides useful comparison context.

## What Was Found

### NextGen Office EHI Export Documentation (the target product)

The documentation for NextGen Office's EHI export is **extremely minimal**. The entire documentation consists of a single paragraph on the shared EHI landing page stating that the export is a ZIP archive containing four file types: C-CDA XML, CSV, binary files, and HTML files.

There is:
- **No data dictionary** — no table/field definitions, no column listings, no schema
- **No sample export files** — no example ZIP, no example CSV, no example C-CDA
- **No export instructions** — no user guide for how to trigger or perform the export
- **No field-level documentation** — no data types, no value sets, no cardinality
- **No relationship documentation** — no explanation of how CSV files relate to each other
- **No format specification** — beyond the four file types listed, nothing describes the structure of the CSV files (headers? encoding? quoting?), what C-CDA sections are included, or what the HTML files contain

### NextGen Enterprise EHI Data Dictionary (sibling product, for reference)

The Enterprise data dictionary, by contrast, is a massive 10,875-page PDF documenting approximately 2,097 database tables with their columns, data types, defaults, and not-null constraints. This represents a SQL Server database schema covering clinical, billing, and specialty-specific data across dozens of medical specialties.

However, this dictionary **does not apply to NextGen Office**. These are separate products built on different technology stacks:
- NextGen Enterprise is a traditional on-premise/client-server application using SQL Server
- NextGen Office (formerly HealthFusion MediTouch) is a cloud-based SaaS platform originally built independently

The table naming conventions (e.g., `AB_Cervical_Dilator_hist_`, `ADHD_NextMD_`, `AINF_aud_hearing_eval_`) clearly reflect the Enterprise product's database architecture. NextGen Office, as a cloud-native platform, would have an entirely different data model.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, NextGen Office manages:
- Clinical data (notes, problem lists, medications, allergies, vitals, immunizations, labs, imaging)
- Medications & prescribing (e-prescribing, EPCS, Surescripts)
- Documents & communications (C-CDAs, portal messages, e-fax, telehealth records)
- Scheduling & administrative (appointments, registration, eligibility verification, referrals)
- Financial & billing (claims, charges, payments, collections, EDI, denial management)
- Quality & reporting (MIPS/MACRA, CQMs, public health reporting)

**What appears to be covered:**
- The C-CDA XML component would include standard USCDI clinical data (problems, medications, allergies, immunizations, labs, vitals, procedures)
- Binary files could include documents, images, and attachments

**What is unclear or likely missing:**
- **Billing and financial data** — Claims, charges, payments, denial records, collections, EDI transactions. C-CDA does not support billing data. The CSV files *might* cover this, but there is no documentation to confirm.
- **Specialty-specific clinical data** — NextGen Office serves 40+ specialties with specialty-specific templates. The C-CDA standard does not accommodate all specialty data. Again, CSV might cover this, but it's undocumented.
- **Practice management data** — Appointment history, registration details, insurance eligibility records, referrals. These don't fit in C-CDA and there's no indication they're in the CSV.
- **Patient portal interactions** — Secure messages, intake forms, medication refill requests.
- **Custom form data** — Digital intake forms with discrete data integration.
- **Telehealth/virtual visit records**

The documentation is so minimal that it's impossible to assess coverage with confidence. The mention of CSV files alongside C-CDA suggests the vendor intends to export data beyond what C-CDA supports, but without a data dictionary or even a list of CSV file names, there's no way to know what's actually included.

### Export Format & Standards

The export uses a mixed format:
- **C-CDA XML** — A recognized standard for clinical document exchange, but limited to clinical summary data. Appropriate for demographics, problems, medications, allergies, vitals, procedures, and results.
- **CSV** — A generic tabular format. Without schema documentation, it's unclear what these contain. CSV can represent any tabular data but requires documentation to be interpretable.
- **Binary files** — Images and PDFs, presumably documents and attachments from the patient record.
- **HTML files** — Purpose not described. Could be rendered clinical documents, reports, or something else entirely.

The format mix is reasonable in principle — C-CDA for standardized clinical data plus CSV for additional structured data is a viable (b)(10) approach. But the complete absence of CSV documentation makes the CSV portion useless to any recipient trying to interpret or import the data.

### Documentation Quality

**Rating: Very Poor**

The NextGen Office EHI export documentation is among the most minimal that could conceivably exist while still having *something* on the page. A single paragraph with a bullet list of file types is not documentation — it's a placeholder.

- **No data dictionary**: Not even column names are documented
- **No field definitions**: No data types, no value sets, no descriptions
- **No examples**: No sample export to understand the actual output
- **No instructions**: No guidance on how to perform the export
- **No developer documentation**: A third party could not possibly import this data based on the documentation provided
- **No relationship documentation**: No way to know how CSV files relate to each other or to the C-CDA

The contrast with the Enterprise product is stark. Enterprise has a 10,875-page data dictionary. Office has one paragraph. Both products are certified under the same ONC criteria by the same vendor. This disparity strongly suggests the Office documentation is a compliance checkbox rather than a genuine effort to enable data portability.

### Structure & Completeness

- **Granularity**: No field-level documentation exists at all
- **Coded fields**: No value set documentation
- **Relationships**: Not documented
- **Versioning**: The page copyright says 2023; no change history or version number for the Office-specific content
- **Maintenance**: The Enterprise dictionary was updated June 27, 2025; the Office section shows no evidence of updates

## Access Summary
- Final URL (after redirects): https://www.nextgen.com/sldkjljieo0935jljsrnfkl
- Status: found
- Required browser: no (standard curl works)
- Navigation complexity: direct_link (content is on the registered URL itself)
- Anti-bot issues: none

## Obstacles & Dead Ends

1. **No Office-specific data dictionary link** — The registered URL promises "database dictionaries that define the schema of the EHI data exports for each of NextGen Healthcare's certified health IT products: NextGen Enterprise EHR, NextGen Office, and NextGen Direct Messaging, and Mirth Connect." However, only NextGen Enterprise has an actual dictionary link. Office, Direct Messaging, and Mirth Connect have only format descriptions.

2. **Checked certifications page** (`/certifications-and-cost-disclosures`) — Contains real-world testing plans and results for all products, but no EHI export documentation.

3. **Checked API regulatory page** (`/api/regulatory-ngo`) — Documents the FHIR API (g)(10) endpoints only. The Bulk FHIR API is explicitly limited to USCDIv1 data. No reference to (b)(10) EHI export.

4. **Enterprise dictionary downloaded for context** — The 29MB Enterprise dictionary (DD_Complete_EHI_20250627.pdf) was downloaded and examined. Confirmed it is explicitly "for NextGen Enterprise" and describes a SQL Server schema that does not correspond to the NextGen Office (HealthFusion/MediTouch) cloud platform.
