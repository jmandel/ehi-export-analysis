# Office Practicum — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.officepracticum.com/op/population-health/onc-certification#onccert
- Mandatory Disclosures URL: https://www.officepracticum.com/onc-certification-info
- CHPL ID: 11049
- Certificate: 15.04.04.3048.Offi.21.02.1.221121
- Certification Date: 2022-11-21

## Navigation Journal

### Step 1: Probe registered URL
```bash
curl -sI -L "https://www.officepracticum.com/op/population-health/onc-certification#onccert" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
HTTP 200, Content-Type: text/html. Page loads successfully with Cloudflare CDN. The `#onccert` anchor is a named anchor that scrolls to the "Mandatory Disclosure/Price Transparency" section.

### Step 2: Examine registered URL page
```bash
curl -sL "https://www.officepracticum.com/op/population-health/onc-certification" \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/op-page.html
```
406KB WordPress page. The `#onccert` anchor at line 1156 scrolls to a section with certification information. At lines 1292–1299, there is a section titled **"Electronic Health Information Export"** containing the full extent of the EHI export documentation on this page:

> **Single Patient Export**
> Office Practicum allows a user to export electronic health information (EHI) for a single patient at any time via a Database Viewer stored SQL query built into OP named "Single patient EHI export" without developer assistance. The exported files are in .csv file format explained below
>
> **Multi-Patient Export**
> Office Practicum can export all the data for a patient population in .csv file format explained below:
>
> **CSV**
> A comma-separated values (CSV) file is a delimited text file that uses a comma to separate values. Each line of the file is a data record. Each record consists of one or more fields, separated by commas. The use of the comma as a field separator is the source of the name for this file format.

No links to any data dictionary, schema, table/field definitions, sample data, or any other technical documentation. No downloadable files.

### Step 3: Examine mandatory disclosures page
```bash
curl -sL "https://www.officepracticum.com/onc-certification-info" \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/op-disclosures.html
```
414KB page at the mandatory disclosures URL. Contains five accordion sections:
1. Mandatory Disclosure
2. Price Transparency
3. Costs and Limitations
4. 21st Century Cures Act
5. **Electronic Health Information Export** — contains the exact same text as the registered URL

Expanded the "Electronic Health Information Export" accordion in the browser (JavaScript click required). Content is identical to the registered URL.

### Step 4: Download 2025 Real World Test Results
```bash
curl -sL "https://hub.officepracticum.com/hubfs/OP%20Website/OP_RWT_Results_Report_2025.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/OP_RWT_Results_Report_2025.pdf
```
10-page PDF. Page 3 lists §170.315(b)(10) Electronic Health Information Export under "Care Coordination" measures. Page 7 contains the EHI Export results section:

- Reporting Results Time Frame: Q42025
- Testing Methodology: Logging
- Number of Practices for Interactive Test: up to 5 practices
- Functional testing was conducted with five different practices
- **Single Patient EHI Exports: 2,861**
- **Bulk EHI Exports: 20**
- Key Findings: "There has been a significant increase in utilization of this feature since last year. Satisfaction is high. This functionality is working as expected."
- No action needed; no areas of improvement identified.

The RWT results confirm the feature exists and is used in production, but provide no technical details about the export contents (tables, fields, data types, etc.).

### Step 5: Search for additional documentation
- `grep` of all HTML pages for "data dictionary", "schema", "table", "field", "column" — no EHI-relevant hits
- Web search: `site:officepracticum.com EHI export data dictionary` — only returned the ONC certification page
- Web search: `"office practicum" "EHI export" documentation tables` — no Office Practicum results
- Probed common paths: `/ehi`, `/ehi-export`, `/ehi-documentation`, `/b10`, `/api-docs`, `/developer`, `/docs` — all 404
- Checked `/interoperability/` (redirects to Connectivity page) — no EHI export content
- Checked `/drummond-certification` — no EHI export content
- Checked `/api-terms-of-use/` — no EHI export content
- Searched `site:hub.officepracticum.com EHI export` — no results
- Checked Wayback Machine for historical versions — no additional documentation found

**No additional EHI export documentation exists on the public web for Office Practicum.**

## What Was Found

Office Practicum's entire publicly available EHI export documentation consists of **three short paragraphs** totaling approximately 100 words. The documentation describes:

1. **Export mechanism**: A "Database Viewer stored SQL query built into OP named 'Single patient EHI export'" — this is a pre-built SQL query that users can run without developer assistance.

2. **Export format**: CSV (comma-separated values).

3. **Export scope**: Single patient export (on demand) and multi-patient/population export.

That is the entirety of the documentation. There is:
- **No data dictionary** — no list of tables, fields, data types, or descriptions
- **No schema documentation** — no entity-relationship diagrams, no table definitions
- **No sample data** — no example CSV files showing what the output looks like
- **No field-level specifications** — no information about what columns appear in the CSV, what values they contain, what encoding is used
- **No export instructions** — beyond the name of the SQL query, no step-by-step guide
- **No information about what data is included** — no list of clinical domains, no mapping to EHI requirements
- **No API documentation** — the export is via a built-in SQL query, not an API

