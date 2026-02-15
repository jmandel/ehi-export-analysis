# Dexter Solutions Inc — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://dexter-solutions.com/certification
- Final URL (after redirects): https://www.dexter-solutions.com/ (homepage)
- CHPL IDs: 11432
- Product: eZDocs v5.5
- CHPL Product Number: 15.02.04.2708.eZDo.05.02.1.240102
- Certification Date: 2024-01-02

## Navigation Journal

### Step 1: Initial probe of the registered URL

```bash
curl -sI -L "https://dexter-solutions.com/certification" \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
```

Result: HTTP 301 redirect to `https://www.dexter-solutions.com/certification`, which returned HTTP 200 with `Content-Type: text/html`. The site is hosted on Wix (Pepyaka server, Cloudflare CDN, parastorage.com assets).

### Step 2: Fetching and examining the page

```bash
curl -sL "https://www.dexter-solutions.com/certification" \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/page.html
```

The HTML returned (9,599 bytes) was a Wix SPA shell — nearly all JavaScript framework code (Astro framework + Wix platform), with no visible page-specific content. The `<title>` tag reads "Home | Dexter Solutions Inc." — indicating the `/certification` route is not recognized and falls through to the homepage.

### Step 3: Browser rendering

Navigated to `https://www.dexter-solutions.com/certification` in Chrome. The page renders as the homepage of Dexter Solutions Inc, with navigation links: Home, Products, BPO Services, About, Contact. No "Certification" or "Compliance" link exists in the navigation. The page content is a marketing site for their HealthIT products (eZDocs EHR & PM, WoundPlan, eZDMEs ERP) and BPO services.

### Step 4: Probing alternative paths

Tested the following paths, all of which return HTTP 200 but render as the homepage (Wix catch-all routing):

- `/certification` — homepage
- `/compliance` — homepage
- `/legal` — homepage
- `/onc` — homepage
- `/ehi` — homepage
- `/ehi-export` — homepage
- `/disclosures` — homepage
- `/mandatory-disclosures` — homepage
- `/b10` — homepage
- `/interoperability` — homepage
- `/transparency` — homepage

The Wix platform returns HTTP 200 for any path but always renders the homepage content. The `/sitemap.xml` path also returns the homepage HTML rather than a sitemap.

### Step 5: Checking the eZDocs product page

Navigated to `https://www.dexter-solutions.com/products/ezdocs`. This is a marketing page describing eZDocs EHR & PM features (charting, scheduling, e-prescribing, lab integration, etc.). No links to certification, EHI export documentation, or any compliance resources.

### Step 6: Wayback Machine search

```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=dexter-solutions.com/*&matchType=prefix&output=text&fl=timestamp,original,statuscode&from=20200101&limit=200"
```

No Wayback Machine captures exist for any subpages of dexter-solutions.com from 2020 onward. Historical captures (2011–2016) only captured the homepage. The `/certification` path was never archived.

### Step 7: Web search for cached/indexed content

Multiple web searches confirmed that the certification page previously existed and contained substantive content. Search engine snippets and summaries consistently describe:

1. **Certification disclosures**: eZDocs EHR Version 5.5 is certified by Drummond Group (ONC-ACB), CHPL ID 15.02.04.2708.eZDo.05.02.1.240102, certification date 01/02/2024.
2. **EHI export documentation**: "The attached document lists the details of exporting EHI data in CDA (XML) and pdf format for a single patient and multiple patients."
3. **A downloadable PDF**: Referenced as "170.315 (b)(10) Electronic Health Information Export (pdf)" — a separate document that was linked from the certification page.
4. **Transparency disclosures**: No additional cost for training/implementation for small to medium practices (1–10 providers), onsite support for 2 days at no additional cost, Direct message storage included with subscription.
5. **API access**: Users can email info@dexter-solutions.com with subject "API access" to get started.

### Step 8: Attempted PDF recovery

Probed multiple potential PDF URLs on the Wix site and Wix static storage (static.wixstatic.com, docs.wixstatic.com), but no PDF documents were accessible. The Wix platform serves the homepage HTML for any path, and the static storage requires exact file hashes in the URL.

### Conclusion

