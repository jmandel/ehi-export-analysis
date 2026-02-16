# EHI Export Analysis: Azalea Health

**Product**: ChartAccess ®
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2688.Char.07.01.1.221227 (CHPL 11140)

## 1. Product Context

ChartAccess is Azalea Health's **hospital EHR** designed for rural and critical access hospitals, covering inpatient, emergency department, and hospital-based outpatient settings. It is part of the broader Azalea Health platform which includes:

- **Clinical EHR**: Patient demographics, problem lists, medication lists, allergies, vital signs, CPOE, lab ordering/results, clinical notes, care plans, clinical decision support, implantable device tracking
- **Practice Management**: Patient scheduling, registration, insurance verification, patient kiosk
- **Revenue Cycle Management (RCM)**: Integrated billing, claim scrubbing/submission, denials management, A/R management, patient collections, charge capture, financial analytics
- **Patient Engagement**: myHealthspot patient portal (secure messaging, bill pay, lab results, appointment requests), integrated telehealth, MyPractice mobile app
- **Hospital-specific**: Inpatient admissions, ED workflows, EMAR (medication administration), nursing orders, dietary orders, cardiology/therapy orders, flowsheets
- **Interoperability**: FHIR R4 API, C-CDA exchange, AzaleaConnect HIE, public health reporting

The product has broad clinical and billing capabilities. A complete EHI export should cover clinical data, billing/financial records, patient portal communications, and hospital-specific workflows.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/compliance_b10.html` (18 KB) | (b)(10) EHI Export overview — describes export format (NDJSON), scope (Patient compartment + Location, Practitioner, Binary), single-patient and population export mechanisms | **High** — primary export specification |
| `downloads/hospital_export.html` (23 KB) | Hospital EHI Export Guide — **45 EHR concept-to-FHIR resource mappings** in a table | **High** — the closest thing to a data dictionary |
| `downloads/hospital_resources.html` (37 KB) | Hospital FHIR resources page — lists supported resource types with interactions | Medium — context for API capabilities |
| `downloads/capability-statement-hospital.json` (92 KB) | FHIR R4 CapabilityStatement — 36 resource types with search params | **High** — machine-readable resource/interaction inventory |
| `downloads/implementation_bulk-data-export.html` (18 KB) | Bulk Data Export API endpoints — kick-off, status polling, file download | Medium — export mechanics |
| `downloads/implementation_bulk-data-access.html` (30 KB) | Backend Services authorization (OAuth 2.0 client_credentials) | Low — auth plumbing |
| `downloads/hospital_overview.html` (14 KB) | Hospital API architecture overview | Low — general context |
| `downloads/onc-certification-page.html` (307 KB) | ONC certification landing page with links | Low — navigation page |
| `downloads/screenshot-b10-overview.png` (413 KB) | Screenshot of (b)(10) overview page | Low — visual of HTML already captured |
| `downloads/screenshot-hospital-export-guide.png` (373 KB) | Screenshot of hospital export guide | Low — visual of HTML already captured |
| `downloads/enrichment/export-mappings.json` (51 KB) | Prior agent's extracted mappings JSON | Medium — reference for validation |

## 3. Export Mechanics

- **Format**: FHIR R4 NDJSON (Newline-delimited JSON). Each file contains one FHIR resource type, named `{Resource}_{identifier}.ndjson`.
- **Scope**: All data in the [FHIR Patient compartment](https://hl7.org/fhir/R4/compartmentdefinition-patient.html) plus Location, Practitioner, and Binary resources. Unstructured documents included as base64-encoded Binary resources or inline in DocumentReference.
- **Single-patient export**: Available via in-app UI (runs in background) or via API using `Patient/$export?_typeFilter=Patient?_id=1234`.
- **Population export**: Contact support to initiate (free of charge), or use API (`Patient/$export` or `Group/$export`).
- **Access**: API requires OAuth 2.0 Backend Services authorization (client_credentials). UI export available to authorized users.
- **Fees**: Explicitly stated as no charge.
- **CapabilityStatement**: Instantiates `http://hl7.org/fhir/uv/bulkdata/CapabilityStatement/bulk-data` and `http://hl7.org/fhir/us/core/CapabilityStatement/us-core-server`. Patient resource has `$export-resource` operation.

