# EHI Export Analysis: Health Innovation Technologies, Inc.

**Product**: RevolutionEHR v7
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.1591.Revo.07.00.1.181231 (CHPL ID 9923)

## 1. Product Context

RevolutionEHR is a cloud-based EHR and practice management platform built exclusively for optometry and eye care practices, serving 13,000+ eye care professionals. It is an ambulatory-only, specialty-specific product — not a general hospital EHR.

**Key functional areas relevant to EHI completeness:**
- **Clinical EHR**: Optometric exam templates, refraction data, visual acuity, slit lamp findings, IOP, fundus exams; diagnostic equipment integration (OCT, visual fields, retinal imaging) with 12+ instrument manufacturers; PACS for ophthalmic images
- **Practice management**: Scheduling, multi-location support, staff roles
- **Optical dispensing**: Point-of-sale, frame/lens inventory, contact lens ordering, supplier integrations (Hoya, CooperVision, ABB Optical Group)
- **Billing & claims**: Automated claims submission, clearinghouse processing (RevClear/TriZetto), eligibility verification, remittance posting, patient billing
- **E-prescribing**: Via RXNT integration (separate subscription)
- **Patient portal**: Intake forms (RevIntake/IntakeQ), self-scheduling, reminders, surveys
- **Interoperability**: FHIR API (via Dynamic Health IT ConnectEHR), C-CDA transitions of care, Direct messaging (RevDirect)

