# EHI Export Analysis: CareCloud, Inc.

**Product**: CareCloud Prime v2.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 11504 (CHPL Product Number: 15.04.04.2790.Clou.02.02.1.240821)

## 1. Product Context

CareCloud Prime is a cloud-based, ONC-certified EHR platform from CareCloud, Inc. (NASDAQ: CCLD), serving over 40,000 ambulatory providers across a broad range of specialties. Priced at $249/provider/month, it is the company's flagship product, certified across 40+ ONC criteria.

The platform is an integrated suite encompassing:

- **Clinical EHR (CareCloud Charts)**: Charting with customizable templates, CPOE for medications/labs/imaging, e-prescribing (including EPCS), clinical decision support, AI-powered ambient documentation (cirrusAI Notes)
- **Practice Management (CareCloud Central)**: Scheduling, patient registration, insurance eligibility verification, claims submission and tracking, advanced claim scrubbing (CollectiveIQ), contract management
- **Revenue Cycle Management (RCM)**: End-to-end billing services, denial management and AI-powered appeals, payment processing, patient statements
- **Patient Engagement (Breeze + Community)**: Patient portal with scheduling, check-in, intake forms, secure messaging, prescription refill requests, consent forms, online bill pay, telehealth
- **Reporting & Public Health**: CQMs, population health analytics, immunization/syndromic/cancer registry reporting

This breadth means the EHI export should cover clinical data, billing/claims, insurance, patient portal communications, documents, and specialty-specific clinical content. The product stores far more than what a standard C-CDA clinical summary captures.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `certification_b10_ehi_export_documentation.pdf` (1.15 MB, 12 pages) | The sole EHI export documentation. Created 2024-09-12 in Microsoft Word 2016 by "JAHANZAIB NISAR." Contains: overview (p3), single-patient export instructions with screenshot (p4), bulk export instructions with screenshot (p5), C-CDA data dictionary (pp6–10), PDF export descriptions (p11), FHIR mention and timeliness statement (p12). | **Primary artifact** — everything substantive is here |
| `screenshot-cc-prime-page-top.png` (859 KB) | Screenshot of the CareCloud Prime marketing page top. Confirms the registered URL is a product page, not an EHI documentation page. | Low |
| `screenshot-footer-ehi-link.png` (201 KB) | Screenshot showing the PDF link in the page footer under "Real World Testing Plan." | Low — confirms navigation path only |

**No sample data, no machine-readable schemas, no additional API documentation.** The entire EHI export documentation consists of a single 12-page PDF.

## 3. Export Mechanics

- **Format**: Clinical data in C-CDA XML (HL7 CDA R2, C-CDA 2.1 August 2015); non-clinical data (demographics/insurance, appointments, billing, messages, documents) in PDF; FHIR mentioned but undocumented.
- **Mechanism**: UI-driven. Single-patient export via CCDA Report → CCDA Export Tab → search patient → Generate → Download XML. Bulk export via CCDA Report → Data Portability Tab → select date range → Export → ZIP of XML files. PDF exports via the application's "Reports" section (p11).
- **Single-patient**: Yes, via CCDA Export tab (p4 screenshot shows a "Patient Chart Summary" for "John Doe" with demographics).
- **Bulk capability**: Yes, via Data Portability tab (p5 screenshot shows pagination "1 – 10 of 93" patients and a ZIP download dialog).
- **Access constraints**: Practice administrator must grant access to users for EHI export. No fees mentioned. No developer assistance required (p12).
- **FHIR**: Page 12 states "CareCloud PRIME FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in §170.315(b)(10)(ii)." This is a single sentence with zero further documentation — no resource types, endpoints, profiles, or examples.

## 4. Export Content: What's In It

The export has two documented components: structured C-CDA XML for clinical data, and PDF printouts for non-clinical data.

### C-CDA Clinical Data Dictionary (pp6–10)

The data dictionary maps 24 C-CDA sections to XPATHs and code systems, containing **82 total data elements**. Each element includes a name, an XPATH or template ID entry, and (where applicable) a code system OID and name. There are no textual descriptions of what each element means — identification is by name and XPATH only. Data types and cardinality are not documented (they are implicit in the C-CDA standard). Value sets are identified by OID but not enumerated. No relationships between sections are documented.

### PDF Non-Clinical Exports (p11)

Six categories are listed, each with a single boilerplate sentence ("This file offers a comprehensive view of [X], structured for clarity and ease of access"):

