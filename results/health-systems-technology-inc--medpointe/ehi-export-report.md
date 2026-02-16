# Health Systems Technology, Inc. — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://hstspot.com/help-documents.php
- CHPL IDs: 11238
- Product: MedPointe v13
- Certification date: 2023-02-16

## Navigation Journal

1. **Initial probe:**
   ```bash
   curl -sI -L "https://hstspot.com/help-documents.php" -H 'User-Agent: Mozilla/5.0'
   ```
   Returned HTTP 200 from Apache/2.4.6 (CentOS) with PHP/8.0.30. Content-Type: text/html. No redirects.

2. **Fetched and examined the page:**
   ```bash
   curl -sL "https://hstspot.com/help-documents.php" -H 'User-Agent: Mozilla/5.0' -o /tmp/hst-page.html
   ```
   Page is a small (6,827 bytes) static HTML page titled "Medpointe Customer Help NOW", built with Webflow. It lists documents in three categories:
   - **Exporting Documents** (1 file): `Providers - Exporting Computer Readable Documents.pdf`
   - **Tutorials** (12 MP4 videos): Clinical workflow tutorials (C00-Welcome through C11-Checkin Process)
   - **e-Prescribing** (7 PDFs): Medication and prescribing guides

3. **Downloaded the export documentation:**
   ```bash
   curl -sL 'https://downloads.hstcentral.com/helpdocs/Exporting%20Documents/Providers%20-%20Exporting%20Computer%20Readable%20Documents.pdf' \
     -H 'User-Agent: Mozilla/5.0' \
     -o 'downloads/Providers - Exporting Computer Readable Documents.pdf'
   ```
   Confirmed: PDF document, 2 pages, 474,907 bytes. Author: Tim Schmidt. Created 2023-11-16. Title: "Microsoft Word - Exporting Documents via C62".

4. **Checked the Exporting Documents directory for additional files:**
   ```bash
   curl -sL "https://downloads.hstcentral.com/helpdocs/Exporting%20Documents/" -H 'User-Agent: Mozilla/5.0'
   ```
   Apache directory listing confirms only one file in this directory.

5. **Checked related sites for additional documentation:**
   - `https://medpointemr.com/meaningful-use/` — marketing page about ONC certification, no EHI export details
   - Probed common paths on medpointemr.com (/api, /fhir, /interoperability, /ehi, /docs, /compliance, /onc) — all returned 404
   - Probed hstspot.com and hstcentral.com for similar paths — all 404
   - `https://downloads.hstcentral.com/` root redirects to help-documents.php
   - Web searched for "MedPointe C62 file format" and "Health Systems Technology MedPointe EHI export data dictionary" — no results

6. **Took a full-page screenshot** of the help documents page for the archive.

## What Was Found

The entire EHI export documentation for MedPointe consists of a single 2-page PDF: **"Providers - Exporting Computer Readable Documents"**. It describes how to export clinical documents from the MedPointe EHR using a proprietary format called **"C62"**.

The PDF covers three export methods:

1. **Single Document Export**: Right-click a document in the patient's TOC (Table of Contents) and select "Export via C62."
2. **Chart Export (Multiple Documents)**: From the patient's chart Overview Page, right-click and select "Export Chart." A dialog appears allowing the user to:
   - Set a date range
   - Select document types: Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents, Include Restricted Documents
   - Choose output: Print, Export to Folder, or Export to C62 file
3. **Batch Export (Multiple Charts)**: From Main Menu → Tools → Clinical → Export, select patient criteria (last name range, DOB, classification, provider, etc.), document types, and date range.

**What the documentation does NOT include:**
- Any description of what the "C62" format actually is — no schema, no structure, no field definitions
- No data dictionary — no list of what data fields are exported
- No specification of what data domains are covered (clinical, billing, administrative, etc.)
- No sample files or examples of export output
- No mention of FHIR, C-CDA, CSV, or any recognized standard
- No mention of billing, scheduling, claims, or administrative data
- No description of how relationships between records are preserved
- No versioning or format documentation

The document type checkboxes visible in the export dialog (Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents) suggest the export covers clinical documentation only — not the full breadth of data the product stores.

## Export Coverage Assessment

### Data Domain Coverage

MedPointe is a comprehensive ambulatory EHR storing clinical records, billing/RCM data, scheduling, patient portal data, scanned documents, e-prescribing data, lab results, immunization records, and more. The export documentation addresses only a narrow slice:

