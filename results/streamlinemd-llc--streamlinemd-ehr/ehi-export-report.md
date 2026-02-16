# StreamlineMD, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://streamlinemd.com/wp-content/uploads/2023/10/StreamlineMD-EHR-EHI-Export.pdf
- CHPL IDs: 9974
- Mandatory disclosures page: https://streamlinemd.com/certified-ehr-software/

## Navigation Journal

The registered URL is a direct PDF download hosted on the vendor's WordPress site behind Cloudflare CDN.

```bash
curl -sI -L "https://streamlinemd.com/wp-content/uploads/2023/10/StreamlineMD-EHR-EHI-Export.pdf" \
  -H 'User-Agent: Mozilla/5.0'
# HTTP/2 200, content-type: application/pdf, content-length: 155440
# Last-Modified: Tue, 31 Oct 2023

curl -sL "https://streamlinemd.com/wp-content/uploads/2023/10/StreamlineMD-EHR-EHI-Export.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/StreamlineMD-EHR-EHI-Export.pdf
# Confirmed: PDF document, 2 pages, 155KB
```

Also checked the mandatory disclosures page at `https://streamlinemd.com/certified-ehr-software/` for any additional EHI export documentation. Found links to:
- The same EHI Export PDF (the only (b)(10) documentation)
- FHIR API Documentation at `https://patientportal.streamlinemd.com/FHIRReg/apidoc.html` — this is the (g)(10) FHIR Bulk Data API, a separate system from the (b)(10) EHI export. Not downloaded as it documents a different certification criterion.
- Several Real World Testing plans and results (2022–2025) — not EHI export documentation.

The FHIR API doc page describes a standard SMART on FHIR Bulk Export API using NDJSON output, SMART Backend Services auth, and system/*.read scopes. This is the (g)(10) standardized API and is clearly distinct from the (b)(10) C-CDA/PDF export described in the EHI Export PDF.

No embedded files or follow-on URLs found in the PDF itself (other than a link to healthit.gov's USCDI v1 page, which is an external standard reference).

## What Was Found

The entire EHI export documentation is a **single 2-page PDF** created on October 30, 2023, authored by Smitesh Shah (the developer contact listed in CHPL). It was produced from Microsoft Word.

### Content of the PDF

**Page 1**: Title page — "StreamlineMD EHR Version 15.0, 170.315 (b)(10) Electronic Health Information Export"

**Page 2**: A brief company description followed by three bullet points under the heading "170.315 (b)(10) Electronic Health Information Export":

1. StreamlineMD EHR Version 15.0 allows clients to export Clinical or Healthcare data for patient records without developer intervention. Data may be exported as **C-CDA** or **PDF**. The EHI export may be done for a single, multiple, or entire patient population using **C-CDA USCDI v1** requirements.
2. The use case for export may be for Single, Multiple, or All patient records.
3. The EHI may be exported in C-CDA, PDF, or both formats. The client selects the destination folder.

That is the entirety of the documentation. There is:
- No data dictionary
- No field-level documentation
- No schema or format specification
- No sample data or examples
- No screenshots of the export interface
- No instructions for performing the export
- No description of what data elements are included or excluded
- No mention of billing data, specialty clinical data, or any data beyond USCDI v1

## Export Coverage Assessment

### Data Domain Coverage

The documentation explicitly states the export uses **C-CDA USCDI v1** — which covers a defined (and limited) subset of clinical data:
- Demographics, problems, medications, allergies, lab results, vital signs, immunizations, procedures, clinical notes, care team, goals, assessments, health concerns, smoking status

**Missing or unmentioned data domains** from the product research:

| Domain | Status |
|--------|--------|
| Billing/claims data (CPT, ICD-10, charges, payments, denials) | **Not mentioned** — the product has deeply integrated billing/RCM, but the export only references USCDI v1 clinical data |
| Prior authorization records | **Not mentioned** |
| Inventory/supply usage data | **Not mentioned** |
| Procedure-specific documentation (500+ endovascular/interventional templates, procedure drawings) | **Not mentioned** — USCDI v1 procedure notes may capture some of this, but specialized drawing tools and template-specific data likely don't map to C-CDA |
| Scheduling/appointment data | Not mentioned (and not necessarily EHI) |
| Patient portal messages | **Not mentioned** |
| E-prescribing data | Partially covered via USCDI v1 medications |
| Referral data | **Not mentioned** |
| PACS/imaging references | **Not mentioned** |
| Quality/MIPS reporting data | Not mentioned (borderline — aggregate quality metrics are not EHI, but patient-level CQM data used for reporting may be) |

This is a textbook case of **(g)(10)/(b)(10) conflation**. The vendor has pointed to their C-CDA export (which satisfies Transitions of Care and clinical summary requirements) and called it their EHI export. The explicit reference to "USCDI v1 requirements" confirms this covers only the US Core Data for Interoperability subset, not "all electronic health information."

For a product whose core value proposition is tightly integrated billing and revenue cycle management, the absence of any billing data from the EHI export is a significant gap. The documentation doesn't even acknowledge that billing data exists, let alone explain how it would be exported.

### Export Format & Standards

- **Format**: C-CDA documents and/or PDF, exported to a local folder
- **Standard**: C-CDA with USCDI v1 data classes
- **Scope**: Single patient, multiple patients, or entire population
- **Delivery**: File-based export to a user-selected folder

C-CDA is a reasonable format for clinical summary data but cannot represent billing records, inventory data, or specialty-specific structured data like interventional procedure drawings. Even if the export works perfectly for its stated scope, the format choice inherently limits what can be exported.

The PDF export option likely renders the same clinical data as a human-readable document — useful for patients but not for data portability.

### Documentation Quality

This is among the most minimal EHI export documentation possible while still technically existing. Three bullet points on a single page. There is:

- **No data dictionary**: No listing of what data elements are included in the C-CDA export
- **No field definitions**: No description of how StreamlineMD-specific data maps to C-CDA sections
- **No schema or format spec**: Just "C-CDA USCDI v1" with a link to the USCDI reference
- **No examples**: No sample C-CDA documents or screenshots
- **No export instructions**: No step-by-step guide for performing the export
- **No error handling**: No description of what happens with incomplete or problematic data

A developer receiving a C-CDA from this system would need to reverse-engineer the content entirely. There is nothing in this documentation that goes beyond what any generic C-CDA consumer would already know.

### Structure & Completeness

- **Granularity**: Zero. Not even table names or data categories beyond "USCDI v1"
- **Value sets**: Not documented
- **Relationships**: Not documented
- **Versioning**: The PDF is dated October 2023 and references version 15.0. No change history.

## Access Summary
- Final URL (after redirects): https://streamlinemd.com/wp-content/uploads/2023/10/StreamlineMD-EHR-EHI-Export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none (Cloudflare CDN, but no challenge required)

## Obstacles & Dead Ends

None — the PDF downloaded cleanly on first attempt. The challenge here is not access but content: the documentation is too minimal to meaningfully describe the EHI export.

Notable: the vendor's certification page also documents a September 2025 cybersecurity incident that took their systems offline for multiple days. This is contextual information but does not affect the EHI export documentation assessment.
