# EHI Export Analysis: Advanced Data Systems Corporation

**Product**: MedicsDocAssistant v8.0
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.1044.AVDD.01.01.1.220111 (CHPL #10785)

## 1. Product Context

MedicsDocAssistant is a legacy-generation ambulatory EHR from Advanced Data Systems Corporation (ADS), first released in 2000, certified under ONC 2015 Edition Cures Update (version 8.0, January 2022). It serves ambulatory practices across 28+ specialties including internal medicine, behavioral health/addiction treatment, radiology, cardiology, dermatology, OB/GYN, oncology, and others.

**Clinical capabilities** include encounter-based documentation with specialty-specific templates, CPOE (medications, labs, radiology, procedures), e-prescribing via Newcrop, bidirectional lab integration, immunization registry reporting, clinical decision support, and care plan management. It also supports clinical notes via FlowText voice dictation and a patient portal (MedicsPortal) with secure messaging, online forms, and patient access to records.

**Key for EHI scope**: MedicsDocAssistant is the EHR component of a larger suite. Billing, scheduling, and financial data reside primarily in **MedicsPremier** (practice management), marketed as a tightly integrated "All-in-One Suite." The product also has specialty modules for behavioral health (ASAM assessments, group therapy tracking), radiology (MedicsRIS), and telemedicine. The (b)(10) export is certified only for MedicsDocAssistant, so the question is whether it covers the EHR's full data breadth — including any PM/billing data accessible through MedicsDocAssistant — or just USCDI-scope clinical summaries.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/B10_MedicsDocAssistant.html` (2,375 bytes) | The registered (b)(10) EHI export documentation page. A single HTML page with one paragraph and two external links. | **Most critical** — this is the entirety of the vendor's (b)(10) documentation |
| `downloads/B10_MedicsCloud.html` (2,346 bytes) | Sibling (b)(10) page for MedicsCloud v11.0. Identical content except product name. | Low — confirms pattern across products |
| `downloads/FHIRMedicsDocAssistant.htm` (566 KB, 10,568 lines) | FHIR API documentation (g)(10). Word-to-HTML document covering SMART on FHIR, OAuth2, and 17 US Core resource types with sample JSON. | **Most substantive** — the only artifact showing what data the system can export via FHIR |
| `downloads/service-base-urls.json` (682 KB) | FHIR Bundle with Endpoint/Organization resources for client practices. | Low — confirms FHIR service is operational |
| `downloads/B10_page_screenshot.png` | Screenshot of B10 page rendered in browser. | Low — visual confirmation |
| `downloads/FHIR_API_doc_screenshot.png` | Screenshot of FHIR API doc header. | Low — visual confirmation |
| `downloads/chpl_b10_details.png` | CHPL listing showing (b)(10) conformance method is Attestation. | Moderate — confirms attestation-only approach |
| `downloads/chpl_g10_details.png` | CHPL listing showing (g)(10) details: US Core 6.1.0, FHIR R4, Bulk Data 1.0.0. | Moderate — confirms FHIR capability |

## 3. Export Mechanics

- **Format**: HL7 C-CDA XML (USCDI v1) and HL7 FHIR v4.0.1 US Core v3.1.1
- **Mechanism**: Unclear. The (b)(10) page states "authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population" but provides no instructions on how (no UI screenshots, no API endpoints, no step-by-step guide).
- **Single-patient vs bulk**: The page claims both single-patient and population-level export.
- **Access constraints**: No information on fees, turnaround time, or access restrictions.
- **Documentation of process**: None. There are no instructions for how a user or administrator would initiate an export.

## 4. Export Content: What's In It

### No vendor-specific data dictionary

The (b)(10) documentation page (`B10_MedicsDocAssistant.html`) contains exactly one substantive paragraph:

> "MedicsDocAssistant authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population in both HL7 CCDA xml format that comply with USCDI v1 requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."

The page then links to:
1. The HL7 C-CDA implementation guide (external standard)
2. The HL7 FHIR US Core STU3.1.1 implementation guide (external standard)

There is **no vendor-specific data dictionary, no field mapping, no schema, no sample export data, no entity list, and no documentation of what product-specific data elements map to which C-CDA sections or FHIR resources.**

### FHIR API documentation as proxy

The FHIR API documentation (`FHIRMedicsDocAssistant.htm`) — which is the (g)(10) API doc, not the (b)(10) doc — provides the most detail on what the system can output via FHIR. It documents **17 US Core resource types** with sample JSON responses:

| FHIR Resource | USCDI Class | Category |
|---|---|---|
| Patient | Patient Demographics | Demographics |
| AllergyIntolerance | Allergies & Intolerances | Clinical |
| CarePlan | Assessment & Plan of Treatment | Clinical |
| CareTeam | Care Team Members | Clinical |
| Condition | Problems | Clinical |
| Device | Medical Devices | Clinical |
| DiagnosticReport | Clinical Tests / Diagnostic Imaging | Clinical |
| DocumentReference | Clinical Notes | Clinical |
| Encounter | Encounters | Clinical |
| Goal | Goals & Preferences | Clinical |
| Immunization | Immunizations | Clinical |
| MedicationRequest | Medications | Clinical |
| Observation | Vitals / Labs / Clinical Tests | Clinical |
| Organization | Facility Information | Administrative |
| Practitioner | Care Team Members | Administrative |
| Procedure | Procedures | Clinical |
| Provenance | Provenance | Administrative |

**Notably absent from the FHIR API documentation**: Coverage, Claim, ExplanationOfBenefit, ChargeItem, Invoice, Account, FamilyMemberHistory, Location, Specimen, RelatedPerson, MedicationDispense, Consent, Communication, QuestionnaireResponse, ServiceRequest. Zero billing/financial resources are documented.

No vendor-specific FHIR extensions are documented. All sample responses use standard US Core profiles only.

### Vendor's own content organization

The vendor provides no content organization of its own. The only structure comes from the external standards referenced:
- C-CDA sections (per the HL7 C-CDA IG — standard sections, no vendor-specific additions documented)
- FHIR US Core 3.1.1 resource types (17 resources as listed above)

Since there is no vendor-specific data dictionary, no entity/field inventory can be constructed beyond what the FHIR API documentation shows.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's (b)(10) documentation claims the export produces data in C-CDA and FHIR US Core 3.1.1 format compliant with "USCDI v1 requirements standards." This is, by definition, the USCDI clinical exchange surface — not a purpose-built EHI export.

The FHIR API documentation shows 17 US Core resource types. These map precisely to the standard US Core profile set for USCDI v1, covering: demographics, allergies, care plans, care teams, conditions, devices, diagnostic reports, clinical notes, encounters, goals, immunizations, medications, observations (vitals/labs), procedures, and provenance. This is the standard (g)(10) FHIR API surface.

There is no evidence of any data beyond USCDI scope. No billing tables, no specialty-specific data structures, no custom forms, no behavioral health assessments, no portal messages, no referral tracking, no insurance/coverage details.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient resource (US Core standard fields only) | Product stores race, ethnicity, preferred language, sexual orientation, gender identity per (a)(5) — unclear if all are in export. No vendor field mapping. |
| Encounters / visits | ⚠️ Partial | Encounter resource (US Core) | Standard encounter data only; no visit-level detail beyond US Core minimum |
| Problems / conditions | ⚠️ Partial | Condition resource (US Core) | Standard problem list; product likely stores more detail (onset context, verification workflows) |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest resource (US Core) | Prescription data present; no medication administration records, no detailed e-prescribing history from Newcrop |
| Allergies | ✅ Covered | AllergyIntolerance resource (US Core) | Standard allergy data |
| Immunizations | ✅ Covered | Immunization resource (US Core) | Standard immunization records |
| Vitals | ⚠️ Partial | Observation resource (US Core) | Standard vital signs; depth of internal data unknown |
| Lab results | ⚠️ Partial | Observation, DiagnosticReport (US Core) | Standard lab results; bidirectional lab integration likely stores more detail |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport, DocumentReference (US Core) | Standard reports; radiology-specific data (if MedicsRIS integrated) not addressed |
| Procedures | ⚠️ Partial | Procedure resource (US Core) | Standard procedure list |
| Clinical notes / documents | ⚠️ Partial | DocumentReference, DiagnosticReport (US Core) | C-CDA clinical notes present; specialty templates, FlowText entries, custom forms unknown |
| Care plans / goals | ⚠️ Partial | CarePlan, Goal (US Core) | Standard care plan; product's care plan (b)(9) functionality may store more |
| Orders / referrals | ❌ Not covered | No ServiceRequest resource documented | Product has CPOE for meds, labs, radiology, procedures; referral tracking not in export |
| Insurance / coverage | ❌ Not covered | No Coverage resource | Product integrates with MedicsPremier for insurance; no coverage data in export |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, ChargeItem resources | MedicsPremier handles billing; no billing data in EHI export |
| Payments | ❌ Not covered | No payment-related resources | MedicsPremier handles payments; not in export |
| Consents / directives | ❌ Not covered | No Consent resource | Not documented |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | MedicsPortal includes secure messaging; not in export |
| Specialty-specific (behavioral health) | ❌ Not covered | No QuestionnaireResponse or specialty resources | ASAM assessments, group therapy tracking, dual diagnosis programs not in export |
| Specialty-specific (radiology) | ❌ Not covered | No radiology-specific resources beyond standard DiagnosticReport | MedicsRIS integration data not addressed |
| Family health history | ❌ Not covered | No FamilyMemberHistory resource | Product stores family history per (a)(12) certification; not in export |

## 6. Documentation Quality

The (b)(10) export documentation is **effectively empty**. It consists of:

- **One paragraph** (49 words) stating that exports are available in C-CDA and FHIR formats
- **Two external links** to HL7 standard specifications (not vendor-specific documentation)
- **No data dictionary** — not even a list of what data elements are included
- **No export instructions** — no UI screenshots, no API calls, no step-by-step process
- **No sample data** — no example exports to examine
- **No schema or mapping** — no documentation of how product-internal data maps to C-CDA sections or FHIR resources
- **No vendor extensions** — no indication of any product-specific additions beyond the standard

A developer could not build an import from this documentation. A patient could not understand what data they would receive. The documentation provides no way to assess what is or isn't included in the export without actually requesting one.

The FHIR API documentation (g)(10) is more substantive (566 KB, 10,568 lines) but is not (b)(10) documentation — it describes the standard FHIR API for app integration, not a comprehensive EHI export.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documentation is too thin to fully assess coverage, but all available evidence points to USCDI-scope-only coverage. The export formats are explicitly stated as "USCDI v1 requirements standards" C-CDA and "US Core v 3.1.1" FHIR. The FHIR API documentation shows exactly the 17 standard US Core resource types with no extensions. Zero billing, specialty, or operational data resources are present. For a product that stores behavioral health assessments, has integrated billing via MedicsPremier, supports portal messaging, tracks referrals, and has specialty configurations across 28+ specialties, an export limited to USCDI v1 covers only a fraction of the designated record set.

**Axis 2 — Export approach: Repackaged existing export**

This is a textbook case of repackaging. The (b)(10) page explicitly states the export uses C-CDA (USCDI v1) and FHIR US Core 3.1.1 — the same standards and versions used for clinical exchange under (g)(10) and transitions of care (b)(1)/(b)(2). The documentation links only to external HL7 specs. The FHIR API doc shows exactly the standard US Core resource types. There is no vendor-specific data dictionary, no additional data domains, no custom mappings, and no evidence that any work was done beyond pointing the existing C-CDA/FHIR capabilities at the (b)(10) requirement. The CHPL listing confirms the conformance method is "Attestation" — the vendor self-attested compliance rather than demonstrating it through testing.

### Key Findings

1. **The (b)(10) documentation is a single 49-word paragraph** with two links to external HL7 standards. This is among the thinnest (b)(10) documentation possible — no data dictionary, no export instructions, no sample data, no field mapping (`B10_MedicsDocAssistant.html`).

2. **The export is explicitly USCDI v1 / US Core 3.1.1** — the vendor's own words confirm this is the clinical exchange surface, not a purpose-built EHI export. The 17 FHIR resource types documented in the API exactly match the standard US Core profile set.

3. **Zero billing or financial data** is included. The product integrates with MedicsPremier for billing, claims, payments, and insurance — none of which appear in the export. No Coverage, Claim, ExplanationOfBenefit, or financial resources are documented.

4. **Specialty-specific data is absent**. Despite serving 28+ specialties with dedicated configurations (including behavioral health ASAM assessments, group therapy tracking, radiology workflows), no specialty-specific data structures appear in the export.

5. **Family health history is missing** despite (a)(12) certification requiring it. The FHIR API documentation does not include FamilyMemberHistory resources, and neither format documentation addresses it.

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   HL7 C-CDA XML, HL7 FHIR R4 US Core 3.1.1
    Entities:        17 FHIR resource types (standard US Core only)
    Fields:          N/A (no vendor-specific field documentation)
    Descriptions:    N/A
    Sample data:     No
    Bulk export:     Claimed (single patient and population) but undocumented
    Domains covered: 2-3 of 15+ applicable domains (allergies, immunizations partially; most domains absent or partial)

### Bottom Line

MedicsDocAssistant's (b)(10) export is its existing C-CDA and FHIR US Core clinical exchange rebranded as EHI export, documented with a single paragraph and two links to external standards. A patient requesting their complete health information would receive only the USCDI v1 clinical summary — missing billing records, specialty assessments (behavioral health, radiology), portal messages, referral tracking, family history, and all practice management data from the integrated MedicsPremier system. The single biggest gap is the complete absence of any vendor-specific documentation: without a data dictionary or field mapping, it is impossible to verify what data is actually included even within the claimed USCDI scope.
