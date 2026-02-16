# Physicians EMR, LLC — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ipclinical.com/documentation/b_10_Electronic_Health_Information_export.pdf
- CHPL IDs: 10278
- Product: IPClinical v2.1
- Certification Date: 2020-01-23

## Navigation Journal

1. **Initial probe** — HTTP HEAD request to the registered URL returned HTTP 200
   with `Content-Type: application/pdf` and `Content-Length: 466885` (about 467KB).
   Direct file download, no redirects.

   ```bash
   curl -sI -L "https://ipclinical.com/documentation/b_10_Electronic_Health_Information_export.pdf" -H 'User-Agent: Mozilla/5.0'
   ```

2. **Downloaded the PDF** directly:
   ```bash
   curl -sL "https://ipclinical.com/documentation/b_10_Electronic_Health_Information_export.pdf" -H 'User-Agent: Mozilla/5.0' -o b_10_Electronic_Health_Information_export.pdf
   ```
   Verified: `file` confirms "PDF document, version 1.5, 2 page(s)". Created November 23, 2023 by Ahmed Tariq using Microsoft Word 2016.

3. **Extracted hyperlinks from the PDF**. Found:
   - Links to external standards (HL7, HealthIT) — not followed per instructions
   - Link to `https://ipclinical.com/mu-disclousure` (mandatory disclosures page), referenced as the location of "(g)(10) FHIR API Documentation"
   - No embedded files or attachments in the PDF

4. **Checked the mandatory disclosures page** (`https://ipclinical.com/mu-disclousure`).
   Found two additional API documentation PDFs linked:
   - `https://ipclinical.com/documentation/IPClinical_g10_API_Documentation.pdf`
   - `https://ipclinical.com/documentation/IPClinical-api-documentation.pdf`

   Downloaded both since the (b)(10) PDF explicitly says "Kindly refer to IPClinical – (g)(10) FHIR API Documentation for API specifications" when describing the FHIR export format.

5. **Also checked** the `/documentation/` directory — returns 403 Forbidden after redirecting to `www.ipclinical.com/documentation/`.

## What Was Found

The entire (b)(10) EHI export documentation is a **single 2-page PDF**. Page 1 is a cover page with the IPClinical logo; page 2 is the actual content. The document describes three export formats:

### Format 1: C-CDA
- Supports both single patient and patient population export
- Includes USCDI Version 1 data classes
- References three C-CDA specifications: HL7 CDA R2 IHE Health Story Consolidation DSTU 1.1 (2012), HL7 C-CDA R2.1 (2015/2019), and the C-CDA R2.1 Companion Guide R2 (2019)
- No data dictionary, no field mapping, no examples — just a statement that C-CDA is supported

### Format 2: FHIR
- Supports single patient and patient population export
- References FHIR US Core IG STU V3.1.1 and FHIR Bulk Data Access V1.0.1 STU 1
- Points to the separate g(10) FHIR API Documentation (121-page PDF) for API specifications
- The g(10) documentation covers these US Core FHIR resources:
  - Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device (Implantable), DiagnosticReport (notes & labs), DocumentReference, Encounter, Goal, Immunization, MedicationRequest, Observation (vitals, smoking status, lab results, pediatric measures), Procedure, Organization, Practitioner, Provenance
  - Includes SMART on FHIR authentication, Bulk Data export endpoints, and a full CapabilityStatement
- There is also an older, simpler API doc (8 pages, "IPClinical API v5.0") that describes a proprietary API returning C-CDA XML

### Format 3: Excel/PDF
- Patient Documents: lab results, radiology reports, scanned/imported/faxed documents exported as PDF
- Scheduling & Appointments: exportable in both Excel and PDF
- Billing & Financial information: "most" exportable in Excel, "some" also in PDF
- Imaging Result Reports: exported through FHIR format as well
- **No data dictionary or schema for the Excel exports** — no description of columns, data types, or structure
- **No sample files or examples**

## Export Coverage Assessment

### Data Domain Coverage

IPClinical's (b)(10) documentation describes a multi-format export strategy that attempts to cover data beyond the USCDI/US Core subset. This is a positive sign — the vendor recognizes that (b)(10) requires more than just FHIR US Core data. However, the documentation is extremely thin on specifics.

