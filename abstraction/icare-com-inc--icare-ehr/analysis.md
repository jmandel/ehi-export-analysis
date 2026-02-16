# EHI Export Analysis: iCare.com, Inc.

**Product**: iCare EHR (Version 2)
**Analysis date**: 2026-02-16
**CHPL IDs**: 15.04.04.2617.iCar.02.00.1.200220

## 1. Product Context

iCare EHR is a cloud-native enterprise EHR platform by iCare.com, Inc. (Fort Lauderdale, FL), targeting hospitals, clinics, and physician practices across inpatient, ambulatory, and behavioral health settings. It is a small vendor (51–200 employees, no publicly known major deployments) with a single CHPL-certified product (certified 2020-02-20).

Based on the vendor's website and CHPL certification, iCare EHR stores and manages:

- **Clinical data**: Patient demographics, problem lists, medication lists, allergy lists, clinical notes, vital signs, immunization records, lab orders/results, radiology/imaging, care plans, clinical decision support alerts, CPOE for medications and labs.
- **E-prescribing**: Electronic prescriptions including controlled substances (EPCS), drug interaction checks, formulary data.
- **Revenue cycle management (RCM)**: Insurance verification, billing and claims management, payment tracking, accounts receivable, denial management, E/M coding, financial reporting — described as integrated into the platform.
- **Scheduling**: Appointment, procedure, and surgery scheduling with calendar views and patient self-service.
- **Patient portal**: Secure messaging, appointment requests, bill payment, access to health summaries and test results.
- **Document management**: Attached charts, forms, images, correspondence, radiology images — described as a "centralized vault."
- **Public health reporting**: Syndromic surveillance (f)(2), reportable lab results (f)(3).
- **Interoperability**: C-CDA, FHIR R4 API, Direct messaging.

This breadth of functionality — particularly the integrated RCM module, scheduling, patient portal, and document vault — sets the baseline for what a genuine (b)(10) export should cover.

## 2. Artifacts Reviewed

| Artifact | Size | Description | Informativeness |
|---|---|---|---|
| `ehi-export-page.html` | 15 KB | Clean HTML extraction of the EHI export documentation page via WordPress REST API. Contains 3 export methods and 13 FHIR resource type query examples. | **Primary** — the vendor's (b)(10) documentation |
| `ehi-export-page-wp-json.json` | 18 KB | WordPress REST API JSON for page 1286. Confirms last modified date: 2025-10-18. | Metadata only |
| `iCare-API-Guide.pdf` | 355 KB, 67 pages | Copyright 2020 API guide documenting iCare's proprietary REST API with 16 clinical data categories, input/output JSON examples, and a C-CDA "all criteria" request. | **Most detailed** — provides field-level examples |
| `fhir-capability-statement.json` | 3 KB | FHIR R4 CapabilityStatement from EMR Direct Interoperability Engine sandbox. Declares US Core Server + Bulk Data conformance, Group/$export only. | Confirms third-party infrastructure |
| `screenshot-ehi-export-page.png` | 903 KB | Full-page screenshot of the EHI export page. | Visual confirmation |

The **most informative artifact** is the 67-page API Guide PDF, which provides example JSON responses for each clinical category. The **EHI export HTML page** is the vendor's actual (b)(10) documentation but is thin — it lists FHIR resource types with query URIs but no field-level detail. **No data dictionary, schema, or sample export files** are publicly available.

## 3. Export Mechanics

iCare documents three export methods:

1. **CCD/HIM Export** (in-app, single patient):
   - Navigate to Reports > Clinical Summary > Continuity of Care and Referral Notes for a CCD.
   - Navigate to Patient Info > HIM Request for clinical assessments and notes.
   - Format: C-CDA / HIM records.
   - No further specification of scope or contents.

2. **CSC Request for Full Data Export** (population):
   - Contact vendor ("make a CSC request") for export of "the entirety of your organization's clinical data."
   - Delivered via SFTP or other requested means.
   - Claims to include "a description of the data file formats and data dictionary."
   - **No documentation, data dictionary, format specification, or sample data is publicly available** for this method. The data dictionary is apparently delivered only with the actual export files.

3. **FHIR REST API** (single patient, population, group):
   - Hosted at `sandbox-r4.interopengine.com/fhir/r4/icare/` (EMR Direct Interoperability Engine, a third-party middleware).
   - Single patient: `Patient/id/$export` or resource-specific queries.
   - Population: `Patient/$export` (Bulk Data).
   - Group: `Group/GroupID/$export` (Bulk Data).
   - OAuth2 authorization via `/oauth/icare/token`.
   - 13 FHIR resource types documented.

