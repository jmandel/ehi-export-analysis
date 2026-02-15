# EHI Export Analysis: Nth Technologies, Inc.

**Product**: nAbleMD 6.0c
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2070.nAbl.06.01.1.221221

## 1. Product Context

nAbleMD is a cloud-based, integrated EMR and practice management (PM) platform built by Nth Technologies, Inc. (Houston, TX, ~11–50 employees), targeting small-to-medium ambulatory practices. The product has a strong niche in **fertility/IVF clinics** (200+ providers, 1M+ completed cycles via the nAble IVF module) and also serves OB/GYN, family medicine, internal medicine, pediatrics, cardiology, gastroenterology, ENT, urology, general surgery, urgent care, and behavioral health.

Key data domains the product stores (relevant for export completeness):

- **Patient demographics & registration** — addresses, contacts, insurance, partner info, custom fields
- **Clinical documentation** — chart notes, HPI, physical exams, assessments, plans, specialty templates
- **Medications & e-Prescribing** — via NewCrop/Surescripts integration
- **Allergies** — via NewCrop
- **Problems/diagnoses** — ICD-10 coded
- **Lab orders & results** — LabCorp and other lab interfaces
- **Vital signs & measurements**
- **Immunizations** — with public health registry reporting
- **Documents & images** — scanned charts, photographs, DICOM images, faxes, HL7 messages
- **Billing & revenue cycle** — charge capture, claims submission, payments, eligibility, ICD-10/CPT coding, statement generation
- **Insurance/coverage** — payer records, prior authorizations
- **Patient portal** — secure messaging, self-scheduling, health history forms, consent management
- **SMS communications** — via Navicure/SMS integration
- **IVF/fertility-specific** — cycle management, oocyte tracking, embryology, cryostorage, semen analysis, donor evaluations, SART reporting
- **OB/GYN-specific** — pregnancy history, OB ultrasound, estimated due dates, contraception
- **Care plans & wellness plans**
- **Referrals & transfers**
- **Surgical history**

The mandatory disclosures page notes that "images and non-standard documentation require separate one-time fees for bulk export," indicating the system stores a meaningful volume of binary document data.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `downloads/certification-page.html` (36 KB) | HTML source of the nAbleMD mandatory disclosures page at `nablemd.com/certification2015.html` | **Medium** — contains the EHI export link and the data portability disclosure about fees for image/document export |
| `downloads/csv-sheets/read_me.csv` | Export process instructions, format documentation, document repository description | **High** — detailed export mechanics (authorization, single-patient vs bulk, encryption, retrieval) |
| `downloads/csv-sheets/table_of_contents.csv` | Index of all 106+ data tables in the export | **High** — complete inventory of exported entities |
| `downloads/csv-sheets/revision_history.csv` | Version tracking (v1.0 11/30/2023, v1.0.1 12/12/2023) | **Low** — only 2 entries |
| `downloads/csv-sheets/*.csv` (106 data table CSVs) | Individual data dictionary tabs, each documenting one CSV export table with FieldName and Description columns | **High** — this is the core artifact; 106 entities with 2,995 described fields |
| `downloads/screenshot-certification-page.png` (737 KB) | Full-page screenshot of certification/disclosures page | **Low** — confirms page layout |
| `downloads/screenshot-ehi-export-section.png` (7 KB) | Focused screenshot of EHI export heading and link | **Low** — confirms the link exists |
| `downloads/screenshot-gsheet-overview.png` (326 KB) | Screenshot of Google Sheets showing tabs | **Low** — confirms the spreadsheet structure |

**Most informative**: The 106 data dictionary CSV files and the `read_me.csv` file. Together they provide complete field-level documentation for the entire export, plus detailed export process instructions.

