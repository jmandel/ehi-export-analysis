# EHI Export Analysis: Medplum

**Product**: Medplum v5  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3147.Medp.05.03.1.251231

## 1. Product Context

Medplum is an open-source, FHIR-native "headless EHR" platform — an API-first developer infrastructure for building custom healthcare applications. Unlike traditional EHRs, Medplum provides the backend (clinical data repository, FHIR R4 APIs, authentication, automation, React UI components) and customers build their own clinical applications on top of it. The certified product (Medplum v5, certified 2025-12-31) encompasses the entire platform.

**Key architectural distinction**: Medplum's data store IS FHIR R4. There is no proprietary internal database model being projected into FHIR — FHIR resources are the native storage format. This means the FHIR API surface represents 100% of the data model, not a subset.

**What data it stores** (varies by deployment, but the platform supports):
- **Clinical**: Patient demographics, encounters, conditions, medications (via DoseSpot integration), lab orders/results (via Health Gorilla), immunizations, vitals, observations, procedures, care plans, clinical notes, imaging references, questionnaire responses, family history, allergies, devices
- **Financial**: Claims, billing, charge items, invoices, coverage, explanation of benefits (case studies confirm billing use cases via Develo, Flexpa)
- **Administrative**: Scheduling/appointments, provider directories, consent
- **Communications**: Patient-provider messaging, communication requests
- **Infrastructure**: Bots (automation), access policies, project configuration, user management

**Certified criteria**: (a)(2) CPOE Lab, (a)(5) Demographics, (a)(14) Implantable Devices, (b)(1) Transitions of Care, (b)(10) EHI Export, (b)(11) DSI, (c)(1) CQM, (g)(10) Standardized APIs, plus extensive (d) security criteria.

