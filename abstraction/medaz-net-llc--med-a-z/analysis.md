# EHI Export Analysis: MedAZ.Net, LLC

**Product**: Med A-Z (version 202001)
**Analysis date**: 2026-02-16
**CHPL IDs**: 11300 (15.05.05.3150.MDAZ.01.00.1.230616)

## 1. Product Context

Med A-Z Complete is a fully integrated EHR + Practice Management + Billing/Revenue Cycle Management suite developed by MedAZ.Net, LLC (a subsidiary of KATSI). The product targets small-to-mid-size ambulatory physician practices and bundles all three modules as a single certified product (ONC Cures Act certified June 16, 2023).

**Key data-storing capabilities relevant to export completeness:**

- **EHR Plus**: Patient demographics, chief complaints, allergies, medications, medical/surgical/family/social history, review of systems, vitals (height, weight, BMI), physical exam findings, diagnosis/problem lists, treatment plans, lab orders/results (HL7 interfaces with Quest/LabCorp), imaging orders (CPOE), electronic prescribing (Surescripts), drug interaction checking, clinical decision support, patient education tracking, clinical quality measures, cardiovascular risk assessments (Framingham), clinical notes with customizable templates.

- **Practice Plus**: Patient scheduling, insurance information management, copay collection, office floor plan visualization, check-in/checkout workflows, referral letters.

- **Billing Plus**: Electronic claims submission, claims scrubbing, HCFA form generation, real-time claim status tracking, procedure-diagnosis code linking, credit card payment processing, revenue cycle analytics.

This is a product that stores substantial data across clinical, administrative, and financial domains. An adequate (b)(10) export would need to cover all three modules.

## 2. Artifacts Reviewed

| Artifact | File | Size | Description | Informative? |
|---|---|---|---|---|
| Certification page | `certificationinfo.html` | 15,010 bytes | Main (b)(10) registered URL. Contains certification info, costs, and "Data Exchange/Extraction" section linking to FHIR APIs. **No EHI-specific documentation, no data dictionary, no export instructions.** | Medium — confirms absence of EHI-specific docs |
| Single Patient OpenAPI Spec | `swagger-single-patient.json` | 531 KB | OpenAPI 3.0.1 spec for single-patient FHIR API ("Med A-Z FHIR" v2). 90 API paths, 106 schema definitions (all FHIR infrastructure types, zero vendor-specific resource schemas). | High — definitive source for API coverage |
| Bulk Export OpenAPI Spec | `swagger-bulk.json` | 272 KB | OpenAPI 3.0.1 spec for bulk FHIR API ("Med A-Z FHIRBulk" v2). 37 API paths, 94 schema definitions. Implements FHIR Bulk Data Access via `Group/{id}/$export`. | High — confirms bulk capability |
| Capability Statement (Single) | `fhir-capability-statement-single.json` | 22 KB | FHIR R4 (4.0.1) CapabilityStatement. US Core IG v3.1.1. 20 resource types, all standard US Core profiles. No custom profiles or extensions. 72 search parameters total. | High — definitive resource type list |
| Capability Statement (Bulk) | `fhir-capability-statement-bulk.json` | 22 KB | Identical resource types and profiles to single-patient API. | Confirmatory |
| FHIR Endpoints (Single) | `fhirsingle.xml` | 29 KB | FHIR Bundle with 19 Endpoint resources listing resource types and API URLs. Last modified Sept 21, 2022. | Low — duplicates CapabilityStatement |
| FHIR Endpoints (Bulk) | `fhirsystosys.xml` | 25 KB | FHIR Bundle with 19 Endpoint resources for bulk API. | Low — duplicates CapabilityStatement |
| Screenshot: Certification Page | `screenshot-certification-page.png` | 588 KB | Full-page screenshot of certification page. | Confirmatory |
| Screenshot: Swagger Single | `screenshot-swagger-single-patient.png` | 167 KB | Screenshot showing Swagger UI for single-patient API. | Confirmatory |
| Screenshot: Swagger Bulk | `screenshot-swagger-bulk.png` | 143 KB | Screenshot showing Swagger UI for bulk API. | Confirmatory |

