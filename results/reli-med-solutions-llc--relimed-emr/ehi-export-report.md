# ReLi Med Solutions, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://relimed.happyfox.com/kb/article/410-explanation-of-file-format-for-patient-export-cures-170-315-b-10/
- CHPL IDs: 11024
- Product: ReLiMed EMR, Version 7.3
- Certification date: 2022-11-18

## Navigation Journal

1. **Initial probe**: `curl -sI -L` returned HTTP 405 (HEAD not allowed on HappyFox KB). Switched to GET.

2. **Fetched the page**:
   ```bash
   curl -sL "https://relimed.happyfox.com/kb/article/410-explanation-of-file-format-for-patient-export-cures-170-315-b-10/" \
     -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
     -o kb-article-410.html
   ```
   Page loaded successfully (37 KB HTML). Title: "Explanation of File Format For Patient Export: CURES 170.315 (b)(10)". Author: Lisa Davies (COO of ReLi Med). Last updated: Aug 08, 2024. Views: 2,346. Category: "Certifications & Attestations". Tags: patient charts, Read only, b 10, CURES, 170.315(b)(10) Electronic Health Information export, Export.

3. **Article body**: Minimal — just one sentence: "Please see attached file for Explanation of the File Format for a Single Patient Export and All Patients Export". The substance is entirely in the attached PDF.

4. **Downloaded the PDF attachment**:
   ```bash
   curl -sL "https://hf-files-oregon.s3.amazonaws.com/hdprelimed_kb_attachments/2023/10-18/b1891224-a7cc-4e26-a531-433712c1d9cc/Patient_Export_Data_File_Format.pdf" \
     -H 'User-Agent: Mozilla/5.0' \
     -o Patient_Export_Data_File_Format.pdf
   ```
   Confirmed: PDF document, 4 pages, 189,921 bytes. Created Oct 18, 2023 by Lisa Davies using Microsoft Word for Microsoft 365.

