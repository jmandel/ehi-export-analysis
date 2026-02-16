# Systemedx Inc — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.systemedx.com/dataExport.html
- CHPL IDs: 11536
- Product: Systemedx Clinical Navigator v2024.12
- Certification Date: 2024-11-26

## Navigation Journal

1. **Initial probe**: `curl -sI -L "https://www.systemedx.com/dataExport.html" -H 'User-Agent: Mozilla/5.0'` returned HTTP 200, Content-Type: text/html, Last-Modified: Thu, 05 May 2022 21:50:08 GMT. The page has not been modified since May 2022.

2. **Page download**: `curl -sL "https://www.systemedx.com/dataExport.html" -H 'User-Agent: Mozilla/5.0'` — 19,629 bytes of static HTML. No JavaScript rendering needed.

3. **Content examination**: The page is a simple static HTML page with inline text describing the export module. There are **no download links** — no PDFs, ZIPs, CSVs, JSON schemas, or any other downloadable artifacts on the page. The entire documentation is ~150 words of inline text.

4. **Link search**: `grep -oiE 'href="[^"]*\.(pdf|zip|xlsx|csv|json)"' page.html` returned nothing. No downloadable files linked from this page.

5. **MIPS/Mandatory Disclosures page** (`mipssolutions.html`): Found three links:
   - "Other Mandatory Disclosures" → `images/Mandatory Disclosures 2022.pdf` (downloaded)
   - "Real World Test Plans" → `images/RWT Website.zip` (not relevant to EHI export)
   - "DataExport" → `dataExport.html` (the same page already examined)

6. **Mandatory Disclosures PDF**: Downloaded and examined. 2-page cost transparency document listing fees for various capabilities (e-prescribing, patient portal, lab interfaces, API access at $10,000/year/app). Does not mention the (b)(10) data export module or any associated costs.

7. **FHIR API documentation** (separate system): Checked `API/Header.html` which links to:
   - APIIntro.html — introduction page, links to endpoint.json
   - AuthorizationTechnical.html — OAuth 2.0 authorization docs
   - AppRegistration.html — app registration process
   - SupportedResources.html — FHIR resource listing (standard US Core IG 4.0.0 / USCDI v1)
   - These are (g)(10) FHIR API documentation, not (b)(10) export documentation

8. **SupportedResources.html** lists standard USCDI v1 resources: AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Encounter, Goal, Immunization, Medication, MedicationRequest, MedicationDispense, Observation, Patient, Coverage, Procedure, ServiceRequest, Specimen, Provenance, SmokingStatus, VitalSigns, Location, Organization, Practitioner, BulkExport, Binary. All standard US Core — no custom resources or vendor-specific extensions.

9. **Alternative paths probed**: Checked `ehi.html`, `b10.html`, `bulk.html`, `export.html`, `data-dictionary.html`, `schema.html`, `datadictionary.html` — all returned 404.

10. **Wayback Machine**: CDX API shows 3 snapshots (2022-05-29, 2024-10-15, 2025-06-24), all returning the same content. The page has been unchanged since creation.

11. **Screenshot**: Captured full-page screenshot of dataExport.html.

## What Was Found

The EHI export documentation consists of a single static HTML page with approximately 150 words of inline text. There are no downloadable files, no data dictionary, no schema, and no field-level documentation.

### The Export Module

The export is accessed via a job stream called "CDAEXPORT" which appears in the application as "Data Export." It has three modes:

1. **All Patients** — exports all patients with configurable date range, output directory, and options for chart documents and human-readable CDA copy
2. **Select Patients** — same options but allows selecting a subset of patients manually or by appointment date range
3. **Single Patient** — same options but limited to one patient

### Export Format

The export produces:
- **CDA XML files** — patient demographics and "distinct chart data" (medications, problems, etc.)
- **CDA.html files** — human-readable HTML versions of the CDA documents
- **PDF documents** — patient chart documents, organized in a "Documents" folder with subfolders by document type

Files are organized into patient folders named: `LastName_FirstName_DOB_PatientID`

### What's NOT Documented

The documentation does not specify:
- Which CDA template or standard is used (C-CDA R2.1? Custom CDA? What sections?)
- What "distinct chart data" means — which data elements beyond "medications, problems, etc."
- What document types exist in the Documents folder
- What date ranges mean — encounter dates? modified dates?
- File encoding, character sets, or XML schemas
- How relationships between records are preserved
- Whether billing, surgical pathway, or practice management data is included
- Sample files or examples

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, Systemedx Clinical Navigator stores data across these domains:

| Domain | Covered by Export? | Evidence |
|--------|-------------------|----------|
| Patient demographics | Likely partial | Mentioned in CDA export ("patient demographics") |
| Clinical encounters/visit notes | Unknown | Not mentioned; may be in CDA or PDF documents |
| Medications | Likely partial | Explicitly mentioned ("medications") |
| Problems/diagnoses | Likely partial | Explicitly mentioned ("problems") |
| Lab results | Unknown | Not mentioned |
| Allergies | Unknown | Not mentioned (but standard CDA section) |
| Vital signs | Unknown | Not mentioned |
| Immunizations | Unknown | Not mentioned |
| Orders (lab, imaging) | Unknown | Not mentioned |
| Billing/claims data (CPT, ICD, claims, remittances) | **Likely absent** | No mention of billing data; CDA format does not naturally carry billing information |
| Scheduling/appointments | N/A | Operational data, not EHI |
| Surgical pathway data (case tracking, task lists) | **Likely absent** | No mention; this is a key product differentiator with no apparent export coverage |
| Patient portal messages | Unknown | Not mentioned |
| Quality measures data | Unknown | Not mentioned |
| Documents/images | Yes | Explicitly included as PDF exports |
| E-prescribing/PDMP data | Unknown | Not mentioned |
| Insurance/enrollment data | Unknown | Not mentioned |

The documentation is so sparse that most domains fall into "unknown." The export appears to be CDA-based, which inherently limits it to the CDA document model — primarily clinical summaries. The phrase "distinct chart data" is undefined and could mean anything from a full C-CDA with all sections to a minimal patient summary.

**Critical gap**: There is no mention of billing, claims, or financial data. For a product that includes full practice management with AI-assisted coding, claims submission, and surgical billing recovery, the absence of billing data from the export is a significant concern. Billing records are squarely within the designated record set.

**Critical gap**: The surgical pathways module — a differentiating feature that tracks surgical cases, billing recovery, and pre/post-op workflows — has no apparent representation in the export.

### Export Format & Standards

The export uses CDA XML, which is a recognized clinical document standard. However:

- The specific CDA template/profile is not documented. If it's C-CDA R2.1, the data would include standard sections (allergies, medications, problems, procedures, results, vital signs, immunizations, etc.) — but this is not confirmed.
- CDA is a document format designed for clinical summaries, not comprehensive data export. It does not naturally accommodate billing data, surgical pathway tracking, practice management data, or many types of specialty-specific clinical data.
- PDF export of chart documents is a reasonable supplement for unstructured content.
- The folder structure (`LastName_FirstName_DOB_PatientID`) is clear for organizing per-patient exports.

A third party receiving this export would have CDA XML documents (with unknown sections/completeness), human-readable HTML copies, and PDF chart documents. Without knowing the CDA template, it's impossible to assess whether the XML would enable meaningful data import into another system.

### Documentation Quality

The documentation quality is **very poor**:

- **No data dictionary**: There is no field-level documentation whatsoever
- **No schema**: No XSD, JSON Schema, or any machine-readable specification
- **No examples**: No sample CDA files, no sample export structure
- **No section inventory**: The CDA sections included are not listed
- **No value sets**: No coded terminology documentation
- **~150 words total**: The entire documentation is shorter than most email signatures
- **Unchanged since 2022**: The Last-Modified header shows May 2022, predating the current certification (November 2024). The documentation was not updated for the certification cycle.
- **No developer guidance**: A developer could not implement an import of this data based on this documentation alone. They would need to obtain a sample export and reverse-engineer it.

This documentation reads as a compliance checkbox — the absolute minimum needed to have a URL to register with CHPL. It describes how to trigger the export but not what the export contains.

### Structure & Completeness

- **Granularity**: The documentation provides zero field-level detail. It mentions "medications, problems, etc." as examples of chart data but does not enumerate sections, fields, data types, or cardinality.
- **Relationships**: No documentation of how records relate to each other.
- **Value sets**: No documentation of coded values.
- **Versioning**: No version history. Page unchanged since May 2022.

### (b)(10) vs (g)(10) Assessment

Systemedx has a clear separation between the (b)(10) and (g)(10) mechanisms:
- **(g)(10)**: FHIR R4 API with US Core IG 4.0.0 / USCDI v1 resources, OAuth 2.0 authorization, documented across multiple pages under `/API/`
- **(b)(10)**: CDA-based "CDAEXPORT" module with PDF document export, documented on the single `dataExport.html` page

The (b)(10) export is not repackaged FHIR — it's a genuinely separate CDA-based export mechanism. However, the CDA format may limit what data can be exported, and the documentation is far too sparse to determine whether the export actually covers "all electronic health information" as required.

The (g)(10) FHIR API covers standard USCDI clinical data. The (b)(10) export should cover everything beyond USCDI — billing, surgical pathways, practice management data — but there's no evidence it does.

## Access Summary
- Final URL (after redirects): https://www.systemedx.com/dataExport.html
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- No sitemap.xml or robots.txt on the domain (both 404)
- No downloadable artifacts linked from the export page
- Wayback Machine confirmed page has been unchanged since May 2022
- FHIR API documentation exists separately under `/API/` but is (g)(10), not (b)(10)
- Probed multiple alternative paths (ehi.html, b10.html, bulk.html, export.html, data-dictionary.html, schema.html, datadictionary.html) — all 404
