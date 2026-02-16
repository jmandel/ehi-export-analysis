# Edvak Technologies Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://edvak.com/ehi-export
- CHPL IDs: 11656
- Product: Edvak EHR v1
- Certification date: 2025-06-13

## Navigation Journal

### Step 1: Initial probe of registered URL
```bash
curl -sI -L "https://edvak.com/ehi-export" -H 'User-Agent: Mozilla/5.0'
```
HTTP/2 200, Content-Type: text/html; charset=UTF-8, served via Cloudflare. No redirects. The page loaded directly as a static HTML page with embedded screenshots.

### Step 2: Fetched and examined the page
```bash
curl -sL "https://edvak.com/ehi-export" -H 'User-Agent: Mozilla/5.0' -o downloads/ehi-export-page.html
```
50,380 bytes. The page contains the full EHI export documentation as a single page with inline text and embedded screenshot images. No download links to PDFs, ZIPs, or other structured documentation files.

### Step 3: Downloaded all embedded screenshots
The page references 10 screenshots showing the export workflow. Images are hosted at `https://edvak.com/assets/images/certification/`:
- Single patient export: `SP_!A.png` (Step 1: Dashboard → Patients), `SP_1.png` (Step 2: Patient list), `SP_2.png` (Step 3: Facesheet with "Export CCDA" button), `SP_3.png` (Step 4: Save dialog)
- Population export: `MP_1A.png` (Step 1: Dashboard → Analytics), `MP_1.png` (Step 2: CCDA tab), `MP_7A.png` (Step 3: Patient selection panel), `MP_4.png` (Step 4: Select patients & Export), `MP_6.png` (Step 5: ZIP download), `MP_7.png` (contents of the ZIP)

```bash
curl -sL "https://edvak.com/assets/images/certification/SP_1.png" -o screenshots/SP_1.png
# (repeated for each image)
```

Note: `SP_!A.png` required URL-encoding the `!` as `%21` to download correctly.

### Step 4: Checked certification page for additional export documentation
```bash
curl -sL "https://edvak.com/certification" -o /tmp/edvak-cert.html
```
The certification page links to:
- EHI Export Documentation → https://edvak.com/ehi-export (the same page)
- API Documentation → https://edvak.com/docs (redirects to https://stg.edvak.com/docs/)
- DSI Documentation → /dsi-documentation (not EHI-related)
- Mandatory Disclosures PDF → ./assets/docs/Mandatory_Disclosures_Letter_Template.pdf (costs/fees disclosure, not EHI-related)

### Step 5: Examined API documentation site
The API docs site at `https://stg.edvak.com/docs/` (hosted on Apidog) has two sections:
1. **FHIR API** — Standard FHIR R4 API for §170.315(g)(10). Covers SMART on FHIR, Bulk FHIR Export, US Core IG v6.1.0. This is the standardized API, not the EHI export.
2. **CCDA API** — A separate API for C-CDA document retrieval at `https://darwinapi.edvak.com/ccda/ccda/patient_data`. This API appears to be the programmatic counterpart to the EHI export feature, as the EHI export produces C-CDA documents.

Downloaded the CCDA API documentation pages:
```bash
curl -sL "https://stg.edvak.com/docs/introduction-1018024m0" -o downloads/ccda-api-introduction-1018024m0.html
curl -sL "https://stg.edvak.com/docs/ccda-retrieval-16935528e0" -o downloads/ccda-api-ccda-retrieval-16935528e0.html
# (and 4 other pages)
```

The CCDA API section has 6 pages: Introduction, Authentication & Access, Errors, APIs overview, Generate Token (POST), and CCDA Retrieval (GET).

### Step 6: Took full-page screenshot of EHI export page
Navigated in browser and captured `ehi-export-page-full.png`.

## What Was Found

### EHI Export Documentation (Main Page)
The EHI export documentation at https://edvak.com/ehi-export is a single HTML page that describes two export modes:

**Single Patient EHI Export:**
1. Navigate to the Patients screen
2. Select a patient
3. Go to the Facesheet section and click "Export CCDA"
4. Save the downloaded file

The exported file is named using the pattern `PATIENTNAME-TIMESTAMP` (e.g., `ALICE_NOMEN-1747301459482`). It's a single C-CDA XML file.

**Patient Population EHI Export:**
1. Navigate to the Analytics screen
2. Go to the CCDA tab
3. Click the Export button (download icon)
4. A "CCDA Export" panel appears on the right, listing all patients with checkboxes and a "Select All" option
5. Select patients and click Export
6. A ZIP file is downloaded (e.g., `ccda-bulk-174730176986`) containing individual C-CDA files for each selected patient

**Export format:** All exports are in C-CDA (Consolidated Clinical Document Architecture) format. The documentation states the export includes: "demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, and clinical notes."

### CCDA API Documentation
The CCDA API at `https://darwinapi.edvak.com` provides programmatic access to C-CDA documents:

- **Generate Token** (POST `/ccda/ccda/generate-token`): OAuth 2.0 ROPC flow using client_id, client_secret, username, and password. Returns a bearer token valid for 900 seconds (15 minutes).
- **CCDA Retrieval** (GET `/ccda/ccda/patient_data`): Takes a `patient_token` (required), optional `date` or `start_date`/`end_date` range parameters. Returns a C-CDA XML document (application/xml).

The API response example shows a "Continuity of Care Document" with templateId `2.16.840.1.113883.10.20.22.1.1` (extension 2015-08-01), which is the standard CCD template. The example only shows the document header and patient demographics (patientRole with id, address, telecom, name, gender, birthTime, raceCode, languageCommunication).

The CCDA API Introduction page states the API "conforms to the G9 certification standard for electronic health information access" — this appears to reference §170.315(g)(9) (Application access — all data request), not §170.315(b)(10).

### What's Missing
- **No data dictionary.** There is no field-level documentation describing what C-CDA sections are included, what coded values are used, or how Edvak-specific data maps to C-CDA structures.
- **No schema files.** No XSD, Schematron, or other machine-readable schema is provided or referenced.
- **No sample export files.** The API docs show a truncated XML example (header/demographics only), but no complete sample C-CDA document is available for download.
- **No documentation of C-CDA sections included.** The text lists "demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, and clinical notes" but doesn't specify the corresponding C-CDA section templateIds or entry-level templates.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation claims the export includes:
- Demographics ✓
- Medications ✓
- Problems ✓
- Allergies ✓
- Vitals ✓
- Immunizations ✓
- Lab results ✓
- Procedures ✓
- Care plans ✓
- Clinical notes ✓

Based on the product research, Edvak EHR stores significantly more data than what the export claims to cover. **The following data domains appear to be missing or not mentioned in the export:**

- **Billing and claims data** — Edvak has a full billing/RCM module with ICD/CPT code capture, claims submission, denial tracking, and payment processing. None of this appears in the export. The Facesheet screenshot shows a "Billing" tab, but the export is triggered from the Facesheet level, not from within the billing section.
- **Insurance/enrollment data** — Real-time eligibility checks and insurance information are tracked but not mentioned in the export.
- **Referrals** — The product has referral management. The Facesheet shows a "Referrals" tab, but referrals are not listed in the export contents.
- **Documents** — Edvak has document management and fax management, but stored documents/attachments are not mentioned in the export.
- **Patient communications** — Two-way SMS, phone calls, and portal messages are not mentioned.
- **Encounter/visit history** — Not explicitly listed, though clinical notes may capture some of this.
- **E-prescribing history** — The product connects to Surescripts for e-prescribing, but prescription transmission history isn't mentioned.
- **Imaging orders and results** — The Facesheet shows "Labs & Imaging" as a combined section, but only "lab results" are mentioned in the export.
- **Patient-reported data** — Patient intake forms with AI auto-charting (Premium tier) generate data that may not be captured in the C-CDA.
- **Goals** — The Facesheet shows a "Goals" section, and the API docs show "Goals" as a FHIR resource, but the EHI export page text does not mention goals (though "care plans" is listed, which may include goals).
- **Assessments and Interventions** — The Facesheet shows sections for "Assessments" and "Interventions" which are not explicitly mentioned in the export.

