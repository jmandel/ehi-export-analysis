# Vohra Wound Physicians Management, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://emr.vohrawoundteam.com/CompleteExport.html
- CHPL IDs: 9887
- Developer: Vohra Wound Physicians Management, LLC
- Product: VHS Medical Documentation & Coding v3.5
- Certification date: 2018-12-21

## Navigation Journal

**Step 1: Probe the registered URL**
```bash
curl -sI -L "https://emr.vohrawoundteam.com/CompleteExport.html" -H 'User-Agent: Mozilla/5.0'
```
Returns HTTP 200, Content-Type: text/html, 3772 bytes. The page is a redirect notice — the `emr.vohrawoundteam.com` domain now serves a static page informing visitors that the Facility Portal has moved to `facilityportal.vohrawoundteam.com`. JavaScript on the page constructs the new URL by appending the current path to the new domain.

**Step 2: Follow the redirect to the actual content**
```bash
curl -sL "https://facilityportal.vohrawoundteam.com/CompleteExport.html" -H 'User-Agent: Mozilla/5.0' -o downloads/CompleteExport.html
```
Returns HTTP 200, 11,592 bytes. This is the actual EHI export documentation page — a self-contained static HTML file titled "Export data format and location."

**Step 3: Screenshot the page**
Navigated to `https://facilityportal.vohrawoundteam.com/CompleteExport.html` in Chrome, took a full-page screenshot. The page renders cleanly as a single-scroll document with Vohra branding.

**Step 4: Search for additional documentation**
- Probed 20+ paths on `facilityportal.vohrawoundteam.com` (e.g., `/ehi`, `/export`, `/data-dictionary`, `/DataDictionary.html`, `/schema`, `/api`, `/docs`). All non-existent paths redirect to `/Error.cshtml` (302).
- Probed paths on `emr.vohrawoundteam.com`. All paths return the same 3,772-byte redirect page (200 status, same content regardless of path).
- Checked `facilityportal.vohrawoundteam.com/certificationdetails.html` — exists (5,780 bytes) but contains only the 2014 Edition certification listing (v3.4), with no EHI export information.
- The admin portal linked in the export docs (`https://med.vohrawoundteam.com/LogIn.aspx`) resolves to NXDOMAIN — the subdomain no longer exists in DNS.
- No `robots.txt` or `sitemap.xml` found on either domain.
- No Wayback Machine captures found for either domain's CompleteExport.html page.

**Step 5: Confirm no downloadable files**
The CompleteExport.html page contains no links to downloadable files (PDF, ZIP, CSV, schema files, etc.). The only outbound link is to the dead admin portal login page.

## What Was Found

The entire EHI export documentation consists of a single static HTML page describing the export format and procedure. Here is the complete substantive content:

### Export Location
Bulk-exported records are generated to a server-side directory:
- **Server:** IIS-PROD-02
- **Directory:** `C:\inetpub\webapp\ExportedPatientData`

### Export Format
The export produces two types of files per patient:

1. **PDF files** — Encounter notes
   - Filename template: `PATIENT_IDENTIFIER.pdf` (GUID-based)
   - Example: `GGGGGGGG-GGGG-GGGG-GGGG-GGGGGGGGGGGG.pdf`
   - One PDF per patient containing their encounter notes

2. **XML files** — C-CDA standard documents
   - Filename template: `ENCOUNTER_IDENTIFIER.xml` (GUID-based)
   - Example: `HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH.xml`
   - One XML per encounter conforming to the C-CDA standard

### Export Procedure (Single Patient)
1. Navigate to the administrative portal (link dead: `https://med.vohrawoundteam.com/LogIn.aspx`)
2. Authenticate as a user with export permissions
3. Select menu: Advanced > Data Portability
4. Set "Export Option" to **Patient**
5. Enter patient's First Name, Last Name, and Date of Birth
6. Press "Export Patients" button
7. See confirmation: "Successfully exported 1 patient records"
8. Login to the server and retrieve files from `C:\inetpub\webapp\ExportedPatientData`

### What Is NOT Documented
- No data dictionary (no table/field definitions whatsoever)
- No schema files (no XSD, JSON Schema, or C-CDA template OIDs)
- No specification of which C-CDA document type is used (CCD, referral summary, etc.)
- No specification of what sections or data elements the C-CDA includes
- No specification of what the PDF encounter notes contain
- No sample data or example export files
- No API documentation
- No bulk export procedure (only single-patient export described)
- No mention of how to request or access a bulk export of all patients
- No field-level documentation of any kind
- No value sets, coding systems, or terminology references
- No versioning or change history

## Export Coverage Assessment

### Data Domain Coverage

This is a specialty wound care EMR that stores extensive clinical, billing, and specialty-specific data. Based on the product research, the system contains:

