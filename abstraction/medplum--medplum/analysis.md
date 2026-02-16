# EHI Export Analysis: Medplum

**Product**: Medplum, Version 5
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.3147.Medp.05.03.1.251231 (CHPL listing 11745)

## 1. Product Context

Medplum is an open-source, FHIR-native "headless EHR" platform — an API-first developer infrastructure for building custom healthcare applications. Unlike traditional turnkey EHRs, Medplum provides a clinical data repository (CDR), FHIR R4 APIs, authentication, server-side automation ("Bots"), and a React UI component library. Customers (healthcare technology companies and provider organizations) build their own EHR, patient portal, or clinical application on top of this foundation.

The platform stores data natively as FHIR R4 resources. This is architecturally significant for EHI export assessment: the internal data model IS the FHIR specification. Medplum supports all 146 FHIR R4 resource types plus 19 Medplum-specific custom types (165 total).

**Documented capabilities relevant to EHI completeness:**
- **Clinical**: Patient demographics, encounters, conditions/diagnoses, observations (vitals, labs), medications (via DoseSpot integration), allergies, immunizations, procedures, clinical notes/documents, care plans, imaging references, questionnaire/assessment responses, implantable devices
- **Financial**: Claims, billing, revenue cycle (case studies with Develo for pediatric billing, Flexpa for claims interoperability)
- **Administrative**: Scheduling, provider directory, user management, communications
- **Specialty**: Radiology (Rad AI, IHE IRA certification), pediatrics (Summer Health), cardiac care (Chamber Cardio), diagnostics (Ro Diagnostics)

**Key nuance**: Because Medplum is a platform, the actual data stored varies by deployment. The export mechanism exports whatever FHIR resources exist for a patient, but what exists depends entirely on how the customer application was built.

## 2. Artifacts Reviewed

| Artifact | Description | Informative Value |
|---|---|---|
| `patient-everything.md` (3.3 KB) | Markdown source of the $patient-everything documentation — the designated b(10) EHI export mechanism. Explicitly states the FHIR Bundle is "the supported machine readable Electronic Health Information Export (EHI) format for Medplum." | **High** — primary b(10) documentation |
| `patient-everything.html` (59 KB) | Rendered HTML of the same page | Medium — confirms content |
| `patienteverything.ts` (6.9 KB) | Open-source TypeScript implementation of $patient-everything from GitHub | **High** — authoritative source of truth on exactly what the export includes and excludes |
| `capability-statement.json` (314 KB) | FHIR CapabilityStatement from `api.medplum.com`, server v5.0.14. Lists 146 supported resource types. | **High** — machine-readable catalog of all supported resources |
| `openapi.json` (2.7 MB) | OpenAPI 3.1 spec with 737 schemas covering all FHIR resource types + data types + backbone elements. Every field has a name, type, and description. | **High** — comprehensive machine-readable data dictionary |
| `enrichment/resources.json` (1.6 MB) | Pre-extracted resource catalog: 165 resource types, 4,006 fields, Patient Compartment membership for each. Derived from CapabilityStatement + OpenAPI spec. | **High** — primary structured data source for analysis |
| `enrichment/coverage.json` (10 KB) | Extraction statistics, Patient Compartment resource listing with field counts. | Medium — verification/cross-check |
| `onc-compliance.md` (8.0 KB) | ONC certification page. Maps b(10) directly to `/docs/api/fhir/operations/patient-everything`. | **High** — confirms b(10) linkage |
| `bulk-fhir-api.md` (3.6 KB) | Bulk FHIR API 2.0.0 documentation — alternative export mechanism (NDJSON format, Group-level or system-level). Not designated as b(10) but functionally broader. | Medium — supplementary export option |
| `fhir-resources/*.html` (146 files) | Per-resource documentation pages. Field tables are client-side rendered (Docusaurus/React), so static HTML has empty tables. Field data is better obtained from the OpenAPI spec. | Low — page metadata only due to client-side rendering |
| `fhir-datatypes/*.html` (41 files) | Data type documentation pages. Same client-side rendering limitation. | Low |
| `fhir-operations/*.html` (35 files) | Operation documentation pages including $patient-everything, $bulk-fhir, $ccda-export, $claim-export. | Medium — shows available operations |
| `screenshot-patient-everything.png` (519 KB) | Browser screenshot of the $patient-everything page | Low — visual confirmation |
| `screenshot-onc-compliance.png` (690 KB) | Browser screenshot of the ONC compliance page | Low — visual confirmation |

