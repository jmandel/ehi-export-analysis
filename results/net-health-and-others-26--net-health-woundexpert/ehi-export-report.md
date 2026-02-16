# Net Health / RestorixHealth — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/
- CHPL IDs: 9836 (Net Health WoundExpert v7.0), 10234 (WoundDocs v7.0)
- Mandatory Disclosures URL: https://www.nethealth.com/drummond-certified-page-woundexpert/ (301 redirects to registered URL)

## Navigation Journal

1. **Probed the registered URL:**
   ```bash
   curl -sI -L "https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'
   ```
   Result: HTTP 200, `text/html`, WordPress page served via Cloudflare. No redirects.

2. **Downloaded the full page HTML** (399,282 bytes). Searched for downloadable files:
   ```bash
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/nethealth-page.html
   ```
   Result: No downloadable file links found on the page at all — no PDFs, no ZIPs, no XLSXs.

3. **Searched for EHI-related links:**
   ```bash
   grep -oiE 'href="[^"]*"' /tmp/nethealth-page.html | grep -iE 'ehi|export|data.dictionary|b.10|bulk'
   ```
   Result: No external EHI-specific links found. All EHI export documentation is inline on the page.

4. **Extracted the EHI export section** from the page HTML (line 1404 of source). The section is titled "Electronic Health Information Export" and describes the export format.

5. **Checked linked pages for additional EHI content:**
   - `https://www.nethealth.com/fhir-api-specifications/` — This is the (g)(10) FHIR API page for USCDI/US Core data via Darena Health partnership. Contains no EHI export (b)(10) information.
   - `https://www.nethealth.com/regulatorycompliancewithwoundexpertemr/` — Regulatory compliance page. Contains no EHI-specific content.
   - `https://docs.darena.health/` — Darena Health FHIR server docs. This is the third-party FHIR API, not the EHI export.

6. **Searched for publicly downloadable EHI data dictionary:**
   ```bash
   curl -sI "https://www.nethealth.com/wp-content/uploads/EHIDataExtract_DataDictionary.xlsx"
   ```
   Result: 404. The data dictionary is only included inside the export ZIP, not publicly downloadable.

7. **Searched WordPress REST API** for additional EHI pages or media:
   ```bash
   curl -sL "https://www.nethealth.com/wp-json/wp/v2/pages?search=ehi&per_page=10"
   curl -sL "https://www.nethealth.com/wp-json/wp/v2/media?search=EHI&per_page=10"
   ```
   Result: No EHI-related pages or media files found.

8. **Tried common documentation paths** (`/ehi/`, `/ehi-export/`, `/data-dictionary/`, `/b10/`, etc.) — all returned 404.

9. **Took full-page screenshot** of the certification page and saved page HTML and clean text extraction.

## What Was Found

The EHI export documentation for Net Health WoundExpert consists entirely of a brief inline description on the ONC certification page. There are no downloadable artifacts — no PDF, no data dictionary, no schema, no sample exports, no user guide.

### The EHI Export Description

The page states:

> Single patient and patient population electronic health information can be exported in the form of an "export zip" file which contains files in a machine-readable format in accordance with §170.315(b)(10) – Electronic Health Information export of the ONC 2015 Edition Cures Update Certification Criteria.

> The content and format of the data contained within the export zip file depending on number of patients selected and software functionality in use.

### Export Format

The export is described as a ZIP file containing one folder per patient, with:

1. **CSV files** of EHI data
2. **Image files** from the patient record
3. **Custom scans** on file
4. **EHIDataExtract_DataDictionary.xlsx** — an Excel data dictionary
5. **ExportSummary.txt** — an export summary

This is a proper (b)(10) approach — CSV-based bulk export of all EHI data, not a FHIR API repackaging. The format is straightforward and appropriate for a specialty wound care system. However, the public documentation tells us almost nothing about what data is actually in those CSVs.

### What's NOT Documented Publicly

- **Which CSV files are included** — no list of table/file names
- **What columns each CSV contains** — no field definitions
- **What data types are used** — no type information
- **What coded values mean** — no value set documentation
- **How relationships between CSVs are expressed** — no foreign key documentation
- **What the data dictionary XLSX actually contains** — only that it exists
- **How to perform the export** — no user instructions or screenshots
- **Whether the export is complete** — no statement on which data domains are included

The data dictionary (EHIDataExtract_DataDictionary.xlsx) is bundled inside the export itself — meaning you can only see the documentation after you've already obtained an export. It is not publicly downloadable.

### FHIR API (Separate from EHI Export)

Net Health also has a separate FHIR R4 API certified under (g)(10), provided through partnership with Darena Health. This API supports USCDI v3 data classes and is documented at `https://docs.darena.health/`. This is a completely separate mechanism from the (b)(10) EHI export and covers only the standard USCDI subset of clinical data. The certification page correctly distinguishes between the two.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, WoundExpert stores the following clinical and billing data domains:

