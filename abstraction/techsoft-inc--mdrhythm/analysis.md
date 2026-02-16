# EHI Export Analysis: TechSoft, Inc.

**Product**: MDRhythm Version 8
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2413.MDRh.08.00.1.181208

## 1. Product Context

MDRhythm is a fully integrated EMR/EHR and Practice Management system developed by TechSoft, Inc. (Marlton, NJ), in use since 1992. The practice management/billing system is the original core of the product, with the EMR component added around 1999. It targets small-to-midsize ambulatory practices and free/charitable clinics.

**Data domains the product stores** (based on product research, CHPL certifications, FHIR API documentation, and patient portal capabilities):

- **Clinical**: Problems/conditions, allergies, medications (including EPCS for controlled substances), immunizations, vital signs, lab results, diagnostic reports, procedures, goals, care plans, care teams, clinical notes (SOAP format), devices/UDI
- **Practice Management & Billing**: Patient scheduling, medical billing, claims processing, insurance/coverage information, prior authorizations — this is the *original core* of the product
- **Prescriptions/Pharmacy**: E-prescribing including controlled substances (EPCS), pharmacy and inventory control for dispensing clinics
- **Document Management**: Faxing, document scanning, transcription management
- **Patient Portal ("MDR Online")**: Lab results, medication lists, allergies, appointment scheduling, prescription refill requests, patient health profile, secure messaging
- **Interoperability**: C-CDA documents, Direct messaging, public health reporting (immunization registries, syndromic surveillance, cancer registries)
- **FHIR API**: 20 USCDI-scope FHIR R4 resource types (documented in 240-page API guide)

The key question for (b)(10) is whether the export covers the billing/PM core, pharmacy/inventory, document management, and patient portal data — or only the clinical EMR layer.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/MDRhythm B10 Data Export Instructions.pdf` (573 KB, 3 pages) | The primary (b)(10) documentation. Describes the PDF-based export via the Practice Patient Data web portal. Lists 6 data categories and includes one sample export screenshot. | **Primary artifact** — but extremely thin |
| `downloads/MDR-FHIR-API-Documentation.pdf` (1.1 MB, 240 pages) | FHIR R4 API documentation for (g)(10). Covers 20 USCDI resource types with request/response examples. US Core 5.0.1 profiles. | Useful for comparison — shows the FHIR API scope, which is entirely USCDI-clinical |
| `downloads/onc-compliance.html` (18 KB) | The ONC compliance page at mdrhythm.com. Contains disclosure statement, links to FHIR API and B10 export PDFs. | Minimal — confirms the B10 PDF is the sole (b)(10) documentation |
| `downloads/onc-compliance-page-screenshot.png` (472 KB) | Screenshot of the compliance page. | Minimal — visual confirmation only |

## 3. Export Mechanics

- **Format**: PDF — a rendered, non-machine-readable document format
- **Mechanism**: Web portal at `https://patientdata.mdronline.net`. Practice users log in with practice credentials, select patients from a list, and click "Export EHR."
- **Scope**: Single or multi-patient (up to 5 patients per export batch). All selected patients are exported into one PDF file named with a unique practice code.
- **Access**: Practice-level login required. No patient self-service export documented.
- **Bulk capability**: Limited to 5 patients at a time "to save system resources." No true bulk export mechanism.
- **Fees**: Not mentioned for (b)(10). The (g)(10) FHIR API has fees noted on the compliance page.

## 4. Export Content: What's In It

### Data dictionary status

**There is no data dictionary.** The B10 documentation is a 3-page PDF with:
- 1 page of instructions (steps 1-5)
- 1 page with a sample export screenshot showing one patient's data
- 1 blank page

The documentation explicitly lists 6 data categories that the export contains:
1. Patient Demographics
2. Allergy Details
3. Current Medication Details and Medication History
4. Diagnosis and Problem Information
5. Visit Note Information
6. Vitals Information

### Sample export analysis (from screenshot on page 2-3)

The sample export shows a visit record for patient "AA Hayword M" with provider "Max Burger, MD," visit date 11/07/2022. The content is a rendered SOAP note with embedded data:

**Demographics** (header): Patient name, Sex (Male), DOB (10/01/2000), Visit Date. No address, phone, email, insurance, or other demographic fields.

**Allergies** (Subjective section): Listed as text — "Amoxicillin, Apples, Beer, Shampoo." No severity, reaction, onset, or status information.

**Medical History** (Subjective section): A list of conditions with dates — e.g., "Acute and subacute liver necrosis," "Anxiety started 1/27/2016 test 1," "Bipolar disorder started 1/27/2014 test 3," etc.

**Vitals** (Objective section): BP 130/76 mmHg L Arm Sitting, Respiration 14 Unlabored, Temperature 98.4°F, Pulse 98 Regular/min, Height 5-9.0" (46%), Weight 160 Lbs, BMI 23.63 (70%). Displayed as a single line of text.

