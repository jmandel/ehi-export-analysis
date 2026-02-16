# EHI Export Analysis: Canvas Medical, Inc.

**Product**: Canvas Medical
**Analysis date**: 2026-02-16
**CHPL IDs**: 10904 (15.04.04.3112.Canv.01.00.1.220523)

## 1. Product Context

Canvas Medical is a cloud-hosted, API-first EMR platform designed for outpatient/ambulatory specialty clinics and tech-enabled healthcare organizations. It was founded in 2015, certified in 2022, and won the 2026 Best in KLAS Ambulatory Specialty EHR award. The product serves 20+ healthcare organizations across multiple outpatient specialties including primary care, behavioral health, cardiology, weight management, psychiatry, and others.

The platform stores comprehensive ambulatory healthcare data spanning:

- **Clinical data**: Patient demographics, conditions/diagnoses, allergies, medications (including compound medications, medication history, stop events), immunizations, labs, imaging, observations/vitals, procedures, clinical notes/encounters, assessments, care plans, care teams, goals, detected issues, devices, questionnaires, and uncategorized clinical documents.
- **Billing/Financial data**: Claims, billing line items (CPT/charges linked to notes), charge description master, payor-specific charges, coverage/insurance, eligibility, and a rich payment posting subsystem (10 models covering payment collections, remittance advice, line item payments/adjustments/transfers, and discounts).
- **Communication**: Patient messages, letters, and portal interactions.
- **Orders/Referrals**: Medication prescribing (via Surescripts), lab ordering (via Health Gorilla), imaging orders, and referrals.
- **Administrative**: Appointments, scheduling, tasks, staff management.

