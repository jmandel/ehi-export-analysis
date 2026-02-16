# EHI Export Analysis: Nth Technologies, Inc.

**Product**: nAbleMD 6.0c
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2070.nAbl.06.01.1.221221 (CHPL ID 11118)

## 1. Product Context

nAbleMD is a cloud-based, integrated EMR and practice management (PM) platform from Nth Technologies, Inc. (Houston, TX, ~11–50 employees). The product targets small-to-medium ambulatory practices across multiple specialties, with a strong concentration in **reproductive endocrinology / IVF**. A companion product, nAble IVF, shares the same database and platform.

**Key capabilities relevant to EHI completeness:**

- **Clinical EMR**: Patient charting, HPI, physical exam diagrams, problem lists, medications/allergies (via NewCrop/Surescripts), lab ordering/results (LabCorp interfaces), imaging, referral management, wellness plans, clinical decision support.
- **Practice Management & Billing**: Appointment scheduling, eligibility verification, ICD-10 coding, charge capture, automated claims submission, revenue cycle management, financial/collections reporting, statement generation.
- **Patient Portal**: Secure messaging, self-scheduling, online health history forms, consent form management.
- **Document Management**: Scanned documents, photographs, fax send/receive, DICOM files.
- **IVF/Fertility**: Cycle management with stimulation protocols, oocyte/embryo tracking, semen analysis, cryostorage management, donor evaluations, SART reporting.
- **OB/GYN**: Prenatal records, pregnancy tracking, obstetric ultrasound, birth records.
- **Communications**: Patient portal messaging (PatMail), SMS notifications via SmsNavi.

