# Metasolutions Inc — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.zoommd.com/company-certifications-awards/
- CHPL IDs: 11182 (15.04.04.1979.Zoom.41.01.1.221230)
- Product: ZoomMD v4.1
- Certified: 2022-12-30

## Navigation Journal

1. **Probed the registered URL** with curl:
   ```bash
   curl -sI -L "https://www.zoommd.com/company-certifications-awards/" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200 with `text/html; charset=UTF-8`. WordPress site (PHP/7.3.33, Apache).

2. **Fetched the page HTML** (77,953 bytes) and searched for document links:
   ```bash
   curl -sL "https://www.zoommd.com/company-certifications-awards/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/page.html
   ```
   Found PDFs including `ZoomMD_EHI_Export_Format_Specification.pdf` alongside several Real World Test plans/results and a mandatory disclosure statement.

3. **Downloaded the EHI Export Format Specification PDF** directly:
   ```bash
   curl -sL "https://www.zoommd.com/ZoomMD_EHI_Export_Format_Specification.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/ZoomMD_EHI_Export_Format_Specification.pdf
   ```
   Verified: `file` reports "PDF document, version 1.4, 4 page(s)", 1,712,633 bytes.

4. **Examined the PDF** with `pdftotext` and `pdftoppm` to understand content and review screenshots embedded within it.

5. **Checked the API documentation pages** linked from the certifications page:
   - `https://www.zoommd.com/zoommd-api` — older XML/REST API for patient data access (returns C-CDA in base64). This is for (g)(7)/(g)(9) criteria, not the (b)(10) EHI export.
   - `https://www.zoommd.com/zoommd-file-api-documentation` — FHIR R4 API documentation for (g)(10) Standardized API. Describes SMART App Launch integration. Not the EHI export mechanism.
   - `https://www.zoommd.com/zoommd-file-api-endpoints` — Lists FHIR R4 endpoints (staging: `https://fhirstaging.zoommd.com/r4`, production: `https://fhir.zoommd.com/r4`). Also (g)(10), not (b)(10).

   The API pages are for the FHIR standardized API (g)(10) requirement, which is separate from the EHI export (b)(10). The EHI export is a ZIP download mechanism through the application UI, not an API.

6. **Took screenshots** of the certifications page in the browser, scrolling to capture the EHI export link section.

## What Was Found

The EHI export documentation consists of a single 4-page PDF: **ZoomMD_EHI_Export_Format_Specification.pdf** (dated November 2023, authored by "CS Sekhar").

### Export Mechanism
The export is performed through the ZoomMD application UI:
- Navigate to **Settings > Interoperability > Data Export > Generate Summaries**
- All patients are displayed in a list
- Users can search/filter patients and select one or multiple patients
- Clicking "Export" generates a ZIP file downloaded to the user's local system with a date/time stamp
- A "Configure Schedule" option allows automated/scheduled exports
- Exported files can be re-downloaded from a "Data Export Summaries List" portlet on the user dashboard
- Access is role-controlled — ineligible users cannot perform exports

### Export Format
The export produces a **ZIP file** containing:
- One folder per patient
- Sub-folders containing:
  - **C-CDA documents** (per C-CDA Templates for Clinical Notes R2.1 Companion Guide, Release 2)
  - **PDF documents**, scanned paper, and digital records of faxes
  - **Clinical notes** in HTML format
  - **Image files** (JPEG, JPG, PNG)

### What's NOT in the Documentation
The PDF does not include:
- A data dictionary or field-level specification
- A list of which data domains or tables are exported
- Any description of the C-CDA template customizations or extensions
- Sample export files or example data
- Schema definitions (XSD, JSON Schema, etc.)
- Information about how billing data, scheduling data, or other non-clinical data is handled
- Any indication of what "all accessible EHI information" actually includes beyond C-CDA and document attachments

## Export Coverage Assessment

### Data Domain Coverage

The documentation is extremely vague about what data is actually exported. It says the export includes "all accessible EHI information" but the only concrete format details describe:

1. **C-CDA documents** — These would cover standard clinical data (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, clinical notes) but only to the extent captured in C-CDA R2.1 templates.

2. **PDF/scanned documents and faxes** — This covers document management content.