### Export Format & Standards

The export uses C-CDA (HL7 CDA R2) format, specifically the Continuity of Care Document (CCD) template. This is a recognized healthcare standard, but it has inherent limitations for a (b)(10) EHI export:

- **C-CDA is a clinical summary format**, not a database export format. It is designed for transitions of care and summarization, not for comprehensive data export. Many data types that Edvak stores (billing, claims, referrals, documents, communications) have no natural representation in C-CDA.
- The use of C-CDA templateId `2.16.840.1.113883.10.20.22.1.1` (2015-08-01 extension) confirms this is a standard CCD — the same document type used for transitions of care under §170.315(b)(1). This raises the question: **is the (b)(10) export simply a re-export of the same CCD document used for transitions of care?**
- The data domains listed (demographics, medications, problems, allergies, vitals, immunizations, lab results, procedures, care plans, clinical notes) are essentially the USCDI v1/v3 clinical data classes — the same data covered by the FHIR (g)(10) API. This is a strong indicator that the (b)(10) export is functionally equivalent to the (g)(10) FHIR API output, just delivered in C-CDA format rather than FHIR.

**This is a textbook example of the (b)(10) vs (g)(10) confusion.** The vendor appears to have satisfied the (b)(10) requirement by exporting a C-CDA CCD — which covers clinical summary data — rather than exporting all electronic health information in the designated record set. Billing data, referral tracking, patient communications, document attachments, and other non-clinical-summary data are absent.

A third party could reconstruct a clinical summary from this export but could not reconstruct the full patient record, including billing history, referral chains, attached documents, or communication logs.

### Documentation Quality

The documentation is minimal:
- **No data dictionary.** There are no field-level definitions, no mapping between Edvak's internal data model and C-CDA sections, and no specification of coded value sets used.
- **The instructions are clear but shallow.** The step-by-step screenshots effectively show how to perform the export, but there's no technical depth about what's in the export.
- **The API documentation adds some structure** but only shows the response schema at a high level (document header and patient demographics). The full set of C-CDA sections in the body is not documented.
- **No sample files.** A developer trying to build an import for Edvak C-CDA exports would have no reference document to work from.
- **The documentation reads as a compliance checkbox** — enough to demonstrate the feature exists, but not enough for someone to meaningfully work with the exported data.

### Structure & Completeness

- **Granularity:** The documentation only identifies data domains at the category level (e.g., "medications," "allergies"). There is no table-level, field-level, or entry-level documentation.
- **Coded fields:** No value sets or code systems are documented beyond what's implied by the C-CDA standard.
- **Relationships:** No documentation of how entities relate to each other within the export.
- **Versioning:** No version history or change log for the export documentation.

## Access Summary
- Final URL (after redirects): https://edvak.com/ehi-export
- Status: found
- Required browser: no (static HTML page, all content visible in curl)
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare present but no blocking)

## Obstacles & Dead Ends
- The screenshot `SP_!A.png` required URL-encoding the exclamation mark (`%21`) to download correctly; the un-encoded URL returned HTML instead of an image.
- The CCDA API docs are hosted on a JavaScript-heavy Apidog platform (`stg.edvak.com/docs/`), requiring browser rendering to read. Downloaded raw HTML pages contain the content embedded in script tags but require JS execution to render.
- The certification page EHI Export section has copy-paste description text that doesn't match the EHI export page text — it says "Edvak's EHR platform offers FHIR-enabled APIs that empower developers and healthcare partners to securely integrate with patient data systems" as a description for the EHI Export section, which is the same text used for the FHIR API section. This suggests the descriptions were copied without tailoring.
