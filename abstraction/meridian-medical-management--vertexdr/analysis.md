# EHI Export Analysis: Meridian Medical Management

**Product**: VertexDr v9.1
**Analysis date**: 2025-02-15
**CHPL ID**: 15.04.04.2112.Vert.09.01.1.221024 (CHPL #11002)

## 1. Product Context

VertexDr is a fully integrated electronic medical records (EMR) and practice management (PM) system developed by Meridian Medical Management, now a division of CareCloud, Inc. (NASDAQ: CCLD). The product was originally two separate systems — SSIMED (practice management) and EMRge (EMR) — rebranded as VertexDr in 2016. It is positioned as "one of the only fully-integrated EMR and PM systems built from the ground up."

**Target market**: Ambulatory physician practices, particularly large multi-specialty groups and academic faculty practice plans (200–600 providers). Notable customers include Hutchinson Clinic and The Polyclinic.

**Key data domains the product should store**:
- **Clinical**: Patient demographics, problem lists, medications, allergies, immunizations, lab results, vitals, clinical notes, procedures, care plans, e-prescribing (including EPCS), family health history
- **Practice management / billing**: Appointment scheduling, insurance enrollment, claims management with proactive claims editing, billing records, payments, revenue cycle management
- **Patient engagement**: Patient portal (via MedFusion), secure messaging (via DataMotion), SMS reminders
- **Analytics/reporting**: Embedded PrecisionBI analytics (operational/financial — likely not EHI)

The integration of EMR and PM in a single product means the (b)(10) export should cover both clinical and financial/billing domains comprehensively.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `VertexDr-b10-EHI-Export-Documentation.pdf` (716 KB, 11 pages) | Primary (b)(10) documentation. Contains export instructions with screenshots, C-CDA data element mapping table (pages 6–10), brief descriptions of PDF exports for non-clinical data, and a single sentence about FHIR. | **Most informative** — the only substantive artifact |
| `VertexDr-Mandatory-Disclosures.pdf` (135 KB, 1 page) | Costs and limitations for patient portal (MedFusion), secure messaging (DataMotion), and patient health info capture. Not EHI export documentation. | Low — provides context on third-party dependencies only |
| `vertexdr-homepage-full.png` (1.2 MB) | Full-page screenshot of vertexdr.com homepage | Low — confirms minimal web presence |
| `vertexdr-homepage-top.png` (853 KB) | Top portion of homepage | Low |
| `vertexdr-ehi-section-screenshot.png` (6 KB) | Screenshot of the "Electronic Health Information Export" heading on the homepage where the PDF is linked | Low — confirms one-click access to PDF |

**The entire (b)(10) documentation consists of a single 11-page PDF.** There are no supplementary schema files, no sample data, no API documentation, no data dictionary, and no machine-readable artifacts.

## 3. Export Mechanics

VertexDr describes three export mechanisms:

**1. C-CDA Export (Clinical Data)**
- **Format**: XML conforming to HL7 CDA R2 Consolidated CDA Templates (DSTU R2.1, August 2015), per § 170.205(a)(4)
- **Single patient**: File → Export CCD from patient chart; user selects which C-CDA sections to include
- **Bulk patient**: File → Export CCD(s) for Patients; generates a ZIP file with CCDA XML documents
- **Mechanism**: UI-driven within the VertexDr application

**2. PDF Exports (Non-Clinical Data)**
- **Format**: PDF (not machine-readable)
- **Mechanism**: Via the application's "Reports" section
- **Bulk capability**: Not mentioned; appears to be single-patient only
- **Organization**: Files saved to user-specified folder, sortable by document type and sub-type

**3. FHIR Data Export**
- **Documentation**: A single sentence on page 11: "VertexDr FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)."
- No endpoint URL, authentication details, resource types, format specifications, or sample payloads are provided. This is an unverifiable claim.

**Access constraints/fees**: None mentioned in the (b)(10) documentation. The Mandatory Disclosures PDF lists fees for the patient portal and secure messaging, but not for EHI export.

## 4. Export Content: What's In It

### C-CDA Clinical Data (Pages 6–10)

The PDF documents a C-CDA data element mapping table across 5 pages (pages 6–10). Based on manual verification of the extracted text:

- **24 C-CDA sections** documented
- **82 data elements** (fields) total across all sections
- **27 fields** (33%) have associated code system OIDs
- **30 fields** (37%) have XPATH or template OID references
- **0 fields** have descriptions, data types, cardinality, or optionality documented

The documentation provides field names, XPATH/entry paths, code system OIDs, and code system names — but **no field descriptions, no data types, no cardinality constraints, no value set enumerations, and no sample data**.

### PDF Exports (Page 11)

Six categories of non-clinical data are described for PDF export. Each receives a single boilerplate sentence:

| Category | Vendor Description |
|---|---|
| Patient Demographic/Insurance | "comprehensive view of demographics and insurance details" |
| Advance Directive | "comprehensive view of Advance Directive" |
| Appointments | "comprehensive view of appointments" |
| Provider-to-Patient Messages | "comprehensive view of messages" |
| Billing Data (Claim) | "comprehensive view of billing data (CPT, ICD, Modifier)" |
| Documents | "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" |

**No field-level documentation exists for any PDF export category.** The descriptions are identical boilerplate ("structured for clarity and ease of access") with no specifics about what fields are included.

### Vendor's own content organization

The vendor organizes the export into C-CDA sections (clinical) and PDF categories (non-clinical):

| Section/Category | Fields | Code Systems Specified | Category |
|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | C-CDA |
| Provider's name and office contact info | 3 | 0 | C-CDA |
| Date and Location of visit | 2 | 0 | C-CDA |
| Chief Complaint and Reason for visit | 1 | 0 | C-CDA |
| Encounters | 5 | 2 | C-CDA |
| Immunizations | 9 | 3 | C-CDA |
| Instructions | 1 | 1 | C-CDA |
| Treatment Plan | 2 | 1 | C-CDA |
| Social History | 3 | 2 | C-CDA |
| Problems | 3 | 1 | C-CDA |
| Medications | 5 | 1 | C-CDA |
| Medication Allergies | 4 | 4 | C-CDA |
| Laboratory Tests | 4 | 1 | C-CDA |
| Laboratory Information | 5 | 0 | C-CDA |
| Laboratory value(s)/result(s) | 5 | 1 | C-CDA |
| Vitals | 2 | 1 | C-CDA |
| Goal | 3 | 0 | C-CDA |
| Procedures | 2 | 1 | C-CDA |
| Care team member(s) | 3 | 0 | C-CDA |
| Reason for Referral | 1 | 1 | C-CDA |
| Medical Equipment | 2 | 1 | C-CDA |
| Mental Status | 4 | 1 | C-CDA |
| Functional Status | 4 | 1 | C-CDA |
| Health Concern | 3 | 1 | C-CDA |
| Patient Demographic/Insurance | — | — | PDF export |
| Advance Directive | — | — | PDF export |
| Appointments | — | — | PDF export |
| Provider-to-Patient Messages | — | — | PDF export |
| Billing Data (Claim) | — | — | PDF export |
| Documents | — | — | PDF export |

Full inventory available in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export has two tiers of documentation quality:

**C-CDA (well-structured, moderately documented)**: 24 sections mapping to standard USCDI/US Core clinical data elements. This covers the standard clinical summary content: demographics, problems, medications, allergies, labs, vitals, immunizations, procedures, encounters, social history, care team, goals, mental/functional status, health concerns, referrals, and medical equipment. The mapping table on pages 6–10 is the strongest part of the documentation, providing XPATH paths and code system OIDs for each element.

**PDF exports (minimally documented)**: 6 categories of non-clinical data — demographics/insurance, advance directives, appointments, messages, billing (claims), and documents. These receive no field-level documentation at all. The billing category mentions "CPT, ICD, Modifier" as the only specifics. The documents category mentions "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document."

**FHIR export (undocumented)**: A single sentence claims support for FHIR Document Reference and FHIR Bulk Data export. No technical details whatsoever.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 fields (name, sex, DOB, race, ethnicity, language); PDF: "demographics and insurance details" (unspecified) | C-CDA covers basic USCDI demographics. Detailed demographics (address, phone, emergency contacts, etc.) may be in the PDF export but are not documented at field level. |
| Encounters / visits | ✅ Covered | C-CDA Encounters section: code, performer, diagnosis, location, date (5 fields); Date and Location of visit (2 fields); Chief Complaint (1 field) | Standard encounter data covered via C-CDA |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA Problems section: problem (SNOMED + ICD-10), status, active date (3 fields) | Standard problem list covered |
| Medications / prescriptions | ✅ Covered | C-CDA Medications section: medication (RxNorm + NDC), directions, start/end date, status (5 fields) | Standard medication list covered. However, detailed e-prescribing transaction history (EPCS data, pharmacy transmissions) is not explicitly addressed. |
| Allergies | ✅ Covered | C-CDA Medication Allergies: substance (RxNorm), reaction, severity, status (4 fields, all with SNOMED coding) | Well-documented with code systems |
| Immunizations | ✅ Covered | C-CDA Immunizations: vaccine (CVX + CPT-4), date, status, route, site, manufacturer, dose, lot, notes (9 fields) | Most detailed C-CDA section |
| Vitals | ✅ Covered | C-CDA Vitals: observation (LOINC), date/time (2 fields) | Covered but thin — only 2 fields |
| Lab results | ✅ Covered | Three C-CDA sub-sections: Laboratory Tests (4 fields), Laboratory Information (5 fields), Laboratory value(s)/result(s) (5 fields) = 14 fields total | Relatively well-covered across 3 sub-sections |
| Imaging / diagnostic reports | ⚠️ Partial | PDF Documents export mentions "radiology reports" | Radiology reports included via PDF document export, but not as structured data |
| Procedures | ✅ Covered | C-CDA Procedures: procedure (CPT-4/SNOMED/HCPCS), date (2 fields) | Standard procedure data covered |
| Clinical notes / documents | ⚠️ Partial | PDF Documents export: "signed progress notes, available lab results, radiology reports, and any other scanned or uploaded document" | Notes exported as PDF documents — non-machine-readable. No structured note content, no note types/categories enumerated. |
| Care plans / goals | ✅ Covered | C-CDA Treatment Plan (2 fields) + Goal (3 fields) + Health Concern (3 fields) | Basic care planning data covered |
| Orders / referrals | ⚠️ Partial | C-CDA Reason for Referral (1 field); Treatment Plan mentions referrals and pending tests | Referral reason captured but no order detail (order IDs, statuses, fulfillment data) |
| Insurance / coverage | ⚠️ Partial | PDF export: "Patient Demographic/Insurance" — no field-level documentation | Product manages insurance enrollment. PDF export mentioned but no specifics on what insurance fields are included. Not machine-readable. |
| Claims / billing | ⚠️ Partial | PDF export: "billing data (CPT, ICD, Modifier)" — no field-level documentation | Product has full claims management and billing. Export includes billing data but only as PDF (non-machine-readable) with only 3 field types mentioned. The depth of billing data in the export is unknown. |
| Payments | ❌ Not covered | No evidence of payment data in export | Product handles revenue cycle management. No payment data appears in the export documentation. |
| Consents / directives | ✅ Covered | PDF export: "Advance Directive" | Advance directives exported (via PDF) |
| Patient communications / portal messages | ⚠️ Partial | PDF export: "Provider-to-Patient Messages" — no field-level documentation | Messages exported as PDF. Not machine-readable. No details on what message fields are included. |
| Family health history | ❌ Not covered | Not mentioned in any C-CDA section or PDF export | Product is certified for (a)(12) family health history. Not listed in C-CDA sections (might be subsumed under Social History, but not explicit). |

### Gap Analysis Summary

The C-CDA portion covers standard clinical data well — this is essentially what the (g)(10) FHIR API would provide. The PDF exports *acknowledge* that billing, insurance, appointments, messages, and documents exist, but provide no field-level detail and export them in a non-machine-readable format.

**Key gaps**:
1. **Payments**: Not mentioned at all despite the product having revenue cycle management capabilities
2. **Family health history**: Product is certified for (a)(12) but this data is not mentioned in the export
3. **Billing depth**: Only "CPT, ICD, Modifier" mentioned — what about claim status, amounts, payer info, dates of service, adjustments?
4. **E-prescribing transaction history**: Product has EPCS capability but prescription transaction details beyond the medication list are not addressed

## 6. Documentation Quality

**C-CDA mapping table (pages 6–10)**: Moderately useful. A developer familiar with C-CDA standards could use the XPATH paths and code system OIDs to validate exported C-CDA documents. However, the table lacks data types, cardinality, optionality, and value set enumerations. It essentially says "here are the standard C-CDA sections we populate" without adding vendor-specific detail.

**PDF export descriptions (page 11)**: Useless for development purposes. Identical boilerplate sentences for each category with no field definitions, no sample outputs, and no schema. A developer could not build an import from these descriptions. The only specific content is "CPT, ICD, Modifier" for billing and a list of document types.

**FHIR export (page 11)**: A single sentence that amounts to an unverifiable claim. No endpoint, no authentication, no resource types, no format, no sample data.

**Screenshots (pages 3–5)**: Show the UI for triggering single-patient and bulk C-CDA exports. Useful for understanding the export workflow but not for understanding output content.

**Overall documentation assessment**: A developer could understand the C-CDA portion (because it follows a well-known standard), but could not independently build an import for the non-clinical data. The documentation provides no machine-readable artifacts, no sample exports, and no data dictionary beyond the C-CDA element mapping. It would be very difficult to understand the full scope and structure of the export from this documentation alone.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is primarily a C-CDA projection of clinical data supplemented by non-machine-readable PDF exports for non-clinical domains. The C-CDA content maps directly to standard USCDI/US Core clinical data — the same data available through the (g)(10) FHIR API. The non-clinical PDF exports (billing, insurance, appointments, messages) acknowledge broader data domains but export them in PDF format with no field-level documentation. This is a standards-based clinical summary augmented by opaque PDF dumps, not a native data model export.

### Key Findings

1. **C-CDA is the backbone**: The export's documented clinical content is a standard C-CDA with 24 sections and 82 data elements. This is essentially the same data available through the certified (g)(10) FHIR API — a USCDI clinical summary, not a comprehensive EHI export of the native data model.

2. **Non-clinical data exported as non-machine-readable PDF**: Billing data, insurance information, appointments, messages, and clinical documents are all exported in PDF format. This defeats the purpose of data portability — a patient or third party cannot programmatically process billing records, insurance details, or appointment history from PDF files.

3. **Billing export is superficially documented**: Despite VertexDr being a fully integrated EMR+PM system with claims management, proactive claims editing, and revenue cycle management, the billing export documentation is a single sentence mentioning "CPT, ICD, Modifier." The depth of financial data in the export is unknown.

4. **FHIR Bulk Data export is an unverifiable claim**: A single sentence claims FHIR Bulk Data support with zero technical documentation. No endpoint, no auth, no resource types, no format. This cannot be evaluated.

5. **No native data model export**: The export does not expose VertexDr's internal database tables, relationships, or proprietary data structures. All output is either standard C-CDA or opaque PDF — there is no way to reconstruct the full data model from the exported formats.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML + PDF (dual format)
Model type:      Standard projection (C-CDA) + non-machine-readable PDFs
Entities:        24 C-CDA sections + 6 PDF categories = 30 documented components
Fields:          82 (C-CDA only; PDF categories have 0 documented fields)
Descriptions:    0% (field names and code systems only, no descriptions)
Sample data:     No
Bulk export:     Yes (C-CDA bulk via ZIP; FHIR bulk claimed but undocumented)
Domains covered: 9 of 17 applicable domains fully; 7 partial; 1 not covered
```

### Bottom Line

VertexDr's (b)(10) export is a C-CDA clinical summary with PDF printouts for non-clinical data. A patient would get a readable clinical record (via C-CDA) and printable copies of billing and insurance information (via PDF), but no machine-readable access to the billing, insurance, or practice management data that makes VertexDr distinctive as an integrated EMR+PM system. The single biggest gap is that the product's core differentiator — tight EMR/PM integration with comprehensive billing and revenue cycle management — is reduced to an opaque "billing data (CPT, ICD, Modifier)" PDF export with no field-level documentation.
