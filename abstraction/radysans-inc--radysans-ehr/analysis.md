# EHI Export Analysis: Radysans, Inc

**Product**: Radysans EHR v5.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2912.Rady.05.00.1.191231 (CHPL #10253)

## 1. Product Context

Radysans EHR is an integrated ambulatory EHR and practice management platform targeting small outpatient clinics and physician practices. It is cloud-hosted (at ehr.cutecharts.com) and offered as a SaaS subscription. The company is based in Apex, North Carolina and appears to have a very small customer base (one identifiable customer: Mann ENT, an otolaryngology practice).

The product comprises several integrated modules relevant to EHI scope:

- **EMR Module**: Clinical documentation, CPOE for medications/labs/imaging, clinical decision support, drug interaction checks, problem lists, allergies, vital signs, immunizations, implantable devices, social/psychological/behavioral data, care plans.
- **Practice Management (PMS)**: Enterprise scheduling (multi-location, multi-provider), patient registration with document scanning (photos, insurance cards), referral management with pre-authorization, message/task routing.
- **eBilling Module**: Charge capture, claim scrubbing, electronic claims submission to 2,500+ payers, payment posting/reconciliation, denial tracking, EOB/ERA processing, patient statement generation.
- **Patient Portal**: Patient access to health information, patient representative login.
- **Transcription Services**: Medical transcription with long-term storage and retrieval.
- **Order Entry**: CPOE for medications, labs, and imaging.

The product is certified across 40+ ONC criteria including (b)(10) EHI Export. For a complete EHI export, one would expect coverage of clinical data, billing/claims records, insurance data, and referral management — all of which are used to make decisions about patients.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `B-10-Documentation.pdf` (61 KB, 1 page) | The primary (b)(10) EHI export documentation. Lists 22 C-CDA sections and references FHIR Bulk Data. No data dictionary, no field-level detail. | **Low** — names sections only |
| `G10ApplicationAccessTermsandCondition.pdf` (311 KB, 41 pages) | The (g)(10) FHIR API documentation. Covers 18 FHIR resource types with OAuth2 flow, endpoint URLs, search parameters, and full sample JSON responses. | **Medium** — implicitly documents field structure via samples |
| `RadysansEHRCostsandLimitations.pdf` (582 KB, 2 pages) | Mandatory Disclosure Statement. Confirms a one-time per-provider fee for data extraction. | **Low** — fee/cost info only |
| `fhir-endpoint-bundle.json` (1.2 KB) | FHIR Bundle with Endpoint and Organization resources. Confirms API base URL. | **Low** — confirms FHIR endpoint exists |
| `screenshot-onc-certification-page.png` (275 KB) | Screenshot of the ONC certification page. | **Low** — navigation context |

The most informative artifact is the G10 API documentation PDF, which provides sample JSON outputs that implicitly show what fields each FHIR resource contains. However, this is (g)(10) documentation repurposed for (b)(10), not purpose-built EHI export documentation.

## 3. Export Mechanics

- **Format(s)**: C-CDA XML documents and FHIR R4 JSON via Bulk Data API
- **Mechanism**: The B-10 document states the system supports "bulk export" for both single patient and patient population. The FHIR path uses standard OAuth2/SMART authorization (documented in G10 PDF). The mandatory disclosure statement mentions "One-time fee per provider upon request of data extraction," suggesting a vendor-assisted process rather than pure self-service.
- **Single-patient**: Yes (stated in B-10 document)
- **Bulk capability**: Yes (stated in B-10 document; FHIR Bulk Data referenced)
- **Access constraints**: Requires OAuth2 credentials for FHIR API. Data portability incurs a one-time per-provider fee (`RadysansEHRCostsandLimitations.pdf`).

## 4. Export Content: What's In It

### No Data Dictionary

There is **no data dictionary** provided. The B-10 documentation is a single-page PDF that lists C-CDA section names and points to the FHIR API documentation. There are no field definitions, no entity-relationship diagrams, no value set specifications, and no mapping between internal data model and export format.

### C-CDA Export Content

The B-10 document (`B-10-Documentation.pdf`) lists 22 C-CDA sections. These are the standard C-CDA sections corresponding to USCDI v1 data classes. The document provides section names only — no field-level detail, no description of what data populates each section, and no vendor-specific extensions. The reader is referred to the HL7 C-CDA specification for format details.

### FHIR Export Content

The G10 documentation (`G10ApplicationAccessTermsandCondition.pdf`, 41 pages) documents 18 FHIR resource types. Each resource section includes:
- Endpoint URL
- Search parameters (2–7 per resource)
- Sample JSON output

All 18 resources have sample outputs included in the documentation.

### Vendor's own content organization

The vendor does not organize content into custom categories. The C-CDA sections follow the HL7 standard naming, and the FHIR resources follow US Core STU 3.1.1. There are no vendor-specific groupings, extensions, or custom resources.

**C-CDA Sections (22 total, from `B-10-Documentation.pdf`):**

| Section Name | Format | Documentation Detail |
|---|---|---|
| Allergies, Adverse Reactions, Alerts | C-CDA XML | Name only |
| Assessment Plan | C-CDA XML | Name only |
| Chief Complaint | C-CDA XML | Name only |
| Cognitive Status | C-CDA XML | Name only |
| Demographics | C-CDA XML | Name only |
| Reason for Visit / Encounters | C-CDA XML | Name only |
| Family History | C-CDA XML | Name only |
| Functional Status | C-CDA XML | Name only |
| Goals | C-CDA XML | Name only |
| Health Concerns | C-CDA XML | Name only |
| Immunizations | C-CDA XML | Name only |
| Instructions | C-CDA XML | Name only |
| Lab Results | C-CDA XML | Name only |
| Medical Equipment UDI | C-CDA XML | Name only |
| Medications | C-CDA XML | Name only |
| Plan of Care | C-CDA XML | Name only |
| Problem List | C-CDA XML | Name only |
| Procedures | C-CDA XML | Name only |
| Reason for Referral | C-CDA XML | Name only |
| Social History | C-CDA XML | Name only |
| Plan of Treatment | C-CDA XML | Name only |
| Vitals | C-CDA XML | Name only |

**FHIR Resources (18 total, from `G10ApplicationAccessTermsandCondition.pdf`):**

| Resource Type | Search Parameters | Has Sample Output | Category |
|---|---|---|---|
| AllergyIntolerance | Clinical-Status, Patient | Yes | Clinical |
| CarePlan | Category, Date, Patient, Status | Yes | Clinical |
| CareTeam | Patient, Status | Yes | Clinical |
| Condition | Category, Clinical-Status, Patient, Onset-Date | Yes | Clinical |
| Device | Patient, Type | Yes | Clinical |
| DiagnosticReport | Status, Patient, Category, Code, Date | Yes | Clinical |
| DocumentReference | _id, Status, Patient, Category, Type, Date, Period | Yes | Clinical |
| Encounter | _id, Class, Date, Identifier, Patient, Status, Type | Yes | Clinical |
| Goal | Lifecycle-status, Patient, Target-date | Yes | Clinical |
| Immunization | Patient, Status, Date | Yes | Clinical |
| MedicationRequest | Status, Intent, Patient, Encounter, Authoredon | Yes | Clinical |
| Observation | Status, Category, Code, Date, Patient | Yes | Clinical |
| Organization | Name, Address | Yes | Administrative |
| Patient | _id, Birthdate, Family, Gender, Given, Identifier, Name | Yes | Demographics |
| Practitioner | Name, Identifier | Yes | Administrative |
| PractitionerRole | Specialty, Practitioner | Yes | Administrative |
| Procedure | Status, Patient, Date, Code | Yes | Clinical |
| Provenance | Patient, Id | Yes | Infrastructure |

These 18 resources are exactly the US Core STU 3.1.1 required set — no more, no less. There are no vendor-specific FHIR resources, no custom extensions, and no resources for billing, claims, insurance, scheduling, or any administrative/financial data.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export consists of two standard clinical data exchange formats:

1. **C-CDA**: 22 standard sections covering USCDI v1 clinical data classes. No field-level documentation beyond section names. This is a clinical summary format — by definition it captures a patient's clinical snapshot, not the full record.

2. **FHIR R4 US Core**: 18 resource types matching US Core STU 3.1.1. The G10 document provides the most detail — each resource has a sample JSON output showing actual field structures and coded values (SNOMED, LOINC, RxNorm, CVX). But these are standard FHIR resources with no vendor extensions.

The coverage is exclusively clinical. The vendor has not documented any export of billing, claims, insurance, scheduling, referral tracking, transcription, or any other administrative/financial data that the product stores.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | C-CDA Demographics section; FHIR Patient resource (7 search params, sample output) | Standard USCDI demographics |
| Encounters / visits | ✅ Covered | C-CDA Reason for Visit/Encounters; FHIR Encounter resource | Clinical encounter data; no scheduling/appointment data |
| Problems / conditions / diagnoses | ✅ Covered | C-CDA Problem List; FHIR Condition resource | Standard problem list |
| Medications / prescriptions | ✅ Covered | C-CDA Medications; FHIR MedicationRequest resource | Prescription data present; no medication administration records |
| Allergies | ✅ Covered | C-CDA Allergies section; FHIR AllergyIntolerance resource | Standard allergy data |
| Immunizations | ✅ Covered | C-CDA Immunizations; FHIR Immunization resource | Standard immunization records |
| Vitals | ✅ Covered | C-CDA Vitals; FHIR Observation resource | Standard vital signs |
| Lab results | ✅ Covered | C-CDA Lab Results; FHIR DiagnosticReport + Observation resources | Lab results present |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport may include imaging; no dedicated imaging section evident in samples | Product supports CPOE for diagnostic imaging; unclear if imaging reports are fully captured |
| Procedures | ✅ Covered | C-CDA Procedures; FHIR Procedure resource | Standard procedure records |
| Clinical notes / documents | ✅ Covered | C-CDA has multiple note-related sections (Chief Complaint, Assessment Plan, etc.); FHIR DocumentReference resource | Clinical notes present; transcription records unclear |
| Care plans / goals | ✅ Covered | C-CDA Goals, Plan of Care, Plan of Treatment; FHIR CarePlan, Goal, CareTeam resources | Standard care planning data |
| Orders / referrals | ✅ Covered | C-CDA Reason for Referral; FHIR MedicationRequest (order intent) | Clinical referral reasons present; referral tracking/pre-auth data absent |
| Insurance / coverage | ❌ Not covered | No insurance/coverage resources in export | Product has insurance eligibility verification and registration with insurance card scanning; **significant gap** |
| Claims / billing | ❌ Not covered | No billing resources in export | Product has full eBilling module with charge capture, claim submission, denial tracking, EOB/ERA; **major gap** |
| Payments | ❌ Not covered | No payment resources in export | Product handles payment posting, reconciliation, patient statements; **significant gap** |
| Consents / directives | ❌ Not covered | No consent resources in export | No evidence product stores formal advance directives; likely N/A but uncertain |
| Patient communications / portal messages | ❌ Not covered | No communication resources in export | Product has patient portal with representative access; gap if messaging exists |
| Specialty-specific (ENT) | ❌ Not covered | No specialty-specific data in export beyond standard USCDI | Known customer is ENT practice; any ENT-specific clinical data (audiograms, procedural detail) would be absent |

**Summary**: 12 of 17 applicable domains are covered, but all coverage is limited to what C-CDA and FHIR US Core natively support. The entire billing/financial domain (3 domains: insurance, claims, payments) is absent despite being a core product capability. Specialty-specific clinical data is also absent.

## 6. Documentation Quality

**Overall: Very poor.** The (b)(10) documentation is a single page listing section/resource names with no vendor-specific detail.

- **Data dictionary**: None provided
- **Field-level documentation**: None for C-CDA; implicit via FHIR sample outputs only
- **Value sets**: Not documented (standard terminologies visible in FHIR samples: SNOMED, LOINC, RxNorm, CVX)
- **Relationships**: Not documented (standard FHIR references visible in samples)
- **Sample data**: FHIR sample JSON outputs exist in the G10 document (1 example per resource type), but no sample C-CDA files
- **Machine-readable schemas**: None (no XSD, no FHIR StructureDefinitions, no JSON Schema)
- **Export instructions**: No step-by-step instructions for initiating an export; the B-10 document states capability but not process

**Could a developer build an import from this documentation?** A developer familiar with C-CDA and FHIR could build a consumer for the standard portions, since the formats are well-specified by HL7. However, they would have no insight into vendor-specific data, no understanding of what data is or isn't included beyond the standard, and no way to verify completeness. The documentation provides no information about the internal data model, what data is excluded from the export, or how to handle vendor-specific nuances.

## 7. Overall Assessment

### Classification

**Standard-based projection**: The EHI export is entirely composed of existing C-CDA and FHIR US Core capabilities repackaged as the (b)(10) mechanism. There is no native database export, no data dictionary, and no vendor-specific content. The export covers the USCDI v1 clinical data subset but omits the product's billing, scheduling, insurance, and specialty clinical data.

### Key Findings

1. **Classic C-CDA/FHIR repackaging**: The (b)(10) documentation explicitly points to C-CDA sections and the (g)(10) FHIR API as the two export mechanisms. The 18 FHIR resources match exactly the US Core STU 3.1.1 required set — no additions, no extensions (`G10ApplicationAccessTermsandCondition.pdf`, sections 1.1–1.18).

2. **Complete absence of billing/financial data**: The product has a full eBilling module with claims, payments, EOBs/ERAs, and denial tracking, yet no billing or financial resources appear in the export. This is a significant EHI gap given billing records are explicitly part of the HIPAA designated record set.

3. **One-page (b)(10) documentation with no data dictionary**: The entire EHI export documentation is a single-page PDF (`B-10-Documentation.pdf`, 61 KB) listing 22 C-CDA section names and deferring to the FHIR API docs. No field-level detail, no entity definitions, no schema, no sample files.

4. **Fee-gated export**: The mandatory disclosure statement (`RadysansEHRCostsandLimitations.pdf`) confirms a "one-time fee per provider upon request of data extraction" for data portability, suggesting this is a vendor-assisted process rather than self-service.

5. **G10 API doc is the only substantive artifact**: The 41-page G10 document with sample FHIR JSON outputs provides more detail than the actual (b)(10) documentation, but it's standard FHIR API documentation, not EHI export documentation.

### Summary Stats

    Classification:  Standard-based projection
    Export format:   C-CDA XML + FHIR R4 JSON
    Model type:      Standard projection (C-CDA + US Core FHIR)
    Entities:        22 C-CDA sections + 18 FHIR resources (no native entities)
    Fields:          N/A (no data dictionary; fields defined by standards)
    Descriptions:    N/A (no vendor-specific field documentation)
    Sample data:     Partial (FHIR sample outputs in G10 doc; no C-CDA samples)
    Bulk export:     Yes (claimed for both C-CDA and FHIR Bulk Data)
    Domains covered: 12 of 17 applicable domains (clinical only)

### Bottom Line

Radysans EHR's (b)(10) export is a textbook case of repackaging existing C-CDA and FHIR API capabilities as an EHI export. A patient or provider would receive a clinical summary covering standard USCDI data (problems, meds, allergies, labs, vitals, etc.) but would get none of the billing, claims, insurance, payment, or scheduling data that the product stores — data that is squarely within the HIPAA designated record set. The single biggest gap is the complete absence of billing/financial data from a product that has a full eBilling and revenue cycle management module.
