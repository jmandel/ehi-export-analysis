# Medcare MSO — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://docs.healusehr.com/EHI
- CHPL IDs: 11495
- Product: HealUs EHR v1.0
- Certification date: 2024-07-15

## Navigation Journal

**1. Initial probe:**
```bash
curl -sI -L "https://docs.healusehr.com/EHI" -H 'User-Agent: Mozilla/5.0'
```
Result: HTTP 200, Content-Type: text/html. The URL serves an Angular SPA (single-page application) with `<app-root>` and JavaScript bundles.

**2. Fetched and examined the HTML source:**
The page is an Angular app that renders a PDF viewer in-browser. The HTML contains no substantive content — everything is rendered by JavaScript.

**3. Opened in browser:**
The Angular SPA renders a knowledge hub with a left sidebar containing sections:
- All APIs (Patient Access API, FHIR API)
- Security
- Data Export > **Electronic Health Information** (selected by default at /EHI)
- Predictive DSIs

The main content area displays an embedded PDF viewer showing "170.315(b)(10) Electronic Health Information Export".

**4. Identified the underlying PDF via network requests:**
```bash
# The Angular app loads this PDF:
curl -sL "https://docs.healusehr.com/assets/docs/EHI.pdf" -H 'User-Agent: Mozilla/5.0' -o downloads/EHI.pdf
```
The PDF is 6 pages, 681KB. Created 2024-04-22, authored by "Ramsha Rasheed" in Microsoft Word 2016, processed through ilovepdf.com.

**5. Searched the Angular main.js bundle for other assets:**
Found three PDF assets in the bundle:
- `/assets/docs/EHI.pdf` — the EHI export documentation (downloaded)
- `/assets/docs/Security.pdf` — MFA documentation (not EHI-related)
- `/assets/docs/PDSI.pdf` — Predictive DSI documentation (not EHI-related)

**6. Checked the FHIR API section:**
Since the EHI PDF claims FHIR is one of the export mechanisms, I checked the FHIR API page. It documents the (g)(10) standardized API with base URL `https://fhirapi.medcaremso.com/api/R4/`. Fetched the CapabilityStatement to identify supported FHIR resources.

```bash
curl -s "https://fhirapi.medcaremso.com/api/R4/metadata" -H 'Accept: application/fhir+json' -o downloads/fhir-capability-statement.json
```

The CapabilityStatement identifies it as a "Medcare Reference Server for US Core Implementation Guide v6.0.11 based on HAPI FHIR R4 Server" that instantiates `us-core-server` and `bulk-data` capability statements.

Supported FHIR resource types (28 total): AllergyIntolerance, CarePlan, CareTeam, Condition, Coverage, Device, DiagnosticReport, DocumentReference, Encounter, Endpoint, Goal, Group, Immunization, Location, Medication, MedicationDispense, MedicationRequest, Observation, Organization, Patient, Practitioner, PractitionerRole, Procedure, Provenance, RelatedPerson, ServiceRequest, Specimen.

This is a standard US Core resource set — no custom resources, no billing-specific resources, no specialty extensions.

**7. Checked the ONC mandatory disclosures page:**
```bash
curl -sL "https://healusehr.com/onc-certified/" -H 'User-Agent: Mozilla/5.0' -o /tmp/healus-onc.html
```
The mandatory disclosures page (WordPress/Elementor site) mentions "EHI Export Version 1.0" and links back to `https://docs.healusehr.com/EHI`. No additional documentation or downloads found there.

## What Was Found

The entire EHI export documentation consists of a single 6-page PDF (5 pages of content + 1 blank page). The document describes:

### Export Mechanisms
HealUs EHR provides four export channels:

1. **C-CDA Export** — Clinical data via Consolidated CDA (HL7 CDA R2 IHE Health Story Consolidation DSTU 1.1). Available for both single patient and bulk export.

2. **FHIR Export** — Clinical data via HL7 FHIR US Core IG STU 4.0.0 and FHIR Bulk Data Access v1.0.1. Available for both single patient and bulk (population) export. The document states this is "compliant with the specifications outlined in § 170.315(b)(10)(ii)."

