# EHI Export Analysis: MedAZ.Net, LLC

**Product**: Med A-Z (version 202001)
**Analysis date**: 2026-02-16
**CHPL ID**: 15.05.05.3150.MDAZ.01.00.1.230616

## 1. Product Context

Med A-Z is a fully integrated ambulatory EHR, practice management, and billing/revenue cycle management suite developed by MedAZ.Net, LLC (a subsidiary of KATSI). It targets small-to-mid-size physician practices and bundles free EHR/PM software with revenue cycle management services. The product consists of three tightly integrated modules:

- **EHR Plus**: Demographics, chief complaints, allergies, medications, medical/surgical/family/social history, review of systems, vitals, diagnoses, treatment plans, CPOE for meds/labs/imaging, e-prescribing (Surescripts), HL7 lab interfaces (Quest, LabCorp), drug interaction checking, clinical decision support, clinical notes, quality measures.
- **Practice Plus**: Scheduling, insurance management, check-in/rooming/checkout workflows, real-time patient tracking, referral letters, multi-location support.
- **Billing Plus**: Electronic claims submission, claims scrubbing (LMRP edits, CCI compliance), HCFA forms, claim status tracking, procedure/diagnosis code linking, credit card payment processing, revenue cycle analytics.

This product profile means a genuine (b)(10) export should cover: clinical data (demographics, encounters, diagnoses, medications, allergies, labs, vitals, immunizations, procedures, notes, imaging, devices), billing data (claims, charges, payments, procedure/diagnosis codes), insurance information, scheduling/visit data, referrals, and any custom forms or templates.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `certificationinfo.html` (15 KB) | Main certification page; lists certified criteria, costs, and links to FHIR API documentation. The (b)(10) section points only to FHIR APIs. | **High** — establishes that vendor equates (b)(10) with their FHIR API |
| `swagger-single-patient.json` (531 KB) | OpenAPI 3.0.1 spec for single-patient FHIR API. 90 paths, 81 schemas (all generic FHIR infrastructure types). | **Medium** — confirms API scope but no product-specific schemas |
| `swagger-bulk.json` (272 KB) | OpenAPI 3.0.1 spec for bulk FHIR API. 37 paths including Group/$export. | **Medium** — confirms bulk export mechanism |
| `fhir-capability-statement-single.json` (22 KB) | CapabilityStatement: FHIR R4, US Core 3.1.1, 20 resource types, all standard US Core profiles. | **High** — definitive list of supported resources and profiles |
| `fhir-capability-statement-bulk.json` (22 KB) | CapabilityStatement for bulk API. Identical resource types and profiles. | **Low** — duplicates single-patient CS |
| `fhirsingle.xml` (29 KB) | FHIR Bundle of Endpoint resources. Lists 19 resource types. | **Low** — confirms resource list |
| `fhirsystosys.xml` (25 KB) | FHIR Bundle of Endpoint resources for bulk API. Same 19 types. | **Low** — duplicates |
| `screenshot-certification-page.png` (588 KB) | Full-page screenshot of certification page. | **Low** — visual confirmation of HTML content |
| `screenshot-swagger-single-patient.png` (167 KB) | Screenshot of Swagger UI for single-patient API. | **Low** — visual confirmation |
| `screenshot-swagger-bulk.png` (143 KB) | Screenshot of Swagger UI for bulk API. | **Low** — visual confirmation |

**No data dictionary, no sample data, no product-specific schema documentation, and no field-level documentation were found in any artifact.**

## 3. Export Mechanics

- **Format**: FHIR R4 JSON, conforming to US Core IG v3.1.1
- **Mechanism**: Two FHIR APIs:
  - Single-patient API (`fhirapi.mhealthaz.com`) — 90 endpoints for per-resource CRUD and search
  - Bulk export API (`fhirbulk.mhealthaz.com`) — implements FHIR Bulk Data Access via `Group/{id}/$export`
- **Single-patient vs bulk**: Both supported. Bulk uses the standard FHIR Bulk Data Access polling pattern (`$export` → `$export-poll-status` → `/download`)
- **Access constraints**: Requires SMART on FHIR authorization. Application registration endpoint exists in the API. The certification page notes "Data extraction in custom formats" incurs fees, but "no fees for extraction in ONC certified formats like QRDA1, CCD, etc." — unclear if the FHIR API is fee-free.
- **Notable**: The implementation URL in the CapabilityStatement is an ngrok tunnel (`https://21f7-173-72-103-2.ngrok.io`), suggesting the FHIR server may run on-premise behind a temporary tunnel rather than on dedicated infrastructure.

## 4. Export Content: What's In It

The export provides exactly the 20 FHIR resource types defined by US Core 3.1.1, with no extensions, no custom profiles, and no vendor-specific documentation:

### Vendor's own content organization

The vendor provides no product-specific data dictionary or content organization. The only documentation is the standard FHIR CapabilityStatement and Swagger UI, which list standard US Core resource types. The Swagger schemas contain only generic FHIR infrastructure types (Bundle, CapabilityStatement, Element, etc.) — no resource-specific field definitions.

| Resource Type | Profiles | Category (USCDI) | In Bulk API | Vendor Schema |
|---|---|---|---|---|
| AllergyIntolerance | us-core-allergyintolerance | Allergies & Intolerances | Yes | No |
| CarePlan | us-core-careplan | Assessment & Plan of Treatment | Yes | No |
| CareTeam | us-core-careteam | Care Team Members | Yes | No |
| Condition | us-core-condition | Problems | Yes | No |
| Device | us-core-implantable-device | Medical Devices | Yes | No |
| DiagnosticReport | us-core-diagnosticreport-lab, us-core-diagnosticreport-note | Labs / Imaging | Yes | No |
| DocumentReference | us-core-documentreference | Clinical Notes | Yes | No |
| Encounter | us-core-encounter | Encounters | Yes | No |
| Goal | us-core-goal | Goals | Yes | No |
| Immunization | us-core-immunization | Immunizations | Yes | No |
| Location | us-core-location | Facility Information | Yes | No |
| Medication | us-core-medication | Medications | Yes | No |
| MedicationRequest | us-core-medicationrequest | Medications | Yes | No |
| Observation | 13 profiles (vitals, labs, smoking, pediatric) | Vitals / Labs / Clinical Tests | Yes | No |
| Organization | us-core-organization | Facility Information | Yes | No |
| Patient | us-core-patient | Demographics | Yes | No |
| Practitioner | us-core-practitioner | Care Team | Yes | No |
| PractitionerRole | us-core-practitionerrole | Care Team | Yes | No |
| Procedure | us-core-procedure | Procedures | Yes | No |
| Provenance | (no profile specified) | Provenance | Yes | No |

**Total**: 20 resource types, all standard US Core profiles, 0 vendor extensions, 0 vendor-specific field definitions.

The Observation resource supports 13 standard profiles covering vitals (BP, height, weight, heart rate, respiratory rate, temperature, SpO2, BMI) and lab results, plus pediatric measurements — all part of the US Core specification.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no custom organization of their export content. The entire export is the US Core 3.1.1 resource set — the exact same set of resources exposed via their (g)(10) Standardized API. The certification page's "Data Exchange/Extraction" section links directly to the same FHIR API endpoints used for (g)(10) compliance, with no separate (b)(10) documentation, no additional data sources, and no indication that the export includes anything beyond the standard clinical exchange surface.

The Swagger APIs confirm this: the single-patient API has 90 paths and the bulk API has 37 paths, but all map to the same 20 US Core resource types. The Swagger schemas (81 in the single-patient spec, 72 in bulk) are all generic FHIR infrastructure types (Bundle, CapabilityStatement, Element, Coding, etc.) — none are product-specific resource definitions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (US Core profile) | Standard USCDI fields only; product stores richer demographics |
| Encounters / visits | ✅ Covered | Encounter resource (US Core profile) | Standard fields; product's check-in/rooming/checkout workflow data not captured |
| Problems / conditions | ✅ Covered | Condition resource (US Core profile) | Standard USCDI scope |
| Medications / prescriptions | ✅ Covered | Medication, MedicationRequest (US Core profiles) | Standard; product has Surescripts e-prescribing integration with potentially richer data |
| Allergies | ✅ Covered | AllergyIntolerance (US Core profile) | Standard USCDI scope |
| Immunizations | ✅ Covered | Immunization (US Core profile) | Standard USCDI scope |
| Vitals | ✅ Covered | Observation (13 vital sign profiles) | Good vital sign coverage per US Core |
| Lab results | ✅ Covered | Observation (lab profile), DiagnosticReport (lab profile) | Standard; product has HL7 interfaces with Quest/LabCorp — raw HL7 data not exported |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport (note profile) | Only note-type reports; no imaging-specific data beyond narrative |
| Procedures | ✅ Covered | Procedure (US Core profile) | Standard USCDI scope |
| Clinical notes / documents | ✅ Covered | DocumentReference (US Core profile) | Standard USCDI scope |
| Care plans / goals | ✅ Covered | CarePlan, Goal (US Core profiles) | Standard USCDI scope |
| Orders / referrals | ⚠️ Partial | MedicationRequest covers medication orders | No ServiceRequest; product has CPOE for labs/imaging and referral letters — these are not exported |
| Insurance / coverage | ❌ Not covered | No Coverage resource | Product stores insurance info extensively (Practice Plus module); significant gap |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing resources | Product has full billing module (Billing Plus); major gap |
| Payments | ❌ Not covered | No PaymentReconciliation or payment resources | Product processes payments including credit card; significant gap |
| Consents / directives | ❌ Not covered | No Consent resource | Unknown if product stores these |
| Patient communications | ❌ Not covered | No Communication resources | Unknown if product has portal messaging |
| Specialty-specific | N/A | — | Product is general-purpose ambulatory; no specialty modules identified |

