# EHI Export Analysis: iSALUS Healthcare

**Product**: OfficeEMR v2021
**Analysis date**: 2026-02-15
**CHPL IDs**: 15.04.04.2629.Offi.21.02.1.220606 (CHPL ID 10914)

## 1. Product Context

OfficeEMR is a cloud-based, all-in-one EHR, practice management, and billing suite for small to mid-sized ambulatory specialty practices. Developed by iSALUS Healthcare (now part of EverCommerce's EverHealth division), it provides integrated clinical charting, scheduling, e-prescribing (including EPCS), billing/claims management, patient portal, telehealth (AnywhereCare), and document management in a single platform. The product has purpose-built configurations for nephrology (including dialysis rounding), urology, ENT, orthopedics, neurosurgery, and pain management, plus a customizable "Choice EHR" option covering 45+ additional specialties.

Key data domains the product should store and export:
- **Clinical**: demographics, encounters, progress notes, template-based encounter documentation (HPI, ROS, exam, assessment, treatment plan), problem lists, allergies, medications, vitals, immunizations, lab results, orders, referrals, care plans, clinical notes, patient education, pregnancy data
- **Billing/PM**: claims, claim procedures, payments, denials, statements, prior authorizations, fee schedules, price estimates, insurance/eligibility, sliding fee schedules
- **Specialty**: dialysis setup/visits, case management (CKCC), chronic care management, remote patient monitoring (md_revolution)
- **Documents/Communications**: scanned documents (eDocuments), patient portal messages, letters, phone encounters, patient communications
- **Patient engagement**: patient intake forms (Intelligent Intake), telehealth session records

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.pdf` (56 pages, 3.98 MB) | Full PDF export of KnowledgeOwl knowledge base article with all sections expanded. Contains overview, purpose, access instructions, single/all-patient export procedures, "What's Included" section, complete data dictionary (Clinical + Practice Management), and export references. | **High** — most comprehensive single document |
| `officeemr-b10-schema-v1-oct2023.zip` (80 JSON Schema files) | JSON Schema draft-07 definitions for all export entity types. Every field has a name and type but all `description` fields are empty strings. 2 files have JSON syntax errors (payment.json, statement.json). | **Medium** — provides machine-readable structure but no semantic context |
| `isalus-ehi-export-data-elements-version1-oct2023.zip` (1 XLSX file) | Excel data dictionary with two sheets: "Export File Name Listing" (79 entities) and "Export Field Listing" (1,051 fields with descriptions, examples, and Clinical/PM classification). | **High** — best source for field-level understanding |
| `export-311322-voct2023.zip` (58 JSON data files) | Complete sample single-patient export for test patient ID 311322. Contains realistic test data with 1,960 total records across all entities. | **High** — demonstrates actual export output and data quality |
| `screenshot-main-ehi-page.png` | Screenshot of KnowledgeOwl page with collapsed accordion sections. | Low |
| `screenshot-main-ehi-expanded.png` (16.8 MB) | Full-page screenshot with all sections expanded. | Low (PDF is more useful) |
| `screenshot-ht1-b10-updates.png` | Shows upcoming HTI-1/USCDIv3 additions: Tribal Affiliation, Occupation, Industry (demographics); Verification (allergies, problems). Marked Q1 2026. | Low — future plans only |

## 3. Export Mechanics

- **Format**: Proprietary JSON — one file per entity type, each containing a JSON array of record objects. Not FHIR, C-CDA, or any healthcare standard.
- **Single-patient export**: Self-service via Reports portal → EHI Export tool. Users with "EHI Export" role search for a patient, request the export, and download a ZIP file immediately upon completion. No developer assistance required.
- **All-patient (practice) export**: Users with "EHI Practice Export" role submit a request through the same tool. This triggers a process involving the iSALUS Data Export team. Described as being for practices migrating to a new EHR platform. Approximate turnaround is ~15 days. The vendor notes that "charges for All Patient exports are very limited in scope when the request is for practice moving to a new EHR platform" and outlines what is "no-cost" vs. what "will incur a cost," though specific pricing is not detailed in the documentation.
- **Document images**: Provided separately as a zipped file containing document images in their original format (PDF, JPEG, PNG).
- **Export includes**: A `readme.json` file with a link to the publicly accessible format documentation (`https://officeemr.knowledgeowl.com/help/ehi-export`).
- **Linking**: All entity files contain a `patientId` field for patient association. Some entities have foreign keys (e.g., `claimId` in claim_procedure), but relationships are not formally documented.

## 4. Export Content: What's In It

### Data Dictionary Summary

The XLSX data dictionary (`iSalus_EHI_ExportDataElements_published_version1_Oct2023_pristine.xlsx`) defines **79 entities** with **1,051 total fields**. All 1,051 fields have human-readable descriptions, examples, and a Clinical/PM data type classification. The entities are divided into:

- **Clinical entities**: 64 entities, 751 fields
- **Practice Management entities**: 15 entities, 304 fields (note: the XLSX classifies demographics, appointments, insurance, and claims as "PM" rather than "Clinical")

The JSON Schema package contains **80 files** (78 entity schemas + readme + 1 entity that maps to readme). Schema files provide field names and JSON types but all `description` fields are empty strings (`""`). Two schema files (`payment.json`, `statement.json`) contain JSON syntax errors (e.g., double commas) and cannot be parsed.

### Sample Export Summary

The sample export for test patient 311322 contains **58 JSON files** with **1,960 total records**. Entities absent from the sample but present in schemas (22 entities) likely have no data for this test patient. Key record counts:

| Entity | Records | Fields | Domain |
|---|---|---|---|
| lab_result | 233 | 17 | Lab Results |
| template_encounter_exam | 229 | 11 | Encounters |
| order | 229 | 15 | Orders |
| medication | 188 | 28 | Medications |
| template_encounter | 179 | 6 | Encounters |
| appointment | 134 | 20 | Encounters |
| letter | 79 | 6 | Clinical Notes |
| claim_procedure | 65 | 30 | Billing |
| image_xref | 62 | 17 | Documents |
| communication_recipient | 61 | 5 | Communications |
| claim | 58 | 36 | Billing |
| progress_note | 45 | 11 | Clinical Notes |
| template_encounter_hpi | 39 | 11 | Encounters |
| template_encounter_treatment_plan | 39 | 11 | Encounters |
| communication | 32 | 8 | Communications |
| problem_list_note | 29 | 6 | Problems |
| extension_results | 25 | 11 | Lab Results |
| template_encounter_history | 25 | 11 | Encounters |
| problem_list | 23 | 15 | Problems |
| epa | 19 | 4 | Medications |
| vital | 18 | 44 | Vitals |
| template_encounter_ros | 17 | 11 | Encounters |
| pharmacy | 16 | 8 | Medications |
| template_encounter_order_fulfillment | 13 | 11 | Encounters |
| immunization | 10 | 30 | Immunizations |
| payment | 9 | 21 | Payments |
| allergy | 7 | 11 | Allergies |
| comment | 7 | 8 | Communications |
| care_plan_goal | 5 | 10 | Care Plans |
| image_document | 5 | 5 | Documents |
| template_encounter_assessment | 5 | 11 | Encounters |
| insurance | 4 | 46 | Insurance |
| denial | 4 | 11 | Billing |
| dialysis_visit | 4 | 11 | Specialty |
| order_finding | 4 | 6 | Orders |
| prior_authorization | 4 | 32 | Authorizations |
| prior_authorization_code | 3 | 7 | Authorizations |
| care_team | 3 | 24 | Care Plans |
| case_management | 3 | 30 | Specialty |
| allergy_symptom | 2 | 8 | Allergies |
| dialysis_setup | 2 | 19 | Specialty |
| education | 2 | 9 | Education |
| emergency_contact | 2 | 16 | Demographics |
| extension_encounter | 2 | 9 | Encounters |
| prior_authorization_rendering | 2 | 4 | Authorizations |
| responsible_party | 2 | 30 | Demographics |
| demographics | 1 | 41 | Demographics |
| consent | 1 | 13 | Consents |
| chronic_care_management | 1 | 19 | Specialty |
| Others (1 record each) | — | — | Various |

### Field Detail Quality

From the XLSX, every field has:
- **Field name**: Yes (all 1,051)
- **Description**: Yes (all 1,051) — plain-English explanations like "The country where the accident occurred", "Patient's date of birth", "The charge amount"
- **Example value**: Yes (all 1,051) — inline JSON examples like `"accidentCountry": "USA"`
- **Data type classification**: Yes — "Clinical" or "PM" (Practice Management)
- **JSON Schema type**: Yes (in schema files) — string, number, object (used for nullable), array
- **Value sets/enumerations**: **No** — coded fields like `claimStatus`, `gender`, `maritalStatus`, `employmentStatus` are typed as strings with no documented valid values
- **Relationships/foreign keys**: **Not formally documented** — implied through shared ID fields (e.g., `patientId` in every file, `claimId` in claim_procedure) but no ER diagram or relationship documentation exists

### Notable Data Structures

- **Vitals**: Exceptionally detailed with 44 fields including sitting/standing/supine blood pressure (systolic, diastolic, pulse, rhythm, extremity for each position), pulse oximetry (O2 saturation, FiO2, liters/min, delivery method), anthropometric measurements (height, weight, head/neck/waist/hip circumference, body fat), and percentiles.
- **Template encounters**: Decomposed into 8 sub-entities (assessment, exam, history, HPI, order_fulfillment, ROS, treatment_plan, plus the parent encounter), providing granular structured encounter documentation.
- **Claims**: 36 fields including charge, balance, aging, claim status/sub-status, multiple payer levels (primary/secondary/tertiary), multiple provider roles (billing, attending, ordering, referring, rendering, supervising).
- **Progress notes**: Store clinical notes as HTML content in a `html` field, preserving formatting. Sign-off tracking included.
- **Insurance**: 46 fields — the most field-rich entity — covering subscriber details, policy numbers, group information, and multiple coverage levels.

## 5. Coverage Assessment

| Domain | Status | Evidence |
|---|---|---|
| **Demographics** | ✅ Covered | `demographics.json` (41 fields): name, DOB, death date, address, phones, email, IDs (SSN, member ID), gender, marital status, race, ethnicity, language, employment, employer, provider assignments. `emergency_contact.json` (16 fields), `responsible_party.json` (30 fields). |
| **Encounters / Visits** | ✅ Covered | `appointment.json` (20 fields), `template_encounter.json` + 7 sub-entities (HPI, ROS, exam, history, assessment, treatment plan, order fulfillment — 11 fields each), `extension_encounter.json` (9 fields), `phone_encounter.json` (10 fields). 134 appointments and 179 template encounters in sample. |
| **Problems / Diagnoses** | ✅ Covered | `problem_list.json` (15 fields), `problem_list_note.json` (6 fields), `health_concern.json` (10 fields). 23 problems and 29 problem notes in sample. |
| **Medications / Prescriptions** | ✅ Covered | `medication.json` (28 fields), `pharmacy.json` (8 fields), `optimize_rx.json` (7 fields), `epa.json` (electronic prior authorization, 4 fields). 188 medications in sample. |
| **Allergies** | ✅ Covered | `allergy.json` (11 fields), `allergy_symptom.json` (8 fields). 7 allergies in sample. |
| **Immunizations** | ✅ Covered | `immunization.json` (30 fields), `immunization_registry.json` (12 fields). Detailed: vaccine description, dates, VIS info, VFC status, funding source, manufacturer, lot, site, route, reaction, ordered/admin by. 10 immunizations in sample. |
| **Vitals** | ✅ Covered | `vital.json` (44 fields). Exceptionally detailed with positional BP, pulse ox, anthropometrics. 18 records in sample. |
| **Lab Results** | ✅ Covered | `lab_result.json` (17 fields), `extension_results.json` (11 fields), `order_finding.json` (6 fields). 233 lab results in sample. |
| **Procedures** | ✅ Covered | `claim_procedure.json` (30 fields) captures procedure-level detail. Template encounter sub-entities capture surgical/procedure documentation. |
| **Clinical Notes / Documents** | ✅ Covered | `progress_note.json` (11 fields, notes stored as HTML), `letter.json` (6 fields). 45 progress notes and 79 letters in sample. |
| **Documents / Images** | ✅ Covered | `image_document.json` (5 fields), `image_xref.json` (17 fields). Document images provided separately in original format (PDF, JPEG, PNG). 5 documents and 62 cross-references in sample. |
| **Care Plans / Goals** | ✅ Covered | `care_plan_goal.json` (10 fields), `care_team.json` (24 fields), `goal.json` + 4 sub-entities (comment, intervention, objective, problem). |
| **Orders / Referrals** | ✅ Covered | `order.json` (15 fields), `order_finding.json` (6 fields), `referral_tracking.json` (2 fields). 229 orders in sample. |
| **Insurance / Coverage** | ✅ Covered | `insurance.json` (46 fields), `eligibility.json` (4 fields). Detailed subscriber, policy, group, and multi-level coverage data. |
| **Claims / Billing** | ✅ Covered | `claim.json` (36 fields), `claim_procedure.json` (30 fields), `denial.json` (11 fields), `statement.json` (26 fields), `fee_schedule.json` (referenced in XLSX), `sliding_fee.json` (11 fields), `preschool_billing.json` (6 fields), `price_estimate.json` (11 fields), `price_estimate_line.json` (9 fields). 58 claims, 65 procedures, 4 denials in sample. |
| **Payments** | ✅ Covered | `payment.json` (21 fields). Includes paid amount, adjustment, method, type, payer info at primary/secondary/tertiary levels. 9 payments in sample. |
| **Prior Authorizations** | ✅ Covered | `prior_authorization.json` (32 fields), `prior_authorization_code.json` (7 fields), `prior_authorization_rendering.json` (4 fields). |
| **Consents / Directives** | ✅ Covered | `consent.json` (13 fields). 1 consent in sample. |
| **Patient Communications** | ✅ Covered | `communication.json` (8 fields), `communication_recipient.json` (5 fields), `portal_message.json` (12 fields), `comment.json` (8 fields). 32 communications in sample. |
| **Patient Education** | ✅ Covered | `education.json` (9 fields). 2 records in sample. |
| **Specialty: Dialysis** | ✅ Covered | `dialysis_setup.json` (19 fields), `dialysis_visit.json` (11 fields). Purpose-built for nephrology. |
| **Specialty: Pregnancy** | ✅ Covered | `pregnancy.json` (24 fields), `pregnancy_visit.json` (22 fields). |
| **Specialty: Case Mgmt** | ✅ Covered | `case_management.json` (30 fields), `case_management_ckcc_note.json` (6 fields), `ckcc_status.json` (3 fields). |
| **Specialty: Chronic Care** | ✅ Covered | `chronic_care_management.json` (19 fields). |
| **Specialty: RPM** | ✅ Covered | `md_revolution_status.json` (5 fields). |
| **Accident/Injury** | ✅ Covered | `accident.json` (17 fields). |
| **Imaging / Diagnostic Reports** | ⚠️ Partially covered | No dedicated radiology/imaging report entity. Image documents are covered but structured imaging results (e.g., radiology reads) would need to be in `progress_note` or `extension_results`. |
| **Telehealth Sessions** | ⚠️ Unclear | AnywhereCare is a product feature but no dedicated telehealth entity. Likely captured within `template_encounter` or `progress_note`. |
| **Patient Intake Forms** | ⚠️ Unclear | Intelligent Intake (digital intake) is a product feature but no dedicated intake form entity. May be subsumed under existing clinical documentation. |

## 6. Documentation Quality

### Strengths

- **Three complementary artifacts**: JSON Schema (machine-readable structure), XLSX data dictionary (human-readable field descriptions with examples), and sample patient export (working demonstration). This is an unusually thorough documentation set, especially for a smaller vendor.
- **100% field description coverage**: All 1,051 fields in the XLSX have plain-English descriptions and inline examples. A developer could understand the meaning and expected format of every field.
- **Sample data**: The 58-file sample export with 1,960 records across clinical and billing domains provides a concrete reference implementation. A developer could build an import parser from these artifacts.
- **Public accessibility**: All documentation is publicly accessible at `https://officeemr.knowledgeowl.com/help/ehi-export` with no login required.
- **Active maintenance**: Documentation was last modified 2025-12-19, and HTI-1/USCDIv3 additions are already documented as coming Q1 2026.
- **Clear "What's Included" section**: Explicitly defines scope — patient-identifiable data that is "explicitly associated with a patient record" — and what is excluded (internal communications, practice operations, system data).

### Weaknesses

- **Empty JSON Schema descriptions**: All `description` fields in the 80 JSON Schema files are empty strings. The schemas provide type information but no semantic context. A developer must cross-reference the XLSX or PDF to understand field meanings.
- **JSON Schema errors**: `payment.json` and `statement.json` schema files contain JSON syntax errors and cannot be parsed programmatically.
- **No value set documentation**: Coded fields (e.g., `claimStatus` values like "Closed - Electronic Superbill", `gender`, `maritalStatus`, `employmentStatus`) have no enumerated valid values documented anywhere. A developer seeing `claimStatus` could not know all possible values without examining production data.
- **No relationship documentation**: Entity relationships are implicit (shared `patientId`, `claimId`, `encounterId`) but never formally described. No ER diagram, no foreign key documentation, no cardinality specification. The PDF mentions one relationship in passing: "price_estimate_line.json can be 1-to-many" relative to price_estimate.
- **Date format inconsistency**: Some dates are `YYYYMMDD` strings (e.g., `birthDate: "19011212"`), others include time and timezone (e.g., `authorLogDateUtc: "20150302144846-0400"`), and immunization dates use `MM/DD/YYYY` (e.g., `dateGiven: "07/25/2016"`). No date format convention is documented.
- **XLSX character encoding artifacts**: Some entity names in the XLSX contain "PM" character substitutions (e.g., "eligiPMility" for "eligibility", "implantaPMle_device" for "implantable_device"), suggesting a rendering or character encoding issue in the spreadsheet.

### Could a developer build an import?

**Yes, with caveats.** The combination of sample data + XLSX descriptions + JSON schemas provides enough to parse and understand the export. The main barriers would be: (1) interpreting coded field values without value set documentation, (2) reconstructing entity relationships without a relationship schema, and (3) handling date format inconsistencies.

## 7. Overall Assessment

### Classification

**Comprehensive native export.** This is a genuine, purpose-built (b)(10) export that covers the vendor's native data model across clinical, billing, and specialty domains. It is explicitly not FHIR, C-CDA, or any healthcare standard — it exports the product's internal data structure as JSON. The coverage spans 79 entities with 1,051 documented fields across demographics, encounters, problems, medications, allergies, immunizations, vitals, labs, orders, clinical notes, documents, care plans, claims, payments, denials, statements, prior authorizations, insurance, and multiple specialty domains (dialysis, pregnancy, case management, chronic care management, RPM). The documentation includes machine-readable schemas, a complete field-level data dictionary, and a sample patient export.

### Key Findings

1. **Genuine native data model export with broad coverage.** 79 entities and 1,051 fields covering both clinical and practice management data — this is not a C-CDA or FHIR repackaging. The export covers domains (claims, denials, payments, statements, prior authorizations, fee schedules, sliding fees, price estimates, dialysis data, case management) that would never appear in a standard clinical summary.

2. **Excellent field-level documentation.** All 1,051 fields have human-readable descriptions and inline examples in the XLSX data dictionary. This is 100% description coverage — rare among EHR vendors of any size.

3. **Working sample export with realistic data.** The 58-file, 1,960-record sample patient export demonstrates actual output with populated fields across clinical and billing domains. This is concrete evidence the export works, not just documentation of intent.

4. **No value set or relationship documentation.** The biggest gap is the absence of coded value enumerations and formal relationship documentation. A developer could parse the export but would need production data or vendor support to fully interpret coded fields and reconstruct entity relationships.

5. **Minor schema quality issues.** JSON Schema files have universally empty descriptions and two files have syntax errors. The schemas provide structure and types but require the XLSX for semantic understanding.

### Bottom Line

A patient or provider would get a usable, largely complete copy of their data from this export. The export covers clinical documentation, billing records, specialty data, and documents in a well-documented JSON format with field-level descriptions. The main gap is the lack of value set documentation for coded fields, which would impede fully automated interpretation of the exported data — but the data itself appears to be comprehensive across the product's stored domains.
