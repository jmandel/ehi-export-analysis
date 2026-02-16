# EHI Export Analysis: AdvancedMD

**Product**: AdvancedMD (v25), AdvancedMD Mobile (v8)
**Analysis date**: 2026-02-16
**CHPL IDs**: 11732, 11734

## 1. Product Context

AdvancedMD is a cloud-based, integrated ambulatory EHR and practice management platform serving 65,000+ practitioners across 14,000+ practices. It targets independent, small-to-mid-sized ambulatory practices across a broad range of specialties (primary care, dermatology, orthopedics, mental/behavioral health, physical therapy, pediatrics, cardiology, and many others).

The platform stores data across multiple domains relevant to EHI assessment:

- **Clinical**: Patient charts, clinical notes (fully customizable templates), problem lists, medication lists, allergy lists, vital signs, immunization records, lab orders/results, imaging orders, referrals, clinical decision support alerts, care plans, custom medical plans
- **Prescriptions**: E-prescribing records including EPCS (controlled substances), drug interactions, pharmacy information, Surescripts integration data
- **Billing/Financial**: Charges, claims, ERA/remittance, denial management, A/R, patient balances, payments, insurance eligibility verification, payer information
- **Demographics/Insurance**: Patient demographics, insurance information, contacts
- **Documents**: Scanned documents (consent forms, insurance cards, photos), faxes, clinical note attachments, claim attachments
- **Patient Engagement**: Portal messages, prescription renewal requests, appointment requests, online bill pay
- **Scheduling**: Appointments, patient self-scheduling, recalls
- **Telehealth**: Integrated video visit sessions with charting and billing

This is a full-featured EHR+PM system, so a complete EHI export should cover clinical, billing, documents, and patient-facing data.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `data-export-page.html` (279 KB) | Main EHI export documentation web page. Describes all 7 export mechanisms with field-level detail for CSV exports. | **High** — primary source for export mechanics and CSV field lists |
| `advancedmd-ehrExport-dataDictionary.pdf` (826 KB, 13 pages) | EHR Bulk Data Export data dictionary. Documents 12 SQL tables with 313 column-level descriptions, SQL JOIN examples, and detailed explanation of clinical notes structure. | **Highest** — most detailed technical artifact |
| `advancedmd-dataExport-dataDictionary.pdf` (453 KB, 6 pages) | C-CDA/HTML Data Dictionary. Maps USCDIv1 sections to AdvancedMD data sources and vocabulary codes (SNOMED, LOINC, ICD10, CPT, RxNorm). | **Medium** — useful for C-CDA export understanding |
| `advancedmd-bulkDataExport-scannedDocsImages.pdf` (2.1 MB, 9 pages) | Scanned Documents & Images export guidance. Step-by-step screenshots showing folder hierarchy and index file structure for PM and EHR document exports. | **Medium** — mostly annotated screenshots with limited extractable text |
| `advancedmd-flyer-dataExport.pdf` (36 KB, 2 pages) | Desk guide flyer summarizing all export options. Condensed overview created in Adobe InDesign. | **Low** — summary of web page content, no unique detail |
| `screenshot-data-export-page.png` (866 KB) | Full-page screenshot of the documentation web page. | **Low** — visual backup of HTML page |

**Correction to prior report**: The prior agent's report claimed all PDFs are "image-only" with "pdftotext extracts no text." This is **incorrect**. All four PDFs yield extractable text via `pdftotext -layout`. The EHR data dictionary yields 33,386 characters, the C-CDA dictionary yields 13,285 characters, and the flyer yields 8,482 characters. The scanned docs PDF is mostly annotated screenshots but still yields 3,679 characters of text.

## 3. Export Mechanics

AdvancedMD provides **7 export mechanisms** across two categories:

### Single-Patient Exports (4 mechanisms, no developer assistance needed)

| Export | Format | Mechanism | Content Domain |
|---|---|---|---|
| Patient Transaction Report | CSV | PM Reports > Patient Listings | Billing/financial |
| Patient Visit Summary Report | CSV | PM Reports > Patient Listings | Visit/billing summary |
| EHR Data Portability Export Tool | C-CDA XML + HTML | EHR > Tools > Data Portability Export Tool | USCDIv1 clinical data |
| EHR Patient Chart Print Tool | PDF | Chart Print icon in patient chart | Clinical chart (selective sections) |

