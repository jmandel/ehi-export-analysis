# Patient First — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.patientfirst.com/mandatory-disclosure-for-ehr
- CHPL IDs: 11065
- Product: PAS Version 2015.0.0.1
- Certification Date: Dec 12, 2022

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://www.patientfirst.com/mandatory-disclosure-for-ehr" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200, Content-Type `text/html; charset=UTF-8`. The site runs on WordPress (wpcloud hosting). The response headers exposed a WordPress JSON API endpoint: `https://www.patientfirst.com/wp-json/wp/v2/pages/109967`.

2. **Page fetch**: Downloaded the full HTML page (530 KB). It's a single WordPress page containing all mandatory disclosures — certification details, Real World Testing links, criteria tracker tables, measurement options, the EHI Export section, and SED usability reports.

3. **Structured data**: Fetched the WordPress REST API JSON for the page (`/wp-json/wp/v2/pages/109967`), which contains the rendered HTML content in a cleaner format (26 KB). This is more useful than the full HTML page for machine processing.

4. **EHI Export section**: Found under the heading "Electronic Health Information (EHI) Export" (h3 level), approximately 2/3 down the page. No accordion or hidden content — it's inline HTML with a descriptive paragraph and a table describing the export format. No download links, PDFs, data dictionaries, or schema files are provided — the entire EHI export documentation consists of this brief HTML section.

5. **RWT results**: Downloaded the CY 2025 Real World Testing Results PDF (23 pages, dated Feb 2, 2026). RWT Measure #3 covers b(10) — "Number of EHI Exports Run." The metric is labeled "Number of C-CDA Batch Exports Sent" which is revealing (see analysis below). Results show 31 exports in Q1 2025 (20 VA, 6 MD, 5 PA, 0 NJ).

6. **No additional links**: There are no links to a data dictionary, schema files, sample exports, API documentation, or any other EHI-specific documentation beyond the inline HTML table. The page also links to RWT plans/results PDFs and SED usability reports, none of which contain additional export format details.

## What Was Found

The EHI export documentation is a single paragraph plus a 7-row table embedded directly in the mandatory disclosures WordPress page. There are no downloadable documents, schemas, or data dictionaries specific to the EHI export.

### Export Format Description

The export is described as a **compressed (ZIP) archive** containing files organized into folders by category. The documentation states: "EHI Export functionality allows health systems to do a manual one-time export of health data. The export contains the electronic health information available in a patient's record in a computable file format. Some electronic health information might not be available in a computable format, such as PDF documents or images."

The ZIP contains 7 categories:

| Category | Description | Folder | Format |
|---|---|---|---|
| Medical Records | C-CDA clinical records | CCDA | XML (C-CDA) |
| X-Rays | X-Ray images | Xray | DCM (DICOM) |
| Scanned Images | Insurance cards, photo ID, etc. | Scan (subfolders per type, e.g. InsCard, PhotoID) | JPG, PNG |
| Consults | Documents from referrals | ConsultNotes | PDF |
| Messages | Secure messages to/from patient | DirectSecureMessages | EML |
| Forms | Various forms (e.g., drug screen results) | Forms | PDF |
| Financials | Billing and claim information | BillingClaim | JSON |

### RWT b(10) Findings

The CY 2025 RWT results reveal a notable detail: the b(10) testing metric is labeled **"Number of C-CDA Batch Exports Sent"** even though it's associated with criterion 315(b)(10). This wording conflates the EHI export (which per the disclosure page is a multi-format ZIP with 7 categories) with C-CDA batch exports. It's unclear whether this metric is tracking the full ZIP export or just C-CDA generation. The analysis section simply states: "While not every site uses the EHI export functionality, we do have some which do, and it worked as certified."

Volume: 31 exports in Q1 2025 (annualized ~124/year across ~79 clinics).

## Export Coverage Assessment

### Data Domain Coverage

Patient First's EHI export is **notably comprehensive for an urgent care EHR**, covering domains that go well beyond the typical USCDI/C-CDA clinical subset:

**Clearly covered:**
- Clinical records (problems, medications, allergies, vitals, procedures, lab results, immunizations, etc.) — via C-CDA
- Diagnostic imaging (x-rays) — via DICOM files, which is excellent for an urgent care chain where on-site x-ray is standard
- Scanned documents (insurance cards, photo IDs) — via images
- Referral/consult documents — via PDF
- Secure patient-provider messages — via EML files
- Miscellaneous clinical forms (drug screen results specifically mentioned) — via PDF
- Billing and claims — via JSON, a computable format

