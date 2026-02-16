# EHI Export Analysis: athenahealth, Inc.

**Products**: athenaPractice (v25), athenaFlow (v25)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2880.prac.25.07.1.250428 (athenaPractice), 15.04.04.2880.flow.25.08.1.250711 (athenaFlow)

## 1. Product Context

athenaPractice and athenaFlow are legacy ambulatory EHR/PM products originally from GE Healthcare (Centricity Practice Solution and Centricity EMR, respectively), acquired by athenahealth via the Veritas/Virence transaction. Both are Windows-based client-server applications, distinct from athenahealth's cloud-native athenaOne platform.

**athenaPractice** is a fully integrated EHR + Practice Management system supporting:
- **Clinical**: charting, problem lists, medications, allergies, immunizations, CPOE, lab ordering/results, imaging, procedures, family history, clinical impressions, care plans, goals, consent management, device tracking, clinical notes/documents, media/images, e-prescribing
- **Practice Management**: scheduling, patient registration, insurance/coverage management, patient accounting (charges, payments, adjustments, collections), billing statements, claims submission, eligibility verification, deductible tracking, revenue cycle management
- **Patient Engagement**: patient portal, secure messaging
- **Interoperability**: FHIR R4 API, C-CDA, Direct messaging, public health reporting

**athenaFlow** shares the clinical capabilities but lacks scheduling (Schedule/Slot) and all 9 custom financial/billing resource types — making its EHI export significantly narrower.

