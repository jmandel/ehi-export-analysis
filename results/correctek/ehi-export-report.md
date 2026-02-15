# CorrecTek — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.correctek.com/cost-disclosure-and-transparency/
- CHPL ID: 10274
- Product: Spark 7.1
- Certification date: 2020-01-14

## Navigation Journal

**1. Initial probe:**
```bash
curl -sI -L "https://www.correctek.com/cost-disclosure-and-transparency/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 301 → `https://correctek.com/cost-disclosure-and-transparency/` → 301 → `https://correctek.com/cost-disclosure-and-transparency` → 200 OK. Content-Type: text/html. HubSpot-hosted site behind Cloudflare.

**2. Page fetch with curl:**
```bash
curl -sL "https://correctek.com/cost-disclosure-and-transparency" \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/correctek-page.html
```
Result: 307KB HTML, but the page is client-side rendered (HubSpot JS SPA). No visible text extracted via standard HTML parsing — all content is injected via JavaScript.

**3. Browser navigation:**
Navigated to the URL in Chrome. The page rendered correctly. Title: "Cost Disclosure & Transparency | CorrecTek". The page is a standard ONC mandatory disclosures page listing certified criteria, cost information, and API details.

**4. Searched for downloadable files:**
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/correctek-page.html
```
Result: Only one file link found: `https://appstudio.interopengine.com/partner/fhirR4endpoints-umc.json` (FHIR endpoints JSON for their g(10) API).

**5. Located the b(10) EHI Export section:**
Found at the bottom of the certification criteria table. The entire b(10) documentation is:

> §170.315(b)(10) Electronic Health Information (EHI) Export*
>
> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the us

The text is truncated on the live page — it cuts off at "the us". Confirmed via Wayback Machine (2024-04-18 capture) that the complete sentence reads "...saved to a folder specified by the **user**." — a minor content authoring error likely introduced during a site update.

**6. Downloaded the FHIR endpoints JSON:**
```bash
curl -sL "https://appstudio.interopengine.com/partner/fhirR4endpoints-umc.json" -o fhirR4endpoints-umc.json
```
Result: An empty FHIR Bundle with no entries: `{"resourceType":"Bundle","type":"collection","timestamp":"2026-02-07T14:37:24-08:00"}`. No customer endpoints are listed.

