# Genensys LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://docs.google.com/document/d/1HsYw7-fWQW-6txwQBw0OcsT0M5H7Wxnv7A2YopWGXSo/edit?usp=sharing
- CHPL IDs: 10317 (15.05.05.1523.GENS.01.00.1.200225)
- Product: Simplify EMR v4.0
- Certification date: 2020-02-25

## Navigation Journal

1. Probed the registered URL with `curl -sI -L`. It's a Google Docs document returning HTTP 200 with `text/html; charset=utf-8`.

2. Exported the document in three formats using Google's export API:
   ```
   curl -sL "https://docs.google.com/document/d/1HsYw7-fWQW-6txwQBw0OcsT0M5H7Wxnv7A2YopWGXSo/export?format=pdf" -o ehi-export-doc.pdf
   curl -sL "https://docs.google.com/document/d/1HsYw7-fWQW-6txwQBw0OcsT0M5H7Wxnv7A2YopWGXSo/export?format=txt" -o ehi-export-doc.txt
   curl -sL "https://docs.google.com/document/d/1HsYw7-fWQW-6txwQBw0OcsT0M5H7Wxnv7A2YopWGXSo/export?format=docx" -o ehi-export-doc.docx
   ```

3. Verified the PDF: `pdfinfo` confirms 2 pages, title "Simplify EMR b(10) Export Format", produced by Google Docs Renderer.

4. Opened the document in Chrome and took screenshots of both pages. The document has a title page ("Simplify EMR / Export Format") and a single content page with the export format description.

5. Checked the mandatory disclosures page at `https://genensys.com/mu-disclosure/` — it confirms (b)(10) certification but contains no additional EHI export documentation or download links.

6. Checked the vendor's API documentation page at `https://genensys.com/api/` — it contains links to g(10) FHIR API documentation, API terms, and an API framework page. These are all related to the (g)(10) standardized API, not the (b)(10) export. The b(10) export described in the Google Doc is a separate C-CDA + documents export mechanism, not FHIR-based.

7. No additional EHI export documentation was found anywhere on the vendor's site.

## What Was Found

The entire EHI export documentation consists of a single Google Doc (831 bytes of text, 2 PDF pages) titled "Simplify EMR b(10) Export Format." The document describes two export modes:

### All Patient Mode
- Produces a ZIP file named `Patient_export_{date}.zip`
- Contains one folder per patient, each in the single-patient format described below

### Single Patient Mode
- Creates a folder named `Lastname_FirstName_patientId_Date`
- The folder contains:
  1. **A C-CDA file** (`Lastname_FirstName_ccda.xml`) — described as "Conformant to USCDI v1" with a reference to the USCDI Version 1 July 2020 Errata document for C-CDA specifications
  2. **Encounters subfolder** — contains all visit notes as PDF or HTML files, named `{encounterId}_{date}.pdf` or `.html` (0 to many)
  3. **Patient Documents subfolder** — contains other documents as PDF or HTML files, named `{documentId}_{date}.pdf` or `.html` (0 to many)

That is the entirety of the documentation. There is no data dictionary, no field-level documentation, no schema file, no sample data, no export instructions, and no description of what data fields are included in the C-CDA or what types of documents appear in the subfolders.

## Export Coverage Assessment

### Data Domain Coverage

The export format relies on two mechanisms to cover EHI:
1. A **USCDI v1 C-CDA document** per patient
2. **Encounter notes and patient documents** as PDF/HTML files

**What USCDI v1 C-CDA covers** (standardized clinical summary data):
- Demographics, problems, medications, allergies, immunizations, vital signs, lab results, procedures, care team, goals, health concerns, assessment/plan, clinical notes (some), implantable devices

**What appears to be missing or undocumented** from the product's known data stores:
- **Billing/claims data** — The product has integrated practice management with billing, claims, eligibility, authorization, and revenue cycle management. None of this is mentioned in the export documentation. C-CDA does not carry billing data. No separate billing export is described.
- **Scheduling data** — Appointments, reminders, automated messages are part of the PM system but not covered by C-CDA or the export.
- **E-prescribing data** — While medication lists appear in C-CDA, the full e-prescribing transaction history (via MDToolBox integration), prescription benefits, formulary data, and controlled substance prescribing records are unlikely to be fully captured.
- **Patient portal data** — Messages between patients and providers, prescription renewal requests, appointment requests, bill payment records — none of these are mentioned or covered by C-CDA.
- **Lab ordering details** — C-CDA includes lab results but not the full ordering workflow, task assignments, or trending data the product stores.
- **Clinical quality measure data** — CQM reporting data is part of the certified system but not addressed in the export.
- **Therapy-specific data** — The product has a strong focus on pediatric therapy (OT, PT, speech, ABA) with specialty-specific templates, dashboards, and workflows. None of this specialty clinical data is specifically addressed. It may partially appear in encounter notes as PDFs, but there's no structured export of therapy-specific assessments.
- **Custom form/template data** — The product emphasizes customizability with configurable templates. Structured data from custom forms may be lost when rendered as PDF encounter notes.