A (b)(10) export for athenaPractice should cover clinical records, billing/financial data, insurance, scheduling, and patient communications. For athenaFlow, clinical and basic administrative data are the baseline.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/site/ehiexport.html` (25 KB) | EHI Export main page — lists all resource types by product and category | **High** — primary documentation of export scope |
| `downloads/site/operations.html` (11 KB) | FHIR operations — confirms Group/$export endpoint | **Medium** — confirms export mechanism |
| `downloads/site/index.html` (23 KB) | IG home page with supported resource table | Medium |
| `downloads/site/artifacts.html` (84 KB) | Full artifact index (profiles, extensions, examples, value sets) | Medium |
| `downloads/site/definitions.json.zip` (1.3 MB) | 121 JSON files: 54 profiles, 56 extensions, CapabilityStatements, etc. | **High** — machine-readable schemas for all resources |
| `downloads/site/examples.json.zip` (2.0 MB) | 220 JSON example instances | **High** — demonstrates actual data content |
| `downloads/definitions/` (121 files) | Extracted StructureDefinition profiles and extensions | **High** — field-level documentation |
| `downloads/examples/` (220 files) | Extracted example resource instances (100 clinical/admin examples) | **High** — shows data depth |
| `downloads/profiles/` (43 HTML files) | Profile HTML pages with human-readable field documentation | Medium |
| `downloads/enrichment/profiles-catalog.json` | Pre-parsed profile summary (259 KB) | Medium — used for orientation |
| `downloads/enrichment/coverage-accounting.json` | Category breakdown of profiles | Medium |

All artifacts were accessible and well-structured. The IG is built with standard HL7 FHIR IG Publisher tooling (v25.0.0, generated 2025-04-10).

## 3. Export Mechanics

- **Format**: FHIR R4 resources as Newline Delimited JSON (NDJSON), per the FHIR Bulk Data Access specification. Includes both standard FHIR resources and custom (non-standard) FHIR-like resources for financial data.
- **Mechanism**: FHIR Bulk Data `Group/$export` operation. The CapabilityStatement confirms a Group resource type with export capability. Patient-level `$everything` and Encounter-level `$everything` operations are also available.
- **Single-patient vs bulk**: Both supported — `Patient/$everything` for single-patient, `Group/$export` for bulk.
- **Access constraints**: SMART on FHIR / OAuth 2.0 authentication required. No evidence of fees or vendor-assisted processes mentioned.

## 4. Export Content: What's In It

### Data dictionary scope

The export is documented through a full FHIR Implementation Guide containing **54 StructureDefinition profiles** (resource schemas). Of these, **42 are included in the athenaPractice EHI export** and **30 in the athenaFlow EHI export**.

Across the 42 athenaPractice EHI profiles:
- **3,641 total fields** (snapshot elements)
- **3,512 fields with descriptions** (96.5% description rate)
- **1,731 differential elements** (vendor-constrained/customized)
- **56 custom extensions** adding vendor-specific data points
- **Types documented**: Yes, for all fields
- **Value set bindings**: 53 of 54 profiles have coded element bindings
- **Relationships**: Foreign keys via FHIR References (e.g., Charge.patient → Patient, Charge.doctor → Practitioner)

### Vendor's own content organization

The EHI export page organizes resources into four categories:

**System Resources (5 in EHI, 501 fields)**

| Entity | Resource Type | Fields | Described | Category |
|---|---|---|---|---|
| Location | Location | 94 | 93 | System |
| Medication | Medication | 95 | 95 | System |
| Organization | Organization | 121 | 121 | System |
| Practitioner | Practitioner | 87 | 83 | System |
| PractitionerRole | PractitionerRole | 104 | 104 | System |

**Clinical Resources (21 in EHI, 1,937 fields)**

| Entity | Resource Type | Fields | Described | Category |
|---|---|---|---|---|
| AllergyIntolerance | AllergyIntolerance | 198 | 197 | Clinical |
| Binary | Binary | 16 | 16 | Clinical |
| CarePlan | CarePlan | 81 | 81 | Clinical |
| CareTeam | CareTeam | 70 | 70 | Clinical |
| ClinicalImpression | ClinicalImpression | 73 | 73 | Clinical |
| Condition | Condition | 88 | 88 | Clinical |
| Consent | Consent | 87 | 84 | Clinical |
| Device | Device | 84 | 82 | Clinical |
| DiagnosticReport | DiagnosticReport | 59 | 59 | Clinical |
| DocumentReference | DocumentReference | 99 | 96 | Clinical |
| Encounter | Encounter | 126 | 122 | Clinical |
| FamilyMemberHistory | FamilyMemberHistory | 63 | 63 | Clinical |
| Goal | Goal | 50 | 50 | Clinical |
| Immunization | Immunization | 110 | 108 | Clinical |
| MedicationAdministration | MedicationAdministration | 69 | 65 | Clinical |
| MedicationRequest | MedicationRequest | 134 | 128 | Clinical |
| MedicationStatement | MedicationStatement | 80 | 76 | Clinical |
| Observation | Observation | 193 | 190 | Clinical |
| Procedure | Procedure | 82 | 82 | Clinical |
| Provenance | Provenance | 98 | 98 | Clinical |
| ServiceRequest | ServiceRequest | 77 | 77 | Clinical |

**Practice Management Resources (7 in EHI, 697 fields)**

| Entity | Resource Type | Fields | Described | Category |
|---|---|---|---|---|
| Account | Account | 83 | 70 | Practice Management |
| Appointment | Appointment | 101 | 98 | Practice Management |
| Coverage | Coverage | 74 | 72 | Practice Management |
| Patient | Patient | 279 | 259 | Practice Management |
| RelatedPerson | RelatedPerson | 102 | 98 | Practice Management |
| Schedule | Schedule | 25 | 25 | Practice Management |
| Slot | Slot | 33 | 32 | Practice Management |

**Custom Financial/PM Resources (9 in EHI, 506 fields — athenaPractice only)**

| Entity | Resource Type | Fields | Described | Category |
|---|---|---|---|---|
| Adjustment | Custom | 40 | 35 | Custom (Financial/PM) |
| BillingStatement | Custom | 21 | 20 | Custom (Financial/PM) |
| Charge | Custom | 106 | 95 | Custom (Financial/PM) |
| Claim | Custom | 40 | 31 | Custom (Financial/PM) |
| Collection | Custom | 78 | 69 | Custom (Financial/PM) |
| Deductible | Custom | 40 | 37 | Custom (Financial/PM) |
| Eligibility | Custom | 86 | 83 | Custom (Financial/PM) |
| PatientInsurance | Custom | 46 | 43 | Custom (Financial/PM) |
| Payment | Custom | 49 | 44 | Custom (Financial/PM) |

The full inventory (all 54 profiles, 4,270 fields) is in `analysis/entity-inventory-full.json`. The summary statistics are in `analysis/entity-inventory-summary.json`.

### Notable depth examples

The **Charge** custom resource (106 fields, 69 differential elements) includes: CPT codes, modifiers (1-4), fee/allowed amounts with currency, RVU values, place/type of service, authorization numbers, referral information, rendering/supervising/referring/ordering providers, diagnosis pointers, and revenue codes. This is genuine billing line-item detail — not a summary.

The **Patient** profile (279 fields, 146 differential elements) includes 14 custom extensions beyond US Core: guarantor details, patient-as-guarantor flag, responsible provider, referring doctor, occupation, occupation industry, gender identity, sexual orientation, pronouns, tribal affiliation, preferred contact method, and US Core sex.

The **Observation** profile (193 fields, 108 differential elements) covers vitals, lab results, social determinants, disability status, clinical observations, and specimen-linked results — all via a single resource type differentiated by `Observation.category`.

### Example data

The IG includes 100 clinical/administrative example resource instances (excluding StructureDefinitions and system artifacts). Examples cover all standard FHIR resource types in the EHI export. However, **no example instances exist for the 9 custom financial resources** (Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment). There is a Posting example (Basic resource) that demonstrates financial data (batch, amounts, payer info).

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor organizes the EHI export into four tiers:

1. **Clinical (21 resources, 1,937 fields)**: The deepest category. Covers the full breadth of ambulatory clinical documentation — problems, medications (requests, statements, administration), allergies (198 fields — the most granular clinical resource), immunizations, labs/vitals (via Observation), diagnostic reports, clinical notes/documents (DocumentReference + Binary), procedures, care plans, goals, clinical impressions, consent, devices, family history, service requests/orders, and provenance. Each resource uses athena-specific profiles with vendor extensions beyond US Core.

2. **Custom Financial/PM (9 resources, 506 fields — athenaPractice only)**: This is the strongest signal of a purpose-built (b)(10) export. These 9 custom resource types (Adjustment, BillingStatement, Charge, Claim, Collection, Deductible, Eligibility, PatientInsurance, Payment) map directly to the product's internal billing/PM data model, not to any standard FHIR clinical exchange format. The Charge resource alone has 106 fields with CPT codes, modifiers, fees, RVUs, authorization numbers, and provider chains. The Collection resource (78 fields) tracks debt collection workflows. The Eligibility resource (86 fields) captures insurance eligibility verification responses.

3. **Practice Management (7 resources, 697 fields)**: Patient demographics (279 fields with 14 extensions), coverage/insurance, appointments, scheduling (Schedule/Slot — athenaPractice only), related persons, and financial accounts.

4. **System (5 resources, 501 fields)**: Reference data — locations, medications, organizations, practitioners, and practitioner roles. These support cross-referencing in clinical and financial records.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (279 fields, 14 extensions), `RelatedPerson` (102 fields) | Exceptionally thorough — includes guarantor, occupation, tribal affiliation, pronouns |
| Encounters / visits | ✅ Covered | `Encounter` (126 fields), `Account` (83 fields with visit-level detail) | Visit-level clinical and financial data linked |
| Problems / conditions | ✅ Covered | `Condition` (88 fields) with onset, verification, linked orders | Deep |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (134 fields), `MedicationStatement` (80), `MedicationAdministration` (69), `Medication` (95) | Very thorough — includes DDIDs, NDCs, RxNorm, dispense instructions |
| Allergies | ✅ Covered | `AllergyIntolerance` (198 fields — largest clinical resource) | Exceptionally detailed |
| Immunizations | ✅ Covered | `Immunization` (110 fields) with VFC eligibility extension | Thorough |
| Vitals | ✅ Covered | `Observation` (193 fields, category=vital-signs) | Via category filtering |
| Lab results | ✅ Covered | `Observation` (category=laboratory), `DiagnosticReport` (59 fields), `Specimen` (66 fields — in API but not in EHI export list) | Good, though Specimen not explicitly in EHI list |
| Imaging / diagnostic reports | ✅ Covered | `DiagnosticReport` (59 fields), `Media` (in API, not in EHI list) | Imaging reports covered; Media (images) profiled but not listed in EHI export |
| Procedures | ✅ Covered | `Procedure` (82 fields) | Thorough |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (99 fields), `Binary` (16 fields for attachments) | Full document management including scanned/uploaded documents |
| Care plans / goals | ✅ Covered | `CarePlan` (81 fields), `Goal` (50 fields), `CareTeam` (70 fields) | Thorough |
| Orders / referrals | ✅ Covered | `ServiceRequest` (77 fields) categorized as service/referral/test | Covers lab orders, imaging orders, referrals, consultations |
| Insurance / coverage | ✅ Covered | `Coverage` (74 fields), `PatientInsurance` (46 fields, custom), `Eligibility` (86 fields, custom) | Deep — includes eligibility verification responses |
| Claims / billing | ✅ Covered | `Charge` (106 fields, custom), `Claim` (40 fields, custom) | Deep line-item billing detail (athenaPractice only) |
| Payments | ✅ Covered | `Payment` (49 fields, custom), `Adjustment` (40 fields, custom), `Deductible` (40 fields, custom), `Collection` (78 fields, custom), `BillingStatement` (21 fields, custom), `Posting` (Basic resource) | Comprehensive revenue cycle (athenaPractice only) |
| Consents / directives | ✅ Covered | `Consent` (87 fields) | Covered |
| Patient communications | ⚠️ Partial | No dedicated messaging/communications resource. Portal messages may be captured via `DocumentReference`. | Product has patient portal and secure messaging; no dedicated communications entity in export |
| Clinical assessments | ✅ Covered | `ClinicalImpression` (73 fields), `Observation` for SDOH/health status | Covered |

**Gap Analysis Summary**: For athenaPractice, 18 of 19 applicable domains are covered, with patient communications as the only notable gap. For athenaFlow, the 9 custom financial/billing resources and Account/Schedule/Slot are excluded — meaning Claims/Billing, Payments, and some Insurance/Coverage depth are missing from athenaFlow's export.

## 6. Documentation Quality

**Strengths**:
- Full FHIR Implementation Guide with machine-readable StructureDefinitions for every resource type
- 96.5% of fields have descriptions beyond just a name
- 56 custom extensions with definitions, each specifying context (which resource they apply to) and data type
- Value set bindings on 53 of 54 profiles — coded fields reference specific terminologies
- 220 example resource instances demonstrating actual data content
- CapabilityStatement documenting supported interactions and operations
- Cross-resource references documented (e.g., Charge.patient → Patient, Charge.doctor → Practitioner)

**Weaknesses**:
- No example instances for the 9 custom financial resources (StructureDefinitions exist but no sample data)
- Custom resources use URL-based type identifiers rather than simple names, making programmatic parsing slightly harder
- No explicit documentation of the export's completeness claim — the page states "EHI export" but doesn't explicitly discuss what's included vs excluded relative to the full database
- No sample NDJSON output files showing actual bulk export results

**Developer usability**: A developer could build an import from this documentation. The StructureDefinitions provide field-level schemas with types, cardinality, and descriptions. The FHIR-based format means standard FHIR parsers can handle the standard resources. Custom resources would require custom parsing but their schemas are fully documented. The main challenge would be the 9 custom financial resource types which lack examples — a developer would need to infer data patterns from the StructureDefinitions alone.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains athenaPractice stores. The 42 resource types in the athenaPractice EHI export span clinical records (21 resources), practice management (7 resources), system reference data (5 resources), and custom financial/PM data (9 resources). The inclusion of 9 custom financial resource types — Charge (106 fields), Collection (78 fields), Eligibility (86 fields), Payment (49 fields), Adjustment (40 fields), Claim (40 fields), Deductible (40 fields), PatientInsurance (46 fields), and BillingStatement (21 fields) — goes well beyond USCDI and demonstrates genuine engagement with the designated record set. The only notable gap is patient communications/portal messages, which may be partially captured via DocumentReference.

For athenaFlow, the export is narrower (30 resources, no billing/financial data), which could be classified as Partial — but this appears to reflect the product's actual scope (athenaFlow historically lacked PM/billing functionality), so it's appropriately scoped rather than artificially limited.

**Axis 2 — Export approach: Purpose-built EHI export**

Multiple signals indicate this is a purpose-built export, not a repackaged clinical exchange:

1. **9 custom financial resource types** that have no equivalent in USCDI, US Core, or any standard FHIR clinical exchange. These resources (Charge, Claim, Payment, Adjustment, Collection, Deductible, Eligibility, PatientInsurance, BillingStatement) are custom FHIR logical models mapping the product's internal billing data — something that would never appear in a (g)(10) FHIR Bulk Data export.

2. **Dedicated EHI export page** with explicit resource listing per product (athenaPractice vs athenaFlow), separate from the general API documentation.

3. **Profiles are athena-specific**, not US Core. While they build on base FHIR, they include vendor-specific extensions (56 total) and constraints beyond what the (g)(10) API would require.

4. **Account resource with billing extensions** (billStatus, companyId, facilityId, financialClassMid, patientVisitId, visitDate) — operational billing context not present in clinical exchange.

5. **Group/$export mechanism** — while FHIR Bulk Data is also used for (g)(10), the resource types exported here include the custom financial resources that would not be in a (g)(10) scope.

### Key Findings

1. **Genuinely comprehensive billing data**: The 9 custom financial resources with 506 total fields represent one of the deepest billing/financial data exports seen in a FHIR-based EHI export. The Charge resource alone (106 fields) includes CPT codes, 4 modifier slots, fee/allowed/RVU amounts, authorization numbers, place/type of service, and a full provider chain (rendering, supervising, referring, ordering).

2. **High documentation quality**: 96.5% field description rate across 3,641 fields, with machine-readable StructureDefinitions, 56 custom extensions, and value set bindings on 53/54 profiles. This is a genuinely usable data dictionary.

3. **Product-appropriate scoping**: The differentiation between athenaPractice (42 resources with billing) and athenaFlow (30 resources without billing) reflects the actual product capabilities, not artificial limitation.

4. **Missing example data for financial resources**: Despite thorough StructureDefinitions, none of the 9 custom financial resources have example instances — only the Posting (Basic) resource demonstrates financial data patterns. This is a documentation gap, not a coverage gap.

5. **Patient communications gap**: The product supports patient portal and secure messaging, but no dedicated communications resource appears in the EHI export. Portal messages may be captured via DocumentReference but this is not explicitly documented.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   FHIR R4 NDJSON (standard + custom resources)
Entities:        42 (athenaPractice), 30 (athenaFlow)
Fields:          3,641 (athenaPractice EHI scope)
Descriptions:    96.5% of fields
Sample data:     Yes (100 examples, but none for custom financial resources)
Bulk export:     Yes (Group/$export)
Domains covered: 18 of 19 applicable domains (athenaPractice)
```

### Bottom Line

athenaPractice's EHI export is one of the stronger implementations among certified EHR products. The purpose-built inclusion of 9 custom financial resource types (506 fields covering charges, claims, payments, adjustments, collections, deductibles, eligibility, insurance, and billing statements) alongside 21 clinical resources demonstrates genuine engagement with (b)(10)'s "all EHI" mandate. The main gap is patient portal communications, and the athenaFlow variant is significantly narrower due to the absence of all financial resources.