1. **Patient Demographic/Insurance** — no field documentation
2. **Advance Directive** — no field documentation
3. **Appointments** — no field documentation
4. **Provider-to-Patient Messages** — no field documentation
5. **Billing Data (Claim)** — mentions "CPT, ICD, Modifier" (3 named fields)
6. **Documents** — "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" in PDF format

No field-level detail, no schema, no sample files for any PDF export.

### Vendor's own content organization

| Section / Category | Elements | Code Systems | Format | Documentation Depth |
|---|---|---|---|---|
| Patient Demographics/Information | 6 | AdministrativeGender, Race & Ethnicity - CDC | C-CDA XML | XPATH + code system OIDs |
| Provider's name and office contact | 3 | — | C-CDA XML | XPATH only |
| Date and Location of visit | 2 | — | C-CDA XML | XPATH only |
| Chief Complaint and Reason for visit | 1 | — | C-CDA XML | XPATH only |
| Encounters | 5 | CPT, SNOMED, ICD10 | C-CDA XML | XPATH + code system OIDs |
| Immunizations | 9 | CVX, CPT-4, NCI Thesaurus, SNOMED | C-CDA XML | XPATH + code system OIDs |
| Instructions | 1 | SNOMED | C-CDA XML | XPATH + code system OIDs |
| Treatment Plan | 2 | LOINC | C-CDA XML | XPATH + code system OIDs |
| Social History | 3 | LOINC, SNOMED | C-CDA XML | XPATH + code system OIDs |
| Problems | 3 | SNOMED, ICD10 | C-CDA XML | XPATH + code system OIDs |
| Medications | 5 | RxNorm, NDC | C-CDA XML | XPATH + code system OIDs |
| Medication Allergies | 4 | RxNorm, SNOMED | C-CDA XML | XPATH + code system OIDs |
| Laboratory Tests | 4 | LOINC | C-CDA XML | XPATH + code system OIDs |
| Laboratory Information | 5 | — | C-CDA XML | XPATH only |
| Laboratory value(s)/result(s) | 5 | LOINC | C-CDA XML | XPATH + code system OIDs |
| Vitals | 2 | LOINC | C-CDA XML | XPATH + code system OIDs |
| Goal | 3 | — | C-CDA XML | XPATH only |
| Procedures | 2 | CPT-4, SNOMED, HCPCS | C-CDA XML | XPATH + code system OIDs |
| Care team member(s) | 3 | — | C-CDA XML | XPATH only |
| Reason for Referral | 1 | SNOMED | C-CDA XML | XPATH only |
| Medical Equipment | 2 | SNOMED | C-CDA XML | XPATH + code system OIDs |
| Mental Status | 4 | SNOMED | C-CDA XML | XPATH + code system OIDs |
| Functional Status | 4 | SNOMED | C-CDA XML | XPATH + code system OIDs |
| Health Concern | 3 | SNOMED | C-CDA XML | XPATH + code system OIDs |
| *Patient Demographic/Insurance* | *0 documented* | — | PDF | *One sentence, no fields* |
| *Advance Directive* | *0 documented* | — | PDF | *One sentence, no fields* |
| *Appointments* | *0 documented* | — | PDF | *One sentence, no fields* |
| *Provider-to-Patient Messages* | *0 documented* | — | PDF | *One sentence, no fields* |
| *Billing Data (Claim)* | *3 named (CPT, ICD, Modifier)* | — | PDF | *One sentence, 3 field names* |
| *Documents* | *0 documented* | — | PDF | *One sentence, no fields* |

**Totals**: 24 C-CDA sections with 82 elements + 6 PDF categories with 3 named fields = **85 documented data elements across 30 categories**.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor divides its export into two tracks:

**C-CDA track (pages 6–10)**: This is standard C-CDA 2.1 clinical summary content. The 24 sections and 82 elements map directly to standard CDA template IDs — demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, care plans, goals, social history, mental/functional status, health concerns, referrals, medical equipment, and care team. This is essentially a standard USCDI/US Core clinical summary. The documentation is a code system mapping table, not a vendor-native data dictionary — it describes C-CDA output structure, not the underlying CareCloud data model.

**PDF track (page 11)**: Six categories of non-clinical data exported as PDF files. This is where the vendor addresses billing, insurance, appointments, messages, and documents — the data domains that C-CDA does not cover. However, documentation is essentially zero: each category gets one boilerplate sentence with no field-level detail. The billing export mentions "CPT, ICD, Modifier" but nothing about charges, amounts, dates of service, payer information, claim status, payments, adjustments, or any other billing field. PDF is a non-computable format — there is no way to programmatically parse or import this data.

