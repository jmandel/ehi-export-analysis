# EHI Export Analysis: TechSoft, Inc.

**Product**: MDRhythm Version 8
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2413.MDRh.08.00.1.181208

## 1. Product Context

MDRhythm is a comprehensive medical practice management and EHR system developed by TechSoft, Inc., a small (~15 employees) New Jersey-based company founded in 1989 with an R&D center in India. The product has been in use since 1992 and targets outpatient clinics across specialties.

Based on the vendor's own product pages (mdrhythm.com/products.html, /product_info.html, /emr.html, /services.html), MDRhythm includes:

- **EMR/EHR**: Template-based visit notes (SOAP format), vitals, prescriptions, lab integration, document scanning, faxing
- **Practice Management**: Patient record keeping, appointment scheduling, referrals
- **Billing & Claims**: Patient ledger and accounting, paper and electronic billing, claim management
- **Clearinghouse**: Medstech Clearing House (branded clearinghouse service for claims processing, eligibility verification)
- **E-Prescribing**: Electronic prescriptions, refills
- **Patient Portal**: Patient-facing access (fee-based add-on)
- **FHIR API**: US Core 5.0.1 / USCDI v2 compliant (fee-based)
- **Retail Sales Management**: Listed as a product module
- **Reporting**: "Versatile Report Generation"

The product explicitly describes itself as providing "administrative, clinical [and] claim handling from a single platform." This means a complete EHI export should cover clinical data, billing/claims, insurance, and practice management data.

## 2. Artifacts Reviewed

| Artifact | Source | Description | Informativeness |
|---|---|---|---|
| `MDRhythm_B10_Data_Export_Instructions.pdf` | http://www.mdrhythm.com/MDRhythm%20B10%20Data%20Export%20Instructions.pdf | 3-page PDF describing the (b)(10) EHI export process. Contains instructions, 2 screenshots, and a list of 6 data categories. **This is the primary (b)(10) documentation.** | ⭐ Most informative (for the (b)(10) export) |
| `MDR-FHIR-API-Documentation.pdf` | http://www.mdrhythm.com/MDR-FHIR-API-Documentation.pdf | 240-page PDF documenting the FHIR R4 API (US Core 5.0.1). Covers SMART App Launch, OAuth2, and 19 clinical data sections with request/response examples. **Not the (b)(10) export; this is the (g)(10) FHIR API.** | Contextually useful |
| `onc-compliance.html` | http://www.mdrhythm.com/onc-compliance.html | ONC compliance page with mandatory disclosures, price transparency, links to RWT plans, FHIR docs, and B10 export docs. | Moderately informative |
| Vendor website pages | mdrhythm.com (products, product_info, emr, services, aboutus) | Product feature descriptions establishing what data MDRhythm stores. | Important for gap analysis |
| RWT pages (2022–2025) | mdrhythm.com/rwtplan_*.html, rwtresult*.html | All return only a copyright footer — effectively empty. | Not informative |

## 3. Export Mechanics

- **Format**: PDF — a flat, non-machine-readable document. The export produces a single PDF file containing patient visit records.
- **Mechanism**: Web-based UI at `https://patientdata.mdronline.net`. Users log in with practice credentials, select patients from a list, and click "Export EHR."
- **Single-patient vs bulk**: Supports 1–5 patients per export batch. Not a true bulk export capability.
- **Access constraints**: Requires practice login credentials. The price transparency statement does not list a specific fee for (b)(10) exports, though the (g)(9) "all data request" is noted as requiring "a fee every time such data is requested" and the (g)(10) FHIR API requires "a fee published from time to time."

## 4. Export Content: What's In It

### The (b)(10) Export

The B10 export documentation (`MDRhythm_B10_Data_Export_Instructions.pdf`, 3 pages) describes an export that produces **a flat PDF file** — not structured data. The documentation explicitly lists 6 categories of exported data:

1. Patient Demographics
2. Allergy Details
3. Current Medication Details and Medication History
4. Diagnosis and Problem Information
5. Visit Note Information
6. Vitals Information

There is **no data dictionary**, **no schema**, **no field-level documentation**, and **no machine-readable format**. The only detail beyond the 6-item list is a sample screenshot (page 2 of the PDF) showing one patient's exported visit record.

### What the sample screenshot reveals

From the sample export screenshot (page 2), the exported PDF for a single patient visit contains:

| Section | Content Observed |
|---|---|
| Visit Details | Patient name, provider name, sex, DOB, visit date |
| Subjective: Allergies | Comma-separated list (e.g., "Amoxicillin, Apples, Beer, Shampoo") |
| Subjective: Medical History | Conditions with start dates (e.g., "Diabetes mellitus type 1", "Fibromyalgia") |
| Meds Review | Brief text note |
| Objective: Vitals | BP, position, respiration, temperature, pulse, height, weight, BMI |
| Objective: Physical Exam | General and eyes exam findings (free text) |
| Assessment: Diagnosis Codes | ICD-10 codes with descriptions |
| Assessment: Procedure Codes | CPT codes with descriptions |
| Plan: Diagnostic Tests | Ordered tests with lab/facility names |
| Plan: Current Medications | Table with medication name, SIG/directions, supply, count, refills, date, status |
| Plan: Medication by Others | Same table format for externally prescribed medications |
| Plan: Plan Of Care | Care goals and health concerns with dates |
| Signature | "Electronically Signed By [Provider], MD on [date/time]" |

