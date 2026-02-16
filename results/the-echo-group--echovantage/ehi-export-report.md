# The Echo Group (Ensora Health) — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ensorahealth.com/onc/echo/
- CHPL IDs: 11129
- Product: EchoVantage, Version 3
- Developer: The Echo Group (now part of Ensora Health)
- Certification Date: 2022-12-27

## Navigation Journal

### Step 1: Probe the registered URL
```bash
curl -sI -L "https://ensorahealth.com/onc/echo/" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: text/html; charset=UTF-8. WordPress site on Cloudflare. No redirects.

### Step 2: Fetch and examine the page
```bash
curl -sL "https://ensorahealth.com/onc/echo/" -H 'User-Agent: Mozilla/5.0' -o /tmp/echo-page.html
```
The page is a standard ONC certification compliance page for EchoVantage by Ensora Health. It contains:
- ONC certification details (developer, product, version, certification number)
- Attestation Disclosure listing all certified criteria
- An "Electronic Health Information (EHI) Export" section with a link to a PDF
- A "EchoVantage FHIR API" section (g(10), not b(10))
- An "ONC Real World Testing" section (link to separate page)

### Step 3: Identify EHI export documentation
```bash
grep -oiE 'href="[^"]*"' /tmp/echo-page.html | grep -iE 'ehi|export|data.dictionary|b.10|bulk'
```
Found one link directly relevant to EHI export:
- `https://ensorahealth.com/wp-content/uploads/2025/08/Electronic-Health-Information-Export_EchoVantage.pdf`

The "File Formats" link text points to this PDF.

### Step 4: Download the PDF
```bash
curl -sL "https://ensorahealth.com/wp-content/uploads/2025/08/Electronic-Health-Information-Export_EchoVantage.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/Electronic-Health-Information-Export_EchoVantage.pdf
```
Verified: `file` confirms PDF document, version 1.6. 148,587 bytes, 1 page. Created 2025-08-15 by "Acrobat PDFMaker 25 for Word", author "Catherine Baker".

### Step 5: Examine the PDF
```bash
pdftotext Electronic-Health-Information-Export_EchoVantage.pdf -
```
The single-page PDF titled "Electronic Health Information (EHI) Export" describes file formats for export:

**Single Patient:**
- CCD/C-CDA documents — "will contain data required by the USCDI v1 standards"
- JSON — "a lightweight format for storing and transporting data"
- PDF documents

**Patient Population:**
- .bak file — "a full MSSQL Server database backup of all data for an agency that can be restored"

No embedded URLs or attachments in the PDF (`pdfdetach -list` shows 0 embedded files).

### Step 6: Check adjacent links
The Echo API page (`https://ensorahealth.com/onc/echo/echo-api/`) contains only FHIR API Terms of Use — legal terms for the g(10) certified API. No EHI export documentation.

The FHIR Endpoint listing (`https://ensorahealth.com/onc/echo/fhir/r4/Endpoint`) returns a FHIR Bundle of Endpoint resources listing individual customer FHIR servers (e.g., hamilton.echoehr.com). This is g(10) infrastructure, not b(10) export documentation.

### Step 7: Screenshot
Full-page screenshot taken via browser at `downloads/onc-echo-page-screenshot.png`.

## What Was Found

The EHI export documentation for EchoVantage consists of:

1. **A section on the ONC certification page** describing two export modes:
   - **Single Patient Export**: Users can export EHI for a single patient "without developer assistance" in CCD/C-CDA, JSON, or PDF formats.
   - **Patient Population Export**: All data for a patient population can be exported by "submitting a support ticket via Salesforce." The export format is a `.bak` file — a full MSSQL Server database backup.

2. **A one-page PDF** ("Electronic Health Information Export_EchoVantage.pdf") that lists the same file formats with brief descriptions. This is the entirety of the technical documentation.

The page notes that export content "might vary based on a variety of factors" including software applications in use, software version, documentation practices, configuration decisions, and "the health system including materials not sourced from the application."

There is no data dictionary, no schema documentation, no field-level definitions, no sample exports, no worked examples, and no documentation of what specific data elements are included in the CCD/C-CDA, JSON, or database backup exports.

## Export Coverage Assessment

### Data Domain Coverage

The export documentation describes two fundamentally different approaches:

**Single Patient Export (CCD/C-CDA, JSON, PDF):**
The PDF explicitly states these will "contain data required by the USCDI v1 standards." This is a significant red flag for b(10) completeness. USCDI v1 covers only a defined subset of clinical data (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, clinical notes, goals, assessments, and health concerns). For a behavioral health EHR like EchoVantage, this almost certainly excludes:

- **Treatment plans** — structured behavioral health treatment plans with outcome linkage (a core EchoVantage feature)
- **Assessments** — standardized and custom behavioral health assessment instruments with scored results
- **Billing and claims data** — charges, claims, eligibility, payments, remittances
- **State reporting data** — state-specific mandatory behavioral health reporting datasets
- **Custom clinical forms** — forms built with EchoVantage's Forms Designer
- **Telehealth session records**
- **Substance use recovery-specific data** (SUR)
- **I/DD-specific clinical data**
- **Crisis intervention documentation**
- **Medication Assisted Treatment (MAT) data** (methadone dosing, dispensing)
- **Documents and attachments** beyond what fits in C-CDA
- **Visual Health Record (VHR) timeline data** — EchoVantage's signature feature

The single-patient CCD/C-CDA export appears to be the g(10) clinical summary repackaged as the b(10) export — a classic case of the (b)(10)/(g)(10) confusion described above.

**Patient Population Export (.bak database backup):**
The MSSQL Server `.bak` file is described as "a full MSSQL Server database backup of all data for an agency that can be restored." This is actually a strong b(10) approach — a full database backup would include everything in the system: clinical data, billing, assessments, custom forms, all specialty-specific data. However:

- This export requires submitting a support ticket, not self-service
- There is absolutely no documentation of the database schema — table names, column names, data types, relationships, value sets, or any other structural information
- A recipient would need MSSQL Server to restore the backup and would then need to reverse-engineer the entire schema to understand the data
- There's no indication of what's included or excluded from the backup

### Export Format & Standards

| Export Type | Format | Standard? | Appropriate? |
|---|---|---|---|
| Single Patient (CCD/C-CDA) | C-CDA | HL7 C-CDA | Partially — covers USCDI but not full EHI scope |
| Single Patient (JSON) | JSON | Unspecified | Unknown — no documentation of structure |
| Single Patient (PDF) | PDF | N/A | Renders human-readable record but not computable |
| Population (.bak) | MSSQL .bak | Vendor-proprietary | Complete data but requires MSSQL and schema knowledge |

The JSON format is particularly opaque — is it FHIR JSON? A proprietary JSON schema? The documentation says nothing beyond "JSON is a lightweight format for storing and transporting data." This is a description of the JSON format itself, not of the vendor's JSON export schema.

The .bak file format is effective for completeness but impractical for portability. It requires Microsoft SQL Server and knowledge of the proprietary database schema to be useful.

### Documentation Quality

This is among the most minimal EHI export documentation possible. The entire documentation consists of:
- ~100 words on the ONC certification page
- A 1-page PDF with ~80 words of substance

There are no:
- Data dictionaries
- Schema documentation
- Field definitions
- Sample exports
- Worked examples
- API documentation specific to the export
- User guides for performing the export
- Screenshots of the export interface
- Documentation of what JSON structure is used
- Documentation of which C-CDA sections/templates are populated
- Documentation of the database schema for the .bak backup

A developer receiving any of these export files would have no basis for understanding the data structure from this documentation alone. The C-CDA would be self-describing to some extent (as C-CDA is a standard), but the JSON export and the .bak database backup are completely undocumented.

### Structure & Completeness

- **Granularity**: Format names only. No table names, no field names, no data types, no descriptions, no cardinality.
- **Value sets**: None documented.
- **Relationships**: Not documented.
- **Versioning**: The PDF was created 2025-08-15. No version history or changelog.

### Overall Assessment

EchoVantage's EHI export documentation is a compliance checkbox — the bare minimum required to have something published. The approach has two significant problems:

1. **The single-patient export is actually a USCDI/g(10) clinical summary**, not a comprehensive EHI export. It explicitly limits itself to "data required by the USCDI v1 standards," which for a behavioral health EHR represents a small fraction of the total patient record. Behavioral health-specific data (treatment plans, assessments, custom forms, substance use data, I/DD data, crisis documentation) is where EchoVantage stores its most unique and valuable clinical information, and none of this appears to be covered by the USCDI-scoped export.

2. **The population export is a raw database dump with zero documentation.** While a full MSSQL backup is technically complete, it is practically unusable without schema documentation. This shifts the entire burden of understanding the data to the recipient — who would need to restore the backup, explore hundreds of tables, reverse-engineer relationships, and guess at coded values. This doesn't satisfy the spirit of EHI export, which should enable a recipient to actually understand and use the data.

The vendor appears to have genuinely different approaches for different scopes — structured standards-based export for the USCDI subset, and a raw database dump for "everything else" — but the documentation for both is so thin that neither approach is practically useful to a recipient.

## Access Summary
- Final URL (after redirects): https://ensorahealth.com/onc/echo/
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: one_click (PDF linked directly from the page)
- Anti-bot issues: none (Cloudflare present but not blocking)

## Obstacles & Dead Ends
- None encountered. The page loaded cleanly, the PDF downloaded without issues, and all content was accessible without JavaScript.
- The Echo API page was checked but contains only FHIR API Terms of Use (g(10)), not EHI export documentation.
- The FHIR Endpoint page was checked but is a g(10) endpoint listing.
- No additional EHI export documentation was found anywhere on the site.
