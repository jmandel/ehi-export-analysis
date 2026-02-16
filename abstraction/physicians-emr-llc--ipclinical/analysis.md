# EHI Export Analysis: Physicians EMR, LLC

**Product**: IPClinical v2.1
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.2163.PEMR.01.00.1.200123

## 1. Product Context

IPClinical is a cloud-based EHR and practice management platform from Physicians EMR, LLC, a small vendor (~51–200 employees) in Longwood, FL founded by cardiologist Dr. Wasim Ahmar. It targets small-to-mid-size ambulatory practices across cardiology, spine care, primary care, and diagnostic centers.

The product combines:
- **EHR/Clinical**: CPOE, e-prescribing, clinical documentation (with virtual scribe service), document management, task management, immunization reporting, CQM tracking
- **Revenue Cycle Management**: Charge capture, claim submission, payment posting, AR management, eligibility verification, authorization services
- **Scheduling**: Appointment scheduling, reminders, cancellation lists
- **Patient Engagement**: Patient portal for viewing/downloading clinical info, online registration
- **Medical Documentation**: Transcription, record retrieval, fax management
- **Specialty**: Remote patient monitoring, cardiac device home monitoring

This breadth means a genuine (b)(10) export should cover: demographics, encounters, problems, medications, allergies, immunizations, vitals, labs, imaging, procedures, clinical notes, care plans, goals, orders/referrals, **billing/claims/payments**, **insurance/eligibility**, **scheduling/appointments**, **patient documents (scanned/faxed)**, **task data**, and **patient communications**. The product is certified across 47 ONC criteria, including (b)(10).

## 2. Artifacts Reviewed

| Artifact | Description | Informative? |
|---|---|---|
| `downloads/b_10_Electronic_Health_Information_export.pdf` (467 KB, 2 pages) | The sole (b)(10) documentation. Page 1 is a cover page; page 2 describes three export formats (C-CDA, FHIR, Excel/PDF) in a single page of prose. No data dictionary, no schema, no sample data. Created Nov 2023. | **Primary source**, but very thin |
| `downloads/IPClinical_g10_API_Documentation.pdf` (784 KB, 121 pages) | The (g)(10) FHIR API documentation. Covers SMART on FHIR auth, Bulk Data export, and US Core FHIR resources. Includes CapabilityStatement, search parameters, and JSON sample responses for each resource. Created May 2023. | Detailed for FHIR/US Core scope only |
| `downloads/IPClinical-api-documentation.pdf` (270 KB, 8 pages) | Older proprietary API doc (v5.0). Describes OAuth2 auth and a REST API returning C-CDA XML for USCDI v1 data classes. Created Mar 2024. | Supplementary; confirms USCDI v1 scope |

No additional artifacts exist — no data dictionary, no sample export files, no Excel templates, no schema files, no screenshots of the export UI.

## 3. Export Mechanics

- **Formats**: Three formats described:
  1. **C-CDA**: Consolidated Clinical Document Architecture per HL7 specs (USCDI v1 scope)
  2. **FHIR**: US Core STU V3.1.1 + FHIR Bulk Data Access V1.0.1 (identical to g(10) API)
  3. **Excel/PDF**: For non-clinical data (billing, scheduling, documents)
- **Mechanism**: The b(10) doc does not describe how to initiate the export (no UI screenshots, no API endpoints specific to b(10), no step-by-step instructions). The FHIR export mechanism is documented in the g(10) API doc (Bulk Data endpoints at `https://staging.pemr.com:93/api`). The Excel/PDF mechanism is entirely undocumented.
- **Scope**: Claims single patient and patient population export for C-CDA and FHIR. No specification for the Excel/PDF exports.
- **Fees**: The FHIR API documentation states "IPClinical does not currently charge any fees for the use of the API" but reserves the right to charge in the future.

## 4. Export Content: What's In It

### No data dictionary exists