**Potentially missing or unclear:**
- **Demographics, registration, and insurance detail data** — the C-CDA includes some demographics, but administrative registration data (visit history, registration details, insurance plan details beyond scanned cards) is not explicitly mentioned as a separate export category
- **Occupational health data** — Patient First does DOT physicals, workers' comp, drug testing, and employer portal data. Drug screen results are mentioned under "Forms" as PDFs, but structured occupational health data (DOT exam results, workers' comp case details, employer billing) is not clearly documented
- **Prescriptions/e-prescribing records** — ~1.9 million prescriptions/year flow through PAS. C-CDA includes medication lists, but the actual prescription transaction records (Surescripts messages, medication dispensing records from on-site dispensing) may not be fully captured
- **Telehealth encounter data** — Patient First offers telehealth; it's unclear if telehealth-specific data (video visit records, consent) is captured in the C-CDA or at all
- **Lab orders and discrete results** — C-CDA includes lab results, but the structured order data and full discrete result values from the on-site CLIA labs may lose granularity in C-CDA translation
- **Patient portal activity** — portal message content is covered via EML, but portal account data, login history, and download requests are administrative data (not EHI)

**What's commendable:**
The export goes beyond what many vendors offer. Including DICOM images, scanned documents, secure messages, billing data in JSON, and miscellaneous forms is a genuine attempt at comprehensive EHI coverage. The use of native formats (DICOM for x-rays, EML for messages, JSON for billing) rather than forcing everything through C-CDA shows practical thinking.

### Export Format & Standards

The export uses a **multi-format approach**, which is well-suited for a b(10) export:

- **C-CDA XML** for structured clinical data — an industry standard, appropriate for clinical records
- **DICOM** for x-rays — the native medical imaging standard, excellent choice
- **EML** for messages — standard email format, preserves original content
- **JSON** for financials — computable and parseable, though no schema or data dictionary is provided
- **PDF/JPG/PNG** for documents and images — necessary for non-structured content

This is **not a FHIR-based export** and is **not a repackaged g(10) API** — it's a genuinely different system designed for bulk patient data export. The multi-format ZIP approach is practical and covers more data types than a FHIR-only export would.

**Critical gap**: The financial JSON format is undocumented. There is no schema, no data dictionary, no sample file, and no field definitions for the billing/claims JSON. A third party receiving this export would have no way to interpret the financial data without reverse-engineering the JSON structure. Similarly, there are no C-CDA implementation notes or custom extensions documented — it's just described as "industry-standard C-CDA format" with no version, template, or profile specification.

### Documentation Quality

The documentation is **minimal**. The entire EHI export documentation is a single paragraph and a 7-row HTML table on the mandatory disclosures page. There is:

- **No data dictionary** — no field definitions for any export category
- **No schema files** — no JSON Schema for the billing data, no C-CDA template specification, no DICOM metadata description
- **No sample exports** — no example ZIP, no sample C-CDA, no sample billing JSON
- **No user guide** — no instructions for requesting or performing an export
- **No API documentation** — the export appears to be a manual process ("manual one-time export")
- **No versioning or change history** — no indication of when the format was established or updated

A developer receiving this export would know the folder structure and file formats, but would have no documentation to interpret the content. The C-CDA is at least a standard format with external specifications, and DICOM is self-describing. But the billing JSON, EML message structure, and the specific C-CDA sections/templates used are completely undocumented.

### Structure & Completeness

Documentation granularity: **category-level only**. The table describes 7 top-level categories with folder names and file formats. There is no field-level documentation, no entity relationships, no value set definitions, no cardinality constraints.

For a proprietary, internally-developed EHR used exclusively in ~79 clinics by the same organization that built it, this level of documentation may suffice for internal use (they know their own data). But it falls short of what would be needed for external portability — which is the purpose of b(10).

## Access Summary
- Final URL (after redirects): https://www.patientfirst.com/mandatory-disclosure-for-ehr
- Status: found
- Required browser: no (all content available via curl)
- Navigation complexity: direct_link (EHI section is inline HTML, no accordion or navigation needed)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The page loaded cleanly, all content was inline HTML, and the WordPress JSON API provided a clean structured version. No files were behind authentication, no Cloudflare challenges, no JavaScript rendering required.

The only notable finding is the absence of downloadable documentation — the EHI export section contains no links to PDFs, schemas, data dictionaries, or any other artifacts. The documentation *is* the HTML table on the page.