### Bulk Patient Exports (3 mechanisms, developer assistance for 2 of 3)

| Export | Format | Mechanism | Developer Needed? |
|---|---|---|---|
| Practice Management Data Export | Microsoft Access .mdb | Utilities > Data Export | No |
| Scanned Documents & Images | Native files + text index | Contact Client Support Services | **Yes** |
| EHR Bulk Data Export | SQL Server .bak | Contact Client Support Services | **Yes** |

**Key considerations**:
- The EHR Bulk Data Export requires SQL Server Management Studio to restore, creating a practical accessibility barrier. The vendor acknowledges: "you'd need an IT/conversion person or team to restore the database."
- The two most comprehensive bulk exports (EHR SQL backup and Scanned Documents) require contacting Client Support Services.
- No fees are mentioned in the documentation.
- Single-patient exports are fully self-service.

## 4. Export Content: What's In It

### EHR Bulk Data Export (SQL Server .bak) — Primary Data Dictionary

This is the most detailed and documented export mechanism. The 13-page data dictionary documents **12 SQL tables** with **313 total fields**, of which **267 (85.3%) have descriptions**.

| Table | Fields | Described | Category |
|---|---|---|---|
| EHR_Allergies | 14 | 14 (100%) | Clinical — Allergies |
| EHR_Immunizations | 39 | 39 (100%) | Clinical — Immunizations |
| EHR_Messages | 23 | 12 (52%) | Clinical — Messages |
| EHR_PatientNoteDiagnosis | 5 | 5 (100%) | Clinical — Diagnoses |
| EHR_Problems | 18 | 12 (67%) | Clinical — Problem List |
| EHR_Prescriptions | 78 | 68 (87%) | Clinical — Medications/Rx |
| EHR_LabResults | 47 | 43 (91%) | Clinical — Lab Results |
| EHR_ResultItems | 11 | 11 (100%) | Clinical — Lab Results |
| EHR_ResultSets | 24 | 9 (38%) | Clinical — Lab Results |
| EHR_ResultValues | 21 | 21 (100%) | Clinical — Lab Results |
| EHR_PatientNotes | 30 | 30 (100%) | Clinical — Notes/Documentation |
| EHR_WordMerge | 3 | 3 (100%) | Clinical — Note Templates |

**Notable characteristics:**

- **EHR_Prescriptions** is the richest table (78 fields) with comprehensive drug details, DEA scheduling, Surescripts e-prescribing integration fields, pharmacy info, and prescriber/supervisor provenance.
- **Lab results** are modeled across 4 related tables (EHR_LabResults, ResultSets, ResultItems, ResultValues) with documented SQL JOIN syntax for assembly.
- **EHR_PatientNotes** uses a distinctive field-level row structure rather than assembled documents. Each row represents one field on a note template, with positioning coordinates (Left_Loc, Top_Loc), control types, and selected values. Reassembly requires understanding the parent/child ordinal system documented on pages 11-13.
- **EHR_WordMerge** stores note templates as binary blobs that must be converted to Word documents. Variable substitution (`<<field_name>>` → `selected_value`) is documented.
- **No data types** are documented for any column — only names and text descriptions.
- **No value sets** are provided for coded fields (e.g., AllergyStatus, ProblemStatus, PrescriptionType, Control_Type).
- **No foreign key documentation** beyond the lab results join and the implicit PatientID/LicenseKey relationships.

### C-CDA Export (Single Patient)

The 6-page C-CDA data dictionary documents **27 sections** mapped to USCDIv1 data elements with vocabulary codes:

Key sections with assigned codes: Allergies (RxNorm, SNOMED), Medications (RxNorm), Problems (SNOMED, ICD10), Encounters (ICD10), Procedures (CPT), Vital Signs (10 LOINC codes), Clinical Notes (6 note types with LOINC codes: Consultation 11488-4, H&P 34117-2, Discharge 18842-5, Progress 11506-3, Imaging 18748-4, Pathology 22638-1), Functional/Mental Status (SNOMED), Assessments (LOINC 51848-0), Goals (LOINC 61146-7), Health Concerns (LOINC 75310-3), Plan of Treatment (LOINC 18776-5), Care Team, Advanced Directives, Immunizations, Social History, Lab Results, Medical Equipment.