This is essentially a **printout of a clinical visit note** — what a clinician would see on screen during a visit.

### What is NOT in the export

Based on the B10 documentation and sample, the following are absent:

- **Billing data**: No charges, claims, superbills, payment records, or financial data
- **Insurance information**: No insurance/coverage data
- **Lab results**: No actual lab result values (only orders mentioned in the Plan section)
- **Imaging results**: No radiology or imaging reports
- **Immunization records**: Not listed in the 6 categories
- **Documents/attachments**: No scanned documents, faxes, or uploaded files
- **Referrals**: Not included
- **Patient portal communications**: Not included
- **Encounter history**: Only the selected visit(s), not a comprehensive encounter history
- **Structured clinical data**: Everything is flattened into a PDF narrative — no discrete data elements

### Vendor's own content organization

The vendor's B10 documentation uses 6 categories. Since no data dictionary exists, fields below are **inferred from the sample screenshot only**:

| Category (vendor's) | Fields (inferred) | Formally Documented | Types | Notes |
|---|---|---|---|---|
| Patient Demographics | 5 | 0 | No | Name, sex, DOB, provider, visit date |
| Allergy Details | 1 | 0 | No | Free-text list |
| Medical History | 1 | 0 | No | Free-text list with dates |
| Current Medication Details and Medication History | 7 | 0 | No | Tabular in sample |
| Visit Note Information | 6 | 0 | No | SOAP note sections (free text) |
| Vitals Information | 8 | 0 | No | Standard vital signs |

**Total inferred fields: 29. Formally documented fields: 0.** No field names, types, descriptions, or value sets are provided by the vendor.

The complete extraction is in `analysis/full-entity-inventory.json`.

### The FHIR API (for context, not the (b)(10) export)

For context, the separately documented FHIR API (`MDR-FHIR-API-Documentation.pdf`, 240 pages) supports 22 FHIR resource types across 19 clinical sections conforming to US Core 5.0.1 / USCDI v2. This covers standard clinical data (allergies, conditions, encounters, medications, observations, procedures, etc.) but, as expected for a FHIR API, does not cover billing, claims, insurance, practice management, or vendor-specific data. The FHIR API is the (g)(10) certification, not the (b)(10) EHI export.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) export covers **6 categories of clinical data**, all rendered as flat PDF text:

1. **Patient Demographics** — Basic identifying information (name, sex, DOB, provider)
2. **Allergy Details** — Simple text list of allergies
3. **Current Medication Details and Medication History** — Tabular medication list with dosing and status
4. **Diagnosis and Problem Information** — ICD-10 and CPT codes with descriptions
5. **Visit Note Information** — Full SOAP note text (the richest section)
6. **Vitals Information** — Standard vital signs

The "richest" section is the visit note, which reproduces the full SOAP note. The thinnest sections are allergies (a comma-separated list) and demographics (5 header fields).

There are no sections covering billing, claims, insurance, lab results (discrete values), imaging, immunizations, referrals, documents, or any practice management data — despite MDRhythm explicitly storing all of these.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 5 header fields in sample PDF (name, sex, DOB, provider, visit date) | Product stores full demographics including address, contacts, insurance — only basic identifiers exported |
| Encounters / visits | ⚠️ Partial | Visit date and provider shown per note; selected visits only | No comprehensive encounter history; only selected visit(s) exported |
| Problems / conditions / diagnoses | ⚠️ Partial | ICD-10 codes in Assessment section; Medical History list | Diagnoses embedded in visit notes as text; no structured problem list export |
| Medications / prescriptions | ✅ Covered | Detailed medication table with name, SIG, supply, refills, date, status | Reasonably detailed medication information in the sample |
| Allergies | ⚠️ Partial | Comma-separated text list | No severity, reaction type, onset date, or coded allergens |
| Immunizations | ❌ Not covered | Not listed in 6 categories; absent from sample | Product stores immunization data (certified for f(1) immunization registry reporting); significant gap |
| Vitals | ✅ Covered | BP, respiration, temperature, pulse, height, weight, BMI | Reasonably complete vital signs |
| Lab results | ❌ Not covered | Only lab orders appear in Plan section; no result values | Product has lab integration (per EMR page); significant gap |
| Imaging / diagnostic reports | ❌ Not covered | No imaging data in export | Product mentions document scanning capability; gap |
| Procedures | ⚠️ Partial | CPT codes listed in Assessment section | Procedure codes embedded in visit note text; no dedicated procedure records |
| Clinical notes / documents | ⚠️ Partial | Full SOAP note text exported | Visit notes included but no scanned documents, faxes, or uploaded files |
| Care plans / goals | ⚠️ Partial | Plan of Care section in sample with goals and health concerns | Embedded in visit note PDF; not structured |
| Orders / referrals | ❌ Not covered | Diagnostic test orders appear in Plan but no referral data | Product has referral management capability; gap |
| Insurance / coverage | ❌ Not covered | No insurance data in export | Product stores insurance/coverage data (visible in product pages); significant gap |
| Claims / billing | ❌ Not covered | No billing, charges, claims, or financial data | Product has full billing, claim management, and clearinghouse services; **major gap** |
| Payments | ❌ Not covered | No payment records | Product has patient ledger and accounting; significant gap |
| Consents / directives | ❌ Not covered | No consent information | N/A — unclear if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No portal messages or communications | Product has patient portal; gap if portal messages are stored |
| Specialty-specific data | N/A | None visible | Product is cross-specialty; no specialty-specific data visible in export |

