# Health Information Management Systems, LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://axiomehr.com/ehiexport/
- CHPL IDs: 10512
- Product: Axiom Version 7
- Developer: Health Information Management Systems, LLC (HiMS)

## Navigation Journal

**1. Initial probe:**
```bash
curl -sI -L "https://axiomehr.com/ehiexport/" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, `text/html; charset=UTF-8`, served via Cloudflare. No redirects.

**2. Page fetch and examination:**
```bash
curl -sL "https://axiomehr.com/ehiexport/" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
```
The page is a WordPress/Elementor page (298KB of HTML). Much of the content is JS-based lazy loading (WP Rocket). After rendering in browser, the page is extremely simple: a purple hero banner with "EHI Export Instructions" heading, a subheading "Axiom EHI Export Instructions", and a single "Download PDF" button.

**3. PDF download:**
```bash
curl -sL "https://axiomehr.com/wp-content/uploads/2024/05/Axiom-EHI-Export-Instructions.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o Axiom-EHI-Export-Instructions.pdf
```
Result: 4-page PDF (187,728 bytes), confirmed as valid PDF document. Created 2026-01-30 by Khalid Maskari (CEO) using Microsoft Word.

**4. Search for additional documentation:**
Checked the site's XML sitemap (`page-sitemap.xml`) and found two adjacent pages:
- `/apidocs/` — "API Documentation" page with a separate PDF (`apidocumentation.pdf`, 16 pages). This is the (g)(10) FHIR/CCDS Patient Access API documentation, covering standard clinical data categories only (problems, medications, allergies, labs, vitals, procedures, immunizations, etc.). This is **not** the EHI export — it's the Patient Access API.
- `/oncmandatorydisclosure/` — ONC Mandatory Disclosure page confirming certification for (b)(10) among other criteria. Notes that "AxiomEHR, our newest product, is due to be ONC certified in 2026."

No additional EHI export documentation, data dictionaries, schema files, or sample exports were found anywhere on the site.

## What Was Found

The entire EHI export documentation consists of a **single 4-page PDF** titled "170.315 (b)(10) Electronic Health Information Export." Here is what it contains:

**Page 1:** Cover page with HiMS logo, title, company name, product name (Axiom), and version number (7).

**Page 2:** Instructions for single-patient EHI export:
1. Login to Axiom EHR
2. Go to the Report page
3. Enter patient name and parameters (screenshot shows a form with Start Date, End Date, Patient name, and a "Form Types" dropdown listing dynamic forms such as "AccountLog", "Adult ASAM", "Adult ASAM Text", "Adult ACE/Self Report Scale (AIRS)", etc.)
4. Click "BUILD REPORT"
5. Review the results showing patient information and number of records
6. Select data to export (checkbox per document)
7. Select "EHI Export" from the action dropdown menu

**Page 3:** Screenshots showing:
- The export record list with columns: Form Type, Doc Type, File Date (showing items like "Dynamic Form: 13-17 EPIIDT", "Dynamic Form: NIPP Weekly Progress Report", "Encounter: CPT Note")
- The "EHI Export" action dropdown
- A success confirmation message: "The EHI Export for KING, TERRY is generating. We will notify you when the export file is ready"

**Page 4:**
- An "EHI Export History" table showing completed exports with columns: Rec, Patient Name, Patient #, Patient Id, Form Type, Form Date, File Name, Status
- The file appears to be a password-encrypted compressed ZIP (filename example: `1BA97653-8CC0-4C82-A96F-FF42748F15AA.zip`)
- Note that the file is "compressed and encrypted with a password that will be sent to the employee's email as well as the patient's email"
- A brief section on "Patient Population Data Bulk Export": "The request for patient population export will include all population data. The export file(s) will be compressed to reduce file size."

**Notably absent from the documentation:**
- No data dictionary or field definitions
- No description of the export file format (what's inside the ZIP)
- No schema or structural documentation
- No list of what data categories are included
- No sample export files
- No description of how "all population data" is defined for the bulk export
- No mention of export format (CSV? JSON? PDF? Database dump? FHIR?)

## Export Coverage Assessment

### Data Domain Coverage

The documentation provides **no information whatsoever** about what data domains are included in the export. The screenshots suggest the export operates on a per-form basis — the user selects from "Form Types" (dynamic forms and encounter types) and exports selected documents. This is essentially a document-level export, not a structured data export.

Based on the screenshots, the form types visible include behavioral health assessment forms (ASAM, ACE/Self Report Scale, NIPP Weekly Progress Reports, EPIIDT forms) and encounter notes (CPT Notes). The "Form Types" dropdown appears to list all clinical form types configured in the system.

**Critical gaps relative to what Axiom stores (per product research):**

- **Billing/RCM data** — Axiom has full built-in RCM (claims, eligibility, payments, coding). No mention in the export documentation. The form-based export mechanism seems unlikely to capture billing data.
- **Scheduling data** — Appointments, reminders. Not mentioned.
- **Prescribing/medication data** — e-prescribing is a core feature. Not mentioned.
- **Lab orders and results** — Not mentioned.
- **Patient portal data** — Secure messages, patient-initiated requests. Not mentioned.
- **EVV (Electronic Visit Verification) records** — Critical for Medicaid-funded services. Not mentioned.
- **DD/foster care records** — Specialty modules. Not mentioned.
- **CRM/intake tracking data** — Not mentioned.
- **Analytics/reporting data** — Not mentioned.
- **Audit logs** — Not mentioned.

The "select all documents" checkbox and form-based export model suggests the export captures clinical documentation (forms and encounters), but there is no evidence it covers the full scope of electronic health information that Axiom stores. The bulk export section claims it "will include all population data" but provides no definition of what that encompasses.

### Export Format & Standards

The documentation **does not describe the export format at all.** We know:
- The output is a compressed, password-encrypted ZIP file
- The password is emailed to both the employee and the patient
- The ZIP filename is a GUID (e.g., `1BA97653-8CC0-4C82-A96F-FF42748F15AA.zip`)

We do not know:
- What format the files inside the ZIP use (PDF? CSV? JSON? FHIR? Proprietary XML?)
- How structured the data is
- Whether relationships between records are preserved
- Whether coded values are included or just rendered text

The form-based export model (selecting "Dynamic Form: Adult ASAM" etc.) suggests each exported item may be a rendered document (possibly PDF) rather than structured data. This is speculation — the documentation simply doesn't say.

This is **not** a FHIR-based export. The separate API documentation (`/apidocs/`) covers a CCDS/FHIR Patient Access API for (g)(10), but the (b)(10) EHI export is a completely separate mechanism accessed through the Report page in the EHR.

### Documentation Quality

The documentation quality is **very poor.** The 4-page PDF contains:
- A cover page
- ~1 page of step-by-step instructions (with typos: "informaiton", "cllick")
- ~2 pages of screenshots
- A 2-sentence description of bulk export

There are no field definitions, no data dictionary, no format specifications, no schema documentation, no sample files, and no worked examples. A developer could not implement an import of this data based on this documentation because they wouldn't know what format to expect inside the ZIP, what fields are included, or how to interpret the exported data.

The documentation reads as a minimal compliance artifact — enough to demonstrate that an EHI export button exists, but not enough for anyone to actually understand or use the exported data.

### Structure & Completeness

- **Granularity:** Zero field-level documentation. Not even table names or data categories are listed.
- **Value sets:** Not documented.
- **Relationships:** Not documented.
- **Versioning:** The PDF was created 2026-01-30 (3 weeks before this collection). No change history.

## Access Summary
- Final URL (after redirects): https://axiomehr.com/ehiexport/
- Status: found
- Required browser: no (PDF link extractable from HTML source, but page renders via JS/Elementor)
- Navigation complexity: direct_link (one click from page to PDF)
- Anti-bot issues: none (Cloudflare CDN present but no blocking)

## Obstacles & Dead Ends
- The web page (298KB HTML) is heavily loaded with WordPress/Elementor JS, but the actual content is trivial — just a heading and a download link. No hidden content in collapsed sections.
- The API documentation PDF at `/apidocs/` is for the (g)(10) FHIR/CCDS API, not the (b)(10) EHI export. It covers only standard clinical data categories (problems, medications, allergies, labs, vitals, procedures, care team, immunizations, implantable devices, assessments, plans of treatment, goals, health concerns).
- No additional EHI export documentation exists elsewhere on the site based on a full sitemap review.
