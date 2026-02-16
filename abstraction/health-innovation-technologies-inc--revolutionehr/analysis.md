# EHI Export Analysis: Health Innovation Technologies, Inc.

**Product**: RevolutionEHR v7
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.1591.Revo.07.00.1.181231

## 1. Product Context

RevolutionEHR is a cloud-based EHR and practice management platform built exclusively for optometry and eye care practices, serving 13,000+ eye care professionals. The product integrates clinical EHR, practice management, scheduling, optical dispensing, and billing into a single platform.

Key data domains the product stores:
- **Clinical/exam data**: Optometric exams with customizable templates, visual acuity, refraction data, slit lamp findings, fundus results, intraocular pressure, and diagnostic equipment integrations (OCT, visual fields, retinal imaging from 12+ instrument manufacturers)
- **Optical dispensing**: Eyeglass/contact lens prescriptions, frame selections, lens orders, optical POS, inventory management, supplier integrations (Hoya, CooperVision, ABB Optical)
- **Billing/claims**: Claims submission via RevClear/TriZetto, insurance eligibility verification, ledger reconciliation, remittance posting, patient billing
- **E-prescribing**: Via RXNT integration (separate subscription)
- **Patient engagement**: Portal with intake forms, automated reminders, surveys, RevEngage for marketing
- **Imaging/PACS**: Ophthalmic images from integrated diagnostic devices
- **Provider communication**: Direct secure messaging via RevDirect

This baseline establishes what the EHI export should cover to be comprehensive.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `openapiServices.json` | 46,534 bytes | OpenAPI 3.0.1 specification defining the EHI export JSON format. 35 schemas, 279 fields. | **Primary artifact** — the complete data dictionary |
| `certification-disclosures.html` | 64,944 bytes | Full HTML of the certification disclosures page with b(10) export instructions | **Informative** — confirms export mechanics (single patient via Admin > Patient Management; bulk via customer support request) |
| `certification-disclosures-fullpage.png` | 560,887 bytes | Screenshot of the disclosures page | Low — visual backup only |
| `enrichment/schemas.json` | 68,239 bytes | Prior agent's parsed extraction of all 35 schemas with relationships | Moderate — cross-checked against my own parse |
| `enrichment/coverage-accounting.json` | 2,104 bytes | Parse statistics from prior agent | Low — verified independently |

The OpenAPI spec is the sole substantive artifact. No sample data files, user guides, or additional documentation were provided.

## 3. Export Mechanics

- **Format**: Proprietary JSON (vendor-specific schema, not FHIR or C-CDA)
- **Endpoint**: `patient/export` (POST)
- **Single-patient export**: Available within RevolutionEHR's Admin module under Patient Management
- **Bulk/population export**: Available upon request by contacting customer support
- **Data dictionary**: OpenAPI 3.0.1 specification linked from the certification disclosures page
- **Access constraints**: No stated fees for the export itself; however, RevDirect and RXNT require separate subscriptions for full incentive program attestation
- **Not FHIR**: The FHIR API (g)(10) is a separate system powered by Dynamic Health IT's ConnectEHR +BulkFHIR. The b(10) export is a distinct, vendor-specific JSON format.

## 4. Export Content: What's In It

The OpenAPI 3.0.1 specification defines a single root `Patient` object containing 17 top-level properties, decomposed into **35 schemas** with **279 total fields**. All 279 fields have explicit types. 268 of 279 fields (96.1%) have descriptions, though most descriptions are trivial restatements of the field name (e.g., `city` → "City", `code` → "Code"). Only 191 fields (68.5%) have descriptions that go meaningfully beyond the field name. No value sets or enumerations are documented for coded fields (e.g., `severity`, `status`, `smokingStatus` are typed as plain strings). No sample data is provided.

### Vendor's own content organization

The export schema uses a flat patient-centric JSON structure. The root Patient schema nests all data as direct properties. I categorized schemas into functional domains based on their content:

**Demographics (5 schemas, 34 fields)**