## 4. Export Content: What's In It

The Hospital EHI Export Guide (`hospital_export.html`) provides a mapping table of **45 EHR concepts** to **24 unique FHIR resource types**. This is the vendor's only export content documentation — there is **no field-level data dictionary**, no value sets, no sample data, and no schema beyond the FHIR resource type names.

The CapabilityStatement declares **36 FHIR resource types** with search parameters but no field-level documentation.

### Documentation depth

- **45 EHR concepts** mapped to FHIR resources (concept-to-resource-type level only)
- **0 fields** documented at the field/element level
- **10 of 45** mappings include FHIR path notes (e.g., `Condition.where(category.coding.code = "encounter-diagnosis")`)
- **0 value sets** or coded value documentation
- **0 sample data** files
- **No foreign key/relationship documentation** beyond what FHIR resource references imply

### Vendor's own content organization

The vendor maps 45 EHR concepts to FHIR resources. The table below reproduces this mapping exactly as documented:

| EHR Concept | FHIR Resource | Notes | Category (assigned) |
|---|---|---|---|
| Admissions | Encounter | | Encounters & Scheduling |
| Allergies | AllergyIntolerance | | Allergies |
| Amendments | Communication | | Clinical Notes & Documents |
| Appointments | Appointment | | Encounters & Scheduling |
| Cardiology Execution | Procedure | | Procedures |
| Cardiology Order | ServiceRequest | | Orders |
| Care Level | Condition | | Problems / Conditions |
| Chart Notes (All) | DocumentReference | | Clinical Notes & Documents |
| Diagnoses | Condition | `Condition.where(category.coding.code = "encounter-diagnosis")` | Problems / Conditions |
| Dietary | NutritionOrder | | Orders |
| EMAR | MedicationAdministration | | Medications |
| Files | DocumentReference | | Clinical Notes & Documents |
| Financial Account | Account | | Financial / Billing |
| Flowsheets | Observation | | Flowsheets / Observations |
| Immunizations | Immunization | | Immunizations |
| Implantable Devices | Device | | Other |
| Laboratory Orders | ServiceRequest | | Laboratory |
| Laboratory Reports | DiagnosticReport | | Laboratory |
| Laboratory Results | Observation | `Observation.where(category.coding.code = "laboratory")` | Laboratory |
| Locations | Location | | Administrative |
| Medication History | MedicationStatement | | Medications |
| Medication Orders | MedicationRequest | | Medications |
| Nursing Orders | ServiceRequest | | Orders |
| Patient Death Report | Observation | | Demographics & Patient Info |
| Patient Demographics | Patient | | Demographics & Patient Info |
| Patient Emergency Contact | Patient | `Patient.contact.where(relationship.code = "C")` | Demographics & Patient Info |
| Patient Lactating Status | Condition | | Problems / Conditions |
| Patient Memo | Flag | | Patient Communications |
| Patient Portal Messages | Communication | `Communication.where(sender.type = "Patient") or Communication.where(recipient.type = "Patient")` | Patient Communications |
| Patient Preferred Pharmacy | HealthcareService | | Pharmacy |
| Patient Pregnancy Status | Condition | | Problems / Conditions |
| Payments | PaymentReconciliation | | Financial / Billing |
| Problem History | Condition | `Condition.where(category.coding.code = "patient-problem-list")` | Problems / Conditions |
| Procedure History | Procedure | | Procedures |
| Providers | Practitioner | | Administrative |
| Radiology Orders | ServiceRequest | | Radiology / Imaging |
| Radiology Reports | DiagnosticReport | | Radiology / Imaging |
| Radiology Results | Observation | `Observation.where(category.coding.code = "laboratory")` | Radiology / Imaging |
| Sexual Orientation | Observation | `Observation.where(code.coding.code = "76690-7")` | Social History |
| Smoking Status | Observation | `Observation.where(code.coding.code = "72166-2")` | Social History |
| Social History | Observation | `Observation.where(category.coding.code = "social-history")` | Social History |
| Supplies | SupplyRequest | | Other |
| Therapy Execution | Procedure | | Procedures |
| Therapy Order | ServiceRequest | | Orders |
| Vital Signs | Observation | `Observation.where(category.coding.code = "vital-signs")` | Vitals |

