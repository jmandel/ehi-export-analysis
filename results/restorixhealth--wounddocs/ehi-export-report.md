# Net Health (RestorixHealth) — WoundDocs/WoundExpert — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/
- CHPL IDs: 10234
- Developer: Net Health (product branded as "WoundDocs" by RestorixHealth; underlying software is WoundExpert v7.0)
- Mandatory Disclosures URL: https://www.nethealth.com/drummond-certified-page-woundexpert/ (identical content to registered URL)

## Navigation Journal

### Step 1: Initial probe of registered URL
```bash
curl -sI -L "https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 200, `text/html; charset=UTF-8`, WordPress site behind Cloudflare CDN. No redirects.

### Step 2: Fetched and examined page content
The page is a WordPress page (page ID 948). The raw HTML is ~400KB but most is theme/JS boilerplate. The meaningful content was extracted by rendering in browser and taking a snapshot. The page title is "ONC Certified: Net Health® WoundExpert".

### Step 3: Identified EHI Export section on registered URL
The page contains a clearly labeled **"Electronic Health Information Export"** section that describes the b(10) export mechanism. Key text:

> "Single patient and patient population electronic health information can be exported in the form of an 'export zip' file which contains files in a machine-readable format in accordance with §170.315(b)(10) – Electronic Health Information export of the ONC 2015 Edition Cures Update Certification Criteria."

> "The content and format of the data contained within the export zip file depending on number of patients selected and software functionality in use."

> "The EHI Export zipped folder contains a folder for each patient that contains:
> - csv files of EHI data
> - all image files from the patient record
> - all custom scans on file
> - EHIDataExtract_DataDictionary.xlsx
> - ExportSummary.txt"

### Step 4: Checked sidebar links
The page links to:
1. **WoundExpert Regulatory Compliance** (https://www.nethealth.com/regulatorycompliancewithwoundexpertemr/) — about MACRA/MIPS, ICD-10, Joint Commission, EPCS. No EHI export content.
2. **Real World Testing Plans and Results** (https://www.nethealth.com/real-world-testing/) — contains downloadable PDFs with b(10) testing details.
3. **WoundExpert FHIR API documentation** (https://www.nethealth.com/fhir-api-specifications/) — about the g(10) FHIR API via Darena Health partnership. Not the b(10) EHI export.
4. **Data and AI Governance Plan** — not relevant to EHI export.
5. **Darena Health Technical Documentation** (https://docs.darena.health/) — Postman-hosted FHIR API docs for g(10); not the b(10) export.

### Step 5: Checked mandatory disclosures page
```bash
curl -sL "https://www.nethealth.com/drummond-certified-page-woundexpert/" ...
```
Identical content to the registered URL (same HTML, same text). Both URLs serve the same page.

### Step 6: Examined FHIR API / Darena Health docs
- The FHIR API specs page describes the FHIR R4 API based on HL7 US Core IG STU 4.0.0, satisfying g(10) requirements, operated in partnership with Darena Health (formerly MeldRx).
- docs.darena.health is a Postman documenter with sections: Getting Started, Workspace Permissions, HTI-1 (g10 & b11), MIPS API, FHIR to MIPS, Developer Account, FHIR API.
- **None of this is the b(10) EHI export.** The FHIR API is a separate system from the CSV/ZIP export described on the registered URL.

### Step 7: Downloaded Real World Testing PDFs
From https://www.nethealth.com/real-world-testing/:
```bash
curl -sL "https://www.nethealth.com/wp-content/uploads/2026/01/Real-World-Testing-Results-2025.pdf" -o Real-World-Testing-Results-2025.pdf
curl -sL "https://www.nethealth.com/wp-content/uploads/2026/01/Net-Health-Real-World-Testing-Plan-2026-FINAL.pdf" -o Real-World-Testing-Plan-2026.pdf
```
The 2026 RWT Plan (18 pages) contains **Measure 8: Electronic Health Record Export** with the most detailed description of the b(10) export mechanism found anywhere in the publicly available documentation.

### Step 8: Searched for downloadable data dictionary
The page mentions `EHIDataExtract_DataDictionary.xlsx` as a file included in every export ZIP, but this file is **not publicly downloadable** from the website. Searched:
- WordPress media library API (returned empty/restricted)
- Common wp-content/uploads paths for the .xlsx file (all 404)
- Google: `site:nethealth.com "EHIDataExtract_DataDictionary"` — only returns the registered URL page
- WordPress sitemap — no EHI-specific pages beyond what was already found

The data dictionary exists only within actual export outputs, not as a standalone public download.

## What Was Found

### Export Mechanism (from registered URL + 2026 RWT Plan)
Net Health WoundExpert has built a **proprietary data export tool** (not FHIR-based) for b(10) compliance. The export produces a **ZIP file** with the following structure:

```
export.zip/
  PatientFolder1/
    *.csv                          — CSV files of EHI data
    *.jpg, *.png, etc.            — All image files from patient record
    [custom scans]                — All custom scans on file
    EHIDataExtract_DataDictionary.xlsx  — Data dictionary
    ExportSummary.txt             — Export summary
  PatientFolder2/
    ...
