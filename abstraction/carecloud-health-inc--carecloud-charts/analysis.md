# EHI Export Analysis: CareCloud Health, Inc.

**Product**: CareCloud Charts v3.0
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2981.Care.03.01.1.221229 (CHPL ID 11173)

## 1. Product Context

CareCloud Charts is a cloud-based ambulatory EHR that is part of a larger integrated platform. The certified EHR module (Charts) works alongside CareCloud Central (practice management, billing, claims), CareCloud Breeze (patient portal, digital intake, online payments), CareCloud Live (telehealth), and CareCloud Analytics (reporting). CareCloud, Inc. (NASDAQ: CCLD) serves over 40,000 providers across 50+ specialties, from solo practices to large multi-site groups, with pricing around $628/provider/month.

The product stores data across multiple domains relevant to EHI export completeness:

- **Clinical (Charts)**: Patient demographics, encounter documentation, problem lists, medications, allergies, vitals, lab orders/results, imaging orders, immunizations, care plans, clinical decision support alerts, configurable specialty templates, and AI-generated clinical notes (cirrusAI).
- **Administrative/Financial (Central)**: Appointment scheduling, insurance/payer information, billing charges (CPT/E&M codes), claims submission and tracking, denial management, payment records, revenue cycle analytics.
- **Patient Engagement (Breeze)**: Patient portal accounts, digital intake form submissions, secure patient-provider messaging, appointment requests, online bill pay, check-in records.
- **Telehealth (Live)**: Virtual visit records integrated with EHR encounters.
- **E-Prescribing**: Pharmacy lookup, prescription transmission via Surescripts.