**Access**: The FHIR API is self-service (with credentials); the CSC full export requires contacting the vendor. The in-app CCD/HIM export requires logged-in user access with appropriate privileges. No fees beyond the iCare subscription are mentioned.

**Psychotherapy exclusion**: "Items related to psychotherapy will not be included in any data export."

## 4. Export Content: What's In It

### Overview

The publicly documented export covers **16 clinical data categories** (per the API Guide) accessible via a proprietary REST API, and **13 FHIR resource types** (per the EHI export page) accessible via a FHIR R4 Bulk Data API. Both cover the same clinical domain — standard USCDI data. There is also a C-CDA "all criteria" endpoint that bundles everything into a single XML document.

**There is no data dictionary.** No field names, types, descriptions, value sets, or relationships are formally documented. The only field-level information comes from example JSON responses in the 67-page API Guide PDF (Copyright 2020), which show the structure of FHIR resources returned by the proprietary API.

### What the API Guide documents (16 categories)

From parsing the API Guide PDF, each category maps to one or more FHIR resource types and has example JSON showing specific fields. Total: 17 entities (16 categories + 1 C-CDA "all criteria"), with ~202 unique field names visible across all JSON examples. **Zero fields have formal descriptions** — the only documentation is the shape of example JSON.

| Category | FHIR Types Used | Fields in Examples | Domain |
|---|---|---|---|
| patient | Patient | 25 | Demographics |
| smokingStatus | Composition | 9 | Social History |
| problem | Condition, Composition | 13 | Problems / Conditions |
| medication | MedicationStatement, Composition | 15 | Medications |
| medAllergy | AllergyIntolerance, Composition | 15 | Allergies |
| labTest | CarePlan | 10 | Laboratory |
| labResult | Observation, DiagnosticReport, Organization, Composition | 21 | Laboratory |
| vital | Observation, Composition | 13 | Vitals |
| procedure | Procedure, Composition | 17 | Procedures |
| careTeam | CareTeam | 6 | Care Team |
| immunization | Immunization, Composition | 15 | Immunizations |
| device | Device, Composition | 9 | Devices |
| planOfTreatment | CarePlan | 10 | Care Plans |
| assessment | CarePlan, RiskAssessment | 12 | Clinical Notes / Documents |
| goal | Goal | 7 | Goals |
| healthConcern | Composition | 5 | Health Concerns |
| allCriteria (C-CDA) | N/A (C-CDA XML) | 0 (XML, not parsed) | All Clinical |

### EHI Export Page FHIR Resources (13 types)

The EHI export page lists these FHIR resource types for the FHIR API:
CarePlan, AllergyIntolerance, CareTeam, Condition, Device, DiagnosticReport, DocumentReference, Goal, Immunization, MedicationRequest, Observation, Procedure, Encounter.

These are standard US Core resource types. No vendor-specific extensions, custom profiles, or non-USCDI resource types are documented. The page has copy-paste errors (e.g., the Encounter section example URI points to Procedure; most resource sections repeat the `Patient/id/$export` URI regardless of resource type).

### What's NOT in the documented export

Based on the product's known capabilities (Section 1), the following are **absent from all documented export methods**:

- **Billing / Revenue Cycle**: No claims, charges, payments, denials, superbills, accounts receivable — despite iCare having an integrated RCM module.
- **Insurance / Coverage**: No insurance details beyond what's in the Patient resource.
- **Scheduling**: No appointments, procedures, or surgery schedules.
- **Patient Portal Data**: No secure messages, portal interactions, patient-submitted forms.
- **E-Prescribing Transactions**: No EPCS records, prescription tracking, Surescripts data.
- **Document Vault**: The "centralized vault" of charts, forms, images, and correspondence is not specifically addressed (DocumentReference may partially cover clinical notes but not the full vault).
- **Orders**: Only MedicationRequest is documented; no ServiceRequest, lab orders as separate entities, or referral orders.
- **Behavioral Health**: Explicitly excluded ("items related to psychotherapy will not be included").
- **Inpatient-Specific Data**: No nursing documentation, medication administration records (MAR), bed management, or operative records, despite the product being certified for inpatient use.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export documentation covers a **narrow set of standard clinical data categories**, organized as FHIR resource types / API categories. The coverage maps directly to USCDI data classes:

