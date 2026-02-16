# Benchmark Systems — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.benchmarksystems.com/wp-content/uploads/2023/12/b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf
- CHPL ID: 9098
- Product: Benchmark EHR v7.1 (software version: Denali 3.1)
- Developer: Benchmark Systems (now Benchmark Solutions, a division of Harris)

## Navigation Journal

1. **Initial probe** — the registered URL returns HTTP 403:
   ```bash
   curl -sI -L "https://www.benchmarksystems.com/wp-content/uploads/2023/12/b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf" -H 'User-Agent: Mozilla/5.0'
   # → HTTP/2 403, Content-Type: text/html, 75193 bytes
   ```
   The entire benchmarksystems.com domain returns 403 (including the root `/`). The site appears to be behind a hosting provider that blocks all access.

2. **Wayback Machine check** — found a February 2024 snapshot:
   ```bash
   curl -s "https://web.archive.org/web/2024/https://www.benchmarksystems.com/wp-content/uploads/2023/12/b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf" -o /dev/null -w "%{http_code} %{redirect_url}"
   # → 302 → https://web.archive.org/web/20240220215439/...
   ```

3. **Downloaded from Wayback Machine**:
   ```bash
   curl -sL "https://web.archive.org/web/20240220215439/https://www.benchmarksystems.com/wp-content/uploads/2023/12/b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf" -H 'User-Agent: Mozilla/5.0' -o b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf
   ```
   Result: valid PDF, 539,084 bytes, 28 pages.

4. **Verified PDF content**: `pdfinfo` confirmed 28-page PDF created 2023-12-01 by Neha Parmar in Microsoft Word. `pdftotext` extracted clean text. No embedded URLs or attachments in the PDF (`pdfdetach -list` = 0 files, no URLs in text layer).

5. **Web search for additional documentation**: Searched `site:benchmarksystems.com` for EHI export terms — no additional EHI-specific documentation found beyond this PDF.

## What Was Found

The document is a **28-page §170.315(b)(10) self-attestation document** titled "Electronic Health Information export_Self Attestation Document" for Benchmark EHR version Denali 3.1. It is a genuine (b)(10) export documentation — not a repackaged FHIR/(g)(10) document.

### Export Mechanism

The export is a **proprietary database dump** delivered as a ZIP file containing:
- **XLS (Excel)** files for structured/tabular data
- **TXT** files for text data
- **PDF** files for documents and attachments (progress notes, letters, legal documents, etc.)
- **HTML/XML** files for CCD (Consolidated Clinical Document) data

There are two export modes:
1. **Single Patient Export**: Self-service via the EHR UI. Users with the `CuresEHIExport` role can select a patient, choose data element types via checkboxes, and trigger an async background export. The ZIP is available under Settings → Configuration → Download Files → "Cures EHI Export" category.
2. **Patient Population Export**: Not self-service — requires contacting the "Bizmatics Data Migration Team" at support@bizmaticsinc.com. This is described as resource-intensive and managed by the vendor. (Note: "Bizmatics" appears to be the development/services entity behind Benchmark.)

### Data Elements (47 categories)

The export covers **47 data element types**, each documented with a description and most with explicit database column-level field lists. The 42 core (non-billing) elements are always available; the 5 billing elements appear only "when Billing is turned on for the clinic":

**Clinical data (core EHR):**
- Patient Demographics (131 fields — extremely detailed including race, ethnicity, language, sexual orientation, gender identity)
- Patient Insurance (62 fields)
- Vaccination records
- Health Maintenance
- Family History
- Past Medical History
- Surgery history
- Allergies (with RxNorm and NDC codes)
- Current Medications (with NDC and RxNorm codes)
- Social History (with SNOMED and LOINC codes)
- Vitals / All Vitals (with SNOMED and LOINC codes)
- Diagnosis Codes (ICD-10, with assessment and plan notes)
- CPT Codes (with SNOMED codes and IMO descriptions)
- HCPC Codes
- Prescriptions (complete Rx history)
- Lab Results and Lab Test Result Values (discrete results with LOINC codes)
- Radiology Results
- Procedure Orders
- Consults
- Encounter Progress Notes (closed encounters, with extensive provider/referee fields)
- Procedure Notes
- CCD (Consolidated Clinical Document as HTML+XML)

