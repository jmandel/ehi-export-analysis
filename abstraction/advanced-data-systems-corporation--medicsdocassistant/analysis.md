# EHI Export Analysis: Advanced Data Systems Corporation

**Product**: MedicsDocAssistant v8.0
**Analysis date**: 2026-02-15
**CHPL ID**: 10785 (15.02.05.1044.AVDD.01.01.1.220111)

## 1. Product Context

MedicsDocAssistant is an ambulatory EHR developed by Advanced Data Systems Corporation (ADS), a privately held healthcare IT company founded in 1977. The product has been in production since 2000 and is certified under the 2015 Edition Cures Update (43 criteria, certified January 2022). It targets small-to-mid-size ambulatory practices across 28+ specialties, with particular strength in behavioral health/addiction treatment, radiology, and internal medicine.

**What the product stores (relevant to EHI export completeness):**

- **Clinical data**: Demographics (with USCDI fields), problem lists, medication lists, allergies, vitals, lab results, immunizations, procedures, clinical notes (specialty-specific templates for 28+ specialties), care plans, goals, implantable devices, family health history, social/psychological/behavioral data, smoking status
- **Orders & prescriptions**: CPOE for medications, labs, radiology; e-prescribing via Newcrop/Surescripts (controlled and non-controlled)
- **Documents & communications**: C-CDA transitions of care, consult letters, referrals, incoming faxes routed to patient records, patient portal secure messages
- **Specialty-specific data**: ASAM-certified behavioral health assessments, group therapy session records, dual diagnosis tracking, treatment plans auto-generated from assessments
- **Patient portal data**: Questionnaires/forms, appointment requests, online payments
- **Billing/PM data**: MedicsDocAssistant integrates tightly with **MedicsPremier** (practice management) as an "All-in-One Suite." Billing, claims, insurance, and financial data live in MedicsPremier. Whether the (b)(10) export covers PM data is a key question.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `B10_MedicsDocAssistant.html` (2,375 bytes, 57 lines) | The registered (b)(10) EHI export documentation page. Single paragraph claiming C-CDA and FHIR US Core export, with links only to external HL7 standards. No vendor-specific content. | **Primary source; extremely thin** |
| `B10_MedicsCloud.html` (2,346 bytes, 58 lines) | Identical (b)(10) page for the sibling product MedicsCloud v11.0. Same single paragraph, same external links. | Low (confirms pattern) |
| `FHIRMedicsDocAssistant.htm` (566 KB, 10,568 lines) | FHIR API documentation (g(10), not b(10)). Word-to-HTML document describing SMART on FHIR launch, OAuth2 authorization, and 20 US Core resource types with search parameters and sample JSON responses. Mentions Bulk Data 1.0.1 in intro but contains no $export documentation. | **Most detailed artifact; defines the FHIR resource scope** |
| `service-base-urls.json` (682 KB) | FHIR Bundle with 922 entries (461 Endpoint + 461 Organization resources) listing production FHIR service URLs for client practices. | Low (operational infrastructure, confirms FHIR service is live) |
| `B10_page_screenshot.png` (132 KB) | Screenshot of the B10 page as rendered. Confirms the page is a single paragraph with two links and vast whitespace. | Corroborative |
| `chpl_b10_details.png` (218 KB) | Screenshot of CHPL listing showing (b)(10) details: Conformance Method = Attestation, Export Documentation URL = the B10 page. | Corroborative |
| `chpl_g10_details.png` (217 KB) | Screenshot of CHPL listing showing (g)(10) details: USCDI v3, FHIR R4, US Core 6.1.0, SMART App Launch 2.0.0, Bulk Data 1.0.0, Inferno 3.3.2. API Documentation URL = the FHIR doc. | Corroborative (note: g(10) references US Core 6.1.0 while b(10) page references US Core 3.1.1 — version discrepancy) |
| `FHIR_API_doc_screenshot.png` (227 KB) | Screenshot of the FHIR API documentation header. | Low |

**Key observation**: There are no data dictionaries, no schemas, no sample export files, no field-level documentation, and no export procedure instructions among the artifacts. The entire (b)(10) documentation is a single paragraph on a static HTML page.

