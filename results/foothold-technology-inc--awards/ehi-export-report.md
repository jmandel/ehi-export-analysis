# Foothold Technology, Inc. — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://awards1.zendesk.com/hc/en-us/articles/33133755413012-ExportBuilders
- CHPL ID: 9267 (`15.04.04.1500.AWAR.03.00.1.171220`)
- Product: AWARDS 3.0
- Certification date: 2017-12-20
- Developer: Foothold Technology, Inc. (part of Radicle Health / Alpine Software Group)

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://awards1.zendesk.com/hc/en-us/articles/33133755413012-ExportBuilders" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 200, content-type: text/html; charset=utf-8. Served by Zendesk help center behind Cloudflare.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://awards1.zendesk.com/hc/en-us/articles/33133755413012-ExportBuilders" \
  -H 'User-Agent: Mozilla/5.0' -o exportbuilders-main.html
```
The page is a Zendesk help center article titled "ExportBuilders" (updated June 03, 2025). It is publicly accessible without login. The article is approximately 192KB of HTML (article body ~36KB of text) and contains detailed step-by-step instructions for using the ExportBuilder feature.

### Step 3: Check for downloadable files
```bash
grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json).*"' exportbuilders-main.html
```
No downloadable files (PDF, ZIP, etc.) linked from the article. The page has 4 embedded image attachments, all of which are tiny UI icons (27-44px, used as inline button icons for "add field", "combine", "split", "delete").

### Step 4: Explore the ExportBuilder section
```bash
curl -sL "https://awards1.zendesk.com/hc/en-us/sections/30909683668884-ExportBuilder" -H 'User-Agent: Mozilla/5.0'
```
The ExportBuilder section contains only one article: the ExportBuilders main article.

### Step 5: Search the help center for related content
Searched the Zendesk help center for: "EHI export", "b10 export electronic health information", "ReportBuilder", "data dictionary", "FHIR API", "interoperability", "certification b10", "designated record set".

Key findings from search:
- **"HMIS Data Export"** (article 36276142319380) — publicly accessible, describes HMIS CSV export per HUD specification
- **"ReportBuilder Report Contents"** (article 366712240208) — returns HTTP 403 (login required)
- **"ReportBuilders"** (article 366711613001) — returns HTTP 403 (login required)
- **"Advanced Data Features Available for AWARDS"** (article 331330615182) — returns HTTP 403 (login required)
- **"ReportBuilder Configuration Options"** (article 366712208637) — returns HTTP 403 (login required)
- **"FormBuilder ReportBuilder"** (article 314967007636) — returns HTTP 403 (login required)

The vast majority of the help center articles require authentication. Only the ExportBuilders and HMIS Data Export articles are publicly accessible.

### Step 6: Fetch the HMIS Data Export article
```bash
curl -sL "https://awards1.zendesk.com/hc/en-us/articles/36276142319380-HMIS-Data-Export" \
  -H 'User-Agent: Mozilla/5.0' -o hmis-data-export.html
```
Successfully downloaded (274KB). This article describes the HMIS CSV export feature in detail, including export types, field mapping, and service type configurations.

### Step 7: Check the mandatory disclosures page
Navigated to the mandatory disclosures URL from CHPL metadata: `https://footholdtechnology.com/human-services-software/meaningful-use/`

This page (JavaScript-rendered, viewed in browser) lists:
- Certificate of Compliance PDF
- Mandatory Disclosures PDF (Dec 2024 update)
- Real World Testing Plans/Results (2022-2025)
- **FHIR API documentation** at https://fhir-docs.footholdtechnology.com/
- FHIR API Terms of Use PDF
- Costs and Limitations PDF

### Step 8: Download PDFs from mandatory disclosures
```bash
curl -sL "https://5320565.fs1.hubspotusercontent-na1.net/hubfs/5320565/Cures%20Act%20Mandatory%20Disclosures%20Dec%202024%20update.pdf" \
  -o mandatory-disclosures-dec-2024.pdf
curl -sL "https://footholdtechnology.com/wp-content/uploads/2020/09/MU-2015-Costs-and-Limitations-060520.pdf" \
  -o costs-and-limitations.pdf
```
Both downloaded successfully. The Mandatory Disclosures PDF (7 pages) contains the key (b)(10) description. The Costs and Limitations PDF (4 pages) covers the original 2015 edition criteria.

### Step 9: Examine FHIR API documentation
Navigated to https://fhir-docs.footholdtechnology.com/ in browser. This is a Postman-style API documentation site for the (g)(10) FHIR API. It documents standard US Core FHIR R4 resources:
AllergyIntolerance, CarePlan, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Goal, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, Provenance, ServiceRequest, Specimen.

This is the (g)(10) standardized API documentation, not the (b)(10) EHI export.

## What Was Found

### The (b)(10) EHI Export Mechanism: ExportBuilder