3. **PDF Export** — Lab results, encounters, appointments, imaging results, documents, procedure results, referrals, and advance directives in "interpretable, machine-readable PDF."

4. **CSV Export** — Patient demographics and appointments.

### Export Workflow
The document describes identical step-by-step procedures for both single patient and bulk export:
- Navigate to "Data Export" in quick links
- Select patient(s) and date range
- Optionally enable password protection
- Click Process, select sections, click Proceed
- Download or share when complete

Practice administrators can approve export requests. Users can perform exports "at any time without the developer assistance" and files are exported "in real time."

### Data Categories Described
The PDF lists these data categories with their export formats:
| Category | Format |
|----------|--------|
| Patient Demographics | CSV |
| Appointments | PDF and CSV |
| Lab Results | PDF |
| Imaging Results | PDF |
| Procedure Results | PDF |
| Encounters | PDF |
| Referrals | PDF |
| Advance Directives | PDF |
| Documents (lab, imaging, scanned/uploaded) | PDF |
| Clinical Data (via C-CDA) | XML (C-CDA) |
| Clinical Data (via FHIR) | JSON (FHIR) |

### What Is NOT Described
- No data dictionary or field definitions for any export format
- No CSV column specifications for demographics or appointments
- No sample export files or example data
- No schema files (XSD, JSON Schema, OpenAPI)
- No description of what fields appear in the PDF exports
- No documentation of encounter data structure
- No billing data mentioned anywhere
- No description of what "clinical data" specifically includes beyond the C-CDA/FHIR standards references
- No description of relationships between exported entities

## Export Coverage Assessment

### Data Domain Coverage

Comparing the EHI export documentation against the product research findings:

**Clearly covered (at least mentioned):**
- Patient demographics (CSV export)
- Appointments (PDF + CSV)
- Lab results (PDF export)
- Imaging results (PDF export)
- Procedure results (PDF export)
- Encounters (PDF export)
- Referrals (PDF export)
- Advance directives (PDF export)
- Documents/scanned records (PDF export)
- Clinical data via C-CDA (which covers: problems, medications, allergies, immunizations, vitals, care plans per the HL7 standard)
- Clinical data via FHIR (US Core resources — see CapabilityStatement)

