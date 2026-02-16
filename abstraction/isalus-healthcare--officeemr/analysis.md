# EHI Export Analysis: iSALUS Healthcare

**Product**: OfficeEMR  
**Analysis date**: 2026-02-16  
**CHPL IDs**: 15.04.04.2629.Offi.21.02.1.220606 (CHPL #10914)

## 1. Product Context

OfficeEMR is a cloud-based all-in-one EHR, practice management, and billing suite from iSALUS Healthcare (now part of EverCommerce/EverHealth). It targets small-to-mid-sized ambulatory specialty practices across 45+ specialties, with purpose-built configurations for nephrology (including dialysis), urology, ENT, orthopedics, neurosurgery, and pain management.

Key data domains the product stores:
- **Clinical**: charting, progress notes, template-based encounters (HPI, ROS, exam, history, assessment, treatment plan), problem lists, medications, allergies, vitals, immunizations, lab results, orders, implantable devices, care plans/goals, health concerns, pregnancy tracking
- **Billing/Revenue Cycle**: claims, claim procedures, payments, denials, statements, prior authorizations, eligibility verification, fee schedules, price estimates, sliding fee schedules
- **Practice Management**: demographics, appointments/scheduling, insurance, responsible parties, emergency contacts, referral tracking, patient communications, portal messages, phone encounters
- **Specialty**: dialysis setup/visits, case management (CKCC), chronic care management, preschool billing
- **Documents**: scanned/uploaded documents (image_document, image_xref), letters, e-prescribing (optimize_rx), electronic prior authorization
- **Interoperability**: chart sharing, HIE data, immunization registry submissions

This sets a high bar for export coverage — the product has substantial billing, specialty, and operational data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `downloads/ehi-export-page.pdf` | 56-page PDF of the full EHI Export KnowledgeOwl article (all accordions expanded). Contains overview, purpose, instructions, and complete data dictionary for clinical and PM entities. Last modified 12/19/2025. | **Most informative** — complete data dictionary with field descriptions |
| `downloads/officeemr-b10-schema-v1-oct2023.zip` → `schema/OfficeEMR_B10_Schema_v1-OCT2023/` (80 files) | JSON Schema draft-07 definitions for all 79 export entities (+ readme). Each schema defines field names and JSON types. All `description` fields are empty strings. | **Highly informative** — definitive field/type inventory, but no semantic content |
| `downloads/isalus-ehi-export-data-elements-version1-oct2023.zip` → `data-elements/` (1 XLSX file) | Excel data dictionary with 1,051 field rows across 79 entities. Columns: Export Name, Field Items, FIELD Position, FIELD, Description, Example, Data Type (Clinical/PM). | **Highly informative** — descriptions, examples, and vendor categorization |
| `downloads/export-311322-voct2023.zip` → `sample-export/` (58 files) | Complete single-patient sample export for test patient ID 311322. Contains 57 data entity JSON files + readme.json with realistic test data. | **Highly informative** — working example of actual export output |
| `downloads/screenshot-main-ehi-page.png` | Screenshot of main EHI Export page (accordions collapsed) | Low — orientation only |
| `downloads/screenshot-main-ehi-expanded.png` | Full-page screenshot with all accordions expanded (16.8 MB) | Medium — confirms PDF content |
| `downloads/screenshot-ht1-b10-updates.png` | Screenshot of HTI-1 2026 updates: adding Tribal Affiliation, Occupation, Industry, Allergy Verification, Problem Verification (Q1 2026) | Medium — shows active maintenance |

## 3. Export Mechanics

- **Format**: Proprietary JSON — one `.json` file per entity type, each containing a JSON array of record objects. Not FHIR, C-CDA, or any healthcare standard.
- **Mechanism**: Self-service via Reports portal → EHI Export tool (UI-based, role-restricted)
- **Single-patient**: Users with "EHI Export" role search for a patient, request export, download ZIP immediately when completed.
- **All-patient (bulk)**: Users with "EHI Practice Export" role submit a request; fulfilled by iSALUS Data Export team. Approximately 15 days turnaround. Described as for practices migrating to a new EHR platform.
- **Access constraints**: Role-based access control (two specific roles). No mention of fees for single-patient export; all-patient export involves the vendor's data export team.
- **Included metadata**: Every export includes a `readme.json` with a link to the public format documentation.

## 4. Export Content: What's In It

### Data dictionary overview

Three complementary artifacts define the export format:
1. **JSON Schema files** (80 files): machine-readable structure with field names and JSON types; `description` fields are all empty strings
2. **XLSX data dictionary** (1,051 rows): field descriptions, examples, and Clinical/PM categorization for 79 entities (note: the XLSX has a systematic "b→PM" text corruption affecting ~9 entity and field names — e.g., `eligiPMility` instead of `eligibility`)
3. **PDF data dictionary** (56 pages): complete field-level descriptions organized into Clinical Data Exports and Practice Management Data Exports sections

Combined stats (from `analysis/entity-inventory-full.json`):
- **79 entities** (excluding readme)
- **1,069 total fields**
- **1,057 fields with descriptions** (98.9%)
- **1 entity with 0 descriptions**: `sliding_fee` (11 fields — present in schema but absent from both XLSX and PDF)
- **All 79 entities have JSON Schema type definitions**

### Sample export

The sample export contains 57 data entity files for test patient 311322 with realistic data:
- **Largest entities by record count**: lab_result (233), order (229), template_encounter_exam (229), medication (188), template_encounter (179), appointment (134)
- **22 entities absent from sample** (likely no data for test patient): accident, chart_share sub-files, eligibility, goal sub-files, health_concern, hie, immunization_registry, implantable_device, portal_message, pregnancy/pregnancy_visit, price_estimate_line, referral_tracking, sliding_fee, statement

### Vendor's own content organization

The vendor divides entities into two categories: **Clinical Data** (64 entities, 763 fields) and **Practice Management** (15 entities, 306 fields).

**Practice Management Entities** (vendor's categorization):

| Entity | Fields | Described | Sample Records |
|---|---|---|---|
| appointment | 20 | 20 | 134 |
| claim | 36 | 36 | 58 |
| claim_procedure | 30 | 30 | 65 |
| demographics | 41 | 41 | 1 |
| denial | 11 | 11 | 2 |
| eligibility | 4 | 4 | — |
| insurance | 46 | 46 | 4 |
| payment | 21 | 21 | 18 |
| preschool_billing | 6 | 6 | 1 |
| price_estimate | 11 | 11 | 1 |
| price_estimate_line | 9 | 9 | — |
| prior_authorization | 34 | 34 | 4 |
| prior_authorization_code | 7 | 7 | 4 |
| prior_authorization_rendering | 4 | 4 | 4 |
| statement | 26 | 26 | — |

**Clinical Data Entities** (top 20 by field count):

| Entity | Fields | Described | Sample Records |
|---|---|---|---|
| vital | 44 | 44 | 18 |
| immunization | 32 | 32 | 10 |
| case_management | 30 | 30 | 3 |
| responsible_party | 30 | 30 | 2 |
| medication | 29 | 29 | 188 |
| care_team | 24 | 24 | 2 |
| pregnancy | 24 | 24 | — |
| pregnancy_visit | 22 | 22 | — |
| chronic_care_management | 19 | 19 | 6 |
| dialysis_setup | 19 | 19 | 2 |
| accident | 17 | 17 | — |
| image_xref | 17 | 17 | 62 |
| implantable_device | 17 | 17 | — |
| lab_result | 17 | 17 | 233 |
| emergency_contact | 16 | 16 | 2 |
| order | 16 | 16 | 229 |
| problem_list | 15 | 15 | 24 |
| consent | 13 | 13 | 5 |
| immunization_registry | 14 | 13 | — |
| portal_message | 12 | 12 | — |

The complete inventory of all 79 entities is in `analysis/entity-inventory-full.json`.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

The vendor's export is organized around their internal data model rather than any standard. Key strengths:

**Deep billing coverage**: The Practice Management section includes 15 entities spanning claims (36 fields), claim procedures (30 fields), payments (21 fields), denials (11 fields), statements (26 fields), prior authorizations (34 fields + codes + rendering providers), price estimates (11 + 9 fields), and eligibility. This is not window dressing — the claim entity includes fields like `charge`, `balance`, `agingDate`, `agingDays`, `agingType`, `claimStatus`, `claimSubStatus`, `submissionDate`, and multiple payer references.

**Specialty-specific data**: Dialysis setup (19 fields) and dialysis visits (11 fields) reflect the nephrology specialization. Case management and CKCC (Comprehensive Kidney Care Contracting) entities are nephrology-specific. Preschool billing is a niche entity. Pregnancy and pregnancy_visit (24 + 22 fields) cover OB/GYN workflows.

**Granular clinical encounters**: Template encounters are decomposed into 8 sub-entities (base + HPI, ROS, exam, history, assessment, order fulfillment, treatment plan), each with 6-11 fields. This captures structured clinical documentation at a level well beyond what C-CDA or FHIR US Core would expose.

**Patient communications**: portal_message (12 fields), communication/communication_recipient (8 + 5 fields), phone_encounter (10 fields), letter (6 fields).

**Thinnest areas**: referral_tracking has only 2 fields. The goal sub-entities (goal_objective, goal_problem, goal_intervention, goal_comment) each have 4-6 fields. `sliding_fee` has 11 fields but zero descriptions.

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `demographics` (41 fields): name, DOB, address, phones, email, SSN, gender, marital status, race, ethnicity, language, employment, employer, multiple ID types, doctor/PCP/referring names | Thorough — well beyond USCDI minimums |
| Encounters / visits | ✅ Covered | `appointment` (20 fields), `template_encounter` + 7 sub-entities (83 combined fields), `extension_encounter` (9 fields), `progress_note` (11 fields), `phone_encounter` (10 fields) | Very thorough — structured encounters decomposed into clinical components |
| Problems / conditions | ✅ Covered | `problem_list` (15 fields: chronicInd, onsetDate, resolveDate, severity, status, ICD code), `problem_list_note` (7 fields), `health_concern` (10 fields) | Good depth with chronic indicators and notes |
| Medications / prescriptions | ✅ Covered | `medication` (29 fields: drugName, dosage, frequency, refills, daw, quantity, dateStart/Stop, rxNorm, ndc, prescriber), `pharmacy` (8 fields), `optimize_rx` (7 fields) | Thorough — includes pharmacy info and real-time benefit check data |
| Allergies | ✅ Covered | `allergy` (11 fields), `allergy_symptom` (8 fields) | Good — allergies + symptoms separated |
| Immunizations | ✅ Covered | `immunization` (32 fields: cvxCode, mvxCode, lotNumber, manufacturer, administeredDate, route, site, dose), `immunization_registry` (14 fields) | Very thorough — includes registry submission data |
| Vitals | ✅ Covered | `vital` (44 fields: BP sitting/standing/supine, pulse, respirations, height, weight, BMI, SpO2, temperature, head circumference, pain, waist, peak flow, visual acuity) | Exceptionally detailed — multiple positional BP readings |
| Lab results | ✅ Covered | `lab_result` (17 fields: labName, labAddress, abnormalFlags, resultValue, units), `order_finding` (6 fields) | Good coverage with 233 sample records |
| Imaging / diagnostic reports | ⚠️ Partial | `order` (16 fields) covers generic orders which may include imaging. `image_document` (5 fields) and `image_xref` (17 fields) appear to reference scanned/uploaded documents, not DICOM imaging | Product supports e-labs and order entry; imaging-specific entities not apparent |
| Procedures | ✅ Covered | `claim_procedure` (30 fields: cptCode, modifier, diagCode, units, charge), `template_encounter_order_fulfillment` (11 fields) | Captured via billing codes and encounter documentation |
| Clinical notes / documents | ✅ Covered | `progress_note` (11 fields), template encounter sub-entities, `image_document` (5 fields), `image_xref` (17 fields), `letter` (6 fields) | Progress notes + structured templates + document metadata. Note: actual document files (PDF, JPEG) referenced via image_xref and provided separately |
| Care plans / goals | ✅ Covered | `care_plan_goal` (10 fields), `goal` + 4 sub-entities (27 combined fields), `template_encounter_treatment_plan` (11 fields) | Solid — goals with objectives, interventions, problems, comments |
| Orders / referrals | ✅ Covered | `order` (16 fields), `order_finding` (6 fields), `referral_tracking` (2 fields), `epa` (4 fields) | Orders well-covered; referral_tracking is thin (only 2 fields) |
| Insurance / coverage | ✅ Covered | `insurance` (46 fields: policyNumber, groupNumber, subscriber info, payer details, copay, coinsurance, authorization, eligibility status), `responsible_party` (30 fields) | Very thorough — largest entity by field count |
| Claims / billing | ✅ Covered | `claim` (36 fields), `claim_procedure` (30 fields), `denial` (11 fields), `prior_authorization` + code + rendering (45 combined fields), `preschool_billing` (6 fields) | Genuinely deep — claims, procedures, denials, prior auth all detailed |
| Payments | ✅ Covered | `payment` (21 fields), `statement` (26 fields), `price_estimate` + line (20 combined fields), `sliding_fee` (11 fields) | Comprehensive — payments, statements with aging, price estimates |
| Consents / directives | ✅ Covered | `consent` (13 fields: consentType, signatureDate, startDate, endDate, status) | Present and adequately detailed |
| Patient communications | ✅ Covered | `portal_message` (12 fields), `communication` (8 fields), `communication_recipient` (5 fields), `phone_encounter` (10 fields), `letter` (6 fields) | Multiple communication channels covered |
| Specialty-specific (nephrology) | ✅ Covered | `dialysis_setup` (19 fields), `dialysis_visit` (11 fields), `case_management` (30 fields), `case_management_ckcc_note` (6 fields), `ckcc_status` (3 fields), `chronic_care_management` (19 fields) | Specialty data specifically built for nephrology/CKCC programs |
| Specialty-specific (OB/GYN) | ✅ Covered | `pregnancy` (24 fields), `pregnancy_visit` (22 fields) | Dedicated pregnancy/prenatal tracking entities |
| Implantable devices | ✅ Covered | `implantable_device` (17 fields: deviceName, deviceDescription, UDI data, implantDate) | Present with UDI-level detail |
| Education | ✅ Covered | `education` (9 fields) | Patient education materials documented |
| HIE / interoperability | ✅ Covered | `hie` (9 fields), `chart_share` + detail/note entities (26 combined fields) | Health information exchange records included |

## 6. Documentation Quality

**Strengths:**
- **Three complementary artifacts**: JSON Schema (machine-readable structure), XLSX (human-readable descriptions with examples), and PDF (comprehensive reference). This is an uncommonly thorough documentation approach, especially for a smaller vendor.
- **Near-complete descriptions**: 1,057 of 1,069 fields (98.9%) have plain-English descriptions. Only `sliding_fee` (11 fields) lacks any descriptions.
- **Working sample export**: A complete single-patient export with realistic test data across 57 entities — a developer could immediately understand the format and begin building an import.
- **Public accessibility**: All documentation freely accessible at the registered URL, no login required.
- **Active maintenance**: Documentation last updated 12/19/2025; HTI-1/USCDIv3 additions being prepared for Q1 2026.

**Weaknesses:**
- **Empty JSON Schema descriptions**: All `description` fields in the 80 schema files are empty strings. The schemas provide structure/types but no semantic meaning — the XLSX or PDF must be consulted separately.
- **No value set documentation**: Coded fields (e.g., `claimStatus`, `gender`, `agingType`, `consentType`) are typed as strings with no enumeration of valid values or code systems.
- **No relationship documentation**: Entity relationships are implicit via shared IDs (e.g., `patientId`, `claimId`). No ER diagram, no foreign key documentation, no cardinality notes.
- **XLSX data corruption**: The XLSX has a systematic text corruption where "b" is replaced by "PM" in ~9 entity names and some field names (e.g., `eligiPMility` for `eligibility`, `proPMlem_list` for `problem_list`). This is a vendor QA issue.
- **No date format specification**: Dates appear in inconsistent formats: `"19011212"` (YYYYMMDD), `"20150302144846-0400"` (with timezone), `"MM/DD/YYYY HH:MMAM/PM"`. No documentation of format conventions.
- **Could a developer build an import?** Largely yes — the combination of schemas, descriptions, examples, and sample data provides enough to build a parser. The gaps are in coded value interpretation, entity relationships, and date format handling.

## 7. Overall Assessment

### Classification

**Axis 1 — Coverage breadth: Comprehensive**

This export demonstrably covers the breadth of data domains that OfficeEMR stores. It goes well beyond USCDI/clinical summary territory into billing (claims, procedures, denials, payments, statements, prior authorizations), practice management (appointments, demographics, insurance with 46 fields), specialty clinical data (dialysis, CKCC case management, pregnancy tracking), patient communications (portal messages, phone encounters, letters), and operational data (chart sharing, HIE, eligibility verification). With 79 entities and 1,069 fields, this is a genuine representation of the product's internal data model, not a clinical summary repackaged.

The export is comprehensive *relative to what OfficeEMR stores*. The product is an ambulatory EHR+PM — it doesn't do inpatient, ED, or pharmacy dispensing — and the export appropriately reflects that scope. The only notable gap is the absence of a dedicated `fee_schedule` entity (mentioned in documentation but not present in the schema ZIP), and the extremely thin `referral_tracking` entity (just 2 fields). Telehealth session data (from the AnywhereCare module) and patient intake forms (Intelligent Intake) are not explicitly surfaced as separate entities, though they may be captured within progress notes or template encounters.

**Axis 2 — Export approach: Purpose-built EHI export**

This is clearly a purpose-built export for (b)(10), not a repackaged FHIR or C-CDA export. The signals:
1. The vendor explicitly states this "replaces and expands upon our existing certified §170.315(b)(6) Data export which allows our customers to bulk export patient CCDA files" — they distinguish this from their C-CDA capability.
2. The export uses a proprietary JSON format mirroring the vendor's internal data model — it is not FHIR resources or C-CDA sections.
3. Billing entities (claims, payments, denials, prior authorizations, statements) are extensively covered — these have no analog in FHIR US Core / (g)(10) or C-CDA.
4. Specialty entities (dialysis_setup, dialysis_visit, case_management, ckcc_status, pregnancy/pregnancy_visit) are product-specific and have no standard exchange counterpart.
5. The vendor built dedicated JSON Schema files, an XLSX data dictionary, and a sample export specifically for this capability.

### Key Findings

1. **Genuinely deep billing coverage**: 15 Practice Management entities with 306 fields covering claims, claim procedures, payments, denials, statements, prior authorizations (with codes and rendering providers), price estimates, and eligibility. This is the strongest signal that the vendor took (b)(10) seriously — billing data is entirely absent from standard clinical exchange formats.

2. **Specialty clinical data included**: Nephrology-specific entities (dialysis_setup, dialysis_visit, case_management, CKCC notes/status, chronic care management) and OB/GYN entities (pregnancy, pregnancy_visit) demonstrate the vendor exports beyond generic clinical data.

3. **Unusually thorough documentation for a small vendor**: Three complementary artifacts (JSON Schema, XLSX, sample export), 98.9% field description coverage, and a 56-page PDF reference. The XLSX even includes example values for every field.

4. **XLSX has systematic data corruption**: The "b→PM" text replacement corruption affects ~9 entity names and associated field names. While the correct names can be inferred from the schema files, this is a quality control issue that could confuse consumers of the XLSX.

5. **Value sets and relationships undocumented**: Despite the thorough field descriptions, there is no documentation of valid values for coded fields or formal entity relationships. A consumer would need to reverse-engineer these from the sample data.

### Summary Stats

```
Coverage:        Comprehensive
Approach:        Purpose-built EHI export
Export format:   Proprietary JSON (one file per entity type)
Entities:        79
Fields:          1,069
Descriptions:    98.9% (1,057 of 1,069)
Sample data:     Yes (57 entity files for test patient)
Bulk export:     Yes (vendor-assisted, ~15 days)
Domains covered: 19 of 19 applicable domains
```

### Bottom Line

OfficeEMR provides one of the more complete (b)(10) implementations among smaller EHR vendors. A patient or provider would receive a comprehensive copy of their clinical, billing, and administrative data in a machine-readable format with solid documentation. The single biggest strength is the genuine inclusion of billing and specialty data alongside clinical records; the single biggest gap is the lack of value set documentation for coded fields, which limits downstream interpretability without reverse engineering.