**Summary: 2 of 17 applicable domains adequately covered; 5 partially covered; 8 not covered at all.**

## 6. Documentation Quality

The B10 export documentation is extremely thin:

- **3 pages total**: 1 page of instructions, 1 page with a sample screenshot, 1 blank page
- **No data dictionary**: Zero field definitions, types, descriptions, or value sets
- **No schema**: No machine-readable format definition
- **No sample data files**: The only "sample" is a screenshot of a PDF export
- **No relationships/foreign keys**: N/A — the export is a flat PDF
- **No structured format**: The export itself is a non-machine-readable PDF

A developer could not build an import from this documentation. The export produces a flat PDF that would require OCR or manual extraction to recover any data from, and there is no specification of what fields or data elements will appear in the PDF.

The FHIR API documentation (240 pages) is substantially more detailed but documents a different capability — the (g)(10) FHIR API, not the (b)(10) EHI export.

## 7. Overall Assessment

### Classification

**Minimal/stub**

The (b)(10) export is a 3-page instruction document describing how to download a flat PDF of clinical visit notes. It covers 6 categories of basic clinical data (demographics, allergies, medications, diagnoses, visit notes, vitals) with no structured output, no data dictionary, and no documentation beyond a bulleted list and a screenshot. Entire domains the product explicitly stores — billing, claims, insurance, lab results, immunizations, referrals, documents, and practice management data — are absent from the export.

### Key Findings

1. **The (b)(10) export is a flat PDF printout, not structured data.** Patient records are exported as a single PDF file from a web portal (`patientdata.mdronline.net`). This is not machine-readable and cannot be programmatically imported by another system. (Source: `MDRhythm_B10_Data_Export_Instructions.pdf`, pages 1–2)

2. **Only 6 categories of clinical data are included, covering a fraction of what MDRhythm stores.** The export lists demographics, allergies, medications, diagnoses, visit notes, and vitals. MDRhythm also stores billing records, claims, insurance data, lab results, immunizations, scanned documents, referrals, and practice management data — none of which appear in the export. (Source: B10 PDF category list vs. mdrhythm.com/products.html feature list)

3. **No data dictionary or schema exists.** The vendor provides zero field-level documentation. The only detail beyond the 6-item list is a sample screenshot showing what an exported PDF looks like. (Source: `MDRhythm_B10_Data_Export_Instructions.pdf`, 3 pages total)

4. **The export is limited to 5 patients per batch**, making bulk data portability impractical. (Source: B10 PDF, page 1: "A practice can export out maximum 5 patients per export at a time")

5. **Fees may apply for related data access.** The price transparency statement notes that the (g)(9) "all data request" requires "a fee every time such data is requested" and the (g)(10) FHIR API requires a prepaid fee. The (b)(10) export does not explicitly list fees, but the pattern of fee-gating data access is concerning. (Source: `onc-compliance.html`, items I and J)

### Summary Stats

```
Classification:  Minimal/stub
Export format:   PDF (flat, non-machine-readable)
Model type:      Clinical summary printout (not a data model export)
Entities:        6 categories listed (no formal entities/tables)
Fields:          ~29 inferred from sample screenshot (0 formally documented)
Descriptions:    0% (no field descriptions provided)
Sample data:     Screenshot only (no machine-readable sample)
Bulk export:     No (max 5 patients per batch)
Domains covered: 2 of 17 applicable domains (medications, vitals adequately; 5 more partially)
```

### Bottom Line

MDRhythm's (b)(10) export is one of the thinnest implementations encountered: a flat PDF printout of clinical visit notes with no structured data, no data dictionary, and no coverage of billing, insurance, claims, lab results, immunizations, or any practice management data — despite the product explicitly providing all of these capabilities. A patient or provider receiving this export would get a PDF of their visit notes but would be missing the majority of their electronic health information, and the data they do receive would not be importable into another system.
