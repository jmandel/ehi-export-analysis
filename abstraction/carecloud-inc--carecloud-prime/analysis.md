# EHI Export Analysis: CareCloud, Inc.

**Product**: CareCloud Prime v2.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 11504 (15.04.04.2790.Clou.02.02.1.240821)

## 1. Product Context

CareCloud Prime is a cloud-based, ONC-certified EHR platform from CareCloud, Inc. (NASDAQ: CCLD), serving ambulatory practices across a broad range of specialties. Priced at $249/provider/month, it is the company's flagship product, covering over 40,000 providers according to vendor claims.

The product is an integrated suite encompassing:

- **Clinical Documentation & Charting** (CareCloud Charts): customizable templates, AI-powered ambient documentation (cirrusAI Notes), CPOE for medications, labs, and imaging, e-prescribing including EPCS
- **Practice Management** (CareCloud Central): scheduling, patient registration, insurance eligibility verification, claims submission and tracking, claim scrubbing (CollectiveIQ), contract management
- **Revenue Cycle Management**: end-to-end billing, denial management, payment processing, patient statements
- **Patient Engagement** (Breeze portal): patient scheduling, intake forms, secure messaging, bill pay, telehealth, consent forms
- **Reporting & Analytics**: clinical quality measures, population health, practice performance dashboards
- **Public Health Reporting**: immunization registry, syndromic surveillance, cancer case, electronic lab, healthcare surveys

This broad scope — clinical, billing/RCM, patient engagement, practice management — is the baseline for assessing export completeness. The product stores substantial data across clinical, financial, administrative, and patient-communication domains.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `certification_b10_ehi_export_documentation.pdf` (1.15 MB, 12 pages) | The sole EHI export documentation. Contains C-CDA data dictionary (pp. 6–10), single/bulk export instructions with screenshots (pp. 3–5), brief non-clinical PDF export descriptions (p. 11), one-sentence FHIR mention (p. 12). Created 2024-09-12 by Jahanzaib Nisar in Microsoft Word 2016. | **Primary source** — contains all substantive export documentation |
| `screenshot-cc-prime-page-top.png` (859 KB) | Screenshot of the CareCloud Prime marketing page. Confirms the registered URL is a product page, not dedicated EHI documentation. | Low — contextual only |
| `screenshot-footer-ehi-link.png` (201 KB) | Screenshot showing the PDF link location in the page footer under "Real World Testing Plan" heading. | Low — contextual only |

No sample data files, machine-readable schemas, FHIR endpoint documentation, or additional data dictionaries were found.

## 3. Export Mechanics

- **Format**: Multi-format hybrid:
  - Clinical data → C-CDA XML (HL7 CDA R2, C-CDA 2.1 August 2015)
  - Non-clinical data (demographics/insurance, appointments, billing, messages, advance directives, documents) → PDF
  - FHIR mentioned but undocumented
- **Mechanism**: UI-based export within the application
  - **Single patient**: CCDA Report → CCDA Export Tab → select patient → Generate → Download XML
  - **Bulk export**: CCDA Report → Data Portability Tab → select date range → Export → downloads ZIP of XML files
  - **Non-clinical**: Reports section → export appointments, demographics, insurance, messages, claims in PDF format
- **Single-patient vs. bulk**: Both supported for C-CDA clinical data. Bulk produces ZIP of patient C-CDA files. PDF non-clinical exports appear to be per-patient (documentation unclear on bulk capability for these).
- **Access constraints**: Practice administrator grants access to users for EHI export. Users can export at any time without developer assistance. No fees mentioned in the documentation.

## 4. Export Content: What's In It

### C-CDA Clinical Data (Pages 6–10)

The PDF documents 24 C-CDA sections containing 82 data elements. Each element is listed with its name, XPATH/entry reference (where applicable), code system OID, and code system name. **No descriptive text** accompanies any field — just names and technical references.

Of the 82 C-CDA fields:
- **30** have XPATH/entry references
- **27** have code system identifiers
- **0** have descriptive text beyond the field name

This is a standard C-CDA data dictionary — it documents the structure of the C-CDA output by mapping to standard template IDs and code systems. It does not describe vendor-specific extensions, custom fields, or anything beyond what the C-CDA 2.1 standard defines.

### Non-Clinical PDF Exports (Page 11)

Six categories are listed, each receiving a single boilerplate sentence. Only Billing Data mentions any specific fields (CPT, ICD, Modifier — 3 field names with no types, descriptions, or structure). The remaining five categories (Demographics/Insurance, Advance Directive, Appointments, Messages, Documents) have **zero field-level documentation**.

