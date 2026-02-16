# ezEMRx Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.ezemrx.com/ehi-export
- CHPL IDs: 10779
- CHPL Product Number: 15.02.05.2886.EZEM.01.01.1.220105
- Certification date: 2022-01-05

## Navigation Journal

### 1. Initial probe
```bash
curl -sI -L "https://www.ezemrx.com/ehi-export" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, `Content-Type: text/html; charset=UTF-8`. Server is `Pepyaka` (Wix CDN). The site is hosted on Wix and renders entirely client-side via JavaScript.

### 2. Page fetch and examination
```bash
curl -sL "https://www.ezemrx.com/ehi-export" -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
```
The raw HTML is 673KB of Wix framework JavaScript. No meaningful text content is available without browser rendering. Searched for downloadable file links (PDF, ZIP, XLSX, CSV, JSON, DOC):
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/page.html
```
**No downloadable files found.** The only relevant link is to `https://www.healthit.gov/test-method/electronic-health-information-export` (the ONC test method reference page, an external standard — not vendor documentation).

### 3. Browser rendering
Opened the page in Chrome. The page renders three visible sections:

1. **Header section** — "EHI Export Specifications" with a stock image ("Server Room") and a paragraph defining EHI by quoting 45 CFR 160.103 / 164.501, with a "Reference" link to healthit.gov.

2. **Dark section** — "§170.315(b)(10) Electronic Health Information Export Certification" listing bullet-point compliance claims for single-patient and patient-population exports. These are requirements paraphrased from the ONC regulation, not descriptions of the actual export format.

3. **Bottom section** — A paragraph stating: "The documentation listed on this page is intended to provide the user an understanding of the resulting files from the EHI Export. It will explain how to read the files, understand the meaning behind fields, and offer other insight to properly make use of this extensive amount of information."

### 4. Empty PDF Viewer Pro widget — the critical finding
Between sections 2 and 3, there is a **large blank area** approximately 1109 pixels tall. Investigation via JavaScript DOM inspection revealed:
- An `<iframe>` element with `title="PDF Viewer Pro"` — a Wix third-party app widget (component ID `comp-lpim12rl`, type `TPAWidget`).
- The iframe has **no `src` attribute** — it is completely empty.
- No PDF URL is configured in any of the Wix page data payloads (checked `wix-warmup-data`, `wix-viewer-model`, `thunderbolt-features`, and `thunderbolt-platform` JSON responses).
- No PDF download requests appear in the network waterfall.
- No console errors indicate a failed PDF load — the widget simply has no document assigned.

**Conclusion: The page has a placeholder PDF viewer widget where export documentation (presumably a data dictionary or format specification) was intended to be embedded, but no PDF was ever uploaded to it.**

The bottom paragraph ("The documentation listed on this page is intended to provide the user an understanding of the resulting files...") appears to be introductory text for a document that was never published.

### 5. Navigation menu exploration
Expanded the "Health IT" navigation dropdown. Subpages are:
- Public Health (marketing)
- Private Practice (marketing)
- Revenue Services (marketing)

None contain EHI export documentation.

### 6. Footer links exploration
Checked "Usability & Specifications" page (`/specifications`) — contains hardware/software requirements, not export docs.
Checked "ONC Mandatory Cost Disclosure & Compliance" page (`/mu-compliance`) — contains general certification compliance text, no export documentation.