**Most informative**: The two OpenAPI specs and the CapabilityStatements definitively establish what the FHIR APIs expose.
**Least informative**: The endpoint XML files and screenshots are confirmatory duplicates.

## 3. Export Mechanics

- **Format**: FHIR R4 (4.0.1), US Core Implementation Guide v3.1.1
- **Mechanism**: RESTful FHIR API (requires authentication via OAuth-style application registration)
  - Single patient: standard FHIR RESTful API with search, pagination, and history (`fhirapi.mhealthaz.com`)
  - Bulk: FHIR Bulk Data Access via `Group/{id}/$export` with poll/download pattern (`fhirbulk.mhealthaz.com`)
- **Single-patient vs bulk**: Both supported
- **Access constraints**: Application registration required (via `/myapplication/*` endpoints). OAuth-style consent flow with client key generation. The certification page notes "Data extraction in custom formats" incurs fees, but "no fees for extraction in ONC certified formats like QRDA1, CCD, etc." This raises the question of whether non-FHIR export of additional data domains would require payment.
- **No separate EHI export mechanism**: There is no UI button, no dedicated EHI export process, and no documentation describing how to obtain "all electronic health information." The (b)(10) documentation simply points to the same FHIR API that satisfies (g)(10).

## 4. Export Content: What's In It

### What the API exposes

The export is entirely defined by the FHIR CapabilityStatement. Both APIs (single-patient and bulk) expose the same 20 US Core resource types with standard profiles:

| Resource Type | US Core Profile(s) | Search Params | Interactions |
|---|---|---|---|
| AllergyIntolerance | us-core-allergyintolerance | 2 | read, search, vread, history |
| CarePlan | us-core-careplan | 4 | read, search, vread, history |
| CareTeam | us-core-careteam | 2 | read, search, vread, history |
| Condition | us-core-condition | 5 | read, search, vread, history |
| Device | us-core-implantable-device | 2 | read, search, vread, history |
| DiagnosticReport | us-core-diagnosticreport-lab, us-core-diagnosticreport-note | 5 | read, search, vread, history |
| DocumentReference | us-core-documentreference | 7 | read, search, vread, history |
| Encounter | us-core-encounter | 7 | read, search, vread, history |
| Goal | us-core-goal | 3 | read, search, vread, history |
| Immunization | us-core-immunization | 3 | read, search, vread, history |
| Location | us-core-location | 5 | read, search, vread, history |
| Medication | us-core-medication | 0 | read, search, vread, history |
| MedicationRequest | us-core-medicationrequest | 5 | read, search, vread, history |
| Observation | multiple (vitals, labs, smoking, pediatric BMI/weight, pulse ox, BP, temp, etc.) | 5 | read, search, vread, history |
| Organization | us-core-organization | 2 | read, search, vread, history |
| Patient | us-core-patient | 7 | read, search, vread, history |
| Practitioner | us-core-practitioner | 2 | read, search, vread, history |
| PractitionerRole | us-core-practitionerrole | 2 | read, search, vread, history |
| Procedure | us-core-procedure | 4 | read, search, vread, history |
| Provenance | (none specified) | 0 | read, search, vread, history |

**Total: 20 resource types, 72 search parameters, 0 vendor-defined schemas.**

### What's NOT in the API

The Swagger specifications contain 106 schema definitions (single-patient API) and 94 (bulk API), but these are entirely FHIR infrastructure types (Bundle, CapabilityStatement, Meta, Coding, CodeableConcept, etc.) and application management schemas (myapplication with 58 properties for OAuth registration). **Zero** vendor-specific resource schemas are defined. The API returns standard FHIR resources with no custom profiles, no extensions, and no vendor-specific data elements.

This means the export contains exactly what US Core defines — no more. The vendor's native data model (which includes billing, scheduling, insurance, custom clinical forms, drug interaction records, etc.) is not represented in any way.

### No data dictionary

