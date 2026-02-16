# EHI Export Analysis: Advanced Data Systems Corporation

**Product**: MedicsDocAssistant
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.02.05.1044.AVDD.01.01.1.220111 (CHPL ID 10785)

## 1. Product Context

MedicsDocAssistant is Advanced Data Systems Corporation's (ADS) legacy-generation ambulatory EHR, in production since 2000, currently certified at version 8.0 (ONC 2015 Edition Cures Update, certified January 2022). It serves 28+ clinical specialties including behavioral health/addiction treatment, radiology, internal medicine, cardiology, and more.

MedicsDocAssistant is the **EHR component** of an integrated suite. Billing, scheduling, and financial data reside primarily in **MedicsPremier**, the companion practice management system. The two are typically deployed together as the "All-in-One Suite" with shared data.

Key data domains the product stores:
- **Clinical**: encounter notes (specialty-specific templates), problem lists, medications/prescriptions (via Newcrop e-prescribing), allergies, lab results (bidirectional integration), vitals, immunizations, procedures, care plans, implantable devices, family health history, social/behavioral data
- **Specialty-specific**: ASAM assessments for behavioral health, group therapy records, dual diagnosis tracking, radiology reports (via MedicsRIS)
- **Documents**: clinical notes, consult letters, referral documents, incoming faxes, imaging attachments
- **Patient portal**: secure messages, questionnaires, online payments
- **Billing** (via MedicsPremier): claims, charges, payments, insurance/payer data, eligibility, denial management
- **Public health**: immunization registry submissions, syndromic surveillance, cancer case reports, electronic case reports

This product context is relevant because a genuine (b)(10) export should cover all EHI the product stores about patients — not just the USCDI clinical summary subset.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `B10_MedicsDocAssistant.html` | 2,375 bytes (57 lines) | The registered (b)(10) EHI export documentation page. Contains a single paragraph and two external links. | **Primary artifact** — but contains almost no information |
| `B10_MedicsCloud.html` | 2,346 bytes | Identical B10 page for sibling product MedicsCloud v11.0. Confirms same approach across products. | Low — duplicates B10 page |
| `FHIRMedicsDocAssistant.htm` | 566,412 bytes (10,568 lines) | FHIR API documentation registered as g(10) API docs on CHPL. Word-to-HTML document describing SMART on FHIR launch, OAuth2, and 20 US Core resource type sections. | **Most informative artifact** — though it's g(10) documentation, not b(10) |
| `service-base-urls.json` | 681,905 bytes | FHIR Bundle with 461 Endpoint + 461 Organization resources listing client practice FHIR service URLs. | Low — confirms FHIR service is active across 461 client practices |
| `B10_page_screenshot.png` | 132 KB | Screenshot of B10 page as rendered in Chrome. | Low — visual confirmation |
| `chpl_b10_details.png` | 218 KB | Screenshot of CHPL listing showing b(10) certification: Conformance Method is Attestation. | Low — confirms attestation-only conformance |
| `chpl_g10_details.png` | 217 KB | Screenshot of CHPL listing showing g(10) details: USCDI v3, FHIR R4, US Core 6.1.0, SMART App Launch 2.0.0, Bulk Data 1.0.0. | Moderate — shows g(10) standards |
| `FHIR_API_doc_screenshot.png` | 227 KB | Screenshot of FHIR API documentation page header. | Low — visual confirmation |

The B10 page — the sole (b)(10)-specific documentation — contains 103 words of content. The FHIR API doc provides detail about the FHIR API but is g(10) documentation, not b(10) documentation, and was not linked from the B10 page.

## 3. Export Mechanics