**Physical Exam** (Objective section): Free-text examination findings — General inspection, Eyes, Pupils.

**Assessment**: Diagnosis codes with descriptions (ICD codes visible, e.g., "G8112 Spastic hemiplegia affecting left dominant side") and Procedure codes (CPT codes, e.g., "99213 OFFICE/OUTPATIENT VISIT, NEW").

**Plan**: Diagnostic tests, Current Medications table (columns: Medication, SIG/Directions, Supply, Count, Refills, Date, Status), Medication by Others table (same columns), Plan of Care entries, Goals, Health Concerns, Electronic signature.

### Vendor's own content organization

| Entity/Category | Fields Visible | Types Documented | Category |
|---|---|---|---|
| Patient Demographics | 3 (name, sex, DOB) | No | Demographics |
| Allergy Details | 1 (allergen name) | No | Allergies |
| Current Medications | 7 (med, SIG, supply, count, refills, date, status) | No | Medications |
| Diagnosis/Problem Information | 2 (medical history list, diagnosis codes) | No | Diagnoses/Problems |
| Visit Note Information | 11 (visit date, provider, SOAP sections, procedures, plan of care, goals, concerns, signature) | No | Clinical Notes |
| Vitals Information | 8 (BP, arm/position, respiration, temp, pulse, height, weight, BMI) | No | Vitals |

**Totals**: 6 entities, 32 observable fields (from sample screenshot). No field types, no data types, no relationships, no value sets, no foreign keys documented. Zero fields have formal documentation beyond what can be inferred from column headers in the sample screenshot.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) export covers **6 clinical data categories**, all rendered as a PDF visit note. This is essentially a printed chart note with embedded medication lists and diagnosis codes. The content maps closely to what a clinician would see in a single visit encounter in the EMR.

The export is:
- **Shallow within covered domains**: Demographics shows only 3 fields (name, sex, DOB) despite the product storing full demographic records including address, contacts, insurance, and guarantor information. Allergies show only allergen names with no severity, reaction, or status. Vitals are rendered as a single text line.
- **Narrow across domains**: Only 6 of the product's many data domains are covered. The entire practice management/billing core — the original foundation of the product — is absent.

The medications section is the deepest, showing a 7-column table with directions, supply, refills, dates, and status. This is the only tabular data in the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 3 fields (name, sex, DOB) in export header | Product stores full demographics including address, contacts, insurance, guarantor. Major gap. |
| Encounters / visits | ⚠️ Partial | Visit date and provider name visible in note header | Visit structure exists but no encounter-level metadata (type, status, duration, location). |
| Problems / conditions | ⚠️ Partial | Medical History list and Diagnosis Codes in Assessment | Conditions listed but minimal structure — no onset dates consistently, no status, no severity. |
| Medications / prescriptions | ✅ Covered | Current Medications table (7 columns) + Medication by Others | Reasonable depth for current meds. Prescription details (prescriber, pharmacy, DEA) not visible. |
| Allergies | ⚠️ Partial | Allergen names listed as text | No severity, reaction type, onset, or clinical status. Minimal. |
| Immunizations | ❌ Not covered | Not present in export | Product stores immunizations (certified (f)(1), in FHIR API). Significant gap. |
| Vitals | ✅ Covered | BP, respiration, temp, pulse, height, weight, BMI | Rendered as text within visit note. Reasonable coverage for a single encounter. |
| Lab results | ❌ Not covered | Not present in export | Product stores lab results (in FHIR API, patient portal). Significant gap. |
| Imaging / diagnostic reports | ❌ Not covered | Not present in export | Product has DiagnosticReport in FHIR API. Gap. |
| Procedures | ⚠️ Partial | Procedure codes listed in Assessment section | CPT codes visible but no procedure details, dates, or outcomes. |
| Clinical notes / documents | ✅ Covered | SOAP visit notes with provider signature | Core strength of the export. Full SOAP notes rendered in the PDF. |
| Care plans / goals | ⚠️ Partial | Plan of Care, Goals, Health Concerns in Plan section | Listed as text items but minimal structure. |
| Orders / referrals | ⚠️ Partial | "Diagnostic Tests" section in Plan | Orders listed by name but no structured order details or referral tracking. |
| Insurance / coverage | ❌ Not covered | Not present in export | Product manages insurance/coverage (PM core, FHIR Coverage). Significant gap. |
| Claims / billing | ❌ Not covered | Not present in export | Billing is the *original core* of MDRhythm (PM system since 1992). **Critical gap.** |
| Payments | ❌ Not covered | Not present in export | Product handles billing/payments. Gap. |
| Consents / directives | ❌ Not covered | Not present in export | N/A — no evidence product stores these beyond standard intake. |
| Patient communications / portal | ❌ Not covered | Not present in export | Product has patient portal (MDR Online) with messaging. Gap. |
| Pharmacy / inventory | ❌ Not covered | Not present in export | Product has pharmacy/inventory module. Gap. |
| Scanned documents / media | ❌ Not covered | Not present in export | Product has document scanning and fax management. Gap. |
| Devices / UDI | ❌ Not covered | Not present in export | Product certified for (a)(14) UDI. Gap. |

