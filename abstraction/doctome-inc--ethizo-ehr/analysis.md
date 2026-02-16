# EHI Export Analysis: DocToMe, Inc.

**Product**: ethizo EHR
**Analysis date**: 2026-02-16
**CHPL IDs**: 10265 (15.05.05.3060.DOTM.01.00.1.200107)

## 1. Product Context

ethizo EHR is a cloud-based, ONC-certified EHR and practice management platform developed by DocToMe, Inc., a very small vendor (~5–9 employees) based in Gig Harbor, WA. Despite its small size, ethizo is certified across an unusually broad range of ONC criteria and targets ambulatory practices, FQHCs, and post-acute/long-term care (PALTC) settings across 20+ specialties.

**Modules and data domains relevant to EHI export completeness:**

- **Core EHR**: Clinical documentation, problem lists, medications, allergies, vitals, labs, immunizations, procedures, care plans, goals, referrals, clinical decision support, implantable devices
- **Practice Management System (PMS)**: Full billing and revenue cycle — claims scrubbing, clearinghouse connectivity, ERA posting, CPT macros, eligibility verification, copay collection, PCI-compliant payment processing, patient statements, revenue KPIs
- **Patient Portal**: Appointment booking, medication tracking, secure messaging, questionnaires, Fitbit/device integration
- **Vezo (Telemedicine)**: Virtual visits, transit notes, video calls
- **Hybrid eFax**: Fax/email/e-signature document management
- **CCM (Chronic Care Management)**: Care plans, enrollment, activity logs, automated billing
- **RPM (Remote Patient Monitoring)**: BP, glucose, CGM, SpO2, weight, temp, HR, ECG from connected devices
- **ePrescribing with PDMP**: Controlled substance prescribing with PDMP integration
- **MIPS**: Quality measure tracking and reporting

This is a full-stack product — a genuine export should cover clinical data, billing/financial data, patient communications, documents, telehealth records, RPM data, and CCM activity.

## 2. Artifacts Reviewed

| Artifact | Description | Informational Value |
|---|---|---|
| `downloads/EHI-Export-b.10-Documentation-v2.pdf` | 9-page PDF (311 KB, created 2025-03-01). Core EHI export documentation: overview, export process instructions, CDA data dictionary with XPATH paths and code systems, brief mention of CSV and document components, one-sentence FHIR mention. | **Primary artifact** — contains all export documentation |
| `downloads/ehi-export-landing-page.png` | Screenshot of the EHI export landing page at ethizo.com. Shows page title and single download link to the PDF. | Low — confirms the page is simple with only the PDF link |
| `product-research.md` | Prior research on ethizo's modules, market, and data domains | Useful for establishing baseline of what the product stores |
| `ehi-export-report.md` | Prior agent's narrative analysis of the export documentation | Useful for orientation; independently verified all claims |
| `files.json` | Manifest of collected artifacts | Confirms only 2 artifacts were downloaded |

## 3. Export Mechanics

- **Format**: Multi-format ZIP containing:
  1. CDA XML (C-CDA R2.1) — clinical data
  2. CSV — demographics/insurance and appointments
  3. PDF/JPG/PNG — scanned documents
- **Alternative pathway**: FHIR Bulk Data mentioned in one sentence; undocumented
- **Mechanism**: UI-based ("Share Data" feature)
  - Single patient: Search patient → Share Data → select sections → Process → receive secure link via email/text → download ZIP
  - Bulk/population: Quick Links → Share Data → select EHI export → Process → secure link → download ZIP of ZIPs
- **Access constraints**: Requires authenticated login; file delivery via secure email/text link with token
- **Fees**: Not mentioned

## 4. Export Content: What's In It

The export documentation is contained in a single 9-page PDF. The primary clinical data export uses C-CDA R2.1, supplemented by two undocumented CSV files and scanned documents.

### CDA Clinical Document

The CDA data dictionary maps **24 sections** containing **82 data elements** across standard CCD sections. Of these 82 fields:
- **30 fields** (37%) have XPATH paths or template IDs documented
- **27 fields** (33%) have code system OIDs specified
- The remaining fields list only a name with no XPATH or code system

**12 code systems** are referenced: SNOMED CT, ICD-10, LOINC, RxNorm, NDC, CPT/CPT-4, CVX, HCPCS, GMDN, AdministrativeGender, CDC Race & Ethnicity, and NCI Thesaurus.

No field types, descriptions (beyond the name), value set bindings, nullability, or example values are provided. The documentation maps elements to their CDA structure but does not describe what each element means or what values it can take.

### CSV Components

