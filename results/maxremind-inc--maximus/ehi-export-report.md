# MaxRemind Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://maxremind.com/maximusehr-certification/
- CHPL IDs: 11360
- Product: Maximus 1.0
- Certification date: 2023-10-31

## Navigation Journal

1. **Initial probe** of `https://maxremind.com/maximusehr-certification/`:
   ```bash
   curl -sI -L "https://maxremind.com/maximusehr-certification/" -H 'User-Agent: Mozilla/5.0'
   ```
   Result: HTTP 200, Content-Type: text/html, PHP/8.0.30 on Apache. WordPress/Elementor page.

2. **Fetched page** (~191KB HTML). Scanned for downloadable file links:
   ```bash
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/maxremind-page.html
   ```
   Found 4 file links:
   - `B10-Electronic-Health-information-Export.pdf` (EHI export — relevant)
   - `d12-Multi-factor-Authentication.pdf` (MFA — not relevant)
   - Two real-world testing PDFs (not relevant)

3. **Downloaded the B10 EHI Export PDF** directly:
   ```bash
   curl -sL "https://maxremind.com/wp-content/uploads/2024/04/B10-Electronic-Health-information-Export.pdf" -o downloads/B10-Electronic-Health-information-Export.pdf
   ```
   Verified: PDF document, 4 pages, 254,534 bytes. Created 2023-10-03 by Nouman Zafar using Microsoft Word.

4. **Extracted and read the PDF text** via `pdftotext`. The PDF describes six export components (detailed below) and references `https://documents.maximus.care/` for FHIR API specifications.

5. **Investigated `https://documents.maximus.care/`**: This is a React single-page application (SPA) serving FHIR API documentation. The static HTML shell is only 1,359 bytes; content is rendered client-side via `js/js_main.js`. Opened in browser and took a snapshot of the rendered content.

   The FHIR docs portal documents standard US Core STU3.1.1 resources: AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Location, MedicationRequest, Observation (vitals, labs, smoking status, pediatric), Organization, Patient, Practitioner, Procedure, Provenance. It includes OAuth2 authorization flow documentation, client registration, error codes, and terms & conditions.

6. **Checked FHIR API endpoints** — `https://fhir.maximus.care/api/metadata` and `https://fhir.maximus.care/api/.well-known/smart-configuration` both return HTTP 404. The API is not publicly accessible.

7. **Certification page structure** (Elementor-based WordPress): The page has a documentation section with three links:
   - FHIR API DOCUMENTATION → documents.maximus.care
   - ELECTRONIC HEALTH INFORMATION EXPORT → B10 PDF
   - MULTI-FACTOR AUTHENTICATION → d12 PDF
   Plus real-world testing plans/results (not EHI-relevant).

## What Was Found

The EHI export documentation consists of a single 4-page PDF describing six export components:

### Export Components (per the B10 PDF)

1. **CCD/C-CDA Documents**: Bulk export of HL7 C-CDA XML files complying with USCDI v1 requirements. References HL7 C-CDA R2.1 specifications.

2. **FHIR Bulk Data Access**: FHIR R4 / US Core STU V3.1.1 bulk data export. References the (g)(10) SmartOnFHIR API documentation at `https://documents.maximus.care/`.

3. **Patient Demographics & Insurance** (Excel format): "Comprehensive view of demographics and insurance details." No field-level detail provided — just a one-sentence description.

4. **Appointments** (Excel format): "Comprehensive view of all future appointment details." Again, one sentence, no field-level detail.

5. **Documents**: Signed progress notes, lab results, radiology reports, and any other scanned/uploaded documents (PDF, JPG, PNG formats). Organized by patient chart number folders with category subfolders (Lab Reports, Radiology, Scanned Receipts, etc.).

6. **Single vs. Multi-Patient Export**: The system supports both single-patient and population-level export using the above formats.

### FHIR API Documentation (documents.maximus.care)

The FHIR documentation portal is a (g)(10) SMART on FHIR API reference. It documents:
- OAuth 2.0 authorization flow (authorization code + client credentials for bulk)
- FHIR Base URL: `https://fhir.maximus.care/api`
- Auth server: `https://apiauth.maximus.care/connect/authorize`
- 20 standard US Core STU3.1.1 FHIR resource types
- GET/POST search operations for each resource
- HTTP error codes (200, 400, 401, 403, 404)
- Client registration form
- Terms and conditions

No custom FHIR profiles, no extensions beyond US Core, no bulk export endpoint documentation, no sample data.

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes a **hybrid approach** combining C-CDA, FHIR, and proprietary Excel/file exports. This is actually more thoughtful than many small vendors — they've recognized that not everything fits into C-CDA or FHIR and have added Excel exports for demographics/insurance and raw document files.

