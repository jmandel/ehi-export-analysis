# Office Ally, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://cms.officeally.com/onc-acb-certification
- Final URL (after redirect): https://cms.officeally.com/resources/onc-acb-certification
- CHPL ID: 11572
- Product: EHR 24/7, version 5.9.255
- Certification date: 2024-12-26

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://cms.officeally.com/onc-acb-certification"` returned a 301 redirect to `/resources/onc-acb-certification`, then 200 OK with `Content-Type: text/html`. Served via Cloudflare.

2. **Page fetch** — `curl -sL "https://cms.officeally.com/onc-acb-certification" -o /tmp/oa-page.html` returned 123KB of HTML. The page is a Webflow-hosted compliance/certification page titled "Office Ally's Certified EHR (Electronic Health Records)".

3. **Page structure** — The page has:
   - A Drummond Certified seal with buttons for "Cost and Considerations", "Find your CMS Certification ID", and "Certificate of Compliance"
   - A table showing CMS Certification ID `2025CUD8GVA660Z`, live date 12/26/2024, EHR Version 5.9.255, FHIR 4-B, etc.
   - "21st Century CURES Act Certification Real World Test Documents" section with RWT plans/results for 2022-2025
   - **"Electronic Health Information Export"** section with a single bullet link: "170.315 (b)(10) EHI Export Documentation"

4. **Downloaded the EHI Export PDF** —
   ```
   curl -sL "https://cdn.prod.website-files.com/6830ce6e8206ddade0c99cae/68b897ca686e527d9b1d1250_20240208%20EHI%20Export%20Documentation.pdf" -o downloads/EHI_Export_Documentation.pdf
   ```
   Confirmed: PDF document, 1 page, 97KB. Author: Mark Vomocil. Created: 2024-02-08 via Microsoft Word.

5. **Checked for additional artifacts** — Searched all links on the page. The only EHI-relevant file is the single PDF. The "Costs and Considerations" PDF is a general pricing/feature disclosure document and does not contain EHI export details. No data dictionary, schema files, API documentation, or sample data files were found on the page.

6. **Checked PDF for embedded links/attachments** — `pdfdetach -list` reports 0 embedded files. The PDF text contains links to the HL7 USCDI and C-CDA specifications (external standards, not vendor-specific documentation).

7. **Browser screenshot** — Navigated to the page in Chrome and took a full-page screenshot confirming the page structure described above.

## What Was Found

The entire EHI export documentation consists of a **single one-page PDF** (dated February 8, 2024, version 1.0.1). It describes four export components:

1. **CCDA** — Bulk export of HL7 C-CDA XML files complying with USCDI Version 1. Links to the HL7 C-CDA specification for format details. No vendor-specific profile documentation, no field mapping, no sample files.

2. **Appointments** — CSV export with "a comprehensive view of appointment details." No field list, no schema, no sample.

3. **Claims** — CSV export with "a comprehensive view of claim details." No field list, no schema, no sample.

4. **Attachments** — Scanned/uploaded documents exported in their original upload format.

The documentation states the export supports both single-patient and patient-population export. The product version listed in the PDF is 5.6.81 (older than the current certified version 5.9.255).

There is **no data dictionary** — no table names, no field names, no data types, no value sets, no schema files, no API documentation, no sample data, and no export instructions beyond the four bullet points above.

## Export Coverage Assessment

### Data Domain Coverage

The export documentation claims four export streams. Here is how they map against the data domains identified in the product research:

**Covered (at least nominally):**
- Clinical data via C-CDA: demographics, medications, allergies, problems, vital signs, immunizations, lab results, clinical notes, procedures, care plans — to the extent they fit in USCDI v1 / C-CDA
- Appointments: CSV export mentioned
- Claims: CSV export mentioned
- Attachments: scanned/uploaded documents in original format

