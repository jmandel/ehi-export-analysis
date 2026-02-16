# EHI Export Analysis: MD Synergy Solutions, LLC

**Product**: Althea Smart EHR Version 3.0  
**Analysis date**: 2026-02-16  
**CHPL ID**: 15.04.04.1821.Alth.03.02.1.221205 (CHPL #11046)

## 1. Product Context

Althea Smart EHR is a cloud-based ambulatory EHR developed by MD Synergy Solutions, LLC (Calabasas, CA, ~50–70 employees). It targets independent physician practices and multi-specialty groups across internal medicine, family medicine, pediatrics, dermatology, psychiatry, pain management, surgery, orthopedics, and podiatry.

The product is paired with **mds:practice**, an integrated practice management and billing system. Together they cover:

- **Clinical**: encounter documentation (AI-powered ambient listening, voice-to-text), problem lists, medication lists, allergy lists, vitals, immunizations, lab/imaging orders and results (Quest, Labcorp integrations), e-prescribing (EPCS via Surescripts/NewCrop), clinical decision support, implantable device tracking, social/behavioral data
- **Billing/PM (mds:practice)**: claim generation from closed encounters, electronic claim submission (Change Healthcare, Emdeon, Trizetto, Waystar, Office Ally), ERA/remittance, payment posting, patient statements, insurance eligibility verification, denial tracking
- **Patient engagement**: patient portal (Althea Health) with messaging, forms, consent documents, Apple Health data import, online payments, telemedicine (video visits)
- **Administrative**: multi-location scheduling, appointment reminders, document management, quality measures/MIPS, immunization registry reporting

The CHPL certification includes (b)(10) EHI export, (g)(10) FHIR API, and a broad set of clinical criteria. The key question is whether the (b)(10) export covers the billing/PM data in mds:practice and the full depth of clinical data, or is limited to USCDI-scope clinical exchange.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/AltheaEHIDocumentation.pdf` | 108-page PDF, primary EHI export documentation. Contains introduction, 28 FHIR resource sections with JSON examples, CCD export instructions, contact info, and API terms of use. Generated from Google Docs, uploaded December 2024. | **Primary source** — the only substantive artifact |
| `downloads/enrichment/fhir-examples.json` | 52 extracted FHIR JSON examples across 13 resource types (5 sections had parse failures) | Useful for field analysis |
| `downloads/enrichment/extraction-summary.json` | Accounting of sections and parse results | Reference for completeness |
| `product-research.md` | Product research covering features, integrations, pricing | Context for coverage assessment |
| `chpl-metadata.json` | CHPL certification details | Certification scope reference |

**Most informative**: The PDF is the only artifact. There is no separate data dictionary, no schema, no sample export files, no machine-readable documentation.

## 3. Export Mechanics

- **Format**: FHIR R4 JSON files in a ZIP archive; also offers C-CDA (CCD) export as an alternative
- **Mechanism**: User requests export, system processes it, and sends a download link via message (e.g., `https://data.mdsynergy.com/FHIRBulkExport/24/{uuid}.zip`)
- **Scope**: Single patient, multiple patients, or entire patient population — user can choose
- **Access**: No fees or access constraints mentioned; contact `altheasupport@mdsynergy.com` for integration assistance
- **Documentation URL**: The ZIP download link includes accompanying documentation link

The export URL pattern (`FHIRBulkExport`) suggests this may share infrastructure with the (g)(10) FHIR Bulk Data API.

## 4. Export Content: What's In It

### Documentation approach

The 108-page PDF consists entirely of **FHIR JSON examples** — one or more sample JSON objects per resource type — with links to US Core profile specifications. There is:

- **No data dictionary** — no table of field names, types, or descriptions
- **No schema** — no JSON Schema, StructureDefinition, or CapabilityStatement
- **No field-level documentation** — no explanation of what each field means or what values are valid
- **No relationship documentation** — no description of how resources reference each other
- **No value set documentation** — code systems are used in examples but not enumerated

Each section follows the pattern: heading → "For more information on [X] profile, visit link [US Core Profile URL]" → one or more JSON examples.

### Resource types documented

The PDF documents 28 sections mapping to **16 FHIR resource types** (including 5 sections with parse failures that still contain valid examples):

| Resource Type | PDF Sections | Examples | Fields Observed | Category |
|---|---|---|---|---|
| Patient | Patient | 1 | 58 | Demographics |
| AllergyIntolerance | Allergies and Intolerances | 1 | 42 | Allergies |
| CarePlan | Care Plan | 1 | 31 | Care Planning |
| CareTeam | Care Team | 1 | 18 | Care Team |
| Condition | Condition, Health Concern | 6 | 32 | Problems |
| Device | Implantable Device | 1* | ~20 | Devices |
| DiagnosticReport | Diagnostic Report | 1* | ~25 | Diagnostics |
| DocumentReference | Document Reference | 1* | ~15 | Clinical Notes |
| Goal | Goal | 2 | 24 | Goals |
| Immunization | Immunization | 4 | 33 | Immunizations |
| MedicationRequest | Medication Request | 1 | 42 | Medications |
| Observation | 12 sections (vitals, labs, smoking status, pediatric) | 30 | 56 | Vitals/Labs |
| Procedure | Procedure | 2 | 35 | Procedures |
| Claim | Claims | 1 | 64 | Billing |
| Coverage | Coverage | 1 | 12 | Insurance |
| ExplanationOfBenefit | Explanation of Benefits | 1 | 75 | Billing |

\* Parse failure in enrichment extraction; example exists in PDF but has formatting issues (line-broken UDI strings, truncated base64 data).

**Total**: 16 resource types, ~52+ FHIR examples, ~522+ fields observed across successfully parsed examples. **0 fields have descriptions** — all documentation is by example only.

### Vendor's own content organization

The vendor organizes sections by FHIR resource type with no higher-level grouping. The sections align with US Core profiles, plus three financial resource types (Claim, Coverage, ExplanationOfBenefit).

### Notable observations from examples

- **Claim example** (pp. 91–97): Contains diagnosis codes, procedure codes (CPT), service dates, provider references, total amounts, and insurance references. The example shows a professional claim with multiple line items and modifier codes. This is real billing data structure, not a stub.
- **ExplanationOfBenefit example** (pp. 99–101): Contains payment amounts, adjustment amounts, diagnosis codes, billable period, and insurer reference. Shows claim adjudication data.
- **Coverage examples** (p. 98): Minimal — only status, policyHolder, subscriberId, and beneficiary. One example has subscriberId "CASH" (self-pay).
- **DocumentReference** (pp. 28–39): Contains base64-encoded CDA documents as `presentedForm` content — these are embedded clinical documents.
- **Observation sections**: 12 separate sections covering smoking status, pediatric growth charts (weight-for-height, BMI-for-age, head circumference percentile), pulse oximetry, body height, body temperature, blood pressure, body weight, heart rate, respiratory rate, and lab results. This is thorough vital signs coverage but dominated by pediatric growth chart examples (14 of 30 Observation examples).
- **No Encounter resource**: Despite references to Encounter IDs in DiagnosticReport, Claim, and other resources, there is no dedicated Encounter section or example. This is a notable gap given that Encounter is a core USCDI data class.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's documentation maps closely to US Core FHIR profiles with three additions beyond standard USCDI clinical exchange:

1. **Claim** — professional claims with diagnosis codes, CPT procedure codes, line items with costs, provider and insurer references
2. **Coverage** — insurance enrollment with policy holder and subscriber information
3. **ExplanationOfBenefit** — payment/adjudication data linked to claims

The clinical resource types (Patient, AllergyIntolerance, CarePlan, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Goal, Immunization, MedicationRequest, Observation, Procedure) are standard US Core profiles. Every section links directly to the US Core specification with no vendor-specific extensions or additional mappings documented.

The depth within each resource is limited to what the examples show. With no data dictionary, it's impossible to know whether the export populates fields beyond what appears in the sample JSON — a single example of each resource type cannot demonstrate the full range of data the system stores.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `Patient` (58 fields in example: name, DOB, gender, address, phone, race, ethnicity, birth sex, marital status, language, contacts) | Reasonable for a single example |
| Encounters / visits | ❌ Not covered | No Encounter resource despite references in other resources (e.g., DiagnosticReport.encounter) | **Significant gap** — product stores encounter data (certified for encounter documentation); Encounter references exist but no Encounter resource is exported |
| Problems / conditions | ✅ Covered | `Condition` (6 examples including health concerns) with SNOMED codes, clinical/verification status, onset dates, categories | Adequate |
| Medications / prescriptions | ✅ Covered | `MedicationRequest` (1 example) with medication codes, dosage instructions, prescriber, status | Single example; product has extensive e-prescribing capabilities — unclear if full Rx history depth is captured |
| Allergies | ✅ Covered | `AllergyIntolerance` (1 example) with clinical status, type, category, criticality, reactions | Adequate |
| Immunizations | ✅ Covered | `Immunization` (4 examples) with vaccine codes, dates, lot numbers, sites, routes | Good coverage with multiple examples |
| Vitals | ✅ Covered | `Observation` (12 sections, 30 examples) covering BP, height, weight, temperature, HR, RR, SpO2, pediatric growth charts | Thorough — most detailed section in the document |
| Lab results | ⚠️ Partial | `Observation` (1 lab example), `DiagnosticReport` (1 example with radiology category) | Only 1 lab result example; product integrates with Quest/Labcorp — lab depth likely underrepresented |
| Imaging / diagnostic reports | ⚠️ Partial | `DiagnosticReport` (1 radiology example with embedded PDF) | Single example; product has radiology integrations |
| Procedures | ✅ Covered | `Procedure` (2 examples) with SNOMED/CPT codes, dates, performers | Adequate |
| Clinical notes / documents | ✅ Covered | `DocumentReference` (1 example with embedded CDA), also C-CDA export option | CDA documents are embedded as base64 in DocumentReference |
| Care plans / goals | ✅ Covered | `CarePlan` (1 example), `Goal` (2 examples) | Basic coverage |
| Orders / referrals | ❌ Not covered | No ServiceRequest resource | **Gap** — product supports CPOE for medications, labs, imaging; no non-medication order resource is exported |
| Insurance / coverage | ⚠️ Partial | `Coverage` (1 example) — very minimal (status, subscriber ID, beneficiary only) | Product does insurance eligibility verification; export Coverage is thin (12 fields, no plan details, no group info) |
| Claims / billing | ⚠️ Partial | `Claim` (1 example with line items), `ExplanationOfBenefit` (1 example with payment data) | Product has extensive billing via mds:practice (claims, ERA, denial tracking, patient statements, payment posting). Export shows claim structure but unclear if full billing depth (denials, adjustments, ERA detail, patient payments) is captured. Only 1 example each. |
| Payments | ⚠️ Partial | Payment amount in `ExplanationOfBenefit` | Basic payment data in EOB; no dedicated payment resource; product tracks credit card payments, patient balances |
| Consents / directives | ❌ Not covered | No Consent resource | Product accepts consent documents via patient portal; not in export |
| Patient communications / portal messages | ❌ Not covered | No Communication resource | Product has patient portal messaging, SMS (Twilio), secure messaging; none exported |
| Specialty-specific data | ❌ Not covered | No specialty resources | Product serves dermatology, psychiatry, pain management, orthopedics, podiatry — no specialty-specific data in export |

## 6. Documentation Quality

**Overall quality: Poor.** The documentation is examples-only with no supporting reference material.

- **Can a developer understand the export?** Partially — a developer familiar with FHIR can look at the examples and understand the structure, but there's no way to know the full field coverage, valid value sets, or handling of edge cases without access to the system itself.
- **What's well-documented?** The basic FHIR resource structure is clear from the examples. The export mechanism (ZIP via download link) is described.
- **What requires guesswork?** Almost everything beyond basic structure: which fields are always populated vs. optional; what code systems are used for each coded field; how resources reference each other; what happens with missing data; whether the examples represent typical data or edge cases; the full set of data that could appear in each resource type.
- **Machine-readable artifacts?** None. No JSON Schema, no CapabilityStatement, no FHIR StructureDefinitions, no sample export ZIP files. The PDF is the only artifact, and it's not programmatically parseable as documentation.
- **Import feasibility?** A developer could not build a reliable import system from this documentation alone. They would need access to the actual system to discover the full data model.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Partial**

The export goes slightly beyond pure USCDI by including three financial FHIR resources (Claim, Coverage, ExplanationOfBenefit), which is notable — many vendors provide zero billing data. However, the billing coverage is shallow (1 example each, minimal Coverage data), and significant domains are missing relative to what the product stores:

- No Encounter resource (a core USCDI gap)
- No orders beyond medications (ServiceRequest missing despite CPOE capabilities)
- No patient communications despite active portal messaging
- No consent documents despite portal form collection
- No specialty-specific clinical data despite serving multiple specialties
- The mds:practice billing depth (ERA, denials, patient statements, eligibility responses, payment posting) is not represented beyond the basic Claim/EOB structure

The 16 resource types with financial additions represent an effort beyond pure USCDI clinical exchange, but the product's full data footprint — especially the practice management side — is substantially broader than what's documented.

**Axis 2 — Export approach: Repackaged existing export with minor additions**

Several signals indicate this is primarily the (g)(10) FHIR API output relabeled as (b)(10):

1. The export URL pattern is `FHIRBulkExport` — the same infrastructure as the FHIR Bulk Data (g)(10) API
2. Every clinical resource section links to the corresponding US Core profile with no vendor-specific documentation
3. No data dictionary, no vendor-specific field mapping, no documentation of how internal EHR data maps to FHIR resources
4. The resource types closely mirror the US Core required resource set

The three financial resources (Claim, Coverage, ExplanationOfBenefit) are a genuine addition beyond the (g)(10) surface — these are not part of US Core or standard FHIR Bulk Data. This represents a modest effort to extend the export toward (b)(10) completeness. However, the financial data is documented with only 1 example each and no field-level documentation, and the overall documentation quality is too thin to constitute a purpose-built EHI export effort.

### Key Findings

1. **Documentation is examples-only**: 108 pages containing solely FHIR JSON examples with links to US Core specs. Zero field descriptions, zero data dictionary entries, zero schemas. This is the thinnest form of FHIR documentation possible.

2. **Three financial resource types are a genuine addition**: Claim, Coverage, and ExplanationOfBenefit go beyond USCDI/US Core and represent real billing data. However, Coverage is barely populated (12 fields) and the depth of the billing data is unclear from single examples.

3. **Missing Encounter resource**: Despite Encounter references appearing in DiagnosticReport, Claim, and other resources, there is no Encounter resource section. This is a gap even within USCDI scope.

4. **mds:practice billing depth is not represented**: The product's PM system handles claims submission, ERA, denial tracking, patient statements, eligibility verification, and payment posting. The export's Claim/EOB examples scratch the surface but don't demonstrate coverage of this full billing workflow.

5. **Export infrastructure appears shared with (g)(10)**: The `FHIRBulkExport` URL pattern and exclusive use of US Core profiles suggest the (b)(10) export is built on top of the existing FHIR Bulk Data API with financial resources added.

### Summary Stats

```
Coverage:        Partial
Approach:        Repackaged existing export (with minor billing additions)
Export format:   FHIR R4 JSON (ZIP), also C-CDA (CCD)
Entities:        16 FHIR resource types
Fields:          ~522 observed across examples (no definitive count possible without data dictionary)
Descriptions:    0% (no field descriptions — examples only)
Sample data:     Yes (embedded in documentation as JSON examples, but no standalone sample export file)
Bulk export:     Yes (single, multiple, or all patients)
Domains covered: 10 of 18 applicable domains (with 4 partial)
```

### Bottom Line

Althea Smart EHR's (b)(10) export is a thin layer on top of its (g)(10) FHIR Bulk Data API, documented with nothing more than sample JSON — no data dictionary, no schema, no field descriptions. The addition of Claim, Coverage, and ExplanationOfBenefit resources represents a modest effort beyond pure USCDI clinical exchange, but the product's extensive practice management and billing capabilities (mds:practice) are barely represented, and several core domains (encounters, orders, communications, specialty data) are absent entirely.