**Domains covered (at least mentioned):**
- Demographics and insurance (via Excel export)
- Clinical data covered by USCDI v1 / US Core STU3.1.1 (via C-CDA and FHIR): problems, medications, allergies, labs, vitals, immunizations, procedures, care plans, goals, encounters, devices, diagnostic reports, documents
- Clinical documents: progress notes, lab results, radiology reports, scanned documents (via file export)
- Appointment data (via Excel export — though only "future" appointments, not historical)

**Domains clearly missing or not mentioned:**
- **Billing and financial data**: This is a critical gap. MaxRemind's core business is medical billing/RCM, and Maximus EHR stores claims, billing records, charges, and payment data. The export documentation makes no mention of billing data export whatsoever.
- **Medication administration records**: Only MedicationRequest is documented; no MAR data
- **E-prescribing history**: No mention of prescription transmission records
- **Referral data**: Not mentioned despite being a listed product feature
- **Care coordination / transitions of care documents**: While C-CDA covers some of this, there's no mention of Direct messages or transition records
- **Remote patient monitoring data** (MaxRPM): Not mentioned at all
- **Custom clinical assessments**: No specialty-specific data export described (the product claims 75+ specialties)
- **Patient portal data**: Secure messages, access history — not mentioned
- **Historical appointments**: The Excel export only mentions "future" appointments, omitting visit history

**Ambiguous areas:**
- The "Documents" export (item 6) is described broadly enough that it *might* capture some of the above as scanned/attached documents, but there's no specificity about what document types are included
- The C-CDA export "complying with USCDI v1" doesn't specify exactly which C-CDA sections are populated

### Export Format & Standards

The export uses a reasonable multi-format approach:
- **C-CDA XML** for structured clinical data (USCDI v1)
- **FHIR R4 / US Core 3.1.1** via Bulk Data API for the same clinical data
- **Excel** for demographics/insurance and appointments
- **Native file formats** (PDF, JPG, PNG) for clinical documents

This is appropriate for an ambulatory EHR. The C-CDA and FHIR components cover standard clinical data well. The Excel exports for demographics and appointments are pragmatic. The document file export preserves original formats.

However, there is significant concern about the **C-CDA and FHIR components being essentially the (g)(10) API repackaged as (b)(10) export**. The PDF explicitly references "170.315(g)(10) SmartOnFHIR API Documentation" and the FHIR docs portal only documents standard US Core resources. The only genuinely (b)(10)-specific components are items 4–6 (demographics Excel, appointments Excel, and document files), which cover data *beyond* USCDI but with essentially no documentation about their structure.

### Documentation Quality

**Very poor.** The entire EHI export is described in a 4-page PDF with:
- No data dictionary
- No field-level definitions for any export component
- No schema files (no XSD for C-CDA customizations, no JSON schema, no Excel column headers)
- No sample data or worked examples
- No export procedure instructions (no screenshots, no step-by-step guide)
- One-sentence descriptions for the Excel exports with zero specificity
- No description of how to initiate an export request

The FHIR documentation portal (documents.maximus.care) is somewhat more detailed for the API, with endpoint URLs, auth flows, and resource descriptions, but it's purely (g)(10) documentation — standard US Core with no custom extensions or profiles.

A developer receiving this export would have:
- C-CDA files they could parse with standard tools
- FHIR NDJSON they could parse with standard tools
- Excel files with completely unknown column structure
- A folder of documents with no manifest or metadata schema

### Structure & Completeness

- **Granularity**: Table-name level only. No field definitions anywhere.
- **Coded fields**: Not documented. The C-CDA and FHIR formats inherit standard value sets, but the Excel exports have no value set documentation.
- **Relationships**: Not documented. How does the Excel demographics data relate to the C-CDA patient records? How are documents linked to encounters?
- **Versioning**: Document dated 2023-10-03, no change history. The FHIR docs site was last modified 2024-08-28 per HTTP headers.

## Access Summary
- Final URL (after redirects): https://maxremind.com/maximusehr-certification/
- Status: found
- Required browser: No (PDF is direct link); Yes (for FHIR docs at documents.maximus.care which is a SPA)
- Navigation complexity: one_click (PDF link clearly labeled "ELECTRONIC HEALTH INFORMATION EXPORT")
- Anti-bot issues: none

## Obstacles & Dead Ends
- FHIR API endpoints at `fhir.maximus.care` return 404 — not publicly accessible, so no CapabilityStatement or SMART configuration could be retrieved
- The FHIR docs portal at `documents.maximus.care` requires JavaScript (React SPA), but renders fine in a browser
- No additional EHI export documentation found beyond the single PDF and the (g)(10) FHIR docs portal
