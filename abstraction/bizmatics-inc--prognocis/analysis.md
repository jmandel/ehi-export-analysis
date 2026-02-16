# EHI Export Analysis: Bizmatics Inc.

**Product**: PrognoCIS
**Analysis date**: 2026-02-16
**CHPL IDs**: 8856 (version Denali 3.1, certified 2017-09-29), 11738 (version 4.0, certified 2025-12-24)

## 1. Product Context

PrognoCIS by Bizmatics Inc. is an integrated cloud-based EHR, practice management, and medical billing platform targeting small-to-mid-sized ambulatory/outpatient practices. It supports 30+ clinical specialties including family medicine, internal medicine, cardiology, dermatology, psychiatry, OB-GYN, pediatrics, and many others.

Key data domains the product stores:

- **Clinical**: Patient demographics, encounters/progress notes, problem lists, medications, allergies, vitals, lab results, radiology results, immunizations, procedures, consults, social history, family history, clinical decision support
- **Prescribing**: E-prescribing (Surescripts-certified, including EPCS for controlled substances), prescription history, medication lists
- **Billing/RCM**: Claims, charges, payments, AR management, denial tracking, clearinghouse submissions, financial analytics — the billing module is integrated, not separate
- **Practice management**: Scheduling, referral management, pre-authorization, insurance eligibility verification
- **Documents**: Scanned documents, faxes (PrognoFax), images, progress notes, letters, procedure notes, legal documents
- **Patient portal**: Secure messaging, intake forms, appointment scheduling, prescription refills, lab results
- **Specialty data**: Workers' compensation case management, customizable specialty templates
- **Interoperability**: C-CDA/CCD documents, FHIR API, HL7 interfaces