This is a standard USCDIv1 C-CDA export — no vendor extensions are documented.

### Patient Transaction Report (CSV)

**37 fields** total (13 header + 24 body). Header includes demographics (Patient, Chart Number, Address, Birthdate, Phone, Email, SSN, Sex) and insurance (Primary, Secondary, Tertiary). Body includes billing detail: Transaction Type, Charge Code, Transaction Code, Diagnosis, Payment Method, Charges, Patient Payments, Insurance Payments, Adjustments, Units, Void.

### Patient Visit Summary Report (CSV)

**27 fields** total (4 header + 23 body). Body includes visit-level billing: CPT Code, Diagnosis Codes, Charge Codes, Modifiers, Place of Service, Carrier, Copay, Current Balance, Billing Provider, Appointment Status/Date/Time/Type.

### Practice Management Data Export (.mdb)

Always includes demographics; optionally transactions and appointment data. Content: charges, payments, write-offs, patient demographics, provider information, appointments, carrier information. **No field-level data dictionary** is provided for this export.

### Scanned Documents & Images

Exports all scanned documents and images in native formats (JPG, DOC, etc.) organized by date in folder hierarchies. PM index file has 7 columns: FirstName, LastName, ChartNumber, ProfileCode, CategoryName, FileLocation, FileName. EHR index file has 2 columns: File_Key_Ptr, Document_UID. Also includes blob data CSVs.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

AdvancedMD takes a **multi-mechanism approach** to EHI export, using different formats and tools for different data domains:

**Clinical data (EHR Bulk Export — SQL .bak)**: This is the deepest part of the export. 12 tables covering allergies, immunizations, messages, diagnoses, problems, prescriptions, lab results (4-table structure), clinical notes, and note templates. The prescription table alone has 78 fields including Surescripts e-prescribing integration data. Clinical notes are exported as raw field-level data with positioning coordinates rather than assembled documents — this is a genuine "database dump" approach that preserves all captured data.

**Standard clinical summary (C-CDA)**: A USCDIv1-conformant C-CDA export covering 27 sections. This covers the standard clinical data elements (allergies, meds, problems, vitals, immunizations, encounters, procedures, lab results, clinical notes, care plans, goals, functional/mental status, social history, advance directives, care team, medical equipment).

**Billing/Financial (PM CSV reports + .mdb)**: Patient Transaction Report (37 fields) and Visit Summary Report (27 fields) provide single-patient billing data. The PM Data Export (.mdb) provides bulk billing data but lacks a published field-level data dictionary.

**Documents/Images (Scanned Documents export)**: All scanned documents and images from both PM and EHR, with index files mapping files to patients.

