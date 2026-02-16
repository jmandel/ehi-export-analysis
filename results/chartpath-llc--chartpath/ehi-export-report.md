# ChartPath, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://info.chartpath.com/ehiexport
- CHPL IDs: 10258
- Product: ChartPath v1.29
- Developer: ChartPath, LLC (now part of LivTech)
- Certification date: 2019-12-27

## Navigation Journal

### Step 1: Probe registered URL
```bash
curl -sI -L "https://info.chartpath.com/ehiexport" -H 'User-Agent: Mozilla/5.0'
```
Returned HTTP 200, `Content-Type: text/html`, hosted on HubSpot (Cloudflare CDN). The `info.chartpath.com` subdomain is a HubSpot-hosted marketing/landing page site, separate from the main `chartpath.com` domain.

### Step 2: Fetch and examine page content
```bash
curl -sL "https://info.chartpath.com/ehiexport" -H 'User-Agent: Mozilla/5.0' -o ehiexport-page.html
```
Page is 15,298 bytes. After stripping HTML/CSS/JS, the substantive content is just 7 sentences (approximately 90 words) describing the EHI export format. No download links, no data dictionary, no schema, no API documentation, no sample files, no screenshots of the export interface.

### Step 3: View page in browser
Navigated to https://info.chartpath.com/ehiexport in Chrome. The page renders as:
- ChartPath logo at top
- Blue banner heading: "Electronic Health Information Export"
- Seven bullet-style paragraphs describing the export
- Copyright © 2023 footer
- HubSpot live chat widget

No interactive elements, expandable sections, or hidden content. Screenshot saved.

### Step 4: Check mandatory disclosures page
Navigated to https://chartpath.com/2015-cehrt (the registered mandatory disclosures URL from CHPL metadata). This page contains:
- "2015 CEHRT" heading
- Buttons for: Costs and Considerations (PDF), Testing Plans/Results 2022-2025 (PDFs), FHIR - API (PDF), FHIR - OAUTH (PDF), and "EHI Export"
- Certification details: Date December 27, 2019; Version 1.29; Certificate 15.04.04.2996.Char.12.01.1.191227
- Certified criteria listing
- FHIR documents section at bottom with links to FHIR API and FHIR OAUTH PDFs

The "EHI Export" button on the CEHRT page links back to the same https://info.chartpath.com/ehiexport page (via HubSpot CTA redirect).

