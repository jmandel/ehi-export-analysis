# EHI Export Analysis: MD Synergy Solutions, LLC

**Product**: Althea Smart EHR, Version 3.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1821.Alth.03.02.1.221205 (CHPL #11046)

## 1. Product Context

MD Synergy Solutions, LLC is a small (~50–70 employees) health IT company based in Calabasas, California. Their integrated platform consists of **Althea Smart EHR** (clinical documentation) and **mds:practice** (practice management/billing). The platform targets independent ambulatory practices across multiple specialties including internal medicine, family medicine, pediatrics, dermatology, psychiatry, pain management, surgery, orthopedics, and podiatry.

**Key data domains the product stores:**

- **Clinical**: Patient demographics, encounter notes (with AI ambient transcription), problem lists, medication lists, allergy lists, vital signs, lab orders/results (Quest, Labcorp integrations), radiology orders/results, immunizations, e-prescribing (Surescripts/NewCrop), implantable devices, clinical decision support interventions, social/psychological/behavioral data (SDOH), and procedures.
- **Financial/Billing** (via mds:practice): Claims generation, electronic claim submission (Change Healthcare, Waystar, etc.), ERA/remittance posting, patient statements, insurance eligibility, denial tracking, payment processing.
- **Patient engagement**: Patient portal (Althea Health) with messaging, online forms/consent, Apple Health data sharing, appointment scheduling, telemedicine video visits, patient satisfaction surveys.
- **Communication**: SMS messaging (Twilio), cloud fax, internal chat, Direct messaging for care coordination.

This product has broad certified criteria including (b)(10) EHI export, (g)(10) FHIR APIs, e-prescribing criteria (a)(1)–(a)(5), and transitions of care (b)(1)–(b)(3). The certification scope indicates a full-stack ambulatory EHR.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `AltheaEHIDocumentation.pdf` (410 KB, 108 pages) | Primary EHI export documentation. Generated from Google Docs (Skia/PDF m120 renderer), uploaded December 2024. Contains introduction, FHIR JSON examples for 16 resource types across 27 sections, CCD export note, contact info, and API terms of use. | **Primary source** — nearly all analysis derives from this artifact |
| `enrichment/fhir-examples.json` (81 KB) | Pre-extracted FHIR JSON examples: 52 resource instances across 13 resource types. | **Highly useful** — machine-readable extraction of the PDF's JSON examples |
| `enrichment/extraction-summary.json` (4 KB) | Extraction accounting: 28 sections found, 52 examples extracted, 5 parse failures. | Useful for understanding extraction completeness |
| `enrichment/extract-fhir-examples.ts` (10 KB) | Bun TypeScript extraction script. | Reference for methodology |
| `enrichment/README.md` (2 KB) | Enrichment documentation. | Minimal value |

**Most informative**: The PDF itself is the sole documentation artifact. There is no data dictionary, no schema, no sample export files, and no separate documentation website. Everything is in this single 108-page PDF.

## 3. Export Mechanics

- **Format**: FHIR R4 JSON (primary) and C-CDA/CCD (secondary)
- **Mechanism**: User-initiated request through the EHR UI. After requesting an export, the system processes it and sends a download link via message. The FHIR export URL pattern is `https://data.mdsynergy.com/FHIRBulkExport/{orgId}/{uuid}.zip`; the CCD export URL pattern is `https://mdsdata.mdsynergy.com/FHIRBulkExport/{orgId}/{uuid}-CCD.zip`.
- **Scope**: Single patient, multiple patients, or entire patient population. The documentation states: "User has the ability to choose single, multiple or all patients."
- **Delivery**: ZIP file containing individual JSON files per resource type (FHIR) or CCD documents (C-CDA).
- **Access constraints**: The Contact Information section says "If you need any further assistance on integrating the FHIR API please email us at altheasupport@mdsynergy.com." The Terms and Conditions section (pages 103–108) contains standard API Terms of Use. No mention of fees for the export.
- **Relationship to (g)(10)**: The export URL path literally contains "FHIRBulkExport," and the contact information references "integrating the FHIR API." This strongly suggests the (b)(10) EHI export is built on top of the (g)(10) FHIR Bulk Data mechanism, with the addition of financial FHIR resources (Claim, Coverage, ExplanationOfBenefit) beyond the standard US Core scope.

## 4. Export Content: What's In It

### Overview

The export documentation consists entirely of **FHIR JSON examples** — one or more complete resource instances per resource type — with no data dictionary, no field-level definitions, no schema, and minimal narrative. Each section has a heading, a one-line link to the relevant US Core FHIR profile, and the JSON example(s).

From the 108-page PDF:
- **28 resource-related sections** in the table of contents (pages 5–101)
- **16 unique FHIR resource types** documented
- **52 extractable JSON examples** (13 resource types successfully parsed; 3 types have examples that couldn't be cleanly extracted due to line-break-split strings and base64 data)
- **522 unique field paths** across the successfully parsed examples
- **0 fields with descriptions** — no field-level documentation exists; the documentation relies entirely on US Core/FHIR specifications for field definitions
- **2 empty/cross-reference sections**: Body Temperature (empty section header, no example) and Body Weight (says "See example listed in Pediatric Weight")

### Vendor's own content organization

The vendor organizes the documentation into named sections in the PDF table of contents. The following table shows each section and its FHIR resource mapping:

| Section Name (vendor's) | FHIR Resource Type | Examples | Field Paths | Category |
|---|---|---|---|---|
| Patient | Patient | 1 | 58 | Demographics |
| Allergies and Intolerances | AllergyIntolerance | 1 | 42 | Clinical |
| Care Plan | CarePlan | 1 | 31 | Clinical |
| Care Team | CareTeam | 1 | 18 | Clinical |
| Condition | Condition | 5 | 32 | Clinical |
| Health Concern | Condition | 1 | (shared) | Clinical |
| Implantable Device | Device | 1 | ~25* | Clinical |
| Diagnostic Report | DiagnosticReport | 1 | ~28* | Clinical |
| Document Reference | DocumentReference | 4 | ~30* | Clinical |
| Goal | Goal | 2 | 24 | Clinical |
| Immunization | Immunization | 4 | 33 | Clinical |
| Medication Request | MedicationRequest | 1 | 42 | Clinical |
| Smoking Status Observation | Observation | 8 | 56 (shared) | Clinical |
| Pediatric Weight/Height Observation | Observation | 14 | (shared) | Clinical |
| Laboratory Result Observation | Observation | 1 | (shared) | Clinical |
| Pediatric BMI for Age Observation | Observation | 1 | (shared) | Clinical |
| Pulse Oximetry Tests | Observation | 1 | (shared) | Clinical |
| Pediatric Head Circumference | Observation | 1 | (shared) | Clinical |
| Observation Body Height | Observation | 1 | (shared) | Clinical |
| Observation Body Temperature | Observation | 0 | 0 | Clinical |
| Observation Blood Pressure | Observation | 1 | (shared) | Clinical |
| Observation Body Weight | Observation | 0 | 0 | Clinical |
| Observation Heart Rate | Observation | 1 | (shared) | Clinical |
| Observation Respiratory Rate | Observation | 1 | (shared) | Clinical |
| Procedure | Procedure | 2 | 35 | Clinical |
| Claims | Claim | 1 | 73 | Financial |
| Coverage | Coverage | 1 | 12 | Financial |
| Explanation of Benefits | ExplanationOfBenefit | 1 | 66 | Financial |

\* Estimated from manual inspection of PDF text; JSON extraction failed due to line-break-split UDI strings (Device) or truncated base64 data (DocumentReference).

**Category breakdown (from successfully parsed data):**

| Category | Resource Types | Total Field Paths | Examples |
|---|---|---|---|
| Demographics | 1 (Patient) | 58 | 1 |
| Clinical | 10+ types (Observation subtypes share one type) | ~397 | 47 |
| Financial | 3 (Claim, Coverage, ExplanationOfBenefit) | 151 | 3 |

### Notable content details

**Financial resources are genuinely present.** The Claim example (pages 91–97) is detailed: it includes professional claim type, billable period, diagnosis codes (ICD-10), procedure codes (CPT), line items with unit pricing ($150.00, $225.00), care team roles (primary, supervisor), and insurer references. The Coverage resource includes subscriber ID and payor references. The ExplanationOfBenefit resource includes adjudication outcomes with payment amounts, patient responsibility, and benefit categories. This is meaningfully beyond a US Core clinical summary.

**DocumentReference embeds clinical notes as base64 PDFs.** The Document Reference section (pages 28–39, the longest section) includes 4 examples of embedded clinical documents: after-visit summaries, echocardiogram reports, and progress notes. These are full PDFs encoded as base64 in the `content.attachment.data` field, which explains why this section spans 12 pages.

**Observation subtypes are extensively documented.** 13 of the 27 sections are Observation variants covering vitals (height, weight, BMI, BP, heart rate, respiratory rate, temperature, pulse oximetry, head circumference), lab results, smoking status, and pediatric growth percentiles.

**No Encounter resource.** Despite encounters being referenced in DiagnosticReport, DocumentReference, MedicationRequest, and other resources (e.g., `"encounter": {"reference": "https://altheafhir.mdsynergy.com/Encounter/445673"}`), there is no Encounter section in the documentation and no Encounter resource example.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export, as documented, covers three broad areas:

1. **Standard US Core clinical data** (the bulk of the documentation): Patient demographics, allergies, care plans, care teams, conditions/problem lists, health concerns, implantable devices, diagnostic reports, clinical document references, goals, immunizations, medication requests, a full suite of vital sign observations, lab results, smoking status, and procedures. This is essentially the USCDI v1/v2 data set mapped to US Core FHIR profiles. The clinical sections are reasonably thorough — for example, the Condition section shows 5 distinct conditions (hypertension, hypothyroidism, etc.) with SNOMED coding, clinical status, verification status, and onset dates.

2. **Financial/billing data** (3 resource types, ~151 field paths): Claim, Coverage, and ExplanationOfBenefit. This is a genuine effort to go beyond clinical summaries into the billing domain. The Claim resource is the richest single resource type in the documentation (73 field paths), with line-item detail including CPT codes, ICD diagnoses, pricing, and care team members. However, this is a FHIR representation of billing data, not a native database dump — the mds:practice system almost certainly stores more granular billing data (denial tracking, ERA details, payment posting, statement generation, eligibility verification records) than what maps to these three FHIR resource types.

3. **Embedded clinical documents** (via DocumentReference): Progress notes, after-visit summaries, and specialty reports are included as base64-encoded PDFs. This is a reasonable approach for unstructured/semi-structured clinical notes, though it means the content of these documents is not machine-readable within the FHIR export itself.

**Thinnest areas**: Coverage has only 12 field paths from one example. CareTeam has only 18 field paths. The Body Temperature and Body Weight sections are effectively empty (header only or cross-reference). The entire clinical section relies on standard FHIR resource structures with no vendor-specific extensions visible.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (58 fields): name, DOB, gender, race, ethnicity, birth sex, address, phone, marital status, employer contact, identifiers | Thorough for standard demographics |
| Encounters / visits | ❌ Not covered | No Encounter resource in export, despite encounters being referenced by DiagnosticReport, DocumentReference, MedicationRequest, etc. | **Significant gap** — product tracks encounters; encounter metadata (dates, types, providers, visit reasons) is core clinical data |
| Problems / conditions / diagnoses | ✅ Covered | `Condition` (32 fields, 6 examples): SNOMED-coded problems, clinical/verification status, onset dates. Includes separate Health Concern section | Adequate |
| Medications / prescriptions | ⚠️ Partial | `MedicationRequest` (42 fields, 1 example): RxNorm-coded prescriptions with dosage, route, provider. No MedicationStatement/MedicationAdministration | Product integrates Surescripts/NewCrop for e-prescribing; fill history, pharmacy details, EPCS data not represented |
| Allergies | ✅ Covered | `AllergyIntolerance` (42 fields, 1 example): drug allergies with reaction details, SNOMED coding, clinical status | Adequate |
| Immunizations | ✅ Covered | `Immunization` (33 fields, 4 examples): CVX-coded vaccines, occurrence dates, status, manufacturer | Adequate |
| Vitals | ✅ Covered | `Observation` subtypes (13 sections): height, weight, BMI, BP, HR, RR, temperature, SpO2, head circumference, pediatric growth percentiles | Thorough — full vital sign coverage |
| Lab results | ✅ Covered | `Observation` Laboratory Result (LOINC-coded) + `DiagnosticReport` for lab/radiology reports | Adequate, though only 1 lab result example shown |
| Imaging / diagnostic reports | ✅ Covered | `DiagnosticReport` (1 example: Chest XR, LOINC-coded, with performer and encounter references) | Present but thin (1 example, parse failure prevents field counting) |
| Procedures | ✅ Covered | `Procedure` (35 fields, 2 examples): SNOMED + CPT dual-coded, with performer and patient references | Adequate |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (4 examples): after-visit summaries, echo reports, progress notes as base64-embedded PDFs | Covered but not machine-readable (embedded PDF blobs) |
| Care plans / goals | ✅ Covered | `CarePlan` (31 fields, 1 example) + `Goal` (24 fields, 2 examples) | Adequate |
| Orders / referrals | ❌ Not covered | No ServiceRequest or similar resource in export | Product likely handles referrals (FindEMR lists it as a feature); gap if so |
| Insurance / coverage | ⚠️ Partial | `Coverage` (12 fields, 1 example): subscriber ID, payor reference, basic coverage info | Present but thin — only 12 field paths from 1 example |
| Claims / billing | ⚠️ Partial | `Claim` (73 fields) + `ExplanationOfBenefit` (66 fields): professional claims with line items, diagnoses, procedures, pricing, adjudication | Meaningfully present via FHIR financial resources, but product's native billing system (mds:practice) stores much more: denial tracking, ERA details, payment posting, patient statements, eligibility verification — none of these have a clear FHIR representation |
| Payments | ⚠️ Partial | Adjudication amounts in `ExplanationOfBenefit` | Only insurer-side; patient payments, credit card transactions, statement balances not represented |
| Consents / directives | ❌ Not covered | No Consent resource in export | Product portal collects consent documents from patients |
| Patient communications / portal messages | ❌ Not covered | No Communication resource in export | Product has patient portal with messaging, SMS (Twilio), and internal chat — none exported |
| Specialty-specific data | ❌ Not covered | No specialty-specific resources or extensions visible | **Significant gap** — product serves dermatology, psychiatry, pain management, orthopedics, podiatry. No specialty-specific clinical data representation beyond what fits in standard FHIR resources. Specialty data may be partially captured in DocumentReference as embedded PDFs, but this is unverifiable from the documentation |

**Covered**: 10 of 19 applicable domains
**Partial**: 4 domains
**Not covered**: 5 domains

## 6. Documentation Quality

**Overall quality: Poor.** The documentation is a 108-page PDF that is approximately 95% FHIR JSON examples with almost no narrative explanation.

**What's present:**
- Complete FHIR JSON examples for each resource type (the examples are well-structured and use real-looking test data)
- One-line links to the relevant US Core profile specifications for each resource type
- A brief introduction defining EHI and stating that CCDA and FHIR formats are supported

**What's missing:**
- **No data dictionary**: Zero field-level definitions, descriptions, or documentation. The documentation relies entirely on the reader knowing the US Core/FHIR specification.
- **No schema**: No JSON Schema, no OpenAPI specification, no FHIR StructureDefinition, no CapabilityStatement.
- **No value set documentation**: Code systems (SNOMED, LOINC, RxNorm, ICD, CPT, CVX) are visible in examples but there is no systematic documentation of which code systems are used, what value sets are supported, or what vendor-specific codes might appear.
- **No relationship documentation**: Cross-resource references are visible in examples (Patient → Encounter → DiagnosticReport chains) but not systematically described.
- **No cardinality or constraint documentation**: No indication of which fields are required vs. optional, what multiplicities are supported, or what business rules apply.
- **No sample export files**: No actual ZIP file or representative export data is provided.
- **No export workflow documentation**: The process of requesting an export is described in 2 sentences. No screenshots, no step-by-step instructions, no admin configuration guidance.
- **No vendor-specific extension documentation**: If the vendor uses any FHIR extensions beyond US Core, they are not documented.
- **No versioning or change history**: The title says "Version 3.0" but there is no revision history.

**Developer usability**: A developer familiar with FHIR and US Core could understand the general shape of the export, but would need to reference external FHIR specifications for all field definitions. Any vendor-specific behaviors (e.g., the smoking status example shows `"display": "LV EDD^^67^^78"` which doesn't match expected SNOMED display values) would be discovered only through trial and error. A developer unfamiliar with FHIR would find this documentation nearly unusable.

**Machine-readable artifacts**: None. The PDF is the only artifact, and it contains no machine-readable schema. The extracted `fhir-examples.json` in the enrichment folder was created by the collection agent, not provided by the vendor.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is a FHIR R4 JSON representation of patient data mapped to US Core profiles, augmented with three FHIR financial resource types (Claim, Coverage, ExplanationOfBenefit). The export mechanism appears to be the (g)(10) FHIR Bulk Data API extended with financial resources. This is not a native database export — it's a projection of the vendor's internal data model into standard FHIR resources. While the inclusion of financial resources shows awareness that EHI extends beyond clinical summaries, the export is fundamentally limited to "what maps to FHIR," which leaves significant gaps in billing detail, specialty clinical data, patient communications, and administrative data.

### Key Findings

1. **Financial resource inclusion is a genuine positive.** The Claim (73 fields), Coverage, and ExplanationOfBenefit (66 fields) resources go beyond what most small EHR vendors provide. The Claim example includes line-item pricing, CPT/ICD codes, and care team roles — real billing data, not a placeholder. (Source: `AltheaEHIDocumentation.pdf`, pages 91–101)

2. **No data dictionary or schema exists.** The entire 108-page PDF is FHIR JSON examples with one-line profile links. Zero fields have descriptions. A recipient of this export would need deep FHIR expertise and access to the US Core specification to interpret the data. (Source: `AltheaEHIDocumentation.pdf`, all pages)

3. **Encounter resource is missing despite being referenced.** Other resources (DiagnosticReport, DocumentReference, MedicationRequest) contain encounter references like `"encounter": {"reference": ".../Encounter/445673"}`, but no Encounter resource is documented or exported. This means encounter metadata (visit dates, types, reasons, locations) is lost. (Source: DiagnosticReport example, page 26)

4. **Specialty clinical data has no representation.** The product serves 10+ medical specialties with specialty-specific workflows, but the export contains only standard FHIR resources with no visible vendor-specific extensions. Dermatology assessments, psychiatric evaluations, pain management protocols, and orthopedic data either get flattened into DocumentReference PDFs or are simply not exported. (Source: product-research.md vs. PDF content)

5. **The export mechanism is the FHIR Bulk Data API repackaged.** URL paths contain "FHIRBulkExport," the contact section references "integrating the FHIR API," and the resource set aligns closely with US Core + financial resources. This is a (g)(10) API with financial resources added, presented as (b)(10) compliance. (Source: `AltheaEHIDocumentation.pdf`, pages 4, 102–103)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 JSON (primary), C-CDA/CCD (secondary)
Model type:      Standard projection (US Core FHIR profiles + financial resources)
Entities:        16 unique FHIR resource types across 28 documentation sections
Fields:          ~522 unique field paths (from parsed examples; no formal schema)
Descriptions:    0% (no field-level descriptions; examples only)
Sample data:     Yes (embedded in documentation as FHIR JSON examples; no standalone sample export)
Bulk export:     Yes (single patient, multiple, or all patients via download link)
Domains covered: 10 of 19 applicable domains fully covered; 4 partial; 5 not covered
```

### Bottom Line

MD Synergy's EHI export is a FHIR Bulk Data projection with the notable addition of Claim, Coverage, and ExplanationOfBenefit resources — better than many small vendors who simply point to their (g)(10) API. However, it remains a standard-based projection, not a comprehensive native export. The biggest gap is the absence of the product's native billing detail (denial tracking, payment posting, patient statements), specialty clinical data, patient portal communications, and encounter records. A patient receiving this export would get a reasonable clinical summary and partial billing picture, but would miss significant portions of their designated record set — particularly anything that doesn't map cleanly to a standard FHIR resource type.
