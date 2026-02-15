# EHI Export Analysis: Comtron Inc.

**Product**: Medgen EHR (Version 9)
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2984.Medg.09.02.1.220915 (CHPL ID 10986)

## 1. Product Context

Medgen EHR, developed by Comtron Inc. (now integrated into MEDFAR Clinical Solutions), is a cloud-based ONC-certified EHR with integrated billing and practice management for ambulatory practices. It targets general primary care but has two deep specialty modules:

- **Addiction medicine / Opioid Treatment Programs (OTPs)**: controlled substance inventory management (methadone, buprenorphine), dispensing pump interfaces, drug screening panels, lot/bottle tracking, dosing records, service plans, bio-psychosocial assessments, counselor dashboards, incident management
- **OB/GYN**: antepartum/postpartum forms, pregnancy tracking, estimated fetal weight calculators, EDD calculators, ultrasound DICOM integration, high-risk care plans, OB questionnaires

Beyond these specialties, Medgen includes: e-prescribing (including EPCS), patient portal with secure messaging, scheduling, integrated medical billing with EDI claim submission, electronic payment reconciliation, document scanning (MedScan), lab/radiology interfaces, and public health reporting (immunization registries, syndromic surveillance, cancer case reporting).

For EHI export completeness, the key question is whether the export covers not just standard clinical data but also:
- Billing and financial data (charges, claims, payments, insurance)
- Addiction medicine specialty data (dispensing, screening, dosing)
- OB/GYN specialty data (pregnancy records, ultrasound reports)
- Patient documents and communications
- E-prescribing records

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/MedgenBackupUtility.pdf` | "Medgen Data Export & Backup Utility Guide v1.0" (July 2023, 79 pages, 2.98 MB). The sole artifact. Documents a Windows desktop application for exporting patient data as C-CDA XML + document ZIPs + supplementary CSV files. | **Primary source** — the only documentation available. Contains installation instructions (pp. 5–17), C-CDA section documentation (pp. 18–70), document download examples (pp. 71–72), and CSV data dictionaries (pp. 72–77). |

Only one artifact was collected. The registered (b)(10) URL pointed directly to this PDF. No additional documentation, sample data files, schemas, or data dictionaries were found.

## 3. Export Mechanics

- **Format**: Hybrid — C-CDA XML per patient + patient document ZIP files + 5 supplementary CSV files
- **Mechanism**: Windows desktop application (`MedBackup_Utility.exe`) installed via MSI; connects to Medgen EHR cloud service using Medgen login credentials
- **Single-patient vs bulk**: Supports both. Users can export by: (1) all patients in a practice, (2) date/time range, or (3) individual patient ID selection. Automated bulk export via Windows Task Scheduler using `AUTORUN <PRACTICE CODE>` command-line argument is documented.
- **Bulk caveat**: The final page (p. 78) states: "For a bulk data export of full patient populations please contact a Medgen support team member: medgensupport@comtronusa.com" — suggesting the utility may have practical limits for large populations.
- **Encryption**: Optional AES encryption of exported files with user-specified key; built-in decrypt function.
- **Access constraints**: Requires Medgen EHR login credentials and Windows with administrative rights. No fees mentioned.

## 4. Export Content: What's In It

The export has three components:

### Component 1: C-CDA XML (per patient)

Each patient gets one C-CDA XML document. The PDF documents 16 C-CDA sections with template IDs, XPath structures, and USCDI data class mappings. These are standard C-CDA sections — the documentation largely reproduces standard C-CDA specifications rather than describing Medgen-specific extensions or customizations.

**16 C-CDA sections documented** with 57 total data elements across them (see table below). No custom vendor extensions are documented.

### Component 2: Patient Document ZIPs (per patient)

Each patient gets a ZIP file containing scanned/attached documents (lab reports, patient education materials, etc.). File naming convention documented on p. 72: `{docno}_{date}_{idcode}_{firstname}_{lastname}_{dob}_{provider}_{description}.{ext}`

### Component 3: Supplementary CSV files

Five CSV files extend beyond C-CDA to cover data not captured in the standard clinical document. Column-level data dictionaries are provided on pp. 72–77.

### Vendor's own content organization

**C-CDA Sections** (pp. 18–70):

| C-CDA Section | USCDI Data Class | Data Elements | Pages |
|---|---|---|---|
| Allergy Intolerance | Allergies & Intolerance | Drug allergies, Reactions | 20–24 |
| CarePlan | CarePlan | Health concerns, Interventions, Goals, Outcomes | 25–26 |
| CareTeam | Care Team | Member Name, Identifier, Role, Location, Telecom | 27–30 |
| Problems | Problems | Problems, Health Concerns, Date of diagnosis, Date of resolution | 31–33 |
| Medication | Medication | Medication, Dose, Indication, Fill status | 34–36 |
| Immunization | Immunization | Vaccination status, Code | 37–38 |
| Functional Status | Functional Status | Health Concerns, Functional Status, Smoking status | 39–41 |
| Cognitive Status | Cognitive Status | Physical, Cognitive, Intellectual, Psychiatric disabilities | 42–44 |
| Result Section Data | Results | Tests, Values/Results | 45–48 |
| Vital Signs | Vital Signs | Systolic BP, Diastolic BP, Heart Rate, Respiratory Rate, Temperature, Height, Weight, Pulse Ox, O2 Conc. | 49–53 |
| Social History | Social History | Name, DOB, Birth sex, Address, Telecom, Smoking status | 54–57 |
| Implant or Device | Implant/Device | Device (UDI) | 58–59 |
| History of Encounter | Encounters | Encounter Type, Diagnosis, Time, Location | 60–63 |
| Goals | Goals | Patient Goals | 64–65 |
| Procedure | Procedure | Procedures | 66–67 |
| Clinical Notes | Clinical Notes | Consultation note, Discharge summary, Procedure note, Progress note, Test Reports | 68–70 |

**CSV Files** (pp. 72–77):

| CSV File | Title | Fields | Meaningful Descriptions | Types Documented |
|---|---|---|---|---|
| patients.csv | Patient Demographics & Insurance | 22 | 22 (100%) | No |
| appointments.csv | Patient Appointments | 12 | 12 (100%) | No |
| pharmacy.csv | Patient Pharmacies | 7 | 7 (100%) | No |
| comments.csv | Patient Comments | 6 | 5 (83%) | No |
| Transactions.csv | Patient Charges & Transactions | 114 | 0 (0%) | No |
| **Total** | | **161** | **46 (29%)** | |

**Critical finding on Transactions.csv**: This is the largest CSV file at 114 columns (not 117 as the prior report claimed — verified by direct extraction from the PDF). However, every single "Description" entry simply repeats the column name verbatim. For example: column "Claim No" has description "Claim No"; column "Deductible" has description "Deductible"; column "PriInsGroupName" has description "PriInsGroupName." Zero of 114 fields have meaningful descriptions. A developer would need to guess the meaning and data types of fields like "InitialIns," "POS," "Hold," "SALES_GROUP_1," and "Test Code."

The smaller CSV files (patients.csv, appointments.csv, pharmacy.csv, comments.csv) do have genuine descriptions — e.g., "Patient DOB (MM/DD/YYYY)," "Appointment Provider Medgen Identifier," "Pharmacy NCPDPID."

Full field inventory saved to `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export combines two distinct approaches:

**C-CDA (standard clinical data)**: 16 sections covering USCDI v1 data classes — allergies, care plans, care teams, problems, medications, immunizations, functional/cognitive status, lab results, vitals, social history, devices, encounters, goals, procedures, and clinical notes. This is essentially a standard USCDI clinical summary. The documentation on these sections spans pp. 18–70 but consists primarily of generic C-CDA standard education (explaining what C-CDA is, showing XML template structures) rather than Medgen-specific documentation. No vendor extensions, custom sections, or specialty-specific C-CDA content is documented.

**CSV files (non-clinical supplementary data)**: 5 files covering demographics/insurance (22 fields), appointments (12 fields), pharmacy associations (7 fields), patient comments/alerts (6 fields), and billing transactions (114 fields). The billing CSV is notably comprehensive in scope — covering claims, charges, payments, adjustments, balances, diagnoses, insurance details, and provider information — even though its documentation quality is poor.

**Document ZIPs**: Patient-attached documents exported as files, preserving the original format.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | C-CDA Social History section + `patients.csv` (22 fields: name, address, phone, email, SSN, DOB, sex) | Adequate. CSV includes SSN and contact details beyond C-CDA. |
| Encounters / visits | ✅ Covered | C-CDA History of Encounter section (type, diagnosis, time, location) + `appointments.csv` (12 fields) | Encounters in C-CDA; scheduling data in CSV. |
| Problems / conditions | ✅ Covered | C-CDA Problems section (problems, health concerns, diagnosis/resolution dates) | Standard USCDI coverage. |
| Medications / prescriptions | ⚠️ Partial | C-CDA Medication section (medication, dose, indication, fill status) | Current medications are covered. No e-prescribing transmission history, EPCS records, or pharmacy refill request history — the product does e-prescribing including controlled substances. |
| Allergies | ✅ Covered | C-CDA Allergy Intolerance section (drug allergies, reactions) | Standard coverage. Food/environmental allergies noted as excluded per documentation. |
| Immunizations | ✅ Covered | C-CDA Immunization section (vaccination status, code) | Standard coverage. |
| Vitals | ✅ Covered | C-CDA Vital Signs section (9 data elements: BP, HR, RR, temp, height, weight, pulse ox, O2 concentration) | Thorough. |
| Lab results | ✅ Covered | C-CDA Result Section Data (tests, values/results) | Standard coverage. |
| Imaging / diagnostic reports | ⚠️ Partial | Results section may include some imaging. OB/GYN ultrasound DICOM integration is a product feature but no specific imaging export documented. | Product integrates ultrasound DICOM (for OB/GYN) and radiology interfaces, but export does not specifically address imaging data. |
| Procedures | ✅ Covered | C-CDA Procedure section | Standard coverage. |
| Clinical notes / documents | ✅ Covered | C-CDA Clinical Notes section (consultation, discharge, procedure, progress notes, test reports) + patient document ZIPs | Notes via C-CDA; attached documents via ZIP. |
| Care plans / goals | ✅ Covered | C-CDA CarePlan + Goals sections | Standard USCDI coverage. |
| Orders / referrals | ❌ Not covered | No order or referral data in export | Product has CPOE and referral authorization tracking; neither is in the export. |
| Insurance / coverage | ✅ Covered | `patients.csv` (primary/secondary insurance code, name, policy number) + `Transactions.csv` (insurance details, plan IDs, effective/term dates, group names) | Good coverage across both CSV files. |
| Claims / billing | ✅ Covered | `Transactions.csv` (114 fields: claims, procedure codes, charges, payments, deductibles, copays, adjustments, balances, diagnosis codes, claim status, dates) | Broad coverage despite poor documentation quality. |
| Payments | ✅ Covered | `Transactions.csv` includes payment fields (Paid, Amount, CheckDate, PaymentPostedDate, PayInsurance, PaidToPatient) | Included within billing CSV. |
| Consents / directives | ❌ Not covered | No consent or directive data in export | Product has "pre-populated release authorization templates" (addiction medicine); not in export. |
| Patient communications / portal messages | ❌ Not covered | No portal message or patient communication data in export | Product has patient portal with secure messaging and appointment reminders. Not addressed. |
| Specialty: Addiction medicine | ❌ Not covered | No addiction medicine data in export | **Major gap.** Product's signature specialty includes: controlled substance inventory (methadone, buprenorphine), dispensing records, drug screening panels, lot/bottle tracking, dosing records, spillage tracking, service plans, bio-psychosocial assessments, counselor notes, incident management. None of this appears in the export. |
| Specialty: OB/GYN | ❌ Not covered | No OB/GYN-specific data in export | **Major gap.** Product features antepartum/postpartum forms, pregnancy tracking, EFW calculations, EDD records, ultrasound reports, high-risk care plans, OB questionnaires. None is in the export. |

