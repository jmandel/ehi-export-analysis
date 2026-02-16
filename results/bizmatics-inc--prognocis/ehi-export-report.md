# Bizmatics Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://prognocis.com/macra/#ehiexport
- CHPL IDs: 11738 (version 4.0, certified 2025-12-24), 8856 (version Denali 3.1, certified 2017-09-29)

## Navigation Journal

1. **Initial probe with curl** returned HTTP 403 — the site blocks direct curl requests (even with a standard User-Agent header and Referer). The 403 response body is 75KB of HTML.

```bash
curl -sI -L "https://prognocis.com/macra/#ehiexport" -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36' 2>&1
# Returns: HTTP/2 403, Content-Type: text/html
```

2. **Navigated via browser** to `https://prognocis.com/macra/#ehiexport`. The page loaded successfully — it's a WordPress-based MACRA/ONC compliance page. Despite the `#ehiexport` anchor, the page does not auto-scroll to any specific section (no matching `id` attribute in the DOM).

3. **Found the EHI export PDF link** in the page body. The relevant text reads:

> PrognoCIS Electronic Health Information Export functionality is ONC 2015 Edition Cures Update Certified, which allows users to export the health data for Single Patient or Patient Populations.

> ONC Certifications for Healthcare IT — Criteria '§170.315(b)(10) Electronic Health Information export PrognoCIS Support'.

The "ONC Certifications for Healthcare IT" link (uid=1_75) points to:
`https://prognocis.com/wp-content/uploads/2023/12/b-10-EHI-Export_PrognoCIS-Support.pdf`

4. **Downloaded the PDF via browser** — curl gets a 403, so the file was fetched using the browser's fetch API, base64-encoded, decoded, and stripped of leading garbage bytes. Verified as valid PDF 1.7 with `pdfinfo`.

5. **No other EHI-specific documentation** was found on the page. Other links on the page are for:
   - Multi-factor authentication use case support (§170.315(d)(13))
   - Certification disclosures / transparency PDF
   - Real World Testing plans and results (CY 2022–2025)
   - Predictive DSI / IRM summaries
   - MIPS/MACRA regulatory content
   - 2014 ONC HIT compliance page (separate, historical)

None of these relate to the EHI export mechanism itself.

## What Was Found

The EHI export documentation is a single 26-page PDF document:

**"§170.315(b)(10) Electronic Health Information export_Self Attestation Document"**
- Product: PrognoCIS, Version Denali 3.1
- Author: Neha Parmar
- Created: December 1, 2023
- 26 pages, 678 KB

### Export Mechanism

PrognoCIS provides two export paths:

1. **Single Patient Export**: Available directly to authorized users (those with the `CuresEHIExport` role). Users search for a patient, select data element checkboxes, and click EXPORT. The export runs in the background and the user is notified by email when ready. The exported ZIP file is then available under Settings → Configuration → Download Files → "Cures EHI Export" category.

2. **Patient Population Export**: Handled by the Bizmatics Data Migration Team. The user must contact `support@bizmaticsinc.com` to initiate. The vendor states this depends on "size of data, time and efforts required to manage the server resources."

### Export Format

Data is exported as a **ZIP file** containing:
- **XLS (Excel) files** for structured data (one per data element type)
- **TXT files** for structured data (parallel to XLS)
- **PDF files** for documents, progress notes, letters, legal documents, statements, and procedure notes
- **CCD exports** include HTML and XML (C-CDA) files

For data elements that include attached documents (Legal Documents, Other Documents, Encounter Attachments, Old Progress Notes, Encounter Progress Notes, Procedure Notes, Letters, Statements), the Excel file includes a "File" column with paths to PDF files organized in CHARTxx folders.

### Data Elements Covered (47 types)

The export covers 47 selectable data element types, organized into:

**Reference/Provider Data (1–7):**
Insurance Master, Medics (providers), Referring Doctor, Adjusters, Attorneys, Employers, Guarantor

