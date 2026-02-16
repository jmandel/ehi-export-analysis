# Indian Health Service — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://www.ihs.gov/rpms/applications/ftp/?parent=&fld=EHI_Schemas
- CHPL ID: 11717
- Product: Resource and Patient Management System Electronic Health Record (BCERv9.0)
- Certification date: 2025-11-24
- Developer: Indian Health Service (IHS), Office of Information Technology

## Navigation Journal

**Step 1: Probe the URL**
```bash
curl -sI -L "https://www.ihs.gov/rpms/applications/ftp/?parent=&fld=EHI_Schemas" \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
```
Result: HTTP 200, Content-Type: text/html. The page is a file browser (IHS FTP file listing application) showing the `EHI_Schemas` folder contents.

**Step 2: Fetch and examine the page**
```bash
curl -sL "https://www.ihs.gov/rpms/applications/ftp/?parent=&fld=EHI_Schemas" \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/ihs-page.html
```
The page is an HTML file browser (99 KB, mostly Mura CMS template and JavaScript). The file listing table contains 4 files with download links. The page also has a login/registration section but the files are publicly downloadable without authentication.

**Step 3: Download all 4 files**
```bash
# Schema definition PDF
curl -sL "https://www.ihs.gov/rpms/applications/ftp/?p=rpms%5CEHI_Schemas%5CIHS_EHI_Schema_Definition.pdf&flname=IHS_EHI_Schema_Definition.pdf&download=1" \
  -H 'User-Agent: Mozilla/5.0' -o IHS_EHI_Schema_Definition.pdf

# 2023 schema
curl -sL "https://www.ihs.gov/rpms/applications/ftp/?p=rpms%5CEHI_Schemas%5CBREH_OIT_20230607.txt&flname=BREH_OIT_20230607.txt&download=1" \
  -H 'User-Agent: Mozilla/5.0' -o BREH_OIT_20230607.txt

# 2024 schema
curl -sL "https://www.ihs.gov/rpms/applications/ftp/?p=rpms%5CEHI_Schemas%5CBREH_OIT_20240703.txt&flname=BREH_OIT_20240703.txt&download=1" \
  -H 'User-Agent: Mozilla/5.0' -o BREH_OIT_20240703.txt

# 2025 schema
curl -sL "https://www.ihs.gov/rpms/applications/ftp/?p=rpms%5CEHI_Schemas%5CBREH_OIT_20250714.txt&flname=BREH_OIT_20250714.txt&download=1" \
  -H 'User-Agent: Mozilla/5.0' -o BREH_OIT_20250714.txt
```

All files verified: PDF is a valid PDF document (241 KB, 7 pages), and all three `.txt` files are valid JSON (5.4–5.5 MB each).

**Step 4: Check for additional documentation**
Checked the FTP root (`/rpms/applications/ftp/`) and the certification overview page (`/promotinginteroperability/certificationoverview/`) for additional EHI-related documentation. No additional EHI export documents were found beyond the 4 files in the `EHI_Schemas` folder. The PDF itself references only the IHS IT support contact page.

## What Was Found

### Overview

IHS has built a dedicated EHI export package called **BREH (RPMS Electronic Health Information Export)** that generates patient-level exports in JSON format using a predefined national schema. This is a genuine (b)(10) implementation — not a repackaged FHIR API.

### Documentation Set

1. **IHS_EHI_Schema_Definition.pdf** (241 KB, 7 pages, September 2023): A brief user manual explaining the BREH package. Key points:
   - The BREH package allows authorized users to manually generate an EHI export for a single patient or a patient population
   - Exports are generated using a **predefined national schema** published on the IHS website (the `.txt` files)
   - Sites can also create **custom schemas** based on the national schema
   - Export format is **JSON**
   - "All EHI information is available in an EHI export, with the exception of images. Imaging links/data are presented but not the images themselves"
   - The PDF correctly defines EHI per 45 CFR 171.102 and excludes psychotherapy notes and litigation compilations

2. **BREH_OIT_20230607.txt** (5.6 MB, June 2023): Initial national schema — 296 patient files, ~8,221 field definitions
3. **BREH_OIT_20240703.txt** (5.7 MB, July 2024): Updated schema — 298 patient files, ~8,274 field definitions
4. **BREH_OIT_20250714.txt** (5.8 MB, July 2025): Latest schema — 301 patient files, ~8,415 field definitions, 548 pointer/reference files

### Schema Structure

Each schema file is a single JSON object with the following top-level keys:
- `SCHEMA NAME`: Version identifier (e.g., "BREH_OIT_20250714")
- `VERSION STATUS`: "ORIGINAL VERSION"
- `PUBLIC URL`: Points back to the IHS FTP page
- `EXPORT TYPE`: "EHI" (also supports "4DW PAMPI" and "4DW ALL" for data warehouse exports)
- `PATIENT`: Array containing a single template entry with `DFN` (patient identifier) and `FILE` (301 file/table definitions)
- `POINTER FILE`: Array of 548 reference/lookup tables

