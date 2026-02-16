# AdvancedMD — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://www.advancedmd.com/medical-office-software/data-export/
- CHPL IDs: 11732 (AdvancedMD v25), 11734 (AdvancedMD Mobile v8)
- Certification dates: 2025-12-15, 2025-12-18

## Navigation Journal

### Step 1: Initial probe
```bash
curl -sI -L "https://www.advancedmd.com/medical-office-software/data-export/" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 200, Content-Type: text/html; charset=UTF-8. WordPress site on WP Engine behind Cloudflare. No redirects.

### Step 2: Fetch and examine page
```bash
curl -sL "https://www.advancedmd.com/medical-office-software/data-export/" \
  -H 'User-Agent: Mozilla/5.0' -o data-export-page.html
```
Page is 279 KB of HTML. Text extraction from raw HTML was blank — the page content is rendered via JavaScript/WordPress Bricks builder, but the actual text content is present in the HTML source within structured elements.

### Step 3: Browser navigation
Navigated to the URL in Chrome. Page title: "Secure Data Export & Retrieval Services | AdvancedMD". The page loaded fully with all content visible — no accordion clicks or extra navigation needed. Took full-page screenshot.

The page is well-organized with two main sections:

**Single Patient Export Options:**
1. Patient Transaction Report (CSV)
2. Patient Visit Summary Report (CSV)
3. EHR Data Portability Export Tool (C-CDA XML)
4. EHR Patient Chart Print Tool (PDF)

**Bulk Patient Export Options:**
1. Practice Management Data Export (Microsoft Access .mdb)
2. Scanned Documents & Images (folder structure with native files)
3. EHR Bulk Data Export (SQL Server .bak file)

### Step 4: Download linked documents
Four PDF links found on the page:

1. **AdvancedMD Data Export C-CDA/HTML Data Dictionary** (uid=1_69)
   ```bash
   curl -sL -H 'User-Agent: Mozilla/5.0' \
     "https://info.advancedmd.com/rs/332-PCG-555/images/advancedmd-dataExport-dataDictionary.pdf" \
     -o advancedmd-dataExport-dataDictionary.pdf
   ```
   Verified: PDF document, 6 pages, 452 KB.

2. **AdvancedMD Bulk Data Export Data Dictionary** (uid=1_95)
   ```bash
   curl -sL -H 'User-Agent: Mozilla/5.0' \
     "https://info.advancedmd.com/rs/332-PCG-555/images/advancedmd-ehrExport-dataDictionary.pdf" \
     -o advancedmd-ehrExport-dataDictionary.pdf
   ```
   Verified: PDF document, 13 pages, 825 KB.

3. **AdvancedMD Bulk Data Export Scanned Doc/Images Guidance** (uid=1_97)
   ```bash
   curl -sL -H 'User-Agent: Mozilla/5.0' \
     "https://info.advancedmd.com/rs/332-PCG-555/images/advancedmd-bulkDataExport-scannedDocsImages.pdf" \
     -o advancedmd-bulkDataExport-scannedDocsImages.pdf
   ```
   Verified: PDF document, 9 pages, 2.1 MB.

4. **Data Export & Retrieval Services Desk Guide** (uid=1_76, "DOWNLOAD DESK GUIDE")
   ```bash
   curl -sL -H 'User-Agent: Mozilla/5.0' \
     "https://info.advancedmd.com/rs/332-PCG-555/images/advancedmd-flyer-dataExport.pdf" \
     -o advancedmd-flyer-dataExport.pdf
   ```
   Verified: PDF document, 2 pages, 35 KB.

One additional link on the page points to the HL7 C-CDA Implementation Guide at hl7.org — this is an external standard and was not downloaded per instructions.

All PDFs were created on 2023-12-05 by author "aknox" (Angela Knox, the developer contact listed in CHPL metadata), produced via "Microsoft: Print To PDF" (data dictionaries) or "Adobe InDesign 19.0" (flyer).

## What Was Found

AdvancedMD provides **genuinely comprehensive EHI export documentation** that goes well beyond what many vendors offer. The documentation describes multiple complementary export mechanisms covering different data domains, each with its own format and delivery method.

### Export Mechanisms

#### 1. Single Patient — Patient Transaction Report (CSV)
Exports billing/financial data for a single patient from Practice Management. Header includes patient demographics and insurance info. Body includes transaction types, visit details, charge codes, diagnosis codes, payments, and adjustments. User-accessible: Reports > Patient Listings > Patient Transaction Report.

#### 2. Single Patient — Patient Visit Summary Report (CSV)
Another PM report with visit-level data: service dates, charge codes, CPT codes, diagnosis codes, facility, carrier, provider info, and appointment data. User-accessible: Reports > Patient Listings > Patient Visit Summary.

#### 3. Single Patient — EHR Data Portability Export Tool (C-CDA XML + HTML)
Exports USCDIv1 clinical data as a C-CDA document. Covers: allergies, medications, problems, procedures, results, medical equipment, vital signs, assessments, plan of treatment, goals, health concerns, clinical notes (consultation, H&P, progress, discharge, imaging narrative, pathology narrative), immunizations, reason for referral, functional status, mental status, encounters, social history, care team, advance directives. User-accessible: EHR > Tools > Data Portability Export Tool.

#### 4. Single Patient — EHR Patient Chart Print Tool (PDF)
Exports a printable PDF of the patient chart. Can include: demographics, insurance, allergies, problems, immunization history, risk factors, advanced directives, misc info, audit trail, messages, annotations, healthwatcher items, education lists, patient portal/staff messages, current/historical medications, orders/tests, appointments, scanned documents, results, and patient notes. User-accessible from Chart Print icon.

#### 5. Bulk — Practice Management Data Export (Microsoft Access .mdb)
Exports PM data as a Microsoft Access database file. Always includes demographics; optionally includes transactions and appointment data. Covers: charges, payments, write-offs, patient demographics, provider info, appointments, and carrier information. User-accessible: Utilities > Data Export.

#### 6. Bulk — Scanned Documents & Images (folder structure)
Exports all scanned documents and images from both PM and EHR. Delivered as a hierarchical folder structure organized by date (YYYY/MM/DD), with index files (PM.Export.XXXXXX for PM docs, EHR.docmap.Export.XXXXXX for EHR docs) mapping each file to its patient, document type, and category. Files are in their native format (JPG, DOC, etc.). **Requires developer assistance** — contact Client Support Services.

#### 7. Bulk — EHR Bulk Data Export (SQL Server .bak file)
The most comprehensive clinical export. Delivered as a SQL Server database backup file (.bak) that must be restored in SQL Server Management Studio. Contains **all discrete clinical data** from the EHR.

### EHR Bulk Export Data Dictionary (13 pages)

The data dictionary documents the following SQL tables with column-level descriptions:

| Table | Content | Column Count |
|-------|---------|-------------|
| EHR_Allergies | Patient allergies with names, reactions, treatments, status | 14 columns |
| EHR_Immunizations | Immunization records with vaccine details, dosage, route, VFC eligibility, manufacturer, MVX/CVX codes | 30+ columns |
| EHR_Messages | Patient messages with sender/recipient, priority, action type | 20+ columns |
| EHR_PatientNoteDiagnosis | Diagnosis codes linked to clinical notes | 6 columns |
| EHR_Problems | Problem list with onset/updated dates, diagnosis codes, status | 18 columns |
| EHR_Prescriptions | Comprehensive prescription data including drug details, DEA class, pharmacy info, e-prescribing status, Surescripts integration fields | 50+ columns |
| EHR_LabResults | Lab results with ordering physician, result status, patient demographics | 30+ columns |
| EHR_ResultItems | Individual lab result line items | 11 columns |
| EHR_ResultSets | Lab result set groupings | 15+ columns |
| EHR_ResultValues | Lab result values with units, ranges, abnormal flags | 20+ columns |
| EHR_PatientNotes | Clinical note data with template fields, coordinates, control types, selected values, images | 30+ columns |
| EHR_WordMerge | Word Merge templates stored as blobs convertible to Word documents | 3 columns |

The dictionary also includes SQL JOIN syntax for assembling lab results from the four related tables (EHR_LabResults, EHR_ResultSets, EHR_ResultItems, EHR_ResultValues).

A detailed explanation of the EHR_PatientNotes structure describes how clinical notes are stored as individual field-level rows rather than assembled documents. Each row has positioning coordinates (Left_Loc, Top_Loc) and template references. The EHR_WordMerge table contains the templates as binary blobs that can be converted to Word documents. Variable substitution is documented: `<<field_name>>` placeholders in templates are replaced with `selected_value` from the PatientNotes table.

Pages 11-13 provide a detailed walkthrough of how radio button selections generate multiple rows in EHR_PatientNotes, with parent/child control ordinal relationships explained through an annotated example using a genitourinary exam.

### C-CDA Data Dictionary (6 pages)

Documents the C-CDA export field mappings with columns for: Field Name, Information on Field, Vocabulary Code, and Required Text in Optional Description. Covers all USCDIv1 sections with specific LOINC/SNOMED codes for each section header.

### Scanned Documents & Images Guidance (9 pages)

Step-by-step visual guide with annotated screenshots showing:
- **PM Documents**: Folder hierarchy (PM.Export.XXXXXX > decrypted-pm > FileType > FileLocation > FileName). Index file structure with columns: FirstName, LastName, ChartNumber, ProfileCode, CategoryName, FileLocation, FileName.
- **EHR Documents**: Folder hierarchy (EHR.docmap.Export.XXXXXX > decrypted-ehr > EHR > Year > Month > Day > document). Index file maps File_Key_Ptr to Document_UID. Includes notes about preview files, lab result files with no patient (ID=1), and file extension mismatches between index and actual files.
- Also includes 2 CSV files for EHR blob data and PM templates.

The guide references a sample export zip file ("EHR Export Sample Data.zip") shown in screenshots containing: decrypted-pm, decrypted-ehr, PM.Export.992054.txt, EHR.PTDrug.Export.992054.txt, EHR.Export.992054.txt, EHR.docmap.Export.992054.txt, and 992065SQL.bak.

### Desk Guide Flyer (2 pages)

A formatted one-pager summarizing all export options with brief descriptions and navigation paths. Essentially a condensed version of the web page content. References the same linked documents.

## Export Coverage Assessment

### Data Domain Coverage

AdvancedMD's export documentation describes a **multi-mechanism approach** that, taken together, covers the vast majority of data domains the product stores. This is notably better than many vendors who offer only a FHIR-based or C-CDA-based export.

**Clearly covered domains:**
- **Clinical notes**: Comprehensive via EHR Bulk Export (EHR_PatientNotes with templates)
- **Allergies**: Both C-CDA and EHR Bulk Export (EHR_Allergies table)
- **Medications/Prescriptions**: Very detailed — 50+ columns including DEA class, Surescripts e-prescribing data, pharmacy info, drug interactions
- **Problems/Diagnoses**: Both C-CDA and EHR Bulk Export (EHR_Problems, EHR_PatientNoteDiagnosis)
- **Lab results**: Detailed 4-table structure (Results, ResultSets, ResultItems, ResultValues) with JOIN documentation
- **Immunizations**: Comprehensive (30+ columns including VFC, MVX/CVX codes, route, manufacturer)
- **Vital signs**: Via C-CDA export (LOINC-coded: BMI, BP, height, weight, heart rate, temp, O2, resp rate, pediatric measures)
- **Encounters**: Via C-CDA and PM reports
- **Care plans, goals, assessments**: Via C-CDA export
- **Clinical messages**: EHR_Messages table in bulk export
- **Scanned documents and images**: Comprehensive with index files mapping to patients
- **Billing/financial data**: Patient Transaction Report and PM Data Export cover charges, payments, adjustments, claims, write-offs, insurance info
- **Demographics**: Multiple exports include demographics
- **Insurance info**: Included in PM exports and Patient Transaction Report header
- **Appointments**: Available in PM Data Export (optional) and Patient Visit Summary
- **Care team**: Via C-CDA export
- **Advance directives**: Via C-CDA and Chart Print
- **Functional/mental status**: Via C-CDA export
- **Social history**: Via C-CDA export
- **Word Merge templates**: Exported as binary blobs with documented reconstruction process
- **E-prescribing/EPCS data**: Rich Surescripts integration fields in EHR_Prescriptions

**Domains with limited or unclear coverage:**
- **Orders (non-lab)**: The web page mentions "Orders/Tests" in the Chart Print tool, but the EHR Bulk Export data dictionary doesn't document a separate orders table. Lab orders are covered via EHR_LabResults, but imaging orders, referral orders, and other non-lab orders may not be discretely exported in the SQL backup.
- **Referrals**: Mentioned in C-CDA ("Reason for Referral") but not as a discrete table in the bulk export.
- **Patient portal messages**: The Chart Print tool includes "Patient Portal and Staff Messages" but these don't appear in the EHR Bulk Export data dictionary as a separate entity from EHR_Messages.
- **Telehealth session data**: Not mentioned in any export documentation despite AdvancedMD offering integrated telehealth.
- **Patient self-scheduling/engagement data**: Not explicitly documented.
- **Document management metadata**: While scanned documents are exported, metadata like fax transmission records or e-signature data aren't separately documented.

**Domains that appear genuinely missing:**
- **Claims data**: The PM Data Export includes charges, payments, and write-offs but there's no mention of claim-level data (submission dates, clearinghouse responses, denial reasons, ERA details). The Patient Transaction Report includes transaction-level billing but not claim lifecycle data.
- **Insurance eligibility verification results**: Not mentioned in any export.
- **Population health/MIPS reporting data**: Not included in exports (though this may be aggregated data and not EHI).

### Export Format & Standards

AdvancedMD uses **multiple proprietary formats** rather than a single standardized export:

- **C-CDA XML**: Used for single-patient clinical summaries. Standard format, covers USCDIv1 data.
- **CSV**: Used for PM billing/visit reports. Simple, portable format.
- **Microsoft Access (.mdb)**: Used for PM bulk data export. Widely readable but dated format.
- **SQL Server backup (.bak)**: Used for EHR bulk clinical data. Requires SQL Server Management Studio to restore — this is a significant barrier. The vendor acknowledges this: "you'd need an IT/conversion person or team to restore the database."
- **Native file formats**: Scanned docs exported in original formats (JPG, DOC, etc.) with text index files.

The SQL Server .bak format is the most concerning from an accessibility standpoint. While it provides the most complete data, it requires commercial Microsoft software (SQL Server) or compatible tools to access. This creates a practical barrier to data portability, though the data itself is comprehensive once you can open it.

**Could a third party reconstruct the patient record?** Mostly yes, with significant effort. The data dictionary provides column descriptions and JOIN syntax. The clinical note reconstruction process is documented but complex — reassembling notes from individual field rows using coordinates and WordMerge templates requires understanding the parent/child ordinal system. The vendor candidly acknowledges this complexity: "we just give the dump of raw data so that it can be manipulated in any way needed."

### Documentation Quality

**Strengths:**
- The documentation is **substantive and practical**. It explains not just what fields exist but how to interpret and use them.
- The EHR Bulk Export Data Dictionary includes real SQL JOIN examples and detailed explanations of complex structures (like the note template system).
- The Scanned Documents guide is thoroughly illustrated with step-by-step screenshots.
- The vendor is transparent about limitations (complex note structure, needing IT assistance for bulk exports).
- Each export option has clear navigation instructions within the product UI.

**Weaknesses:**
- The PDFs are "Print to PDF" exports from Excel/Word with no embedded text layer (image-only), making them non-searchable and non-machine-readable.
- The data dictionary lacks data type specifications for columns — you get column names and brief descriptions but not SQL types, sizes, or nullability.
- No sample data files are downloadable (the screenshots reference an "EHR Export Sample Data.zip" but it's not linked from the public page).
- Value sets for coded fields are not documented — fields like "AllergyStatus", "ProblemStatus", "PrescriptionType" have no enumeration of valid values.
- No versioning or change history on the documentation.
- All documents were last updated 2023-12-05, over two years ago.

### Structure & Completeness

**Granularity:** Table names and column names with brief descriptions. No data types, constraints, cardinality, or foreign key documentation beyond the lab results JOIN example.

**Coded fields:** Not documented with value sets. Many columns that are clearly coded (e.g., AllergyStatus, ProblemStatus, PrescriptionType, Control_Type, Field_Data_Type) have no enumeration.

**Relationships:** Only the lab results 4-table join is explicitly documented. The PatientNotes parent/child ordinal system is explained narratively but not as a formal schema relationship. The connection between EHR_PatientNotes.Template_Name and EHR_WordMerge.Template_Name is mentioned but not formalized.

**Overall assessment:** AdvancedMD has made a genuine, good-faith effort at (b)(10) compliance. Unlike many vendors who simply point to their FHIR/g(10) API, AdvancedMD provides **actual database-level exports** of clinical data (SQL Server backup), billing data (Access database), and documents (native files with indexes). The approach covers far more data than a USCDI-only export would. The multi-mechanism design (C-CDA for standard clinical summaries, SQL for raw EHR data, Access for PM data, folder exports for documents) reflects the real complexity of the data they store.

The main gaps are: (1) the lack of machine-readable documentation formats, (2) missing data type and value set documentation, (3) the practical barrier of requiring SQL Server to access the most complete export, and (4) some data domains (claims lifecycle, eligibility verifications, telehealth) that aren't clearly covered. The documentation would benefit from a structured data dictionary in CSV or JSON format with full type information.

## Access Summary
- Final URL (after redirects): https://www.advancedmd.com/medical-office-software/data-export/
- Status: found
- Required browser: no (PDFs downloadable via curl; page content visible in HTML source but browser recommended for readability)
- Navigation complexity: direct_link (all documentation linked directly from the registered URL)
- Anti-bot issues: none (Cloudflare present but no blocking)

## Obstacles & Dead Ends
- The PDFs are image-only (Print to PDF from Word/Excel) — pdftotext extracts no text. Content was examined by rendering pages as images.
- The Scanned Documents guidance references a sample export zip file ("EHR Export Sample Data.zip") visible in screenshots but not available for public download.
- The page includes a link to the HL7 C-CDA Implementation Guide (external standard, not downloaded).
- A chat widget (Drift) loads on the page but doesn't contain documentation content.
