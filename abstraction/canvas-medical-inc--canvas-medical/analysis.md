# EHI Export Analysis: Canvas Medical

**Product**: Canvas Medical  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.3112.Canv.01.00.1.220523

## 1. Product Context

Canvas Medical is an API-first, cloud-hosted ambulatory EMR platform targeting tech-enabled healthcare organizations and specialty practices. It is ONC-certified for 35+ criteria including (b)(10). Canvas covers:

- **Clinical**: charting (proprietary "Narrative Charting" with Commands), problem lists, allergies, medications (including compounds, history, statements, stop events), immunizations, vitals, labs (via Health Gorilla), imaging, procedures, care plans, care teams, goals, clinical notes, detected issues, clinical decision support protocols, assessments
- **Orders/Prescribing**: CPOE for meds, labs, imaging; e-prescribing (Surescripts); referrals
- **Billing/RCM**: claims submission (via Claim.MD), billing line items, charge description master, payor-specific charges, coverage/insurance, eligibility checking, payment posting, remittance advices, adjustments, write-offs, installment plans, transactors
- **Patient engagement**: patient portal, secure messaging, questionnaires, letters, banner alerts
- **Scheduling**: appointments, calendars, provider schedules
- **Administrative**: staff management, organizations, facilities, practice locations, teams, tasks, business lines, consents

The Canvas SDK documentation exposes 134 internal data models with 1,784 fields across 51 data pages, plus 55 enumerations — a detailed internal data model covering clinical, financial, administrative, and communication domains.

## 2. Artifacts Reviewed

| Artifact | Description | Scope |
|---|---|---|
| `downloads/ehi-export.html` (21 KB) | Main EHI export documentation page | Lists 29 FHIR R4 resources in the export; describes UI and API mechanisms |
| `downloads/api-pages/*.html` (29 files, ~5 MB total) | FHIR R4 API documentation for each resource | Field-level attribute definitions for all 29 resources including types, descriptions, value options |
| `downloads/sdk-data-pages/data-*.html` (51 files, ~2 MB total) | Canvas SDK internal data model documentation | 134 models with 1,784 fields, 55 enums — shows what Canvas stores internally |
| `downloads/enrichment/fhir-api-resources.json` (1.7 MB) | Pre-extracted FHIR API definitions | 29 resources, 3,698 fields across all operations (read/write/search) |
| `downloads/enrichment/sdk-data-models.json` (230 KB) | Pre-extracted SDK data models | 51 pages, 134 models, 1,784 fields, 55 enums |
| `downloads/ehi-export-page-screenshot.png` | Full-page screenshot | Visual verification of EHI export page content |

**Most informative**: The EHI export page and FHIR API pages together provide a complete view of what's exported and how each resource is documented. The SDK data model pages are critical for assessing coverage gaps — they reveal the internal data model that the export should cover.

## 3. Export Mechanics

- **Format**: FHIR R4 resources in Newline Delimited JSON (NDJSON), via FHIR Bulk Data Access pattern
- **Mechanism**: 
  - **Single patient**: UI button in admin settings ("Fhir bulk data exports") or API call (`GET /Patient/{id}/$export`)
  - **Population/bulk**: Must contact Canvas support; Canvas team initiates the export on the customer's behalf
- **Single-patient vs bulk**: Both supported; single-patient is self-service, bulk requires vendor assistance
- **Access constraints**: UI access is permission-based (requires admin group membership). Population exports may take significant time. No fees mentioned.

## 4. Export Content: What's In It

The export includes 29 FHIR R4 resources. Based on FHIR API documentation, these resources document 1,069 unique fields across read operations, of which 1,055 (98.7%) have descriptions.

The export uses the FHIR Bulk Data Access pattern, outputting all patient-associated resources. Each resource is documented with field names, types, descriptions, required flags, and value options/enums.

### Vendor's own content organization

The vendor organizes resources by FHIR resource type. Based on the export documentation and API pages:

| Resource | Fields (Read) | With Descriptions | Types Documented | Category |
|---|---|---|---|---|
| AllergyIntolerance | 36 | 36 | Yes | Clinical - Allergies |
| Appointment | 48 | 48 | Yes | Administrative - Scheduling |
| CarePlan | 28 | 28 | Yes | Clinical - Care Plans |
| CareTeam | 29 | 29 | Yes | Clinical - Care Teams |
| Claim | 47 | 47 | Yes | Financial - Billing |
| Communication | 26 | 26 | Yes | Communication |
| Condition | 39 | 39 | Yes | Clinical - Problems |
| Consent | 29 | 29 | Yes | Administrative - Consents |
| Coverage | 48 | 48 | Yes | Financial - Insurance |
| CoverageEligibilityResponse | 34 | 34 | Yes | Financial - Insurance |
| Device | 33 | 33 | Yes | Clinical - Devices |
| DiagnosticReport | 36 | 36 | Yes | Clinical - Diagnostics |
| DocumentReference | 42 | 42 | Yes | Clinical - Documents |
| Encounter | 40 | 37 | Yes | Clinical - Encounters |
| Goal | 35 | 35 | Yes | Clinical - Goals |
| Immunization | 32 | 32 | Yes | Clinical - Immunizations |
| Media | 34 | 34 | Yes | Clinical - Documents |
| MedicationDispense | 37 | 37 | Yes | Clinical - Medications |
| MedicationRequest | 46 | 46 | Yes | Clinical - Medications |
| MedicationStatement | 38 | 38 | Yes | Clinical - Medications |
| Observation | 44 | 44 | Yes | Clinical - Observations/Vitals/Labs |
| Patient | 68 | 65 | Yes | Demographics |
| Procedure | 26 | 26 | Yes | Clinical - Procedures |
| Provenance | 31 | 29 | Yes | Administrative - Provenance |
| QuestionnaireResponse | 37 | 37 | Yes | Clinical - Questionnaires |
| RelatedPerson | 31 | 31 | Yes | Demographics |
| ServiceRequest | 33 | 33 | Yes | Clinical - Orders/Referrals |
| Specimen | 20 | 20 | Yes | Clinical - Labs |
| Task | 42 | 40 | Yes | Administrative - Tasks |
| **Total** | **1,069** | **1,055 (98.7%)** | | |

Full inventory saved to `analysis/entity-inventory-full.json`.

**Category breakdown:**

| Category | Entities | Fields |
|---|---|---|
| Clinical - Medications | 3 | 121 |
| Demographics | 2 | 99 |
| Financial - Insurance | 2 | 82 |
| Clinical - Documents | 2 | 76 |
| Administrative - Scheduling | 1 | 48 |
| Financial - Billing | 1 | 47 |
| Clinical - Observations/Vitals/Labs | 1 | 44 |
| Administrative - Tasks | 1 | 42 |
| Clinical - Encounters | 1 | 40 |
| Clinical - Problems | 1 | 39 |
| Clinical - Questionnaires | 1 | 37 |
| Clinical - Allergies | 1 | 36 |
| Clinical - Diagnostics | 1 | 36 |
| Clinical - Goals | 1 | 35 |
| Clinical - Devices | 1 | 33 |
| Clinical - Orders/Referrals | 1 | 33 |
| Clinical - Immunizations | 1 | 32 |
| Administrative - Provenance | 1 | 31 |
| Administrative - Consents | 1 | 29 |
| Clinical - Care Teams | 1 | 29 |
| Clinical - Care Plans | 1 | 28 |
| Communication | 1 | 26 |
| Clinical - Procedures | 1 | 26 |
| Clinical - Labs | 1 | 20 |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Canvas's EHI export includes 29 FHIR R4 resources covering clinical, financial, administrative, and communication domains. Notable strengths:

**Clinical depth is good**: The export covers the full clinical spectrum — allergies, conditions, medications (3 resources: requests, dispenses, statements), immunizations, observations (vitals, labs, social history), procedures, diagnostic reports, documents, care plans, care teams, goals, devices, specimens, questionnaire responses, and service requests/referrals.

**Financial data is included**: The export includes `Claim` (47 fields), `Coverage` (48 fields), and `CoverageEligibilityResponse` (34 fields). The FHIR Claim resource includes diagnosis codes, line items with procedure codes/charges/units, insurance references, NDC codes, and place of service. This is significantly more than USCDI requires.

**Beyond USCDI**: 8 resources in the export are not part of USCDI/US Core: Appointment, Claim, Communication, Consent, CoverageEligibilityResponse, Media, MedicationStatement, and Task. This indicates a purpose-built effort.

**Communication**: Communication resource captures messaging data.

