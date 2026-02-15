# EHI Export Analysis: InPracSys

**Product**: InPracSys EHR  
**Analysis date**: 2026-02-15  
**CHPL ID**: 15.05.05.2762.INPS.01.00.1.191206 (CHPL #10194)

## 1. Product Context

InPracSys EHR is a cloud-based EHR system built specifically for urology practices, developed by Innovative Practice Systems, Inc. (Minneapolis, MN). Founded in 2003 by Dr. Ashu Kataria, the company is very small (~25 employees, sub-$1M revenue). The product is certified across 35+ ONC criteria (version 9.0, certified 2019-12-06).

**Key data domains the product stores** (relevant to export completeness):

- **Clinical charting**: Single-page "Point and Click" interface with "FastCharting" for rapid encounter documentation (HPI, ROS, exam, assessment/plan). Urology-specific templates pre-loaded.
- **Urology-specific clinical data**: Urine analysis, bladder scans, TRUS (transrectal ultrasound) results, stent tracking — the specialty data that differentiates this product.
- **Billing**: Superbill generation, E/M coding, Level 1 coding, professional component anatomical pathology billing. Vendor claims 99% clean claim rate.
- **Care Pathways / PRACTICE iQ**: Stepped therapy programs, pre-authorization, drug program qualification — described as a significant revenue feature ($2,500–$7,500/patient/year).
- **Risk Management**: Automated clinical decision support with urology-specific alerts (e.g., stents placed but not removed, missed ultrasounds). Related to the separate RiskAssistMD product.
- **E-Prescribing**: Via SureScripts/DoseSpot integration.
- **Patient Portal**: Records access, appointments, messaging, account management.
- **Lab and imaging orders/results**: Certified for CPOE (a)(1)-(a)(3).
- **Care coordination**: C-CDA transitions of care, clinical information reconciliation, electronic referrals, Direct messaging.
- **Quality measures**: CQM/PQRS reporting, Meaningful Use attestation.
- **Public health reporting**: Syndromic surveillance (f)(2), electronic case reporting (f)(5).

The product's customer base appears extremely small (possibly single-digit clinics), with only one identifiable customer (Comprehensive Urologic Care, S.C. in Illinois).

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `Disclosure-EHR-Inpracsys_NewV6.1.pdf` (192 KB, 3 pages) | Mandatory ONC disclosure letter. Page 3 contains the (b)(10) statement: export produces ZIP files containing XML files, links to FHIR page for format details. | **High** — contains the (b)(10) disclosure text |
| `fhir-api-documentation-page.html` (691 KB) | FHIR API documentation page linked from the disclosure as the "EHI export format." Documents 15 FHIR resource-type endpoints with field definitions, cardinality, types, and sample JSON output. | **High** — the only substantive technical documentation |
| `FhirServiceBaseBundleV10.json` (4 KB) | FHIR Bundle with one Endpoint resource (pointing to `sfp-proxy23604.azurewebsites.net/fhir`) and two sample Organization resources with placeholder data. | **Low** — service configuration only |
| `screenshot-disclosure-page.png` (259 KB) | Screenshot of disclosure page with embedded PDF viewer. | **Low** — confirms page layout |
| `screenshot-disclosure-bottom.png` (191 KB) | Screenshot showing download links: "Download EHI export format here" → /fhir, "Download Service URL Bundle here" → JSON file. | **Medium** — confirms link structure |
| `screenshot-fhir-page.png` (305 KB) | Screenshot of FHIR API documentation page navigation. | **Low** — confirms page structure |

**No sample export files, data dictionaries, schemas (XSD/JSON Schema), or export procedure documentation were provided.**

## 3. Export Mechanics

- **Format**: The disclosure PDF states: "The export(s) can be downloaded as a zip file containing .xml file(s)." However, the linked "EHI export format" documentation describes a FHIR JSON API. This is a direct contradiction — the PDF says XML/ZIP, the documentation describes JSON REST API responses. There is no documentation for the XML format.
- **Mechanism**: Unclear. The disclosure says "authorized users" can export, but no user guide, UI screenshots, or procedural documentation explains how to trigger the export. The FHIR page documents a REST API (OAuth 2 + Bearer token), suggesting API-based access rather than a UI export button.
- **Single-patient vs bulk**: The disclosure states both "single patient as well as for the patient population." The FHIR API documentation shows per-patient queries (`?pid=...`), with no bulk export endpoint documented.
- **Access constraints**: OAuth 2 authentication required. The FHIR API is hosted on Azure (`fhirips.azurehealthcareapis.com`). No information on fees, turnaround time, or request process for patients.

## 4. Export Content: What's In It

The export documentation consists entirely of the FHIR API documentation page. This page documents 15 FHIR resource-type endpoints with a total of **303 fields** across all resources. Field-level documentation includes names, FHIR data types, cardinality, and descriptions for 300 of 303 fields (99%).

### Non-standard serialization

The sample JSON outputs in the documentation use a **non-standard serialization** that does not conform to the FHIR JSON specification. Instead of standard FHIR property names, the samples use C#/.NET FHIR library internal object model names:

- `TotalElement` instead of `total`
- `SystemElement.Value` instead of `system`
- `CodeElement.Value` instead of `code`
- `DisplayElement.Value` instead of `display`
- `StatusElement.Value` instead of `status`
- `ValueElement.Value` instead of `value`

This pattern appears 118+ times across the sample outputs (31 occurrences of `SystemElement`, 30 of `DisplayElement`, 25 of `CodeElement`, 20 of `StatusElement`, 12 of `ValueElement`). A developer expecting standard FHIR JSON would not be able to parse these responses without custom adaptation.

### Non-standard resource types

The API uses non-standard endpoint paths and resource type names: `SmokingStatus`, `LabOrders`, `Procedures` (plural) — these are not valid FHIR R4 resource types. The documentation references Argonaut/DSTU2-era profile URLs despite claiming FHIR R4 compliance.

### Vendor's own content organization

| Resource Section | FHIR Resource | Fields | Described | Types | Category |
|---|---|---|---|---|---|
| Patients | Patient | 20 | 19 | 19/20 | Demographics |
| Smoking status | Observation | 12 | 12 | 11/12 | Social History |
| Condition(Problem) | Condition | 29 | 29 | 27/29 | Problems/Diagnoses |
| Medications | MedicationStatement | 29 | 27 | 27/29 | Medications |
| Allergy or Intolerance | AllergyIntolerance | 21 | 21 | 20/21 | Allergies |
| Laboratory Result DiagnosticReport | DiagnosticReport | 5 | 5 | 4/5 | Lab Results |
| Laboratory Result Observations | DiagnosticOrder | 20 | 20 | 18/20 | Lab Results |
| VitalSign | Observation | 31 | 31 | 30/31 | Vitals |
| Procedure | Procedure | 27 | 27 | 24/27 | Procedures |
| Care Team | Practitioner | 7 | 7 | 5/7 | Care Team |
| Immunization | Immunization | 34 | 34 | 30/34 | Immunizations |
| Implantable Devices/UDI | Device | 16 | 16 | 15/16 | Devices |
| Assessment and Plan of Treatment | CarePlan | 5 | 5 | 4/5 | Care Plans |
| Goal | Goal | 18 | 18 | 16/18 | Goals |
| Health Concern | Condition/HealthcareService | 29 | 29 | 26/29 | Problems/Diagnoses |
| **TOTAL** | **15 resources** | **303** | **300** | **276/303** | |

Full field-level inventory is in `analysis/field_inventory.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly the USCDI v1 / US Core data classes — the same data available through any (g)(10)-certified FHIR API. The 15 documented resource types map one-to-one to the standard USCDI clinical data elements:

- **Demographics** (Patient): 20 fields — name, DOB, gender, race, ethnicity, language, contact info, identifiers.
- **Problems/Diagnoses** (Condition + Health Concern): 58 fields across two resources — clinical status, verification, severity, onset, codes (SNOMED CT), body site, evidence.
- **Medications** (MedicationStatement): 29 fields — medication codes (RxNorm), dosage, form, route, timing.
- **Allergies** (AllergyIntolerance): 21 fields — substance, reaction, criticality, type, category.
- **Lab Results** (DiagnosticReport + DiagnosticOrder): 25 fields — order codes, results, status, dates. Notably thin DiagnosticReport (only 5 fields).
- **Vitals** (Observation): 31 fields — the richest resource; individual vital sign measurements with codes and values.
- **Procedures** (Procedure): 27 fields — procedure codes, dates, body site, performer, outcome.
- **Immunizations** (Immunization): 34 fields — the largest resource; vaccine codes, dates, lot numbers, site, route, dose quantity.
- **Care Plans/Goals** (CarePlan + Goal): 23 fields — assessment, plan, goal descriptions. CarePlan is very thin (5 fields).
- **Care Team** (Practitioner): 7 fields — minimal; name, role, specialty.
- **Devices** (Device): 16 fields — UDI, type, manufacturer, model, serial number.
- **Smoking Status** (Observation): 12 fields — smoking status codes and dates.

**What is completely absent:**
- No billing, financial, or claims data
- No clinical notes or encounter documentation (no DocumentReference)
- No encounters (no Encounter resource)
- No e-prescribing history beyond medication list
- No care pathway / PRACTICE iQ data
- No risk management alerts
- No patient portal messages or communications
- No referral records
- No urology-specific clinical data (urine analysis, bladder scans, TRUS, cystoscopy)
- No insurance or coverage information
- No family health history (despite (a)(12) certification)
- No social determinants of health data (despite (a)(15) certification)

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | Patient resource (20 fields) with race, ethnicity, language extensions | Adequate for basic demographics |
| Encounters / visits | ❌ Not covered | No Encounter resource documented | Product stores encounter data via FastCharting; significant gap |
| Problems / conditions | ✅ Covered | Condition (29 fields) + Health Concern (29 fields) | Adequate |
| Medications / prescriptions | ⚠️ Partial | MedicationStatement (29 fields); no MedicationRequest or e-prescribing history | Product has e-prescribing via DoseSpot; prescription workflow data likely missing |
| Allergies | ✅ Covered | AllergyIntolerance (21 fields) | Adequate |
| Immunizations | ✅ Covered | Immunization (34 fields) | Adequate |
| Vitals | ✅ Covered | Observation/VitalSign (31 fields) | Adequate |
| Lab results | ✅ Covered | DiagnosticReport (5 fields) + DiagnosticOrder (20 fields) | Present but DiagnosticReport is thin |
| Imaging / diagnostic reports | ❌ Not covered | No imaging-specific resources | Product certified for diagnostic imaging CPOE (a)(3); gap |
| Procedures | ✅ Covered | Procedure (27 fields) | Adequate |
| Clinical notes / documents | ❌ Not covered | No DocumentReference, no clinical note export | Product's primary differentiator is FastCharting encounter notes; **major gap** |
| Care plans / goals | ⚠️ Partial | CarePlan (5 fields) + Goal (18 fields) | CarePlan is very thin (5 fields); may miss care pathway detail |
| Orders / referrals | ❌ Not covered | No ServiceRequest or referral resources | Certified for electronic referrals (b)(3); gap |
| Insurance / coverage | ❌ Not covered | No Coverage resource | Product handles billing/superbills; gap |
| Claims / billing | ❌ Not covered | No billing entities whatsoever | Product has billing module with superbills, E/M coding, claims; **major gap** |
| Payments | ❌ Not covered | No payment data | Unclear if product stores payment data |
| Consents / directives | N/A | No evidence product stores advance directives | Not flagged |
| Patient communications | ❌ Not covered | No Communication resource | Product has patient portal with messaging; gap |
| Specialty-specific (Urology) | ❌ Not covered | No urology-specific clinical data | Product stores urine analysis, bladder scans, TRUS data, stent tracking; **major gap** |

**Summary**: 7 of 17 applicable domains are covered (41%). The covered domains are precisely the USCDI clinical summary data classes. All product-specific, billing, specialty, and communication data domains are absent.

## 6. Documentation Quality

**Strengths:**
- The FHIR API documentation is well-structured with per-resource sections, each containing field definitions with names, types, cardinality, and descriptions.
- 300 of 303 fields (99%) have descriptions. 276 of 303 (91%) have typed values.
- Sample JSON output is provided for every resource type.

**Weaknesses:**
- **Non-standard serialization**: The sample JSON uses C#/.NET FHIR library internal object names (`SystemElement`, `CodeElement`, `DisplayElement`, etc.) rather than standard FHIR JSON. A developer following these samples would produce invalid FHIR.
- **Version inconsistency**: Claims FHIR R4 but references Argonaut/DSTU2-era profile URLs and uses non-standard resource type names.
- **Format contradiction**: Disclosure PDF says XML/ZIP; documentation page describes JSON API. No XML format is documented anywhere.
- **No export procedure**: No user guide, no screenshots, no step-by-step instructions for triggering the export from the EHR UI.
- **No sample export files**: No downloadable example ZIP or XML files to demonstrate the actual export output.
- **No schema files**: No XSD, JSON Schema, OpenAPI, or CapabilityStatement.
- **No data model documentation**: No entity-relationship diagrams, no description of how the exported data relates to the EHR's internal data model.

**Could a developer build an import from this documentation?** Partially. The field-level documentation for the 15 FHIR resource types is detailed enough to understand the data structure, but the non-standard serialization would cause confusion, and the lack of sample export files means a developer wouldn't know the actual output format (XML? JSON? What container structure?).

## 7. Overall Assessment

### Classification

**Standard-based projection.** The (b)(10) EHI export documentation is the vendor's (g)(10) FHIR API documentation repackaged. The export covers only the standard USCDI clinical data classes — the same data available through any certified FHIR API. There is no evidence of native database model export, no billing data, no specialty clinical data, no encounter notes, and no documentation of data domains beyond the standard FHIR resources.

### Key Findings

1. **Classic (b)(10)/(g)(10) conflation**: The disclosure page explicitly links to the FHIR API documentation as the "EHI export format." The 15 documented resource types map exactly to USCDI v1 clinical data classes. This is the vendor's FHIR API relabeled as the EHI export — not a genuine "all electronic health information" export. (`Disclosure-EHR-Inpracsys_NewV6.1.pdf`, page 3; `fhir-api-documentation-page.html`)

2. **Major domain gaps**: Billing/superbills, clinical notes (FastCharting), urology-specific clinical data, e-prescribing history, care pathways, patient portal messages, and referrals are all absent from the export. These are core data domains the product stores and uses for patient decision-making. Only 7 of 17 applicable EHI domains are covered.

3. **Non-standard FHIR serialization**: Sample JSON outputs use C#/.NET FHIR library internal property names (`SystemElement.Value`, `CodeElement.Value`, etc.) rather than standard FHIR JSON. This appears 118+ times in the documentation and would cause interoperability failures for any consumer expecting standard FHIR.

4. **Format contradiction**: The disclosure PDF states the export produces "zip file containing .xml file(s)" but the linked documentation describes a JSON REST API. No XML format documentation exists anywhere in the artifacts. The actual export format is unclear.

5. **No export procedure or sample data**: There is no user guide explaining how to trigger the export, no sample export files, and no schema files. A patient or provider requesting an EHI export would have no way to understand what they'd receive or how to request it.

### Summary Stats

```
Classification:  Standard-based projection
Export format:   JSON (FHIR API) — PDF claims XML/ZIP but no XML docs exist
Model type:      Standard projection (FHIR resources, non-standard serialization)
Entities:        15 FHIR resource types
Fields:          303
Descriptions:    99% (300/303)
Sample data:     Yes (inline JSON samples in documentation, non-standard format)
Bulk export:     Unclear (disclosure claims population-level; API docs show per-patient queries)
Domains covered: 7 of 17 applicable domains (41%)
```

### Bottom Line

This is a textbook example of a vendor repurposing their (g)(10) FHIR API documentation as their (b)(10) EHI export. A patient or provider would receive only the standard USCDI clinical summary data — demographics, problems, medications, allergies, labs, vitals, procedures, and immunizations. They would **not** receive their billing records, clinical encounter notes (the product's flagship FastCharting documentation), urology-specific clinical data, care pathway records, or patient portal communications. For a urology-specific EHR, the absence of specialty clinical data is the most significant gap — the very data that distinguishes this product from a generic EHR is excluded from the export.