## 6. Documentation Quality

**Strengths:**
- Step-by-step installation and configuration instructions with screenshots (pp. 5–17)
- C-CDA sections documented with template IDs and XPath structures
- Smaller CSV files (patients.csv, appointments.csv, pharmacy.csv, comments.csv) have column-level specifications with meaningful descriptions
- File naming convention for patient documents is documented (p. 72)

**Weaknesses:**
- **Transactions.csv (114 fields) has zero meaningful descriptions** — every "Description" column simply repeats the column name. This is the largest and most complex data file in the export.
- No data types are specified for any CSV field. Some can be inferred from descriptions (e.g., "MM/DD/YYYY" for dates in the smaller CSVs) but most cannot.
- No value sets or code system documentation for coded fields (e.g., claim status values, insurance class codes, bill types).
- No foreign key or relationship documentation, though `Id_code` appears to be the patient join key across CSVs.
- No sample data files are provided.
- No machine-readable schemas (no JSON Schema, no XSD, no CSV headers).
- Much of the 79-page document (approximately pp. 4–70) consists of generic C-CDA standard education rather than product-specific documentation.
- The "Software Requirements" page (p. 78) appears truncated — it says requirements are "needed" but doesn't list them.
- The document is v1.0 from July 2023 with no change history or versioning.