**Thinner areas**: The Claim FHIR resource (47 fields) represents a significant compression of the internal billing model. Canvas's SDK exposes 12 claim-related models with 210 fields plus 10 posting/payment models with 78 fields — a total of 288 fields across 22 models for billing alone. The FHIR Claim resource, while reasonably deep, cannot capture the full granularity of payment postings, remittance advices, line-item adjustments, write-offs, coverage posting details, and transactor information that the SDK reveals.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (68 fields), `RelatedPerson` (31 fields) | Thorough — includes extensions, identifiers, addresses, contacts |
| Encounters / visits | ✅ Covered | `Encounter` (40 fields) | Good — includes type, class, period, participants, reason codes |
| Problems / conditions | ✅ Covered | `Condition` (39 fields) | Good — includes clinical status, verification, onset, codings |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (46), `MedicationDispense` (37), `MedicationStatement` (38) | Deep — 3 resources totaling 121 fields. SDK also has CompoundMedication, MedicationHistory, StopMedicationEvent (66 SDK fields) not directly mapped to separate FHIR resources |
| Allergies | ✅ Covered | `AllergyIntolerance` (36 fields) | Good |
| Immunizations | ✅ Covered | `Immunization` (32 fields) | Good — SDK also has ImmunizationStatement model (11 fields) |
| Vitals | ✅ Covered | `Observation` (44 fields) | Good — covers vitals, labs, social history via Observation |
| Lab results | ✅ Covered | `Observation` (44), `DiagnosticReport` (36), `Specimen` (20) | Good — SDK has 8 lab models with 123 fields (LabOrder, LabReport, LabValue, etc.) that provide more granularity than FHIR mapping |
| Imaging / diagnostic reports | ✅ Covered | `DiagnosticReport` (36 fields) | Moderate — SDK has 3 imaging models with 48 fields (ImagingOrder, ImagingReport, ImagingReview) |
| Procedures | ✅ Covered | `Procedure` (26 fields) | Adequate |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (42), `Media` (34) | Good — SDK has Note (18 fields), NoteType (26 fields), UncategorizedClinicalDocument (18 fields) |
| Care plans / goals | ✅ Covered | `CarePlan` (28), `Goal` (35) | Good |
| Orders / referrals | ✅ Covered | `ServiceRequest` (33 fields) | Moderate — SDK has Referral (21 fields), ReferralReport (19), ReferralReview (13) with more tracking detail |
| Insurance / coverage | ✅ Covered | `Coverage` (48), `CoverageEligibilityResponse` (34) | Good — 82 fields total; SDK Coverage page has 93 fields across 5 models |
| Claims / billing | ⚠️ Partial | `Claim` (47 fields) | Product has deep billing: SDK has 12 claim models (210 fields) + 10 posting models (78 fields) = 288 fields. FHIR Claim captures claim structure but likely loses payment posting, remittance, adjustments, write-offs, transactor details |
| Payments | ⚠️ Partial | No dedicated payment resource | SDK has PaymentCollection, BasePosting, CoveragePosting, PatientPosting, BulkPatientPosting, NewLineItemPayment, NewLineItemAdjustment, LineItemTransfer — 78 fields across 10 models. These are likely flattened into Claim or lost |
| Consents / directives | ✅ Covered | `Consent` (29 fields) | Good — SDK has PatientConsent (9 fields) |
| Patient communications | ✅ Covered | `Communication` (26 fields) | Moderate — SDK also has Message, Letter, BannerAlert models |
| Questionnaires / custom forms | ✅ Covered | `QuestionnaireResponse` (37 fields) | Good — SDK has Questionnaire (19), Question (12), ResponseOption (11) models |
| Scheduling | ✅ Covered | `Appointment` (48 fields) | Good — beyond USCDI |
| Tasks | ✅ Covered | `Task` (42 fields) | Good — beyond USCDI |
| Detected issues (CDS) | ❌ Not covered | No DetectedIssue resource in export | SDK has DetectedIssue (18 fields), DetectedIssueEvidence (8 fields). Minor gap — protocol/CDS alerts |

## 6. Documentation Quality

**Strengths:**
- Every FHIR resource has a dedicated API documentation page with field-level detail
- 98.7% of fields have descriptions (1,055 of 1,069)
- Types are documented for all fields
- Value options/enums are specified for coded fields (e.g., status values, category codes)
- Canvas-specific extensions are documented (e.g., note-id extension on AllergyIntolerance, queue extension on Claim)
- The API pages include endpoint paths, HTTP methods, and operation summaries