## 3. Export Mechanics

**Format**: FHIR R4 JSON Bundle (for `$patient-everything`); NDJSON (for Bulk FHIR API `$export`)

**Mechanism**: REST API call — `GET [base]/R4/Patient/<id>/$everything`

**Parameters** (from `patient-everything.md`):
- `start` / `end`: Filter by care date range
- `_since`: Only resources updated since a given instant
- `_count`: Max results (default: 1,000 per the source code, line 33)
- `_offset`: Pagination offset
- `_type`: Restrict to specific resource types (comma-separated)

**Single-patient vs. bulk**:
- `$patient-everything` is single-patient by design
- The Bulk FHIR API 2.0.0 (`/fhir/R4/Group/<id>/$export` or `/fhir/R4/$export`) supports multi-patient and system-level export in NDJSON format. Not explicitly designated as the b(10) mechanism, but is functionally a superset.

**Access constraints**: Requires API authentication (OAuth2/SMART-on-FHIR). No mention of fees for the export itself. The API is developer-facing — no documented UI button for non-technical users.

## 4. Export Content: What's In It

### Data dictionary

Medplum's data dictionary is the FHIR R4 specification itself, made machine-readable through the OpenAPI 3.1 spec (737 schemas, 2.7 MB) and the FHIR CapabilityStatement (146 resource types). The enrichment extraction (`resources.json`) catalogs 165 resource types with 4,006 total fields.

**Field documentation quality** (from `full-entity-inventory.json`):
- 4,006 / 4,006 fields (100%) have descriptions
- 4,006 / 4,006 fields (100%) have type information
- All fields specify array cardinality and required status
- Relationships are expressed through FHIR Reference types — each reference field specifies target resource types
- Value sets are referenced via standard FHIR bindings

### What the export includes

The `$patient-everything` operation (source: `patienteverything.ts`) exports:

1. **Patient Compartment resources** (68 resource types): All FHIR R4 resources linked to the patient via the Patient Compartment definition. Binary is explicitly excluded from compartment search (line 111: `r.code === 'Binary' ? undefined : r.code`).

2. **Resolved references** (6 additional types): Organization, Practitioner, PractitionerRole, Location, Medication, Device — recursively resolved from references in compartment resources (line 180).

**Total exportable resource types: 74** (68 compartment + 6 resolved). These contain **1,904 fields** total (1,771 compartment + 133 resolved references).

### Vendor's own content organization

Because Medplum is FHIR-native, it uses FHIR resource types as its organizational structure. Below are the Patient Compartment resources (the resources actually included in the b(10) export), organized by EHI-relevant domain. Full inventory is in `analysis/full-entity-inventory.json`.

**Summary by domain** (68 compartment resources + 6 resolved reference types):

