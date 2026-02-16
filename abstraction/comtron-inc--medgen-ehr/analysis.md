# EHI Export Analysis: Comtron Inc. (Medgen EHR)

**Product**: Medgen EHR (Version 9)  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2984.Medg.09.02.1.220915

## 1. Product Context

Medgen EHR is a cloud-based, ONC-certified electronic health record system with integrated billing and practice management, developed by Comtron Inc. (now part of MEDFAR Clinical Solutions). It targets ambulatory physician practices with particular specialization in **addiction medicine / opioid treatment programs (OTPs)** and **OB/GYN practices**, plus general ambulatory care across internal medicine, pediatrics, cardiology, psychiatry, and other specialties.

Key data domains the product stores:
- **Core clinical**: Demographics, problems, medications, allergies, immunizations, vitals, lab results, clinical notes, procedures, care plans, goals, functional/cognitive status
- **Billing & practice management**: Integrated claims, charges, payments, adjustments, EDI electronic claims, insurance eligibility, superbills, referral authorizations
- **E-prescribing**: Electronic prescriptions including controlled substances (EPCS)
- **Scheduling**: Appointments, wait lists, procedure scheduling, group sessions
- **Document management**: Scanned documents, faxes, patient documents
- **Patient portal**: Secure messaging, appointment reminders
- **Addiction medicine specialty**: Controlled substance inventory (methadone, buprenorphine), dispensing records, drug screening panels, dosing records, service plans, bio-psychosocial assessments, incident reports
- **OB/GYN specialty**: Antepartum/postpartum forms, pregnancy tracking, EFW calculators, ultrasound DICOM integration
- **Lab integration**: Interfaces with multiple labs, result tracking
- **Public health reporting**: Immunization registries, syndromic surveillance, cancer case reporting

