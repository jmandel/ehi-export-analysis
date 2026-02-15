# Aarista Technology LLC — EHI Export Documentation

Collected: 2026-02-14

## Source
- Registered URL: https://alteahc.com/wp-content/uploads/2023/11/Aarista_EHI_Export-.pdf
- CHPL IDs: 11329
- Product: Aarista v1.0
- Certification date: 2023-08-08

## Navigation Journal

1. **Initial probe of registered URL** — returned HTTP 403 Forbidden. Both alteahc.com and aarista.com are currently returning 403 on all paths, suggesting the sites are down or access-restricted.

```bash
curl -sI -L "https://alteahc.com/wp-content/uploads/2023/11/Aarista_EHI_Export-.pdf" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
# → HTTP/2 403
```

2. **Attempted with Referer and Accept headers** — still 403; downloaded content was an HTML error page (75KB), not a PDF.

3. **Checked Wayback Machine** — found snapshot from 2024-08-09:

```bash
curl -sL "https://web.archive.org/web/20240809132500/https://alteahc.com/wp-content/uploads/2023/11/Aarista_EHI_Export-.pdf" \
  -H 'User-Agent: Mozilla/5.0' -o downloads/Aarista_EHI_Export.pdf
# → PDF document, 8 pages, 183,079 bytes. Verified: file command confirms PDF.
```

4. **Checked aarista.com/about/ via Wayback Machine** (snapshot 2025-08-04) — the mandatory disclosures page links to:
   - `Aarista_EHI_Export-.pdf` (under /wp-content/uploads/2025/02/) — downloaded; byte-identical to the 2023 version (same 183,079 bytes, no text diff). This confirms the data dictionary has not been updated since original creation (Nov 28, 2023).
   - `b10-Real-World-Test-Plan-2025-Electronic-Health-Info-Export.pdf` — downloaded separately (204,611 bytes, 5 pages). This is a regulatory filing describing the real-world testing plan for b(10), signed 10/15/2024.

5. **Confirmed both vendor domains (alteahc.com, aarista.com) are currently inaccessible** — all paths return HTTP 403 with an nginx error page.

## What Was Found

### EHI Export Data Dictionary (PDF, 8 pages)

The primary documentation is a PDF titled "Data Dictionary for Aarista EHI Export" authored by Michael Mai, created November 28, 2023 in Microsoft Word.

**Overview section** states: "The Electronic Health Information (EHI) Data Dictionary Export for Aarista allows customers to easily export patient's demographics and clinical data such as insurances, encounters, problems, allergies, medications, immunizations, vitals, labs, procedures, etc. Customers can request to export individual patients or all patients for the practice."

**File format**: "Export data files are machine readable file formats." No further specification of the actual file format (CSV, JSON, XML, etc.) is provided.

**The document defines 7 data tables:**

1. **Single Patient - Patient Demographics** (28 fields) — names, DOB, SSN, gender identity, race, ethnicity, language, PCP info, Medicare/Medicaid identifiers, employment/military status.

2. **Single Patient - Patient Addresses** (10 fields) — address lines, city/state/zip, plus communication type (phone/email) with preferred indicator.

3. **Single Patient - Patient Contacts** (20 fields) — emergency contacts and guarantors with relationship, contact info, addresses.

4. **Single Patient - Patient Insurances** (24 fields) — insurance type, payer, policy details, policy holder demographics and contact info.

5. **Single Patient - Patient Encounters – Clinical and Billing** (29 fields) — encounter-level clinical documentation including chief complaint, HPI, medications, problems, allergies, surgical/medical/family/social history, immunizations, ROS, vitals, physical exam, labs, radiology, assessment, plan, billing codes, and disclaimer. Many clinical fields are nvarchar(4000) free-text blobs; medications, problems, allergies, assessment, and billing are "multiple records" within nvarchar fields.

6. **Practice Patients - Patient Demographics and Billing Encounters** (16 fields) — practice-wide billing export with TIN, NPI, MRN, visit date, encounter/diagnosis codes, modifiers, place of service, and insurer names.

