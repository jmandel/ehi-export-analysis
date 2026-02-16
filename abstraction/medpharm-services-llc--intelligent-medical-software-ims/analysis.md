# EHI Export Analysis: MedPharm Services LLC (Meditab)

**Product**: Intelligent Medical Software (IMS)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.99.04.2804.Inte.SP.01.1.181113 (CHPL ID 9739)

## 1. Product Context

Intelligent Medical Software (IMS) is a comprehensive all-in-one ambulatory EHR and practice management system developed by MedPharm Services LLC (an affiliate of Meditab Software, Inc.). It targets small-to-medium ambulatory practices and FQHCs, serving approximately 41,000 healthcare professionals across 1,600+ clinics.

IMS is a **Complete EHR** certified for 50 ONC criteria. It runs on a single Sybase SQL Anywhere database encompassing:

- **Clinical EHR**: Charting with specialty-specific modules for 40+ specialties (allergy, cardiology, dermatology, dental, fertility, mental health, OB/GYN, oncology, ophthalmology, orthopedics, etc.), problem lists, medication lists, allergy lists, vital signs, clinical notes, care plans, referral/authorization management
- **E-Prescribing**: Full Surescripts integration including EPCS, prior authorizations, drug interaction checking
- **Lab & Diagnostics**: Bi-directional lab interfaces with 90+ labs (Labcorp, Quest, etc.), medical device integrations
- **Billing & RCM**: Integrated billing — claims creation/scrubbing/submission, denial management, superbills, insurance posting, payment processing, patient statements. Users describe it as "a biller's dream"
- **Patient Portal & Engagement**: IMS Care portal/app with secure messaging, appointment scheduling, medication refill requests, document uploads, telemedicine (Televisit)
- **Practice Management**: Scheduling, task management, office management (EMO), practice analytics
- **Quality Reporting**: MIPS/MACRA, HEDIS, UDS (FQHC), HCC coding
- **Public Health**: Immunization registry, syndromic surveillance, cancer registry reporting

