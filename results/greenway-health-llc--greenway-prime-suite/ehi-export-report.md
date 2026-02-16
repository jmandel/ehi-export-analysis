# Greenway Health, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ehi.greenwayhealth.com/PrimeSuite/PrimeSuiteEHIExport.html
- Developer: Greenway Health, LLC
- Product: Greenway Prime Suite
- CHPL IDs: 11681 (v22, certified 2025-08-14), 11352 (v21, certified 2023-10-03)

## Navigation Journal

**Step 1: Probe the registered URL.**

```bash
curl -sI -L "https://ehi.greenwayhealth.com/PrimeSuite/PrimeSuiteEHIExport.html" -H 'User-Agent: Mozilla/5.0'
```

Response: HTTP 200, `Content-Type: text/html`, 8068 bytes. Served from AmazonS3 via CloudFront. Last-Modified: 2023-11-27.

**Step 2: Fetch and examine the main page.**

```bash
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/PrimeSuiteEHIExport.html" -H 'User-Agent: Mozilla/5.0' -o PrimeSuiteEHIExport.html
```

The page is a static HTML page describing the Prime Suite EHI Export. It explains that exports produce a package of XML data tables plus document files, and links to two major reference documents:
- **Data Dictionary**: `PrimeSuiteEHIExport_Data_Dictionary.html`
- **XML Reference**: `PrimeSuiteEHIExport_Document_Reference.html`

It also links to two structure/schema pages:
- **Single Patient Export Structure & Schema**: `SinglePatientExport_Structure_Schema.html`
- **Patient Population Export Structure & Schema**: `PatientPopulationExport_Structure_Schema.html`

**Step 3: Download all four linked sub-pages.**

```bash
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/PrimeSuiteEHIExport_Data_Dictionary.html" -H 'User-Agent: Mozilla/5.0' -o PrimeSuiteEHIExport_Data_Dictionary.html
# 1,753,399 bytes

curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/PrimeSuiteEHIExport_Document_Reference.html" -H 'User-Agent: Mozilla/5.0' -o PrimeSuiteEHIExport_Document_Reference.html
# 2,471,063 bytes

curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/SinglePatientExport_Structure_Schema.html" -H 'User-Agent: Mozilla/5.0' -o SinglePatientExport_Structure_Schema.html
# 21,403 bytes

curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/PatientPopulationExport_Structure_Schema.html" -H 'User-Agent: Mozilla/5.0' -o PatientPopulationExport_Structure_Schema.html
# 167,227 bytes
```

**Step 4: Download referenced images and assets.**

The Single Patient Export page references 5 screenshots in `SinglePatientExport_Structure_Schema_files/`. The Patient Population Export page references 2 screenshots in `PatientPopulationExport_Structure_Schema_files/`. All pages reference `./assets/ehistyle.css` and `./assets/GW_Logo_White.png`.

```bash
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/SinglePatientExport_Structure_Schema_files/image001.jpg" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/SinglePatientExport_Structure_Schema_files/image002.jpg" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/SinglePatientExport_Structure_Schema_files/image003.jpg" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/SinglePatientExport_Structure_Schema_files/image004.jpg" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/SinglePatientExport_Structure_Schema_files/image005.gif" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/PatientPopulationExport_Structure_Schema_files/Patient_Population_Export_Root.png" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/PatientPopulationExport_Structure_Schema_files/Patient_Population_Export_Document_Folder.png" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/assets/ehistyle.css" ...
curl -sL "https://ehi.greenwayhealth.com/PrimeSuite/assets/GW_Logo_White.png" ...
```

All verified with `file` command: JPEG, GIF, PNG, and CSS as expected.

**Step 5: Download the EHI docs home page.**

```bash
curl -sL "https://ehi.greenwayhealth.com/default.htm" -H 'User-Agent: Mozilla/5.0' -o default.htm
```

The home page is a landing page for Greenway's EHI Export documentation covering both Prime Suite and Intergy products. It also links to the Greenway Health Developer Platform (external FHIR API docs — not relevant to b(10) export).

**Step 6: Check for additional downloadable artifacts.**

The XML Reference page references a `Face.png` file, but this returned an S3 `AccessDenied` error (not a real asset). No PDF, ZIP, CSV, JSON, or other downloadable file links were found on any of the pages. All documentation is delivered as HTML with inline content.

**Step 7: Run enrichment extraction.**

Created Bun TypeScript scripts to parse the large Data Dictionary (1.7MB, 1026 tables) and XML Reference (2.5MB) into structured JSON. Both ran successfully with zero parse failures.

## What Was Found

Greenway Health has built a dedicated, well-organized documentation website for their EHI export at `ehi.greenwayhealth.com`. The documentation covers both their Prime Suite and Intergy products, with separate pages for each. For Prime Suite, the documentation consists of five interconnected HTML pages:

### Export Format

The Prime Suite EHI export produces a **package of XML files** — one file per database table — containing patient data in a simple row-based XML schema:

```xml
<TableName>
  <row>
    <Column1>value</Column1>
    <Column2>value</Column2>
  </row>
  <row>...</row>
</TableName>
```

This is essentially a **database dump in XML format**, with each table from the Prime Suite database exported as a separate XML file. This is a genuine (b)(10) export approach — not a FHIR API repackaged.

### Two Export Modes

1. **Single Patient Export**: Exports all data for one patient. The export package contains:
   - A `DataExport` folder with one XML file per table
   - A `DocumentExport` folder with three sub-folders:
     - `AdamImage` — sketchpad annotations/drawings
     - `ClinicalBin` — clinical documents in native format (PDF, C-CDA, TIF, JPG, GIF, BMP, TXT)
     - `ImgLibGroupItem` — sketchpad images
   - A `Logs` folder with error and process logs

2. **Patient Population Export**: Exports data for all patients at a site. Initiated via the My Greenway support portal and fulfilled by Greenway Professional Services. Uses the naming convention `PatientPopulation_DataExport_SiteID<id>_<Tablename>_Batch1.xml` with batching at 1 million documents per file.

### Important Caveats

- **Encryption**: Some exported files require processing through the "Prime Suite Conversion Tool" to be decrypted. The tool is available only through the My Greenway support portal (requires authentication).
- **Proprietary document formats**: Some clinical documents (progress notes, procedure notes, custom notes, lab flowsheets, allergy tests) are stored in Greenway proprietary XML formats. The XML Reference document provides specifications for interpreting these formats.
- **Minimum version**: Export requires Prime Suite version 21.23.00.00 or later.

### Data Dictionary

The data dictionary is the most substantial artifact. It documents **1,026 database tables** with a total of **11,868 columns**. Each table has:
- A table description
- Column name, data type, nullable flag, and description for every column
- Foreign key references to related tables

The tables span an extremely wide range of data domains (counts are approximate due to overlap):
- **Clinical**: ~135 tables (diagnoses, problems, medications, allergies, vitals, lab results, orders, clinical documents)
- **Billing/Claims**: ~101 tables (ASCX12 EDI transactions, claims, payments, adjustments, charges, billing registers)
- **Patient**: ~92 tables (demographics, addresses, insurance, patient portal)
- **Community Health Center (CHC)**: ~84 tables (FQHC-specific workflows, sliding fee scales, UDS reporting)
- **Clinical Documents**: ~67 tables (document metadata, clinical notes, templates)
- **Immunization**: ~39 tables (vaccines, antigen tracking, VFC codes, series management)
- **Orders**: ~29 tables (lab orders, imaging orders, referral orders)
- **Claims Processing**: ~27 tables (claim status, submission tracking, ERA processing)
- **Scheduling**: ~26 tables (appointments, resources, scheduling rules)
- **Referrals**: ~16 tables (authorization, referral tracking, out-of-network)
- **Lab**: ~14 tables (lab results, panels, test definitions)
- **Insurance**: ~13 tables (payer info, eligibility, coverage)
- **Vocabulary/Codeset**: ~13 tables (coded answer sets, question definitions)

### XML Reference

The XML Reference document describes Greenway's proprietary document formats — specifically how clinical notes (file type 1005), custom notes (1016), lab flowsheets, allergy tests, and allergy education documents are encoded in XML. It includes:
- A table listing generic document types (those exported in standard formats: PDF, TIF, etc.)
- Detailed XML element specifications for proprietary formats
- Instructions for reconstructing annotated medical drawings as SVG
- Instructions for converting lab flowsheet XML-like JSON to SVG

## Export Coverage Assessment

### Data Domain Coverage

This is one of the most comprehensive EHI export data dictionaries encountered. Comparing against the product research, the coverage is remarkably thorough:

**Clearly covered with detailed table definitions:**
- Patient demographics and registration (PatDemo, Address, AddressHistory, and many more)
- Clinical encounters and visits (Visit, VisitHistory, VisitInsurance, VisitTypes)
- Diagnoses and problem lists (Diagnosis*, Problem* tables, ICD code tables)
- Medications and prescriptions (Medication*, Rx*, DrugInteraction tables)
- Allergies (13+ Allergy* tables including tests, severity, coding systems)
- Lab orders and results (Lab* tables, Order* tables)
- Vital signs and clinical observations
- Immunizations (39+ Vac* and Imm* tables — very detailed)
- Clinical documents and notes (67+ Clinical* tables, document metadata)
- Billing and claims (101+ tables including ASCX12 EDI, ERA, payment allocations)
- Insurance and payer information (13+ Insurance* tables)
- Scheduling and appointments (26+ Schedule* tables)
- Referrals and authorizations (16+ Referral* tables)
- Procedures and charges (38+ Procedure*, CPT*, Charge* tables)
- Patient portal data (PatientPortal* tables)
- Care plans and clinical decision support
- E-prescribing and EPCS (electronic prescribing for controlled substances)
- Growth charts (WHOPediatricWeightForLength, Growth* tables)
- Community Health Center workflows (84 CHC* tables — FQHC-specific)