7. **Practice Patients - Patient Demographics and Clinical Encounters** (25 fields) — practice-wide clinical data with a generic structure: Name, Description, Code, Codesys, Category, Status, Textresult, Numresult, Units, plus various dates and medication-specific fields (strength, sig, dispense, refills).

All data types are SQL Server types (nvarchar, int, date, datetime, float, bit), indicating the export is a direct projection of the underlying database schema.

### b(10) Real World Testing Plan (PDF, 5 pages)

A regulatory document signed 10/15/2024 by Michael Mai. Key details:
- **Certification criteria**: §170.315(b)(10)(EA) — create export file(s) with all of a single patient's EHI. §170.315(b)(10)(EB) — executable at any time without developer assistance. §170.315(b)(10)(ED) — export file(s) must be electronic and in a computable format.
- **Approach**: Random sampling of single-patient exports in each care setting; population-level export tested for facilities managing multiple patients.
- **Format**: "The export files will be generated in the specified computable format (e.g., C-CDA files or FHIR APIs)."
- **Care settings**: Ambulatory (outpatient) and Post-Acute Care (long-term care, home health).
- **Timeline**: January 1–December 31, 2025 for data collection; January 31, 2026 for report submission.
- **Success metrics**: Exports should be generated without error, meet certification criteria, and allow import into other certified systems.

## Export Coverage Assessment

### Data Domain Coverage

The data dictionary covers a moderate subset of what the product stores, focused primarily on **clinical encounter documentation** and **billing/claims data**. Comparing against the product research:

**Clearly covered:**
- Patient demographics (comprehensive — includes SSN, MBI, Medicaid#, gender identity, sexual orientation, race, ethnicity, language)
- Patient addresses and contact information
- Patient contacts/emergency contacts/guarantors
- Insurance/payer information
- Clinical encounter notes (chief complaint, HPI, ROS, physical exam, assessment, plan)
- Problem lists
- Medication lists
- Allergies
- Immunizations
- Vital signs
- Lab results
- Radiology results
- Surgical and medical history
- Family and social history
- Billing data (encounter codes, diagnosis codes, modifiers, place of service, insurer names)

**Notably absent or unclear:**
- **Scheduling/appointment data** — the product has a "Smart Scheduler" but no appointment/schedule table appears in the export
- **Care plans** — certified under (b)(11) but not represented as a distinct export entity
- **E-prescribing records** — medications appear in encounter notes but no structured prescription/dispensing table
- **Telehealth encounter metadata** — no distinction between in-person and telehealth encounters
- **Remote patient monitoring data** — vital signs from RPM not separately identified
- **AI/ML risk scores and alerts** — the "Aari" analytics layer generates risk predictions, but these are absent from the export
- **Clinical quality measure data** — certified (c)(1) but not in the export dictionary
- **Audit logs** — no audit or access log data
- **Practice/facility configuration** — dashboards, practice hierarchy, facility settings not included
- **Transitions of care documents** — certified (b)(1) C-CDAs but not mentioned in the export
- **Patient portal/patient-generated data** — not mentioned
- **Document attachments** — no mechanism for exporting attached files, scanned documents, etc.
- **Coding trends/RVU data** — mentioned on the features page but not in the export

The export appears to capture **encounter-focused clinical and billing data** but misses several operational domains the product manages.

### Export Format & Standards

The documentation is frustratingly vague about the actual export format. It says "machine readable file formats" without specifying what those formats are. The data types are all SQL Server column types (nvarchar, int, date, datetime, float, bit), which suggests the export is a **flat file (likely CSV) derived directly from database tables or views**.

The Real World Test Plan mentions "C-CDA files or FHIR APIs" as possible formats, but the data dictionary doesn't align with either standard — it describes flat, denormalized tables with free-text clinical content, not structured C-CDA documents or FHIR resources.

**Key format concerns:**
- Clinical data in the encounter table is stored as large nvarchar(4000) text blobs (e.g., "Review of Systems", "Physical Exam"), not structured/coded data
- Medications, problems, allergies, assessment, and billing are described as "multiple records" within single nvarchar fields — it's unclear how these are delimited or structured within the export
- The "Practice Patients - Clinical Encounters" table uses a generic Name/Description/Code/Category/Status structure, mixing different data types (labs, medications, etc.) in a single flat table with a "Category" discriminator
- No relationships between tables are documented (e.g., how encounters link to demographics)
- No foreign keys, join fields, or entity relationships described

A third party receiving this export would face significant challenges reconstructing a complete patient record. The encounter data is largely free-text blobs, and the generic clinical encounter table mixes heterogeneous data types without clear documentation of the Category values or how to distinguish labs from medications from other clinical items.

### Documentation Quality

**Low to moderate.** The document is a basic data dictionary — field names and SQL data types in tabular format. It provides:
- Field names (somewhat self-descriptive)
- SQL Server data types with lengths
- Required field indicators (asterisks)

**It lacks:**
- Field-level descriptions or definitions
- Value sets or allowed values for coded fields (e.g., what are the valid values for "Administrative Gender", "Progress Notes Type", "Category"?)
- Sample data or example exports
- Export file format specification (CSV? JSON? What delimiter? What encoding?)
- Instructions for how to perform the export
- Documentation of how multi-valued fields are serialized (the "multiple records" notation)
- Relationship documentation between the 7 tables
- Error handling or edge case documentation
- Versioning or change history

The document was created in November 2023 (at certification time) and has not been updated since — the 2025 version hosted on aarista.com is byte-identical. This suggests it was created as a certification artifact and has not been maintained.

Several typos are present: "Ethnithity" (Ethnicity), "Mother Mainder Name" (Mother Maiden Name), "Chief Comlaint" (Chief Complaint), "Historhy of Present Illness" (History of Present Illness), "L:abs" (Labs). These suggest the document received limited editorial review.

### Structure & Completeness

The documentation provides **field-level granularity** (field names and data types) but lacks almost everything else needed for a developer to work with the export:
- No entity-relationship model
- No value set definitions
- No cardinality documentation (beyond "multiple records" notation)
- No export file format or encoding specification
- No sample files
- No schema files (no XSD, JSON Schema, CSV header spec, or DDL)

The 7 tables represent a reasonable decomposition of the data (demographics, addresses, contacts, insurance, encounters, billing, clinical), but the generic "Clinical Encounters" table conflates many different data types into a single flat structure, reducing usability.

## Access Summary
- Registered URL: https://alteahc.com/wp-content/uploads/2023/11/Aarista_EHI_Export-.pdf
- Final URL (after redirects): same (no redirect, returns 403)
- Status: dead (both alteahc.com and aarista.com returning 403 on all paths as of 2026-02-14)
- Retrieved via: Wayback Machine snapshot 2024-08-09
- Required browser: no (direct PDF download when site was live)
- Navigation complexity: direct_link
- Anti-bot issues: entire site returning 403 — unclear if this is intentional blocking, site migration, or domain expiration

## Obstacles & Dead Ends

1. **Both vendor domains are down.** alteahc.com and aarista.com both return HTTP 403 Forbidden on every path tested (root, /about/, the PDF URL). The 403 comes from nginx with a consistent 75KB HTML error page. This could indicate the hosting provider suspended the accounts, a site migration is in progress, or the domains have been parked.

2. **PDF text extraction works but pdftotext fails on the b(10) test plan** — that PDF appears to be a scanned/image-based document, so it was read via rendered images instead.

3. **No format specification** — despite downloading all available documentation, the actual export file format (CSV, JSON, XML, etc.) is never specified. This is a significant gap that would prevent anyone from actually importing the data.

4. **The 2025 re-upload is identical** — the aarista.com/about/ page linked to what appeared to be a newer version of the EHI Export PDF (under /wp-content/uploads/2025/02/) but it was byte-identical to the November 2023 original, confirming no updates have been made to the documentation.