This is a small-market vendor (3 Capterra reviews) but with genuinely deep features in its niche areas, particularly the addiction medicine and OB/GYN specialty modules.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/MedgenBackupUtility.pdf` | Medgen Data Export & Backup Utility Guide v1.0, July 2023, 79 pages. Documents the desktop backup utility for exporting patient data as C-CDA XML files, patient document ZIPs, and supplementary CSV files. Contains installation instructions (pp. 5–17), C-CDA section-by-section documentation with template IDs (pp. 18–70), patient document download description (pp. 71–72), file naming conventions (p. 72), and CSV column-level data dictionaries (pp. 73–78). | **Primary source** — the only artifact, and it is the complete EHI export documentation |

Only one artifact was collected. The PDF is the vendor's sole EHI export documentation.

## 3. Export Mechanics

- **Format**: Three output types combined:
  1. **C-CDA XML** files — one per patient, containing standard clinical sections
  2. **ZIP archives** — patient documents (PDFs, scanned documents, etc.)
  3. **CSV files** — supplementary data: demographics/insurance, appointments, pharmacies, comments, and billing transactions
- **Mechanism**: Desktop application ("Medgen Backup Utility" — `MedBackup_Utility.exe`) installed locally, connects to the Medgen cloud system via API. Requires Medgen login credentials and administrative permissions.
- **Single-patient vs bulk**: Supports both. Configuration options include: all patients, by date/time range, or by specific patient ID codes (multiple selectable). Auto-backup via Windows Task Scheduler is also supported.
- **Access constraints**: Requires installation of the desktop utility (MSI installer), Medgen login credentials, and administrative Windows permissions. Backup files can optionally be encrypted with a user-defined key. For bulk data export of full patient populations, the documentation directs users to contact Medgen support (medgensupport@comtronusa.com).
- **Fees**: Not documented.

## 4. Export Content: What's In It

The export consists of three components documented across 79 pages.

### 4a. C-CDA Clinical Data (pages 18–70)

The C-CDA component covers 16 clinical sections, each documented with:
- USCDI data class mapping
- Data elements listed per section
- C-CDA template IDs and LOINC section codes
- XML structure examples with sample data screenshots
- Specific code constraints (e.g., SNOMED CT codes for allergy types, RxNorm for drugs)

The 16 C-CDA sections contain a total of **74 documented data elements** across the following USCDI-aligned areas:

| C-CDA Section | Data Elements | USCDI Class |
|---|---|---|
| Allergy Intolerance | 5 | Allergies & Intolerance |
| CarePlan | 6 | CarePlan |
| CareTeam | 5 | Care Team |
| Problems | 5 | Problems |
| Medication | 5 | Medication |
| Immunization | 4 | Immunization |
| Functional Status | 3 | Functional Status |
| Cognitive Status | 6 | Cognitive Status |
| Result Section Data | 5 | Laboratory / Clinical Tests |
| Vital Signs | 9 | Vital Signs |
| Social History | 9 | Social History / Demographics |
| Implant or Device | 1 | Medical Devices |
| History of Encounter | 4 | Encounters |
| Goals | 1 | Goals |
| Procedure | 1 | Procedures |
| Clinical Notes | 5 | Clinical Notes |

This is a standard C-CDA implementation aligned with USCDI requirements — the documentation explicitly references USCDI data classes for each section.

### 4b. Patient Documents (pages 71–72)

Patient documents are exported as ZIP archives. File naming convention: `docnumber_date_idcode_firstname_lastname_dob_providerid_description.filetype`. Example: `82097048_20230719_100011_TEST_DEMO_19570923_78_Lab Reports.PDF`. This captures scanned documents, lab reports, and other uploaded files from the patient chart.

### 4c. Supplementary CSV Files (pages 73–78)

Five CSV files provide data beyond what C-CDA covers. All fields have documented column names and descriptions, though the Transactions.csv descriptions mostly just repeat the field name.

| CSV File | Fields | Description Quality |
|---|---|---|
| patients.csv | 22 | Good — all 22 fields have meaningful descriptions (e.g., "Patient DOB (MM/DD/YYYY)", "Patient Primary Insurance Policy Number") |
| appointments.csv | 12 | Good — all 12 fields have meaningful descriptions |
| pharmacy.csv | 7 | Good — all 7 fields have meaningful descriptions |
| comments.csv | 6 | Good — all 6 fields have meaningful descriptions |
| Transactions.csv | 114 | Poor — the vast majority of the 114 fields have descriptions that simply repeat the column name (e.g., field "Paid" described as "Paid", field "Deductible" described as "Deductible"). Some fields like dates lack format specifications. |

**Total CSV fields**: 161 across 5 files.

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| C-CDA: Allergy Intolerance | 5 | 5 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: CarePlan | 6 | 6 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: CareTeam | 5 | 5 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Problems | 5 | 5 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Medication | 5 | 5 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Immunization | 4 | 4 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Functional Status | 3 | 3 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Cognitive Status | 6 | 6 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Result Section Data | 5 | 5 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Vital Signs | 9 | 9 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Social History | 9 | 9 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Implant or Device | 1 | 1 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: History of Encounter | 4 | 4 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Goals | 1 | 1 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Procedure | 1 | 1 | N/A (XML) | C-CDA Clinical Data |
| C-CDA: Clinical Notes | 5 | 5 | N/A (XML) | C-CDA Clinical Data |
| patients.csv | 22 | 22 | No | CSV Supplementary Data |
| appointments.csv | 12 | 12 | No | CSV Supplementary Data |
| pharmacy.csv | 7 | 7 | No | CSV Supplementary Data |
| comments.csv | 6 | 6 | No | CSV Supplementary Data |
| Transactions.csv | 114 | ~5 meaningful | No | CSV Supplementary Data - Billing |
| Patient Documents (ZIP) | N/A | N/A | N/A | Document Export |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three tiers:

1. **C-CDA Clinical Data** (16 sections, 74 data elements): This is a standard USCDI-aligned C-CDA implementation. The documentation explicitly maps each section to USCDI data classes and references standard C-CDA template IDs. There is nothing product-specific here — this is the same C-CDA output any certified EHR would produce for transitions of care.

2. **CSV Supplementary Files** (5 files, 161 fields): This is where the vendor goes beyond C-CDA. The standout is `Transactions.csv` with 114 fields covering claims, charges, payments, adjustments, insurance details, diagnosis codes (12 slots), procedure codes with modifiers, referring providers, payer information, and multiple date tracking fields. This is genuinely detailed billing data. The other CSVs cover demographics/insurance (22 fields), appointments (12), pharmacies (7), and comments (6).

3. **Patient Documents** (ZIP archives): Scanned documents, lab reports, and other uploaded files from the patient chart.

The **strongest component** is the Transactions.csv — 114 fields of billing data is genuinely deep and goes well beyond USCDI. The **weakest component** is the C-CDA, which is entirely standard with no vendor extensions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patients.csv` (22 fields incl. SSN, multiple phones, email); C-CDA Social History section (name, DOB, sex, address) | Good coverage across two sources |
| Encounters / visits | ⚠️ Partial | C-CDA History of Encounter (type, diagnosis, time, location); `appointments.csv` (12 fields) | Encounters are in C-CDA; appointments add scheduling context. No visit-level detail beyond what C-CDA provides |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA Problems section (problems, status, dates of diagnosis/resolution) | Standard C-CDA coverage |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medication section (medication, dose, indication, fill status) | C-CDA standard only — no e-prescribing detail (EPCS data, pharmacy communications, refill history), despite product having deep e-prescribing features |
| Allergies | ✅ Covered | C-CDA Allergy Intolerance (type, coded substance, status, reaction) | Standard C-CDA coverage |
| Immunizations | ✅ Covered | C-CDA Immunization section (status, code, date, quantity) | Standard C-CDA coverage |
| Vitals | ✅ Covered | C-CDA Vital Signs (9 vital sign types) | Standard C-CDA coverage |
| Lab results | ✅ Covered | C-CDA Result Section Data (tests, values, status, location) | Standard C-CDA coverage |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA Result Section Data mentions imaging; patient documents may include imaging reports | No specific imaging data structure; OB/GYN ultrasound DICOM data appears absent |
| Procedures | ✅ Covered | C-CDA Procedure section | Standard C-CDA — minimal detail |
| Clinical notes / documents | ✅ Covered | C-CDA Clinical Notes (5 note types); Patient Documents ZIP export | Notes via C-CDA plus raw document files |
| Care plans / goals | ✅ Covered | C-CDA CarePlan and Goals sections | Standard C-CDA coverage |
| Orders / referrals | ❌ Not covered | No order or referral data in export | Product has CPOE and referral authorization tracking; gap |
| Insurance / coverage | ✅ Covered | `patients.csv` (primary/secondary insurance code, name, policy); `Transactions.csv` (detailed insurance fields: PriInsCode through SecTermDate, 16 insurance fields) | Good coverage — basic info in demographics, detailed per-claim in transactions |
| Claims / billing | ✅ Covered | `Transactions.csv` (114 fields: claims, charges, payments, adjustments, balances, diagnosis codes, procedure codes, billing dates, payer info) | **Strongest non-USCDI component** — genuinely detailed billing export |
| Payments | ✅ Covered | `Transactions.csv` includes Paid, Amount, CHECKCREDITNUMBER, CheckDate, PaymentPostedDate, PaidToPatient | Covered within billing transactions |
| Consents / directives | ❌ Not covered | No consent data in export | Product likely stores consent forms; gap |
| Patient communications / portal | ⚠️ Partial | `comments.csv` (6 fields: date, alert flag, comment text) | Comments only — no portal messages, no secure messaging threads despite product having patient portal |
| Addiction medicine specialty | ❌ Not covered | No addiction-specific data in export | **Major gap**: Product has deep OTP features (controlled substance inventory, dispensing records, drug screening, dosing records, service plans, bio-psychosocial assessments, incident reports) — none exported |
| OB/GYN specialty | ❌ Not covered | No OB/GYN-specific data in export | **Major gap**: Product has antepartum/postpartum forms, pregnancy tracking, EFW calculators, ultrasound DICOM integration — none exported |
| Functional / cognitive status | ✅ Covered | C-CDA Functional Status and Cognitive Status sections | Standard C-CDA coverage |
| Care team | ✅ Covered | C-CDA CareTeam section (member name, ID, role, location, telecom) | Standard C-CDA coverage |
| Devices | ✅ Covered | C-CDA Implant or Device section | Standard C-CDA, minimal |

