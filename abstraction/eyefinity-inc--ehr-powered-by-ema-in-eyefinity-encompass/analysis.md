# EHI Export Analysis: Eyefinity, Inc.

**Product**: EHR powered by EMA in Eyefinity Encompass
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2900.Eyef.07.17.1.221219 (CHPL ID 11088)

## 1. Product Context

Eyefinity Encompass is a cloud-based integrated practice management (PM) and electronic health records (EHR) platform built specifically for eye care — primarily optometry practices, but also ophthalmology. Eyefinity, Inc. is a subsidiary of VSP Vision (the largest US vision benefits company), giving it unique integration with VSP insurance. The EHR component is built on Modernizing Medicine's EMA (Electronic Medical Assistant) platform, customized for eye care and branded as "Eyefinity EHR, powered by EMA."

The product serves over 7,000 independent optometry practices and is deployed in 20,000+ offices. Target users include providers, medical assistants, ophthalmic technicians, and administrators.

**Data domains relevant to EHI export completeness:**

- **Clinical documentation**: Eye exams (refraction, visual acuity, contact lens fitting, binocular vision, color vision, etc.), visit notes, problem lists, medication lists, allergy lists, medical/ocular/social/family history, immunizations, diagnostic imaging references (OCT, visual fields, fundus photos), vitals
- **Specialty data**: Eyeglass prescriptions, contact lens prescriptions (soft, RGP/hybrid), specialty contact lens parameters, IOL tracking, pathology/biopsy logs, cancer logs
- **Prescribing**: e-prescribing via Surescripts, eyeglass Rx, contact lens Rx
- **Lab/diagnostics**: Lab orders and results, pathology results
- **Practice management**: Scheduling, appointment management, billing, claims, insurance eligibility (including VSP-specific), payments, statements, ERA/remittance, refunds, accounts receivable
- **Patient engagement**: Secure messaging (IntraMail), patient portal, consent forms
- **Optical/inventory**: Optical lab orders, inventory management, package sales
- **Workflow**: Tasks, office flow tracking, referral management