Each patient file definition includes:
- File metadata (global, EHI-enabled flag, custom file flag, file version)
- Field definitions with: field type, FileMan data dictionary info (file-subfile number, global reference, node, piece), constraints (min/max length, bounds, decimal places), pointer references to other files, value set codes

### Field Type Distribution (2025 schema)

| Field Type | Count |
|-----------|-------|
| POINTER TO A FILE | 2,291 |
| FREE TEXT | 1,445 |
| SET OF CODES | 1,411 |
| DATE/TIME | 1,251 |
| NUMERIC | 698 |
| COMPUTED | 573 |
| WORD PROCESSING | 554 |
| WORD-PROCESSING | 170 |
| VARIABLE-POINTER | 21 |
| MULTIPLE COMPUTED | 1 |
| **Total** | **8,415** |

### Schema Evolution

The schema has grown steadily across versions:
- **2023 → 2024**: Added 2 files (BJVN HL7 EXCEPTIONS, CHS CHEF REGISTRY), field count changes in 13 files
- **2024 → 2025**: Added 3 files (BLRAU ANTIMICROBIAL USE LOG, BPHR MED REFILL REQUEST, V DELIVERY), field count changes in 12 files (notably PATIENT went from 171→194 fields, MHSS RECORD from 125→143 fields)

No files have been removed across any version.

## Export Coverage Assessment

### Data Domain Coverage

IHS RPMS's EHI export schema is **remarkably comprehensive** and represents one of the most thorough (b)(10) implementations in the industry. The 301 files cover the full breadth of RPMS's clinical and administrative data:

**Clinical Data — Thoroughly Covered:**
- **PCC V-files (43 files)**: The complete Patient Care Component visit-linked data — measurements, medications, procedures, diagnoses (POV), providers, immunizations, lab results, microbiology, pathology, radiology, dental, eye glass, health factors, skin tests, hospitalizations, emergency visits, elder care, well-child, nutrition screening, telehealth, patient education, stroke, AMI, anticoagulation, asthma, and more
- **Clinical notes (4 files)**: TIU DOCUMENT (all clinical notes), TIU EXTERNAL DATA LINK, TIU MULTIPLE SIGNATURE, TIU PROBLEM LINK
- **Pharmacy (13 files)**: PRESCRIPTION, PHARMACY PATIENT, PHARMACY ARCHIVE, controlled substance audit, DEA archive, interventions, Surescripts requests, drug accountability, medication verification
- **Laboratory (7 files)**: LAB DATA, LAB ORDER ENTRY, BLRA LAB AUDIT, BLS LOINC EXPORT, antimicrobial use, blood inventory, patient lab data
- **Behavioral health (27 files)**: Complete MHSS system — intake, records, case dates, groups, treatment plans, treatment notes, problems, goals, methods, suicide forms, personal history, health factors, measurements, prevention activities, CPT codes, providers, Navajo referral forms, CD staging tool
- **Dental (4 files)**: Dental patient, dental procedure, deferred services register, followup
- **Immunizations (7 files)**: BI PATIENT system — patient records, contraindications, forecast errors, immunizations due, deleted immunizations, IZ exports
- **Imaging (6 files)**: IMAGE, IMAGE AUDIT, IMAGING ANNOTATION, MULTI IMAGE PRINT, PACS MESSAGE, TELEREADER (note: actual image files are not included per PDF documentation, but metadata and links are)
- **Allergies**: PATIENT ALLERGIES (file 120.8), ADVERSE REACTION ASSESSMENT, ADVERSE REACTION REPORTING
- **Problem list**: PROBLEM file (9000011)
- **Orders**: ORDER file (100), NON-VERIFIED ORDERS, OE/RR PATIENT EVENT
- **Consultations/Referrals**: REQUEST/CONSULTATION, REFERRAL PATIENT, RCIS system (6 files)
- **Care plans**: CARE PLAN, TREATMENT PLAN, PATIENT GOALS
- **Specialty data**: Reproductive factors, birth measurement, prenatal problems, podiatry history, elder care, women's health (BW system), diabetes management (BCDM), HIV management (HMS REGISTRY), community health (CHR system), chronic disease (CIC VISIT), workman's compensation

**Administrative & Financial Data — Thoroughly Covered:**
- **Billing (35 files)**: 3P BILL, 3P CLAIM DATA, A/R system (7 files), BILL/CLAIMS, BILLING PATIENT, CLAIMS TRACKING, INTEGRATED BILLING ACTION, INSURANCE CLAIMS, CDMIS billing
- **Insurance eligibility**: MEDICAID ELIGIBLE/CLAIMS, MEDICARE ELIGIBLE/CLAIMS, PRIVATE INSURANCE ELIGIBLE/CLAIMS, RAILROAD ELIGIBLE/CLAIMS, ABSP COMBINED INSURANCE, ABSP ELIGIBILITY, AGEV INSURANCE ELIGIBILITY
- **Registration (40 files)**: PATIENT (9000001) with 194 fields, VA PATIENT (file 2) with 436 fields, enrollment data, demographic data, name changes, legal documents
- **Scheduling (10 files)**: Appointments, scheduled visits, wait lists, SD wait list, transfer requests

