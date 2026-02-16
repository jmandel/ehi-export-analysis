# EHI Export Analysis: AssureCare LLC

**Product**: iPatientCare (versions 18.0, 22.5, 23.0)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2627.iPat.18.00.1.171201, 15.04.04.2627.iPat.22.01.1.221221, 15.04.04.2627.iPat.23.02.1.230522

## 1. Product Context

iPatientCare is an **integrated ambulatory EHR, practice management, and billing platform** developed by AssureCare LLC (which acquired iPatientCare in 2019). It targets small to mid-size physician practices, community health centers, rural health clinics, and specialty practices (mental/behavioral health, cardiology, pain management, orthopedics, pediatrics, internal medicine, women's health).

The product stores:
- **Clinical records**: demographics, problem lists, medication lists, allergy lists, vital signs, clinical notes, family health history, social/psychological/behavioral data, implantable device lists, growth charts
- **Orders & results**: e-prescriptions (including EPCS), lab orders/results, imaging orders/reports
- **Documents**: scanned documents, referral letters, consent forms, clinical attachments
- **Scheduling**: appointments, wait lists, recall lists, provider schedules
- **Billing & financial data**: insurance information, eligibility verification, claims (submitted/tracked), payment postings, electronic remittances, denials, appeals, patient balances, fee schedules
- **Patient portal data**: secure messages, prescription refill requests, appointment requests, patient demographic updates
- **Telehealth**: virtual visit records
- **Quality measures**: eCQM calculations, MIPS scores

This is a full-featured ambulatory EHR with integrated billing — the (b)(10) export should cover clinical, billing, scheduling, and patient communication data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `170.315b10-Electronic-Health-Information-Export-v1.0.0.2.pdf` (3 pages, 127 KB) | The entire (b)(10) export documentation. Single substantive page states export uses C-CDA XML (USCDI v1) and FHIR R4 Bulk Data. No data dictionary, no field definitions, no export instructions. | **Primary but extremely thin** |
| `SMART-on-FHIR-API-Authentication-and-Access-Guide-1.0.0.3.pdf` (118 pages, 570 KB) | SMART on FHIR / (g)(10) API documentation. Covers OAuth2 auth, FHIR endpoints, and example requests/responses for 26 US Core resource types. Updated Nov 2025 for US Core STU 6.1.0 and USCDI v3. | **Detailed but is (g)(10) documentation, not (b)(10)-specific** |
| `fhir-capability-statement.json` (23 KB) | FHIR R4 CapabilityStatement from production server. Lists 26 resource types with US Core profiles. Server self-identifies as "Inferno Reference Server for US Core, Bulk Data, and SMART App Launch" based on HAPI FHIR. | **Confirms standard USCDI scope** |
| `fhir-endpoints-bundle.json` (194 KB) | FHIR Bundle of Endpoint/Organization resources listing 107 practice tenants with FHIR service URLs. Shows multi-tenant architecture. | **Infrastructure only** |
| `smart-configuration.json` (1 KB) | SMART well-known configuration: OAuth2 endpoints, supported capabilities (launch-ehr, launch-standalone, backend services). | **Infrastructure only** |
| `page-screenshot-top.png`, `page-screenshot-full.png` | Screenshots of the ONC certification page at ipatientcare.com/onc-certified-health-it/ | **Confirms page layout and links** |

## 3. Export Mechanics

- **Format**: C-CDA XML (USCDI v1) and FHIR R4 (US Core STU 6.1.0 / USCDI v3)
- **Mechanism**: The (b)(10) PDF states the product "provide[s] export of electronic health information (EHI) for a single patient as well as for patient population" in both formats. For FHIR, it refers to the (g)(10) SMART on FHIR API documentation. For C-CDA, it refers to HL7 C-CDA specifications. No UI workflow or step-by-step instructions are provided.
- **Single-patient vs bulk**: Both supported per the documentation (single patient and "patient population")
- **Access constraints**: The FHIR API requires OAuth2 authentication (SMART App Launch). The SMART guide describes client registration, authorization flows, and token management. No mention of fees.

## 4. Export Content: What's In It

### No data dictionary exists

The (b)(10) documentation provides **zero field-level detail**. It consists of:
1. A title page and revision history (page 1-2)
2. A single substantive page (page 3) stating that the export uses C-CDA (USCDI v1) and FHIR R4 Bulk Data (US Core STU 3.1.1 — note: the SMART guide was updated to STU 6.1.0 but the (b)(10) PDF still references STU 3.1.1)
3. References to HL7 specifications and the (g)(10) API guide for details

There is no product-specific data dictionary, no mapping of iPatientCare internal data to export fields, no description of what data elements are included or excluded, no sample export files, and no schema beyond pointing to the standard FHIR/C-CDA specifications.

### FHIR resource types from CapabilityStatement

The FHIR server supports 26 resource types, all standard US Core / USCDI:

| Resource Type | US Core Profiles | Interactions | Search Params | Category |
|---|---|---|---|---|
| AllergyIntolerance | 1 | 4 | 2 | USCDI: Allergies |
| CarePlan | 1 | 4 | 4 | USCDI: Assessment & Plan |
| CareTeam | 1 | 4 | 2 | USCDI: Care Team |
| Condition | 3 | 4 | 5 | USCDI: Problems/Health Status |
| Coverage | 1 | 2 | 1 | USCDI: Insurance |
| Device | 1 | 4 | 2 | USCDI: Medical Devices |
| DiagnosticReport | 2 | 5 | 5 | USCDI: Clinical Tests/Labs |
| DocumentReference | 1 | 5 | 7 | USCDI: Clinical Notes |
| Encounter | 1 | 4 | 7 | USCDI: Encounters |
| Goal | 1 | 4 | 3 | USCDI: Goals |
| Group | 0 | 0 | 0 | Bulk Data (infrastructure) |
| Immunization | 1 | 4 | 3 | USCDI: Immunizations |
| Location | 1 | 4 | 5 | USCDI: Facility Info |
| Medication | 1 | 3 | 0 | USCDI: Medications |
| MedicationDispense | 1 | 2 | 3 | USCDI: Medications |
| MedicationRequest | 1 | 4 | 5 | USCDI: Medications |
| Observation | 37 | 4 | 5 | USCDI: Vitals/Labs/Assessments |
| Organization | 1 | 4 | 2 | USCDI: Facility Info |
| Patient | 1 | 4 | 7 | USCDI: Demographics |
| Practitioner | 1 | 4 | 2 | USCDI: Care Team |
| PractitionerRole | 1 | 4 | 2 | USCDI: Care Team |
| Procedure | 1 | 4 | 4 | USCDI: Procedures |
| Provenance | 1 | 3 | 0 | USCDI: Provenance |
| RelatedPerson | 1 | 2 | 2 | USCDI: Demographics |
| ServiceRequest | 1 | 1 | 6 | USCDI: Orders |
| Specimen | 1 | 2 | 2 | USCDI: Laboratory |

All 26 resource types map directly to USCDI data classes. There are no vendor-specific extensions, no custom resources, and no resources addressing billing, scheduling, or other non-USCDI domains.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor provides exactly what USCDI and US Core require — nothing more. The 26 FHIR resource types correspond precisely to the US Core 6.1.0 profile set. The (b)(10) PDF explicitly frames the export in terms of USCDI compliance ("CCDA xml files which comply to United States Core Data for Interoperability (USCDI), Version 1 requirements"). The SMART guide documents each resource type with example API requests and responses, all using standard US Core profiles.

There are no vendor-specific categories, no custom data structures, and no indication of any export content beyond the FHIR (g)(10) / C-CDA exchange surface.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient, RelatedPerson resources | Standard US Core fields only; product stores more |
| Encounters / visits | ✅ Covered | Encounter resource | Standard US Core; no visit-level detail beyond base |
| Problems / conditions | ✅ Covered | Condition (3 profiles) | Standard USCDI |
| Medications / prescriptions | ✅ Covered | Medication, MedicationRequest, MedicationDispense | Standard USCDI; product does EPCS — unclear if full Rx detail exported |
| Allergies | ✅ Covered | AllergyIntolerance | Standard USCDI |
| Immunizations | ✅ Covered | Immunization | Standard USCDI |
| Vitals | ✅ Covered | Observation (37 profiles including vitals) | Standard USCDI vital sign profiles |
| Lab results | ✅ Covered | Observation, DiagnosticReport, Specimen | Standard USCDI |
| Imaging / diagnostic reports | ✅ Covered | DiagnosticReport | Standard USCDI |
| Procedures | ✅ Covered | Procedure | Standard USCDI |
| Clinical notes / documents | ✅ Covered | DocumentReference, DiagnosticReport | Standard USCDI clinical note types |
| Care plans / goals | ✅ Covered | CarePlan, Goal | Standard USCDI |
| Orders / referrals | ⚠️ Partial | ServiceRequest (read-only, 1 interaction) | Basic order data; no referral workflow detail |
| Insurance / coverage | ⚠️ Partial | Coverage resource | Basic USCDI coverage; product stores eligibility verification, payer credentialing — not exported |
| Claims / billing | ❌ Not covered | No billing resources (no Claim, ExplanationOfBenefit, Account, Invoice, ChargeItem) | **Major gap**: product has full billing/RCM with claims, payments, denials, appeals |
| Payments | ❌ Not covered | No payment resources | Product tracks payment postings, remittances, patient balances |
| Consents / directives | ❌ Not covered | No Consent resource | Product stores consent forms (document management) |
| Patient communications | ❌ Not covered | No Communication resource | Product has patient portal with secure messaging |
| Scheduling | N/A | No Schedule/Appointment resources | Scheduling data is operational, not EHI per se |
| Custom forms / specialty | ❌ Not covered | No QuestionnaireResponse or custom resources | Product has specialty-specific templates (mental health, cardiology, etc.) |
| Scanned documents | ❌ Not covered | DocumentReference exists but limited to USCDI clinical note types | Product stores scanned records, referrals, attachments |

## 6. Documentation Quality

The (b)(10) export documentation is **functionally empty**:
- **3-page PDF** with 1 substantive page pointing to C-CDA specs and the (g)(10) API guide
- **No data dictionary** — zero field definitions, zero entity descriptions
- **No export workflow** — no UI screenshots, no step-by-step instructions
- **No sample data** — no example exports provided
- **No schema** — relies entirely on external HL7 specifications
- **No mapping** — no documentation of how iPatientCare internal data maps to C-CDA sections or FHIR resources
- **Version inconsistency** — the (b)(10) PDF references US Core STU 3.1.1 while the SMART guide (updated Nov 2025) references US Core STU 6.1.0

The 118-page SMART guide is well-structured (g)(10) API documentation with OAuth2 flows, example requests/responses for each resource type, and endpoint URLs. However, it is (g)(10) documentation, not (b)(10)-specific, and contains no information about data beyond USCDI.

A developer could use the SMART guide to query the FHIR API for USCDI data. They could not determine what other data iPatientCare stores, how to export billing records, or what fields are available beyond US Core Must Support elements.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The export covers only USCDI/US Core FHIR resources — the regulatory minimum for clinical exchange. iPatientCare is an integrated EHR, practice management, and billing platform that stores extensive non-USCDI data: claims, payment postings, denials, appeals, eligibility verification, patient portal messages, scanned documents, consent forms, specialty-specific templates, and referral workflows. None of this is addressed in the export. The (b)(10) documentation is a 3-page document that provides zero additional information beyond "we do C-CDA and FHIR." There is no way to determine from the documentation whether any non-USCDI data can be exported, and the CapabilityStatement confirms only standard US Core resources.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of a vendor relabeling their existing (g)(10) FHIR Bulk Data API and C-CDA exchange as "(b)(10)." The evidence is overwhelming:
1. The (b)(10) PDF explicitly says "Please refer 170.315(g)(10) SmartOnFHIR API Documentation.PDF for the API Specifications" — it is literally pointing to the (g)(10) document.
2. The CapabilityStatement lists exactly the 26 US Core resource types required by (g)(10) with no additions.
3. The FHIR server self-identifies as "Inferno Reference Server for US Core, Bulk Data, and SMART App Launch" — the Inferno test server framework, not a purpose-built EHI export system.
4. The C-CDA export is described only in terms of USCDI v1 compliance, with references to standard HL7 C-CDA specifications.
5. No vendor-specific data dictionary, no custom resources, no billing/PM data, no documentation of anything beyond the standard clinical exchange surface.

### Key Findings

1. **The (b)(10) export is the (g)(10) API with a new label.** The entire (b)(10) documentation consists of a single page that says "we do C-CDA and FHIR" and refers users to the (g)(10) SMART on FHIR guide. No purpose-built EHI export exists.

2. **Billing and practice management data is completely absent.** iPatientCare is an integrated EHR+PM+billing product, but the export includes zero billing resources (no claims, payments, denials, remittances, superbills, fee schedules). This is a major gap in the designated record set.

3. **No data dictionary exists.** There are zero field-level definitions, zero entity descriptions, and zero export-specific documentation. The vendor relies entirely on external HL7/FHIR specifications.

4. **The FHIR server appears to be a generic Inferno reference server**, not a purpose-built export system. The CapabilityStatement publisher field says "Inferno Reference Server for US Core, Bulk Data, and SMART App Launch."

5. **Patient portal messages, scanned documents, consent forms, and specialty templates are not exported**, despite the product storing all of these.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   C-CDA XML, FHIR R4 (US Core STU 6.1.0)
    Entities:        26 (FHIR resource types, all standard US Core)
    Fields:          N/A (no data dictionary)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Yes (FHIR Bulk Data)
    Domains covered: 12 of 18 applicable domains (all USCDI-scope; 0 non-USCDI)

### Bottom Line

iPatientCare's (b)(10) export is their existing (g)(10) FHIR API and C-CDA exchange relabeled. A patient or provider would receive USCDI-scope clinical data but no billing records, no patient portal messages, no scanned documents, and no specialty-specific data — despite the product storing all of these. The single biggest gap is the complete absence of billing/RCM data from a product whose integrated billing capability is a core selling point.
