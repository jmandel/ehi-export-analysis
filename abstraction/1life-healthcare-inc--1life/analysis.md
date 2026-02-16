# EHI Export Analysis: 1Life Healthcare, Inc (One Medical)

**Product**: 1Life v1.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 10964 (15.05.05.3121.ONEL.01.00.1.220823)

## 1. Product Context

1Life is the proprietary EHR platform built in-house by One Medical (acquired by Amazon in 2023). It is **not sold to third parties** — it is the internal technology backbone for One Medical's membership-based primary care practice, operating 125+ ambulatory offices across 19+ U.S. cities with employed physicians and nurse practitioners.

**Data the product should store:**
- **Clinical**: Demographics, encounters/visit notes, problem lists, medications/prescriptions (via SureScripts e-prescribing), allergies, immunizations, vital signs, lab orders/results, procedures, clinical notes, care plans, family health history, implantable devices
- **Communication**: Patient-provider secure messaging, provider-to-provider messaging, "Treat Me Now" on-demand visit threads, After Visit Summaries
- **Care coordination**: Specialist referrals, chronic care management (Impact program), care navigator notes, care team assignments
- **Administrative**: Scheduling/appointments, insurance verification, billing/claims (they bill insurance for every clinical visit), membership data, consent records
- **Virtual care**: Video visit records, on-demand telehealth records, photo attachments from virtual visits
- **Patient-generated**: Questionnaire/survey responses (e.g., PHQ-9), prescription renewal requests, referral requests