**The richest coverage is clinical EHR data** (313 fields across 12 well-documented tables). Billing data is covered but with less documentation depth — the CSV field lists are published on the web page but the bulk .mdb export lacks field-level documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | CSV headers (Patient Transaction Report: 13 fields), PM Data Export (always includes demographics), C-CDA | Multiple sources; adequately covered |
| Encounters / visits | ✅ Covered | C-CDA Encounters section (ICD10), Patient Visit Summary (visit-level detail) | Covered across C-CDA and PM exports |
| Problems / conditions | ✅ Covered | EHR_Problems (18 fields), EHR_PatientNoteDiagnosis (5 fields), C-CDA Problem List | Well covered with ICD10 and SNOMED codes |
| Medications / prescriptions | ✅ Covered | EHR_Prescriptions (78 fields including NDC, DEA class, Surescripts data), C-CDA Medications | Exceptionally detailed — strongest domain |
| Allergies | ✅ Covered | EHR_Allergies (14 fields), C-CDA Allergies | Thorough including reactions, treatments, status |
| Immunizations | ✅ Covered | EHR_Immunizations (39 fields including CVX, MVX, VFC eligibility, route, site), C-CDA Immunizations | Very detailed |
| Vitals | ✅ Covered | C-CDA Vital Signs (10 LOINC-coded measures including pediatric) | Via C-CDA only; not in EHR SQL tables |
| Lab results | ✅ Covered | 4-table structure: EHR_LabResults (47 fields), EHR_ResultSets (24), EHR_ResultItems (11), EHR_ResultValues (21), plus SQL JOIN documentation | Comprehensive multi-table model |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA Imaging Narrative section; no discrete imaging data in EHR bulk export | Imaging narrative only — no discrete imaging orders/results in SQL tables |
| Procedures | ⚠️ Partial | C-CDA Procedure List (CPT-coded, with noted exclusions for surgical/radiology/lab/medicine CPT ranges); Procedure Note section | C-CDA only; no procedure table in EHR bulk export; CPT exclusion ranges are concerning |
| Clinical notes / documents | ✅ Covered | EHR_PatientNotes (30 fields), EHR_WordMerge (3 fields), C-CDA clinical note sections (6 note types), Chart Print tool | Complex but comprehensive — raw field-level data with template reconstruction documented |
| Care plans / goals | ✅ Covered | C-CDA Plan of Treatment (6 sub-sections), Goals, Assessments, Health Concerns | Via C-CDA only |
| Orders / referrals | ⚠️ Partial | C-CDA "Reason for Referral" section; Chart Print includes "Orders/Tests" | No discrete orders table in EHR bulk export; referrals only as narrative |
| Insurance / coverage | ✅ Covered | CSV report headers (Primary, Secondary, Tertiary insurance), PM Data Export (carrier information), Chart Print (Insurance section) | Multiple sources |
| Claims / billing | ⚠️ Partial | Patient Transaction Report (24 body fields: charges, payments, adjustments), Visit Summary (23 body fields: CPT codes, diagnosis codes, carrier), PM .mdb (charges, payments, write-offs) | Transaction-level billing data exists, but no claim lifecycle data (submission dates, ERA details, denial reasons). PM .mdb lacks field-level documentation. |
| Payments | ✅ Covered | Patient Transaction Report (Patient Payments, Insurance Payments, Total Payments, Adjustments, Check Number, Payment Method) | Per-transaction payment detail |
| Consents / directives | ✅ Covered | C-CDA Advanced Directives, Chart Print (Advanced Directives) | Present in multiple exports |
| Patient communications / portal messages | ⚠️ Partial | EHR_Messages (23 fields), Chart Print includes "Patient Portal and Staff Messages" | EHR_Messages likely covers internal clinical messaging; Chart Print mentions portal messages but no discrete export table for portal-specific communications |
| Specialty-specific data | ⚠️ Partial | EHR_PatientNotes captures all template-based specialty content; no specialty-specific tables documented | Custom specialty templates are captured via the generic note field-level export, but no discrete specialty data structures (e.g., behavioral health assessments, dental charts) are separately documented |

**Domains covered**: 12 of 18 fully, 6 partially
**Domains not covered**: None are completely absent, but several are thin

## 6. Documentation Quality