- **Format(s)**: HL7 C-CDA XML (USCDI v1) and HL7 FHIR R4 (US Core 3.1.1)
- **Mechanism**: Unclear. The B10 page states "authorized users can generate the Electronic Health Information Export (EHI)" but provides no instructions on how — no UI screenshots, no API endpoints, no step-by-step guide. The FHIR API doc (g(10)) describes SMART on FHIR authorization and individual resource queries but does not document a bulk/$export endpoint.
- **Single-patient**: Claimed ("for a single patient") but no instructions provided
- **Bulk/population**: Claimed ("and also the patient population") but no instructions or documentation for how population-level export works. The FHIR API doc mentions "Bulk Data 1.0.1" once in the introduction but contains zero documentation of a $export endpoint or workflow.
- **Access constraints/fees**: Not documented

## 4. Export Content: What's In It

### No vendor-specific data dictionary

The B10 page provides **no data dictionary, no field definitions, no schema, no sample data, and no export format specification**. The vendor's entire (b)(10) documentation is:

> "MedicsDocAssistant authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population in both HL7 CCDA xml format that comply with USCDI v1 requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."

The only links are to external HL7 standards:
1. HL7 C-CDA Implementation Guide: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=492
2. HL7 FHIR US Core IG STU3.1.1: https://hl7.org/fhir/us/core/STU3.1.1/

### Content inferred from FHIR API documentation (g(10))

Since the B10 page claims FHIR US Core 3.1.1 as an export format, the g(10) FHIR API documentation (`FHIRMedicsDocAssistant.htm`) provides the best available indication of what data types the export might cover. It documents 20 resource sections:

| # | Section Name | FHIR Resource Type | Category |
|---|---|---|---|
| 1 | Patient | Patient | Demographics |
| 2 | AllergyIntolerance | AllergyIntolerance | Clinical |
| 3 | CarePlan | CarePlan | Clinical |
| 4 | CareTeam | CareTeam | Clinical |
| 5 | Condition | Condition | Clinical |
| 6 | Implantable Device | Device | Clinical |
| 7 | DiagnosticReport | DiagnosticReport | Clinical |
| 8 | Laboratory Results | Observation | Clinical |
| 9 | DocumentReference | DocumentReference | Clinical |
| 10 | Goal | Goal | Clinical |
| 11 | Immunization | Immunization | Clinical |
| 12 | Medication | MedicationRequest | Clinical |
| 13 | Smoking Status | Observation | Clinical |
| 14 | Vitals | Observation | Clinical |
| 15 | Procedure | Procedure | Clinical |
| 16 | Encounter | Encounter | Clinical |
| 17 | Organization | Organization | Administrative |
| 18 | Practitioner | Practitioner | Administrative |
| 19 | Provenance | Provenance | Administrative |
| 20 | Clinical Notes Guidance | DocumentReference | Clinical |

These map to 17 unique FHIR resource types (Observation covers 3 profiles: Laboratory, Vitals, Smoking Status; DocumentReference covers 2 sections). This is exactly the US Core STU3.1.1 / USCDI v1 resource set — the same set required for g(10) Standardized API certification. No vendor extensions, custom resources, or additional data beyond the standard are documented.

**Key numbers:**
- Entities/resource types documented: 17 unique FHIR resource types (20 sections)
- Field-level documentation: **None** from the vendor. The B10 page defers entirely to external HL7 specifications.
- Value sets/code systems: None vendor-specific
- Relationships/foreign keys: None documented
- Sample data: None provided (the FHIR API doc has example JSON responses but these are g(10) examples, not b(10) export samples)

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's B10 documentation provides no organizational structure — it is a single paragraph. The only structure comes from the g(10) FHIR API documentation, which organizes content by FHIR resource type following the US Core IG specification.

The export, as described, covers the standard USCDI v1 clinical data classes:
- **Demographics**: Patient resource
- **Clinical conditions**: Condition, AllergyIntolerance
- **Medications**: MedicationRequest (via Medication section)
- **Results**: Observation (Laboratory, Vitals, Smoking Status), DiagnosticReport
- **Clinical notes**: DocumentReference (including Clinical Notes Guidance section)
- **Care coordination**: CarePlan, CareTeam, Goal
- **Procedures/devices**: Procedure, Device (Implantable)
- **Immunizations**: Immunization
- **Encounters**: Encounter
- **Administrative**: Organization, Practitioner, Provenance