**Could a developer build an import?** For C-CDA: yes, because C-CDA is a well-documented standard (the developer would use the C-CDA spec, not this document). For the smaller CSVs: possibly, with some assumptions about data types. For Transactions.csv: it would require significant guesswork — field names like "InitialIns," "POS," "Hold," "ThirdParty," and "SALES_GROUP_1" through "SALES_GROUP_4" have no documentation at all.

## 7. Overall Assessment

### Classification

**Partial native export.** This is a hybrid approach — standard C-CDA clinical data supplemented with native CSV data for demographics, appointments, pharmacy, comments, and billing transactions. The C-CDA component is a standard clinical summary (not a native data model export), while the CSV files do expose native tabular data. The approach covers general clinical domains and billing, but has significant gaps in specialty data (addiction medicine, OB/GYN) and non-clinical EHI (orders, referrals, portal messages, consents). Documentation quality is uneven — adequate for smaller CSVs but essentially absent for the 114-field billing file.

### Key Findings

1. **Addiction medicine data is entirely missing from the export.** This is Medgen's signature specialty — controlled substance dispensing, drug screening, dosing records, service plans — and none of it is addressed. For OTP practices, this represents a critical gap in the designated record set.

2. **OB/GYN specialty data is entirely missing.** Antepartum/postpartum records, pregnancy tracking, EFW calculations, ultrasound reports, and OB questionnaires are absent. For OB/GYN practices, this is a significant omission.

3. **Transactions.csv provides broad billing coverage but zero documentation.** All 114 fields have "descriptions" that simply repeat the column name. This is the most important non-C-CDA component of the export, and it's essentially undocumented.

4. **The C-CDA portion is standard, not custom.** No vendor extensions or Medgen-specific content is documented. The 50+ pages of C-CDA documentation largely reproduce standard specifications rather than describing what Medgen specifically exports.

5. **The export is a purpose-built tool, not a FHIR/API repackaging.** The Medgen Backup Utility is a dedicated desktop application with its own documentation, encryption, and scheduling capabilities — demonstrating genuine effort toward (b)(10) compliance beyond simply pointing at the (g)(10) FHIR API.

### Summary Stats

    Classification:  Partial native export
    Export format:   C-CDA XML + CSV + document ZIPs
    Model type:      Hybrid (standard C-CDA + native CSV supplement)
    Entities:        5 CSV files + 16 C-CDA sections + document ZIPs
    Fields:          161 CSV fields + 57 C-CDA data elements = 218 documented data points
    Descriptions:    29% of CSV fields have meaningful descriptions (46/161); 0% for the 114-field billing file
    Sample data:     No
    Bulk export:     Yes (with caveats — vendor contact may be needed for full populations)
    Domains covered: 12 of 19 applicable domains

### Bottom Line

Medgen's export makes a genuine effort by supplementing C-CDA clinical data with native CSV files for billing, demographics, and scheduling — better than vendors who simply point to their FHIR API. However, the complete absence of the product's two signature specialty modules (addiction medicine and OB/GYN) from the export represents a critical gap for the practices that depend on those features. For a general ambulatory practice, the export is reasonable; for an opioid treatment program or OB/GYN practice, large portions of the designated record set would be missing.
