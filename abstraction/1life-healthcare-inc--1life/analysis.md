# EHI Export Analysis: 1Life Healthcare, Inc

**Product**: 1Life (One Medical)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.05.05.3121.ONEL.01.00.1.220823

## 1. Product Context

1Life is One Medical's proprietary, purpose-built EHR platform powering all of One Medical's clinical, administrative, and patient-facing operations. One Medical (acquired by Amazon in 2023) is a membership-based primary care practice operating 125+ offices across 19+ U.S. cities. The product was built from scratch on AWS using Rails, React, and GraphQL — it is not a third-party EHR.

**Key data domains the product stores** (per product research and feature descriptions):

- **Clinical charting**: encounter notes, problem lists, medication lists, allergies, immunizations, vitals, lab orders/results, family health history, implantable devices
- **Prescriptions**: electronic prescribing via SureScripts integration
- **Scheduling**: appointment booking, same-day/next-day availability, virtual vs. in-person visits
- **Patient messaging**: secure patient-provider messaging, provider-to-provider internal messaging, administrative messages
- **Virtual care**: video visit records, on-demand "Treat Me Now" sessions, photo attachments
- **Patient portal**: prescription renewals, referral requests, health screening questionnaires
- **Referrals & care coordination**: specialist referrals, transitions of care (C-CDA)
- **Chronic care management**: care plans, coaching, care navigator notes
- **Billing & insurance**: insurance verification, claims billing (accepts major carriers + Medicare), membership management
- **Consent**: Terms of Service tracking (documented via custom FHIR Consent resource)
- **Communications**: After Visit Summaries, Treat Me Now threads (documented via custom Communication resource)

