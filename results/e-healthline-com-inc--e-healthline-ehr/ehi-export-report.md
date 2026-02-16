# E*HealthLine.com, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf
- CHPL IDs: 10833
- Product: CARE© Integrated Hospital Information Management System
- Version: 10.0.0
- Certification Date: 2022-02-17

## Navigation Journal

1. Probed the registered URL with `curl -sI -L`:
   ```
   curl -sI -L "http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
   ```
   Result: HTTP 200, `Content-Type: application/pdf`, 265,837 bytes. Direct PDF download — no redirects, no authentication.

2. Downloaded the PDF:
   ```
   curl -sL "http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' \
     -o downloads/Electronic_Health_Information_Export.pdf
   ```
   Verified: `file` confirms "PDF document, version 1.4, 10 page(s)".

3. Examined the PDF: extracted text with `pdftotext`, rendered all 10 pages as images with `pdftoppm`. The PDF is text-based (not scanned), no embedded URLs, no attachments (`pdfdetach -list` reports 0 embedded files).

4. The PDF references "full Export Batch CCDA documentation for additional information" (p. 7). Probed for additional PDFs at `http://ehealthline.com/dev/pdf/` using 10 filename variations (Export Batch CCDA.pdf, ExportBatchCCDA.pdf, CDA Export.pdf, etc.) — all returned 404. The `/dev/pdf/` directory itself returns 403 Forbidden.

5. Checked `http://ehealthline.com/` homepage (148 KB HTML) for any links to PDFs or EHI-related content — found none.

6. No additional documentation artifacts were found beyond the single registered PDF.

## What Was Found

The registered URL delivers a single 10-page PDF titled "170.315(b)(10) Electronic Health Information Export" (version 2.0, dated October 24, 2023; PDF file last modified July 18, 2024). The document is a user guide combined with a high-level export format description.

### Export Mechanism

The export is performed via an **"Export Batch CCDA"** function accessible from the Data Maintenance Menu in the EHR. It supports:

- **Single patient export**: Select a patient by name or medical record number, choose provider, clinic, and optional chart document inclusion. Outputs a ZIP file.
- **Patient population export**: Select multiple patients (by name selection or MR# range). Same ZIP format.

The export is a desktop/server operation, not an API. Output is written to a UNC network path: `\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports`.

### Export Format

The export produces a **ZIP file** (`CDAXMLExport_8.Zip`) containing these components:

| File/Folder | Format | Content |
|---|---|---|
| **CCDA** | XML (HL7 C-CDA) | Clinical data compliant with USCDI v1 — standard clinical summary (problems, medications, allergies, labs, vitals, immunizations, procedures, etc.) |
| **BillingReport** | CSV | Patient financial transactions: patient info, transaction dates, charges, claims, descriptions, status |
| **demographics** | CSV | Patient key information, identification, contact, insurance |
| **Schedule** | CSV | Encounter records: appointment date, provider, location, appointment type, workflow, notes, note dates |
| **Documents** | CDA XML folder | Patient supporting documents/attachments |
| **Notes** | CDA XML folder | All clinical notes from previous medical visits/encounters |
| **PatientDocumentFiles** | CSV | Mapping file listing document attachments in the Documents folder |

Optional additions (new in the b(10) update):
- **Chart Documents**: Optionally included via `[Include Chart Documents]` checkbox
- **Sticky Notes on TIF docs**: Optionally included
- **Custom Patient Data Tables**: Automatically included in the CDA unless explicitly excluded via the "Exclude FHR" flag in General Table Setup

### Access Control

Export requires privileges granted by an admin user: the user must have `[Edit General Database Setup]` privilege AND either `[Print Documents]` or `[Chart Reviewer]` privileges in Security Roles Settings.

### FHR Exclusion Mechanism

Custom (user-created) Patient Data Tables are included by default in the CDA export. Administrators can exclude specific tables by setting the `[Exclude FHR]` flag in General Table Setup. This is the vendor's mechanism for scoping what constitutes the Formal Health Record.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered:**
- **Demographics** (dedicated CSV: patient key information, identification, contact, insurance)
- **Clinical summary data** (CCDA XML: problems, medications, allergies, labs, vitals, procedures, immunizations — standard USCDI v1 content)
- **Clinical notes** (dedicated Notes folder with CDA XML documents from all encounters)
- **Billing/financial data** (dedicated BillingReport CSV: charges, claims, transaction descriptions, status)
- **Encounter/scheduling data** (Schedule CSV: dates, providers, locations, appointment types)
- **Patient documents/attachments** (Documents folder + PatientDocumentFiles mapping CSV)
- **Custom Patient Data Tables** (included in CDA by default)

**Likely gaps or ambiguous coverage:**
- **Laboratory orders and results** — the CCDA would include lab results as standard USCDI content, but the eLab module stores far more detail (specimen collection, routing, preparation, quality assurance, auto-verification, reflex testing rules). The CCDA representation likely captures results but not the full lab workflow data.
- **Radiology orders, exams, and reports** — eRad data includes order entry, exam tracking, film tracking, transcription, and detailed reports. The CCDA would include some procedure/result data, but full radiology workflow detail (modality scheduling, film tracking, PACS image references) is unlikely to be captured in a CCDA-structured export.
- **Medical images** — PACS images are mentioned on the vendor's product page but the export documentation does not specifically mention image file export. Chart Documents *may* include some, but this is unspecified.
- **CPOE order detail** — the product has a full CPOE module with medication orders, allergy alerts, clinical decision support templates. Standard CCDA captures medication lists and allergy lists, but active orders, order history, and decision support interactions are likely not fully represented.
- **Medication administration records** — if the hospital module tracks MAR data (which a hospital system should), it's unclear whether this is included beyond what CCDA captures.
- **Material management / inventory** — these are operational/administrative data, not patient-specific EHI. Not a gap.
- **Bed management / ADT detail** — the Schedule CSV captures encounters, but detailed ADT events (transfers, bed assignments) may not be fully represented.
- **Financial management (SPHINX)** — billing is covered via BillingReport CSV, but the SPHINX module may contain additional financial management data. The BillingReport CSV description focuses on patient-facing billing (charges, claims, payments), which is the appropriate EHI scope.
- **Public health reporting data** — the product is certified for (f)(1)–(f)(7) but there's no mention of immunization registry submissions or syndromic surveillance data in the export. These are typically outbound reporting functions, not stored patient records, so this is not necessarily a gap.
- **EDIMS, OTIMS, INDS modules** — these are listed on the vendor's product pages (all returned 404), so their data content is unknown. If they store patient-level data, coverage is unclear.

### Export Format & Standards

The export uses a **hybrid approach**: HL7 C-CDA XML for clinical data + CSV files for billing, demographics, scheduling, and document mapping. This is a reasonable design for (b)(10):

- The **CCDA component** covers USCDI v1 clinical data in a recognized standard format. However, it inherently carries the limitations of C-CDA — it's a clinical summary standard, not a bulk data format for everything in a hospital database.
- The **CSV supplements** (BillingReport, demographics, Schedule, PatientDocumentFiles) extend beyond what C-CDA covers, which shows the vendor recognized that CCDA alone is insufficient for (b)(10).
- The **Notes and Documents folders** export narrative clinical content and attachments in CDA XML format.
- **Custom Patient Data Tables** are included in the CDA, which is a meaningful attempt to capture non-standard data.

**Format appropriateness**: The hybrid CCDA + CSV approach is better than a pure CCDA-only export. A third party could reconstruct most of the patient record from this export, though the CSV file structures are described only at a high level (column names are not documented in the PDF, nor are there sample files or schemas).

### Documentation Quality

**Weak.** The documentation is a 10-page PDF that is more of a user guide and compliance attestation than a technical specification:

- **No data dictionary**: There are no field-level definitions for the CSV files (BillingReport, demographics, Schedule, PatientDocumentFiles). Column names, data types, formats, value sets, and cardinality are not documented.
- **No schema files**: No XSD for the CDA documents, no CSV header specifications, no sample data.
- **No sample export files**: No example ZIP file or representative excerpts.
- **No worked examples**: The instructions describe the UI steps but not the resulting data structures.
- **CCDA specification punted to HL7**: The document says "The specifications for the CCDA can be obtained from the HL7 website" — useful for the standard CCDA sections but says nothing about how E*HealthLine-specific data (custom tables, billing, scheduling) maps into or supplements the standard.
- **Incomplete sentences**: Steps 14 (p. 9) and 15 (p. 10) both end with "For additional details on the export format and default paths," — the sentence is cut off, suggesting the document references another document that is not provided.
- **Confusing footer**: Every page has a footer reading "170.315(g)(10) — Standardized API For Patient and Population services" which is the wrong ONC criterion. The document is about (b)(10), not (g)(10). This is a copy-paste error from a different document template.
- **No screenshots**: Despite describing a multi-step UI workflow, the document contains zero screenshots of the export interface.

A developer trying to import this data would need to actually perform an export and reverse-engineer the CSV column structures and CDA mapping from sample output.

### Structure & Completeness

- **Granularity**: File-level descriptions only (7 file types in the ZIP). No field/column-level documentation.
- **Coded fields**: Not documented. Value sets for status fields, appointment types, etc. are unknown.
- **Relationships**: The PatientDocumentFiles CSV maps to the Documents folder, but other inter-file relationships are not described.
- **Versioning**: Two revision entries (v1.0 Oct 14, 2023 and v2.0 Oct 24, 2023), both described identically as "Original Document."
- **The "Exclude FHR" mechanism** is documented procedurally but raises questions: what is included vs. excluded by default? Which system Patient Data Tables exist? This is left entirely opaque.

### (b)(10) vs (g)(10) Assessment

This vendor has made a **genuine effort** at (b)(10) differentiation. Unlike many vendors who simply point to their FHIR API, E*HealthLine:
- Exports billing data as a separate CSV (not part of standard CCDA)
- Exports scheduling/encounter data as a separate CSV
- Exports patient documents and attachments as separate folders
- Includes custom Patient Data Tables in the CDA by default
- Provides a mechanism to scope the Formal Health Record

However, the export is still built on top of the existing CCDA export infrastructure ("Export Batch CCDA"), and the clinical data portion relies on USCDI v1 CCDA, which only covers the standard clinical summary domains. The breadth of a full hospital information system — lab workflow detail, radiology workflow, CPOE order history, medication administration records — is unlikely to be fully captured in this format.

## Access Summary
- Final URL (after redirects): http://ehealthline.com/dev/pdf/Electronic%20Health%20Information%20Export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

1. The PDF references "full Export Batch CCDA documentation for additional information" (page 7) and steps 14/15 end with "For additional details on the export format and default paths," (truncated sentence) — suggesting a separate detailed document exists but is not publicly linked or available.
2. Probed 10 filename variations at `http://ehealthline.com/dev/pdf/` — all returned 404. The directory itself returns 403 Forbidden.
3. The homepage (`http://ehealthline.com/`) contains no links to PDFs or EHI documentation.
4. The PDF footer on every page incorrectly references "170.315(g)(10) — Standardized API For Patient and Population services" instead of (b)(10), suggesting the document was created from a (g)(10) template.
5. The PDF is copy-protected (encrypted with RC4, copy:no), though text extraction via pdftotext still works.