```

**Two export modes exist:**
1. **Facility Administrator role**: Can generate and download a CDA file containing relevant treatment information for one or more patients in a specific date and time range.
2. **Net Health Administrator role**: Can execute full facility EHI exports that include patient medical records in PDF format and all EHI in CSV files.

The content and format vary depending on the number of patients selected and the software functionality in use at the facility.

### Export Format
- **Primary data format**: CSV files (machine-readable)
- **Images**: All wound images and clinical photographs from the patient record
- **Custom scans**: All scanned documents on file
- **Data dictionary**: `EHIDataExtract_DataDictionary.xlsx` — an Excel spreadsheet included in every export ZIP that documents the CSV file contents
- **Summary**: `ExportSummary.txt` — plain text summary of the export
- **Separate from the FHIR API**: The b(10) export is a standalone, internal tool. The FHIR API (via Darena Health) serves the g(10) requirements.

### What Is NOT Documented Publicly
- The **data dictionary itself** is not available for public download — only within actual exports
- No **sample export files** or example data are provided
- No **field-level documentation** describing what the CSV columns contain
- No **list of CSV file names** or entity types that are exported
- No **schema files** (no JSON Schema, XSD, or similar)
- No **documentation of relationships** between CSV files

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, WoundExpert stores extensive wound care-specific clinical data. The registered URL describes the export as containing "csv files of EHI data" plus images and scans. The 2026 RWT plan says the full EHI export includes "patient medical records in PDF format and all EHI in CSV files."

**Likely covered** (based on the "all EHI" claim + CSV format):
- Patient demographics
- Wound assessment data (measurements, tissue types, exudate, etc.)
- Treatment plans
- Progress notes / clinical documentation
- Medications (wound care-related)
- Diagnoses / ICD-10 codes
- Procedures (debridement, NPWT, HBOT, etc.)
- Lab/diagnostic results
- Allergies
- Billing/claims data (CPT codes, charges)

**Likely covered via images/scans**:
- Wound photographs (the export explicitly includes "all image files")
- Custom scans (explicitly included)

**Cannot be confirmed** (the documentation doesn't specify):
- Whether scheduling/appointment data is included (though not strictly EHI)
- Whether all clinical note types are exported or just summaries
- Whether billing detail (line items, payments, denials) is included vs. just coding
- Whether referral information is included
- Whether care plan goals and outcomes are included
- The exact scope of "all EHI" — without seeing the data dictionary, we can't verify what tables/entities are actually exported

The phrase "all EHI in CSV files" is encouraging — it suggests the vendor intends a comprehensive database-level export rather than just a USCDI clinical summary. However, there is no public documentation to verify this claim.

### Export Format & Standards
- **Format**: CSV files in a ZIP archive — a reasonable, practical choice for a specialty EHR
- **Not FHIR-based**: The b(10) export is correctly distinguished from the g(10) FHIR API. This is appropriate — CSV is a better fit for bulk EHI export of a specialty system's complete data than trying to map everything to FHIR resources
- **Images included**: The explicit inclusion of all patient images and scans is a strong positive for a wound care system where clinical photographs are core data
- **Data dictionary bundled**: Including `EHIDataExtract_DataDictionary.xlsx` with every export is a good practice — it means the export is self-describing
- **Interoperability concern**: CSV format with a bundled data dictionary means a receiving system would need to parse the data dictionary to understand the export. There are no standard CSV schemas or formal relationship definitions

### Documentation Quality
The documentation is **minimal but honest**. The registered URL provides:
- A clear description of the export format (ZIP containing CSV + images + data dictionary)
- Explicit reference to §170.315(b)(10)
- The fact that the export supports both single-patient and population-level exports

However, the documentation **lacks**:
- **No public data dictionary**: The `EHIDataExtract_DataDictionary.xlsx` file that documents the CSV contents is only available inside actual exports. A developer trying to build an import tool would need to obtain an actual export first.
- **No field-level documentation**: There is no description of what CSV files are included, what columns they contain, what data types are used, or what coded values mean.
- **No sample data**: No example export files are provided.
- **No export instructions**: No user guide or screenshots showing how to initiate an export. The 2026 RWT plan reveals that exports require a "Facility Administrator" or "Net Health Administrator" role, but this is not on the registered URL.
- **No format specification**: Beyond "CSV files" and "images," there is no specification of encoding, delimiters, date formats, null handling, etc.

A developer could not implement an import of this data based solely on the public documentation. They would need to obtain an actual export ZIP to understand the structure.

### Structure & Completeness
- **Granularity**: Table-level only (we know the export contains "CSV files" but not what tables/entities)
- **Field definitions**: Not publicly available (only in the bundled .xlsx)
- **Value sets/coded fields**: Not documented publicly
- **Relationships**: Not documented publicly
- **Versioning**: No change history or version documentation for the export format

### The b(10) vs g(10) Distinction
Net Health handles this **correctly and clearly**. The b(10) EHI export (CSV/ZIP with data dictionary) is described on the registered URL as a separate mechanism from the FHIR API (g(10)), which is operated through the Darena Health partnership. The FHIR API page explicitly describes itself as satisfying "United States Core Data for Interoperability requirements" (USCDI), while the EHI export page explicitly references §170.315(b)(10). These are kept as distinct systems, which is appropriate.

The 2025 RWT results show that b(10) metrics ("Data Export") were struck through (dropped per Executive Order 14192), while g(10) metrics ("Data Requests" and "Patient Selection") were reported. The 2026 RWT plan includes b(10) as Measure 8 with specific milestones.

## Access Summary
- Final URL (after redirects): https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/
- Status: found
- Required browser: no (content visible in HTML, though rendered better in browser due to WordPress/JS)
- Navigation complexity: direct_link (EHI export section is on the registered URL page itself)
- Anti-bot issues: Cloudflare CDN present, but standard User-Agent header was sufficient

## Obstacles & Dead Ends
- The mandatory disclosures URL (https://www.nethealth.com/drummond-certified-page-woundexpert/) is identical to the registered URL — same page, different slug
- WordPress REST API for media (`/wp-json/wp/v2/media`) returned empty responses — media library is restricted
- The `EHIDataExtract_DataDictionary.xlsx` file is not hosted anywhere on the public website — it exists only within actual export ZIPs
- docs.darena.health is a Postman documenter for the FHIR API (g(10)), not the EHI export (b(10))
- The FHIR API page links to the Darena Health App & Extension Marketplace (https://app.meldrx.com/marketplace) for developer onboarding — this is for the standardized API, not the EHI export
- The 2025 RWT results dropped the "Data Export" metric (b(10)) mid-year per Executive Order 14192, so there are no real-world testing results for the EHI export function