5. **Checked for related articles**: The "Export" tag (3 articles) led to:
   - Article 531: "Medical Record Request (CCDA) Help Document" — describes the CCDA export process (transitions of care, not b(10)-specific). Contains screenshots of the Admin → Medical Records Request (CCD) screen. No additional file attachments.
   - Article 107: "Front Desk: Exporting Medical Records / Referrals Export" — a 2-minute YouTube training video (https://www.youtube.com/watch?v=Gf6rF0CSA04) showing the single-patient export UI. No additional documentation.
   - Neither article adds substantive information about the (b)(10) export format beyond what's in the PDF.

6. **Checked the parent section** (section 21): Only contains article 410.

7. **Checked vendor certification page** (https://relimedsolutions.com/certification/): General compliance/marketing page. No additional EHI export documentation or data dictionaries found.

8. **Took a full-page screenshot** of article 410 in a browser for the archive.

## What Was Found

The entire EHI export documentation consists of a single 4-page PDF titled "Patient Export File Format." The document describes two export mechanisms:

### Single Patient Export

- **Access**: Patient Chart → Patient Export menu option (requires "Medical Record Request" privilege)
- **User interface**: An "Export Patient Data Selection" dialog with checkboxes for data sections. The screenshot in the PDF shows these selectable categories:
  - Encounters (with count columns A and S)
  - Active Medications
  - Chronic Problems
  - Allergies
  - Documents
  - eLab Results
  - Patient Forms
  - CCD
  - Claims
  - Insurance (Include Insurance Information checkbox)
  - Medical History (Include Active Allergies, Include Active Medications, Include Chronic Problems checkboxes)
  - Restricted (Include Encounter Types, Include Document Types)
  - Date range filter (From Date / To Date)
  - Additional Notes / Additional Files tabs
- **Output format**: A single PDF file containing all selected health information sections. User can Save, Print, or Fax.

### All Patient Export (Bulk)

- **Access**: Provided by ReLi Med Solutions support team upon request — not a self-service feature
- **Delivery method**: Password-protected ZIP file placed on ReLi Med's SFTP server. Practice contact receives SFTP host/port/username plus instructions for separate passwords (SFTP vs ZIP passwords are different for HIPAA compliance separation).
- **Output structure**: The ZIP file contains:

  **`patient-data-export.xlsx`** — An Excel workbook with these worksheets:
  | Worksheet | Content |
  |-----------|---------|
  | Locations | Practice location data |
  | License Providers | Licensed provider information |
  | Referring Providers | Referring provider information |
  | Master Insurances | Insurance plan definitions |
  | Resources/staff members | Staff/resource data |
  | Patient Employers | Employer information |
  | Patient Demographics | Patient demographic data |
  | Patient Guarantors | Guarantor information |
  | Patient Contacts | Contact persons |
  | Patient Pharmacies | Pharmacy preferences |
  | Patient Insurances | Patient-specific insurance |
  | Past Appointments | Historical appointments |
  | Patient Notes | Clinical notes |
  | Patient Alerts (Billing etc.) | Billing and other alerts |
  | Patient Medications | Medication records |
  | Patient Allergies | Allergy records |
  | Patient Diagnosis | Diagnosis records |
  | Future Appointments | Scheduled future appointments |

  **`Medical Records/` folder** — Sub-folders per patient (organized by MR Number), containing:
  | File Pattern | Format | Content |
  |-------------|--------|---------|
  | `CCD.xml` | XML | Continuity of Care Document — for EMR import |
  | `CCD.html` | HTML | Human-readable CCD |
  | `Demographics_*_MedicalHistory.pdf` | PDF | Demographics and insurance snapshot |
  | `MedicalHx_*_MedicalHistory.pdf` | PDF | Active meds, chronic problems, active allergies |
  | `Encounter_<date>_<time>_<type>.pdf` | PDF | Individual encounter summaries |
  | `Document_<type>_<name>.pdf` | PDF | Uploaded documents from patient chart |
  | `LabResult_<date>_<time>_<guid>.pdf` | PDF | Electronic lab results |
  | `Form_<date>_<time>_<type>_<name>.rtf` | RTF | Custom user forms |

## Export Coverage Assessment

### Data Domain Coverage

Based on the product research, ReLiMed EMR stores clinical encounters, medications, lab results, allergies, diagnoses, immunizations, scheduling, billing/claims, patient portal data, telemedicine records, referrals, documents, and specialty-specific templates (behavioral health, pediatrics, women's health for FQHCs).

**Domains clearly covered in the export:**
- Patient demographics, contacts, guarantors, employers
- Insurance information (both master plans and patient-specific)
- Provider data (licensed and referring)
- Medications
- Allergies
- Diagnoses
- Encounter summaries (as PDFs)
- Lab results (as PDFs)
- Documents uploaded to charts
- Custom forms (as RTF files)
- CCD/CCDA (clinical summary)
- Appointments (past and future)
- Patient notes
- Patient alerts (billing and other)
- Claims (visible in single-patient export UI)

**Domains with unclear or missing coverage:**
- **Billing/financial detail**: The single-patient export UI shows "Claims" as a selectable category, but the bulk export (patient-data-export.xlsx) does not list a Claims worksheet. The documentation doesn't describe what claim data fields are included, or whether charges, payments, adjustments, denial data, and AR information are exported. For a product that prominently features integrated billing and RCM, this is a notable gap in documentation.
- **Immunization records**: Not explicitly mentioned in either export path. The product is certified for immunization registry reporting (f)(1), so immunization data exists in the system, but the export documentation doesn't list an immunization-specific worksheet or file type.
- **Vitals/clinical observations**: Not explicitly listed. Likely contained within encounter PDFs, but discrete vitals data (structured, queryable) doesn't appear to be exported separately.
- **Referral data**: Not mentioned in the export documentation despite referral tracking being a documented product feature.
- **Care plans/goals**: Not mentioned.
- **Telemedicine-specific data**: Not specifically mentioned, though telehealth encounters presumably appear as encounter PDFs.
- **Patient portal messages**: Secure messaging between patients and providers is a product feature, but portal messages are not listed in the export.
- **Behavioral health and specialty-specific data**: The product markets specialty templates for behavioral health, pediatrics, and women's health (especially for FQHCs). These likely appear within encounter PDFs, but there's no documentation of how specialty-specific structured data is exported.

### Export Format & Standards

The export uses a **proprietary, mixed-format approach**:
- **XLSX workbook** for structured tabular data (demographics, medications, allergies, diagnoses, etc.) — 18 worksheets
- **CCD/CCDA XML** for clinical summary (standard interoperable format)
- **PDF files** for encounter notes, lab results, demographics summaries, and uploaded documents
- **RTF files** for custom forms

This is a reasonable approach for a small ambulatory EHR. The XLSX workbook provides queryable structured data for the core clinical and administrative domains. The CCD provides a standards-based clinical summary. PDFs preserve the visual layout of clinical documents.

However, there is a significant limitation: **encounter data is exported only as rendered PDFs**, not as structured data. This means the clinical content of visits — HPI, exam findings, assessment, plan, orders — is locked in a non-computable format. A third party receiving this export could read the encounter notes but could not programmatically extract structured data from them. The same applies to lab results (PDF rather than structured HL7/FHIR results).

The single-patient export produces only a PDF, which is even more limited — it's a non-computable document with no structured data at all.

### Documentation Quality

The documentation is **minimal**. The entire EHI export specification is a 4-page PDF containing:
- Brief instructions for accessing each export path
- Screenshots of the single-patient export UI
- A list of XLSX worksheet names (no field definitions)
- A list of per-patient file types with one-sentence descriptions
- Instructions for SFTP download and ZIP password retrieval

**Critical gaps:**
- **No data dictionary**: The worksheet names are listed but there is no documentation of column names, data types, value sets, or field descriptions for any of the 18 worksheets in `patient-data-export.xlsx`.
- **No schema or sample data**: No example XLSX, no sample CCD, no field-level specification.
- **No coded value documentation**: No documentation of what codes or value sets are used for diagnoses, medications, allergies, etc.
- **No relationship documentation**: No explanation of how entities relate across worksheets (e.g., how Patient Demographics rows link to Patient Medications rows).
- **No versioning**: No version number, change history, or documentation of format evolution.

A developer receiving an export file would need to reverse-engineer the column structure entirely from the data itself. The documentation tells you that a worksheet called "Patient Medications" exists, but not what columns it contains, what format medication names take, whether NDC codes are included, or how medications link to patients.

### Structure & Completeness

- **Granularity**: Worksheet-name level only. No field-level documentation whatsoever.
- **Value sets**: Not documented.
- **Relationships**: Not documented.
- **Export trigger**: The bulk export is not self-service — it requires contacting ReLi Med support. The single-patient export is self-service but produces only a PDF.

### (b)(10) vs (g)(10) Assessment

This is **not** a case of (g)(10) FHIR API being repackaged as (b)(10). The export is genuinely a custom bulk data export (XLSX + per-patient files), distinct from any FHIR API. The CCD.xml files included per-patient are a standard interoperability artifact, but the core structured data export is in the proprietary XLSX format. This is a legitimate (b)(10) approach.

### Overall Assessment

ReLi Med has built a functional EHI export mechanism that goes beyond the minimum — the bulk export includes structured tabular data (XLSX) alongside document-format records (PDFs), and it covers the core clinical domains. However, the **documentation is severely inadequate**. There is essentially no data dictionary. The documentation tells you *what kinds of files you get* but not *what data is in them*. For a compliance requirement specifically about providing electronic health information in an export format, the lack of any field-level specification means recipients cannot meaningfully interpret or import the data without significant reverse engineering.

The vendor appears to have built the export feature itself competently (the export UI in the screenshots looks well-organized with clear category selection), but treated the documentation as an afterthought — a 4-page PDF with file listings rather than a comprehensive format specification.

## Access Summary
- Final URL (after redirects): https://relimed.happyfox.com/kb/article/410-explanation-of-file-format-for-patient-export-cures-170-315-b-10/
- Status: found
- Required browser: no (curl works for page and PDF download)
- Navigation complexity: direct_link (PDF is linked directly from the article as an attachment)
- Anti-bot issues: HEAD method returns 405 (use GET instead); Cloudflare in front but no challenge for standard User-Agent

## Obstacles & Dead Ends
- HEAD requests return HTTP 405 from HappyFox KB — use GET
- Tag pages (e.g., `/kb/tag/export/`) work differently from the URL patterns shown in the page source — `/kb/tag/299` works, `/kb/tag/export/` returns 404
- Articles 531 and 107 (related by "Export" tag) contain supplementary context about CCDA export and patient chart export UI but no additional (b)(10) documentation
- The vendor certification page (relimedsolutions.com/certification/) contains no EHI export technical content