| Schema | Fields | Description |
|---|---|---|
| Demographics | 17 | Patient identity: name, DOB, sex, race, ethnicity, language, address, phone, email, employment |
| Address | 5 | Street address components (reused by Demographics and Employment) |
| Employment | 4 | Employment status, employer, position, address |
| Contact | 4 | Emergency/responsible party contacts |
| FamilyMember | 4 | Family account members (name, role) |

**Clinical — Encounters (5 schemas, 34 fields)**

| Schema | Fields | Description |
|---|---|---|
| Encounter | 19 | Visit records with date, location, type, category, provider, signed status; nests diagnoses, vitals, refractions, tests, services, family/social history, CDS, orientation/mood |
| EncounterDiagnosis | 3 | Diagnosis code, description, and linked care plan items |
| ReasonForVisit | 3 | Patient and provider reasons for visit, linked diagnosis/care plan items |
| Service | 3 | Performed services with CPT codes and linked diagnoses |
| OrientationMood | 6 | Mental/functional status assessment within encounters |

**Clinical — Diagnoses & Care Plans (5 schemas, 24 fields)**

| Schema | Fields | Description |
|---|---|---|
| Diagnosis | 7 | Diagnosis history with ICD codes, eye location, qualifier, resolution date |
| DiagnosisCarePlanItem | 2 | Links diagnoses to care plan items |
| CarePlanItem | 4 | Care plan entries with type, dates, description |
| HealthGoal | 5 | Patient health goals with status tracking |
| HealthConcern | 6 | Health concerns with type, reporter, status |

**Clinical — Other (7 schemas, 69 fields)**

| Schema | Fields | Description |
|---|---|---|
| Allergy | 7 | Allergies with severity, reactions, treatment |
| Immunization | 16 | Immunizations with CVX codes, administration details, lot info |
| ImplantableDevice | 7 | UDI-tracked devices with location, surgeon |
| VitalSigns | 9 | BP (systolic/diastolic), pulse, height, weight with units |
| MedicalOrder | 30 | Lab orders with LOINC codes, results, values, units, interpretation |
| SocialHistory | 6 | Tobacco, drinking, smoking status |
| ClinicalDecisionSupport | 8 | CDS rules with SNOMED exception codes |

**Clinical — Family History & Referrals (3 schemas, 27 fields)**

| Schema | Fields | Description |
|---|---|---|
| FamilyHealthHistory | 11 | SNOMED-coded conditions with per-relationship flags (father, mother, brother, sister, son, daughter) |
| FamilyHistory | 3 | Encounter-level medical and ocular family conditions (string arrays) |
| Referral | 13 | Referral tracking with response dates, report receipt status |

**Specialty — Optometry (3 schemas, 23 fields)**

| Schema | Fields | Description |
|---|---|---|
| Refraction | 19 | Full OD/OS refraction: sphere, cylinder, axis, horizontal/vertical prism with orientation, intermediate/near add |
| Test | 2 | Generic name/values structure for diagnostic equipment readings |
| TestValue | 2 | Name-value pairs for test results |

**Financial — Billing & Insurance (6 schemas, 37 fields)**

| Schema | Fields | Description |
|---|---|---|
| Insurance | 6 | Coverage: company, type, relationship, policy, group, payer ID |
| Invoice | 7 | Billing invoices with bill-to, dates, status; nests items, payments, claims |
| InvoiceItem | 12 | Line items with CPT codes, modifiers, pricing (unit price, discounts, tax, extended price, adjustments, paid, balance) |
| Payment | 3 | Payment records with date, method, amount |
| Claim | 5 | Claim submission tracking with dates, methods, status messages |
| Statement | 4 | Billing statements with print date, due date, message, balance |

**Root (1 schema, 17 fields)**

| Schema | Fields | Description |
|---|---|---|
| Patient | 17 | Root object with export timestamp and references to all domain arrays |

