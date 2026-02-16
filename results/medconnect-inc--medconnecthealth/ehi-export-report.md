# MedConnect, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://medconnecthealth.com/electronic-health-information-export/
- CHPL IDs: 9183
- Product: MedConnectHealth 3.0
- Certification date: 2017-12-12

## Navigation Journal

1. Probed the registered URL with curl:
   ```bash
   curl -sI -L "https://medconnecthealth.com/electronic-health-information-export/" \
     -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
   ```
   Returned HTTP 200, Content-Type: text/html; charset=UTF-8. WordPress site (Link headers point to wp-json endpoints). Curious custom headers: `Server: Commodore64`, `X-Powered-By: Sunshine and Rainbows`.

2. Downloaded the full page HTML (49,778 bytes):
   ```bash
   curl -sL "https://medconnecthealth.com/electronic-health-information-export/" \
     -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html
   ```

3. Searched page source for downloadable file links:
   ```bash
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' ehi-export-page.html
   ```
   Found three PDFs:
   - `EHI_Export_Documentation.pdf` — the EHI export documentation (relevant)
   - `RealWorldTestResults2022.pdf` — real-world testing results (not relevant)
   - `Xerox-Scan_10312022091038-rwt-updated.pdf` — scanned real-world testing doc (not relevant)

4. Downloaded the EHI Export Documentation PDF:
   ```bash
   curl -sL "https://staging.medconnecthealth.com/wp-content/uploads/2023/11/EHI_Export_Documentation.pdf" \
     -H 'User-Agent: Mozilla/5.0' -o EHI_Export_Documentation.pdf
   ```
   Verified: `file EHI_Export_Documentation.pdf` → "PDF document, version 1.6 (zip deflate encoded)". 334,660 bytes, 1 page.

5. Confirmed page content via WordPress REST API:
   ```bash
   curl -sL "https://www.medconnecthealth.com/wp-json/wp/v2/pages/2479" -H 'User-Agent: Mozilla/5.0'
   ```
   Page content is simply a single link to the PDF. Page published and last modified 2023-11-09.

6. Navigated to the page in a browser. Screenshot confirms: the page has a heading "Electronic Health Information Export" and a single link labeled "170.315(b)(10) EHI Export Documentation" pointing to the PDF. No other substantive content — just the site footer and sidebar with recent blog posts.