**Market**: ~20M patients, hundreds of practices. Customers include Summer Health (pediatrics), Ro Diagnostics (labs), Rad AI (radiology), Develo (pediatric billing). ~12-person team, YC-backed.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/patient-everything.md` (3.3 KB) | Markdown source documenting the `$patient-everything` operation — the (b)(10) export mechanism. Describes parameters, output format, and included resources. | **High** — primary export docs |
| `downloads/patienteverything.ts` (6.9 KB) | TypeScript source code implementing `$patient-everything`. Shows exact logic: Patient Compartment search + recursive resolution of Organization/Practitioner/PractitionerRole/Location/Medication/Device references. | **High** — definitive source of truth |
| `downloads/capability-statement.json` (314 KB) | FHIR CapabilityStatement from production server listing 146 supported resource types with search parameters and interactions. | **High** — defines the full data surface |
| `downloads/openapi.json` (2.7 MB) | OpenAPI 3.1 spec with 737 schemas covering all FHIR resource types and data types. Provides complete field-level definitions. | **High** — serves as data dictionary |
| `downloads/onc-compliance.md` (8 KB) | ONC compliance page linking (b)(10) to `$patient-everything`. | **Medium** — confirms export mapping |
| `downloads/bulk-fhir-api.md` (3.6 KB) | Bulk FHIR API docs for group/system-level exports via `$export`. | **Medium** — alternative bulk mechanism |
| `downloads/fhir-resources/*.html` (146 files, ~17 MB total) | Individual resource documentation pages (Docusaurus HTML). Field tables are client-rendered and not available in static HTML. | **Low** — page metadata only; field data from OpenAPI |
| `downloads/fhir-datatypes/*.html` (41 files, ~2.5 MB total) | Data type documentation pages. Same client-rendering limitation. | **Low** |
| `downloads/fhir-operations/*.html` (36 files, ~2.8 MB total) | Operation documentation pages. | **Low** |
| `downloads/enrichment/resources.json` (1.6 MB) | Pre-parsed resource inventory from enrichment scripts. | **Reference** — used to cross-check my parse |
| `downloads/enrichment/coverage.json` (10 KB) | Extraction statistics from enrichment. | **Reference** |
| `downloads/screenshot-*.png` (2 files) | Visual evidence of documentation pages. | **Low** |

## 3. Export Mechanics

- **Format**: FHIR R4 JSON Bundle. The output is a standard FHIR Bundle containing all resources for the patient. The documentation explicitly states: *"The FHIR Bundle created from this operation is the supported machine readable Electronic Health Information Export (EHI) format for Medplum."*
- **Mechanism**: REST API call — `GET [base]/R4/Patient/<id>/$everything`. Available programmatically via the TypeScript SDK (`MedplumClient.readPatientEverything`). No special UI button mentioned.
- **Single-patient**: `$patient-everything` is single-patient. For bulk export, Medplum supports the FHIR Bulk Data API 2.0.0 (`$export`) at group and system level, outputting NDJSON.
- **Parameters**: Supports date filtering (`start`, `end`), incremental export (`_since`), pagination (`_count`, `_offset`), and type filtering (`_type`). Default limit is 1000 resources.
- **Access constraints**: Requires authentication (OAuth2/SMART). AccessPolicy must grant access to relevant resource types. No fees mentioned (open-source platform).

## 4. Export Content: What's In It

### Data dictionary

Medplum's documentation doubles as the data dictionary via the OpenAPI spec and the FHIR specification itself. The platform implements standard FHIR R4 with no vendor-specific extensions or custom resource types in the patient data model.

**From the OpenAPI spec** (`openapi.json`):
- **165 total resource types** (146 standard FHIR R4 + 19 Medplum infrastructure types like Bot, Project, AccessPolicy)
- **4,171 total fields** across all resource types
- **4,171 fields (100%)** have descriptions (these are standard FHIR R4 element definitions)
- Types are documented for all fields
- Relationships are implicit via FHIR references

**In the export** (`$patient-everything`):
- **74 resource types**: 68 in the FHIR R4 Patient Compartment + 6 resolved reference types (Organization, Location, Practitioner, PractitionerRole, Medication, Device)
- **1,978 fields** across export resource types
- **100% have descriptions** (standard FHIR definitions)
- Binary resources are explicitly excluded from the compartment search (per source code)

### Vendor's own content organization

Medplum organizes documentation by FHIR resource type. Since the platform is FHIR-native, there is no separate vendor-specific taxonomy — the FHIR specification IS the data model. Below are the resource types included in the export, grouped by clinical domain:

| Domain | Resources | Total Fields | Notes |
|---|---|---|---|
| Claims / Billing | Account, ChargeItem, Claim, ClaimResponse, ExplanationOfBenefit, Invoice | 207 | Full billing resource set |
| Orders / Referrals | DeviceRequest, GuidanceResponse, RequestGroup, ServiceRequest, SupplyDelivery, SupplyRequest, Task | 225 | Comprehensive order model |
| Medications / Prescriptions | Medication, MedicationAdministration, MedicationDispense, MedicationRequest, MedicationStatement | 153 | Full medication lifecycle |
| Diagnostic Reports / Imaging | DiagnosticReport, ImagingStudy, Media, MolecularSequence, Specimen | 136 | |
| Care Plans / Goals | CarePlan, CareTeam, Goal, NutritionOrder | 106 | |
| Insurance / Coverage | Coverage, CoverageEligibilityRequest, CoverageEligibilityResponse, EnrollmentRequest | 91 | |
| Provider Directory | Location, Organization, Practitioner, PractitionerRole | 87 | Resolved references |
| Immunizations | Immunization, ImmunizationEvaluation, ImmunizationRecommendation | 76 | |
| Clinical Notes / Documents | Composition, DocumentManifest, DocumentReference | 70 | |
| Demographics | Patient, Person, RelatedPerson | 67 | |
| Scheduling | Appointment, AppointmentResponse, Schedule | 65 | |
| Patient Communications | Communication, CommunicationRequest | 64 | |
| Problems / Conditions | ClinicalImpression, Condition | 64 | |
| Medical Devices | Device, DeviceUseStatement | 59 | Device is a resolved reference |
| Encounters / Visits | Encounter, EpisodeOfCare | 53 | |
| Observations (Vitals, Labs) | Observation | 46 | Single resource, many uses |
| Procedures | Procedure | 41 | |
| Provenance / Audit | AuditEvent, Provenance | 40 | |
| Other domains | AdverseEvent, Basic, BodyStructure, Consent, DetectedIssue, FamilyMemberHistory, Flag, Group, List, MeasureReport, QuestionnaireResponse, ResearchSubject, RiskAssessment, VisionPrescription | 294 | Various clinical/admin |

The full inventory of all 74 export resource types with all 1,978 fields is in `analysis/entity-inventory-full.json`. Summary statistics are in `analysis/entity-inventory-summary.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Medplum's export leverages a fundamental architectural advantage: because the platform is FHIR-native, the FHIR R4 Patient Compartment IS the complete patient record. There is no proprietary database being projected or summarized — what's in FHIR is what's in the system.

The export includes 74 resource types spanning clinical, financial, administrative, and communication domains. The breadth is inherent in the FHIR Patient Compartment definition, which was designed to capture all patient-associated data across these domains.

**Richest areas** (by field count):
- Orders/Referrals (225 fields, 7 resources) — ServiceRequest alone has 47 fields
- Claims/Billing (207 fields, 6 resources) — ExplanationOfBenefit has 52 fields, the most of any resource
- Medications (153 fields, 5 resources) — full lifecycle from request through administration

**Key strength**: Unlike most vendors, billing/claims data (Claim, ClaimResponse, ExplanationOfBenefit, ChargeItem, Invoice, Account) is included in the Patient Compartment and thus in the export. This is genuinely part of the FHIR R4 spec, not a vendor addition.

**Documentation quality**: All fields have descriptions and types, but these are standard FHIR R4 definitions, not vendor-specific annotations. There are no Medplum-specific extensions, custom value sets, or implementation notes. A developer would need FHIR R4 knowledge to use the export — the FHIR spec IS the documentation.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (27 fields), `Person` (19), `RelatedPerson` (21) | Standard FHIR demographics; comprehensive |
| Encounters / visits | ✅ Covered | `Encounter` (32), `EpisodeOfCare` (21) | Full encounter model |
| Problems / conditions | ✅ Covered | `Condition` (34), `ClinicalImpression` (30) | Standard FHIR problems |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (43), `MedicationAdministration` (30), `MedicationDispense` (35), `MedicationStatement` (28), `Medication` (17) | Full lifecycle; e-prescribing via DoseSpot integration |
| Allergies | ✅ Covered | `AllergyIntolerance` (29) | Standard allergy model |
| Immunizations | ✅ Covered | `Immunization` (38), `ImmunizationEvaluation` (24), `ImmunizationRecommendation` (14) | Complete |
| Vitals | ✅ Covered | `Observation` (46) | Via Observation with vital sign codes |
| Lab results | ✅ Covered | `Observation` (46), `DiagnosticReport` (28), `Specimen` (22) | Standard FHIR lab model |
| Imaging / diagnostic reports | ✅ Covered | `DiagnosticReport` (28), `ImagingStudy` (29), `Media` (32) | Includes imaging studies and media |
| Procedures | ✅ Covered | `Procedure` (41) | Standard procedure model |
| Clinical notes / documents | ✅ Covered | `Composition` (24), `DocumentReference` (25), `DocumentManifest` (21) | Notes/docs supported; Binary excluded from compartment search |
| Care plans / goals | ✅ Covered | `CarePlan` (32), `CareTeam` (22), `Goal` (26), `NutritionOrder` (26) | Comprehensive care planning |
| Orders / referrals | ✅ Covered | `ServiceRequest` (47), `Task` (40), `DeviceRequest` (36), `RequestGroup` (27) | Full order model |
| Insurance / coverage | ✅ Covered | `Coverage` (26), `CoverageEligibilityRequest` (24), `CoverageEligibilityResponse` (25), `EnrollmentRequest` (16) | Includes eligibility checking |
| Claims / billing | ✅ Covered | `Claim` (36), `ClaimResponse` (36), `ExplanationOfBenefit` (52), `ChargeItem` (38), `Invoice` (25), `Account` (20) | Genuinely comprehensive billing; ExplanationOfBenefit is largest resource |
| Payments | ⚠️ Partial | `Account` partially covers; `PaymentNotice` and `PaymentReconciliation` are NOT in the Patient Compartment and thus excluded | `PaymentNotice` (21 fields) and `PaymentReconciliation` (24 fields) exist in the platform but are not patient-compartment-linked per FHIR spec |
| Consents / directives | ✅ Covered | `Consent` (23) | Standard consent model |
| Patient communications | ✅ Covered | `Communication` (32), `CommunicationRequest` (32) | Messaging supported |
| Questionnaires / forms | ✅ Covered | `QuestionnaireResponse` (20) | Captures form responses; `Questionnaire` (definitional) not in export |
| Specialty-specific | ⚠️ Varies | `VisionPrescription` (17), `MolecularSequence` (25), `FamilyMemberHistory` (35), `NutritionOrder` (26) | Product is a platform — specialty data depends on what customers build. FHIR resource types for specialty data are available but may not be populated. |

**Gap Analysis Notes**:
- **Binary resources excluded**: The source code explicitly filters out Binary resources from the compartment search. This means patient-attached documents (PDFs, images, scanned records) stored as Binary resources may not be included. However, `DocumentReference` resources that point to them ARE included, preserving the metadata.
- **PaymentNotice/PaymentReconciliation**: These billing resources exist in the platform (accessible via API) but are not in the FHIR Patient Compartment per the FHIR spec, so they're excluded from `$patient-everything`. This is a minor gap for deployments that use these resources.
- **Contract**: Not in Patient Compartment. Contains 44 fields; could be relevant for some deployments.
- **Platform-specific data**: Medplum's 19 custom resource types (Bot, Project, AccessPolicy, etc.) are infrastructure, not patient data — correctly excluded from EHI.

## 6. Documentation Quality

**Strengths**:
- **Complete field-level documentation**: Every field across all 165 resource types has a name, type, and description via the OpenAPI spec. 100% description coverage.
- **Machine-readable artifacts**: The CapabilityStatement and OpenAPI spec are excellent machine-readable references. A developer can programmatically discover all supported types and fields.
- **Source code available**: The `$patient-everything` implementation is open-source, so the exact export logic is fully transparent and auditable.
- **Standards-based**: Because the data model IS FHIR R4, there's no proprietary schema to learn. A developer familiar with FHIR can immediately understand the export.

**Weaknesses**:
- **No vendor-specific documentation**: There is no Medplum-specific data dictionary beyond the standard FHIR spec. The documentation doesn't describe how Medplum-specific workflows map to FHIR resources, what extensions (if any) are used, or what value sets are typical in practice.
- **No sample export data**: No sample `$patient-everything` Bundle is provided in the documentation.
- **Client-rendered HTML**: The individual resource documentation pages (146 HTML files) have field tables that are client-rendered JavaScript, making the downloaded HTML files nearly empty of field data. The OpenAPI spec compensates for this.
- **No implementation guide**: No Medplum-specific FHIR Implementation Guide describing profiles, extensions, or constraints beyond base FHIR R4.
- **Pagination concern**: Default `_count` is 1000. For patients with extensive records, the consumer must implement pagination to get all data. The documentation describes pagination parameters but doesn't emphasize this as a potential completeness issue.

**Could a developer use this?** Yes, if they know FHIR R4. The export is a standard FHIR Bundle, the API is standard FHIR, and the OpenAPI spec documents every field. A developer without FHIR experience would need to learn the FHIR spec itself — Medplum doesn't provide a simplified mapping or guide.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

Medplum's architectural choice to be FHIR-native means the Patient Compartment genuinely represents the complete patient record. The export covers 74 resource types spanning demographics, clinical data, billing/claims (Claim, ClaimResponse, ExplanationOfBenefit, ChargeItem, Invoice, Account — 207 fields), insurance/coverage, communications, questionnaires, care plans, consent, and more. This goes well beyond USCDI's ~26 resource types across ~22 data classes.

The coverage is comprehensive *relative to what the product stores*, which is the correct benchmark. Since Medplum stores all data as FHIR resources, and the Patient Compartment captures all patient-linked FHIR resources, the export covers essentially everything except Binary resources (explicitly excluded), a few financial resources outside the compartment (PaymentNotice, PaymentReconciliation), and infrastructure types (correctly excluded).

The main caveat is that Medplum is a platform — actual data breadth depends on what each customer implements. A deployment focused only on lab results will have a narrow export not because of the export mechanism, but because the data simply doesn't exist.

**Axis 2 — Export approach: Purpose-built EHI export (with nuance)**

This classification requires careful reasoning. The `$patient-everything` operation is a standard FHIR operation, not something custom-built for (b)(10). Medplum also uses it for clinical exchange. However, the typical "repackaged" signal — pointing at an existing (g)(10)/USCDI-scoped API and calling it (b)(10) — doesn't apply here because:

1. **FHIR IS the native data model.** Unlike traditional EHRs where (g)(10) exposes a curated USCDI projection of a much larger proprietary database, Medplum's FHIR API exposes *everything*. There is no hidden data behind the API.
2. **The Patient Compartment includes billing data.** The FHIR R4 Patient Compartment includes 68 resource types covering billing (Claim, ExplanationOfBenefit), insurance (Coverage), communications, consent, and other domains well beyond USCDI. This isn't a USCDI-limited surface.
3. **The export resolves referenced resources.** The implementation goes beyond a simple compartment search to recursively resolve Organization, Practitioner, PractitionerRole, Location, Medication, and Device references — ensuring contextual completeness.

The most accurate characterization is that Medplum's architecture makes the distinction between "clinical exchange API" and "EHI export" moot — they are the same thing because the API surface IS the complete data model. This is a legitimate architectural outcome, not a compliance dodge. Classified as purpose-built because the result is a comprehensive EHI export, even though the mechanism is a standard FHIR operation.

### Key Findings

1. **FHIR-native architecture eliminates the typical EHI gap.** Because Medplum stores all data as FHIR resources, the `$patient-everything` operation genuinely returns everything in the patient record — no proprietary data is hidden behind the API. This is verified by examining the source code (`patienteverything.ts`), which searches all Patient Compartment resource types and recursively resolves references.

2. **Billing and financial data are included.** The export covers Claim (36 fields), ClaimResponse (36), ExplanationOfBenefit (52), ChargeItem (38), Invoice (25), and Account (20) — a total of 207 fields across 6 billing-related resources. This is a genuine strength; many vendors omit billing data entirely.

3. **Binary resources are explicitly excluded.** The source code (`patienteverything.ts`, line filtering `r.code === 'Binary' ? undefined : r.code`) excludes Binary resources from the compartment search. This means attached documents (PDFs, images) stored as Binary resources may not be exported, though their DocumentReference metadata is included. This is a notable gap for deployments with significant document storage.

4. **Documentation is the FHIR spec itself — nothing more.** There is no Medplum-specific data dictionary, no sample export data, no implementation guide, and no vendor-specific field descriptions. The OpenAPI spec (737 schemas, 4,171 fields) serves as the de facto data dictionary with 100% field coverage, but all descriptions are standard FHIR R4 definitions. This is adequate for FHIR-literate developers but provides no guidance specific to Medplum implementations.

5. **Platform variability means coverage breadth varies by deployment.** The export *mechanism* is comprehensive, but actual data breadth depends entirely on what each customer has implemented. A pediatric SMS-based care app (Summer Health) will have very different data than a radiology reporting system (Rad AI). The export infrastructure is sound; the actual data depends on the use case.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   FHIR R4 JSON Bundle (single-patient); NDJSON (bulk)
Entities:        74 resource types in export (of 165 total in platform)
Fields:          1,978 (across export resource types)
Descriptions:    100% (standard FHIR R4 definitions)
Sample data:     No
Bulk export:     Yes (via FHIR Bulk Data API $export)
Domains covered: 17 of 19 applicable domains (Payments partial; specialty varies by deployment)
```

### Bottom Line

Medplum's FHIR-native architecture makes `$patient-everything` a genuinely comprehensive EHI export — the FHIR API surface IS the complete data model, including billing, insurance, communications, and other domains well beyond USCDI. The main gaps are the explicit exclusion of Binary resources (attached documents) and the absence of vendor-specific documentation beyond the standard FHIR spec. For a platform where customers build their own applications, the export infrastructure is sound; actual data completeness depends on each deployment's data population.