This integrated platform means the designated record set extends well beyond what a standard C-CDA clinical summary captures. A complete (b)(10) export should include structured data from Charts, Central, and Breeze.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-documentation.pdf` (457,681 bytes, 11 pages) | The sole substantive artifact. Titled "CareCloud Charts Certification - §170.315(b)(10) Electronic Health Information Export - Documentation." Created 2023-11-14 by Rico Lopez in Microsoft Word. Contains export overview (pp. 3–5), CCD data dictionary (pp. 6–10), and brief PDF/FHIR export descriptions (p. 11). | **Primary source** — all analysis is based on this document. |
| `screenshot-box-page.png` (146,319 bytes) | Screenshot of the Box.com shared link page showing the PDF in Box's viewer with Download button and CareCloud branding. Confirms the PDF is accessible at the registered URL. | Low — confirms access only. |

**No other artifacts exist.** There are no sample data files, no machine-readable schemas (XSD, JSON Schema), no sample C-CDA documents, no sample PDF exports, and no FHIR capability statements or resource documentation. The entire (b)(10) documentation is a single 11-page PDF.

## 3. Export Mechanics

CareCloud describes three export mechanisms:

**1. C-CDA Clinical Summary Export (XML)**
- **Single patient**: Open patient account → click Print icon → select "Clinical Summary CCD" → downloads C-CDA XML file. This appears to be the same Clinical Summary CCD used for (b)(1)/(b)(2)/(b)(3) transitions of care.
- **Bulk patient**: Analytics Application → Clinical → Patient List → apply filters → set Render Format to CDA → Run Report → ZIP file of C-CDA XML files.
- Standard: HL7 CDA R2, Consolidated CDA Templates for Clinical Notes (US Realm), Draft Standard for Trial Use Release 2.1, August 2015 (§170.205(a)(4)).

**2. PDF Exports (non-clinical data)**
- Generated via the Analytics Application for: Patient Demographics/Insurance, Advance Directives, Appointments, Provider-to-Patient Messages, Billing Data (Claims), and Documents (signed notes, lab results, radiology reports, scanned/uploaded documents).
- Documents can be sorted and categorized by type.
- Mechanism: user-initiated via Analytics Application UI.

**3. FHIR Data Export**
- Described in a single sentence: "CareCloud Charts' FHIR Server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for the patient population as described in §170.315(b)(10)(ii)."
- No detail on which FHIR resources are included, what endpoints to call, or what data is covered.

**Access**: User-initiated through the product UI (Patient Application and Analytics Application). No API endpoint documented for programmatic export beyond the vague FHIR mention. No indication of fees. Both single-patient and bulk capabilities exist for clinical data; unclear whether bulk capability exists for the PDF exports.

## 4. Export Content: What's In It

### CCD Data Dictionary (pages 6–10)

The CCD data dictionary maps data elements to CDA XPaths and code systems across **24 sections** containing **82 data elements**. Of these 82 elements, 27 (32.9%) have an associated code system specified (e.g., SNOMED, LOINC, RxNorm). The remaining elements have names and XPaths but no code system. No element has a prose description, cardinality, optionality, or data type documented beyond what's implicit in the CDA standard.

Code systems referenced: AdministrativeGender, CPT, CPT-4, CVX, HCPCS, ICD-10, LOINC, NCI Thesaurus, NDC, Race & Ethnicity - CDC, RxNorm, SNOMED.

This is not a vendor-specific data dictionary — it is a mapping of standard C-CDA sections to their CDA XPaths. It documents what the C-CDA standard already specifies, not what CareCloud's internal data model contains or how vendor-specific data is represented.

### Vendor's own content organization

#### CCD Sections (pages 6–10)

| CCD Section | Elements | Code Systems | Template ID |
|---|---|---|---|
| Patient Demographics/Information | 6 | AdministrativeGender, CDC Race/Ethnicity | — |
| Provider's Name and Office Contact | 3 | — | — |
| Date and Location of Visit | 2 | — | 2.16.840.1.113883.10.20.22.2.22.1 |
| Chief Complaint and Reason for Visit | 1 | — | 2.16.840.1.113883.10.20.22.2.13 |
| Encounters | 5 | CPT, SNOMED, ICD-10 | 2.16.840.1.113883.10.20.22.2.22.1 |
| Immunizations | 9 | CVX, CPT-4, NCI Thesaurus, SNOMED | 2.16.840.1.113883.10.20.22.2.2.1 |
| Instructions | 1 | SNOMED | 2.16.840.1.113883.10.20.22.2.45 |
| Treatment Plan | 2 | LOINC | 2.16.840.1.113883.10.20.22.2.10 |
| Social History | 3 | LOINC, SNOMED | 2.16.840.1.113883.10.20.22.2.17 |
| Problems | 3 | SNOMED, ICD-10 | 2.16.840.1.113883.10.20.22.2.5.1 |
| Medications | 5 | RxNorm, NDC | 2.16.840.1.113883.10.20.22.2.1.1 |
| Medication Allergies | 4 | RxNorm, SNOMED | 2.16.840.1.113883.10.20.22.2.6.1 |
| Laboratory Tests | 4 | LOINC | — |
| Laboratory Information | 5 | — | — |
| Laboratory Values/Results | 5 | LOINC | 2.16.840.1.113883.10.20.22.2.3.1 |
| Vitals | 2 | LOINC | 2.16.840.1.113883.10.20.22.2.4.1 |
| Goal | 3 | — | 2.16.840.1.113883.10.20.22.2.60 |
| Procedures | 2 | CPT-4, SNOMED, HCPCS | 2.16.840.1.113883.10.20.22.2.7.1 |
| Care Team Members | 3 | — | 2.16.840.1.113883.10.20.22.2.500 |
| Reason for Referral | 1 | SNOMED | 1.3.6.1.4.1.19376.1.5.3.1.3.1 |
| Medical Equipment | 2 | SNOMED | 2.16.840.1.113883.10.20.22.2.23 |
| Mental Status | 4 | SNOMED | 2.16.840.1.113883.10.20.22.2.56 |
| Functional Status | 4 | SNOMED | 2.16.840.1.113883.10.20.22.2.14 |
| Health Concern | 3 | SNOMED | 2.16.840.1.113883.10.20.22.2.58 |
| **Total** | **82** | | |

#### PDF Export Categories (page 11)

| PDF Export | Documentation Detail |
|---|---|
| Patient Demographic/Insurance | 1 sentence: "comprehensive view of demographics and insurance details" |
| Advance Directive | 1 sentence: "comprehensive view of Advance Directive" |
| Appointments | 1 sentence: "comprehensive view of Appointments" |
| Provider-to-Patient Messages | 1 sentence: "comprehensive view of messages" |
| Billing Data (Claim) | 1 sentence: "comprehensive view of billing data (CPT, ICD, Modifier)" |
| Documents | 1 sentence: "signed progress notes, lab results, radiology reports, scanned/uploaded documents" |

Each PDF export category has exactly **zero** field-level documentation. The descriptions are identical boilerplate ("offers a comprehensive view... structured for clarity and ease of access") with no indication of what specific fields, data elements, or layout the PDFs contain. No sample PDFs are provided.

#### FHIR Export (page 11)

One sentence states FHIR support for DocumentReference and Bulk Data EHI Export. No documentation of which FHIR resources are included, what profiles are used, what endpoints are available, or what data coverage is achieved. This appears to be a reference to the (g)(10) Standardized API functionality rather than an independently designed (b)(10) export mechanism.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has three tiers of documentation depth:

1. **C-CDA clinical data (well-documented)**: 24 sections with 82 data elements and CDA XPath mappings. This covers standard clinical summary content — demographics, encounters, problems, medications, allergies, labs, vitals, immunizations, procedures, care plans, goals, referrals, mental/functional status, health concerns, medical equipment, and social history. This is the standard C-CDA Clinical Summary, which is the same format used for transitions of care under (b)(1)/(b)(2)/(b)(3). The documentation is essentially a C-CDA implementation guide section-to-XPath mapping, not a description of the vendor's native data model.

2. **PDF exports for non-clinical data (barely documented)**: 6 categories covering demographics/insurance, advance directives, appointments, messages, billing claims, and documents. Each is described in a single boilerplate sentence. No field-level documentation, no sample output, no description of content structure. It is impossible to assess the completeness or depth of these exports from the documentation alone.

3. **FHIR export (undocumented)**: Mentioned in one sentence. No actionable information.

The C-CDA layer is the only part with substantive documentation, and it represents the standard clinical summary — approximately what USCDI v1/US Core covers. The PDF layer attempts to address non-clinical data gaps (billing, messages, appointments) but provides no evidence of depth or completeness.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | CCD: 6 elements (name, sex, DOB, race, ethnicity, language). PDF: "demographics and insurance details" (undocumented). | CCD covers USCDI demographics. Missing: address, phone, email, emergency contacts, preferred pharmacy. Some may be in the PDF export but no way to verify from documentation. |
| Encounters / visits | ✅ Covered | CCD Encounters section: code, diagnosis, performer, location, date (5 elements). CCD Date/Location of Visit: 2 elements. | Basic encounter data present. Missing encounter-level detail that the EHR likely stores: visit type, chief complaint detail, duration, room, referring provider. |
| Problems / conditions | ✅ Covered | CCD Problems: problem, status, active date (3 elements). SNOMED + ICD-10. | Standard coverage. |
| Medications / prescriptions | ⚠️ Partial | CCD Medications: medication, directions, start/end date, status (5 elements). RxNorm + NDC. | Medication list is covered. E-prescribing transaction details (pharmacy, fill status, refill history, prior auth) likely stored by the product but not in C-CDA. |
| Allergies | ✅ Covered | CCD Medication Allergies: substance, reaction, severity, status (4 elements). | Standard coverage. |
| Immunizations | ✅ Covered | CCD Immunizations: 9 elements including vaccine, date, status, route, site, manufacturer, dose, lot number, notes. | Thorough for C-CDA. |
| Vitals | ✅ Covered | CCD Vitals: observation, date/time (2 elements). LOINC. | Standard coverage. Individual vital types not enumerated but follow LOINC. |
| Lab results | ✅ Covered | CCD Lab Tests (4 elements), Lab Information (5 elements), Lab Values/Results (5 elements) = 14 elements total. LOINC. | Good coverage for structured lab data. |
| Imaging / diagnostic reports | ⚠️ Partial | PDF Documents category mentions "radiology reports." No CCD section for imaging results. | Radiology reports exported as PDF documents (human-readable only). No structured imaging order or result data in the CCD. |
| Procedures | ✅ Covered | CCD Procedures: procedure, date (2 elements). CPT-4, SNOMED, HCPCS. | Standard coverage. |
| Clinical notes / documents | ✅ Covered | PDF Documents: "signed progress notes, available lab results, radiology reports and any other scanned or uploaded document." | Documents exported as PDFs organized by type. This appropriately captures unstructured clinical documentation. |
| Care plans / goals | ✅ Covered | CCD Treatment Plan: 2 elements. CCD Goal: 3 elements. | Standard coverage. |
| Orders / referrals | ⚠️ Partial | CCD Reason for Referral: 1 element. CCD Treatment Plan mentions "referrals to other providers." | Referral reasons captured. Pending orders, order status, and order history are not documented. |
| Insurance / coverage | ⚠️ Partial | PDF: "Patient Demographic/Insurance" (undocumented content). | Insurance is mentioned but with zero field-level documentation. Cannot assess whether this includes plan details, subscriber info, group numbers, eligibility dates, or just a plan name. |
| Claims / billing | ⚠️ Partial | PDF: "Billing Data (Claim)" described as "CPT, ICD, Modifier." | The product has extensive RCM capabilities (claims tracking, denial management, payment posting, CollectiveIQ rules engine). The PDF export mentions only CPT, ICD, and Modifier — this likely captures charge data but almost certainly misses claims lifecycle data (submission status, denials, appeals, EOBs). PDF format makes the data non-computable. |
| Payments | ❌ Not covered | No mention of payment data in the export. | The product processes payments (online bill pay, payment plans, payment posting). No payment records are documented in the export. Significant gap. |
| Consents / directives | ✅ Covered | PDF: "Advance Directive" category. | Present but undocumented in terms of content. |
| Patient communications | ⚠️ Partial | PDF: "Provider-to-Patient Messages" category. | Secure messages exported as PDF (non-computable). Missing: patient portal activity, intake form submissions, appointment requests, check-in records from Breeze. |
| Specialty-specific data | ❌ Not covered | No specialty-specific data elements in the CCD or PDF exports. | The product serves 50+ specialties with configurable templates and specialty-specific charting. Custom template fields that don't map to standard CCD sections would be lost in the C-CDA projection. No evidence of specialty data export. |

## 6. Documentation Quality

**Overall: Thin.** The documentation is a single 11-page PDF that describes what the export *is* at a high level but does not provide the detail needed to independently use, validate, or import the exported data.

**What's adequate:**
- The CCD section-to-XPath mapping (pages 6–10) gives enough information to parse a standard C-CDA document, though this is largely redundant with the C-CDA IG itself. A developer familiar with C-CDA would not need this mapping; a developer unfamiliar with C-CDA would need much more.
- The export process steps (pages 3–5) clearly explain how to trigger the export through the UI.
- Code system OIDs are documented for CCD elements.

**What's missing or inadequate:**
- **No field-level documentation for PDF exports**: The 6 PDF export categories get one sentence each. A developer cannot build an import for these without obtaining and reverse-engineering sample PDFs.
- **No sample data**: No sample C-CDA documents, no sample PDFs, no sample FHIR responses.
- **No machine-readable schemas**: No XSD, JSON Schema, or other machine-readable artifact.
- **No relationship documentation**: No documentation of how entities relate to each other.
- **No cardinality or optionality**: No indication of which elements are required vs. optional.
- **No value set documentation**: Code system OIDs are listed but specific value sets within those systems are not.
- **No FHIR documentation**: The FHIR export is mentioned in one sentence with no actionable detail.
- **No data types**: Beyond what's implicit in the CDA standard.
- **No versioning or changelog**: Single creation date (November 2023), no update history.

A developer could parse the C-CDA output using the referenced IG standard and existing C-CDA libraries. The PDF exports and FHIR export are essentially undocumented — a developer would need sample data, vendor assistance, or both to work with them.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The core export is a C-CDA Clinical Summary — the same format used for transitions of care under (b)(1)/(b)(2)/(b)(3). This covers standard clinical summary content (approximately USCDI v1 scope) but is a projection of vendor data into a standard format, not an export of the vendor's native data model. The supplementary PDF exports attempt to address non-clinical data (billing, messages, appointments) but are non-computable and effectively undocumented. The FHIR export is mentioned but undocumented.

### Key Findings

1. **The export is C-CDA repackaging with PDF supplements.** The "Clinical Summary CCD" export is explicitly the same mechanism used for transitions of care — it is not a native database export. The 24 CCD sections and 82 data elements represent standard clinical summary content, not the full breadth of data CareCloud stores. (Source: pages 3–5 and 6–10 of `ehi-export-documentation.pdf`)

2. **Non-clinical data is exported as PDF — non-computable and undocumented.** Billing claims, insurance details, appointments, messages, and documents are exported as PDF files with zero field-level documentation. PDF format preserves data for human reading but makes it essentially impossible to programmatically import or analyze. (Source: page 11 of `ehi-export-documentation.pdf`)

3. **The integrated platform's richest data domains are poorly covered.** CareCloud Central (practice management) stores detailed claims lifecycle data, denial management, payment records, and revenue cycle analytics. The export captures only "CPT, ICD, Modifier" billing data as a PDF. CareCloud Breeze (patient portal) stores intake forms, check-in records, appointment requests, and online payment transactions — none of which are documented in the export. (Source: `product-research.md` vs. page 11 of `ehi-export-documentation.pdf`)

4. **No sample data or machine-readable schemas exist.** The entire (b)(10) documentation is a single 11-page PDF with no accompanying artifacts. There are no sample exports, no XSD/JSON schemas, and no FHIR capability statements. The FHIR Bulk Data export is described in one sentence. (Source: `files.json` — only 2 files collected, one is a screenshot)

5. **Specialty-specific clinical data is likely lost in the C-CDA projection.** CareCloud serves 50+ specialties with configurable templates and charting-by-exception. Custom template fields that don't map to standard C-CDA sections have no documented export path. (Source: `product-research.md` specialty template documentation vs. CCD data dictionary scope)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + PDF + FHIR (undocumented)
Model type:      Standard projection (C-CDA) with PDF supplements
Entities:        24 CCD sections + 6 PDF export categories = 30 total
Fields:          82 CCD data elements; PDF exports undocumented
Descriptions:    0% (element names and XPaths only, no prose descriptions)
Sample data:     No
Bulk export:     Yes (C-CDA bulk via Analytics; PDF/FHIR unclear)
Domains covered: 8 of 17 applicable domains adequately; 7 partial; 2 not covered
```

### Bottom Line

CareCloud's (b)(10) export is primarily its existing C-CDA Clinical Summary relabeled as an EHI export, supplemented by PDF printouts of billing, messaging, and administrative data. The C-CDA covers standard clinical summary content but misses the vendor-specific, specialty-specific, and administrative/financial data that CareCloud's integrated platform stores. A patient receiving this export would get a readable clinical summary and PDF printouts, but would lose the structured billing data, payment history, e-prescribing details, patient portal activity, and custom specialty documentation that constitute much of their designated record set. The single biggest gap is the absence of a structured, computable export of the practice management and billing data that CareCloud Central stores.