| Domain | Covered by Export? | Evidence |
|--------|-------------------|----------|
| Patient demographics | Unknown | Not documented |
| Wound assessments (size, depth, tissue type, location, etiology) | Unknown | Not documented — this is the CORE data for a wound care EHR |
| Wound photographs and measurements | Likely yes | "all image files from the patient record" |
| Treatment plans | Unknown | Not documented |
| Progress notes / clinical documentation | Unknown | Not documented |
| Medication data | Unknown | Not documented |
| Lab/diagnostic imaging orders & results | Unknown | Not documented |
| Problem lists, medication lists, allergy lists | Unknown | Not documented |
| Family health history | Unknown | Not documented |
| Implantable device list | Unknown | Not documented |
| Billing and financial data | Unknown | Not documented |
| Scheduling/appointment data | Unknown | Not documented |
| Transitions of care documents (C-CDAs) | Unknown | Not documented |
| Hyperbaric oxygen therapy records | Unknown | Not documented |
| Custom scans | Likely yes | "all custom scans on file" |
| Clinical quality measure data | Unknown | Not documented |

The documentation says "csv files of EHI data" without specifying which data. The phrase "content and format ... depending on ... software functionality in use" suggests the CSV contents may vary by which modules a facility uses, but no specifics are given. This makes independent coverage assessment impossible from the public documentation alone.

### Export Format & Standards

- **Format:** ZIP containing CSV files + images + XLSX data dictionary + TXT summary
- **Standard:** Ad-hoc vendor format (CSV), which is appropriate for (b)(10) — no requirement for FHIR or any standard
- **Strengths:**
  - CSV is universally readable
  - Including a data dictionary XLSX in each export is thoughtful — it provides self-documenting exports
  - Including all images and custom scans shows awareness of non-structured data
  - Supporting both single-patient and population exports is correct per the regulation
- **Weaknesses:**
  - No public documentation of the CSV structure means no one can prepare to receive or process these exports in advance
  - Relationships between CSV files are undocumented
  - No sample export data available

### Documentation Quality

**Very poor.** The public EHI export documentation is approximately 100 words — two short paragraphs on a certification page. This is among the most minimal (b)(10) documentation possible while still technically acknowledging the requirement exists.

Specific gaps:
- No data dictionary (the one in the export is not publicly accessible)
- No field definitions, data types, or cardinality
- No value set documentation
- No sample export files
- No export instructions or user guide
- No screenshots of the export interface
- No API specification (the export is not API-based)
- No worked examples

A developer could not implement an import of this data based on the public documentation. They would need to obtain an actual export and reverse-engineer the CSV structure from the bundled data dictionary.

### Structure & Completeness

The documentation mentions that the export exists and describes what container types are in it (CSVs, images, scans, a data dictionary, a summary). That's it. There is zero granularity beyond this — no table names, no field names, no data types, no relationships, no value sets.

The one positive structural element is the mention of `EHIDataExtract_DataDictionary.xlsx` — this suggests Net Health has actually built a data dictionary, just not published it publicly. The export may be quite well-documented for those who have access to it.

### Overall Assessment

Net Health has taken the correct architectural approach to (b)(10) compliance: a CSV-based bulk export of all EHI data with an embedded data dictionary, rather than trying to shoehorn everything through their FHIR API (which they correctly treat as a separate (g)(10) mechanism). The inclusion of images, custom scans, and a per-export data dictionary shows genuine thought about what a complete export should contain.

However, the public-facing documentation is functionally nonexistent. The certification page provides just enough information to confirm that the capability exists and that it uses CSVs, but nowhere near enough for a recipient to prepare for, validate, or process an export. The data dictionary — arguably the most important artifact — is locked inside the export itself and not publicly available.

This is a common pattern for specialty EHR vendors: the actual (b)(10) implementation may be solid, but the public documentation consists of a single paragraph on a certification page. For WoundExpert specifically, this is a missed opportunity — wound care data has specialized structures (wound measurements, tissue types, healing trajectories) that would benefit from clear documentation to enable data portability between wound care systems.

## Access Summary
- Final URL (after redirects): https://www.nethealth.com/drummond-certified-for-meaningful-use-woundexpert/
- Status: found
- Required browser: no (page is static HTML served by WordPress)
- Navigation complexity: direct_link (EHI export section is inline on the page, no clicks needed)
- Anti-bot issues: Cloudflare present but no blocking observed with standard User-Agent

## Obstacles & Dead Ends
- No downloadable files (PDF, XLSX, CSV, ZIP) linked from the certification page
- Data dictionary (EHIDataExtract_DataDictionary.xlsx) exists only inside export ZIPs, not publicly hosted
- WordPress REST API search for "EHI" returned no additional pages or media
- Common documentation paths (/ehi/, /ehi-export/, /data-dictionary/, etc.) all 404
- The FHIR API documentation (via Darena Health) is for (g)(10), not (b)(10)
- Mandatory disclosures URL redirects to the same certification page