The vendor's website was recently rebuilt on Wix (the current site appears to be a modern redesign), and the certification page with its EHI export documentation was not migrated to the new site. The certification page content — including the linked PDF documenting the b(10) EHI export format — is no longer publicly accessible.

## What Was Found

**Nothing currently accessible.** The registered URL redirects to the vendor's homepage, and the EHI export documentation (including a PDF describing the CDA/XML export format) is no longer available at any publicly accessible URL on the vendor's site.

**From search engine caches**, we can reconstruct that the certification page previously described:

- **Export format**: CDA (XML) and PDF, supporting both single-patient and multi-patient (bulk) exports
- **A detailed PDF document** titled "170.315 (b)(10) Electronic Health Information Export" that was available for download
- **API access** available by emailing info@dexter-solutions.com with subject "API access"

However, the actual documentation content — the PDF with export format details, data dictionaries, field definitions — could not be retrieved from any source (Google cache, Wayback Machine, Bing cache, or the current site).

## Export Coverage Assessment

### Data Domain Coverage

**Cannot be assessed.** The EHI export documentation is not currently accessible. Based solely on search engine snippet reconstructions:

- The export uses CDA (XML) and PDF format, which suggests it may be based on the C-CDA standard. If so, it would likely cover clinical domains (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, clinical notes) but potentially miss:
  - **Billing data** (charges, claims, payments) — C-CDA does not natively represent billing
  - **Scheduling/appointment data** — not part of C-CDA
  - **RPM/CCM data** — remote patient monitoring readings and chronic care management records
  - **DME ordering data** — durable medical equipment orders with comments
  - **Insurance eligibility data**
  - **Custom specialty templates** — practice-specific clinical forms
  - **Task management data**

Without the actual documentation, this is speculative. The format description ("CDA (XML) and PDF") raises a concern about (b)(10) vs (g)(10) conflation — if the export is purely C-CDA, it may only cover the clinical summary subset rather than all EHI. However, it's also possible the PDF format supplements the CDA with additional data domains.

### Export Format & Standards

- **Format**: CDA (XML) and PDF (per search engine caches)
- **Standard**: Likely C-CDA (Consolidated Clinical Document Architecture)
- **Scope**: Single patient and multiple patients (bulk)
- **Concern**: C-CDA is primarily a clinical summary standard. A true (b)(10) export of *all* EHI would need to go beyond what C-CDA covers, particularly for billing, scheduling, and specialty-specific data that eZDocs stores.

### Documentation Quality

**Cannot be assessed** — the documentation is not accessible. The fact that search engine snippets reference a specific downloadable PDF suggests there was at least some structured documentation, but its depth and quality cannot be evaluated.

### Structure & Completeness

**Cannot be assessed** — no documentation is available for review.

## Access Summary
- Final URL (after redirects): https://www.dexter-solutions.com/ (homepage)
- Status: redirect_to_homepage
- Required browser: yes (Wix SPA, but even with browser the page is gone)
- Navigation complexity: dead — the registered URL no longer serves the certification content
- Anti-bot issues: none (the page simply doesn't exist on the rebuilt site)

## Obstacles & Dead Ends

1. **Site rebuild lost the certification page**: The vendor rebuilt their website on Wix, and the `/certification` path (along with all other non-standard paths) now falls through to the homepage via Wix's catch-all routing.

2. **No Wayback Machine archive**: The certification page was never captured by the Wayback Machine. The domain has historical captures going back to 2011, but only of the homepage — no subpages were ever archived.

3. **Google cache blocked**: Attempting to access Google's cached version of the page was blocked by a CAPTCHA challenge.

4. **PDF not recoverable**: The "170.315 (b)(10) Electronic Health Information Export" PDF that was previously linked from the certification page could not be found on any Wix static storage URL or cached version.

5. **No alternative documentation locations**: The vendor's site has no other pages linking to certification or EHI documentation. The eZDocs product page is purely marketing content.

6. **Search engine snippets are the only evidence**: Multiple web search queries returned consistent summaries describing the certification page content (CDA/XML and PDF export, single and multiple patients, API access via email), but the actual full page content and linked PDF are not accessible.

This represents a **compliance gap**: the (b)(10) certification requirement mandates that export format documentation be available at a publicly accessible hyperlink. The registered URL no longer serves this documentation, meaning Dexter Solutions is currently not meeting this requirement.