| Domain | Resources | Fields | In Compartment | Key Resource Types |
|---|---|---|---|---|
| Demographics | 3 | 64 | 3 | Patient (26), Person (18), RelatedPerson (20) |
| Encounters / Visits | 2 | 51 | 2 | Encounter (31), EpisodeOfCare (20) |
| Problems / Conditions | 2 | 62 | 2 | Condition (33), ClinicalImpression (29) |
| Medications | 4+2 | 178 | 4 | MedicationRequest (42), MedicationAdministration (29), MedicationDispense (34), MedicationStatement (27), + Medication (17) resolved |
| Allergies | 1 | 28 | 1 | AllergyIntolerance (28) |
| Immunizations | 3 | 73 | 3 | Immunization (37), ImmunizationEvaluation (23), ImmunizationRecommendation (13) |
| Vitals / Observations | 1 | 45 | 1 | Observation (45) |
| Lab Results / Diagnostics | 3 | 72 | 3 | DiagnosticReport (27), Specimen (21), MolecularSequence (24) |
| Imaging | 2 | 59 | 2 | ImagingStudy (28), Media (31) |
| Procedures | 2 | 86 | 2 | Procedure (40), ServiceRequest (46) |
| Clinical Notes / Documents | 3 | 67 | 3 | Composition (23), DocumentReference (24), DocumentManifest (20) |
| Care Plans / Goals | 4 | 102 | 4 | CarePlan (31), CareTeam (21), Goal (25), NutritionOrder (25) |
| Orders / Referrals | 6 | 172 | 6 | Task (39), DeviceRequest (35), SupplyRequest (26), SupplyDelivery (21), RequestGroup (26), GuidanceResponse (25) |
| Insurance / Coverage | 4 | 109 | 4 | Coverage (25), CoverageEligibilityRequest (23), CoverageEligibilityResponse (24), EnrollmentRequest (15), + Contract (43, not in compartment) |
| Claims / Billing | 6 | 201 | 6 | Claim (35), ClaimResponse (35), ExplanationOfBenefit (51), ChargeItem (37), Account (19), Invoice (24) + PaymentNotice, PaymentReconciliation (not in compartment) |
| Consents / Directives | 1 | 22 | 1 | Consent (22) |
| Patient Communications | 2 | 62 | 2 | Communication (31), CommunicationRequest (31) |
| Scheduling | 3 | 62 | 3 | Appointment (30), AppointmentResponse (16), Schedule (16) |
| Devices | 1+1 | 56 | 1 | DeviceUseStatement (23), + Device (33) resolved |
| Risk / Safety | 4 | 91 | 4 | AdverseEvent (28), DetectedIssue (21), Flag (16), RiskAssessment (26) |
| Questionnaires / Assessments | 1 | 19 | 1 | QuestionnaireResponse (19) |
| Family History | 1 | 34 | 1 | FamilyMemberHistory (34) |
| Provider Directory | 0+6 | 154 | 0 | Organization (21), Practitioner (22), PractitionerRole (23), Location (24), HealthcareService (30), Endpoint (17), OrganizationAffiliation (17) — resolved via references |
| Provenance / Audit | 2 | 38 | 2 | Provenance (19), AuditEvent (19) |

**Representative high-field-count resources (top 10 in compartment):**

| Resource Type | Fields | Category |
|---|---|---|
| ExplanationOfBenefit | 51 | Claims / Billing |
| ServiceRequest | 46 | Procedures |
| Observation | 45 | Vitals / Observations |
| MedicationRequest | 42 | Medications |
| Procedure | 40 | Procedures |
| Task | 39 | Orders / Referrals |
| ChargeItem | 37 | Claims / Billing |
| Immunization | 37 | Immunizations |
| Claim | 35 | Claims / Billing |
| ClaimResponse | 35 | Claims / Billing |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Medplum's export is architecturally unique: because the data model IS FHIR R4, the export returns the actual stored data without transformation. The `$patient-everything` operation exports all 68 FHIR R4 Patient Compartment resource types plus 6 referenced types.

**Richest domains** (by field count):
- Claims / Billing: 6 compartment resources, 201 fields — includes ExplanationOfBenefit (51 fields), Claim (35), ClaimResponse (35), ChargeItem (37), Account (19), Invoice (24). This is genuinely deep billing coverage.
- Medications: 6 resources (4 compartment + 2 resolved), 178 fields — covers prescriptions, administration, dispensing, and statements.
- Orders / Referrals: 6 resources, 172 fields — Task, DeviceRequest, SupplyRequest/Delivery, RequestGroup, GuidanceResponse.
- Provider Directory: 7 resources, 154 fields — resolved via references for contextual completeness.

**Thinnest domains** (by resource count):
- Allergies: 1 resource (AllergyIntolerance, 28 fields) — adequate, this is a single-concept domain.
- Consents: 1 resource (Consent, 22 fields) — standard FHIR coverage.
- QuestionnaireResponse: 1 resource (19 fields) — the Questionnaire definition itself (30 fields) is NOT in the compartment, so exported responses lack their form definition context.