**Clearly NOT covered or ambiguous (no documentation to confirm):**
- **Wound assessments** (etiology, staging, measurements, treatment plans) — the core specialty data of the product. No mention of how this appears in the export.
- **Wound photographs/images** — likely stored in the system but no mention of export.
- **Billing/coding data** — the product name literally includes "Coding" and assists with billing documentation. No mention of billing data in the export.
- **MDS-compliant documentation** — critical for SNF Medicare reimbursement. Not mentioned.
- **Procedure documentation** (debridement, Doppler studies, skin substitutes, negative pressure therapy) — not mentioned.
- **Clinical decision support data** — not mentioned.
- **Outcomes/analytics data** (healing timelines, re-hospitalization rates) — not mentioned.
- **Integration data** (PointClickCare, MatrixCare records) — not mentioned.
- **Patient portal content** — not mentioned.
- **Allergies** — not mentioned (though likely in C-CDA if standard sections are used).

**Potentially partially covered via C-CDA:**
- Demographics, vital signs, problem lists, medications, immunizations — these would be included IF the C-CDA export uses standard sections. But without documentation of which C-CDA template or sections are generated, this is speculative.

**Potentially partially covered via PDF encounter notes:**
- Clinical notes content — the PDF files are described as "encounter notes," which would capture the narrative clinical documentation. However, PDFs are not computable data — they represent rendered documents, not structured data.

The fundamental problem is that the documentation doesn't tell you what data is actually exported. The C-CDA XML files could contain comprehensive clinical data or just a minimal patient summary — there is no way to know from the documentation alone.

### Export Format & Standards

The export uses two formats:
1. **C-CDA XML** — a recognized healthcare interoperability standard. However, C-CDA is a clinical document standard designed for care transitions, not bulk data export. It excels at clinical summaries but is not well-suited for specialty wound care data (wound measurements, staging, photograph references, dressing orders) or billing data.
2. **PDF** — rendered encounter notes. While useful for human review, PDFs are not computable and represent a significant downgrade from structured data. A third party cannot import, query, or transform PDF content without OCR/NLP.

**The (b)(10) vs (g)(10) concern:** This export appears to be a C-CDA-based clinical summary export rather than a true bulk export of all electronic health information. C-CDA is appropriate for the (b)(1) transitions of care criterion and the (g)(10) patient access API, but for (b)(10) it likely covers only the standard clinical domains (problems, medications, allergies, vitals, etc.) and misses the specialty wound care data, billing data, and other non-standard domains that constitute the bulk of this product's data.

A wound care EMR's most valuable data — wound assessments with measurements, staging, healing trajectories, procedure details, dressing protocols, photograph metadata — does not map naturally to standard C-CDA sections. The export documentation gives no indication that custom C-CDA sections or extensions are used to capture this data.

### Documentation Quality

The documentation is among the most minimal possible while still technically existing:
- **No data dictionary** — zero field-level documentation
- **No schema** — no machine-readable artifact of any kind
- **No examples** — no sample files to understand what the export produces
- **No C-CDA template specification** — impossible to know what data elements are included
- **Dead administrative portal link** — the only link in the documentation points to a non-existent subdomain
- **Server-side file retrieval** — the export requires logging into the production server to retrieve files, which is an unusual and operationally challenging delivery mechanism
- **Single-patient only** — only a single-patient export procedure is documented, with no mention of bulk export

A developer could not implement an import of this data based solely on this documentation. They would need to obtain actual export files and reverse-engineer the C-CDA structure and PDF content.

### Structure & Completeness

- **Granularity:** File-type level only (PDF and XML). No table, section, field, or element documentation.
- **Coded fields:** Not documented.
- **Relationships:** Not documented (the relationship between patient-level PDFs and encounter-level XMLs is implied by naming convention but not formally specified).
- **Value sets:** Not documented.
- **Versioning:** None. The page was last modified 2023-12-14 (per HTTP headers on facilityportal version) / 2024-10-08 (per emr redirect version).

This documentation reads as a minimal compliance checkbox — the bare minimum to have a URL registered with CHPL. It does not provide the information needed to understand, validate, or utilize the EHI export.

## Access Summary
- Registered URL: https://emr.vohrawoundteam.com/CompleteExport.html
- Final URL (after following JS redirect): https://facilityportal.vohrawoundteam.com/CompleteExport.html
- Status: found
- Required browser: no (static HTML, works with curl; browser needed only for screenshot)
- Navigation complexity: one_click (JS redirect from emr to facilityportal domain)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The registered URL (`emr.vohrawoundteam.com/CompleteExport.html`) is a redirect notice page, not the actual documentation. The JS-based redirect constructs the real URL at `facilityportal.vohrawoundteam.com/CompleteExport.html`.
- The admin portal link in the export documentation (`https://med.vohrawoundteam.com/LogIn.aspx`) resolves to NXDOMAIN — the subdomain no longer exists.
- No Wayback Machine captures found for any version of the page.
- The certification details page (`certificationdetails.html`) exists but covers only the older 2014 Edition certification, with no EHI export information.
- No additional documentation files (PDF, schema, data dictionary) were found anywhere on either domain.
