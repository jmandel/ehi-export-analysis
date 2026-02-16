# MDLAND — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://mdland.net/iClinicEHR/ehiexport/
- CHPL IDs: 9814
- Product: iClinic v12.3
- Certification date: 2018-12-21

## Navigation Journal

The registered URL immediately redirects (HTTP 302) to a static PDF file:

```bash
curl -sI -L "https://mdland.net/iClinicEHR/ehiexport/" -H 'User-Agent: Mozilla/5.0'
# HTTP/2 302 → Location: /static/docs/ehiexport.pdf
# HTTP/2 200 → Content-Type: application/pdf, 250123 bytes
```

Downloaded the PDF:
```bash
curl -sL "https://mdland.net/iClinicEHR/ehiexport/" -H 'User-Agent: Mozilla/5.0' -o ehiexport.pdf
```

Verified: `file ehiexport.pdf` → PDF document, version 1.7, 2 pages. Author: Catherine Cai. Created 2023-12-01 via Microsoft Word for Microsoft 365.

Also checked:
- The mandatory disclosures page (`/iClinicEHR/Meaningful-use-disclosure/`) — no EHI-related content or links beyond standard certification criteria listings.
- The iClinic product page (`/iClinicEHR/`) — no links to data dictionaries, XML schemas, or additional EHI export documentation.
- The `/static/docs/` directory — returns 403 (not browsable).

No additional EHI export documentation was found beyond the single PDF.

## What Was Found

The entire EHI export documentation is a **2-page PDF** that describes the export feature at a high level:

**Export format:** Patient EHI is exported as a **ZIP file containing XML**, password-protected. The PDF references the W3C XML standard (https://www.w3.org/TR/xml/) as the format specification, but provides no vendor-specific XML schema, DTD, XSD, or sample XML file.

**Export scope:** The document states the export covers "all of a single patient's electronic health information" and also supports patient population export. Users can filter by:
- All Patients (including active, inactive, and deceased)
- All Active Patients
- Patients with Encounters
- Patients with DOB
- Specify Patient (single patient)

**User privileges:** Export access is restricted to authorized users through "Advanced Settings" — the feature is available under Settings → Advanced → Patient Data Export.

**Export workflow (4 steps):**
1. Log in as authorized user
2. Navigate to Settings/Advanced/Patient Data Export, select export scope, click Submit
3. Wait for MDLand IT to complete processing (10 minutes to several hours depending on data volume) — the user receives a notification with the unzip password
4. Download the ZIP file and extract the XML

**Screenshots:** Page 2 includes two screenshots:
1. The "Patient Data Export" dialog showing the Batch Editor with radio buttons for selecting export scope
2. A "Patient Data Export" list view showing batch IDs, creation dates, status (Downloaded/Finished), type, and Detail/Download links

**What is NOT documented:**
- No XML schema, DTD, XSD, or structure definition for the exported XML
- No data dictionary — no description of what XML elements/attributes are included
- No field-level documentation
- No sample XML output
- No list of what data domains or tables are included in the export
- No description of how relationships between entities are represented in the XML
- No encoding, character set, or namespace information beyond the generic W3C XML reference
- No API documentation (the export is a UI-driven process with server-side processing by MDLand IT)

## Export Coverage Assessment

### Data Domain Coverage

The PDF makes the regulatory claim that the export includes "all of a single patient's electronic health information stored at the time of certification." However, there is **no documentation whatsoever** of what data is actually included in the export.

Based on the product research, iClinic stores a substantial range of data:
- Patient demographics, insurance, photos, ID scans
- Clinical documentation (encounter notes, customizable templates)
- Medications and e-prescribing history (including EPCS)
- Allergies, problem/condition lists
- Lab orders and results
- Imaging orders and results
- Immunization records
- Documents (scanned, uploaded, consultation letters)
- Scheduling/appointment data
- Billing/claims data (electronic claims, statuses, payments, eligibility)
- Patient portal messages
- Telehealth visit records
- Care management data (CCM/RPM/TCM/CoCM/PCM)
- Population health analytics
- Public health reports
- Audit logs
- Clinical decision support alerts

**None of these domains are enumerated in the documentation.** The user is told they get "all" EHI in XML format, but there is no way to verify this claim from the documentation alone. There is no data dictionary, no table listing, no field listing, and no sample XML to inspect.

### Export Format & Standards

The export uses XML inside a password-protected ZIP file. The only format reference is the generic W3C XML specification — this tells a recipient essentially nothing about the structure of the data. XML is a meta-format; without a schema or documentation of the actual element structure, a third party cannot programmatically parse or import the data.

Key concerns:
- **No schema definition** (XSD, DTD, RelaxNG) is provided or referenced
- **No namespace documentation** — it's unclear if the XML uses any namespaces
- **No sample files** — there's no way to understand the structure without actually performing an export
- The format is **not FHIR, C-CDA, or any recognized healthcare standard** — it appears to be a proprietary XML format
- A third party receiving this export would need to reverse-engineer the XML structure to import the data

### Documentation Quality

This is **minimal compliance documentation** — 2 pages that describe how to trigger the export and what format the output is in, without documenting the content or structure of the export itself.

- **No data dictionary** at any level of granularity
- **No field definitions**, data types, value sets, or constraints
- **No worked examples** or sample data
- **No developer-oriented documentation** — a developer could not implement an import based on this documentation
- The documentation reads as a user guide for triggering the export, not as technical documentation of what the export contains
- The document was created in December 2023 (after certification) and hasn't been updated since

### Structure & Completeness

The documentation provides zero structural information about the export:
- No table/entity names
- No field/element names
- No data types
- No cardinality
- No value sets for coded fields
- No relationship documentation
- No versioning or change history

This is one of the least detailed EHI export documentations possible while still technically having a publicly accessible URL. The documentation answers "how do I trigger an export?" but not "what will the export contain?" or "how is the data structured?"

### (b)(10) vs (g)(10) Distinction

Notably, this documentation does **not** conflate (b)(10) with (g)(10). The export is described as a proprietary XML-based bulk export process, not a FHIR API. The vendor appears to have built a genuine (b)(10) export mechanism that is separate from their FHIR API. However, without a schema or data dictionary, it's impossible to assess whether the XML export truly covers "all" EHI or just a subset.

The fact that the export requires "MDLand IT" to complete processing (Step 3) suggests this may be a database dump that gets converted to XML on the server side, which is a reasonable approach for comprehensive data export — but the lack of documentation about the XML structure is a significant gap.

## Access Summary
- Final URL (after redirects): https://mdland.net/static/docs/ehiexport.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link (302 redirect to PDF)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The `/static/docs/` directory is not browsable (403 Forbidden)
- The mandatory disclosures page has no additional EHI export links
- The iClinic product page has no links to data dictionaries or schemas
- No XML schema, sample data, or data dictionary could be found anywhere on the mdland.net domain
