# EHI Export Analysis: ReLi Med Solutions, LLC

**Product**: ReLiMed EMR (Version 7.3)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2990.ReLi.07.01.1.221118

## 1. Product Context

ReLiMed EMR is an integrated cloud-based EHR and practice management system targeting small to mid-size ambulatory practices. Developed by ReLi Med Solutions, LLC (~50 employees, Cary, NC), it serves family medicine, internal medicine, pediatrics, urgent care, psychiatry/behavioral health, and FQHCs/CHCs. The product bundles:

- **Clinical documentation/charting** with customizable templates (multi-specialty including behavioral health, pediatrics, women's health)
- **E-prescribing** (CPOE certified)
- **Lab integration** (electronic lab interface, Quest Diagnostics integration)
- **Scheduling** (appointments, self-scheduling, self-check-in kiosk)
- **Integrated billing and claims** (auto-populated superbills, claim scrubbing, automated posting, AR management)
- **Revenue cycle management** (full-service RCM offering)
- **Patient portal** (secure messaging, health history, lab results, appointment requests, online payments)
- **Telemedicine** (video visits with documentation)
- **Reporting** (UDS, quality measures, population health)
- **Document management**
- **Referral tracking**
- **Immunization registry reporting** (certified (f)(1))

The product is certified across 38 ONC criteria including (b)(10) for EHI export. Given its integrated billing, practice management, patient portal, and multi-specialty clinical capabilities, a complete EHI export should cover clinical encounters, medications, labs, allergies, diagnoses, immunizations, vitals, billing/claims/payments, insurance, referrals, portal messages, custom forms, and uploaded documents.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Patient_Export_Data_File_Format.pdf` | 4-page PDF (190 KB). The sole substantive documentation. Lists 18 XLSX worksheet names and 8 per-patient file types. No field-level data dictionary. Created Oct 18, 2023 by Lisa Davies. | **Primary source** — but very thin |
| `downloads/kb-article-410.html` | HappyFox KB article page (37 KB HTML). Contains only one sentence: "Please see attached file for Explanation of the File Format for a Single Patient Export and All Patients Export." Last updated Aug 8, 2024. | Minimal — just a wrapper for the PDF |
| `downloads/kb-article-410-screenshot.png` | Browser screenshot of the KB article page (111 KB). Confirms page layout and metadata. | Confirmatory only |

The PDF is the only artifact with substantive content. There are no sample data files, no schemas, no field-level documentation, and no data dictionary of any kind.

## 3. Export Mechanics

ReLiMed provides two export mechanisms:

### Single Patient Export
- **Access**: Self-service via Patient Chart → Patient Export (requires "Medical Record Request" privilege)
- **Format**: Single PDF file containing selected sections
- **Selectable sections**: Encounters, Active Medications, Chronic Problems, Allergies, Documents, eLab Results, Patient Forms, CCD, Claims, Insurance Information, Medical History, Restricted content
- **Limitations**: Output is a non-computable PDF; no structured data export

### All Patient (Bulk) Export
- **Access**: Vendor-assisted — must contact ReLi Med Solutions support team
- **Delivery**: Password-protected ZIP file on vendor SFTP server (dual passwords: one for SFTP, one for ZIP extraction)
- **Format**: Mixed format ZIP containing:
  - `patient-data-export.xlsx` — 18-worksheet Excel workbook with structured tabular data
  - `Medical Records/` folder — per-patient subfolders (by MR number) containing CCD XML/HTML, encounter PDFs, lab result PDFs, uploaded documents, and custom forms (RTF)
- **Constraints**: Not self-service; requires vendor involvement; files available for limited time only

**Notable**: The bulk export is not available on-demand — it requires contacting vendor support, receiving SFTP credentials, and downloading within a time window. No API or automated mechanism exists.

## 4. Export Content: What's In It

### Documentation depth

The entire export documentation is **entity-name level only**. The PDF lists 18 worksheet names and 8 per-patient file types. There is:

- **Zero field-level documentation**: No column names, no data types, no field descriptions for any worksheet
- **Zero sample data**: No example files or records
- **Zero schema**: No machine-readable format specification
- **Zero relationship documentation**: No explanation of how worksheets relate to each other (e.g., foreign keys between Patient Demographics and Patient Medications)
- **Zero value set documentation**: No coded values, no terminology references

### Vendor's own content organization

| Entity/Table | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| Locations | 0 (undocumented) | N/A | N/A | Practice/Administrative |
| License Providers | 0 (undocumented) | N/A | N/A | Practice/Administrative |
| Referring Providers | 0 (undocumented) | N/A | N/A | Practice/Administrative |
| Master Insurances | 0 (undocumented) | N/A | N/A | Practice/Administrative |
| Resources/staff members | 0 (undocumented) | N/A | N/A | Practice/Administrative |
| Patient Employers | 0 (undocumented) | N/A | N/A | Patient Demographics |
| Patient Demographics | 0 (undocumented) | N/A | N/A | Patient Demographics |
| Patient Guarantors | 0 (undocumented) | N/A | N/A | Patient Demographics |
| Patient Contacts | 0 (undocumented) | N/A | N/A | Patient Demographics |
| Patient Pharmacies | 0 (undocumented) | N/A | N/A | Patient Demographics |
| Patient Insurances | 0 (undocumented) | N/A | N/A | Patient Demographics |
| Past Appointments | 0 (undocumented) | N/A | N/A | Scheduling |
| Patient Notes | 0 (undocumented) | N/A | N/A | Clinical |
| Patient Alerts (Billing etc.) | 0 (undocumented) | N/A | N/A | Clinical |
| Patient Medications | 0 (undocumented) | N/A | N/A | Clinical |
| Patient Allergies | 0 (undocumented) | N/A | N/A | Clinical |
| Patient Diagnosis | 0 (undocumented) | N/A | N/A | Clinical |
| Future Appointments | 0 (undocumented) | N/A | N/A | Scheduling |

**Per-patient files** (in Medical Records folder):

| File Type | Format | Description |
|---|---|---|
| CCD.xml | XML | Continuity of Care Document for EMR import |
| CCD.html | HTML | Human-readable CCD |
| Demographics_*_MedicalHistory.pdf | PDF | Demographics and insurance snapshot |
| MedicalHx_*_MedicalHistory.pdf | PDF | Active meds, chronic problems, active allergies |
| Encounter_\<date\>_\<type\>.pdf | PDF | Individual encounter summaries |
| Document_\<type\>_\<name\>.pdf | PDF | Uploaded documents from patient chart |
| LabResult_\<date\>_\<guid\>.pdf | PDF | Electronic lab results |
| Form_\<date\>_\<type\>_\<name\>.rtf | RTF | Custom user forms |

**Summary**: 18 XLSX worksheets + 8 per-patient file types = 26 documented entities. Zero fields documented across all entities. No field-level specification exists anywhere in the available documentation.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the bulk export into two components:

1. **Structured tabular data** (XLSX workbook, 18 worksheets): Covers practice administrative data (5 worksheets: locations, providers, insurances, staff), patient demographics and relationships (6 worksheets: demographics, guarantors, contacts, employers, pharmacies, insurances), scheduling (2 worksheets: past and future appointments), and clinical data (5 worksheets: notes, alerts, medications, allergies, diagnoses).

2. **Per-patient documents** (8 file types): CCD for interoperability, PDF snapshots of demographics/medical history, encounter summaries as PDFs, uploaded documents, lab results as PDFs, and custom forms as RTF.

The **clinical** category (notes, medications, allergies, diagnoses) is present but with zero field-level detail — we cannot assess depth. Encounters and lab results are exported only as rendered PDFs, not structured data. The single-patient export UI shows "Claims" as selectable, but the bulk export documentation has no claims worksheet — a notable discrepancy.

The **thinnest** areas are clinical detail (encounter content locked in PDFs), billing (no dedicated worksheet despite the product having full billing capabilities), and any specialty-specific data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient Demographics`, `Patient Contacts`, `Patient Guarantors`, `Patient Employers` worksheets (no field documentation) | Worksheets exist but without field-level docs, actual content unknown |
| Encounters / visits | ⚠️ Partial | `Encounter_<date>_<type>.pdf` per-patient files; `Patient Notes` worksheet | Encounters exported only as rendered PDFs — not structured data. Notes worksheet is undocumented. |
| Problems / conditions / diagnoses | ⚠️ Partial | `Patient Diagnosis` worksheet | Worksheet exists but zero field documentation |
| Medications / prescriptions | ⚠️ Partial | `Patient Medications` worksheet | Worksheet exists but zero field documentation |
| Allergies | ⚠️ Partial | `Patient Allergies` worksheet | Worksheet exists but zero field documentation |
| Immunizations | ❌ Not covered | No immunization worksheet or file type | Product is certified for immunization registry reporting (f)(1); immunization data exists but is absent from export documentation |
| Vitals | ❌ Not covered | No vitals worksheet; may be embedded in encounter PDFs | Product captures vitals; no dedicated structured export |
| Lab results | ⚠️ Partial | `LabResult_<date>_<guid>.pdf` per-patient files | Lab results exported only as rendered PDFs — no structured data (HL7 results, discrete values) |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-related entities | Product does not appear to have imaging capabilities — likely N/A |
| Procedures | ❌ Not covered | No procedures worksheet | Procedures likely captured in encounters; no dedicated export |
| Clinical notes / documents | ⚠️ Partial | `Patient Notes` worksheet; `Document_<type>_<name>.pdf`; `Encounter_*.pdf` | Notes worksheet undocumented; documents exported as PDFs |
| Care plans / goals | ❌ Not covered | No care plan entities | Product may store care plans; absent from export |
| Orders / referrals | ❌ Not covered | No orders or referral entities | Product has referral tracking; absent from export |
| Insurance / coverage | ⚠️ Partial | `Patient Insurances`, `Master Insurances` worksheets | Worksheets exist but zero field documentation |
| Claims / billing | ❌ Not covered | No billing/claims worksheet in bulk export | **Significant gap**: Product has integrated billing, claim scrubbing, automated posting, and full RCM. Single-patient UI shows "Claims" but bulk export omits it entirely. |
| Payments | ❌ Not covered | No payment entities | Product handles payments and AR management; absent from export |
| Consents / directives | ❌ Not covered | No consent entities | May be captured in custom forms (RTF) but not documented |
| Patient communications / portal messages | ❌ Not covered | No messaging entities | Product has secure messaging via patient portal; absent from export |
| Specialty-specific (behavioral health, pediatrics, women's health) | ❌ Not covered | No specialty-specific entities | Product markets specialty templates for FQHCs; may be embedded in encounter PDFs but no structured export |

**Summary**: Of 17 applicable domains (excluding imaging as N/A), 0 are fully covered with documented fields, 7 are partially covered (entity names exist but no field documentation), and 10 are not covered at all.

## 6. Documentation Quality

The documentation quality is **severely deficient**:

- **Completeness**: The entire specification is 4 pages listing entity names only. Zero of the 18 worksheets have any field-level documentation.
- **Usability**: A developer receiving this export would need to reverse-engineer every worksheet's column structure from the raw XLSX data. The documentation provides no guidance on data types, coded values, relationships between tables, or how to interpret any field.
- **Machine-readability**: No schemas, no sample data, no JSON/XML specifications — only a PDF with prose descriptions and screenshot.
- **Maintenance**: Created October 2023, no version history, no changelog.

A developer could not build an import from this documentation alone. They could determine that they will receive an XLSX with 18 worksheets and a folder of per-patient files, but they would know nothing about the actual data structure, field names, or content format until they receive the actual export file and inspect it.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers core clinical domains (medications, allergies, diagnoses, notes) and demographics through XLSX worksheets, plus encounters and lab results as rendered PDFs. However, it is missing entire data domains that the product stores: billing/claims (despite integrated billing and RCM being a core feature), immunizations (despite certified registry reporting), vitals (as structured data), referrals, patient portal messages, and specialty-specific data. The most conspicuous gap is billing — ReLiMed heavily markets its integrated billing and RCM capabilities, yet the bulk export has no billing worksheet. The single-patient export UI shows "Claims" as selectable, suggesting claims data exists in the system but was excluded from the bulk export specification. Additionally, encounter data and lab results are locked in non-computable PDF format rather than structured data, limiting their utility.

**Axis 2 — Export approach: Purpose-built EHI export**

This is not a repackaged (g)(10) FHIR export or C-CDA relabel. The vendor built a custom export mechanism: an XLSX workbook with 18 product-specific worksheets plus a per-patient document folder. The CCD XML files are included as one component alongside the proprietary structured data — they are supplementary, not the primary export. The export structure reflects the vendor's own data model (Patient Demographics, Patient Guarantors, Patient Alerts, etc.) rather than mapping to USCDI or FHIR resource types. This is a genuine (b)(10) effort, though the execution is incomplete.

### Key Findings

1. **Zero field-level documentation**: The most critical deficiency. Across 18 XLSX worksheets, not a single column name, data type, or field description is documented. The entire "data dictionary" is a list of worksheet names. (Source: `Patient_Export_Data_File_Format.pdf`, pages 2-3)

2. **Billing data absent from bulk export despite being a core product feature**: The product's integrated billing, claims, and RCM capabilities are prominent in marketing, yet the bulk export has no billing or claims worksheet. The single-patient export UI shows "Claims" as a selectable section, suggesting the data exists but was excluded from bulk export specification. (Source: `Patient_Export_Data_File_Format.pdf`, pages 1 and 2-3)

3. **Clinical encounter data locked in PDFs**: Encounter summaries and lab results are exported only as rendered PDFs — non-computable, non-importable into another system as structured data. The XLSX contains a "Patient Notes" worksheet, but its content is undocumented. (Source: `Patient_Export_Data_File_Format.pdf`, pages 3-4)

4. **Bulk export is not self-service**: The all-patient export requires contacting vendor support, who generate a ZIP file on an SFTP server with a time-limited download window. Only the single-patient export (which produces only a PDF) is self-service. (Source: `Patient_Export_Data_File_Format.pdf`, page 2)

5. **Multiple clinical domains missing**: Immunizations, vitals (structured), procedures, referrals, care plans, portal messages, and specialty-specific data are absent from the export documentation despite being capabilities of the product.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   XLSX + PDF + RTF + CCD XML (mixed, in ZIP)
    Entities:        26 (18 XLSX worksheets + 8 per-patient file types)
    Fields:          N/A (zero field-level documentation)
    Descriptions:    N/A (0% — no fields documented at all)
    Sample data:     No
    Bulk export:     Yes (vendor-assisted only)
    Domains covered: 7 of 17 applicable domains (partial coverage only; 0 fully documented)

### Bottom Line

ReLiMed built a purpose-built EHI export that goes beyond USCDI/C-CDA repackaging, with a custom XLSX workbook covering core clinical and demographic data. However, the export has two critical deficiencies: (1) there is literally zero field-level documentation — a recipient gets worksheet names but no column definitions, data types, or relationships — and (2) entire data domains the product stores (billing/claims, immunizations, vitals, referrals, portal messages) are absent from the export. The biggest gap is billing data, which is a core capability of the product but is not included in the bulk export despite appearing in the single-patient export UI.
