# Practice EHR LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.practiceehr.com/data-export
- CHPL IDs: 10923
- Product: Practice EHR V12 (certified 2022-06-28)

## Navigation Journal

1. **Initial probe:** `curl -sI -L "https://www.practiceehr.com/data-export" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200 with `Content-Type: text/html`. The page is hosted on HubSpot CMS behind Cloudflare CDN.

2. **Fetched page:** `curl -sL "https://www.practiceehr.com/data-export" -o /tmp/page.html` — 62,235 bytes of HTML. The page is extremely simple: a "Data Export" banner heading followed by a single link.

3. **Searched for download links:** `grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json)...' /tmp/page.html` found one PDF link:
   ```
   https://www.practiceehr.com/hubfs/PracticeEHR-2023/Practice%20EHR%20B10-Electronic%20Health%20Information%20Export.pdf
   ```

4. **Downloaded the PDF:**
   ```bash
   curl -sL "https://www.practiceehr.com/hubfs/PracticeEHR-2023/Practice%20EHR%20B10-Electronic%20Health%20Information%20Export.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o Practice-EHR-B10-Electronic-Health-Information-Export.pdf
   ```
   Verified with `file`: "PDF document, version 1.7, 4 page(s)". 116,552 bytes.

5. **Examined the PDF** with `pdftotext` and `pdftoppm` to render all pages. The document is 4 pages (cover page + 3 pages of content), created with Microsoft Word for Microsoft 365 on 2023-11-22, version 1.0.

6. **Checked for hidden content** on the HTML page — no accordions, collapsed sections, tabs, or additional links. The page is a plain HubSpot site page with just the banner and one link.

7. **Took a screenshot** of the web page in browser to confirm visual appearance matches source analysis.

## What Was Found

The entire EHI export documentation consists of a single 4-page PDF (including cover page). Here is what it describes:

### Export Modes
- **Single Patient Export**: Users can export EHI for one patient at any time without developer assistance.
- **Multi-Patient Export**: Users can export EHI for multiple patients at any time without developer assistance.

No further detail is provided about how to initiate either mode (no screenshots, no menu paths, no step-by-step instructions).

### Export Structure
Each patient's export is delivered as **a single compressed ZIP file** containing:

1. **Clinical folder** — Contains one XML-based C-CDA file per patient. The C-CDA complies with "US Core Data for Interoperability (USCD), Version 1 requirements" (note: the document misspells "USCDI" as "USCD"). The document references three HL7 specifications:
   - HL7 CDA R2 IHE Health Story Consolidation, DSTU Release 1.1 (July 2012)
   - HL7 CDA R2 Consolidated CDA Templates, DSTU Release 2.1 (August 2015, June 2019 with Errata)
   - HL7 CDA R2 C-CDA Templates R2.1 Companion Guide, Release 2 (October 2019)

2. **Documents folder** — Contains patient documents in their original upload/scan formats (.jpg, .gif, .bmp, .png, .pdf, .txt). The document types listed are:
   - Signed progress notes
   - Available lab results
   - Radiology reports
   - Scanned documents
   - Imported documents
   - "Iploaded" documents (typo for "Uploaded")

3. **Patient Documents Detail.xls** — An Excel spreadsheet described as being included in the ZIP, though its structure and contents are not documented.

### What Is NOT Documented
The PDF provides no:
- Data dictionary or field-level documentation
- Schema files or machine-readable format specifications
- Sample export files or example data
- Screenshots of the export interface
- Step-by-step user instructions for performing the export
- Description of what the Patient Documents Detail.xls file contains
- Information about the specific C-CDA sections populated or template IDs used
- Explanation of how non-C-CDA data (billing, scheduling, etc.) is handled
- Timing, size limits, or performance characteristics of the export

## Export Coverage Assessment

### Data Domain Coverage

The export documentation reveals a **severely limited approach to EHI export** that fundamentally misunderstands the (b)(10) requirement. Based on what the documentation describes, the export consists of:

1. **A C-CDA document** — This is the standard clinical summary format, which by definition covers only USCDI v1 data classes. This means the clinical data export is limited to:
   - Problems/diagnoses
   - Medications
   - Allergies
   - Lab results (structured)
   - Vital signs
   - Procedures
   - Immunizations
   - Patient demographics
   - Care team
   - Goals
   - Health concerns
   - Smoking status

2. **Attached documents** — Progress notes, lab results, radiology reports, and scanned/uploaded documents in their original formats. This is better than nothing but is essentially a document dump rather than a structured data export.

