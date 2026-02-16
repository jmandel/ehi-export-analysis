# EHI Export Analysis: CareCloud, Inc.

**Product**: CareCloud Prime  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2790.Clou.02.02.1.240821

## 1. Product Context

CareCloud Prime is a cloud-based, ONC-certified EHR platform from CareCloud, Inc. (NASDAQ: CCLD), serving over 40,000 ambulatory providers across a wide range of specialties. It is an integrated suite combining EHR, practice management, and revenue cycle management (RCM).

**Key data domains the product stores** (per product-research.md and vendor website):

- **Clinical**: Problem lists, medications, allergies, vitals, labs, imaging orders, clinical notes (including AI-generated summaries), immunizations, care plans, procedures, clinical decision support alerts
- **Medications & Prescribing**: ePrescribing (including EPCS), drug interactions, Surescripts integration
- **Scheduling & Workflow**: Appointment calendars, patient check-in, task management
- **Billing & Financial**: Insurance eligibility, claims submission/tracking/scrubbing, payment records, denial management, contract rates, patient statements — full RCM capabilities
- **Patient Portal**: Intake forms, secure messaging, appointment requests, prescription refill requests, consent forms, telehealth
- **Documents**: Scanned/uploaded documents, progress notes, lab reports, radiology reports
- **Reporting**: Clinical quality measures, public health reporting, analytics

This is a comprehensive ambulatory platform with deep billing/RCM capabilities. A genuine (b)(10) export should cover clinical data, billing/claims detail, insurance information, patient communications, documents, and custom forms.

## 2. Artifacts Reviewed

| Artifact | Description | Informative Value |
|---|---|---|
| `certification_b10_ehi_export_documentation.pdf` (1.1 MB, 12 pages) | Primary EHI export documentation. Contains overview, UI screenshots for single/bulk export, C-CDA data dictionary (pp. 6–10), brief PDF export descriptions (p. 11), one-sentence FHIR mention (p. 12). | **Most informative** — sole substantive artifact |
| `screenshot-cc-prime-page-top.png` (859 KB) | Screenshot of marketing page at registered URL | Low — confirms URL is a marketing page, not dedicated EHI docs |
| `screenshot-footer-ehi-link.png` (201 KB) | Screenshot showing the PDF link location in the page footer | Low — shows where to find the PDF |

Only one substantive artifact exists: the 12-page PDF. No sample data, no machine-readable schemas, no JSON/XML examples, no additional data dictionaries.

## 3. Export Mechanics

- **Format**: Three formats described:
  1. **C-CDA XML** (clinical data) — standard CCD per § 170.205(a)(4)
  2. **PDF** (non-clinical data) — demographics/insurance, appointments, billing, messages, documents
  3. **FHIR** — briefly mentioned; "single-patient FHIR DocumentReference and FHIR Bulk Data EHI Export"
