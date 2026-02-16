# EHI Export Analysis: Acurus Solutions, Inc.

**Product**: Capella EHR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.02.05.2669.ACUR.01.01.1.220131 (CHPL ID 10807)

## 1. Product Context

Capella EHR is an integrated EHR + Practice Management system developed by Acurus Solutions, Inc., a subsidiary of Akido Labs, Inc. It is primarily used within Akido Care's own clinical network (~240 providers, 100 clinics, 500,000+ patients) and may also be offered to external ambulatory practices. Certified as an ambulatory EHR (version 6.1, January 2022) with 40+ ONC certification criteria.

**Clinical capabilities** (confirmed by certification): Patient demographics, problem lists, medication lists, allergy lists, CPOE, clinical decision support, drug interaction checking, implantable device tracking, family health history, vital signs, clinical quality measures, immunization and cancer case reporting.

**Practice management capabilities** (confirmed by product descriptions): Appointment scheduling, revenue cycle management (RCM), HCC coding support, claims and referral management. The product is described as "EHR + Practice Management" with RCM as part of the "Capella suite."

**Interoperability**: C-CDA exchange (b)(1)-(b)(3), FHIR R4 API (g)(7)/(g)(10) via EMR Direct, Direct secure messaging (h)(1), patient portal (e)(1)/(e)(3).

**Baseline expectation for EHI export**: Given the integrated EHR+PM scope, a genuine (b)(10) export should cover clinical data (demographics, encounters, problems, meds, allergies, labs, vitals, notes, immunizations, procedures, care plans, referrals, implantable devices) AND practice management data (billing/claims, scheduling, insurance, payments, referral workflows).

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `170.315(b)(10)-EHI-export-v3.pdf` | 547 KB, 9 pages | **Primary (b)(10) documentation.** Describes a CCD-based export with 24 C-CDA sections and 82 data elements. Includes UI screenshots for single-patient and bulk export. Dated Sep 5, 2023. | **Most informative** — sole (b)(10) documentation |
| `170.315-g10-API-Documentation.pdf` | 346 KB, 11 pages | FHIR R4 API documentation for (g)(10). Documents US Core 3.1.1 FHIR API at fhir.capellaehr.com/r4. Useful for context (separate from (b)(10) mechanism). | Contextual |
| `170.315-g7-g9-API-Documentation.pdf` | 333 KB, 9 pages | API documentation for (g)(7)/(g)(9) single-patient FHIR API. | Contextual |
| `certification-page-screenshot.png` | 606 KB | Screenshot of acurussolutions.com/Certification.html showing documentation links. | Low — confirms download links |

## 3. Export Mechanics

- **Format**: C-CDA (CCD) — Consolidated CDA Templates for Clinical Notes, DSTU R2.1, August 2015 (§170.205(a)(4))
- **Output**: CCD XML plus Adobe PDF format (human-readable)
- **Single-patient export**: User selects sections from a checklist, clicks "Generate CCD"
- **Bulk export**: Select multiple patients by provider or appointment date range, generate CCD for all selected patients
- **Mechanism**: UI-driven (screenshots show an in-application interface)
- **Additional**: "Ability to download Images / Clinical notes on demand" (mentioned in overview but not further detailed)
- **Access constraints**: No fees mentioned. Contact capella-support@akidolabs.com for assistance
- **Scheduling**: Documentation mentions an "export scheduler for recurring exports" (per screenshot, though details are minimal)

## 4. Export Content: What's In It

The export consists of a standard C-CDA (CCD) document. The documentation provides a mapping table listing 24 CDA sections with 82 total data elements, specifying XPATH paths and code systems for each element.

**Documentation quality for each element:**
- **82 data elements** across 24 sections
- **0 field descriptions** — elements are listed by name only (e.g., "Patient Name," "Date," "Status") with no explanatory descriptions
- **0 explicit type definitions** — no data types specified
- **27 elements** have code system references (SNOMED, LOINC, CPT, RxNorm, CVX, NCI Thesaurus, etc.)
- **No value sets** enumerated — code system OIDs are referenced but specific allowed values are not listed
- **No relationships/foreign keys** — this is a flat CDA document, not a relational model
- **No sample data** provided

### Vendor's own content organization

The vendor organizes the export as standard CCD sections. All 24 sections are CCD sections with CDA template OIDs:

| CCD Section | Data Elements | Has OID | Code Systems Referenced |
|---|---|---|---|
| Patient Demographics/Information | 6 | No | AdministrativeGender, Race & Ethnicity CDC |
| Provider's name and office contact information | 3 | No | None |
| Date and Location of visit | 2 | Yes | None |
| Chief Complaint and Reason for visit | 1 | Yes | None |
| Encounters | 5 | Yes | CPT, SNOMED, ICD10 |
| Immunizations | 9 | Yes | CVX, CPT-4, NCI, SNOMED |
| Instructions | 1 | Yes | SNOMED |
| Treatment Plan | 2 | Yes | LOINC |
| Social History | 3 | Yes | LOINC, SNOMED |
| Problems | 3 | Yes | SNOMED, ICD10 |
| Medications | 5 | Yes | RxNorm, NDC |
| Medication Allergies | 4 | Yes | RxNorm, SNOMED |
| Laboratory Tests | 4 | No | LOINC |
| Laboratory Information | 5 | No | None |
| Laboratory value(s)/result(s) | 5 | Yes | LOINC |
| Vitals | 2 | Yes | LOINC |
| Goal | 3 | Yes | None |
| Procedures | 2 | Yes | CPT-4, SNOMED, HCPCS |
| Care team member(s) | 3 | Yes | None |
| Reason for Referral | 1 | Yes | SNOMED |
| Medical Equipment | 2 | Yes | SNOMED |
| Mental Status | 4 | Yes | SNOMED |
| Functional Status | 4 | Yes | SNOMED |
| Health Concern | 3 | Yes | SNOMED |
| **TOTAL** | **82** | | |

This is a standard set of C-CDA sections. There are no vendor-specific extensions, no custom sections, and no data elements beyond what the C-CDA standard defines. The sections map directly to standard CCD template OIDs from the HL7 Consolidated CDA Implementation Guide.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly what a standard CCD document covers — a clinical summary. The 24 sections map to the standard C-CDA CCD template sections:

- **Clinical core**: Problems, medications, allergies, lab results, vitals, immunizations, procedures — adequately represented with standard CDA elements
- **Encounter context**: Encounters, chief complaint, date/location — basic encounter framing
- **Care planning**: Goals, treatment plan, instructions, care team, referral reasons — present but thin (1-3 elements each)
- **Health status**: Mental status, functional status, health concerns, social history — present as standard CCD sections
- **Patient demographics**: 6 basic elements (name, sex, DOB, race, ethnicity, language)
- **Devices**: Implantable device section (medical equipment)

No section goes beyond the standard CCD template. The deepest section is Immunizations with 9 elements; most sections have 2-5 elements. There are no vendor-specific or product-specific data elements — this is a stock CCD.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | 6 basic elements (name, sex, DOB, race, ethnicity, language) | Missing: address, phone, email, emergency contacts, employer, marital status — basic demographic fields any EHR stores |
| Encounters / visits | ⚠️ Partial | Encounters section (5 elements: code, performer, diagnosis, location, date) | Only encounter-level summary data; no detailed visit documentation |
| Problems / conditions | ⚠️ Partial | Problems section (3 elements: problem, status, active date) | Minimal — no onset context, severity, verification, linked orders |
| Medications / prescriptions | ⚠️ Partial | Medications section (5 elements: medication, directions, start/end date, status) | Missing: dosage details, pharmacy, prescriber, refill info, prior auths |
| Allergies | ✅ Covered | Medication Allergies section (4 elements: substance, reaction, severity, status) | Reasonable for standard CCD scope |
| Immunizations | ✅ Covered | Immunizations section (9 elements) | Most complete section; includes vaccine, route, site, dose, lot, manufacturer |
| Vitals | ⚠️ Partial | Vitals section (2 elements: observation, date/time) | Only 2 elements — individual vital types not enumerated |
| Lab results | ⚠️ Partial | Three lab sections (14 elements total) | Covers test info, results, and lab information; reasonable for CCD |
| Imaging / diagnostic reports | ❌ Not covered | No imaging section in export | Product likely handles imaging orders/reports; gap |
| Procedures | ⚠️ Partial | Procedures section (2 elements: procedure, date) | Very thin — no details beyond procedure code and date |
| Clinical notes / documents | ❌ Not covered | No clinical notes section in CCD export | Documentation mentions "download Images / Clinical notes on demand" separately, but no structured export of notes. Significant gap |
| Care plans / goals | ⚠️ Partial | Goal (3 elements) + Treatment Plan (2 elements) | Present but minimal |
| Orders / referrals | ⚠️ Partial | Reason for Referral section (1 element) + Treatment Plan (planned observations) | No order details, no referral tracking |
| Insurance / coverage | ❌ Not covered | No insurance/coverage data in export | Product is "EHR + Practice Management" — insurance data is stored; significant gap |
| Claims / billing | ❌ Not covered | No billing/claims entities in export | Product has RCM module; significant gap |
| Payments | ❌ Not covered | No payment data in export | Product has RCM; significant gap |
| Consents / directives | ❌ Not covered | No consent/advance directive section | Gap |
| Patient communications | ❌ Not covered | No portal messages, secure messaging data | Product has patient portal (e)(1)/(e)(3); gap |
| Family health history | ❌ Not covered | No family history section despite (a)(12) certification | Product is certified for family health history; gap |
| Specialty-specific data | ❌ Not covered | No specialty-specific sections | Product serves multiple specialties per SED; gap if specialty workflows exist |