**Noteworthy specialty coverage:**
- Advanced Beneficiary Notice (ABN) documents — 6 tables
- Allergy testing with detailed battery/detail/location tracking
- Sliding fee scale management (CHC-specific)
- UDS reporting tables (FQHC-specific)
- Drug utilization review (DUR) tables
- Surgery scheduling and tracking

**Potentially missing or unclear:**
- **Telehealth visit data**: No tables with "Telehealth" prefix visible, consistent with the product research noting telehealth is a separate add-on
- **Patient intake forms from Patient Connect**: May be captured under generic document or form tables but not explicitly labeled
- **Fax/document management**: The DocumentManager-specific tables are not clearly separated, though ClinicalBin documents include externally scanned documents
- **Care coordination/CCM workflows**: Not explicitly visible as separate tables, may be embedded in existing clinical tables

### Export Format & Standards

The export format is a **proprietary XML database dump** — each table exported as an XML file with rows and columns. This is an appropriate and honest approach for a (b)(10) export:

- It is NOT a FHIR API repackaged as EHI export. This is a genuine database-level export.
- The XML schema is simple and well-documented, making it machine-parseable.
- Relationships between tables are documented via foreign key descriptions in column definitions.
- The format preserves the full relational structure of the underlying database.
- Documents (clinical notes, images, scanned documents) are exported alongside the data tables in their native formats.

The one significant concern is the **encryption/conversion tool requirement**. Some exported files must be processed through a proprietary "Prime Suite Conversion Tool" available only through the authenticated My Greenway portal. This creates a barrier to third-party use of the export data — you cannot fully access the export without Greenway's proprietary tool.

### Documentation Quality

**Strengths:**
- The documentation is well-organized with a clear hierarchy: main page → structure/schema → data dictionary + XML reference
- The data dictionary is exceptionally detailed — 1,026 tables with 11,868 columns, all with descriptions
- Data types and nullable flags are specified for every column
- Foreign key relationships are documented in column descriptions
- The XML Reference provides detailed specifications for proprietary document formats
- Export directory structure is documented with screenshots and naming conventions
- Both single-patient and population-level exports are documented separately

**Weaknesses:**
- No sample data or example export files are provided
- No formal XSD or JSON Schema — the XML schema is described in prose/examples only
- Value sets for coded fields are not always explicitly listed (some reference tables serve as implicit value sets)
- The data dictionary is delivered as a single enormous HTML page (1.7MB) with no downloadable CSV/JSON/PDF alternative
- The XML Reference contains base64-encoded inline images rather than linking to external files
- The encryption/conversion tool documentation is behind a login wall on the My Greenway portal
- No versioning or change history is visible on the documentation pages (last-modified date on the main page is 2023-11-27, suggesting it may not have been updated for v22)

### Structure & Completeness

**Field-level granularity**: Excellent. Every column has a name, data type, nullable flag, and textual description. Descriptions often include foreign key references (e.g., "References: dbo.ABNDocumentStatus").

**Coded fields**: Many lookup/reference tables serve as value sets (e.g., AllergyTestType, ABNDocumentStatus, BillingReasonCode). However, the actual code values within these tables are not listed in the documentation — you would need to inspect the exported XML files themselves to see what values appear.

**Relationships**: Documented informally through foreign key references in column descriptions (e.g., "Foreign Key of the table represents ABNDocument StatusID. References: dbo.ABNDocumentStatus"). There is no formal ERD or relationship diagram.

**Overall assessment**: Greenway's Prime Suite EHI export documentation represents one of the more thorough implementations of the (b)(10) requirement. The approach of exporting the actual database tables in XML format, rather than trying to map everything to FHIR or another standard, is practical and captures far more data than a FHIR-based export would. The 1,026-table data dictionary covering 11,868 columns demonstrates a serious effort to document the full breadth of data the system stores. The inclusion of billing/claims data (101 tables), scheduling data (26 tables), referral tracking (16 tables), and FQHC-specific workflows (84 tables) — alongside the expected clinical data — shows this is a genuine effort to export the full designated record set, not just clinical summaries. The main gaps are the lack of sample data, the proprietary conversion tool dependency, and the somewhat informal documentation of relationships and value sets.

## Access Summary
- Final URL: https://ehi.greenwayhealth.com/PrimeSuite/PrimeSuiteEHIExport.html (no redirects)
- Status: found
- Required browser: no (all content is static HTML, no JavaScript needed for content)
- Navigation complexity: one_click (main page links directly to all sub-pages)
- Anti-bot issues: none

## Obstacles & Dead Ends
- `Face.png` referenced in the XML Reference page returns S3 AccessDenied — this appears to be a reference to a face diagram used in the medical drawings reconstruction section that was not properly uploaded
- The main page's last-modified date (2023-11-27) predates the v22 certification (2025-08-14), suggesting the documentation may not have been updated for the latest version
- The Prime Suite Conversion Tool (needed to decrypt some exported files) is only available through the authenticated My Greenway support portal — not publicly accessible