## 3. Export Mechanics

- **Format(s)**: C-CDA XML (USCDI v1) and FHIR v4.0.1 US Core v3.1.1, per the B10 page
- **Mechanism**: Unclear. The B10 page states "authorized users can generate the Electronic Health Information Export" but provides no instructions for how to trigger it — no UI screenshots, no API endpoint documentation, no step-by-step procedure. The FHIR API doc (g(10)) describes single-patient SMART on FHIR queries but not a bulk export mechanism. Bulk Data 1.0.1 is mentioned in the FHIR doc intro but no $export endpoint is documented.
- **Single-patient vs bulk**: The B10 page claims both "single patient and also the patient population" export, but neither mechanism is documented
- **Access constraints**: No information provided about fees, turnaround time, or access requirements beyond "authorized users"

## 4. Export Content: What's In It

### 4a. B10 page content

The entire (b)(10) documentation (`B10_MedicsDocAssistant.html`) is a single paragraph:

> "MedicsDocAssistant authorized users can generate the Electronic Health Information Export (EHI) for a single patient and also the patient population in both HL7 CCDA xml format that comply with USCDI v1 requirements standards and HL7 FHIR v 4.0.1 US Core v 3.1.1."

No data dictionary. No field definitions. No entity list. No schema. No sample data. No export procedure.

The two links on the page point to the **external HL7 standards** (C-CDA IG and US Core IG), not to any vendor-specific documentation.

### 4b. FHIR API documentation (g(10) — indirect evidence)

The FHIR API documentation (`FHIRMedicsDocAssistant.htm`, 10,568 lines) is the g(10) API documentation, not b(10)-specific. However, since the B10 page claims FHIR US Core as an export format, this document defines the outer boundary of what the FHIR-based export could contain.

The document describes 20 FHIR resource type sections, each with search parameters and sample JSON responses:

| # | Resource Type (vendor's label) | FHIR Resource | Category |
|---|---|---|---|
| 1 | Patient | Patient | Demographics |
| 2 | AllergyIntolerance | AllergyIntolerance | Clinical |
| 3 | CarePlan | CarePlan | Clinical |
| 4 | CareTeam | CareTeam | Clinical |
| 5 | Condition Tests | Condition | Clinical |
| 6 | Implantable Device Tests | Device | Clinical |
| 7 | DiagnosticReport for Report and Note exchange | DiagnosticReport | Clinical/Documents |
| 8 | Laboratory Results | Observation | Labs |
| 9 | DocumentReference | DocumentReference | Documents |
| 10 | Goal | Goal | Clinical |
| 11 | Immunization | Immunization | Clinical |
| 12 | Medication | MedicationRequest | Medications |
| 13 | Smoking Status | Observation | Social History |
| 14 | Vitals | Observation | Clinical |
| 15 | Procedure | Procedure | Clinical |
| 16 | Encounter | Encounter | Clinical |
| 17 | Organization | Organization | Administrative |
| 18 | Practitioner | Practitioner | Administrative |
| 19 | Provenance | Provenance | Administrative |
| 20 | Clinical Notes Guidance | DocumentReference | Documents |

These are exactly the US Core STU3.1.1 / USCDI v1 resource types — the standard set required for g(10) certification. No vendor-specific extensions or additional resource types are documented.

**Notable FHIR resources NOT documented** (verified by parsing the full HTML):
- FamilyMemberHistory — despite (a)(12) certification for Family Health History
- Coverage, Claim, ExplanationOfBenefit — no financial/billing resources
- MedicationAdministration, MedicationDispense — only MedicationRequest
- ServiceRequest — no order resources beyond what's in CarePlan
- Questionnaire, QuestionnaireResponse — no patient-submitted forms
- RelatedPerson — no emergency contacts/guarantors as separate resources
- Consent — no consent/directive resources

### 4c. No vendor-specific data dictionary

There is no data dictionary, no field-level documentation, no entity-relationship diagram, no schema file, and no sample export data. The vendor provides zero information about how their internal data model maps to C-CDA or FHIR, what fields are populated, what value sets are used, or what data is included beyond the standard resource types.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation describes coverage exclusively in terms of two external standards:

