# EHI Export Analysis: Sevocity (Conceptual MindWorks, Inc.)

**Product**: Sevocity v13.0
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2324.Sevo.13.01.1.221230 (CHPL #11187)

## 1. Product Context

Sevocity is a cloud-based ambulatory EHR developed by Conceptual MindWorks, Inc. (CMI), a small company (~18 employees, ~$2.9M revenue) based in San Antonio, TX. It targets solo and small-to-mid-size outpatient practices across 40+ states and supports 40+ medical specialties with customizable encounter templates.

**Core capabilities relevant to EHI completeness:**
- **Clinical documentation**: Customizable encounter templates, physical exam documentation, clinical notes, flow sheets, ICD-10/CPT coding
- **E-Prescribing**: Embedded e-prescribing including EPCS for controlled substances
- **Orders/Labs**: Lab ordering (Quest bidirectional interface), diagnostic test ordering, results management
- **Referral management**: Provider referrals with Direct protocol support
- **Patient portal**: Real-time patient-physician communication
- **Immunizations**: Tracking with barcode scanner support, state registry reporting
- **Document management**: Scanned documents, faxes, up to 4MB per file
- **Practice management/scheduling**: Appointment calendars, demographics management
- **Billing/Claims** (Sevocity Premier tier): Integrated clearinghouse, claims submission, ERAs, eligibility verification; non-Premier users integrate with third-party PM/billing systems via HL7
- **Clinical decision support**: Alerts, standardized protocols
- **Clinical assessments**: 24+ structured screening tools (PHQ-9, GAD-7, AUDIT-C, Zung Depression Scale, Morse Fall Scale, HARK, food insecurity, etc.)

This establishes the baseline: the export should cover demographics, encounters, problems, medications, allergies, immunizations, vitals, labs, procedures, clinical notes, documents, referrals, insurance/coverage, care plans, and clinical assessments. For Sevocity Premier users, billing/claims data should also be present.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-technical-documentation.html` (44 KB) | Main EHI export page describing the encrypted RAR file structure, folder layout, and FHIR NDJSON resources. Single HTML page from `sevocity.com`. | **High** — primary source for export mechanics |
| `downloads/openAPIDocs.yml` (9.3 KB) | OpenAPI 3.0.1 root specification listing 25 FHIR resource types with server URLs, tags, and $ref links | **High** — definitive resource list |
| `downloads/fhir-api-docs/components/schemas/*.yml` (52 files) | Individual OpenAPI schema definitions for READ and SEARCH variants of each FHIR resource | **High** — field-level data dictionary |
| `downloads/fhir-api-docs/examples/*.yml` (26 files) | Example FHIR resource instances with realistic test data | **High** — demonstrates actual field population |
| `downloads/fhir-api-docs/paths/*.yml` (52 files) | API path definitions with search parameters and response schemas | **Medium** — search parameter documentation |
| `downloads/fhir-api-docs/components/parameters/*.yml` (2 files) | Parameter definitions (IdParam, PatientParam) | **Low** — minimal content |
| `downloads/enrichment/sevocity-fhir-api-extracted.json` (115 KB) | Pre-extracted JSON parse of all OpenAPI schemas with recursive field counts | **High** — machine-readable inventory |
| `downloads/screenshot-ehi-export-page.png` | Screenshot of the EHI export documentation page | **Low** — confirms visual layout |
| `downloads/screenshot-fhir-api-docs.png` | Screenshot of the Swagger UI FHIR API docs | **Low** — confirms Swagger UI presentation |

**Total files examined**: 136 (1 HTML page, 1 root OpenAPI spec, 52 schema files, 52 path files, 26 example files, 2 parameter files, 1 enrichment JSON, 2 screenshots).

## 3. Export Mechanics

- **Format**: Encrypted RAR archive containing:
  1. FHIR R4 NDJSON files in `/{Customer ID}/Resources/`
  2. Document/image files (PDF, JPEG, PNG) in `/{Customer ID}/DocumentData/{Patient ID}/`
  3. CSV demographics file at `/{Customer ID}/PatientsDemographics.csv`
  4. README.txt pointing to the documentation URL
- **Mechanism**: Not explicitly documented. No user-facing instructions for triggering the export are provided on the documentation page. The FHIR API documentation includes a `Group/{id}/$export` endpoint (FHIR Bulk Data Export), suggesting programmatic bulk export capability.
- **Single-patient vs bulk**: The `Group/$export` endpoint and the folder structure (`/{Customer ID}/...`) indicate bulk/multi-patient export at the customer (practice) level. Individual patient export is not separately documented.
- **Access constraints**: The RAR file is encrypted. No details on key distribution, encryption algorithm, or file size limits are documented.
- **Fees**: Not documented.

## 4. Export Content: What's In It

### Overview

The export contains **25 FHIR R4 resource types** documented via OpenAPI 3.0.1 schemas with a total of **597 fields** across all resources (counting all nested levels). Of these, 20 are certified under (g)(10) and 5 are non-certified additions (Appointment, MedicationStatement, QuestionnaireResponse, RelatedPerson, ServiceRequest).

The schemas conform to **US Core STU6.1.0** profiles. No vendor-proprietary extensions beyond standard US Core extensions were observed.

**Documentation quality**: The OpenAPI schemas provide **type information only** (string, boolean, object, array) with no field-level descriptions, no value set bindings, and no documentation of allowed values. **0 of 597 fields have descriptions**. However, the 22 example files (out of 25 resource types) provide realistic sample data that demonstrates actual field usage with standard code systems (ICD-10-CM, SNOMED CT, LOINC, CPT, RxNorm, HL7 terminology).

Additionally, the export includes:
- **Document files** (PDFs, JPEGs, PNGs) organized per patient in `DocumentData/{Patient ID}/` with subfolders for "admissions", "finalizedencounters", "referrals", etc.
- A **`summary.pdf`** chart summary per patient
- A **`PatientsDemographics.csv`** file (schema undocumented — no column headers or data types specified)

### Vendor's own content organization

The vendor organizes resources by FHIR resource type. The table below uses the enrichment extraction's field counts (all nesting levels):

| Resource Type | Fields | (g)(10) | Category |
|---|---|---|---|
| Patient | 64 | Yes | Demographics |
| Encounter | 45 | Yes | Encounters / Visits |
| DocumentReference | 37 | Yes | Clinical Notes / Documents |
| MedicationRequest | 36 | Yes | Medications |
| MedicationDispense | 33 | Yes | Medications |
| QuestionnaireResponse | 33 | No | Clinical Assessments |
| Condition | 29 | Yes | Problems / Conditions |
| AllergyIntolerance | 28 | Yes | Allergies |
| ServiceRequest | 26 | No | Orders / Referrals |
| Observation | 25 | Yes | Vitals / Labs / Social History |
| RelatedPerson | 24 | No | Demographics |
| DiagnosticReport | 21 | Yes | Lab / Diagnostic Reports |
| Organization | 20 | Yes | Administrative |
| Practitioner | 18 | Yes | Administrative |
| Device | 17 | Yes | Devices |
| Immunization | 17 | Yes | Immunizations |
| Provenance | 16 | Yes | Provenance |
| MedicationStatement | 16 | No | Medications |
| CarePlan | 15 | Yes | Care Plans / Goals |
| Location | 15 | Yes | Administrative |
| Appointment | 14 | No | Encounters / Visits |
| CareTeam | 14 | Yes | Care Plans / Goals |
| Procedure | 14 | Yes | Procedures |
| Goal | 13 | Yes | Care Plans / Goals |
| Medication | 7 | Yes | Medications |

**Category summary:**

| Category | Resources | Total Fields |
|---|---|---|
| Demographics | 2 (Patient, RelatedPerson) | 88 |
| Medications | 4 (MedicationRequest, MedicationDispense, MedicationStatement, Medication) | 92 |
| Encounters / Visits | 2 (Encounter, Appointment) | 59 |
| Administrative | 3 (Organization, Practitioner, Location) | 53 |
| Care Plans / Goals | 3 (CarePlan, CareTeam, Goal) | 42 |
| Clinical Notes / Documents | 1 (DocumentReference) | 37 |
| Clinical Assessments | 1 (QuestionnaireResponse) | 33 |
| Problems / Conditions | 1 (Condition) | 29 |
| Allergies | 1 (AllergyIntolerance) | 28 |
| Orders / Referrals | 1 (ServiceRequest) | 26 |
| Vitals / Labs / Social History | 1 (Observation) | 25 |
| Lab / Diagnostic Reports | 1 (DiagnosticReport) | 21 |
| Devices | 1 (Device) | 17 |
| Immunizations | 1 (Immunization) | 17 |
| Provenance | 1 (Provenance) | 16 |

### Non-FHIR components

Beyond the FHIR NDJSON resources, the export includes:

1. **DocumentData folder**: Per-patient folders containing raw document files (PDFs, images) organized into subfolders:
   - `summary.pdf` — patient chart summary
   - `admissions/` — admission documents
   - `finalizedencounters/` — finalized encounter documents
   - `referrals/` — referral documents
   - Other document type subfolders

2. **PatientsDemographics.csv**: Maps patients to internal Patient IDs. Column structure is **not documented** — no schema, no column headers, no sample data provided.

3. **DocumentReference linkage**: Resources with `type.coding.code` of "11503-0" (LOINC: Medical records) have `content.attachment.url` pointing to physical files in the DocumentData folder via relative paths. This links structured FHIR metadata to unstructured document content.

### Notable details from examples

- **Patient** example includes US Core extensions for race (with detailed subcategory), ethnicity, birth sex, sex, gender identity, and tribal affiliation (3 tribes). Contacts with full address/phone/email.
- **QuestionnaireResponse** example shows a Zung Self-Rating Depression Scale with 20 individually scored items — genuine structured clinical assessment data.
- **Questionnaire** example bundle contains **24 distinct screening tools**: PHQ-2, PHQ-9, GAD-7, AUDIT-C, AD8 (dementia), Morse Fall Scale, HARK (domestic violence), food insecurity screens, social isolation survey, ASCVD risk score, mammography tracking, tobacco cessation, adolescent/adult depression screens, functional assessment (FACT-G, 53 items), and disability screening (ACS, 9 items).
- **ServiceRequest** example shows lab orders with CPT codes and ICD-10-CM reason codes, linked to encounters.
- **Coverage** example shows Medicare coverage with member numbers, plan groups, payer references, and coverage periods.
- **Observation** example demonstrates SDOH (Social Determinants of Health) screening with LOINC codes and answer codes.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Sevocity's export is a **FHIR R4 projection** enhanced with raw document files. The vendor goes meaningfully beyond the standard (g)(10) USCDI data set by including:

1. **5 non-certified resources**: Appointment, MedicationStatement, QuestionnaireResponse, RelatedPerson, and ServiceRequest add scheduling, medication history, clinical assessments, emergency contacts, and lab/diagnostic orders.

2. **24 structured clinical assessments** via QuestionnaireResponse — this is genuinely impressive for a small vendor. It exports structured, scored responses from PHQ-9, GAD-7, AUDIT-C, fall risk, domestic violence screens, SDOH assessments, and specialty-specific instruments. Most FHIR-only exports miss this entirely.

3. **Raw document export** via the DocumentData folder — finalized encounter notes, admission documents, referrals, and chart summaries as PDFs/images. This captures unstructured clinical content that FHIR resources can't fully represent.

4. **Coverage resource** — insurance enrollment data beyond what's required by (g)(10) alone.

The richest categories are Medications (92 fields across 4 resources) and Demographics (88 fields across 2 resources). The thinnest are Medication (7 fields — just code, form, and ID), Goal (13 fields), and Procedure (14 fields).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (64 fields with US Core extensions), RelatedPerson (24 fields), PatientsDemographics.csv | Thorough — race, ethnicity, gender identity, tribal affiliation, contacts |
| Encounters / visits | ✅ Covered | Encounter (45 fields), Appointment (14 fields) | Good — includes diagnoses, participants, locations, service providers |
| Problems / conditions | ✅ Covered | Condition (29 fields) with ICD-10-CM coding | Solid — clinical/verification status, onset, categories |
| Medications / prescriptions | ✅ Covered | MedicationRequest (36 fields), MedicationStatement (16 fields), MedicationDispense (33 fields), Medication (7 fields) | Strong — prescriptions, history, dispensing all covered |
| Allergies | ✅ Covered | AllergyIntolerance (28 fields) | Good — reactions, severity, categories |
| Immunizations | ✅ Covered | Immunization (17 fields) | Adequate |
| Vitals | ✅ Covered | Observation (25 fields) covers vitals via LOINC codes | Adequate — uses standard Observation resource |
| Lab results | ✅ Covered | Observation (25 fields), DiagnosticReport (21 fields) | Good — standard FHIR lab result representation |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport covers some; no dedicated imaging resource | Product does diagnostic ordering; results may be in DocumentData as scanned reports |
| Procedures | ✅ Covered | Procedure (14 fields) | Adequate |
| Clinical notes / documents | ✅ Covered | DocumentReference (37 fields) + DocumentData folder with PDFs/images organized by type (encounters, admissions, referrals) + summary.pdf | Strong — hybrid approach captures both structured metadata and raw documents |
| Care plans / goals | ✅ Covered | CarePlan (15 fields), Goal (13 fields), CareTeam (14 fields) | Adequate |
| Orders / referrals | ✅ Covered | ServiceRequest (26 fields) with CPT/HCPCS/SNOMED codes and ICD-10-CM reason codes | Good — non-certified addition that adds real value |
| Insurance / coverage | ✅ Covered | Coverage resource with member numbers, payer references, plan groups, periods | Good for enrollment data |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, ChargeItem, or billing-specific resources | **Significant gap for Sevocity Premier users** who have integrated billing. Non-Premier users' billing is in third-party systems, so N/A for them. |
| Payments | ❌ Not covered | No payment resources | Gap for Premier users; N/A for non-Premier |
| Consents / directives | ❌ Not covered | No Consent resource | Product likely stores consent data; minor gap |
| Patient communications / portal | ❌ Not covered | No Communication resource or portal message export | Product has active patient portal; moderate gap |
| Specialty-specific assessments | ✅ Covered | QuestionnaireResponse (33 fields) with 24 distinct screening tools | Impressive — PHQ-9, GAD-7, AUDIT-C, fall risk, SDOH, etc. |

## 6. Documentation Quality

**Strengths:**
- OpenAPI 3.0.1 specification is well-structured and machine-readable — 52 schema files, 52 path files covering all 25 resource types
- 22 of 25 resource types have example instances with realistic test data using standard code systems
- The main EHI export page clearly explains the RAR file structure and the DocumentReference-to-DocumentData linkage
- US Core STU6.1.0 conformance provides an implicit schema reference
- Swagger UI at `fhirapi-docs.sevocity.com` provides interactive browsing

**Weaknesses:**
- **No field-level descriptions**: 0 of 597 fields have descriptions in the OpenAPI schemas — fields are typed but not explained
- **No value set bindings**: Coded fields like `status`, `category`, and `type` are typed as `string` with no enumeration of allowed values
- **PatientsDemographics.csv is undocumented**: No column headers, types, or sample rows
- **No export trigger documentation**: No instructions on how to initiate an export, who can request it, turnaround time, or access controls
- **No NDJSON file naming conventions**: Unclear how many .ndjson files exist or how they're organized in the Resources folder
- **No encryption details**: RAR encryption algorithm and key management undocumented
- **No data volume guidance**: No information on export size limits or handling of large practices

**Could a developer build an import?** Partially. A developer familiar with FHIR R4 and US Core profiles could infer most semantics from the resource types and example data. However, they would need external knowledge of FHIR to fill the gaps left by missing descriptions and value set bindings. The PatientsDemographics.csv would require guesswork without column documentation. The DocumentData folder structure relies on convention ("finalizedencounters", "referrals") without formal specification.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is a FHIR R4 projection of the vendor's native data model, enhanced with raw document files and a CSV demographics file. It is not the vendor's native database schema. While the FHIR resource coverage goes meaningfully beyond the basic (g)(10) USCDI requirements (adding Appointment, MedicationStatement, QuestionnaireResponse, RelatedPerson, ServiceRequest, and the DocumentData folder), it remains a standardized projection that likely omits vendor-specific internal data structures, custom fields, and — critically — all billing/claims data for Premier users.

### Key Findings

1. **Genuinely enhanced FHIR export, not just (g)(10) repackaging.** Sevocity added 5 non-certified resource types (Appointment, MedicationStatement, QuestionnaireResponse, RelatedPerson, ServiceRequest) and a raw document export folder. The QuestionnaireResponse resource with 24 clinical assessment instruments (PHQ-9, GAD-7, AUDIT-C, fall risk, SDOH screens, etc.) is an unusually strong feature for a vendor of this size.

2. **No billing/claims export despite offering integrated billing.** Sevocity Premier includes a full clearinghouse, claims submission, ERAs, and eligibility verification. None of this data appears in the export — no Claim, ExplanationOfBenefit, or ChargeItem resources. This is a genuine EHI gap for Premier users.

3. **Documentation has correct structure but lacks depth.** The OpenAPI schema files provide type information for 597 fields across 25 resources, but 0 fields have descriptions. No value set bindings, no relationship documentation beyond FHIR references. The PatientsDemographics.csv is entirely undocumented.

4. **Document export is a genuine strength.** The `DocumentData/` folder with per-patient PDFs, images, and chart summaries — organized by document type and linked to FHIR DocumentReference resources — captures unstructured clinical content that pure FHIR exports miss.

5. **Patient portal messages are absent.** The product has an active patient portal for physician-patient communication, but no Communication or messaging resources are exported.

### Summary Stats

```
Classification:  Standard-based projection (enhanced FHIR R4 + documents)
Export format:   FHIR R4 NDJSON + raw documents (PDF/JPEG/PNG) + CSV, in encrypted RAR
Model type:      Standard projection (FHIR R4 / US Core STU6.1.0)
Entities:        25 FHIR resource types + DocumentData files + PatientsDemographics.csv
Fields:          597 (across all FHIR resource schemas, all nesting levels)
Descriptions:    0% (type information only, no field descriptions)
Sample data:     Yes (22 of 25 resources have example instances)
Bulk export:     Yes (Group/$export endpoint documented)
Domains covered: 13 of 17 applicable domains
```

### Bottom Line

Sevocity delivers a FHIR R4 export that goes meaningfully beyond the minimum (g)(10) requirements, with particular strength in clinical assessments (24 screening instruments via QuestionnaireResponse) and unstructured document export (the DocumentData folder). However, the complete absence of billing/claims data for Sevocity Premier users — who have integrated billing within the same product — is a significant gap. The export covers clinical data well but is not a complete representation of "all electronic health information" the product stores.