**Summary**: 3 of 19 applicable domains covered, 5 partially covered, 11 not covered at all.

## 6. Documentation Quality

The (b)(10) documentation is **severely inadequate**:

- **No data dictionary**: No field names, types, descriptions, value sets, or relationships are documented anywhere. The only reference is the 6-item bulleted list of data categories and one screenshot.
- **No machine-readable artifacts**: The export itself is PDF (not machine-readable), and no schema, JSON, CSV, or structured format is provided.
- **No sample data file**: Only a screenshot of a sample export embedded in the instructions PDF. No actual downloadable sample.
- **No import guidance**: A developer could not build an import tool from this documentation. The export is a rendered PDF with no consistent structure or parsing specification.
- **3 pages total**: The entire (b)(10) documentation fits on 3 pages (one of which is blank), compared to 240 pages for the (g)(10) FHIR API documentation.

The FHIR API documentation (240 pages) is far more thorough but is explicitly (g)(10) documentation, not (b)(10). It covers only USCDI-scope clinical data and makes no reference to billing, PM, or operational data.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub**

The export covers only 6 clinical data categories, all rendered as a non-machine-readable PDF. This is far less than even the product's FHIR API (g)(10) surface, which covers 20 resource types. The entire practice management and billing system — the original core of MDRhythm dating to 1992 — is completely absent. Immunizations, lab results, imaging, insurance, patient portal data, scanned documents, pharmacy/inventory, and device data are all missing despite the product storing them. The export is essentially a printed visit note, not an EHI export.

**Axis 2 — Export approach: Repackaged existing export**

The (b)(10) export appears to be the product's existing "print patient chart" or "export visit note" functionality relabeled as an EHI export. Key signals:
- The output format is PDF — a rendered document, not structured data
- The content matches what a clinician would see printing a patient encounter
- There is no data dictionary, no schema, no structured format
- The web portal (`patientdata.mdronline.net`) is labeled "Practice Patient Data" — suggesting it predates (b)(10) compliance
- The export covers less than the (g)(10) FHIR API, which itself covers only USCDI
- No billing, PM, or operational data is included despite these being the product's foundational capabilities

This is not a purpose-built EHI export. It is a minimal clinical summary in PDF format dressed up as (b)(10) compliance.

### Key Findings

1. **Export is a PDF, not structured data.** The (b)(10) export produces a non-machine-readable PDF file. No JSON, CSV, XML, FHIR, or other parseable format is offered. This makes the export unsuitable for data portability or downstream processing.

2. **Only 6 clinical categories covered; billing/PM core entirely absent.** MDRhythm's founding product is its practice management and billing system (since 1992). The (b)(10) export includes zero billing, claims, insurance, payment, or PM data. This is the most critical gap — the product's most mature and extensive data domain is completely excluded.

3. **Export covers less than the existing (g)(10) FHIR API.** The FHIR API supports 20 resource types including immunizations, lab results, devices, care plans, and encounters. The (b)(10) export covers only 6 categories, making it a strict subset of the (g)(10) surface. The vendor did not even repackage their FHIR API as (b)(10) — they provided something even narrower.

4. **No data dictionary or schema.** The entire (b)(10) documentation is 3 pages (1 blank) with step-by-step instructions and a single screenshot. No field definitions, no data types, no relationships, no value sets. A developer cannot build anything from this documentation.

5. **5-patient batch limit.** The export is capped at 5 patients per batch "to save system resources," making bulk export of a practice's patient population impractical.

### Summary Stats

```
Coverage:        Minimal/stub
Approach:        Repackaged existing export
Export format:   PDF (non-machine-readable)
Entities:        6 (clinical categories only)
Fields:          ~32 (observable from sample screenshot; no formal data dictionary)
Descriptions:    0% (no data dictionary exists)
Sample data:     Screenshot only (no downloadable sample)
Bulk export:     No (5-patient limit per batch)
Domains covered: 3 of 19 applicable domains (+ 5 partial)
```

### Bottom Line

MDRhythm's (b)(10) export is a minimal PDF printout of clinical visit notes — not a genuine EHI export. The product's core practice management and billing data (its original and most mature capability since 1992) is entirely excluded, along with immunizations, lab results, insurance, patient portal data, scanned documents, and pharmacy/inventory data. The single biggest gap is the complete absence of structured, machine-readable data export in any format.
