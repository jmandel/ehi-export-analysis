# PointClickCare Technologies Inc. — EHI Export Documentation

Collected: 2026-02-16

## Source
- Registered URL: https://ehi-export.pointclickcare.com/site/index.html?_ga=2.54104619.209929156.1701272387-1273753859.1701272387
- CHPL IDs: 10246 (PointClickCare, version 4), 11729 (EHR for Practice Groups, version 3)
- Both products share the same EHI export documentation URL

## Navigation Journal

**Step 1: Initial probe**

```bash
curl -sI -L "https://ehi-export.pointclickcare.com/site/index.html" \
  -H 'User-Agent: Mozilla/5.0'
```

Result: HTTP 200, Content-Type: text/html, Content-Length: 13609. Hosted on Azure Web (Windows-Azure-Web/1.0). Last-Modified: 2026-02-09 (very recently updated). No redirects needed.

**Step 2: Page examination**

The index page is a FHIR Implementation Guide (IG) built with the HL7 FHIR IG Publisher toolchain. Title: "EHI Export Implementation Guide v0.1.0" (ci-build). Package: `ehi-export.pointclickcare.com#0.1.0`, based on FHIR R4 (4.0.1). Generated 2026-02-04.

Navigation has two links: Home and Artifacts. TOC link in breadcrumb reveals the full structure.

**Step 3: TOC page** (`toc.html`)

Table of contents shows:
1. EHI Export Implementation Guide (index.html)
2. Minimum Data Set (MDS) Export (MDS.html)
3. All Assessments Export (NonMDS.html)
4. Artifacts Summary (artifacts.html) — 71 sub-items (4.1–4.71)

**Step 4: Artifacts page** (`artifacts.html`)

Lists all artifacts in categories:
- Structures: Resource Profiles (26 profiles)
- Structures: Extension Definitions (31 extensions)
- Terminology: Value Sets (2)
- Terminology: Code Systems (2)
- Other (10 custom resources)

**Step 5: FHIR IG NPM package**

```bash
curl -sL "https://ehi-export.pointclickcare.com/site/package.tgz" \
  -H 'User-Agent: Mozilla/5.0' -o downloads/package.tgz
```

Successfully downloaded the standard FHIR IG package (479 KB, gzip compressed). Extracted to `downloads/package/package/` — contains 135 JSON files including 67 StructureDefinitions, 2 ValueSets, 2 CodeSystems, the ImplementationGuide resource, and validation artifacts.

**Step 6: Downloaded all 76 HTML pages**

All StructureDefinition, ValueSet, CodeSystem, MDS, NonMDS, index, TOC, and artifacts pages downloaded to `downloads/site/`.

**Step 7: Enrichment extraction**

Ran two Bun TypeScript scripts to extract structured data from the package JSON and HTML pages:
- `structure-definitions.json`: 67 profiles, 2 value sets, 2 code systems — zero parse failures
- `csv-schemas.json`: 12 CSV schemas with 225 total columns — zero parse failures

## What Was Found

PointClickCare has built a genuine FHIR R4 Implementation Guide specifically for their EHI Export. This is one of the most thorough and well-structured (b)(10) export documentation sets encountered. The IG goes well beyond repackaging a (g)(10) FHIR API — it defines custom FHIR-like resources for data categories that have no standard FHIR representation, and exports assessments in CSV format.

### Export Format

The export produces **encrypted compressed files** containing:

1. **FHIR R4 NDJSON files** — one per resource type per patient, for both standard and custom resources
2. **CSV files** — for MDS (Minimum Data Set) and non-MDS clinical assessments
3. **Attached files** — consent/advance directive documents in a `Files` folder, radiology images in a `radiology-attachments` folder, lab attachments in a `lab-attachments` folder

The directory structure per patient is:
```
[Patient ID]/
  [Patient ID].json              # Patient FHIR resource
  [Patient ID]-manifest.json     # Manifest of export contents
  mds_assessments/
    [Assessment ID]/
      assessment.csv, sections.csv, sectionV.csv,
      pdpmScores.csv, score.csv, sectionVRapProfile.csv, responses.csv
  non_mds_assessments/
    [Assessment ID]/
      assessment.csv, sections.csv, score.csv,
      responses.csv, sdoh_and_health_status_responses.csv
  Files/                         # Consent and advance directive documents
  radiology-attachments/         # Radiology images
  lab-attachments/               # Lab result attachments
```

Encryption keys are obtained through PointClickCare documentation (not publicly specified in the IG).

### Standard FHIR R4 Resource Profiles (26)