### Step 5: Examine FHIR API PDF (for context)
The FHIR API PDF (hosted on HubSpot Documents at https://hubs.ly/Q01l6phT0) is a 55-page document covering ChartPath's (g)(10) FHIR API. Table of contents shows standard US Core FHIR resources: Patient, AllergyIntolerance, CarePlan, CareTeam, Problems/Health Concern, Implantable Device, Diagnostic Report/Clinical Notes/DocumentReference, Laboratory Result Observation, Goal, Immunization, Medication, Smoking Status, Procedure, Provenance, Vital Signs, Encounter List, and Complete Patient Summary (CCDA). This is clearly (g)(10) standardized API documentation, not (b)(10) EHI export documentation. Did not download as it is not the EHI export mechanism.

### Step 6: Search for additional documentation
- `site:info.chartpath.com` — only the single ehiexport page exists on this subdomain
- `site:chartpath.com EHI export data dictionary` — only returns the ehiexport page
- General web search for "ChartPath EHI export documentation data dictionary" — no additional ChartPath-specific documentation found
- No Wayback Machine captures found for the ehiexport page

## What Was Found

The EHI export documentation consists of a single HubSpot landing page with approximately 90 words of text. The entire content is:

> The patient EHI export contains data from the patient's chart. Multiple file formats are used to store this information.
>
> ZIP is an archive file format.
>
> PDF or Portable Document Format is a file format that is used to present text or image based documents.
>
> C-CDA or Consolidated Clinical Document Architecture is a file format used for health information exchange.
>
> The export file itself is a zip file. It contains zip files of PDFs, C-CDAs, and other files attached to the patient's chart.
>
> Patient demographic information can be found in the face sheet document as well as in the PDF and C-CDA documents for each encounter.
>
> Information for each patient encounter is available in both PDF and C-CDA format in their respective zip archive.
>
> Files attached to the patient's chart are also included in their original format in a zip archive.

**Export format described**: A ZIP archive containing:
1. Per-encounter PDFs (in a sub-ZIP)
2. Per-encounter C-CDA documents (in a sub-ZIP)
3. Attached files in original format (in a sub-ZIP)
4. A "face sheet" document with patient demographics

There is no data dictionary, no schema, no field-level documentation, no sample export files, no API specification, no user guide, and no screenshots of the export interface.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export page provides almost no information about what data domains are covered. Based on the description, the export appears to produce:

- **Encounter-level clinical documents** (PDF + C-CDA) — these would contain whatever clinical data is in the encounter note, but there's no specification of what fields or data elements are included
- **Patient demographics** — mentioned as being in the "face sheet" and encounter documents
- **Attachments** — files attached to the patient's chart are included in original format

**Domains likely missing or not addressed** (based on product research showing ChartPath stores):
- **Billing/claims data** — No mention of CPT codes, RVU data, claims, charges, or payments being in the export. ChartPath has a full RCM module (ChartPath RCM and RCM Pro), so billing data is a significant omission if absent from the export.
- **Medication prescriptions** — ChartPath is certified for e-prescribing (a)(2), but the export documentation doesn't mention medication data beyond what might be in C-CDA encounter documents.
- **Problem/diagnosis lists** — Not mentioned explicitly; may be partially captured in C-CDA documents.
- **Screening/assessment scores** — ChartPath stores structured screening data (anxiety, dementia staging, depression, caregiver burden assessments). These specialty-specific scores are unlikely to be fully captured in generic C-CDA documents.
- **Census/multi-facility data** — Patient census and facility assignment data is core to ChartPath's workflow but not mentioned.
- **Orders** — Not mentioned.
- **Implantable device data** — Certified for (a)(14) but not mentioned in export.
- **Care coordination data** — Patient flagging, GUIDE Model data, not mentioned.

The export appears to be structured around **clinical encounter documents** rather than a comprehensive data dump. A C-CDA document for each encounter would capture a subset of clinical data, but C-CDA is a document format — it doesn't naturally express billing records, structured assessment scores, census management data, or many other data types that ChartPath stores.

**Critical ambiguity**: The export says it includes "data from the patient's chart" but doesn't define what "the patient's chart" encompasses. For a LTPAC rounding EHR, the chart likely contains encounter notes, demographics, medications, problems, and allergies. But billing data, structured screening scores, and operational data like census management may or may not be considered part of "the chart."

### Export Format & Standards

- **Format**: ZIP archive containing sub-ZIPs of PDFs, C-CDAs, and attached files
- **Standards**: C-CDA (HL7 Consolidated Clinical Document Architecture) is a recognized standard for clinical document exchange. PDF is a universal document format but not computable for data extraction.
- **FHIR**: The (b)(10) export is **not** FHIR-based. ChartPath has a separate FHIR API for (g)(10), but the EHI export is a document-based approach.
- **Reconstructability**: A third party receiving this export would get human-readable documents (PDFs) and semi-structured clinical documents (C-CDAs). The C-CDA documents could be parsed programmatically, but without knowing what sections and entries are populated, it's impossible to assess completeness. The PDFs would require OCR or manual review to extract structured data.
- **Appropriateness**: For a LTPAC rounding EHR, a document-per-encounter approach is reasonable for clinical notes but inadequate for billing data, structured assessments, and other non-narrative data. A CSV/database export of tables would provide far more complete coverage.

### Documentation Quality

This is among the most minimal EHI export documentation encountered. Seven sentences, no technical detail beyond "it's a ZIP with PDFs and C-CDAs."

- **No data dictionary** — no field-level definitions, no table/column listings
- **No schema** — no C-CDA template specifications, no description of which C-CDA sections are populated
- **No value sets** — no coded field documentation
- **No sample files** — no example export for a developer to reference
- **No user guide** — no instructions on how to initiate or configure the export
- **No screenshots** — no visual documentation of the export interface
- **No API specification** — (the export appears to be UI-driven, not API-based)

A developer attempting to build an import of ChartPath EHI export data would have essentially nothing to work with beyond "expect a ZIP containing PDFs and C-CDAs." They would have to reverse-engineer the structure from an actual export.

### Structure & Completeness

- **Granularity**: Zero. The documentation provides no field-level, table-level, or even section-level detail.
- **Coded fields**: Not documented.
- **Relationships**: Not documented. The ZIP structure (sub-ZIPs for PDFs, C-CDAs, attachments) is the only structural information provided.
- **Versioning**: The copyright says 2023; no version number, no change history.

### (b)(10) vs (g)(10) Assessment

ChartPath has clearly separated their (b)(10) and (g)(10) documentation:
- **(g)(10)**: A 55-page FHIR API document covering US Core resources (Patient, AllergyIntolerance, CarePlan, etc.)
- **(b)(10)**: The minimal EHI export page describing a ZIP/PDF/C-CDA export

This separation is actually positive — they're not conflating the two requirements. However, the (b)(10) documentation is so sparse that it's impossible to assess whether the export actually covers more data than the (g)(10) API. The (g)(10) FHIR API covers standard USCDI clinical data. The (b)(10) export *should* cover everything the product stores, including billing, screening assessments, and specialty clinical data that doesn't fit into US Core. But without a data dictionary or field listing, there's no way to verify this.

## Access Summary
- Final URL (after redirects): https://info.chartpath.com/ehiexport (no redirect)
- Status: found
- Required browser: no (static HTML, fully rendered server-side by HubSpot)
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare, but no challenge presented)

## Obstacles & Dead Ends
- The info.chartpath.com subdomain is a HubSpot marketing site with only the single EHI export page
- The mandatory disclosures page (chartpath.com/2015-cehrt) links back to the same EHI export page via a HubSpot CTA button — no additional EHI documentation
- FHIR API and FHIR OAuth PDFs are available on the CEHRT page but are (g)(10) documentation, not (b)(10) EHI export docs
- No Wayback Machine archives found for the EHI export page
- No additional EHI documentation found via web search
- The HubSpot CTA buttons on the CEHRT page use tracking redirects, making direct curl downloads difficult (though the underlying documents are accessible via the HubSpot Documents viewer)
