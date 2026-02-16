# MD Logic, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.mdlogic.com/solutions/b10-export-documentation
- CHPL IDs: 11403 (v8.0, certified 2023-12-06), 11056 (v7.2, certified 2022-12-07)
- Developer: MD Logic, Inc., Lawrenceville, Georgia

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL:
   ```
   curl -sI -L "https://www.mdlogic.com/solutions/b10-export-documentation" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ...'
   ```
   Result: HTTP 200, `Content-Type: text/html; charset=utf-8`, Drupal 7 site on Apache. No redirects.

2. **Page fetch** — Downloaded the full HTML page (66,819 bytes):
   ```
   curl -sL "https://www.mdlogic.com/solutions/b10-export-documentation" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ...' \
     -o downloads/b10-export-documentation.html
   ```

3. **Link analysis** — Searched the HTML for downloadable files (PDF, ZIP, CSV, JSON, etc.). Found no external file downloads. The only file-like links were `http://example.com/example.json` (placeholder `$id` values inside the JSON Schema definitions) and `https://json-schema.org/draft/2019-09/schema` (standard schema reference). No data dictionary files, no sample exports, no ZIP downloads.

4. **Schema extraction** — The page contains two JSON Schema definitions embedded as syntax-highlighted HTML (inline `<span>` elements with color styling inside scrollable `<div>` containers). Extracted both schemas by parsing the text content and saved as clean JSON files.

5. **Screenshot** — Opened the page in Chrome, took a full-page screenshot confirming the visual layout: a header "B10 EXPORT DOCUMENTATION", three paragraphs of prose about individual patient export, a scrollable dark-themed JSON code block (Schema 1), three paragraphs about bulk export, and a second scrollable dark-themed JSON code block (Schema 2).

6. **Related pages checked:**
   - `/solutions/meaningful-use` (mandatory disclosures) — Contains the statement: "Data Export: MD Logic will charge a fee to export health data out of the MD Logic EHR software in the event the customer requires data to transfer to another EHR." No additional technical export documentation.
   - `/solutions/standard-api-documentation` (G10 API) — FHIR API documentation for (g)(10). No references to EHI export or (b)(10) beyond navigation links.
   - `/solutions/api-documentation` — Blocked by ModSecurity with short User-Agent. With full headers, returned the general API docs page. No EHI export content.

## What Was Found

The entire EHI export documentation consists of a single HTML page with approximately 150 words of prose and two JSON Schema definitions. Here is the complete substantive content:

### Export Process Description

The documentation describes a **document-centric export** mechanism:

1. **Individual patient export:** A user requests data for a patient. MD Logic sends an email with a direct download link. The link leads to a page where the user can download a ZIP file containing "all the documents in the requested patient's record." Inside the ZIP is a `manifest.json` file that indexes the documents.

2. **Bulk export (all patients):** For a full export, the user must "contact mdlogic support" because "this can be an extremely large amount of data, special arrangements will need to be made to deliver the data." The bulk export produces a collection of ZIP files (one per patient, structurally identical to the individual export) plus a top-level manifest file with patient demographics and ZIP file assignments.

### Schema 1: Per-Patient Manifest (`manifest.json`)

An array of objects, each with four fields:
- `Descripton` [sic — typo in original] — string, e.g., "MRI Spine", "MRI Hip", "Registration Form", "Progress Notes"
- `FileName` — string, e.g., "testFile_51.pdf", "testFile_3305.xml", "testFile_3305.jpg"
- `FileType` — string, e.g., "Word", "PDF", "CCDA", "JPEG"
- `DateCreated` — string (M/D/YYYY format), e.g., "8/25/2020"

### Schema 2: Bulk Export Manifest