The key question for this analysis: the EHI export documentation URL points to a ModMed-hosted data dictionary. Does it cover the full Eyefinity Encompass data model — including PM, scheduling, billing, and VSP-specific data — or only the EMA (EHR) portion?

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf` (684 KB, 131 pages) | Primary artifact: complete data dictionary for ModMed EMA EHI Export. Documents 196 database tables across 16 groupings with ~4,803 columns. | **Most informative** — the sole documentation artifact and quite substantial |
| `Data-Dictionary-for-ModMed-EMA-EHI-Export4.txt` (123 KB) | Plain text extraction of the PDF (pdftotext, no layout) | Derivative — used for orientation |
| `Data-Dictionary-layout.txt` (511 KB) | Layout-preserved text extraction (pdftotext -layout) | Derivative — used for column verification and cross-checking |
| `enrichment/data-dictionary.json` (174 KB) | Structured JSON parse of the PDF by a prior agent's Bun TypeScript script | Useful base — contains 197 entries (196 valid + 1 parse artifact) with some parser bugs corrected in this analysis |
| `enrichment/coverage-summary.json` (26 KB) | Statistics from the enrichment parse | Useful for cross-checking |
| `enrichment/extract-data-dictionary.ts` (10 KB) | The Bun TypeScript parser script | Reviewed to understand parse methodology and limitations |
| `enrichment/README.md` (2 KB) | Documentation for the enrichment scripts | Minor |

**Note**: There is exactly one primary artifact — the 131-page PDF data dictionary. No sample export data, no machine-readable schema (the JSON was derived by a prior agent, not provided by the vendor), no user guide beyond the PDF's introduction.

## 3. Export Mechanics

**Format**: ZIP file (`ehi_export.zip`) containing:
- `ehi_export/xxxx_data_extract/` — pipe-delimited CSV files, one per database table
- `ehi_export/attachments/` — human-readable files (XML, JPEG, PNG, TIFF, JSON, PDF) for imaging results, scanned clinical documents, lab attachments, prescription attachments, etc.

**Mechanism**: The PDF introduction states exports can be run "for a single or for multiple (all) patients." The exact UI/API mechanism is not described in the documentation.

**Single-patient vs bulk**: Both supported per the introduction.

**Access constraints**: Not documented. The PDF itself carries a confidentiality notice requesting recipients not share it with third parties, though it acknowledges 45 C.F.R. § 170.403 protections.

**Fees**: Not documented in the available artifacts.

## 4. Export Content: What's In It

### Data dictionary structure

The 131-page PDF documents database tables in a 5-column format:

| Column | Content |
|---|---|
| Grouping | Logical category (16 populated + 3 declared-but-empty) |
| Table | Database table name (snake_case) |
| Description | Prose description of the table's purpose and cardinality |
| Columns | Column names (snake_case) |
| Longitudinal Tracking | Y/N/L/S flag indicating history tracking behavior |

**What's documented**: Table names, table-level descriptions (195 of 196 tables have descriptions, 99.5%), column names, and longitudinal tracking flags.

**What's NOT documented**: Column-level data types, column-level descriptions, value sets/code systems, foreign key relationships (implied only through naming conventions like `patient_id`), field lengths (mentioned in the introduction as existing in a "Field Length column of the Data Dictionary sheet" but not present in the PDF), and sample data.

### Summary statistics

- **196 tables** across 16 groupings (after correcting parse artifacts)
- **~4,803 columns** total
- **0% of columns** have individual descriptions (only table-level descriptions exist)
- **0% of columns** have documented data types
- **3 groupings declared but empty**: Lookup, MIPS, Medical Lookup

### Vendor's own content organization

The vendor organizes tables into 16 populated groupings. Three additional groupings (Lookup, MIPS, Medical Lookup) are described in the introduction but contain no table entries.

| Grouping | Tables | Fields | Description |
|---|---|---|---|
| Ophth Pretesting | 25 | 1,242 | Contact lens fitting (wearing, trials, RGP), refraction, visual acuity, keratometry, binocular vision, cover test, color vision, diagnostic drops, visual fields, IOP, pachymetry, retinal thickness |
| PM Financials | 38 | 1,206 | Bills, charges, payments, claims, accounts receivable, refunds, statements, adjustments, ERA reconciliation, production summaries |
| Patient | 31 | 739 | Demographics, insurance policies, medical/surgical/family/social history, allergies, medications, problem list, immunizations, chart notes, secure messaging (IntraMail) |
| eLab | 19 | 237 | Lab orders, results, panels, observations, attachments |
| Prescription | 4 | 234 | Medication Rx, eyeglass Rx, contact lens Rx, RGP contacts Rx |
| Appointment | 10 | 209 | Appointments, logs, authorizations, waitlists, reminders, recall |
| Visit | 16 | 200 | Visit records, attendees, review of systems, vitals, billing codes (final/original), follow-ups, outcome measures, quality measures |
| Pathology | 8 | 149 | Pathology specimens, results, notifications, cancer logs (with linked procedures and medications) |
| Inventory | 5 | 119 | Package sales, itemized items, utilization |
| Document Management | 4 | 96 | File attachments, fax management (inbound/outbound) |
| Diagnosis | 9 | 93 | Findings/impressions, differential/associated/cause diagnoses, body locations, morphology, measurements, referrals |
| Office Flow | 7 | 82 | Tasks, task notes/attachments, staff/group assignees |
| CC/HPI | 6 | 72 | Chief complaint, history of present illness, follow-ups, body locations |
| Practice | 7 | 65 | Protocol logs, referral sources, referring/primary care provider mappings, visit referrals, consent forms |
| Procedure | 3 | 33 | Procedure body locations, metadata, MIPS quality measures |
| Exam | 4 | 27 | Exam sets, elements, metadata |

### Representative large entities

| Entity | Fields | Grouping | Description |
|---|---|---|---|
| `patient` | 177 | Patient | Demographics, practice data, single-response clipboard (race, ethnicity, gender identity, sexual orientation, language, contact info, emergency contacts, insurance summary) |
| `insurance_policy` | 136 | Patient | Insurance policy details per patient — one of the most detailed insurance tables seen in EHI exports |
| `bill` | 131 | PM Financials | Complete bill records with charges, payer info, status, dates |
| `production_summary` | 113 | PM Financials | Summarized charges, payments, payer/patient adjustments |
| `wearing_contacts` | 112 | Ophth Pretesting | Contact lens parameters the patient is currently wearing |
| `contacts_trial` | 107 | Ophth Pretesting | Contact lens trial data from eye exam |
| `binocular` | 107 | Ophth Pretesting | Binocular vision test battery |
| `glasses_rx` | 106 | Prescription | Eyeglass prescription details |
| `accounts_receivable` | 105 | PM Financials | Outstanding balance details |
| `charges` | 100 | PM Financials | Line-item charge details |

### Parser corrections

The original enrichment parse had several bugs, corrected in this analysis (see `analysis/build-corrected-inventory.py`):
- `allergy`: 0 → 25 columns (parser completely missed all columns)
- `keratometry`: 1 → 5 columns
- `central_retinal_thickness`: 1 → 6 columns
- `rgp_contacts_rx`: 2 parsed columns but PDF shows ~22 garbled entries (PDF rendering issue — column names all display as the table name)
- `diagnosis_referral_correspondence_id`: renamed to `diagnosis_referral_correspondence` (parser included `_id` suffix from the primary key column)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized around ModMed EMA's database model, covering clinical, financial, and specialty eye care data in impressive depth:

**Strongest areas:**
- **Ophthalmology/optometry specialty data** (1,242 fields across 25 tables): Exceptionally detailed coverage of eye-specific measurements — refraction, visual acuity, keratometry, binocular vision, cover test, color vision, contact lens fitting (soft, RGP, trials), visual fields, IOP, pachymetry, retinal thickness, amsler grid, light reflex, motility, duction, pupil assessment, diagnostic drops, infant vision. This is genuine specialty clinical data that would never appear in a C-CDA or FHIR US Core export.
- **Financial/billing data** (1,206 fields across 38 tables): Comprehensive PM financials covering the full billing lifecycle — bills, charges (posted/unposted/unbilled), claims (with submissions, logs, bill items), payments (posted/unposted/received), payer adjustments (with RARC codes), patient statements, refunds, pre-collections, accounts receivable, production summaries, transfer funds, billing quotes.
- **Patient demographics and history** (739 fields across 31 tables): Thorough demographics (177 fields for the patient table alone, including USCDI v2+ fields like gender identity, sexual orientation, preferred pronouns), insurance policies (136 fields), medical/surgical/family/social/specialty history, allergies (with detailed reactions), medications, problem list, immunizations.
- **Prescriptions** (234 fields across 4 tables): Medication Rx, eyeglass Rx (106 fields — exceptionally detailed), contact lens Rx (79 fields).

**Adequate areas:**
- **Lab orders and results** (237 fields across 19 tables): Covers electronic lab orders, results, attachments, and notes.
- **Visit/encounter data** (200 fields across 16 tables): Visit records, vitals, review of systems, billing codes, follow-ups, outcome measurements, quality measures.
- **Appointments** (209 fields across 10 tables): Scheduling, waitlists, reminders, recall.
- **Pathology** (149 fields across 8 tables): Pathology specimens, results, cancer logs with linked procedures and medications.

**Thinner areas:**
- **Exam** (27 fields across 4 tables): The virtual exam room elements are thinly documented.
- **Procedure** (33 fields across 3 tables): Procedure body locations and metadata; less detailed than expected for a surgical specialty.
- **Inventory** (119 fields across 5 tables): Only package sales; no frame/lens ordering, optical lab orders, or barcode inventory tracking despite the product offering these features.

**Declared but empty groupings:**
- **Lookup**: "Static lookup tables for medical and industry codes" — without these, coded values in the export (status codes, type codes, etc.) cannot be interpreted by a third party.
- **MIPS**: "MIPS scores, including overall scores and measure-specific scores"
- **Medical Lookup**: "Static lookup tables for medical content (CC/HPI, Exam, Diagnosis, Procedure, Pathology Log)"

The absence of lookup tables is a significant documentation gap. While the exported data includes coded fields, recipients cannot decode values like status codes, type identifiers, or medical content codes without the reference tables.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient` (177 fields) including name, DOB, sex, gender identity, sexual orientation, race, ethnicity, language, contact info, emergency contacts, preferred pronouns | Thorough — 177 fields is among the most detailed demographic exports observed |
| Encounters / visits | ✅ Covered | `visit` (41 fields), `visit_attendee` (8), `visit_follow_up` (21), `visit_code` (8), plus 8 billing code tables | Solid |
| Problems / conditions | ✅ Covered | `problem_list` (15 fields) | Adequate |
| Medications / prescriptions | ✅ Covered | `medication` (21 fields), `rx` (47 fields), `glasses_rx` (106), `contacts_rx` (79), `rgp_contacts_rx` (~2 parsed, likely more) | Strong — particularly for specialty prescriptions |
| Allergies | ✅ Covered | `allergy` (25 fields) including 14 specific reaction columns | Thorough |
| Immunizations | ✅ Covered | `immunization` (26 fields) | Adequate |
| Vitals | ✅ Covered | `vitals` (20 fields) | Adequate |
| Lab results | ✅ Covered | 19 eLab tables (237 fields): `elab_order`, `elab_result`, `lab_request`, `lab_result`, `result_log`, etc. | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | Attachments folder includes imaging files (JPEG, PNG, TIFF). Document Management tables reference file attachments. No structured imaging report tables (though diagnostic imaging data like OCT, visual fields is captured in Ophth Pretesting tables) | Eye-specific imaging captured in pretesting tables; general imaging reports only as attachments |
| Procedures | ✅ Covered | `procedure_body_location` (8), `procedure_metadata` (14), `procedure_mips_quality` (11), `procedure_log` (12) | Adequate |
| Clinical notes / documents | ✅ Covered | `chart_note` (26 fields), `chart_note_signature` (7), `file_attachment` (30), plus attachments folder | Solid |
| Care plans / goals | ⚠️ Partial | `visit_follow_up` (21 fields), `visit_follow_up_reason` (6) — follow-up plans exist but no explicit care plan entities | Product is certified for (b)(11) care plans; no dedicated care plan table in export |
| Orders / referrals | ✅ Covered | `diagnosis_referral` (9), `diagnosis_referral_correspondence` (19), `referral_source_link` (18), `visit_referral` (5), `order_log` (24) | Solid |
| Insurance / coverage | ✅ Covered | `insurance_policy` (136 fields), `insurance_group` (7), `insurance_group_policy` (8), `bill_insurance` (24) | Exceptionally detailed |
| Claims / billing | ✅ Covered | 38 PM Financials tables (1,206 fields): `claim` (45), `charges` (100), `bill` (131), `accounts_receivable` (105), etc. | One of the most comprehensive billing exports observed |
| Payments | ✅ Covered | `payments_posted` (56), `payments_received` (50), `patient_payments_unposted` (30), `transfer_funds` (20), `refunds` (54) | Thorough |
| Consents / directives | ⚠️ Partial | `consent_form_patient` listed in Practice grouping; `patient` table includes `health_care_proxy`, `living_will`, `do_not_intubate`, `do_not_resuscitate` fields | Advance directives captured as patient fields; consent forms exist but details thin |
| Patient communications | ✅ Covered | `intra_mail` (17 fields), `intra_mail_recipient` (10) | Adequate for secure messaging |
| Specialty-specific (eye care) | ✅ Covered | 25 Ophth Pretesting tables (1,242 fields), 4 Prescription tables (234 fields including eyeglass/contact lens Rx), `pathology_log` (37), `cancer_log` (54) | **Exceptionally strong** — this is the standout feature of this export |

