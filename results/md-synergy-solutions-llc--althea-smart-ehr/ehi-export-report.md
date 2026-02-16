# MD Synergy Solutions, LLC — EHI Export Documentation

Collected: 2026-02-15

## Source
- Registered URL: https://mdsynergy.com/wp-content/uploads/2024/12/AltheaEHIDocumentation.pdf
- CHPL ID: 11046
- Product: Althea Smart EHR, Version 3.0
- Certification date: 2022-12-05

## Navigation Journal

The registered URL is a direct PDF download hosted on the vendor's WordPress site.

```bash
curl -sI -L "https://mdsynergy.com/wp-content/uploads/2024/12/AltheaEHIDocumentation.pdf" \
  -H 'User-Agent: Mozilla/5.0'
```

Response: HTTP/2 200, Content-Type: application/pdf, 410,315 bytes. No redirects.

```bash
curl -sL "https://mdsynergy.com/wp-content/uploads/2024/12/AltheaEHIDocumentation.pdf" \
  -H 'User-Agent: Mozilla/5.0' \
  -o downloads/AltheaEHIDocumentation.pdf
```

Verified with `file` command: confirmed PDF document, version 1.4, 108 pages. Produced by "Skia/PDF m120 Google Docs Renderer" (created from Google Docs). Title: "Electronic Health Information Export".

