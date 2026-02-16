# EHI Export Analysis: Vision Infonet Inc

**Product**: MDCare EMR/PMS  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2872.MDCa.06.02.1.250604 (CHPL #11650)

## 1. Product Context

MDCare EMR/PMS is a combined Electronic Medical Records and Practice Management System developed by Vision Infonet Inc, an Illinois-based healthcare IT and services company. The product is web-based and serves ambulatory/outpatient practices across multiple specialties (cardiology, dermatology, endocrinology, psychiatry, pulmonary, podiatry, radiology, internal medicine, family practice, critical care, geriatric/palliative care). Vision Infonet's primary business is medical billing/RCM services, and MDCare is tightly coupled with those services.

**Key data domains the product stores** (per vendor marketing and certification criteria):

- **Clinical**: Patient demographics, encounters/visit notes (SOAP notes, specialty templates), problem lists, medication lists, allergy lists, vital signs, lab orders/results, imaging (DICOM interface), prescriptions (Surescripts eRx), immunizations, clinical decision support data, care plans, family health history, implantable devices, clinical notes (multiple documentation modes including AI-generated SOAP notes in v6.0), mental/functional status assessments, health concerns
- **Billing/PM**: Insurance claims (CMS-1500), superbills, accounts receivable, payment posting, denial management, CPT/ICD coding, point-of-service collections — this is a core product capability and Vision Infonet's primary business
- **Documents**: Scanned documents, consent forms, insurance ID cards, fax records (integrated "Faxtone" fax system), consult letters
- **Communications**: Patient portal (app.mdcare.com/mdcareportal), clinical messaging between providers/staff, HIPAA-compliant email
- **Scheduling**: Appointment scheduling, multi-provider/resource scheduling (though scheduling data is generally not EHI)

The "PMS" in the product name is significant — this is explicitly an EMR **and** Practice Management System. Billing is a core function, not an ancillary feature.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/EHIexport.pdf` (5.1 MB, 19 pages) | Primary (b)(10) EHI export documentation. Contains overview, UI screenshots with annotated export workflow, and C-CDA data dictionary (pages 12–19). Created 2023-11-29, references MDCare V5.1. | **Most informative** — sole source of (b)(10) export detail |
| `downloads/APIDocument.pdf` (1.4 MB, 54 pages) | FHIR R4 SMART on FHIR API documentation for (g)(10). Covers OAuth 2.0 auth, FHIR resource examples. Created 2024-12-05. | Low — documents (g)(10) API, not (b)(10) export |
| `downloads/API.json` (4 KB) | FHIR R4 Bundle with Endpoint/Organization for fhir.mdcare.com. | Minimal — (g)(10) service base URL only |

Note: The APIDocument.pdf is actually 54 pages (not 20 as stated in the prior report's files.json description), per `pdfinfo` output. The prior report's page count was incorrect.

## 3. Export Mechanics

- **Format**: C-CDA (Consolidated CDA) per §170.205(a)(4), HL7 CDA R2 DSTU R2.1 (August 2015). Output delivered as a ZIP file containing three representations per encounter: C-CDA XML, PDF, and HTML. Also includes "all scanned clinical and administrative documents."
- **Standard referenced**: USCDI Version 1 (not the current USCDI v3)
- **Mechanism**: Dedicated UI feature at Home → Records Tab → "EHI-Export" → "Add Request." Not API-based.
- **Single-patient**: Search by patient name, select specific encounter(s) or all encounters. Download or Export button generates ZIP.
- **Bulk export**: Select "Multiple Patients," specify date range, resource, and physicians. Generates one ZIP per patient.
- **Access constraints**: Role-based — documentation states "Based on specific user roles, this helps the clinical users to generate the Clinical Care Document." No mention of fees or processing time.
- **Version note**: Documentation references V5.1; current certified version is V6.0 (certified June 2025). The PDF was created November 2023 and has not been updated.

## 4. Export Content: What's In It

The export is a C-CDA document with a data dictionary documented on pages 12–19 of EHIexport.pdf. There is no sample data, no machine-readable schema, and no product-specific data dictionary beyond the C-CDA section listing.

### Data Dictionary Metrics

- **Sections (entities)**: 24 C-CDA sections
- **Total fields**: 82 data elements across all sections
- **Fields with XPATH references**: 30 (36.6%)
- **Fields with code system references**: 27 (32.9%)
- **Fields with descriptions**: 0 — no field has a prose description; fields are identified by name only
- **Field types**: Not documented
- **Relationships/foreign keys**: Not documented (inherent in C-CDA structure)
- **Value sets**: Code system OIDs are listed (SNOMED, ICD-10, LOINC, RxNorm, NDC, CVX, CPT-4, HCPCS, NCI Thesaurus) but specific value set bindings are not documented

### UI Checkboxes vs Data Dictionary

The UI screenshot (page 4) shows a "C-CDA/Referral Summary" panel with ~41 selectable data categories, all checked by default. Several UI items are NOT individually documented in the data dictionary on pages 12–19:

- Medication Administered
- Diagnostic Pending Test
- Future Scheduled Tests
- Future Appointments
- Recommended Patient Decision Aids
- Assessment
- Interventions
- General Status
- Physical Exam
- HPI (History of Present Illness)
- ROS (Review of Systems)
- Past Medical History
- Clinical Notes

Some of these (e.g., Future Appointments, Diagnostic Pending Test) are covered under the "Treatment Plan" section in the data dictionary, but the per-item documentation is absent for many.

### Vendor's Own Content Organization

The data dictionary is organized by C-CDA section. All content is clinical:

| C-CDA Section | Fields | With XPATH | With Code System | Category |
|---|---|---|---|---|
| Patient Demographics/Information | 6 | 6 | 3 | Demographics |
| Provider Information | 3 | 3 | 0 | Provider |
| Date and Location of Visit | 2 | 2 | 0 | Encounters |
| Chief Complaint and Reason for Visit | 1 | 0 | 0 | Encounters |
| Encounters | 5 | 1 | 2 | Encounters |
| Immunizations | 9 | 1 | 3 | Clinical |
| Instructions | 1 | 1 | 1 | Clinical |
| Treatment Plan | 2 | 2 | 1 | Clinical |
| Social History | 3 | 1 | 2 | Clinical |
| Problems | 3 | 1 | 1 | Clinical |
| Medications | 5 | 1 | 1 | Clinical |
| Medication Allergies | 4 | 1 | 4 | Clinical |
| Laboratory Tests | 4 | 0 | 1 | Labs |
| Laboratory Information | 5 | 0 | 0 | Labs |
| Laboratory Values/Results | 5 | 1 | 1 | Labs |
| Vitals | 2 | 1 | 1 | Clinical |
| Goals | 3 | 1 | 0 | Clinical |
| Procedures | 2 | 1 | 1 | Clinical |
| Care Team Members | 3 | 1 | 0 | Clinical |
| Reason for Referral | 1 | 1 | 1 | Clinical |
| Medical Equipment | 2 | 1 | 1 | Clinical |
| Mental Status | 4 | 1 | 1 | Assessments |
| Functional Status | 4 | 1 | 1 | Assessments |
| Health Concern | 3 | 1 | 1 | Clinical |
| **TOTAL** | **82** | **30** | **27** | |

The full machine-readable inventory is at `analysis/entity-inventory-full.json`.

### Additional Export Content (Not in Data Dictionary)

The documentation states the ZIP includes "all scanned clinical and administrative documents for the patient in C-CDA, PDF, and XML formats." The UI shows checkboxes for "Medical Records," "Patient Demographics," and "All POS Documents." There is no documentation of what "All POS Documents" includes, how scanned documents are organized, or what metadata accompanies them.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is organized entirely around C-CDA sections — there is no vendor-specific data model exposed. The 24 documented sections map directly to standard C-CDA clinical document sections. The content is clinical in nature with no billing, insurance, or administrative data beyond basic demographics and encounter codes.

The richest sections are:
- **Immunizations** (9 fields) — includes vaccine, date, status, route, site, manufacturer, dose, lot number, notes
- **Patient Demographics** (6 fields) — name, sex, DOB, race, ethnicity, preferred language
- **Medications** (5 fields) and **Laboratory Values/Results** (5 fields) — standard clinical data

The thinnest sections are:
- **Chief Complaint** (1 field, no XPATH, no code system)
- **Instructions** (1 field)
- **Reason for Referral** (1 field)

No section addresses billing, claims, insurance, payments, or any practice management data.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient Demographics section (6 fields: name, sex, DOB, race, ethnicity, language). No address, phone, email, emergency contacts, or insurance info. | Basic USCDI demographics only; thin for a product that stores full registration data |
| Encounters / visits | ✅ Covered | Date and Location of Visit, Encounters sections (7 fields total). CPT encounter codes, performer, diagnosis, location. | Standard C-CDA encounter coverage |
| Problems / conditions | ✅ Covered | Problems section (3 fields: problem code SNOMED/ICD-10, status, active date) | Standard C-CDA coverage |
| Medications / prescriptions | ✅ Covered | Medications section (5 fields: medication RxNorm/NDC, directions, start/end date, status) | Standard C-CDA; no Surescripts eRx transaction history |
| Allergies | ✅ Covered | Medication Allergies section (4 fields: substance, reaction, severity, status) | Standard C-CDA |
| Immunizations | ✅ Covered | Immunizations section (9 fields including vaccine, route, site, manufacturer, dose, lot) | Reasonably detailed |
| Vitals | ✅ Covered | Vitals section (2 fields: observation LOINC, date/time) | Standard C-CDA |
| Lab results | ✅ Covered | Laboratory Tests, Laboratory Information, Laboratory Values/Results (14 fields total) | Standard C-CDA lab coverage |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging section. Product has DICOM interface; unclear if imaging reports are in export. UI shows "Diagnostic Pending Test" checkbox. | Product has DICOM interface — imaging data may not be fully captured |
| Procedures | ✅ Covered | Procedures section (2 fields: procedure CPT-4/SNOMED/HCPCS, date) | Standard C-CDA |
| Clinical notes / documents | ⚠️ Partial | UI shows "Clinical Notes" checkbox. Documentation says ZIP includes "scanned clinical and administrative documents." No detail on note types or structure. | Scanned documents included but no documentation of what's captured |
| Care plans / goals | ✅ Covered | Treatment Plan (2 fields), Goals (3 fields), Health Concern (3 fields) | Standard C-CDA |
| Orders / referrals | ⚠️ Partial | Reason for Referral (1 field). UI shows "Referrals" checkbox. No lab/imaging order detail beyond results. | Minimal referral coverage |
| Insurance / coverage | ❌ Not covered | No insurance entities in the data dictionary. Demographics don't include insurance fields. | **Significant gap** — product stores insurance data for billing/claims |
| Claims / billing | ❌ Not covered | No claims, superbills, CMS-1500, or billing entities anywhere in export documentation | **Critical gap** — product is explicitly an EMR/**PMS** with integrated billing as a core function |
| Payments | ❌ Not covered | No payment, AR, collection, or denial management data | **Significant gap** — product handles payment posting, AR, denial management |
| Consents / directives | ⚠️ Partial | UI tab shows "Advance Directives" in the Records module. Not documented in the data dictionary. Scanned consent forms may be included as documents. | Unclear coverage |
| Patient communications | ❌ Not covered | No portal messages, clinical messages, or communication data | Product has patient portal and clinical messaging — gap |
| Specialty-specific data | ❌ Not covered | No specialty-specific data structures despite product marketing specialty versions for cardiology, dermatology, psychiatry, etc. | Product has specialty templates — none appear in export beyond standard C-CDA |

## 6. Documentation Quality

**Overall quality: Low-to-moderate.**

**Strengths:**
- Clear step-by-step UI instructions with annotated screenshots for both single-patient and bulk export workflows
- A data dictionary listing all C-CDA sections with XPATHs and code system OIDs
- The UI screenshot reveals ~41 selectable data categories, providing visibility into export scope

**Weaknesses:**
- **No field descriptions**: All 82 data elements are listed by name only — no prose descriptions explaining what each field contains, its format, or its semantics
- **No data types**: No field typing documented
- **No sample data**: No example export files provided
- **No machine-readable schema**: The data dictionary is only available as a PDF table
- **Incomplete**: The data dictionary (pages 12–19) documents only 24 sections, while the UI shows ~41 selectable categories — at least 13 UI items have no corresponding data dictionary documentation
- **Outdated**: References V5.1 and USCDI v1; current product is V6.0 (certified June 2025) and USCDI v3 is now mandatory
- **No ZIP structure documentation**: States exports include "scanned clinical and administrative documents" but provides no specification of how these are organized, named, or indexed

A developer could not build an import from this documentation alone. The data dictionary provides C-CDA section names and code systems, but without field types, cardinality, optionality, value set bindings, or sample data, meaningful ingestion would require reverse-engineering the C-CDA output.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers standard clinical data domains (demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, care plans, assessments) but completely omits billing and practice management data. This is a significant gap because MDCare is explicitly an EMR/**PMS** — the "PMS" (Practice Management System) means billing, claims, insurance, payments, and revenue cycle management are core product functions. Vision Infonet's primary business is medical billing services, making the absence of billing data from the (b)(10) export particularly notable. Insurance/coverage data, patient communications, and specialty-specific structured data are also absent. The export covers clinical domains at a USCDI-level depth but does not go meaningfully beyond USCDI into the full designated record set.

**Axis 2 — Export approach: Repackaged existing export**

The export is a C-CDA document — the same format used for clinical document exchange under (b)(1) Transitions of Care. The data dictionary maps directly to standard C-CDA sections with standard code systems, referencing USCDI v1 and the 2015 C-CDA IG. There is no product-specific data model, no vendor-specific extensions, no coverage of data domains beyond what C-CDA naturally supports. The vendor did build a dedicated "EHI-Export" UI feature (not just reusing the FHIR g(10) API), which shows some effort, but the underlying export content is a C-CDA clinical summary — the same artifact type used for transitions of care. The inclusion of "scanned clinical and administrative documents" in the ZIP is a positive addition beyond pure C-CDA, but it's undocumented and doesn't change the fundamental character of the export as a clinical summary repackaged for (b)(10).

### Key Findings

1. **Export is a C-CDA clinical summary, not a comprehensive EHI export.** 24 C-CDA sections with 82 data elements covering standard clinical domains. No billing, insurance, payment, or practice management data despite the product being an EMR/PMS with billing as a core function. (Source: `downloads/EHIexport.pdf`, pages 12–19)

2. **Critical billing gap for a billing-centric vendor.** Vision Infonet's primary business is medical billing/RCM services, and MDCare includes integrated billing (CMS-1500 claims, AR, superbills, denial management, payment posting). None of this data appears in the export. This is the single largest gap. (Source: product-research.md; absence in EHIexport.pdf)

3. **Data dictionary is incomplete relative to UI.** The UI shows ~41 selectable data categories, but the data dictionary only documents 24 sections. Items like Clinical Notes, HPI, ROS, Past Medical History, Physical Exam, Assessment, Interventions, and General Status appear in the UI but have no data dictionary entries. (Source: EHIexport.pdf page 4 screenshot vs pages 12–19)

4. **Documentation is outdated.** The PDF references V5.1 (November 2023), but the current certified version is V6.0 (June 2025). It references USCDI v1, while USCDI v3 is now required. No updates appear to have been made in over 2 years. (Source: EHIexport.pdf page 1 vs metadata.json certification date)

5. **No sample data or machine-readable artifacts.** There are no sample export files, no JSON/XML schemas, and no documentation of the ZIP file structure. A developer would need access to the actual system to understand the export output. (Source: absence in downloads/)

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   C-CDA (XML, PDF, HTML) + scanned documents in ZIP
Entities:        24 C-CDA sections
Fields:          82
Descriptions:    0% (no field descriptions; names and code systems only)
Sample data:     No
Bulk export:     Yes (multi-patient by date range)
Domains covered: 8 of 15 applicable domains (fully); 4 partial; 3 not covered
```

### Bottom Line

The MDCare EMR/PMS EHI export is a C-CDA clinical summary repackaged as a (b)(10) export. It covers standard clinical data at USCDI depth but completely omits billing, insurance, and practice management data — a critical gap for a product whose name literally includes "PMS" (Practice Management System) and whose parent company's primary business is medical billing services. A patient or provider would receive their clinical chart but not their billing history, insurance records, claims, payments, or any specialty-specific structured data.