**Appears covered (based on the export dialog):**
- Clinical notes / encounter documentation
- Cover sheets
- Text documents
- Scanned/faxed documents

**Not mentioned or clearly absent:**
- Patient demographics
- Problem lists / diagnoses
- Medication lists and prescription history
- Allergy lists
- Lab orders and results
- Imaging orders
- Immunization records
- Vital signs / clinical observations
- Care plans
- Referral records
- Appointment schedules / scheduling history
- Insurance/eligibility data
- Claims, ERA/EOB, denial data
- Payment records / accounting
- Patient portal messages
- Online intake form submissions
- Audit logs
- Clinical quality measure data
- Clinical decision support data

The export appears to be a **document-level export** — it exports clinical documents as files, rather than exporting the underlying structured data (problems, meds, allergies, labs, etc.) that lives in the EHR's database. This is a critical gap. Even within the clinical domain, there's no indication that the structured data behind those documents (coded diagnoses, discrete lab values, medication records) is preserved in a computable form.

The billing, scheduling, and administrative data that MedPointe stores — which is a substantial portion of "all electronic health information" — appears entirely absent from the export.

### Export Format & Standards

The export uses a proprietary format called **"C62"**. No public documentation exists describing this format:
- No schema, XSD, JSON Schema, or format specification was found
- Web searches for "C62 file format" in healthcare contexts returned no results
- The format appears to be entirely vendor-proprietary with no external documentation

The C62 format is not a recognized healthcare standard. It is not FHIR, C-CDA, CSV, or any other format a third party could reasonably import without proprietary tooling. The documentation does not indicate whether C62 files are human-readable, binary, structured data, or rendered documents.

A third party receiving a C62 export would have no way to interpret it without MedPointe-specific import tools or additional documentation from the vendor.

### Documentation Quality

The documentation is extremely minimal:
- **2 pages total** — mostly step-by-step UI instructions
- **No data dictionary** — not even a list of table names or data categories
- **No field definitions** — no data types, value sets, or constraints
- **No examples** — no sample export files or sample records
- **No format specification** — the C62 format is named but never described
- Two screenshots show the export dialog and right-click menu, providing some context about the available options

A developer could not implement an import of this data based on this documentation. A patient receiving this export could not meaningfully use the data without MedPointe software. The documentation reads as a compliance checkbox rather than a genuine effort to enable data portability.

### Structure & Completeness

- **Granularity**: The documentation operates at the level of "document types" (Notes, Cover Sheets, Text Documents, Scanned/Faxed Documents). There are no field-level definitions.
- **Coded fields**: Not documented.
- **Relationships**: Not documented.
- **Versioning**: The PDF metadata shows it was created on 2023-11-16, approximately 9 months after the certification date (2023-02-16). No version history.
- **Completeness**: This is among the most minimal EHI export documentation possible. It documents how to click the export button but not what comes out.

### Overall Assessment

Health Systems Technology's EHI export documentation is a serious compliance concern. The (b)(10) requirement calls for the ability to export "all electronic health information" — MedPointe stores clinical data, billing/RCM data, scheduling data, patient portal data, scanned documents, lab results, prescriptions, and more. The documentation describes exporting only clinical documents in a proprietary, undocumented format (C62), with no data dictionary, no schema, no format specification, and no coverage of administrative or financial data.

This is not a case of (g)(10)/(b)(10) confusion — the vendor isn't pointing to their FHIR API. Instead, they've documented a document-level export function that appears to predate the (b)(10) requirement and was likely repurposed to satisfy it. The export dialog's document type categories (Cover Sheet, Notes, Text Documents, Scanned/Faxed Documents) suggest this is a clinical records export tool, not a comprehensive EHI export covering all data the system stores.

The vendor is very small (appears to be primarily one developer, Tim Schmidt), which may explain the minimal documentation effort, but does not excuse the gap between what (b)(10) requires and what is documented here.

## Access Summary
- Final URL (after redirects): https://hstspot.com/help-documents.php (no redirects)
- Status: found
- Required browser: no (static HTML page, all content in source)
- Navigation complexity: direct_link (one click to PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The `medpointemr.com/meaningful-use` mandatory disclosures URL renders as a WordPress marketing page with no EHI-specific content
- The helpdocs directory on downloads.hstcentral.com is browsable but contains only the one export PDF
- No additional documentation found on any of the vendor's three domains (hstspot.com, hstcentral.com, medpointemr.com)
- The "C62" file format has zero documentation available publicly — appears entirely proprietary
- Wayback Machine returned no useful historical snapshots