The PDF format makes these exports non-computable — a receiving system cannot programmatically parse billing claims, appointment data, or messages from PDF files.

### FHIR Export (Page 12)

A single sentence: "CareCloud PRIME FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in §170.315(b)(10)(ii)."

No resource types listed, no endpoint URLs, no profiles, no examples. This appears to reference their (g)(10) FHIR API capability, but no documentation supports assessment of what FHIR resources are included.

### Vendor's own content organization

| Section | Fields | Has XPATH | Has Code System | Format | Category |
|---|---|---|---|---|---|
| Patient Demographics/Information | 6 | 5 | 2 | C-CDA XML | Clinical |
| Provider Information | 3 | 3 | 0 | C-CDA XML | Clinical |
| Date and Location of Visit | 2 | 2 | 0 | C-CDA XML | Clinical |
| Chief Complaint and Reason for Visit | 1 | 0 | 0 | C-CDA XML | Clinical |
| Encounters | 5 | 1 | 2 | C-CDA XML | Clinical |
| Immunizations | 9 | 1 | 3 | C-CDA XML | Clinical |
| Instructions | 1 | 1 | 1 | C-CDA XML | Clinical |
| Treatment Plan | 2 | 2 | 1 | C-CDA XML | Clinical |
| Social History | 3 | 1 | 2 | C-CDA XML | Clinical |
| Problems | 3 | 1 | 1 | C-CDA XML | Clinical |
| Medications | 5 | 1 | 1 | C-CDA XML | Clinical |
| Medication Allergies | 4 | 1 | 3 | C-CDA XML | Clinical |
| Laboratory Tests | 4 | 0 | 1 | C-CDA XML | Clinical |
| Laboratory Information | 5 | 0 | 0 | C-CDA XML | Clinical |
| Laboratory Results | 5 | 1 | 1 | C-CDA XML | Clinical |
| Vitals | 2 | 1 | 1 | C-CDA XML | Clinical |
| Goals | 3 | 1 | 0 | C-CDA XML | Clinical |
| Procedures | 2 | 1 | 1 | C-CDA XML | Clinical |
| Care Team Members | 3 | 1 | 0 | C-CDA XML | Clinical |
| Reason for Referral | 1 | 1 | 1 | C-CDA XML | Clinical |
| Medical Equipment / Implanted Devices | 2 | 1 | 1 | C-CDA XML | Clinical |
| Mental Status | 4 | 1 | 1 | C-CDA XML | Clinical |
| Functional Status | 4 | 1 | 1 | C-CDA XML | Clinical |
| Health Concerns | 3 | 1 | 1 | C-CDA XML | Clinical |
| Patient Demographic/Insurance (PDF) | 0 | — | — | PDF | Non-clinical |
| Advance Directive (PDF) | 0 | — | — | PDF | Non-clinical |
| Appointments (PDF) | 0 | — | — | PDF | Non-clinical |
| Provider-to-Patient Messages (PDF) | 0 | — | — | PDF | Non-clinical |
| Billing Data / Claims (PDF) | 3 | — | — | PDF | Non-clinical |
| Documents (PDF) | 0 | — | — | PDF | Non-clinical |

**Totals**: 24 C-CDA sections (82 fields), 6 PDF exports (3 field names), 1 FHIR mention (0 documented fields). Grand total: 85 documented data elements across 31 sections.