**Patient Clinical Data (8–37):**
Patient Demographics, Patient Insurance, Vaccination, Health Maintenance, Family History, Past Medical History, Surgery, Allergy, Current Medication, Social History, Legal Documents, Other Documents, Encounter Attachments, Old Progress Notes, Messages, Future Appointments, Vitals, Diagnosis Codes, CPT Codes, HCPC Codes, CCD, Prescriptions, Lab Results, Radiology Results, Procedure Orders, Consults, Encounter Progress Notes, Procedure Notes, Letters, All Vitals, Lab Test Result Values

**Patient Administrative/Case Data (38–42):**
Patient Cases, Patient Notes, Patient Alert, Past Appointments

**Billing Data (43–47, conditional on billing module):**
Billing Ledger, Billing Claims, Billing Charges, Patient Advance, Statements

### Field-Level Documentation

The PDF provides explicit field-by-field documentation for 40 of the 47 data element types (1,180 total fields extracted). The remaining 7 either describe file attachments only (Legal Documents, Other Documents, Enc Attach Docs, Old Progress Notes) or have minimal detail (CCD, Billing Ledger, Statements).

Notable field counts:
- **Billing Claims**: 185 fields — extremely detailed claim-level export
- **Patient Demographics**: 131 fields — comprehensive demographic data
- **Billing Charges**: 123 fields — line-item billing detail
- **Enc Progress Notes**: 63 fields — detailed encounter records
- **Patient Insurance**: 60 fields
- **Patient Cases**: 41 fields (workers' comp / case management)

## Export Coverage Assessment

### Data Domain Coverage

**Well covered** — The export documentation maps convincingly to a genuine (b)(10) export. PrognoCIS appears to have done real work here rather than just pointing to their FHIR API. Key evidence:

- **Clinical data is comprehensive**: Demographics, problems, medications, allergies, vitals, labs, radiology, immunizations, encounters, prescriptions, procedures, consults — all present with field-level detail.
- **Billing data is present and deeply detailed**: Billing Claims (185 fields!), Billing Charges (123 fields), Patient Advance, Billing Ledger, and Statements are all included. This is not a USCDI-only export.
- **Documents and attachments are exported**: Progress notes, procedure notes, legal documents, "other documents," encounter attachments, and letters are all exported as actual files (PDFs) with metadata in Excel.
- **Workers' comp / case management data**: Patient Cases (41 fields including injury details, WCAB#, case managers, approved amounts) — specialty data beyond USCDI.
- **Administrative entities**: Insurance companies, referring providers, adjusters, attorneys, employers, guarantors — all the supporting entities needed to reconstruct the patient record.

**Potentially missing or unclear:**

- **Secure patient portal messages**: The "Messages" export (5 fields: ID, Date, Subject, Notes, Sender) appears to cover internal message compose — it's unclear if this captures patient portal secure messages or only internal staff messages.
- **E-prescribing details**: Prescriptions are exported with 20 fields, but the EPCS-specific data (two-factor auth records, Surescripts transaction IDs) is not explicitly mentioned.
- **Scheduling details beyond appointments**: The appointment exports (Future + Past) cover the essentials, but pre-authorization tracking and referral records are not listed as separate export types — they may be embedded in encounter or billing data.
- **Telemedicine encounter data**: No specific mention of telehealth-specific fields (video session metadata, etc.), though telehealth encounters likely export through the standard encounter progress notes pathway.
- **PrognoAI/AI Scribe data**: The vendor has AI features (ambient scribe, AI chat box) — it's unclear whether AI-generated draft notes are included in the export or only the finalized notes.
- **Document management metadata**: The "Attach Center" documents appear covered via Enc Attach Docs and Other Documents, but PrognoFax (electronic faxing) transmission records are not explicitly listed.

### Export Format & Standards

The export format is **proprietary but practical**: ZIP files containing Excel spreadsheets (one per data element), TXT parallels, and PDF files for documents. This is not FHIR, not C-CDA (except for the CCD element), and not any other recognized standard — it's essentially a structured database dump in a consumer-friendly format.

**Strengths of this approach:**
- XLS/TXT formats are universally readable
- Documents are preserved as actual files (PDFs)
- The export structure is flat and straightforward — no complex nested relationships to navigate
- Each data element type has its own file, making the export organized and navigable
- CCD provides a standards-based clinical summary alongside the detailed flat exports

**Weaknesses:**
- **No schema definition**: The field lists are documented in prose, not in a machine-readable schema (no XSD, JSON Schema, or formal DDL). A developer would need to parse the PDF to understand the format.
- **Relationships between entities are implicit**: There's no explicit foreign key documentation. For example, how does a Billing Claim reference a specific Encounter? The IDs exist in the data but the relationships aren't documented.
- **No data types or constraints**: Fields are listed by name only — no indication of data type (string, date, numeric), length constraints, nullability, or value sets for coded fields.
- **Document paths are relative**: File paths like `CHART01/PROG_53942.pdf` reference the folder structure inside the ZIP, but the naming convention isn't fully specified.

### Documentation Quality

**Moderate quality** — functional but not developer-grade.

**Positives:**
- Every data element type has a description explaining what data it covers
- 40 of 47 types have explicit field lists
- Notes about data filtering (e.g., "Only active patient's details are exported," "Void claims will not be exported") help set expectations
- The document explains the user workflow for triggering exports
- Role-based access control for the export is documented

**Negatives:**
- No data types, constraints, or cardinality for any field
- No value sets for coded fields (e.g., what are the valid "Status Code" values for a Billing Claim?)
- No sample export files or example data
- No formal schema (XSD, JSON Schema, etc.)
- No API specification — the export is a UI-driven process with no programmatic API
- The document is titled "Self Attestation Document" suggesting it was written primarily for certification compliance rather than as genuine developer documentation
- Patient Population export requires contacting vendor support — this is a compliance concern for (b)(10) which requires exports "without subsequent developer assistance"

### Structure & Completeness

- **Granularity**: Field-level (names only, no types/descriptions per field)
- **Coded fields**: Not documented with value sets
- **Relationships**: Not documented
- **Versioning**: Document is dated December 2023 for version Denali 3.1. The newer CHPL listing (11738, version 4.0, certified December 2025) presumably uses the same or updated export, but the PDF hasn't been visibly updated.

### The (b)(10) vs (g)(10) Question

This is a **genuine (b)(10) export**. Key indicators:
- The export format is XLS/TXT/PDF, not FHIR
- Billing data is front and center (185 fields for claims alone)
- Workers' comp case management data is included
- Reference entities (insurance companies, attorneys, adjusters) are exported
- The documentation makes no mention of FHIR resources, US Core, or USCDI as the organizing principle

This is one of the better (b)(10) implementations in terms of data breadth. The vendor clearly exports from their internal database tables rather than through a FHIR API facade.

### Notable Compliance Concern

The Patient Population Export requires contacting Bizmatics support and is handled by the "Data Migration Team." The (b)(10) regulation requires that population export "create an export of all the electronic health information" — while the regulation doesn't explicitly require the same self-service model as single-patient export, the operational dependency on the vendor team raises questions about timeliness and independence. The single-patient export, by contrast, is fully self-service.

## Access Summary
- Final URL (after redirects): https://prognocis.com/macra/#ehiexport
- Status: found
- Required browser: yes (site returns 403 to curl/wget)
- Navigation complexity: one_click (PDF link visible on main page)
- Anti-bot issues: Server returns 403 for non-browser requests; standard User-Agent and Referer headers insufficient

## Obstacles & Dead Ends
- **curl blocked**: All curl attempts returned 403, even with browser-like User-Agent and Referer headers. The site appears to use server-side bot detection (possibly checking for cookie handling or JavaScript execution). The PDF was successfully downloaded only through the browser.
- **No anchor scroll**: The `#ehiexport` fragment in the URL does not correspond to any element ID in the page DOM, so the page doesn't auto-scroll to the EHI section.
- **PDF metadata mismatch**: The PDF title in metadata is "Unprocessed Claims" (likely the author's working document title), not the actual document title shown on the cover page.