## 6. Documentation Quality

**Strengths:**
- The PDF is well-organized at 79 pages with clear section structure, table of contents, and screenshots
- C-CDA sections include template IDs, LOINC codes, and XML structure examples with sample data
- CSV files have column-level data dictionaries with position numbers and descriptions
- Installation and configuration instructions are detailed with screenshots
- File naming conventions are documented with examples

**Weaknesses:**
- **Transactions.csv descriptions are essentially useless**: 109+ of 114 field descriptions simply repeat the column name (e.g., "Paid" → "Paid", "Deductible" → "Deductible"). No data types, no value sets, no format specifications for dates or amounts
- **No data types documented** for any CSV field (no indication of string length, numeric precision, date format beyond a few examples)
- **No relationships/foreign keys** documented between CSV files (e.g., how Id_code in patients.csv relates to Patient ID in Transactions.csv)
- **No sample data files** provided — only screenshots in the PDF
- **No machine-readable schema** — everything is in a PDF
- **C-CDA documentation is generic**: It describes the C-CDA standard rather than Medgen-specific implementation details. The section overviews read like a C-CDA tutorial rather than a product data dictionary

**Could a developer build an import from this documentation?**
For the C-CDA portion, yes — but only because C-CDA is a well-known standard, not because of Medgen's documentation. For the CSV files, a developer could parse patients.csv, appointments.csv, pharmacy.csv, and comments.csv reasonably well. For Transactions.csv, the lack of meaningful descriptions, data types, and value sets would make interpretation of many fields (especially status fields, insurance class codes, sales groups) require guesswork.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth**: **Partial**

