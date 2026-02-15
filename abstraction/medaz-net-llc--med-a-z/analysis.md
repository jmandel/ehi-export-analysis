# EHI Export Analysis: MedAZ.Net, LLC

**Product**: Med A-Z (version 202001)
**Analysis date**: 2026-02-15
**CHPL ID**: 15.05.05.3150.MDAZ.01.00.1.230616 (CHPL #11300)

## 1. Product Context

Med A-Z Complete is a fully integrated EHR, Practice Management, and Billing/Revenue Cycle Management suite developed by MedAZ.Net, LLC (a subsidiary of KATSI). It targets ambulatory physician practices, from solo practitioners to multi-physician groups. Certified June 16, 2023, the product covers both clinical and administrative workflows.

The product consists of three tightly integrated modules:

- **EHR Plus**: Patient demographics, chief complaints, allergies, medications, medical/surgical/family/social history, review of systems, vitals, problem lists, treatment plans, lab orders/results (Quest, LabCorp, regional labs via HL7), diagnostic imaging orders, e-prescribing (Surescripts), drug interaction checking, clinical decision support, CPOE, clinical quality measures, and clinical notes with customizable templates.
- **Practice Plus**: Patient scheduling, insurance management, check-in/checkout workflows, real-time patient location tracking, copay collection, referral preparation, and multi-location support.
- **Billing Plus**: Electronic claims submission, claims scrubbing, HCFA form generation, procedure/diagnosis code linking, payment processing, claim status tracking, and revenue cycle analytics.

This product profile means the EHI export should cover clinical data, billing/claims data, insurance information, and practice management data — not just the USCDI clinical summary.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `certificationinfo.html` (15 KB) | Main certification page at medaz.com. Lists certified criteria (including (b)(10)), costs, and "Data Exchange/Extraction" section. The sole source of (b)(10) documentation. | **High** — establishes that the vendor's only EHI export documentation is links to FHIR APIs |
| `swagger-single-patient.json` (531 KB) | OpenAPI 3.0.1 spec for single-patient FHIR API. 90 paths, 106 schema definitions, 19 FHIR resource types. | **Medium** — confirms API scope is standard US Core |
| `swagger-bulk.json` (272 KB) | OpenAPI 3.0.1 spec for bulk FHIR API. 37 paths, 94 schema definitions. Includes Group-level `$export` endpoint. | **Medium** — confirms bulk export is FHIR Bulk Data Access |
| `fhir-capability-statement-single.json` (22 KB) | FHIR CapabilityStatement from single-patient API. Declares 20 resource types, all US Core profiles, FHIR R4 (4.0.1). | **High** — definitively shows only standard US Core resources, no extensions |
| `fhir-capability-statement-bulk.json` (22 KB) | FHIR CapabilityStatement from bulk API. Same 20 resource types and US Core profiles as single-patient. | **High** — confirms bulk API has identical scope to single-patient |
| `fhirsingle.xml` (29 KB) | FHIR Bundle with 19 Endpoint resources for single-patient API. Lists resource type URLs. | **Low** — service discovery, duplicates CapabilityStatement info |
| `fhirsystosys.xml` (25 KB) | FHIR Bundle with 19 Endpoint resources for bulk API. Same resource types as single-patient. | **Low** — same as above |
| `screenshot-certification-page.png` (588 KB) | Full-page screenshot of the certification page. | **Low** — visual confirmation of HTML content |
| `screenshot-swagger-single-patient.png` (167 KB) | Screenshot of Swagger UI for single-patient API. | **Low** — visual confirmation |
| `screenshot-swagger-bulk.png` (143 KB) | Screenshot of Swagger UI for bulk API. | **Low** — visual confirmation |

No data dictionary, no sample data, no export format documentation, no field-level documentation, and no EHI-specific documentation were found. Verified by probing 8 additional URL paths on medaz.com — all returned 404.

## 3. Export Mechanics

- **Format**: FHIR R4 (4.0.1) resources conforming to US Core Implementation Guide v3.1.1
- **Mechanism**: FHIR RESTful API (single-patient) and FHIR Bulk Data Access API (bulk export via `Group/{id}/$export`)
- **Single-patient**: Yes — via single-patient FHIR API with search, pagination, read, vread, and history operations
- **Bulk capability**: Yes — via FHIR Bulk Data Access with Group-level export, poll status, and download endpoints
- **Access constraints**: API access requires application registration (endpoints at `/myapplication/*` in single-patient spec). The certification page notes "Data extraction in custom formats" incurs fees, but "no fees for extraction in ONC certified formats like QRDA1, CCD, etc." It is unclear whether the FHIR API is considered fee-free or falls under "custom formats."
- **Initiation**: API-based; no evidence of a UI-initiated export workflow

The vendor's "Data Exchange/Extraction" section on the certification page links directly to the FHIR API Swagger documentation and FHIR endpoint service discovery files. There is no separate EHI export mechanism — the (b)(10) certification points entirely to the (g)(10) FHIR API.

## 4. Export Content: What's In It

The export consists exclusively of standard FHIR R4 US Core resources. There is no vendor-specific data dictionary, no native database export, no field-level documentation, and no sample data.

### FHIR Resource Types (20 total)

Both the single-patient and bulk APIs expose the same 20 resource types, all using standard US Core profiles with no vendor extensions:

| Resource Type | US Core Profile | Category |
|---|---|---|
| Patient | us-core-patient | Demographics |
| AllergyIntolerance | us-core-allergyintolerance | Clinical |
| CarePlan | us-core-careplan | Clinical |
| CareTeam | us-core-careteam | Clinical |
| Condition | us-core-condition | Clinical |
| Device | us-core-implantable-device | Clinical |
| DiagnosticReport | us-core-diagnosticreport-lab, us-core-diagnosticreport-note | Clinical |
| DocumentReference | us-core-documentreference | Clinical |
| Encounter | us-core-encounter | Clinical |
| Goal | us-core-goal | Clinical |
| Immunization | us-core-immunization | Clinical |
| Medication | us-core-medication | Clinical |
| MedicationRequest | us-core-medicationrequest | Clinical |
| Observation | us-core-smokingstatus, us-core-observation-lab, vitals profiles (BP, height, weight, HR, RR, temp, pulse oximetry, pediatric BMI/weight, head circumference) | Clinical |
| Procedure | us-core-procedure | Clinical |
| Provenance | (none specified) | Metadata |
| Location | us-core-location | Administrative |
| Organization | us-core-organization | Administrative |
| Practitioner | us-core-practitioner | Administrative |
| PractitionerRole | us-core-practitionerrole | Administrative |

This is exactly the standard US Core / USCDI v1 resource set. No custom profiles, no vendor extensions, and no resources beyond what (g)(10) requires. The CapabilityStatements declare no implementation guides (the `implementationGuide` array is empty), though the descriptions reference "US Core Implementation Guide v3.1.1."

### What's Not In the Export

Based on the product's documented capabilities (Section 1), the following data domains stored by Med A-Z have no representation in the FHIR API:

- **Billing/claims data**: Claims, HCFA forms, charge records, claim status — the entire Billing Plus module
- **Insurance/coverage information**: Insurance plans, coverage details — no Coverage or InsurancePlan resources
- **Payment records**: Copay collection, payment processing, credit/debit transactions
- **Scheduling data**: Appointments, scheduling — no Schedule or Appointment resources
- **E-prescribing transaction history**: Surescripts transaction details beyond basic MedicationRequest
- **Drug interaction alerts**: Drug-drug, drug-allergy, drug-procedure alerts and history
- **Clinical decision support records**: Disease management prompts, under/over-coding detection
- **Clinical quality measures data**: CQM recording and reporting data (QRDA-1 export exists separately but is not part of this API)
- **Patient education materials**: Tracking/logging of education delivered
- **Referral correspondence**: Referral letters
- **Cardiovascular risk assessments**: Framingham calculations
- **Custom clinical templates**: One-click diagnostic templates, auto-populated HPI/exam/treatment plans

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no categorization or organization of its export beyond the FHIR API structure. The export is simply the standard set of 20 US Core FHIR resource types. There are no vendor-specific groupings, no data dictionary sections, and no acknowledgment that the product stores data beyond what the FHIR API exposes.

The vendor's "Data Exchange/Extraction" section on the certification page lists:
- **Standards**: HL7 and HL7 FHIR
- **Documentation**: Swagger UI for single-patient and bulk APIs
- **Endpoints**: FHIR endpoint discovery files
- **Preferred Formats**: QRDA-1 and CCD-A

This is a standards-only view — the vendor describes data exchange exclusively in terms of interoperability standards (FHIR, CCD-A, QRDA-1), not in terms of the product's actual data model or complete data set.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | `Patient` resource (US Core) | Basic demographics via FHIR Patient. Product stores richer data (contacts, insurance info per Practice Plus) not fully represented. |
| Encounters / visits | ⚠️ Partial | `Encounter` resource (US Core) | Basic encounter data. Product's detailed check-in/checkout workflow data, patient location tracking not captured. |
| Problems / conditions | ✅ Covered | `Condition` resource (US Core) | Standard condition/problem list. |
| Medications / prescriptions | ⚠️ Partial | `Medication`, `MedicationRequest` resources | Basic medication data. Product's e-prescribing transaction history (Surescripts), drug interaction alerts not included. |
| Allergies | ✅ Covered | `AllergyIntolerance` resource (US Core) | Standard allergy data. |
| Immunizations | ✅ Covered | `Immunization` resource (US Core) | Standard immunization records. |
| Vitals | ✅ Covered | `Observation` resource with 13 vital sign profiles | Comprehensive vital signs coverage including BP, height, weight, HR, RR, temp, pulse oximetry, pediatric measures. |
| Lab results | ✅ Covered | `DiagnosticReport` (lab), `Observation` (lab) | Standard lab results. Product integrates with Quest/LabCorp — unclear if all interface data (raw HL7 messages) is preserved. |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport` (note) | Diagnostic report notes available. Product supports CPOE for diagnostic imaging and PACS interfaces — imaging orders and PACS data likely not fully captured. |
| Procedures | ✅ Covered | `Procedure` resource (US Core) | Standard procedure records. |
| Clinical notes / documents | ⚠️ Partial | `DocumentReference` resource (US Core) | Documents available. Product's customizable templates, auto-populated HPI/exam/plans — unclear how much vendor-specific structure is preserved vs flattened to documents. |
| Care plans / goals | ✅ Covered | `CarePlan`, `Goal`, `CareTeam` resources | Standard care plan data. |
| Orders / referrals | ❌ Not covered | No ServiceRequest or referral-specific resource | Product supports CPOE for meds/labs/imaging and referral letter preparation. No order or referral resources in export. |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resources | Product manages "unlimited insurance plan configuration" per Practice Plus. Significant gap. |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing resources | Product has entire Billing Plus module (claims, HCFA forms, claims scrubbing, payment processing). Major gap. |
| Payments | ❌ Not covered | No PaymentReconciliation or payment resources | Product handles copay collection, credit/debit processing. Gap. |
| Consents / directives | ❌ Not covered | No Consent resource | No evidence of consent/directive export. |
| Patient communications | N/A | No patient portal documented | Product may lack active patient portal (not certified for (e)(1)). |

**Summary**: 7 of 17 applicable domains have at least adequate coverage. 4 domains are partially covered. 5 domains with known product data are completely absent from the export. The entire billing/financial layer — arguably the largest data domain in this integrated EHR/PM/Billing product — is missing.

## 6. Documentation Quality

The EHI export documentation is essentially nonexistent as a standalone artifact. What exists:

- **No data dictionary**: No field-level documentation of any kind. The only "documentation" is the FHIR API's OpenAPI/Swagger specs, which define API endpoints and standard FHIR schemas — not vendor-specific data.
- **No sample data**: No example exports or sample FHIR resources are provided.
- **No export instructions**: No user-facing documentation explaining how to initiate an EHI export, what data will be included, or how long it takes.
- **No schema documentation**: No description of how the vendor's internal data maps to FHIR resources, what data is lost in translation, or what vendor-specific extensions exist (there are none).
- **Machine-readable artifacts**: The OpenAPI specs and FHIR CapabilityStatements are machine-readable, but they describe a standard FHIR API, not a vendor-specific export.

A developer could build a FHIR client to consume this API using standard FHIR/US Core knowledge plus the Swagger specs. However, they would only receive the clinical data subset and would have no way to know what data is missing or how to obtain the rest. The documentation provides zero guidance on accessing billing, insurance, scheduling, or other non-FHIR data.

The cost disclosure on the certification page ("Data extraction in custom formats" has fees, "no fees for extraction in ONC certified formats") raises a question: is accessing the full EHI (which necessarily includes non-FHIR data) considered a "custom format" that incurs fees? This is ambiguous and potentially problematic under the (b)(10) requirement.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The EHI export is the vendor's (g)(10) FHIR API repackaged as (b)(10). It covers only the standardized US Core clinical data subset — 20 FHIR resource types with no vendor extensions. The entire billing/PM layer (Billing Plus, Practice Plus) — which constitutes a major portion of the product's data — is absent.

### Key Findings

1. **Classic (b)(10)/(g)(10) conflation**: The vendor's certification page points the (b)(10) EHI export directly to the same FHIR APIs that satisfy (g)(10). There is no separate EHI export mechanism, no additional data beyond US Core, and no acknowledgment that the product stores data the FHIR API doesn't cover. Verified by examining the certification HTML source and confirming the "Data Exchange/Extraction" section contains only FHIR links.

2. **Entire billing module absent**: Med A-Z is marketed as an integrated EHR/PM/Billing suite with claims submission, HCFA forms, claims scrubbing, payment processing, and revenue cycle management. None of this data appears in the export. The CapabilityStatements confirm zero billing-related FHIR resources (no Claim, ExplanationOfBenefit, Coverage, or InsurancePlan).

3. **No data dictionary or field-level documentation**: The only documentation is OpenAPI specs for a standard FHIR API. No vendor-specific data model, no field descriptions, no value sets, no relationships, no sample data. The 106 schema definitions in the single-patient Swagger spec are generic FHIR data types, not vendor-specific entities.

4. **Ambiguous fee structure**: The certification page states fees apply for "data extraction in custom formats" while "ONC certified formats like QRDA1, CCD, etc." are free. Since a complete EHI export necessarily includes non-FHIR data (billing, insurance), it's unclear whether the full EHI is available without charge as (b)(10) requires.

5. **Bulk export technically available**: The FHIR Bulk Data Access API (Group-level `$export`) does provide a mechanism for population-level export of the clinical data it covers, which is more than some vendors offer — though the scope limitation (20 US Core resources only) severely limits its value as an EHI export.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 (4.0.1), US Core IG v3.1.1
Model type:      Standard projection (US Core FHIR, no vendor extensions)
Entities:        20 FHIR resource types
Fields:          N/A (standard FHIR resources, no vendor-specific field documentation)
Descriptions:    N/A (no vendor-specific documentation)
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data Access, Group-level $export)
Domains covered: 7 of 17 applicable domains (4 additional partially covered)
```

### Bottom Line

Med A-Z's EHI export is its (g)(10) FHIR API relabeled as (b)(10). A patient or provider requesting their complete health information would receive standard clinical data (conditions, medications, allergies, immunizations, labs, vitals, procedures, care plans) but zero billing records, zero insurance information, zero claims data, and zero practice management data — despite these being core features of the product. The single biggest gap is the complete absence of the Billing Plus module's data, which for an integrated EHR/PM/Billing product represents a substantial portion of the designated record set.