**Source**: All data dictionary CSVs were downloaded from a publicly accessible Google Sheets document linked from the certification page: [nAbleMD 6.0c export guide and data dictionary](https://docs.google.com/spreadsheets/d/11Yj6cH8GsXPnTuxDDIvYwgoF5sgM6zrwy4Ql6OEdWRQ/edit?gid=1058514257#gid=1058514257). Both the certification page and the Google Sheet were verified accessible on 2026-02-15.

## 3. Export Mechanics

**Format**: CSV files (one per data table) + a document repository folder, packaged in a 7-zip archive with AES-256 encryption, split into ~10 GB volumes (.zip.001, .zip.002, etc.).

**Mechanism**: Built-in UI at PM Home → System Configuration → Data Export. Requires:
1. Administrator grants user access to the Data Export screen
2. User must enable 2FA on their account
3. User clicks "Request Download" and enters an encryption password

**Single-patient vs bulk**:
- **Single patient**: Select a patient via the search, then "Request Download." Takes ~5 minutes per patient.
- **Full export**: Click "Request Download" without selecting a patient. Duration depends on total data volume.

**Retrieval**: Completed exports show checksums and download links. Files are retained on the server for 7 days.

**Access constraints**: The certification page discloses that "photographs, scanned images, faxes, other uploaded documents as well as medical documentation not included in the Common Data Set are not included in the export summaries. A one-time fee will be charged for the bulk export of these images, documents and documentation." This means the standard structured data export is included, but binary documents (PDFs, DICOM, HL7, faxes, etc.) require a separate paid export. The document repository is documented in the data dictionary (the `document` table with 58 fields references files in a Documents folder), so the technical capability exists.

## 4. Export Content: What's In It

The export contains **106 data tables** with a total of **2,995 fields**, all with plain-English descriptions (100% description coverage). The data dictionary is hosted as a Google Sheets workbook with 109 tabs (106 data tables + Read Me + Table of Contents + Revision History).

### Documentation structure

Each data table CSV follows a consistent format:
- **Table Description** (present in 3 tables: `patients`, `visit`, `insurance`) — 1–2 sentences describing the table's purpose and primary key
- **FieldName / Description** — two-column listing of every exported field with plain-English descriptions

Field descriptions are informative: dates are described as "Date when…", booleans as "Indicates if/whether…", foreign keys are identified by "identifier for…" or "Map with patientkey." Some descriptions note format details (e.g., "comma separated if multiple," gender codes "M:Male F:Female U:Unknown X:Undifferentiated Blank:Undocumented"). No explicit data types, constraints, or value set enumerations are provided as separate columns.

### Vendor's own content organization

The vendor organizes tables by naming convention rather than explicit categories. Based on prefixes and content analysis (see `analysis/full-entity-inventory.json` for complete inventory):

**Summary by category** (my categorization based on entity naming/content):

| Category | Entities | Fields | Description |
|---|---|---|---|
| IVF/Fertility | 32 | 1,216 | Cycle management, oocyte tracking, semen analysis, donor records, cryostorage, embryology, culture media |
| Patient/Demographics | 14 | 406 | Patient records, contacts, relatives, allowed contacts, kiosk answers, surveys, amendment requests |
| Scheduling/Workflow | 8 | 284 | Visits/encounters, appointments, waitlist, actions, tasks, daily worklist |
| Clinical/EMR | 16 | 247 | Assessments, HPI, chief complaint, reviews, medical history, surgery, encounter reports, checklist items |
| Billing/Financial | 7 | 176 | Insurance, procedures, charges, ledger items, payments, prepayments, prior authorizations |
| OB/GYN | 9 | 169 | OB history, pregnancy, pregnancy plan, estimated due dates, OB ultrasound, contraception, multiple births |
| Documents/Notes | 4 | 98 | Document repository metadata, chart notes, co-sign notes, chart documents |
| Labs/Results | 2 | 91 | Lab orders (40 fields), measurements/vitals (51 fields) |
| Medications/Allergies | 2 | 68 | NewCrop drug records (52 fields), NewCrop allergy records (16 fields) |
| Communications | 4 | 60 | Patient mail, SMS consent/messages/notifications |
| Immunizations | 2 | 52 | Immunization records (43 fields), immunization schedule (9 fields) |
| Care Plans | 2 | 45 | EMR plans, wellness plans |
| Problems/Conditions | 2 | 43 | Problems (with ICD codes), visit-specific problems |
| Procedures | 1 | 28 | Procedure codes, modifiers, NDC, anesthesia minutes |
| Consent | 1 | 12 | Completed consent forms |

**Top 10 largest entities:**

| Entity | Fields | Category |
|---|---|---|
| emrcycle | 231 | IVF/Fertility — comprehensive IVF cycle data |
| patients | 203 | Patient/Demographics — base patient record with demographics, clinical, insurance |
| emrivfobus | 162 | IVF/Fertility — OB ultrasound measurements during IVF |
| visit | 156 | Scheduling/Workflow — encounter/claim record with ICD codes 1–12, billing data |
| emroocyteday | 132 | IVF/Fertility — daily oocyte/embryo tracking |
| emrivfsample | 85 | IVF/Fertility — specimen/sample tracking |
| emrivffollicularus | 84 | IVF/Fertility — follicular ultrasound data |
| emrivfsemenanalysis | 81 | IVF/Fertility — semen analysis parameters |
| insurance | 65 | Billing/Financial — payer-level insurance records |
| document | 58 | Documents/Notes — document repository metadata |

### Notable details

- The **`visit` table** (156 fields) doubles as both the encounter record and the claim record, with fields for ICD codes 1–12, claim ID, place of service, provider, and charting/approval status. This confirms the integrated EMR/PM design.
- The **`patients` table** (203 fields) includes not just standard demographics but fertility-specific fields (blood type, Rh factor, partner info) and 10 custom fields.
- The **IVF domain** (32 entities, 1,216 fields) is remarkably deep — `emrcycle` alone has 231 fields covering every aspect of an IVF treatment cycle. This is specialty clinical data that has no FHIR equivalent.
- The **document repository** supports DICOM files, HL7 messages (.orm.hl7, .oru.hl7), EDI claim files (.835, .837, .277), and standard document formats. The `document` table contains 58 metadata fields including MIME type, patient portal release status, and fax tracking.
- **EDI/claims messages** (.835, .837, .277) are stored in the document repository, providing raw claims interchange data alongside the structured billing tables.
- All 106 entities have 100% field-level descriptions — no entity has fields without descriptions.
- Only 3 of 106 entities (`patients`, `visit`, `insurance`) have table-level description paragraphs; the remaining 103 entities have only the field-level FieldName/Description rows.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is genuinely broad, covering the vendor's native database model across clinical, billing, specialty, and patient-facing domains.

**Strongest domains:**
- **IVF/Fertility** (32 entities, 1,216 fields): Exceptionally deep. Covers cycles, oocyte tracking, embryology daily tasks, semen analysis, follicular and OB ultrasound, donor records (including education, employment, family), cryostorage billing, culture media, cycle scheduling, and more. This is the vendor's core specialty and it shows.
- **Patient/Demographics** (14 entities, 406 fields): Thorough patient record with contacts, relatives, biological family history, kiosk-entered data, surveys, patient requests (amendments, callbacks, forms, online requests, recalls).
- **Scheduling/Workflow** (8 entities, 284 fields): Encounters (with billing data), appointments, waitlist, actions, tasks, and daily worklist.
- **Clinical/EMR** (16 entities, 247 fields): Assessments, HPI, chief complaints, review of systems, medical history, surgical history/procedures, encounter reports, checklist items, DVT risk.

**Solid domains:**
- **Billing/Financial** (7 entities, 176 fields): Insurance payer records, procedure codes/charges, ledger items, payments, prepayments, prior authorizations. Plus EDI files in the document repository.
- **OB/GYN** (9 entities, 169 fields): OB history, pregnancy tracking, pregnancy plans, ultrasound, contraception, multiple births, estimated due dates.
- **Documents/Notes** (4 entities, 98 fields): Comprehensive document metadata with repository support for original files (PDF, DICOM, HL7, images).
- **Labs/Results** (2 entities, 91 fields): Lab orders and clinical measurements/vitals.

**Thinner domains (but still present):**
- **Medications/Allergies** (2 entities, 68 fields): Relies on NewCrop integration tables.
- **Communications** (4 entities, 60 fields): Patient mail and SMS.
- **Immunizations** (2 entities, 52 fields): Records and schedules.
- **Care Plans** (2 entities, 45 fields): EMR plans and wellness plans.
- **Problems/Conditions** (2 entities, 43 fields): Problems with ICD codes.
- **Consent** (1 entity, 12 fields): Completed consent forms.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients` (203 fields), `patientcontact` (22 fields), `patientallowedcontacts` (7 fields), `relative` (14 fields), `patientglobal` (19 fields), `emrbiologicalfamily` (10 fields) | Thorough — includes demographics, contacts, relatives, biological family, custom fields |
| Encounters / visits | ✅ Covered | `visit` (156 fields), `emrencounterprovider` (14 fields), `emrencounterreport` (13 fields), `emrencounterreportaddendum` (13 fields) | Thorough — visit record integrates encounter and claim data |
| Problems / conditions / diagnoses | ✅ Covered | `emrproblem` (31 fields), `emrvisitproblem` (12 fields), `emrhealthconcern` (14 fields) | Covered with ICD codes, onset dates, status tracking |
| Medications / prescriptions | ✅ Covered | `newcropdrug` (52 fields) | Medications via NewCrop integration; 52 fields is solid |
| Allergies | ✅ Covered | `newcropallergy` (16 fields) | Via NewCrop integration |
| Immunizations | ✅ Covered | `immunizationrecord` (43 fields), `immunizationschedule` (9 fields) | Vaccine codes, lot numbers, manufacturer, VIS dates, administration details |
| Vitals | ✅ Covered | `emrmeasurement` (51 fields) | Vital signs and anthropometric data |
| Lab results | ✅ Covered | `emrlaborder` (40 fields), plus HL7 result files (.oru.hl7) in document repository | Lab orders with results stored as HL7 messages |
| Imaging / diagnostic reports | ✅ Covered | `emrivffollicularus` (84 fields), `emrivfobus` (162 fields), `emrobultrasound` (17 fields), DICOM files in document repository | Ultrasound data deeply covered; DICOM files preserved |
| Procedures | ✅ Covered | `procedure` (28 fields), `emrsurgery` (34 fields), `emrsurghis` (18 fields) | Procedure codes, modifiers, NDC, surgical records |
| Clinical notes / documents | ✅ Covered | `chartnote` (24 fields), `emrnotes` (13 fields), `document` (58 fields), `emrchartdocument` (8 fields), `cosignnote` (5 fields) | Chart notes, encounter reports, plus full document repository |
| Care plans / goals | ✅ Covered | `emrplan` (32 fields), `emrwellnessplan` (13 fields) | EMR plans and wellness plans |
| Orders / referrals | ✅ Covered | `emrlaborder` (40 fields), `emrtransfer` (11 fields), `emrdonorpatrequest` (12 fields) | Lab orders and transfers |
| Insurance / coverage | ✅ Covered | `insurance` (65 fields), `priorauth` (16 fields) | Payer records, prior authorizations; fertility coverage noted |
| Claims / billing | ✅ Covered | `procedure` (28 fields), `procedurecharge` (26 fields), `ledgeritem` (10 fields), `visit` (156 fields — includes ICD 1–12, claim ID), EDI files (.835, .837, .277) in doc repository | Structured billing data + raw EDI messages |
| Payments | ✅ Covered | `payment` (27 fields), `visitpayment` (10 fields), `prepayment` (13 fields) | Patient and insurance payments, reconciliation |
| Consents / directives | ✅ Covered | `consentformcompleted` (12 fields) | Completed consent forms tracked |
| Patient communications / portal messages | ✅ Covered | `patmail` (11 fields), `smsnaviconsent` (7 fields), `smsnavimessages` (17 fields), `smsnavinotification` (14 fields) | Patient mail and SMS communications |
| Specialty-specific: IVF/Fertility | ✅ Covered | 32 entities, 1,216 fields covering cycles, oocytes, embryology, semen analysis, donor records, cryostorage, culture media, etc. | Exceptionally deep |
| Specialty-specific: OB/GYN | ✅ Covered | 9 entities, 169 fields covering pregnancy, OB history, ultrasound, contraception, multiple births | Thorough |

**Gap analysis summary**: All applicable EHI domains are represented in the export. The product stores data across clinical, billing, specialty (IVF/OB), and patient-facing domains, and the export covers all of them. The only notable constraint is the fee-based separate process for binary documents (images, DICOM, faxes, HL7 messages, EDI files), but the structured metadata for those documents is included in the standard export, and the document repository capability is documented.

## 6. Documentation Quality

**Strengths:**
- **100% field-level descriptions**: All 2,995 fields across 106 entities have plain-English descriptions. Descriptions are meaningful — not just column names repeated, but actual explanations of what the data represents.
- **Clear export process documentation**: The Read Me tab provides step-by-step instructions with specific screen paths, authorization requirements, encryption details, and format specifications.
- **Document repository documentation**: Clear explanation of file types (PDF, DICOM, HL7, EDI, images), naming conventions, and how to access them.
- **Format documentation**: CSV encoding, ZIP encryption (AES-256), volume splitting, and extraction instructions are well-documented.
- **Publicly accessible**: The Google Sheets workbook is publicly viewable, no authentication needed.

**Weaknesses:**
- **No explicit data types column**: Types are inferred from descriptions ("Date when…" = date, "Indicates if…" = boolean) but no dedicated type column exists. A developer would need to examine actual export data to confirm.
- **No value set enumerations**: Coded fields mention codes in passing within descriptions but don't provide exhaustive lists. Gender codes are mentioned ("M:Male F:Female U:Unknown X:Undifferentiated Blank:Undocumented") but most coded fields lack this.
- **No foreign key documentation**: Key relationships are mentioned in descriptions (e.g., "Map with patientkey") but there's no entity-relationship diagram or formal schema definition.
- **No sample data**: No worked examples or sample export files are provided.
- **No cardinality or constraint documentation**: Required vs optional fields, max lengths, and NULL handling are not specified.
- **Only 3 of 106 entities have table-level descriptions**: Most entities lack a summary paragraph explaining their purpose.

**Usability assessment**: A developer could build an import from this documentation with moderate effort. The field descriptions are clear enough to understand the data semantics, and key relationships can be inferred from naming conventions (e.g., `patientKey`, `visitKey`). However, the lack of explicit types, constraints, and formal relationships would require trial-and-error with actual export data.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

nAbleMD exports its native database model as CSV files with a well-organized, field-level data dictionary covering 106 entities and 2,995 fields across all major data domains. This is not a C-CDA or FHIR repackaging — it's a genuine bulk export of the vendor's relational database, including deep specialty-specific data (IVF/fertility, OB/GYN) that has no standard equivalent.

### Key Findings

1. **Genuinely comprehensive scope**: 106 native database tables covering clinical, billing, specialty (IVF/fertility with 32 tables and 1,216 fields), OB/GYN, patient portal, documents, and communications. Every applicable EHI domain is represented.

2. **100% field-level documentation**: All 2,995 fields have plain-English descriptions — an unusually high standard for EHI export documentation. The data dictionary is publicly hosted on Google Sheets.

3. **Specialty depth is exceptional**: The IVF/fertility domain alone accounts for 32 entities and 1,216 fields (41% of all fields), documenting everything from cycle management to oocyte tracking to donor evaluations. This is exactly the kind of specialty clinical data that distinguishes a real (b)(10) export.

4. **Binary documents require separate fee**: The certification page explicitly states that "photographs, scanned images, faxes, other uploaded documents… are not included in the export summaries" and require a one-time fee. The technical capability exists (the `document` table and repository are documented), but the fee-gating is notable.

5. **Documentation lacks formal structure**: No explicit data types, no foreign key schema, no value sets, no sample data. The descriptions are informative but a developer would need actual export data to fully understand the format.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   CSV (in AES-256 encrypted 7-zip archive) + document repository
Model type:      Native database
Entities:        106
Fields:          2,995
Descriptions:    100%
Sample data:     No
Bulk export:     Yes (single-patient and full-database)
Domains covered: 19 of 19 applicable domains
```

### Bottom Line

nAbleMD provides one of the more thorough EHI exports encountered: 106 native database tables with 2,995 fully described fields, covering clinical, billing, IVF/fertility specialty, OB/GYN, documents, communications, and patient portal data. The single biggest strength is the exceptional depth in IVF/fertility clinical data (32 tables, 1,216 fields) that goes far beyond any standard interchange format. The main gap is that binary documents (images, DICOM, faxes) require a separate fee for bulk export, though the structured metadata is included in the standard export.