Two CSV files are mentioned:
1. **Patient Demographics and Insurance Details** — described only as "CSV, comma-separated" with "comprehensive view of demographics and insurance details." Zero field documentation.
2. **Appointments** — "comprehensive view of all future appointments details." Zero field documentation. Notably limited to **future** appointments only.

### Scanned Documents

PDF, JPG, and PNG files organized by patient chart number with category subfolders (e.g., Lab Reports, Radiology, Scanned Receipts). Includes signed progress notes, lab results, radiology reports, and other uploaded documents. No metadata schema documented.

### FHIR Bulk Data

A single sentence: "ethizo FHIR server can creates a single-patient FHIR resource Document Reference as well as supports FHIR Bulk Data EHI Export for patient population as described in §170.315(b)(10)(ii)." No endpoints, authentication, resource types, or any other detail is provided. The FHIR API documentation at fhir-api.ethizo.com (per the prior report) lists only standard US Core resources with no billing or EHI-specific extensions.

### Vendor's own content organization

| Entity/Table | Fields | Fields with Code Systems | Format | Category (vendor's) |
|---|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | CDA XML | Clinical Data |
| Provider's name and office contact | 3 | 0 | CDA XML | Clinical Data |
| Date and Location of visit | 2 | 0 | CDA XML | Clinical Data |
| Chief Complaint and Reason for visit | 1 | 0 | CDA XML | Clinical Data |
| Encounters | 5 | 2 | CDA XML | Clinical Data |
| Immunizations | 9 | 3 | CDA XML | Clinical Data |
| Instructions | 1 | 1 | CDA XML | Clinical Data |
| Treatment Plan | 2 | 1 | CDA XML | Clinical Data |
| Social History | 3 | 2 | CDA XML | Clinical Data |
| Problems | 3 | 1 | CDA XML | Clinical Data |
| Medications | 5 | 1 | CDA XML | Clinical Data |
| Medication Allergies | 4 | 3 | CDA XML | Clinical Data |
| Laboratory Tests | 4 | 1 | CDA XML | Clinical Data |
| Laboratory Information | 5 | 0 | CDA XML | Clinical Data |
| Laboratory value(s)/result(s) | 5 | 1 | CDA XML | Clinical Data |
| Vitals | 2 | 1 | CDA XML | Clinical Data |
| Goal | 3 | 0 | CDA XML | Clinical Data |
| Procedures | 2 | 1 | CDA XML | Clinical Data |
| Care team member(s) | 3 | 0 | CDA XML | Clinical Data |
| Reason for Referral | 1 | 1 | CDA XML | Clinical Data |
| Medical Equipment | 2 | 1 | CDA XML | Clinical Data |
| Mental Status | 4 | 1 | CDA XML | Clinical Data |
| Functional Status | 4 | 1 | CDA XML | Clinical Data |
| Health Concern | 3 | 1 | CDA XML | Clinical Data |
| Patient Demographics and Insurance Details | 0 (undocumented) | 0 | CSV | Demographics / Insurance |
| Appointments | 0 (undocumented) | 0 | CSV | Scheduling |
| Scanned Documents | 3 (organizational only) | 0 | PDF/JPG/PNG | Documents |
| FHIR Bulk Data Export | 0 (undocumented) | 0 | FHIR R4 | Alternative Pathway |

**Totals**: 28 entities/components, 82 documented CDA fields, 0 documented CSV fields, 27 fields with code systems (33% of CDA fields).

Full inventory saved to `analysis/entity-inventory-full.json`; summary statistics in `analysis/entity-inventory-summary.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into four categories:

1. **Clinical Data in CDA Format** — The deepest component. 24 CDA sections covering standard clinical summary domains: demographics, encounters, immunizations, medications, allergies, problems, labs, vitals, procedures, goals, care team, referrals, devices, social history, mental/functional status, and health concerns. This maps directly to C-CDA R2.1 section templates — it is a standard Continuity of Care Document, not a custom export.

2. **Patient Demographics and Insurance Details (CSV)** — Mentioned as "comprehensive" but completely undocumented. May extend beyond the CDA demographics to include insurance coverage details, but there is no way to verify from the documentation.

3. **Appointments (CSV)** — Future appointments only. Undocumented fields. Past visit history would be in the CDA encounters section.

4. **Documents** — Scanned/uploaded files (notes, lab reports, radiology, receipts). This is the most genuinely "all EHI" component — it captures whatever has been filed to the patient's chart regardless of category.

The richest section is Clinical Data (82 fields across 24 CDA sections). The thinnest components are the two CSV files (zero documented fields) and the FHIR pathway (one sentence).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CDA: 6 fields (name, sex, DOB, race, ethnicity, language). CSV: "demographics" mentioned but undocumented | CDA covers USCDI demographics. CSV may have more but is unverifiable. No address, phone, email, emergency contacts documented in CDA. |
| Encounters / visits | ✅ Covered | CDA Encounters section (code, performer, diagnosis, location, date) using CPT, SNOMED, ICD-10 | Standard encounter data. Depth is thin (5 fields). |
| Problems / conditions | ✅ Covered | CDA Problems section (problem, status, active date) with SNOMED + ICD-10 | 3 fields — minimal but functional. |
| Medications / prescriptions | ✅ Covered | CDA Medications section (medication, directions, start/end date, status) with RxNorm + NDC | 5 fields. Does not distinguish ePrescribing/EPCS-specific data or PDMP records. |
| Allergies | ✅ Covered | CDA Medication Allergies (substance, reaction, severity, status) with RxNorm + SNOMED | 4 fields — standard allergy documentation. |
| Immunizations | ✅ Covered | CDA Immunizations (vaccine, date, status, route, site, manufacturer, dose, lot, notes) with CVX + CPT-4 | 9 fields — richest CDA section. |
| Vitals | ✅ Covered | CDA Vitals (observation, date/time) with LOINC | 2 fields — minimal. Individual vital types not enumerated. |
| Lab results | ✅ Covered | CDA Labs: 3 sub-sections (test info, lab info, results) totaling 14 fields with LOINC | Reasonably detailed for CDA. |
| Imaging / diagnostic reports | ⚠️ Partial | No dedicated imaging section in CDA. Scanned documents may include radiology reports as PDF/JPG | Product does radiology ordering; no structured imaging data export. Documents component may capture reports as scans. |
| Procedures | ✅ Covered | CDA Procedures (procedure, date) with CPT-4/SNOMED/HCPCS | 2 fields — minimal. |
| Clinical notes / documents | ✅ Covered | Scanned Documents component (PDF/JPG/PNG organized by category). CDA chief complaint provides some note content. | Good coverage via document files. Structured note content beyond chief complaint not evident. |
| Care plans / goals | ✅ Covered | CDA Treatment Plan (planned observation, date) with LOINC; CDA Goal (goal, value, date) | 5 fields across 2 sections. CCM-specific care plans not addressed. |
| Orders / referrals | ⚠️ Partial | CDA Reason for Referral (1 field). CDA Treatment Plan mentions "pending tests, future appointments, referrals." | Referral reason captured; order details, order sets, and order tracking not covered. |
| Insurance / coverage | ⚠️ Partial | CSV: "insurance details" mentioned but zero field documentation | Cannot verify depth. CDA does not include insurance. Product does eligibility verification — those records likely not exported. |
| Claims / billing | ❌ Not covered | No billing entities in any export component | **Major gap.** Product has full PMS with claims scrubbing, clearinghouse connectivity, ERA posting, CPT macros. None of this appears in the export. |
| Payments | ❌ Not covered | No payment data in export | **Major gap.** Product has PCI-compliant payment processing, copay collection, patient statements. None exported. |
| Consents / directives | ❌ Not covered | No consent data documented | May be captured as scanned documents if filed to chart. No structured consent export. |
| Patient communications / portal messages | ❌ Not covered | No messaging data in export | Product has secure messaging via patient portal. Not exported. |
| Specialty-specific data | ❌ Not covered | No specialty-specific sections beyond standard CDA | Product claims 20+ specialties. No specialty assessments, questionnaires, or custom forms in export. |
| Telehealth records | ❌ Not covered | No Vezo/telemedicine data in export | Product has Vezo telemedicine with transit notes and video visits. Not exported. |
| RPM data | ❌ Not covered | No RPM data in export | Product integrates with CCN Health for RPM (BP, glucose, CGM, SpO2, etc.). Device-sourced data not in export. Vitals in CDA may capture some manually-entered values. |
| CCM data | ❌ Not covered | No CCM-specific data in export | Product has CCM module with enrollment, activity logs, automated billing. Not exported. |

**Summary**: 10 of 21 applicable domains are covered (mostly via standard CDA sections), 4 are partially covered, and 7 are not covered at all. The uncovered domains include the entire billing/financial stack and all specialty modules (telehealth, RPM, CCM, portal messaging).

## 6. Documentation Quality

**Strengths:**
- CDA data dictionary provides XPATH paths and code system OIDs for key fields, giving a developer enough to parse the CDA XML output
- Export process is clearly documented with step-by-step instructions for both single-patient and bulk export
- The standard reference (C-CDA R2.1, §170.205(a)(4)) is explicitly cited

**Weaknesses:**
- **CSV files are completely undocumented** — a developer cannot build an import for demographics/insurance or appointments data without sample files
- **No sample data** — no example CDA documents, CSV files, or ZIP structure provided
- **No machine-readable schema** — no XSD, JSON Schema, or other parseable artifact
- **No field descriptions** — CDA fields have names and code system OIDs but no textual descriptions of what each field means or what values are valid
- **No relationship documentation** — how the CDA, CSV, and document components relate to each other is not described
- **FHIR pathway is essentially undocumented** — one sentence with no actionable detail
- **No value set bindings** — code systems are identified but specific value sets within those systems are not constrained

**Could a developer build an import?** Partially. The CDA portion follows C-CDA R2.1, so a developer familiar with that standard could parse it using the template IDs provided. The CSV and document components would require reverse-engineering from actual export files.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers standard clinical summary domains via C-CDA but omits the entire billing/financial stack (claims, ERA, payments, eligibility, patient statements) despite ethizo having a full Practice Management System. It also omits data from the product's telehealth (Vezo), remote patient monitoring (RPM), chronic care management (CCM), patient portal messaging, and eFax modules. The CDA clinical data is a standard clinical summary — it's the same data that would go in a (g)(10) export or a transitions-of-care document. The CSV components *might* add insurance and scheduling data, but they're completely undocumented so their scope cannot be verified. The scanned documents component adds genuine breadth by capturing whatever has been filed to the chart.

**Axis 2 — Export approach: Repackaged existing export**

The clinical data export is a standard C-CDA R2.1 Continuity of Care Document — the same format used for transitions of care under §170.205(a)(4). The 24 CDA sections map directly to standard CCD template IDs with no custom extensions. The vendor has added CSV files for demographics/insurance and appointments, plus a document dump, which shows some effort beyond bare C-CDA. However, the CSV components are undocumented, there are no billing or specialty-specific data components, and the FHIR pathway is just the (g)(10) API mentioned in one sentence. The dominant signal is that this is a C-CDA clinical summary with minor CSV supplements, not a purpose-built comprehensive EHI export.

### Key Findings

1. **The export is fundamentally a C-CDA clinical summary.** All 82 documented fields map to standard C-CDA R2.1 sections and template IDs. There are no custom CDA extensions, no vendor-specific data elements, and no coverage of data domains beyond what C-CDA was designed to carry. (Source: `EHI-Export-b.10-Documentation-v2.pdf`, pages 4–8)

2. **Billing and financial data is entirely absent.** Despite ethizo having a full Practice Management System with claims, ERA, payments, eligibility verification, and revenue cycle management, the export contains no billing entities. This is the single largest gap. (Source: product-research.md PMS section vs. PDF export documentation)

3. **Two CSV components are completely undocumented.** The demographics/insurance and appointments CSV files have zero field-level documentation — no column names, no types, no descriptions. A developer cannot assess or use these components from the documentation alone. (Source: `EHI-Export-b.10-Documentation-v2.pdf`, page 8)

4. **Multiple product modules generate patient data that is not exported.** Vezo telemedicine, RPM device data, CCM activity logs, patient portal messages, eFax documents, and questionnaire responses are all missing from the export documentation. (Source: cross-reference of product-research.md modules vs. PDF export content)

5. **The FHIR Bulk Data mention is a footnote, not documentation.** One sentence references FHIR Bulk Data for population export with no endpoints, authentication, or resource details. The FHIR API documents only standard US Core resources. (Source: `EHI-Export-b.10-Documentation-v2.pdf`, final sentence)

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   C-CDA R2.1 XML + CSV + PDF/JPG/PNG documents
Entities:        28 (24 CDA sections + 2 CSV files + documents + FHIR mention)
Fields:          82 (CDA only; CSV fields undocumented)
Descriptions:    0% (field names only, no descriptions)
Sample data:     No
Bulk export:     Yes (population-level via UI and mentioned FHIR Bulk Data)
Domains covered: 10 of 21 applicable domains (4 partial, 7 not covered)
```

### Bottom Line

Ethizo's EHI export is a standard C-CDA clinical summary with two undocumented CSV files and a document dump bolted on. A patient would get their clinical data (diagnoses, medications, labs, vitals, immunizations) and scanned documents, but would be missing their entire billing history, telehealth records, remote monitoring data, portal messages, and any specialty-specific assessments. The single biggest gap is the complete absence of billing/financial data from a product that has a full practice management system.
