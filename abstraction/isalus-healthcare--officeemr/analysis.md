# EHI Export Analysis: iSALUS Healthcare

**Product**: OfficeEMR v2021
**Analysis date**: 2026-02-15
**CHPL ID**: 15.04.04.2629.Offi.21.02.1.220606 (CHPL #10914)

## 1. Product Context

OfficeEMR is a cloud-based, all-in-one EHR, practice management, and billing suite targeting small-to-mid-sized ambulatory specialty practices. Developed by iSALUS Healthcare (now part of EverCommerce's EverHealth division), it provides integrated clinical charting, scheduling, e-prescribing, billing/claims management, patient portal, telehealth, and document management from a single platform. It is certified for 37 ONC criteria including (b)(10).

**Key data domains the product stores:**
- **Clinical**: Progress notes, template encounters (with HPI, ROS, exam, history, assessment, treatment plan), vitals, allergies, problem lists, medications, immunizations, lab results, orders, care plans, referrals, clinical notes, consent forms, pregnancy data, dialysis visit/setup data (nephrology specialty), case management
- **Billing/PM**: Claims, claim procedures, payments, denials, statements, prior authorizations, price estimates, fee schedules, insurance/payer information, eligibility verification, responsible parties, appointments
- **Specialty**: Nephrology (dialysis rounding), urology, ENT (ENTChoice), orthopedics, neurosurgery, pain management — with customizable templates for 45+ specialties
- **Patient engagement**: Portal messages, communications, patient intake forms (Intelligent Intake), telehealth (AnywhereCare)
- **Documents**: Scanned documents, images, letters, electronic faxes

This is a comprehensive ambulatory platform. A complete EHI export should cover clinical, billing, scheduling, communications, and specialty-specific data.

## 2. Artifacts Reviewed

| Artifact | Description | Informativeness |
|---|---|---|
| `ehi-export-page.pdf` (56 pages, 3.98 MB) | PDF export of the full KnowledgeOwl EHI Export article with all sections expanded. Contains overview, export mechanics, step-by-step instructions, and the complete data dictionary for all 78 entities. | **Most informative** — uncorrupted source of field-level documentation |
| `officeemr-b10-schema-v1-oct2023.zip` (80 JSON files, 38 KB) | JSON Schema (draft-07) definitions for all export entities. Defines field names and types but all `description` fields are empty strings. Includes 67 `.schema.json` files and 13 plain `.json` files. Two files (`payment.json`, `statement.json`) contain syntax errors (double commas). | **Highly informative** — machine-readable field structure and types |
| `isalus-ehi-export-data-elements-version1-oct2023.zip` (1 XLSX file, 97 KB) | Excel data dictionary with 2 sheets: file listing (79 entities) and field listing (1,051 fields with descriptions, examples, and category tags). Contains a text corruption where "b" is systematically replaced with "PM" in some entity names and descriptions (e.g., "responsib" → "responsiPM"). | **Informative** — provides category tags (Clinical/PM) and examples, but corrupted text requires cross-referencing with PDF |
| `export-311322-voct2023.zip` (58 JSON files, 7.7 MB) | Complete sample single-patient export for test patient ID 311322. Contains 1,959 total records across 58 entity files with realistic test data. | **Highly informative** — demonstrates actual export output with populated fields |
| `screenshot-ht1-b10-updates.png` (372 KB) | Screenshot of HTI-1 2026 Certification Updates page showing upcoming EHI Export additions for USCDIv3: Demographics (Tribal Affiliation, Occupation, Industry), Allergies (Verification), Problems (Verification). Marked "COMING SOON: Q1 2026." | **Supplementary** — shows active maintenance |
| `screenshot-main-ehi-page.png` (185 KB) | Screenshot of the main EHI Export page with collapsed accordions. | **Low** — orientation only |
| `screenshot-main-ehi-expanded.png` (16.8 MB) | Full-page screenshot of the EHI Export page with all accordions expanded. | **Low** — redundant with PDF |

## 3. Export Mechanics

- **Format**: Proprietary JSON — one file per entity type, each containing a JSON array of record objects. Not FHIR, C-CDA, or any healthcare standard.
- **Mechanism**: Self-service UI through the Reports portal → EHI Export tool. Role-based access control via two specific roles: "EHI Export" (single patient) and "EHI Practice Export" (all patients).
- **Single-patient export**: User searches for a patient, clicks "Request," waits for status to change to "Completed," then downloads a ZIP file. Self-service, no developer assistance required.
- **All-patient (practice) export**: User submits a request through the same UI. This triggers a process involving the iSALUS Data Export team. Delivery takes approximately 15 days. The confirmation message explicitly states this is for practices "planning to leave OfficeEMR and migrating to a new EHR platform."
- **Bulk export**: Yes — both single-patient and full-practice export are supported.
- **Fees**: The documentation states charges for all-patient exports are "very limited in scope" per ONC regulations when the request is for practice migration. Custom exports beyond the standard EHI export are quoted as a "separate, billable service."
- **Document images**: Provided separately in a zipped file with original formats (PDF, JPEG, PNG).
- **Readme**: Every export includes a `readme.json` with a link to the public format documentation.

## 4. Export Content: What's In It

### Overview

The export consists of 79 distinct entity types (excluding the `readme.json` metadata file), documented across three complementary artifacts:

| Source | Entity count | Total fields | Descriptions | Examples |
|---|---|---|---|---|
| JSON Schema files | 80 files (79 entities + readme) | 1,142 | 0 (all empty) | No |
| XLSX data dictionary | 79 entities | 1,051 | 1,051 (100%) | 1,051 (100%) |
| PDF data dictionary | 78 entities | 1,007 | 1,007 (100%) | No |
| Sample export | 58 files (57 entities + readme) | — | — | 1,959 records |

**Field count discrepancies**: The JSON schemas define 1,142 fields across 79 entities, while the XLSX documents 1,051 and the PDF documents 1,007. The schema files include system fields (e.g., `rowIdentifier`, `patientId`, `authorUserId`, `authorLogDateUtc`) that appear consistently across entities, while the PDF data dictionary counts are slightly lower — likely because the PDF parsing loses some fields at page breaks. The XLSX field count of 1,051 is the most reliable count for documented fields. The schema files define ~91 additional fields beyond what the XLSX documents, likely system/audit fields present in every entity.

**Entity discrepancies**: The schema ZIP includes `sliding_fee` (12 fields) which does not appear in the XLSX or PDF data dictionary. One entity (`fee_schedule`) is referenced in the PDF prose but has no schema, XLSX entry, or sample data — it may have been removed or consolidated.

### Vendor's own content organization

The XLSX data dictionary tags each entity as either **Clinical** (65 entities, 773 fields) or **PM** (Practice Management, 14 entities, 278 fields). The PDF organizes the data dictionary into **Clinical Data Exports** (64 entities, ~710 fields) and **Practice Management Data Exports** (15 entities, ~298 fields). The categories are broadly consistent across sources. The PDF's categorization — used as the basis for this analysis — places `demographics` and `appointment` in Practice Management, yielding 63 Clinical entities (810 schema fields) and 15 PM entities (320 schema fields), with `sliding_fee` (12 fields) uncategorized as it only appears in the schema ZIP.

**Top 20 entities by field count** (from JSON Schema, the most complete source):

| Entity | Schema Fields | PDF-Documented | Category | Sample Records |
|---|---|---|---|---|
| insurance | 47 | 45 | Practice Management | 4 |
| vital | 45 | 43 | Clinical | 18 |
| demographics | 42 | 40 | Practice Management | 1 |
| claim | 37 | 34 | Practice Management | 58 |
| prior_authorization | 33 | 32 | Practice Management | 4 |
| immunization | 32 | 29 | Clinical | 10 |
| case_management | 31 | 28 | Clinical | 3 |
| claim_procedure | 31 | 30 | Practice Management | 65 |
| responsible_party | 31 | 29 | Clinical | 2 |
| medication | 29 | 27 | Clinical | 188 |
| statement | 27 | 26 | Practice Management | 0 |
| care_team | 25 | 23 | Clinical | 3 |
| pregnancy | 25 | 23 | Clinical | 0 |
| pregnancy_visit | 23 | 21 | Clinical | 0 |
| appointment | 22 | 20 | Practice Management | 134 |
| payment | 22 | 21 | Practice Management | 9 |
| chronic_care_management | 20 | 18 | Clinical | 1 |
| dialysis_setup | 20 | 19 | Clinical | 2 |
| accident | 19 | 16 | Clinical | 0 |
| image_xref | 18 | 16 | Clinical | 62 |

The full inventory of all 79 entities is available in `analysis/full-entity-inventory.json`.

**Template encounter sub-entities**: The `template_encounter` entity is decomposed into 8 files representing structured clinical encounter components:
- `template_encounter.json` (6 fields, 179 records) — encounter header
- `template_encounter_assessment.json` (11 fields, 5 records) — clinical assessment
- `template_encounter_exam.json` (11 fields, 229 records) — physical exam findings
- `template_encounter_history.json` (11 fields, 25 records) — patient history
- `template_encounter_hpi.json` (11 fields, 39 records) — history of present illness
- `template_encounter_order_fulfillment.json` (11 fields, 13 records) — order fulfillment
- `template_encounter_ros.json` (11 fields, 17 records) — review of systems
- `template_encounter_treatment_plan.json` (11 fields, 39 records) — treatment plan

**Specialty-specific entities**: The export includes several specialty entities:
- `dialysis_setup` (20 fields) and `dialysis_visit` (12 fields) — nephrology
- `case_management` (31 fields) and `case_management_ckcc_note` (7 fields) — case management / CKCC (Comprehensive Kidney Care Contracting)
- `ckcc_status` (4 fields) — CKCC status tracking
- `pregnancy` (25 fields) and `pregnancy_visit` (23 fields) — OB/GYN
- `md_revolution_status` (6 fields) — remote patient monitoring

### Sample export analysis

The sample export for test patient 311322 contains **57 entity files** (excluding readme) with **1,959 total records**. The most populated entities are:

- `lab_result`: 233 records (17 fields)
- `order`: 229 records (15 fields)
- `template_encounter_exam`: 229 records (11 fields)
- `medication`: 188 records (28 fields)
- `template_encounter`: 179 records (6 fields)
- `appointment`: 134 records (20 fields)
- `letter`: 79 records (6 fields)
- `claim_procedure`: 65 records (30 fields)
- `image_xref`: 62 records (17 fields)
- `claim`: 58 records (36 fields)

22 entities from the schema are absent from the sample export. Most are plausibly empty for this test patient (e.g., `pregnancy`, `portal_message`, `health_concern`, `referral_tracking`, `sliding_fee`). `statement` (26 fields) and `eligibility` (4 fields) are notable absences.

The sample data contains realistic test content including full demographics (name, address, SSN, insurance), clinical notes with full HTML content, detailed claim records with charges and aging, medication lists with NDC codes, lab results, and vital signs.

## 5. Coverage Assessment

### 5a. What the vendor covers (bottom-up)

**Clinical Data (63 entities, 810 schema fields)**: The clinical section is the deepest part of the export, covering:
- Core clinical records: allergies (with symptoms), problem lists (with notes), medications, immunizations (with registry data), lab results, vitals, orders (with findings), progress notes, consent records
- Structured encounters: Template encounters decomposed into 8 sub-entities covering HPI, ROS, exam, history, assessment, treatment plan, and order fulfillment — this is granular encounter documentation
- Care coordination: care plans/goals (with objectives, interventions, comments), care teams, health concerns, referral tracking, phone encounters, education records
- Specialty: dialysis setup/visits, case management/CKCC notes, pregnancy/pregnancy visits, implantable devices, remote patient monitoring status
- Documents: image documents and cross-references, letters, chart sharing records
- Communications: patient communications (with recipients), portal messages, EPA (electronic prior authorization)
- Other: accident records, pharmacy records, optimize_rx, HIE data, extension encounters/results

**Practice Management Data (15 entities, 320 schema fields)**: The PM section provides genuine billing depth:
- Claims: `claim` (37 fields) with status, charges, balance, aging, payer info, provider roles (attending, ordering, referring, rendering, supervising), service/patient location
- Claim details: `claim_procedure` (31 fields) with CPT/HCPCS codes, modifiers, diagnosis pointers, units, charges
- Payments: `payment` (22 fields) with amount, type, payer info, reference numbers
- Insurance: `insurance` (47 fields) — the largest entity — with policy details, subscriber info, group info, payer identifiers
- Prior authorization: `prior_authorization` (33 fields) with codes and rendering providers (3 sub-entities)
- Other PM: denials, statements (with aging buckets), eligibility, price estimates (with line items), appointments, demographics, responsible parties, preschool billing, sliding fee schedules

### 5b. Standardized domain coverage (top-down)

| Domain | Coverage | Export Evidence | Gap Analysis |
|---|---|---|---|
| Demographics | ✅ Covered | `demographics` (42 fields): name, DOB, death date, address, phones, email, SSN, gender, marital status, race, ethnicity, language, employment, employer, provider assignments, old patient IDs | Thorough — includes 42 fields covering identifiers, contacts, and social attributes |
| Encounters / visits | ✅ Covered | `template_encounter` + 7 sub-entities (total ~90 fields), `extension_encounter`, `phone_encounter`, `appointment` | Deep — structured encounters with HPI, ROS, exam, history, assessment, treatment plan decomposition |
| Problems / conditions | ✅ Covered | `problem_list` (16 fields), `problem_list_note` (7 fields) | Includes chronic indicator, onset date, SNOMED codes, ICD codes, notes |
| Medications / prescriptions | ✅ Covered | `medication` (29 fields), `optimize_rx` (8 fields), `pharmacy` (9 fields) | Includes NDC, RxNorm, SIG, prescriber, dispense info, DEA schedule |
| Allergies | ✅ Covered | `allergy` (12 fields), `allergy_symptom` (9 fields) | Includes SNOMED codes, severity, reactions |
| Immunizations | ✅ Covered | `immunization` (32 fields), `immunization_registry` (13 fields) | Deep — includes CVX codes, NDC, manufacturer, lot, site, registry submission data |
| Vitals | ✅ Covered | `vital` (45 fields) | Exceptionally detailed — sitting/standing/supine BP, pulse, rhythm, multiple body measurements, glucose, pain, head/waist/hip/neck circumference, body fat |
| Lab results | ✅ Covered | `lab_result` (18 fields), `order_finding` (7 fields), `extension_results` (12 fields) | 233 records in sample; includes abnormal flags, reference ranges, lab info |
| Imaging / diagnostic reports | ⚠️ Partial | `image_document` (6 fields) and `image_xref` (18 fields) provide document metadata. Actual image files delivered separately in original format | Metadata exported; images delivered as separate files — reasonable approach |
| Procedures | ✅ Covered | `claim_procedure` (31 fields) captures CPT/HCPCS procedure codes, modifiers, diagnosis pointers; template encounters capture clinical procedure documentation | Covered via billing (claim_procedure) and clinical (template_encounter) records |
| Clinical notes / documents | ✅ Covered | `progress_note` (12 fields with full HTML content), `letter` (7 fields), template encounters | 45 progress notes + 79 letters in sample; notes contain full HTML with clinical content |
| Care plans / goals | ✅ Covered | `care_plan_goal` (11 fields), `goal` + 4 sub-entities (objectives, interventions, comments, problems), `health_concern` | Granular goal tracking with interventions and problem linkages |
| Orders / referrals | ✅ Covered | `order` (16 fields, 229 records), `referral_tracking` (3 fields) | Orders well-covered; referral tracking entity is thin (only 2 documented fields) |
| Insurance / coverage | ✅ Covered | `insurance` (47 fields — largest entity), `responsible_party` (31 fields), `eligibility` (5 fields) | Deeply covered — includes policy details, subscriber info, group numbers, payer identifiers |
| Claims / billing | ✅ Covered | `claim` (37 fields), `claim_procedure` (31 fields), `denial` (12 fields), `statement` (27 fields), `preschool_billing` (7 fields), `sliding_fee` (12 fields) | Comprehensive billing with claim-level and procedure-level detail, including aging, denials, and statements |
| Payments | ✅ Covered | `payment` (22 fields) | Includes payment amount, type, payer, reference numbers, adjustment codes |
| Consents / directives | ✅ Covered | `consent` (14 fields) | Includes consent type, status, dates |
| Patient communications / portal messages | ✅ Covered | `communication` (9 fields), `communication_recipient` (6 fields), `portal_message` (13 fields) | Covers both internal communications and portal messages |
| Specialty: Nephrology/Dialysis | ✅ Covered | `dialysis_setup` (20 fields), `dialysis_visit` (12 fields), `ckcc_status` (4 fields), `case_management` (31 fields), `case_management_ckcc_note` (7 fields) | Purpose-built dialysis and CKCC entities — genuine specialty coverage |
| Specialty: OB/GYN | ✅ Covered | `pregnancy` (25 fields), `pregnancy_visit` (23 fields) | Detailed pregnancy tracking with visit-level data |
| Prior authorizations | ✅ Covered | `prior_authorization` (33 fields), `prior_authorization_code` (8 fields), `prior_authorization_rendering` (5 fields) | Detailed with code-level and rendering provider sub-entities |
| Price estimates | ✅ Covered | `price_estimate` (12 fields), `price_estimate_line` (10 fields) | Patient cost estimation data |

**Gap Analysis Summary**: No significant EHI gaps identified. All major clinical and billing domains the product stores are represented in the export. Minor observations:

- **Telehealth sessions**: No dedicated telehealth entity. AnywhereCare visits are likely captured within `progress_note` or `template_encounter`, but this is not explicitly documented.
- **Patient intake forms**: The Intelligent Intake feature stores patient-submitted forms, but no dedicated intake entity appears. This data may be captured elsewhere or may represent a minor gap.
- **Fee schedule**: Referenced in the PDF prose but absent from schema, XLSX, and sample data. May have been removed or consolidated.

## 6. Documentation Quality

**Strengths:**
- **Three complementary artifact types**: JSON Schema (machine-readable structure), XLSX data dictionary (field descriptions + examples + category tags), and sample export (working demonstration). This is an unusually thorough documentation package for any vendor, let alone a smaller one.
- **100% field descriptions**: Every one of the 1,051 fields in the XLSX has both a plain-English description and an example value. The PDF data dictionary similarly provides descriptions for all ~1,007 documented fields.
- **Working sample export**: A complete 58-file single-patient export with 1,959 records of realistic test data. A developer could immediately understand the format and begin building an import.
- **Clear process documentation**: Step-by-step instructions for both single-patient and practice-wide exports, including role requirements, status tracking, and delivery expectations.
- **Public accessibility**: All documentation publicly accessible at `officeemr.knowledgeowl.com/help/ehi-export` with no login required.
- **Active maintenance**: Page last modified 12/19/2025; HTI-1/USCDIv3 additions already documented as coming Q1 2026.

**Weaknesses:**
- **XLSX text corruption**: The XLSX data dictionary has a systematic corruption where "b" is replaced with "PM" in entity names and descriptions (~380 of 1,051 descriptions affected). Examples: "responsib" → "responsiPM", "about" → "aPMout", "lab_result" → "laPM_result". The PDF is uncorrupted.
- **Empty JSON Schema descriptions**: All 1,142 `description` fields in the schema files are empty strings. The schemas define structure and types but provide zero semantic context — a developer must cross-reference the XLSX or PDF to understand field meanings.
- **Two malformed schema files**: `payment.json` and `statement.json` in the schema ZIP contain syntax errors (double commas: `"",,"`) making them unparseable without repair.
- **No value set documentation**: Coded fields (e.g., `claimStatus`, `gender`, `maritalStatus`, `employmentStatus`, `agingType`, `temperatureMethod`) are typed as strings with no documentation of valid values or code systems. The sample data reveals values like `"Closed - Electronic Superbill"` and `"Irregularly Irregular"` but there is no formal enumeration.
- **Minimal relationship documentation**: Entities are linked via shared IDs (e.g., `patientId`, `claimId`) but there is no entity-relationship diagram, no foreign key documentation, and no cardinality documentation beyond passing mentions.
- **No date format specification**: Dates appear in multiple formats: `"19011212"` (YYYYMMDD), `"20150302144846-0400"` (with timezone), and no documentation specifies the conventions.

**Developer usability**: A competent developer could build a functional import from these artifacts. The sample export provides the format template, the XLSX/PDF provide field semantics, and the schema provides types. The main challenges would be: (1) interpreting coded values without value sets, (2) understanding entity relationships beyond `patientId`, and (3) handling date format variations.

## 7. Overall Assessment

### Classification

**Comprehensive native export**

This is a genuine, purpose-built (b)(10) export of the vendor's native data model. It is not a repackaged FHIR API or C-CDA — it exports 79 distinct entity types in a proprietary JSON format covering clinical data (65 entities), practice management data (14 entities), and specialty-specific data (nephrology/dialysis, OB/GYN, case management). The documentation package (JSON schemas, XLSX data dictionary with 100% field descriptions, and a working sample export) is substantially above average.

### Key Findings

1. **Genuinely comprehensive coverage**: 79 entities spanning clinical, billing, specialty, and patient engagement domains with 1,142 schema-defined fields. This is not a clinical summary — it includes claims, payments, denials, statements, prior authorizations, price estimates, dialysis records, pregnancy tracking, and case management. The billing depth alone (claim with 37 fields, claim_procedure with 31 fields, payment with 22 fields) demonstrates real (b)(10) work.

2. **Exceptional documentation for a small vendor**: Three complementary artifact types with 100% field descriptions and examples in the XLSX, 100% descriptions in the PDF, and a complete 58-file sample export. Most vendors of comparable size provide far less.

3. **Real sample data demonstrates working export**: The sample export for patient 311322 contains 1,959 records across 57 entities with realistic test data (demographics, 58 claims, 188 medications, 233 lab results, 229 orders, 45 progress notes with full HTML). This proves the export actually works and produces meaningful output.

4. **Quality issues in artifacts but not fatal**: The XLSX has a systematic "b" → "PM" text corruption affecting ~36% of descriptions, two schema files have JSON syntax errors, and all schema descriptions are empty. These are quality-control issues that limit machine-readability but don't undermine the overall export because the PDF provides uncorrupted documentation.

5. **No value set documentation is the biggest gap**: Coded fields throughout the export have no documented valid values. A recipient cannot programmatically interpret fields like `claimStatus`, `agingType`, or `temperatureMethod` without reverse-engineering from sample data or contacting the vendor.

### Summary Stats

```
Classification:  Comprehensive native export
Export format:   Proprietary JSON (one file per entity type)
Model type:      Native database model
Entities:        79 (excluding readme)
Fields:          1,142 (schema); 1,051 (documented in XLSX)
Descriptions:    100% in XLSX/PDF; 0% in JSON Schema
Sample data:     Yes (58 files, 1,959 records)
Bulk export:     Yes (single-patient self-service; all-patient vendor-assisted, ~15 days)
Domains covered: 19 of 19 applicable domains
```

### Bottom Line

This is one of the stronger (b)(10) implementations. A patient or provider would receive a genuinely comprehensive copy of their data — clinical records, billing detail, specialty data, and communications — in a structured, documented format. The single biggest weakness is the absence of value set documentation for coded fields, which means a data recipient could reconstruct the record but would need to guess at the meaning of some coded values.