This sets a high bar for the EHI export: a compliant export should cover clinical data, billing/claims, IVF/fertility specialty data, OB/GYN records, patient communications, documents, and financial records.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/certification-page.html` (36 KB) | nAbleMD certification/mandatory disclosures page; contains EHI export link and data portability disclosure | Medium — confirms export mechanism and fees |
| `downloads/csv-sheets/read_me.csv` | ReadMe tab from Google Sheets data dictionary; documents export process, ZIP format, CSV format, and document repository | **High** — detailed export mechanics |
| `downloads/csv-sheets/table_of_contents.csv` | Table of Contents listing all exported entities | **High** — complete entity inventory |
| `downloads/csv-sheets/revision_history.csv` | Version history (v1.0 Nov 2023, v1.0.1 Dec 2023) | Low |
| `downloads/csv-sheets/*.csv` (106 entity CSVs) | Individual data dictionary sheets for each exported table, with field names and descriptions | **High** — primary artifact; complete field-level data dictionary |
| `downloads/screenshot-certification-page.png` | Full-page screenshot of certification page | Low — redundant with HTML |
| `downloads/screenshot-ehi-export-section.png` | Focused screenshot of EHI export section | Low |
| `downloads/screenshot-gsheet-overview.png` | Screenshot of Google Sheets data dictionary | Low — CSVs provide same data |

**Most informative**: The 106 CSV data dictionary sheets and the ReadMe CSV. Together they document every table and field in the export with descriptions.

## 3. Export Mechanics

- **Format**: Password-encrypted ZIP archive containing **CSV files** (UTF-8, standard comma-separated) plus a **Document Repository** folder with binary files (PDFs, images, DICOM, HL7 messages, EDI claim files).
- **Encryption**: AES-256 via 7-zip format; requires a password set at export time.
- **Mechanism**: UI-driven. Authorized users access PM Home → System Configuration → Data Export.
  - Users must have administrator-granted access and 2FA enabled on their account.
- **Single-patient**: Select a patient via search, click "Request Download." ~5 minutes per patient.
- **Bulk export**: Click "Request Download" without selecting a patient to export all records. Duration depends on total data volume. Limited to one active export at a time.
- **Retrieval**: Download links with checksums appear on the Data Export screen. Each ZIP volume is ~10 GB. Files retained on server for 7 days.
- **Access constraints**: The certification page notes that "images and non-standard documentation require separate one-time fees for bulk export," and a "reduced monthly fee" for inactive practice access. The data portability disclosure states: "photographs, scanned images, faxes, other uploaded documents as well as medical documentation not included in the Common Data Set are not included in the export summaries. A one-time fee will be charged for the bulk export of these images, documents and documentation."

**Important note on data portability disclosure vs. EHI export**: The certification page mentions two distinct capabilities: (1) a "Data Portability" export that generates "export summaries" which exclude images/documents (likely the (b)(6) criterion), and (2) the "Electronic Health Information Export" which links to the data dictionary and appears to be the (b)(10) export covering CSV files plus the Document Repository. The ReadMe in the data dictionary explicitly describes including scanned documents, DICOM, HL7, and EDI messages in the export archive.

## 4. Export Content: What's In It

### Overview

The export consists of **106 CSV tables** covering **3,109 fields**, all with descriptions. Additionally, a Document Repository folder contains binary files (images, PDFs, DICOM, HL7, EDI claim messages). The data dictionary is published as a Google Sheets document with individual tabs for each table, downloaded here as CSV files.

**Data dictionary quality**:
- 106 entities documented (each as a separate tab/CSV)
- 3,109 total fields across all entities
- **100% of fields have descriptions** (3,109 / 3,109)
- 3 entities have table-level descriptions (patients, visit, insurance)
- Field types are NOT explicitly documented (no type column)
- Foreign key relationships are partially documented via key field naming conventions (e.g., `PatientKey`, `VisitKey`, `EmrCycleKey`)
- Value sets/coded values are NOT documented
- No sample data provided

### Vendor's own content organization

The vendor organizes data by table name with no explicit category groupings. I categorized them by naming patterns and domain. The full inventory is in `analysis/entity-inventory-full.json`.

**Category breakdown:**

| Category | Entities | Fields | Key Tables |
|---|---|---|---|
| IVF/Fertility | 31 | 1,317 | emrcycle (231), emrivfobus (162), emroocyteday (132), emrdonor (94), emrivfsample (85), emrivffollicularus (84), emrivfsemenanalysis (81) |
| Clinical/EMR | 26 | 472 | emrmeasurement (50), emrlaborder (39), emrproblem (27), emrencounterreport (22), emrmedicalhistory (20) |
| Patient Demographics/Admin | 12 | 386 | patients (203), patientglobal (30), patientcontact (29) |
| Encounters/Visits | 2 | 184 | visit (156), procedure (28) |
| Billing/Financial | 7 | 176 | insurance (65), procedurecharge (25), ledgeritem (9), payment (8) |
| OB/GYN | 9 | 161 | emrpregnancy (33), emrobhistorypreg (28), emrobgynhc (27) |
| Documents/Notes | 3 | 89 | document (58), chartnote (19), cosignnote (12) |
| Scheduling | 3 | 78 | appointment (48), dailyworklist (20), appointmentwaitlist (10) |
| Medications | 2 | 68 | newcropdrug (51), newcropallergy (15) (data from NewCrop e-prescribing) |
| Communications | 4 | 60 | smsnavimessages (19), patmail (10), smsnaviconsent (17), smsnavinotification (14) |
| Immunizations | 2 | 52 | immunizationrecord (30), immunizationschedule (22) |
| Tasks/Workflow | 3 | 43 | task (19), taskassigned (14), action (10) |
| Consent/Forms | 2 | 23 | consentformcompleted (15), kioskanswer (8) |
| **Total** | **106** | **3,109** | |

### Representative entities (top 15 by field count)

| Entity | Fields | Category | Notable Content |
|---|---|---|---|
| emrcycle | 231 | IVF/Fertility | Comprehensive IVF cycle data: stimulation protocols, monitoring, dosages, outcomes, transfer details |
| patients | 203 | Demographics | Full patient record: demographics, insurance, billing address, custom fields, discharge info |
| emrivfobus | 162 | IVF/Fertility | IVF obstetric ultrasound with embryo measurements across multiple embryos |
| visit | 156 | Encounters | Encounter/claim record: clinical data + billing codes + insurance + claim status |
| emroocyteday | 132 | IVF/Fertility | Daily oocyte/embryo tracking: grading, biopsy, PGT results, culture status |
| emrdonor | 94 | IVF/Fertility | Donor demographics, physical characteristics, eligibility, approval status |
| emrivfsample | 85 | IVF/Fertility | Specimen tracking: oocyte, embryo, sperm samples with location/status |
| emrivffollicularus | 84 | IVF/Fertility | Follicular ultrasound measurements (multiple follicle sizes per exam) |
| emrivfsemenanalysis | 81 | IVF/Fertility | Semen analysis: motility, morphology, concentration, wash results |
| insurance | 65 | Billing | Payer-level records: claim address, payer ID, clearinghouse, electronic claim config |
| document | 58 | Documents | Document metadata: MIME types, categories, portal release, file references |
| newcropdrug | 51 | Medications | Prescription records from NewCrop: drug, dose, frequency, pharmacy, refills |
| emrmeasurement | 50 | Clinical | Clinical measurements (vitals and other measurements) |
| appointment | 48 | Scheduling | Scheduling data: appointment time, provider, status, reminders |
| emrlaborder | 39 | Clinical | Lab orders: order details, draw status, PGT linkage |

### Document Repository contents

Per the ReadMe, the Document Repository within the export archive contains:
- **Documents and images**: PDF, PNG, JPG, GIF, TIF, DOC, DOCX, and other uploaded formats
- **ANSI Claim/EDI messages**: .835 (remittances), .837 (claims), .277 (claim status), .271 (eligibility), plus XML-wrapped variants and non-standard formats (.DPR, .EBR)
- **HL7 messages**: .orm.hl7 (lab results), .oru.hl7 (lab orders), radiology orders
- **DICOM**: .dcm files (image data and structured reports)

This is significant — the export includes the raw EDI claim transactions, not just summarized billing data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is remarkably deep in its areas of focus:

**IVF/Fertility (31 entities, 1,317 fields)**: This is the standout domain. The emrcycle table alone has 231 fields covering stimulation protocols, monitoring, dosages, outcomes, transfer details, and cycle scheduling. Oocyte/embryo tracking (emroocyte, emroocyteday — 132 fields for daily tracking), semen analysis, follicular ultrasound, cryostorage billing, donor evaluations (with physical characteristics, family history, eligibility), and IVF quotes are all deeply covered. This is clearly the vendor's primary specialty.

**Clinical EMR (26 entities, 472 fields)**: Core clinical data including problems (emrproblem, 27 fields with LOINC codes), measurements/vitals (emrmeasurement, 50 fields), lab orders, encounter reports, medical history, HPI, assessments, surgery records, surgical history, health concerns, wellness plans, chief complaints, and clinical checklists.

**Patient Demographics (12 entities, 386 fields)**: The patients table has 203 fields — extremely thorough, including custom fields (custom1–custom10), billing address, discharge information, and many demographic details. Related tables cover contacts, allowed contacts, patient notes, patient requests (amendment, callback, form, online, recall), and surveys.

**Billing/Financial (7 entities, 176 fields)**: Insurance (65 fields, payer-level), procedurecharge (25 fields with insurance payments), ledgeritem (9 fields for adjustments), payment, prepayment, visitpayment, and priorauth. Plus the Document Repository includes raw EDI 835/837/277/271 files.

**OB/GYN (9 entities, 161 fields)**: Pregnancy records, obstetric history (current and prior pregnancies), OB/GYN health concerns, estimated due dates, multibirth records, pregnancy plans, contraception, and kiosk pregnancy outcome answers.

**Documents (3 entities, 89 fields)**: The document table (58 fields) stores metadata; actual files are in the Document Repository. Chart notes (19 fields with form content and signatures), co-sign records.

**Communications (4 entities, 60 fields)**: Patient mail (patmail), SMS consent, messages, and notifications via SmsNavi integration.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients` (203 fields), `patientcontact` (29), `patientglobal` (30), `relative` (15) | Extremely thorough |
| Encounters / visits | ✅ Covered | `visit` (156 fields — clinical + claim data combined), `emrencounterprovider` (9) | Deep; visit table combines clinical and billing |
| Problems / conditions | ✅ Covered | `emrproblem` (27 fields incl LOINC), `emrvisitproblem` (8), `emrhealthconcern` (10) | Solid |
| Medications / prescriptions | ✅ Covered | `newcropdrug` (51 fields from NewCrop e-prescribing) | Thorough |
| Allergies | ✅ Covered | `newcropallergy` (15 fields) | Adequate |
| Immunizations | ✅ Covered | `immunizationrecord` (30 fields), `immunizationschedule` (22) | Thorough |
| Vitals | ✅ Covered | `emrmeasurement` (50 fields — covers vitals and other clinical measurements) | Deep |
| Lab results | ✅ Covered | `emrlaborder` (39 fields), plus HL7 .orm/.oru files in Document Repository | Good |
| Imaging / diagnostic reports | ✅ Covered | DICOM files in Document Repository, `emrobultrasound`, `emrivffollicularus`, `emrivfobus` (IVF/OB-specific imaging) | Good; DICOM raw data included |
| Procedures | ✅ Covered | `procedure` (28 fields), `emrsurgery` (13), `emrsurghis` (14) | Covered |
| Clinical notes / documents | ✅ Covered | `chartnote` (19 fields with form content), `emrnotes` (10), `emrencounterreport` (22), `emrencounterreportaddendum` (6), `document` (58), plus Document Repository files | Thorough |
| Care plans / goals | ✅ Covered | `emrplan` (15 fields), `emrwellnessplan` (6) | Present |
| Orders / referrals | ⚠️ Partial | `emrlaborder` (39) covers lab orders; no dedicated referral entity, though order management implied in clinical tables | Lab orders documented; referral tracking not explicitly present as a table |
| Insurance / coverage | ✅ Covered | `insurance` (65 fields, payer-level), `priorauth` (9 fields) | Deep payer-level data |
| Claims / billing | ✅ Covered | `procedurecharge` (25 fields), `visit` (claim data within 156-field table), EDI 835/837 files in Document Repository | Strong — raw EDI transactions included |
| Payments | ✅ Covered | `payment` (8), `prepayment` (7), `visitpayment` (5), `ledgeritem` (9) | Covered |
| Consents / directives | ✅ Covered | `consentformcompleted` (15 fields) | Adequate |
| Patient communications | ✅ Covered | `patmail` (10 fields), `smsnavimessages` (19), `smsnavinotification` (14), `smsnaviconsent` (17) | Good; portal messages and SMS |
| Specialty: IVF/Fertility | ✅ Covered | 31 entities, 1,317 fields (see Section 5a) | Exceptionally deep |
| Specialty: OB/GYN | ✅ Covered | 9 entities, 161 fields (pregnancy, obstetric history, birth records, ultrasound) | Thorough |
| Family health history | ✅ Covered | `emrbiologicalfamily` (8 fields), `emrmedicalhistory` (20 fields) | Present |

**Gap Analysis**: 18 of 19 applicable domains show ✅ Covered, with 1 ⚠️ Partial (referrals). No significant gaps relative to the product's known capabilities. The billing/financial domain is covered both through structured CSV tables AND raw EDI transactions in the Document Repository.

## 6. Documentation Quality

**Strengths:**
- **Complete field-level data dictionary**: Every one of the 3,109 fields has a description. This is exceptional among EHI exports.
- **Clear export process documentation**: The ReadMe tab explains authorization, single-patient and bulk export mechanics, ZIP format, CSV format, and document repository contents in detail.
- **Practical guidance**: Instructions for 7-zip, password handling, multi-volume extraction, and file format identification.
- **Machine-readable**: Published as a Google Sheet with per-table tabs; each tab downloadable as CSV with consistent `FieldName, Description` structure.

**Weaknesses:**
- **No data types documented**: Fields lack type declarations (string, integer, date, boolean). A developer would need to infer types from field names and descriptions.
- **No value sets / code systems**: Coded fields (e.g., `PaymentType`, `eligibility`, `ProblemTypeLoinc`) don't document valid values.
- **No explicit foreign key documentation**: Relationships are implied by naming conventions (`PatientKey`, `VisitKey`, `EmrCycleKey`) but not formally documented.
- **No sample data**: No example CSV rows or sample export files provided.
- **Table descriptions sparse**: Only 3 of 106 entities have a table-level description.

**Developer usability**: A developer could build an import with moderate effort. Field names and descriptions are clear enough to understand the data model, but the lack of types and value sets would require trial-and-error or access to sample data. The foreign key naming convention is consistent enough to reconstruct relationships.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains nAbleMD stores. With 106 tables and 3,109 fields, it goes far beyond USCDI/clinical summaries to include:
- Billing and financial data (7 entities + raw EDI transactions)
- Specialty-specific IVF/fertility data (31 entities, 1,317 fields — the deepest single domain)
- OB/GYN records (9 entities)
- Patient communications (portal messages and SMS)
- Documents and images (including DICOM and HL7 raw files)
- Consent forms, patient surveys, kiosk answers

The IVF/fertility depth is particularly impressive — 231 fields in the emrcycle table alone, daily oocyte tracking with 132 fields, detailed semen analysis, donor evaluations with physical characteristics. This is not a clinical summary repackaged; it's the vendor's actual data model exposed as CSV.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export, not a repackaged clinical exchange. Key evidence:
1. **Native database model exported as CSV** — the table/field structure reflects internal database tables, not a FHIR/C-CDA projection.
2. **106 tables far exceeds any clinical exchange format** — C-CDA or FHIR Bulk Data g(10) would cover ~20-30 resource types; this export has 106 entities.
3. **Billing/financial data included** — insurance, procedurecharge, payment, ledgeritem, priorauth, plus raw EDI 835/837/277/271 files. This data is not available via FHIR or C-CDA exchange.
4. **Specialty-specific IVF data included** — 31 fertility-specific tables are not representable in standard clinical exchange formats.
5. **Document Repository with raw binary files** — DICOM, HL7, EDI transactions included alongside structured CSV data.
6. **Dedicated export UI** — purpose-built Data Export screen under System Configuration with authorization, 2FA, and password-protected ZIP generation.
7. **Revision-tracked data dictionary** — published documentation with version history (v1.0 Nov 2023, v1.0.1 Dec 2023) specifically for the export.

### Key Findings

1. **Exceptionally deep IVF/fertility coverage**: 31 entities and 1,317 fields dedicated to fertility workflows — cycle management, embryology, oocyte tracking, semen analysis, donor evaluations, cryostorage. This is the deepest specialty-specific coverage I've seen in an EHI export, reflecting the vendor's core market.

2. **100% field-level documentation**: All 3,109 fields across 106 entities have descriptions. While types and value sets are missing, the description coverage is comprehensive — every field has a substantive explanation, not just a name repeat.

3. **Raw EDI transactions included**: The Document Repository includes .835, .837, .277, and .271 EDI claim files alongside clinical documents and DICOM images. This provides billing data in its rawest, most complete form.

4. **Genuine native database export**: The table structure clearly reflects the vendor's internal data model (e.g., `EmrCycle`, `EmrOocyteDay`, `NewcropDrug`, `ProcedureCharge`), not a standards-based projection. This is a true (b)(10) export.

5. **Minor gap — referral tracking**: While clinical referrals exist in the product, there's no dedicated referral entity in the export. This is a small gap relative to the otherwise comprehensive coverage.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   CSV (structured data) + binary files (DICOM, HL7, EDI, images/PDFs) in AES-256 encrypted ZIP
Entities:        106
Fields:          3,109
Descriptions:    100% (all fields have descriptions; types and value sets not documented)
Sample data:     No
Bulk export:     Yes (full-practice export supported)
Domains covered: 18 of 19 applicable domains (✅ 17 full + ⚠️ 1 partial)
```

### Bottom Line

nAbleMD's EHI export is one of the more complete (b)(10) implementations available. A patient or provider would receive a thorough, usable copy of their data — structured clinical records, billing/claims (including raw EDI transactions), specialty IVF/OB data, documents, images, and communications — all documented with field-level descriptions across 106 tables. The main limitation is the lack of data type and value set documentation, which would require some reverse-engineering effort from a developer importing the data.