The encounter PDFs/HTMLs may capture some clinical narrative data beyond what's in C-CDA, but rendering clinical notes as PDF/HTML means the structured data (coded diagnoses, measurements, therapy progress metrics) becomes unstructured and non-computable.

**Bottom line:** This export appears to be a thin wrapper around C-CDA (covering USCDI v1 clinical summaries) plus document dumps. It is essentially a (g)(6)-style clinical summary export repackaged as a (b)(10) export, with encounter notes added as flat documents. The export does not appear to cover "all electronic health information" — billing, scheduling, patient portal interactions, therapy-specific structured data, and e-prescribing workflow data are all absent.

### Export Format & Standards

- **Primary format:** USCDI v1 C-CDA XML (one per patient)
- **Supplementary format:** PDF and/or HTML files for encounter notes and patient documents
- **Packaging:** ZIP file (all-patient mode) or folder (single-patient mode)
- **Standard compliance:** Claims conformance to USCDI v1 C-CDA. References the official USCDI Version 1 errata document.
- **No proprietary schema or data dictionary** is provided.

The format choice is problematic for a (b)(10) export. C-CDA is designed for clinical summaries — it covers USCDI data classes well but cannot represent billing records, scheduling data, patient portal interactions, or arbitrary specialty-specific clinical structures. A true (b)(10) export of "all EHI" from a practice management system with billing would need a separate mechanism (CSV, database dump, etc.) for data that doesn't fit into C-CDA.

A third party could reconstruct a clinical summary from this export but could **not** reconstruct the full patient record including billing history, e-prescribing transactions, portal messages, or specialty therapy assessments.

### Documentation Quality

The documentation is **extremely minimal** — 831 bytes of plain text describing only the folder structure and file naming conventions. There is:

- **No data dictionary** — no field/element definitions for the C-CDA content
- **No value sets or coded field documentation**
- **No sample data or example exports**
- **No user guide or instructions** for performing the export
- **No screenshots of the export interface**
- **No description of what clinical data elements** are included in the C-CDA
- **No description of what types of encounter notes or documents** appear in the subfolders
- **No error handling or edge case documentation**
- **No versioning or change history**

The only external reference is to the USCDI v1 errata document for C-CDA specifications, which is a standard reference — it tells you what C-CDA can contain but not what Simplify EMR actually puts into its C-CDA exports.

A developer attempting to import this data would need to treat the C-CDA as a generic USCDI v1 document and the encounter/document files as opaque blobs. There is no vendor-specific documentation to guide the process.

### Structure & Completeness

- **Granularity:** File/folder naming conventions only. No field-level documentation whatsoever.
- **Coded fields:** Not documented.
- **Relationships:** Not documented beyond the folder hierarchy (patient → C-CDA + encounters + documents).
- **Completeness:** The documentation describes the container format (folders and files) but not the content. Knowing that a file is named `Lastname_FirstName_ccda.xml` tells you nothing about what clinical data it contains or how complete it is.

This is among the most minimal EHI export documentation possible — it describes how files are organized in folders but provides zero insight into the data content, coverage, or format details.

## Access Summary
- Final URL (after redirects): https://docs.google.com/document/d/1HsYw7-fWQW-6txwQBw0OcsT0M5H7Wxnv7A2YopWGXSo/edit?usp=sharing
- Status: found
- Required browser: no (Google Docs export API works with curl)
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. The Google Doc was publicly accessible and exportable via curl.
- The vendor's API documentation page (https://genensys.com/api/) contains only (g)(10) FHIR API documentation, which is a separate system from the (b)(10) export.
- The mandatory disclosures page (https://genensys.com/mu-disclosure/) confirms (b)(10) certification but provides no additional export documentation.
- No additional EHI export documentation was found on the vendor's website.
