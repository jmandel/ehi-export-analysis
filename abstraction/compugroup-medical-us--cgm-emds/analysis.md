# EHI Export Analysis: CompuGroup Medical US

**Product**: CGM eMDs v10
**Analysis date**: 2026-02-16
**CHPL IDs**: 11133 (15.04.04.2700.eMDs.10.02.1.221227)

## 1. Product Context

CGM eMDs is an **integrated EHR and practice management suite** for ambulatory/outpatient practices, originally created in 1996 by physicians in Austin, TX and acquired by CompuGroup Medical in 2020 for $240M. It is a single certified module encompassing clinical charting, e-prescribing (CGM PRESCRIBE with EPCS, ePA, PDMP), scheduling, practice management, billing, and patient engagement. It supports 70+ medical specialties with customizable templates and includes add-on modules for document management (DocMan), internal messaging (TaskMan), quality reporting (CGM MEASURES), telehealth (CGM ELVI), and AI documentation (CGM AMBI).

**Data the product stores that is relevant to EHI export completeness:**
- **Clinical**: Demographics, encounter notes, problems, medications, allergies, immunizations, vitals, lab orders/results, procedures, social history, family history, SDOH, care plans, referrals, clinical decision support alerts
- **Prescribing**: Electronic prescriptions (including EPCS), prior authorization records, PDMP queries, medication benefit info
- **Billing/PM**: Insurance/guarantor information, claims, charges (ICD/CPT), payments, adjustments, eligibility verification, ERA posting, denial management
- **Documents**: Scanned documents, imported files/images, external records (via DocMan)
- **Communications**: Patient portal messages, internal staff messages/tasks, patient communication logs
- **Specialty**: OB module with pregnancy history; specialty-specific templates across 70+ specialties

This establishes a broad baseline: a complete (b)(10) export should cover clinical data across all these domains, billing/financial data, documents, and communications.

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `cgm-emds-electronic-health-information-export-user-guide.pdf` | 14-page PDF (December 2023, 196 KB). Primary and sole EHI export documentation. Contains export instructions, 27 document category table, and field-level data dictionary for 5 export files. | **Most informative** — this is the only substantive artifact |
| `fhir-api-documentation-guide.pdf` | 76-page PDF (April 2024, 498 KB). FHIR R4 API documentation for (g)(10) certification. Covers US Core resources. Separate from the (b)(10) export. | Useful for confirming EHI export is distinct from FHIR API |
| `screenshot-certifications-links.png` | Screenshot of the product page's Certifications accordion. | Confirms the EHI export doc link exists on the product page |
| `enrichment/ehi-data-dictionary.json` | Prior agent's structured extraction of the PDF data dictionary. 28 KB JSON. | Useful starting point; contains minor errors corrected in my parse (see analysis/full-entity-inventory.json) |

**Key finding**: The entire EHI export documentation consists of a single 14-page PDF. No sample data, no machine-readable schemas, no JSON/XML schema files, no example export files.

## 3. Export Mechanics

- **Format**: Password-protected ZIP file containing XLSX spreadsheets (4 files), an RTF/text file (1 file), a README, and a folder of document files (DocMan Files)
- **Naming convention**: `Patient(lastname, firstname[AccountNumber]) YYYY-MM-DD HH-MM-SS.zip`
- **Mechanism**: Generated within the CGM eMDs application (in-app export). Not an API call.
- **Scope**: **Single-patient only**. No evidence of bulk/multi-patient export capability.
- **Access constraints**: Password-protected ZIP. No documented fees for the export itself.
- **Distinctness from FHIR**: This is a completely separate mechanism from the (g)(10) FHIR R4 API. The FHIR API serves US Core resources; the EHI export produces XLSX/RTF/document files. This is correctly scoped as a dedicated (b)(10) implementation.

## 4. Export Content: What's In It

The export is a **report-style extraction** — it packages existing clinical and billing reports (Chart Cover, Health Summary, Trial Balance, etc.) plus document management files into a ZIP. It is **not** a native database model export; it is a projection of internal data into spreadsheet reports.

### Data dictionary overview

The PDF documents 5 structured export files across 29 sections with 162 total fields. However:
- **148 fields** have formal column-level definitions (name + data type)
- **14 fields** are content-area descriptions for the Entire Patient Chart Report (which has no formal field table in the PDF — only a prose description)
- **0 fields** have descriptions beyond the field name itself
- **1 field** has no data type listed (`Insurance Address` in Chart Cover Report)
- **0 fields** have value sets, foreign keys, format specifications, or nullability documented

