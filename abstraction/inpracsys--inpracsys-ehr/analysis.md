# EHI Export Analysis: InPracSys

**Product**: InPracSys EHR
**Analysis date**: 2026-02-16
**CHPL ID**: 15.05.05.2762.INPS.01.00.1.191206

## 1. Product Context

InPracSys EHR is a cloud-based, urology-specific EHR developed by Innovative Practice Systems, Inc. (Minneapolis, MN). It is a very small vendor (~25 employees, sub-$1M revenue) with likely single-digit clinic deployments. The product is certified across 35+ ONC criteria.

Relevant data domains the product stores, per vendor documentation:

- **Clinical**: Patient demographics, problem lists (ICD-10), medications (via DoseSpot e-prescribing), allergies, vitals, lab orders/results, diagnostic imaging, procedures, immunizations, implantable devices, smoking status, family health history, social determinants
- **Charting/Notes**: Full encounter documentation via "FastCharting" (HPI, ROS, exam, assessment/plan) — the product's primary differentiator
- **Urology-specific**: Urine analysis, bladder scans, TRUS results, cystoscopy data, stent tracking — specialty clinical data
- **Billing**: Superbill generation, E/M coding, claims (99% clean claim rate claimed), professional component anatomical pathology billing, pre-authorization (via Care Pathways/PRACTICE iQ module)
- **Care coordination**: C-CDA transitions of care, referrals, direct messaging
- **Patient portal**: View/download/transmit, messaging, appointment scheduling
- **Quality**: CQMs (CMS22, CMS50, CMS68, CMS69, CMS129, CMS134, CMS138, CMS165, CMS645)
- **Risk management**: Urology-specific CDS alerts (stent removal tracking, missed ultrasounds)

This establishes a broad baseline: the export should cover clinical, billing, specialty urology, and care coordination data.

## 2. Artifacts Reviewed

| Artifact | Description | Size/Scope | Informativeness |
|---|---|---|---|
| `Disclosure-EHR-Inpracsys_NewV6.1.pdf` | Mandatory disclosure letter to SLI Compliance. Contains cost tables, certified criteria list, and b(10) disclosure statement. | 3 pages, 192 KB | **High** — contains the only prose description of the EHI export mechanism |
| `fhir-api-documentation-page.html` | FHIR API documentation page from inpracsys.com/fhir/. Documents 15 FHIR resource endpoints with field definitions, cardinality, types, and sample JSON. | 691 KB HTML, 15 resources, 303 response fields, 31 tables | **High** — the primary "export format" documentation |
| `FhirServiceBaseBundleV10.json` | FHIR Bundle containing 1 Endpoint and 2 Organization resources. Points to `sfp-proxy23604.azurewebsites.net/fhir`. | 4 KB, 3 resources | **Low** — service discovery metadata only |
| `screenshot-disclosure-page.png` | Screenshot of disclosure page with embedded PDF | 259 KB | **Low** — confirms page layout |
| `screenshot-disclosure-bottom.png` | Screenshot showing download links: "EHI export format" → /fhir, "Service URL Bundle" → JSON | 191 KB | **Medium** — confirms the link between b(10) disclosure and FHIR page |
| `screenshot-fhir-page.png` | Screenshot of FHIR documentation page | 305 KB | **Low** — visual confirmation |

## 3. Export Mechanics

- **Format**: The disclosure PDF states exports are "downloaded as a zip file containing .xml file(s)." However, the linked documentation page describes a REST JSON API with no XML documentation. There is a contradiction — the actual export format is unclear.
- **Mechanism**: The FHIR API documentation describes REST endpoints at `fhirips.azurehealthcareapis.com` (Azure Health Data Services) queried by patient ID (`?pid=...`). Access requires OAuth 2 Bearer tokens. No UI export button or user-facing export process is documented.
- **Single-patient vs bulk**: The disclosure PDF claims both: "export of electronic health information (EHI) for a single patient as well as for the patient population." The API endpoints accept a patient ID parameter, suggesting single-patient queries. No bulk export mechanism is documented.
- **Access constraints**: OAuth 2 authentication required. No mention of fees for the export itself, though interface setup costs are disclosed for other modules.

## 4. Export Content: What's In It