- **Demographics**: Patient resource with name, DOB, gender, race, ethnicity, address, phone, language (25 fields in examples).
- **Problems/Conditions**: Active and resolved conditions with SNOMED CT codes, onset dates, clinical status (13 fields).
- **Medications**: MedicationStatements with RxNorm codes, dosage, status (15 fields).
- **Allergies**: AllergyIntolerance with reaction details (15 fields).
- **Lab Results**: Observations and DiagnosticReports with LOINC codes, values, units, reference ranges (31 fields across labTest + labResult).
- **Vitals**: Observations with LOINC codes for standard vital signs (13 fields).
- **Immunizations**: Immunization resources with CVX codes, dates, lot numbers (15 fields).
- **Procedures**: Procedure resources with codes and dates (17 fields).
- **Care Team**: CareTeam members (6 fields — thin).
- **Care Plans / Goals**: CarePlan and Goal resources (17 fields combined).
- **Clinical Notes/Documents**: DocumentReference and assessments (12 fields).
- **Smoking Status / Health Concerns**: Social history and health concern Compositions (14 fields combined).
- **Devices**: Implanted device records with UDI (9 fields).

**Notably absent**: The vendor's own categories do not include anything outside standard USCDI clinical data. There are no categories for billing, insurance, scheduling, portal messages, or any administrative/operational data — despite the product storing all of these.

The vendor's mention of a "CSC request" for "the entirety of your organization's clinical data" is the only hint at a broader export, but it has **zero public documentation** and cannot be assessed.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `patient` category: 25 fields, Patient resource with name, DOB, gender, race, ethnicity, address, phone, language | Standard USCDI coverage |
| Encounters / visits | ✅ Covered | `Encounter` on EHI page; encounter timestamps structure all API responses | Present but thin — encounters mainly serve as grouping containers |
| Problems / conditions | ✅ Covered | `problem` category: Condition resources with SNOMED codes, onset, clinical status | Adequate |
| Medications / prescriptions | ✅ Covered | `medication` category: MedicationStatement with RxNorm, dosage, status | Standard coverage; no MAR |
| Allergies | ✅ Covered | `medAllergy` category: AllergyIntolerance with reactions | Standard |
| Immunizations | ✅ Covered | `immunization` category: Immunization with CVX codes | Standard |
| Vitals | ✅ Covered | `vital` category: Observation with LOINC codes | Standard |
| Lab results | ✅ Covered | `labTest` + `labResult`: DiagnosticReport + Observation with LOINC, values, ranges | Standard |
| Imaging / diagnostic reports | ⚠️ Partial | DiagnosticReport limited to category=LAB in documentation | Product has PACS integration; imaging reports not clearly covered |
| Procedures | ✅ Covered | `procedure` category: Procedure with codes | Standard |
| Clinical notes / documents | ⚠️ Partial | `assessment` + DocumentReference | Only assessments/notes visible; broader document vault unclear |
| Care plans / goals | ✅ Covered | `planOfTreatment` + `goal`: CarePlan, Goal | Standard |
| Orders / referrals | ⚠️ Partial | MedicationRequest only; no ServiceRequest or referral entities | Product has CPOE for meds and labs; lab orders and referrals not in export |
| Insurance / coverage | ❌ Not covered | No insurance/coverage entities in any export method | Product does insurance verification (RCM module); significant gap |
| Claims / billing | ❌ Not covered | No claims, charges, or billing entities | Product has full RCM with claims, coding, denials; **major gap** |
| Payments | ❌ Not covered | No payment or accounts receivable data | Product tracks payments/AR; significant gap |
| Scheduling | N/A | No scheduling entities | Scheduling data (appointments) is generally not EHI per the scope reference |
| Consents / directives | ❌ Not covered | No consent or advance directive entities | Uncertain if product stores these |
| Patient communications / portal messages | ❌ Not covered | No messaging or portal interaction data | Product has patient portal with secure messaging; gap |
| Specialty-specific (behavioral health) | ❌ Excluded | Psychotherapy data explicitly excluded from all exports | Product serves behavioral health settings per CHPL SED; this is a gap, though psychotherapy notes are carved out of EHI by statute — however, the exclusion appears broader than just psychotherapy notes |
| E-prescribing details | ❌ Not covered | No EPCS transaction records, formulary data, or prescription tracking | Product has e-prescribing with EPCS; gap |

## 6. Documentation Quality

**Poor.** The documentation is insufficient for a developer to understand, build against, or import from this export.

**What exists:**
- A single HTML page (15 KB) listing 3 export methods and 13 FHIR resource types with query URIs. No field definitions.
- A 67-page API Guide PDF (Copyright 2020) for a different (proprietary REST) API, with example JSON responses showing field structures. This is the best artifact but is 6 years old and documents a legacy API.
- A FHIR CapabilityStatement from a third-party middleware (EMR Direct) that only declares Group/$export.