**Likely missing or ambiguous — not mentioned anywhere in the documentation:**
- Medication administration records and prescription history beyond what C-CDA captures
- Referral orders and radiology orders (may partially appear in C-CDA but not guaranteed)
- Family health history (certified under (a)(12) but not mentioned in export)
- Implantable device list (certified under (a)(14) but not mentioned in export)
- Patient billing records: invoices, copays, balances, payments, patient ledger entries — the "Claims" CSV likely covers payer claims but not patient-facing billing
- Insurance/enrollment information
- Superbills and charge capture detail
- Patient portal messages and secure messages
- Patient intake form submissions
- E-prescribing history and controlled substance prescribing records

**The (b)(10) vs (g)(10) concern:**
The C-CDA component is essentially a USCDI v1 clinical summary export — this is the same data that would be available through their (g)(10) FHIR API, just in C-CDA format instead. The Appointments and Claims CSVs represent a genuine attempt to go beyond the USCDI clinical data set, but without field-level documentation it's impossible to assess how comprehensive they are. The export does not describe how it handles data that doesn't fit into C-CDA or the two CSV files — for example, custom clinical templates, SOAP note free text, blood sugar logs, or clinical decision support data.

### Export Format & Standards

- **C-CDA XML** — a recognized standard, but limited to what USCDI v1 defines. The documentation references USCDI v1 (not v3/v4), which is notably behind the current standard.
- **CSV** — for appointments and claims. No schema or field definitions provided. Without column headers, data types, or value set documentation, a third party cannot reliably interpret these files.
- **Native format** — for attachments (scanned documents exported as-is).

The combination of C-CDA + CSV + attachments is a reasonable multi-format approach, but the complete absence of field-level documentation for the CSV components makes them practically opaque to any recipient.

### Documentation Quality

This is among the most minimal EHI export documentation possible. The entire documentation is a single page with four bullet points. There are:

- **No field-level definitions** for any export component
- **No data dictionary** of any kind
- **No CSV column headers** or schema documentation
- **No C-CDA template constraints** or customizations beyond referencing the standard
- **No sample export files** or worked examples
- **No export instructions** (how does a user trigger the export? Where do they find it in the UI?)
- **No API documentation** for programmatic access
- **No relationship documentation** between the export components
- **No versioning alignment** — the PDF references product version 5.6.81 while the current certified version is 5.9.255

A developer receiving this export would have C-CDA files they could parse with standard tooling, but the CSV files would require reverse-engineering from column headers in the actual export files. The documentation provides no basis for building an import system.

### Structure & Completeness

- **Granularity**: Export type names only. No table names, no field names, no data types.
- **Coded fields**: Not documented.
- **Relationships**: Not documented.
- **Value sets**: Not documented.
- **Versioning**: The PDF has a two-entry version history (v1.0.0 Nov 2023, v1.0.1 Jan 2024). No updates since then despite the product being re-certified in Dec 2024.

### Overall Assessment

Office Ally's EHI export documentation is a compliance checkbox — a single page that acknowledges the existence of an export mechanism without providing the technical detail needed to understand, validate, or use it. The inclusion of Appointments and Claims CSVs alongside C-CDA shows awareness that EHI extends beyond clinical summaries, but the total absence of field-level documentation for these components undermines their utility. The C-CDA component, while referencing a recognized standard, is limited to USCDI v1 and does not address how data outside that scope is handled. Significant data domains stored by EHR 24/7 — patient billing, secure messages, custom templates, specialty-specific clinical data, e-prescribing records — have no documented export path.

## Access Summary
- Final URL (after redirects): https://cms.officeally.com/resources/onc-acb-certification
- Status: found
- Required browser: no (curl works fine, browser used for screenshot only)
- Navigation complexity: direct_link (one redirect, then a single bullet link to the PDF)
- Anti-bot issues: none (Cloudflare present but not blocking)

## Obstacles & Dead Ends
- None. The page loaded cleanly via curl and browser. The PDF downloaded without issues.
- The only limitation is the extreme brevity of the documentation itself.