**FHIR track (page 12)**: A single sentence claiming FHIR Bulk Data EHI Export support. Completely undocumented — no resource types, no endpoint URLs, no profiles, no examples. Cannot be assessed.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 elements (name, sex, DOB, race, ethnicity, language). PDF: "Patient Demographic/Insurance" (undocumented) | C-CDA covers basic demographics. Contact info, address, emergency contacts unclear — may be in undocumented PDF export. Product stores detailed registration data (Central module). |
| Encounters / visits | ✅ Covered | C-CDA: Encounters section (5 elements: code, performer, diagnosis, location, date) with CPT/SNOMED/ICD10 coding | Standard C-CDA encounter data present |
| Problems / conditions | ✅ Covered | C-CDA: Problems section (3 elements) with SNOMED and ICD10 coding | Adequately represented |
| Medications / prescriptions | ⚠️ Partial | C-CDA: Medications section (5 elements: medication, directions, start/end date, status) with RxNorm/NDC | Medication list is present, but product has full e-prescribing with EPCS, Surescripts integration, drug interaction records. Prescription workflow data (Rx history, pharmacy responses, controlled substance logs) not in C-CDA. |
| Allergies | ✅ Covered | C-CDA: Medication Allergies section (4 elements: substance, reaction, severity, status) with RxNorm/SNOMED | Standard allergy data present |
| Immunizations | ✅ Covered | C-CDA: Immunizations section (9 elements) with CVX/CPT-4 coding — richest section | Well-represented |
| Vitals | ✅ Covered | C-CDA: Vitals section (2 elements: observation, date/time) with LOINC | Standard vitals present |
| Lab results | ✅ Covered | C-CDA: Three lab-related sections (14 combined elements) with LOINC coding | Well-represented with test info, results, reference ranges, interpretation |
| Imaging / diagnostic reports | ⚠️ Partial | PDF Documents export mentions "radiology reports" but with no field documentation | Radiology reports mentioned as PDFs only; no structured imaging order or report data |
| Procedures | ✅ Covered | C-CDA: Procedures section (2 elements) with CPT-4/SNOMED/HCPCS | Standard procedure data present |
| Clinical notes / documents | ⚠️ Partial | PDF Documents export: "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" | Documents exported as PDFs — covers document content but loses any structured metadata. No documentation of what metadata is preserved. |
| Care plans / goals | ✅ Covered | C-CDA: Treatment Plan (2 elements), Goal (3 elements), Health Concern (3 elements) | Adequately represented in C-CDA |
| Orders / referrals | ⚠️ Partial | C-CDA: Reason for Referral (1 element, SNOMED). No lab/imaging order data beyond what's in results. | Product has full CPOE (medications, labs, imaging). Only referral reasons are in the export; order workflow data missing. |
| Insurance / coverage | ⚠️ Partial | PDF: "Patient Demographic/Insurance" — no fields documented | Insurance data is claimed to be exported, but as an undocumented PDF. Product does eligibility verification and contract management — none of that detail is documented. |
| Claims / billing | ⚠️ Partial | PDF: "Billing Data (Claim)" — mentions CPT, ICD, Modifier only. No charges, amounts, payments, payer info, claim status, denial data. | Product has full RCM with CollectiveIQ claim scrubbing, denial management, contract management, payment processing. The export mentions 3 code fields — this is a tiny fraction of the billing data the product stores. |
| Payments | ❌ Not covered | No evidence of payment data in the export | Product processes insurance and patient payments, manages patient statements and balances. Not in export. |
| Consents / directives | ⚠️ Partial | PDF: "Advance Directive" (undocumented). C-CDA has no consent section. | Advance directives mentioned; patient consent forms (Breeze portal e-signatures) not addressed. |
| Patient communications / portal messages | ⚠️ Partial | PDF: "Provider-to-Patient Messages" (undocumented) | Messages exported as undocumented PDF. Product has full secure messaging, prescription refill requests, appointment requests via Breeze portal — only "messages" mentioned. |
| Specialty-specific | ❌ Not covered | No specialty-specific data entities in the export | Product serves 40+ specialties with customizable templates. No specialty-specific clinical data structures appear in the export beyond what C-CDA provides generically. |

**Summary**: Of 18 applicable domains, 7 are adequately covered (all via standard C-CDA), 9 are partially covered (either via undocumented PDF exports or with significant structural gaps), and 2 have no evidence of coverage.

## 6. Documentation Quality

