# EHI Export Analysis: E*HealthLine.com, Inc.

**Product**: CARE© Integrated Hospital Information Management System
**Analysis date**: 2026-02-16
**CHPL IDs**: 10833 (15.02.05.1384.EHLC.01.01.0.220217)

## 1. Product Context

CARE© is a full-scope hospital information system (HIS) marketed by E*HealthLine.com, Inc., a small (~7 employee) Sacramento-based vendor founded in 1999. The product is certified across 40+ ONC criteria (including clinical, interoperability, public health, and quality measures), positioning it as an all-in-one inpatient and ambulatory platform.

The core modules relevant to EHI export assessment are:

- **ADT** — Admission, Discharge, Transfer, patient registration
- **CARE Chart / Clinical Foundation** — Electronic medical records, charts, flow sheets, clinical documentation
- **CARE CPOE** — Computerized Provider Order Entry with medication, lab, and radiology ordering
- **eLab** — Clinical Laboratory Information System (orders, specimens, results, QA, auto-verification)
- **eRad / PACS** — Radiology Information System and imaging (orders, exams, reports, film tracking, images)
- **eBilling** — Billing and revenue management (claims, payments, patient liability, EDI)
- **SPHINX** — Hospital Financial Management System (details unavailable; product page returned 404)
- **Scheduling** — Appointment and resource scheduling