**Strengths:**
- The EHR Bulk Export data dictionary is **substantive and practical**: 13 pages of column-level descriptions with real SQL JOIN examples and a 3-page walkthrough of clinical note reconstruction logic including parent/child ordinal relationships.
- The vendor is **transparent about complexity**: they explain why notes are stored as field-level rows, acknowledge that "adjusting your import process to account for this type of database structure is complicated," and provide concrete examples (genitourinary exam radio button scenario).
- Each export mechanism has **clear UI navigation instructions** (e.g., "From the Practice Management, go to Reports > Patient Listings > Patient Transaction Report").
- The scanned documents guidance provides **illustrated step-by-step instructions** with annotated screenshots of the folder hierarchy and index file usage.
- All text is extractable from the PDFs (contrary to the prior report's claim of "image-only" PDFs).

**Weaknesses:**
- **No data types** documented for any column — a developer cannot determine whether a field is varchar(50), int, datetime, or bit without restoring the actual .bak file.
- **No value sets** for coded fields: AllergyStatus, ProblemStatus, PrescriptionType, Control_Type, Field_Data_Type, etc. have no enumeration of valid values.
- **No foreign key documentation** beyond the lab results JOIN and the implicit LicenseKey/PatientID patterns.
- The PM Data Export (.mdb) has **no field-level data dictionary** — only a prose description of content categories.
- **No sample data files** are publicly available. The scanned documents guide references an "EHR Export Sample Data.zip" visible in screenshots but not downloadable.
- **No machine-readable schema** (JSON, XML, CSV) — all documentation is in PDF and HTML prose.
- **46 of 313 fields (14.7%)** in the EHR bulk export have no description at all, concentrated in EHR_Messages (11 undescribed), EHR_ResultSets (15 undescribed), and EHR_Prescriptions (10 undescribed).
- Documentation is dated **2023-12-05** (over 2 years old) with no versioning or change history.

**Could a developer build an import?** Partially. The EHR bulk export documentation provides enough to understand the table structure and reconstruct clinical notes, but missing data types, value sets, and relationships would require significant reverse engineering from the actual .bak file. The PM .mdb export has essentially no developer documentation.

## 7. Overall Assessment

### Classification

**Partial native export**

AdvancedMD provides a genuine native database export (SQL Server .bak) rather than repackaging C-CDA/FHIR, which puts it ahead of many vendors. However, the coverage has significant gaps: only 12 EHR tables are documented (clinical data only), the PM billing data lacks a field-level dictionary, vital signs and care plans exist only in the C-CDA projection, and there are no discrete tables for encounters, orders, referrals, or scheduling. The multi-mechanism approach (SQL + .mdb + CSV + C-CDA + documents) covers more ground than any single export, but the fragmentation and documentation gaps prevent a "comprehensive" classification.

### Key Findings

1. **Genuine native database export**: The EHR Bulk Export is a SQL Server .bak file containing raw clinical data — 12 tables, 313 fields — not a C-CDA/FHIR repackaging. This is a good-faith approach to (b)(10) that goes beyond what many vendors offer. (Source: `advancedmd-ehrExport-dataDictionary.pdf`)

2. **Multi-mechanism design covers breadth but fragments the data**: 7 export mechanisms across 5 different formats (SQL .bak, Access .mdb, CSV, C-CDA XML, native files) are required to get all the data. No single mechanism covers everything. A receiving system would need to import from all formats and cross-reference by patient ID/chart number. (Source: `data-export-page.html`, `advancedmd-flyer-dataExport.pdf`)

3. **Billing/PM data is under-documented**: While billing data is exportable via CSV reports and the Access .mdb file, the .mdb bulk export has no field-level data dictionary at all. This is a significant documentation gap for a product whose core value proposition includes billing and practice management. (Source: absence in all artifacts)

4. **Clinical notes use a complex but complete raw data model**: Notes are stored as individual field-level rows with template positioning coordinates rather than assembled documents. The vendor provides detailed reconstruction guidance (pages 8-13 of the EHR data dictionary) including SQL JOINs and parent/child ordinal interpretation. This is the vendor's actual database structure, transparently exported. (Source: `advancedmd-ehrExport-dataDictionary.pdf`, pages 8-13)

5. **Vitals, care plans, and several clinical domains exist only in C-CDA**: Vital signs, care plans, goals, assessments, functional/mental status, social history, encounters, procedures, and advance directives are documented only in the C-CDA export — not as discrete tables in the SQL backup. This means the "all EHI" export for these domains relies on a standard clinical summary projection rather than native data. (Source: comparison of `advancedmd-ehrExport-dataDictionary.pdf` tables vs. `advancedmd-dataExport-dataDictionary.pdf` C-CDA sections)

### Summary Stats

```
Classification:  Partial native export
Export format:   SQL Server .bak + Access .mdb + CSV + C-CDA XML + native files
Model type:      Hybrid (native database for EHR clinical, standard projection for USCDIv1 via C-CDA, flat file for billing)
Entities:        12 (EHR SQL tables) + PM .mdb (undocumented) + 27 C-CDA sections
Fields:          313 (EHR SQL) + 64 (CSV reports) = 377 documented fields
Descriptions:    85.3% of EHR SQL fields (267/313)
Sample data:     No (referenced in screenshots but not publicly available)
Bulk export:     Yes (SQL .bak + Access .mdb + scanned docs; 2 of 3 require developer assistance)
Domains covered: 12 of 18 fully, 6 of 18 partially (0 completely absent)
```

### Bottom Line

AdvancedMD makes a genuine, above-average effort at EHI export — providing a raw SQL database dump of clinical data rather than just a C-CDA summary, plus separate billing and document exports. A patient would receive a reasonably complete picture of their clinical data, billing transactions, and scanned documents. The biggest gap is that billing/PM data, which is a core part of the product, lacks the same field-level documentation depth as the clinical EHR data, and several clinical domains (vitals, care plans, procedures) exist only in the C-CDA projection rather than as native data structures. The fragmentation across 7 mechanisms and 5 formats also creates practical barriers to data portability.