**Other Patient-Level Data:**
- Advance directives, notice of privacy practices, restricted health information, patient refusals for service, family history, personal history, guarantor information, beneficiary travel, spenddown information, prior authorizations, patient implanted devices

### What's Not in the Schema

Comparing against the product research, the schema covers virtually all patient-level clinical and billing data. Notable observations:

- **Images are excluded by design**: The PDF explicitly states "Imaging links/data are presented but not the images themselves in accordance with certification requirements." Image metadata files (IMAGE, IMAGING ANNOTATION) are included.
- **No quality reporting aggregates**: GPRA/clinical reporting data (BGP system) is not in the schema — this is appropriate as those are aggregate quality metrics, not individual patient records.
- **No audit logs beyond clinical**: The schema includes BLRA LAB AUDIT and IMAGE AUDIT (clinical audit trails) but not general system access audit logs — this is appropriate as system audit logs are not part of the designated record set.
- **No provider credentialing or system configuration**: Appropriate exclusions.
- **MailMan/messaging not included**: Internal system messaging is not in the schema. This is borderline — if messages contain clinical content about patients, they could be EHI, but they are primarily an operational communication system.

### Export Format & Standards

The export format is **native JSON** reflecting the RPMS FileMan database structure. This is:
- **Not FHIR**: The export uses RPMS's own data model, not HL7 FHIR. Fields reference FileMan file numbers, globals, nodes, and pieces.
- **Not a standardized format**: The JSON structure mirrors the MUMPS/FileMan database schema directly. Field names are the FileMan data dictionary field names.
- **Comprehensive but requires RPMS knowledge to interpret**: A receiving system would need to understand the FileMan data model to parse the export. The pointer references (2,291 pointer fields across 548 reference files) create a complex relational structure.
- **Self-documenting**: The schema files themselves serve as a data dictionary — each field definition includes type, constraints, validation rules, and pointer targets. The export data would follow this schema structure.

This is an appropriate format for (b)(10). The requirement doesn't mandate any standard — a comprehensive database dump in JSON with a published schema is a legitimate and thorough approach. The fact that it's in the native database format means nothing is lost in translation to a different standard.

### Documentation Quality

**Strengths:**
- The schema files are **machine-readable JSON** — excellent for automated processing
- Field definitions include **data types, constraints, value sets, and cross-references** — this is more detail than many commercial vendors provide
- Three years of versioned schemas show **active maintenance** (2023, 2024, 2025)
- The schema is **self-contained** — the 548 pointer files provide the lookup tables needed to interpret coded references
- The PDF correctly scopes EHI per 45 CFR 171.102

**Weaknesses:**
- The PDF is **very brief** (4 pages of content in 7 pages). It describes what the BREH package does but provides no examples, no sample export output, no walkthrough of the JSON structure.
- There are **no worked examples or sample export files**. A developer trying to build an importer would need to reverse-engineer the JSON structure from the schema definition files alone.
- **No user guide** for how to actually perform an export from the RPMS EHR GUI — only a statement that it "allows authorized users to manually generate an EHI export."
- **No documentation of the JSON output format** — the schema defines what data is included and its field types, but doesn't show what the actual export JSON looks like (key names, nesting structure, array handling).
- Field definitions lack **human-readable descriptions** — field names are generally descriptive (e.g., "BLOOD TYPE", "BIRTH CERTIFICATE NO.") but there are no narrative descriptions explaining what each field contains or how it should be interpreted.

### Structure & Completeness

- **Granularity**: Excellent. 8,415 field-level definitions across 301 files, with data types, FileMan metadata, pointer references, and value sets for coded fields.
- **Relationships**: Documented via POINTER TO A FILE fields (2,291 of them) and 548 pointer/reference file definitions. The relational structure is complete and machine-readable.
- **Value sets**: 1,411 SET OF CODES fields include their full value lists in the schema.
- **Versioning**: Three annual versions (2023, 2024, 2025) with clear version names and dates. The schema has grown from 296 to 301 files and from ~8,221 to 8,415 fields.
- **Change history**: The schema diff shows that changes are additive (new files, new fields) with no removals — suggesting careful backward compatibility.

## Access Summary
- Final URL (after redirects): https://www.ihs.gov/rpms/applications/ftp/?parent=&fld=EHI_Schemas
- Status: found
- Required browser: no (direct curl download works)
- Navigation complexity: direct_link (all files listed on a single page with download links)
- Anti-bot issues: none (User-Agent header recommended but standard browser UA suffices)

## Obstacles & Dead Ends

None. The documentation was straightforward to access. The IHS FTP file browser page loaded correctly, all 4 files were publicly downloadable without authentication, and the JSON schema files were well-formed and parseable.

The page does include a login/registration panel, but the file downloads work without authentication. The login may be required for other folders on the FTP site (e.g., RPMS software packages) but not for the EHI_Schemas folder.