There is no data dictionary, no field-level documentation, no schema documentation, and no sample data. The certification page's "Data Exchange/Extraction" section contains four links (two Swagger UIs, two FHIR endpoint XMLs) and a list of preferred formats (QRDA-1, CCD-A). There is no description of what data the export includes or excludes.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides no organizational framework for their export — no categories, no modules, no sections. The export is simply "the FHIR API," which exposes the 20 standard US Core resource types. There is no vendor-supplied categorization to reference.

The export covers standard clinical data as defined by US Core IG v3.1.1 / USCDI v1:
- **Patient identification**: Patient, Practitioner, PractitionerRole, Organization, Location
- **Clinical observations**: Observation (vitals, labs, smoking status, pediatric measures, pulse ox)
- **Conditions & procedures**: Condition, Procedure, AllergyIntolerance
- **Medications**: Medication, MedicationRequest
- **Care coordination**: CarePlan, CareTeam, Goal, Encounter
- **Documents & reports**: DocumentReference, DiagnosticReport
- **Other**: Device (implantable), Immunization, Provenance

This is the minimum USCDI clinical data set. It contains no billing, no insurance, no scheduling, no custom clinical data, and no vendor-specific extensions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (US Core profile, 7 search params) | Standard US Core demographics |
| Encounters / visits | ✅ Covered | `Encounter` (US Core profile, 7 search params) | Standard encounter data |
| Problems / conditions / diagnoses | ✅ Covered | `Condition` (US Core profile, 5 search params) | Standard problem list |
| Medications / prescriptions | ✅ Covered | `Medication`, `MedicationRequest` (US Core profiles, 5 search params) | Standard med data; no Surescripts e-prescribing transaction history |
| Allergies | ✅ Covered | `AllergyIntolerance` (US Core profile, 2 search params) | Standard allergy data |
| Immunizations | ✅ Covered | `Immunization` (US Core profile, 3 search params) | Standard immunization data |
| Vitals | ✅ Covered | `Observation` (BP, height, weight, temp, heart rate, resp rate, pulse ox, pediatric) | Standard vital signs |
| Lab results | ✅ Covered | `DiagnosticReport` (lab + note profiles), `Observation` (lab) | Standard lab results; no HL7 interface transaction data |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport` (note profile) | May include imaging reports but no imaging data or PACS integration data |
| Procedures | ✅ Covered | `Procedure` (US Core profile, 4 search params) | Standard procedure data |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (US Core profile, 7 search params) | Standard clinical documents |
| Care plans / goals | ✅ Covered | `CarePlan`, `Goal`, `CareTeam` (US Core profiles) | Standard care plan data |
| Orders / referrals | ⚠️ Partial | `MedicationRequest` covers med orders | No ServiceRequest for lab/imaging orders (CPOE data); no referral letters |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resources | Product stores "unlimited insurance plan configuration" and insurance info (Practice Plus). **Significant gap.** |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing resources | Product has dedicated "Billing Plus" module with claims, HCFA forms, claims scrubbing, claim status tracking. **Major gap.** |
| Payments | ❌ Not covered | No payment-related resources | Product processes credit card/debit payments. **Gap.** |
| Consents / directives | ❌ Not covered | No Consent resource | No evidence |
| Patient communications / portal messages | N/A | No communication resources | Product has limited/no patient portal per research |
| Drug interaction alerts / CDS data | ❌ Not covered | No DetectedIssue or CDS resources | Product checks drug-drug, drug-allergy, drug-procedure interactions; tracks patient education materials. **Gap.** |

**Domains covered**: 11 of 17 applicable domains have at least partial coverage (all via standard US Core).
**Domains missing**: Insurance/coverage, claims/billing, payments, consents, and drug interaction/CDS data are absent despite the product storing this data.

## 6. Documentation Quality

**Overall**: The documentation is minimal. There is no EHI-specific documentation at all.

- **Can a developer understand and use the export?** A developer familiar with FHIR and US Core could implement a client based on the Swagger specs and CapabilityStatements. However, they would have no way to know what vendor-specific data exists beyond the FHIR API, nor any guidance on how to obtain a complete EHI export.
- **Data dictionary**: None. Zero field-level documentation specific to this vendor's implementation.
- **Machine-readable artifacts**: The OpenAPI specs (Swagger JSON) and FHIR CapabilityStatements are machine-readable. However, they describe a standard FHIR API, not a vendor-specific export.
- **Sample data**: None provided.
- **Value sets**: Entirely inherited from US Core; no vendor-specific documentation.
- **Export instructions**: None. The certification page lists (b)(10) among certified criteria but provides no instructions for initiating an EHI export, no description of what's included, and no acknowledgment that the product stores data beyond what the FHIR API exposes.
- **Cost implications**: The certification page states "Data extraction in custom formats" has fees while "ONC certified formats like QRDA1, CCD, etc." are free. This suggests that extracting data beyond the FHIR API may require payment, which raises compliance concerns with (b)(10)'s no-fee requirement.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is the vendor's (g)(10) FHIR API repackaged as their (b)(10) EHI export. It covers the standard US Core / USCDI clinical data subset using 20 standard FHIR resource types with no custom profiles, no extensions, and no vendor-specific schemas. The entire administrative (Practice Plus) and financial (Billing Plus) layers of the product — representing roughly half the product's data domains — are completely absent from the export.

### Key Findings

1. **Classic (g)(10)/(b)(10) conflation**: The vendor's registered (b)(10) URL (`certificationinfo.html`) points to FHIR API Swagger documentation — the exact same API that satisfies (g)(10). There is no separate EHI export mechanism, no additional data beyond standard US Core, and no acknowledgment that the product stores data outside the FHIR scope. (Source: `certificationinfo.html` lines 219–244; both CapabilityStatements show identical 20 US Core resource types with no custom profiles.)

2. **Billing Plus module entirely absent**: Despite being a core product pillar with claims submission, HCFA form generation, claims scrubbing, payment processing, and revenue cycle analytics, zero billing or financial data is available through the export. No Claim, ExplanationOfBenefit, Coverage, or payment-related resources exist. (Source: `fhir-capability-statement-single.json` — no billing resource types listed.)

3. **Zero vendor-specific schemas**: The Swagger specs define 106 schemas (single) and 94 schemas (bulk), but every one is a standard FHIR infrastructure type or application management schema. Not a single vendor-specific resource schema exists, confirming this is a pure standard projection with no custom data. (Source: `swagger-single-patient.json` schema definitions.)

4. **No data dictionary exists**: There is no field-level documentation, no description of what the export includes or excludes, no sample data, and no export instructions. The entire (b)(10) documentation consists of four links on the certification page. (Source: `certificationinfo.html`.)

5. **Fee ambiguity**: The certification page notes "Data extraction in custom formats" incurs fees, while "ONC certified formats like QRDA1, CCD" are free. This suggests obtaining non-FHIR data (i.e., the billing and PM data missing from the export) may require payment, potentially conflicting with (b)(10) requirements. (Source: `certificationinfo.html` line 212.)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR R4 (4.0.1), US Core IG v3.1.1
Model type:      Standard projection (pure US Core, no custom profiles or extensions)
Entities:        20 FHIR resource types
Fields:          N/A (no vendor-defined schemas; relies on standard FHIR resource definitions)
Descriptions:    N/A (no vendor-specific field documentation)
Sample data:     No
Bulk export:     Yes (FHIR Bulk Data Access via Group/$export)
Domains covered: 11 of 17 applicable domains (clinical only; no billing, insurance, or payments)
```

### Bottom Line

Med A-Z's EHI export is a textbook case of a vendor repackaging their FHIR (g)(10) API as their (b)(10) export. For an integrated EHR/PM/Billing product, the export covers only the clinical data that US Core defines — roughly half the product's data domains. The entire Billing Plus module (claims, payments, HCFA forms), all insurance data, and all practice management data are absent. A patient or provider requesting their complete health record would receive standard clinical data but none of the billing, financial, or administrative records the product stores about them.
