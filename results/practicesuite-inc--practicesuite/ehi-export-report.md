# PracticeSuite, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://academy.practicesuite.com/%c2%a7-170-315b10-electronic-health-information-ehi-export/
- CHPL IDs: 10788 (PracticeSuite), 10789 (FreeChiro)
- Developer: PracticeSuite, Inc.
- Products: PracticeSuite (EHR-18.0.0), FreeChiro (EHR-18.0.0)
- Both products certified 2022-01-13; same underlying platform

## Navigation Journal

1. **Probed the registered URL with curl:**
   ```bash
   curl -sI -L "https://academy.practicesuite.com/%c2%a7-170-315b10-electronic-health-information-ehi-export/" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200, Content-Type: text/html. WordPress site on WP Engine behind Cloudflare.

2. **Downloaded the page HTML:**
   ```bash
   curl -sL "https://academy.practicesuite.com/%c2%a7-170-315b10-electronic-health-information-ehi-export/" -H 'User-Agent: Mozilla/5.0' -o ehi-export-page.html
   ```
   159,057 bytes. Single WordPress page with embedded screenshots.

3. **Identified downloadable files:** No PDF, ZIP, CSV, JSON, or other structured file downloads on the page. The page contains only inline text and embedded PNG screenshots demonstrating the export workflow.

4. **Downloaded all embedded screenshots** (12 PNG files total) showing:
   - Report Central menu with K3 report highlighted (`k3.png`)
   - User access/privilege configuration (`UserAcess.png`)
   - Single patient search interface (`singlepatsearch.png`)
   - Patient population search interface (`patpopulationsrch.png`)
   - CCDA download button and resulting ZIP contents (`ccdadownload-1.png`, `ccdadownloadzip.png`)
   - Document download button and resulting ZIP contents (`docdownload-1.png`, `docdownloadzip.png`)
   - Population CCDA download and ZIP (`patpopccdadownload-2.png`, `patpopccdadownloadzip.png`)
   - Population document download and ZIP (`patpopdocdownload.png`, `patpopdocdownloadzip.png`)

5. **Checked WordPress JSON API** for the page content:
   ```bash
   curl -sL "https://academy.practicesuite.com/wp-json/wp/v2/pages/10911" -H 'User-Agent: Mozilla/5.0'
   ```
   Page created 2023-11-14, last modified 2024-05-20.

6. **Searched academy.practicesuite.com** for related documentation:
   ```bash
   curl -sL "https://academy.practicesuite.com/?s=ehi+export" -H 'User-Agent: Mozilla/5.0'
   curl -sL "https://academy.practicesuite.com/?s=ccda" -H 'User-Agent: Mozilla/5.0'
   ```
   Found a related page: **K3. Patient Clinical Analysis Report** at `https://academy.practicesuite.com/k3-patient-clinical-analysis-report/` — this is the report used for EHI export. Downloaded it and its screenshots.

7. **Checked Clinical Summary page** at `https://academy.practicesuite.com/clinical-summary/` — this describes the patient portal's C-CDA view, not the EHI export itself.

8. **Took full-page browser screenshot** of the EHI export page.

## What Was Found

### Export Mechanism

PracticeSuite's EHI export is accessed through **Report Central > K3. Patient Clinical Analysis Report**. The export produces two separate downloads:

1. **C-CDA Export**: A ZIP file containing XML files in C-CDA (HL7 CDA R2) format, one per patient. Each XML file is a "full CCDA Summary" of the patient. A `cda.xsl` stylesheet is included in the ZIP for rendering. File naming: `<FirstName>_<LastName>_<MR#>_CCDAhl7V3Xml_<timestamp>.xml`

2. **Documents Export**: A separate ZIP file containing all documents associated with the patient(s) in their original formats. File naming: `<FileName>_<Category>[file]`, organized into per-patient subfolders.

### Single Patient vs. Population Export

- **Single Patient**: Search by patient name or MR#, then click "Download C-CDA" or "Download Documents"
- **Patient Population**: Search by health parameters (vitals, diagnoses, medications, facesheet parameters, lab orders, lab results, radiology, CPT codes), then bulk download for all matching patients

### Access Control

Export is restricted to users with access to the Report Central menu. The documentation states: "Unauthorized users will not have access to Report Central menu from where we can export the EHI."

### Data in the Export

The C-CDA export contains a "full CCDA Summary" — standard C-CDA sections. Based on the screenshots and documentation, the C-CDA includes at minimum:
- Patient demographics
- Chief complaint
- Past medical history
- Allergies
- Medication list
- Vital signs
- Assessment/Diagnosis
- Plan/Recommended action

The documents export includes all documents associated with a patient in their original file formats (presumably PDFs, images, scanned documents, etc.).

### What the Documentation Does NOT Include

- **No data dictionary**: There is no listing of database tables, fields, or schema
- **No C-CDA section inventory**: The documentation doesn't specify which C-CDA sections are populated or which are omitted
- **No field mapping**: No description of how PracticeSuite data fields map to C-CDA elements
- **No sample export files**: No example C-CDA XML or sample data provided
- **No schema files**: No XSD, JSON Schema, or machine-readable format specification
- **No value set documentation**: No description of coded values, vocabularies, or terminologies used
- **No API specification**: The export is UI-driven only; no programmatic access documented

## Export Coverage Assessment

### Data Domain Coverage

PracticeSuite is a comprehensive ambulatory EHR with practice management, billing, patient portal, e-prescribing, lab integration, and telehealth. The product research identifies extensive data domains including clinical data, prescriptions, billing/financial data, scheduling, patient registration, portal data, telehealth, documents, quality measures, and public health reporting.

The EHI export provides two components:

**C-CDA Export (clinical data):**
The C-CDA format, by its nature, covers a defined set of clinical data sections. A standard C-CDA document typically includes demographics, problems, medications, allergies, immunizations, vital signs, procedures, results, encounters, and care plans. However, the documentation never specifies which C-CDA sections PracticeSuite populates. It merely says "full CCDA Summary" without elaboration.

**Documents Export (attached documents):**
The separate documents download captures files attached to patient records in their original format. This is a useful supplement but only covers explicitly uploaded/attached documents, not structured data stored in database fields.

**Domains likely missing or uncertain:**

| Domain | Status |
|--------|--------|
| **Billing/financial data** (charges, claims, payments, insurance) | **Not mentioned.** C-CDA does not have standard billing sections. The documents export would not capture structured billing data. This is a major gap — PracticeSuite processes $10B+ in claims annually. |
| **Scheduling/appointments** | Not mentioned. Not part of C-CDA. (Not necessarily EHI, but encounter history should be covered.) |
| **E-prescribing details** (prior auths, PDMP, refill history) | Uncertain. Basic medication list is in C-CDA, but detailed prescribing data from NewCropRx may not be. |
| **Patient portal data** (messages, chat, surveys, appointment requests) | **Not mentioned.** Not part of C-CDA. Portal data stored in HelloHealth may be entirely absent. |
| **Telehealth data** (session records, virtual encounter details) | Uncertain. Encounter notes from telehealth visits may be in C-CDA, but telehealth-specific metadata likely not. |
| **Lab orders and results** | Partially covered. C-CDA includes Results sections, but the level of detail depends on implementation. |
| **Imaging/radiology** | Uncertain. C-CDA may include diagnostic report references but not actual images. |
| **Custom forms/templates** | Uncertain. PracticeSuite has 30+ customizable EMR templates; whether custom template data maps into C-CDA sections is undocumented. |
| **Clinical decision support alerts** | Not mentioned. Not part of standard C-CDA. |
| **Implantable device data** | Uncertain. C-CDA has a Medical Equipment section but implementation varies. |

**The core issue: C-CDA is a clinical summary standard, not a complete data export format.** It was designed to communicate a summary of care between providers, not to export an entire patient record. Using C-CDA as the sole structured export format for (b)(10) compliance inherently limits what structured data can be exported. The addition of a raw documents download helps but doesn't address structured data that lives in database fields rather than as attached documents.

### Export Format & Standards

- **Format**: C-CDA (HL7 CDA R2) XML + original-format documents
- **Standard**: C-CDA is a recognized, widely-used clinical document standard
- **Appropriateness**: C-CDA is appropriate for clinical summary data but inadequate as a complete EHI export format. It cannot represent billing records, scheduling data, portal communications, or many other data domains that PracticeSuite stores.
- **Reconstructability**: A third party could import the C-CDA into another EHR for clinical data. However, they could NOT reconstruct the full patient record (billing history, portal messages, appointment history, etc.) from the export.

### Documentation Quality

The documentation is **basic but clear** for its limited scope:

- **Readable**: The step-by-step instructions are easy to follow with annotated screenshots
- **No data dictionary**: There is no field-level documentation whatsoever
- **No examples**: No sample C-CDA files or example data are provided
- **No technical specification**: Beyond saying "CCDA format," there is no description of which C-CDA template/version is used, which sections are populated, or what coded vocabularies are employed
- **Could a developer implement an import?** A developer would know to expect C-CDA XML and could parse it with standard C-CDA libraries, but they would have no PracticeSuite-specific documentation to guide them on what data to expect or how PracticeSuite-specific concepts map to C-CDA elements
- **Maintenance**: Page created November 2023, last updated May 2024. Appears to be a compliance deliverable rather than ongoing technical documentation.

### Structure & Completeness

- **Granularity**: The documentation describes the export at the *workflow* level (how to click buttons) but not at the *data* level (what fields/sections the export contains)
- **No value sets documented**: No vocabulary or code system information
- **No relationships documented**: No description of how exported data elements relate to each other
- **No versioning**: No mention of export format versions or change history
- **The K3 report page** adds marginal detail: it describes the search filters (diagnosis, medication, vitals, facesheet, CPT, lab order, lab result, radiology) and mentions a Custom Visit Summary report, but still doesn't document the C-CDA content

### Overall Assessment

PracticeSuite's EHI export documentation is a **minimal compliance effort**. The approach — exporting a C-CDA summary plus raw documents — covers clinical summary data reasonably well through an established standard, but almost certainly does not export "all electronic health information" as (b)(10) requires. The most glaring gap is **billing and financial data**: PracticeSuite is fundamentally a practice management and billing platform (processing $10B+ in claims annually), yet the export format (C-CDA) has no mechanism to carry billing records, claims, payments, or insurance information. Patient portal communications, scheduling history, and other non-clinical data are similarly absent.

The documentation itself provides only export *instructions* (how to click buttons) without any export *specification* (what data is exported and in what structure). There is no data dictionary, no field mapping, no sample files, and no description of C-CDA section coverage. A developer receiving this export would need to reverse-engineer the C-CDA content from actual export files.

## Access Summary
- Final URL: https://academy.practicesuite.com/%c2%a7-170-315b10-electronic-health-information-ehi-export/
- Status: found
- Required browser: no (standard HTML, no JavaScript required for content)
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare present but not blocking)

## Obstacles & Dead Ends
- No obstacles encountered. The page loaded cleanly via curl with a standard User-Agent header.
- The mandatory disclosures page at `https://practicesuite.com/ehr-onc-certification/` did not contain any additional EHI export documentation.
- No downloadable structured files (PDF, ZIP, CSV, JSON, etc.) were found — all documentation is inline HTML with embedded screenshots.