7. Checked the mandatory disclosures page (https://www.medconnecthealth.com/pricing/) for additional EHI documentation — found only a mention of "170.315 (b)(10): Electronic Health Information Export" in the certified criteria list, no additional links or content.

8. Checked for embedded URLs, attachments within the PDF:
   ```bash
   pdfdetach -list EHI_Export_Documentation.pdf  # 0 embedded files
   pdftotext EHI_Export_Documentation.pdf - | grep -oiE 'https?://[^ ]+'  # only self-referential URL
   ```
   The PDF contains only a self-referential link back to the same page (https://www.medconnecthealth.com/electronic-health-information-export/).

## What Was Found

The entire EHI export documentation consists of a single 1-page PDF authored by Brett Chapman (created 2023-11-09 using Acrobat PDFMaker 23 for Word). The document contains:

### Compliance Statement
The document restates the regulatory requirements of 170.315(b)(10), confirming that MedConnectHealth supports:
- **Single patient EHI export**: Users can create export files for individual patients at any time, without developer assistance. Export capability is restricted to specific users or system administrators.
- **Patient population EHI export**: Two options — individual exports for each patient, or a bulk export of all patients "upon request" (performed by MedConnectHealth, not self-service by the user).
- **Documentation**: Links back to the registered URL.

### Export Format
The export is a ZIP file containing a folder per patient/clinic with:
- **C-CDA in compliance with USCDI v1** (XML format)
- **Demographics** (PDF)
- **Scanned Documents** (PDF, JPG, PNG)
- **Clinical Notes/Lab Results** (PDF)

That is the complete description of the export format. There is no data dictionary, no field-level documentation, no schema files, no sample exports, and no API documentation.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, MedConnectHealth stores data across many domains. The export format description reveals significant gaps:

**Covered (at least partially):**
- **Demographics** — exported as PDF (not computable)
- **Clinical documentation** — C-CDA covers problems, medications, allergies, immunizations, vitals, lab results, procedures per USCDI v1
- **Clinical notes** — exported as PDF
- **Lab results** — exported as PDF
- **Scanned documents** — exported as original formats (PDF, JPG, PNG)

**Clearly missing or not mentioned:**
- **Billing/financial data** — charges, claims, remittance advice, payment postings, patient balances, insurance eligibility. This is a major gap; MedConnectHealth has a full practice management/billing module.
- **Prescriptions/e-prescribing history** — medication orders, EPCS data, formulary checks (beyond what's in the C-CDA medication list)
- **Orders** — lab/diagnostic orders and their status
- **Care plans and goals** — beyond what the C-CDA may contain
- **Patient portal data** — messages, refill requests, appointment requests, electronic form submissions, bill pay history
- **Kiosk/check-in data** — scanned IDs, insurance cards, check-in records
- **Telehealth session data** — visit records, session metadata
- **Quality/CQM data** — clinical quality measure calculations
- **Interoperability records** — C-CDA documents sent/received, DIRECT messages, HIE exchange records
- **Insurance/enrollment information** — beyond basic demographics

**Ambiguous:**
- The C-CDA "in compliance with USCDI v1" covers a defined subset of clinical data (problems, medications, allergies, immunizations, vitals, labs, procedures, health concerns, goals, assessments, care teams, clinical notes). However, C-CDA is a clinical summary standard — it does not naturally accommodate billing records, custom form data, or specialty-specific clinical data beyond what USCDI v1 defines.
- "Demographics (PDF)" — exporting demographics as PDF rather than structured data means the information is not computably accessible. It's unclear if this PDF contains more demographic detail than the C-CDA header.
- "Clinical Notes/Lab Results (PDF)" — unclear if these duplicate the C-CDA content or include additional notes/results not in the C-CDA.

### Export Format & Standards

The export uses a hybrid approach:
- **C-CDA XML** for structured clinical data (USCDI v1 scope)
- **PDF** for demographics, clinical notes, and lab results
- **Original format files** (PDF/JPG/PNG) for scanned documents
- **ZIP packaging** with folder-per-patient structure

This is essentially a **USCDI v1 clinical summary plus scanned documents**, not a comprehensive EHI export. The C-CDA covers the (g)(10) clinical data slice, while the PDFs and scanned documents add some additional material — but the export entirely omits the practice management, billing, and specialty-specific data domains that constitute a large portion of the designated record set.

The heavy use of PDF is problematic: demographics and lab results in PDF are not computable. A third party could not import this data into another system without manual data entry or OCR for anything beyond the C-CDA XML content.

### Documentation Quality

The documentation is extremely minimal:
- **No data dictionary** — no field-level documentation of any kind
- **No schema files** — no XSD, no C-CDA template constraints, no custom profile documentation
- **No sample exports** — no example files showing what the export looks like
- **No export instructions** — no screenshots or step-by-step guide for users
- **No value set documentation** — no description of coded fields or terminology
- **No format specification** beyond the 4-bullet folder structure

The document reads as a compliance checkbox — it restates the regulatory requirements verbatim and adds a minimal export format description. A developer could not implement an import of this data based solely on this documentation; they would need to know C-CDA independently and would have no guidance on the PDF content structure.

### Structure & Completeness

The documentation is a single page with two sections: a restatement of regulatory requirements and a 4-line export format description. There is:
- No versioning or change history (though the PDF creation date is visible)
- No entity/relationship documentation
- No cardinality or constraint information
- No description of how the population export differs structurally from the single-patient export
- No documentation of the "upon request" bulk export process

### (b)(10) vs (g)(10) Assessment

This export conflates (b)(10) and (g)(10). The C-CDA with USCDI v1 compliance is essentially the same clinical data scope as a (g)(10) patient summary. The addition of PDF demographics, scanned documents, and PDF clinical notes goes slightly beyond a pure C-CDA clinical summary, but the export still does not address the fundamental (b)(10) requirement: export of **all** electronic health information the product stores.

MedConnectHealth is an integrated EHR + practice management platform with billing, scheduling, patient portal, kiosk, telehealth, and quality reporting modules. The export documentation describes a clinical summary plus document attachments — a small fraction of the total data the product manages about patients.

## Access Summary
- Final URL (after redirects): https://medconnecthealth.com/electronic-health-information-export/ (no redirect)
- Status: found
- Required browser: no (PDF direct link works with curl)
- Navigation complexity: direct_link (one click from page to PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The URL was live, the PDF downloaded cleanly.
- The page references `staging.medconnecthealth.com` in several internal links (including the PDF link), suggesting the site may have been migrated from a staging environment without updating internal URLs. Both staging and www domains resolve to the same content.
- The PDF contains no embedded URLs or attachments pointing to additional documentation.
- No additional EHI export documentation was found elsewhere on the site.