**Summary**: 2 domains adequately covered, 8 domains partially covered (thin CCD representation), 9 domains not covered at all. The export covers only the standard CCD clinical summary; all practice management, billing, insurance, patient communication, and non-CCD clinical data are absent.

## 6. Documentation Quality

- **Data dictionary**: No true data dictionary exists. The PDF provides a CDA section-to-element mapping table — essentially a reference to what's in a standard CCD document, not a product-specific data dictionary.
- **Field descriptions**: None. Elements are listed by name only.
- **Types**: None explicitly stated (implicitly defined by CDA data types).
- **Relationships**: None documented (CDA structure is inherent but not explained).
- **Value sets**: Code system OIDs are referenced but no enumerated value sets.
- **Sample data**: None provided.
- **Machine-readable schemas**: None. The documentation is a 9-page PDF.
- **Import feasibility**: A developer familiar with C-CDA could process the output (it's a standard CCD), but the documentation adds little value beyond pointing to the CDA standard itself. There is no product-specific mapping guide, no explanation of what internal data maps to which CDA element, and no coverage of data that doesn't fit in a CCD.

The documentation is essentially: "We export a CCD. Here are the sections." It adds no product-specific insight beyond what the C-CDA standard already defines.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only what a standard CCD document contains — approximately the USCDI clinical summary scope. For a product described as "integrated EHR + Practice Management" with RCM, claims management, scheduling, patient portal, multi-specialty workflows, and 500,000+ patients, the CCD export covers a narrow slice of the designated record set. Entire domains the product stores (billing/claims, insurance, payments, patient communications, clinical notes, family history, imaging, consent forms) are absent. The 82 data elements across 24 CCD sections represent standard clinical exchange, not a comprehensive EHI export.

**Axis 2 — Export approach: Repackaged existing export**

This is clearly a repackaged C-CDA export being labeled as (b)(10). The evidence is unambiguous:

1. The documentation explicitly states: "Capella EHR meets the certification criterion §170.315(b)(10) Electronic Health Information export by implementing the CCD Export"
2. The output format is the same C-CDA CCD used for transitions of care (b)(1)-(b)(3)
3. The standard referenced (§170.205(a)(4) HL7 CDA R2) is the transitions of care standard, not an EHI-specific format
4. All 24 sections use standard CCD template OIDs with no vendor extensions
5. There is no product-specific data dictionary — just a reference to standard CDA elements
6. No billing, insurance, scheduling, or practice management data is included
7. The (g)(10) FHIR API documentation is a completely separate document, confirming the vendor has two clinical exchange mechanisms (CCD and FHIR) and chose CCD for (b)(10) — neither is an EHI-specific export

### Key Findings

1. **The (b)(10) export is explicitly a CCD export** — the documentation says so in its opening sentence, references the transitions of care CDA standard, and produces standard CCD XML. This is a clinical summary, not an EHI export.

2. **Zero practice management data is exported** despite the product being described as "integrated EHR + Practice Management" with RCM, claims management, and billing capabilities. This is the most significant gap.

3. **Documentation is extremely thin** — 9 pages, 82 data elements, no field descriptions, no types, no value sets, no sample data, no product-specific mapping. The mapping table merely lists standard CDA section names and element XPATHs.

4. **Clinical notes are notably absent** from the structured export, despite being a core EHR function. The documentation mentions downloading "Images / Clinical notes on demand" separately, suggesting these are handled outside the CCD but not in a structured or documented way.

5. **Family health history is missing** from the CCD sections despite the product being certified for §170.315(a)(12) Family Health History — an unusual omission even within the CCD scope.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA (CCD) + PDF
    Entities:        24 CCD sections
    Fields:          82 data elements
    Descriptions:    0% (no field descriptions)
    Sample data:     No
    Bulk export:     Yes (by provider or date range)
    Domains covered: 2 of 19 applicable domains adequately; 8 partial

### Bottom Line

The Capella EHR (b)(10) export is a standard CCD document relabeled as an EHI export. With 82 data elements across 24 standard CDA sections, it covers basic clinical summary data but omits billing, insurance, payments, clinical notes, patient communications, and all practice management data that the integrated EHR+PM product stores. A patient or provider receiving this export would get a clinical summary — not a complete copy of their designated record set.