Full schema details are in `analysis/full-entity-inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export is organized as a single nested JSON object per patient. The richest schemas are:

- **MedicalOrder** (30 fields) — the most detailed schema, covering lab orders and results with LOINC codes, result values, units, interpretation, specimen source, and comments
- **Encounter** (19 fields) — visits with nested structured clinical data (but no narrative notes)
- **Refraction** (19 fields) — optometry-specific refraction data with full OD/OS measurements including prism
- **Demographics** (17 fields) — standard patient identity with address, employment, and contact info
- **Immunization** (16 fields) — detailed administration records with CVX codes and lot tracking
- **Referral** (13 fields) — referral workflow with response tracking

The financial domain is genuinely covered: Invoice → InvoiceItem → Payment → Claim forms a complete billing chain from services through claims to payments, with 31 fields across 5 schemas. This is stronger billing coverage than many EHI exports.

The optometry specialty data (Refraction, Test/TestValue) captures the core clinical measurement data unique to eye care. The `Test` schema's generic name/value structure allows flexible capture of diverse diagnostic equipment readings.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Demographics` (17 fields), `Address` (5), `Contact` (4), `FamilyMember` (4), `Employment` (4) | Thorough — name, DOB, sex, race, ethnicity, language, address, phone, email, employment |
| Encounters / visits | ✅ Covered | `Encounter` (19 fields) with nested diagnoses, vitals, refractions, tests, services, history | Good structured data; no narrative note text |
| Problems / conditions / diagnoses | ✅ Covered | `Diagnosis` (7 fields), `EncounterDiagnosis` (3 fields) with ICD codes and eye-specific qualifiers | Includes optometry-specific eye location and qualifier fields |
| Medications / prescriptions | ❌ Not covered | No Medication or Prescription schema | Product uses RXNT for e-prescribing; medication lists and prescription history absent from export. Significant gap — medication data is used for patient care decisions |
| Allergies | ✅ Covered | `Allergy` (7 fields) with severity, reactions, treatment | Adequate |
| Immunizations | ✅ Covered | `Immunization` (16 fields) with CVX codes, administration details, lot info | Thorough |
| Vitals | ✅ Covered | `VitalSigns` (9 fields) — BP, pulse, height, weight | Adequate for optometry context |
| Lab results | ✅ Covered | `MedicalOrder` (30 fields) with LOINC codes, results, values, units, interpretation | Most detailed schema in the export |
| Imaging / diagnostic reports | ❌ Not covered | No image or document schema | Product includes PACS for retinal photos, OCT images, visual fields, corneal topography. No image export documented. Significant gap |
| Procedures | ⚠️ Partial | `Service` (3 fields) within encounters captures CPT codes | Basic — code and description only; no procedure detail |
| Clinical notes / documents | ❌ Not covered | No field for encounter notes, progress notes, or clinical narrative | Encounters capture structured data but no free-text documentation. Significant gap for a system with customizable exam templates |
| Care plans / goals | ✅ Covered | `CarePlanItem` (4 fields), `HealthGoal` (5), `HealthConcern` (6), `DiagnosisCarePlanItem` (2) | Adequate |
| Orders / referrals | ✅ Covered | `MedicalOrder` (30 fields), `Referral` (13 fields) | Thorough, with response tracking for referrals |
| Insurance / coverage | ✅ Covered | `Insurance` (6 fields) | Basic but sufficient — company, coverage type, policy, group, payer ID |
| Claims / billing | ✅ Covered | `Invoice` (7), `InvoiceItem` (12), `Payment` (3), `Claim` (5), `Statement` (4) — 31 fields total | Strong — full billing chain from services through claims to payments |
| Payments | ✅ Covered | `Payment` (3 fields) nested within Invoice | Basic — date, method, amount |
| Consents / directives | ❌ Not covered | No consent or advance directive schema | Unclear whether product stores consents beyond intake forms |
| Patient communications / portal | ❌ Not covered | No portal messages, intake forms, surveys, or communication schema | Product has patient portal (RevIntake/IntakeQ), automated reminders, surveys. This data is absent |
| Specialty-specific (optometry) | ⚠️ Partial | `Refraction` (19 fields), `Test`/`TestValue` (4 fields) | Refraction data is well-covered. However, **optical dispensing data** (eyeglass/contact lens prescriptions, frame selections, lens orders, optical inventory, supplier order tracking) is entirely absent despite being a major functional area of the product |

