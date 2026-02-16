# Keiser Computers, Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://drsdoc.com/DataExport
- CHPL IDs: 11072
- Product: Drs Enterprise 12
- Certification date: 2022-12-13

## Navigation Journal

1. **Initial probe** — `curl -sI -L "https://drsdoc.com/DataExport"` returned HTTP 405 (Method Not Allowed, HEAD not supported on this ASP.NET Kestrel endpoint). Server: Kestrel, X-Powered-By: ASP.NET.

2. **GET request** — `curl -sL "https://drsdoc.com/DataExport" -H 'User-Agent: Mozilla/5.0'` returned an 8.3 KB HTML page with a brief introduction paragraph and a single link to the export documentation PDF.

3. **Found PDF link** — The page at `/DataExport` contains:
   - A brief introduction: "Drs® Enterprise provides the capability to export Electronic Health Information (EHI) for a single patient as well as for multiple patients in compliance with 170.315(b)(10)..."
   - A single resource link: `https://drsdoc.com/Export_data.pdf` labeled "EHI Export Documentation"

4. **Downloaded PDF** — `curl -sL 'https://drsdoc.com/Export_data.pdf' -o Export_data.pdf` — confirmed as a 10-page PDF document (1,001,575 bytes), created with Microsoft Word 2010, dated November 7, 2023.

5. **Checked Certification page** — `curl -sL "https://drsdoc.com/Home/Certification"` — This is the vendor's main certification hub. It lists all certified criteria and links to:
   - `/DataExport` for (b)(10) EHI Export (already visited)
   - `/FHIRapi` for API documentation (SMART on FHIR / (g)(10) — separate from EHI export)
   - `/CostsAndRequirements.htm` for costs/requirements
   - `/RWT` for real-world testing
   No additional EHI export documentation was found beyond the PDF.

6. **Checked FHIR API page** — Confirmed `/FHIRapi` is the (g)(10) standardized API documentation, not part of the (b)(10) EHI export. It links to a "SmartOnFHIR API Documentation" resource — unrelated to the EHI export mechanism.

7. **Checked PDF for embedded URLs and attachments** — No embedded files. Only URLs are to HL7.org C-CDA specifications (external standards, not downloaded per instructions).

8. **Took screenshot** of the DataExport landing page and rendered PDF pages for visual inspection.

## What Was Found

The EHI export documentation is a single 10-page PDF (`Export_data.pdf`) that describes a hybrid export format:

### Export Format
The export produces **two types of data per patient**:

1. **C-CDA XML file** (`account_ccda.xml`) — Contains the patient's clinical EHI data (demographics, problems, medications, allergies, etc.) "in compliance with the USCDv1 standard." The C-CDA content itself is documented only by reference to the HL7 C-CDA 2.1 standard — no vendor-specific field mapping or customization details are provided.

2. **Proprietary XML sidecar files and raw documents** — Additional patient data that doesn't fit in C-CDA is exported in vendor-specific XML formats:
   - `account_tasks.xml` — Tasks linked to the patient account
   - `<Document_ID>_info.xml` — Metadata for each exported document (with nested office notes, tasks, and "Drs Data Lookup" elements)
   - `<Document_ID>.<ext>` — The actual document files (PDF, TIF, RTF, XML, etc.)
   - `Account_U.img` — Patient photo
   - Fax export: `Fax_inbox.xml`, `Fax_outbox.xml`, and TIF fax files organized by year/month

### Directory Structure
Patient data is organized in a hexadecimal folder structure based on Account ID, using 4 levels of 2-hex-digit folders. Example: Account ID 9999 → hex 270F → path `00\00\27\0F`.

### Documentation Detail
The PDF documents 7 XML entities across the sidecar files:
- **Document** (15 fields) — document metadata including folder location, creation info, user-defined fields
- **office_notes** (13 fields) — office notes linked to documents
- **tasks** (14 fields) — tasks linked to accounts or documents
- **doc_data** (8 fields) — "Drs Data Lookup" discrete data with LOINC codes, conversion types, and field types
- **loinc_code** (1 field) — nested LOINC description element
- **fax_inbox** (10 fields) — inbox fax metadata
- **fax_outbox** (10 fields) — outbox fax metadata

Two enumerators are documented:
- **convert_type** — 12 unit conversion types (inches, pounds, centimeters, etc.)
- **TFieldType** — 20 Delphi-derived field types (ftString, ftInteger, ftBoolean, etc.)

XML examples are provided for each entity except the fax entities.

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, Drs Enterprise stores clinical documentation, prescriptions, documents/images, lab results, charges/billing codes, tasks/messages, forms, scheduling data, patient portal data, and fax communications.

**Clearly covered:**
- **Clinical data** (demographics, problems, medications, allergies) — via C-CDA, though only described by reference to "USCDv1 standard"
- **Documents** — all chart documents exported as original files (PDF, TIF, RTF, etc.) with XML metadata including folder location, office notes, and user-defined fields
- **Tasks/messages** — exported in account_tasks.xml and document-linked task structures
- **Office notes** — exported as part of document metadata
- **Discrete data lookups** — clinical observations with LOINC codes exported in doc_data elements (the example shows BMI)
- **Patient photo** — Account_U.img
- **Faxes** — inbox and outbox faxes with metadata and TIF files