**Documents and correspondence:**
- Legal Documents (as PDF)
- Other Documents (as PDF)
- Encounter Attached Documents (as PDF)
- Old Progress Notes (as PDF)
- Letters (inward/outward, consolidated PDF)
- Messages (patient messages)

**Administrative/reference data:**
- Insurance Master (insurance company reference data)
- Medics (provider/staff reference)
- Referring Providers
- Adjusters, Attorneys, Employers, Guarantors
- Patient Cases (workers' comp, injury cases)
- Patient Notes, Patient Alerts
- Future Appointments, Past Appointments

**Billing data (when billing module enabled):**
- Billing Ledger
- Billing Claims (185 fields — extremely detailed CMS 1500 claim data)
- Billing Charges (line-level charge detail)
- Patient Advance (advance payments)
- Statements (rendered as PDF)

### Field-Level Detail

The documentation provides **1,146 explicitly named database column fields** across the 36 entities that have quoted field lists. Column naming follows a consistent `PREFIX_FIELDNAME` convention (e.g., `PT_FNAME`, `BLH_CLAIM_STATUS`, `LOD_TEST_LOINC`). This is essentially a flattened view of the underlying database schema.

## Export Coverage Assessment

### Data Domain Coverage

This is an **unusually thorough (b)(10) export** that covers substantially all data domains identified in the product research:

**Clearly covered:**
- Demographics, contacts, insurance/enrollment ✓ (extensive — 131 demographic fields, 62 insurance fields)
- Diagnoses, problem lists ✓ (ICD-10, SNOMED, assessment notes)
- Medications and prescriptions ✓ (current meds + full prescription history, with RxNorm/NDC)
- Lab results ✓ (both order-level and discrete test result values with LOINC)
- Radiology results ✓
- Vital signs ✓ (per-encounter and all-encounters, with LOINC/SNOMED)
- Allergies ✓ (with RxNorm, NDC, adverse event, SNOMED reaction codes)
- Immunization records ✓ (CVX codes, manufacturer, lot, route, site)
- Procedures and surgical history ✓
- Clinical notes (progress notes, procedure notes) ✓ (as PDF exports from encounters)
- Letters and correspondence ✓
- Consults and referrals ✓
- Family history ✓ (with SNOMED)
- Social history ✓ (with SNOMED and LOINC)
- Patient messages ✓
- Billing records ✓ (claims, charges, ledger, advance payments, statements — 185 fields for claims alone)
- Patient cases (workers' comp, injury) ✓
- Documents and attachments ✓ (legal, other, encounter-attached, old progress notes)
- CCD (C-CDA documents) ✓
- Care team / provider reference data ✓ (medics, referring providers, with NPI/taxonomy)
- Appointments ✓ (future and past)

**Potentially missing or ambiguous:**
- **Care plans / goals**: Not explicitly listed as a separate export category. Care plan data may be embedded in progress notes or CCD documents, but there's no dedicated "Care Plans" entity.
- **Patient education materials distributed**: The product research notes MedlinePlus education materials are distributed to patients. No explicit export for this.
- **Patient intake forms**: Mentioned as a portal feature; no explicit export for intake form responses as structured data (though they may be captured in encounter documents).
- **Custom specialty templates**: The product supports 40+ specialty templates for notes, but the export captures the rendered notes (as PDFs), not the structured template field data.

These gaps are minor. The export covers the core clinical record, billing records, and documents comprehensively.

### Export Format & Standards

The export uses a **proprietary format** — not FHIR, C-CDA, or any interoperability standard. It is essentially a **database dump in Excel/text files with associated PDF documents**, organized by data element type.

This is an appropriate format for (b)(10). The export is clearly computable (XLS, TXT files), and for documents that are inherently rendered (progress notes, letters, legal documents), PDF is a reasonable format. The inclusion of CCD HTML/XML exports adds a layer of standards-based clinical summary alongside the raw data.

The format is **not self-describing**: there are no embedded data types, value set definitions, or schema files in the export. A consumer would need this PDF document to understand the column names and their meanings. However, the column naming convention is largely self-explanatory (e.g., `PT_DOB` = patient date of birth, `BLH_BILL_AMOUNT` = billing amount).

Relationships between entities are implicit through shared ID fields (e.g., `PT_ID`, `BLH_ENC_ID`, `LOH_DOC_ID`) but not formally documented as foreign keys. A developer importing this data would need to infer relationships from column naming patterns.

### Documentation Quality

**Strengths:**
- **Field-level granularity**: 1,146 named fields across 47 entities — this is unusually detailed for (b)(10) documentation
- **Comprehensive scope**: 47 data element types covering clinical, administrative, and billing domains
- **Consistent format**: Each entity has a numbered description, export notes, and a quoted field list
- **Practical export instructions**: Clear description of the CuresEHIExport role, UI workflow, and where to find downloaded files
- **Honest about limitations**: Notes which data is excluded (inactive records, void claims, UB04 forms, deleted encounters)

**Weaknesses:**
- **No data type information**: Fields are listed by name only — no column data types (string, date, integer, boolean), lengths, or constraints
- **No value set documentation**: Fields like `PT_MARITAL_STATUS`, `TEI_STATUS_NAME`, `BLH_CLAIM_STATUS` use coded values that are not defined
- **No relationship documentation**: No foreign key or entity-relationship documentation
- **No sample data**: No example export files or sample records
- **Population export requires vendor assistance**: The bulk export is not self-service, potentially creating an information blocking concern since it depends on the "Bizmatics Data Migration Team"
- **Boolean fields undocumented**: Many `BOOL_*` fields (e.g., `PT_BOOL_SELFPAY`, `BLH_BOOL_WORK_COMP`) with no explanation of what true/false means
- **Original URL is dead**: The live URL returns 403; the document was only retrievable via Wayback Machine

### Structure & Completeness

The documentation is moderately granular:
- Entity-level: 47 named entities with descriptions ✓
- Field-level: database column names for 36 of 47 entities ✓
- Data types: Not documented ✗
- Value sets/codes: Not documented (except noting which standard code systems are used: ICD-10, SNOMED, LOINC, CVX, RxNorm, NDC) ✗
- Relationships: Not formally documented ✗
- Examples: None ✗
- Versioning: Document is version "Denali 3.1", no change history ✗

A developer could identify what data is included in an export from this documentation, but could not fully reconstruct the patient record without additional context about data types, value sets, and inter-entity relationships.

### Overall Assessment

Benchmark EHR's (b)(10) export documentation is **above average** for the EHR market. The vendor has clearly invested effort in documenting a genuine EHI export that goes well beyond USCDI/US Core. The 47 data element types cover clinical, administrative, billing, and document data — this is a proper designated record set export, not a repackaged FHIR API.

The export is a proprietary database dump format, which is pragmatic: it exports more data than any standardized format would easily accommodate, and the field naming convention makes most columns self-explanatory. The main documentation gaps are in data types, value sets, and relationships — the sort of metadata that would be present in a formal schema definition.

The population-level export requiring vendor contact (Bizmatics Data Migration Team) is a compliance concern for the (b)(10)(ii) requirement, which calls for creating a bulk export without specifying it must be self-service — but the spirit of the regulation suggests it should be available without dependency on the vendor's schedule.

## Access Summary
- Registered URL: https://www.benchmarksystems.com/wp-content/uploads/2023/12/b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf
- Final URL (after redirect): https://web.archive.org/web/20240220215439/https://www.benchmarksystems.com/wp-content/uploads/2023/12/b-10-EHI-Export_Benchmark-Support_Self-Attestation-Document_final-1.pdf
- Status: found (via Wayback Machine; live URL returns 403)
- Required browser: no
- Navigation complexity: direct_link (once accessible)
- Anti-bot issues: Entire benchmarksystems.com domain returns 403; appears to be a hosting/CDN block

## Obstacles & Dead Ends

1. **Live URL returns 403**: The registered CHPL URL and the entire benchmarksystems.com domain return HTTP 403 Forbidden. The 403 response is 75KB of HTML (likely a hosting provider error page). Both the root domain and the specific PDF path are blocked. This may be a temporary hosting issue or a configuration change following the Harris Healthcare acquisition.

2. **No alternative live source found**: Web search for Benchmark Systems EHI export documentation found only the registered URL. No mirror or alternative hosting location was identified.

3. **Wayback Machine recovery successful**: The Internet Archive had a snapshot from February 20, 2024, which yielded the complete 539KB PDF. The document dates to December 1, 2023 (shortly before the ONC compliance deadline of Dec 31, 2023).

4. **"Bizmatics" entity**: The document references "Bizmatics" as the development/support entity (support@bizmaticsinc.com, "Bizmatics Data Migration Team"), while the product is branded "Benchmark EHR" / "Benchmark Solutions." This suggests Bizmatics is the underlying technology company that developed the EHR.