### Vendor's own content organization

The vendor organizes the export into 5 structured files plus a DocMan Files folder covering 27 document categories.

**Structured export files:**

| Export File | Sections | Fields | Detail Level |
|---|---|---|---|
| Chart Cover Report.xlsx | 7 | 53 | Formal columns with data types |
| Entire Patient Chart Report.xlsx | 1 | 14 | Content-area descriptions only (no column-level table) |
| Health Summary Report.xlsx | 8 | 27 | Formal columns with data types |
| Referral Authorization Report.xlsx | 4 | 19 | Formal columns with data types |
| Trial Balance Report.rtf | 9 | 49 | Formal columns with data types |
| **Total** | **29** | **162** | |

**Largest file: Chart Cover Report.xlsx (53 fields)** — covers demographics (16 fields), employment (6), guarantor (10), insurance (10), health summary lists (6), plus practice/audit metadata (5). This is the richest file in terms of structured data.

**Billing file: Trial Balance Report.rtf (49 fields)** — covers invoice headers (8 fields), ICD codes (2), CPT codes (7), insurance per-invoice (8), payment line items (8), payment totals (9), and invoice balances (3). This provides genuine billing granularity.

**Least documented: Entire Patient Chart Report.xlsx (14 content areas)** — the PDF provides only a prose description listing what content areas appear. No column headers, no field-level detail. This file reportedly contains "all clinical visit notes" but the structure is opaque from the documentation.

**Empty section: "Tests and Procedures"** in Health Summary Report lists a section header but documents zero fields underneath.

**DocMan Files folder: 10 document categories** including C-CDA/CCD documents (.xml, .zip), care plans (.xml, .zip), consent forms (.tif, .pdf), general images, lab images (.hl7, .tif), letters, patient documents, pregnancy history (.rtf, .pdf), procedure images, and radiology images. File naming convention: `<date added to encounter><ID><description>.<extension>`.

The complete field-level inventory is in `analysis/full-entity-inventory.json`.

**Data type distribution across all 162 fields:**

| Data Type | Count |
|---|---|
| String | 121 |
| Date | 16 |
| String List | 11 |
| Number | 9 |
| Time | 2 |
| Image | 2 |
| (none listed) | 1 |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is organized around **5 report-style files** plus a **document folder**:

**Demographics & Insurance** (Chart Cover Report): Solid coverage with 53 fields covering patient identity, contact info, employment, guarantor, insurance details including card images, and summary health lists. This is the most structured file.

**Clinical Visit Notes** (Entire Patient Chart Report): Claims to contain "all clinical visit notes" plus allergies, medications, problems, messages, histories (medical, social, family, substance, mental health), patient education, immunizations, and SDOH responses. However, the documentation provides no column-level detail — only a prose list of content areas. The actual structure of this file is unknown from the documentation alone.

**Health Summary** (Health Summary Report): 27 fields covering current problems, current medications (with dosage/form/instructions), allergies, extensive past medical history (including tobacco, alcohol, supplements, substance abuse, mental health, communicable diseases), health maintenance items, and orders. The "Tests and Procedures" section is listed but has no documented fields.

**Referrals & Authorizations** (Referral Authorization Report): 19 fields covering referral/authorization metadata with dates, insurance, specialist info, and visit tracking.

**Billing** (Trial Balance Report): 49 fields providing genuine billing depth — invoice-level detail with ICD codes, CPT codes with descriptions/dates/units/fees, insurance data per invoice, payment line items (patient and insurance), adjustments, and running balances. This is notably better than many EHR (b)(10) exports that omit billing entirely.

