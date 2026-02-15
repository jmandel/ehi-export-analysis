# EHI Export Analysis: EyeMD EMR Healthcare Systems, Inc.

**Product**: EyeMD Electronic Medical Records, Version 2  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.04.04.2725.EyeM.02.00.1.190501 (CHPL #9988)

## 1. Product Context

EyeMD EMR is a specialty EHR designed exclusively for ophthalmology and optometry practices. Founded in 2009 and based in Bonita Springs, FL, the vendor claims ~20% ophthalmology EMR market share and won the 2024 Best in KLAS award for Ambulatory Ophthalmology EMR. The product uses a desktop "Fog & Edge Computing" architecture with local processing and cloud FHIR API connectivity.

The product is an integrated platform spanning multiple modules relevant to EHI completeness assessment:

- **Core EMR**: Ophthalmology-specific clinical documentation — slit lamp findings, visual acuity, intraocular pressure (IOP), refraction data, complex optical mathematical formulas, surgical documentation (e.g., cataract surgery parameters, IOL calculations), customizable clinical templates, automated E&M code suggestion, visit summaries with abnormal condition alerts.
- **Practice Management**: Scheduling, insurance claims, claim tracking, patient financial responsibility estimates, payments, eStatements, business intelligence dashboards.
- **Image Management**: Integration with ophthalmic diagnostic devices (Zeiss, iCare, iTrace, Heidelberg, Topcon, Oculus) — OCT, fundus photography, visual fields, B-scan ultrasound, HRT, ICG/ICGA, autofluorescence imaging. DICOM and proprietary integrations. Imaging progression analysis.
- **Axon Patient Engagement**: Digital intake forms, consent signing, two-way HIPAA-compliant messaging, appointment reminders, medication adherence tracking.
- **Optical Shop (FlexSys)**: Point of sale, optical orders, lab orders, contact lens/frame inventory, prescription transmission from EMR.
- **Revenue Cycle Management (AbillifEye)**: Billing services for practices.

This is a data-rich ophthalmology EMR with deep specialty clinical data, practice management, imaging, and billing capabilities. A complete EHI export should cover all patient-facing data across these modules.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `eyemd-fhir-api-postman-collection.json` | Complete Postman collection for the FHIR API. Contains all endpoint definitions, USCDI v3 mappings, setup instructions, terms of use, authentication docs. **This is the vendor's sole EHI export documentation.** | 3.99 MB; 59,467-char description; 33 folders; 62 endpoints; 9 embedded screenshots | **Primary artifact** — the only documentation of export capabilities |
| `mandatorydisclosures.pdf` | ONC Costs and Considerations mandatory disclosures. 1 page. Lists certified capabilities with costs. | 1 page, 102 KB | **Significant** — reveals vendor's framing of (b)(10) as "Ability to send CCDA information to other systems via secure transmission" |
| `fhir-endpoints-bundle.json` | FHIR Bundle with 37 active Endpoint resources (production customer instances) | 31 KB; 37 endpoints (35 production, 2 test) | **Moderate** — confirms operational FHIR infrastructure exists |
| `screenshot-fhir-resource-center.png` | Screenshot of the FHIR Resource Center landing page at the registered URL | 217 KB | Low — confirms minimal landing page |
| `screenshot-postman-api-docs.png` | Screenshot of the rendered Postman API documentation | 217 KB | Low — visual confirmation only |

## 3. Export Mechanics

- **Format**: FHIR R4 with US Core STU6.1 profiles, delivered as NDJSON via FHIR Bulk Data Export (`$export`). Also supports CCD generation (C-CDA R2) via a DocumentReference endpoint (`?type=ALLDATA`).
- **Mechanism**: API-based. The `$export` endpoint is `GET /Group/{id}/$export`. Patients access via patient portal; practices require port forwarding configuration and a $300 one-time FHIR setup fee; third-party application vendors pay a $3,000 registration fee.
- **Single-patient vs bulk**: The `$export` endpoint operates at the Group level (population), consistent with FHIR Bulk Data. Individual patient data is available via per-resource search endpoints and the CCD generation endpoint.
- **Access constraints**: Rate-limited to 300 API requests per endpoint per day for application vendors. FHIR server requires customer-specific endpoint identifiers (e.g., `smartonfhir.myeyecarerecords.com/fhir/{ENDPOINT_ID}`). Setup requires local EMR gateway configuration.
- **Fees**: Monthly ongoing fee for FHIR API access (amount not specified). $300 one-time practice setup. $3,000 one-time vendor registration.

**Critical observation**: The API documentation explicitly states it "meets the requirements of the Standardized API for Patient and Population Services criterion §170.315(g)(10)" — it is the (g)(10) API. There is no separate (b)(10) EHI export mechanism or documentation. The Export section has two undocumented endpoints with zero descriptions:
- `GET /Group/{id}/$export` (Start Group Export) — no description
- `GET /_operations/export/{id}/{uuid}/{ResourceType}-{n}.ndjson` (Get Export File) — no description

## 4. Export Content: What's In It

### What the FHIR API exposes

The Postman collection documents **26 FHIR resource type folders** (excluding system-level operations, Export, and App Registration) with a total of **210 search parameters** (all with descriptions). The collection maps **111 USCDI v3 data elements** across **19 USCDI data categories** to **22 distinct FHIR resource types**.

There is **no data dictionary** — no field-level documentation of what data elements populate each FHIR resource, no value sets, no terminology bindings, no sample data, no example API responses. The documentation describes search parameters for querying resources, not the structure or content of the resources themselves.

### FHIR resource types documented

| Resource Type | Search Params | Endpoints | Category |
|---|---|---|---|
| AllergyIntolerance | 15 | 1 | Allergies |
| CarePlan | 5 | 1 | Care Plans |
| CareTeam | 2 | 1 | Care Teams |
| Condition | 6 | 2 | Problems / Diagnoses |
| Coverage | 6 | 2 | Insurance |
| Device | 9 | 1 | Devices |
| DiagnosticReport | 7 | 2 | Lab / Imaging Results |
| DocumentReference | 10 | 3 | Clinical Notes / CCD |
| Encounter | 12 | 2 | Encounters |
| Goal | 0 | 1 | Goals |
| Group | 3 | 1 | Population grouping |
| Immunization | 16 | 1 | Immunizations |
| Location | 11 | 2 | Practice locations |
| Medication | 9 | 1 | Medications |
| MedicationDispense | 7 | 2 | Medication fill status |
| MedicationRequest | 7 | 1 | Medication orders |
| Observation | 12 | 2 | Vitals / Labs / Assessments |
| Organization | 11 | 2 | Organizations |
| Patient | 12 | 2 | Demographics |
| Practitioner | 14 | 2 | Providers |
| Procedure | 6 | 1 | Procedures |
| Provenance | 6 | 1 | Provenance |
| QuestionnaireResponse | 12 | 2 | SDOH Assessments |
| RelatedPerson | 0 | 2 | Related persons |
| ServiceRequest | 0 | 2 | Referrals |
| Specimen | 12 | 2 | Lab specimens |

### USCDI v3 mapping categories

The documentation provides a comprehensive USCDI v3 mapping table with these 19 categories (plus a "New in USCDI v3" addendum):

1. Allergies and Intolerances (4 elements)
2. Assessment and Plan of Treatment (4 elements)
3. Care Team Members (6 elements)
4. Clinical Notes (6 elements — Consultation, Discharge Summary, H&P, Procedure, Progress notes)
5. Clinical Tests (3 elements)
6. Diagnostic Imaging (3 elements)
7. Encounter (6 elements)
8. Goals (3 elements)
9. Health Insurance Information (8 elements)
10. Health Status / Assessments (9 elements)
11. Immunizations (1 element)
12. Laboratory (5 elements)
13. Medications (5 elements — Dose, Unit of Measure, Indication, Fill Status)
14. Patient Demographics (25 elements)
15. Problems (5 elements)
16. Procedures (4 elements)
17. Provenance (3 elements)
18. Unique Device Identifiers (2 elements)
19. Vital Signs (9 elements)

This is a standard USCDI v3 mapping — exactly what is required for (g)(10), not (b)(10).

### What's NOT in it

The export contains **zero ophthalmology-specific content**. There are no FHIR extensions, custom profiles, or vendor-specific resources for:
- Ophthalmic examination data (slit lamp, visual acuity, IOP, refraction)
- Diagnostic imaging (OCT, fundus, visual fields, DICOM)
- Optical prescriptions
- Surgical parameters (IOL calculations, cataract surgery details)
- Practice management / billing data
- Optical shop data
- Patient engagement data (messages, intake forms, consents)

A search for ophthalmology-specific terms (`ophthal`, `iop`, `visual acuity`, `slit lamp`, `oct`, `fundus`, `dicom`, `retina`, `cataract`, `refraction`, `keratometry`) in the 59,467-character collection description found **zero clinical references** — only trademark-related mentions of "ophthalmology" and "eye."

### CCD generation endpoint

The `DocumentReference?patient={id}&type=ALLDATA` endpoint "outputs a CCDA R2 Continuity of Care Document, encoded in base64 format." This is the closest thing to a comprehensive single-patient export, but a CCD is a clinical summary format — it cannot capture ophthalmology-specific measurements, imaging data, or billing records.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides a standard FHIR US Core API covering USCDI v3 data classes. The documentation is organized around FHIR resource types, not around the product's clinical or operational domains. There is:

- **Good coverage of generic clinical data**: Demographics (25 USCDI elements), vitals, problems, medications, allergies, immunizations, encounters, procedures, lab results, clinical notes, care plans, and insurance coverage are all mapped to standard FHIR resources with documented search parameters.
- **Complete absence of specialty-specific data**: Not a single ophthalmology-specific data element, measurement, or image format appears anywhere in the documentation. For a product whose core value proposition is ophthalmology-specific clinical documentation, this is a critical gap.
- **Complete absence of billing/financial data**: No claims, charges, payments, superbills, or financial transactions. The Coverage resource captures insurance *coverage* information (8 USCDI elements), but not billing *transactions*.
- **Complete absence of practice management data**: No scheduling, appointment, recall, or waitlist data.
- **Complete absence of optical shop data**: No optical orders, prescriptions, inventory, or point-of-sale data.
- **Complete absence of patient engagement data**: No messages, intake forms, or consent documents beyond what's captured in standard FHIR resources.

The **Export folder** itself has **zero documentation** — both the `Start Group Export` and `Get Export File` endpoints have no descriptions, no example requests or responses, and no documentation of what resource types are included in the bulk export output.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource, 25 USCDI elements mapped, 12 search params | Standard US Core demographics; adequate for generic data |
| Encounters / visits | ✅ Covered | Encounter resource, 6 USCDI elements, 12 search params | Standard encounter data; no ophthalmology-specific visit detail |
| Problems / conditions | ✅ Covered | Condition resource, 5 USCDI elements, 6 search params | Standard problem list |
| Medications / prescriptions | ✅ Covered | Medication, MedicationRequest, MedicationDispense; 5 USCDI elements | Standard medication data; no optical prescriptions |
| Allergies | ✅ Covered | AllergyIntolerance, 4 USCDI elements, 15 search params | Adequate |
| Immunizations | ✅ Covered | Immunization resource, 1 USCDI element, 16 search params | Adequate |
| Vitals | ✅ Covered | Observation resource, 9 USCDI elements | Standard vital signs |
| Lab results | ✅ Covered | Observation + DiagnosticReport, 5 USCDI elements | Standard lab results |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport resource, 3 USCDI elements | FHIR DiagnosticReport covers lab-style reports only. Product stores OCT, fundus photos, visual fields, B-scan ultrasound from multiple device vendors — **none of this imaging data has a documented export path**. This is the most significant gap. |
| Procedures | ✅ Covered | Procedure resource, 4 USCDI elements, 6 search params | Standard procedures; no cataract surgery–specific parameters (IOL calculations, keratometry, etc.) |
| Clinical notes / documents | ✅ Covered | DocumentReference, 6 USCDI note types, plus CCD generation | Standard clinical notes via US Core |
| Care plans / goals | ✅ Covered | CarePlan + Goal, 7 USCDI elements | Standard |
| Orders / referrals | ✅ Covered | ServiceRequest, 2 endpoints | Standard |
| Insurance / coverage | ✅ Covered | Coverage resource, 8 USCDI elements | Coverage status only; not billing transactions |
| Claims / billing | ❌ Not covered | No billing resources in export | **Product has integrated claim tracking, patient financial responsibility, payments, eStatements, and revenue cycle management (AbillifEye). Significant gap.** |
| Payments | ❌ Not covered | No payment resources in export | Product supports online patient payments and eStatements. Gap. |
| Consents / directives | ❌ Not covered | No Consent resource | Product captures digital consent forms via Axon. Gap. |
| Patient communications | ❌ Not covered | No Communication resource | Product has HIPAA-compliant two-way messaging (Axon Converse). Gap. |
| Specialty-specific (Ophthalmology) | ❌ Not covered | No ophthalmology-specific data elements, measurements, extensions, or profiles anywhere in documentation | **Product's core differentiator is ophthalmology-specific clinical data — slit lamp, IOP, visual acuity, refraction, diagnostic imaging from 6+ device vendors, surgical parameters, optical formulas. None of this has any export pathway. This is the single largest gap.** |

## 6. Documentation Quality

The FHIR API documentation is **professionally structured and reasonably detailed as (g)(10) API documentation**:
- 59,467-character collection description covering overview, setup instructions, fees, authorization, terms of use, USCDI mappings, and API syntax
- 26 FHIR resource folders, 23 with descriptions including search parameter tables
- 210 search parameters, all with type and description information
- 9 embedded screenshots for setup instructions
- Complete USCDI v3 mapping table (111 elements across 19 categories)
- SMART on FHIR / OAuth2 authentication documentation
- Error handling and pagination guidance

**However, as EHI export documentation, it is fundamentally inadequate:**
- **No data dictionary**: No field-level documentation of what data elements populate each FHIR resource. A developer cannot determine what specific data the export contains without making API calls.
- **No sample data**: No example API responses or export files.
- **No value sets**: No terminology bindings or coded field definitions specific to ophthalmology.
- **No export documentation**: The Export section's two endpoints have zero descriptions — no documentation of what resource types are included, what data is covered, or how to interpret output.
- **No mention of (b)(10)**: The term "(b)(10)," "EHI," "electronic health information," or "designated record set" does not appear anywhere in the documentation. The documentation explicitly references §170.315(g)(10).
- **No ophthalmology-specific content**: For a specialty EMR, there is no documentation of how the product's distinctive clinical data maps to the export.
- **No schema or machine-readable data model**: No JSON Schema, OpenAPI spec, or FHIR StructureDefinitions beyond the standard US Core profiles.

A developer working from this documentation alone could implement a FHIR client to retrieve standard USCDI clinical data, but would have no way to access the ophthalmology-specific data, billing records, imaging data, or practice management information that constitutes the majority of the product's stored data.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The vendor's "(b)(10)" EHI export is their (g)(10) FHIR US Core API repackaged. The documentation explicitly states it meets §170.315(g)(10) requirements and provides only USCDI v3 clinical data through standard FHIR R4 resources. There is no native data model export, no data dictionary, and no ophthalmology-specific content. The mandatory disclosures PDF confirms this framing by describing capabilities 170.315(b)(1-2,10,11) collectively as "Ability to send CCDA information to other systems via secure transmission."

### Key Findings

1. **The (b)(10) export is the (g)(10) FHIR API.** The registered (b)(10) URL points to the FHIR Resource Center, which links to Postman API documentation that explicitly references §170.315(g)(10). There is no separate EHI export mechanism, documentation, or data dictionary. (`eyemd-fhir-api-postman-collection.json`, collection description: "The API meets the requirements of the Standardized API for Patient and Population Services criterion §170.315(g)(10)")

2. **Zero ophthalmology-specific data in the export.** For a specialty EMR that stores slit lamp findings, IOP measurements, visual acuity, refraction data, OCT scans, fundus photos, visual fields, and surgical parameters, the FHIR API contains no ophthalmology-specific resources, extensions, or profiles. The product's core clinical value is entirely absent from the export.

3. **No billing, practice management, optical shop, or patient engagement data.** The product integrates claim tracking, patient payments, scheduling, optical orders, and two-way messaging — none of which has any export pathway.

4. **The Export section is completely undocumented.** The Bulk Data `$export` endpoint and the export file retrieval endpoint have zero descriptions, no parameter documentation, and no example output. A user cannot determine what the export contains without running it.

5. **The mandatory disclosures conflate (b)(10) with CCDA transmission.** The PDF groups 170.315(b)(1-2,10,11) and (h)(1) together as "Ability to send CCDA information to other systems via secure transmission" — equating the EHI export requirement with transitions of care CCDA capability.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   FHIR R4 (NDJSON via Bulk Data), C-CDA R2 (via DocumentReference)
    Model type:      Standard projection (US Core / USCDI v3)
    Entities:        26 FHIR resource types (standard US Core, no extensions)
    Fields:          N/A (no field-level data dictionary; 210 search parameters documented)
    Descriptions:    N/A (no field-level documentation; search params 100% described)
    Sample data:     No
    Bulk export:     Yes (FHIR Bulk Data $export, undocumented)
    Domains covered: 13 of 19 applicable domains (all partial — USCDI-level only)

### Bottom Line

EyeMD EMR's EHI export is a textbook case of (g)(10) FHIR API being relabeled as (b)(10) EHI export. For a specialty ophthalmology EMR, the export covers only the generic USCDI clinical data layer — perhaps 20–30% of the patient data the product actually stores. The most clinically and operationally valuable data — ophthalmology-specific exam findings, diagnostic imaging, optical measurements, billing records, and specialty surgical documentation — has no documented export path. A patient requesting their "complete" health information through this export would receive a standard clinical summary while missing the detailed eye care data that is the core reason they use this provider.