**Notable**: Binary resources are explicitly excluded from the compartment search in the source code (line 111 of `patienteverything.ts`). If clinical documents are stored as Binary + DocumentReference, the DocumentReference would be exported but the raw Binary content (PDFs, images, DICOM files) would only be included if referenced by a compartment resource AND if the reference resolution logic catches it — but Binary is not one of the 6 allowed reference types (line 180). This is a potential gap for document-heavy implementations.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (26 fields), Person (18), RelatedPerson (20) | Thorough — standard FHIR Patient resource with all demographic fields |
| Encounters / visits | ✅ Covered | Encounter (31 fields), EpisodeOfCare (20) | Thorough — includes class, type, period, participants, locations, diagnoses |
| Problems / conditions / diagnoses | ✅ Covered | Condition (33 fields), ClinicalImpression (29) | Thorough — code, severity, onset, evidence, stage |
| Medications / prescriptions | ✅ Covered | MedicationRequest (42), MedicationAdministration (29), MedicationDispense (34), MedicationStatement (27), Medication (17 resolved) | Thorough — covers full medication lifecycle |
| Allergies | ✅ Covered | AllergyIntolerance (28 fields) | Thorough |
| Immunizations | ✅ Covered | Immunization (37), ImmunizationEvaluation (23), ImmunizationRecommendation (13) | Thorough |
| Vitals | ✅ Covered | Observation (45 fields) — vitals use Observation with vital-signs category | Thorough |
| Lab results | ✅ Covered | Observation (45), DiagnosticReport (27), Specimen (21) | Thorough |
| Imaging / diagnostic reports | ✅ Covered | ImagingStudy (28), Media (31), DiagnosticReport (27) | Covered for metadata; Binary exclusion may affect actual image data |
| Procedures | ✅ Covered | Procedure (40), ServiceRequest (46) | Thorough |
| Clinical notes / documents | ⚠️ Partial | Composition (23), DocumentReference (24), DocumentManifest (20) — but Binary excluded from compartment search | Metadata covered; raw document content (PDFs, images) may be excluded due to Binary exclusion |
| Care plans / goals | ✅ Covered | CarePlan (31), CareTeam (21), Goal (25), NutritionOrder (25) | Thorough |
| Orders / referrals | ✅ Covered | ServiceRequest (46), Task (39), DeviceRequest (35), RequestGroup (26) | Thorough |
| Insurance / coverage | ✅ Covered | Coverage (25), CoverageEligibilityRequest (23), CoverageEligibilityResponse (24), EnrollmentRequest (15) | Thorough |
| Claims / billing | ✅ Covered | Claim (35), ClaimResponse (35), ExplanationOfBenefit (51), ChargeItem (37), Account (19), Invoice (24) | Thorough — 6 resource types with 201 fields |
| Payments | ⚠️ Partial | PaymentNotice and PaymentReconciliation exist in the FHIR spec but are NOT in the Patient Compartment and not in the 6 resolved reference types | Minor gap — these 2 resources would need to be explicitly queried |
| Consents / directives | ✅ Covered | Consent (22 fields) | Adequate |
| Patient communications / portal messages | ✅ Covered | Communication (31), CommunicationRequest (31) | Thorough |
| Specialty-specific | ✅ Covered (structurally) | QuestionnaireResponse (19) for custom assessments; Observation extensions for specialty data; platform supports any FHIR resource type | Coverage depends on what the customer application stores; the export mechanism itself is not a bottleneck |

## 6. Documentation Quality

**Strengths:**
- The `$patient-everything` documentation is clear, concise, and developer-oriented. It explicitly names the operation as "the supported machine readable Electronic Health Information Export (EHI) format for Medplum."
- Machine-readable artifacts are outstanding: the OpenAPI 3.1 spec (2.7 MB, 737 schemas) provides complete field definitions (name, type, description, cardinality) for every resource type. The CapabilityStatement lists all 146 supported resource types with their interactions.
- 100% of all 4,006 fields across 165 resource types have both descriptions and type information.
- Open-source code: the actual `$patient-everything` implementation is available on GitHub (`patienteverything.ts`), providing the ultimate source of truth on export behavior.
- The ONC compliance page cleanly maps b(10) to the `$patient-everything` operation.

**Weaknesses:**
- No sample export output — there is no example of what a real `$patient-everything` response looks like. A developer must understand FHIR to work with the export.
- No explicit enumeration of Patient Compartment resources on the documentation page itself — it refers to the FHIR R4 specification but doesn't list the 68 included resource types.
- No export instructions for non-technical users. The documentation assumes API fluency.
- The Binary exclusion is not documented — it can only be discovered by reading the source code.
- The FHIR resource documentation pages (146 HTML files) have empty field tables because they rely on client-side React rendering. The field data exists in the OpenAPI spec but is not visible in the downloaded HTML.
- No documented relationship between `$patient-everything` (b(10)) and the Bulk FHIR API ($export). Both export patient data but in different formats and via different mechanisms.