The designated record set for this product should include optometric exam data (refractions, diagnostic tests, images), optical dispensing records (prescriptions, orders), billing data, medications/prescriptions, clinical notes, and patient communications — in addition to standard clinical data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/openapiServices.json` (46,534 bytes) | OpenAPI 3.0.1 specification titled "RevolutionEHR Patient Export" v1.0 — the primary data dictionary defining 35 schemas with 279 fields | **Most informative** — this is the sole substantive artifact |
| `downloads/certification-disclosures.html` (64,944 bytes) | Full certification disclosures page with b(10) export description (3 sentences), FHIR API links, and certification details | Moderately informative — provides export mechanics (where to access, single vs population) |
| `downloads/certification-disclosures-fullpage.png` (560,887 bytes) | Screenshot of the certification disclosures page | Visual reference only |
| `downloads/enrichment/schemas.json` (68,239 bytes) | Prior agent's parsed extraction of the OpenAPI schemas | Used for orientation; independently verified |
| `downloads/enrichment/coverage-accounting.json` (2,104 bytes) | Prior agent's parse statistics | Verified: 35 schemas, 279 fields confirmed |

No sample export data was provided. No user guide, export instructions, or screenshots of the export UI were found.

## 3. Export Mechanics

- **Format**: Proprietary JSON — a single nested JSON object per patient
- **Mechanism**: UI-based. Single-patient export via Admin module → Patient Management. Population-level export available upon request by contacting customer support.
- **Single-patient**: Yes (self-service via Admin module)
- **Bulk capability**: Yes, but only via vendor support request — not self-service
- **Access constraints/fees**: Not documented. Population export requires contacting support, which introduces potential friction/delay.
- **Endpoint**: `POST patient/export` per the OpenAPI spec

The export is clearly separate from RevolutionEHR's FHIR/g(10) API, which is powered by Dynamic Health IT's "ConnectEHR +BulkFHIR" — a third-party interoperability layer.

## 4. Export Content: What's In It

### Data dictionary overview

The OpenAPI 3.0.1 specification defines **35 schemas** with **279 total fields**. The root `Patient` schema has 17 top-level properties that reference all other schemas via nesting and arrays.

- **Fields with any description**: 268 of 279 (96.1%)
- **Fields with meaningful descriptions** (beyond restating the field name): 205 of 279 (73.5%)
- **Data types**: Fully specified (string, integer, number, boolean) with format annotations (date, date-time, double, int32, int64)
- **Required fields**: Documented per schema (e.g., Allergy requires `severity` and `name`)
- **Value sets/enums**: **None documented**. Fields like `severity`, `status`, `smokingStatus`, `type` are plain strings with no enumerated values.
- **Foreign keys/relationships**: Expressed via JSON nesting and `$ref` references — 37 cross-schema relationships
- **Sample data**: None provided

### Vendor's own content organization

The export uses a single nested JSON structure rooted at `Patient`. The following table shows all 35 entities organized by domain:

| Entity | Fields | Described | Types | Category |
|---|---|---|---|---|
| Patient | 17 | 16 | yes | Root |
| Demographics | 17 | 15 | yes | Demographics |
| Address | 5 | 5 | yes | Demographics |
| Employment | 4 | 4 | yes | Demographics |
| Contact | 4 | 4 | yes | Demographics |
| FamilyMember | 4 | 4 | yes | Demographics |
| Encounter | 19 | 18 | yes | Clinical - Encounters |
| EncounterDiagnosis | 3 | 2 | yes | Clinical - Encounters |
| ReasonForVisit | 3 | 1 | yes | Clinical - Encounters |
| Service | 3 | 3 | yes | Clinical - Encounters |
| VitalSigns | 9 | 9 | yes | Clinical - Vitals |
| Refraction | 19 | 19 | yes | Clinical - Optometry |
| Test | 2 | 2 | yes | Clinical - Diagnostics |
| TestValue | 2 | 2 | yes | Clinical - Diagnostics |
| ClinicalDecisionSupport | 8 | 8 | yes | Clinical - Decision Support |
| OrientationMood | 6 | 6 | yes | Clinical - Assessments |
| SocialHistory | 6 | 6 | yes | Clinical - Social/Family History |
| FamilyHealthHistory | 11 | 11 | yes | Clinical - Social/Family History |
| FamilyHistory | 3 | 1 | yes | Clinical - Social/Family History |
| Diagnosis | 7 | 7 | yes | Clinical - Diagnoses |
| DiagnosisCarePlanItem | 2 | 0 | yes | Clinical - Diagnoses |
| CarePlanItem | 4 | 4 | yes | Clinical - Care Plans |
| HealthGoal | 5 | 5 | yes | Clinical - Goals |
| HealthConcern | 6 | 6 | yes | Clinical - Concerns |
| Allergy | 7 | 7 | yes | Clinical - Allergies |
| Immunization | 16 | 16 | yes | Clinical - Immunizations |
| ImplantableDevice | 7 | 7 | yes | Clinical - Devices |
| MedicalOrder | 30 | 30 | yes | Clinical - Orders/Labs |
| Referral | 13 | 13 | yes | Clinical - Referrals |
| Insurance | 6 | 6 | yes | Billing & Insurance |
| Invoice | 7 | 7 | yes | Billing & Insurance |
| InvoiceItem | 12 | 12 | yes | Billing & Insurance |
| Claim | 5 | 5 | yes | Billing & Insurance |
| Payment | 3 | 3 | yes | Billing & Insurance |
| Statement | 4 | 4 | yes | Billing & Insurance |

Full entity inventory with all field-level detail: `analysis/entity-inventory-full.json`

### Category breakdown summary

| Category | Entities | Fields |
|---|---|---|
| Root | 1 | 17 |
| Demographics | 5 | 34 |
| Clinical - Encounters | 4 | 28 |
| Clinical - Optometry | 1 | 19 |
| Clinical - Orders/Labs | 1 | 30 |
| Clinical - Social/Family History | 3 | 20 |
| Clinical - Immunizations | 1 | 16 |
| Clinical - Vitals | 1 | 9 |
| Clinical - Diagnoses | 2 | 9 |
| Clinical - Decision Support | 1 | 8 |
| Clinical - Allergies | 1 | 7 |
| Clinical - Devices | 1 | 7 |
| Clinical - Assessments | 1 | 6 |
| Clinical - Concerns | 1 | 6 |
| Clinical - Goals | 1 | 5 |
| Clinical - Care Plans | 1 | 4 |
| Clinical - Diagnostics | 2 | 4 |
| Clinical - Referrals | 1 | 13 |
| Billing & Insurance | 6 | 37 |

### Notable schema details

**MedicalOrder** (30 fields) is the largest schema, combining order and result data into a single flat entity. It includes LOINC codes, ordering provider, lab name, result values/units/status, specimen source, and interpretation fields. This covers both lab orders and results.

**Invoice/InvoiceItem/Claim/Payment** (27 fields across 4 entities) represent a genuine billing chain: invoices with CPT-coded line items (code, modifiers, quantity, unit price, discounts, tax, adjustments, paid, balance), linked payments (date, method, amount), and claim history (dates, submit method, status messages).

**Refraction** (19 fields) captures optometry-specific refraction data for both eyes (OD/OS): sphere, cylinder, axis, horizontal/vertical prism with orientation, intermediate add, and near add. This is specialty-specific data that would not appear in a generic USCDI export.

**Encounter** (19 fields) is richly nested, referencing 10 other schemas: diagnoses, family history, social history, reason for visit, services, vital signs, refractions, tests, clinical decision support, and orientation/mood.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers three broad areas:

1. **Clinical encounter data** (most entities): Encounters with nested structured data — diagnoses, vitals, refractions, diagnostic tests, services, mental status, clinical decision support, family/social history, and reason for visit. Also standalone entities for diagnoses, allergies, immunizations, medical orders/lab results, referrals, care plans, health goals, health concerns, and implantable devices. The Refraction schema is genuinely optometry-specific.

2. **Demographics and relationships** (5 entities, 34 fields): Patient identity, address, employment, emergency contacts, and family account members. Covers race, ethnicity, language, previous names.

3. **Billing and insurance** (6 entities, 37 fields): Insurance coverage, invoices with CPT-coded line items and full financial detail (unit price, discounts, tax, adjustments, paid, balance), payments, claims with submission tracking, and patient statements. This is a meaningfully detailed billing export.

**Thinnest areas**: The Test/TestValue schemas (4 fields total) are generic name/value pairs — minimal structure for what could be rich diagnostic equipment data. The DiagnosisCarePlanItem has zero descriptions. The Contact and FamilyMember schemas are very thin (4 fields each, no phone/address).

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` (17 fields), `Address` (5), `Employment` (4), `Contact` (4), `FamilyMember` (4) | Solid. Covers name, DOB, sex, race, ethnicity, language, address, phone, email, employment, contacts. |
| Encounters / visits | ✅ Covered | `Encounter` (19 fields) with nested diagnoses, vitals, tests, services, etc. | Well-structured with 10 sub-entity references. Captures date, location, type, category, provider, signed status. |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis` (7 fields) with ICD codes, eye location, qualifier, onset/resolved dates | Includes optometry-specific `eyeLocation` and `qualifier` fields. |
| Medications / prescriptions | ❌ Not covered | No Medication or Prescription schema. No medication-related fields found across all 35 schemas. | **Significant gap.** Product integrates with RXNT for e-prescribing. If medication lists and prescription history are stored in RevolutionEHR (even if originated via RXNT), their absence is a real gap. If all medication data lives entirely in RXNT's system, this is a data boundary issue rather than an export gap — but this is not documented. |
| Allergies | ✅ Covered | `Allergy` (7 fields): name, severity, reaction, treatment, onset/resolved dates, status | Adequate. |
| Immunizations | ✅ Covered | `Immunization` (16 fields): CVX code/name, manufacturer, lot, expiration, site, route, administered by, etc. | Thorough. |
| Vitals | ✅ Covered | `VitalSigns` (9 fields): BP systolic/diastolic, pulse, height, weight, BMI, temperature, respiration, O2 saturation | Good coverage of standard vitals. |
| Lab results | ✅ Covered | `MedicalOrder` (30 fields): LOINC codes, lab name, result value/unit/status, specimen source, interpretation | Comprehensive order-to-result chain. |
| Imaging / diagnostic reports | ⚠️ Partial | `Test`/`TestValue` (4 fields total) — generic name/value pairs for diagnostic equipment readings | Product has PACS and integrates with 12+ diagnostic instruments. The export captures test names and values but **no images, no structured imaging reports, no OCT/visual field data in its native form**. |
| Procedures | ⚠️ Partial | `Service` within Encounter (3 fields: code, description, diagnosis) | Captures CPT-coded services performed but minimal detail beyond code/description. |
| Clinical notes / documents | ❌ Not covered | No free-text note field, no document schema, no narrative encounter documentation | **Significant gap.** Encounter schema captures structured data only (diagnoses, vitals, tests) with no field for clinical narrative, progress notes, or assessment/plan text. |
| Care plans / goals | ✅ Covered | `CarePlanItem` (4), `HealthGoal` (5), `HealthConcern` (6), `DiagnosisCarePlanItem` (2) | Present but thin. |
| Orders / referrals | ✅ Covered | `MedicalOrder` (30 fields) for lab orders; `Referral` (13 fields) with tracking, response, and report receipt | Referral schema is detailed: includes referring/referred-to provider, reason, status, response date, report received flag. |
| Insurance / coverage | ✅ Covered | `Insurance` (6 fields): company, policy number, group, subscriber, payer ID, type | Adequate but not deep — missing plan details, copay/deductible, eligibility data. |
| Claims / billing | ✅ Covered | `Invoice` (7), `InvoiceItem` (12), `Claim` (5), `Payment` (3), `Statement` (4) = 31 fields | **Genuinely detailed.** Full billing chain from services through claims to payments with line-item financial detail. |
| Payments | ✅ Covered | `Payment` (3 fields: date, method, amount) nested within Invoice | Basic but present. |
| Consents / directives | ❌ Not covered | No consent or advance directive schema | Unknown if product stores consents beyond intake forms. Not a clear gap. |
| Patient communications / portal | ❌ Not covered | No portal message, intake form, or communication schema | Product has patient portal (RevIntake/IntakeQ), automated reminders, and surveys. If intake form data is stored in RevolutionEHR, its absence is a gap. |
| Specialty-specific (optometry) | ⚠️ Partial | `Refraction` (19 fields) covers refraction data for both eyes. `Test`/`TestValue` generic pairs for diagnostic equipment. `Diagnosis.eyeLocation` for eye-specific diagnoses. | Refraction data is well-covered. **Missing: optical dispensing data** — spectacle/contact lens prescriptions, frame selections, lens orders, contact lens parameters, optical orders/fulfillment. This is a core product capability (optical POS, supplier integrations) with no representation in the export. Also missing: ophthalmic images from PACS. |

## 6. Documentation Quality

**Format**: The OpenAPI 3.0.1 specification is a good format choice — machine-readable, self-documenting, widely supported by developer tools. A developer can generate client libraries, validate export data, and understand the structure programmatically.

**Strengths**:
- All 279 fields have data types specified
- 268 of 279 fields (96.1%) have description strings
- Schema relationships are clearly expressed via `$ref`
- Required fields are documented per schema

**Weaknesses**:
- Most descriptions simply restate the field name (e.g., `city` → "City", `address1` → "Address1") — only 205 of 279 (73.5%) provide meaningful descriptions
- **No value sets or enumerations** for any coded field (severity, status, smokingStatus, type, etc.). A developer parsing the export cannot programmatically interpret these fields without sample data.
- **No sample export data** provided
- **No user guide or export instructions** beyond the 3 sentences on the certification disclosures page
- No versioning or change history beyond "1.0"
- The spec is hosted as a static file on HubSpot's CDN, suggesting manual upload rather than auto-generation from the system

**Developer usability**: A developer could build a parser from this spec. They would struggle with semantic interpretation of coded fields. The absence of sample data makes testing impossible without access to a live system.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical encounter data (including optometry-specific refractions), demographics, billing/insurance, allergies, immunizations, lab orders/results, referrals, care plans, and goals — a reasonable breadth that goes meaningfully beyond USCDI by including billing data (invoices, claims, payments) and optometry-specific data (refractions, eye-location diagnoses).

However, there are significant gaps relative to what RevolutionEHR stores:
- **Optical dispensing data** is entirely absent — spectacle/contact lens prescriptions, frame selections, lens orders, and order fulfillment are core product features with no export representation
- **Medications/prescriptions** are missing (the product integrates with RXNT for e-prescribing)
- **Clinical notes/narrative** have no field anywhere in the schema — only structured encounter data
- **Ophthalmic images** from the built-in PACS are not exported
- **Patient portal data** (intake forms, messages, surveys) is not represented

These are not marginal omissions — optical dispensing is arguably the #2 data domain for an optometry EHR after clinical exams. The export covers maybe 60-70% of the designated record set.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built b(10) export, not a repackaged existing exchange:
1. It uses a proprietary JSON format completely separate from their FHIR/g(10) API (powered by Dynamic Health IT's ConnectEHR +BulkFHIR)
2. The certification disclosures page explicitly separates b(10) documentation from the FHIR API links
3. The data dictionary includes billing data (invoices, claims, payments) and optometry-specific data (refractions, eye-location diagnoses) that would not appear in a standard USCDI/US Core FHIR export
4. The OpenAPI spec is a dedicated artifact — not a link to a generic standard specification

The vendor made a genuine effort to build a b(10)-specific export. The gaps appear to be omissions in scope rather than a cynical relabeling of existing exports.

### Key Findings

1. **Genuine purpose-built export with meaningful billing coverage.** The Invoice/InvoiceItem/Claim/Payment schemas (31 fields total) provide a real billing chain with CPT-coded line items, financial detail (unit price, discounts, tax, adjustments, paid, balance), payment tracking, and claim submission history. This is meaningfully beyond USCDI. (`openapiServices.json`, Invoice/InvoiceItem/Claim/Payment schemas)

2. **Major gap: optical dispensing data is entirely absent.** RevolutionEHR's optical POS, frame/lens inventory, contact lens ordering, and supplier integrations are core product features. No schema addresses spectacle prescriptions, contact lens parameters, optical orders, or fulfillment status. This is the single biggest gap. (`openapiServices.json` — no optical/dispensing/prescription schemas)

3. **No medications or prescriptions in the export.** Despite RXNT e-prescribing integration, there is no Medication or Prescription entity. Whether this is a data boundary issue (medications live in RXNT) or an export gap is undocumented. (`openapiServices.json` — grep for medication-related fields returns none)

4. **No clinical notes or narrative documentation.** The Encounter schema captures structured data (diagnoses, vitals, refractions, tests, services) but has no field for free-text clinical notes, progress notes, or assessment/plan narrative. (`openapiServices.json`, Encounter schema)

5. **Optometry-specific refraction data is well-modeled.** The Refraction schema (19 fields) captures OD/OS sphere, cylinder, axis, prism (horizontal/vertical with orientation), and add powers — core optometric data that demonstrates genuine engagement with specialty-specific EHI beyond USCDI. (`openapiServices.json`, Refraction schema)

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   Proprietary JSON (OpenAPI 3.0.1 documented)
    Entities:        35
    Fields:          279
    Descriptions:    96.1% have descriptions (73.5% meaningful)
    Sample data:     No
    Bulk export:     Yes (via vendor support request)
    Domains covered: 11 of 17 applicable domains (✅ or ⚠️)

### Bottom Line

RevolutionEHR built a genuine purpose-built EHI export with a well-structured OpenAPI data dictionary and meaningful billing coverage, but it has significant gaps in optical dispensing data (the product's signature specialty feature), medications/prescriptions, clinical notes, and ophthalmic images. A patient would get structured clinical encounter data, billing records, and refraction data — but not their spectacle/contact lens prescriptions, clinical narratives, or diagnostic images, which are core parts of an optometric patient record.
