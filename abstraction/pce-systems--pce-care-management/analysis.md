# EHI Export Analysis: PCE Systems

**Product**: PCE Care Management v9.4
**Analysis date**: 2026-02-16
**CHPL ID**: 11045 (15.04.04.2125.PCEC.94.01.1.221205)

## 1. Product Context

PCE Care Management is a behavioral health EHR system built for Michigan's publicly funded community mental health system. It serves Community Mental Health Service Programs (CMHSPs) and Prepaid Inpatient Health Plans (PIHPs) managing care for Medicaid beneficiaries with serious mental illness, substance use disorders, and developmental disabilities. PCE claims over 70% of Michigan's Medicaid mental health budget flows through their system.

**Data domains the product should store:**
- **Clinical**: Demographics, conditions/diagnoses, medications, allergies, immunizations, vitals, lab results, procedures, clinical notes, care plans, care teams, goals, devices
- **Behavioral health-specific**: Individualized treatment plans, clinical assessments (MichiCANS), intake/discharge records, incident reports, consent directives (42 CFR Part 2 / Michigan Mental Health Code), substance use disorder treatment records
- **Billing/claims**: Claims submission (confirmed by CMHPSM), coverage/insurance, service reporting — the FHIR API includes Claim and Coverage resources
- **Care coordination**: PIX (Provider Information Exchange) records, HIE data, social service referrals (MiHIN Interoperable Referrals Pledge)
- **Documents**: Scanned documents, PDFs, non-computable files
- **Portal/messaging**: Patient portal (CEHR), messaging capabilities (Message data element in API)