This sets a high bar for export completeness: a genuine (b)(10) export should cover clinical data, billing/financial data, documents, specialty data, and patient communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `b-10-EHI-Export_PrognoCIS-Support.pdf` | 26-page PDF (678 KB): "§170.315(b)(10) Electronic Health Information export_Self Attestation Document" by Neha Parmar, dated 2023-12-01. Version Denali 3.1. **Primary source** for all export documentation. | ★★★★★ Most informative |
| `b-10-EHI-Export_PrognoCIS-Support.txt` | Plain text extraction from the PDF (890 lines). Used for programmatic parsing. | ★★★★ (derived from PDF) |
| `enrichment/data-dictionary.json` | Structured JSON extraction of all 47 data elements and 1,180 fields from the PDF (prior agent's enrichment). Verified against raw text. | ★★★★★ Most useful for analysis |
| `enrichment/extract-data-dictionary.ts` | Bun TypeScript script that produced the enrichment JSON. Reviewed for parsing logic. | ★★★ (methodology check) |
| `macra-page-top.png`, `macra-page-ehi-section.png` | Screenshots of the vendor's MACRA compliance page showing the PDF download link. Confirm the PDF is the sole (b)(10) documentation. | ★★ (context only) |

**Key observations about the source**: The entire EHI export documentation is a single 26-page PDF. There is no separate data dictionary, no machine-readable schema, no sample export files, and no API documentation. The PDF serves as both the user guide (export workflow) and the technical reference (field lists).

## 3. Export Mechanics

- **Format**: ZIP file containing **XLS (Excel)** and **TXT** files for structured data (one per data element type), plus **PDF files** for documents (progress notes, procedure notes, legal documents, letters, statements). CCD export includes **HTML and XML (C-CDA)** files.
- **Mechanism**: UI-driven. Single-patient export via a built-in UI button accessible to users with the `CuresEHIExport` role. User searches for a patient, selects data element checkboxes, clicks EXPORT. The export runs in background and the user receives email notification when ready. Download via Settings → Configuration → Download Files → "Cures EHI Export" category.
- **Single-patient**: Fully self-service, no developer assistance required.
- **Bulk/population export**: Requires contacting Bizmatics Data Migration Team (`support@bizmaticsinc.com`). Vendor states this "depends on size of data, time and efforts required to manage the server resources." This is a notable compliance concern — (b)(10) requires population export capability.
- **Access constraints**: Export requires the `CuresEHIExport` user role. The role is assignable to providers, medical assistants, office staff, and clinical staff.
- **Fees**: Not mentioned in the documentation. Population export handled by vendor team may involve fees (unstated).

**Notable export options** (from PDF pp. 4–5):
- "Include Deleted Encounters" checkbox (labeled "Use with caution")
- "Reason for Data Export" field
- Billing data elements only appear when billing is enabled for the clinic
- Only active patients' data is exported (inactive patients excluded)

## 4. Export Content: What's In It

The export covers **47 selectable data element types**, of which **41 have explicit field lists** (totaling **1,185 fields**) and **6 have no discrete field lists** (document/attachment types that export PDFs or have minimal metadata). Additionally, every exported XLS/TXT file includes 6 standard patient identifier columns (Last name, First name, Middle name, Chart no, Account no, Birth date) that are not counted in the per-element field totals.

**Documentation quality per field**: The PDF provides field **names only** — no data types, no descriptions beyond the field name, no nullability constraints, no max lengths, no foreign key documentation, no value sets or code systems, and no sample data. Field names are generally self-explanatory (e.g., "Insurance Company Name", "Date of Birth", "ICD10 Code") but some are cryptic (e.g., "3032 Emergency Contact Address Single Line", "Bool Icd10", "CLM053").

### Vendor's own content organization

The PDF organizes the 47 data elements into these groups:

**Reference / Provider Data (elements 1–7)**: 7 entities, 177 fields

| Entity | Fields | Category |
|---|---|---|
| Insurance Master | 22 | Reference / Provider |
| Medics | 31 | Reference / Provider |
| Referring Doctor | 28 | Reference / Provider |
| Adjusters | 33 | Reference / Provider |
| Attorneys | 16 | Reference / Provider |
| Employers | 25 | Reference / Provider |
| Guarantor | 22 | Reference / Provider |

**Patient Clinical & Administrative Data (elements 8–37)**: 30 entities, 570 fields

| Entity | Fields | Notes |
|---|---|---|
| Patient Demographics | 131 | Comprehensive; includes emergency contacts, multiple PCPs, race, ethnicity, sexual orientation, gender identity |
| Patient Insurance | 60 | Insurance plan details, eligibility, pre-authorization |
| Vaccination | 18 | Administered vaccines with CVX codes, lot numbers, VIS dates |
| Health Maintenance | 7 | Due/tentative tests only; history not exported |
| Family History | 7 | SNOMED-coded problems and relations |
| Past Medical Hist | 9 | ICD-9, ICD-10, SNOMED coded |
| Surgery | 6 | Surgical history |
| Allergy | 13 | RxNorm, NDC, SNOMED coded reactions |
| Current Medication | 18 | Active meds with NDC, RxNorm |
| Social History | 11 | LOINC and SNOMED coded |
| Legal Documents | 0* | PDF attachments only |
| Other Documents | 0* | PDF attachments only |
| Enc Attach Docs | 0* | PDF attachments only |
| Old Progress Notes | 0* | PDF attachments only |
| Messages | 5 | ID, Date, Subject, Notes, Sender |
| Future Appointments | 18 | Scheduled/tentative appointments |
| Vitals | 11 | Latest encounter only; LOINC and SNOMED coded |
| Diagnosis Code | 11 | ICD-9, ICD-10 with assessment and plan |
| CPT Codes | 10 | CPT with modifiers, SNOMED, revenue codes |
| HCPC Codes | 10 | HCPC with modifiers, SNOMED |
| CCD | 5† | C-CDA HTML/XML document references |
| Prescriptions | 20 | All prescribed drugs, with pharmacy, status, mode |
| Lab Results | 23 | Order and result metadata |
| Rad Results | 21 | Radiology order and result metadata |
| Procedure Orders | 33 | Orders with results, attending/primary doctors |
| Consults | 30 | Consult orders with referral details |
| Enc Progress Notes | 63 | Encounter records with multiple provider roles, insurance, case # |
| Procedure Notes | 3 | Procedure note PDFs with template info |
| Letters | 16 | Inbound/outbound letters with recipients |
| All Vitals | 11 | Vitals across all encounters |
| Lab Test Result Values | 38 | Discrete lab results with LOINC, ranges, units |

*\* Document-type elements export PDFs; metadata is in the standard patient identifier columns plus a "File" path column.*
*† CCD field list found in Appendix section of PDF, not in section 28.*

**Patient Case & Administrative Data (elements 38–42)**: 5 entities, 100 fields

| Entity | Fields | Notes |
|---|---|---|
| Patient Cases | 41 | Workers' comp / case management with injury details, WCAB#, approved amounts |
| Patient Notes | 2 | Free-text notes with date |
| Patient Alert | 2 | Alert text with timestamp |
| Past Appointments | 17 | Historical appointments with visit statuses |

**Billing Data (elements 43–47, conditional on billing module)**: 5 entities, 338 fields

| Entity | Fields | Notes |
|---|---|---|
| Billing Ledger | 0* | No field list; exports ledger for run date, billed claims only |
| Billing Claims | 185 | Extremely detailed: claim status, amounts, insurance layers, EDI details, collection agency info |
| Billing Charges | 123 | Line-item charges with modifiers, amounts per payer, adjustments |
| Patient Advance | 30 | Advance payments, copays, refunds |
| Statements | 0* | Exports latest patient statement as PDF |

*\* Billing Ledger has no field list (description only). Statements export as PDFs with no discrete field list.*

The complete entity inventory (47 entities, all fields) is saved in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized into four broad categories with clear functional groupings:

**Strongest areas:**
- **Billing** (308 fields across 4 entities with field lists + 1 PDF-only entity): Billing Claims alone has 185 fields — this is genuinely deep, covering claim status, multi-payer amounts, EDI details, collection agency data, capitation, and pre-authorization. Billing Charges adds 123 fields of line-item detail. This is not a token billing export.
- **Patient Demographics** (131 fields): Exceptionally thorough — emergency contacts, multiple PCP assignments (up to 5), race/ethnicity (SNOMED), sexual orientation/gender identity (SNOMED), workers' comp flags, financial class, and more.
- **Encounter/Progress Notes** (63 fields): Detailed encounter records with multiple provider roles (attending, rendering, referring, supervising, reviewing), insurance linkage, case reference, and pregnancy tracking.
- **Insurance/Coverage** (172 fields across 5 entities): Insurance master, patient insurance plans with eligibility data, adjusters, attorneys, and case management.

**Moderate areas:**
- **Lab Results**: Two complementary entities — Lab Results (23 fields, order/result metadata) and Lab Test Result Values (38 fields, discrete test results with LOINC, ranges, units). Together these provide solid coverage.
- **Orders/Referrals**: Procedure Orders (33 fields) and Consults (30 fields) with scheduling, results, and multi-provider documentation.
- **Medications**: Current Medication (18 fields) and Prescriptions (20 fields) with NDC, RxNorm, pharmacy, status.
- **Documents**: 7 entities export actual PDF files (progress notes, procedure notes, legal documents, letters, statements, encounter attachments, other documents). These preserve the original document content.

**Thinnest areas:**
- **Messages** (5 fields): Only ID, Date, Subject, Notes, Sender. Unclear if this captures patient portal secure messages or only internal staff messages. No threading, no recipient info.
- **Patient Notes** (2 fields) and **Patient Alert** (2 fields): Minimal structured data.
- **Health Maintenance** (7 fields): Only due/tentative tests; historical data not exported.
- **Vitals** (element 24, 11 fields): Exports only latest encounter vitals. However, element 37 ("All Vitals", 11 fields) exports vitals across all encounters, compensating for this.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics` (131 fields), `Guarantor` (22 fields) | Thorough — includes race, ethnicity, sexual orientation, gender identity, emergency contacts, multiple PCPs |
| Encounters / Visits | ✅ Covered | `Enc Progress Notes` (63 fields), `Future Appointments` (18 fields), `Past Appointments` (17 fields) | Solid — encounters include multiple provider roles, insurance linkage |
| Problems / Conditions / Diagnoses | ✅ Covered | `Diagnosis Code` (11 fields), `Past Medical Hist` (9 fields), `Family History` (7 fields) | ICD-9, ICD-10, SNOMED coded |
| Medications / Prescriptions | ✅ Covered | `Current Medication` (18 fields), `Prescriptions` (20 fields) | Current meds + full Rx history; NDC, RxNorm coded |
| Allergies | ✅ Covered | `Allergy` (13 fields) | RxNorm, NDC, SNOMED coded reactions |
| Immunizations | ✅ Covered | `Vaccination` (18 fields) | CVX coded, lot numbers, VIS dates, route/site |
| Vitals | ✅ Covered | `Vitals` (11 fields, latest encounter), `All Vitals` (11 fields, all encounters) | LOINC and SNOMED coded |
| Lab Results | ✅ Covered | `Lab Results` (23 fields), `Lab Test Result Values` (38 fields) | Order metadata + discrete results with LOINC, ranges, units |
| Imaging / Diagnostic Reports | ✅ Covered | `Rad Results` (21 fields) | Order/result metadata; no DICOM image export (product likely stores orders/results, not images) |
| Procedures | ✅ Covered | `Surgery` (6 fields), `CPT Codes` (10 fields), `HCPC Codes` (10 fields), `Procedure Orders` (33 fields), `Procedure Notes` (3 fields + PDFs) | Surgical history, encounter procedure codes, and procedure order/results |
| Clinical Notes / Documents | ✅ Covered | `Enc Progress Notes` (63 fields + PDFs), `Old Progress Notes` (PDFs), `Procedure Notes` (PDFs), `Legal Documents` (PDFs), `Other Documents` (PDFs), `Enc Attach Docs` (PDFs), `Letters` (16 fields + PDFs), `Patient Notes` (2 fields), `Patient Alert` (2 fields) | 9 entities across notes, documents, and attachments; PDF preservation |
| Care Plans / Goals | ⚠️ Partial | `Health Maintenance` (7 fields) — only due/tentative tests | Health maintenance reminders exported, but no structured care plans or clinical goals |
| Orders / Referrals | ✅ Covered | `Procedure Orders` (33 fields), `Consults` (30 fields) | Orders with scheduling, results, multi-provider roles |
| Insurance / Coverage | ✅ Covered | `Insurance Master` (22 fields), `Patient Insurance` (60 fields), `Adjusters` (33 fields), `Attorneys` (16 fields), `Patient Cases` (41 fields) | Detailed; includes eligibility, pre-authorization, workers' comp case management |
| Claims / Billing | ✅ Covered | `Billing Claims` (185 fields), `Billing Charges` (123 fields), `Billing Ledger` (PDF), `Statements` (PDF) | Exceptionally detailed — multi-payer, EDI, collection agency, capitation. Conditional on billing module being enabled. |
| Payments | ✅ Covered | `Patient Advance` (30 fields) | Advance payments, copays, refunds with rendering/attending provider |
| Consents / Directives | ⚠️ Partial | `Legal Documents` (PDFs) | Legal documents exported as PDFs, but no structured consent data |
| Patient Communications / Portal Messages | ⚠️ Partial | `Messages` (5 fields) | Only 5 fields (ID, Date, Subject, Notes, Sender). Unclear if this captures portal messages. Product has patient portal with secure messaging — potential gap. |
| Specialty-specific (Workers' Comp) | ✅ Covered | `Patient Cases` (41 fields) | Injury details, WCAB#, case managers, approved amounts, lien notes |

**Domains covered**: 15 of 19 applicable domains have dedicated export entities. 3 have partial coverage. 1 (Care Plans/Goals) has only tangential coverage through health maintenance reminders.

**Key gap analysis**: The product stores data for patient portal messages, referral tracking, and pre-authorization tracking that may not be fully represented in the export. The "Messages" entity's 5 fields are thin relative to the product's secure messaging capability. However, the core clinical and billing domains are well-covered.

## 6. Documentation Quality

**Strengths:**
- Field-level documentation for 41 of 47 data elements (1,185 fields)
- Each data element has a description explaining what data it covers
- Export workflow is clearly documented with step-by-step instructions and role requirements
- Important filtering notes (e.g., "Only active patient's details are exported," "Void claims will not be exported," "Lab results with status as 'Received' or 'Complete' are exported")
- Appendix explains the general export format structure (XLS/TXT for data, PDF for documents, HTML/XML for CCD)

**Weaknesses:**
- **No data types**: Every field is just a name — no indication of string, date, integer, boolean, decimal, etc.
- **No descriptions beyond the field name**: Fields like "Bool Icd10", "CLM053", "PATINV", "EDI Q" are unexplained
- **No value sets or code systems**: What values does "Claim Status" accept? What are the valid "Status Code" values? Not documented
- **No relationships/foreign keys**: How does a Billing Claim reference an Encounter? How does a Lab Test Result link to a Lab Results order? IDs exist but joins are not documented
- **No sample data or example exports**: A developer has no way to see what an actual export looks like
- **No machine-readable schema**: The only documentation is the PDF — no XSD, JSON Schema, DDL, or CSV header templates
- **Stale versioning**: Document is for version Denali 3.1 (2023); the newer CHPL listing (v4.0, certified 2025-12-24) references the same document
- **CCD field list inconsistency**: The CCD section (28) in the detailed description says only "This contains the CCD details" — the actual field list is buried in the Appendix section
- **Cryptic artifact "3032"**: The phone number suffix "3032" from the page footer bleeds into field names and descriptions throughout the text extraction (e.g., "3032 Emergency Contact Address Single Line"), indicating the PDF's layout causes parsing issues

**Developer usability**: A developer could build a basic import pipeline from this documentation — the field names are mostly self-explanatory and the per-entity XLS structure is straightforward. However, without data types, relationships, or value sets, significant reverse-engineering from actual export files would be required. This is a "get started" reference, not a complete integration specification.

## 7. Overall Assessment

### Classification

**Comprehensive native export**: PrognoCIS exports its native data model across clinical, billing, administrative, and document domains. The export is not a C-CDA or FHIR repackaging — it is a flat-file dump of internal database tables in XLS/TXT format with PDF document attachments. While the documentation has gaps (no types, no relationships, no value sets), the breadth of coverage across 47 data elements and 1,185+ fields with genuine billing depth (185-field claims, 123-field charges) places this clearly in the "comprehensive" tier.

### Key Findings

1. **Genuine native export, not standards repackaging**: The export format is proprietary XLS/TXT/PDF — not FHIR or C-CDA (except as one of 47 elements). Billing Claims alone has 185 fields covering EDI details, multi-payer amounts, and collection agency data. This is clearly derived from internal database tables, not a clinical summary projection.

2. **Billing coverage is exceptionally detailed**: 308 fields across billing entities (Claims: 185, Charges: 123, Advance: 30) — this is among the deepest billing exports observable. The export explicitly conditions on the billing module being enabled, meaning it's aware of its own scope.

3. **Documentation is field-name-only**: Despite listing 1,185 fields across 41 entities with field lists, not a single field has a data type, description (beyond its name), value set, or relationship documented. This is a significant documentation gap — the *coverage* is comprehensive but the *documentation quality* is thin.

4. **Patient population export requires vendor assistance**: Bulk export is handled by the Bizmatics Data Migration Team, not self-service. This raises compliance questions under (b)(10) which requires that population export capability exist. The single-patient export is fully self-service.

5. **Patient portal messages may be underrepresented**: The "Messages" entity exports only 5 fields (ID, Date, Subject, Notes, Sender) from "Message Compose screen." Given the product's patient portal with secure messaging, prescription refill requests, and appointment scheduling, this may not capture all patient-provider communications.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   XLS, TXT, PDF, HTML/XML (C-CDA for CCD element)
Model type:      Native database
Entities:        47
Fields:          1,185 (plus 6 standard patient identifier columns per file)
Descriptions:    0% (field names only; no per-field descriptions, types, or value sets)
Sample data:     No
Bulk export:     Vendor-assisted only (single-patient is self-service)
Domains covered: 15 of 19 applicable domains fully covered; 3 partial; 1 thin
```

### Bottom Line

PrognoCIS provides one of the more complete (b)(10) exports in terms of **data breadth** — 47 data element types spanning clinical, billing, administrative, and document domains, with genuinely deep billing coverage (308 fields). A patient or provider would get a meaningfully complete copy of their data. The biggest weakness is **documentation quality**: every field is a name with no type, description, or relationship information, and there are no sample exports or machine-readable schemas. The requirement for vendor assistance for population exports is also a compliance concern.