**Documents** (DocMan Files): 10 categories covering the full range of document management — images, scanned documents, C-CDA files, care plans, consents, lab images (HL7 format), radiology images, pregnancy history, and letters. This captures unstructured/semi-structured data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Chart Cover Report: Patient Information (16 fields), Employment Information (6 fields), Guarantor Information (10 fields) | Thorough — name, address, DOB, SSN, gender, marital status, phone numbers, email, employer, DL# |
| Encounters / visits | ⚠️ Partial | Entire Patient Chart Report lists "All clinical visit notes" as content area; Trial Balance Report has invoice dates that imply encounter dates | Visit notes present but no structured encounter metadata (date, type, location, provider, disposition) documented at field level |
| Problems / conditions / diagnoses | ✅ Covered | Health Summary Report: Current Problems; Chart Cover Report: Current Problem List; ICD codes in Trial Balance Report | Active/inactive problems covered; ICD codes in billing |
| Medications / prescriptions | ✅ Covered | Health Summary Report: Current Medications (4 fields: name, dosage, form, instructions); Chart Cover Report: Current Medication List | Current/past medication lists covered. Prescription transmission records (Surescripts, ePA, EPCS) from CGM PRESCRIBE module not explicitly documented |
| Allergies | ✅ Covered | Health Summary Report: Allergies/Adverse Reactions; Entire Patient Chart Report: Allergies content area | Covered in two files |
| Immunizations | ✅ Covered | Entire Patient Chart Report: Immunizations content area | Listed but no field-level detail documented |
| Vitals | ❌ Not covered | No dedicated vitals section in any export file | Product stores vitals (certified under (a)(4) Vital Signs). May be embedded in visit notes (Entire Patient Chart Report) but not documented as discrete data. **Genuine gap.** |
| Lab results | ⚠️ Partial | Health Summary Report: "Tests and Procedures" section (0 fields documented); "Orders" category; DocMan Files: Lab Images (.hl7, .tif) | Lab images exported but no evidence of discrete lab result values (numeric results, reference ranges, units) in structured form. The "Tests and Procedures" section is empty. **Significant gap in structured lab data.** |
| Imaging / diagnostic reports | ⚠️ Partial | DocMan Files: Radiology Images, Procedure Images | Images exported but no structured radiology/diagnostic report data (findings, impressions) documented |
| Procedures | ⚠️ Partial | Trial Balance Report: CPT codes with descriptions; DocMan Files: Procedure Images | Procedure codes captured in billing; images captured in DocMan. No structured clinical procedure documentation beyond billing codes |
| Clinical notes / documents | ✅ Covered | Entire Patient Chart Report: "All clinical visit notes"; DocMan Files: patient documents, letters | Claimed as comprehensive; however, field-level structure undocumented |
| Care plans / goals | ✅ Covered | DocMan Files: Care Plan (.xml, .zip) as CDA files | Exported as CDA documents |
| Orders / referrals | ✅ Covered | Health Summary Report: Orders, Upcoming Test/Health Maintenance Items (4 fields); Referral Authorization Report (19 fields) | Referrals well-documented; orders partially documented |
| Insurance / coverage | ✅ Covered | Chart Cover Report: Insurance Information (10 fields); Trial Balance Report: Insurance Data per invoice (8 fields) | Insurance details with card images; per-invoice insurance data in billing |
| Claims / billing | ✅ Covered | Trial Balance Report: Invoice headers, ICD codes, CPT codes, fees, units (49 fields total across 9 sections) | Notably thorough billing data with invoice-level granularity, charges, payments, adjustments, and balances |
| Payments | ✅ Covered | Trial Balance Report: Payment Data (8 fields per payment line), Payment Total Data (9 fields) | Patient and insurance payments with adjustment tracking |
| Consents / directives | ✅ Covered | DocMan Files: Consents (.tif, .pdf) | Consent forms as scanned documents |
| Patient communications / portal messages | ✅ Covered | Entire Patient Chart Report: "Patient messages" content area | Listed but no field-level detail |
| Specialty-specific (OB) | ✅ Covered | DocMan Files: Pregnancy History (.rtf, .pdf) | OB/pregnancy data exported as documents |

**Domain score: 13 of 18 applicable domains covered or partially covered; 1 not covered (vitals as discrete data); 4 partially covered.**

## 6. Documentation Quality

**Field-level documentation**: Names and data types only. Zero fields have descriptions, value sets, format specifications, foreign keys, nullability, or max length. Data types are generic ("String", "Date", "Number", "Image", "String List", "Time") — no date format, string length limits, or encoding specifications.

**Relationships**: No foreign key documentation, no entity-relationship diagram. The "Patient Account Number" appears in multiple files and could theoretically be used to join them, but this is not documented.

**Sample data**: None provided. No example export files, no sample XLSX or RTF.

**Machine-readable schemas**: None. No XSD, JSON Schema, or any machine-readable artifact. The data dictionary exists only as tables embedded in a PDF.

