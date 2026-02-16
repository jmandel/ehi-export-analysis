# Prime Clinical Systems, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.primeclinical.com/wp-content/themes/BLANK-Theme/images/EHI_Export_170.315_b10.pdf
- CHPL ID: 10791
- Product: Patient Chart Manager, Version 7.1
- Certification date: 2022-01-14

## Navigation Journal

1. **Initial probe** — the registered URL is a direct PDF download:
   ```bash
   curl -sI -L "https://www.primeclinical.com/wp-content/themes/BLANK-Theme/images/EHI_Export_170.315_b10.pdf" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, `content-type: application/pdf`, `content-length: 4300225` (4.3 MB). No redirects. Direct file download.

2. **Downloaded the PDF**:
   ```bash
   curl -sL "https://www.primeclinical.com/wp-content/themes/BLANK-Theme/images/EHI_Export_170.315_b10.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/EHI_Export_170.315_b10.pdf
   ```
   Verified: `file` reports "PDF document, version 1.7, 3 page(s)". Created by PDFium, dated 2026-01-13.

3. **Extracted text** via `pdftotext` — clean extraction, all 3 pages readable. Rendered pages as PNG via `pdftoppm -r 150` to capture embedded screenshots of file explorer windows.

4. **Checked for companion documents** — the PDF references "See Including and Excluding Data" (underlined, suggesting a link). Probed variations of this filename at the same URL path:
   ```bash
   curl -sI "https://www.primeclinical.com/wp-content/themes/BLANK-Theme/images/Including_and_Excluding_Data.pdf"
   ```
   All candidates returned HTTP 200 but with `content-type: text/html` and `content-length: 3799` — the server returns the site maintenance page for non-existent paths rather than a 404. No companion document exists.

5. **Checked the vendor homepage** — `https://www.primeclinical.com/` displays "This site is currently undergoing scheduled maintenance. Please check back soon." Paths like `/ehi/`, `/compliance/`, `/interoperability/`, `/onc/` all return the same maintenance page.

6. **Checked mandatory disclosure PDF** — `https://www.primeclinical.com/wp-content/themes/BLANK-Theme/images/Mandatory-Disclosure.pdf` exists (582 KB) but contains only certification criteria listing, pricing, and legal text. No additional EHI export documentation.

7. **No embedded URLs or attachments** in the PDF — `pdfdetach -list` reports 0 embedded files. The only URL in the PDF text is a self-reference to the PDF's own URL.

## What Was Found

The entire EHI export documentation is a single 3-page PDF titled "Export Format & Naming Conventions," updated 12/23/2025 for PCM Ver. 7.1.1877.

### Export Mechanism