The product is ambulatory primary care only — no hospital, no surgery, no imaging/PACS. However, it does include billing (insurance claims), referral management, chronic care programs, and extensive patient communication features beyond typical clinical charting.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-overview.html` (37KB) | Core EHI export page listing FHIR resource types (17 rows, 16 unique) and C-CDA sections (18). Defines export format as ZIP with .json + .xml. | **High** — primary EHI export documentation |
| `fhir/resources/*.html` (22 files) | Individual FHIR resource documentation pages with field-level tables (name, type, cardinality, description). 629 total fields across 22 resources. | **High** — the export schema |
| `fhir/extensions.html` (70KB) | 11 FHIR extensions including US Core Race/Ethnicity, ML model extensions, and First Party Data. | **Medium** — shows vendor-specific augmentation |
| `fhir/terminology.html` (39KB) | 3 custom terminology codes (TOS consent, TMN messaging, AVS summaries) under `http://onemedical.com/terminology`. | **Medium** — shows custom data types |
| `ccda/patient-continuity-of-care-document.html` (37KB) | C-CDA API endpoint documentation with authentication, parameters, and section list. | **Medium** — confirms C-CDA is a separate API |
| `fhir/overview.html` (37KB) | FHIR API overview with root URLs, media types, error codes. | **Low** — standard API infrastructure docs |
| `fhir/authentication.html` (40KB) | FHIR API authentication documentation. | **Low** — infrastructure |
| `fhir/search-and-output.html` (43KB), `fhir/pagination.html` (41KB) | Search and pagination docs for the FHIR API. | **Low** — standard API capabilities |
| `fhir/capability-statement.html` (33KB) | CapabilityStatement endpoint documentation. | **Low** — standard FHIR metadata |
| `enrichment/fhir-resources.json` (158KB) | Machine-parsed extraction of all 22 resource schemas into structured JSON. | **High** — verified against source HTML |
| `enrichment/ehi-export-summary.json` (12KB) | Extracted EHI export format, C-CDA sections, extensions, and terminology. | **High** — structured summary |
| `screenshot-ehi-export-overview.png` (266KB) | Full-page screenshot of the EHI export overview. | **Low** — visual confirmation |
| `homepage.html` (30KB), `ehi-export-index.html` (31KB) | Site navigation pages. | **Low** — site structure only |

**No sample data files, no downloadable schemas, no PDF documentation.** The entire documentation is HTML only.

## 3. Export Mechanics

- **Format**: ZIP file containing two files per patient:
  - `.json` — FHIR R4 Bundle with all resources on record
  - `.xml` — C-CDA v2.1 Patient Continuity of Care Document
- **Mechanism**: **Unclear.** The EHI export overview page describes only the output format. No documentation exists for how to trigger, request, or initiate an export — no API endpoint, no UI button, no workflow description. The C-CDA section documents a separate API endpoint (`GET https://production.app.1life.com/api/ccda`), but the EHI export page does not reference this endpoint or describe its own.
- **Single-patient vs bulk**: The page states exports are "for a single patient or multiple patients," but no details on bulk export mechanics are provided.
- **Access constraints**: Not documented. The FHIR API requires authentication, but the EHI export trigger mechanism is undocumented.

## 4. Export Content: What's In It

### FHIR Bundle (JSON)

The EHI export overview lists **17 resource type rows** in the FHIR bundle, but "Condition" appears twice (a documentation error), yielding **16 unique resource types**:

AllergyIntolerance, CareTeam, Communication, Condition, Consent, Device, Diagnostic Report, DocumentReference, Encounter, Goal, Immunization, MedicationRequest, Observation, Patient, Procedure, ServiceRequest

Of these 16, **3 have no individual documentation pages**: Communication, Consent, and Goal. Their field structure and content are not documented.

The FHIR API documentation covers **22 resource types** (629 fields total), which includes 9 resources not explicitly listed on the EHI export page: CarePlan, Coverage, Location, Medication, Organization, Practitioner, Provenance, Questionnaire, QuestionnaireResponse. These are likely included in the FHIR bundle as referenced/supporting resources.

### Documentation quality per field

- **Total fields across 22 documented resources**: 629
- **Fields with descriptions**: 628 (99.8%)
- **Fields with types**: 582 (92.5%)
- **Fields without types**: 47 (7.5%) — these are typically structural parent fields (e.g., `meta`, `coding`) where the type is implicit

### C-CDA Document (XML)

The C-CDA portion contains **18 sections**: Allergies, Assessment and Plan, Care Team, Encounters, Family History, Goals, Health Concerns, Immunizations, Medical Equipment, Medications, Notes, Patient, Plan of Treatment, Problems, Procedures, Results, Social History, Vital Signs.

The C-CDA sections cover some domains not explicitly represented in the FHIR resource list — notably **Family History** and **Social History** — providing complementary coverage.

### Vendor's own content organization

The documentation is organized by FHIR resource type. There are no vendor-defined categories. All resources use standard FHIR naming.

| Resource Type | Fields | Described | Types | In EHI Export List |
|---|---|---|---|---|
| Patient | 60 | 60 | 58 | ✓ |
| Observation | 48 | 47 | 43 | ✓ |
| DocumentReference | 42 | 42 | 40 | ✓ |
| Immunization | 36 | 36 | 34 | ✓ |
| DiagnosticReport | 35 | 35 | 33 | ✓ |
| Procedure | 34 | 34 | 32 | ✓ |
| Encounter | 33 | 33 | 31 | ✓ |
| Questionnaire | 31 | 31 | 29 | Supporting |
| Coverage | 31 | 31 | 29 | Supporting |
| ServiceRequest | 30 | 30 | 28 | ✓ |
| AllergyIntolerance | 27 | 27 | 25 | ✓ |
| CareTeam | 26 | 26 | 24 | ✓ |
| Location | 26 | 26 | 24 | Supporting |
| CarePlan | 24 | 24 | 22 | Supporting |
| QuestionnaireResponse | 23 | 23 | 21 | Supporting |
| Condition | 23 | 23 | 21 | ✓ |
| MedicationRequest | 21 | 21 | 19 | ✓ |
| Practitioner | 19 | 19 | 17 | Supporting |
| Organization | 18 | 18 | 16 | Supporting |
| Provenance | 17 | 17 | 15 | Supporting |
| Medication | 13 | 13 | 11 | Supporting |
| Device | 12 | 12 | 10 | ✓ |

**Undocumented EHI resources** (listed in export but no field-level documentation): Communication, Consent, Goal.

### Notable vendor-specific features

1. **Machine Learning extensions**: Observation and Procedure resources can carry ML model extensions (source type, model name, model repository, model type, model use case, model performance, prediction characteristics). Resources generated by ML models are flagged as non-authoritative with preliminary/draft status.

2. **Custom terminology codes**:
   - `Consent.TOS` — Terms of Service consent signed by new members
   - `Communication.TMN` — Treat Me Now on-demand visit message threads
   - `Communication.AVS` — After Visit Summary follow-up instructions

3. **First Party Data extension**: Marks Procedure resources created from One Medical interactions vs. external care records.

4. **Questionnaire/QuestionnaireResponse**: Captures patient surveys (e.g., PHQ-9), linking survey templates to patient-specific answers. This is beyond standard USCDI.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers clinical data through **standard FHIR R4 resources** with some One Medical-specific extensions. The strongest coverage areas are:

- **Core clinical data**: Patient demographics (60 fields), conditions/problems (23 fields), medications (21+13 fields), allergies (27 fields), immunizations (36 fields), observations/vitals/labs (48 fields), procedures (34 fields), encounters (33 fields)
- **Documents and reports**: DocumentReference (42 fields) and DiagnosticReport (35 fields) provide clinical document and lab report coverage
- **Care coordination**: CarePlan (24 fields), CareTeam (26 fields), ServiceRequest (30 fields) for referrals and care planning
- **Insurance coverage**: Coverage (31 fields) captures payor information, plan details, subscriber relationships
- **Patient engagement**: Questionnaire (31 fields) and QuestionnaireResponse (23 fields) capture surveys like PHQ-9
- **Communication**: Communication resource (undocumented but listed) captures Treat Me Now threads and After Visit Summaries
- **Consent**: Consent resource (undocumented but listed) captures Terms of Service consent

The **thinnest areas** are:
- Communication, Consent, and Goal have no field-level documentation
- No billing/claims data at all — Coverage captures insurance information but no charges, claims, or payments
- No family health history in the FHIR bundle (only in C-CDA)

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient (60 fields) with US Core Race/Ethnicity extensions | Thorough |
| Encounters / visits | ✅ Covered | Encounter (33 fields) including status, class, type, participants, period, location | Thorough; virtual vs in-person distinction not explicitly documented |
| Problems / conditions | ✅ Covered | Condition (23 fields) with clinical/verification status, category, code, onset | Thorough |
| Medications / prescriptions | ✅ Covered | MedicationRequest (21 fields) + Medication (13 fields) | Thorough; SureScripts e-prescribing integrated |
| Allergies | ✅ Covered | AllergyIntolerance (27 fields) with reaction details | Thorough |
| Immunizations | ✅ Covered | Immunization (36 fields) with vaccine codes, lot numbers | Thorough |
| Vitals | ✅ Covered | Observation (48 fields) covers vitals, labs, social history | Thorough |
| Lab results | ✅ Covered | DiagnosticReport (35 fields) + Observation for individual results | Thorough |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport may include some imaging reports; no PACS integration expected for primary care | N/A — product unlikely to store imaging beyond external records |
| Procedures | ✅ Covered | Procedure (34 fields) with First Party Data extension | Good; includes ML-derived procedures |
| Clinical notes / documents | ✅ Covered | DocumentReference (42 fields) for clinical documents; C-CDA Notes section | Good |
| Care plans / goals | ✅ Covered | CarePlan (24 fields), Goal (undocumented but listed), CareTeam (26 fields) | Partial — Goal has no field documentation |
| Orders / referrals | ✅ Covered | ServiceRequest (30 fields) for orders and referrals | Thorough |
| Insurance / coverage | ✅ Covered | Coverage (31 fields) with payor, plan, subscriber details | Good for insurance information |
| Claims / billing | ❌ Not covered | No billing entities in the export | **Significant gap**: One Medical bills insurance for every visit; billing data exists but is not exported |
| Payments | ❌ Not covered | No payment entities in the export | Gap: membership fees and insurance payments not represented |
| Consents / directives | ⚠️ Partial | Consent resource listed but has no field-level documentation; TOS consent captured via custom terminology | Partially covered — consent records exist but their structure is undocumented |
| Patient communications / portal messages | ⚠️ Partial | Communication resource listed but undocumented; custom codes for Treat Me Now (TMN) and After Visit Summary (AVS) threads | Partially covered — communication exists but granularity (full message text vs metadata) is unclear |
| Specialty-specific | N/A | Primary care — no specialty-specific data expected | N/A |

**Domains covered**: 13 of 16 applicable domains (✅ or ⚠️)
**Domains missing**: Claims/billing, payments (2 domains with genuine gaps)

## 6. Documentation Quality

**Strengths:**
- Field-level documentation is excellent: 628 of 629 fields (99.8%) have descriptions. 582 (92.5%) have explicit types. This is unusually thorough for EHI export documentation.
- The documentation is organized in a clean Hugo-based static site (hosted on GitHub Pages) that is fast, accessible, and requires no JavaScript to read.
- Custom extensions and terminology are explicitly documented with example JSON snippets.
- The Questionnaire documentation specifically calls out clinical use cases (PHQ-9 surveys) connecting the FHIR resource to One Medical's actual clinical workflows.

**Weaknesses:**
- **No sample export files**: No example FHIR Bundle or C-CDA document is provided anywhere. A developer would have to construct expected outputs from field tables alone.
- **No export trigger documentation**: How a patient, provider, or administrator actually initiates an EHI export is completely undocumented. Is it a UI button? An API call? A support request? This is a significant omission for (b)(10) compliance.
- **3 undocumented resources**: Communication, Consent, and Goal are listed as EHI export resource types but have no documentation pages. A developer cannot understand what these resources contain.
- **No value set documentation**: While 3 custom codes are documented, standard code system bindings (SNOMED, LOINC, ICD-10) are mentioned in descriptions without specifying which value sets One Medical actually uses.
- **ML extension URLs are internal**: The machine learning extension URLs point to internal Google Sites (`sites.google.com/onemedical.com/...`) that are not publicly accessible.
- **No relationship diagram**: FHIR reference mechanics connect resources (e.g., Observation → Encounter → Patient), but there's no documentation of which references One Medical actually populates.

**Could a developer build an import from this documentation?** Partially. The field-level detail for the 22 documented resources is sufficient to parse a FHIR Bundle, but the 3 undocumented resources, lack of sample data, and absence of value set specifics would require significant guesswork. A developer familiar with FHIR R4 could work with this; a developer unfamiliar with FHIR would struggle.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical data domains thoroughly — demographics, encounters, conditions, medications, allergies, immunizations, vitals, labs, procedures, notes, care plans, referrals, and insurance coverage are all represented with detailed field-level documentation. The inclusion of Questionnaire/QuestionnaireResponse (for patient surveys), Communication (for secure messaging threads), and Consent goes beyond basic USCDI clinical summaries.

However, there is a **significant gap in billing/claims data**. One Medical bills insurance for every clinical visit, so claims, charges, and payment data exist in the 1Life system. None of this appears in the export. The Coverage resource captures which insurance plan a patient has, but not what was billed or paid. For a practice that processes insurance claims for every encounter, omitting billing data is a meaningful gap relative to the product's data scope.

**Axis 2 — Export approach: Purpose-built EHI export (with caveats)**

The export shows evidence of purpose-built effort beyond simply repackaging the (g)(10) FHIR API:

1. **Non-US Core resources**: Communication, Consent, Goal, Questionnaire, and QuestionnaireResponse go beyond the standard US Core / USCDI scope required for (g)(10).
2. **Custom terminology and extensions**: The TMN/AVS communication codes and ML extensions are One Medical-specific, not standard US Core.
3. **Bundled export format**: The export produces a complete per-patient ZIP file (FHIR Bundle + C-CDA), not a query-by-query API — this is a purpose-built delivery mechanism.
4. **Separate documentation page**: The EHI export has its own documentation section distinct from the FHIR API docs.

That said, the export is **clearly built on top of the same FHIR infrastructure** that serves the (g)(10) API. The 22 documented FHIR resources are the same resources available through the API. The EHI export appears to be a "collect and bundle" operation on top of the existing FHIR server, adding a few resources beyond US Core scope. This is a legitimate approach — the vendor extended their FHIR coverage for (b)(10) — but it means the export is limited to data that maps to FHIR resources, which excludes billing/claims data that has no natural FHIR representation in their implementation.

### Key Findings

1. **Field-level documentation is exceptionally thorough**: 629 fields across 22 FHIR resources, with 99.8% having descriptions. This is among the best-documented EHI exports in terms of schema detail.

2. **Billing data is completely absent**: Despite One Medical billing insurance for every visit, no claims, charges, or payment data appears in the export. The Coverage resource captures insurance plan information but not billing transactions. This is the largest gap.

3. **Three EHI resources are undocumented**: Communication, Consent, and Goal are listed in the export but have no field-level documentation, making it impossible to assess their completeness.

4. **Export trigger mechanism is undocumented**: The documentation describes what the export contains but not how to obtain it. No API endpoint, UI workflow, or request process is described for the EHI export itself.

5. **Beyond-USCDI resources show genuine effort**: Questionnaire/QuestionnaireResponse (patient surveys), Communication (secure messaging), Consent, and custom ML extensions demonstrate that One Medical built beyond the minimum (g)(10) requirements.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   FHIR R4 JSON Bundle + C-CDA v2.1 XML (ZIP)
    Entities:        22 documented FHIR resources (16 unique in EHI list + 9 supporting; 3 undocumented)
    Fields:          629
    Descriptions:    99.8%
    Sample data:     No
    Bulk export:     Unclear (page says "single or multiple patients" but no details)
    Domains covered: 13 of 16 applicable domains

### Bottom Line

One Medical built a genuine EHI export that goes beyond their (g)(10) FHIR API by including patient communications, consent records, questionnaire responses, and ML-derived clinical data. The field-level documentation is excellent (629 fields, nearly all described). However, the complete absence of billing/claims data — for a practice that bills insurance for every visit — is a significant gap. The export covers clinical EHI thoroughly but omits the financial side of the designated record set.