**Category breakdown** (45 concepts across 19 categories):

| Category | Concept Count | Concepts |
|---|---|---|
| Problems / Conditions | 5 | Care Level, Diagnoses, Patient Lactating Status, Patient Pregnancy Status, Problem History |
| Orders | 4 | Cardiology Order, Dietary, Nursing Orders, Therapy Order |
| Clinical Notes & Documents | 3 | Amendments, Chart Notes (All), Files |
| Procedures | 3 | Cardiology Execution, Procedure History, Therapy Execution |
| Medications | 3 | EMAR, Medication History, Medication Orders |
| Laboratory | 3 | Laboratory Orders, Laboratory Reports, Laboratory Results |
| Demographics & Patient Info | 3 | Patient Death Report, Patient Demographics, Patient Emergency Contact |
| Radiology / Imaging | 3 | Radiology Orders, Radiology Reports, Radiology Results |
| Social History | 3 | Sexual Orientation, Smoking Status, Social History |
| Encounters & Scheduling | 2 | Admissions, Appointments |
| Financial / Billing | 2 | Financial Account, Payments |
| Patient Communications | 2 | Patient Memo, Patient Portal Messages |
| Administrative | 2 | Locations, Providers |
| Other | 2 | Implantable Devices, Supplies |
| Allergies | 1 | Allergies |
| Flowsheets / Observations | 1 | Flowsheets |
| Immunizations | 1 | Immunizations |
| Pharmacy | 1 | Patient Preferred Pharmacy |
| Vitals | 1 | Vital Signs |

### CapabilityStatement vs Export Mapping discrepancies

- **16 resources in CapabilityStatement but NOT in export mapping**: AuditEvent, Binary, CapabilityStatement, CarePlan, CareTeam, Coverage, Goal, InsurancePlan, MedicationDispense, Organization, PractitionerRole, Provenance, QuestionnaireResponse, RelatedPerson, Specimen, StructureDefinition. Many of these (CarePlan, CareTeam, Coverage, Goal, InsurancePlan, Provenance, QuestionnaireResponse, RelatedPerson) are Patient compartment resources and likely *are* exported via the Patient compartment scope but not explicitly listed in the mapping table.
- **4 resources in export mapping but NOT in CapabilityStatement**: Appointment, Account, Flag, PaymentReconciliation. These may be exported through a different mechanism or the CapabilityStatement may be incomplete.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export mapping covers 45 EHR concepts organized across clinical, financial, and administrative domains. Key observations:

**Strengths beyond typical USCDI exports:**
- **Hospital-specific clinical concepts**: EMAR (MedicationAdministration), Flowsheets, Nursing Orders, Cardiology Orders/Executions, Therapy Orders/Executions, Dietary (NutritionOrder), Supplies (SupplyRequest), Care Level — these go well beyond standard USCDI scope and reflect genuine hospital EHR data.
- **Financial data**: Financial Account (Account) and Payments (PaymentReconciliation) are explicitly included.
- **Patient communications**: Patient Portal Messages and Patient Memo (Flag) are included.
- **Unstructured data**: Binary resources for images/documents, Chart Notes (All), Files, Amendments.
- **Specialty observations**: Patient Pregnancy Status, Patient Lactating Status, Patient Death Report.