The export documentation is the vendor's FHIR API page at `inpracsys.com/fhir/`. It documents 15 FHIR resource-type endpoints with 303 total response fields. The documentation provides field names, FHIR data types, cardinality, and descriptions for nearly all fields (300 of 303 fields have descriptions; 276 have explicit types).

The introduction section explicitly states: "The EHI export contains available electronic health information for a single patient or multiple patients in computable file format. The export(s) can be downloaded as a zip file containing .xml file(s)." — directly linking this FHIR API documentation to the b(10) export.

### FHIR serialization anomalies

Sample JSON in the documentation uses a non-standard C#/.NET FHIR library serialization rather than standard FHIR JSON. Properties like `ValueElement`, `SystemElement`, `CodeElement`, `DisplayElement`, `StatusElement`, and `TotalElement` appear throughout 10 of 14 sample outputs. For example, a standard FHIR Condition would have `"code": {"coding": [{"system": "http://snomed.info/sct", "code": "59621000"}]}` but the InPracSys samples show `"Code": {"Coding": [{"SystemElement": {"Value": "http://snomed.info/sct"}, "CodeElement": {"Value": "59621000"}}]}`. This appears to be a direct serialization of the Firely .NET SDK's internal object model. A developer expecting standard FHIR JSON would be unable to parse these responses.

The API endpoint paths are also non-standard: `/SmokingStatus`, `/LabOrders`, `/Procedures`, `/DiagnosticOrder`, `/HealthcareService` instead of standard FHIR resource paths like `/Observation`, `/CarePlan`, `/DiagnosticReport`, `/Condition`.

### Vendor's own content organization

The vendor organizes resources as FHIR resource types. All 15 documented resources are listed below with field counts:

| Resource | Response Fields | Described | Types | Sample JSON |
|---|---|---|---|---|
| Patients | 20 | 19 | 19 | Yes |
| Smoking status | 12 | 12 | 11 | Yes |
| Condition(Problem) | 29 | 29 | 27 | Yes |
| Medications | 29 | 27 | 27 | Yes |
| Allergy or Intolerance | 21 | 21 | 20 | No |
| Laboratory Result DiagnosticReport | 5 | 5 | 4 | Yes |
| Laboratory Result Observations | 20 | 20 | 18 | Yes |
| VitalSign | 31 | 31 | 30 | Yes |
| Procedure | 27 | 27 | 24 | Yes |
| Care Team | 7 | 7 | 5 | Yes |
| Immunization | 34 | 34 | 30 | Yes |
| Implantable Devices/UDI | 16 | 16 | 15 | Yes |
| Assessment and Plan of Treatment | 5 | 5 | 4 | Yes |
| Goal | 18 | 18 | 16 | Yes |
| Health Concern | 29 | 29 | 26 | Yes |
| **TOTAL** | **303** | **300** | **276** | **14/15** |

The full field-level inventory is in `analysis/full-entity-inventory.json`.

Notable observations:
- The "Laboratory Result DiagnosticReport" and "Assessment and Plan of Treatment" resources are thin (5 fields each), essentially wrapping a CarePlan reference with minimal metadata
- "Care Team" has only 7 fields — just practitioner identity information
- The value set references point to DSTU2/Argonaut-era URLs (e.g., DAF Race ValueSet), inconsistent with the claimed "FHIR V4" base
- Field `careProvider` on Patient uses the DSTU2 name (renamed to `generalPractitioner` in STU3+)
- Type `Hl7.Fhir.Model.Instant` and `Hl7.Fhir.Model.Range` appear as field types, exposing C# class names rather than FHIR primitive types

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The export covers exactly the USCDI v1/US Core clinical data classes — the same data domains required for the (g)(10) Standardized API certification. The 15 resources map directly to USCDI data classes:

- **Patient demographics** (20 fields) — including race, ethnicity, religion
- **Smoking status** (12 fields) — via Observation
- **Problems/conditions** (29 fields) + Health Concerns (29 fields) — via Condition
- **Medications** (29 fields) — via MedicationStatement
- **Allergies** (21 fields) — via AllergyIntolerance
- **Lab results** (5 + 20 = 25 fields) — via DiagnosticReport and Observation
- **Vital signs** (31 fields) — via Observation
- **Procedures** (27 fields)
- **Care team** (7 fields) — via Practitioner/CarePlan
- **Immunizations** (34 fields)
- **Implantable devices** (16 fields) — via Device
- **Care plans/goals** (5 + 18 = 23 fields) — via CarePlan and Goal