**Domains not applicable to this product:**
- N/A: This product does not appear to store general hospital-level data (ICU, surgical suites, etc.)

## 6. Documentation Quality

**Strengths:**
- Substantial scope: 131 pages documenting 196 tables and ~4,803 columns
- Every table has a prose description explaining purpose and cardinality (99.5%)
- Longitudinal tracking flags (Y/N/L/S) clearly indicate which tables preserve history vs. snapshots
- Export format and folder structure clearly documented
- UTC vs. local time conventions documented

**Weaknesses:**
- **No column-level descriptions**: Only table-level descriptions exist. A field named `status` in the `claim` table could mean anything without a per-field description.
- **No data types**: The introduction mentions a "Field Length column of the Data Dictionary sheet" but this is not present in the PDF. No column has a documented type (integer, varchar, date, boolean, etc.).
- **No value sets**: Coded fields (status codes, type identifiers, category codes) have no documented allowed values. Compounded by the three empty lookup groupings.
- **No foreign key documentation**: Relationships must be inferred from naming conventions (e.g., `patient_id` in multiple tables presumably references `patient.patient_id`).
- **No sample data**: No example export files or worked examples showing actual pipe-delimited output.
- **No machine-readable schema**: The data dictionary is a PDF generated from Google Docs. No JSON schema, SQL DDL, or other machine-processable format.
- **Confidentiality notice conflicts with transparency**: The PDF asks recipients not to share the document with third parties — unusual for ONC-mandated documentation.