Full inventory saved to `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the export into three tiers:

1. **C-CDA Clinical Data** (24 sections, 82 fields): This is the most detailed portion. It maps standard C-CDA sections — demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, care plans, goals, social history, mental/functional status, health concerns, implanted devices, care team, and referrals. This is essentially the USCDI / US Core clinical summary set. The documentation is a standard C-CDA implementation guide mapping, not a vendor-specific data dictionary — it tells you what C-CDA sections are produced, but not what vendor-specific data underlies them or how complete the mapping is.

2. **PDF Non-Clinical Exports** (6 categories, essentially undocumented): Demographics/insurance, advance directives, appointments, messages, billing claims, and documents are exported as PDFs. Each gets a single boilerplate sentence. Only billing mentions specific data elements (CPT, ICD, Modifier). This tier nominally addresses some gaps the C-CDA doesn't cover (billing, appointments, messages), but the PDF format and lack of documentation make it impossible to assess completeness or usability.

3. **FHIR Export** (1 sentence, fully undocumented): Mentioned but provides no actionable detail. Cannot be assessed.

The C-CDA clinical tier is the richest, but it is a standard projection, not a native data model export. The PDF tier attempts broader coverage but is non-computable and undocumented. The FHIR tier is a placeholder.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 fields (name, sex, DOB, race, ethnicity, language); PDF: "demographics and insurance" (no fields documented) | C-CDA covers basic demographics per USCDI. PDF presumably adds more but is undocumented and non-computable. Product stores extensive registration data (contacts, addresses, employer, etc.) — unclear how much is exported. |
| Encounters / visits | ✅ Covered | C-CDA: Encounters section (5 fields — code, performer, diagnosis, location, date); Date and Location of Visit (2 fields) | Standard encounter summary via C-CDA. Adequate for clinical encounters. |
| Problems / conditions | ✅ Covered | C-CDA: Problems section (3 fields — problem code SNOMED/ICD10, status, active date) | Standard problem list. |
| Medications / prescriptions | ⚠️ Partial | C-CDA: Medications section (5 fields — medication code RxNorm/NDC, directions, start/end date, status) | C-CDA covers medication list. However, product has ePrescribing/EPCS — detailed prescription records, pharmacy transactions, controlled substance logs are not addressed. |
| Allergies | ✅ Covered | C-CDA: Medication Allergies (4 fields — substance, reaction, severity, status) | Standard allergy list. |
| Immunizations | ✅ Covered | C-CDA: Immunizations (9 fields — vaccine CVX/CPT-4, date, status, route, site, manufacturer, dose, lot, notes) | Well-documented section with the most fields of any C-CDA section. |
| Vitals | ✅ Covered | C-CDA: Vitals (2 fields — observation LOINC, date/time) | Standard vitals via C-CDA. |
| Lab results | ✅ Covered | C-CDA: Laboratory Tests (4 fields), Laboratory Information (5 fields), Laboratory Results (5 fields) — 14 fields total across 3 sections | Lab data is the most thoroughly documented domain with dedicated sections for test metadata, lab information, and results. |
| Imaging / diagnostic reports | ⚠️ Partial | PDF Documents export includes "radiology reports"; C-CDA Procedures covers imaging procedures | Radiology reports exported as PDF documents. No structured imaging data or DICOM references. |
| Procedures | ✅ Covered | C-CDA: Procedures (2 fields — procedure code CPT-4/SNOMED/HCPCS, date) | Standard procedure list. |
| Clinical notes / documents | ⚠️ Partial | PDF Documents export: "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" | Notes exported as PDF documents. No structured note content, no note types enumerated, no field-level detail. |
| Care plans / goals | ✅ Covered | C-CDA: Treatment Plan (2 fields), Goals (3 fields), Health Concerns (3 fields) | Standard C-CDA care plan sections. |
| Orders / referrals | ⚠️ Partial | C-CDA: Reason for Referral (1 field — SNOMED); CPOE orders for meds/labs/imaging flow through respective sections | Referral reasons are included, but detailed order records (order status, fulfillment, ordering provider workflows) are not documented. |
| Insurance / coverage | ⚠️ Partial | PDF: "demographics and insurance details" — no fields documented | Product stores insurance/eligibility data extensively (CareCloud Central). PDF export nominally includes insurance but with zero field documentation and non-computable format. |
| Claims / billing | ⚠️ Partial | PDF: "billing data (CPT, ICD, Modifier)" — 3 field names only | Product has full RCM capabilities (claims submission, tracking, scrubbing, denial management, appeals). The PDF export mentions only 3 data elements. This is a major documentation gap — it's impossible to tell if the actual PDF export includes claim amounts, dates of service, payer information, payment status, or just procedure/diagnosis codes. |
| Payments | ❌ Not covered | No payment data mentioned in export documentation | Product processes insurance and patient payments, patient statements, bill pay. Not mentioned in export. Significant gap. |
| Consents / directives | ⚠️ Partial | PDF: "Advance Directive" — no fields documented; Breeze portal collects consent forms with e-signatures | Advance directives nominally included as PDF but undocumented. Patient consent forms from Breeze portal not mentioned. |
| Patient communications / portal messages | ⚠️ Partial | PDF: "Provider-to-Patient Messages" — no fields documented | Messages nominally included as PDF. Breeze portal has extensive secure messaging, appointment requests, prescription refill requests — unclear if all are captured. PDF format makes these non-computable. |
| Specialty-specific data | ❌ Not covered | No specialty-specific content in the export documentation | Product supports multiple specialties with customizable templates and workflows. No specialty-specific assessments, forms, or data are documented in the export. |

## 6. Documentation Quality

The export documentation is a **12-page PDF that allocates 5 pages to C-CDA section mappings and gives all non-clinical exports a single page of boilerplate sentences**.

**What's documented reasonably:**
- The C-CDA data dictionary (pp. 6–10) maps CDA sections to XPATHs, template IDs, and code systems. This is adequate for someone already familiar with C-CDA — it tells you which standard sections are populated. However, it contains no vendor-specific information. A developer familiar with C-CDA 2.1 could process the XML output without this documentation.

**What's poorly documented or undocumented:**
- All 6 PDF non-clinical exports receive identical boilerplate ("This file offers a comprehensive view of [X], structured for clarity and ease of access") with no field-level documentation
- Billing data mentions 3 field names (CPT, ICD, Modifier) but no types, no structure, no example
- FHIR export is a single sentence with no endpoint, resource types, or profiles
- No sample data for any format
- No machine-readable schema
- No documentation of relationships between C-CDA, PDF, and FHIR exports
- No documentation of how files are organized in the export package

**Could a developer build an import from this documentation alone?**
For the C-CDA portion — yes, because C-CDA is a well-known standard and the documentation identifies which sections are present. For the PDF exports — no, because PDFs have no defined structure and no fields are documented. For the FHIR export — no, because nothing is documented. A developer would need to request actual sample exports to understand the non-clinical data.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is primarily a C-CDA clinical summary supplemented by undocumented PDF exports for non-clinical data. The C-CDA portion covers the standard USCDI clinical data elements — this is the same clinical summary used for care transitions and patient access, repackaged as the (b)(10) EHI export. The PDF exports nominally extend coverage to billing, appointments, and messages, but the PDF format is non-computable and the lack of documentation makes it impossible to verify these exports are comprehensive.

This is not a native database export. There is no evidence that the vendor exports their internal data model, custom fields, specialty-specific templates, or any data structure beyond what the C-CDA standard defines. The 85 documented data elements across 31 sections represent a tiny fraction of what a full-featured EHR/PM/RCM system like CareCloud Prime stores.

### Key Findings

1. **C-CDA repackaging as (b)(10)**: The clinical data export is a standard C-CDA document — the same output used for (b)(1)/(b)(2) care transitions. The data dictionary on pp. 6–10 maps standard C-CDA sections, not vendor-specific data. This covers USCDI clinical data but not the breadth of data the product stores. (Source: `certification_b10_ehi_export_documentation.pdf`, pp. 6–10)

2. **Non-clinical data exported as non-computable PDFs**: Billing, appointments, messages, insurance, and documents are exported as PDFs — a print format with no programmatic structure. This makes the non-clinical portion of the export essentially unusable for data portability. (Source: `certification_b10_ehi_export_documentation.pdf`, p. 11)

3. **6 out of 6 PDF export categories have zero field-level documentation**: Each receives an identical boilerplate sentence. Only billing data mentions 3 field names (CPT, ICD, Modifier). This makes it impossible to assess what these exports actually contain. (Source: `certification_b10_ehi_export_documentation.pdf`, p. 11)

4. **Major coverage gaps in billing/RCM despite product's deep capabilities**: The product offers full revenue cycle management (CollectiveIQ claim scrubbing, denial management, payment processing, contract management). The export documents billing as a PDF with 3 field names. Payments are not mentioned at all. (Source: product-research.md; `certification_b10_ehi_export_documentation.pdf`, p. 11)

5. **FHIR export is a placeholder**: One sentence mentions FHIR Bulk Data EHI Export with zero specifics — no resources, no endpoints, no profiles. (Source: `certification_b10_ehi_export_documentation.pdf`, p. 12)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + PDF + FHIR (mentioned only)
Model type:      Standard projection (C-CDA 2.1)
Entities:        31 sections (24 C-CDA + 6 PDF + 1 FHIR)
Fields:          85 (82 C-CDA + 3 PDF billing field names)
Descriptions:    0% (no fields have descriptive text)
Sample data:     No
Bulk export:     Yes (C-CDA bulk via ZIP; unclear for PDF exports)
Domains covered: 8 of 17 applicable domains fully; 8 partial; 1 not covered
```

### Bottom Line

CareCloud Prime's (b)(10) export is a C-CDA clinical summary repackaged as an EHI export, supplemented by undocumented PDF exports for non-clinical data. A patient or provider would receive a standard clinical summary in C-CDA XML plus PDF printouts of billing, appointments, and messages — but the PDFs are non-computable, the billing data is barely documented (3 field names), and major domains like payments, specialty-specific data, and detailed prescription records appear absent. The single biggest gap is the use of PDF for non-clinical data, which makes the billing, insurance, appointment, and messaging portions of the export essentially unusable for data portability or import into another system.