**Unclear or likely missing:**
- **Prescriptions / e-prescribing data** — Not explicitly mentioned in the export documentation. The C-CDA would contain medication lists, but detailed prescribing data (SureScripts transaction history, prescription status, refill data) may not be fully captured. The vendor describes integration with DrFirst Rcopia for e-prescribing — data managed by DrFirst may be outside the export scope.
- **Lab results** — Partially covered via C-CDA (which includes results) and potentially as document exports if stored as scanned images. However, discrete lab data received via HL7 interface is not specifically addressed in the proprietary sidecar format.
- **Charge capture / billing data** — Not mentioned in the export documentation. The product research notes that Drs Enterprise captures charges during visits and has an EOB Manager, but the export documentation makes no reference to billing data, charges, CPT/ICD codes, or financial information. This is a significant gap, though the product research also notes that core billing/claims reside in external PM systems (MicroMD, Medisoft, etc.), so the charge capture and EOB data within Drs Enterprise itself should still be exported.
- **Forms data** — Auto-populated clinical and administrative forms are not specifically mentioned. If stored as documents, they would be exported as files; if stored as discrete form data, it's unclear.
- **Family health history** — Certified for (a)(12) but not mentioned in export documentation beyond what C-CDA captures.
- **Implantable device data** — Certified for (a)(14) but not specifically mentioned.
- **Scheduling/appointment data** — Not mentioned in the export (though this is not necessarily EHI — see scope reference).
- **Patient portal data** — Not specifically mentioned.

**Genuinely absent from documentation:**
- **Charge capture data and EOBs** — The product stores charges and EOB data, which are billing records about patients (part of the designated record set). The export documentation does not mention these.

### Export Format & Standards

The hybrid approach is sensible:
- **C-CDA 2.1** for standard clinical data — this is a recognized standard for clinical document exchange, widely understood.
- **Proprietary XML** for data that doesn't fit in C-CDA (tasks, document metadata, fax logs, discrete data lookups). This is a reasonable approach for a (b)(10) export since much of what an EHR stores doesn't map to C-CDA sections.

However, the C-CDA portion is described only by reference to the USCDv1 standard without any vendor-specific mapping documentation. A third party receiving this export would know the C-CDA structure from the HL7 standard but would not know:
- Which C-CDA sections Drs Enterprise actually populates
- How vendor-specific data maps to C-CDA elements
- What data might be in the sidecar XML files that overlaps with or supplements the C-CDA

The proprietary XML format is well-documented — field names, types, descriptions, optionality, and examples are all provided. A developer could parse these files without difficulty.

The `doc_data` / "Drs Data Lookup" structure is interesting — it appears to be how the system stores discrete clinical observations (like vitals) with LOINC codes. The TFieldType enum values (ftString, ftFMTBcd, ftDateTime, etc.) are Delphi data types, revealing the product's underlying technology stack.

### Documentation Quality

**Strengths:**
- Clear and readable 10-page document
- Well-structured tables for each XML entity with field names, types, descriptions, and optionality flags
- XML examples provided for most entities
- Directory structure clearly explained with hexadecimal encoding examples
- Error handling documented (export_xml folder with errors_<Session_ID>.xml)
- The document is dated (November 2023) and attributed

**Weaknesses:**
- The C-CDA portion — which is the core clinical data export — is documented entirely by reference to the external HL7 standard. No vendor-specific mapping or field-level documentation for what goes into account_ccda.xml.
- No sample export files or test data provided
- No user guide or instructions for how to actually perform the export within the Drs Enterprise application
- No documentation of what clinical data categories map to which export components
- Value sets for coded fields (like task_priority_desc, task_type_desc, receive_status, sent_status) are not enumerated — only the TFieldType and convert_type enumerators are documented
- No versioning or change history beyond the single document date

### Structure & Completeness

The documentation is moderately granular:
- **Table/entity names**: Yes — 7 entities documented
- **Field names**: Yes — 71 fields total
- **Data types**: Yes — including Delphi-native types
- **Descriptions**: Yes — brief but adequate
- **Optionality**: Yes — each field marked optional or required
- **Value sets**: Partial — enumerators for TFieldType and convert_type, but text-typed categorical fields (like task_type_desc, task_priority_desc) lack value set documentation
- **Relationships**: Implicit — doc_id links documents to tasks; account_id links to patient accounts
- **Examples**: Yes for most entities — helpful XML snippets

### Overall Assessment

This is a genuine (b)(10) effort — not a repackaged (g)(10) FHIR API. The vendor has built a custom export that goes beyond standard C-CDA by including documents, tasks, office notes, discrete data lookups with LOINC codes, and faxes. The proprietary XML sidecar format is well-documented with field-level detail.

However, there are notable gaps:
1. The C-CDA content (the largest clinical data component) has no vendor-specific documentation
2. Billing/charge capture data and EOBs are absent from the export documentation despite being stored in the product
3. No export instructions, sample files, or user guide

For a small vendor (~40 years old, likely a handful of employees), this is a reasonable effort that shows awareness of the (b)(10) requirement. The documentation quality is above average for the proprietary XML portions but thin for the C-CDA core. A third party could reconstruct the sidecar data from this documentation, but would need the C-CDA standard itself plus trial-and-error to understand the account_ccda.xml content.

## Access Summary
- Final URL (after redirects): https://drsdoc.com/DataExport
- Status: found
- Required browser: no
- Navigation complexity: one_click (landing page → single PDF link)
- Anti-bot issues: HEAD request returns 405 (ASP.NET/Kestrel), GET works fine with standard User-Agent

## Obstacles & Dead Ends
- HEAD request to `/DataExport` returns HTTP 405 (Method Not Allowed). This is a Kestrel server quirk, not a real obstacle — GET works fine.
- The FHIR API page (`/FHIRapi`) was checked but confirmed as (g)(10) documentation, unrelated to the (b)(10) EHI export.
- No additional documentation was found on the Certification page beyond the single PDF link.