**Thinness in documentation:**
- No field-level detail for any of the 45 concepts — the mapping only tells you *which* FHIR resource type, not what fields are populated or how EHR-specific data is mapped.
- No vendor-specific extensions or profiles documented (though the CapabilityStatement does reference US Core profiles).
- No information about how EHR-specific fields (beyond FHIR base spec) are represented.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient Demographics, Patient Emergency Contact, Sexual Orientation | Covered via Patient + Observation |
| Encounters / visits | ✅ Covered | Admissions → Encounter, Appointments → Appointment | Covers inpatient admissions; appointments also included |
| Problems / conditions / diagnoses | ✅ Covered | Diagnoses, Problem History, Care Level, Patient Pregnancy/Lactating Status → Condition | 5 distinct condition concepts mapped |
| Medications / prescriptions | ✅ Covered | Medication Orders → MedicationRequest, Medication History → MedicationStatement, EMAR → MedicationAdministration | Includes MAR — beyond typical USCDI |
| Allergies | ✅ Covered | Allergies → AllergyIntolerance | Standard coverage |
| Immunizations | ✅ Covered | Immunizations → Immunization | Standard coverage |
| Vitals | ✅ Covered | Vital Signs → Observation | Standard coverage |
| Lab results | ✅ Covered | Laboratory Results → Observation, Laboratory Reports → DiagnosticReport, Laboratory Orders → ServiceRequest | Full orders-results-reports chain |
| Imaging / diagnostic reports | ✅ Covered | Radiology Orders, Reports, Results → ServiceRequest, DiagnosticReport, Observation | Full orders-results-reports chain |
| Procedures | ✅ Covered | Procedure History, Cardiology Execution, Therapy Execution → Procedure | Hospital-specific procedure types |
| Clinical notes / documents | ✅ Covered | Chart Notes (All), Files, Amendments → DocumentReference, Communication; Binary for unstructured data | Broad: "All" chart notes plus files |
| Care plans / goals | ⚠️ Partial | Not in export mapping table, but CarePlan and Goal are in CapabilityStatement (Patient compartment) | Likely exported via compartment scope but not explicitly documented |
| Orders / referrals | ✅ Covered | Cardiology Order, Nursing Orders, Therapy Order, Lab Orders, Radiology Orders, Dietary → ServiceRequest, NutritionOrder | 6 distinct order types — granular |
| Insurance / coverage | ⚠️ Partial | Not in export mapping table, but Coverage and InsurancePlan are in CapabilityStatement | Likely exported via compartment scope but not explicitly documented |
| Claims / billing | ⚠️ Partial | Financial Account → Account, Payments → PaymentReconciliation | Some billing data present, but no claims, charges, CPT/ICD coding detail, superbills, or denial management data visible. Product has full RCM capabilities. |
| Payments | ✅ Covered | Payments → PaymentReconciliation | Explicitly included |
| Consents / directives | ❌ Not covered | No consent or advance directive entities in mapping or CapabilityStatement | Product likely stores consents; gap |
| Patient communications / portal messages | ✅ Covered | Patient Portal Messages → Communication | Explicitly includes portal messages |
| Specialty-specific (Cardiology, Therapy) | ✅ Covered | Cardiology Order/Execution, Therapy Order/Execution → ServiceRequest/Procedure | Hospital-specific specialty data included |

### Key domain gaps

1. **Claims / billing depth**: While Financial Account and Payments are present, the product has full RCM capabilities (claim scrubbing, submission, denials management, A/R, charge capture). No Claims, ExplanationOfBenefit, ChargeItem, or detailed billing entities are documented in the export. This is a significant gap given the product's billing capabilities.
2. **Insurance / Coverage**: Coverage and InsurancePlan are in the CapabilityStatement but not in the export mapping table — ambiguous whether they're actually exported.
3. **Care plans / Goals**: Similarly in CapabilityStatement but not mapped — ambiguous.
4. **Consents**: No evidence of consent or advance directive export.

## 6. Documentation Quality

**Positives:**
- The vendor provides a dedicated (b)(10) page with clear export mechanics (format, scope, mechanism)
- The Hospital EHI Export Guide provides a mapping of 45 EHR concepts to FHIR resources — more granular than many vendors
- A machine-readable CapabilityStatement (92 KB JSON) is available with 36 resource types and search parameters
- Export is free, available for both single-patient and population, with both UI and API access