These are constrained profiles on standard FHIR resources:

| Resource | Description |
|----------|-------------|
| AllergyIntolerance | With PCC extensions for RecordedBy, RevisionBy, ResolvedDate, RevisionDate |
| CarePlan | Patient care plans |
| CareTeam | Care team with cross-references to Practitioner, PractitionerRole, Organization, RelatedPerson |
| Condition | Diagnoses and conditions |
| Coverage | Insurance coverage with PCC extensions for PayerType, PayerDescription, MedicareAdvantagePlan |
| DiagnosticReport | Lab and diagnostic results |
| DocumentReference | Progress notes, advanced directives, consent documents, radiology reports, skin/wound docs, therapy files |
| Encounter | Patient encounters (admissions/visits) |
| FamilyMemberHistory | Family health history |
| Goal | Care plan goals |
| Immunization | With PCC extension for ImmunizationStatus |
| Device (Implantable) | Implantable devices |
| Location | PCC-specific facility/location info |
| Medication | Drug details with RxNorm coding, form, strength, UOM |
| MedicationDispense | Pharmacy dispensing records |
| MedicationRequest | Orders with dose quantity, frequency, timing, indications, pharmacy details; extensive extension set (RouteOfAdministration, ScheduleStartDate, TimeCode, AdministeredBy, OrderCategory, OrderType, OrderedBy, Context, Custodian) |
| Observation | Vitals, occupation, smoking status, pregnancy status/intent |
| Organization | Facility/organization info |
| Patient | Demographics with US Core extensions (race, ethnicity, birth sex, gender identity, sex, tribal affiliation, pronouns) plus PCC extensions (PreviousName, Occupation, CompanyName) |
| Practitioner | Provider info |
| PractitionerRole | Provider roles |
| Procedure | Procedures performed |
| Provenance | Record provenance/audit trail |
| RelatedPerson | Patient contacts/relationships |
| ServiceRequest | Lab, imaging, and other service requests with LOINC order codes |
| Specimen | Lab specimens |

### Custom (Non-FHIR) Resources (10)

These are PCC-specific resource types that conform to FHIR Base Resource structure but define entirely new schemas for data domains that don't map to standard FHIR:

| Custom Resource | Description | Key Fields |
|----------------|-------------|------------|
| **Authorization** | Prior authorization records | payer, insurance, start/end dates, review dates, request status, authorization number, remaining days/visits |
| **BillingStatement** | Patient billing statements | statement date, invoice transactions, balance due, previous balance, payments, current charges, total due |
| **CareProfile** | Patient care profile questionnaires | category name, question text, value |
| **Census** | Patient census/admission tracking | 27 fields including action, payer, status, admission/discharge dates, room/bed, physician, payor plan, RAP billing flags, LOA (leave of absence) data |
| **Claim** | Insurance claims | 29 fields including status, revenue code, HIPPS code, service dates, charges, units, diagnosis codes, DRG, attending physician |
| **InvoiceTransaction** | Individual billing line items | effective date, description, units, unit amount, amount |
| **Order** | Non-pharmacy orders (lab, diet, imaging, immunization) | 36 fields including category, status, dates, diet details, lab details, communication method, LOINC codes |
| **Payment** | Payment records | receipt amount, trust amount, payer, posting date, check info, payment type |
| **medicalDevice** | Medical devices (non-implantable) | auxiliary device, device treatment (each with sub-elements) |
| **singleDevice** | Individual device records | device name, created by, detail |

### Custom Extensions (31)

PCC defines 31 extensions covering medication administration details, ordering metadata, payer information, patient demographics, and clinical tracking fields. These are well-documented with proper FHIR extension definitions.

### CSV Assessment Schemas

**MDS Assessments (7 CSV files, 166 columns total):**
- `assessment.csv` (90 columns) — Comprehensive MDS 3.0 assessment metadata including RUG scores, PDPM data, ADL indices, CAT triggers, CMI weights, HIPPS codes, submission batches
- `sections.csv` (9 columns) — Assessment section metadata
- `sectionV.csv` (9 columns) — Section V specific data (discharge planning)
- `pdpmScores.csv` (35 columns) — Patient-Driven Payment Model scoring across all five PDPM components (PT, OT, SLP, nursing, NTA) plus non-case-mix
- `score.csv` (2 columns) — RUG/PDPM scoring summaries
- `sectionVRapProfile.csv` (6 columns) — RAP (Resident Assessment Protocol) profiles
- `responses.csv` (15 columns) — Individual MDS question responses