IPClinical provides **no data dictionary** for the (b)(10) export. The FHIR resources are documented via standard US Core profiles in the g(10) doc, but these are generic FHIR specifications — not a product-specific data dictionary mapping IPClinical's internal data model to the export format. The Excel/PDF exports have zero documentation of structure, columns, data types, or content.

### FHIR/C-CDA content (g(10) = b(10))

The g(10) API doc documents 17 unique FHIR resource types across 29 profiles/views:

| Entity/Profile | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| Patient | 11 | 11 | yes | Clinical (FHIR) |
| AllergyIntolerance | 7 | 7 | yes | Clinical (FHIR) |
| CarePlan | 5 | 5 | yes | Clinical (FHIR) |
| CareTeam | 4 | 4 | yes | Clinical (FHIR) |
| Condition | 6 | 6 | yes | Clinical (FHIR) |
| Device (Implantable) | 3 | 3 | yes | Clinical (FHIR) |
| DiagnosticReport (Notes) | 6 | 6 | yes | Clinical (FHIR) |
| DiagnosticReport (Labs) | 6 | 6 | yes | Clinical (FHIR) |
| DocumentReference | 7 | 7 | yes | Clinical (FHIR) |
| Goal | 4 | 4 | yes | Clinical (FHIR) |
| Immunization | 5 | 5 | yes | Clinical (FHIR) |
| MedicationRequest | 7 | 7 | yes | Clinical (FHIR) |
| Observation (Smoking Status) | 4 | 4 | yes | Clinical (FHIR) |
| Observation (Lab Results) | 6 | 6 | yes | Clinical (FHIR) |
| Observation (Blood Pressure) | 7 | 7 | yes | Clinical (FHIR) |
| 10× Observation (other vitals/pediatric) | 6 each | varies | yes | Clinical (FHIR) |
| Procedure | 4 | 4 | yes | Clinical (FHIR) |
| Encounter | 5 | 5 | yes | Clinical (FHIR) |
| Organization | 4 | 4 | yes | Clinical (FHIR) |
| Practitioner | 2 | 2 | yes | Clinical (FHIR) |
| Provenance | 4 | 4 | yes | Clinical (FHIR) |

These are **standard US Core profiles** with no vendor-specific extensions or additional fields documented. The field counts above (161 total) reflect US Core Must Support elements. No IPClinical-specific data elements are mapped to FHIR.

### Excel/PDF content (undocumented)

The b(10) PDF's single paragraph about Excel/PDF exports:

| Entity (vendor's language) | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patient Documents (PDF) | 0 | N/A | N/A | Documents |
| Scheduling & Appointments (Excel/PDF) | 0 | N/A | N/A | Scheduling |
| Billing & Financial Information (Excel) | 0 | N/A | N/A | Billing |
| Imaging Result Reports (FHIR) | 0 | N/A | N/A | Clinical |

Zero fields are documented for any of these categories. The vendor says "most" billing data is exportable in Excel and "some" in PDF, with no clarification of what "most" or "some" means, what columns the Excel files contain, or what the structure looks like.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation divides the export into two tiers:

**Tier 1 — Clinical data via FHIR/C-CDA**: This is the vendor's existing g(10) API repackaged as (b)(10). It covers standard USCDI v1 data classes: demographics, allergies, conditions, medications, labs, vitals, immunizations, procedures, clinical notes, encounters, care plans, goals, care teams, implantable devices, smoking status, and provenance. The 121-page g(10) doc provides genuine technical detail (search parameters, sample JSON responses, CapabilityStatement). This tier is well-documented but covers only what every certified EHR must provide for clinical exchange — it's the USCDI floor.

**Tier 2 — Non-clinical data via Excel/PDF**: A single paragraph (approximately 80 words) mentions patient documents, scheduling/appointments, and billing/financial information. No schema, no field definitions, no sample files, no instructions. This tier purports to go beyond USCDI but provides zero documentation to substantiate the claim. A receiving party would have no way to anticipate or parse these exports.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | FHIR Patient (11 fields: name, DOB, sex, race, ethnicity, language, address, telecom) | Standard US Core only; product likely stores more (registration data, emergency contacts, employer) |
| Encounters / visits | ✅ Covered | FHIR Encounter (5 fields: status, class, type, subject, period) | US Core minimum; product's encounter records likely have more detail (visit reason, location, attending) |
| Problems / conditions | ✅ Covered | FHIR Condition (6 fields) | Standard US Core |
| Medications / prescriptions | ✅ Covered | FHIR MedicationRequest (7 fields) | US Core only; e-prescribing system likely stores pharmacy details, fill history, prior authorizations |
| Allergies | ✅ Covered | FHIR AllergyIntolerance (7 fields) | Standard US Core |
| Immunizations | ✅ Covered | FHIR Immunization (5 fields) | Standard US Core |
| Vitals | ✅ Covered | FHIR Observation (12 vital sign profiles) | Standard US Core vital signs |
| Lab results | ✅ Covered | FHIR Observation (Lab Results), DiagnosticReport | Standard US Core |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (Notes), b(10) mentions "Imaging Result Reports" via FHIR. No imaging-specific schema. | Product stores imaging results via "configurable interfaces"; export detail unclear |
| Procedures | ✅ Covered | FHIR Procedure (4 fields) | Standard US Core |
| Clinical notes / documents | ✅ Covered | FHIR DocumentReference (7 fields) + clinical notes guidance (11 pages in g10 doc). Also PDF export of scanned/faxed docs. | Clinical notes via FHIR are standard; PDF export of documents is mentioned but undocumented |
| Care plans / goals | ✅ Covered | FHIR CarePlan (5 fields), Goal (4 fields) | Standard US Core |
| Orders / referrals | ⚠️ Partial | MedicationRequest covers medication orders. No ServiceRequest or referral-specific resource. | Product has CPOE and referral capabilities ((a)(13) certified); referral data appears missing from export |
| Insurance / coverage | ❌ Not covered | Not mentioned in any export documentation | Product does in-app eligibility verification and stores insurance data; significant gap |
| Claims / billing | ⚠️ Partial | b(10) doc says "most" billing/financial info exportable in Excel. Zero detail on what's included. | Product has comprehensive RCM (charge capture, claim submission, payment posting, AR management). Mentioned but completely undocumented — cannot verify actual coverage |
| Payments | ⚠️ Partial | Subsumed under "billing & financial" but not specifically mentioned | Product handles payment posting and reconciliation; cannot verify |
| Consents / directives | ❌ Not covered | Not mentioned | Product likely stores consent forms (patient portal, treatment consents) |
| Patient communications / portal | ❌ Not covered | Not mentioned | Product has patient portal; communications data appears missing |
| Specialty-specific (cardiology/RPM) | ❌ Not covered | Not mentioned | Product offers RPM and cardiac device home monitoring; this data is not addressed in the export |

## 6. Documentation Quality

**Overall: Poor.** The (b)(10)-specific documentation is a single page of prose with no technical substance.

- **Can a developer use the export?** A developer could implement a FHIR US Core import from the g(10) doc alone — but that's the g(10) API, not something specific to (b)(10). A developer could **not** implement an import of the Excel/PDF exports; there is nothing to implement against.
- **What's well-documented?** The FHIR API (121 pages of genuine technical detail: search params, sample responses, CapabilityStatement, error codes).
- **What requires guesswork?** Everything beyond USCDI: billing structure, scheduling data format, document export mechanism, imaging export details. The Excel exports are a complete black box.
- **Machine-readable artifacts?** The g(10) API provides a CapabilityStatement JSON. No schemas, no sample export files, no OpenAPI specs for the b(10)-specific exports.
- **Completeness?** The b(10) doc does not describe: how to initiate the export, what the output looks like, how many files are generated, naming conventions, encoding, delimiters, column headers, or any structural detail for the non-FHIR exports.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The vendor acknowledges that (b)(10) requires more than USCDI by mentioning Excel/PDF exports for billing, scheduling, and documents. This is a positive signal — most repackaged exports don't even acknowledge non-clinical data. However, the acknowledgment is purely verbal: "most of the billing and financial information can be exported in Excel format" is a claim with zero documentation to substantiate it. The FHIR/C-CDA layer covers the standard USCDI clinical domains adequately. The Excel/PDF layer promises coverage of billing, scheduling, and documents but is completely undocumented — we cannot verify what's actually exported. Several domains the product stores (insurance/eligibility, patient communications, RPM/cardiac monitoring data, referrals, consents) are not mentioned at all. We give the benefit of the doubt on billing/scheduling/documents being present in some form but classify as Partial due to the undocumented nature and the missing domains.

**Axis 2 — Export approach: Repackaged existing export (with minor additions)**

The core of the (b)(10) export is the vendor's existing g(10) FHIR API and C-CDA exchange — this is explicitly stated in the documentation ("Kindly refer to IPClinical – (g)(10) FHIR API Documentation for API specifications"). The telltale signs are clear: the b(10) doc references USCDI v1, US Core 3.1.1, and FHIR Bulk Data — the exact standards for g(10). There is no product-specific data dictionary, no mapping of internal IPClinical data structures to the export format, and no vendor extensions. The Excel/PDF mention represents a modest acknowledgment that (b)(10) should go beyond g(10), but the complete absence of any schema or specification for these exports means they are effectively undocumented bolt-ons rather than a purpose-built EHI export system.

### Key Findings

1. **The (b)(10) export is the g(10) FHIR API relabeled**, with a vague mention of Excel/PDF for non-clinical data. The b(10)-specific documentation is a single page — the other 121 pages are the existing g(10) API docs. (Source: `b_10_Electronic_Health_Information_export.pdf`, p.2)

2. **Zero documentation exists for non-FHIR exports.** Billing, scheduling, and document exports are mentioned in a single paragraph with no schema, no column definitions, no sample files, and no export instructions. A developer cannot implement an import from this documentation. (Source: `b_10_Electronic_Health_Information_export.pdf`, p.2)

3. **Several product domains are absent from the export documentation entirely**: insurance/eligibility data, patient portal communications, RPM/cardiac monitoring data, referral workflows, and consent forms — all of which the product stores per its feature descriptions. (Source: comparison of `product-research.md` capabilities vs. export documentation)

4. **The FHIR layer is well-documented but standard.** The 121-page g(10) doc provides genuine technical detail for US Core resources, including sample responses and search parameters. However, it documents only standard US Core profiles — no vendor-specific extensions, no additional fields beyond the USCDI floor. (Source: `IPClinical_g10_API_Documentation.pdf`)

5. **The qualifier "most" for billing data is concerning.** The b(10) doc says "most of the billing and financial information can be exported in Excel format" — implying some billing data is not exportable, but without specifying what's included or excluded. (Source: `b_10_Electronic_Health_Information_export.pdf`, p.2)

### Summary Stats

    Coverage:        Partial
    Approach:        Repackaged existing export
    Export format:   FHIR R4 (US Core), C-CDA, Excel, PDF (mixed)
    Entities:        33 (29 FHIR profiles + 4 undocumented Excel/PDF categories)
    Fields:          161 (FHIR only; 0 for Excel/PDF)
    Descriptions:    77.6% of FHIR fields (0% for Excel/PDF)
    Sample data:     No (FHIR doc has JSON examples but no standalone sample exports)
    Bulk export:     Yes (FHIR Bulk Data)
    Domains covered: 10 of 18 applicable domains (clinical domains via FHIR; billing/scheduling/documents claimed but undocumented)

### Bottom Line

IPClinical's (b)(10) export is primarily its existing g(10) FHIR API with a vague mention of Excel/PDF for billing, scheduling, and documents — but zero documentation for these non-FHIR exports. A patient or provider would receive a standard USCDI clinical summary via FHIR/C-CDA, and possibly some billing/scheduling Excel files whose structure is unknowable from the documentation. The biggest gap is the complete absence of any data dictionary or schema for the non-clinical exports, making it impossible to verify whether the vendor's claim of covering "most" billing data is genuine or aspirational.
