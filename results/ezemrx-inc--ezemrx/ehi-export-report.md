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

### 4. PDF Viewer Pro widget — embedded data dictionary
Between sections 2 and 3, there is a **Wix PDF Viewer Pro widget** (component ID `comp-lpim12rl`, type `TPAWidget`). The widget loads a PDF via a Firebase cloud function (`us-central1-wix-pdf.cloudfunctions.net/getPdfUrl`) which returns a signed Google Cloud Storage URL:
- `storage.googleapis.com/wix-pdf.appspot.com/8fb6d68d-98e9-4813-9688-18e764071753/comp-lpim12rl.pdf`
- The PDF is 189 KB, 9 pages, titled "170.315(b)(10) Electronic Health Information (EHI) Export"
- Document Control ID: 01US03P98C001, Version 2.0, dated April 25, 2024

**Note:** This widget requires full browser rendering — the iframe `src` is populated dynamically by the Wix TPA framework after page load. A previous collection attempt using DOM inspection found an empty iframe, but the PDF loads correctly when the page is fully rendered and the widget's Firebase integration completes. The PDF is not discoverable via curl or static HTML analysis.

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

The page at `https://www.ezemrx.com/ehi-export` contains a 9-page EHI Export data dictionary PDF (Document Control: 01US03P98C001, v2.0, April 25, 2024) embedded in a Wix PDF Viewer Pro widget. The PDF is the vendor's primary and only b(10) export documentation.

The document describes the EHI export as producing one or more ZIP files containing per-patient data in four categories:

1. **Patient Demographics and Clinical Data** — HL7 C-CDA R2.1 format, always an XML+HTML pair. No TYPE indicator in filename.
2. **Patient Billing and Claims Data** — CSV format, TYPE=`ClaimData`. 17 columns defined: PID, DOS, Payor, Provider, CPT, ICD, NDC, Modifier, Charge, plus payment columns for primary/secondary/tertiary/other/patient, patient responsibility, write-offs/adjustments, and balance.
3. **Adhoc Patient Notes** — CSV format, TYPE=`patNotes`. 7 columns: PID, Patient Notes ID, User Name, Subject, Category, Date, Notes.
4. **Scanned Records** — HL7 C-CDA R2.1 XML with Base64-encoded scanned documents, TYPE=`Echart`.

File naming convention: `PID_INTERNALNUMBERING[_TYPE].EXT` where PID is patient ID, INTERNALNUMBERING is an internal control number, TYPE indicates content category, and EXT is XML, HTML, or CSV.

The PDF also states: no fees for self-service export, potential fees if vendor performs the export. Support contact: support@ezemrx.com.

## Export Coverage Assessment

### Data Domain Coverage

The export covers a meaningful but incomplete set of the data domains identified in product research:

**Clearly covered:**
- **Clinical data** — Demographics and clinical records via C-CDA R2.1. The C-CDA standard covers problems, medications, allergies, immunizations, vital signs, lab results, procedures, and encounters. However, the PDF provides no detail on which C-CDA sections are populated or what data is included beyond referencing the standard.
- **Billing and financial data** — CSV export with 17 columns covering claims at the line-item level: CPT codes, ICD codes, NDC codes, modifiers, charges, multi-payor payments, adjustments, and balances. This is genuine b(10) content — billing data that would not be available through a FHIR g(10) API.
- **Patient notes** — Ad-hoc clinical notes (telephone calls, etc.) exported as CSV with category, subject, and full note text.
- **Scanned documents** — All patient-scanned and uploaded documents exported as Base64-encoded CDA XML.

**Appears missing or not mentioned:**
- **Inventory data** — Medication/supply inventory, vaccine batch records, and distribution logs are a significant ezEMRx feature (especially for public health sites managing vaccine distribution) but are not mentioned in the export.
- **Scheduling/appointment data** — No mention of appointment history export.
- **Patient engagement data** — Portal access records, appointment reminders, and self-registration data are not addressed.
- **Interoperability records** — DIRECT messages, HIE exchange records, and FHIR API access logs are not mentioned.
- **Public health reporting data** — Immunization registry submissions, syndromic surveillance data, and quality measure records are not covered.
- **Audit logs** — No mention of system audit trail data.
- **Staff/administrative data** — Time tracking, user activity records not mentioned.

**Ambiguous:**
- Clinical data completeness depends entirely on which C-CDA sections ezEMRx populates, which is not documented. The PDF simply says "follows HL7 C-CDA R2.1 specifications" without detailing section coverage. Behavioral health, substance abuse, and treatment plan data — all core ezEMRx features — may or may not be captured in the C-CDA output.

### Export Format & Standards

