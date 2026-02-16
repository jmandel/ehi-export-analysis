# EHI Export Analysis: Azalea Health

**Product**: Azalea EHR
**Analysis date**: 2026-02-16
**CHPL ID**: 15.04.04.2688.Azal.04.02.1.221227 (CHPL #11151)

## 1. Product Context

Azalea Health is a cloud-based EHR, practice management, and revenue cycle management platform focused on rural hospitals, critical access hospitals, and community-based ambulatory clinics. The company originated as a billing company and acquired Prognosis Innovation Healthcare in 2017, adding hospital capabilities. The product serves both **ambulatory** and **hospital** settings from a single platform.

Key capabilities relevant to EHI completeness:
- **Clinical EHR** (ambulatory & hospital): charting, problem lists, medications, allergies, labs, vitals, clinical notes, CPOE, e-prescribing (EPCS), immunizations, care plans
- **Practice Management**: scheduling, patient registration, insurance verification
- **Revenue Cycle Management**: claim scrubbing, submission, denial management, payment posting, A/R management — core to the company's origin
- **Patient Portal (myHealthspot)**: secure messaging, lab results, bill pay, appointment requests
- **Telehealth**: integrated video visits saved to patient record
- **Hospital-specific**: ADT, EMAR, dietary orders, nursing orders, ED management
- **Analytics**: enterprise data warehouse, KPI dashboards, CQM/MIPS reporting

The product's billing/RCM roots and integrated PM module mean billing, financial, and insurance data are central to what the product stores.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Value |
|---|---|---|---|
| `b10-main.html` | 18 KB | §170.315(b)(10) EHI Export overview page | **High** — defines export format (NDJSON), scope (Patient compartment + Location + Practitioner), and single/population export mechanisms |
| `ambulatory-export.html` | 27 KB | Ambulatory EHI Export Guide with 57 EHR concept → FHIR resource mappings | **Highest** — primary data dictionary for ambulatory export |
| `hospital-export.html` | 23 KB | Hospital EHI Export Guide with 45 EHR concept → FHIR resource mappings | **Highest** — primary data dictionary for hospital export |
| `ambulatory-capability-statement.json` | 197 KB | FHIR R4 CapabilityStatement declaring 50 resource types | **Medium** — confirms resource types and interactions |
| `hospital-capability-statement.json` | 92 KB | FHIR R4 CapabilityStatement declaring 36 resource types | **Medium** — confirms resource types and interactions |
| `ambulatory-profiles.html` | 35 KB | 51 custom profile definitions | **Medium** — resource-level descriptions but no field-level detail |
| `ambulatory-extensions.html` | 37 KB | 72 custom extension definitions | **High** — reveals vendor-specific data elements beyond base FHIR |
| `ambulatory-resources.html` | 62 KB | Resource catalog for ambulatory platform | **Low** — general descriptions |
| `hospital-resources.html` | 37 KB | Resource catalog for hospital platform | **Low** — general descriptions |
| `bulk-data-export.html` | 18 KB | Bulk Data Export implementation guide | **Medium** — API mechanics |
| `uscore-mappings.html` | 28 KB | USCDI to FHIR resource mappings | **Low** — standard US Core mapping |
| `ambulatory-overview.html` | 18 KB | Ambulatory platform overview | **Low** |
| `hospital-overview.html` | 14 KB | Hospital platform overview | **Low** |

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON (one file per resource type, named `{Resource}_{identifier}.ndjson`)
- **Mechanism**: 
  - **Single patient**: In-app UI button; also available via Bulk Data Export API with `_typeFilter=Patient?_id=1234`
  - **Population export**: Via Bulk Data Export API (`Patient/$export` or `Group/[id]/$export`); alternatively, contact support for vendor-assisted delivery
  - API follows FHIR Bulk Data Export spec (async kick-off → status polling → NDJSON download)
- **Single-patient**: Yes (UI + API)
- **Bulk**: Yes (API; vendor-assisted also available)
- **Fees**: Explicitly stated: "There is no charge for this export type"
- **Access constraints**: API requires SMART on FHIR authorization; scoped to pre-authorized resource types

## 4. Export Content: What's In It

### Overview

The export is organized as a mapping from internal **EHR concepts** to **FHIR R4 resources**. The ambulatory platform maps 57 EHR concepts to 30 FHIR resource types; the hospital platform maps 45 EHR concepts to 24 FHIR resource types. Combined, 81 unique EHR concepts are mapped to 34 distinct FHIR resource types.

The documentation provides concept-level mappings (e.g., "Encounter (Billing) → Claim") with filter notes (e.g., `Claim.where(use = "claim")`), but does **not** provide field-level detail — there is no list of individual data elements/fields within each resource, no data types, no value sets, and no sample data. Field-level detail is partially supplemented by:
- **51 custom profile definitions** (resource-level descriptions only)
- **72 custom FHIR extensions** (extension name + description per extension)

### Vendor's own content organization

The vendor organizes content by EHR concept with platform-specific guides. Below are the complete mapping tables.

#### Ambulatory Export (57 concepts)

| EHR Concept | FHIR Resource | Notes | Category |
|---|---|---|---|
| Allergies | AllergyIntolerance | | Allergies |
| Appointments | Appointment | | Encounters & Scheduling |
| Care Plans | CarePlan | | Care Plans & Goals |
| Care Plans (Goals) | Goal | | Care Plans & Goals |
| Care Teams | CareTeam | | Care Plans & Goals |
| Chart Evaluation Tables (Answers) | QuestionnaireResponse | | Assessments & Questionnaires |
| Chart Plan Note | DocumentReference | type = "11506-3" | Clinical Notes & Documents |
| Chart Procedure Note | DocumentReference | type = "28570-0" | Clinical Notes & Documents |
| Chart Subjective (PMH) Note | DocumentReference | type = "34117-2" | Clinical Notes & Documents |
| Documents | DocumentReference | | Clinical Notes & Documents |
| Encounter (Billing) | Claim | use = "claim" | Billing & Financial |
| Encounter (Clinical) | Encounter | | Encounters & Scheduling |
| Encounter Diagnoses | Condition | category = "encounter-diagnosis" | Problems & Diagnoses |
| Encounter Financial Account | Account | type.text = "charge-group" | Billing & Financial |
| Encounter Procedures | Procedure | | Procedures |
| Family History | FamilyMemberHistory | | Family History |
| Health Concerns | Condition | category = "health-concern" | Problems & Diagnoses |
| Immunizations | Immunization | | Immunizations |
| Implantable Devices | Device | | Devices |
| Insurance | Coverage | | Insurance |
| Laboratory Orders | ServiceRequest | | Laboratory |
| Laboratory Reports | DiagnosticReport | | Laboratory |
| Laboratory Results | Observation | category = "laboratory" | Laboratory |
| Locations | Location | | Administrative |
| Medications | MedicationStatement | | Medications |
| Patient Classes | Group | code.text = "patient-group" | Administrative |
| Patient Comments | Flag | category.text = "patient-comment" | Patient Communications |
| Patient Demographics | Patient | | Demographics & Contacts |
| Patient Documents | DocumentReference | | Clinical Notes & Documents |
| Patient Emergency Contact | Patient | contact.relationship = "C" | Demographics & Contacts |
| Patient Employer | Patient | contact.relationship = "E" | Demographics & Contacts |
| Patient Employment Status | Observation | code = "224362002" | Social History & Observations |
| Patient Financial Account | Account | type.text = "financial-account" | Billing & Financial |
| Patient Guarantor | RelatedPerson | relationship = "GUAR" | Billing & Financial |
| Patient Handouts | DocumentReference | type = "51855-5" | Clinical Notes & Documents |
| Patient Next of Kin | Patient | contact.relationship = "next-of-kin" | Demographics & Contacts |
| Patient Popup Comments | Flag | category.text = "patient-popup" | Patient Communications |
| Patient Portal Messages | Communication | sender/recipient type = "Patient" | Patient Communications |
| Patient Power of Attorney | RelatedPerson | relationship = "GUARD" | Demographics & Contacts |
| Patient Statements | Invoice | | Billing & Financial |
| Patient Travel History | Observation | code = "443846001" | Social History & Observations |
| Patient Urls | DocumentReference | type = "51899-3" | Clinical Notes & Documents |
| Payments (Applied + Unapplied) | PaymentReconciliation | | Billing & Financial |
| Pre-Certifications | Claim | use = "preauthorization" | Billing & Financial |
| Prescriptions | MedicationRequest | | Medications |
| Problem History | Condition | category = "patient-problem-list" | Problems & Diagnoses |
| Procedure History | Procedure | | Procedures |
| Providers | Practitioner | | Administrative |
| Radiology Orders | ServiceRequest | | Radiology / Imaging |
| Radiology Reports | DiagnosticReport | | Radiology / Imaging |
| Radiology Results | Observation | category = "laboratory" | Radiology / Imaging |
| Recalls | CarePlan | category.text = "recall" | Care Plans & Goals |
| Sexual Orientation | Observation | code = "76690-7" | Social History & Observations |
| Smoking Status | Observation | code = "72166-2" | Social History & Observations |
| Social History | Observation | category = "social-history" | Social History & Observations |
| Social Questions (Answers) | QuestionnaireResponse | | Assessments & Questionnaires |
| Vital Signs | Observation | category = "vital-signs" | Vital Signs |

#### Hospital Export (45 concepts)

| EHR Concept | FHIR Resource | Notes | Category |
|---|---|---|---|
| Admissions | Encounter | | Encounters & Scheduling |
| Allergies | AllergyIntolerance | | Allergies |
| Amendments | Communication | | Clinical Notes & Documents |
| Appointments | Appointment | | Encounters & Scheduling |
| Cardiology Execution | Procedure | | Cardiology |
| Cardiology Order | ServiceRequest | | Cardiology |
| Care Level | Condition | | Problems & Diagnoses |
| Chart Notes (All) | DocumentReference | | Clinical Notes & Documents |
| Diagnoses | Condition | category = "encounter-diagnosis" | Problems & Diagnoses |
| Dietary | NutritionOrder | | Dietary / Nutrition |
| EMAR | MedicationAdministration | | Medications |
| Files | DocumentReference | | Clinical Notes & Documents |
| Financial Account | Account | | Billing & Financial |
| Flowsheets | Observation | | Flowsheets |
| Immunizations | Immunization | | Immunizations |
| Implantable Devices | Device | | Devices |
| Laboratory Orders | ServiceRequest | | Laboratory |
| Laboratory Reports | DiagnosticReport | | Laboratory |
| Laboratory Results | Observation | category = "laboratory" | Laboratory |
| Locations | Location | | Administrative |
| Medication History | MedicationStatement | | Medications |
| Medication Orders | MedicationRequest | | Medications |
| Nursing Orders | ServiceRequest | | Nursing |
| Patient Death Report | Observation | | Patient Status |
| Patient Demographics | Patient | | Demographics & Contacts |
| Patient Emergency Contact | Patient | contact.relationship = "C" | Demographics & Contacts |
| Patient Lactating Status | Condition | | Patient Status |
| Patient Memo | Flag | | Patient Communications |
| Patient Portal Messages | Communication | sender/recipient type = "Patient" | Patient Communications |
| Patient Preferred Pharmacy | HealthcareService | | Pharmacy |
| Patient Pregnancy Status | Condition | | Patient Status |
| Payments | PaymentReconciliation | | Billing & Financial |
| Problem History | Condition | category = "patient-problem-list" | Problems & Diagnoses |
| Procedure History | Procedure | | Procedures |
| Providers | Practitioner | | Administrative |
| Radiology Orders | ServiceRequest | | Radiology / Imaging |
| Radiology Reports | DiagnosticReport | | Radiology / Imaging |
| Radiology Results | Observation | category = "laboratory" | Radiology / Imaging |
| Sexual Orientation | Observation | code = "76690-7" | Social History & Observations |
| Smoking Status | Observation | code = "72166-2" | Social History & Observations |
| Social History | Observation | category = "social-history" | Social History & Observations |
| Supplies | SupplyRequest | | Supplies |
| Therapy Execution | Procedure | | Therapy |
| Therapy Order | ServiceRequest | | Therapy |
| Vital Signs | Observation | category = "vital-signs" | Vital Signs |

#### Custom Extensions (72 total)

The 72 custom FHIR extensions demonstrate vendor-specific data fields beyond base FHIR. Notable groups:

| Extension Group | Count | Examples |
|---|---|---|
| Patient extensions | 13 | Citizenship, Occupation, Religion, Annual Income, Household Members, Preferred Contact Method |
| Invoice (billing statements) | 10 | Line Item Charges, Adjustments, Payments, Subtotal, Payer, Visit Date |
| Account (financial) | 9 | Aging Buckets, Balance Amount, Unapplied Amount, Related Parts, Location ID |
| Appointment | 5 | Reminder Eligibility/Status, Requested State, Status History, Reason Color |
| Claim | 5 | Insurance Referral, Authorization Number, NDC Quantity, NOC, Third Party Liability |
| Schedule | 5 | Start/End Time, Slot Interval, Insurance, Insurance Class |
| Encounter | 4 | Class, Note, Signature, Status |
| Coverage | 3 | Medicare Secondary Reason, Note, Vaccines Covered |
| Other | 18 | Billing Code, ChargeItem Note, RxNorm TTY Code, Communication Read Flag, etc. |

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

Azalea organizes their EHI export as two platform-specific guides. The ambulatory guide is broader (57 concepts) and includes a significant billing/financial section. The hospital guide (45 concepts) adds hospital-specific clinical workflows.

**Strongest areas:**
- **Billing & Financial** (8 concepts): Claims, payments (applied + unapplied), patient statements (Invoice), financial accounts (both encounter-level and patient-level), pre-certifications, guarantor relationships. The 72 custom extensions add significant depth here — 10 Invoice extensions, 9 Account extensions, 5 Claim extensions, and a billing code extension.
- **Demographics & Contacts** (7 concepts): Patient demographics, emergency contact, next of kin, employer, employment status, guarantor, power of attorney. 13 patient-specific extensions add fields like citizenship, religion, occupation, income, household members.
- **Clinical Notes & Documents** (9 concepts): Multiple clinical note types (plan, procedure, PMH), documents, patient documents, handouts, files, amendments.
- **Patient Communications** (4 concepts): Portal messages, patient comments, popup comments, patient memos.

**Hospital-specific additions:**
- EMAR (MedicationAdministration), cardiology orders/executions, therapy orders/executions, nursing orders, dietary orders (NutritionOrder), flowsheets, supplies, patient death reports, pregnancy/lactating status

**Thinnest areas:**
- No concept-level field/element documentation — only mappings to FHIR resource types
- No sample data or example resources

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient Demographics`, `Patient Emergency Contact`, `Patient Employer`, `Patient Next of Kin`, `Patient Power of Attorney`, `Patient Employment Status` + 13 Patient extensions (citizenship, religion, occupation, income, household members) | Thorough — extends well beyond USCDI demographics |
| Encounters / visits | ✅ Covered | `Encounter (Clinical)`, `Admissions`, `Appointments` | Covered for both ambulatory and inpatient |
| Problems / conditions / diagnoses | ✅ Covered | `Problem History`, `Encounter Diagnoses`, `Health Concerns`, `Diagnoses`, `Care Level` | Covered |
| Medications / prescriptions | ✅ Covered | `Medications` (MedicationStatement), `Prescriptions` (MedicationRequest), `Medication Orders`, `Medication History`, `EMAR` (MedicationAdministration) | Strong — includes MAR for hospital |
| Allergies | ✅ Covered | `Allergies` (AllergyIntolerance) + 2 extensions (category/severity SNOMED coding) | Covered |
| Immunizations | ✅ Covered | `Immunizations` (Immunization) | Covered |
| Vitals | ✅ Covered | `Vital Signs` (Observation), `Flowsheets` (hospital) | Covered |
| Lab results | ✅ Covered | `Laboratory Results`, `Laboratory Reports`, `Laboratory Orders` | Full lab chain (order → report → results) |
| Imaging / diagnostic reports | ✅ Covered | `Radiology Orders`, `Radiology Reports`, `Radiology Results` | Full radiology chain |
| Procedures | ✅ Covered | `Encounter Procedures`, `Procedure History`, `Cardiology Execution`, `Therapy Execution` | Covered including specialty procedures |
| Clinical notes / documents | ✅ Covered | `Chart Plan Note`, `Chart Procedure Note`, `Chart Subjective (PMH) Note`, `Chart Notes (All)`, `Documents`, `Patient Documents`, `Files`, `Patient Handouts`, `Amendments` | Thorough — multiple note types + uploaded files |
| Care plans / goals | ✅ Covered | `Care Plans`, `Care Plans (Goals)`, `Care Teams`, `Recalls` | Covered |
| Orders / referrals | ✅ Covered | Lab/Radiology/Nursing/Cardiology/Therapy orders via ServiceRequest, `Pre-Certifications` via Claim | Multiple order types |
| Insurance / coverage | ✅ Covered | `Insurance` (Coverage) + 3 Coverage extensions (Medicare Secondary Reason, Note, Vaccines Covered) | Covered |
| Claims / billing | ✅ Covered | `Encounter (Billing)` (Claim), `Pre-Certifications` (Claim), 5 Claim extensions | Beyond USCDI — real claims data |
| Payments | ✅ Covered | `Payments (Applied + Unapplied)` (PaymentReconciliation), `Patient Statements` (Invoice) + 10 Invoice extensions, PaymentReconciliation Gateway extension | Genuine billing depth |
| Patient communications / portal messages | ✅ Covered | `Patient Portal Messages` (Communication), `Patient Comments` (Flag), `Patient Popup Comments` (Flag), `Patient Memo` (Flag) + Communication Read Flag extension | Covered |
| Assessments / questionnaires | ✅ Covered | `Chart Evaluation Tables (Answers)`, `Social Questions (Answers)` (QuestionnaireResponse) | Custom forms exported |
| Social history | ✅ Covered | `Social History`, `Smoking Status`, `Sexual Orientation`, `Patient Employment Status`, `Patient Travel History` | Beyond USCDI |
| Family history | ✅ Covered | `Family History` (FamilyMemberHistory) | Covered |
| Devices | ✅ Covered | `Implantable Devices` (Device) | Covered |
| Specialty: Cardiology | ✅ Covered | `Cardiology Order`, `Cardiology Execution` (hospital) | Hospital-specific specialty coverage |
| Specialty: Dietary/Nutrition | ✅ Covered | `Dietary` (NutritionOrder) — hospital | Hospital-specific |
| Specialty: Therapy | ✅ Covered | `Therapy Order`, `Therapy Execution` (hospital) | Hospital-specific |
| Consents / directives | ❌ Not covered | No consent-related concepts in export | Product likely stores consent forms (patient portal has them); minor gap |
| Telehealth records | ⚠️ Partial | Not explicitly listed as a concept, but telehealth visits are "automatically saved to patient record" per product docs, so they may appear as Encounters | Unclear if telehealth metadata is fully captured |

**N/A domains**: The product does not appear to do dental, oncology-specific, or correctional health, so those absences are not gaps.

## 6. Documentation Quality

**Strengths:**
- Clear export format specification (NDJSON, FHIR R4)
- Well-documented API mechanics (Bulk Data Export spec with examples)
- 72 custom extensions reveal vendor-specific data fields not in base FHIR
- Separate guides for ambulatory (57 concepts) and hospital (45 concepts) platforms
- FHIR filter expressions (e.g., `Condition.where(category.coding.code = "encounter-diagnosis")`) help disambiguate multi-use resources

**Weaknesses:**
- **No field-level data dictionary**: The documentation maps EHR concepts to FHIR resource types but does not enumerate individual fields/elements. A developer would need to rely on the FHIR R4 base spec + the 51 profile definitions + 72 extensions to reconstruct the full schema.
- **No sample data**: No example NDJSON files or representative resources are provided.
- **Profile definitions are bare**: 51 profiles are listed with resource-level descriptions only — no element constraints, cardinality, Must Support flags, or slicing details.
- **No machine-readable schema beyond CapabilityStatement**: The StructureDefinitions for profiles and extensions are presumably available at the FHIR endpoint but not documented in the developer portal content reviewed.

**Could a developer build an import?** Partially. The FHIR resource type mappings and extensions give a structural roadmap, but without field-level profiles or sample data, a developer would need to discover the actual data shape empirically by requesting exports and inspecting the NDJSON.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

Azalea's EHI export covers a genuinely broad set of data domains relative to what the product stores. The 81 combined EHR concepts span demographics, clinical data, billing/financial, patient communications, custom forms, and hospital-specific workflows. Critically, the export includes:
- **Billing data**: Claims, payments (applied + unapplied), patient statements, pre-certifications, financial accounts — with 24+ custom extensions adding billing-specific fields (Invoice line items, Account aging, PaymentReconciliation gateway details). This is especially significant given Azalea's origins as a billing company.
- **Beyond-USCDI concepts**: 31 ambulatory and 30 hospital concepts go beyond standard USCDI scope (portal messages, guarantors, financial accounts, patient statements, pre-certifications, cardiology, dietary, nursing, therapy, etc.)
- **Hospital-specific data**: EMAR, nursing orders, dietary orders, cardiology, therapy, flowsheets, supplies

The only notable gap is the absence of explicit consent/directive records.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built (b)(10) export, not a repackaged (g)(10) or C-CDA export. Key evidence:
1. **Dedicated EHI Export Guides**: Separate pages for ambulatory and hospital EHI export with platform-specific EHR concept mappings, distinct from the US Core / g(10) documentation
2. **Non-USCDI resource types**: The export uses FHIR resource types not part of US Core / g(10) — including Claim, Invoice, PaymentReconciliation, Account, Flag, Communication, NutritionOrder, MedicationAdministration, SupplyRequest, Group, HealthcareService
3. **72 custom extensions**: Vendor-built extensions specifically mapping internal billing, scheduling, and clinical data fields to FHIR — these don't exist in any standard IG
4. **Coverage far exceeds g(10)**: The ambulatory CapabilityStatement has 50 resource types vs. the ~26 needed for US Core; the export mappings explicitly include billing, financial accounts, patient statements, and pre-certifications

### Key Findings

1. **Genuinely deep billing/financial export**: With Claim, Invoice, PaymentReconciliation, Account resources and 24+ custom billing/financial extensions, Azalea exports real financial data. The Invoice extensions (line item charges, adjustments, payments, subtotals, payers) demonstrate genuine EHR-specific mapping, not just FHIR boilerplate.

2. **81 EHR concepts across two platforms exceed USCDI**: 31 ambulatory concepts and 30 hospital concepts go beyond USCDI scope, including patient communications, financial records, specialty orders (cardiology, therapy), dietary orders, and EMAR.

3. **Documentation lacks field-level detail**: While the concept-to-resource mappings and custom extensions are well-documented, there is no field-level data dictionary, no sample data, and profiles are listed without element-level constraints. This limits the usability of the documentation for building imports.

4. **Separate ambulatory and hospital guides show platform awareness**: The vendor maintains distinct export specifications for each platform, with hospital-specific concepts (EMAR, nursing/dietary/therapy orders, flowsheets) that demonstrate genuine engagement with inpatient data.

5. **FHIR-native approach is well-executed**: Rather than dumping raw database tables, Azalea mapped their internal data model to FHIR R4 resources with custom extensions — a more interoperable approach that still captures vendor-specific data.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   FHIR R4 NDJSON
Entities:        81 EHR concepts (57 ambulatory + 45 hospital, 81 combined unique)
Fields:          N/A (no field-level data dictionary; 72 custom extensions documented)
Descriptions:    N/A (concept-level descriptions only)
Sample data:     No
Bulk export:     Yes (Bulk Data Export API + vendor-assisted)
Domains covered: 22 of 23 applicable domains
```

### Bottom Line

Azalea Health has built a genuinely purpose-built EHI export that covers the breadth of what their product stores, including billing/financial data, patient communications, hospital-specific workflows, and custom assessments — all mapped to FHIR R4 with 72 vendor-specific extensions. The main weakness is the lack of field-level documentation: the export tells you *which* data domains are covered via concept-to-resource mappings, but doesn't enumerate the specific fields within each resource, making it harder for consumers to build imports without empirical discovery. Despite this documentation gap, the coverage breadth is among the stronger (b)(10) implementations.