This is the standard US Core / USCDI v1 data set. There is no evidence of any vendor-specific data beyond this standard set. No billing, insurance, specialty-specific, or custom form data is mentioned or documented anywhere.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | Patient resource (US Core) | US Core Patient covers basic demographics but may not include all vendor-specific fields (e.g., custom identifiers, detailed contact preferences) |
| Encounters / visits | ⚠️ Partial | Encounter resource (US Core) | Basic encounter data; unlikely to capture full encounter documentation, templates, or specialty-specific encounter details |
| Problems / conditions / diagnoses | ✅ Covered | Condition resource (US Core) | Standard problem list coverage via US Core |
| Medications / prescriptions | ⚠️ Partial | MedicationRequest resource | Covers medication orders; may miss e-prescribing history/transmission details via Newcrop |
| Allergies | ✅ Covered | AllergyIntolerance resource | Standard allergy/intolerance coverage |
| Immunizations | ✅ Covered | Immunization resource | Standard immunization coverage |
| Vitals | ✅ Covered | Observation (Vitals) | Standard vital signs coverage |
| Lab results | ✅ Covered | Observation (Laboratory), DiagnosticReport | Standard lab result coverage |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport | Reports may be covered; actual images/attachments likely not |
| Procedures | ✅ Covered | Procedure resource | Standard procedure coverage |
| Clinical notes / documents | ⚠️ Partial | DocumentReference, Clinical Notes Guidance | Standard clinical notes; specialty-specific templates (28+ specialties) with custom fields unlikely to be fully captured in US Core DocumentReference |
| Care plans / goals | ✅ Covered | CarePlan, Goal resources | Standard care plan coverage |
| Orders / referrals | ❌ Not covered | No order or referral resources documented | Product handles lab orders, imaging orders, referrals. US Core 3.1.1 does not include ServiceRequest. Gap. |
| Insurance / coverage | ❌ Not covered | No Coverage or insurance resources | MedicsPremier manages insurance/payer data. Neither C-CDA nor US Core 3.1.1 adequately covers insurance. Significant gap for the integrated suite. |
| Claims / billing | ❌ Not covered | No billing/claims resources | MedicsPremier handles claims, charges. FHIR US Core does not include Claim/ExplanationOfBenefit. Major gap. |
| Payments | ❌ Not covered | No payment resources | Portal payments and billing payments not addressed. Gap. |
| Consents / directives | ❌ Not covered | No Consent resources documented | Not clear if product stores advance directives; if so, this is a gap |
| Patient communications / portal messages | ❌ Not covered | No Communication resources | Product has patient portal with secure messaging. US Core 3.1.1 doesn't include Communication. Gap. |
| Specialty-specific (behavioral health) | ❌ Not covered | No ASAM, group therapy, dual diagnosis resources | Product has dedicated behavioral health/addiction treatment modules with ASAM assessments, group therapy documentation, MAT tracking. None exportable via US Core. **Major gap.** |
| Specialty-specific (28+ specialties) | ❌ Not covered | No specialty template/form data | Product supports 28+ specialty-specific clinical templates. Custom form data cannot be represented in standard US Core resources. **Major gap.** |
| Family health history | ❌ Not covered | No FamilyMemberHistory resource | Product is certified for (a)(12) Family Health History but FamilyMemberHistory is not in the documented resource set |
| Social/behavioral data | ⚠️ Partial | Observation (Smoking Status) only | Product is certified for (a)(15) social, psychological, behavioral data. Only smoking status is documented, not broader SDOH. |

**Summary**: 7 of 20 applicable domains are covered (mostly via standard US Core resources), 4 are partially covered, and 9 are not covered at all. The missing domains include billing/claims, insurance, patient portal communications, specialty-specific clinical data, and family history — all of which the product stores.

## 6. Documentation Quality

The (b)(10) documentation quality is **extremely poor** — among the thinnest possible for a certified product:

- **103 words total** in the B10 page (excluding HTML boilerplate)
- **No data dictionary** — zero field names, types, or descriptions
- **No export instructions** — no UI screenshots, no API endpoints, no workflow description
- **No schema or format specification** — defers entirely to external HL7 standards
- **No sample data** — no example exports in either format
- **No mapping documentation** — no explanation of how internal data maps to C-CDA or FHIR
- **No error handling or edge case documentation**
- **No information about data completeness** — no discussion of what is or isn't included

A developer attempting to import data from this export would have:
1. No vendor-specific guidance whatsoever
2. No way to know what data is actually in the export vs. what's theoretically possible in the standard
3. No understanding of vendor-specific extensions, mappings, or data transformations
4. No sample data to test against

The g(10) FHIR API documentation (566 KB, 10,568 lines) is substantially more detailed, with OAuth2 flows, resource-specific endpoints, search parameters, and example JSON responses. However, this is **not** (b)(10) documentation — it was registered separately on CHPL as g(10) API documentation and was not linked from the B10 page.

## 7. Overall Assessment

### Classification

**Standard-based projection** (minimal/stub documentation)

This is a textbook case of FHIR/C-CDA repackaging as (b)(10). The vendor's "EHI export" is their existing C-CDA and FHIR US Core API — the same data already required for g(10) Standardized API certification — relabeled as a (b)(10) export. The documentation is a single paragraph pointing to external HL7 standards with no vendor-specific content.

### Key Findings

1. **B10 documentation is a single 103-word paragraph** (`B10_MedicsDocAssistant.html`, 2,375 bytes) with no data dictionary, no export instructions, no sample data, and no vendor-specific documentation of any kind. It links only to external HL7 C-CDA and FHIR US Core specifications.

2. **The export is a direct repackaging of the g(10) FHIR API / C-CDA output.** The resource types documented (in the g(10) FHIR API doc) are exactly the US Core STU3.1.1 / USCDI v1 set — 17 unique FHIR resource types across 20 sections. No vendor extensions or additional data types are mentioned.

3. **Major data domains are missing from the export.** Billing/claims (via MedicsPremier), insurance/coverage, specialty-specific clinical data (behavioral health ASAM assessments, 28+ specialty templates), patient portal communications, family health history, and referral/order data are all absent. These are data the product demonstrably stores about patients.

4. **Population/bulk export is claimed but undocumented.** The B10 page states both single-patient and population export are available, but no documentation exists for how population export works. The FHIR API doc mentions "Bulk Data 1.0.1" once in the introduction but contains no $export endpoint documentation.

5. **The B10 page has not been updated since December 5, 2023** (per HTTP Last-Modified header), suggesting no ongoing development effort for (b)(10) compliance beyond the initial certification.

### Summary Stats

```
Classification:  Standard-based projection (minimal/stub documentation)
Export format:   C-CDA XML, FHIR R4 (US Core 3.1.1)
Model type:      Standard projection (no native database model)
Entities:        17 unique FHIR resource types (20 sections, standard US Core set)
Fields:          N/A (no vendor-specific field documentation)
Descriptions:    N/A (defers to external HL7 specifications)
Sample data:     No
Bulk export:     Claimed but undocumented
Domains covered: 7 of 20 applicable domains fully covered; 4 partial; 9 not covered
```

### Bottom Line

MedicsDocAssistant's (b)(10) EHI export is a compliance checkbox, not a genuine effort to export all electronic health information. The entire documentation is a single paragraph pointing to the same C-CDA and FHIR US Core standards already required for g(10) API certification. A patient or provider requesting their complete EHI would receive a clinical summary covering standard USCDI data classes but would miss billing records, specialty-specific assessments (particularly behavioral health/addiction treatment data), patient portal communications, family history, and referral data — all of which the product stores. The single biggest gap is the complete absence of vendor-specific data export: no native data model, no custom fields, no specialty templates, and no billing data.