**Overall**: Poor. The documentation cannot support a developer attempting to import or process this export.

**Strengths**:
- The C-CDA data dictionary (pp6–10) provides XPATH entries and code system OIDs for 82 data elements across 24 sections. This is useful for someone familiar with C-CDA but adds minimal information beyond what the C-CDA 2.1 standard itself defines.
- UI screenshots (pp4–5) show the actual export interface for both single and bulk export, confirming the workflow exists.

**Weaknesses**:
- **No field-level documentation for non-clinical exports**: 6 PDF export categories get one boilerplate sentence each. The billing export — for a product with comprehensive RCM capabilities — is described only as "CPT, ICD, Modifier."
- **No sample data files**: There are no example exports (XML or PDF) to examine.
- **No machine-readable schemas**: No JSON schema, no XSD customization, no FHIR CapabilityStatement.
- **FHIR export completely undocumented**: A single sentence claiming FHIR Bulk Data support with zero actionable detail.
- **No data types or cardinality**: The C-CDA dictionary relies entirely on implicit C-CDA standard definitions.
- **No relationships documented**: No explanation of how C-CDA files relate to PDF files, or how data is linked across export components.
- **No descriptions**: Data element names only; no textual explanation of what each element contains or how it's populated in CareCloud Prime.

A developer receiving this export would be able to process the C-CDA XML using standard C-CDA parsers, but would have no way to programmatically handle the PDF exports and no way to understand what's in them without manually inspecting samples.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is fundamentally a C-CDA clinical summary supplemented by PDF printouts of non-clinical data. The C-CDA portion covers the standard USCDI clinical summary domains (problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, care plans). The non-clinical data (billing, insurance, appointments, messages, documents) is exported as unstructured PDF — not the vendor's native data model, not computable, and not documented at the field level.

This is not a native data model export. There is no evidence that CareCloud exports its internal database tables, relational structure, or vendor-specific data fields. The C-CDA output is a standardized projection of clinical data, and the PDF output is a print-format rendering of non-clinical data.

### Key Findings

1. **The export is a C-CDA clinical summary, not a comprehensive EHI export.** The 24 C-CDA sections and 82 data elements are standard C-CDA 2.1 content — essentially a clinical summary document. This covers perhaps 30–40% of the data CareCloud Prime stores about patients. (Source: `certification_b10_ehi_export_documentation.pdf`, pp6–10; analysis script `parse_ccda_dictionary.py`)

2. **Non-clinical data is exported as unstructured PDFs with no documentation.** Billing, insurance, appointments, messages, and documents are exported as PDF files. PDF is a non-computable format; a third party cannot programmatically import or process this data. Each category receives a single boilerplate sentence of documentation. (Source: PDF p11)

3. **Billing/RCM coverage is nominal.** CareCloud has comprehensive RCM capabilities (CollectiveIQ claim scrubbing, denial management, payment processing, contract management), but the export mentions only "CPT, ICD, Modifier" for billing — three code fields in a PDF. Charges, amounts, payments, adjustments, claim status, denial reasons, and payer information are not documented. (Source: PDF p11 vs. product-research.md billing capabilities)

4. **FHIR export is claimed but entirely undocumented.** Page 12 contains a single sentence asserting FHIR Bulk Data EHI Export support. No resource types, endpoints, profiles, or examples are provided. This claim cannot be evaluated. (Source: PDF p12)

5. **No sample data or machine-readable artifacts.** The entire export documentation is a single 12-page PDF with no sample exports, no schemas, and no API documentation.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + PDF (FHIR claimed but undocumented)
Model type:      Standard projection (C-CDA 2.1) + unstructured PDF printouts
Entities:        24 C-CDA sections + 6 PDF categories = 30 total
Fields:          82 C-CDA data elements + 3 named PDF fields = 85
Descriptions:    0% (names and XPATHs only; no textual descriptions)
Sample data:     No
Bulk export:     Yes (ZIP of C-CDA XMLs via Data Portability tab)
Domains covered: 7 of 18 applicable domains adequately; 9 partial; 2 not covered
```

### Bottom Line

CareCloud Prime's EHI export is a standard C-CDA clinical summary with PDF printouts bolted on for billing and administrative data. A patient would get a usable clinical summary but not a complete, computable copy of their data. The single biggest gap is that the product's extensive billing/RCM data — one of its core value propositions — is reduced to an undocumented PDF mentioning three code fields, and the entire non-clinical data layer is exported in a format that cannot be programmatically processed or imported.