**What's missing:**
- **No data dictionary**: No entity-field listing, no formal field definitions, no types, no constraints.
- **No schema files**: No JSON Schema, no FHIR profiles, no XML Schema.
- **No sample data or export files**: No downloadable examples of what the export produces.
- **No value sets or code systems**: Beyond SNOMED/LOINC/RxNorm implied by FHIR standard, no vendor-specific value sets.
- **No relationship documentation**: No foreign keys, no entity-relationship model, no data model diagrams.
- **No documentation for the CSC bulk export**: The most promising export method has zero public documentation.
- **Copy-paste errors**: The EHI page has incorrect example URIs (Encounter section points to Procedure endpoint).
- **No versioning alignment**: The EHI page (2025) and API Guide (2020) describe different APIs.

A developer receiving data from this export would have to reverse-engineer the format from the data itself. The only field-level insight comes from example JSON in a 6-year-old PDF that documents a different API than what the EHI page describes.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Minimal/stub/unclear**

The documented export covers only standard USCDI/US Core clinical data — the same 13 FHIR resource types that would satisfy the (g)(10) standardized API requirement. Major data domains that the product stores — billing/RCM, insurance details, patient portal messages, e-prescribing transactions, the document vault — are entirely absent from the documented export. The vendor mentions a "CSC request" for full data, but provides zero documentation for it, making its scope unassessable. Behavioral health data is explicitly excluded. The publicly documented export covers roughly the USCDI floor and nothing beyond it.

**Axis 2 — Export approach: Repackaged existing export**

Multiple signals confirm this is the vendor's existing (g)(10) FHIR API and C-CDA exchange relabeled as (b)(10):

1. **Same resource types**: The 13 FHIR resources on the EHI page are exactly the US Core resource types required for (g)(10). No additional resources, no vendor extensions, no custom profiles.
2. **Third-party middleware**: The FHIR endpoint is hosted on EMR Direct Interoperability Engine — a standard interoperability middleware, not a custom EHI export tool. The CapabilityStatement instantiates the standard US Core Server and Bulk Data CapabilityStatements.
3. **No product-specific data dictionary**: The documentation references FHIR resource types generically without any product-specific mapping, field enumeration, or data model documentation.
4. **API Guide documents same clinical scope**: The older proprietary API guide covers the same 16 clinical categories (which map to the same USCDI domains) — confirming this has always been the clinical exchange surface, not a purpose-built EHI export.
5. **No billing/operational coverage**: Despite having an integrated RCM module, no billing, insurance, payment, or operational data appears in any export method's documentation.

The "CSC request" method hints at something broader ("the entirety of your organization's clinical data"), but even its own description says "clinical data" (not "all EHI"), and the complete absence of documentation means it cannot change the classification.

### Key Findings

1. **Repackaged (g)(10) as (b)(10)**: The documented EHI export is the vendor's standard FHIR Bulk Data API (13 US Core resource types) plus an older proprietary REST API (16 clinical categories covering the same scope), both limited to USCDI clinical data. No billing, insurance, scheduling, portal, or specialty data is included.

2. **No data dictionary exists publicly**: Despite the vendor claiming a data dictionary is provided with CSC-requested exports, no data dictionary, schema, or format specification is available in the public documentation. The only field-level detail comes from example JSON in a 6-year-old PDF.

3. **Billing/RCM entirely absent**: iCare has an integrated Revenue Cycle Management module (insurance verification, claims, payments, denials, coding), but zero billing entities appear in any documented export method. This is the single largest gap.

4. **Behavioral health explicitly excluded**: The vendor excludes "items related to psychotherapy" from all exports. While psychotherapy notes are carved out of EHI by statute, the exclusion language is broader and may encompass treatment plans, session summaries, and diagnoses that are EHI.

5. **Documentation quality is poor**: Copy-paste errors on the EHI page, a 6-year-old API guide for a different API, no schemas, no samples, and zero documentation for the most promising export method (CSC request).

### Summary Stats

    Coverage:        Minimal/stub/unclear
    Approach:        Repackaged existing export
    Export format:   FHIR R4 JSON (Bulk Data), C-CDA XML
    Entities:        17 (16 API categories + 1 C-CDA composite)
    Fields:          ~202 (visible in example JSON only; no formal data dictionary)
    Descriptions:    0% (no field descriptions provided)
    Sample data:     No
    Bulk export:     Yes (FHIR Bulk Data + CSC request)
    Domains covered: 10 of 17 applicable domains (all clinical/USCDI; zero non-clinical)

### Bottom Line

iCare's (b)(10) documentation is their existing (g)(10) FHIR API and C-CDA exchange relabeled — 13 standard US Core resource types covering USCDI clinical data only. A patient or provider would get a clinical summary (demographics, conditions, meds, labs, vitals, immunizations, notes) but would miss their complete billing history, insurance records, portal messages, and any behavioral health data. The biggest gap is the total absence of the integrated RCM/billing data that the product stores.
