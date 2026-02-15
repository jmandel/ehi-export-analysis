# WRS Health — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.wrshealth.com/onc-certification-and-costs
- CHPL ID: 10750 (15.02.05.2527.WRSH.01.01.1.211214)
- Product: WRS Health Web EHR and Practice Management System v7.0
- Certification date: 2021-12-14

## Navigation Journal

1. Probed the registered URL with curl:
   ```bash
   curl -sI -L "https://www.wrshealth.com/onc-certification-and-costs" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
   ```
   Result: HTTP 200, `text/html; charset=UTF-8`, ~102KB page served from CloudFront/S3.

2. Downloaded the page and searched for file links:
   ```bash
   curl -sL "https://www.wrshealth.com/onc-certification-and-costs" -H 'User-Agent: Mozilla/5.0' -o /tmp/wrs-page.html
   grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|xls|csv|json|doc|docx|yaml|yml)[^"]*"' /tmp/wrs-page.html
   ```
   Found 9 PDF links total: 4 Real World Testing Plans, 4 RWT Results, and 1 EHI Export PDF.

3. The page is a static WordPress page (hosted on S3 via CloudFront). The "ELECTRONIC HEALTH INFORMATION EXPORT" section is near the bottom, containing a single link:
   - [170.315 (b)(10) EHI Export Documentation](https://www.wrshealth.com/wp-content/uploads/2023/10/170.315-b10-EHI-Export.pdf)

4. Downloaded the PDF:
   ```bash
   curl -sL "https://www.wrshealth.com/wp-content/uploads/2023/10/170.315-b10-EHI-Export.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/170.315-b10-EHI-Export.pdf
   ```
   Verified: `file` confirms it is a PDF document, version 1.4, 8 pages, 1.1 MB. Created with Google Docs.

5. No additional links, accordions, or hidden content were found on the page related to EHI export. No data dictionary, schema, API docs, or sample data files are linked. The single PDF is the complete EHI export documentation.

## What Was Found

The EHI export documentation is a single 8-page PDF (v1.0, dated October 14, 2023) titled "170.315 (b)(10) Electronic Health Information Export." It describes a ZIP-based export mechanism for single-patient and multi-patient data.

### Export Mechanism

**Single Patient Export**: Users with Clinical Admin/Admin permissions log into the EHR Admin, search for a patient, right-click their name, select "EHI Export", click "Request Electronic Health Information", wait for processing, then download a ZIP file. The PDF includes screenshots of this workflow.

**Multi-Patient Export**: WRS Health can export data for an entire patient population in the same ZIP format. To obtain this, users must email accountmanagement@wrshealth.com — it is not self-service.

### Export File Structure

The downloaded ZIP (`ehi_documents.zip`) contains:

| File/Folder | Format | Description |
|-------------|--------|-------------|
| `Documents/` | Various (PDF, DOCX, XLS, XML, HTML, DAT, JPG, GIF, PNG) | Patient's supporting documents, attachments, lab results uploaded by practice. Filename convention references patient name and patient ID. |
| `Notes/` | HTML + CSS/JS/images | Encounter notes from patient visits, one HTML file per note. Includes CSS, images, and JavaScript for readable formatting. Filename references patient name, ID, date, and note type. |
| `Notes/PatientNoteFiles.csv` | CSV | Mapping file listing all exported notes. |
| `Notes/NOTES.LOG` | Text | Log of successfully exported notes and any errors during export. |
| `BillingReport.csv` | CSV | Financial transactions: patient info, transaction dates, charges, claims, descriptions, status. |
| `CCDA.xml` | XML (C-CDA) | Clinical data export compliant with HL7 C-CDA and USCDI v1. |
| `demographics.csv` | CSV | Patient key information, identification, contacts, insurance. |
| `PatientDocumentFiles.csv` | CSV | Mapping file listing all documents in the Documents folder. |
| `schedule.csv` | CSV | Encounter records: appointment date, provider, location, type, workflow, notes, note dates. |

### What the PDF Does NOT Include

- No column-level data dictionary for any of the CSV files (no field names, data types, or value sets)
- No schema files (no XSD, JSON Schema, OpenAPI, DDL)
- No sample export files or example data
- No documentation of the C-CDA profile beyond stating it follows USCDI v1
- No description of what specific clinical data categories are included in the C-CDA
- No API documentation (the export is UI-driven, not API-based)
- No field-level documentation for the BillingReport, demographics, or schedule CSVs

## Export Coverage Assessment

### Data Domain Coverage

WRS Health's EHI export takes a **hybrid approach**: structured CSV files for billing, demographics, and scheduling; a C-CDA XML for clinical data; HTML files for encounter notes; and raw document attachments.

**Domains that appear covered:**
- **Demographics & insurance**: Explicitly mentioned in `demographics.csv` (identification, contacts, insurance)
- **Billing/financial**: `BillingReport.csv` covers financial transactions, charges, claims, descriptions, and status
- **Encounter/visit history**: `schedule.csv` captures appointment dates, provider, location, type, workflow
- **Clinical notes**: HTML encounter notes exported individually per visit, across note types (visit notes, ENT notes, dermatology notes, internal medicine notes visible in screenshots)
- **Documents/attachments**: The `Documents/` folder exports all uploaded documents including lab results, external reports, images
- **Clinical summary (USCDI v1)**: `CCDA.xml` covers the standard US Core clinical data (problems, medications, allergies, immunizations, vitals, labs, procedures per USCDI v1)

**Domains with significant uncertainty or likely gaps:**
- **Medications**: The C-CDA presumably includes current medications per USCDI, but the full medication history, prescriptions, EPCS records, formulary/PBM data, and Surescripts medication history are not explicitly documented as being in the export. WRS Health's e-prescribing module stores prescription records, pharmacy info, and drug interaction data — none of this is mentioned.
- **Lab orders & results**: Lab results may be in the Documents folder as uploaded files, and some structured lab data is likely in the C-CDA. But the Lab Order Tracking System (order status, alerts, patient communications around orders) is not mentioned.
- **Allergies & immunizations**: Presumably in the C-CDA but not explicitly documented.
- **Problem list / diagnoses**: Presumably in the C-CDA but not explicitly documented.
- **Vitals**: Presumably in the C-CDA but not explicitly documented.
- **Care plans, goals, referrals**: Not mentioned. The product has referral management and health maintenance features — their data is not documented as exported.
- **Patient portal data**: Secure messages, prescription refill requests, patient-entered demographics, online payment records — none mentioned.
- **Telehealth data**: Virtual visit records, waiting room check-in data — not mentioned.
- **eFax records**: The product has integrated eFax. These documents may be in the Documents folder, but it's not explicitly stated.
- **Health maintenance/recall data**: Not mentioned.
- **Custom/specialty clinical data**: WRS Health supports 32+ specialties with specialty-specific templates and workflows. The encounter notes (HTML) would capture the narrative content, but any structured specialty-specific data fields are not documented as being exported in a computable format.

**Domains that are NOT EHI (correctly excluded):**
- Audit logs, system configuration, quality metrics, provider credentialing — none of these would be expected.

### The (b)(10) vs (g)(10) Question

This export is **genuinely a (b)(10) effort**, not a repackaged FHIR API. Evidence:
- The export produces a ZIP file with CSV files and documents — not FHIR resources
- It includes billing data (`BillingReport.csv`), which is beyond USCDI/US Core scope
- It includes raw documents and encounter notes, not just structured clinical data
- There is no mention of FHIR, Bulk Data API, or (g)(10) in the export documentation
- The C-CDA is included as one component alongside vendor-specific CSV files

However, the C-CDA component (which covers the USCDI clinical data) means the clinical coverage is effectively limited to what USCDI v1 defines — a well-known subset. The CSV files add billing and scheduling, but there's a significant middle ground of data the product stores (medications detail, lab order tracking, referrals, portal data, telehealth data, specialty-specific structured data) that is neither in the USCDI clinical summary nor in the documented CSV files.

### Export Format & Standards

The export uses a **mixed format**:
- **C-CDA XML**: Standard HL7 format for clinical summaries (USCDI v1). Well-understood by the industry but limited to the standard data classes.
- **CSV files**: Vendor-specific format for billing, demographics, and scheduling. No column definitions or schemas are provided, making import by a third party difficult without reverse-engineering the files.
- **HTML files**: Encounter notes rendered as web pages. Human-readable but not computable — a third party could not programmatically parse the clinical content without significant effort.
- **Raw files**: Documents/attachments in their original formats.

The format is appropriate for producing a human-readable export package. It would allow a patient or provider to review the record. But it would be challenging for a third party to programmatically reconstruct the patient record because:
1. The CSV columns are undocumented
2. The encounter notes are in HTML (narrative, not structured)
3. The C-CDA only covers the USCDI subset
4. Relationships between entities across files are not documented

### Documentation Quality

The documentation is **minimal but functional**. It is an 8-page PDF that explains *how* to perform the export (with screenshots) and *what files* the export produces (with a file-level description table). What it does not provide:

- **No field-level data dictionary**: The CSV files are described at the file level ("patient information, transaction dates, charges, claims") but individual columns are not listed or defined. A developer receiving `BillingReport.csv` would have to examine the actual file to understand the schema.
- **No data types or value sets**: No indication of date formats, code systems, enumerated values, or nullable fields.
- **No sample data**: No example exports or worked examples.
- **No schema files**: Nothing machine-readable.
- **No versioning detail**: The document is v1.0 from October 2023. No changelog beyond the initial entry.

The documentation reads as a compliance deliverable rather than a technical specification. It answers "what does the export contain?" at a high level but would not enable a developer to build an import tool without access to actual export files.

### Structure & Completeness

- **Granularity**: File-level only. The table describes each file/folder in the ZIP but provides no column names, data types, or field descriptions for any CSV.
- **Coded fields**: Not documented. The C-CDA references USCDI v1 but no custom value sets or code systems are mentioned.
- **Relationships**: The `PatientDocumentFiles.csv` and `PatientNoteFiles.csv` serve as mapping/index files for the Documents and Notes folders, but the document doesn't explain their columns or how they relate to other data.
- **Completeness**: The export appears to cover the major categories of patient data (clinical, billing, scheduling, documents) but the lack of field-level documentation makes it impossible to assess whether the coverage within each category is thorough.

### Overall Assessment

WRS Health has built a genuine (b)(10) EHI export that goes beyond simply repackaging their FHIR/C-CDA API. The inclusion of billing data, encounter notes, and raw documents shows an effort to export "all" patient data. The export mechanism is straightforward (UI-driven with a clear workflow).

However, the documentation is thin. An 8-page PDF with file-level descriptions and screenshots is a starting point, not a complete technical specification. The absence of any field-level data dictionary for the CSV files is a significant gap — without it, the export is a black box to anyone who hasn't actually run it. The reliance on HTML for encounter notes and C-CDA for clinical data means that much of the richly structured data WRS Health stores (32+ specialty templates, medication management details, lab order tracking, referral workflows) is either flattened into narrative HTML or limited to the USCDI v1 subset.

The multi-patient export requiring an email request to accountmanagement@wrshealth.com is also notable — while individual patient export is self-service, population-level export is manually facilitated.

## Access Summary
- Final URL (after redirects): https://www.wrshealth.com/onc-certification-and-costs
- Status: found
- Required browser: no (static HTML page, PDF is a direct download)
- Navigation complexity: one_click (EHI section is near the bottom of a compliance page, single PDF link)
- Anti-bot issues: none (standard User-Agent header works fine)

## Obstacles & Dead Ends
None. The URL loaded cleanly, the PDF downloaded without issues, and no authentication was required. The page is static HTML served from CloudFront/S3 — no JavaScript rendering, no accordions to expand, no login walls.