### 7. External searches
- **Wayback Machine CDX API**: Only two captures exist (`2024-10-12` and `2025-02-17`), both returning the same Wix HTML shell (client-side rendering means Wayback can't capture actual content).
- **Web search** for `ezEMRx "EHI export" data dictionary`: No results specific to ezEMRx.
- **Web search** for `"ezemrx" "data dictionary" OR "export format" filetype:pdf`: No results.
- **CDP partner site** (`cdpehs.com/solutions-and-services/electronic-health-records`): No EHI export documentation found.
- **Wayback Machine PDF search** across all of `ezemrx.com`: No PDF files archived.

## What Was Found

The page at `https://www.ezemrx.com/ehi-export` exists and loads successfully but contains **no substantive EHI export documentation**. Specifically:

- **No data dictionary** — no table definitions, field listings, schemas, or database structure documentation.
- **No export format specification** — no description of file formats, encoding, structure, or output.
- **No sample data or examples** — no example export files or sample records.
- **No schema files** — no XSD, JSON Schema, OpenAPI specs, DDL, or other machine-readable artifacts.
- **No export instructions** — no user guide for performing the export.
- **No API documentation** — no endpoint specifications.

What IS present is:
1. A regulatory definition of EHI (quoting 45 CFR)
2. A list of (b)(10) requirements paraphrased from the ONC rule
3. An empty PDF Viewer Pro widget — a placeholder for documentation that was never published
4. Introductory text that promises documentation about "resulting files from the EHI Export" that does not exist on the page

## Export Coverage Assessment

### Data Domain Coverage

**Cannot be assessed.** The page provides no information whatsoever about what data the export includes. There is no data dictionary, no table listing, no field inventory, and no description of export contents. Based on the product research, ezEMRx stores extensive data across clinical, administrative, billing, inventory, and public health domains — but the export documentation does not address any of these.

The page text mentions the export must "include all EHI" and be in "a computable format," but these are regulatory requirements being parroted back, not descriptions of actual implementation. There is no evidence on this page of what data domains are actually exported, what format is used, or how complete the export is.

### Export Format & Standards

**Unknown.** The documentation page does not specify:
- What format the export uses (FHIR, C-CDA, CSV, SQL dump, PDF, etc.)
- Whether it is a standardized or proprietary format
- How the data is structured or organized
- How relationships between data entities are expressed

The introductory text promises to "explain how to read the files, understand the meaning behind fields" — suggesting there IS an export with files and fields — but this documentation was never published.

### Documentation Quality

**Effectively nonexistent.** The page functions as a compliance checkbox — it exists at a registered URL, contains regulatory language, but provides no technical content. A developer receiving an export from ezEMRx would have no public documentation to help them interpret the data.

The presence of the empty PDF Viewer Pro widget suggests the vendor intended to publish a document (likely a PDF data dictionary or format guide) but never completed this step. This is not a case of missing a link — the widget placeholder was placed on the page, text introducing the documentation was written, but the actual document was never created or uploaded.

### Structure & Completeness

**No documentation structure to assess.** There are:
- No table or entity definitions
- No field-level documentation
- No data types, value sets, or constraints
- No relationship documentation
- No versioning or change history
- No worked examples

### (b)(10) vs (g)(10) Assessment

Notably, the page does NOT attempt to pass off FHIR/g(10) documentation as b(10) export documentation — which is a common pattern among other vendors. The page simply has no technical documentation at all. This means we cannot assess whether the actual export (which presumably exists in the product, given it was certified) covers all EHI or just a USCDI subset.

### Overall Assessment

This is one of the weakest EHI export documentation pages encountered. The vendor has:
1. Created a page at the registered URL ✓
2. Written regulatory language about what EHI means ✓
3. Listed the b(10) requirements they're supposed to meet ✓
4. Placed a PDF viewer widget to display documentation ✓
5. Written introductory text for the documentation ✓
6. **Actually published the documentation** ✗

The page is a shell — structurally ready for documentation that was never delivered. Given that ezEMRx was certified in January 2022 (over 4 years ago), this is not a case of recent certification with pending documentation. The empty state appears to be long-standing.

For a product serving over 1,000 public health locations (via the CDP partnership), the absence of any public EHI export documentation is a significant compliance gap. Users and third parties have no way to understand the export format without contacting the vendor directly.

## Access Summary
- Final URL (after redirects): https://www.ezemrx.com/ehi-export
- Status: found (page loads, but documentation content is missing)
- Required browser: yes (Wix SPA, client-side rendering)
- Navigation complexity: direct_link
- Anti-bot issues: none (standard Wix site)

## Obstacles & Dead Ends
- **Wix client-side rendering**: Raw HTML fetch returns only JavaScript framework; browser required for content extraction.
- **Wayback Machine**: Cannot capture Wix SPA content — archived pages are the same JS shell.
- **Empty PDF viewer**: The Wix PDF Viewer Pro widget (`comp-lpim12rl`) on the page has no PDF configured — the `src` attribute is empty, no PDF URL exists in any Wix page data JSON, and no PDF-related network requests are made.
- **No alternative documentation locations**: Checked CDP partner site, Wayback Machine, web searches — no EHI export documentation exists for ezEMRx anywhere publicly accessible.
- **No downloadable files**: No PDFs, ZIPs, CSVs, JSONs, or any other downloadable files are linked from or embedded in the page.