## 6. Documentation Quality

**Strengths:**
- The OpenAPI 3.0.1 specification is machine-readable and structurally sound — a developer could auto-generate a JSON parser from it
- All 279 fields have explicit types (100% coverage) with format annotations (date, date-time, double, int32, int64)
- Inter-schema relationships are expressed via `$ref` references (37 total)
- Required fields are documented per schema (72 fields marked required)

**Weaknesses:**
- Descriptions are mostly trivial: 96.1% of fields have descriptions, but most restate the field name (e.g., `city` → "City", `diastolic` → "Diastolic blood pressure"). Only 68.5% have descriptions going beyond the field name
- **No value sets or enumerations** for coded fields — `severity`, `status`, `smokingStatus`, `submitMethod`, `coverageType`, `encounterType`, `category`, `role` are all plain strings with no documented valid values
- **No sample data** — a developer cannot verify their parser without trial and error
- **No user guide** — the only export instructions are two sentences on the certification disclosures page ("Single patient export is available within RevolutionEHR in the Admin module under Patient Management. Population export is available upon request by contacting customer support.")
- No versioning beyond "1.0" with no change history

A developer could build a parser from this specification, but would struggle to interpret the semantics of coded fields and would have no way to validate against expected output.

## 7. Overall Assessment

### Classification

**Partial native export** — This is a genuine, purpose-built b(10) export using the vendor's own data model (not C-CDA or FHIR repackaging). It covers clinical structured data and billing well, with optometry-specific extensions (refraction data). However, it has significant coverage gaps: no medications/prescriptions, no clinical notes, no images/PACS data, no optical dispensing data, and no patient portal data — all of which are core functional areas of this optometry EHR.

### Key Findings

1. **Genuine b(10) export, clearly separate from FHIR API**: The export uses a proprietary JSON format documented via OpenAPI spec, distinct from their g(10) FHIR API powered by Dynamic Health IT. This is a purpose-built effort, not a repackaged clinical summary.

2. **Billing coverage is notably strong**: The Invoice → InvoiceItem → Payment → Claim → Statement chain (31 fields across 5 schemas) provides a complete financial record. Many EHI exports omit billing entirely; RevolutionEHR includes the full lifecycle from service coding through claims submission to payment receipt.

3. **Optical dispensing data — the product's core differentiator — is entirely absent**: RevolutionEHR is primarily an optometry practice management system. Eyeglass prescriptions, contact lens prescriptions, frame selections, lens orders, optical inventory, and supplier order tracking are all absent from the export despite being central to the product's value proposition.

4. **No medications/prescriptions exported**: The product integrates with RXNT for e-prescribing. Medication lists and prescription history are not represented in any schema. Whether this data lives in RevolutionEHR's database or solely in RXNT is unclear, but medication data is unquestionably EHI.

5. **No clinical notes or narrative documentation**: Encounters capture structured data (diagnoses, vitals, tests, services) but there is no field for progress notes, clinical narrative, or the text content of customizable exam templates — a significant gap for a system whose exam documentation is a primary feature.

### Summary Stats

    Classification:  Partial native export
    Export format:   Proprietary JSON
    Model type:      Native (vendor-specific schema)
    Entities:        35 schemas
    Fields:          279
    Descriptions:    96.1% have descriptions; 68.5% non-trivial
    Value sets:      None documented
    Sample data:     No
    Bulk export:     Yes (upon request to customer support)
    Domains covered: 11 of 17 applicable domains (3 partial)

### Bottom Line

RevolutionEHR's EHI export is a genuine effort — a purpose-built proprietary JSON format with machine-readable documentation and real billing data. However, it falls short of "all EHI" by omitting several major data domains the product stores: optical dispensing (the product's core specialty), medications/prescriptions, clinical notes, ophthalmic images, and patient portal data. A patient would receive their demographics, structured encounter data, refraction measurements, billing records, and lab results — but not their eyeglass or contact lens prescriptions, clinical note narratives, retinal images, or medication history.