3. **Clinical notes in HTML** — Progress notes, encounter documentation.

4. **Image files** — Clinical images attached to patient records.

**Domains likely covered** (via C-CDA):
- Patient demographics
- Problem lists / diagnoses
- Medications and prescriptions
- Allergies
- Lab results
- Vital signs
- Immunizations
- Procedures
- Clinical notes (as HTML and within C-CDA)
- Implantable device identifiers
- Care plans / goals

**Domains with unclear or likely absent coverage:**
- **Billing data** — claims, superbills, charges, insurance eligibility, collections data. The documentation makes no mention of billing information in the export. ZoomMD has an integrated billing module, so this is a significant gap.
- **Scheduling data** — appointments, follow-ups. Not mentioned.
- **Insurance information** — eligibility, coverage details. Not mentioned.
- **E-prescribing details** — controlled substance prescriptions, pharmacy routing, formulary data. Only standard C-CDA medication data would be captured.
- **Lab orders** (as distinct from results) — CPOE order details may not survive C-CDA export.
- **Patient portal communications** — messages, chat history. Not mentioned.
- **Transcription records** — dictation metadata, transcription workflow data. Not mentioned.
- **Family health history** — ZoomMD is certified for (a)(12) but unclear if this is in the C-CDA export.
- **Quality measure data** — CMS measure tracking data. Not mentioned.
- **Public health reporting data** — immunization registry submissions, case reports. Not mentioned.

### Export Format & Standards

The export uses **C-CDA R2.1** as the primary structured format, supplemented by raw documents (PDF, HTML, images). This is a reasonable choice for clinical data — C-CDA is a well-understood standard — but it inherently limits coverage to the clinical domains that C-CDA templates support.

The critical question is whether the C-CDA export includes **all** data the product stores about patients, or only the standard USCDI/clinical summary subset. C-CDA R2.1 has templates for most clinical data, but it does not naturally accommodate:
- Billing records (claims, superbills, charges)
- Scheduling data
- Practice management data
- Custom fields or specialty-specific assessments
- Patient portal interaction history

Without a data dictionary or field mapping, it's impossible to verify what's included. The documentation describes the *container* (ZIP with C-CDA + documents) but not the *contents* at a field level.

A third party receiving this export could reconstruct a clinical summary of the patient but would likely be missing billing, scheduling, and administrative data.

### Documentation Quality

**Very poor.** The 4-page PDF is primarily a set of screenshots showing the export UI workflow — how to log in, where to click, how to select patients, and how to download. It reads like a minimal user guide created for certification compliance rather than a technical specification.

There is:
- No data dictionary
- No field-level documentation
- No schema files
- No sample exports
- No description of what C-CDA sections/templates are populated
- No mapping from ZoomMD's internal data model to the export format
- No description of how non-C-CDA data (billing, scheduling) is handled
- No versioning or change history

A developer receiving this export would know they're getting a ZIP with C-CDA files and document attachments, but would have no vendor-specific guidance on what to expect in those files.

### Structure & Completeness

The documentation provides essentially **zero** granularity below the format level. We know: ZIP > patient folders > C-CDA documents + PDFs + HTML notes + images. That's it. There is no table-level, field-level, or even section-level specification.

This is one of the most minimal EHI export documentation sets possible — it meets the bare letter of the requirement to have "format specification" documentation by naming the format (C-CDA R2.1) and the container (ZIP), but provides no substantive technical detail about what data is exported or how it's structured.

## Access Summary
- Final URL (after redirects): https://www.zoommd.com/company-certifications-awards/
- Status: found
- Required browser: no (PDF is directly linked, accessible via curl)
- Navigation complexity: one_click (single "Click Here" link on certifications page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The URL is live, the PDF downloads cleanly.
- The API documentation pages (ZoomMD API, FHIR API Documentation, FHIR API Endpoints) are for the (g)(10) FHIR API, not the (b)(10) EHI export. These were investigated but correctly excluded from the EHI export documentation.
- The FHIR API endpoints page contains a reference to `pc-fhir-stg.amazingcharts.com` which appears to be leftover from a template — suggesting the FHIR infrastructure may be shared/white-labeled.