**Non-MDS Assessments (5 CSV files, 59 columns total):**
- `assessment.csv` (25 columns) — Assessment metadata
- `sections.csv` (9 columns) — Section data
- `score.csv` (2 columns) — Scoring
- `responses.csv` (9 columns) — Question-level responses
- `sdoh_and_health_status_responses.csv` (14 columns) — SDOH and health status assessment responses

### Value Sets and Code Systems

- **Immunization Status** — PCC-defined: Historical, Active, Inactive, Discontinued, Refused, Not Applicable
- **Order Status** — PCC-defined: Active, Cancelled, Completed, Discontinued, Not Applicable, Pending, Voided

### Dependencies

The IG depends on:
- HL7 FHIR R4 Core (4.0.1)
- HL7 Terminology R4 (7.0.1)
- HL7 FHIR UV Extensions R4 (5.2.0)
- US Core 3.1.1
- mCODE 1.0.0 (Minimal Common Oncology Data Elements — interesting dependency for an LTPAC product)

## Export Coverage Assessment

### Data Domain Coverage

This is an **unusually comprehensive** EHI export for a certified EHR. Based on the product research, PointClickCare stores data across clinical, medication, financial/billing, administrative, care coordination, and analytics domains. The export covers:

**Clearly covered domains:**
- **Demographics and contacts** — Patient resource with extensive extensions (race, ethnicity, gender identity, pronouns, occupation, previous names)
- **Diagnoses/conditions** — Condition resource
- **Medications** — Three resources: Medication (drug details), MedicationRequest (orders with detailed dosing/timing), MedicationDispense (pharmacy dispensing)
- **Allergies** — AllergyIntolerance with PCC-specific tracking extensions
- **Lab results** — DiagnosticReport, Observation, ServiceRequest, Specimen; plus lab attachments folder
- **Vital signs** — Observation resource
- **Immunizations** — Immunization resource with status extension
- **Procedures** — Procedure resource
- **Care plans and goals** — CarePlan, Goal resources
- **Clinical notes** — DocumentReference covers progress notes, radiology reports, skin/wound docs, therapy files
- **Encounters** — Encounter resource
- **Care team** — CareTeam resource with cross-references
- **Family history** — FamilyMemberHistory
- **Insurance/coverage** — Coverage resource with payer type, Medicare Advantage plan extensions
- **Prior authorizations** — Custom Authorization resource with remaining days/visits tracking
- **Billing statements** — Custom BillingStatement with InvoiceTransaction line items
- **Insurance claims** — Custom Claim resource with 29 fields (revenue codes, HIPPS, DRG, charges, diagnosis codes)
- **Payments** — Custom Payment resource
- **MDS 3.0 assessments** — Exported as CSV with 7 files per assessment, 166 total columns covering all MDS data including PDPM scores, RUG calculations, ADL indices, CATs — this is critical for LTPAC and is excellently documented
- **Non-MDS clinical assessments** — All other assessments exported as CSV, including SDOH and health status data
- **Census/admission data** — Custom Census resource with 27 fields covering admission, discharge, transfers, leave of absence, bed/room, physician, payer
- **Care profiles** — Custom CareProfile resource for questionnaire-type data
- **Orders (non-pharmacy)** — Custom Order resource with 36 fields for diet, lab, diagnostic, and immunization orders
- **Medical devices** — Custom medicalDevice and singleDevice resources
- **Documents and consents** — DocumentReference plus Files folder for consent and advance directive documents
- **Radiology images** — Dedicated radiology-attachments folder
- **Provenance** — Provenance resource for record tracking

**Potentially missing or unclear domains:**
- **Medication administration records (eMAR)** — The product has a sophisticated eMAR (QuickMAR), but the export has MedicationRequest and MedicationDispense but no explicit MedicationAdministration resource. Medication administration may be partly captured via the AdministeredBy extension on MedicationRequest, or it may not be exported at the individual administration level.
- **Wound care tracking** — Mentioned as a DocumentReference type (skin/wound files) but may lack structured wound assessment data (measurements, staging).
- **Incident/event reports** — Not mentioned in the export documentation; these could be in the non-MDS assessments.
- **Trust fund management** — Not explicitly documented as a separate export; could be partially in Payment records.
- **Therapy data** — Therapy files referenced in DocumentReference, but structured therapy minutes/outcomes (critical for PDPM PT/OT/SLP scoring) are not clearly documented as a separate export — though PDPM scores are in the MDS CSV.
- **Secure messaging content** — The Secure Conversations module data doesn't appear to be exported.
- **External records incorporated into chart** — Not explicitly mentioned.