This is a well-documented FHIR API for the standard clinical data, but it is exactly the (g)(10) API — nothing more. There is no evidence of any vendor-specific, native-model, or non-USCDI data in the export.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patients` (20 fields) incl. race, ethnicity, contacts, language | Adequate for standard demographics |
| Encounters / visits | ❌ Not covered | No Encounter resource documented; encounter is only a reference field on other resources | Product does encounters (FastCharting is encounter-based); gap |
| Problems / conditions / diagnoses | ✅ Covered | `Condition(Problem)` (29 fields), `Health Concern` (29 fields) | Good coverage with ICD/SNOMED coding |
| Medications / prescriptions | ⚠️ Partial | `Medications` (29 fields) — medication statements only | No prescription/dispense data from DoseSpot e-prescribing integration; missing Rx history |
| Allergies | ✅ Covered | `Allergy or Intolerance` (21 fields) | Adequate |
| Immunizations | ✅ Covered | `Immunization` (34 fields) | Adequate |
| Vitals | ✅ Covered | `VitalSign` (31 fields) | Adequate |
| Lab results | ✅ Covered | `Laboratory Result DiagnosticReport` (5 fields), `Laboratory Result Observations` (20 fields) | Adequate for structured results |
| Imaging / diagnostic reports | ⚠️ Partial | Imaging orders may be covered by DiagnosticOrder endpoint but imaging results/reports not explicitly addressed | Product is certified for (a)(3) CPOE-Diagnostic Imaging |
| Procedures | ✅ Covered | `Procedure` (27 fields) | Adequate |
| Clinical notes / documents | ❌ Not covered | No DocumentReference, no note content in any resource | **Major gap** — FastCharting encounter documentation (HPI, ROS, exam, assessment/plan) is the product's core differentiator; entirely absent |
| Care plans / goals | ✅ Covered | `Assessment and Plan of Treatment` (5 fields), `Goal` (18 fields) | Present but thin (5 fields for care plans) |
| Orders / referrals | ❌ Not covered | No ServiceRequest or ReferralRequest resource | Product is certified for (b)(3) Electronic Prescribing/Referrals; gap |
| Insurance / coverage | ❌ Not covered | No Coverage or InsurancePlan resource | Billing module implies insurance data is stored |
| Claims / billing | ❌ Not covered | No Claim, ExplanationOfBenefit, or billing entity | **Major gap** — product has billing module with superbill generation, E/M coding, claims, pathology billing |
| Payments | ❌ Not covered | No payment data | Product may manage payment records via billing module |
| Consents / directives | ❌ Not covered | No Consent resource | N/A — unclear if product stores advance directives |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has patient portal with messaging; gap |
| Specialty-specific (urology) | ❌ Not covered | No urology-specific data: urine analysis, bladder scans, TRUS, cystoscopy, stent tracking | **Major gap** — this is a urology-specific EHR; the specialty data that distinguishes it from a generic EHR is entirely absent |

**Covered**: 8 of 18 domains (plus 2 partial)
**Not covered**: 8 domains, of which at least 4 (clinical notes, billing, referrals, urology-specific data) represent significant gaps given what the product stores.

## 6. Documentation Quality

**Strengths:**
- Field-level documentation is reasonably thorough for the 15 covered resources: 300 of 303 fields (99%) have descriptions, 276 (91%) have explicit types, and all 303 have cardinality
- Sample JSON output is provided for 14 of 15 resources
- The page is navigable with a left sidebar for resource selection

**Weaknesses:**
- **No data dictionary for native data model.** The documentation describes only FHIR resource shapes, not the underlying InPracSys database tables
- **Non-standard FHIR serialization.** The sample JSON uses C#/.NET internal object structures (`ValueElement`, `SystemElement`, etc.) that would fail standard FHIR parsing. A developer could not build an import from these examples without reverse-engineering the serialization
- **Version inconsistencies.** Claims "FHIR V4" but uses DSTU2-era field names (`careProvider`), profile references (DAF/Argonaut), and type names (`Hl7.Fhir.Model.*`)
- **Format contradiction.** The disclosure PDF says "zip file containing .xml file(s)" but the documentation describes JSON API responses. What XML structure the export actually produces is undocumented
- **No export procedure documentation.** No user guide, no screenshots showing how to trigger an export, no workflow description
- **No machine-readable schema.** No XSD, JSON Schema, OpenAPI spec, or CapabilityStatement
- **No sample export files.** No downloadable example ZIP or XML files
- **No relationship documentation.** Entity relationships are implicit via FHIR references but not explicitly documented
- **No value set enumeration.** Value sets are referenced by URL but actual coded values used by InPracSys are not listed

A developer could understand the covered FHIR resource structures from this documentation, but could not build a reliable import due to the non-standard JSON serialization, the undocumented XML format, and the missing domains.

## 7. Overall Assessment

### Classification

**Standard-based projection.** The EHI export documentation is the vendor's (g)(10) FHIR API documentation repurposed as the (b)(10) EHI export. It covers 15 FHIR resources corresponding to USCDI v1 clinical data classes — the exact same data available through the Standardized API. There is no evidence of native data model export, no billing data, no clinical notes, no urology-specific data, and no vendor-specific extensions beyond the standard FHIR resources.

### Key Findings

1. **The b(10) export is the g(10) FHIR API repackaged.** The FHIR documentation page at `inpracsys.com/fhir/` is linked directly from the b(10) disclosure as the "EHI export format." The 15 resources are exactly the USCDI v1/US Core data classes, with no additional data domains. (Source: `Disclosure-EHR-Inpracsys_NewV6.1.pdf` page 3, `fhir-api-documentation-page.html`)

2. **Clinical notes — the product's core feature — are absent.** FastCharting (rapid encounter documentation with HPI, ROS, exam, assessment/plan) is InPracSys's primary differentiator. No DocumentReference or clinical note content appears in the export. This is a significant omission for a product whose charting speed is its main selling point. (Source: `fhir-api-documentation-page.html` — no DocumentReference resource)

3. **All billing, claims, and specialty urology data are missing.** The product has a billing module (superbills, E/M coding, claims, pathology billing), a care pathways module (pre-authorization, drug programs), and urology-specific clinical data (urine analysis, bladder scans, stent tracking). None of this appears in the export. (Source: absence from `fhir-api-documentation-page.html`)

4. **The FHIR JSON is non-standard.** 10 of 14 sample JSON outputs use a C#/.NET FHIR library internal serialization (`ValueElement`, `SystemElement`, `CodeElement`) rather than standard FHIR JSON. The API also uses non-standard endpoint paths (`/SmokingStatus`, `/LabOrders`). This creates practical interoperability issues. (Source: sample JSON in `fhir-api-documentation-page.html`)

5. **Format contradiction is unresolved.** The disclosure PDF says "zip file containing .xml file(s)" but the documentation describes JSON REST API responses with no XML documentation. The actual export format is ambiguous. (Source: `Disclosure-EHR-Inpracsys_NewV6.1.pdf` page 3 vs. `fhir-api-documentation-page.html`)

### Summary Stats

```
Classification:  Standard-based projection
Export format:   FHIR JSON (non-standard serialization); PDF claims XML/ZIP
Model type:      Standard projection (FHIR/USCDI)
Entities:        15 FHIR resources
Fields:          303
Descriptions:    99.0% (300/303)
Sample data:     Yes (14/15 resources have sample JSON, but non-standard format)
Bulk export:     Unclear (claimed but not documented)
Domains covered: 8 of 16 applicable domains (+ 2 partial)
```

### Bottom Line

This is a textbook case of a vendor repurposing their (g)(10) FHIR API as a (b)(10) "all EHI" export. A patient or provider would get a clinical summary comparable to a C-CDA — demographics, problems, meds, allergies, labs, vitals — but would miss clinical notes, billing records, urology-specific data, and every other domain that makes this product more than a generic data viewer. The single biggest gap is the complete absence of clinical notes and encounter documentation, which is the product's core workflow and primary differentiator.