Based on these modules, the product stores clinical data (demographics, encounters, problems, medications, allergies, labs, radiology, vitals, immunizations, procedures, notes), billing/financial data (charges, claims, payments), and departmental workflow data (lab specimens, radiology exams, image references). This sets the baseline for what a complete EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/Electronic_Health_Information_Export.pdf` | 10-page PDF (265,837 bytes). Version 2.0, dated October 24, 2023 (PDF last modified July 18, 2024). Title: "170.315(b)(10) Electronic Health Information Export." User guide describing the export mechanism and file structure at a high level. Encrypted with RC4 (copy disabled) but text extractable via pdftotext. | **Primary and only artifact.** Contains all available documentation. No screenshots, no data dictionary, no schemas, no sample data. |

No additional artifacts were found. The `files.json` manifest lists exactly one file. The vendor's PDF directory (`/dev/pdf/`) returns 403, and probes for related PDFs (Export Batch CCDA, CDA Export, etc.) all return 404. The referenced "full Export Batch CCDA documentation" mentioned on page 7 of the PDF is not publicly available.

## 3. Export Mechanics

- **Function**: "Export Batch CCDA" accessible from the Data Maintenance Menu in the EHR
- **Format**: ZIP file (`CDAXMLExport_8.Zip`) containing C-CDA XML, CSV files, and CDA XML folders
- **Single patient**: Yes — select by patient name or medical record number
- **Population export**: Yes — select multiple patients by name or MR# range
- **Output location**: UNC network path `\\SERVERNAME\BarcodeScans\HL7ExportFiles\CDAexports`
- **Access control**: Requires admin-granted privileges: `[Edit General Database Setup]` plus `[Print Documents]` or `[Chart Reviewer]`
- **API**: No — this is a desktop/server UI operation, not an API
- **Vendor assistance**: Not required; users can export independently
- **Fees**: Not mentioned

The export function is described as an update to the existing CDA Batch export screen, with new options added for (b)(10) compliance: Clinic Logon selection, Include Chart Documents checkbox, Show Sticky Notes on TIF docs, and inclusion of Custom Patient Data Tables.

## 4. Export Content: What's In It

The export ZIP contains 7 core components (plus 2 optional), described at a **file-level only** — no field/column-level documentation exists anywhere in the PDF.

### Vendor's own content organization

The vendor does not organize content into formal categories. The following table reconstructs the export components from the PDF's file structure descriptions (pages 5–6):

| Component | Format | Description (vendor's words) | Field-Level Docs |
|---|---|---|---|
| **CCDA** | XML (HL7 C-CDA) | "XML file export of a patient's clinical data... complies with USCDI, Version 1 requirements" | None — defers to HL7 spec |
| **BillingReport** | CSV | "Patient's financial transactions with their provider. Includes patient information, transaction dates, charges, claims and the description of transactions made with status." | None — mentions 6 data concepts but no column names |
| **demographics** | CSV | "Patient's key information, identification details, contact information, insurance information etc." | None — mentions 4 data categories but no column names |
| **Schedule** | CSV | "Record of the patient's encounters... appointment date, provider, location, appointment type, workflow, notes and date on which notes are recorded." | None — mentions 7 data concepts but no column names |
| **Notes** | CDA XML (folder) | "All the notes recorded during the patient's previous medical visits/encounters." | None |
| **Documents** | CDA XML (folder) | "Patient's supporting documents or attachments when available." | None |
| **PatientDocumentFiles** | CSV | "Mapping file that contains the list of patient's documents... outlines the contents of the patients supporting attachments contained in the 'Documents' folder." | None |
| **Chart Documents** *(optional)* | Mixed (TIF, etc.) | Optionally included via checkbox. Chart documents with optional sticky notes on TIF. | None |
| **Custom Patient Data Tables** *(auto-included)* | Embedded in CDA | "Custom (user created) Patient Data Tables will be included as part of the CDA" unless excluded via [Exclude FHR] flag. | None — no information on what tables exist or their structure |

**Critical gap**: Zero fields are documented. The CSV files (BillingReport, demographics, Schedule, PatientDocumentFiles) have no column headers, data types, formats, value sets, or sample rows documented. The C-CDA component defers entirely to the HL7 specification with no vendor-specific mapping. The Custom Patient Data Tables mechanism is described procedurally but provides no indication of what tables exist, how many there are, or what they contain.

The total field-level information in the entire document amounts to natural-language mentions of ~17 data concepts across the CSV descriptions (e.g., "transaction dates," "charges," "provider," "location") — but these are embedded in prose, not formal column names.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has two layers:

1. **C-CDA layer**: Standard USCDI v1 clinical summary covering the typical C-CDA sections (problems, medications, allergies, labs, vitals, immunizations, procedures, etc.). This is the same content any certified EHR can produce — it's a clinical summary, not a comprehensive data export.

2. **CSV supplement layer**: Four CSV files extending beyond C-CDA to cover billing (BillingReport), demographics/insurance (demographics), encounters/scheduling (Schedule), and document mapping (PatientDocumentFiles). This shows awareness that C-CDA alone is insufficient for (b)(10).

3. **Document/Notes layer**: CDA XML folders for clinical notes and supporting documents/attachments.

4. **Custom data layer**: Custom Patient Data Tables embedded in the CDA export, with an opt-out mechanism.

The supplement layer is a positive signal — the vendor recognized that (b)(10) requires more than C-CDA. However, the supplements are described at such a high level that it's impossible to assess their completeness. The BillingReport CSV could be a single summary row per encounter or a detailed claims-level extract — we can't tell from the documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `demographics` CSV mentions "key information, identification details, contact information, insurance information" — but no field-level detail | Product stores full ADT/registration data; CSV likely covers basics but completeness unverifiable |
| Encounters / visits | ⚠️ Partial | `Schedule` CSV mentions "appointment date, provider, location, appointment type, workflow, notes" | Mentions encounter data concepts but no ADT-level detail (admit/discharge times, transfer events, bed assignments) |
| Problems / conditions / diagnoses | ⚠️ Partial | C-CDA (USCDI v1 includes problem list) | Standard C-CDA problem list; no evidence of vendor-specific problem detail beyond USCDI |
| Medications / prescriptions | ⚠️ Partial | C-CDA (USCDI v1 includes medications) | Standard C-CDA medication list; CPOE order detail, medication administration records likely not captured |
| Allergies | ⚠️ Partial | C-CDA (USCDI v1 includes allergies) | Standard C-CDA allergy section |
| Immunizations | ⚠️ Partial | C-CDA (USCDI v1 includes immunizations) | Standard C-CDA immunization section |
| Vitals | ⚠️ Partial | C-CDA (USCDI v1 includes vitals) | Standard C-CDA vital signs section |
| Lab results | ⚠️ Partial | C-CDA (USCDI v1 includes lab results) | Standard C-CDA results; eLab stores far more (specimen tracking, QA, auto-verification, reflex testing) — this workflow/detail data is likely absent |
| Imaging / diagnostic reports | ⚠️ Partial | C-CDA may include some procedure/result data; Documents folder may include reports | eRad/PACS stores orders, exams, film tracking, reports, images — most of this detail is likely not in C-CDA. No mention of image file export. |
| Procedures | ⚠️ Partial | C-CDA (USCDI v1 includes procedures) | Standard C-CDA procedures section |
| Clinical notes / documents | ✅ Covered | `Notes` folder (CDA XML, "all notes from previous medical visits/encounters") + `Documents` folder + optional Chart Documents | Appears to be a genuine export of all notes and documents |
| Care plans / goals | ⚠️ Partial | C-CDA may include care plan section if populated | No specific mention; depends on C-CDA content |
| Orders / referrals | ❌ Not covered | No specific mention of order export beyond what C-CDA includes | CPOE is a major module; order history and detail likely not in C-CDA summary |
| Insurance / coverage | ⚠️ Partial | `demographics` CSV mentions "insurance information" | Mentioned but no field-level detail; unknown depth |
| Claims / billing | ⚠️ Partial | `BillingReport` CSV mentions "financial transactions, charges, claims, description, status" | Dedicated CSV is a positive signal, but no field-level detail — could be summary or detailed |
| Payments | ⚠️ Partial | Possibly included in BillingReport CSV ("transactions" and "charges") | eBilling includes revenue management; unclear if payment detail is in the export |
| Consents / directives | ❌ Not covered | No mention in export documentation | Unknown if product stores advance directives beyond C-CDA |
| Patient communications / portal messages | ❌ Not covered | No mention of patient portal messages or communications | Product is certified for (e)(1) patient portal VDT; portal messages are not exported |

**Summary**: Of 18 applicable domains, 1 is clearly covered (clinical notes/documents), 13 are partially covered (primarily through C-CDA's standard sections, with limited CSV supplements), 3 are not covered, and 1 (consents) is unclear. The coverage is heavily dependent on what C-CDA provides by default, with meaningful but underdocumented CSV supplements for billing, demographics, and scheduling.

## 6. Documentation Quality

**Rating: Very Poor**

The documentation fails on every axis a developer would need:

| Quality Dimension | Assessment |
|---|---|
| **Field names** | ❌ Not documented for any CSV file. C-CDA defers to HL7 spec. |
| **Data types** | ❌ Not documented |
| **Value sets / coded values** | ❌ Not documented |
| **Relationships** | ❌ Only the PatientDocumentFiles → Documents folder relationship is mentioned |
| **Sample data** | ❌ Not provided |
| **Machine-readable schemas** | ❌ Not provided |
| **Screenshots** | ❌ Not provided (despite 14-step UI workflow descriptions) |
| **Usability for import** | ❌ A developer could not build an importer from this documentation alone |

**Documentation defects identified**:
1. **Wrong criterion in footer**: Every page footer says "170.315(g)(10) — Standardized API For Patient and Population services" instead of (b)(10). This is a copy-paste error from a different document template.
2. **Truncated sentences**: Steps 14 (p. 9) and 15 (p. 10) both end with "For additional details on the export format and default paths," — the sentence is cut off mid-thought, referencing a document that is not provided.
3. **Confusing version history**: Both v1.0 (Oct 14, 2023) and v2.0 (Oct 24, 2023) are described identically as "Original Document."
4. **Missing referenced document**: Page 7 references "the full Export Batch CCDA documentation for additional information" — this document is not publicly available.

The 10-page PDF is approximately 40% compliance attestation text (restating the (b)(10) regulatory requirements verbatim), 30% step-by-step UI instructions (without screenshots), and 30% high-level file structure descriptions. There is no technical specification content.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is fundamentally built on the existing C-CDA export ("Export Batch CCDA") with CSV supplements added for (b)(10) compliance. The clinical data is a standard C-CDA/USCDI v1 clinical summary, not a native database export. The CSV supplements for billing, demographics, and scheduling extend beyond pure C-CDA, but they are undocumented at the field level and may be thin.

### Key Findings

1. **Export is a C-CDA wrapper, not a native data model export.** The function is literally called "Export Batch CCDA" and was updated for (b)(10) by adding a few checkboxes. Clinical data comes from a standard USCDI v1 C-CDA — the same format as the (b)(1)/(g)(10) exports. This inherently limits what patient data is exported to what C-CDA can represent. (Source: PDF pages 5–7)

2. **CSV supplements show genuine (b)(10) awareness but are completely undocumented.** The BillingReport, demographics, Schedule, and PatientDocumentFiles CSVs extend beyond C-CDA's clinical summary scope. However, without any column names, data types, or sample data, it's impossible to assess whether these contain meaningful detail or summary-level information. (Source: PDF pages 5–6)

3. **Zero field-level documentation exists.** Across the entire 10-page PDF, not a single column name, data type, or value set is specified for any export file. The vendor describes 4 CSV files and 2 CDA XML folders using only 1–2 sentence prose descriptions. (Source: full-entity-inventory.json)

4. **Major product modules likely have no export representation.** The CARE system includes full eLab (lab orders, specimens, QA, reflex testing), eRad (radiology orders, exams, film tracking), and CPOE (medication/lab/radiology orders) modules. These store detailed workflow and clinical data far beyond what a C-CDA clinical summary captures. The export documentation makes no mention of lab workflow data, radiology workflow data, or order history. (Source: product-research.md vs PDF pages 5–6)

5. **Documentation has quality control issues.** Wrong criterion in footer ((g)(10) instead of (b)(10) on every page), truncated sentences referencing missing documents, and identical version descriptions suggest this was produced hastily as a compliance deliverable. (Source: PDF pages 1–10 footers, pages 9–10 steps 14–15)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + CSV + CDA XML folders (in ZIP)
Model type:      Standard projection (C-CDA/USCDI v1) with vendor CSV supplements
Entities:        9 file components (no field-level breakdown)
Fields:          N/A (zero fields documented)
Descriptions:    N/A (no field-level documentation)
Sample data:     No
Bulk export:     Yes (population export via MR# range or multi-select)
Domains covered: 1 of 18 clearly, 13 of 18 partially (via C-CDA + CSV)
```

### Bottom Line

The CARE EHI export is a C-CDA clinical summary repackaged with CSV supplements for billing, demographics, and scheduling. While the CSV supplements show the vendor recognized that C-CDA alone doesn't meet (b)(10), the complete absence of field-level documentation makes it impossible to verify what data is actually exported. A patient or provider receiving this export would get a standard clinical summary plus some billing and scheduling data, but would likely be missing detailed lab workflow data, radiology workflow data, CPOE order history, and other data stored in the product's departmental modules. The single biggest gap is the lack of any data dictionary or field-level documentation — without it, neither completeness nor usability can be assessed.