### Export Format & Standards

The export format is **FHIR R4 NDJSON plus CSV**, which is an excellent choice for a (b)(10) export:

- **Standard FHIR R4** for data that maps well to FHIR resources (clinical data, demographics, medications, etc.)
- **Custom FHIR-like resources** for data that doesn't fit standard FHIR (billing, claims, census, orders, devices) — these follow FHIR Base Resource structure with id and meta, making them parseable with FHIR tooling even though they're non-standard
- **CSV** for assessment data (MDS and non-MDS) — this is appropriate because MDS data is inherently tabular and question-response oriented
- **File attachments** for documents, radiology images, and lab results

The use of custom resources for billing/financial data is a strength — PCC could have omitted billing data (as many vendors do) or crammed it into ill-fitting standard FHIR resources. Instead, they created purpose-built schemas.

Cross-references between resources use FHIR references (e.g., CareTeam members reference Practitioner/PractitionerRole/Organization/RelatedPerson IDs), and index files provide lookup tables for referenced entities.

The FHIR version is R4 (4.0.1). US Core 3.1.1 is a dependency. The mCODE 1.0.0 dependency is notable but its impact on the export is not explicitly documented.

### Documentation Quality

**Strengths:**
- The documentation is a proper FHIR Implementation Guide built with standard HL7 tooling — the same tooling used for official HL7 IGs. This means it comes with machine-readable StructureDefinitions, proper navigation, and a familiar format for FHIR developers.
- The FHIR IG NPM package is published and downloadable — this is a machine-readable artifact that can be loaded into FHIR tooling for validation.
- 67 StructureDefinitions with snapshot and differential views provide complete field-level documentation.
- CSV schemas are documented with column names, data types, nullable flags, and descriptions.
- The index page explains the export format, directory structure, and cross-referencing mechanism with worked examples.
- Custom resources are clearly identified as "PointClickCare specific" in their descriptions.
- Recently updated (2026-02-04 generation date, 2026-02-09 last modified).

**Weaknesses:**
- Version 0.1.0 with "ci-build" status and `notForPublication: true` in the package metadata — this is technically a draft/development build, not a published release. The "Draft as of 2026-02-04" label confirms this.
- No sample export files or example resources are provided — a developer implementing an import would need to work entirely from the StructureDefinitions.
- No explicit user guide for how to request/perform an export — the documentation describes what comes out but not how to trigger it.
- Encryption key distribution is mentioned but not documented.
- The descriptions for some custom resources are minimal (e.g., CareProfile: "Patient CareProfile").
- No changelog or versioning beyond 0.1.0.

### Structure & Completeness

**Granularity:** Field-level documentation is comprehensive for most resources. Each element has a path, data type, cardinality (min/max), short description, and in many cases detailed definition. Binding information links to value sets where applicable. The MDS assessment CSV schemas have 90 columns for the main assessment file alone, with clear type and nullable specifications.

**Coded fields:** Some coded fields are documented with proper value set bindings (immunization status, order status). Others use reference to external coding systems (RxNorm for medications, NUCC for provider taxonomy, LOINC for observations and orders, ICD-10 for diagnoses, HCPCS for claims).

**Relationships:** Cross-references between resources are documented through the FHIR reference mechanism. The index page explains how to resolve references using index files. Parent-child relationships (e.g., BillingStatement → InvoiceTransaction, Census → payer details) are expressed through FHIR references.

**Overall assessment:** This is one of the strongest (b)(10) export documentation efforts observed. PointClickCare has clearly invested real engineering effort in their EHI export — they haven't simply repackaged their (g)(10) FHIR API. The custom resource definitions for billing, claims, census, and orders demonstrate genuine engagement with the (b)(10) requirement to export *all* EHI, not just the USCDI/US Core clinical subset. The use of the FHIR IG toolchain means the documentation is both human-readable (via the HTML site) and machine-readable (via the NPM package), which is a significant advantage.

## Access Summary
- Final URL (after redirects): https://ehi-export.pointclickcare.com/site/index.html
- Status: found
- Required browser: no (all content accessible via curl)
- Navigation complexity: direct_link (two-page site: Home + Artifacts, plus individual resource pages)
- Anti-bot issues: none

## Obstacles & Dead Ends

None. The documentation was immediately accessible, well-structured, and included a downloadable FHIR IG package. The URL had a Google Analytics tracking parameter (`_ga=...`) that had no effect on accessibility. The Azure Web hosting responded without any authentication, rate limiting, or anti-bot measures.