**Most undocumented file**: The Entire Patient Chart Report — described as containing "all clinical visit notes" and 13 other content areas — has **no column-level detail whatsoever**. The PDF simply lists what categories of data appear, not how they're structured. This is the single most important clinical file in the export and it's the least documented.

**Could a developer build an import?** With significant effort and reverse engineering. The 4 structured files (Chart Cover, Health Summary, Referral Authorization, Trial Balance) have column headers documented, so their XLSX structure could be parsed. But the Entire Patient Chart Report would require sample data to understand. The DocMan Files folder structure is partially documented (naming convention given) but file-level parsing would depend on the content type. No developer could confidently build a complete import pipeline from this documentation alone.

**Minor PDF issues found during verification**:
- "Practice Data" and "Audit Information" are separate sections in Chart Cover Report (prior enrichment merged them)
- "Insurance" field belongs in "Report Data" section of Referral Authorization Report (prior enrichment placed it in "Report Filter Information")
- "Insurance Address" has no data type listed (blank cell in PDF)
- "Patient Nam" typo in Trial Balance Report
- Trial Balance Report header says ".rtf" but File Type field says "Text File (.txt)"

## 7. Overall Assessment

### Classification

**Partial native export.** The export attempts to cover most data domains the product stores — including billing, which many vendors omit — but it is a report-style projection (XLSX reports + document folder) rather than a native database model export. The lack of field-level documentation for the Entire Patient Chart Report, the absence of discrete vitals and structured lab results, and zero field descriptions significantly limit its utility. However, the inclusion of 49-field billing detail and 10 categories of document management files demonstrates genuine effort beyond a clinical-summary-only approach.

### Key Findings

1. **Dedicated (b)(10) implementation** — CGM eMDs correctly separates its EHI export from its FHIR API. The export is an in-app ZIP generator, not a FHIR/C-CDA repackaging. This is a positive signal. (Source: comparing `cgm-emds-electronic-health-information-export-user-guide.pdf` with `fhir-api-documentation-guide.pdf`)

2. **Billing data is a strength** — The Trial Balance Report provides 49 fields of invoice-level billing detail including ICD codes, CPT codes with fees/units, insurance/patient payment line items, adjustments, and running balances. This is more billing granularity than many comparable vendor exports. (Source: Trial Balance Report section, PDF pages 8-10)

3. **Most important clinical file is undocumented** — The Entire Patient Chart Report, which claims to contain "all clinical visit notes," has no column-level documentation — only a prose list of 14 content areas. This is the file that would contain the bulk of clinical data, and its structure is completely opaque. (Source: PDF page 5, which has only a prose paragraph rather than a field table)

4. **No discrete vitals or structured lab results** — Vital signs have no dedicated section anywhere in the export despite the product being certified for vitals capture (criterion (a)(4)). Lab results appear only as images (.hl7, .tif) in DocMan Files, with no structured numeric data. The "Tests and Procedures" section in Health Summary Report documents zero fields. (Source: Health Summary Report section, PDF pages 6-7; DocMan Files categories table, PDF pages 1-3)

5. **Zero field descriptions** — None of the 162 fields have descriptions, value sets, format specifications, or relationship documentation. The data dictionary is names-and-types only. No sample data or machine-readable schemas are provided. (Source: all field tables in PDF pages 4-10)

### Summary Stats

```
Classification:  Partial native export
Export format:   XLSX, RTF, plus document files (images, XML, HL7, PDF, TIF) in ZIP
Model type:      Report-style projection (not native database tables)
Entities:        5 structured files + 1 document folder (27 document categories)
Fields:          162 total (148 formal column definitions + 14 content-area descriptions)
Descriptions:    0% (names and data types only; no descriptions)
Sample data:     No
Bulk export:     No (single-patient only)
Domains covered: 13 of 18 applicable domains (✅ or ⚠️)
```

### Bottom Line

CGM eMDs provides a dedicated EHI export that goes beyond clinical summaries to include genuine billing data and document management files — a real effort. However, the export is hampered by opaque documentation for its most important clinical file (Entire Patient Chart Report), missing discrete vitals and structured lab data, and zero field descriptions across all 162 fields. A patient would receive a reasonably broad data package, but a developer attempting to import or analyze this data would face significant reverse-engineering challenges.