Foothold Technology's approach to (b)(10) EHI export is to point users to the **ExportBuilder** tool — a flexible, user-configurable data export feature built into AWARDS. This is not a one-click "export everything" button. Instead, it is an ad-hoc reporting and export tool that:

1. **Operates through module-specific ReportBuilders** — each AWARDS module (Demographics, Medical, Employment, HMIS, Progress Notes, etc.) has its own ReportBuilder, and the ExportBuilder extends each one with export file generation capabilities.

2. **Supports multiple export formats** — CSV, TXT (fixed-width or delimited), XLS, and XML.

3. **Is fully user-configurable** — users select which data fields to include, set filters, configure field ordering, choose formatting options (date formats, delimiters, boolean values, padding), and can map values during export.

4. **Supports saved export formats** — configurations can be saved and reused, and shared across staff.

5. **Allows sub-exports** — the Demographics ExportBuilder can embed data from other modules (Hospital Episodes, Allergies, Medications, Job Placements, Job Interviews) via XML sub-exports.

6. **Includes FormBuilder custom fields** — custom forms created by agencies via FormBuilder are available as data variables in the corresponding ExportBuilder, provided they were configured for inclusion in ReportBuilders.

7. **Has a 2-year date range limit** per export (except HMIS History ExportBuilder), with recommendation to concatenate multiple exports for longer periods.

8. **Can export for single patients or multiple patients** — supports "Select Client" for single-patient export, "Clients with Records" for matching records, or "All Clients" for full roster.

### The Mandatory Disclosures (b)(10) Statement

From the mandatory disclosures PDF:
> "A user of the Product can perform an electronic health information (EHI) export for a single patient or for multiple patients at any time the user chooses by exporting data via our ExportBuilder tool available for data to which they have access throughout the system and which provides flexibility in the data included and the export format. The export file is created in real-time when the user generates an export and can also be sent or scheduled to run and be delivered to the user's inbox. The file can be in csv, xls or xml format and would be electronic and computable. The data elements included and the export format are highly customizable by the user who has been granted access and saved formats can be saved for quick exports in a predefined format."

### HMIS Data Export (Separate Feature)

A separate "HMIS Data Export" feature exists for exporting HMIS (Homeless Management Information System) data as HUD-compliant zipped CSV files. This is a specialized export for HUD reporting, not the general EHI export. It supports four export types:
- **Full** — complete set of HUD HMIS CSV files
- **HIC** — Housing Inventory Chart data only
- **RHY** — Full set with encrypted PII for Runaway & Homeless Youth repository
- **Full+** — Everything in Full, plus FormBuilder data as additional CSV files and a `ServicesOther.csv` with service contact details

### FHIR API Documentation (g)(10)

The FHIR API docs at fhir-docs.footholdtechnology.com document the (g)(10) standardized API using FHIR R4 with US Core STU 6.1.0 profiles and USCDI v3. It supports Bulk Data Access (Flat FHIR) STU 1. This covers standard clinical data (allergies, conditions, care plans, medications, observations, etc.) but is explicitly for (g)(10) compliance, not (b)(10) EHI export.

## Export Coverage Assessment

### Data Domain Coverage

**What AWARDS stores** (from product research):
AWARDS is a behavioral health and human services EHR with HMIS capabilities. It stores clinical health records, case management/program data, HMIS/housing data (HUD elements), administrative/billing data, custom agency-defined forms, interoperability exchange data, and reporting configurations.

**What the ExportBuilder documentation covers:**
The ExportBuilder documentation describes the *mechanism* for export in great detail — how to configure exports, set formats, apply filters, save configurations. However, it does **not** provide a data dictionary or field listing. The specific data variables available in each ExportBuilder are described as being "based on the ReportBuilder through which you have accessed this ExportBuilder," and the documentation refers users to the individual ReportBuilder instructions for details on available data variables.

**Critical gap: The ReportBuilder documentation is behind a login wall.** The articles that would list the actual data fields available for export — "ReportBuilder Report Contents", "ReportBuilders", "ReportBuilder Configuration Options", "FormBuilder ReportBuilder" — all return HTTP 403 and require Zendesk authentication. Without these, we cannot determine:
- Which specific data fields are available in each module's ExportBuilder
- Whether all data domains (billing, HMIS, custom forms, etc.) have corresponding ExportBuilders
- The complete list of modules that have ExportBuilder support

**What we can infer from the documentation:**
- The Demographics ExportBuilder exists and can embed sub-exports from: Hospital > Episodes, Medical > Allergies, Medical > Medications, Employment > Job Placements, Employment > Job Interviews
- FormBuilder custom fields can be included when configured
- HMIS data has a separate dedicated export (HMIS Data Export) with Full+ mode including FormBuilder fields
- The ExportBuilder is described as available for "data to which they have access throughout the system"
- Progress Notes ExportBuilder exists (mentioned in FormBuilder context)