**Could a developer build an import from this documentation?** Partially. A developer could identify tables and columns, load the pipe-delimited CSV files, and establish basic relationships through naming conventions. However, interpreting coded values, understanding data types, and resolving ambiguous column names would require trial-and-error with actual export data. The missing lookup tables are the biggest barrier — without them, many fields are opaque integers or codes.

## 7. Overall Assessment

### Classification

**Comprehensive native export** — with documentation gaps.

This is a genuine native database model export covering 196 tables across clinical, financial, and specialty domains. It is not a C-CDA or FHIR repackaging. The export covers the full breadth of data the EHR/PM system stores, including deep specialty eye care data (1,242 fields) and comprehensive billing/financial data (1,206 fields) that would never appear in a clinical summary standard. The primary weaknesses are documentation depth (no column descriptions, types, or value sets) and the three declared-but-empty lookup groupings that prevent full interpretation of coded fields.

### Key Findings

1. **Genuine native database export with exceptional specialty depth**: 196 tables, ~4,803 columns covering clinical, billing, and specialty eye care data in native pipe-delimited CSV format. The 25 Ophth Pretesting tables (1,242 fields) represent one of the most detailed specialty clinical data exports observed, documenting every aspect of ophthalmic examination from refraction through retinal thickness. (Source: `Data-Dictionary-for-ModMed-EMA-EHI-Export4.pdf`, pages 6–131)

