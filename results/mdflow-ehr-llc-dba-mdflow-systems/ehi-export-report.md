# MDFlow EHR, LLC DBA: MDFlow Systems — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://www.mdflow.com/EHIExport.pdf
- CHPL IDs: 11459
- Product: MDFlow EHR and Patient Care Workflow Management System v8.0
- Certification date: 2024-04-02

## Navigation Journal

The registered URL is a direct PDF download:

```bash
curl -sI -L "https://www.mdflow.com/EHIExport.pdf" -H 'User-Agent: Mozilla/5.0'
# HTTP/2 200, Content-Type: application/pdf, Content-Length: 442126
```

Downloaded the primary file:
```bash
curl -sL "https://www.mdflow.com/EHIExport.pdf" -H 'User-Agent: Mozilla/5.0' -o EHIExport.pdf
```

Then checked the mandatory disclosures page (https://www.mdflow.com/www/mdflow-electronics-health-records.html) for additional documentation. Found these EHI-relevant links in the compliance section near the bottom of the page:

1. "EHI Export Iinformation" → https://www.mdflow.com/EHIExport.pdf (same as registered URL)
2. "EHI B10 Export" → https://www.mdflow.com/www/pdf%20files/EHI%20B10-Export.pdf
3. "API Documentation (g7910)" → https://www.mdflow.com/www/pdf%20files/API%20Documentation%20(g7910).pdf
4. "Json" → https://www.mdflow.com/www/pdf%20files/ValidURLs.json

Downloaded all three additional files:
```bash
curl -sL "https://www.mdflow.com/www/pdf%20files/EHI%20B10-Export.pdf" -o EHI-B10-Export.pdf
curl -sL "https://www.mdflow.com/www/pdf%20files/API%20Documentation%20(g7910).pdf" -o API-Documentation-g7910.pdf
curl -sL "https://www.mdflow.com/www/pdf%20files/ValidURLs.json" -o ValidURLs.json
```

Also captured a full-page screenshot of the mandatory disclosures page.

## What Was Found

### EHIExport.pdf (registered URL — 1 page, v8.0)
A single-page PDF with the MDFlow logo and a brief description of the EHI export. The complete text states:
- The export contains data stored in the patient's chart in the SQL database
- Supported formats: C-CDA, CSV text file, or PDF
- The **primary** export format is C-CDA
- CSV and PDF are available for "special and customized requests"
- Can export single patient or group of patients
- ZIP compression is used for large files

No data dictionary, no field definitions, no schema, no sample data, no screenshots, no procedural instructions.

### EHI B10-Export.pdf (1 page, v8.1)
An even more minimal document than the registered PDF. For version 8.1, it states:
- The export contains data from the patient's chart
- Multiple file formats are used
- ZIP is used as the archive format
- C-CDA is the health information exchange format
- The export file is a ZIP containing ZIP files of C-CDAs
- Each patient encounter has a C-CDA in the ZIP archive

This is marginally more specific — it clarifies the structure as a ZIP of per-encounter C-CDA ZIPs — but still provides no data dictionary or field-level documentation.

### API Documentation (g7910).pdf (58 pages, v8.0)
A comprehensive FHIR API document covering the SMART on FHIR authentication flow and individual FHIR resource endpoints. This is the (g)(7)/(g)(9)/(g)(10) documentation, **not** the (b)(10) EHI export. It covers:
- SMART App Launch with OAuth 2.0 (standalone, EHR-embedded, backend services)
- Symmetric and asymmetric authentication
- Individual FHIR R4 resource endpoints: Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, ImplantableDevice, DiagnosticReport/ClinicalNotes/DocumentReference, Observation (labs), Goal, Immunization, Medication, SmokingStatus, Procedure, Provenance, VitalSigns
- Complete Patient Summary (CCDA) endpoint
- Search for Patient, Encounter
- Error handling

The FHIR resources listed are the standard US Core / USCDI v1 set. There is no mention of bulk data export being used for (b)(10), and this document is clearly the (g)(10) standardized API documentation.

### ValidURLs.json
A FHIR Bundle (type: collection) containing two Endpoint resources and two Organization resources. This lists the FHIR server endpoints (https://fhir.mdflow.com:8443/fhirserver/fhir/) for two test organizations. This is a (g)(10) Service Base URL artifact, not related to EHI export.

## Export Coverage Assessment

### Data Domain Coverage

The EHI export documentation is profoundly vague — it says only that the export "contains data stored in the patient's chart in the SQL database" without specifying what data elements, tables, or clinical domains are included. The primary format is C-CDA per encounter, with CSV and PDF available "for customized requests."

**The critical question is what a C-CDA per encounter actually contains.** Standard C-CDA documents (CCD or Continuity of Care Document) typically include: demographics, problems, medications, allergies, immunizations, vital signs, procedures, lab results, and clinical notes for an encounter. This would cover core clinical data but leaves major gaps relative to the full designated record set.

Based on the product research, MDFlow stores the following data domains. Assessment of likely export coverage:

| Domain | Likely in C-CDA export? | Notes |
|--------|------------------------|-------|
| Patient demographics | Yes | Standard C-CDA section |
| Problem lists / diagnoses | Yes | Standard C-CDA section |
| Medications / e-prescribing | Yes | Standard C-CDA section |
| Allergies | Yes | Standard C-CDA section |
| Lab results | Yes | Standard C-CDA section |
| Vital signs | Yes | Standard C-CDA section |
| Immunizations | Yes | Standard C-CDA section |
| Procedures | Yes | Standard C-CDA section |
| Clinical notes / encounter documentation | Partially | C-CDA can include narrative sections |
| HCC/MRA scores, Star Ratings, HEDIS | **Unclear** | Not standard C-CDA content |
| Scheduling / appointments | **No** | Not part of C-CDA |
| Telemedicine session records | **Unclear** | May be in notes, but session recordings likely not |
| Billing / charges / claims | **No** | Not standard C-CDA content |
| PBM history (pharmacy benefits) | **Unclear** | Medication history may partially cover this |
| Referrals / utilization management | **Unclear** | May be in C-CDA referral sections |
| Secure messages | **No** | Not part of C-CDA |
| Scanned documents | **Unclear** | C-CDA can embed documents, but unclear if MDFlow includes them |
| Quality measures (PQRS/MIPS) | **No** | Not standard C-CDA content |

The documentation mentions CSV and PDF as alternative formats for "customized requests," which suggests the vendor may provide broader exports on request, but there is no documentation of what those CSV or PDF exports contain, what fields are included, or how to request them.

### Export Format & Standards

The export uses **C-CDA** (Consolidated Clinical Document Architecture) as its primary format, packaged as a ZIP file containing per-encounter C-CDA ZIP archives. C-CDA is a well-established HL7 standard, which is good for interoperability — but it is a **clinical summary** standard, not a comprehensive database export format.

C-CDA was designed for transitions of care, not for complete EHI export. It has well-defined sections for core clinical data (the same data domains covered by USCDI/US Core) but does not naturally accommodate:
- Billing and financial data
- Administrative data (scheduling, referral tracking)
- Risk adjustment and quality measurement data
- Custom workflow data specific to value-based care operations

This creates a strong suspicion that MDFlow's (b)(10) export is functionally equivalent to their (g)(10) clinical data — just packaged as C-CDA documents rather than via FHIR API. The documentation does not describe any mechanism for exporting data that falls outside standard C-CDA sections.

A third party receiving this export could reconstruct a clinical summary per encounter, but would likely miss billing records, quality scores, custom assessments, and operational data that MDFlow stores as part of the patient's designated record set.

### Documentation Quality

The documentation quality is **extremely poor** — among the worst possible for a certified product:

- The registered EHI Export PDF is a single page with 5 bullet points and no technical substance
- The supplemental B10-Export PDF is also a single page with even less content
- There is **no data dictionary** — zero documentation of what specific data elements are exported
- There are **no field definitions**, data types, constraints, or value sets
- There are **no sample files or worked examples**
- There are **no screenshots** of the export interface
- There are **no procedural instructions** for performing an export
- There is **no schema documentation** for the C-CDA templates used
- A developer could not implement an import of this data based solely on this documentation — they would need to know C-CDA generically, then examine actual export files to understand MDFlow's specific implementation

The API Documentation PDF (58 pages) is by contrast quite detailed for the FHIR (g)(10) API, with full endpoint descriptions, request/response examples, and OAuth2 flow documentation. This disparity suggests the vendor invested real effort in the (g)(10) API but treated (b)(10) as a compliance checkbox.

### Structure & Completeness

- **Field-level documentation**: None. Not even table or section names.
- **Coded fields / value sets**: Not documented.
- **Relationships between entities**: Not documented. The per-encounter ZIP structure is described but nothing about how encounters relate to each other or to the patient.
- **Versioning**: The original PDF references v8.0, the supplemental B10-Export.pdf references v8.1. No change history.

### The (b)(10) vs (g)(10) Assessment

While MDFlow's EHI export uses C-CDA rather than FHIR, the same conceptual problem applies: C-CDA, like FHIR US Core, covers the standard clinical summary data but not the full designated record set. MDFlow's product stores significant data beyond what C-CDA naturally represents — particularly HCC/MRA risk adjustment scores, quality measures, scheduling data, and value-based care workflow data that is central to the product's purpose.

The vendor mentions CSV and PDF as alternative export formats for "customized requests," which could theoretically cover broader data domains, but these are undocumented. There is no data dictionary, no field list, no sample — nothing to indicate what a CSV export contains or how to interpret it.

## Access Summary
- Final URL (after redirects): https://www.mdflow.com/EHIExport.pdf (no redirect)
- Status: found
- Required browser: no
- Navigation complexity: direct_link (for registered URL); one_click from mandatory disclosures page for supplemental files
- Anti-bot issues: none

## Obstacles & Dead Ends
- No obstacles encountered. All URLs returned HTTP 200 with expected content types.
- The MFA PDF (mfa.pdf) linked from the same disclosures page is about multi-factor authentication, not EHI export — skipped.
- The link text on the disclosures page contains a typo ("Iinformation") and the MFA link text appears garbled ("Multi-Factor Authentication IJson URLEHI Export Iinformation"), suggesting sloppy HTML editing.