**Domains with clear coverage:**
- Demographics
- Medical (Allergies, Medications)
- Hospital Episodes
- Employment (Job Placements, Job Interviews)
- HMIS data (via separate HMIS Data Export)
- Custom FormBuilder fields (when configured)
- Progress Notes

**Domains with uncertain coverage:**
- Billing/claims records — no specific mention of a Billing ExportBuilder
- Treatment plans — not explicitly mentioned as having an ExportBuilder
- Lab results — not specifically referenced
- Vital signs — not specifically referenced
- Immunizations — not specifically referenced
- Intake/assessment data — not specifically referenced
- Service documentation — not specifically referenced beyond HMIS context
- Program enrollment/discharge records — not specifically referenced

### Export Format & Standards

The export uses **ad-hoc vendor-specific formats** — CSV, TXT, XLS, or XML with fully user-configurable field selection, ordering, and formatting. There is no use of FHIR, C-CDA, or any other recognized health data standard for the (b)(10) export.

This approach has trade-offs:
- **Pro**: Maximum flexibility — users can export exactly the fields they need in whatever format the receiving system requires
- **Pro**: Covers custom FormBuilder data that wouldn't fit into any standard
- **Con**: No standardized schema — a third party receiving an export would need to understand the specific field selections and mappings used
- **Con**: Requires expert knowledge to set up — the documentation explicitly warns that "The ExportBuilder functionality was designed for use by individuals who are familiar with export files and formats"
- **Con**: No single "export everything" operation — users must navigate multiple module-specific ExportBuilders and configure each one

For reconstructing a complete patient record, a recipient would need multiple export files from different ExportBuilders, each with different configurations, and no formal schema to tie them together. The XML sub-export feature for Demographics helps somewhat by allowing embedding of related module data.

### Documentation Quality

**Strengths:**
- The ExportBuilder article is detailed and well-written (36KB of instructional text)
- Step-by-step workflow is clearly documented with numbered steps
- FAQ section addresses common questions
- Export format options (CSV/TXT/XLS/XML) are well-described with a comparison table
- Sub-export and field mapping functionality is thoroughly explained

**Weaknesses:**
- **No data dictionary** — the documentation describes the tool but not the data. There is no listing of available fields, data types, value sets, or table relationships.
- **No sample export files** — no examples of what an actual export looks like
- **No schema or format specification** — beyond the generic CSV/XML type options
- **Key reference documentation is behind a login wall** — the ReportBuilder articles that would list available data fields are not publicly accessible
- **No guidance on performing a complete EHI export** — no documentation of which ExportBuilders to use, in what combination, to export all of a patient's electronic health information
- **The documentation is for a general-purpose export tool, not specifically an EHI export process** — it reads as generic product help documentation that has been pointed to by the CHPL registration

### Structure & Completeness

The documentation describes the export *mechanism* at a procedural level (how to click through the UI) but provides essentially zero information about the data *content*:
- No table/entity definitions
- No field-level specifications
- No data types beyond the generic format options (Text, Numeric, Date, Time, Yes/No, List, Phone)
- No value sets or coded field documentation
- No relationship documentation between entities
- No versioning or change history for the data model

The sole exception is the HMIS Data Export, which references the external HUD HMIS CSV specification at hudhdx.info/VendorResources.aspx — but that's a HUD standard, not Foothold's documentation of their own data.

## Access Summary
- Registered URL: https://awards1.zendesk.com/hc/en-us/articles/33133755413012-ExportBuilders
- Final URL (after redirects): Same (no redirects)
- Status: found
- Required browser: No (curl works for the registered URL)
- Navigation complexity: direct_link (for the registered article), but related documentation is behind login wall
- Anti-bot issues: Cloudflare present but not blocking; User-Agent header recommended

## Obstacles & Dead Ends

1. **Login-walled ReportBuilder documentation** — The most critical documentation gap. The articles that would list available data fields and export options for each module (ReportBuilder Report Contents, ReportBuilders overview, FormBuilder ReportBuilder, etc.) all return HTTP 403 and require Zendesk authentication. This means the publicly registered URL provides the export *tool* documentation but not the export *content* documentation.

2. **Help center home and most sections require sign-in** — The Zendesk help center at awards1.zendesk.com appears to be largely restricted. Searching for "data dictionary", "FHIR API", "interoperability", and other terms yielded no results, suggesting most content is only visible to authenticated users.

3. **No downloadable artifacts** — Neither the ExportBuilders article nor the HMIS Data Export article links to any downloadable files (no PDFs, CSVs, ZIPs, schemas, or sample exports).

4. **Small icon images only** — The 4 embedded images in the ExportBuilders article are tiny UI button icons (27-44px), not screenshots of the export interface.

5. **FHIR API docs are (g)(10) only** — The FHIR API documentation site is explicitly for the standardized (g)(10) API and covers only US Core/USCDI resources, not the broader EHI export.