**7. Checked for additional EHI documentation:**
- Sitemap (`/sitemap.xml`): Only one disclosure-related URL exists: the cost-disclosure-and-transparency page itself.
- Probed common paths: `/ehi`, `/ehi-export`, `/interoperability`, `/onc`, `/compliance`, `/legal`, `/api`, `/fhir`, `/documentation` — all returned 404.
- The linked Interoperability Engine Open API Documentation (https://www.interopengine.com/2021/open-api-documentation.html) is a detailed (g)(10) FHIR R4/US Core API guide from EMR Direct. It documents the SMART on FHIR authorization flow, USCDI data classes, and Bulk Data Access. This is entirely the g(10) standardized API — not the b(10) EHI export.

**8. Checked Wayback Machine:**
```bash
curl -s "http://web.archive.org/cdx/search/cdx?url=www.correctek.com/cost-disclosure-and-transparency&output=text&fl=timestamp,statuscode&from=20230101&limit=20"
```
10 captures from 2020–2025, all returning 200. The 2024-04-18 capture confirmed the complete (untruncated) EHI text. No additional EHI documentation was ever present on any captured version.

## What Was Found

The entire EHI export documentation from CorrecTek consists of a **single sentence** on their mandatory disclosures page:

> *EHI can be exported in PDF or C-CDA format. Records for a patient are exported to one or more PDF/C-CDA files. The files created by the export are saved to a folder specified by the user.*

That is the complete technical documentation for their 170.315(b)(10) EHI Export certification. There is:

- **No data dictionary** — no listing of what data fields, tables, or categories are exported
- **No export format specification** — no details on the PDF structure or C-CDA template/profile used
- **No schema files** — no XSD, JSON Schema, or other machine-readable format definition
- **No sample data** — no example export files
- **No user guide** — no instructions for initiating the export, no screenshots of the export interface
- **No API documentation** specific to the export (the linked API docs are for the g(10) FHIR API)

The only additional artifact is a FHIR R4 endpoints JSON file linked on the page, which is an empty Bundle with no entries — suggesting either no customers are currently integrated with the FHIR API, or the file is a placeholder.

## Export Coverage Assessment

### Data Domain Coverage

This is where the single-sentence documentation creates the biggest gap. CorrecTek Spark is a **correctional healthcare EHR** that stores a wide range of patient data:

**Known data domains (from product research):**
- Demographics, contacts, insurance/enrollment
- Medical encounters and clinical notes
- Behavioral health records
- Dental records
- Medication management (eMAR, EPCS, e-prescribing)
- Lab orders and results
- Radiology/imaging orders and results
- Allergies, immunizations, vital signs, problem lists
- Billing (claims, eligibility, ERA posting, Medicaid 1115 waiver)
- Sick call requests
- Inmate tracking/custody data (received from jail management systems)
- Care plans, referrals
- Custom correctional healthcare forms (intake screenings, NCCHC/ACA compliance forms)

**What the documentation tells us about coverage:** Almost nothing. The export is described as "PDF or C-CDA format" — but there is no specification of which data domains are included. The key questions are completely unanswered:

- **Billing data**: Not mentioned. PDF/C-CDA formats are clinical document standards that don't naturally represent billing records (claims, ERA postings, eligibility data).
- **Behavioral health records**: Not mentioned. These are critical in a correctional EHR. Are they included in the C-CDA?
- **Dental records**: Not mentioned. Spark explicitly integrates dental into the unified chart — is dental data exported?
- **Correctional-specific data**: Intake screenings, sick call requests, custody/tracking data, compliance documentation — none of these have natural C-CDA representations.
- **Medication administration records (eMAR)**: The eMAR is a core correctional nursing workflow. Is it captured in the C-CDA, or only active medication lists?
- **Lab and imaging results**: Likely partially covered by C-CDA, but no confirmation.

The statement "Records for a patient are exported to one or more PDF/C-CDA files" could mean anything from a single-page clinical summary to a comprehensive dump of every document in the chart. Without a data dictionary or content specification, it's impossible to assess coverage.

**Likely reality:** Given that the export uses PDF and C-CDA:
- C-CDA will cover the standard clinical summary data (demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures) — essentially the USCDI/US Core subset.
- PDF may capture additional clinical notes and documents.
- Billing, dental, behavioral health-specific assessments, correctional forms, eMAR details, and custody data are almost certainly **not** included in a standard C-CDA export unless CorrecTek has done significant custom work (which they haven't documented).

### Export Format & Standards

- **Format**: PDF and/or C-CDA (the asterisk with "PDF or C-CDA" suggests the user may have a choice, or different data may go to different formats).
- **C-CDA**: No version, template, or profile specified. No indication of which C-CDA document type (CCD, Discharge Summary, etc.). No section-level detail.
- **PDF**: No detail on structure — could be a simple printout of the chart, or structured clinical documents rendered as PDF.
- **Delivery**: Files saved to a local folder. No mention of encryption, compression, or integrity verification.

The choice of PDF/C-CDA is concerning for a b(10) export. C-CDA is designed for clinical summaries — it covers the standard clinical data classes well but has no natural representation for:
- Detailed billing records
- Correctional-specific workflows (intake screenings, sick call management)
- eMAR administration details
- Dental charts
- Custom form data

A vendor that has genuinely addressed b(10) for a correctional EHR would need to export data that goes well beyond what C-CDA can represent. The absence of any additional export format (database dump, CSV, custom XML) for non-clinical data suggests this export likely covers only the clinical summary portion of the record.

### Documentation Quality

**Extremely poor.** One truncated sentence is not documentation. A developer receiving this export would have no way to:
- Know what data to expect
- Parse the C-CDA reliably (no profile/template guidance)
- Verify completeness (no data dictionary to compare against)
- Automate import (no schema or sample files)

This is the absolute minimum a vendor could provide — a single sentence saying "we export in these formats" — without any substantive technical detail. It reads as a compliance checkbox rather than genuine documentation.

### Structure & Completeness

- **Field-level documentation**: None
- **Data types/value sets**: None
- **Entity relationships**: None
- **Sample data**: None
- **Versioning/change history**: None
- **Export instructions**: None (just "saved to a folder specified by the user")

## Access Summary
- Final URL (after redirects): https://correctek.com/cost-disclosure-and-transparency
- Status: found
- Required browser: yes (HubSpot JS-rendered page; curl returns empty HTML)
- Navigation complexity: direct_link (b(10) section is on the single disclosure page)
- Anti-bot issues: Cloudflare present but not blocking; main issue is JS rendering requirement

## Obstacles & Dead Ends
- **Truncated text**: The b(10) description is cut off at "the us" on the live page (missing "er." to complete "the user."). Confirmed complete text via Wayback Machine.
- **JS-rendered page**: curl cannot extract visible content; browser required for text extraction.
- **Empty FHIR endpoints JSON**: The linked endpoints file contains an empty FHIR Bundle with no entries.
- **No additional documentation found**: Sitemap, path probing, and Google searches returned no additional EHI-specific pages or documents.
