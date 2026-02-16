# ASP.MD Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.asp.md/export/
- CHPL IDs: 10818
- Certification Number: 15.02.05.1026.ASPM.01.01.0.220203
- Certification Date: 2022-02-03
- Product: ASP.MD Medical Office System, Version 92

## Navigation Journal

**Step 1: Initial probe**
```bash
curl -sI -L "https://www.asp.md/export/" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200 OK, Content-Type: text/html; charset=UTF-8. The site is a WordPress installation (nginx/1.10.3 on Ubuntu). No redirects.

**Step 2: Fetch and examine page content**
```bash
curl -sL "https://www.asp.md/export/" -H 'User-Agent: Mozilla/5.0' -o export-page.html
```
Page is 76,272 bytes. Most of the HTML is WordPress theme boilerplate (Visual Composer CSS, navigation, footer). The actual content is a single short block of text.

**Step 3: Extract structured content via WordPress REST API**
```bash
curl -sL "https://www.asp.md/wp-json/wp/v2/pages/72194" -H 'User-Agent: Mozilla/5.0'
```
Confirmed the page was published 2023-11-14 and has never been modified since. The rendered content is five short paragraphs.

**Step 4: Search for downloadable files**
Searched the HTML for links to PDF, ZIP, XLSX, CSV, JSON, YAML, XSD, and other downloadable formats. Found only one link: `http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf` — an external HL7 standard document, not vendor-specific documentation. Not downloaded per instructions (external standards documentation).

**Step 5: Search for additional export-related pages**
- Enumerated all pages via WordPress REST API (`/wp-json/wp/v2/pages?per_page=100`): 10 pages total. Only one is export-related: the `/export/` page itself.
- Checked the WordPress sitemap (`/wp-sitemap-posts-page-1.xml`): same result.
- Probed common documentation paths (`/api/`, `/fhir/`, `/interoperability/`, `/data-dictionary/`, `/api-docs/`, `/developer/`): all returned 404.
- Checked the mandatory disclosures page (`/disclosures-2/`): confirms (b)(10) certification but contains no additional export documentation or links.
- Checked the software features page (`/software/`): marketing copy about the EHR/PM system with no references to data export, FHIR APIs, or interoperability documentation.
- Web search for `"asp.md" "electronic health information" export documentation`: no additional documentation found beyond the registered URL.

**Step 6: Browser verification**
Loaded the page in Chrome and took a full-page screenshot. The page renders exactly as the HTML suggests: a heading, five lines of text, and the site footer. No hidden content, no collapsed accordions, no JavaScript-loaded content.

## What Was Found

The EHI export documentation at https://www.asp.md/export/ consists of a single web page with the following complete text:

> **Health Information Export**
>
> The electronic health information export will include data in the following formats:
>
> C-CDA Documentation can be found here http://www.hl7.org/ccdasearch/pdfs/Companion_Guide.pdf
>
> Text files (industry standard)
>
> PDF files (industry standard)
>
> Files relevant to each patient will be stored in folders with name format LASTNAME_FIRSTNAME_DOB_MRN where DOB is Date of Birth formatted YYYYMMDD and MRN is medical record number, an integer linking to the MRN in C-CDA.

That is the entirety of the documentation. There is:
- **No data dictionary** — no tables, fields, columns, data types, or schemas
- **No export format specification** beyond naming three formats (C-CDA, text, PDF)
- **No field-level documentation** of any kind
- **No sample exports or examples**
- **No schema files** (XSD, JSON Schema, etc.)
- **No API documentation**
- **No instructions** for how a practice administrator or patient would initiate an export
- **No description of what data is included** in the export beyond the implicit scope of C-CDA

The page was published 2023-11-14 (roughly a year and a half after the product's 2022-02-03 certification date) and has not been modified since.

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes three output formats — C-CDA, text files, and PDF files — but provides **no specification of what data domains are included** in any of them.

**C-CDA coverage (implied):** C-CDA is a well-defined standard that covers a specific set of clinical data: demographics, problems, medications, allergies, lab results, vitals, immunizations, procedures, and clinical notes. However, the documentation does not specify which C-CDA document type(s) are generated (CCD, Referral Note, Discharge Summary, etc.) or which sections are populated. It only links to the HL7 Companion Guide — an external reference document, not a vendor-specific mapping.

**Text and PDF files (undefined):** The documentation says the export includes "text files (industry standard)" and "PDF files (industry standard)" but provides no information about what data these contain, what "industry standard" means in this context, or how they relate to the C-CDA content. These could be anything from clinical notes to billing statements to the full medical record — there is no way to know from the documentation.

**Data domains from product research — coverage status:**

| Domain | Covered? | Notes |
|--------|----------|-------|
| Demographics | Unknown | Likely in C-CDA but not documented |
| Problem lists | Unknown | Likely in C-CDA but not documented |
| Medications / e-prescribing | Unknown | Likely in C-CDA but not documented |
| Allergies | Unknown | Likely in C-CDA but not documented |
| Lab results | Unknown | Likely in C-CDA but not documented |
| Vital signs | Unknown | Likely in C-CDA but not documented |
| Clinical notes | Unknown | May be in text/PDF files but not documented |
| Immunizations | Unknown | Likely in C-CDA but not documented |
| Procedures | Unknown | Likely in C-CDA but not documented |
| Documents/images | Unknown | May be in PDF files but not documented |
| **Billing/claims data** | **Not mentioned** | No reference to billing, claims, charges, payments, or remittances |
| **Scheduling/appointments** | **Not mentioned** | Not required EHI, but notable given it's a PM system |
| **Insurance/eligibility** | **Not mentioned** | Part of billing records, no reference |
| **Patient portal messages** | **Not mentioned** | No reference to secure messages |
| **Quality measure data** | **Not mentioned** | No reference to CQM/MIPS data |
| **Family health history** | Unknown | May be in C-CDA but not documented |
| **Implantable devices** | Unknown | May be in C-CDA but not documented |
| **Care plans** | Unknown | May be in C-CDA but not documented |

The fundamental problem is that the documentation is too sparse to assess coverage. We can infer that C-CDA will carry the standard clinical data domains, but:

1. There is no confirmation of which C-CDA sections are populated
2. The text and PDF file contents are completely unspecified
3. **Billing data — a core data domain for this integrated EHR/PM product — is entirely absent from the documentation.** ASP.MD's product research shows it is a deeply integrated billing system with claims submission, adjudication, electronic remittance, and HCC coding. None of this appears in the export documentation.
4. No specialty-specific or custom clinical data is described

### Export Format & Standards

The export uses three formats:
- **C-CDA**: A recognized healthcare data standard, appropriate for clinical summaries. However, C-CDA has inherent limitations — it does not naturally represent billing data, scheduling data, or many types of administrative records. If the export relies solely on C-CDA for structured data, it will miss significant portions of what this integrated EHR/PM system stores.
- **Text files**: Completely unspecified. No format definition, no field descriptions, no encoding information.
- **PDF files**: Completely unspecified. These could be rendered clinical notes, printed reports, scanned documents, or anything else.

The folder structure (`LASTNAME_FIRSTNAME_DOB_MRN`) is the only structural detail provided. It tells us the export is organized per-patient with the MRN linking to the C-CDA content.

A third party receiving this export would have C-CDA data they could parse (using the standard), but the text and PDF files would be opaque without additional documentation. There is no way to programmatically process the non-C-CDA portions of the export.

### Documentation Quality

This is among the most minimal EHI export documentation possible. Five sentences on a web page, with no:
- Data dictionary
- Field definitions
- Data type specifications
- Value sets or coded value references
- Sample exports
- Worked examples
- User instructions for initiating an export
- Schema or machine-readable format specification
- Version history or change log

A developer could not implement an import of this data based on the documentation alone. They would know to expect C-CDA files (parseable via the standard) in patient-named folders, but the text and PDF files would require manual inspection of actual export output to understand.

The documentation reads as a compliance checkbox — the minimum text needed to have a page at the registered URL. It was published in November 2023, roughly 20 months after certification, and has not been updated since.

### Structure & Completeness

- **Granularity**: Page-level only. No tables, no fields, no data types.
- **Coded fields**: Not documented.
- **Relationships**: Not documented (the MRN linking to C-CDA is the only cross-reference mentioned).
- **Versioning**: None.

### (b)(10) vs (g)(10) Assessment

The documentation does not appear to conflate (b)(10) with (g)(10). It does not mention FHIR, Bulk Data, or standardized APIs. However, the reliance on C-CDA as the primary structured format suggests the export may only cover the clinical data domains that C-CDA naturally represents — which substantially overlaps with USCDI/US Core scope. The text and PDF files could extend coverage beyond C-CDA's scope, but without documentation, this is speculative.

The critical question for this vendor: **does the export include billing data?** ASP.MD is an integrated EHR and billing system. Billing records — claims, charges, payments, remittances, coding — are core EHI for this product. C-CDA does not naturally carry this data. The text and PDF files might contain billing information, but the documentation does not say so.

## Access Summary
- Final URL (after redirects): https://www.asp.md/export/
- Status: found
- Required browser: no (content is static HTML, no JS needed)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends

No technical obstacles were encountered. The URL works, the page loads, the content is accessible. The obstacle is the content itself — it is extremely sparse and does not constitute meaningful technical documentation of the EHI export.

- No downloadable files exist on the page (only an external HL7 link)
- No additional export documentation exists elsewhere on the site (confirmed via sitemap, WP API, path probing, and web search)
- The mandatory disclosures page confirms (b)(10) certification but adds no export documentation
- The software features page describes the product's capabilities but provides no technical export documentation