An array of objects, each with twelve fields:
- `FirstName`, `LastName`, `MiddleName`, `Suffix` — patient name components
- `Address1`, `Address2`, `City`, `State`, `Zip` — address fields
- `Gender` — listed as required but not defined in `properties` (missing from schema)
- `DOB` — date of birth as string (MM/DD/YYYY format)
- `PatientFileName` — reference to the patient's ZIP file, e.g., "5125.zip"

**Notable schema issues:**
- The `required` array includes `"Address"` but the property is named `"Address1"` (mismatch)
- `Gender` is listed as required but has no corresponding property definition
- The `FirstName` property has a trailing comma after `"Jane"` in its examples array (invalid JSON — trailing commas are not valid in JSON)
- Both schemas use placeholder `$id` values (`http://example.com/example.json`)
- The `Descripton` field has a typo (missing 'i')

### Export Format

The export is a **file-based document dump**: each patient gets a ZIP containing their documents as individual files (PDF, Word, JPEG, CCDA XML) plus a `manifest.json` that indexes them. This is not a structured data export — it's a collection of the documents that have been stored or generated in the patient's chart.

## Export Coverage Assessment

### Data Domain Coverage

This is the most critical finding: **the export documentation describes only a document collection, not a structured data export.** Based on the product research, MD Logic EHR stores extensive structured clinical and billing data:

**Domains with no evidence of structured export:**
- **Diagnoses / Problem lists** — No mention. The (a)(1) certification implies these exist in the system.
- **Medications / Prescriptions** — The product has generated "47 million prescriptions" per vendor statistics. No structured medication data in the export.
- **Lab results** — The eLabs module provides bi-directional lab interfaces with trending/graphing. No structured lab data in the export.
- **Vital signs / Clinical observations** — No mention.
- **Allergies and adverse reactions** — Implied by (a)(3) certification. No structured export.
- **Immunization records** — Implied by (a)(3) certification. No structured export.
- **Billing data** — The PM module handles claims, EOBs, charge entry, clearinghouse integration. No billing data appears in the export at all.
- **Insurance/enrollment information** — Not mentioned.
- **Scheduling/appointment data** — Not in export (though this is not necessarily EHI).
- **Care plans, referrals** — Not mentioned.

**What may be partially covered:**
- **Clinical notes / Progress notes** — The manifest examples include "Progress Notes" as a document description. Clinical notes are likely exported as document files (PDF/Word), which preserves the content but not the structured data within them.
- **Imaging** — The examples include "MRI Spine" and "MRI Hip" descriptions, and JPEG file types. Images stored as documents may be exported.
- **Patient demographics** — The bulk export manifest includes basic demographics (name, address, gender, DOB). However, this is only in the index manifest, not as structured patient data within the per-patient export.
- **CCDA documents** — The FileType examples include "CCDA", suggesting some structured clinical summaries may be included as pre-generated C-CDA documents. But this would only cover the USCDI-equivalent data that fits into a C-CDA, not the full breadth of EHR data.

**The fundamental gap:** The export appears to treat the patient record as a collection of documents (PDFs, Word docs, images, CCDAs) rather than extracting the structured data stored in the EHR's database. For a product with extensive structured data (medications, labs, vitals, billing codes, insurance claims, prescription history), exporting only documents means most of the structured, queryable clinical data is either:
1. Flattened into PDF/Word renderings that lose structure, or
2. Omitted entirely

### Export Format & Standards

- **Format:** ZIP files containing mixed document types (PDF, Word, JPEG, CCDA XML) with a JSON manifest index.
- **Standard:** The manifest uses a simple custom JSON schema. The inclusion of CCDA as a file type suggests some use of the C-CDA standard for clinical summaries, but this is just one file type among many.
- **Appropriateness:** For a product that stores structured clinical data (discrete lab values, coded diagnoses, medication lists, vital signs, billing codes), a document dump is a poor fit. A third party receiving this export would get rendered documents but would not be able to reconstruct the discrete, structured patient record. Lab trends, medication lists, problem lists, and billing records would all need to be manually extracted from document text — if they're included at all.
- **Could a third party reconstruct the record?** Partially, at best. Documents like progress notes and imaging reports preserve narrative content. But discrete data (structured lab values, coded diagnoses, medication dosages and frequencies, insurance claim details) would be lost or degraded.