No embedded files/attachments (verified with `pdfdetach -list`). All URLs in the document are either FHIR specification links (hl7.org, snomed, loinc — external standards we don't need to follow) or references to the vendor's own FHIR server at `altheafhir.mdsynergy.com` (sample data within the examples). Two vendor-specific URLs of note:
- `https://data.mdsynergy.com/FHIRBulkExport/24/acdd260f-aa99-4620-b457-52c5f74575b3.zip` — example FHIR bulk export download link
- `https://mdsdata.mdsynergy.com/FHIRBulkExport/24/61ea968e-523e-4199-a9d7-09a57e16410d-CCD.zip` — example CCD export download link

These are time-limited export download URLs, not documentation endpoints; no additional docs to retrieve from them.

## What Was Found

The PDF is a 108-page document titled "Electronic Health Information Export — Althea Version 3.0." It was generated from Google Docs and uploaded to the vendor's WordPress site in December 2024.

### Document Structure

1. **Cover page** (page 1): Althea Smart EHR / MD Synergy branding
2. **Table of Contents** (page 2): Lists all sections with page numbers
3. **Introduction** (pages 4): Defines EHI, states export is available in CCDA and FHIR formats, for single patient or entire population
4. **Resources** (pages 4–98): Sample FHIR JSON for each resource type with brief headers
5. **Export Current CCD** (page 102): Brief note about CCD export
6. **Contact Information** (page 103): Support email
7. **Terms and Conditions** (pages 103–108): API Terms of Use

### Export Mechanism

The document describes two export formats:
1. **FHIR JSON** — The primary format. After a user requests an export, the system processes it and sends a download link to a ZIP file containing individual JSON files per resource type. The download URL pattern is `https://data.mdsynergy.com/FHIRBulkExport/{orgId}/{uuid}.zip`. Users can select single, multiple, or all patients.
2. **C-CDA** — A secondary option. The CCD export also delivers a ZIP file via a download link, with a different URL pattern: `https://mdsdata.mdsynergy.com/FHIRBulkExport/{orgId}/{uuid}-CCD.zip`.

### FHIR Resources Documented

The document provides sample FHIR JSON for the following resource types (each section includes one or more complete example instances):

| Resource Type | Description | Sample Data |
|---|---|---|
| Patient | Demographics, race, ethnicity, birth sex, contacts | 1 example patient (Alice Newman) |
| AllergyIntolerance | Drug allergies with reactions | 1 example |
| CarePlan | Assessment and Plan of Treatment entries | 4 examples (per-condition care plans) |
| CareTeam | Patient + practitioner participants | 1 example |
| Condition | Problem list items (SNOMED coded) | 5 examples (hypertension, hypothyroidism, etc.) |
| Condition (Health Concern) | Health concerns as separate Condition resources | 1 example |
| Device (Implantable) | UDI-carrying devices | 1 example (spinal fixation device) |
| DiagnosticReport | Radiology and lab reports | 1 example (chest XR) |
| DocumentReference | Clinical documents (notes, reports) as base64-encoded PDFs | 4 examples (after-visit summary, echo report, progress notes) |
| Goal | Patient health goals | 2 examples |
| Immunization | Vaccination records | 4 examples |
| MedicationRequest | Prescription orders | 1 example |
| Observation (Smoking Status) | Social history observations | Multiple examples |
| Observation (Pediatric Weight/Height) | Growth chart observations | Examples shown |
| Observation (Lab Results) | Laboratory result observations | Examples shown |
| Observation (Pediatric BMI) | Pediatric BMI percentile | Examples shown |
| Observation (Pulse Oximetry) | SpO2 measurements | Examples shown |
| Observation (Head Circumference) | Pediatric OFC percentile | Examples shown |
| Observation (Body Height) | Height measurement | Examples shown |
| Observation (Body Temperature) | Temperature measurement | Examples shown |
| Observation (Blood Pressure) | Systolic/diastolic BP | Examples shown |
| Observation (Body Weight) | Weight measurement | Examples shown |
| Observation (Heart Rate) | Heart rate | Examples shown |
| Observation (Respiratory Rate) | Respiratory rate | Examples shown |
| Procedure | Clinical procedures (SNOMED + CPT coded) | Examples shown |
| Claim | Professional claims with diagnosis/procedure codes, line items with pricing | 1 detailed example |
| Coverage | Insurance coverage records | 2 examples |
| ExplanationOfBenefit | EOB with adjudication, payment info | 1 detailed example |

### Documentation Style

The document is almost entirely composed of FHIR JSON examples — there is no data dictionary, no field-level definitions, no schema, and no narrative description of what each field means. Each resource section consists of:
1. A heading (e.g., "Allergies and Intolerances")
2. A one-line reference to the US Core profile (e.g., "For more information on Allergy intolerance profile, visit link US Core Allergies Profile")
3. One or more complete FHIR JSON examples

There are no descriptions of field semantics, no value set documentation, no cardinality constraints, and no explanation of vendor-specific mappings. The documentation assumes the reader will refer to the US Core specification for all structural details.

## Export Coverage Assessment

### Data Domain Coverage

**Clearly covered domains (with FHIR examples):**
- Patient demographics (name, DOB, gender, race, ethnicity, birth sex, address, phone, marital status, language, contact/employer)
- Allergies and intolerances
- Care plans (assessment and plan of treatment)
- Care teams
- Conditions/problem list (SNOMED coded)
- Health concerns
- Implantable devices (UDI data)
- Diagnostic reports (radiology, lab)
- Document references (clinical notes as embedded PDFs — progress notes, after-visit summaries, specialty procedure reports like echocardiograms)
- Goals
- Immunizations
- Medication requests/prescriptions (RxNorm coded)
- Smoking status and social history observations
- Vital signs (full set: height, weight, BMI, BP, HR, RR, temperature, pulse oximetry, pediatric growth percentiles)
- Lab results
- Procedures (SNOMED + CPT coded)
- **Claims** (professional claims with ICD diagnosis codes, CPT procedure codes, line-item pricing, insurer references, care team)
- **Coverage** (insurance enrollment with subscriber IDs)
- **Explanation of Benefits** (adjudication outcomes, payment amounts)

**Notable positive finding:** The inclusion of Claim, Coverage, and ExplanationOfBenefit resources is significant. This goes beyond the typical US Core/USCDI data set and into financial/billing territory, which is a genuine (b)(10) consideration. Many vendors omit billing data entirely. MD Synergy has at least modeled these financial resources in FHIR, which shows awareness that EHI extends beyond clinical summaries.

**Domains likely stored by the product but NOT documented in the export:**
- **Encounter data**: The product clearly tracks encounters (encounters are referenced in many resources like DocumentReference, DiagnosticReport, MedicationRequest), but there is no Encounter resource documented in the export. This is a gap — encounter metadata (dates, types, providers, facilities, reasons) is clinical data used for decision-making.
- **E-prescribing details**: Only MedicationRequest is shown. The product integrates with Surescripts/NewCrop for e-prescribing, and detailed prescription fill history, pharmacy information, and EPCS data are not represented.
- **Medication administration / medication history**: No MedicationStatement or MedicationAdministration resources.
- **Referrals**: No ServiceRequest resources for referrals.
- **Patient portal messages**: The product has a patient portal (Althea Health) with messaging, but no Communication resources are documented.
- **Patient-submitted forms**: The portal allows form submission, but no QuestionnaireResponse resources.
- **Apple Health data**: The portal integrates with Apple Health, but no representation of patient-generated data.
- **Telemedicine session data**: The product offers video visits, but no documentation of how these encounters are exported.
- **Clinical decision support interactions**: Certified for (a)(12) but no documentation of CDS data in exports.
- **Social/psychological/behavioral data**: Certified for (a)(15) SDOH data but only smoking status is documented as an observation.
- **Patient satisfaction surveys**: Collected by the portal but not in the export.
- **SMS/fax communication logs**: While operational in nature, patient-directed communications that document care coordination could be part of the designated record set.

### Export Format & Standards

The export uses **FHIR R4 JSON** delivered as ZIP files, with resource types mapped to US Core profiles. This is a recognized standard and an appropriate format choice.

However, the export appears to be essentially a **FHIR Bulk Data export** — the URL paths literally contain "FHIRBulkExport" and the contact information section says "If you need any further assistance on integrating the FHIR API please email us." This strongly suggests the (b)(10) EHI export is the same mechanism as the (g)(10) FHIR API, with the addition of Claim, Coverage, and ExplanationOfBenefit resources (which are beyond US Core's typical scope).

The critical question is whether this FHIR export captures **everything** the system stores about patients, or only what maps to standard FHIR resource types. The resource list is fundamentally the US Core resource set plus financial resources. The product stores specialty-specific clinical data across dermatology, psychiatry, pain management, orthopedics, and podiatry — none of which is documented as having a distinct export representation. It's unclear whether specialty clinical data gets folded into DocumentReference (as embedded PDFs of clinical notes), or whether it's simply not exported.

A third party receiving this export could reconstruct a reasonable clinical summary (demographics, problems, meds, labs, vitals, notes, immunizations) and a partial financial picture (claims, coverage, EOB). But they would lack encounter structure, would need to parse embedded PDFs for narrative clinical notes, and would miss any specialty-specific structured data that doesn't map to US Core resources.

### Documentation Quality

**Readability**: The document is a long PDF that is nearly 100% example JSON. It is readable in the sense that the examples are well-formatted, but there is no narrative explanation of the export process, field semantics, or data mapping.

**Data dictionary**: **None.** There is no field-level data dictionary. The documentation relies entirely on the US Core specification and FHIR standard for field definitions.

**Value sets and constraints**: **Not specified.** The examples show some coded values (SNOMED, LOINC, RxNorm, ICD, CPT) but there is no documentation of which code systems are used for which fields, what value sets are supported, or what vendor-specific codes might appear.

**Worked examples**: The entire document is examples, which is both a strength (concrete, testable) and a weakness (no systematic schema description). The examples are helpful but they represent a single test patient, so they don't demonstrate the full range of data the system can export.

**Developer usability**: A developer could understand the general structure of the export from this document, but would need to refer to US Core and FHIR specifications for all details. The lack of vendor-specific field documentation means any non-standard mappings (and there appear to be some — e.g., smoking status display value "LV EDD^^67^^78" doesn't match expected SNOMED display values) would be discovered only through trial and error.

**Maintenance**: The document title references "Version 3.0" and was uploaded December 2024. No revision history or versioning information is provided.

### Structure & Completeness

- **Granularity**: Resource-type level only. Individual fields are shown in examples but not described.
- **Coded fields**: Code systems are shown in examples (SNOMED, LOINC, RxNorm, ICD, CPT, CVX) but no systematic value set documentation.
- **Relationships**: Cross-references between resources are shown in examples (patient references, encounter references, practitioner references) but not systematically documented.
- **Versioning**: None.
- **Machine-readable schema**: None provided. No OpenAPI spec, no JSON Schema, no StructureDefinition, no CapabilityStatement.

### Overall Assessment

MD Synergy's EHI export documentation is a moderately good effort that shows genuine awareness of the (b)(10) requirement beyond just wrapping the (g)(10) FHIR API. The inclusion of Claim, Coverage, and ExplanationOfBenefit resources demonstrates that billing/financial data was considered, which is more than many small EHR vendors provide.

However, the documentation has significant shortcomings:

1. **It is examples-only** — no schema, no data dictionary, no field definitions. This is the weakest documentation format: it shows what one patient's data looks like but doesn't systematically describe what the export *can* contain.

2. **The coverage appears to be "what maps to FHIR"** rather than "everything the product stores." The product manages data for 10+ medical specialties, has a patient portal with forms and messaging, tracks telemedicine visits, handles referrals, and processes complex billing workflows. The export documentation covers a standard set of FHIR clinical resources plus financial resources, but there's no evidence that specialty-specific data, portal interactions, or communication records are captured.

3. **Missing Encounter resources** is a notable gap — encounters are the backbone of clinical documentation and are referenced by many other resources in the export, yet there is no Encounter resource in the export itself.

4. **The export mechanism appears identical to the FHIR Bulk Data API** (g)(10), augmented with financial resources. This is better than many vendors who just point to g(10), but the fundamental question remains: does the FHIR JSON export cover the full designated record set?

## Access Summary
- Final URL (after redirects): https://mdsynergy.com/wp-content/uploads/2024/12/AltheaEHIDocumentation.pdf
- Status: found
- Required browser: no
- Navigation complexity: direct_link
- Anti-bot issues: none

## Obstacles & Dead Ends
None. The URL was a clean, direct PDF download that required no special headers, no browser rendering, and no navigation. The PDF text extracted cleanly with pdftotext (Google Docs renderer produces good text-layer PDFs).