Canvas exposes its internal data model through a Python SDK (51 data pages, 136 models, 1,811 fields) and a FHIR R4 API (40 resources). This transparency is unusual and enables rigorous gap analysis.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export.html` (21 KB) | Main EHI export documentation page listing 29 FHIR R4 resources and describing the export mechanism | **High** — primary source for export scope |
| `downloads/api-pages/*.html` (29 files, 5.2 MB total) | FHIR R4 API documentation for each of the 29 exported resource types, with field-level attribute definitions | **High** — detailed field documentation |
| `downloads/sdk-data-pages/data-*.html` (51 files, 2.2 MB total) | Canvas SDK internal data model documentation for 51 data pages covering 136 models | **High** — ground truth for internal data model, critical for gap analysis |
| `downloads/enrichment/fhir-api-resources.json` (1.1 MB) | Pre-extracted structured FHIR API definitions: 29 resources, 84 operations, 3,698 field entries | **High** — machine-readable parse of API pages |
| `downloads/enrichment/sdk-data-models.json` (257 KB) | Pre-extracted SDK data models: 51 pages, 136 models, 1,811 fields, 57 enums | **High** — machine-readable parse of SDK pages |
| `downloads/ehi-export-page-screenshot.png` (175 KB) | Full-page screenshot of the EHI export documentation page | Low — visual confirmation only |
| `downloads/fhir-service-base-urls-production.json` (62 KB) | FHIR R4 Bundle listing 94 production FHIR endpoint base URLs | Low — confirms active deployments |
| `downloads/enrichment/extract-fhir-api.ts` / `extract-sdk-models.ts` | Bun TypeScript extraction scripts used to generate the JSON files | Low — tooling only |

## 3. Export Mechanics

- **Format**: FHIR R4 resources in Newline Delimited JSON (NDJSON), following the FHIR Bulk Data Access (STU 1.0.1) specification.
- **Model type**: Standard-based projection (FHIR R4) with Canvas-specific extensions — not a native database dump.
- **Single-patient export (UI)**: Navigate to "FHIR Bulk Data Exports" in admin settings → "ADD FHIR BULK DATA EXPORT" → select OAuth application → search for patient → "Start Export." Downloads available as NDJSON files per resource type. Permission-based access.
- **Single-patient export (API)**: `GET https://fumage-{instance}.canvasmedical.com/Patient/{id}/$export`
- **Population/bulk export**: Requires contacting Canvas support with instance name, username, role, patient group, and purpose. Canvas staff initiates the export on the customer's behalf. This introduces friction for legitimate bulk EHI export requests.
- **Fees**: None documented.

## 4. Export Content: What's In It

### Export structure

The EHI export includes **29 FHIR R4 resource types** delivered as NDJSON files. The documentation page (`ehi-export.html`) states the export includes "the patient resource itself" and "any resource that is associated with the patient."

Across all 29 resources, after deduplicating fields that appear in multiple operations (POST, GET, PUT, Search), there are **1,131 unique fields**. Of these, **1,123 (99.3%) have text descriptions** and **905 have explicit type declarations**.

No sample export data is provided. No JSON Schema, OpenAPI spec, or machine-readable profile definitions accompany the documentation.

### Vendor's own content organization

Canvas organizes its export as 29 FHIR R4 resource types. The table below shows each resource with its field count (unique fields after deduplication across operations):

| Resource | Unique Fields | Described | Types | Category |
|---|---|---|---|---|
| Patient | 61 | 60 | yes | Demographics |
| Appointment | 53 | 50 | yes | Scheduling |
| Claim | 51 | 51 | yes | Billing |
| DocumentReference | 51 | 51 | yes | Clinical Notes/Documents |
| MedicationRequest | 49 | 49 | yes | Medications |
| Observation | 47 | 47 | yes | Vitals/Labs |
| Task | 46 | 46 | yes | Workflow |
| CoverageEligibilityResponse | 44 | 44 | yes | Insurance |
| Condition | 43 | 43 | yes | Problems/Diagnoses |
| Coverage | 42 | 42 | yes | Insurance |
| RelatedPerson | 42 | 41 | yes | Demographics |
| QuestionnaireResponse | 41 | 41 | yes | Clinical Forms |
| AllergyIntolerance | 40 | 40 | yes | Allergies |
| Encounter | 40 | 40 | yes | Encounters |
| MedicationStatement | 40 | 40 | yes | Medications |
| MedicationDispense | 38 | 38 | yes | Medications |
| DiagnosticReport | 36 | 36 | yes | Lab/Imaging Reports |
| Goal | 35 | 35 | yes | Care Plans |
| Immunization | 35 | 35 | yes | Immunizations |
| Device | 33 | 33 | yes | Devices |
| Media | 33 | 33 | yes | Images/Attachments |
| ServiceRequest | 33 | 33 | yes | Orders/Referrals |
| CareTeam | 32 | 32 | yes | Care Teams |
| Consent | 32 | 32 | yes | Consents |
| Provenance | 31 | 28 | yes | Data Tracking |
| Communication | 29 | 29 | yes | Messaging |
| CarePlan | 28 | 28 | yes | Care Plans |
| Procedure | 26 | 26 | yes | Procedures |
| Specimen | 20 | 20 | yes | Labs |
| **Total** | **1,131** | **1,123** | — | — |

The full entity inventory with all field details is at `analysis/full-entity-inventory.json`.

### Canvas-specific extensions

Canvas goes beyond standard FHIR R4. The API documentation shows Canvas-specific extensions on many resources — e.g., custom queue extensions on Claim, note-id extensions on AllergyIntolerance, social determinants extensions on Patient (housing, education, veteran status). These preserve some Canvas-internal semantics that wouldn't exist in vanilla FHIR. However, there's no documentation mapping which internal Canvas fields map to which FHIR fields or extensions, so it's unclear whether all internal data is preserved in the projection.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Canvas includes 29 FHIR R4 resource types in the EHI export. Compared to what (g)(10) / US Core STU3.1.1 would require, Canvas includes approximately **11 additional resource types** beyond the US Core baseline:

- **Billing/Insurance**: Claim, Coverage, CoverageEligibilityResponse — genuinely useful billing data not typically in FHIR clinical summaries
- **Communication**: Communication — patient messaging
- **Consent**: Consent — patient consent records
- **Media**: Media — images and attachments
- **Questionnaires**: QuestionnaireResponse — patient forms
- **Workflow**: Task, RelatedPerson, ServiceRequest, Specimen

This demonstrates Canvas gave genuine thought to (b)(10) scope rather than simply repackaging their (g)(10) API. However, the export is still a FHIR projection, and Canvas's internal data model (136 models, 1,811 fields across 51 SDK pages) is substantially richer than what 29 FHIR resource types can represent.

### 5b. Standardized domain coverage (top-down)

Using Canvas's SDK data model (51 pages, 136 internal models) as ground truth for what the product stores:

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (61 fields), `RelatedPerson` (42 fields) with Canvas extensions for social determinants | Thorough; internal Patient model has 7 sub-models/118 fields — some may compress in FHIR projection |
| Encounters / visits | ✅ Covered | `Encounter` (40 fields) | Internal Note model (4 models, 57 fields) is richer than FHIR Encounter; notes are Canvas's primary encounter container |
| Problems / conditions | ✅ Covered | `Condition` (43 fields) | Good coverage |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (49), `MedicationStatement` (40), `MedicationDispense` (38) | Covers main medication workflow. **Gap**: CompoundMedication (6 fields) and StopMedicationEvent (11 fields) have no clear FHIR mapping — unclear if captured |
| Allergies | ✅ Covered | `AllergyIntolerance` (40 fields) | Good coverage |
| Immunizations | ✅ Covered | `Immunization` (35 fields) | Good coverage |
| Vitals | ✅ Covered | `Observation` (47 fields) | Good coverage |
| Lab results | ✅ Covered | `DiagnosticReport` (36), `Observation` (47), `Specimen` (20) | Internal Labs model is complex (8 models, 123 fields) — FHIR may not capture all lab order/result detail |
| Imaging / diagnostic reports | ✅ Covered | `DiagnosticReport` (36), `Media` (33) | Internal Imaging model (3 models, 48 fields) may lose some detail in FHIR projection |
| Procedures | ✅ Covered | `Procedure` (26 fields) | Adequate |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (51), `Encounter` (40) | Internal Note model (57 fields) and UncategorizedClinicalDocument (31 fields) are projected into FHIR; fidelity depends on Canvas extensions |
| Care plans / goals | ✅ Covered | `CarePlan` (28), `Goal` (35) | Adequate |
| Orders / referrals | ✅ Covered | `ServiceRequest` (33 fields) | Internal Referral model (3 models, 53 fields) is richer — referral tracking detail may be lost |
| Insurance / coverage | ✅ Covered | `Coverage` (42), `CoverageEligibilityResponse` (44) | Internal Coverage model (5 models, 93 fields) is significantly richer; eligibility details may compress |
| Claims / billing | ⚠️ Partial | `Claim` (51 fields) | Canvas exports claims but **not billing line items** (2 models, 21 fields), **not payment postings** (10 models, 78 fields), **not charge description master** (9 fields), **not payor-specific charges** (7 fields). Total unmapped billing: 24 models, 115 fields. This is the single largest gap. |
| Payments | ❌ Not covered | No FHIR resource for payment postings | Canvas has 10 Posting models (78 fields) covering payment collections, remittance advice, line item payments, adjustments, transfers, and discounts. None of this maps to a FHIR resource in the export. |
| Consents / directives | ✅ Covered | `Consent` (32 fields) | Internal PatientConsent model (3 models, 26 fields) appears well-covered |
| Patient communications | ✅ Covered | `Communication` (29 fields) | Internal Message model maps to Communication. **Gap**: Letter model (8 fields) for patient correspondence has no clear FHIR mapping. |
| Assessments | ⚠️ Partial | May be partially in `Encounter` or `Condition` | Canvas stores Assessments as a distinct model (18 fields including narrative, ICD-10 codes, background, status). No dedicated FHIR resource — assessment narrative and structure may be lost in the FHIR projection. |
| Detected issues | ❌ Not covered | DetectedIssue **not listed** in the 29 EHI export resources, despite having its own FHIR API endpoint | Canvas has a DetectedIssue model (2 models, 26 fields) for clinical issues like drug interactions. The FHIR API supports DetectedIssue CRUD, but it's explicitly absent from the EHI export resource list. |
| Questionnaires / forms | ✅ Covered | `QuestionnaireResponse` (41 fields) | Good coverage of patient-completed forms |

**Domains covered**: 16 of 18 applicable standard domains (Claims/Billing partial, Payments not covered).

### Key coverage gaps

1. **Payment/posting data** (10 models, 78 fields): The most significant gap. Canvas has a sophisticated payment posting system with payment collections, remittance advice, line item payments, adjustments, transfers, and discounts — none of which maps to a FHIR resource in the export. This is patient-level financial data used for billing decisions.

2. **Billing line items** (2 models, 21 fields): CPT codes, charges, units, and modifiers linked to clinical notes. While Claim captures some billing data, the granular billing line item detail that connects charges to specific note content is not in the export.

3. **DetectedIssue** (2 models, 26 fields): Drug interactions and clinical contraindications — clinically relevant patient data. Notably, Canvas has a DetectedIssue FHIR API endpoint but chose not to include it in the EHI export resource list.

4. **Assessments** (1 model, 18 fields): Clinical assessments with narrative content, ICD-10 codes, and status information. May be partially captured in Encounter or Condition resources, but the assessment-specific structure (narrative, background) is likely lost.

5. **Minor gaps**: CompoundMedication (6 fields), StopMedicationEvent (11 fields), Letter (8 fields), ReasonForVisit (7 fields) — smaller models that may be partially captured in related FHIR resources but lack explicit mapping.

## 6. Documentation Quality

**Strengths:**
- Each of the 29 FHIR resource API pages has rich field-level documentation: 1,123 of 1,131 unique fields (99.3%) have text descriptions.
- Fields include types, required/optional markers, value set options for coded fields, and documentation of Canvas-specific extensions.
- The Canvas SDK documentation provides unusual transparency into the internal data model (136 models, 1,811 fields), enabling rigorous gap analysis that most vendors make impossible.
- The EHI export page is clear and straightforward about the mechanism and scope.

**Weaknesses:**
- **No sample export data**: There are no example NDJSON files showing what an actual patient export looks like. A developer would have to rely solely on the API documentation.
- **No FHIR-to-internal mapping**: No documentation explains how Canvas's 136 internal models map to the 29 FHIR resources. Which internal fields become FHIR extensions? Which are dropped? This is the critical question for assessing export completeness, and it's unanswered.
- **SDK model fields lack descriptions**: While the FHIR API documentation has excellent field descriptions, the SDK internal model fields (1,811 total) have names and types only — zero descriptions. This limits the ability to assess exactly what data is lost in the FHIR projection.
- **No machine-readable schemas**: No JSON Schema, OpenAPI spec, or FHIR StructureDefinition profiles are provided. The HTML API documentation is the only artifact.
- **No explicit (b)(10) framing**: The export page doesn't mention the regulatory basis, doesn't explain how the 29 resources were selected, and doesn't address whether the export captures "all EHI."
- **Population export requires support contact**: Adding friction to legitimate bulk EHI requests.

**Verdict**: A competent developer could build a FHIR-based import from this documentation, but would have no way to verify whether the export actually contains all of a patient's data. The gap between what Canvas stores (136 models) and what it exports (29 FHIR resources) is documented only because Canvas publishes its SDK data model — not because the EHI export documentation itself addresses completeness.

## 7. Overall Assessment

### Classification

**Standard-based projection** — The export is the vendor's FHIR Bulk Data API with an expanded resource set beyond US Core. It includes ~11 resource types beyond (g)(10) requirements (notably Claim, Coverage, and Communication), showing genuine effort to broaden scope. However, it remains a FHIR R4 projection of a richer native data model, and significant internal data domains (payment postings, billing line items, assessments, detected issues) have no FHIR mapping and are absent from the export.

### Key Findings

1. **The export is a FHIR Bulk Data projection, not a native data model export.** Canvas exports 29 FHIR R4 resource types in NDJSON format. While this goes meaningfully beyond US Core / (g)(10), the internal data model has 136 models across 51 domains — the FHIR projection inherently cannot represent all of this.

2. **Payment/posting data is the single largest gap.** Canvas has a sophisticated 10-model payment posting subsystem (78 fields) covering payment collections, remittance advice, line item payments/adjustments/transfers, and discounts. None of this appears in the export. This is patient-level billing data.

3. **Documentation quality is strong for the FHIR layer.** 99.3% of the 1,131 unique exported fields have text descriptions. Canvas-specific extensions preserve some internal semantics. But there's no mapping between internal models and FHIR output, so completeness is unknowable from the documentation alone.

4. **Canvas's SDK transparency enables gap analysis that most vendors prevent.** The 51 SDK data model pages with 136 models and 1,811 fields provide ground truth for what Canvas stores internally. This makes the gap between "what's stored" and "what's exported" measurable: ~21 EHI-relevant internal models (191 fields) have no FHIR export mapping.

5. **DetectedIssue is a notable omission.** Canvas has both an internal DetectedIssue model and a FHIR DetectedIssue API endpoint, yet explicitly excluded it from the 29 EHI export resources. Drug interactions and clinical contraindications are clearly EHI.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 NDJSON (Bulk Data Access)
Model type:      Standard projection (FHIR R4 with Canvas extensions)
Entities:        29 FHIR resource types
Fields:          1,131 unique fields (3,698 total across all operations)
Descriptions:    99.3% of fields have descriptions
Sample data:     No
Bulk export:     Yes (vendor-assisted; single-patient available via UI/API)
Domains covered: 16 of 18 applicable standard domains
```

### Bottom Line

Canvas Medical's EHI export is a thoughtful FHIR-based implementation that goes meaningfully beyond a (g)(10) repackaging — it includes billing claims, insurance coverage, communications, and questionnaire data that many vendors omit. However, it remains a FHIR projection of a substantially richer internal data model (29 FHIR resources vs. 136 internal models), and the most significant gap is the complete absence of payment/posting data (10 models, 78 fields) — patient-level financial records that are clearly part of the designated record set. A patient would get most of their clinical data but would be missing granular billing and payment details.
