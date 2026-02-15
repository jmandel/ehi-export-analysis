# EHI Export Analysis: Qualifacts Systems, LLC

**Product**: Insync EMR/PM, Version 10
**Analysis date**: 2026-02-15
**CHPL ID**: 15.02.05.3124.INSY.01.03.1.220314 (CHPL #10858)

## 1. Product Context

InSync EMR/PM is a cloud-based, fully integrated electronic health record and practice management platform targeting **small to mid-size behavioral health, rehabilitative therapy, and medical practices**. Originally developed by InSync Healthcare Solutions (acquired by Qualifacts in December 2021), it serves solo practitioners through mid-size agencies across behavioral health (mental health, SUD, IDD), rehabilitative therapy (PT, OT, SLP), and ambulatory medical specialties.

Key data domains the export should cover:

- **Clinical documentation**: Progress notes, treatment plans, assessments (including behavioral health-specific instruments like ASAM), therapy notes (individual, group, telehealth), H&P, procedure notes, discharge summaries
- **Charting**: Problems/diagnoses, medications/ePrescribing/EPCS, allergies, immunizations, vitals, lab results, referrals, care plans/goals
- **Billing/PM**: Claims, charges, payments, denials, EOBs, insurance coverage, prior authorizations, price estimates, financial assistance, billing statements
- **Patient management**: Demographics, relationships/contacts, consents, patient portal messages, intake forms, custom dynamic forms
- **Specialty data**: Psychiatric history, substance abuse, behavioral data, OB/GYN history, pregnancy tracking, case management, program enrollment
- **Documents**: Uploaded/scanned documents, images, e-faxes, clinical forms with eSignatures
- **Medication management**: ePrescriptions, eMAR, PDMP queries, medication history

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `insync-ehi-export.html` (9,900 bytes) | Main EHI export documentation page (Sphinx-generated). Describes single-patient and population export workflows, NDJSON format, document attachment structure. | **High** — primary source for export mechanics |
| `InSync_EHI_Export_Data_Dictionary.xls` (1.5 MB) | XLS with 84 sheets: INDEX, Changelogs, Confidential Notice, and 81 data section sheets. Last saved 2025-11-17 by Rob Sipe. | **Critical** — primary source for export content |
| `Qualifacts_EHI_Export_Terms_of_Use_SEP_2024.pdf` (3 pages, 149 KB) | Legal terms governing EHI export requests. Includes usage restrictions, disclaimers, indemnification. | **Low** — operational/legal only |
| `enrichment/data-dictionary.json` (241 KB) | Machine-readable JSON extraction of all 81 sections and 960 fields from the XLS. | **High** — enabled programmatic analysis |
| `enrichment/extraction-stats.json` (15 KB) | Parse accounting: 84 sheets, 81 parsed, 0 failures. | **Medium** — confirmed completeness of extraction |

## 3. Export Mechanics

- **Format**: Newline Delimited JSON (NDJSON) — a vendor-native flat JSON structure, not FHIR or C-CDA. Attachments (documents, images) are exported as physical files in a "Supported File" folder.
- **Mechanism**: Two modes:
  - **Single Patient Export**: Initiated by designated agency staff within InSync upon patient request. Produces a ZIP with one NDJSON file + attachments folder.
  - **Patient Population Export**: Requested by submitting a ticket through Qualifacts Care Center. Qualifacts staff initiates. Produces a ZIP with one JSON file per patient + shared attachments folder. Up to 30 calendar days to complete. Requires acceptance of Terms of Use.
- **Access**: Completed exports appear in the requester's To Do list within InSync. Download links expire after 30 calendar days.
- **Bulk capability**: Yes, via the population export path, though it requires vendor involvement and a 30-day wait.
- **Access constraints**: Population exports limited to one request at a time; require Terms of Use acceptance. No fee mentioned.

## 4. Export Content: What's In It

The export is documented through an XLS data dictionary containing **81 data sections** with **960 total fields**. The XLS was verified directly (`xlrd` parsing of the raw `.xls` file) — all counts are independently confirmed.

### Documentation structure per section

Each of the 81 sheets contains:
- A section description (1-2 sentences)
- A field table with columns: Row #, Name of the Column, Data Type, Nullable, Used For (description), Remarks

### Field-level statistics

| Metric | Count | Percentage |
|---|---|---|
| Total fields | 960 | — |
| Fields with data types | 960 | 100% |
| Fields with any description ("Used For") | 960 | 100% |
| Fields with non-trivial descriptions | 905 | 94.3% |
| Fields with remarks | 0 | 0% |

Data types used: String (603), INT (140), Date (57), DateTime (45), Boolean (45), Numeric (35), FLOAT (14), DECIMAL/Decimal (8), BIT (3), TINYINT (3), DATE (2), SMALLINT (2), TIME/Time (2), BIGINT (1).

**Description quality**: Every field has a "Used For" description. Most descriptions are brief restatements of the field name (e.g., `PatientFirstName` → "Patient First Name"). About 5.7% of descriptions are trivially tautological (identical to the column name once normalized). The "Remarks" column is completely empty across all 960 fields. Notably, the Program section (29 fields) contains **copy-paste errors** from the Patient Pharmacy section — fields like `Level of Care Start Date` are described as "Fax" and `PrimaryPayer` as "Controlled Substance" (verified in raw XLS, rows 14–18 of the Program sheet).

**What's missing from documentation**:
- No value sets or enumeration values for coded fields (e.g., `PatientGender`, `AllergiesSeverityCode`, `TransmissionType`)
- No relationship/foreign key documentation between sections
- No cardinality information (which sections are arrays vs. single values)
- No JSON Schema or machine-readable format specification
- No sample export file (only one JSON snippet showing the Documents/Images array structure)

### Vendor's own content organization

The INDEX sheet classifies sections by Category (EMR, PM, EMR/PM, EHI Export) and Module. The 9 sections with blank categories in the enrichment JSON all have proper assignments in the INDEX sheet — the mismatch is due to sheet name truncation in the XLS format.

**Corrected category breakdown** (from INDEX sheet):

| Category | Sections | Total Fields |
|---|---|---|
| EMR | 64 | 756 |
| PM | 12 | 99 |
| EMR / PM | 5 | 107 |
| EHI Export | 1 | 3 |
| **Total** | **81** | **960** |

Note: The count above corrects the enrichment's 9 "unclassified" sections using the INDEX: Clinical tests/Results, Functioning/Functional Status, Health Concerns/Reason for Visit, Documents/Images, Additional/Clinical Forms, List of prices/charges, Chief Complaints/HPI, Case Management, and Pregnancy Status all have proper EMR or PM assignments in the INDEX.

**Module breakdown** (from INDEX sheet):

| Module | Sections | Total Fields |
|---|---|---|
| Patient Demographic | 32 | 372 |
| Charting | 25 | 342 |
| Patient Insurance | 3 | 73 |
| Claims | 2 | 21 |
| Practice Management | 1 | 20 |
| Patient Estimator Calculator | 1 | 17 |
| Sliding Fee Scale | 1 | 16 |
| Payments | 3 | 13 |
| Audit Logs | 1 | 12 |
| Census | 1 | 10 |
| ERA | 1 | 8 |
| Financial Summary | 1 | 6 |
| Document Manager | 1 | 5 |
| Patient Data Export | 1 | 3 |
| Interface | 1 | 2 |
| Other (-) | 3 | 25 |

### Top 20 largest sections (representative examples)

| Section | Fields | Category | Module |
|---|---|---|---|
| Patient Demographics / Information | 64 | EMR | Patient Demographic |
| Health Insurance Information / Payer | 46 | EMR / PM | Patient Insurance |
| Vital signs | 43 | EMR | Charting |
| Case Management | 40 | EMR | Patient Demographic |
| Program | 29 | EMR | Patient Demographic |
| Newborn Delivery Information | 26 | EMR | Charting |
| Patient relationships | 22 | EMR | Patient Demographic |
| Encounter information | 21 | EMR | Charting |
| Patient Summary and Plan | 21 | EMR | Charting |
| Prior Authorizations or Authorizations | 21 | EMR / PM | Patient Insurance |
| Diagnostic Imaging | 20 | EMR | Charting |
| Organization | 20 | EMR / PM | Practice Management |
| Past Pregnancy Data | 19 | EMR | Charting |
| Claims | 18 | PM | Claims |
| Immunizations | 18 | EMR | Charting |
| Gynecological History | 18 | EMR | Charting |
| Price Estimates given to patient | 17 | PM | Patient Estimator Calculator |
| Work information | 17 | EMR | Patient Demographic |
| Financial Assistance applications | 16 | PM | Sliding Fee Scale |
| Family Health History | 15 | EMR | Patient Demographic |

### Notable data quality issue

The Program sheet (29 fields) contains description errors where pharmacy-related descriptions leaked into unrelated fields. Specifically:
- `Level of Care Start Date` → described as "Fax"
- `Level of Care End Date` → described as "Email"
- `ProgramType` → described as "Is Retail"
- `PrimaryPayer` → described as "Controlled Substance"
- `SecondaryPayer` → described as "Is Twenty Four Hours Store"

These are copy-paste errors from the Patient Pharmacy sheet, confirmed by examining the raw XLS. The field names themselves are correct; only the descriptions are wrong.

### Changelog history

The data dictionary has been actively maintained through 7 versions:

| Version | Date | Description |
|---|---|---|
| 1 | 2023-09-04 | Initial release |
| 2 | 2023-10-02 | New sections added |
| 3 | 2023-10-06 | New sections added |
| 4 | 2024-07-30 | Sprint 36 — new fields |
| 5 | 2025-01-24 | Sprint 49 — Fractional Units in Patient Program |
| 6 | 2025-06-27 | Sprint 60 — Out-of-Pocket Payments in Collection Information |
| 7 | 2025-10-31 | Sprint 69 — USCDI v3.1 updates |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into EMR (clinical) and PM (billing/financial) categories with modules reflecting InSync's internal product structure.

**EMR — Patient Demographic module (32 sections, 372 fields)**: The deepest module, covering demographics (64 fields), patient relationships (22 fields), work info (17 fields), family/medical/surgical/psychiatric/genetic history, smoking status, substance abuse, behavioral data, social history, consents, medical devices, referring diagnoses, patient pharmacy, program enrollment (29 fields), case management (40 fields), pregnancy status/intent, and care setting histories (hospice, palliative, long-term care). This module reflects InSync's behavioral health/rehabilitative focus — psychiatric history, behavioral data, and substance abuse are dedicated sections.

**EMR — Charting module (25 sections, 342 fields)**: Covers clinical encounter documentation: encounters (21 fields), clinical notes (13 fields with note types: consultation, discharge, H&P, procedure, progress, imaging, lab, pathology, charting, assessment, plan, health concerns), vital signs (43 fields — very granular), medications (12 fields), allergies (11 fields), immunizations (18 fields), procedures (10 fields), problems (8 fields), goals (11 fields), assessments/treatment plans (7 fields), diagnostic imaging (20 fields), clinical test results (12 fields), and OB/GYN data across 4 sections (pregnancy info, newborn delivery, gynecological history, past pregnancy — 76 fields total). Also includes physical exam (7), ROS (8), chief complaints/HPI (11), health maintenance (6), nutrition/diet (6), referrals (6), patient summary/plan (21), review of results (7), functional status (8), and additional clinical forms (4 fields).

**PM — Billing/Financial modules (12 sections, 99 fields)**: Claims (18 fields), billing codes (3 fields), billing statements (6 fields), charges/refunds/deductibles (6 fields), collection info (3 fields), denials (4 fields), EOB/ERA (8 fields), list of prices (2 fields), price estimates (17 fields), financial assistance (16 fields), eligibility (6 fields), census data (10 fields).

**EMR / PM crossover (5 sections, 107 fields)**: Health insurance (46 fields — very detailed subscriber/payer data), prior authorizations (21 fields), organization data (20 fields), care team members (8 fields), event logs (12 fields).

**Richest areas**: Patient Demographics (64 fields), Health Insurance (46 fields), Vital Signs (43 fields), Case Management (40 fields), Program (29 fields), Newborn Delivery (26 fields). The behavioral health sections (Psychiatric History, Behavioral Data, Substance Abuse) are present but relatively thin (7, 4, and 5 fields respectively).

**Thinnest areas**: List of prices/charges (2 fields — just CPT code and billed amount), Custom Field (2 fields), Social History Elements (2 fields), HL7 ADT notifications (2 fields), Pregnancy Intent (2 fields).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics / Information` (64 fields), `Recorded Sex or Gender` (4), `Custom Field` (2), `Work information` (17) | Thorough — SSN, race, ethnicity, language, address, phone, email |
| Encounters / visits | ✅ Covered | `Encounter information` (21 fields) — type, provider, facility, POS code, CPT codes, insurance, authorization | Solid — includes visit context and billing linkage |
| Problems / conditions | ✅ Covered | `Problems` (8 fields) — ICD codes, onset/resolved dates, SNOMED codes | Adequate |
| Medications / prescriptions | ✅ Covered | `Medications` (12 fields) — RXCUI, SIG, status, dates, dose, dispense quantity | Good for medication list; lacks ePrescription transaction details and eMAR records |
| Allergies | ✅ Covered | `Allergies` (11 fields) — RXCUI, SNOMED, severity, reaction, codes | Thorough with standard coding |
| Immunizations | ✅ Covered | `Immunizations` (18 fields) — CVX codes, manufacturer, lot numbers, route, site | Thorough |
| Vitals | ✅ Covered | `Vital signs` (43 fields) — very granular, includes BMI, BP, pulse ox, pain scale | Among the most detailed sections |
| Lab results | ✅ Covered | `Clinical tests Results` (12 fields) — LOINC codes, values, units, reference ranges | Adequate |
| Imaging / diagnostic reports | ✅ Covered | `Diagnostic Imaging` (20 fields) — includes order info, results, LOINC, SNOMED | Thorough |
| Procedures | ✅ Covered | `Procedures` (10 fields) — CPT/HCPCS codes, modifiers, SNOMED | Adequate |
| Clinical notes / documents | ✅ Covered | `Clinical notes` (13 fields — multiple note types), `Documents / Images` (5 fields + physical files), `Additional Clinical Forms` (4 fields) | Good — covers structured notes and document attachments |
| Care plans / goals | ✅ Covered | `Goals` (11 fields), `Assessments and Plan of Treatment/Plan of Care` (7 fields), `Patient Summary and Plan` (21 fields) | Thorough — treatment planning well-represented |
| Orders / referrals | ✅ Covered | `Referrals` (6 fields), `Referring Diagnosis` (6 fields) | Adequate |
| Insurance / coverage | ✅ Covered | `Health Insurance Information / Payer` (46 fields), `Eligibility Information` (6 fields), `Prior Authorizations` (21 fields) | Very thorough — detailed subscriber data, authorization tracking |
| Claims / billing | ✅ Covered | `Claims` (18 fields), `Billing codes assigned` (3), `List of prices/charges` (2) | Good — claim lifecycle with payer/authorization linkage |
| Payments | ✅ Covered | `Charges, refunds, deductibles, interest paid/due` (6 fields), `Collection information` (3), `Billing statements and summaries` (6), `Denials` (4), `Explanation of benefits` (8), `Financial Assistance` (16), `Price Estimates` (17) | Very thorough — multiple financial sections |
| Consents / directives | ✅ Covered | `Consents (TPO, negotiated, HIE, medication, etc.)` (6 fields) | Adequate |
| Patient communications | ⚠️ Partial | No dedicated section for portal messages. `Patient education / Instruction` (6 fields) covers educational materials. | Product has secure messaging via patient portal; no explicit section for message content in the export |
| Specialty-specific (Behavioral Health) | ✅ Covered | `Psychiatric History` (7), `Behavioral Data` (4), `Substance Abuse` (5), `Social History Consumption` (13), `Social History Elements` (2) | Present but relatively thin for a behavioral-health-focused product. Generic question/answer format in Behavioral Data suggests custom assessments are captured but structure is opaque |
| Specialty-specific (OB/GYN) | ✅ Covered | `Pregnancy information` (13), `Newborn Delivery Information` (26), `Gynecological History` (18), `Past Pregnancy Data` (19), `Medical History (Ob/Gyn)` (13), `Pregnancy Intent` (2), `Pregnancy Status` (5) | Very thorough — 7 dedicated sections, 96 fields |
| Specialty-specific (Rehabilitative/Case Mgmt) | ✅ Covered | `Case Management` (40 fields), `Program` (29 fields) — accident/injury tracking, visit caps, payer authorization, referral source | Thorough — reflects product's rehabilitative therapy market |

**Domains covered**: 19 of 20 applicable domains are covered (✅ or ⚠️). Patient communications/portal messages is the only notable gap.

## 6. Documentation Quality

**Strengths**:
- The data dictionary is **extensive** (81 sections, 960 fields) and covers both EMR and PM modules comprehensively.
- Every field has a name, data type, nullable flag, and description (100% coverage).
- The INDEX sheet provides clear category/module classification for every section.
- Active maintenance (7 versions over 2+ years, most recently October 2025 for USCDI v3.1).
- The export page clearly distinguishes single-patient vs. population workflows.
- The enrichment team already parsed the XLS into machine-readable JSON, demonstrating the dictionary is parseable.

**Weaknesses**:
- **No sample export file**: Only one JSON snippet (for Documents/Images array). No complete patient JSON example exists.
- **No JSON Schema**: No machine-readable format specification beyond the XLS.
- **Descriptions are surface-level**: Most just restate the field name with spaces. They don't explain semantics, business rules, or valid values.
- **No value sets**: Coded fields like `PatientGender`, `AllergiesSeverityCode`, `TransmissionType`, `InsuranceTypeCode` have no enumerated values.
- **No relationships/foreign keys**: The export is flat NDJSON, but how sections relate to each other (e.g., which encounters link to which claims) is undocumented.
- **No cardinality**: No indication of which sections are arrays vs. scalars.
- **Copy-paste errors**: The Program section has 5 fields with incorrect descriptions from the Patient Pharmacy section (confirmed in raw XLS).
- **Remarks column entirely empty**: Not a single remark across 960 fields despite the column existing.

**Developer usability**: A developer receiving this export could identify and parse fields but would need to **reverse-engineer** the JSON structure, relationships, coded values, and array cardinality from actual export data. The documentation is sufficient for orientation but insufficient for building a reliable import pipeline without sample data.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine native data model export with broad coverage across clinical, billing, and specialty domains. The NDJSON format is clearly distinct from their FHIR API (documented separately). The 81 sections and 960 fields span EMR and PM modules, covering behavioral health, OB/GYN, rehabilitative therapy, billing, insurance, financial assistance, and clinical documentation. While documentation depth is moderate (descriptions but no value sets or relationships), the **scope** of the export is genuinely comprehensive.

### Key Findings

1. **Genuine (b)(10) export, not repackaged FHIR/C-CDA**: The export uses a vendor-native NDJSON format covering 81 data sections — far broader than USCDI clinical summaries. The Qualifacts documentation site explicitly separates EHI export from FHIR API documentation.

2. **Broad cross-domain coverage**: 19 of 20 applicable EHI domains are covered across clinical (EMR) and billing (PM) modules, including specialty behavioral health data, OB/GYN, case management, insurance, claims, payments, denials, EOBs, financial assistance, and price estimates. This is notably more complete than most vendor exports.

3. **Active maintenance**: 7 versions over 2+ years (Sept 2023 – Oct 2025), with the latest update adding USCDI v3.1 support. The data dictionary is actively evolving with sprint releases.

4. **Documentation is wide but shallow**: While 100% of fields have descriptions and types, descriptions are mostly tautological restated field names. No value sets, no relationships, no sample data, no JSON schema. The Remarks column is empty across all 960 fields. The Program section has copy-paste errors affecting 5 field descriptions.

5. **Patient portal messages appear missing**: Despite InSync offering secure messaging and a patient portal, no dedicated export section covers portal messages or patient-provider communications. This is the most notable content gap.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   NDJSON (vendor-native flat JSON) + file attachments
Model type:      Native database model
Entities:        81 sections
Fields:          960
Descriptions:    100% have descriptions; ~94% non-trivial
Sample data:     No (one JSON snippet only)
Bulk export:     Yes (population export via vendor ticket, up to 30 days)
Domains covered: 19 of 20 applicable domains
```

### Bottom Line

InSync EMR/PM provides a genuinely comprehensive EHI export that covers the vast majority of data domains the product stores — clinical, billing, behavioral health, OB/GYN, rehabilitative therapy, and financial data. The primary limitation is documentation depth, not scope: a developer could identify what's in the export but would need sample data to build a reliable import. The single biggest gap is the absence of patient portal messages/communications from the export, and the biggest documentation weakness is the complete lack of value sets for coded fields.