The Real World Testing results (2025) confirm the feature is functional and used (2,861 single-patient exports, 20 bulk exports across 5 test practices), but add no technical detail about the export contents.

## Export Coverage Assessment

### Data Domain Coverage

**It is impossible to assess data domain coverage because the documentation does not describe what data is exported.** The documentation says the export produces CSV files via a "Database Viewer stored SQL query" but never specifies which tables or fields are included.

Based on the product research, Office Practicum stores extensive pediatric-specific data including:
- Patient demographics (including family/guardian relationships)
- Clinical documentation (SOAP notes, sick visit templates, preventive exams)
- Growth and development data (growth charts, developmental assessments)
- Immunization records (VacLogic forecasting data)
- Behavioral health screenings (PHQ-9, GAD-7 scores)
- Medications and prescriptions (including EPCS)
- Allergies
- Lab orders and results
- Billing and claims data (superbill charges, claims, payments, denials)
- Scheduling data
- Scanned documents
- Referrals
- School and camp forms (175+ templates)
- Insurance and eligibility data

**None of these domains are explicitly confirmed or denied in the export documentation.** The phrase "export electronic health information (EHI) for a single patient" and "export all the data for a patient population" *implies* comprehensive coverage, but without a data dictionary or table listing, there is no way to verify this claim.

The mention of a "Database Viewer stored SQL query" is the most informative detail — it suggests the export runs directly against the database, which *could* mean comprehensive coverage. But without seeing the query or its output schema, this remains speculative.

### Export Format & Standards

- **Format**: CSV
- **Standard**: None — this is an ad-hoc vendor format with no schema definition
- **FHIR**: Not used for EHI export (FHIR API is separate, for g(10) compliance)
- **Relationships**: Unknown — CSV files do not inherently express relationships between entities. No documentation exists about whether the export produces one CSV or many, how they relate to each other, or whether foreign keys/identifiers link records across files.
- **Reconstruction feasibility**: **Unknown.** Without knowing what tables and fields are exported, it is impossible to assess whether a third party could reconstruct the patient record from the export.

The use of CSV from a "Database Viewer stored SQL query" suggests the export may be relatively raw database output, which could actually be more comprehensive than a polished FHIR-based export — but this is speculation due to the total absence of documentation.

### Documentation Quality

**Critically deficient.** This is among the most minimal EHI export documentation possible while still technically existing:

- **No data dictionary**: Zero field-level documentation
- **No table definitions**: Not even a list of table names
- **No data types or value sets**: Nothing about what values fields can contain
- **No examples**: No sample output files
- **No instructions**: Beyond naming the SQL query, no step-by-step guide
- **No developer guidance**: A developer receiving this export would have no documentation to work from
- **Generic filler text**: The "CSV" paragraph literally just defines what a CSV file is — this is padding, not documentation

A developer tasked with importing data from this export would be working completely blind. They would receive CSV files with column headers and would need to reverse-engineer the meaning of every field.

### Structure & Completeness

- **Granularity**: Zero — not even table names are documented
- **Coded fields**: Not documented
- **Relationships**: Not documented
- **Versioning**: None
- **Change history**: None

### Overall Assessment

Office Practicum has implemented an EHI export feature that appears to be functional and actively used (per RWT results showing thousands of exports). The export mechanism — a pre-built SQL query accessible through a "Database Viewer" — suggests it may provide comprehensive database-level access to patient data.

However, the public documentation is essentially non-existent. The three paragraphs on the certification page tell a reader:
1. The export exists
2. It produces CSV files
3. There is a single-patient and multi-patient mode

Nothing else. This represents a serious documentation gap. The 170.315(b)(10) certification criterion requires that EHI export documentation be publicly accessible. While the *existence* of the export is documented, the *content* of the export — what data it includes, in what structure — is not documented at all.

This is not a case of (b)(10) vs. (g)(10) confusion — Office Practicum does not appear to be conflating their FHIR API with their EHI export. The EHI export is clearly a separate, database-level CSV export. The problem is simply that they have not documented what the export contains.

## Access Summary
- Final URL (after redirects): https://www.officepracticum.com/op/population-health/onc-certification#onccert
- Mandatory Disclosures URL: https://www.officepracticum.com/onc-certification-info (same content in accordion)
- Status: found
- Required browser: yes (accordion expansion requires JavaScript click on disclosures page; registered URL shows content without expansion)
- Navigation complexity: direct_link (registered URL) / accordion (disclosures page)
- Anti-bot issues: none (Cloudflare CDN but no blocking)

## Obstacles & Dead Ends
- The registered URL and mandatory disclosures URL are different pages but contain identical EHI export text
- The disclosures page requires JavaScript to expand the accordion; the registered URL displays the content inline
- No downloadable files exist — the entire documentation is inline HTML text
- pdftotext failed to extract text from the RWT PDF (image-based PDF), but visual reading confirmed the content
- All alternative paths explored (interoperability page, drummond certification page, API terms, common URL patterns) led to no additional EHI export documentation
- The OP Support Hub (officepracticum.my.site.com) requires login — any EHI export documentation behind the login wall would not be publicly accessible as required