**Overall**: A developer with FHIR expertise could build an import system from these artifacts. The machine-readable specs (OpenAPI, CapabilityStatement) are the real deliverable and are excellent. However, a non-developer would find this documentation insufficient.

## 7. Overall Assessment

### Classification

**Standard-based projection** (with important caveats)

While Medplum's export uses the FHIR standard, this classification requires nuance. For most vendors, "standard-based projection" implies a lossy conversion from a richer internal model to a standardized subset. Medplum is different: its internal data model IS FHIR R4. There is no internal proprietary model being projected — the export returns the actual stored data in its native format. This makes the FHIR-based export effectively equivalent to a native data model export.

However, the classification remains "standard-based projection" rather than "comprehensive native export" because:
1. The export is scoped to the FHIR Patient Compartment (68 of 165 resource types), not the entire data model
2. Binary resources are explicitly excluded, potentially omitting document content
3. The Questionnaire definition resource (form templates) is not exported with QuestionnaireResponse
4. PaymentNotice and PaymentReconciliation are not in the Patient Compartment
5. 15 Medplum custom resource types (platform configuration) are not exported — though these are appropriately excluded as they are not EHI

### Key Findings

1. **Architecturally sound export mechanism.** Medplum's FHIR-native architecture means the `$patient-everything` export returns stored data without transformation. The 68 Patient Compartment resource types cover clinical, billing, insurance, communication, and scheduling domains with 1,771 fields — all with 100% description and type coverage from the OpenAPI spec. This is not a C-CDA or USCDI-only export; it includes ExplanationOfBenefit, Claim, ChargeItem, Invoice, and other financial resources. (Source: `patienteverything.ts`, `enrichment/resources.json`)

2. **Excellent machine-readable documentation.** The OpenAPI 3.1 spec (737 schemas, 2.7 MB) and CapabilityStatement (146 resource types) provide complete, queryable data dictionaries publicly accessible without authentication. Every field has a name, type, and description. (Source: `openapi.json`, `capability-statement.json`)

3. **Binary resource exclusion is a real gap for document-heavy deployments.** The source code (line 111 of `patienteverything.ts`) explicitly filters out Binary resources from compartment search, and Binary is not among the 6 resolved reference types (line 180). This means raw PDFs, images, and DICOM files may be excluded from the export even when they are part of the patient's clinical record. This is not documented. (Source: `patienteverything.ts`)

4. **Platform variability makes completeness assessment inherently conditional.** As a platform where customers build their own applications, what data actually exists for any given patient depends entirely on the implementation. The export mechanism itself is complete (it returns all compartment resources that exist), but whether a deployment stores billing data, specialty assessments, or imaging data depends on the customer's application. The export is as complete as the implementation.

5. **Default pagination limit of 1,000 resources.** The source code sets `defaultMaxResults = 1000` (line 33). For patients with extensive records, the initial call may not return all data — the caller must paginate using `_count` and `_offset`. This is standard FHIR behavior but worth noting for completeness.

### Summary Stats

```
Classification:  Standard-based projection (FHIR-native — no lossy conversion)
Export format:   FHIR R4 JSON Bundle (also NDJSON via Bulk FHIR API)
Model type:      Standard projection (but internal model IS FHIR, so effectively native)
Entities:        74 exportable resource types (68 compartment + 6 resolved)
Fields:          1,904 (across exportable resource types)
Descriptions:    100% (4,006/4,006 across all 165 types)
Sample data:     No
Bulk export:     Yes (Bulk FHIR API $export, separate from b(10) $patient-everything)
Domains covered: 17 of 18 applicable domains (Payments partially covered)
```

### Bottom Line

Medplum's EHI export is architecturally one of the strongest among certified EHR products because its internal data model IS the export format — FHIR R4 — eliminating the conversion loss that plagues most vendor exports. The export covers clinical, billing, insurance, communication, and scheduling domains with 74 resource types and 1,904 fields, all with complete documentation. The primary concern is the undocumented Binary exclusion, which could omit document/image content in document-heavy deployments, and the inherent variability of what data exists in any given platform deployment.