The breadth of this product — particularly the integrated billing/RCM, 40+ specialty modules, patient portal, and telemedicine — sets a high bar for what a genuine (b)(10) EHI export should cover.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.html` (326 KB) | Raw HTML of EHI export page (Duda SPA; requires browser rendering) | Low — JS shell, no static content |
| `downloads/ehi-export-page.png` (730 KB) | Full-page screenshot of EHI export page | **High** — shows complete page content: C-CDA section list and FHIR format description |
| `downloads/fhir-specifications.html` (3.3 MB) | Raw HTML of FHIR API specifications page (Duda SPA) | Medium — can grep for resource names, but needs browser rendering for full content |
| `downloads/fhir-specifications-top.png` (167 KB) | Viewport screenshot of FHIR specs page top | Medium — shows nav with 15 resource types (Document Reference in nav but not documented on page) |
| `downloads/enrichment/fhir-resources.json` (34 KB) | Browser-extracted FHIR resource definitions: 16 resources, 131 fields | **High** — structured field-level data for all documented FHIR resources |
| `downloads/enrichment/extraction-stats.json` (2 KB) | Extraction statistics | Medium — confirms counts and notes limitations |
| `downloads/enrichment/fhir-resources-browser-extract.json` (30 KB) | Raw browser extraction data | Medium — source for the normalized JSON |
| `downloads/enrichment/extract-fhir-specs.ts` (5 KB) | Extraction script | Low — methodology documentation |

**Most informative**: The full-page screenshot of the EHI export page (`ehi-export-page.png`) and the structured FHIR resource extraction (`fhir-resources.json`) together provide the complete picture of what the vendor documents.

**Least informative**: The raw HTML files are Duda SPA shells that contain no readable content without JavaScript rendering.

**No downloadable artifacts exist** — no PDFs, ZIPs, CSVs, JSON schemas, sample data, or data dictionary files were available from the vendor.

## 3. Export Mechanics

- **Format(s)**: C-CDA XML (USCDI v1 compliant) and FHIR R4 (US Core STU 3.1.1, Bulk Data STU 1.0.1)
- **Mechanism**: The EHI export page states IMS supports export "for an individual patient and the broader patient population." For FHIR, the vendor explicitly references "170.315(g)(10) for the Standardized API for patient and population services" — indicating the FHIR export is their g(10) API. No separate UI workflow, batch job, or vendor-assisted process is described for b(10).
- **Single-patient vs bulk**: Both individual and population-level export mentioned
- **Access constraints**: No fees, instructions, or access constraints are documented on the EHI export page. No user guide or step-by-step instructions are provided.

## 4. Export Content: What's In It

### C-CDA Export

The EHI export page lists 19 C-CDA sections by name only, with no field-level documentation:

1. Assessment
2. Clinical Notes
3. Durable Medical Equipment
4. Encounters
5. Family History
6. Functional Status
7. Goals
8. Health Concerns
9. Immunization
10. Laboratory Values/Results
11. Medications
12. Medication Allergies
13. Payer
14. Plan of Treatment
15. Problems
16. Procedures
17. Reason for Referral
18. Smoking Status and Tobacco Use
19. Vital Signs

These are standard C-CDA section types. No sample C-CDA documents, no CDA template OIDs, and no field-level mappings are provided. The vendor simply states compliance with "United States Core Data for Interoperability (USCDI), Version 1."

### FHIR Export

The FHIR specifications page documents 16 US Core resource types with field-level detail (131 total fields, all with descriptions and data types):

| Resource Type | Fields | Category | Notes |
|---|---|---|---|
| Patient | 13 | Demographics | Standard US Core Patient |
| MedicationRequest | 12 | Medications | Standard US Core |
| Device | 11 | Medical Devices | Standard US Core |
| Immunization | 11 | Immunizations | Standard US Core |
| Encounter | 10 | Encounters | Standard US Core |
| DiagnosticReport | 10 | Labs/Diagnostics | Standard US Core |
| Condition | 8 | Problems | Standard US Core |
| CarePlan | 7 | Care Plans | Standard US Core |
| Goal | 7 | Care Plans | Standard US Core |
| Organization | 7 | Administrative | Standard US Core |
| Observation | 7 | Vitals/Labs | Standard US Core |
| AllergyIntolerance | 6 | Allergies | Standard US Core |
| CareTeam | 6 | Care Plans | Standard US Core |
| Practitioner | 6 | Administrative | Standard US Core |
| Procedure | 6 | Procedures | Standard US Core |
| Provenance | 4 | Provenance | Standard US Core |

Additionally, **DocumentReference** appears in the FHIR specs page navigation menu but has no content section with field definitions on the collected page (the nav link points to a separate `fhir-2022` page).

**Key observation**: These are strictly standard US Core resources. There are:
- **No custom FHIR profiles** or IMS-specific extensions
- **No vendor-proprietary resource types**
- **No resources for billing, claims, superbills, or payments**
- **No specialty-specific clinical resources** despite IMS supporting 40+ specialties
- **No patient portal, messaging, or telemedicine resources**

### Vendor's own content organization

The vendor organizes content into two formats (C-CDA and FHIR) with no further categorization. The FHIR resources map to standard US Core domains:

| Entity | Fields | Described | Types | Category (vendor's) |
|---|---|---|---|---|
| AllergyIntolerance | 6 | 6 | Yes | FHIR Resource |
| Patient | 13 | 13 | Yes | FHIR Resource |
| Encounter | 10 | 10 | Yes | FHIR Resource |
| Immunization | 11 | 11 | Yes | FHIR Resource |
| Goal | 7 | 7 | Yes | FHIR Resource |
| Condition | 8 | 8 | Yes | FHIR Resource |
| Organization | 7 | 7 | Yes | FHIR Resource |
| MedicationRequest | 12 | 12 | Yes | FHIR Resource |
| Provenance | 4 | 4 | Yes | FHIR Resource |
| Procedure | 6 | 6 | Yes | FHIR Resource |
| Device | 11 | 11 | Yes | FHIR Resource |
| Practitioner | 6 | 6 | Yes | FHIR Resource |
| CarePlan | 7 | 7 | Yes | FHIR Resource |
| CareTeam | 6 | 6 | Yes | FHIR Resource |
| Observation | 7 | 7 | Yes | FHIR Resource |
| DiagnosticReport | 10 | 10 | Yes | FHIR Resource |
| DocumentReference | 0 | 0 | N/A | FHIR Resource (nav only) |

Full inventory: `analysis/entity-inventory-full.json`

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's EHI export documentation describes two standard clinical exchange formats:

1. **C-CDA XML**: 19 standard C-CDA sections covering USCDI v1 clinical summary data classes. No field-level detail, no sample documents, no information about what IMS data populates each section. This is a standard clinical summary document format.

2. **FHIR R4 API**: 16 US Core resource types with 131 fields. This is explicitly their g(10) Standardized API documentation. The vendor's own EHI export page states: *"For detailed specifications, please refer to 170.315(g)(10) for the Standardized API for patient and population services."*

Both formats cover the same USCDI-scope clinical domains: demographics, allergies, conditions, medications, immunizations, labs, vitals, procedures, encounters, care plans, goals, provenance, and basic payer information (C-CDA only). Neither format extends beyond standard USCDI clinical data classes.

The documentation is thinnest in:
- **C-CDA**: No field-level detail at all — just 19 section names
- **Billing/specialty data**: Completely absent from both formats
- **DocumentReference**: Listed in navigation but no field documentation

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | FHIR `Patient` (13 fields), C-CDA header | Standard US Core demographics only; IMS likely stores more (custom intake fields, specialty demographics) |
| Encounters / visits | ✅ Covered | FHIR `Encounter` (10 fields), C-CDA "Encounters" | Standard encounter data; no visit-specific workflow data |
| Problems / conditions | ✅ Covered | FHIR `Condition` (8 fields), C-CDA "Problems" | Standard; IMS likely has richer problem tracking internally |
| Medications / prescriptions | ✅ Covered | FHIR `MedicationRequest` (12 fields), C-CDA "Medications" | Basic prescription data; no EPCS details, no prior auth status, no drug interaction history |
| Allergies | ✅ Covered | FHIR `AllergyIntolerance` (6 fields), C-CDA "Medication Allergies" | Standard |
| Immunizations | ✅ Covered | FHIR `Immunization` (11 fields), C-CDA "Immunization" | Standard |
| Vitals | ✅ Covered | FHIR `Observation` (7 fields), C-CDA "Vital Signs" | Standard vital signs |
| Lab results | ✅ Covered | FHIR `DiagnosticReport` (10 fields), `Observation` (7 fields), C-CDA "Laboratory Values/Results" | Standard; IMS integrates with 90+ labs — likely stores richer result data internally |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR `DiagnosticReport` covers basic reports; no imaging-specific resources | Product stores diagnostic data but imaging details unclear |
| Procedures | ✅ Covered | FHIR `Procedure` (6 fields), C-CDA "Procedures" | Standard |
| Clinical notes / documents | ⚠️ Partial | C-CDA "Clinical Notes", "Assessment"; FHIR `DocumentReference` in nav but no field docs | IMS has extensive specialty-specific templates for 40+ specialties; only generic notes covered |
| Care plans / goals | ✅ Covered | FHIR `CarePlan` (7 fields), `Goal` (7 fields), `CareTeam` (6 fields), C-CDA "Plan of Treatment", "Goals" | Standard |
| Orders / referrals | ⚠️ Partial | C-CDA "Reason for Referral"; no FHIR ServiceRequest | IMS has full referral tracking and authorization management; only "reason" captured |
| Insurance / coverage | ⚠️ Partial | C-CDA "Payer" section (no field detail); no FHIR Coverage resource | IMS stores detailed insurance data; only basic payer info in C-CDA |
| Claims / billing | ❌ Not covered | No billing entities in either format | **Major gap**: IMS has integrated billing/RCM with claims, superbills, denial management, payment posting. None exported. |
| Payments | ❌ Not covered | No payment entities | **Major gap**: IMS processes payments via multiple integrations (Global Payments, Exact Payments, BillFlash). None exported. |
| Consents / directives | ❌ Not covered | No consent resources | IMS likely stores consent forms; not in export |
| Patient communications / portal messages | ❌ Not covered | No messaging resources | **Significant gap**: IMS has patient portal (IMS Care) with secure messaging, refill requests, document uploads; InTouch SMS/email; Televisit. None exported. |
| Specialty-specific data | ❌ Not covered | No specialty resources | **Major gap**: IMS's primary differentiator is 40+ specialty modules (CosmetiSuite, FertilityEHR, dental, mental health, oncology, etc.) with dedicated clinical templates. None of this specialty data appears in the export. |

## 6. Documentation Quality

**Overall: Poor.**

- **Data dictionary**: None. The vendor provides no product-specific data dictionary mapping IMS's internal data model to the export. The FHIR specifications page is standard US Core API documentation, not an IMS-specific export dictionary.
- **Field descriptions**: The 131 FHIR fields all have descriptions (100%), but these are generic FHIR US Core descriptions, not IMS-specific mappings.
- **Value sets**: Not documented. Standard code systems (SNOMED, LOINC, RxNorm) are referenced but no IMS-specific value sets or coded values are enumerated.
- **Relationships**: Basic FHIR references only (e.g., `patient` reference on clinical resources).
- **Sample data**: None provided.
- **Machine-readable schemas**: None. No XSD, JSON Schema, OpenAPI spec, or downloadable files of any kind.
- **User guide**: None. No instructions for how to actually initiate or receive an EHI export.
- **C-CDA documentation**: Extremely thin — only 19 section names with no field-level detail.

A developer trying to build an import from an IMS EHI export would have no product-specific documentation to work with. They would only have generic C-CDA and US Core FHIR specifications, with no understanding of how IMS maps its internal data or what IMS-specific data might appear.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export documentation describes only standard USCDI-scope clinical data via C-CDA and FHIR US Core — the regulatory floor for clinical exchange, not a designated record set. IMS is a comprehensive all-in-one system with integrated billing/RCM, 40+ specialty modules, patient portal/telemedicine, and practice management, all in a single database. The export covers none of the billing data, none of the specialty-specific clinical data, none of the patient portal/messaging data, and none of the practice management data. This is a large product with a tiny export footprint.

**Axis 2 — Export approach: Repackaged existing export**

The vendor explicitly confirms this classification on their own EHI export page: *"For detailed specifications, please refer to 170.315(g)(10) for the Standardized API for patient and population services."* The FHIR export IS their g(10) API. The C-CDA export is their standard clinical summary document. There is no evidence of any purpose-built (b)(10) export effort — no native database dump, no IMS-specific data dictionary, no coverage of data domains beyond what C-CDA and US Core already handle. The 16 FHIR resource types and 19 C-CDA sections are exactly what you'd expect from a standard g(10) + C-CDA clinical exchange implementation.

### Key Findings

1. **Vendor explicitly equates b(10) with g(10)**: The EHI export page directly states to "refer to 170.315(g)(10)" for FHIR specifications, confirming the vendor has not built a separate b(10) export — they're presenting their existing FHIR API as the EHI export.

2. **Entire billing/RCM domain missing**: IMS has deep integrated billing (claims, superbills, denial management, payment processing) that users call "a biller's dream." Zero billing data appears in the export — no claims, no charges, no payments, no superbills.

3. **40+ specialty modules completely absent**: IMS's primary market differentiator is specialty-specific clinical modules (CosmetiSuite, FertilityEHR, dental, mental health, oncology, etc.). None of this specialty-specific data is documented in the export. Only generic US Core clinical resources are provided.

4. **No product-specific documentation**: There is no IMS data dictionary, no mapping from IMS internal tables to export fields, and no documentation of IMS-specific data elements. The FHIR documentation is standard US Core API specs that could describe any certified EHR.

5. **Patient engagement data absent**: IMS has a patient portal (IMS Care), telemedicine (Televisit), SMS/email messaging (InTouch), and secure messaging. None of this data appears in the export.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   C-CDA XML + FHIR R4 (US Core STU 3.1.1)
Entities:        16 FHIR resources (+ 19 C-CDA sections by name only)
Fields:          131 (FHIR only; C-CDA has no field documentation)
Descriptions:    100% of FHIR fields (but all generic US Core, not IMS-specific)
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data STU 1.0.1 referenced)
Domains covered: 9 of 18 applicable domains (all USCDI-scope only)
```

### Bottom Line

A patient or provider requesting their EHI from IMS would receive a standard clinical summary — the same data available through any USCDI-compliant clinical exchange. They would not receive their billing records, specialty-specific clinical assessments, patient portal messages, telemedicine records, or any of the rich data that makes IMS a "complete EHR." The vendor has not engaged with (b)(10) requirements in any meaningful way — they have simply relabeled their existing g(10) FHIR API and C-CDA export as their EHI export solution.
