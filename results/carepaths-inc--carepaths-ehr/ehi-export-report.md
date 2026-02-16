# Carepaths Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://carepaths.com/features/onc-certification/b10-export-format/
- CHPL IDs: 10607
- Product: CarePaths EHR v19.11
- Certification date: 2021-04-08

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL:
   ```bash
   curl -sI -L "https://carepaths.com/features/onc-certification/b10-export-format/" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, content-type `text/html`, 93,196 bytes. No redirects.

2. **Fetched and examined page content:**
   ```bash
   curl -sL "https://carepaths.com/features/onc-certification/b10-export-format/" -H 'User-Agent: Mozilla/5.0' -o downloads/b10-export-format.html
   ```
   The page is static HTML (not a SPA). The main content is in a `<div class="prose">` block at lines 1177–1201 of the HTML. No JavaScript rendering required.

3. **Searched for downloadable files** — no PDF, ZIP, XLSX, CSV, JSON, XSD, or other downloadable artifacts linked from this page. The page contains only prose text describing the export.

4. **Checked related pages:**
   - `/features/onc-certification` — lists certified criteria. The (b)(10) entry links back to the same B10 export format page. No additional export documentation.
   - `/api-documentation` — 309 KB page documenting the FHIR (g)(10) API (patient-facing REST API). This is the g(10) standardized API, not the b(10) EHI export mechanism. Contains organization FHIR API URLs and FHIR resource documentation. Not relevant to EHI export.

5. **Took screenshots** of the full page in the browser for archival purposes.

No additional linked documentation, downloadable files, data dictionaries, sample exports, or schema files were found anywhere on the carepaths.com site related to the (b)(10) EHI export.

## What Was Found

The entire EHI export documentation consists of a single web page (~25 lines of prose) at the registered URL. It describes:

### Export Mechanism
- Admin users with "record management permissions" access the EHI export from the "exports dropdown" on the patient management overview.
- Users select which patients to export.
- The system produces a single `.zip` file per patient containing the relevant files.
- The ZIP is delivered through the internal messaging system and can be downloaded directly.
- For full patient population (bulk) exports, users must contact support or schedule outside business hours due to resource impact.

### Files Included in the Export

The documentation lists 7 categories of files in each patient's ZIP:

| # | File | Format | Naming Convention |
|---|------|--------|-------------------|
| 1 | CCD (Continuity of Care Document) | XML (CDA) | `cda_PATIENT_NAME.xml` |
| 2 | Accounting Statement | PDF | `PATIENT_ID_Statements_asOfDate.pdf` |
| 3 | Messaging History | TXT | `PATIENT_ID_Message_History_asOfDate.txt` |
| 4 | Patient Charts (completed service documents, grouped by year) | PDF | `PATIENT_ID_Chart_Year.pdf` |
| 5 | Audit Logs (changes to patient chart/account) | (format unspecified) | (naming unspecified) |
| 6 | Appointment History and Statuses | (format unspecified) | (naming unspecified) |
| 7 | Document/image uploads from the patient's facesheet | Original format | Original format as uploaded |

There is no data dictionary, no field-level documentation, no schema files, no sample exports, and no worked examples.

## Export Coverage Assessment

### Data Domain Coverage

CarePaths EHR is a behavioral health EHR storing clinical documentation (intakes, progress notes, treatment plans), standardized assessments (PHQ-9, GAD-7, OQ-45, etc.), billing/claims data, messaging, scheduling, and patient-uploaded documents.

**What appears to be covered:**
- **Clinical documentation** — via the CCD (CDA XML) and the Patient Charts PDFs. The CCD would capture structured clinical data (demographics, problems, medications, allergies, vitals). The chart PDFs presumably contain rendered copies of progress notes, intake assessments, and treatment plans.
- **Billing/accounting** — the Accounting Statement PDF covers patient-level financial transactions (charges, payments, adjustments).
- **Messaging** — the Message History TXT file captures patient-provider secure messages.
- **Appointments** — appointment history and statuses are included.
- **Document uploads** — patient-uploaded documents and images are included in original format.
- **Audit logs** — included (though note: audit logs are not EHI per the designated record set definition, so their inclusion is a bonus).

**What appears to be missing or uncertain:**
- **Outcomes/assessment data (MBC)** — CarePaths' core differentiator is measurement-based care with dozens of standardized instruments (PHQ-9, GAD-7, OQ-45, HAM-A, SCARED, etc.) and longitudinal tracking. There is no mention of assessment response data in the export. The CCD likely does not include raw assessment scores and longitudinal tracking data. This is a significant gap — these are clinical records used to make treatment decisions.
- **Treatment plans and goals** — While these may be captured in the chart PDFs as rendered documents, the structured data (goal status, target dates, interventions) would be lost in PDF rendering.
- **Diagnoses as structured data** — The CCD should capture active diagnoses, but the completeness of diagnosis history (including resolved diagnoses, date ranges, and associated metadata) is unclear.
- **E-prescribing / medication data** — Medication data in the CCD would be limited to whatever CarePaths stores locally. The DrFirst/Rcopia integration data (prescription history, medication monitoring) may or may not be included.
- **Claims data (X12)** — The accounting statement is a PDF summary. Whether the underlying X12 claims, remittance records, and payment details are exported as structured data is unclear — a PDF statement is a significant downgrade from the structured billing records the system maintains.
- **Insurance/enrollment information** — Not specifically mentioned.
- **Supervisor/supervisee workflow data** — Notes requiring co-signatures, review status, supervision notes — likely rendered in chart PDFs but structural metadata would be lost.

**The fundamental problem: PDF rendering destroys data fidelity.** The export strategy of rendering clinical documentation into annual PDF compilations means that structured clinical data (diagnoses with ICD codes, CPT codes on services, assessment scores, treatment plan goals with status tracking) is flattened into human-readable documents. A third party could read the PDFs but could not computationally process, query, or import this data into another system.

### Export Format & Standards
- **CCD/CDA XML**: A recognized HL7 standard, but CDA is designed for clinical summaries, not comprehensive data export. A CCD typically covers demographics, problems, medications, allergies, vitals, procedures, and results — essentially the same USCDI/US Core data that (g)(10) covers. It would not capture behavioral health assessments, custom forms, or detailed billing records.
- **PDF**: Not a computable format. Accounting statements, chart compilations, and audit logs as PDFs cannot be imported into another system without manual re-entry or OCR.
- **TXT**: Messaging history as plain text is minimally computable — it preserves content but likely loses metadata (timestamps, sender identification, read status).
- **Original format uploads**: Appropriate — returning documents in their original format is correct.

This export is essentially a **print-to-file** approach rather than a structured data export. The CCD provides some structured clinical data, but the remainder is PDFs and text files. This is a common pattern among small vendors — it satisfies the letter of the regulation (data is exported) but not the spirit (data should be usable).

### The (b)(10) vs (g)(10) Question
This vendor has NOT simply repackaged their FHIR API as the (b)(10) export. The export is a distinct mechanism (ZIP file per patient via the admin UI). However, the CCD XML component of the export covers roughly the same clinical data scope as the (g)(10) FHIR API would — structured clinical summaries — while everything else is rendered as PDFs. The export goes beyond clinical data (billing, messaging, appointments, uploads), but does so in non-computable formats.

### Documentation Quality
- **Extremely minimal.** The entire documentation is ~25 lines of prose on a single web page.
- **No data dictionary.** There is no field-level documentation for any of the exported files.
- **No schema or format specification.** The CCD is described as "CDA XML" but there's no indication of which CDA template, what sections are included, or what coded values are used.
- **No sample exports.** No example files are provided.
- **No import guidance.** A developer receiving this export would not know the structure of the CCD, the format of the audit logs, or the layout of the messaging history file without reverse-engineering actual exports.
- **Two of the seven file categories don't even specify their format** (audit logs and appointment history).
- **Incomplete naming conventions.** The naming scheme is provided for 4 of 7 file types.
- **Could a developer implement an import?** No. The documentation is insufficient for a third party to build an automated import of this data. They could display the PDFs and parse the CCD with a generic CDA parser, but the behavioral health-specific data (assessments, treatment plans) would require manual extraction from PDFs.

### Structure & Completeness
- **Granularity:** File-type level only. No table names, field names, data types, value sets, or relationships documented.
- **Coded fields:** Not documented.
- **Relationships:** Not documented.
- **Versioning:** None visible. Page copyright says 2023.

## Access Summary
- Final URL (after redirects): https://carepaths.com/features/onc-certification/b10-export-format/
- Status: found
- Required browser: no (static HTML, no JS rendering needed)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The page loaded cleanly via curl and browser.
- The page contains no downloadable files, no links to external documentation, and no links to further detail pages about the export.
- The `/api-documentation` page documents the FHIR (g)(10) API only — not relevant to the (b)(10) EHI export.
- The `/features/onc-certification` page links back to the same B10 export format page with no additional context.