**Clearly covered (via C-CDA/FHIR):**
- Demographics / patient information
- Allergies
- Conditions / problem lists
- Medications / prescriptions
- Lab results
- Vital signs
- Immunizations
- Procedures
- Clinical notes (via DocumentReference)
- Encounters
- Care plans / goals
- Care team information
- Implantable devices
- Smoking status

**Mentioned but poorly documented (via Excel/PDF):**
- Billing & financial information — described as "most" exportable in Excel, but no data dictionary, no column definitions, no description of what "most" means or what's excluded
- Scheduling & appointments — exportable in Excel/PDF, but no schema
- Patient documents — PDFs of lab results, radiology, scanned/faxed docs

**Likely missing or not mentioned:**
- Insurance/eligibility data — the product stores this (per product research) but the export documentation doesn't specifically mention it beyond "billing & financial"
- Claims data and charge capture details — subsumed under "billing" but undefined
- Accounts receivable / payment data — not specifically mentioned
- Task/alert data — the product has a task management system, not mentioned in export
- Patient portal communications — the product has a patient portal, no export mentioned
- Remote patient monitoring data — the product supports RPM and cardiac device monitoring, not mentioned in export
- Fax records — the product manages faxes, not mentioned as exportable data (though "faxed documents" as PDFs are)
- E-Scribe/virtual scribe data — unclear if this generates structured data beyond clinical notes

The fundamental problem is that the Excel/PDF exports are described in a single paragraph with no specifics. A developer receiving an Excel file of "billing & financial information" would have no way to know what fields are included, what the columns mean, or how to map them to other systems.

### Export Format & Standards

The export uses a reasonable combination of formats:
- **C-CDA** for structured clinical data (USCDI v1 scope)
- **FHIR US Core 3.1.1 + Bulk Data** for the same clinical data via API
- **Excel/PDF** for non-clinical data (billing, scheduling, documents)

The C-CDA and FHIR formats are well-documented in their respective spec documents (121-page g(10) API doc). The Excel/PDF formats have **zero documentation** — no schema, no column definitions, no examples.

This is a classic (b)(10) pattern: the vendor has invested heavily in their g(10) FHIR API (which is genuinely detailed) and then bolted on a vague mention of Excel/PDF export for everything else. The result is that a third party could reconstruct the USCDI clinical data from the FHIR/C-CDA export, but would be flying blind on the billing, scheduling, and document exports.

### Documentation Quality

- **FHIR/C-CDA documentation**: Good. The 121-page g(10) API doc includes resource-level documentation with field descriptions, search parameters, examples, and a full CapabilityStatement. This is a real, working API specification.
- **(b)(10) documentation**: Very poor. A 2-page document that reads like a compliance checkbox. No data dictionary, no worked examples, no sample files, no export instructions, no screenshots of the export interface. The document says what formats exist but not what's in them.
- **Excel/PDF exports**: Undocumented. A receiving party would have to inspect the actual export files to understand their structure.

A developer could implement a FHIR US Core import based on the g(10) docs. A developer could **not** implement an import of the billing/scheduling Excel exports based solely on this documentation — there is nothing to implement against.

### Structure & Completeness

- **Clinical data (FHIR)**: Field-level documentation exists in the g(10) doc. FHIR resources have defined schemas, search parameters, and value sets. The CapabilityStatement lists supported interactions.
- **Clinical data (C-CDA)**: Relies entirely on external C-CDA specifications. No vendor-specific mapping or customization documented.
- **Non-clinical data (Excel/PDF)**: No field-level documentation at all. No data types, no value sets, no relationships between tables, no cardinality.
- **No versioning or change history** beyond the document version (2.1) and creation date (Nov 2023).

The documentation presents a two-tier system: the FHIR/g(10) layer is professional and detailed, while the (b)(10)-specific layer (the parts that go beyond USCDI) is a single paragraph of prose with no technical substance.

## Access Summary
- Final URL (after redirects): https://ipclinical.com/documentation/b_10_Electronic_Health_Information_export.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
- The `/documentation/` directory listing is forbidden (403), so there's no way to discover additional documentation files beyond what's linked from known pages.
- No additional EHI-specific documentation was found beyond the single 2-page PDF and the referenced g(10) API docs.
- No data dictionary, schema, or sample export files exist at the registered URL or on the mandatory disclosures page.
