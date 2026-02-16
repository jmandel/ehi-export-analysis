# EHI Export Analysis: Sevocity (Conceptual MindWorks, Inc.)

**Product**: Sevocity v13.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2324.Sevo.13.01.1.221230 (CHPL ID 11187)

## 1. Product Context

Sevocity is a cloud-based ambulatory EHR developed by Conceptual MindWorks, Inc. (CMI), a small San Antonio-based company (~18 employees, ~$2.9M revenue). It targets solo practitioners and small-to-mid-size outpatient practices across 40+ states and supports 40+ medical specialties with customizable templates.

The product exists in two tiers:
- **Sevocity EHR** — core clinical EHR (charting, e-prescribing, labs, referrals, patient portal, immunizations, clinical decision support)
- **Sevocity Premier** — adds integrated practice management and billing (clearinghouse, claims, ERAs, eligibility verification)

Key data domains the product stores:
- Patient demographics, contacts, insurance information
- Encounter/visit documentation with customizable specialty templates
- Problem lists, medications, allergies, vital signs
- Lab orders and results (Quest integration), diagnostic test orders
- E-prescribing including EPCS
- Immunization records with registry reporting
- Referrals and referral results
- Clinical notes and documents (scanning, e-faxing)
- Patient portal messages
- Scheduling/appointments
- Clinical assessments and screening tools (e.g., depression scales)
- Billing and claims data (Sevocity Premier users)
- C-CDA documents for transitions of care
- FHIR-accessible patient data via (g)(10) API

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-technical-documentation.html` (44 KB) | Main EHI export documentation page from sevocity.com describing RAR file structure, folder layout, and FHIR NDJSON resources | **High** — primary source for export format/mechanics |
| `downloads/openAPIDocs.yml` (9.3 KB) | OpenAPI 3.0.1 root specification for the Sevocity FHIR API listing 28 resource type tags and $ref links | **High** — master index of all FHIR resources |
| `downloads/fhir-api-docs/components/schemas/*.yml` (52 files) | Individual YAML schema definitions for READ and SEARCH responses for each FHIR resource type | **High** — field-level documentation of every resource |
| `downloads/fhir-api-docs/examples/*.yml` (26 files) | Example FHIR resource instances with realistic test data | **High** — demonstrates actual data depth and coding |
| `downloads/fhir-api-docs/paths/*.yml` (52 files) | API endpoint definitions with search parameters | **Medium** — shows API surface area |
| `downloads/fhir-api-docs/components/parameters/*.yml` (2 files) | Shared parameter definitions (IdParam, PatientParam) | **Low** — standard boilerplate |
| `downloads/screenshot-ehi-export-page.png` (290 KB) | Screenshot of the main EHI export documentation page | **Low** — visual confirmation of HTML content |
| `downloads/screenshot-fhir-api-docs.png` (907 KB) | Screenshot of the Swagger UI FHIR API docs | **Low** — visual confirmation |
| `downloads/enrichment/sevocity-fhir-api-extracted.json` | Prior automated extraction of OpenAPI schemas (no resource names — parsing issue) | **Low** — incomplete extraction, rebuilt from scratch |

## 3. Export Mechanics

- **Format**: Encrypted RAR archive containing three components:
  1. FHIR R4 NDJSON files in a `Resources/` folder
  2. Physical document files (PDFs, JPEGs, PNGs) in `DocumentData/{Patient ID}/` folders
  3. A `PatientsDemographics.csv` file mapping patients to internal IDs
  4. A `README.txt` pointing back to the documentation URL
- **Mechanism**: Not documented. The documentation page does not describe how to request or trigger the export — no UI workflow, no API endpoint for initiating the export, no instructions for who can request it or expected turnaround time.
- **Single-patient vs bulk**: The export structure uses `{Sevocity Customer ID}` as the top-level folder, suggesting a bulk/practice-wide export rather than single-patient. Multiple patients are organized into subfolders by Patient ID.
- **Access constraints**: The RAR file is encrypted (encryption algorithm not specified). Key distribution mechanism not documented. No mention of fees.

## 4. Export Content: What's In It

### Data dictionary scope

The export documentation points to the Sevocity FHIR API documentation (an OpenAPI 3.0.1 specification) as the schema reference for the NDJSON files. This API documentation serves as the de facto data dictionary.

From parsing all 52 schema YAML files (`analysis/parse_schemas.py`):

- **28 FHIR resource types** with schema definitions (excluding Group, which is the $export trigger, not a data resource; including Endpoint as an infrastructure reference resource)
- **242 top-level fields** across all resource types
- **670 total fields** including nested sub-properties
- **0 fields with semantic descriptions** — all fields have JSON types (string, integer, object, array) but no human-readable descriptions
- **0 fields with enumerated value sets** — coded fields like `status` are typed as `string` with no documented valid values
- **26 example files** with realistic test data demonstrating actual field population

The schemas are structural type definitions only — they tell you the shape of each resource but not the meaning of fields or their allowed values. A developer familiar with FHIR R4 and US Core STU6.1.0 would understand most fields, but the documentation provides no Sevocity-specific guidance.

### Non-FHIR components

1. **PatientsDemographics.csv** — Referenced in the export documentation as containing "all patient demographics" and mapping patients to their internal IDs. **No schema is provided** — no column headers, data types, or examples.

2. **DocumentData files** — Physical document files organized by patient ID with subfolders for document types ("admissions", "finalizedencounters", "referrals", etc.). Each patient folder includes a `summary.pdf` (chart summary). FHIR DocumentReference resources with LOINC code "11503-0" link to these files via relative URLs.

### Vendor's own content organization

The vendor organizes resources by FHIR resource type. The OpenAPI tags distinguish certified (g)(10) resources (marked with `*`) from non-certified additions. Below is the complete inventory:

| Resource Type | Top-Level Fields | Total (Nested) | Certified (g)(10) | Has Example | Schema Source |
|---|---|---|---|---|---|
| AllergyIntolerance | 8 | 28 | ✓ | Yes | Read |
| Appointment | 5 | 14 | | Yes | Read |
| CarePlan | 8 | 15 | ✓ | No | Read |
| CareTeam | 5 | 14 | ✓ | No | Read |
| Condition | 10 | 29 | ✓ | Yes | Read |
| Coverage | 11 | 39 | ✓ | Yes | Search bundle |
| Device | 11 | 17 | ✓ | No | Read |
| DiagnosticReport | 10 | 21 | ✓ | Yes | Read |
| DocumentReference | 12 | 37 | ✓ | Yes | Read |
| Encounter | 13 | 45 | ✓ | Yes | Read |
| Endpoint | 7 | 14 | ✓ | No | Search bundle |
| Goal | 6 | 13 | ✓ | No | Read |
| Immunization | 8 | 17 | ✓ | Yes | Read |
| Location | 7 | 15 | ✓ | No | Read |
| Medication | 3 | 7 | ✓ | Yes | Read |
| MedicationDispense | 11 | 33 | ✓ | Yes | Read |
| MedicationRequest | 13 | 36 | ✓ | Yes | Read |
| MedicationStatement | 9 | 16 | | Yes | Read |
| Observation | 9 | 25 | ✓ | Yes | Read |
| Organization | 9 | 20 | ✓ | Yes | Read |
| Patient | 12 | 64 | ✓ | Yes | Read |
| Practitioner | 6 | 18 | ✓ | Yes | Read |
| Procedure | 7 | 14 | ✓ | Yes | Read |
| Provenance | 6 | 16 | ✓ | No | Read |
| Questionnaire | 6 | 19 | | Yes | Search bundle |
| QuestionnaireResponse | 11 | 34 | | Yes | Read |
| RelatedPerson | 8 | 24 | | Yes | Read |
| ServiceRequest | 11 | 26 | | Yes | Read |

**Non-FHIR components:**
| Component | Schema Documented | Description |
|---|---|---|
| PatientsDemographics.csv | No | CSV with patient demographics, maps patients to internal IDs |
| DocumentData (files) | Partial (folder structure described) | PDFs, JPEGs, PNGs organized by patient, includes chart summaries |

Full field-level inventory: `analysis/entity-inventory-full.json` (670 field definitions across 28 resource types)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export uses a hybrid approach: FHIR NDJSON for structured clinical data, physical document files for unstructured documents, and a CSV for demographics. Sevocity has gone beyond its (g)(10) certified API surface by adding 6 non-certified resource types:

**Non-certified additions beyond (g)(10):**
- **Appointment** — scheduling/visit data
- **MedicationStatement** — historical medication use beyond just prescriptions
- **Questionnaire** — assessment form definitions (templates for screening tools)
- **QuestionnaireResponse** — completed clinical assessments (example shows a 20-item Zung Self-Rating Depression Scale with scored items)
- **RelatedPerson** — emergency contacts and guarantors
- **ServiceRequest** — lab/diagnostic orders with CPT/HCPCS/SNOMED coding and ICD-10-CM reason codes

**DocumentData folder** — The physical document export is a genuinely useful addition beyond standard FHIR. It captures chart summaries (`summary.pdf`), finalized encounter notes, admission documents, and referrals as actual files, organized by patient. The FHIR DocumentReference resources link to these files.

**Richest resources by field count:** Patient (64 fields with US Core extensions for race, ethnicity, birthsex, sex, gender identity, tribal affiliation), Encounter (45 fields including diagnoses, participants, locations, discharge disposition), Coverage (39 fields), DocumentReference (37 fields), MedicationRequest (36 fields).

**Thinnest resources:** Medication (7 fields — just code, id, meta, status), Appointment (14 fields), Goal (13 fields), CareTeam (14 fields).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (64 fields), PatientsDemographics.csv, RelatedPerson (24 fields) | Thorough; US Core extensions for race/ethnicity/sex/gender/tribal affiliation |
| Encounters / visits | ✅ Covered | Encounter (45 fields), Appointment (14 fields) | Good; includes class, diagnoses, participants, locations, discharge disposition |
| Problems / conditions / diagnoses | ✅ Covered | Condition (29 fields) | Standard US Core; example shows ICD-10-CM coding |
| Medications / prescriptions | ✅ Covered | MedicationRequest (36 fields), Medication (7 fields), MedicationStatement (16 fields), MedicationDispense (33 fields) | Good depth across 4 resource types |
| Allergies | ✅ Covered | AllergyIntolerance (28 fields) | Standard US Core |
| Immunizations | ✅ Covered | Immunization (17 fields) | Standard US Core |
| Vitals | ✅ Covered | Observation (25 fields) | Via Observation with LOINC codes; standard US Core vitals profiles |
| Lab results | ✅ Covered | Observation (25 fields), DiagnosticReport (21 fields) | Standard FHIR lab result pattern |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (21 fields) | DiagnosticReport covers this but no dedicated imaging resources; product does order imaging tests |
| Procedures | ✅ Covered | Procedure (14 fields) | Standard US Core |
| Clinical notes / documents | ✅ Covered | DocumentReference (37 fields) + DocumentData files (PDFs, images) | Strong — physical files organized by type plus FHIR references; includes chart summaries, encounter notes, referrals, admissions |
| Care plans / goals | ✅ Covered | CarePlan (15 fields), Goal (13 fields) | Present but relatively thin field counts |
| Orders / referrals | ✅ Covered | ServiceRequest (26 fields) | Non-certified addition; example shows lab order with CPT code and ICD-10 reason |
| Insurance / coverage | ✅ Covered | Coverage (39 fields) | Good; example shows Medicare with member number, payer reference, group, period |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or ChargeItem resources | **Significant gap** for Sevocity Premier users with integrated billing. No billing records, charges, claims, payments, or ERA data. |
| Payments | ❌ Not covered | No payment-related resources | Gap for Premier users |
| Consents / directives | ❌ Not covered | No Consent resource | Product likely stores consent forms; may be partially captured as scanned documents in DocumentData |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has a patient portal with messaging; these messages are not in the export |
| Specialty-specific data | ⚠️ Partial | Questionnaire + QuestionnaireResponse (example: Zung Depression Scale, 20 items with scores) | Captures structured screening tools/assessments, but 40+ specialty templates may generate data not fully captured in QuestionnaireResponse format |
| Clinical assessments | ✅ Covered | QuestionnaireResponse with scored items | Non-certified addition; demonstrates structured clinical assessment data export |
| Family health history | ❌ Not covered | No FamilyMemberHistory resource | Product likely captures family history; not in export |
| Medical devices | ✅ Covered | Device (17 fields) | Standard US Core |

## 6. Documentation Quality

**Strengths:**
- The OpenAPI 3.0.1 specification is well-organized with modular YAML files for each resource type — 52 schema files, 52 path files, 26 example files
- Example instances use realistic test data (San Antonio addresses, real clinical codes, structured assessment responses with scores)
- The Swagger UI provides interactive browsing of all endpoints and schemas
- Clear distinction between certified (g)(10) and additional resource types via asterisk markers in tags
- The main export page clearly explains the RAR file structure and how DocumentReference resources link to physical document files

**Weaknesses:**
- **No field descriptions** — zero of 670 fields have semantic descriptions. Fields are typed (string, integer, object, array) but not explained. A developer unfamiliar with FHIR would struggle.
- **No value set documentation** — coded fields like `status`, `clinicalStatus`, `verificationStatus` show `type: string` with no enumerated valid values. The examples implicitly demonstrate correct values, but this is not a substitute for documentation.
- **No PatientsDemographics.csv schema** — the CSV file is mentioned but no column headers, types, or examples are provided.
- **No export workflow documentation** — no instructions on how to request the export, who can initiate it, expected file sizes, or turnaround time.
- **No relationship documentation beyond FHIR references** — standard FHIR references (e.g., Encounter.subject → Patient) are implicit in the schemas but not explicitly documented.
- A developer could build an import from these docs if they know FHIR R4 and US Core STU6.1.0. Without that prerequisite knowledge, the documentation is insufficient.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data domains well — demographics, encounters, conditions, medications, allergies, immunizations, vitals, labs, procedures, documents, care plans, goals, coverage, and orders are all present. The addition of 6 non-certified resource types (Appointment, MedicationStatement, Questionnaire, QuestionnaireResponse, RelatedPerson, ServiceRequest) and the DocumentData file export go meaningfully beyond the (g)(10) FHIR API surface. However, there are notable gaps:

- **No billing/claims data** despite Sevocity Premier offering integrated billing, clearinghouse, claims, ERAs, and eligibility verification. This is the most significant gap.
- **No patient portal messages** despite the product having a patient portal with provider messaging.
- **No family health history** (no FamilyMemberHistory resource).
- **No consent forms** as structured data (may exist as scanned documents).

For the base Sevocity EHR (non-Premier), the gaps are narrower since billing is handled externally. But for Premier users, the omission of all billing data is a real shortcoming.

**Axis 2 — Export approach: Purpose-built EHI export**

Sevocity has built a purpose-specific (b)(10) export that goes beyond simply repackaging their (g)(10) FHIR API. The evidence:

1. The export is delivered as an encrypted RAR file with a defined folder structure — not just an API endpoint.
2. Six non-certified FHIR resource types are added beyond the (g)(10) surface: Appointment, MedicationStatement, Questionnaire, QuestionnaireResponse, RelatedPerson, ServiceRequest.
3. The DocumentData folder exports physical document files (PDFs, images, chart summaries) organized by patient and document type — this is data that the standard FHIR API cannot fully deliver.
4. The PatientsDemographics.csv provides a supplementary demographics export alongside the FHIR Patient resources.
5. The documentation page is specifically framed as (b)(10) compliance ("§170.315(b)(10) – Electronic Health Information export").

This is clearly more than a relabeled (g)(10) API. The vendor has invested effort in building a dedicated export package. However, the export remains FHIR-based (NDJSON) rather than a native database dump, which means it's constrained by what the vendor has mapped to FHIR resource types. Data that doesn't have a FHIR mapping (billing, portal messages, specialty template fields beyond QuestionnaireResponse) likely falls through the cracks.

### Key Findings

1. **Genuine (b)(10) effort with 6 non-certified resource additions**: Sevocity adds Appointment, MedicationStatement, Questionnaire, QuestionnaireResponse, RelatedPerson, and ServiceRequest beyond their (g)(10) API, plus a physical document export and CSV demographics file. This is more work than most small vendors do.

2. **Billing data completely absent despite Premier tier**: No Claim, ExplanationOfBenefit, ChargeItem, or payment resources are in the export. For Sevocity Premier customers with integrated billing, this is a significant gap in EHI completeness.

3. **Zero field descriptions in the data dictionary**: All 670 fields across 28 resource types have JSON types but no semantic descriptions or value set bindings. The documentation implicitly relies on the reader knowing FHIR R4 and US Core STU6.1.0.

4. **Strong document export**: The DocumentData folder with physical files (PDFs, images) organized by patient and document type, linked via FHIR DocumentReference resources, captures clinical documents that pure FHIR exports typically miss.

5. **QuestionnaireResponse captures specialty clinical assessments**: The example shows a 20-item Zung Self-Rating Depression Scale with scored responses, demonstrating that structured clinical assessment data from Sevocity's specialty templates is captured — a domain most small-vendor exports miss entirely.

### Summary Stats

```
Coverage:        Partial
Approach:        Purpose-built EHI export
Export format:   FHIR R4 NDJSON + document files (PDF/JPEG/PNG) + CSV, delivered as encrypted RAR
Entities:        28 FHIR resource types + 2 non-FHIR components (CSV, document files)
Fields:          670 (including nested); 242 top-level
Descriptions:    0% (0/670 fields have descriptions)
Sample data:     Yes (26 example files with realistic test data)
Bulk export:     Yes (practice-wide export by Customer ID)
Domains covered: 14 of 19 applicable domains
```

### Bottom Line

Sevocity has built a genuine (b)(10) export that goes beyond their (g)(10) API with 6 additional resource types, a physical document export, and a CSV demographics file — more effort than most vendors of their size invest. The biggest gap is the complete absence of billing and claims data, which is particularly notable for Sevocity Premier customers with integrated billing capabilities. A patient would get a reasonably complete clinical record but no billing history, no portal messages, and no family health history.