**Negatives:**
- **No field-level data dictionary**: The mapping only identifies which FHIR resource type each EHR concept maps to, not which fields are populated, what extensions are used, or how EHR-specific data is represented within each resource
- **No sample data**: No example NDJSON files to verify actual output
- **No value sets or code systems**: No documentation of coded values used
- **No vendor-specific extensions**: No profiles or extensions documented (despite the export likely needing them for hospital-specific data like care levels, flowsheets, financial accounts)
- **Ambiguous scope**: 16 CapabilityStatement resources are not in the export mapping — it's unclear whether they're exported via the Patient compartment scope or excluded
- **A developer could not build an import from this documentation alone**: They would know the FHIR resource types but not the actual field population, extensions, or data specifics

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export covers clinical domains well — 45 EHR concepts spanning demographics, encounters, problems, medications (including EMAR), labs, radiology, procedures, notes/documents, orders, vitals, immunizations, allergies, social history, and patient communications. This meaningfully exceeds USCDI scope with hospital-specific concepts (EMAR, flowsheets, nursing orders, cardiology/therapy orders, dietary, supplies, care levels). However, the product's full RCM capabilities (claim scrubbing, denials management, A/R, charge capture) are barely represented — only Financial Account and Payments are mapped, with no claims, charges, or coding detail. Insurance/coverage is ambiguously present. This is a genuine gap for a product that markets integrated billing as a core feature.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly not a simple repackaging of the (g)(10) API. The vendor built a dedicated export mapping table with 45 EHR concepts — many of which go beyond USCDI and US Core (EMAR, Flowsheets, Nursing Orders, Cardiology/Therapy Orders/Executions, Dietary, Supplies, Financial Account, Payments, Patient Memo, Patient Portal Messages, Amendments, Patient Death Report, Care Level, Patient Lactating/Pregnancy Status). The export uses FHIR resource types not in the standard US Core profile set (Account, Flag, NutritionOrder, SupplyRequest, PaymentReconciliation, MedicationAdministration, Appointment, HealthcareService). The vendor also includes 4 resource types (Account, Appointment, Flag, PaymentReconciliation) that aren't even in their own CapabilityStatement, suggesting the export was designed to go beyond the standard API surface. The export explicitly mentions Binary resources for unstructured data. This represents genuine (b)(10) engagement, even though billing coverage is incomplete.

### Key Findings

1. **Genuine purpose-built export with hospital-specific concepts**: The 45-concept mapping table includes EMAR, flowsheets, nursing/cardiology/therapy orders, dietary orders, supplies, care levels, and financial data — well beyond USCDI repackaging.
2. **No field-level documentation**: The mapping provides only concept→FHIR resource type (with occasional FHIR path notes for 10 of 45 concepts). No field-level detail, no extensions, no value sets, no sample data. A developer cannot determine what specific data elements are exported.
3. **Billing/RCM gap**: Despite the product having full billing/RCM capabilities (claims, denials, A/R, charge capture), only Financial Account and Payments are in the export. No claims, charges, or coding detail.
4. **Ambiguous CapabilityStatement overlap**: 16 resources are in the CapabilityStatement but not the export mapping (including Coverage, InsurancePlan, CarePlan, Goal). These may be exported via Patient compartment scope but it's unclear.
5. **Free export with both UI and API access**: The vendor provides single-patient UI export, API-based export, and vendor-assisted population export at no charge.

### Summary Stats

    Coverage:        Partial
    Approach:        Purpose-built EHI export
    Export format:   FHIR R4 NDJSON (Bulk Data Export)
    Entities:        45 EHR concepts mapped to 24 FHIR resource types
    Fields:          N/A (no field-level documentation)
    Descriptions:    N/A (concept-level mapping only)
    Sample data:     No
    Bulk export:     Yes (API and vendor-assisted)
    Domains covered: 14 of 18 applicable domains (4 partial/missing: claims depth, insurance, care plans, consents)

### Bottom Line

Azalea Health built a genuine (b)(10) export for ChartAccess that goes meaningfully beyond USCDI, mapping 45 hospital-specific EHR concepts to FHIR resources including EMAR, flowsheets, orders, financial accounts, and patient communications. The biggest gap is billing depth — the product has full RCM capabilities but exports only account-level and payment data, omitting claims, charges, and denials. The documentation is concept-level only, with no field-level detail, making it impossible to assess actual data completeness within each exported resource.