**Summary**: 11 of 18 applicable domains covered (all USCDI clinical domains), 3 partially covered, 4 not covered. All coverage gaps are in billing, insurance, payments, and administrative domains — exactly the domains that distinguish a genuine (b)(10) export from a repackaged (g)(10).

## 6. Documentation Quality

The export documentation is extremely thin:

- **No data dictionary**: There is no product-specific documentation of what fields are included in each resource, what value sets are used, or how the product's internal data maps to FHIR resources.
- **No sample data**: No example exports, sample FHIR bundles, or test patient data are provided.
- **No schemas beyond standard FHIR**: The Swagger specs define only generic FHIR infrastructure schemas. Individual resource types return generic `Bundle` responses with no product-specific structure.
- **No mapping documentation**: No documentation describes how the product's internal data model (EHR Plus, Practice Plus, Billing Plus tables) maps to FHIR resources.
- **Only standard references**: The certification page links to HL7.org FHIR and HL7 standards pages — no product-specific documentation.

A developer attempting to use this export would need to:
1. Register an application via the SMART on FHIR flow
2. Call standard US Core endpoints
3. Hope that the returned resources contain the data they need
4. Have no way to know what product-specific data is or isn't included

The CapabilityStatement implementation URL pointing to an ngrok tunnel raises additional concerns about API availability and stability.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only the 20 US Core resource types — the exact USCDI floor for clinical exchange. Med A-Z is a three-module product (EHR + Practice Management + Billing), and the export completely omits two of those three modules. No billing data (claims, charges, HCFA forms, claim status), no insurance details, no payment records, no scheduling data, and no practice management workflow data are included. The export represents roughly the clinical summary portion of what the product stores. Given the product explicitly includes "Billing Plus" with claims submission, scrubbing, and revenue cycle management, the absence of any billing data in the export is a significant completeness gap.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of a vendor pointing their (g)(10) FHIR API at (b)(10) and calling it done. The evidence is overwhelming:
1. The certification page's "Data Exchange/Extraction" section links to the same FHIR API endpoints used for (g)(10)
2. Both CapabilityStatements declare US Core 3.1.1 with exclusively standard US Core profiles
3. No vendor extensions, no custom profiles, no product-specific schemas
4. No separate (b)(10) documentation or data dictionary
5. The bulk export API implements standard FHIR Bulk Data Access — the exact mechanism required for (g)(10)
6. No billing, insurance, or practice management resources are included

### Key Findings

1. **The (b)(10) export IS the (g)(10) API**: The certification page provides identical FHIR API links for both criteria. The CapabilityStatements, Swagger specs, and endpoint lists are the same. There is no separate (b)(10) export mechanism or data source.

2. **Zero vendor-specific documentation**: No data dictionary, no field-level documentation, no mapping from internal data model to FHIR, no sample data. A developer cannot determine what product-specific data is included without calling the API and inspecting responses.

3. **Entire billing module absent**: Med A-Z's Billing Plus module handles claims, HCFA forms, payment processing, and revenue cycle management. None of this data appears in the export. This is patient-specific billing information that is squarely within the designated record set.

4. **Practice management data absent**: Insurance information, scheduling, check-in/checkout workflows, referral tracking — all stored by the Practice Plus module — are not exported.

5. **Infrastructure concerns**: The FHIR server's CapabilityStatement implementation URL points to an ngrok tunnel, suggesting the API may not be running on dedicated, always-available infrastructure.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   FHIR R4 JSON (US Core 3.1.1)
Entities:        20 (standard US Core resource types)
Fields:          N/A (no vendor-specific field documentation)
Descriptions:    N/A
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data Access)
Domains covered: 11 of 18 applicable domains (USCDI clinical only)
```

### Bottom Line

Med A-Z's (b)(10) export is simply their (g)(10) FHIR API relabeled. A patient or provider would receive only standard USCDI clinical data — demographics, conditions, medications, labs, vitals, notes, and procedures — with no billing records, no insurance details, no payment history, and no practice management data, despite the product storing all of this. The single biggest gap is the complete absence of the Billing Plus module's data (claims, charges, payments), which represents a core part of the designated record set for a product whose business model centers on integrated billing services.