The export produces multiple ZIP files stored on a network share at:
`\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports_#` (where # is a session ID)

The export has three output components:

**1. XMLDATAExport_#.zip** — The core data export, containing XML files in Microsoft ADO (ActiveX Data Objects) recordset format:
- `CHART_DOCS;DataTable.xml` — chart document metadata for the exported date/MR range
- `CHART_STORE;DataTable.xml` — chart storage details
- `PATIENT;DataTable.xml` — patient data tables
- Additional per-patient XML files (e.g., `PT_ALLERGIES;DataTable.xml`, `PT_COMPLAINTS;DataTable.xml`)

The PDF shows a screenshot of the ZIP contents with 5 visible XML files: CHART_DOCS, CHART_STORE, PATIENT, PT_ALLERGIES, PT_COMPLAINTS (sizes ranging from 6 KB to 39 KB).

**2. CDAXMLExport_1.zip** — C-CDA documents, included "only with Bulk CCDA Export."

**3. CDAXMLDOC.Zip** — Chart documents exported as embedded PDFs in C-CDA format, with a naming convention encoding MRN, clinic, account, and document IDs.

### Export Format Details

- Clinical data is exported as **C-CDA R2.1** documents
- Underlying data tables are exported as **Microsoft ADO XML recordsets** (Visual Basic 6.0 `adPersistXML` format)
- The PDF includes VB6 code examples showing how data is serialized via `rs.Save ... adPersistXML` and can be deserialized via `rstTemp.Open`
- The export is controlled by checkboxes: with none selected, only "Patient Data" is exported; with checkboxes selected, exported files vary
- There is a reference to "Including and Excluding Data" options (a HIDE feature) but this companion document was not found online

### Data Migration Section

Section C of the PDF, "Data Export for Migrating to a Different EHR," explains that the XML files use Microsoft ADO recordset format and provides code examples for reading them. This suggests the export is designed to be programmatically processable, though it requires understanding of ADO XML format.

### Table Names Visible in Screenshots

From the screenshots embedded in the PDF, the following data tables are visible in the export:
- `CHART_DOCS;DataTable.xml`
- `CHART_STORE;DataTable.xml`
- `PATIENT;DataTable.xml`
- `PT_ALLERGIES;DataTable.xml`
- `PT_COMPLAINTS;DataTable.xml`

## Export Coverage Assessment

### Data Domain Coverage

**What appears covered (based on document and table names):**
- Patient demographics (PATIENT table)
- Allergies (PT_ALLERGIES table)
- Complaints/problems (PT_COMPLAINTS table)
- Chart documents — clinical notes, scanned documents, faxes (CHART_DOCS, CHART_STORE tables; chart documents exported as embedded PDFs in C-CDA)
- C-CDA clinical summaries (via the Bulk CCDA Export option)

**What is NOT documented and likely missing or unclear:**
- **Billing/claims data** — The product research identifies extensive practice management functionality (claims processing, CMS-1500 forms, payment posting, aging reports, charge posting). None of these billing tables appear in the export documentation. This is a significant gap for a (b)(10) export.
- **Medications/prescriptions** — The product has e-prescribing. No medication or prescription data table is mentioned.
- **Lab results** — The product integrates lab results. No lab data table is mentioned.
- **Immunizations** — The product reports to immunization registries. No immunization table is mentioned.
- **Vital signs** — Standard EHR data, not mentioned.
- **Procedures** — Not mentioned.
- **Insurance/eligibility data** — The product manages insurance verification and enrollment. Not mentioned.
- **Scheduling/appointments** — While appointment data is borderline for EHI scope, the product's scheduling data that documents visit history may qualify.
- **Care plans** — Listed as a product feature, not mentioned in export.
- **Imaging data** — DICOM-compatible images are a product feature. Not mentioned in export.

**Critical ambiguity:** The documentation states that "all patient data tables" are included in the PATIENT;DataTable.xml export (except those hidden via HIDE option), but it provides no listing of what those data tables actually are. The five tables visible in the screenshot may be a small sample — or they may be the complete set. Without a data dictionary or table listing, it's impossible to assess coverage. The phrase "all patient data tables" *could* mean comprehensive coverage, but the documentation doesn't prove it.

**The (b)(10) vs (g)(10) question:** This is NOT a case of conflating (b)(10) with (g)(10). The export is clearly a proprietary database dump (ADO XML recordsets) plus C-CDA documents — not a FHIR API. However, the scope question remains: does the export include *all* patient data from the system, including billing and practice management data? The documentation doesn't answer this.

### Export Format & Standards

- **Primary format:** Microsoft ADO XML recordsets — a proprietary XML serialization of database tables from Visual Basic 6.0 era technology. This is a legitimate data export format that preserves table structure and data types, but it is vendor-specific and requires ADO-aware tooling to parse.
- **Secondary format:** C-CDA R2.1 for clinical documents and bulk CCDA export.
- **Embedded documents:** Chart documents (scanned papers, faxes, etc.) are exported as embedded PDFs within C-CDA XML files.
- The ADO XML format preserves the database schema (field names, types) within each XML file, making it self-describing to some degree. However, relationships between tables are not documented.
- A third party could parse the XML files with ADO-compatible tools or by parsing the XML schema embedded in each file, but cross-table relationships would need to be inferred from field names (e.g., MRN fields linking patient data across tables).

### Documentation Quality

- **Very minimal.** Three pages covering only file naming conventions, directory structure, and a VB6 code example for reading the files. No substance about the *data* being exported.
- **No data dictionary.** There is no listing of tables, fields, data types, or value sets. The documentation tells you file naming patterns but not what's inside the files.
- **No field-level documentation.** A developer receiving this export would need to reverse-engineer the ADO XML schema from the exported files themselves.
- **No sample data.** No example exports or test data provided.
- **No value set documentation.** Coded fields (diagnoses, medications, procedures) are not described.
- **Screenshots are helpful but limited.** The embedded Windows Explorer screenshots show real export file structures, which provides some concrete information about what files to expect.
- **References to undocumented features.** "See Including and Excluding Data" is referenced but the companion document is not publicly available. The HIDE option for excluding tables is mentioned but not explained.
- **Recently updated.** The document is dated 12/23/2025 for PCM Ver. 7.1.1877, indicating active maintenance. However, the content remains sparse despite being current.

### Structure & Completeness

- **Table-level granularity only.** The documentation shows table names (CHART_DOCS, CHART_STORE, PATIENT, PT_ALLERGIES, PT_COMPLAINTS) but no field/column definitions within those tables.
- **No schema documentation.** The ADO XML files are self-describing (they embed schema), but no external schema documentation is provided.
- **No relationship documentation.** How tables relate to each other is not described, though field naming conventions (MRN, clinic keys, account numbers) hint at linkages.
- **No versioning or change history** beyond the document date.
- Could a developer implement an import? Partially — they could parse the ADO XML files using the provided VB6 code patterns, but they would need to discover the schema from the data itself rather than from documentation. Cross-table relationships would require reverse engineering.

### Overall Assessment

This is a **bare-minimum compliance document** that describes how to find and open export files, but provides almost no information about the data being exported. The export mechanism itself appears reasonable — a database dump in ADO XML format plus C-CDA documents covers the technical requirement. However, the documentation fails to demonstrate what data domains are included, making it impossible to independently assess whether the export covers "all electronic health information" as required by (b)(10).

The strongest signal is the phrase "all patient data tables included" in the PATIENT export description, but without a table listing, this is an unverifiable claim. Given that the product is a combined EHR + practice management system, the absence of any mention of billing data (claims, charges, payments, insurance) is the most notable gap.

The use of VB6/ADO XML format — while functional — is notably dated technology (circa late 1990s/early 2000s), consistent with the product's long development history since 1983.

## Access Summary
- Final URL (after redirects): https://www.primeclinical.com/wp-content/themes/BLANK-Theme/images/EHI_Export_170.315_b10.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The vendor's main website (primeclinical.com) is entirely in maintenance mode, preventing exploration of any additional documentation that might exist on the site.
- The PDF references "Including and Excluding Data" but this companion document is not available at the same URL path.
- The server returns HTTP 200 with the maintenance page HTML for all non-existent paths (no proper 404), making it impossible to reliably probe for additional documents by URL pattern.
- No data dictionary, schema file, or sample export data was found or referenced.