### Documentation Quality

- **Readability:** The documentation is extremely brief — about 150 words of prose. It's readable but sparse.
- **Data dictionary:** None. The JSON schemas describe the manifest structure, not the clinical data. There is no documentation of what data domains are included, what document types are generated, or what clinical content appears in each document.
- **Field-level definitions:** Only for the manifest files (4 fields for per-patient manifest, 12 fields for bulk manifest). No definitions for the actual clinical data within the exported documents.
- **Value sets:** None. The `FileType` examples (Word, PDF, CCDA, JPEG) and `Descripton` examples (MRI Spine, Registration Form, Progress Notes) hint at possible values but are not exhaustive.
- **Worked examples / Sample files:** None. No sample exports, sample manifest files, or example documents.
- **Developer implementability:** A developer could parse the manifest JSON but would have no way to programmatically interpret the heterogeneous document collection without significant manual effort per document type.
- **Maintenance:** The page appears to be a static Drupal page. The JSON schemas contain bugs (trailing comma, required/property name mismatch, missing Gender definition, "Descripton" typo), suggesting limited maintenance.

### Structure & Completeness

- **Granularity:** Extremely low. The documentation describes the container format (ZIP + manifest) but says nothing about the contents of the exported documents themselves.
- **Coded fields:** Not documented. The manifest has a `FileType` field with example values but no exhaustive list.
- **Relationships:** The bulk manifest links patients to their ZIP files via `PatientFileName`. Within a patient's ZIP, the manifest links descriptions to filenames. No deeper relational structure.
- **Versioning:** None mentioned.

### (b)(10) vs (g)(10) Assessment

This is **not** a case of conflating (b)(10) with (g)(10). MD Logic has a separate FHIR API documentation page for their (g)(10) certification. The B10 Export Documentation page describes a distinct, non-FHIR mechanism (document ZIP export).

However, the export appears to fall short of the (b)(10) requirement in a different way: rather than exporting "all electronic health information" as structured data, it exports documents from the chart. This likely captures only a subset of the EHI, since much of the structured data (discrete lab values, medication records, billing transactions, insurance data, coded diagnoses) may not exist as standalone documents in the chart. The inclusion of CCDA as a file type suggests some structured clinical summary is generated, but a single CCDA document cannot represent the full breadth of an EHR's data (billing, specialty-specific clinical data, custom forms, etc.).

### Mandatory Disclosures Finding

The mandatory disclosures page (`/solutions/meaningful-use`) states: "Data Export: MD Logic will charge a fee to export health data out of the MD Logic EHR software in the event the customer requires data to transfer to another EHR." This is a relevant policy statement — while ONC allows reasonable fees, this should be noted as a potential barrier to export access.

## Access Summary
- Final URL (after redirects): https://www.mdlogic.com/solutions/b10-export-documentation
- Status: found
- Required browser: no (curl with full User-Agent headers works; short User-Agent triggers ModSecurity on some pages)
- Navigation complexity: direct_link
- Anti-bot issues: ModSecurity blocks requests with short/missing User-Agent headers on some pages (not the B10 page itself)

## Obstacles & Dead Ends
- The `/solutions/api-documentation` and `/solutions/standard-api-documentation` pages return "Not Acceptable" errors when accessed with a minimal User-Agent string; they require a full browser-like User-Agent.
- No downloadable files exist on the B10 page — the JSON schemas are embedded in the HTML as syntax-highlighted spans, not available as standalone downloads.
- The scrollable code blocks on the page are only 300px tall, making it impossible to see the full schemas without scrolling within the embedded containers.
- The JSON schemas contain syntax errors (trailing commas) that make them technically invalid JSON as written on the page.