The product is certified across 44 ONC criteria, indicating a full-featured EHR — not a limited module.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/b10_documentation.pdf` (890 KB, 3 pages) | EHI Export (b)(10) format specification. Describes the ZIP/NDJSON/documentation.json structure but does NOT enumerate exported resources or fields. Dated November 20, 2023. | **Low** — describes container format only, not content |
| `downloads/PIX_9_4_API_Documentation.pdf` (1.9 MB, 87 pages) | FHIR (g)(10) API documentation. Contains field-level data element definitions for 23 patient-data resource types. Updated April 23, 2025. | **Medium** — only public data model enumeration, but represents (g)(10) surface, not (b)(10) |
| `downloads/capability-statement.json` (43 KB) | FHIR CapabilityStatement from production endpoint. Declares 22 resource types. | **Low** — confirms API resource set |
| `downloads/g10APIInfo.html` (2.3 KB) | Landing page with links to both documentation PDFs and FHIR API base URLs. | **Low** — navigation only |
| `downloads/landing-page-screenshot.png` (56 KB) | Screenshot of landing page. | **Low** — visual confirmation |

**Critical gap**: The actual (b)(10) data dictionary is embedded in the `documentation.json` file within the export ZIP itself and is not publicly available. No sample exports, sample data, or sample `documentation.json` files are provided.

## 3. Export Mechanics

- **Format**: Password-protected ZIP files containing NDJSON data files + JSON schema (`documentation.json`) + metadata (`meta.json`) + a `Files/` subdirectory for non-computable content (scanned documents, PDFs)
- **Mechanism**: UI-initiated by "authorized EHR users" within the EHR system
- **Scope**: Per-patient or bulk (all patients)
- **Access constraints**: No public fee schedule for the (b)(10) export specifically; the (g)(10) API has a one-time setup fee for exchange partners
- **Self-describing**: The export includes its own schema (`documentation.json`) with resource definitions, property names, types, and descriptions — the schema travels with the data

This is clearly a **separate mechanism** from the (g)(10) FHIR API — different format (NDJSON in ZIP vs FHIR JSON over HTTP), different invocation (UI export vs API calls), and different documentation.

## 4. Export Content: What's In It

### The fundamental problem: content is unknown

The (b)(10) documentation describes only the export **container format**:
- Data types supported: CLOB, DATE, DECIMAL, INTEGER, RESOURCE (cross-reference), STRING, TIMESTAMP
- Structure: per-patient subdirectories with one NDJSON file per resource type
- Non-computable files in a `Files/` subdirectory
- Cross-references between resources via the RESOURCE data type

The documentation states that `documentation.json` contains "a list of all possible resource definitions" — the word "all" suggests comprehensive coverage, but without seeing the file, this cannot be verified.

### What we can infer from the (g)(10) API documentation

The only public enumeration of PCE's data model comes from the 87-page API documentation, which defines 23 patient-data entities (plus 3 utility types) with 308 total patient-data fields. All 308 fields have descriptions and type information.

**Important caveat**: This represents the FHIR API surface, which by definition conforms to US Core profiles. The (b)(10) export likely uses PCE's native data model (the documentation explicitly uses non-FHIR types like CLOB, DECIMAL, TIMESTAMP) and may contain significantly more resources and fields.

### API-documented entities (g)(10) surface — for reference only

| Entity | Fields | Conforms To |
|---|---|---|
| Address | 9 | — |
| AllergyIntolerance | 12 | US Core AllergyIntolerance Profile |
| CarePlan | 15 | US Core CarePlan Profile |
| CareTeam | 9 | US Core CareTeam Profile |
| Claim | 22 | — (not US Core) |
| Condition | 10 | US Core Condition Profile |
| Coverage | 8 | — (not US Core) |
| Device | 21 | US Core Implantable Device Profile |
| Diagnostic Report | 15 | US Core DiagnosticReport Profile |
| Document Reference | 17 | US Core DocumentReference Profile |
| Encounter | 16 | US Core Encounter Profile |
| Goal | 9 | US Core Goal Profile |
| Healthcare Service | 11 | — |
| Immunization | 19 | US Core Immunization Profile |
| Location | 14 | US Core Location Profile |
| Medication Request | 16 | US Core MedicationRequest Profile |
| Observation | 16 | US Core Vital Signs / Smoking Status Profiles |
| Organization | 12 | US Core Organization Profile |
| Patient | 16 | US Core Patient Profile |
| Practitioner | 13 | US Core Practitioner Profile |
| Practitioner Role | 9 | US Core PractitionerRole Profile |
| Procedure | 8 | US Core Procedure Profile |
| Provenance | 11 | US Core Provenance Profile |

**Notable**: Claim (22 fields) and Coverage (8 fields) are present in the API, going beyond standard USCDI. However, these are thin representations — a Claim resource has fields for type, status, billable period, provider, insurance, line items (product/service code, modifiers, date), and paid/total amounts, but this is a FHIR Claim projection, not a full billing record.

Full parsed inventory saved to `analysis/entity-inventory-full.json` (308 patient-data fields across 23 entities).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's public documentation covers only two things:

1. **The (b)(10) export container format** (3 pages): How the ZIP file is structured, what data types are supported, how resources cross-reference each other, and how non-computable files are included. This is well-designed technically but content-free.

2. **The (g)(10) FHIR API data model** (87 pages): 23 patient-data resource types conforming to US Core profiles, plus Claim and Coverage. This covers standard USCDI v1 data classes plus basic billing.

The vendor explicitly chose to embed the (b)(10) data dictionary inside the export itself (`documentation.json`), meaning the actual content of the EHI export is completely opaque to external review.

### 5b. Standardized domain coverage (top-down)

Because the (b)(10) export content is unknown, this assessment is based on the (g)(10) API documentation as the **floor** of what PCE stores. The actual (b)(10) export may cover more.

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial (API only) | `Patient` (16 fields) — name, gender, birthDate, address, race, ethnicity, birth sex, language | API has standard US Core fields. (b)(10) export content unknown — likely has more demographic detail |
| Encounters / visits | ⚠️ Partial (API only) | `Encounter` (16 fields) — status, class, type, period, reason, participants, location | Standard US Core encounter. Behavioral health encounter details (session type, duration, modality) unknown |
| Problems / diagnoses | ⚠️ Partial (API only) | `Condition` (10 fields) — category, clinical/verification status, code, recorded date | Standard US Core. No evidence of behavioral health-specific diagnostic detail |
| Medications | ⚠️ Partial (API only) | `MedicationRequest` (16 fields) — status, intent, medication code, dosage, refills | Standard US Core. No MAR or psychotropic medication monitoring |
| Allergies | ⚠️ Partial (API only) | `AllergyIntolerance` (12 fields) | Standard US Core |
| Immunizations | ⚠️ Partial (API only) | `Immunization` (19 fields) | Standard US Core |
| Vitals | ⚠️ Partial (API only) | `Observation` (16 fields) — covers vital signs, smoking status, lab results | Standard US Core profiles |
| Lab results | ⚠️ Partial (API only) | `DiagnosticReport` (15 fields), `Observation` | Standard US Core |
| Procedures | ⚠️ Partial (API only) | `Procedure` (8 fields) | Standard US Core, minimal fields |
| Clinical notes / documents | ⚠️ Partial (API only) | `DocumentReference` (17 fields), `DiagnosticReport` (15 fields), plus `Files/` subdirectory for scans | Non-computable files explicitly supported in (b)(10) |
| Care plans / goals | ⚠️ Partial (API only) | `CarePlan` (15 fields), `Goal` (9 fields), `CareTeam` (9 fields) | Standard US Core. Behavioral health treatment plans may have much richer detail |
| Insurance / coverage | ⚠️ Partial (API only) | `Coverage` (8 fields) — status, beneficiary, period, payor | Very thin — only 8 fields for a Medicaid behavioral health system |
| Claims / billing | ⚠️ Partial (API only) | `Claim` (22 fields) — type, items, amounts | Present but FHIR Claim projection. Product handles claims submission; native billing model likely much richer |
| Payments | ❌ Not covered | No payment entities in API | Product does billing; payment tracking likely exists |
| Behavioral health assessments | ❌ Not covered | No assessment instruments (MichiCANS, etc.) in API | **Major gap** — MichiCANS and other structured assessments are core to the product. Unknown if (b)(10) includes them |
| Consent directives | ❌ Not covered | No consent resources in API | **Major gap** — 42 CFR Part 2 consent management is a headline feature of the system |
| Intake / discharge records | ❌ Not covered | No dedicated intake/discharge entities in API | Product handles intake and discharge per product research |
| Incident reports | ❌ Not covered | No incident reporting entities in API | CMHPSM confirms incident reporting is a product feature |
| Patient communications | ❌ Not covered | `Message` data element in API is an error response type, not patient messaging | Patient portal (CEHR) exists; messaging capabilities unclear |
| Orders / referrals | ❌ Not covered | No ServiceRequest or referral entities in API | PCE signed MiHIN Interoperable Referrals Pledge |

## 6. Documentation Quality

**The (b)(10) export documentation is critically thin.** Three pages describe only the container format. There is:

- ❌ No data dictionary (deferred to `documentation.json` inside the export)
- ❌ No enumeration of exported resources
- ❌ No field definitions or descriptions
- ❌ No sample data or sample `documentation.json`
- ❌ No screenshots of the export interface
- ❌ No user guide for initiating the export
- ❌ No machine-readable schema (publicly available)

The design decision to embed the schema in the export (`documentation.json`) is technically sound — it ensures the schema always matches the data and makes the export self-describing. However, it renders the export completely opaque to external evaluation. A patient, provider, or third-party developer cannot determine what the export contains without actually running it.

The (g)(10) API documentation (87 pages) is substantially better — it has field-level definitions with types and descriptions for every attribute. But this documents the FHIR API, not the (b)(10) export.

A developer could not build an import from the public (b)(10) documentation alone. They would need to obtain an actual export to see the `documentation.json` schema.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The public (b)(10) documentation is too thin to assess actual coverage. The 3-page format specification contains zero information about what data is exported. The only public data model enumeration is the (g)(10) FHIR API documentation, which covers standard USCDI v1 data classes plus Claim and Coverage — this is the clinical exchange surface, not a comprehensive EHI export.

Key uncertainty: The `documentation.json` within the export *may* enumerate dozens of behavioral health-specific resources (treatment plans, assessments, consent directives, incident reports, etc.) that go far beyond the FHIR API. The documentation says it contains "all possible resource definitions." But without seeing it, this cannot be verified.

**Axis 2 — Export approach: Purpose-built EHI export**

Despite the documentation gap, the export mechanism itself is clearly purpose-built:
- It uses PCE's native data model (CLOB, DECIMAL, TIMESTAMP types — not FHIR types)
- It has a separate invocation mechanism (UI export, not API)
- It has a self-describing schema (`documentation.json`)
- It includes non-computable files (scanned documents, PDFs)
- It supports cross-references between resources via the RESOURCE type
- It has separate documentation from the (g)(10) API
- It supports both per-patient and bulk export

This is not a repackaged FHIR Bulk Data or C-CDA export. PCE built a dedicated export mechanism for (b)(10). The question is whether the *content* behind this well-designed container is comprehensive.

### Key Findings

1. **Purpose-built but opaque**: PCE built a technically sound (b)(10) export format (NDJSON in password-protected ZIP with self-describing JSON schema and non-computable file support), but the public documentation reveals nothing about what data is actually exported. The data dictionary is embedded in the export itself and not published.

2. **Behavioral health data is the critical unknown**: For a behavioral health EHR serving Michigan's CMH system, the most important EHI domains are treatment plans, clinical assessments (MichiCANS), consent directives (42 CFR Part 2), incident reports, and substance use disorder records. None of these appear in the public (g)(10) API documentation, and there is no way to determine from public artifacts whether the (b)(10) export includes them.

3. **Billing representation is thin even in the API**: The Claim resource (22 fields) and Coverage resource (8 fields) are present in the FHIR API, showing PCE stores billing data. However, these are FHIR projections — a Medicaid behavioral health claims system likely has far richer billing data internally.

4. **Documentation quality is among the worst possible while still technically existing**: Three pages of format specification with zero content enumeration. The self-describing design is clever but fails the transparency requirement — no external party can evaluate the export's completeness.

5. **The (g)(10) API itself is standard USCDI v1 + Claims/Coverage**: 23 patient-data entities with 308 fields, all conforming to US Core profiles except Claim, Coverage, HealthcareService, and Address. This represents the regulatory floor for clinical exchange, not a comprehensive data model.

### Summary Stats

    Coverage:        Minimal/stub/unclear (public documentation insufficient to assess)
    Approach:        Purpose-built EHI export
    Export format:   NDJSON in password-protected ZIP with JSON schema
    Entities:        Unknown (public docs list 0 for b(10); g(10) API has 23)
    Fields:          Unknown (public docs list 0 for b(10); g(10) API has 308)
    Descriptions:    N/A (no public data dictionary for b(10))
    Sample data:     No
    Bulk export:     Yes (per-patient or all patients)
    Domains covered: Unknown for (b)(10); (g)(10) API covers ~13 of 19 applicable domains (USCDI scope only)

### Bottom Line

PCE Systems built a technically well-designed (b)(10) export mechanism — self-describing, structured, with non-computable file support — but published essentially zero information about what data it contains. For a behavioral health EHR serving Michigan's Medicaid mental health system, the critical question is whether the export includes treatment plans, clinical assessments (MichiCANS), 42 CFR Part 2 consent directives, and incident reports — none of which are visible in any public artifact. The export may be comprehensive, but no external party can verify this without actually running it.