The export uses a hybrid approach:
- **C-CDA R2.1** for clinical/demographic data and scanned records — a recognized HL7 standard
- **CSV** for billing claims and patient notes — a simple vendor-defined format

This is a reasonable design. C-CDA is appropriate for clinical data (though the level of detail in each section matters), and CSV is pragmatic for tabular billing data that doesn't map well to C-CDA. The CSV schemas are vendor-specific but straightforward.

The export is **not** FHIR-based and does not conflate b(10) with g(10) — this is genuine export documentation, not repackaged FHIR API docs. The inclusion of billing line items with CPT/ICD/NDC codes is a good signal that the vendor understands the b(10) requirement extends beyond clinical summaries.

Relationships between entities are handled implicitly: all files for a patient share the same PID prefix in the filename. Within the billing CSV, each row is a claim line item linked to a patient by PID. There is no explicit relational key between clinical records and billing records beyond the patient ID.

### Documentation Quality

The documentation is a **minimal but functional** 9-page PDF. It provides:
- ✅ Clear file naming convention with component explanation
- ✅ Complete column-level definitions for both CSV schemas (24 total columns)
- ✅ File category descriptions with format identification
- ✅ Standard references for C-CDA content

However, it lacks:
- ❌ No field-level documentation for C-CDA content (which sections are populated, what coded values are used)
- ❌ No sample export files or worked examples
- ❌ No data type specifications for CSV columns (date formats, string lengths, nullability)
- ❌ No value set documentation (what Payor codes look like, what Patient Notes Categories exist)
- ❌ No relationship documentation beyond shared PID
- ❌ No versioning/changelog (document says v2.0 but no v1.0 differences noted)
- ❌ No documentation of export size limits, performance characteristics, or error handling

A developer could implement a basic CSV import from this documentation. Interpreting the C-CDA output would require independent knowledge of the C-CDA standard — the vendor provides no vendor-specific guidance.

### Structure & Completeness

The billing CSV is the most complete section — 17 columns with descriptions covering the full claims lifecycle from charge through payment and adjustment. The patient notes CSV is simpler but adequate (7 columns).

The C-CDA sections (demographics/clinical and scanned records) have essentially zero field-level documentation. The vendor defers entirely to the HL7 C-CDA R2.1 specification, which is reasonable for standard clinical data but leaves open questions about what data is actually populated (e.g., does the C-CDA include social history? Advance directives? Goals?).

### (b)(10) vs (g)(10) Assessment

This is clearly b(10) documentation, not repurposed g(10)/FHIR content. The export is file-based (ZIP of CSV and XML files), not API-based. The inclusion of billing claims data, scanned documents, and ad-hoc notes demonstrates awareness that b(10) requires "all EHI" — not just the USCDI clinical subset. However, the absence of inventory, scheduling, public health reporting, and other administrative data means the export likely doesn't cover everything the product stores.

### Overall Assessment

ezEMRx provides a functional but sparse EHI export documentation package. The vendor has done genuine b(10) work — the export format is thoughtful (hybrid C-CDA + CSV), includes billing data that many vendors omit, and the documentation clearly explains the file naming convention and CSV schemas. This puts it ahead of vendors who simply point to their FHIR API.

The main weaknesses are: (1) no field-level documentation for C-CDA content, making it impossible to assess clinical data completeness; (2) several data domains the product stores (inventory, scheduling, public health reporting, interoperability records) appear absent from the export; and (3) no sample data or worked examples to validate interpretation.

For a small vendor (~50 employees) serving public health departments and ambulatory clinics, this represents a reasonable effort. The documentation was updated as recently as April 2024, suggesting active maintenance.

## Access Summary
- Final URL (after redirects): https://www.ezemrx.com/ehi-export
- Status: found
- Required browser: yes (Wix SPA, client-side rendering; PDF embedded in Wix PDF Viewer Pro widget requiring full JS execution)
- Navigation complexity: direct_link (single page, no clicks needed — but PDF requires browser rendering to discover)
- Anti-bot issues: none (standard Wix site)

## Obstacles & Dead Ends
- **Wix client-side rendering**: Raw HTML fetch returns only JavaScript framework; browser required for content extraction.
- **Wix PDF Viewer Pro widget**: The PDF is loaded dynamically via a Firebase cloud function (`getPdfUrl`) that returns a signed Google Cloud Storage URL. The iframe `src` is empty in the initial DOM — it gets populated after the TPA widget framework initializes. This caused a previous collection attempt to incorrectly report the widget as empty. The PDF URL is time-limited (signed URL with expiry) and cannot be fetched via a simple curl command.
- **Wayback Machine**: Cannot capture Wix SPA content — archived pages are the same JS shell.
- **No alternative documentation locations**: The PDF embedded in the viewer widget is the only export documentation. No additional docs on other pages.