This establishes the baseline for assessing export completeness.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-overview.html` (37 KB) | Core EHI export page — lists 17 FHIR resource types and 18 C-CDA sections in the export | **High** — primary source for export scope |
| `downloads/fhir/resources/*.html` (22 files, 40-90 KB each) | Field-level FHIR resource documentation with types, cardinality, and descriptions | **High** — detailed field inventory |
| `downloads/fhir/extensions.html` (70 KB) | 11 FHIR extensions including US Core Race/Ethnicity and ML model extensions | **Medium** — shows custom extensions |
| `downloads/fhir/terminology.html` (39 KB) | Custom terminology codes (TOS consent, TMN/AVS communications) | **Medium** — confirms custom data types |
| `downloads/ccda/patient-continuity-of-care-document.html` (37 KB) | C-CDA API endpoint, parameters, 15 sections with date range applicability | **Medium** — defines C-CDA component |
| `downloads/fhir/overview.html` (37 KB) | FHIR API overview — schema, root URLs, media types | **Low** — general API info |
| `downloads/fhir/authentication.html` (40 KB) | FHIR API authentication docs | **Low** — operational detail |
| `downloads/fhir/search-and-output.html` (43 KB) | FHIR search parameters and output formatting | **Low** — API usage detail |
| `downloads/fhir/pagination.html` (41 KB) | Sorting and pagination docs | **Low** — API usage detail |
| `downloads/fhir/capability-statement.html` (33 KB) | CapabilityStatement endpoint docs | **Low** — API metadata |
| `downloads/homepage.html` (30 KB) | One Medical API Documentation homepage | **Low** — navigation only |
| `downloads/screenshot-ehi-export-overview.png` (266 KB) | Screenshot of EHI export page | **Low** — visual confirmation |

No sample data files, no data dictionaries beyond FHIR resource pages, no ZIP file examples, no schemas beyond standard FHIR.

## 3. Export Mechanics

- **Format**: ZIP file containing two files:
  - `.json` — FHIR R4 Bundle with all resources for the patient
  - `.xml` — C-CDA 2.1 Continuity of Care Document (CCD)
- **Mechanism**: API-based. The FHIR API is at `api.prod.1life.com/fhir/4.0`; the C-CDA API is at `production.app.1life.com/api/ccda`. Both require registration and authentication (FHIR: OAuth2; C-CDA: Basic Auth).
- **Single-patient and bulk**: The EHI overview states the export "contains the electronic health information available for a single patient or multiple patients." The FHIR API supports both single-patient and Bulk Data export (per (g)(10) certification).
- **Access constraints**: Registration required; 1Life reviews and approves API access requests.
- **Fees**: Not mentioned in documentation.

## 4. Export Content: What's In It

### FHIR JSON Component

The EHI export overview lists **17 FHIR resource types** (16 unique after deduplicating — "Condition" appears twice, likely a typo):

1. AllergyIntolerance
2. CareTeam
3. Communication
4. Condition
5. Consent
6. Device
7. DiagnosticReport (listed as "Diagnostic Report" with space)
8. DocumentReference
9. Encounter
10. Goal
11. Immunization
12. MedicationRequest
13. Observation
14. Patient
15. Procedure
16. ServiceRequest

The FHIR API documentation provides detailed field-level documentation for **22 resource types** (a superset including CarePlan, Coverage, Location, Medication, Organization, Practitioner, Provenance, Questionnaire, QuestionnaireResponse that are not listed in the EHI export). However, these additional resources are part of the general FHIR API — not explicitly part of the EHI export package.

**Three resource types listed in the EHI export lack dedicated documentation pages**: Communication, Consent, and Goal. These are referenced in custom terminology (Communication for TMN/AVS; Consent for TOS) but have no field-level documentation.

### Field-Level Documentation (22 documented FHIR resources)

Across all 22 documented FHIR resources: **629 total fields, 628 with descriptions (99.8%)**. Documentation quality is high — each field includes name, type, cardinality, and description.

### Vendor's own content organization

The vendor organizes all content as standard FHIR R4 resources. There is no vendor-specific categorization beyond the FHIR resource type names.

| Resource Type | Fields | Described | Types | In EHI Export? |
|---|---|---|---|---|
| AllergyIntolerance | 27 | 27 | Yes | ✅ |
| CarePlan | 24 | 24 | Yes | ❌ (API only) |
| CareTeam | 26 | 26 | Yes | ✅ |
| Condition | 23 | 23 | Yes | ✅ |
| Coverage | 31 | 31 | Yes | ❌ (API only) |
| Device | 12 | 12 | Yes | ✅ |
| DiagnosticReport | 35 | 35 | Yes | ✅ |
| DocumentReference | 42 | 42 | Yes | ✅ |
| Encounter | 33 | 33 | Yes | ✅ |
| Immunization | 36 | 36 | Yes | ✅ |
| Location | 26 | 26 | Yes | ❌ (API only) |
| Medication | 13 | 13 | Yes | ❌ (API only) |
| MedicationRequest | 21 | 21 | Yes | ✅ |
| Observation | 48 | 47 | Yes | ✅ |
| Organization | 18 | 18 | Yes | ❌ (API only) |
| Patient | 60 | 60 | Yes | ✅ |
| Practitioner | 19 | 19 | Yes | ❌ (API only) |
| Procedure | 34 | 34 | Yes | ✅ |
| Provenance | 17 | 17 | Yes | ❌ (API only) |
| Questionnaire | 31 | 31 | Yes | ❌ (API only) |
| QuestionnaireResponse | 23 | 23 | Yes | ❌ (API only) |
| ServiceRequest | 30 | 30 | Yes | ✅ |
| Communication | — | — | — | ✅ (no doc page) |
| Consent | — | — | — | ✅ (no doc page) |
| Goal | — | — | — | ✅ (no doc page) |

### C-CDA XML Component

The C-CDA component contains a standard CCD with **18 sections**:

Allergies, Assessment and Plan, Care Team, Encounters, Family History, Goals, Health Concerns, Immunizations, Medical Equipment, Medications, Notes, Patient, Plan of Treatment, Problems, Procedures, Results, Social History, Vital Signs.

These are standard C-CDA 2.1 sections with no vendor-specific extensions documented. The C-CDA API documentation provides no field-level detail beyond listing section names and whether date range filtering applies.

### Custom Extensions

One Medical defines several custom FHIR extensions:
- **US Core Race/Ethnicity** (on Patient): standard US Core extensions
- **Machine Learning extensions** (on Observation, Procedure): 7 extensions tracking ML-generated data (source type, model name, repository, type, use case, performance, prediction characteristics)
- **First Party Data** (on Procedure): marks resources from One Medical vs. external sources

### Custom Terminology

Three custom codes under `http://onemedical.com/terminology`:
- `TOS` on Consent: Terms of Service consent forms
- `TMN` on Communication: Treat Me Now secure message threads
- `AVS` on Communication: After Visit Summary communications

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export presents data in two parallel formats — FHIR R4 JSON and C-CDA 2.1 XML — covering the same clinical domains. The FHIR component lists 16 unique resource types; the C-CDA component lists 18 standard sections.

The resource types align closely with USCDI v3 requirements and US Core profiles:
- **Standard clinical resources**: AllergyIntolerance, Condition, Encounter, Immunization, MedicationRequest, Observation (vitals, labs, social history), Procedure, DiagnosticReport, DocumentReference
- **Care planning**: CareTeam, Goal (no doc page), ServiceRequest
- **Patient identity**: Patient (60 fields — the richest resource documented)
- **Device**: Device (implantable devices)
- **Custom One Medical resources**: Communication (TMN/AVS — secure messages and after-visit summaries), Consent (TOS)

Communication and Consent are the only resources that go beyond standard USCDI exchange. These capture One Medical-specific workflows (secure messaging, consent tracking) and use custom terminology codes, suggesting some purpose-built effort.

However, several resource types available in the FHIR API are **not included in the EHI export**:
- Coverage (insurance)
- CarePlan
- Questionnaire / QuestionnaireResponse (intake forms, screening questionnaires)
- Provenance
- Medication (standalone med resources)
- Organization, Location, Practitioner (reference resources)

The exclusion of Coverage and QuestionnaireResponse from the EHI export is notable — these capture insurance information and patient-reported data that are part of the designated record set.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (60 fields), US Core Race/Ethnicity extensions | Thorough for standard demographics |
| Encounters / visits | ✅ Covered | Encounter (33 fields), C-CDA Encounters section | Standard encounter data; no distinction between in-person, virtual, or Treat Me Now visits |
| Problems / conditions | ✅ Covered | Condition (23 fields), C-CDA Problems/Health Concerns sections | Standard |
| Medications / prescriptions | ✅ Covered | MedicationRequest (21 fields), C-CDA Medications section | Covers prescriptions; Medication reference resource excluded from EHI export |
| Allergies | ✅ Covered | AllergyIntolerance (27 fields), C-CDA Allergies section | Standard |
| Immunizations | ✅ Covered | Immunization (36 fields), C-CDA Immunizations section | Standard |
| Vitals | ✅ Covered | Observation (48 fields), C-CDA Vital Signs section | Standard vital signs profiles |
| Lab results | ✅ Covered | Observation, DiagnosticReport (35 fields), C-CDA Results section | Standard |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport covers reports; primary care may have limited imaging | N/A — primary care practice likely doesn't store imaging data |
| Procedures | ✅ Covered | Procedure (34 fields), C-CDA Procedures section | Standard; includes ML extensions for auto-generated procedure records |
| Clinical notes / documents | ✅ Covered | DocumentReference (42 fields), C-CDA Notes section | Standard document references |
| Care plans / goals | ⚠️ Partial | Goal listed in EHI (no doc page); CarePlan excluded from EHI despite being documented; C-CDA has Plan of Treatment, Assessment and Plan, Goals sections | Product has chronic care management (Impact program) with care plans — CarePlan exclusion is a gap |
| Orders / referrals | ✅ Covered | ServiceRequest (30 fields) | Standard |
| Insurance / coverage | ❌ Not covered | Coverage resource documented in FHIR API but **excluded from EHI export** | Product stores insurance data and bills insurance directly; significant gap |
| Claims / billing | ❌ Not covered | No billing/claims resources in export | Product bills insurance for clinical visits; no billing data exported. Significant gap. |
| Payments | ❌ Not covered | No payment resources | Product processes membership fees and insurance payments; gap |
| Consents / directives | ⚠️ Partial | Consent resource in EHI (no doc page; TOS consent via custom terminology) | Covers consent forms but no documentation of fields or scope |
| Patient communications / portal messages | ⚠️ Partial | Communication resource in EHI (no doc page; TMN and AVS codes) | Captures some messaging (Treat Me Now, After Visit Summaries) but unclear if all portal messages are included; no field documentation |
| Questionnaire / intake forms | ❌ Not covered | Questionnaire and QuestionnaireResponse documented in FHIR API but **excluded from EHI export** | Product uses intake forms, screening questionnaires, and patient-reported data; gap |
| Family health history | ✅ Covered | C-CDA Family History section; no dedicated FHIR resource (FamilyMemberHistory) | Covered via C-CDA but not FHIR |

## 6. Documentation Quality

**Strengths:**
- FHIR resource documentation is detailed: 22 resources with 629 fields, each with name, type, cardinality, and description. 99.8% description coverage.
- Custom extensions (ML model tracking, first-party data flag) are documented with examples.
- Custom terminology codes have clear descriptions.
- C-CDA API endpoint, authentication, and parameters are documented.

**Weaknesses:**
- Three EHI export resource types (Communication, Consent, Goal) have **no field-level documentation pages**. A developer cannot determine what fields these resources contain.
- No sample export data (no example ZIP, JSON bundle, or XML document).
- No machine-readable schema beyond standard FHIR R4.
- The EHI export page is a single page listing resource types and C-CDA sections — no explanation of how the export differs from the standard FHIR API or C-CDA endpoint.
- No documentation of relationships between resources, value sets beyond standard FHIR bindings, or export-specific behavior.
- The EHI export overview has a data quality issue: "Condition" appears twice in the FHIR resource list, and "Diagnostic Report" is listed with a space (inconsistent with FHIR convention "DiagnosticReport").

**Could a developer build an import?** Partially. The FHIR documentation is standard enough that a FHIR-literate developer could parse the JSON bundle. However, the undocumented resources (Communication, Consent, Goal) and lack of sample data create uncertainty. The C-CDA component follows C-CDA 2.1 spec and would be parseable with standard tools.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers core clinical domains well (demographics, encounters, conditions, medications, allergies, immunizations, vitals, labs, procedures, notes, orders) but has significant gaps relative to what 1Life stores:

- **Insurance/Coverage**: The FHIR API documents a Coverage resource with 31 fields, but it is explicitly excluded from the EHI export. One Medical bills insurance directly and stores coverage data — this is a designated record set gap.
- **Billing/Claims/Payments**: No billing, claims, or payment data in the export. One Medical processes insurance claims for clinical visits and charges membership fees. This is entirely absent.
- **Questionnaires/Intake Forms**: QuestionnaireResponse is documented in the API (23 fields) but excluded from the EHI export. Patient-reported intake data and screening questionnaires are part of the record.
- **Care Plans**: CarePlan is documented (24 fields) but excluded from the EHI export. One Medical's "Impact" chronic care management program generates care plans.

The inclusion of Communication (TMN/AVS) and Consent (TOS) shows some effort beyond pure USCDI, but these are only two additional resource types with no field documentation.

**Axis 2 — Export approach: Repackaged existing export**

Strong evidence this is the existing FHIR (g)(10) API and C-CDA endpoint repackaged as (b)(10):

1. **The EHI export page simply lists FHIR resource types and C-CDA sections** — there is no purpose-built export mechanism described. The export is described as a ZIP containing a FHIR bundle and a C-CDA document, which are the same outputs available through the existing FHIR and C-CDA APIs.
2. **The FHIR resource documentation is shared** — the same 22 resource pages serve both the general FHIR API and the EHI export. There is no separate EHI-specific documentation.
3. **The resource types map almost exactly to USCDI/US Core** — 14 of the 16 unique EHI FHIR resources are standard US Core resource types. Only Communication and Consent are additions.
4. **No billing, custom forms, or operational data** — the export contains only clinical exchange data, not the broader designated record set.
5. **Coverage is documented in the API but excluded from the EHI export** — if this were a purpose-built EHI export, the vendor would include, not exclude, insurance data already available in their FHIR API.

### Key Findings

1. **EHI export is a thin wrapper around existing FHIR + C-CDA APIs.** The export documentation is a single page listing standard FHIR resource types and C-CDA sections. No purpose-built export logic or EHI-specific data dictionary exists.

2. **Coverage resource deliberately excluded from EHI despite being documented in the FHIR API.** This is the most telling signal — insurance data is available in the system and API but omitted from the (b)(10) export.

3. **No billing, claims, or financial data exported.** One Medical bills insurance for visits and charges membership fees. None of this financial data appears in the export.

4. **Three EHI resources (Communication, Consent, Goal) lack field documentation.** These are listed in the export but have no dedicated documentation pages — a developer cannot determine their structure.

5. **FHIR field documentation quality is genuinely good** — 629 fields across 22 resources, 99.8% with descriptions, including custom ML extensions and terminology. The documentation quality is not the problem; the scope is.

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export
Export format:   FHIR R4 JSON + C-CDA 2.1 XML (ZIP)
Entities:        16 unique FHIR resources + 18 C-CDA sections (22 total FHIR resources documented in API)
Fields:          629 (across 22 documented FHIR resources)
Descriptions:    99.8% (628 of 629)
Sample data:     No
Bulk export:     Yes (single and multiple patients per overview)
Domains covered: 11 of 17 applicable domains
```

### Bottom Line

One Medical's EHI export is their existing FHIR (g)(10) API output and C-CDA document bundled into a ZIP file and relabeled as (b)(10). While the clinical data documentation is detailed (629 fields, 99.8% described), the export omits billing/claims data, insurance coverage (despite having a Coverage resource in their API), intake questionnaires, and care plans — all data One Medical stores as part of the designated record set. A patient would receive a solid clinical summary but not a complete copy of their health record.