**Major data domains from product research that appear to be completely absent from the export:**

- **Billing & claims data**: Professional, institutional, workers' comp, no-fault, dental claims — none mentioned
- **Revenue cycle data**: Eligibility verification, ERA/payment records, denial management, statements, adjustments
- **Scheduling data**: Appointment history, scheduling patterns, no-show records
- **E-prescribing history**: Prescription renewals, EPCS records, formulary checks, medication history from Surescripts
- **Patient portal activity**: Secure messages, appointment requests, refill requests
- **Kiosk/intake data**: Patient-entered demographics, consent forms, intake questionnaires
- **Encounter/superbill forms**: Coded encounter data linking clinical to billing
- **Clinical decision support logs**: Drug interaction alerts, clinical alerts
- **Telehealth records**: Virtual visit records, AI Scribe transcriptions
- **Quality measures**: MIPS/CQM reporting data
- **Audit logs**: User activity, access logs
- **Practice management data**: Provider schedules, practice configuration, fee schedules
- **Lab ordering data**: Electronic lab orders (structured, beyond what's in the C-CDA)
- **Implantable device data**: Despite being certified for (a)(14), not mentioned in export

The export is essentially the same data a patient would get through a patient portal or transitions-of-care document, plus a folder of scanned/attached documents. **This is a (g)(10)-level data export being presented as (b)(10) compliance.** The C-CDA is a clinical summary format designed for care transitions — it was never intended to capture "all electronic health information" in a system.

### Export Format & Standards

- **Format**: C-CDA XML (clinical data) + original-format document files + XLS index, bundled in a ZIP per patient
- **Standard**: C-CDA R2.1 per HL7/USCDI v1. This is a recognized standard but it is a clinical summary standard, not a comprehensive data export standard.
- **Appropriateness**: Poor. A C-CDA is inherently limited to clinical summary data. For a product that stores billing, scheduling, RCM, telehealth, patient engagement, and practice management data, a C-CDA captures perhaps 15-20% of the stored data at best. A database dump, CSV export of all tables, or even a FHIR Bulk Data export with extensions would be far more appropriate.
- **Reconstructibility**: A third party could reconstruct a basic clinical summary from this export. They could NOT reconstruct the full patient record including billing history, appointment history, portal communications, prescription history, or any administrative data.

### Documentation Quality

- **Readability**: The document is readable but extremely thin — 3 pages of actual content for what should be a comprehensive data export specification.
- **Data dictionary**: None. No field-level documentation whatsoever.
- **Data types/value sets**: None specified. The C-CDA is referenced by standard but no vendor-specific mappings or extensions are described.
- **Examples**: None. No sample export files, no example records.
- **Developer usability**: A developer could not implement an import of this data based solely on this documentation. The C-CDA standard is referenced but not which templates or sections are populated. The Patient Documents Detail.xls file is not described at all.
- **Maintenance**: Version 1.0, dated November 2023. No change history. The document has typos ("USCD" for "USCDI", "Iploaded" for "Uploaded") suggesting limited review.

### Structure & Completeness

- **Granularity**: Extremely coarse. The documentation describes the export at the folder/file level only — no table names, field names, data types, or value sets.
- **Coded fields**: Not documented.
- **Entity relationships**: Not documented.
- **Versioning**: Version 1.0 with no change history.

### Overall Assessment

This is one of the thinnest EHI export documentation sets possible. Practice EHR has essentially repackaged their C-CDA clinical summary export (the same format used for transitions of care under (b)(1)-(b)(3)) and added a document folder dump, then called it their (b)(10) EHI export. The documentation itself is a 3-page description at the folder level with no data dictionary, no schema, no examples, and no mention of the vast majority of data the product stores (billing, scheduling, RCM, patient engagement, telehealth, practice management).

The approach represents the classic (b)(10)/(g)(10) confusion: the vendor appears to believe that exporting USCDI clinical data in C-CDA format satisfies the "all electronic health information" requirement. For a full-featured ambulatory EHR + practice management platform that handles everything from charting through claims submission and denial management, a C-CDA export falls dramatically short of the regulatory intent.

## Access Summary
- Final URL (after redirects): https://www.practiceehr.com/data-export
- Status: found
- Required browser: no
- Navigation complexity: one_click (single PDF link on the page)
- Anti-bot issues: none

## Obstacles & Dead Ends
- None. The page loaded cleanly and the PDF downloaded without issues.
- The simplicity of the page (one heading, one link) meant there was nothing else to explore.