**Missing or not mentioned:**
- **Billing and claims data** — HealUs EHR's parent company Medcare MSO is primarily a billing/RCM company. The EHI documentation makes zero mention of billing records, charges, claims, payments, or insurance information. If billing data is stored in HealUs EHR (as opposed to the separate Maximus PMS), this is a significant gap. If billing lives exclusively in Maximus, it may be out of scope for the HealUs EHR (b)(10) obligation.
- **E-prescribing data** — The product is certified for e-prescribing via DrFirst integration (criterion b)(11)), but the export documentation doesn't mention prescription transmission records.
- **Medication administration records** — Beyond what's captured in C-CDA medication lists.
- **Insurance/coverage information** — Not mentioned (the FHIR CapabilityStatement does list Coverage as a supported resource, but the EHI PDF doesn't mention it).
- **Clinical decision support alerts and responses** — The product has CDSS capabilities but no mention of exporting CDS interaction data.
- **Patient portal data** — The product has a patient portal (e)(1) with view/download/transmit, but patient-submitted health information (e)(3) is not mentioned in the export.
- **Clinical quality measure data** — The product supports 7 CQMs but no mention of exporting measure results.
- **Immunization registry submissions** — The product transmits to registries but doesn't mention exporting these records specifically (though they may be in the C-CDA export).
- **Direct messaging records** — The product supports Direct messaging (h)(1) but no mention of exporting message content.

### Export Format & Standards

The export uses a **mixed-format approach**: C-CDA XML and FHIR JSON for clinical summaries, CSV for demographics and appointments, and PDF for most other data categories.

**Critical concern: heavy reliance on PDF.** The document describes most data categories (lab results, imaging, encounters, referrals, advance directives, procedure results) as exported in PDF format. While the document calls these "interpretable, machine-readable PDF," PDF is fundamentally a presentation format, not a computable data format. A third party receiving PDF exports of lab results would have to perform OCR or manual data entry to ingest the data — defeating the purpose of an electronic export. This is a significant weakness in the export design.

**The (b)(10) vs (g)(10) issue:** The document explicitly references both C-CDA and FHIR US Core as export formats, which are the same standards used for (g)(10) certification. The FHIR CapabilityStatement confirms a standard US Core resource set with no custom resources. The FHIR export component of this EHI export is essentially the same as the (g)(10) standardized API, which means it only covers the USCDI clinical data subset. The additional data categories (appointments, referrals, advance directives, encounters, documents) are exported as PDF — which is a genuine attempt to go beyond USCDI, but in a non-computable format.

**CSV for demographics** is reasonable and computable, but the documentation provides no column specification — there's no way to know what fields will appear in the CSV without actually performing an export.

### Documentation Quality

The documentation quality is **poor**. The 6-page PDF (5 pages of content) provides:

- A high-level description of what data categories can be exported and in what format
- Step-by-step instructions for triggering an export from the UI
- No field-level documentation whatsoever

**No data dictionary.** There is no description of what fields appear in any export format — not the CSV columns for demographics, not the PDF content structure for encounters, not any extension or customization of the C-CDA or FHIR exports.

**No sample data.** No example export files are provided or referenced.

**No schema files.** No XSD, JSON Schema, CSV header specification, or any other machine-readable format definition.

**A developer attempting to import this data** would have to: (a) request an actual export, (b) reverse-engineer the CSV columns, (c) parse PDFs to extract structured data from unstructured documents, and (d) assume standard C-CDA/FHIR profiles with no vendor-specific documentation.

The document reads as a compliance checkbox — enough to demonstrate that an export capability exists, but insufficient for any practical data portability purpose.

### Structure & Completeness

- **Granularity:** Data category level only. No field names, data types, value sets, or constraints.
- **Coded fields:** Not documented.
- **Relationships:** Not documented. No indication of how exported entities relate to each other (e.g., how encounters link to lab results or how documents are associated with patients).
- **Versioning:** Document appears to be version 1.0 (created April 2024, around the time of certification). No change history.
- **Organizational structure for documents:** The document mentions that exported documents are "sorted and indexed within the Documents module for each patient" with category subfolders (Lab Reports, Imaging Reports, Consents, etc.), which is a useful structural detail.

### Overall Assessment

HealUs EHR's EHI export documentation represents a minimal compliance effort. The vendor has built a genuine export capability that goes slightly beyond a pure (g)(10) FHIR API by including additional data categories (appointments, referrals, advance directives, encounters, documents). However, the documentation has critical weaknesses:

1. **Heavy PDF reliance** makes most of the export non-computable, undermining the purpose of electronic data export.
2. **No data dictionary** means there is no way to understand what data will actually be in the export without performing one.
3. **No billing data** is mentioned, which is a notable gap for a company whose primary business is medical billing and revenue cycle management.
4. **The FHIR component** is just the standard (g)(10) API repackaged, covering only US Core clinical data.

The product was certified in July 2024, making it relatively new. The sparse documentation likely reflects the vendor's limited experience with ONC certification rather than deliberate concealment. The underlying export mechanism (multi-format with C-CDA, FHIR, CSV, and PDF) shows some thought about covering different data types, even if the execution and documentation are thin.

## Access Summary
- Final URL (after redirects): https://docs.healusehr.com/EHI
- Status: found
- Required browser: yes (Angular SPA renders PDF in-browser; PDF also directly downloadable at https://docs.healusehr.com/assets/docs/EHI.pdf)
- Navigation complexity: direct_link (PDF auto-loads when navigating to the registered URL)
- Anti-bot issues: none

## Obstacles & Dead Ends
- The registered URL serves an Angular SPA that requires JavaScript to render. The underlying PDF is accessible directly at `https://docs.healusehr.com/assets/docs/EHI.pdf`.
- The ONC mandatory disclosures page at `https://healusehr.com/onc-certified/` links back to the same documentation URL with no additional materials.
- No data dictionary, sample data, or schema files were found anywhere on the documentation site.
- The FHIR API documentation at `https://docs.healusehr.com/fhir` is (g)(10) API documentation, not specific to the (b)(10) EHI export, though the EHI PDF references FHIR as one of the export mechanisms.