2. **Comprehensive billing coverage**: 38 PM Financials tables (1,206 fields) covering the full billing lifecycle — charges, claims, payments, adjustments, statements, refunds, accounts receivable, pre-collections. This is meaningfully more billing depth than most EHI exports provide. (Source: PM Financials grouping, pages 74–131)

3. **Missing lookup tables undermine interpretability**: Three groupings are declared in the introduction but contain no table entries: Lookup, MIPS, and Medical Lookup. Without reference data for coded values, recipients cannot fully interpret status fields, type codes, or medical content codes. This is the single biggest gap. (Source: PDF introduction, page 3)

4. **No column-level metadata**: While table-level descriptions are excellent (99.5% coverage), zero columns have individual descriptions, data types, or value set documentation. For a 4,803-column export, this significantly increases the effort required to use the data. (Source: analysis of full data dictionary)

5. **Shared ModMed artifact, not Eyefinity-specific**: This data dictionary is hosted on modmed.com and titled "ModMed EMA EHI Export." It is the same document used by all ModMed EMA products. The PM tables note they "will be empty for practices not using PM" — suggesting the export framework encompasses both EHR and PM data, though Eyefinity PM-specific features (VSP integration, optical lab ordering) may not be fully represented.

### Summary Stats

    Classification:  Comprehensive native export
    Export format:   Pipe-delimited CSV (one file per table) + attachments (XML, JPEG, PNG, TIFF, JSON, PDF)
    Model type:      Native database model
    Entities:        196 tables across 16 groupings
    Fields:          ~4,803
    Descriptions:    0% of fields (99.5% of tables have table-level descriptions)
    Sample data:     No
    Bulk export:     Yes (single-patient and multi-patient/all)
    Domains covered: 14 of 16 applicable domains (care plans partial, imaging reports partial)

### Bottom Line

This is one of the stronger (b)(10) exports analyzed. A patient or provider would receive a genuinely comprehensive copy of their data — 196 native database tables covering clinical encounters, specialty eye care measurements, billing, prescriptions, lab results, and attachments. The biggest gap is not data breadth but data interpretability: without column descriptions, data types, and especially the missing lookup tables, a recipient would struggle to fully decode the exported data without substantial reverse-engineering effort.