1. **C-CDA XML (USCDI v1)**: No vendor-specific documentation of which C-CDA sections are populated or what data maps to them. The external C-CDA IG defines standard sections (Demographics, Problems, Medications, Allergies, Results, Vital Signs, Procedures, Encounters, Immunizations, etc.) but without vendor documentation it's impossible to confirm which are populated.

2. **FHIR US Core 3.1.1**: 20 resource types documented in the g(10) FHIR API doc. These cover the USCDI v1 clinical data set. No extensions, no additional resource types, no vendor-specific profiles.

The vendor provides no indication of any data beyond the standard USCDI v1 scope. There are no categories, no modules, no groupings — just a one-sentence reference to two standards.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ⚠️ Partial | FHIR Patient resource documented in g(10) API doc; no vendor-specific field mapping | Standard USCDI v1 demographics only; product stores additional specialty-specific demographic fields (per 28+ specialty configurations) that are unlikely captured |
| Encounters / visits | ⚠️ Partial | FHIR Encounter resource documented | Standard Encounter resource; specialty-specific encounter data (behavioral health sessions, group therapy) not addressed |
| Problems / conditions | ✅ Covered | FHIR Condition resource documented | Standard coverage via US Core |
| Medications / prescriptions | ⚠️ Partial | FHIR MedicationRequest documented; MedicationAdministration and MedicationDispense absent | Prescription orders covered; e-prescribing transmission history via Newcrop/Surescripts not addressed |
| Allergies | ✅ Covered | FHIR AllergyIntolerance documented | Standard coverage via US Core |
| Immunizations | ✅ Covered | FHIR Immunization documented | Standard coverage via US Core |
| Vitals | ✅ Covered | FHIR Observation (Vitals) documented | Standard coverage via US Core |
| Lab results | ✅ Covered | FHIR Observation (Laboratory) documented | Standard coverage via US Core |
| Imaging / diagnostic reports | ⚠️ Partial | FHIR DiagnosticReport documented | Report metadata likely covered; actual images and radiology-specific data (for practices using MedicsRIS) not addressed |
| Procedures | ✅ Covered | FHIR Procedure documented | Standard coverage via US Core |
| Clinical notes / documents | ⚠️ Partial | FHIR DocumentReference and DiagnosticReport documented | Standard clinical notes (progress notes, H&P, etc.) likely covered; specialty-specific templates (28+ specialties), FlowText dictation records, and AI-generated content unclear |
| Care plans / goals | ✅ Covered | FHIR CarePlan and Goal documented | Standard coverage via US Core |
| Orders / referrals | ❌ Not covered | No ServiceRequest or referral-specific resource documented | Product supports CPOE for meds, labs, radiology, and referral documents; order data beyond prescriptions not addressed |
| Insurance / coverage | ❌ Not covered | No Coverage resource documented | MedicsPremier stores insurance/payer data; significant gap if deployed as "All-in-One Suite" |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing resources documented | MedicsPremier handles claims (HCFA, UB, Workers' Comp, No-Fault); significant gap if deployed as "All-in-One Suite" |
| Payments | ❌ Not covered | No payment resources documented | MedicsPremier handles payments; patient portal payments also not addressed |
| Consents / directives | ❌ Not covered | No Consent resource documented | Product likely stores consent records; not addressed |
| Patient communications / portal messages | ❌ Not covered | No Communication resource documented | MedicsPortal supports secure messaging, questionnaires; not addressed |
| Specialty-specific (behavioral health) | ❌ Not covered | No behavioral health resources documented | Product has dedicated ASAM assessments, group therapy tracking, dual diagnosis, MAT, treatment plans from assessments; none addressed |
| Specialty-specific (other 27+ specialties) | ❌ Not covered | No specialty resources documented | Product has specialty-specific templates/configurations for radiology, cardiology, dermatology, etc.; none addressed |
| Family health history | ❌ Not covered | No FamilyMemberHistory resource documented | Product is certified for (a)(12) Family Health History; significant gap |

**Summary**: Of 20 applicable domains, 6 are fully covered (standard USCDI v1 clinical data), 5 are partially covered (standard resources that don't capture the product's full depth), and 9 are not covered at all. The missing domains include billing/insurance (from the integrated MedicsPremier), all specialty-specific clinical data, patient portal interactions, and family health history.

## 6. Documentation Quality

**Rating: Extremely poor — among the worst possible.**

The entire (b)(10) documentation is a single 2,375-byte HTML page containing one paragraph and two links to external standards. There is:

- **No data dictionary** — zero field names, types, or descriptions
- **No export procedure** — no instructions for how to trigger the export
- **No schema** — no machine-readable format specification
- **No sample data** — no example exports in either format
- **No vendor-specific mapping** — no documentation of how the product's internal data model maps to C-CDA or FHIR
- **No value sets** — no coded field documentation
- **No relationship documentation** — no entity-relationship information
- **No error handling** — no documentation of what happens when exports fail
- **No bulk export documentation** — despite claiming population-level export

A developer attempting to import data from this export would have no vendor-specific guidance whatsoever. They would need to independently know C-CDA and FHIR US Core and hope the vendor's implementation conforms to those standards without deviations. Even then, they would have no way to know what data domains are included or excluded.

The g(10) FHIR API documentation (`FHIRMedicsDocAssistant.htm`) provides substantially more detail (10,568 lines, search parameters, sample responses), but it is **not linked from the B10 page** and is registered separately on CHPL as API documentation, not export documentation.

## 7. Overall Assessment

### Classification

**Standard-based projection**

The export is explicitly described as C-CDA XML and FHIR US Core — two standard clinical data formats. The 20 documented FHIR resource types are exactly the US Core STU3.1.1 resource types required for g(10) certification. There is no evidence of any vendor-specific data model export, no native database tables, and no content beyond the USCDI v1 clinical summary scope.

This is a textbook case of repackaging the g(10) FHIR API / C-CDA clinical summary as the (b)(10) "all EHI" export.

### Key Findings

1. **The (b)(10) export is indistinguishable from the g(10) API.** The B10 page references the same standards (FHIR US Core 3.1.1, C-CDA USCDI v1) used for g(10) certification. The FHIR API doc lists exactly the 20 US Core resource types — the g(10) minimum — with no extensions. There is no evidence of any b(10)-specific work.

2. **Documentation is a single paragraph — 2,375 bytes total.** The entire (b)(10) documentation is one sentence claiming C-CDA and FHIR export, plus two links to external HL7 standards. No data dictionary, no export instructions, no sample data, no schema.

3. **Billing, insurance, and financial data are absent.** MedicsDocAssistant is typically deployed as an "All-in-One Suite" with MedicsPremier (practice management). Neither C-CDA nor FHIR US Core carry billing/claims data, and no billing resources are documented. This is a significant coverage gap for the designated record set.

4. **Specialty-specific clinical data (28+ specialties) is unaddressed.** The product's key differentiator is specialty-specific templates and assessments (ASAM behavioral health assessments, group therapy records, radiology reports, etc.). None of this data is represented in the USCDI v1 resource set.

5. **Family health history is missing despite (a)(12) certification.** The product is certified for 170.315(a)(12) Family Health History, but FamilyMemberHistory is not among the 20 documented FHIR resource types. This is a clear gap within the product's own certified data scope.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   C-CDA XML, FHIR R4 (US Core 3.1.1)
Model type:      Standard projection (USCDI v1)
Entities:        20 FHIR resource types (US Core minimum)
Fields:          N/A (no data dictionary)
Descriptions:    N/A (no field-level documentation)
Sample data:     No
Bulk export:     Claimed but undocumented
Domains covered: 6 of 20 applicable domains fully covered; 5 partial
```

### Bottom Line

MedicsDocAssistant's (b)(10) export is its g(10) FHIR API and C-CDA clinical summary repackaged with a one-paragraph web page. A patient or provider would receive a standard clinical summary covering core clinical data (problems, meds, allergies, labs, vitals, immunizations) but would miss billing records, specialty-specific assessments (behavioral health, radiology, etc.), patient portal interactions, family history, and all financial data from the integrated MedicsPremier practice management system. The single biggest gap is the complete absence of any vendor-specific data model export — the product stores far more than USCDI v1, but the export documentation gives no indication that any of it is included.