The export covers standard clinical data through C-CDA (USCDI-scope), plus a genuinely detailed billing/transactions CSV (114 fields). However, it is missing significant portions of what Medgen EHR stores:

- **Addiction medicine specialty data** — a major differentiator for this product — is entirely absent. Controlled substance inventory, dispensing records, drug screening, dosing records, service plans, bio-psychosocial assessments, and incident reports are core data stored by the product for its OTP customers.
- **OB/GYN specialty data** — another key differentiator — is entirely absent. Antepartum/postpartum records, pregnancy tracking, EFW calculations, and ultrasound reports are not in the export.
- **Orders and referrals** are missing despite the product having CPOE and referral authorization tracking.
- **E-prescribing details** beyond what C-CDA captures are absent.
- **Patient portal messages** are absent despite the product having a patient portal with secure messaging.

The billing data (Transactions.csv) is a genuine positive signal — 114 fields covering claims, charges, payments, adjustments, and insurance details shows the vendor engaged with the concept of exporting beyond clinical summaries. But the total absence of both specialty modules that define this product's niche is a significant gap.

**Axis 2 — Export approach**: **Purpose-built EHI export** (with significant limitations)

This is not simply a repackaged C-CDA or FHIR export. The vendor built a dedicated desktop utility ("Medgen Backup Utility") that combines three output types:
1. Standard C-CDA for clinical data
2. Patient document archives
3. Five supplementary CSV files covering demographics, appointments, pharmacies, comments, and — critically — a detailed 114-field billing transactions file

The CSV supplementary files, particularly Transactions.csv, demonstrate that the vendor intentionally went beyond C-CDA/USCDI scope for the (b)(10) requirement. The utility also supports bulk export with auto-scheduling via Windows Task Scheduler. This is a purpose-built tool, not a relabeled existing export — but it covers only a subset of the product's data domains.

### Key Findings

1. **Billing data is genuinely detailed**: The 114-field Transactions.csv covers claims, charges, payments, adjustments, 12 diagnosis code slots, procedure codes with 4 modifiers, insurance details, and multiple date-tracking fields. This is the strongest signal that the vendor engaged with (b)(10) beyond just USCDI.

2. **Specialty modules entirely missing**: Despite addiction medicine (OTP) and OB/GYN being Medgen's primary market differentiators with deep functionality, zero specialty-specific data appears in the export. This is the single biggest gap — patients in these programs have extensive specialty records that would not be exported.

3. **C-CDA component is entirely standard**: The 16 C-CDA sections map directly to USCDI data classes with no vendor extensions. The documentation reads more like a C-CDA tutorial than a product-specific data dictionary.

4. **Transactions.csv documentation is poor**: While the billing CSV has 114 fields, the descriptions are mostly just the field name repeated. A developer would struggle to interpret fields like `PriInsClass`, `SALES_GROUP_1`–`SALES_GROUP_4`, or `Hold` without additional context.

5. **Purpose-built utility is a positive signal**: The dedicated desktop application with bulk export, auto-scheduling, encryption, and multi-format output shows genuine engineering effort for (b)(10) compliance, even though the content coverage has significant gaps.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   C-CDA XML + ZIP (documents) + CSV (5 supplementary files)
Entities:        22 (16 C-CDA sections + 5 CSV files + 1 document archive)
Fields:          235 (74 C-CDA data elements + 161 CSV fields)
Descriptions:    51.1% meaningful (C-CDA elements all described; most Transactions.csv fields echo name only)
Sample data:     No (screenshots only in PDF)
Bulk export:     Yes (all patients, by date range, or by patient ID; auto-backup via Task Scheduler)
Domains covered: 13 of 19 applicable domains (major gaps in specialty modules and orders)
```

### Bottom Line

Medgen EHR built a purpose-specific export utility that combines standard C-CDA with genuinely detailed billing data (114-field Transactions.csv) and supplementary CSVs — a meaningful effort beyond just repackaging clinical exchange. However, the export entirely omits the addiction medicine and OB/GYN specialty data that define this product's niche, meaning patients in those programs would lose their most critical specialized records. The biggest single gap is the absence of any OTP/addiction medicine data (controlled substance dispensing, dosing records, drug screening, service plans) in a product whose primary market is opioid treatment programs.
