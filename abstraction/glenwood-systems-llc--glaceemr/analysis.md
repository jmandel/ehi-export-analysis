# EHI Export Analysis: Glenwood Systems LLC

**Product**: GlaceEMR 6.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1535.Glac.06.00.1.180629 (CHPL #9559)

## 1. Product Context

GlaceEMR is a cloud-based, ONC-certified EHR and practice management system developed by Glenwood Systems LLC (Waterbury, CT). It targets ambulatory outpatient practices across multiple specialties including internal medicine, psychiatry/behavioral health, podiatry, cardiology, neurology, ophthalmology, rheumatology, urgent care, and general surgery. The product is marketed as an all-in-one solution encompassing clinical documentation, e-prescribing (including EPCS via SureScripts), patient portal, scheduling, lab integration, billing/coding, and quality reporting.

Key data domains the product stores, relevant to export completeness:
- **Clinical**: Encounter documentation with specialty templates, problem lists, medication management (active/inactive), allergies, vitals, lab orders/results, immunizations, clinical notes (progress notes, H&P, etc.), care plans/goals, preventive screenings, specialty assessments (PHQ-9, BIMS, DSM-5 for behavioral health), and coumadin/anticoagulation management.
- **Billing/PM**: Insurance enrollment, claims/charges with procedure and diagnosis codes, payment receipts, payment posting, account balances, eligibility verification.
- **Administrative**: Scheduling, patient portal messaging, phone messages, referrals, provider/referring provider registries.
- **Documents**: Scanned documents, clinical templates (HTML/PDF), C-CDA documents, patient photos.
- **Add-on services**: GlaceRCM (full revenue cycle management), GlaceOffice (practice administration), GlaceScribe (AI transcription) — these likely reside outside the core EHR boundary but integrate deeply.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/GlaceEMR Export Data Dictionary.pdf` | 62-page PDF (783 KB), Version 1.0, dated 2023-11-27. Documents all 42 CSV files, column schemas, data types, descriptions, foreign keys, value sets. Created by Adnan Shariq using Microsoft Word. | **Primary source** — most informative artifact |
| `downloads/transparencydisclosure.html` | Transparency disclosure HTML page (27 KB). Contains EHI Data Export section describing single-patient and population export, format (ZIP), and link to data dictionary PDF. | Moderately informative — confirms export mechanism |
| `downloads/enrichment/data-dictionary.json` | Prior agent's structured JSON extraction of the PDF (153 KB). Contains all 42 file schemas with 820 columns. | Useful intermediate — verified against PDF |
| `downloads/enrichment/data-dictionary.txt` | pdftotext extraction of the PDF (59 KB). | Used for verification |
| `downloads/enrichment/extract-data-dictionary.ts` | Bun TypeScript script that produced the JSON extraction (70 KB). | Reference only |
| `downloads/enrichment/README.md` | Documentation for the enrichment process. | Reference only |

No sample data files, no machine-readable schema (JSON Schema, XSD), no API documentation were found.

## 3. Export Mechanics

- **Format**: ZIP file containing CSV files (structured data), HTML + PDF (clinical documents), PNG/JPEG (scanned documents), XML (C-CDA v2), JPG (patient photos)
- **Mechanism**: UI-based export within GlaceEMR. An authorized user initiates the export and receives a download link to a ZIP file.
- **Single-patient**: Yes — export all EHI for one patient as a ZIP file
- **Bulk/population**: Yes — export EHI for a selected group of patients or the entire patient population
- **Access constraints**: Requires authorized user access within GlaceEMR. No fees mentioned.
- **Not FHIR/C-CDA repackaging**: This is a native CSV-based database export. C-CDA documents are included alongside the CSV data as supplementary clinical documents, not as the primary export format.

The ZIP file has five top-level folders:

| Folder | Contents |
|---|---|
| `EMR/` | 31 CSV files — clinical data |
| `PMS/` | 11 CSV files — practice management/billing data |
| `Documents/` | Per-patient subfolders with HTML+PDF clinical templates, scanned docs (PNG/JPEG), C-CDA v2 XML |
| `Photos/` | Patient photos in JPG format |
| `Reference/` | Schema of exported file content (described but not elaborated in documentation) |

## 4. Export Content: What's In It

### Data dictionary overview

The data dictionary documents **42 CSV files** with **820 total columns** across two folders (EMR: 31 files/576 columns; PMS: 11 files/244 columns). This was verified independently by parsing the enrichment JSON against the original PDF text (`pdftotext` output).

- **Fields with descriptions or comments**: 175 of 820 (21.3%)
- **Fields with data types**: 820 of 820 (100%)
- **Fields with foreign key references**: 67
- **Fields with documented possible/example values**: 31
- **Relationships**: Explicitly documented via foreign key annotations cross-referencing other CSV files (e.g., Patient ID → `PMS/Patient_Demographics.csv`, Encounter ID → `EMR/Encounters.csv`)

Every column has a data type specified (Integer, String, Date, Date & Time, Currency, Numeric/Decimal, or qualified types like "Integer (Foreign key)" and "Integer (Primary key)"). However, most columns lack a prose description — only the column name and type are provided.

### Vendor's own content organization

The vendor organizes the export into two primary categories: **EMR** (clinical) and **PMS** (practice management). Additionally, unstructured clinical content is exported in the **Documents** folder.

#### EMR folder (31 files, 576 fields)

| Entity | Fields | Described | Types | Notes |
|---|---|---|---|---|
| Encounters.csv | 18 | 6 | Yes | Visit records with status, chief complaints, referring/service doctor |
| Vitals.csv | 24 | 4 | Yes | BP, pulse, temp, height, weight, BMI, O2, pain, respiration, head circumference |
| Past_Medical_History.csv | 14 | 4 | Yes | Condition, onset date, SNOMED coding |
| Surgical_History.csv | 15 | 4 | Yes | Procedure name, date, SNOMED/CPT4 coding |
| Family_History.csv | 16 | 4 | Yes | Condition, relation, SNOMED coding |
| Family_Relations_History.csv | 14 | 4 | Yes | Family member details |
| Social_History.csv | 14 | 4 | Yes | Social history items |
| Substance_Abuse_History.csv | 14 | 4 | Yes | Substance abuse records |
| Contraception_Sexual_History.csv | 14 | 4 | Yes | Contraception/sexual history |
| Pregnancy_History.csv | 15 | 4 | Yes | Pregnancy records |
| Birthing_History.csv | 14 | 4 | Yes | Birth records |
| Menstrual_History.csv | 14 | 4 | Yes | Menstrual history |
| Occupational_History.csv | 14 | 4 | Yes | Occupational records |
| Obstetric_History.csv | 14 | 4 | Yes | Obstetric records |
| Exposure_History.csv | 14 | 4 | Yes | Exposure records |
| Allergies.csv | 19 | 4 | Yes | Drug/food/environmental allergies with NDC, SNOMED, reaction severity |
| Assesments.csv | 18 | 6 | Yes | Clinical assessments with ICD-9/10, SNOMED, CPT4, NDC, LOINC, RXNORM |
| Problem_List.csv | 22 | 4 | Yes | Active/inactive/resolved problems with ICD-10, SNOMED |
| Medications.csv | 26 | 4 | Yes | Active meds with NDC, dosage, frequency, SIG, pharmacy info |
| InactiveMedications.csv | 28 | 4 | Yes | Inactive/discontinued meds with NDC, discontinuation reason |
| Investigation.csv | 46 | 7 | Yes | Lab orders/results with diagnosis codes, CPT, test status, result values, ranges |
| Preventive_Screenings.csv | 14 | 4 | Yes | Preventive care screenings with SNOMED/LOINC |
| Coumadin.csv | 35 | 5 | Yes | Anticoagulation management with INR/PT values, daily dose schedules |
| Vaccines.csv | 29 | 5 | Yes | Immunizations with CVX codes, manufacturer, lot numbers, VIS dates |
| Messages.csv | 22 | 6 | Yes | Phone/internal messages with doctor responses |
| Reminders.csv | 13 | 3 | Yes | Patient reminders |
| Patient_Photo_Index_File.csv | 12 | 5 | Yes | Index to patient photos in Photos/ folder |
| Clinical_Document_Index_File.csv | 19 | 5 | Yes | Index to clinical templates (HTML/PDF) in Documents/ |
| Phone_Messages_Index_File.csv | 15 | 5 | Yes | Index to phone message documents |
| Scan_And_Attachments_Index_File.csv | 18 | 5 | Yes | Index to scanned docs/attachments |
| CDA_Document_Index_File.csv | 12 | 5 | Yes | Index to C-CDA XML documents |

#### PMS folder (11 files, 244 fields)

| Entity | Fields | Described | Types | Notes |
|---|---|---|---|---|
| Patient_Demographics.csv | 55 | 3 | Yes | Comprehensive: name, DOB, contact, guarantor, emergency contact, race, ethnicity, language, pharmacy, employer, deceased status |
| Patient_Insurance.csv | 51 | 6 | Yes | Primary/secondary/tertiary insurance with subscriber details, copays, group numbers |
| Patient_Account_Balance.csv | 9 | 3 | Yes | Account balance summary |
| Transactions.csv | 33 | 10 | Yes | Claims/charges with procedure codes, diagnoses (1-4), payments, adjustments, balances, insurance/patient splits |
| Payment_Receipts.csv | 22 | 4 | Yes | Cash/check/card/insurance payments with payment/adjustment/denial codes |
| Payment_Posting.csv | 12 | 5 | Yes | Links receipts to specific services/procedures |
| Appointments.csv | 22 | 4 | Yes | Appointment records with status, type, reason, notes, duration, resource |
| Master_Insurance_List.csv | 6 | 1 | Yes | Insurance carrier reference data |
| Master_POS_List.csv | 4 | 0 | Yes | Place of service reference |
| Master_Provider_List.csv | 16 | 0 | Yes | Provider details with NPI, DEA, license |
| Master_Referring_Provider_List.csv | 14 | 0 | Yes | Referring provider details with NPI |

#### Documents folder (unstructured content)

Clinical documents are organized per-patient in folders named `LastName,FirstName-(DOB MM-DD-YYYY)-(Account#)-[PatientID]`. Three categories:

1. **Clinical Templates**: Exported in both HTML and PDF. Indexed by `Clinical_Document_Index_File.csv`. Contains specialty-specific note templates (progress notes, H&P, etc.).
2. **Scanned Documents/Attachments**: Exported in original format (PNG/JPEG/etc.). Indexed by `Scan_And_Attachments_Index_File.csv`.
3. **C-CDA v2 XML**: Standard clinical document architecture documents. Indexed by `CDA_Document_Index_File.csv`.

Full entity inventory saved to `analysis/full-entity-inventory.json` (all 42 entities, all 820 fields, with data types, descriptions, foreign keys, and possible values).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor divides the export into **EMR** (clinical) and **PMS** (practice management/billing) categories, with clinical documents in a separate **Documents** folder.

**Clinical (EMR) — strong depth**: 31 CSV files covering encounters, vitals, an unusually granular set of 13 distinct history categories (past medical, surgical, family, social, substance abuse, contraception/sexual, pregnancy, birthing, menstrual, occupational, obstetric, exposure), allergies with NDC coding, assessments with multi-system coding (ICD-9/10, SNOMED, CPT4, NDC, LOINC, RXNORM), problem lists, active and inactive medications with NDC, lab orders/results with values and ranges, preventive screenings, immunizations with CVX codes, a specialty coumadin/anticoagulation management module (35 fields), messages, reminders, and index files pointing to unstructured documents.

**Billing/PM (PMS) — solid**: 11 CSV files covering comprehensive demographics (55 fields), insurance enrollment (primary/secondary/tertiary — 51 fields), account balances, billing transactions with procedure codes and 4 diagnosis pointers (33 fields), payment receipts with denial codes, payment posting with service-level detail, appointments, and reference master lists (insurance carriers, places of service, providers, referring providers).

**Documents — broad**: HTML+PDF renderings of clinical templates, scanned documents in original format, and C-CDA v2 XML. These capture specialty assessments, behavioral health instruments, and other clinical content that isn't in the structured CSV files.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `PMS/Patient_Demographics.csv` (55 fields) — name, DOB, contact, guarantor, emergency contact, race, ethnicity, language, pharmacy, employer, deceased status | Thorough |
| Encounters / visits | ✅ Covered | `EMR/Encounters.csv` (18 fields) — date, type, status, chief complaints, referring/service doctor, place of service | Solid |
| Problems / conditions / diagnoses | ✅ Covered | `EMR/Problem_List.csv` (22 fields) with ICD-10, SNOMED coding, status (active/inactive/resolved) | Thorough |
| Medications / prescriptions | ✅ Covered | `EMR/Medications.csv` (26 fields) + `EMR/InactiveMedications.csv` (28 fields) — NDC, dosage, frequency, SIG, pharmacy, prescriber; active and inactive tracked separately | Thorough |
| Allergies | ✅ Covered | `EMR/Allergies.csv` (19 fields) — drug/food/environmental, NDC, SNOMED, reaction, severity | Solid |
| Immunizations | ✅ Covered | `EMR/Vaccines.csv` (29 fields) — CVX codes, manufacturer, lot number, VIS dates, site, route | Thorough |
| Vitals | ✅ Covered | `EMR/Vitals.csv` (24 fields) — BP, pulse, temp, height, weight, BMI, O2, pain, respiration, head circumference | Thorough |
| Lab results | ✅ Covered | `EMR/Investigation.csv` (46 fields) — orders, results with values/ranges, diagnosis codes, CPT, status tracking | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | `EMR/Investigation.csv` includes Group Name values like "Radiology", "X Ray", "ECG" suggesting imaging orders are captured here; but no dedicated imaging file or DICOM references | Orders captured; image files/reports may be in Documents folder |
| Procedures | ⚠️ Partial | `EMR/Surgical_History.csv` (15 fields) covers surgical procedures; `PMS/Transactions.csv` has procedure codes. No dedicated procedures file for in-office procedures | Surgical history and billed procedures covered; no dedicated structured procedure log |
| Clinical notes / documents | ✅ Covered | `Documents/` folder with HTML+PDF clinical templates indexed by `Clinical_Document_Index_File.csv`; scanned docs indexed by `Scan_And_Attachments_Index_File.csv`; C-CDA XML indexed by `CDA_Document_Index_File.csv` | Thorough — dual-format HTML+PDF ensures both human and machine readability |
| Care plans / goals | ⚠️ Partial | No dedicated care plan CSV file. Treatment plans and goals (mentioned in product features, especially behavioral health) are likely embedded in clinical document templates (HTML/PDF) rather than structured CSV | Gap for structured data; may be in Documents folder as rendered clinical notes |
| Orders / referrals | ⚠️ Partial | Lab/test orders in `Investigation.csv`; referring doctor tracked in encounters and transactions. No dedicated referral tracking file (referral status, outcomes, etc.) | Product supports referrals per (b)(7)-(9) certification; structured referral records not evident in export |
| Insurance / coverage | ✅ Covered | `PMS/Patient_Insurance.csv` (51 fields) — primary/secondary/tertiary with subscriber details, copays, group numbers; `PMS/Master_Insurance_List.csv` for carrier reference | Thorough |
| Claims / billing | ✅ Covered | `PMS/Transactions.csv` (33 fields) — procedure codes, charges, 4 diagnosis pointers, payments, adjustments, balances, insurance/patient splits, submit status | Solid — captures charge-level detail |
| Payments | ✅ Covered | `PMS/Payment_Receipts.csv` (22 fields) + `PMS/Payment_Posting.csv` (12 fields) — cash/check/card/insurance, denial codes, adjustment codes, service-level posting | Thorough |
| Consents / directives | ⚠️ Partial | Scanned documents folder may include advance directives (example file name in PDF: "Adv-Directive Mental Health Treatment.jpg"). No structured consent tracking | Likely captured as scanned documents, not structured data |
| Patient communications / portal messages | ⚠️ Partial | `EMR/Messages.csv` (22 fields) covers phone and internal messages with doctor responses. Patient portal messages (two-way messaging mentioned in product) not explicitly identified as a separate category | Phone/internal messages present; portal messaging unclear |
| Specialty-specific (behavioral health) | ⚠️ Partial | Product has a significant behavioral health module (PHQ-9, BIMS, Mini Mental Status Exam, DSM-5, treatment plans). No dedicated behavioral health CSV file; these assessments are likely captured within clinical document templates (HTML/PDF) | Structured behavioral health data not in CSV; likely in Documents as rendered notes |
| Specialty-specific (anticoagulation) | ✅ Covered | `EMR/Coumadin.csv` (35 fields) — INR/PT monitoring with daily dose schedules (Mon-Sun), target INR range, dose adjustments | Unusually specific specialty module with dedicated export |

## 6. Documentation Quality

**Strengths:**
- **Comprehensive file inventory**: All 42 CSV files are documented with column-level schemas.
- **Data types specified for every field**: All 820 columns have data type annotations.
- **Foreign key relationships explicitly documented**: 67 foreign key references enable record linking across files.
- **Some value sets documented**: 31 fields have possible/example values listed (e.g., encounter status, payment type, allergy type, test status).
- **Export folder structure clearly described**: File naming conventions for documents and photos include worked examples.
- **Dual-format document export**: Clinical templates in both HTML and PDF ensures usability.

**Weaknesses:**
- **Low description coverage**: Only 175 of 820 fields (21.3%) have any description or comment. The remaining 645 fields are documented only by column name and data type. Many column names are self-explanatory (e.g., "Patient Last Name"), but others are ambiguous (e.g., "Prelimstatus", "Confirmstatus", "Payee Type").
- **No sample data**: No example CSV rows or sample export files are provided. The Reference folder in the export is described as containing schemas but the documentation doesn't elaborate.
- **No machine-readable schema**: No JSON Schema, XSD, or other formal schema definition. The PDF is the only format.
- **No date/time format specification**: Date and Date & Time fields don't specify the format used in CSV output.
- **No string length constraints**: String fields have no max-length specification.
- **Loose data type taxonomy**: Types are general ("String", "Integer", "Currency") without precision/scale details.
- **Version 1.0 only**: Created November 2023, no updates in 2+ years. No change history.

**Could a developer build an import?** Yes, for the structured CSV data. The column names and types are clear enough to build a parser, foreign key relationships enable record linking, and the flat CSV format is universally parseable. The clinical documents (HTML/PDF) would require more effort to systematically ingest. The main obstacle is the 78.7% of fields with no description — a developer would need to infer meaning from column names alone for many fields.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

GlaceEMR provides a genuine (b)(10) native database export covering both clinical (EMR) and billing/practice management (PMS) data in CSV format, supplemented by clinical documents in HTML/PDF/XML and scanned documents in their original format. The export is clearly purpose-built for the (b)(10) requirement — it is not a repackaged FHIR API, C-CDA export, or clinical summary. The 42-file export with 820 columns across clinical and billing domains, combined with explicit relational structure and support for both single-patient and population-level export, represents a substantive compliance effort.

### Key Findings

1. **Genuine native export, not a standard-based repackaging.** The CSV-based export covers the vendor's internal data model across clinical and billing domains. C-CDA documents are included as supplementary content, not as the primary export format. This is clearly distinct from the FHIR (g)(10) API.

2. **Unusually granular clinical history coverage.** The export includes 13 distinct history categories (past medical, surgical, family, family relations, social, substance abuse, contraception/sexual, pregnancy, birthing, menstrual, occupational, obstetric, exposure) — more granular than most vendors provide.

3. **Solid billing/payment coverage.** The PMS folder includes full charge-level transactions with 4 diagnosis pointers, payment receipts with denial codes, and service-level payment posting — genuine billing data, not just a stub.

4. **Documentation has breadth but lacks depth.** All 820 fields have data types, but only 21.3% have descriptions. No sample data, no machine-readable schemas, no date format specifications. A developer could work with this, but considerable guesswork would be needed for ambiguous fields.

5. **Specialty clinical data (behavioral health, care plans) likely resides in Documents rather than structured CSV.** The product's significant behavioral health module (PHQ-9, BIMS, DSM-5 assessments, treatment plans) has no dedicated CSV file. This content is likely captured in the HTML/PDF clinical document templates, meaning it's exported but not in structured, queryable form.

### Summary Stats

    Classification:  Comprehensive native export
    Export format:   CSV (structured data) + HTML/PDF/XML/JPEG (documents)
    Model type:      Native database
    Entities:        42 CSV files
    Fields:          820
    Descriptions:    21.3% (175/820)
    Sample data:     No
    Bulk export:     Yes (single-patient and population)
    Domains covered: 11 of 16 applicable domains fully; 5 partial

### Bottom Line

GlaceEMR provides one of the more complete (b)(10) implementations for a small-to-mid-size EHR vendor, with genuine native database export across clinical and billing domains in a practical CSV format. The biggest weakness is documentation depth — only 21.3% of fields have descriptions, and specialty clinical data (behavioral health assessments, care plans) appears to be exported only as rendered documents rather than structured data. A patient or provider would receive a reasonably complete copy of their designated record set, though programmatic use of some clinical content would require parsing HTML/PDF documents.
