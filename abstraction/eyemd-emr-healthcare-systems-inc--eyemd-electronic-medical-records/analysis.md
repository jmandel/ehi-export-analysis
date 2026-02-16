# EHI Export Analysis: EyeMD EMR Healthcare Systems, Inc.

**Product**: EyeMD Electronic Medical Records, Version 2  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.2725.EyeM.02.00.1.190501 (CHPL #9988)

## 1. Product Context

EyeMD EMR is a specialty EHR focused exclusively on ophthalmology and optometry practices. Founded in 2009, the company claims ~20% ophthalmology EMR market share and won the 2024 Best in KLAS award for Ambulatory Ophthalmology EMR. The product is an integrated platform bundling:

- **Core EMR**: Ophthalmology-specific clinical documentation with advanced charting for sub-specialties, customizable templates, ophthalmic examination data (slit lamp, visual acuity, IOP, refraction), automated E&M code suggestion, visit summaries
- **Practice Management**: Scheduling, appointment reminders, waitlists, recalls, real-time claim tracking, patient responsibility estimation, payments, eStatements, insurance card OCR scanning, business intelligence dashboard
- **Image Management**: Integration with ophthalmic diagnostic devices (Zeiss, iCare, iTrace, Heidelberg, Topcon, Oculus) for OCT, fundus photography, visual fields, B-scan ultrasound, HRT, ICG/ICGA, autofluorescence — stored at native resolution with DICOM support
- **Patient Engagement (Axon)**: Digital intake, two-way patient messaging, appointment reminders, medication adherence tracking, consent signing
- **Optical Shop** (via FlexSys): POS, frame/contact lens inventory, lab orders, optical Rx transmission
- **Revenue Cycle Management (AbillifEye)**: Billing and financial operations as a service

This is a data-rich specialty EMR. A genuine (b)(10) export would need to cover ophthalmology-specific clinical measurements, diagnostic imaging data, practice management/billing records, optical shop data, and patient engagement content — far beyond what standard USCDI/US Core profiles address.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/eyemd-fhir-api-postman-collection.json` (3.99 MB) | Complete Postman collection for the EyeMD EMR FHIR API. Contains 29 folders, 56 endpoints, 59,467-character collection description with USCDI v3 mappings, search parameter tables per resource, setup instructions, and terms of use. | **Most informative** — sole substantive documentation |
| `downloads/mandatorydisclosures.pdf` (103 KB, 1 page) | ONC Costs and Considerations. Lists certified capabilities with costs. Critically describes 170.315(b)(1-2,10,11) collectively as "Ability to send CCDA information to other systems via secure transmission." | **Key evidence** — reveals vendor's conflation of (b)(10) with CCDA/transitions |
| `downloads/fhir-endpoints-bundle.json` (32 KB) | FHIR Bundle with 37 active Endpoint resources representing production customer instances. Shows custom extensions (`endpoint-environment`, `emr-version`). Confirms live FHIR infrastructure. | Moderate — confirms API is operational |
| `downloads/screenshot-fhir-resource-center.png` (217 KB) | Screenshot of the FHIR Resource Center landing page at the registered (b)(10) URL. Shows only links to API Documentation and Application Registration. | Low — confirms minimal landing page |
| `downloads/screenshot-postman-api-docs.png` (217 KB) | Screenshot of the Postman-rendered API documentation. | Low — visual confirmation only |

## 3. Export Mechanics

- **Format**: FHIR R4 via NDJSON (Bulk Data `$export`) and individual FHIR resource queries; also C-CDA R2 CCD via `DocumentReference?patient={id}&type=ALLDATA`
- **Mechanism**: FHIR API (SMART on FHIR / OAuth2 authentication). Bulk Data export via `GET /Group/{id}/$export`. Requires practice-level setup: IT must configure port forwarding to EMR Gateway Server, then EyeMD configures the FHIR API server.
- **Single-patient vs bulk**: Both — individual resource queries by patient, and Group-level Bulk Data export
- **Access constraints**: Practices pay $300 one-time FHIR setup fee. Application vendors pay $3,000 one-time registration fee with 300 API requests/endpoint/day rate limit. Patients access free through patient portal.
- **Architecture note**: Uses "Fog & Edge Computing" desktop architecture — EMR runs locally, with a gateway server connecting to the cloud FHIR API. Each customer has an isolated FHIR endpoint (e.g., `smartonfhir.myeyecarerecords.com/fhir/{ENDPOINT_ID}`).

## 4. Export Content: What's In It

### No Data Dictionary Exists

There is **no field-level data dictionary** in any of the documentation. The Postman collection documents:
- Which FHIR resource types are supported (25 types)
- Search parameters per resource (211 total across all resources)
- USCDI v3 mapping table (118 entries mapping USCDI data elements to US Core profiles)

But there is no documentation of:
- What specific data elements populate each FHIR resource
- What ophthalmology-specific data maps to which FHIR elements
- What vendor extensions exist (though the Endpoints bundle proves they use custom extensions)
- What the Bulk Data `$export` endpoint actually produces
- Value sets, coded fields, or terminology bindings specific to the product

### What the Documentation Covers

The documentation is explicitly the **(g)(10) Standardized API**, not a (b)(10) export. The collection description states: *"The API meets the requirements of the Standardized API for Patient and Population Services criterion §170.315(g)(10) in the 2015 Edition Cures Update."* No mention of (b)(10), EHI, or "electronic health information" appears anywhere.

### Vendor's Own Content Organization

The Postman collection organizes resources by FHIR resource type. Since there is no data dictionary (only search parameters per resource), the table below shows what's documented:

| FHIR Resource Folder | Search Params | Endpoints | Vendor Description |
|---|---|---|---|
| AllergyIntolerance | 15 | 1 | "Used to get reported Patient allergies" |
| CarePlan | 5 | 1 | Search params documented |
| CareTeam | 2 | 1 | Search params documented |
| Condition | 12 | 2 | "Contains Health Concerns and Problems" |
| Coverage | 12 | 2 | (Description is copy-pasted from Condition — likely a bug) |
| Device | 9 | 1 | "Used to retrieve Implantable Devices" |
| DiagnosticReport | 7 | 2 | "Used to retrieve Lab Requests and Results" |
| DocumentReference | 10 | 3 | "Use for retrieving patient documents and CCDAs" |
| Encounter | 12 | 2 | "Used to obtain Patient Encounters" |
| Goal | 0 | 1 | "Used to get Patient Health Goals" |
| Group | 3 | 1 | Search params documented |
| Immunization | 16 | 1 | "Used get the Patients Immunizations" |
| Location | 11 | 2 | "Used to list the Doctors Office Locations" |
| Medication | 9 | 1 | "Used to get Patient medications" |
| MedicationRequest | 7 | 1 | "Used to get medication orders" |
| MedicationDispense | 7 | 2 | "Used to get medication orders" |
| Observation | 12 | 2 | "Used for Vitals and Lab Results" |
| Organization | 11 | 2 | "Used to get the Organization's information" |
| Patient | 12 | 2 | "Used to get Patient Demographics" |
| Practitioner | 15 | 2 | "Used to get information about the practitioner" |
| Procedure | 6 | 1 | Search params documented |
| Provenance | 6 | 1 | Search params documented |
| QuestionnaireResponse | 12 | 2 | Search params documented |
| RelatedPerson | 0 | 2 | (No description) |
| ServiceRequest | 0 | 2 | (No description) |
| Specimen | 12 | 2 | Search params documented (spelled "Speciman" in collection) |

**Additional folders (not FHIR resources):**
- System Level Operations: 9 endpoints (metadata, SMART config, token introspection/revocation)
- Export: 2 endpoints (`$export` start + file retrieval — **zero documentation on either**)
- App Registration: 3 endpoints

### USCDI v3 Mapping

The collection description includes a comprehensive USCDI v3 mapping table with 118 entries across 20 data classes, mapping each USCDI data element to a US Core profile and FHIR resource. This is a standard USCDI crosswalk — it does not document any ophthalmology-specific or vendor-proprietary mappings.

### Export Endpoints

The Export folder contains two endpoints with **no descriptions whatsoever**:
1. `GET /Group/{id}/$export` — starts a Bulk Data export
2. `GET /_operations/export/{id}/{uuid}/{ResourceType}-{n}.ndjson` — retrieves an export file

The sample URL suggests the output includes Observation NDJSON files (`Observation-1.ndjson`), but there is no documentation of which resource types are included, what data elements are populated, or how the output should be interpreted.

## 5. Coverage Assessment

### 5a. What the Vendor Covers (Bottom-Up)

The vendor provides a standard FHIR R4 API with US Core STU6.1 profiles covering the 20 USCDI v3 data classes. This is their (g)(10) Standardized API for clinical data exchange — not a purpose-built EHI export.

The documentation covers 25 FHIR resource types with 211 search parameters. Every resource is a standard FHIR/US Core resource. There are no vendor extensions documented, no ophthalmology-specific profiles, no billing resources (Claim, ExplanationOfBenefit, etc.), and no custom resources for specialty data.

The Coverage folder (insurance) appears to contain a copy-paste error — its description and URLs reference Condition rather than Coverage, suggesting it may not actually be fully implemented or was hastily added.

The CCD generation endpoint (`DocumentReference?patient={id}&type=ALLDATA`) produces a C-CDA R2 Continuity of Care Document — a clinical summary format that, by definition, does not constitute a complete EHI export.

### 5b. Standardized Domain Coverage (Top-Down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient resource (12 search params), RelatedPerson (no params) | Standard US Core Patient — unknown if ophthalmology-specific demographics (referring providers, optical Rx history) are included |
| Encounters / visits | ⚠️ Partial | Encounter resource (12 search params) | Standard encounters only — no visit-level ophthalmology exam detail, no side-by-side visit comparison data |
| Problems / conditions | ✅ Covered | Condition resource (12 search params) | Standard mapping via US Core |
| Medications / prescriptions | ✅ Covered | Medication, MedicationRequest, MedicationDispense | Standard FHIR medication resources. Unknown if optical Rx (prescriptions transmitted to optical shop) are included |
| Allergies | ✅ Covered | AllergyIntolerance (15 search params) | Standard mapping |
| Immunizations | ✅ Covered | Immunization (16 search params) | Standard mapping |
| Vitals | ✅ Covered | Observation resource | Standard vital signs |
| Lab results | ✅ Covered | Observation, DiagnosticReport, Specimen | Standard lab results |
| Imaging / diagnostic reports | ❌ Not covered | DiagnosticReport exists but described as "Lab Requests and Results" — no imaging-specific documentation | **Critical gap**: Product integrates with OCT, fundus cameras, visual fields, B-scan, HRT, ICG/ICGA from Zeiss, Heidelberg, Topcon, etc. No evidence any diagnostic imaging data (DICOM or otherwise) is in the export |
| Procedures | ✅ Covered | Procedure resource (6 search params) | Standard procedures — no ophthalmology-specific surgical documentation (cataract surgery parameters, IOL calculations) |
| Clinical notes / documents | ✅ Covered | DocumentReference (10 search params, 3 endpoints including CCD generation) | Clinical notes available, plus CCD generation |
| Care plans / goals | ✅ Covered | CarePlan, Goal | Standard mapping |
| Orders / referrals | ⚠️ Partial | ServiceRequest (0 search params, no description) | Minimal — ServiceRequest folder has no documentation |
| Insurance / coverage | ⚠️ Partial | Coverage folder exists but description/URLs reference Condition (copy-paste error) | Unclear if Coverage actually works; no insurance detail beyond basic USCDI |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing resources | **Significant gap**: Product has real-time claim tracking, embedded clearinghouse, patient payments, eStatements. None exportable |
| Payments | ❌ Not covered | No payment resources | Product supports online patient payments and eStatements — not in export |
| Consents / directives | ❌ Not covered | No Consent resource | Product has digital consent signing via Axon — not in export |
| Patient communications | ❌ Not covered | No Communication resources | Product has HIPAA-compliant two-way patient messaging — not in export |
| Specialty-specific (Ophthalmology) | ❌ Not covered | No ophthalmology-specific resources, extensions, or profiles | **Most critical gap**: The product's core differentiator — ophthalmic exam data (slit lamp, visual acuity, IOP, refraction, optical formulas), diagnostic imaging integration, imaging progression analysis, surgical documentation — has zero export documentation. This is the majority of clinical data in an ophthalmology EMR |
| Optical shop data | ❌ Not covered | No resources for optical orders, frames, contact lenses | Product has full optical shop module (POS, inventory, lab orders) — entirely absent |
| Patient engagement data | ❌ Not covered | No resources for intake forms, messages, reminders | Product's Axon platform captures digital intake, consent, messaging — not in export |

**Domains covered**: 8 of 20 applicable (with 4 partial)  
**Domains not covered**: 8 of 20 applicable (including the product's core specialty data)

## 6. Documentation Quality

**As (g)(10) FHIR API documentation**: Adequate. The Postman collection is well-structured with setup instructions, authentication flow, search parameter tables, and USCDI v3 mapping. A developer could build a SMART on FHIR app against this API.

**As (b)(10) EHI export documentation**: Fundamentally inadequate.

- **No data dictionary**: No field-level documentation of what the EMR stores vs. what the API exposes. A developer cannot determine what data is included or excluded.
- **No ophthalmology-specific content**: For a specialty EMR, there is zero documentation of how specialty clinical data maps to FHIR or is exported.
- **Export endpoints undocumented**: The `$export` endpoint has literally no description — not even which resource types are included.
- **No sample data**: No example NDJSON files, no sample resources, no test data.
- **No value sets**: No terminology bindings specific to ophthalmology.
- **No schema**: No machine-readable schema beyond the implicit FHIR R4 specification.
- **Copy-paste errors**: The Coverage folder's description references Condition, suggesting hasty documentation.

A developer **could not** build a comprehensive import from this documentation. They would only know they're getting standard US Core FHIR resources — the same data available through any (g)(10) API — with no visibility into what ophthalmology-specific data exists or how to access it.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only standard USCDI/US Core clinical data — approximately 25 FHIR resource types that map to the regulatory floor for clinical exchange. For a specialty ophthalmology EMR with rich practice management, diagnostic imaging, optical shop, and patient engagement modules, this represents a small fraction of stored patient data. The most clinically valuable data — ophthalmic examinations, diagnostic imaging, specialty surgical records, optical prescriptions — has no documented export path. Billing, payments, patient communications, consent forms, and optical shop data are entirely absent.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of (g)(10) relabeled as (b)(10). The evidence is clear:

1. The registered (b)(10) URL points to the FHIR Resource Center — the same page for (g)(10) API access.
2. The collection description explicitly states it meets "§170.315(g)(10)" and never mentions (b)(10) or EHI.
3. The USCDI v3 mapping table is a standard crosswalk — no vendor-specific extensions or ophthalmology-specific mappings.
4. The mandatory disclosures PDF describes (b)(10) collectively with (b)(1-2,11) as "Ability to send CCDA information to other systems via secure transmission" — conflating EHI export with transitions of care.
5. All 25 FHIR resource types are standard US Core resources with no vendor extensions documented.
6. The `$export` endpoint has zero documentation, suggesting it was not built with separate EHI export considerations.

### Key Findings

1. **The (b)(10) export IS the (g)(10) FHIR API.** The vendor registered their existing FHIR API documentation as their EHI export documentation. The API explicitly references §170.315(g)(10) and USCDI, with no mention of (b)(10) or EHI anywhere in any documentation (`mandatorydisclosures.pdf`, Postman collection, FHIR Resource Center page).

2. **Zero ophthalmology-specific export data is documented.** For a product whose core value proposition is specialty ophthalmology data — diagnostic imaging from Zeiss/Heidelberg/Topcon devices, ophthalmic measurements, optical formulas, surgical documentation — there is no evidence any of this data is in the export. This is the most critical gap: the product's defining clinical data has no export path.

3. **Billing, optical shop, and patient engagement data are entirely absent.** The product includes practice management (claims, payments, eStatements), optical shop (POS, inventory, lab orders), and patient engagement (messaging, digital intake, consent) — none of which appear in any export documentation.

4. **The `$export` endpoint is undocumented.** The Bulk Data Export section contains two endpoints with literally no descriptions, no documentation of included resource types, no sample output — making it impossible to assess what the export actually produces without running it.

5. **The mandatory disclosures PDF is the most revealing artifact.** By describing (b)(10) as "Ability to send CCDA information to other systems via secure transmission," the vendor demonstrates they understand (b)(10) as CCDA transmission (which is actually the (b)(1) transitions of care capability), not as a comprehensive EHI export obligation.

### Summary Stats

```
Coverage:        Minimal/stub/unclear
Approach:        Repackaged existing export
Export format:   FHIR R4 (NDJSON via Bulk Data $export)
Entities:        25 FHIR resource types (standard US Core)
Fields:          N/A (no field-level data dictionary)
Descriptions:    N/A (search parameters documented, not data elements)
Sample data:     No
Bulk export:     Yes (undocumented $export endpoint)
Domains covered: 8 of 20 applicable domains (4 partial)
```

### Bottom Line

EyeMD EMR has relabeled their standard (g)(10) FHIR API as their (b)(10) EHI export. For a specialty ophthalmology EMR that stores diagnostic imaging, ophthalmic measurements, optical shop data, billing records, and patient engagement content, the export covers only the generic clinical exchange surface — standard USCDI resources that any certified EHR must provide. The single biggest gap is the complete absence of ophthalmology-specific clinical data — the very data that defines this product — from any export documentation.