- **Mechanism**: UI-driven (screenshots show "CCDA Export" and "Data Portability" tabs within the application's Reports section)
- **Single-patient**: Yes — via CCDA Export tab, select patient and generate
- **Bulk export**: Yes — via Data Portability tab, select date range and export ZIP of CCDAs
- **Access constraints**: Practice administrator controls user access; no mention of fees
- **FHIR Bulk Data**: Mentioned in one sentence for patient population export per § 170.315(b)(10)(ii), with no further detail

## 4. Export Content: What's In It

### C-CDA Clinical Data (pages 6–10)

The data dictionary maps **24 C-CDA sections** with **81 data elements** total. This is a standard CCD section-by-field mapping using HL7 C-CDA R2.1 templates. For each data element, the PDF provides:
- Field name
- XPATH or CDA entry template OID (for ~27 fields)
- Code system OID and name (for 27 fields)

**No field-level descriptions** are provided — only names and code system references. No data types, no value sets, no cardinality, no relationships, no sample values.

### PDF Exports (page 11)

Six categories of data are exported as PDF files, each described in a single sentence:

1. **Patient Demographic/Insurance** — "comprehensive view of demographics and insurance details"
2. **Advance Directive** — "comprehensive view of Advance Directive"
3. **Appointments** — "comprehensive view of appointments"
4. **Provider-to-Patient Messages** — "comprehensive view of messages"
5. **Billing Data (Claim)** — "comprehensive view of billing data (CPT, ICD, Modifier)"
6. **Documents** — "signed progress notes, lab results, radiology reports, scanned/uploaded documents"

**No field-level detail** is provided for any PDF export — no data dictionary, no field lists, no schema, no sample output. The word "comprehensive" is used repeatedly but there is no way to verify what fields or data elements these PDFs actually contain.

### FHIR Export (page 12)

A single sentence: "CareCloud PRIME FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export for patient population as described in § 170.315(b)(10)(ii)."

No FHIR resource types listed, no profiles referenced, no data dictionary, no further detail.

### Vendor's own content organization

| Entity/Section | Fields | Code Systems | Format | Category |
|---|---|---|---|---|
| Patient Demographics/Information | 6 | 3 | C-CDA XML | Clinical |
| Provider's name and office contact information | 3 | 0 | C-CDA XML | Clinical |
| Date and Location of visit | 2 | 0 | C-CDA XML | Clinical |
| Chief Complaint and Reason for visit | 1 | 0 | C-CDA XML | Clinical |
| Encounters | 5 | 2 | C-CDA XML | Clinical |
| Immunizations | 9 | 3 | C-CDA XML | Clinical |
| Instructions | 1 | 1 | C-CDA XML | Clinical |
| Treatment Plan | 2 | 1 | C-CDA XML | Clinical |
| Social History | 3 | 2 | C-CDA XML | Clinical |
| Problems | 3 | 1 | C-CDA XML | Clinical |
| Medications | 5 | 1 | C-CDA XML | Clinical |
| Medication Allergies | 4 | 2 | C-CDA XML | Clinical |
| Laboratory Tests | 3 | 1 | C-CDA XML | Clinical |
| Laboratory Information | 5 | 0 | C-CDA XML | Clinical |
| Laboratory Results | 5 | 1 | C-CDA XML | Clinical |
| Vitals | 2 | 1 | C-CDA XML | Clinical |
| Goal | 3 | 0 | C-CDA XML | Clinical |
| Procedures | 2 | 1 | C-CDA XML | Clinical |
| Care team member(s) | 3 | 0 | C-CDA XML | Clinical |
| Reason for Referral | 1 | 1 | C-CDA XML | Clinical |
| Medical Equipment | 2 | 1 | C-CDA XML | Clinical |
| Mental Status | 4 | 1 | C-CDA XML | Clinical |
| Functional Status | 4 | 1 | C-CDA XML | Clinical |
| Health Concern | 3 | 1 | C-CDA XML | Clinical |
| Patient Demographic/Insurance | 0 | 0 | PDF | Administrative |
| Advance Directive | 0 | 0 | PDF | Clinical |
| Appointments | 0 | 0 | PDF | Administrative |
| Provider-to-Patient Messages | 0 | 0 | PDF | Patient Communications |
| Billing Data (Claim) | 0 | 0 | PDF | Billing |
| Documents | 0 | 0 | PDF | Clinical |
| FHIR Bulk Data Export | 0 | 0 | FHIR R4 | FHIR |

**Totals**: 31 entities, 81 documented fields (all in the C-CDA section), 0 fields with descriptions, 27 fields with code system references.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor describes a **three-layer export approach**:

1. **C-CDA XML** for clinical data: 24 standard CCD sections covering the USCDI-equivalent data elements. This is a standard C-CDA CCD export — the sections and data elements map directly to the HL7 C-CDA R2.1 specification with no vendor-specific extensions or custom content. The 81 data elements across 24 sections are exactly what you'd expect from a standard CCD.

2. **PDF exports** for non-clinical data: The vendor claims to export demographics/insurance, appointments, billing (CPT, ICD, Modifier), messages, advance directives, and documents as PDFs. This is the vendor's attempt to go beyond the standard C-CDA by capturing billing and administrative data. However, there is **zero field-level documentation** for these PDF exports — only single-sentence descriptions using the word "comprehensive."

3. **FHIR Bulk Data**: Mentioned in a single sentence with no detail. This appears to be the (g)(10) FHIR API relabeled — no evidence of any purpose-built FHIR export.

The C-CDA portion is the richest documented section but is entirely standard — this is the vendor's existing clinical exchange surface. The PDF exports represent an attempt to cover non-USCDI data (billing, messages, appointments) but are completely undocumented at the field level, making it impossible to assess their actual coverage or usefulness.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | C-CDA: 6 fields (name, sex, DOB, race, ethnicity, language); PDF: "demographics and insurance details" (no field detail) | C-CDA covers basic USCDI demographics. PDF may have more but undocumented. Product stores much more (contacts, addresses, emergency contacts, etc.) |
| Encounters / visits | ✅ Covered | C-CDA: Encounters section (5 fields: code, performer, diagnosis, location, date) | Standard C-CDA encounter data; likely thin vs. what the EHR stores internally |
| Problems / conditions | ✅ Covered | C-CDA: Problems section (3 fields: problem, status, active date) | Standard SNOMED/ICD10 coded problems; basic |
| Medications / prescriptions | ✅ Covered | C-CDA: Medications section (5 fields: medication, directions, start/end date, status) | Standard C-CDA medication data; no MAR, no prescribing workflow detail |
| Allergies | ✅ Covered | C-CDA: Medication Allergies (4 fields: substance, reaction, severity, status) | Standard allergy data |
| Immunizations | ✅ Covered | C-CDA: Immunizations (9 fields including vaccine, route, site, manufacturer, lot) | Reasonably detailed for a C-CDA section |
| Vitals | ⚠️ Partial | C-CDA: Vitals (2 fields: observation, date/time) | Only lists observation + date; no breakdown of specific vital types/values |
| Lab results | ✅ Covered | C-CDA: Laboratory Tests (3), Information (5), Results (5) — 13 fields total across 3 sections | Standard lab result data with LOINC coding |
| Imaging / diagnostic reports | ⚠️ Partial | PDF: Documents section mentions "radiology reports" | No structured imaging data in C-CDA; PDF may contain reports but undocumented |
| Procedures | ✅ Covered | C-CDA: Procedures (2 fields: procedure code, date) | Minimal — code + date only |
| Clinical notes / documents | ⚠️ Partial | PDF: "signed progress notes, lab results, radiology reports, scanned/uploaded documents" | Notes exported as PDFs (printouts), not as structured clinical note data; no C-CDA clinical notes section documented |
| Care plans / goals | ✅ Covered | C-CDA: Treatment Plan (2 fields), Goal (3 fields), Health Concern (3 fields) | Standard C-CDA care plan data |
| Orders / referrals | ⚠️ Partial | C-CDA: Reason for Referral (1 field) | Only reason for referral; no order details, no referral tracking |
| Insurance / coverage | ⚠️ Partial | PDF: "demographics and insurance details" (no field detail) | Claimed but completely undocumented; product has deep insurance/eligibility capabilities |
| Claims / billing | ⚠️ Partial | PDF: "comprehensive view of billing data (CPT, ICD, Modifier)" (no field detail) | Vendor acknowledges billing data export but provides zero documentation. Product has full RCM with claims, scrubbing, denials, appeals — unclear how much actually exports |
| Payments | ❌ Not covered | No mention | Product handles payments (patient and insurance); not mentioned in export |
| Consents / directives | ✅ Covered | PDF: Advance Directive section | Claimed but no field detail |
| Patient communications | ✅ Covered | PDF: Provider-to-Patient Messages | Claimed but no field detail |
| Specialty-specific data | ❌ Not covered | No specialty-specific entities | Product supports 40+ specialties with customizable templates; no specialty data in export |

## 6. Documentation Quality

**Overall: Poor.** The documentation is a 12-page PDF that provides:

- **Adequate**: UI screenshots showing where to initiate exports; C-CDA section-to-XPATH mapping for standard CCD content
- **Inadequate**: Zero field-level documentation for PDF exports (6 sections, each described in one sentence); one-sentence FHIR mention; no sample data; no machine-readable schemas
- **Missing entirely**: Field descriptions, data types, value sets, cardinality, foreign key relationships, sample export output

**Could a developer build an import?** For the C-CDA portion: yes, because it's a standard CCD — a developer would use the C-CDA spec, not this documentation. For the PDF exports: no — there is no documentation of what these PDFs contain, what fields they have, or how they're structured. For FHIR: no — nothing is documented.

The documentation relies heavily on the word "comprehensive" without providing any evidence of comprehensiveness. There are no machine-readable artifacts (no JSON schema, no XSD, no sample data files).

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export attempts to go beyond USCDI by including PDF exports for billing, appointments, messages, and documents alongside the standard C-CDA clinical export. This suggests awareness that (b)(10) requires more than clinical summaries. However:
- The C-CDA portion is entirely standard — 24 sections, 81 fields, all mapping to the HL7 C-CDA R2.1 spec with no vendor extensions. This is the existing clinical exchange surface.
- The PDF exports are completely undocumented. "Billing Data (Claim)" is described as containing "CPT, ICD, Modifier" — which sounds like a procedure/diagnosis code listing, not the full claims, denials, payments, and RCM data the product stores.
- No specialty-specific data is mentioned despite serving 40+ specialties.
- No custom forms, intake forms, or consent form data beyond "Advance Directive."
- Payments and detailed RCM data (denials, appeals, adjustments) appear absent.

The attempt to export billing and messaging as PDFs shows partial effort, but the total absence of documentation for these sections makes it impossible to confirm actual coverage.

**Axis 2 — Export approach: Repackaged existing export with modest additions**

The core of the export is a standard C-CDA CCD — this is the vendor's existing (g)(10) / clinical exchange capability. The PDF exports for billing, appointments, messages, and documents represent modest additions beyond the C-CDA baseline, but:
- They use PDF format (essentially printouts), not structured data
- They have zero documentation, suggesting minimal engineering investment
- The FHIR mention appears to be the (g)(10) API relabeled
- The C-CDA data dictionary is a verbatim mapping of the CDA spec, not a product-specific dictionary

This is primarily a repackaged C-CDA export with PDF printouts stapled on for non-clinical data.

### Key Findings

1. **Standard C-CDA is the documented core**: The only field-level documentation is for 24 C-CDA sections with 81 data elements — all standard CCD content with no vendor extensions. This is USCDI-scope clinical exchange, not a deep EHI export.

2. **PDF exports are documented in single sentences**: Six categories of non-clinical data (billing, appointments, messages, documents, insurance, advance directives) are claimed as PDF exports but have zero field-level documentation. It's impossible to verify what data they actually contain.

3. **Billing data is acknowledged but opaque**: The vendor explicitly mentions "Billing Data (Claim)" with "CPT, ICD, Modifier" as a PDF export — this is a positive signal that they're trying to include billing. But the product has deep RCM capabilities (claims scrubbing, denial management, contract analysis, payment processing) and there's no evidence these detailed billing workflows are represented.

4. **FHIR Bulk Data is a one-sentence mention**: "CareCloud PRIME FHIR server creates a single-patient FHIR resource Document Reference and supports FHIR Bulk Data EHI Export" — no resource types, no profiles, no detail. This appears to be the (g)(10) API mentioned as (b)(10).

5. **No sample data or machine-readable artifacts**: The entire documentation is a single 12-page PDF with no accompanying schemas, sample exports, or structured data dictionaries.

### Summary Stats

    Coverage:        Partial
    Approach:        Repackaged existing export (C-CDA + PDF printouts)
    Export format:   C-CDA XML + PDF + FHIR (mentioned)
    Entities:        31 (24 C-CDA sections + 6 PDF categories + 1 FHIR)
    Fields:          81 (all in C-CDA sections; 0 for PDF/FHIR)
    Descriptions:    0% (no field descriptions provided)
    Sample data:     No
    Bulk export:     Yes (C-CDA ZIP via Data Portability tab)
    Domains covered: 10 of 18 applicable domains (with several only partially)

### Bottom Line

CareCloud Prime's EHI export is primarily a standard C-CDA CCD clinical summary supplemented by undocumented PDF printouts for billing, appointments, and messages. While the vendor shows awareness that (b)(10) requires more than clinical data by including PDF exports for billing and communications, the complete absence of field-level documentation for these additions makes it impossible to verify their completeness. For a product with deep RCM capabilities, specialty template support, and patient engagement tools, the export documentation is far too thin — a patient or provider would get a standard clinical summary plus some PDF printouts, likely missing detailed billing/claims data, specialty-specific clinical content, custom forms, and structured portal data.