**Weaknesses:**
- No sample export data files are provided
- No machine-readable schema (e.g., FHIR StructureDefinition or CapabilityStatement for the export)
- Relationships between resources are implicit (via `reference` fields) rather than explicitly documented in a relationship diagram
- The EHI export page itself is brief (~1 page); most documentation is in the generic FHIR API pages which serve double duty for both the API and the export
- Population export is described vaguely ("contact support") without technical details

**Could a developer build an import?** Largely yes — the FHIR R4 format is standard, and the API documentation provides sufficient field-level detail. However, Canvas-specific extensions would need careful handling, and the lack of sample data means a developer would need to experiment.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial (strong)**

Canvas's export covers 29 FHIR resources spanning clinical, financial, administrative, and communication domains. This goes meaningfully beyond USCDI — Claim, Appointment, Communication, Consent, CoverageEligibilityResponse, Media, MedicationStatement, and Task are all non-USCDI resources. The Claim resource with 47 fields demonstrates genuine billing coverage. However, the SDK reveals that Canvas internally stores 288 fields across 22 billing/payment models, while the FHIR export compresses this to a single 47-field Claim resource. Payment postings, remittance advices, line-item adjustments, write-offs, and transactor details — all present in the SDK — likely do not survive the FHIR mapping. Similarly, imaging detail (3 SDK models, 48 fields) is compressed into DiagnosticReport, and lab detail (8 models, 123 fields) into Observation/DiagnosticReport. The export covers ~60% of the internal data model's breadth meaningfully, which is strong for a FHIR-based export but not comprehensive.

**Axis 2 — Export approach: Purpose-built EHI export**

This is a purpose-built export, not a repackaged (g)(10) API. Evidence: (1) Canvas explicitly includes Claim, Coverage, CoverageEligibilityResponse, Appointment, Communication, Consent, and Task — none of which are required by (g)(10)/USCDI; (2) the export uses FHIR Bulk Data Access ($export) rather than pointing to their standard FHIR search API; (3) the EHI export page describes a dedicated workflow with its own UI and API endpoint; (4) 8 of 29 resources are non-USCDI, covering billing, scheduling, communications, and task management. The vendor has clearly built something purpose-specific for (b)(10), even though it reuses FHIR as the wire format.

### Key Findings

1. **Purpose-built with billing coverage**: Canvas includes Claim, Coverage, and CoverageEligibilityResponse in the EHI export — genuine billing data that goes well beyond USCDI. The Claim resource includes line items, diagnosis codes, NDC codes, insurance references, and charges. This is not a repackaged clinical exchange.

2. **SDK reveals deeper internal model**: Canvas's SDK documentation (134 models, 1,784 fields) shows the export compresses significant internal detail. Billing alone has 288 SDK fields mapped to 47 FHIR Claim fields. Payment posting/remittance (78 fields across 10 models) has no dedicated FHIR representation.

3. **Strong documentation quality**: 98.7% of exported fields have descriptions, types are documented throughout, and Canvas-specific extensions are explained. The FHIR API pages are detailed and usable.

4. **Bulk export requires vendor assistance**: While single-patient export is self-service (UI + API), population-level exports require contacting Canvas support. This is a practical barrier but not uncommon.

5. **No sample data provided**: The documentation lacks sample export files, making it harder for third parties to validate the export format without access to a Canvas instance.

### Summary Stats

    Coverage:        Partial (strong)
    Approach:        Purpose-built EHI export
    Export format:   FHIR R4 NDJSON (Bulk Data Access)
    Entities:        29 FHIR resources
    Fields:          1,069
    Descriptions:    98.7% of fields
    Sample data:     No
    Bulk export:     Yes (vendor-assisted for population; self-service for single patient)
    Domains covered: 18 of 20 applicable domains (partial on billing/payments; CDS alerts missing)

### Bottom Line

Canvas Medical has built a genuine EHI export that goes meaningfully beyond USCDI, including billing claims, insurance coverage, appointments, communications, tasks, and consents — 8 resource types not required by standard clinical exchange. The export is well-documented (98.7% field descriptions) and uses standard FHIR R4 NDJSON format. The primary gap is depth in billing/payments: the SDK reveals 288 internal billing fields compressed to 47 in the FHIR Claim resource, meaning payment postings, remittance advices, and line-item adjustments likely lose fidelity in the export.
